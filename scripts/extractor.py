#!/usr/bin/env python3
"""
extractor.py — Single-shot LLM entity extractor.

Pipeline: PDF path → text extraction (Docling or pdfplumber fallback)
          → Claude Haiku (JSON Schema tool use) → Markdown+YAML vault files.

Usage:
    python scripts/extractor.py path/to/statute.pdf
    python scripts/extractor.py path/to/statute.pdf --vault vault/ --doc-id dpa2020_s3
    python scripts/extractor.py --text "Section 6 ..." --doc-id dpa2020_s6  # raw text mode

Environment:
    ANTHROPIC_API_KEY  — required for Haiku calls.
                         Set in your shell or in a .env file at the repo root
                         (copy .env.example → .env and fill in the key).

Dependencies:
    pip install anthropic PyYAML python-dotenv
    pip install docling          # preferred PDF extractor
    pip install pdfplumber       # fallback PDF extractor
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from textwrap import dedent

import yaml

# Load .env from repo root (no-op if file absent or python-dotenv not installed)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env", override=True)
except ImportError:
    pass

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic not installed. Run: pip install anthropic", file=sys.stderr)
    sys.exit(1)

VAULT_DIR = Path(__file__).parent.parent / "vault"
MODEL = "claude-haiku-4-5-20251001"
# Relative path (from a vault/*.md file) to the directory holding source PDFs.
# Must resolve inside the Obsidian vault so clicking the link opens the PDF
# in Obsidian's built-in viewer at the given #page=N anchor.
PDF_LINK_BASE = "sources"

# ── JSON Schema that mirrors the OWL class structure ─────────────────────────

ENTITY_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "entities": {
            "type": "array",
            "description": "All legal entities extracted from the text.",
            "items": {
                "type": "object",
                "properties": {
                    "class": {
                        "type": "string",
                        "enum": ["Statute", "Provision", "Definition", "Regulator", "Obligation"],
                        "description": "OWL class this entity belongs to."
                    },
                    "id": {
                        "type": "string",
                        "pattern": "^[a-z][a-z0-9_]*$",
                        "description": "Snake-case identifier, prefixed with doc_id."
                    },
                    "label": {
                        "type": "string",
                        "description": "Human-readable name."
                    },
                    "source_section": {
                        "type": "string",
                        "description": "Section reference, e.g. §6 or §2(1)(a)."
                    },
                    "source_text": {
                        "type": "string",
                        "description": "Verbatim statutory text being encoded (max ~300 chars)."
                    },
                    "properties": {
                        "type": "object",
                        "description": "Ontology property values (entity IDs, not labels).",
                        "properties": {
                            "definedIn":           {"type": "string"},
                            "enforcedBy":          {"type": "string"},
                            "imposesObligationOn": {"type": "string"},
                            "applicableTo":        {"type": "string"},
                            "relatedTo":           {"type": "string"},
                        },
                        "additionalProperties": False
                    }
                },
                "required": ["class", "id", "label", "source_section", "source_text"],
                "additionalProperties": False
            }
        }
    },
    "required": ["entities"],
    "additionalProperties": False
}

FEW_SHOT = dedent("""\
    EXAMPLE INPUT (§2 of a data-protection statute):
    "data controller" means a person who determines the purposes for which
    and the manner in which any personal data are processed.

    EXAMPLE OUTPUT:
    {
      "entities": [
        {
          "class": "Definition",
          "id": "dpa2020_s2_data_controller",
          "label": "Data Controller",
          "source_section": "§2",
          "source_text": "\\"data controller\\" means a person who determines the purposes for which and the manner in which any personal data are processed.",
          "properties": { "definedIn": "dpa2020_s2" }
        }
      ]
    }
    ---
