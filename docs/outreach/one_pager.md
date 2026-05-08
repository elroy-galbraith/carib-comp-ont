# Caribbean Compliance Ontology — One-Page Summary

**Author:** Elroy Galbraith · **Date:** May 2026 · **Contact:** elroy.galbraith@gmail.com

---

## Problem

Caribbean jurisdictions are enacting data-protection and cybercrime legislation
(Jamaica DPA 2020, Cybercrimes Act 2015, BOJ circulars) but no shared,
machine-readable representation of these obligations exists. Compliance
practitioners and researchers work from PDFs; cross-statute reasoning is
manual and error-prone.

---

## Methodology: Curator-Agent Loop

We propose **PR-as-ontology-mutation**: every proposed change to the knowledge
base arrives as a reviewable git branch, produced by an LLM extractor and
approved by a human curator before merging.

```
PDF statute section
        ↓  Docling (text extraction)
        ↓  Claude Haiku (JSON-Schema-constrained entity extraction)
        ↓  Markdown + YAML vault files
        ↓  git PR on proposals/<doc-id>   ← human review point
        ↓  git merge → Turtle → Oxigraph
        ↓  SPARQL competency queries
```

Key properties of the approach:

- **Auditable** — prompt version, model snapshot, and validation status are
  recorded in every commit message
- **Incremental** — each statute section becomes a separate, mergeable PR
- **Reviewable** — a non-programmer can read the Markdown files and assess
  whether the extraction is correct before it enters the ontology
- **FIBO-aligned** — `Regulator` and `Statute` are declared as subclasses of
  established FIBO concepts, enabling future federation with financial-compliance
  work

---

## Prototype Artifact

| Component | Status |
|---|---|
| OWL schema (5 classes, 5 properties) | ✓ complete |
| Hand-curated seed (8 entities, DPA 2020 §1–§10) | ✓ complete |
| Single-shot Haiku extractor | ✓ complete |
| Minimal curator-agent (watchdog + GitPython) | ✓ complete |
| Oxigraph SPARQL store + 3 competency questions | ✓ complete |
| Public GitHub repository (MIT) | ✓ https://github.com/elroy-galbraith/carib-comp-ont |

**Competency questions answered (seed data):**
1. List every obligation imposed on a DataController by the DPA 2020
2. Which regulators enforce the DPA 2020?
3. What terms are formally defined in the DPA 2020?

---

## Relationship to Donalds, Barclay & Osei-Bryson (2023)

The cybercrime classification ontology and this privacy-compliance ontology are
**complementary, not competing** artifacts. The intersection is real:

- *data breach* is both a cybercrime event and a trigger for DPA notification obligations
- *regulatory consequence* appears in both domains
- *incident response* obligations reference both statutory frameworks

We propose aligning the two ontologies at these seams in a Phase 2 extension,
and invite the original authors to advise on schema design before the Phase 2
freeze.

---

## Ask

1. Are you aware of FIBO-aligned compliance ontologies in the Caribbean
   (including unreleased or grant-funded work) we should engage with?
2. Where do you see the natural seams between cybercrime classification and
   privacy compliance?
3. Would you be open to reviewing the schema in an advisory capacity before the
   Phase 2 freeze?
4. Is there a UWI-affiliated venue (workshop, special issue) where this
   methodology and case study would land well, in addition to ICEGOV?

---

*Caribbean Compliance Ontology is released under the MIT licence.
Repository: https://github.com/elroy-galbraith/carib-comp-ont*
