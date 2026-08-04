# Antar Content Foundation

This directory holds **content infrastructure** for future Scripture (and later Translation / Commentary) imports.

It is **not** the database. Backend Flyway migrations remain the durable product schema. Files here support provenance, editorial review, normalization, validation, and checksum verification **before** any import into `scripture.*`.

## Layout

```text
content/
├── raw/            Immutable source downloads (never edited in place)
├── editorial/      Human-reviewed working artifacts (not a production import source)
├── normalized/     Deterministic, reviewed outputs ready for import consideration
├── registry/       Source registry and approval status
├── validation/     Validation rules, Chapter draft validator, and reports
├── checksums/      SHA-256 manifests for raw and normalized artifacts
└── licenses/       License texts and license catalog entries
```

## Status (foundation)

| Concern | State |
|---------|-------|
| Directory layout | Implemented |
| Policy docs | Implemented under `docs/content/` |
| Chapter 1 editorial workspace | Scaffolded (`1.1`–`1.47`, text `null`, not import-ready) |
| Approved Bhagavad Gita corpus | **Not created** |
| Normalization / importer scripts | **Not built** (Chapter draft structural validator exists) |
| Database load of Sanskrit | **Not performed** (`scripture.verses.sanskrit_text` remains NULL until an approved import) |

## Canonical policies

| Document | Purpose |
|----------|---------|
| [`docs/content/01_SCRIPTURE_PROVENANCE.md`](../docs/content/01_SCRIPTURE_PROVENANCE.md) | Provenance requirements and source approval |
| [`docs/content/02_CONTENT_PIPELINE.md`](../docs/content/02_CONTENT_PIPELINE.md) | Pipeline stages, normalization, validation, versioning, checksums |
| [`docs/content/03_EDITORIAL_POLICY.md`](../docs/content/03_EDITORIAL_POLICY.md) | Editorial workflow, edition rules, translation/commentary policy |
| [`docs/content/DATASET_INSPECTION.md`](../docs/content/DATASET_INSPECTION.md) | Inspection of the rejected Tarun Tiwari Kaggle corpus |

## Hard rules

1. Do not modify files under `raw/` after checksum registration.
2. Do not load unapproved content into `scripture.verses` or related tables.
3. Do not invent Translation or Commentary.
4. Antar’s approved verse-segmentation tradition is **Chapter 1 = 47**, **Chapter 13 = 34**, **18 Chapters**, **700 Verses** total (see V003 Chapter seed).
5. No automated splitting, joining, or renumbering of canonical Sanskrit without an approved editorial process.
