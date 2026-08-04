# Editorial reviews

Verse-level editorial review files for Antar’s Canonical Corpus workflow.

## Purpose

These files are **permanent historical records** of editorial decisions.

| Artifact | Role |
|----------|------|
| Review files (`content/editorial/reviews/{chapter}.{verse}.md`) | Decision history and audit trail |
| Chapter workspace JSONL (`content/editorial/bhagavad-gita/...`) | Source comparison + draft working data |
| Canonical / normalized packages (`content/normalized/`) | Product artifact for future import |
| PostgreSQL `scripture.*` | Runtime product store (import later) |

**Canonical corpus packages remain the only import source.** Review files do not feed the database directly.

## Rules

1. Do not invent Sanskrit, Translation, or Commentary.
2. Do not duplicate Sanskrit into review files unless documenting source comparison.
3. Do not mark `APPROVED` without human reviewers and an audit entry.
4. Never overwrite an existing review file via tooling.
5. Append to `# Audit Log` for every substantive change.
6. Backend/mobile and PostgreSQL are out of scope for this workflow layer.

## Layout

```text
content/editorial/reviews/
├── README.md
├── review-schema.md
├── status.md
├── 1.1.md
└── … (future verses)

content/editorial/tools/
├── compare_sources.py
├── generate_review.py
├── validate_reviews.py
├── validate_automated_comparison.py
└── tests/
```

## Commands

```bash
# Generate a review scaffold (refuses overwrite)
python3 content/editorial/tools/generate_review.py --chapter 1 --verse 1

# Automated Chapter comparison (never sets APPROVED)
python3 content/editorial/tools/compare_sources.py \
  --chapter-dir content/editorial/bhagavad-gita/chapter-01

# Optional: append automation block + audit log to existing review files
python3 content/editorial/tools/compare_sources.py \
  --chapter-dir content/editorial/bhagavad-gita/chapter-01 \
  --update-reviews

# Validate all review files
python3 content/editorial/tools/validate_reviews.py

# Validate one file
python3 content/editorial/tools/validate_reviews.py --file content/editorial/reviews/1.1.md

# Validate automated comparison outputs
python3 content/editorial/tools/validate_automated_comparison.py --check-determinism

# Tests
python3 -m unittest discover content/editorial/tools/tests
```

## Phase 2 scope

Deterministic multi-verse source comparison, audit sampling, and review preparation. Automation may recommend readiness and set `READY_FOR_REVIEW` / `SOURCE_CONFLICT` / `NEEDS_SOURCE`; it must never grant `APPROVED`.

Only Verse **1.1** currently has a review file. Status remains `UNDER_REVIEW` — **not approved**.
