"""Help — what kgforge is for, how to use it, and how to recover when it breaks.

Navigation is two-level: tabs across the top, expanders inside each tab.
Nothing here requires a project to be loaded, so the page is reachable from
a fresh install.
"""
from __future__ import annotations

import streamlit as st

from kgforge.ui.helpers import get_active_project, project_chip

st.set_page_config(page_title="Help · kgforge", layout="wide")
project_chip()

st.title("❓ Help")
st.caption(
    "What kgforge is for · how a typical session flows · what each page does "
    "· how to author your own pack · how to fix common problems."
)

overview, workflow, concepts, pages_tab, packs_tab, cli_tab, troubleshooting = st.tabs(
    ["Overview", "Workflow", "Concepts", "Pages", "Pack authoring", "CLI", "Troubleshooting"]
)

# ── Overview ─────────────────────────────────────────────────────────────────
with overview:
    st.subheader("What is kgforge?")
    st.markdown(
        "kgforge turns **structured documents** (statutes, standards, "
        "policies, interview transcripts, journals) into a **queryable "
        "knowledge graph** that a human still controls. An LLM proposes "
        "entities; a person approves them; the graph is rebuilt from the "
        "approved set. Nothing reaches the graph without a review step."
    )

    with st.expander("Who is it for?", expanded=False):
        st.markdown(
            "- **Ontology engineers** building a domain ontology against a "
            "real corpus instead of in the abstract.\n"
            "- **Compliance / legal researchers** asking cross-document "
            "questions over jurisdictional text.\n"
            "- **Qualitative researchers** coding interview transcripts into "
            "themes, sub-themes, codes, and excerpts.\n"
            "- **Literature reviewers** turning paper corpora into a citable, "
            "queryable graph of claims, methods, and findings.\n"
            "- **Anyone** evaluating whether an LLM can be trusted to "
            "populate a schema, by keeping the human in the loop on every "
            "submission."
        )

    with st.expander("How is it different from just prompting an LLM?", expanded=False):
        st.markdown(
            "- The schema (classes, properties, IRIs, prompts, queries) is "
            "**declarative** — defined once in a *pack*, reused across "
            "projects.\n"
            "- Extracted entities land in a **vault** of Markdown + YAML "
            "files, not opaque JSON — you can read, edit, and `git diff` "
            "them.\n"
            "- The graph is rebuilt from the vault, so the **source of "
            "truth is the files**, not the model output.\n"
            "- Natural-language questions are answered by **synthesising "
            "SPARQL** and executing it — answers are grounded in triples, "
            "with citations back to the vault entries that produced them.\n"
            "- A *hook* layer lets each pack drop in small Python overrides "
            "(custom highlight needles, doc-id normalisation) without "
            "touching the engine."
        )

    with st.expander("What's bundled out of the box?", expanded=False):
        st.markdown(
            "Two built-in packs and two matching example projects:\n\n"
            "- **`compliance` pack + project** — Caribbean Compliance "
            "Ontology, covering the Jamaica Data Protection Act 2020. "
            "Five classes (`Statute`, `Provision`, `Definition`, "
            "`Regulator`, `Obligation`), three competency questions, a "
            "hand-curated seed of eight DPA entities, **git approval "
            "backend** (each extraction lands on a `proposals/<doc>` "
            "branch).\n\n"
            "- **`thematic` pack + project** — Qualitative Thematic "
            "Analysis for interview transcripts. Four classes (`Theme`, "
            "`Subtheme`, `Code`, `Excerpt`), three competency questions, "
            "a hand-curated 11-entity synthetic vault, **filesystem "
            "approval backend** (SQLite audit log + in-app approve/reject). "
            "First pack to use a datatype property (`spokenBy`) and "
            "multi-valued object properties (`codedAs`).\n\n"
            "Plus a `blank` template you can start from when defining your "
            "own pack — see the **Pack authoring** tab."
        )

