# Demo Script — Caribbean Compliance Ontology Prototype

**Target duration:** ≤ 2 minutes  
**Audience:** Donalds, Barclay & Osei-Bryson (UWI) — peer-research evaluation  
**Format:** Screen recording (OBS or QuickTime), terminal + text editor side by side

---

## Pre-recording checklist

- [ ] `pip install -r requirements.txt` completed
- [ ] `ANTHROPIC_API_KEY` exported in the shell
- [ ] `python scripts/to_turtle.py` run — `vault/vault.ttl` exists
- [ ] `git status` is clean on `main`
- [ ] A DPA 2020 PDF page (e.g. §6) copied to `demo_assets/dpa_2020_s6.pdf`
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
cp demo_assets/dpa_2020_s6.pdf inbox/
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

### 01:25–01:55 — Run the competency questions

The queries run automatically via `load_to_oxigraph.py`. Highlight CQ1:

```
CQ1 — Obligations on DataController
obligation                                       label                               statute
ccoe:dpa2020_obligation_lawful_processing        Obligation to Process ... Lawfully  dpa2020
```

**Say:**
> "Three competency questions answered directly from the ontology.
> CQ1: every obligation the DPA places on a data controller.
> CQ2: which regulator enforces the act.
> CQ3: all formally defined terms."

---

### 01:55–02:00 — Close on the schema

```bash
cat schema/carib_compliance.ttl | grep subClassOf
```

Show:
```
cco:Statute    rdfs:subClassOf fibo-fbc-fct-rga:Regulation .
cco:Regulator  rdfs:subClassOf fibo-be-ge-ge:GovernmentalAuthority .
```

**Say:**
> "This is the artifact. The methodology is the loop you just watched:
> drop a statute section in, review the PR, merge, query.
> The FIBO alignment means the schema can federate with financial-compliance
> ontologies when the project scales."

---

## Post-recording

- Trim to ≤ 2:00 and upload to YouTube (unlisted)
- Add the link to `README.md` under "Demo recording"
- Share the link in the outreach email
