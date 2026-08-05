# `content/raw/`

Immutable downloads of candidate and rejected source corpora.

## Rules

- One source family per subdirectory (example: `sanskrit/<source-slug>/`).
- Store the original filename when practical.
- Record provenance in a local `README.md` beside the artifact.
- Register SHA-256 under `content/checksums/` before treating the download as inspected.
- **Never** edit raw files in place. Any correction belongs in a later pipeline stage, not here.

## Current contents

| Path | Status |
|------|--------|
| `sanskrit/kaggle-tarun-tiwari/` | `REJECTED_FOR_CANONICAL_IMPORT` — research/reference only |
| `sanskrit/wikisource/chapter-01/` | `ACQUIRED_UNREVIEWED` — Chapter 1 primary transcription candidate |
| `sanskrit/iit-kanpur/verse-1.1/` | `VERIFICATION_ONLY` — Verse 1.1 secondary verification reference |
| `translations/swarupananda-1909/` | `ACQUIRED_UNREVIEWED` — English Translation candidate (Chapter 1 inspected) |

See [`docs/content/DATASET_INSPECTION.md`](../../docs/content/DATASET_INSPECTION.md) for the rejected Kaggle corpus.
See [`content/raw/sanskrit/wikisource/chapter-01/README.md`](sanskrit/wikisource/chapter-01/README.md) for Wikisource provenance.