# ── Workflow ─────────────────────────────────────────────────────────────────
with workflow:
    st.subheader("A typical session")
    st.caption(
        "Step through these in order the first time. Later sessions you'll "
        "mostly live on the Dashboard and Query pages."
    )

    with st.expander("1 — Open or create a project", expanded=True):
        st.markdown(
            "Go to **Projects** in the sidebar. Either:\n\n"
            "- Open the bundled **compliance** project (Caribbean DPA, git "
            "backend) or **thematic** (interview transcripts, filesystem "
            "backend), or\n"
            "- Create a new project from a template:\n"
            "    - **compliance** — clones the DPA pack into your project "
            "  so you can edit it.\n"
            "    - **thematic** — clones the thematic-analysis pack.\n"
            "    - **blank** — minimal scaffold you fill in yourself "
            "  (see the **Pack authoring** tab).\n\n"
            "The active project name shows in the sidebar chip on every "
            "page."
        )

    with st.expander("2 — Confirm your API key", expanded=False):
        st.markdown(
            "Extraction and natural-language queries call the Anthropic "
            "API. Set `ANTHROPIC_API_KEY`:\n\n"
            "- in a `.env` file at the repo root (recommended — survives "
            "restarts), **or**\n"
            "- on the **Settings** page for the current Python process "
            "(local-only; not safe for multi-user deployments — the page "
            "warns about this).\n\n"
            "If the key is missing, a yellow banner appears on every page "
            "that needs it, and the relevant buttons disable."
        )

    with st.expander("3 — Drop a document and extract", expanded=False):
        st.markdown(
            "On **Dashboard**:\n\n"
            "1. **Drop documents** — upload one or more files. The "
            "uploader accepts whatever extensions the active pack's "
            "`inbox.accepted_extensions` declares (the compliance pack "
            "accepts `.pdf`; the thematic pack accepts `.pdf`, `.txt`, "
            "`.md`, `.vtt`).\n"
            "2. **Process all** — the engine runs PDF text extraction "
            "(Docling preferred, pdfplumber fallback) or reads text "
            "directly, calls Claude with a JSON-Schema-validated "
            "`extract_entities` tool, writes one Markdown file per "
            "entity into the project's `vault/` directory, and inserts "
            "a *pending submission* into the approval backend.\n"
            "3. The PDF is archived to `vault/sources/`; per-entity "
            "highlighted copies are generated for click-through."
        )

    with st.expander("4 — Review and approve", expanded=False):
        st.markdown(
            "Each pending submission expands to show the entity cards the "
            "model proposed — class, label, source page/section, source "
            "text snippet, and properties (including multi-value ones "
            "like `codedAs: [c1, c2]`). Click:\n\n"
            "- **✅ Approve** — for the filesystem backend, marks the audit "
            "row APPROVED (vault files are already on disk). For the git "
            "backend, merges the `proposals/<doc>` branch into `main`.\n"
            "- **❌ Reject** — for filesystem: moves the vault files into "
            "`vault/.rejected/<doc_id>_<timestamp>/` and marks the row "
            "REJECTED. For git: deletes the proposal branch.\n\n"
            "Approval is per-document, not per-entity — reject and re-run "
            "if the model got a single entity badly wrong, or edit the "
            "vault file directly after approval (it's just Markdown)."
        )

    with st.expander("5 — Inspect the schema (optional)", expanded=False):
        st.markdown(
            "The **Schema** page shows the active pack's classes, "
            "properties (with `datatype:` flag), prompt templates, IRI "
            "namespaces, competency-question SPARQL, and the generated "
            "tool-use JSON Schema. Use the **Live preview** tab on the "
            "Prompt section to render the prompts against a sample "
            "document ID — handy when you're authoring or tuning a pack."
        )

    with st.expander("6 — Query the graph", expanded=False):
        st.markdown(
            "On **Query** (three tabs):\n\n"
            "- **🎯 Competency questions** — pre-canned SPARQL queries "
            "shipped with the pack. One click runs them against the "
            "current vault.\n"
            "- **💬 Ask (natural language)** — type a question; Claude "
            "synthesises SPARQL using the schema + entity catalog + your "
            "CQs as few-shot, executes it, and summarises the rows with "
            "`[Label](vault/<id>.md)` citations back to the source files. "
            "Toggle **Show generated SPARQL** to see the query.\n"
            "- **✏ Custom SPARQL** — paste your own query for ad-hoc "
            "exploration.\n\n"
            "The graph is **lazily built** the first time you query — if "
            "`vault.ttl` doesn't exist yet, the page rebuilds it from the "
            "vault Markdown in-process. **Rebuild vault.ttl** forces a "
            "refresh after you've edited vault files directly."
        )

