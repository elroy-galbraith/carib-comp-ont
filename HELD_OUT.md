# Held-Out Corpus — Quarantine Policy

## Purpose

The `held-out/` directory contains the evaluation corpus that must remain
**completely isolated** from schema design, extractor development, and all
vault content until final evaluation. Contaminating this corpus invalidates
the paper's evaluation claims.

## Contents

| File | Jurisdiction | Instrument | SHA-256 |
|------|-------------|------------|---------|
| `bahamas_dpa_2003.pdf` | Bahamas | Data Protection (Privacy of Personal Information) Act, 2003 | `<see held-out/SHA256SUMS>` |

## Quarantine Rules

1. **Do not read or reference** any held-out file when designing ontology schema or writing extractors.
2. **Do not add** any held-out content to the vault (vault/*.md files).
3. **Do not run** any extraction scripts against `held-out/` until the evaluation phase.
4. The PDF itself is gitignored — only the SHA-256 hash is committed to verify corpus integrity.

## SHA-256 Verification

The committed hash file is `held-out/SHA256SUMS`. To verify your local copy
matches the locked corpus, run from the repo root:

```bash
sha256sum --check held-out/SHA256SUMS
```

## Evaluation Phase

When evaluation begins, the held-out corpus is treated as a blind test set.
Run the standard extraction pipeline against it **once**, record results, and
do not iterate the extractor based on held-out outcomes.

## Source

Official text: http://laws.bahamas.gov.bs/cms/images/LEGISLATION/PRINCIPAL/2003/2003-0003/2003-0003.pdf  
Mirror: https://www.lexbahamas.com/Data%20Protection%202003.pdf
