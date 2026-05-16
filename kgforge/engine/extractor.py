"""End-to-end extraction: PDF/text → LLM tool-use → vault Markdown files.

Orchestrates pdf_text + schema_builder + prompt + Anthropic API + vault_writer.
The script in scripts/extractor.py is now a CLI shim around this module.
"""
from __future__ import annotations

import sys
from pathlib import Path

import anthropic

from kgforge.engine import pdf_text, prompt as prompt_mod, schema_builder, vault_writer
from kgforge.pack import DomainPack


def call_llm(
    pack: DomainPack,
    text: str,
    doc_id: str,
    prompt_version: str,
) -> list[dict]:
    """Single-shot extraction call. Returns the raw `entities` list."""
    client = anthropic.Anthropic()
    system, user = prompt_mod.render_prompts(pack, doc_id, prompt_version, text)

    response = client.messages.create(
        model=pack.models.extractor,
        max_tokens=4096,
        system=system,
        tools=[
            {
                "name": "extract_entities",
                "description": "Extract legal ontology entities from statutory text.",
                "input_schema": schema_builder.build_entity_schema(pack),
            }
        ],
        tool_choice={"type": "tool", "name": "extract_entities"},
        messages=[{"role": "user", "content": user}],
    )

    for block in response.content:
        if block.type == "tool_use":
            return block.input.get("entities", [])
    return []


def extract(
    pack: DomainPack,
    *,
    pdf_path: Path | None = None,
    text: str | None = None,
    doc_id: str,
    prompt_version: str,
    vault_dir: Path,
    dry_run: bool = False,
) -> list[dict] | list[Path]:
    """Run the full pipeline.

    Returns:
        - list[dict] (raw entities) if dry_run=True
        - list[Path] (written vault files) otherwise
    """
    page_texts: dict[int, str] = {}
    if text is not None:
        body = text
    elif pdf_path is not None:
        body, page_texts = pdf_text.extract_text(pdf_path)
    else:
        raise ValueError("extract: must pass either pdf_path or text")

    print(f"[extractor] calling {pack.models.extractor} (doc_id={doc_id}) …")
    entities = call_llm(pack, body, doc_id, prompt_version)
    print(f"[extractor] {len(entities)} entities extracted")

    # Backfill source_page from the page-text map.
    if page_texts:
        matched = 0
        for entity in entities:
            page = pdf_text.find_page_for_text(entity.get("source_text", ""), page_texts)
            if page is not None:
                entity["source_page"] = page
                matched += 1
        print(
            f"[extractor] source_page resolved for {matched}/{len(entities)} entities",
            file=sys.stderr,
        )

    if dry_run:
        return entities

    return vault_writer.write_vault_files(
        entities, vault_dir, doc_id, prompt_version, pack.models.extractor, pack
    )