# ── Concepts ─────────────────────────────────────────────────────────────────
with concepts:
    st.subheader("Concepts you'll see referenced")
    st.caption("Read these once; the rest of the UI assumes you know them.")

    with st.expander("Pack", expanded=False):
        st.markdown(
            "A **pack** is the declarative bundle of everything that "
            "defines a *domain*:\n"
            "- `pack.yaml` — classes, properties, IRI namespaces, prompt "
            "template, accepted file extensions, CQ list, models.\n"
            "- `schema.ttl` *(optional)* — the formal RDFS/OWL ontology.\n"
            "- `sparql/*.rq` *(optional)* — the competency-question files.\n"
            "- `hooks.py` *(optional)* — pack-specific Python overrides "
            "(see **Hook** below).\n\n"
            "Packs live under `kgforge/pack/builtin/` (or any path you "
            "point at). One pack can drive many projects."
        )

    with st.expander("Project", expanded=False):
        st.markdown(
            "A **project** binds a pack to a concrete working directory "
            "via a `project.json`:\n"
            "- `vault/` (extracted entities), `inbox/` (drop-zone), "
            "`sources/` (archived originals).\n"
            "- An approval backend.\n"
            "- Optional pointers to `schema.ttl` and `sparql/` (handy when "
            "a project reuses files from a built-in pack).\n\n"
            "Switch projects to switch corpora without touching the schema."
        )

    with st.expander("Vault", expanded=False):
        st.markdown(
            "The **vault** is the directory of approved entity files — one "
            "Markdown + YAML frontmatter file per entity. This is the "
            "source of truth. The Turtle graph (`vault.ttl`) is "
            "**regenerated** from the vault, so anything you change in a "
            "vault file flows through to the next query."
        )

    with st.expander("Approval backend", expanded=False):
        st.markdown(
            "How proposed entities get from *extracted* to *in the vault*. "
            "Two backends ship today:\n\n"
            "- **filesystem** (default) — vault writes happen directly; "
            "a SQLite audit log tracks each submission; approve marks the "
            "row APPROVED; reject moves the files to "
            "`vault/.rejected/<doc_id>_<ts>/`.\n"
            "- **git** — each submission is a `proposals/<doc_id>` branch "
            "with a structured commit; approve merges to `main`; reject "
            "deletes the branch. The git backend auto-detects the repo "
            "root by walking up from the vault until it finds a `.git/`."
        )

    with st.expander("Competency question (CQ)", expanded=False):
        st.markdown(
            "A SPARQL query the pack guarantees the graph can answer. CQs "
            "are the acceptance test for the ontology — if a CQ breaks "
            "after a schema change, the change isn't ready. They also "
            "double as worked examples for the natural-language agent."
        )

    with st.expander("Datatype property", expanded=False):
        st.markdown(
            "A property whose value is a **literal** (string, integer) "
            "rather than a link to another entity. Mark it in `pack.yaml` "
            "with `datatype: true` — the vault writer keeps the value "
            "unwrapped (no `[[wikilinks]]`) and the Turtle emitter writes "
            "it as `\"value\"` instead of `prefix:value`. Example: the "
            "thematic pack's `spokenBy: xsd:string` for participant IDs."
        )

    with st.expander("Multi-value property", expanded=False):
        st.markdown(
            "A single property can take a YAML **list** of values:\n\n"
            "```yaml\nproperties:\n  codedAs:\n    - '[[code_a]]'\n    - '[[code_b]]'\n```\n\n"
            "The Turtle emitter expands each element into its own triple "
            "(`tha:codedAs thae:code_a ; tha:codedAs thae:code_b ;`). "
            "Works for both object and datatype properties. The thematic "
            "pack uses this for `codedAs` and `supportsTheme` since one "
            "excerpt can carry several codes."
        )

    with st.expander("Hook", expanded=False):
        st.markdown(
            "A pack's `hooks.py` is a Python module the loader imports "
            "and attaches to the pack. The engine looks up four function "
            "names; supply any subset:\n\n"
            "| Function | Overrides |\n"
            "|---|---|\n"
            "| `derive_doc_id(stem)` | Filename → document-ID rule |\n"
            "| `search_variants(source_text)` | PDF highlight needle generation |\n"
            "| `post_extract(entities)` | Last-mile transforms on LLM output |\n"
            "| `validate_entity(entity)` | Per-entity validation (non-empty list = reject) |\n\n"
            "The compliance pack uses `search_variants` for a "
            "legal-definition term-name regex. The thematic pack uses "
            "`derive_doc_id` to collapse `interview_03` → `interview03` "
            "and `search_variants` to strip speaker prefixes."
        )

