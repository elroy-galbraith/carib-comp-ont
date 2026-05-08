#!/usr/bin/env python3
"""
curator.py — Minimal curator-agent loop.

Watches inbox/ for new PDF files. On each new PDF:
  1. Runs extractor.py to produce Markdown+YAML vault files.
  2. Creates a git branch  proposals/<doc-id>
  3. Commits all new/changed vault files with a structured commit message.
  4. Prints a summary (branch name, files committed, model used).

The user then reviews the PR via:
    git log proposals/<doc-id>
    git diff main...proposals/<doc-id>
    git checkout main && git merge proposals/<doc-id>

Usage:
    python scripts/curator.py               # watch inbox/, loop forever
    python scripts/curator.py --once        # process existing inbox files then exit
    python scripts/curator.py --inbox path  # custom inbox directory

Dependencies:
    pip install watchdog gitpython anthropic PyYAML
"""
from __future__ import annotations

import argparse
import logging
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import git
except ImportError:
    print("ERROR: gitpython not installed. Run: pip install gitpython", file=sys.stderr)
    sys.exit(1)

try:
    from watchdog.events import FileCreatedEvent, FileSystemEventHandler
    from watchdog.observers import Observer
except ImportError:
    print("ERROR: watchdog not installed. Run: pip install watchdog", file=sys.stderr)
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [curator] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("curator")

REPO_ROOT  = Path(__file__).parent.parent
VAULT_DIR  = REPO_ROOT / "vault"
INBOX_DIR  = REPO_ROOT / "inbox"
EXTRACTOR  = REPO_ROOT / "scripts" / "extractor.py"
DONE_DIR   = REPO_ROOT / "inbox" / "processed"
PROMPT_VER = "extractor-v1"
MODEL      = "claude-haiku-4-5-20251001"


# ── Core pipeline ─────────────────────────────────────────────────────────────

def doc_id_from_path(pdf_path: Path) -> str:
    stem = pdf_path.stem.lower()
    return stem.replace("-", "_").replace(" ", "_")


def run_extractor(pdf_path: Path, doc_id: str) -> list[Path]:
    """Run extractor.py and return list of new vault files."""
    cmd = [
        sys.executable, str(EXTRACTOR),
        str(pdf_path),
        "--doc-id", doc_id,
        "--vault", str(VAULT_DIR),
        "--prompt-version", PROMPT_VER,
    ]
    log.info("running extractor: %s", " ".join(cmd))
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if result.stdout:
        for line in result.stdout.strip().splitlines():
            log.info("  extractor: %s", line)
    if result.stderr:
        for line in result.stderr.strip().splitlines():
            log.info("  extractor: %s", line)
    if result.returncode != 0:
        raise RuntimeError(f"extractor.py exited {result.returncode}")

    # Collect files written (named <doc_id>_*.md)
    written = sorted(VAULT_DIR.glob(f"{doc_id}*.md"))
    return written


def open_proposal_branch(repo: git.Repo, doc_id: str) -> str:
    branch_name = f"proposals/{doc_id}"
    # Switch to main (or master) first
    try:
        repo.git.checkout("main")
    except git.GitCommandError:
        try:
            repo.git.checkout("master")
        except git.GitCommandError:
            pass  # may be on initial commit with no branches yet

    # Create or reset the proposals branch
    if branch_name in [b.name for b in repo.branches]:
        log.info("branch %s already exists — resetting to HEAD", branch_name)
        repo.git.branch("-D", branch_name)
    repo.git.checkout("-b", branch_name)
    log.info("created branch %s", branch_name)
    return branch_name


