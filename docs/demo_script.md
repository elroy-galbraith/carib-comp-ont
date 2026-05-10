# Demo Script — Caribbean Compliance Ontology Prototype

**Target duration:** ≤ 2 min 30 sec  
**Audience:** Donalds, Barclay & Osei-Bryson (UWI) — peer-research evaluation  
**Format:** Screen recording (OBS or QuickTime), terminal + text editor side by side

---

## Pre-recording checklist

- [ ] `pip install -r requirements.txt` completed
- [ ] `ANTHROPIC_API_KEY` exported in the shell (or in `.env` at repo root)
- [ ] `python scripts/to_turtle.py` run — `vault/vault.ttl` exists
- [ ] `python scripts/ask.py "test"` smoke-checked once (warms up dependencies)
- [ ] `git status` is clean on `main`
- [ ] A DPA 2020 PDF page (e.g. §6) copied to `vault/sources/dpa_2020_s6.pdf` (in-vault so the clickable provenance links in note bodies resolve to Obsidian's PDF viewer)
- [ ] Terminal font size ≥ 18pt, window maximised

---

## Script

### 00:00–00:15 — Set the scene

Open an empty `inbox/` in the file explorer alongside a terminal.

**Say:**
> "This is the curator-agent loop. I'll drop in a section of the Jamaica
> Data Protection Act 2020, and you'll see it become structured ontology in a
> reviewable git PR — without any manual data-entry."

---

### 00:15–00:35 — Drop the PDF

```bash
cp vault/sources/dpa_2020_s6.pdf inbox/
python scripts/curator.py --once
```

Show the terminal log scrolling: Docling extraction → Haiku call → vault files
written.

**Say:**
> "The curator agent detects the new file, extracts text with Docling,
> then calls Claude Haiku with a JSON-Schema constraint that mirrors our
> OWL class structure. The result is a set of Markdown files — human-readable,
> git-diffable."

---

### 00:35–01:05 — Inspect the proposal branch

```bash
git log proposals/dpa_2020_s6 --oneline
git show proposals/dpa_2020_s6
```

Show the structured commit message: `prompt_version`, `model_snapshot`,
`validation: PENDING`.

```bash
git diff main...proposals/dpa_2020_s6 -- vault/
```

Show the new entity files appearing in the vault diff.

**Say:**
> "Every proposed ontology change is a git branch with a structured commit.
> The prompt version and model snapshot are recorded in the commit — so you
> can audit exactly what produced this output."

---

### 01:05–01:25 — Merge and load

```bash
git checkout main
git merge proposals/dpa_2020_s6
python scripts/to_turtle.py
python scripts/load_to_oxigraph.py
```

**Say:**
> "After human review we merge. The vault converts to Turtle and loads into
> Oxigraph — an embedded SPARQL 1.1 store."

---

### 01:25–01:40 — Run the competency questions

The three CQs run automatically via `load_to_oxigraph.py`. Scroll past quickly,
pause on CQ1:

```text
CQ1 — Obligations on DataController
obligation                                       label                               statute
ccoe:dpa2020_obligation_lawful_processing        Obligation to Process ... Lawfully  dpa2020
```

**Say:**
> "Three pre-written competency questions, answered directly from the
> ontology — obligations on a data controller, regulators, defined terms."

---

### 01:40–02:15 — Ask a natural-language question

```bash
python scripts/ask.py "What does the DPA 2020 say about biometric data?" --show-sparql
```

The script generates SPARQL with Sonnet, runs it against the in-memory store,
then summarises the rows. Show all three: the generated query, the raw row,
the natural-language answer with a `[Biometric Data](vault/...)` citation.

**Say:**
> "The same graph, queried in plain English. Claude writes the SPARQL,
> Oxigraph executes it, then Claude summarises the rows — every claim is
> grounded in a row from the structured graph, with citations back to the
> reviewable Markdown entity. This is the agent-loop counterpart to the
> curator: structured authoring on the way in, structured QA on the way out."

---

### 02:15–02:30 — Close on the schema

```bash
sls subClassOf schema\carib_compliance.ttl
```

Show:

```text
cco:Statute    rdfs:subClassOf fibo-fbc-fct-rga:Regulation .
cco:Regulator  rdfs:subClassOf fibo-be-ge-ge:GovernmentalAuthority .
```

**Say:**
> "This is the artifact. The methodology is the loop you just watched:
> drop a statute in, review the PR, merge, query — by SPARQL or in plain
> English. FIBO alignment means the schema can federate with financial-
> compliance ontologies when the project scales."

---

## Post-recording

- Trim to ≤ 2:00 and upload to YouTube (unlisted)
- Add the link to `README.md` under "Demo recording"
- Share the link in the outreach email
