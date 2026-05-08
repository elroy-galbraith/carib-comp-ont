# Prototype Test Report — Caribbean Compliance Ontology v0.1

**Tested:** 2026-05-08  
**Environment:** Windows 11 Pro, Python 3.11.9, venv in worktree root  
**Deps installed:** anthropic 0.100, pyoxigraph 0.5.8, PyYAML 6.0.3, python-dotenv 1.2.2, pdfplumber 0.11.9, watchdog 6.0, gitpython 3.1.50  
**docling:** NOT installed (optional; pdfplumber fallback used)

---

## What Passes

| Script | Status | Notes |
|---|---|---|
| `scripts/to_turtle.py` | PASS | Generates well-formed Turtle from all 7 vault files |
| `scripts/load_to_oxigraph.py` | PASS | Loads 98 triples; CQ1, CQ2, CQ3 all return correct results |
| `scripts/extractor.py` (dry-run) | PASS (with workaround) | Correct JSON output; API key issue needs fix — see Bug 1 |
| `scripts/curator.py` | NOT RUN (live) | Static review reveals two bugs — see Bugs 2 & 3 |

---

## Bugs

### Bug 1 — BLOCKER: extractor.py and curator.py ignore .env when env var pre-exists (empty)

**Files:** `scripts/extractor.py:37`, `scripts/curator.py:38`  
**Symptom:** `TypeError: Could not resolve authentication method` when running `extractor.py` or `curator.py`.  
**Root cause:** `load_dotenv()` does not override existing environment variables by default. The environment
already has `ANTHROPIC_API_KEY=""` (empty string) set — possibly by the shell profile or Claude Code session.
Because the variable exists (even empty), `load_dotenv()` skips it and the Anthropic client sees an empty key.

**Fix:** Add `override=True` to both calls.

```python
# extractor.py line 37  /  curator.py line 38
load_dotenv(Path(__file__).parent.parent / ".env", override=True)
```

**Workaround (manual):** `$env:ANTHROPIC_API_KEY = (Get-Content .env -Raw).Split("=",2)[1].Trim()`

---

### Bug 2 — CRASH: curator.py prints U+2550 box-drawing character — UnicodeEncodeError on Windows

**File:** `scripts/curator.py` lines 156, 171, 178  
**Symptom:** `UnicodeEncodeError: 'charmap' codec can't encode character '═'` crashes curator on Windows cp1252 terminal.  
**Root cause:** `log.info("═" * 50)` uses U+2550 (BOX DRAWINGS DOUBLE HORIZONTAL), which has no cp1252 mapping.
The same issue affects `—` (U+2014 em dash) in log messages at lines 116, 140, 217.

**Fix:** Replace with ASCII equivalents.

```python
# Lines 156, 171, 178 — replace:
log.info("=" * 50)

# Lines 116, 140, 217 — replace em dash with hyphen:
log.info("branch %s already exists - resetting to HEAD", branch_name)
# etc.
```

---

### Bug 3 — WRONG: dpa2020_ico.md has property with wrong domain direction

**File:** `vault/dpa2020_ico.md` line 13  
**Symptom:** Generates the triple `ccoe:dpa2020_ico cco:enforcedBy ccoe:dpa2020`. The ontology defines
`cco:enforcedBy` with `rdfs:domain cco:Statute` — a Regulator is not a valid subject for this property.  
**Root cause:** The vault entry for the ICO (Regulator) has `properties.enforcedBy: dpa2020`, which
is intended to document the relationship but has the direction backwards. The correct triple
(`ccoe:dpa2020 cco:enforcedBy ccoe:dpa2020_ico`) is already present in `vault/dpa2020.md`.

**Fix:** Remove the `enforcedBy` entry from dpa2020_ico.md:

```yaml
properties:
  # remove: enforcedBy: dpa2020   <-- wrong direction; already in dpa2020.md
```

---

### Bug 4 — DATA: Four §2 definitions reference a non-existent Provision entity (dpa2020_s2)

**Files:** `vault/dpa2020_s2_data_controller.md`, `dpa2020_s2_data_processor.md`, `dpa2020_s2_data_subject.md`, `dpa2020_s2_personal_data.md`  
**Symptom:** All four files have `properties.definedIn: dpa2020_s2`, generating triples like
`ccoe:dpa2020_s2_data_controller cco:definedIn ccoe:dpa2020_s2`. But `ccoe:dpa2020_s2` (the §2 Provision)
is not defined anywhere in the vault or schema — it is a dangling IRI reference.  
**Impact:** SPARQL queries that traverse `cco:definedIn` will find no match for the range entity.
Current CQs are unaffected (they filter on `dcterms:isPartOf ccoe:dpa2020` instead), but any future
query like "what provision defines X?" will silently return nothing.

**Fix (preferred):** Add a `vault/dpa2020_s2.md` Provision entry:
```yaml
class: Provision
id: dpa2020_s2
label: "DPA 2020 §2 — Interpretation"
source_statute: dpa2020
source_section: "§2"
source_text: "In this Act, unless the context otherwise requires—"
properties:
  {}
```

**Fix (minimal):** Or change `definedIn: dpa2020_s2` → `definedIn: dpa2020` in all four files
(coarser but at least resolves to an existing entity).

---

### Bug 5 — PACKAGING: pyoxigraph lower bound is too broad in requirements.txt

**File:** `requirements.txt` line 3  
**Current:** `pyoxigraph>=0.3.22`  
**Problem:** The API changed between 0.3.x and 0.5.x. The code uses `pyoxigraph.RdfFormat.TURTLE`
(0.5.x enum), which does not exist in 0.3.x. A fresh install on a machine that happens to resolve
to 0.3.x (e.g., an older pip cache) would install fine but crash at runtime.

**Fix:**
```
pyoxigraph>=0.5.0
```

---

## Minor Issues (non-breaking)

### M1 — docling is listed as required but is effectively optional

`requirements.txt` lists `docling>=2.0.0` with no `; extra == "..."` marker.
On Windows, docling has complex ML dependencies and often fails to install.
The `extractor.py` already handles the `ImportError` gracefully, falling through to `pdfplumber`.

**Suggestion:** Mark it optional in the file comment, or split into an extras group:
```
# Optional — layout-aware PDF extraction (falls back to pdfplumber)
# docling>=2.0.0
```

### M2 — curator.py will fail if run from a git worktree

`open_proposal_branch()` calls `repo.git.checkout("main")`, which fails when `main` is
already checked out in the parent working tree (git prevents two worktrees from sharing a branch).
This only affects running curator from a worktree context (e.g., this test session).  
No fix needed for normal use — just document that curator.py must run from the main working tree.

### M3 — Terminal shows § and — as ? on cp1252

Output from `load_to_oxigraph.py` and `to_turtle.py` displays `§` and `—` as `?` in Windows
PowerShell with cp1252 encoding. This is cosmetic only — file content is correct UTF-8.  
The section references (`§1`, `§2`, etc.) are stored and loaded correctly; only the terminal
rendering is affected. No code change needed; can be resolved by running in Windows Terminal
(which defaults to UTF-8) or adding `chcp 65001` to the session setup.

---

## Priority Fix Order

1. **Bug 1** — `load_dotenv override=True` — blocks all extractor/curator usage
2. **Bug 2** — ASCII separators in curator.py — crashes curator on Windows
3. **Bug 5** — pyoxigraph version pin — prevents safe fresh installs
4. **Bug 3** — Remove wrong `enforcedBy` from dpa2020_ico.md — data correctness
5. **Bug 4** — Add dpa2020_s2.md Provision entity — completeness for future queries
