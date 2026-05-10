# Fix-up prompt for Set 1 deep-research agent

Copy everything below the line.

---

## Task

I need you to fix four citation errors in the literature review you produced. **Do not re-do the lit review.** Just verify, correct, and report back the corrected entries in the same format you used originally.

For each entry below, return:

- The corrected `Citation:` line (full BibTeX-ready)
- The corrected `Link:` (DOI or canonical URL)
- A one-sentence note saying what you changed and how you confirmed it (which page, which database)
- If the entry should be **dropped** because the paper doesn't support the framing you gave it, say so plainly and propose a replacement from the same bucket.

## The four entries

### 1. "Beyond technical measures" (Donalds, Barclay & Osei-Bryson)

You cited it as *Information Technology & People*, 31(1), 58-73, 2022, DOI `10.1108/ITP-03-2020-0112`. That journal/DOI combination does not match the paper. The paper appears to actually be in *European Journal of Information Systems*, 31(1), 58-73, 2022, DOI `10.1080/0960085X.2021.1978344`. Confirm or correct.

### 2. "LLM-authored Competency Questions (CompCQ)" — arXiv:2604.16258

You attributed this paper to "Bezerra, F., et al. (2024)" with the title "LLM-authored Competency Questions: A Multi-faceted Characterization and Evaluation". The actual paper at arXiv:2604.16258 is by Alharbi, R., Tamma, V., Payne, T. R., & de Berardinis, J., titled "Characterising LLM-Generated Competency Questions: a Cross-Domain Empirical Study using Open and Closed Models". Confirm and rewrite the citation. The "what they do / where we differ" prose can probably stay if it matches the actual paper.

### 3. "Janatian et al. 2023 ICAIL" — wrong arXiv link

You linked arXiv 2604.17153, but that ID actually points to a paper by David Graus titled "From Legal Text to Executable Decision Models: Evaluating Structured Representations for Legal Decision Model Generation". Janatian et al. 2023 ICAIL **is** a real paper (about Quebec traffic regulations + GPT-4) — find its actual citation and DOI/arXiv. Decide whether the better entry for this slot is Janatian et al., the Graus paper at 2604.17153, or both as separate entries.

### 4. CO2 (Co-Compliance Officer) — author and DOI suspect

You cited it as "Al-Kadi, M., et al. (2025), IEEE Access, DOI 10.1109/ACCESS.2025.3524177". The IEEE Xplore page suggests the actual first author may be Turaga (not Al-Kadi) and the DOI may be `10.1109/ACCESS.2025.3639228`. Verify against IEEE Xplore directly and correct.

## Output format

Return one block per entry, in the same format as your original report. Then end with a one-paragraph confidence note: any other citations in the report you're now uncertain about, given that these four had errors.

## Constraint

- Do not pull substantive content from the **Bahamas Data Protection Act 2003** — bibliographic mention only, as before.
