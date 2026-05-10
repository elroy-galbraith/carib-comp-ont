# Deep-research prompt — CBU-31 lit review

Copy everything below the line into your deep-research agent. Paste the agent's findings back to me as a single document and I'll turn it into `docs/related_work.md`.

---

## Task

Run a targeted literature review for an academic paper targeting **JURIX 2026** (workshop or short-paper track). The paper introduces a low-friction, reproducible workflow for **LLM-curated jurisdictional compliance ontologies**, demonstrated on Caribbean data-protection law. I need enough prior-art coverage to (a) write the related-work section and (b) pre-register evaluation metrics.

## Project positioning (so you can write sharp "where we differ" passages)

- **Wedge:** lowest-friction maintenance for jurisdiction-specific compliance graphs. Markdown + YAML vault, Git-PR review workflow, LLM-curated ingestion (inbox → extract → validate → PR), FIBO-aligned without full FIBO import.
- **Closest sibling work:** Donalds, Barclay & Osei-Bryson (UWI / Caribbean compliance NLP). They answer compliance *questions* with NLP; this project adds a typed, queryable *graph* layer with auditable, human-in-the-loop authoring. Find the precise overlap and the precise complementarity.
- **Held-out / quarantined corpus:** Bahamas Data Protection Act 2003. **Do not include any extraction, summary, or analysis of this specific statute** — it is reserved for cold-run evaluation. You may cite it bibliographically but do not pull substantive content from it.
- **Target venue:** JURIX. Note explicitly which kinds of contributions JURIX has accepted in the last 3 years (methodology / tools / empirical / position) so I know which framing to lead with.

## Reading list (mandatory coverage)

### Bucket 1 — Caribbean compliance NLP (sibling work)
1. **Donalds, Barclay & Osei-Bryson** — locate their primary paper(s) on Caribbean / Jamaican data-protection compliance NLP. Pull every paper of theirs in this thread.
2. **Caribbean / UWI sweep** — Google Scholar / Semantic Scholar sweep for "Caribbean data protection NLP", "Jamaica DPA compliance", "CARICOM data protection ontology", "Trinidad data protection NLP". Include any hits even if marginal.

### Bucket 2 — Ontology evaluation methodology
3. **OOPS! (OntOlogy Pitfall Scanner)** — Poveda-Villalón et al.
4. **OntoClean** — Guarino & Welty.
5. At least one **competency-question evaluation** paper — e.g., Bezerra et al., or Suárez-Figueroa et al. (NeOn methodology).
6. Any modern (post-2020) paper on **evaluation metrics for LLM-assisted or LLM-curated ontologies** — bonus if it covers human-in-the-loop validation.

### Bucket 3 — Comparable legal-ontology architectures
7. **LKIF / LKIF-Core**.
8. **LegalRuleML** and **Akoma Ntoso** — both, even briefly.
9. **Eunomos**.
10. **FIBO regulatory modules** — confirm what's in scope and what alignment looks like in practice (not full FIBO import).
11. Any paper on **jurisdiction-specific legal ontologies** (GDPR ontologies, DPV — Data Privacy Vocabulary — especially).

### Bucket 4 — Recent JURIX / ICAIL papers (2023, 2024, 2025)
12. **At least 5 papers** from JURIX or ICAIL in the last 3 years that touch: legal ontologies, LLM-assisted legal knowledge extraction, compliance-graph construction, or evaluation methodology for legal AI artifacts.
13. For each, note the venue's *contribution type* (methodology, system, empirical, position) so I can calibrate framing.

## Output format

For **each entry**, produce a block in this exact shape:

```
### [Author Last name(s), Year] Short title
- **Citation:** full BibTeX-ready citation
- **Link:** DOI or URL (open-access preferred; flag if paywalled)
- **Accessibility:** [Full text read] | [Abstract + 1st page only] | [Abstract only] | [Cited-by description only]
- **What they do:** 2-4 sentences. Concrete: what artifact, what evaluation, what dataset, what claim.
- **Method snapshot:** ontology / NLP / hybrid / rule-based / LLM-curated, plus any evaluation metrics they used (e.g., precision/recall, expert agreement, competency-question coverage, OntoClean violations).
- **Where we differ:** 2-4 sentences specifically contrasting with this project's wedge (low-friction, markdown+YAML vault, Git-PR review, LLM-curated, FIBO-aligned-without-import). Be specific — generic "we focus on X, they focus on Y" is not useful.
- **Strength of "where we differ":** [strong — copyable into paper] | [solid] | [thin — needs a deeper read]
```

Then close with a **synthesis section**:

- **Three strongest "where we differ" passages**, copy-ready prose.
- **Pre-registration implications** — based on what evaluation methods recur in this prior art, suggest 3-5 candidate metrics this project should pre-register (e.g., competency-question coverage on a held-out gold standard, OOPS!-style pitfall count, expert-agreement κ on extractions, FIBO-alignment fidelity).
- **Gaps you couldn't fill** — what's missing from the bibliography (paywalled, not findable, conflicting reports). I'll fill those with institutional access.

## Quality bar

- ≥ 16 entries total across the four buckets.
- ≥ 3 "where we differ" passages strong enough to drop into the paper unedited.
- All claims about specific papers must cite a source; if you couldn't access the paper, mark it and say what you read instead (abstract, citation graph, secondary description).
- No fabricated citations. If a paper you expected doesn't exist, say so.

## Constraints

- Do not extract from or quote the **Bahamas Data Protection Act 2003** itself. Bibliographic mention only.
- Prefer open-access / preprint sources where possible (arXiv, SSRN, ResearchGate, university repositories, JURIX open proceedings).
- Last 3 years means 2023, 2024, 2025 (inclusive).
