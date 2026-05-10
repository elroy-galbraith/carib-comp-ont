#!/usr/bin/env python3
"""
highlight.py — Inject yellow highlight annotations into a source PDF at the
location of each vault entity's source_text. Idempotent: previous highlights
tagged with our marker are cleared before re-injecting.

Pipeline: vault/<doc_id>_*.md → read source_page + source_text →
          fitz.search_for() on that page → page.add_highlight_annot()

Usage:
    python scripts/highlight.py vault/sources/dpa_2020_s6.pdf
    python scripts/highlight.py --doc-id dpa_2020_s6
    python scripts/highlight.py vault/sources/dpa_2020_s6.pdf --vault vault/

Run after extraction (or via curator.py) so the PDF the user clicks through to
already shows the relevant passage highlighted.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: pymupdf not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
DEFAULT_VAULT = REPO_ROOT / "vault"

# Pack-driven configuration. The legal-definition term-name regex below stays
# in place for Phase A; in Phase B it moves to the compliance pack's hooks.py.
sys.path.insert(0, str(REPO_ROOT))
from kgforge.pack import load_builtin  # noqa: E402

_PACK = load_builtin("compliance")

# Tag we set on every annotation we create — used for idempotent re-runs.
ANNOT_TITLE = f"{_PACK.prefix}:provenance"
# Soft yellow (RGB 0-1) for the highlight stroke.
HIGHLIGHT_COLOR = (1.0, 0.95, 0.4)


def _clear_existing_highlights(doc: "fitz.Document") -> int:
    """Remove highlights previously created by this script (idempotency)."""
    removed = 0
    for page in doc:
        targets = []
        for annot in page.annots() or []:
            try:
                if (annot.info or {}).get("title") == ANNOT_TITLE:
                    targets.append(annot)
            except Exception:
                continue
        for annot in targets:
            page.delete_annot(annot)
            removed += 1
    return removed


_TERM_NAME_RE = re.compile(
    r"^\s*['\"`‘“]+([^'\"`’”]+?)['\"`’”]+(?=\s*(?:,|means\b|is\b|shall\b|\Z))",
    re.IGNORECASE,
)


def _extract_term_name(source_text: str) -> str | None:
    """Pull the quoted term from a statutory definition: 'biometric data' → biometric data."""
    if not source_text:
        return None
    m = _TERM_NAME_RE.match(source_text.strip())
    return m.group(1).strip() if m else None


def _search_variants(source_text: str) -> list[str]:
    """Generate needles for PyMuPDF.search_for, prioritising the short
    quoted term name (most distinctive and unlikely to wrap a line break),
    falling back to longer prefix snippets.
    """
    if not source_text:
        return []
    full = source_text.strip()
    variants: list[str] = []

    term = _extract_term_name(full)
    if term:
        # Try quoted variants first — they're most specific to the definition line.
        variants.extend([f"'{term}'", f'"{term}"', f"‘{term}’", f"“{term}”"])
        # Then the bare term name.
        variants.append(term)

    # Final fallback: longer prefixes (rarely match due to line wrapping, but cheap).
    no_quotes = re.sub(r"[‘’“”`'\"]+", "", full)
    for length in (50, 30):
        v = no_quotes[:length].strip()
        if len(v) >= 15:
            variants.append(v)

    # Dedupe, preserve order
    seen, out = set(), []
    for v in variants:
        if v and v not in seen:
            seen.add(v)
            out.append(v)
    return out


def _find_rects(page: "fitz.Page", source_text: str) -> list["fitz.Rect"]:
    """Try multiple needle variants until one returns a non-empty rect list."""
    for needle in _search_variants(source_text):
        rects = page.search_for(needle)
        if rects:
            return rects
    return []


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _collect_entities(vault_dir: Path, doc_id: str) -> list[dict]:
    """Read all vault/*.md whose source_document == doc_id and have a source_page."""
    entities = []
    for path in sorted(vault_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(text)
        if not m:
            continue
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        if meta.get("source_document") != doc_id:
            continue
        page = meta.get("source_page")
        src = meta.get("source_text")
        if not page or not src:
            continue
        entities.append({
            "file": path.name,
            "eid": meta.get("id", path.stem),
            "label": meta.get("label", path.stem),
            "page": int(page),
            "source_text": src,
        })
    return entities


def highlight_pdf(pdf_path: Path, vault_dir: Path, doc_id: str) -> tuple[int, int]:
    """Generate one highlighted PDF per vault entity for doc_id.

    The pristine source PDF at `pdf_path` is kept clean (any prior provenance
    highlights are cleared). For each entity, a copy is written alongside as
    `<entity_id>.pdf` with exactly one yellow highlight at the matched location.
    Vault notes' Source links point at these per-entity PDFs so clicking only
    surfaces the highlight relevant to the entity that was clicked.

    Returns (matched_count, unmatched_count).
    """
    # Restore source to pristine state — clear any of our prior highlights.
    src = fitz.open(pdf_path)
    cleared = _clear_existing_highlights(src)
    if cleared:
        print(f"[highlight] cleared {cleared} prior cco:provenance annotations on source", file=sys.stderr)
    src.save(pdf_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    pristine_bytes = src.write()
    src.close()

    entities = _collect_entities(vault_dir, doc_id)
    if not entities:
        print(f"[highlight] no entities found for doc_id={doc_id} in {vault_dir}", file=sys.stderr)
        return 0, 0

    # Clean up stale per-entity PDFs (idempotent re-runs).
    # Glob `{doc_id}_*.pdf` only matches per-entity files, never the pristine `{doc_id}.pdf`.
    for stale in pdf_path.parent.glob(f"{doc_id}_*.pdf"):
        stale.unlink()

    matched = 0
    unmatched = 0
    for entity in entities:
        out_path = pdf_path.parent / f"{entity['eid']}.pdf"
        out_path.write_bytes(pristine_bytes)
        doc = fitz.open(out_path)
        page = doc[entity["page"] - 1]
        rects = _find_rects(page, entity["source_text"])
        if not rects:
            doc.close()
            out_path.unlink()
            print(f"  no rect match: {entity['file']} (page {entity['page']})")
            unmatched += 1
            continue
        annot = page.add_highlight_annot(rects)
        annot.set_colors(stroke=HIGHLIGHT_COLOR)
        annot.set_info(title=ANNOT_TITLE, content=entity["label"], subject=entity["file"])
        annot.update()
        doc.save(out_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
        doc.close()
        matched += 1
        print(f"  wrote {out_path.name} (page {entity['page']}, {len(rects)} rect{'s' if len(rects)!=1 else ''})")

    return matched, unmatched


def main() -> None:
    parser = argparse.ArgumentParser(description="Inject highlight annotations into a vault source PDF.")
    parser.add_argument("pdf", nargs="?", help="Path to the PDF (default: vault/sources/<doc-id>.pdf).")
    parser.add_argument("--doc-id", default=None, help="Document ID (default: PDF stem).")
    parser.add_argument("--vault", default=str(DEFAULT_VAULT), help="Vault directory.")
    args = parser.parse_args()

    if args.pdf:
        pdf_path = Path(args.pdf)
    elif args.doc_id:
        pdf_path = REPO_ROOT / "vault" / "sources" / f"{args.doc_id}.pdf"
    else:
        parser.error("must provide either a PDF path or --doc-id")

    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    doc_id = args.doc_id or pdf_path.stem.lower().replace("-", "_").replace(" ", "_")
    vault_dir = Path(args.vault)

    matched, unmatched = highlight_pdf(pdf_path, vault_dir, doc_id)
    print(f"[highlight] matched {matched}, unmatched {unmatched} -> {pdf_path}")


if __name__ == "__main__":
    main()