# ── Pages ────────────────────────────────────────────────────────────────────
with pages_tab:
    st.subheader("What each page is for")

    with st.expander("🏠 Home (app.py)", expanded=False):
        st.markdown(
            "Landing page. Shows the active project and a summary of its "
            "pack, paths, approval backend, and entity counts. Use the "
            "sidebar to navigate."
        )

    with st.expander("📂 Projects", expanded=False):
        st.markdown(
            "List existing projects, create one from a template "
            "(`compliance` / `thematic` / `blank`), and set the active "
            "project. Switching project here changes which vault and pack "
            "every other page operates on. The wizard lets you pick the "
            "approval backend (`filesystem` or `git`) at creation time."
        )

    with st.expander("📊 Dashboard", expanded=False):
        st.markdown(
            "The day-to-day workspace:\n\n"
            "1. **Drop documents** — upload PDFs (or text-shaped inputs "
            "if your pack accepts them) into the inbox.\n"
            "2. **Inbox** — see what's queued; **Process all** runs "
            "extraction; **Clear inbox** wipes the queue without "
            "processing.\n"
            "3. **Pending review** — Approve / Reject per submission, "
            "with per-entity cards showing class, label, source, text "
            "snippet, and properties."
        )

    with st.expander("📐 Schema", expanded=False):
        st.markdown(
            "Read-only view of the active pack:\n\n"
            "- **Namespaces** — base IRI, entity IRI, prefixes.\n"
            "- **Classes** — name, label, parent, description.\n"
            "- **Properties** — name, domain, range, datatype flag, "
            "predicate IRI.\n"
            "- **Competency questions** — each CQ's SPARQL inline.\n"
            "- **Prompt template** — system, user, few-shot, plus a "
            "**Live preview** tab that renders the prompts against a "
            "sample document ID.\n"
            "- **Generated tool-use schema** — exactly what gets sent to "
            "Claude as the `extract_entities` tool's `input_schema`."
        )

    with st.expander("🔎 Query", expanded=False):
        st.markdown(
            "Three tabs:\n\n"
            "- **🎯 Competency questions** — pick a CQ, click Run, see "
            "the result table.\n"
            "- **💬 Ask (natural language)** — Claude synthesises SPARQL, "
            "executes it, summarises with citations.\n"
            "- **✏ Custom SPARQL** — paste your own query.\n\n"
            "The graph loads lazily on first query; **Rebuild vault.ttl** "
            "forces a refresh after vault edits."
        )

    with st.expander("⚙ Settings", expanded=False):
        st.markdown(
            "Local Anthropic API key override (process-wide — see the "
            "warning on the page; not safe for multi-user deployments), "
            "read-only view of pack-driven models, path introspection, "
            "and a Reload caches button after editing a pack."
        )

    with st.expander("❓ Help (this page)", expanded=False):
        st.markdown(
            "Self-referential. Reachable without an active project so "
            "it's the right starting point on a fresh install."
        )