def commit_vault_files(repo: git.Repo, vault_files: list[Path],
                       doc_id: str, pdf_path: Path) -> str:
    if not vault_files:
        raise RuntimeError("no vault files to commit")

    # Stage vault files (paths relative to repo root)
    rel_paths = [str(f.relative_to(REPO_ROOT)) for f in vault_files]
    repo.index.add(rel_paths)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entity_count = len(vault_files)
    commit_msg = (
        f"curator: extract {doc_id} [{entity_count} entities]\n\n"
        f"source:         {pdf_path.name}\n"
        f"prompt_version: {PROMPT_VER}\n"
        f"model_snapshot: {MODEL}\n"
        f"timestamp:      {timestamp}\n"
        f"validation:     PENDING — review before merging\n\n"
        f"Files:\n" + "\n".join(f"  {p}" for p in rel_paths)
    )
    repo.index.commit(commit_msg)
    log.info("committed %d file(s) with message: %s", entity_count, commit_msg.splitlines()[0])
    return commit_msg


def archive_pdf(pdf_path: Path) -> None:
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    dest = DONE_DIR / pdf_path.name
    shutil.move(str(pdf_path), dest)
    log.info("archived %s → %s", pdf_path.name, dest)


def process_pdf(pdf_path: Path) -> None:
    log.info("═" * 50)
    log.info("processing: %s", pdf_path.name)

    doc_id = doc_id_from_path(pdf_path)
    repo = git.Repo(REPO_ROOT)

    branch_name = open_proposal_branch(repo, doc_id)
    try:
        vault_files = run_extractor(pdf_path, doc_id)
        if not vault_files:
            log.warning("extractor produced no vault files for %s", doc_id)
            return
        commit_vault_files(repo, vault_files, doc_id, pdf_path)
        archive_pdf(pdf_path)

        log.info("═" * 50)
        log.info("PROPOSAL READY")
        log.info("  branch:  %s", branch_name)
        log.info("  files:   %d", len(vault_files))
        log.info("  review:  git log %s", branch_name)
        log.info("  diff:    git diff main...%s", branch_name)
        log.info("  merge:   git checkout main && git merge %s", branch_name)
        log.info("═" * 50)

    except Exception as exc:
        log.error("pipeline failed for %s: %s", pdf_path.name, exc)
        # Return to main so inbox isn't stuck
        try:
            repo.git.checkout("main")
        except Exception:
            pass
        raise


# ── Watchdog handler ──────────────────────────────────────────────────────────

class InboxHandler(FileSystemEventHandler):
    def on_created(self, event: FileCreatedEvent) -> None:  # type: ignore[override]
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() == ".pdf":
            # Brief wait to ensure the file is fully written
            time.sleep(1.0)
            try:
                process_pdf(path)
            except Exception as exc:
                log.error("unhandled error: %s", exc)


# ── CLI ───────────────────────────────────────────────────────────────────────

def process_existing(inbox_dir: Path) -> None:
    pdfs = sorted(inbox_dir.glob("*.pdf"))
    if not pdfs:
        log.info("no PDF files found in %s", inbox_dir)
        return
    for pdf in pdfs:
        try:
            process_pdf(pdf)
        except Exception as exc:
            log.error("failed: %s — %s", pdf.name, exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Curator-agent: watch inbox for PDFs.")
    parser.add_argument("--inbox", default=str(INBOX_DIR), help="Inbox directory to watch.")
    parser.add_argument("--once",  action="store_true",
                        help="Process existing inbox files then exit (no watch loop).")
    args = parser.parse_args()

    inbox_dir = Path(args.inbox)
    inbox_dir.mkdir(parents=True, exist_ok=True)

    # Ensure we're in a git repo
    try:
        git.Repo(REPO_ROOT)
    except git.InvalidGitRepositoryError:
        log.error("Not a git repository: %s", REPO_ROOT)
        log.error("Run: git init && git add . && git commit -m 'init'")
        sys.exit(1)

    # Process any PDFs already in the inbox
    process_existing(inbox_dir)

    if args.once:
        return

    log.info("watching %s for new PDFs … (Ctrl-C to stop)", inbox_dir)
    handler  = InboxHandler()
    observer = Observer()
    observer.schedule(handler, str(inbox_dir), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    log.info("curator stopped.")


if __name__ == "__main__":
    main()
