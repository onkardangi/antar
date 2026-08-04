# `content/editorial/`

Human-reviewed working artifacts for building Antar’s canonical Scripture corpus.

## Role

Editorial workspaces hold identity scaffolds, source comparisons, draft Verse text, decisions, and review checklists **before** any package is promoted to `content/normalized/` or imported into PostgreSQL.

This directory is **not** a production import source.

## Rules

1. Do not invent Sanskrit, Translation, or Commentary.
2. Do not automate split, merge, or renumber of source verses.
3. Use `null` for missing text — never placeholder prose.
4. Approved content requires human review and approved source evidence.
5. Backend/mobile import happens only from later approved normalized packages.

## Layout

```text
editorial/
├── AUTOMATED_REVIEW_POLICY.md
├── normalization-policy.json
├── reviews/            Verse review files (decision history / audit trail)
├── tools/              compare_sources.py, generate_review.py, validate_*.py
└── bhagavad-gita/
    └── chapter-01/     Chapter 1 workspace (47 Verse identities)
```

Chapters 2–18 workspace packages are not created yet. Review files may be added verse-by-verse.

## Phase 2 — automated comparison

```bash
python3 content/editorial/tools/compare_sources.py \
  --chapter-dir content/editorial/bhagavad-gita/chapter-01

python3 content/editorial/tools/validate_automated_comparison.py --check-determinism
```

Automated classification is not scholarly approval. Final `APPROVED` remains human-only.