# ── Pack authoring ───────────────────────────────────────────────────────────
with packs_tab:
    st.subheader("Author your own pack")
    st.caption(
        "A pack is a folder. The minimum is one `pack.yaml`; the rest "
        "(`schema.ttl`, `sparql/`, `hooks.py`) is optional."
    )

    with st.expander("Quickest path — create from the UI", expanded=True):
        st.markdown(
            "Go to **Projects** → *Create a new project* → pick the "
            "`blank` (or any) template. The wizard:\n\n"
            "1. Creates `projects/<name>/`.\n"
            "2. Copies the template pack into `projects/<name>/pack/` so "
            "you can edit without touching the bundled defaults.\n"
            "3. Writes a `project.json` pointing at it.\n"
            "4. Creates `vault/`, `inbox/`, `vault/sources/`.\n\n"
            "Edit `projects/<name>/pack/pack.yaml` directly, then reload "
            "from the **Settings** page."
        )

    with st.expander("Minimum viable `pack.yaml`", expanded=False):
        st.markdown(
            "Required fields: `metadata`, `namespaces`, ≥1 `classes` "
            "entry, `prompt`. Everything else has defaults."
        )
        st.code(
            """schema_version: 1

metadata:
  name: your_domain
  label: "Your domain"

namespaces:
  base_iri:      "https://your.org/your-domain/"
  entity_iri:    "https://your.org/your-domain/entity/"
  prefix:        "yd"
  entity_prefix: "yde"

classes:
  - {name: Thing, label: "Thing"}

properties:
  - {name: relatesTo, domain: Thing, range: Thing}
  - {name: tag,       domain: Thing, range: "xsd:string", datatype: true}

prompt:
  version: v1
  system: |
    You extract entities from <documents of your domain>.
    Use only these classes: Thing.
    Always prefix entity IDs with the document ID ({doc_id}_).
  user: |2
        {few_shot}
        Document ID: {doc_id}

        ---
        {text_window}
        ---
  few_shot: |
    (a worked input → output example)

competency_questions:
  - {id: cq1, label: "All entities", file: sparql/cq1_all.rq}

inbox:
  accepted_extensions: [".pdf", ".txt"]
""",
            language="yaml",
        )

    with st.expander("Optional `schema.ttl`", expanded=False):
        st.markdown(
            "Pure RDFS/OWL declaring your classes and properties. Used "
            "by the Query page as context when synthesising SPARQL "
            "(Claude sees the schema verbatim), and loaded into Oxigraph "
            "alongside the vault Turtle. Not required, but recommended "
            "for any non-trivial pack."
        )

    with st.expander("Optional `sparql/*.rq`", expanded=False):
        st.markdown(
            "One `.rq` file per competency question, paths referenced "
            "from `pack.yaml`'s `competency_questions` block. The Query "
            "page lists them in the dropdown; the natural-language agent "
            "uses them as few-shot examples."
        )

    with st.expander("Optional `hooks.py`", expanded=False):
        st.markdown(
            "Python module with any of: `derive_doc_id`, "
            "`search_variants`, `post_extract`, `validate_entity` "
            "(see the **Hook** concept). Reference from `pack.yaml`:\n\n"
            "```yaml\nhooks:\n  module: hooks.py\n```\n\n"
            "The loader imports it once at pack-load time and attaches "
            "to `pack.hooks_module`; engine code reads functions off it "
            "with `getattr(..., None)` so missing ones fall back to "
            "sensible defaults."
        )

    with st.expander("Validation", expanded=False):
        st.markdown(
            "`pack.yaml` is validated by Pydantic on load. Common errors:\n\n"
            "- **class name** must match `^[A-Z][A-Za-z0-9]*$` (PascalCase).\n"
            "- **property name** must match `^[a-z][A-Za-z0-9]*$` (camelCase).\n"
            "- **class `parent`** must reference an existing class.\n"
            "- **property `domain`** must reference an existing class.\n"
            "- **property `range`** if non-datatype, should reference an "
            "existing class — issues a `UserWarning` if not.\n"
            "- **classes list** can't be empty (min_length=1)."
        )

# ── CLI ──────────────────────────────────────────────────────────────────────
with cli_tab:
    st.subheader("Command-line equivalents")
    st.caption(
        "Every page in this UI maps to a thin shim under `scripts/` that "
        "calls the same `kgforge.engine` functions. Useful for automation "
        "and headless workflows."
    )

    with st.expander("Extract", expanded=False):
        st.code(
            "python scripts/extractor.py path/to/doc.pdf "
            "--pack compliance --doc-id mydoc",
            language="bash",
        )

    with st.expander("Curate (watch loop)", expanded=False):
        st.code(
            "# Process whatever's already in inbox/ then exit\n"
            "python scripts/curator.py --once --pack compliance --backend git\n\n"
            "# Watch the inbox forever (Ctrl-C to stop)\n"
            "python scripts/curator.py --pack thematic --backend filesystem",
            language="bash",
        )

    with st.expander("Rebuild the Turtle graph", expanded=False):
        st.code(
            "python scripts/to_turtle.py --pack compliance --print "
            "> vault.ttl",
            language="bash",
        )

    with st.expander("Run a competency question", expanded=False):
        st.code(
            "# All CQs in the active pack\n"
            "python scripts/load_to_oxigraph.py --pack compliance\n\n"
            "# A single .rq file\n"
            "python scripts/load_to_oxigraph.py --pack compliance "
            "--query sparql/cq1_obligations_on_controller.rq",
            language="bash",
        )

    with st.expander("Ask a natural-language question", expanded=False):
        st.code(
            "python scripts/ask.py \"Which obligations apply to a data "
            "controller?\" --pack compliance --show-sparql",
            language="bash",
        )

    with st.expander("Re-inject highlights into a source PDF", expanded=False):
        st.code(
            "python scripts/highlight.py --doc-id mydoc --pack compliance",
            language="bash",
        )

