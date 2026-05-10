# Set 1 deep-research — quality pass

**Verdict:** Strong on framing and "where we differ" passages. **Weak on citation accuracy** — at least three entries have wrong author/journal/title attributions. Treat the prose as good first drafts; treat the citations as suspect until each one is verified against the source.

## Verified citation problems

### 1. "Beyond technical measures" — wrong journal *and* wrong DOI
- **Set 1 says:** *Information Technology & People*, 31(1), 58-73 — DOI `10.1108/ITP-03-2020-0112`
- **Actual:** *European Journal of Information Systems*, 31(1), 58-73, 2022 — DOI `10.1080/0960085X.2021.1978344`
- Authors and title are correct. Journal and DOI must be replaced.

### 2. "LLM-authored Competency Questions (CompCQ)" — wrong author *and* wrong title
- **Set 1 says:** Bezerra et al. (2024), "LLM-authored Competency Questions: A Multi-faceted Characterization and Evaluation"
- **Actual (arXiv:2604.16258):** Alharbi, R., Tamma, V., Payne, T. R., & de Berardinis, J. — "Characterising LLM-Generated Competency Questions: a Cross-Domain Empirical Study using Open and Closed Models"
- The arXiv ID is real and the *content summary* in Set 1 roughly matches, but the attribution is fabricated. "Bezerra et al." appears nowhere.

### 3. "Janatian et al. 2023 ICAIL" — arXiv ID points to a different paper
- **Set 1 says:** Janatian, A. et al. (2023), "Using GPT-4 to generate structured representations from legislation for legal decision support" — links arXiv 2604.17153
- **Actual at 2604.17153:** "From Legal Text to Executable Decision Models: Evaluating Structured Representations for Legal Decision Model Generation" by David Graus.
- Janatian et al. 2023 ICAIL **is** a real paper (Quebec traffic regulations + GPT-4) — but it's a different paper than the arXiv link the agent provided. The agent conflated two pieces of work.

### 4. CO2 (Co-Compliance Officer) — author looks wrong
- **Set 1 says:** Al-Kadi, M. et al. (2025), IEEE Access, DOI `10.1109/ACCESS.2025.3524177`
- **Likely actual:** authored by Turaga et al., DOI `10.1109/ACCESS.2025.3639228` (per IEEE Xplore page surfaced in search)
- Needs full verification — DOI mismatch is concerning.

### 5. De Martim JURIX 2025 — title variation, fix arXiv link
- Title has varied across arXiv versions ("Structural" vs "Hierarchical, Temporal, and Deterministic") — pick one and stick with the latest.
- arXiv ID: `2505.00039` (Set 1 omitted this; only linked the JURIX program page).

## Entries that look solid

- LKIF Core (Hoekstra et al. 2007) — correct attribution.
- Bartolini et al. JURISIN 2016 — correct attribution.
- Liga & Robaldo 2023 GPT-3 fine-tuning — correct.
- Eunomos (Boella et al. 2016) — correct.
- DPV (Pandit et al. 2024) — correct.
- D'Amato et al. JURIX 2025 (violence against women KG) — listed in JURIX 2025 program.
- Donalds, Barclay & Osei-Bryson 2018 cybercrime ontology, *Computers in Human Behavior* — correct.
- Donalds, Barclay & Osei-Bryson 2019 awareness-centered model, *IMDS* — *probably* correct, search returned the ResearchGate page but I couldn't independently confirm volume/issue.

## Coverage gaps Set 1 left open

- **OntoClean** — only "Cited-by description only". The "where we differ" passage is a paraphrase of a paraphrase. Needs a real read or at least a primary source check.
- **Akoma Ntoso / LegalRuleML** — only "Abstract + Cited-by". Athan et al. 2013 may also be the wrong primary citation; the canonical work is often credited to Palmirani, Governatori, Athan, Boley, Paschke and others across multiple papers.
- **Comparative Analysis of Africa and US Initiatives (Popoola et al.)** — agent flagged this as thin and the Donalds/Barclay/Osei-Bryson co-authorship is **not confirmed** by my searches. Set 1 itself cites only the ResearchGate landing page. May not belong in the bibliography at all.
- **Recent Caribbean / Jamaican DPA NLP** beyond Donalds et al. — Set 1 found nothing. Either the field is genuinely thin (real possibility, and a useful framing point) or the agent's search was shallow.
- **No JURIX 2024 paper** — Set 1's table cites GPT-4 fine-tuning + UN Security Council resolutions for 2024 but doesn't surface a specific paper.

## Things to ask the Set 2 agent to do

If Set 2 hasn't already covered these, slot them into the prompt before they finish:

1. **Verify the four citations flagged above** (Beyond Technical Measures, CompCQ, Janatian, CO2) — confirm or correct authors, title, journal, DOI.
2. **Find the canonical LegalRuleML paper** — likely Palmirani, Governatori et al., *Semantic Web Journal* or *AI & Law* — and the canonical Akoma Ntoso reference (Barabucci et al. or Vitali & Zeni).
3. **Read OntoClean** properly — Guarino & Welty 2002 *Communications of the ACM*, "Evaluating ontological decisions with OntoClean" — give it a real "where we differ" passage.
4. **Locate ≥1 specific JURIX 2024 paper** that fits the project's framing.
5. **Sweep for non-Donalds Caribbean compliance NLP** — Trinidad, CARICOM, OECS, regional UN-CARIB studies. If nothing is found, *say so explicitly* — it's a useful framing argument that the technical layer is genuinely missing.

## Salvageable assets from Set 1

These are good to keep regardless of citation fixes:

- The **JURIX 2023-2025 contribution-profile table** — useful framing for the paper's pitch.
- The **three "where we differ" synthesis passages** — strong scaffolding, even if specific citations need re-anchoring.
- The **pre-registration metric table** — CQC, LARS, OOPS! pitfall count, Git-PR revision ratio, FIBO-alignment fidelity. The Git-PR revision ratio is original to this project and worth pre-registering.
