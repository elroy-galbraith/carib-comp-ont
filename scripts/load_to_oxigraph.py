#!/usr/bin/env python3
"""
load_to_oxigraph.py — Load schema + vault Turtle into an in-memory Oxigraph store
and run SPARQL competency queries.

Usage:
    # Run all three competency queries
    python scripts/load_to_oxigraph.py

    # Run a specific .rq file
    python scripts/load_to_oxigraph.py --query sparql/cq1_obligations_on_controller.rq

    # Build the vault TTL first, then load
    python scripts/load_to_oxigraph.py --build-vault

Dependencies:
    pip install pyoxigraph PyYAML
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    import pyoxigraph
except ImportError:
    print("ERROR: pyoxigraph not installed. Run: pip install pyoxigraph", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
SCHEMA_TTL = REPO_ROOT / "schema" / "carib_compliance.ttl"
VAULT_TTL  = REPO_ROOT / "vault" / "vault.ttl"
SPARQL_DIR = REPO_ROOT / "sparql"

COMPETENCY_QUERIES = [
    ("CQ1 — Obligations on DataController", SPARQL_DIR / "cq1_obligations_on_controller.rq"),
    ("CQ2 — Regulators and statutes",       SPARQL_DIR / "cq2_regulators.rq"),
    ("CQ3 — Definitions in DPA 2020",       SPARQL_DIR / "cq3_definitions.rq"),
]


def build_vault_ttl() -> None:
    print("[load] Building vault/vault.ttl from vault/*.md …")
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "to_turtle.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    print(result.stdout.strip())


def load_store() -> pyoxigraph.Store:
    store = pyoxigraph.Store()

    for ttl_path in (SCHEMA_TTL, VAULT_TTL):
        if not ttl_path.exists():
            print(f"[load] WARNING: {ttl_path} not found — skipping", file=sys.stderr)
            continue
        data = ttl_path.read_bytes()
        store.load(data, "text/turtle", base_iri=str(ttl_path.as_uri()))
        print(f"[load] loaded {ttl_path.name} ({len(data)} bytes, "
              f"{sum(1 for _ in store)} triples total)")

    return store


def run_query(store: pyoxigraph.Store, sparql: str, title: str) -> None:
    print(f"\n{'═'*60}")
    print(f"  {title}")
    print(f"{'═'*60}")

    results = store.query(sparql)

    if isinstance(results, pyoxigraph.QuerySolutions):
        variables = results.variables
        rows = list(results)
        if not rows:
            print("  (no results)")
            return
        # column widths
        widths = [len(str(v)) for v in variables]
        str_rows = []
        for row in rows:
            sr = [str(row[v]) if row[v] is not None else "" for v in variables]
            for i, cell in enumerate(sr):
                widths[i] = max(widths[i], len(cell))
            str_rows.append(sr)
        # header
        header = "  " + "  ".join(str(v).ljust(widths[i]) for i, v in enumerate(variables))
        sep    = "  " + "  ".join("-" * w for w in widths)
        print(header)
        print(sep)
        for sr in str_rows:
            print("  " + "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(sr)))
        print(f"\n  {len(str_rows)} row(s)")
    elif isinstance(results, bool):
        print(f"  ASK → {results}")
    else:
        # CONSTRUCT / DESCRIBE
        triples = list(results)
        for t in triples:
            print(f"  {t}")
        print(f"\n  {len(triples)} triple(s)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load vault into Oxigraph and run SPARQL.")
    parser.add_argument("--build-vault", action="store_true",
                        help="Run to_turtle.py first to regenerate vault/vault.ttl")
    parser.add_argument("--query", metavar="FILE",
                        help="Run a single .rq file instead of all three CQs")
    args = parser.parse_args()

    if args.build_vault:
        build_vault_ttl()

    store = load_store()

    if args.query:
        qpath = Path(args.query)
        sparql = qpath.read_text(encoding="utf-8")
        run_query(store, sparql, qpath.name)
    else:
        for title, qpath in COMPETENCY_QUERIES:
            if not qpath.exists():
                print(f"[load] WARNING: query file not found: {qpath}", file=sys.stderr)
                continue
            sparql = qpath.read_text(encoding="utf-8")
            run_query(store, sparql, title)

    print(f"\n[load] done. Store contains {sum(1 for _ in store)} triples total.\n")


if __name__ == "__main__":
    main()