# ── Troubleshooting ──────────────────────────────────────────────────────────
with troubleshooting:
    st.subheader("When something doesn't work")

    with st.expander("\"ANTHROPIC_API_KEY is not set\" banner won't go away", expanded=False):
        st.markdown(
            "Streamlit only reads `.env` at process start. If you just "
            "added the key:\n\n"
            "1. Stop the server (`Ctrl+C` in the terminal running "
            "Streamlit).\n"
            "2. Confirm the key is in `.env` at the repo root, on its own "
            "line: `ANTHROPIC_API_KEY=sk-ant-…`\n"
            "3. Restart with `streamlit run kgforge/ui/app.py` (or "
            "`python -m streamlit run …`).\n\n"
            "Or, for an in-session override, paste the key on the "
            "**Settings** page and click *Apply* — that sets `os.environ` "
            "for this Python process (single-user local only)."
        )

    with st.expander("\"No project selected\" / pages keep nudging me to Projects", expanded=False):
        st.markdown(
            "The active project is stored in session state and resets when "
            "the browser tab is closed. Open **Projects** and click into "
            "the project you want — the sidebar chip should then show its "
            "name on every page."
        )

    with st.expander("`ModuleNotFoundError: No module named 'kgforge'`", expanded=False):
        st.markdown(
            "Streamlit is running under a Python that doesn't have "
            "`kgforge` installed — usually a global Python rather than the "
            "venv. From the activated venv:\n\n"
            "```\n"
            "pip install -e \".[ui]\"\n"
            "python -m streamlit run kgforge/ui/app.py\n"
            "```\n\n"
            "`python -m streamlit` bypasses any global `streamlit.exe` "
            "that may be earlier on `PATH`."
        )

    with st.expander("Extraction fails on a specific document", expanded=False):
        st.markdown(
            "Common causes:\n\n"
            "- **Scanned/image-only PDF** — pdfplumber and Docling both "
            "need a text layer. Run OCR (Tesseract, ABBYY, etc.) "
            "beforehand.\n"
            "- **Unsupported extension** — the engine now raises a clear "
            "`ValueError` listing the offending suffix. Add it to "
            "`pack.inbox.accepted_extensions` AND to the dispatch table "
            "in `kgforge/engine/pdf_text.py:extract_input`.\n"
            "- **Rate-limit / 529 from Anthropic** — wait and retry the "
            "single file rather than re-running the whole inbox. The "
            "curator quarantines failures to `vault/sources/.errors/` so "
            "the watch loop continues.\n"
            "- **Schema mismatch** — check the **Schema** page; if the "
            "pack expects classes the document doesn't contain, the model "
            "may return an empty extraction. That's a pack problem, not a "
            "kgforge bug."
        )

    with st.expander("Approved entities don't show up in Query results", expanded=False):
        st.markdown(
            "The graph is rebuilt from the vault on each query — but only "
            "if the vault is reachable from the project's `vault_dir`. "
            "Double-check on **Projects** that the project points at the "
            "directory you expect, and that approved files are in it (not "
            "in a stale `.rejected/` subdirectory). Then click "
            "**Rebuild vault.ttl** on the Query page to force a refresh."
        )

    with st.expander("Multi-value property looks wrong in YAML", expanded=False):
        st.markdown(
            "A property with multiple values should serialise as a YAML "
            "list:\n\n"
            "```yaml\nproperties:\n  codedAs:\n    - '[[c1]]'\n    - '[[c2]]'\n```\n\n"
            "If you see `codedAs: '[[[c1, c2]]]'` instead, the LLM "
            "returned a Python list literal as a string. That used to "
            "happen pre-Phase-D; if you see it on a fresh install, "
            "regenerate the vault entry or edit the frontmatter to the "
            "expected list shape."
        )

    with st.expander("Need to start over for one document", expanded=False):
        st.markdown(
            "1. Delete the vault files for that `doc_id` (the **Dashboard** "
            "card shows the file list).\n"
            "2. Move the PDF back from `vault/sources/` to `inbox/`.\n"
            "3. Click **Process all** again on the Dashboard.\n\n"
            "On the git backend, you'll additionally want to delete the "
            "`proposals/<doc_id>` branch with `git branch -D` if it "
            "wasn't merged."
        )

    with st.expander("Pack changes don't take effect", expanded=False):
        st.markdown(
            "The pack loader memoises by name (`@lru_cache`). After "
            "editing `pack.yaml`, go to **Settings** → *Reload all packs "
            "/ projects* to clear the cache, then revisit the affected "
            "page."
        )

# ── Footer hint ──────────────────────────────────────────────────────────────
st.divider()
project = get_active_project()
if project is None:
    st.info(
        "Tip: open a project on the **Projects** page to unlock the "
        "Dashboard, Schema, and Query pages."
    )
else:
    st.caption(f"Active project: **{project.label}** (`{project.name}`)")