""")


# ── Text extraction ───────────────────────────────────────────────────────────

def extract_text_docling(pdf_path: Path) -> tuple[str, dict[int, str]]:
    """Returns (flat_markdown_for_llm, {page_no: page_text}) using docling.

    The page map enables clickable "page N" provenance links.
    """
    from docling.document_converter import DocumentConverter  # type: ignore
    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    doc = result.document
    pages: dict[int, list[str]] = {}
    for item, _level in doc.iterate_items():
        text = (getattr(item, "text", "") or "").strip()
        if not text:
            continue
        prov = getattr(item, "prov", None)
        if not prov:
            continue
        page_no = prov[0].page_no
        pages.setdefault(page_no, []).append(text)
    page_texts = {p: "\n".join(parts) for p, parts in pages.items()}
    flat = doc.export_to_markdown()
    return flat, page_texts


def extract_text_pdfplumber(pdf_path: Path) -> tuple[str, dict[int, str]]:
    """Returns (flat_text, {page_no: page_text}) using pdfplumber."""
    import pdfplumber  # type: ignore
    page_texts: dict[int, str] = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                page_texts[i] = text
    flat = "\n\n".join(page_texts[p] for p in sorted(page_texts))
    return flat, page_texts


def extract_text(pdf_path: Path) -> tuple[str, dict[int, str]]:
    try:
        flat, pages = extract_text_docling(pdf_path)
        print(f"[extractor] text extracted via docling ({len(flat)} chars, {len(pages)} pages)", file=sys.stderr)
        return flat, pages
    except ImportError:
        pass
    except Exception as e:
        print(f"[extractor] docling failed ({e}), trying pdfplumber…", file=sys.stderr)

    try:
        flat, pages = extract_text_pdfplumber(pdf_path)
        print(f"[extractor] text extracted via pdfplumber ({len(flat)} chars, {len(pages)} pages)", file=sys.stderr)
        return flat, pages
    except ImportError:
        pass

    print("ERROR: no PDF extractor available. Install docling or pdfplumber.", file=sys.stderr)
    sys.exit(1)


def _normalize_for_match(text: str) -> str:
    """Lowercase, collapse whitespace, and strip quote characters and punctuation
    that commonly differ between PDF OCR output and statutory text snippets."""
    text = text.lower()
    # Map curly/typographic quotes to nothing — robust to OCR variation
    text = re.sub(r"[‘’“”`'\"]+", "", text)
    # Collapse all whitespace and most punctuation
    text = re.sub(r"[\s\-–—.,;:()]+", " ", text)
    return text.strip()


def find_page_for_text(source_text: str, page_texts: dict[int, str]) -> int | None:
    """Locate which PDF page a source_text snippet came from.

    Two-stage match:
    1. Try exact substring of the first 80 / 60 normalized chars on each page.
    2. Fall back to longest-consecutive-word-overlap scoring — disambiguates
       TOC references (which only repeat the term name) from the actual
       definition body (which continues with definitional language).
    """
    if not source_text or not page_texts:
        return None
    needle_full = _normalize_for_match(source_text)
    needle_words = needle_full.split()
    if len(needle_words) < 5:
        return None
    normalized_pages = {p: _normalize_for_match(t) for p, t in page_texts.items()}

    # Stage 1: exact substring on a long-enough prefix
    for length in (80, 60):
        needle = needle_full[:length]
        for page_no in sorted(normalized_pages):
            if needle in normalized_pages[page_no]:
                return page_no

    # Stage 2: longest-n-gram-prefix score (5..15 words). Picks the page where
    # the most consecutive prefix-words of the source text appear together.
    best_page, best_score = None, 0
    for page_no in sorted(normalized_pages):
        haystack = normalized_pages[page_no]
        for n in range(min(15, len(needle_words)), 4, -1):
            chunk = " ".join(needle_words[:n])
            if chunk in haystack:
                if n > best_score:
                    best_score = n
                    best_page = page_no
                break
    return best_page


# ── Haiku API call ────────────────────────────────────────────────────────────

def call_haiku(text: str, doc_id: str, prompt_version: str) -> list[dict]:
    client = anthropic.Anthropic()

    system = dedent(f"""\
        You are a legal knowledge-engineering assistant. Extract ontology entities
        from Caribbean statutory text. Use only the five OWL classes:
        Statute, Provision, Definition, Regulator, Obligation.
        Always prefix entity IDs with the document ID ({doc_id}_).
        Be conservative: only extract entities explicitly stated in the text.
    """)

    user = dedent(f"""\
        {FEW_SHOT}
        Document ID: {doc_id}
        Prompt version: {prompt_version}

        Extract all ontology entities from the following statutory text.
        Use the extract_entities tool.

        ---
        {text[:8000]}
        ---
    """)

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=system,
        tools=[{
            "name": "extract_entities",
            "description": "Extract legal ontology entities from statutory text.",
            "input_schema": ENTITY_SCHEMA,
        }],
        tool_choice={"type": "tool", "name": "extract_entities"},
        messages=[{"role": "user", "content": user}],
    )

    for block in response.content:
        if block.type == "tool_use":
            return block.input.get("entities", [])
    return []


# ── Vault file writer ─────────────────────────────────────────────────────────

def entity_to_markdown(entity: dict, doc_id: str, prompt_version: str, model_snapshot: str) -> str:
    eid = entity["id"]
    label = entity["label"]
    cls = entity["class"]
    source_section = entity.get("source_section", "")
    source_text = entity.get("source_text", "")
    source_page = entity.get("source_page")
    raw_properties = entity.get("properties") or {}
    # Wrap property values in Obsidian wikilink syntax so Properties become graph edges.
    # to_turtle.py strips the brackets when emitting RDF.
    properties = {
        k: (v if (isinstance(v, str) and v.startswith("[[")) else f"[[{v}]]")
        for k, v in raw_properties.items() if v
    }

    meta = {
        "class":           cls,
        "id":              eid,
        "label":           label,
        "uri":             f"https://ontology.carib-comp.org/compliance/entity/{eid}",
        "source_document": doc_id,
        "source_section":  source_section,
        "source_page":     source_page,
        "source_text":     source_text,
        "properties":      properties,
        "prompt_version":  prompt_version,
        "model_snapshot":  model_snapshot,
        "validation":      "PENDING",
    }
    if source_page is None:
        meta.pop("source_page")

    frontmatter = yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False)

    if source_page:
        # Per-entity PDF: one highlighted passage per file so the reader sees
        # only the relevant snippet, not every entity's highlight on the page.
        source_line = (
            f"**Source:** [{source_section} — page {source_page}]"
            f"({PDF_LINK_BASE}/{eid}.pdf#page={source_page})"
        )
    else:
        source_line = f"**Source:** {source_section} — {doc_id}"

    body = dedent(f"""\
        ## {label}

        **Class:** `cco:{cls}`
        {source_line}

        > {source_text}

        *Auto-extracted by extractor.py. Review before merging.*
    """)

    return f"---\n{frontmatter}---\n\n{body}"


def write_vault_files(entities: list[dict], vault_dir: Path,
                      doc_id: str, prompt_version: str, model_snapshot: str) -> list[Path]:
    vault_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for entity in entities:
        eid = entity.get("id")
        if not eid:
            continue
        # sanitise id to safe filename
        safe = re.sub(r"[^a-z0-9_]", "_", eid.lower())
        out_path = vault_dir / f"{safe}.md"
        content = entity_to_markdown(entity, doc_id, prompt_version, model_snapshot)
        out_path.write_text(content, encoding="utf-8")
        written.append(out_path)
        print(f"[extractor] wrote {out_path.name}")
    return written


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Extract legal entities from a PDF or text.")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("pdf", nargs="?", help="Path to a PDF file.")
    src.add_argument("--text", metavar="TEXT", help="Raw statutory text (instead of PDF).")
    parser.add_argument("--doc-id",  default=None,
                        help="Document identifier prefix (default: PDF stem).")
    parser.add_argument("--vault",   default=str(VAULT_DIR),
                        help="Output vault directory.")
    parser.add_argument("--prompt-version", default="extractor-v1")
    parser.add_argument("--dry-run",  action="store_true",
                        help="Print extracted JSON without writing files.")
    args = parser.parse_args()

    page_texts: dict[int, str] = {}
    if args.text:
        text = args.text
        doc_id = args.doc_id or "unknown_doc"
    else:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            print(f"ERROR: file not found: {pdf_path}", file=sys.stderr)
            sys.exit(1)
        text, page_texts = extract_text(pdf_path)
        doc_id = args.doc_id or pdf_path.stem.lower().replace("-", "_").replace(" ", "_")

    print(f"[extractor] calling {MODEL} (doc_id={doc_id}) …")
    entities = call_haiku(text, doc_id, args.prompt_version)
    print(f"[extractor] {len(entities)} entities extracted")

    # Backfill source_page by locating each entity's source_text in the page map
    if page_texts:
        matched = 0
        for entity in entities:
            page = find_page_for_text(entity.get("source_text", ""), page_texts)
            if page is not None:
                entity["source_page"] = page
                matched += 1
        print(f"[extractor] source_page resolved for {matched}/{len(entities)} entities", file=sys.stderr)

    if args.dry_run:
        print(json.dumps({"entities": entities}, indent=2, ensure_ascii=False))
        return

    vault_dir = Path(args.vault)
    written = write_vault_files(entities, vault_dir, doc_id, args.prompt_version, MODEL)
    print(f"[extractor] {len(written)} files written to {vault_dir}")


if __name__ == "__main__":
    main()
