# `content/validation/`

Validation rules, Chapter draft validator, and tests for content packages.

## Files

| File | Role |
|------|------|
| `rules.md` | Human-readable validation requirements |
| `antar_verse_counts.json` | Canonical Chapter → verse_count expectations |
| `validate_chapter_draft.py` | Structural validator for Chapter `canonical-draft.jsonl` |
| `validate_chapter01_workspace.py` | Chapter 1 acquisition + extraction + comparison gates |
| `tests/` | `unittest` fixtures for validators |

Editorial Phase 2 also provides:

```bash
python3 content/editorial/tools/validate_automated_comparison.py --check-determinism
```

## Chapter draft validator

Validates editorial `canonical-draft.jsonl` files (Chapter 1 workspace first).

Checks:

- JSONL parses
- exact expected record count (47 for Chapter 1)
- chapter number always matches
- verse numbers exactly `1..N`
- `canonicalReference` matches chapter and verse
- no duplicates
- `approvalStatus` is from the allowed set
- `APPROVED` records require nonblank Sanskrit and transliteration
- unreviewed records may use `null` text
- `import_ready` is true only when all records are approved with text

Does **not** modify corpus data. Does **not** judge textual accuracy.

### Run against Chapter 1 draft

```bash
python3 content/validation/validate_chapter_draft.py \
  content/editorial/bhagavad-gita/chapter-01/canonical-draft.jsonl
```

### Run Chapter 1 workspace validation

```bash
python3 content/validation/validate_chapter01_workspace.py
```

### Run unit tests

```bash
python3 -m unittest discover content/validation/tests
python3 -m unittest discover content/acquisition/tests
python3 -m unittest discover content/normalization/tests
```

## Rules

- Validation must run against Antar’s approved identity model before import.
- Failures block `APPROVED_FOR_IMPORT`.
- Editorial workspace reports live beside the chapter (see `validation-report.md`).

## Current contents

Rules, expected verse counts, Chapter draft validator, and tests. No full-corpus import package yet.
