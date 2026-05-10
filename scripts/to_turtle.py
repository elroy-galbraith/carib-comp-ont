#!/usr/bin/env python3
"""
to_turtle.py — Convert vault/*.md (Markdown+YAML) entities to Turtle RDF.

Usage:
    python scripts/to_turtle.py                     # writes vault/vault.ttl
    python scripts/to_turtle.py --out path/to.ttl   # custom output path
    python scripts/to_turtle.py --print             # print to stdout
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

# Pack-driven configuration. Refactored from hardcoded module-level constants
# in Phase A; future use cases swap to a different pack.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kgforge.pack import load_builtin  # noqa: E402

_PACK = load_builtin("compliance")

BASE_IRI = _PACK.base_iri
ENTITY_IRI = _PACK.entity_iri
SCHEMA_IRI = BASE_IRI

PREFIXES = f"""\
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix {_PACK.prefix}:  <{SCHEMA_IRI}> .
@prefix {_PACK.entity_prefix}: <{ENTITY_IRI}> .
"""

PROP_MAP = _PACK.property_map()


def _ttl_str(value: str) -> str:
    """Escape a string for Turtle triple-quoted literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _parse_frontmatter(path: Path) -> dict | None:
    """Return YAML frontmatter dict from a Markdown file, or None."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    return yaml.safe_load(m.group(1))


def _strip_wikilink(value) -> str:
    """Strip Obsidian wikilink brackets if present: '[[id]]' -> 'id'."""
    m = re.match(r"^\[\[(.+?)\]\]$", str(value).strip())
    return m.group(1) if m else str(value).strip()


def entity_to_triples(meta: dict) -> list[str]:
    eid = meta.get("id", "")
    if not eid:
        return []

    cls = meta.get("class", "")
    label = meta.get("label", eid)
    source_text = meta.get("source_text", "")
    source_section = meta.get("source_section", "")
    properties = meta.get("properties", {}) or {}

    subject = f"{_PACK.entity_prefix}:{eid}"
    lines: list[str] = [f"{subject}"]

    # rdf:type — known classes get the pack's prefix; unknown defaults to the
    # pack's first class (legacy: this branch never fires for the compliance
    # vault, but is kept so renamed/typo'd classes degrade gracefully).
    if cls in _PACK.class_names:
        lines.append(f"    a {_PACK.prefix}:{cls} ;")
    else:
        fallback = _PACK.class_names[0]
        lines.append(f'    a {_PACK.prefix}:{fallback} ;  # unknown class "{cls}" — defaulted')

    # rdfs:label
    lines.append(f'    rdfs:label "{_ttl_str(label)}"@en ;')

    # skos:definition from source_text
    if source_text:
        clean = source_text.strip().replace("\n", " ")
        lines.append(f'    skos:definition """{_ttl_str(clean)}"""@en ;')

    # dcterms:source — section reference
    if source_section:
        lines.append(f'    dcterms:source "{_ttl_str(source_section)}" ;')

    # ontology properties (entries with explicit `iri:` in the pack — e.g.
    # partOfStatute → dcterms:isPartOf — are honoured here).
    for prop_key, prop_iri in PROP_MAP.items():
        value = properties.get(prop_key)
        if value:
            target = _strip_wikilink(value)
            if target == eid:
                continue  # skip self-references
            lines.append(f"    {prop_iri} {_PACK.entity_prefix}:{target} ;")

    # close the triple set
    last = lines[-1]
    lines[-1] = last.rstrip(" ;") + " ."
    lines.append("")

    return lines


def build_turtle(vault_dir: Path) -> str:
    parts = [PREFIXES, ""]
    md_files = sorted(vault_dir.glob("*.md"))
    if not md_files:
        print("[to_turtle] WARNING: no .md files found in vault/", file=sys.stderr)
    for path in md_files:
        meta = _parse_frontmatter(path)
        if meta is None:
            print(f"[to_turtle] SKIP {path.name}: no YAML frontmatter", file=sys.stderr)
            continue
        triples = entity_to_triples(meta)
        if triples:
            parts.extend(triples)
        else:
            print(f"[to_turtle] SKIP {path.name}: missing 'id' field", file=sys.stderr)
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert vault/*.md to Turtle RDF.")
    parser.add_argument("--vault", default="vault", help="Vault directory (default: vault)")
    parser.add_argument("--out", default=None, help="Output .ttl path (default: vault/vault.ttl)")
    parser.add_argument("--print", dest="print_only", action="store_true",
                        help="Print to stdout instead of writing a file")
    args = parser.parse_args()

    vault_dir = Path(args.vault)
    if not vault_dir.is_dir():
        print(f"[to_turtle] ERROR: vault directory not found: {vault_dir}", file=sys.stderr)
        sys.exit(1)

    turtle = build_turtle(vault_dir)

    if args.print_only:
        print(turtle)
    else:
        out_path = Path(args.out) if args.out else vault_dir / "vault.ttl"
        out_path.write_text(turtle, encoding="utf-8")
        print(f"[to_turtle] wrote {out_path} ({len(turtle)} bytes)")


if __name__ == "__main__":
    main()
