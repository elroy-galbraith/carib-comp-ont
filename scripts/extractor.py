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

def extract_text_docling(pdf_path: Path) -> str:
    from docling.document_converter import DocumentConverter  # type: ignore
    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    return result.document.export_to_markdown()


def extract_text_pdfplumber(pdf_path: Path) -> str:
    import pdfplumber  # type: ignore
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)


def extract_text(pdf_path: Path) -> str:
    try:
        text = extract_text_docling(pdf_path)
        print(f"[extractor] text extracted via docling ({len(text)} chars)", file=sys.stderr)
        return text
    except ImportError:
        pass
    except Exception as e:
        print(f"[extractor] docling failed ({e}), trying pdfplumber…", file=sys.stderr)

    try:
        text = extract_text_pdfplumber(pdf_path)
        print(f"[extractor] text extracted via pdfplumber ({len(text)} chars)", file=sys.stderr)
        return text
    except ImportError:
        pass

    print("ERROR: no PDF extractor available. Install docling or pdfplumber.", file=sys.stderr)
    sys.exit(1)


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
    properties = entity.get("properties") or {}

    meta = {
        "class":          cls,
        "id":             eid,
        "label":          label,
        "uri":            f"https://ontology.carib-comp.org/compliance/entity/{eid}",
        "source_statute": doc_id,
        "source_section": source_section,
        "source_text":    source_text,
        "properties":     properties,
        "prompt_version": prompt_version,
        "model_snapshot": model_snapshot,
        "validation":     "PENDING",
    }

    frontmatter = yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False)

    body = dedent(f"""\
        ## {label}

        **Class:** `cco:{cls}`
        **Source:** {source_section} — {doc_id}

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

    if args.text:
        text = args.text
        doc_id = args.doc_id or "unknown_doc"
    else:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            print(f"ERROR: file not found: {pdf_path}", file=sys.stderr)
            sys.exit(1)
        text = extract_text(pdf_path)
        doc_id = args.doc_id or pdf_path.stem.lower().replace("-", "_").replace(" ", "_")

    print(f"[extractor] calling {MODEL} (doc_id={doc_id}) …")
    entities = call_haiku(text, doc_id, args.prompt_version)
    print(f"[extractor] {len(entities)} entities extracted")

    if args.dry_run:
        print(json.dumps({"entities": entities}, indent=2, ensure_ascii=False))
        return

    vault_dir = Path(args.vault)
    written = write_vault_files(entities, vault_dir, doc_id, args.prompt_version, MODEL)
    print(f"[extractor] {len(written)} files written to {vault_dir}")


if __name__ == "__main__":
    main()
