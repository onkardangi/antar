# Antar Content Packages

Immutable release artifacts for approved Scripture content.

A controlled backend importer consumes **packages only**. Editorial workspaces,
source comparisons, review files, and raw source files must never be imported
directly.

## Pipeline

```text
Raw Sources
    → Editorial Workspace
    → Approved Canonical Records
    → Immutable Package
    → Backend Importer (admin CLI)
    → PostgreSQL
```

| Stage | Role |
|-------|------|
| Raw Sources | Immutable downloads under `content/raw/` |
| Editorial Workspace | Human review under `content/editorial/` |
| Approved Canonical Records | Verses with human `APPROVED` decisions only |
| Immutable Package | This directory — the only importer input |
| Backend Importer | Package Format v1 administrative import (never auto-start) |
| PostgreSQL | Durable product store |

## Rules

1. **Packages are immutable release artifacts.** Once published under a package
   ID, contents must not be rewritten. Corrections ship as a new version
   (for example `bhagavad-gita-chapter-01-v2`).
2. **The importer consumes packages only.** Not editorial JSONL, not review
   Markdown, not raw downloads.
3. **Package validation is not scholarly approval.** Structural checks prove
   format integrity. Editorial approval must already have happened upstream.
4. **Editorial approval precedes packaging.** The builder refuses pending and
   conflicted records. Chapter 1 currently has **zero** approved Verses, so a
   real Chapter 1 package build fails.
5. **Revoked packages remain preserved** for audit history (`REVOKED` status).
6. **Only `APPROVED` packages may be imported.** `DRAFT` packages
   are never importable and are never persisted by the importer.

## Package layout

Each package directory contains exactly four files — no extras:

```text
<package-id>/
├── manifest.json
├── verses.jsonl
├── provenance.json
└── SHA256SUMS
```

The directory name must equal `packageId` (example:
`bhagavad-gita-chapter-01-v1`).

### Allowed statuses

| Status | Meaning |
|--------|---------|
| `DRAFT` | Format-complete candidate; never importable |
| `APPROVED` | Editorial evidence complete; only status a future importer may load |
| `SUPERSEDED` | Replaced by a newer package version |
| `REVOKED` | Withdrawn; retained for audit |

## Schemas

Machine-readable contracts live in `schema/`:

- `package-manifest.schema.json`
- `verse-record.schema.json`
- `provenance.schema.json`
- `checksums.schema.json`

## Checksums

- Algorithm: **SHA-256**, lowercase hex.
- `SHA256SUMS` lists `manifest.json`, `provenance.json`, and `verses.jsonl`
  (lexicographic filename order when written).
- Combined `packageChecksum` in the manifest is:

  ```text
  SHA-256( bytes(verses.jsonl) || bytes(provenance.json) )
  ```

  Manifest is excluded from the combined digest to avoid circular hashing.

Identical approved inputs must rebuild to byte-identical content files and
identical checksums when `createdAt` and other declared fields are held fixed.

## Tools

```bash
# Validate a package
python3 content/packages/tools/validate_package.py \
  content/packages/examples/bhagavad-gita-chapter-01-v1-example

# Build from approved editorial records (refuses pending/conflicted)
python3 content/packages/tools/build_package.py \
  --approval-manifest path/to/approval-manifest.json \
  --approved-records path/to/approved-records.jsonl \
  --output-parent content/packages \
  --package-id bhagavad-gita-chapter-01-v1 \
  --chapter-number 1 \
  --package-status DRAFT \
  --created-at 2026-08-04T00:00:00Z

# Attempt real Chapter 1 workspace build (expected failure today)
python3 content/packages/tools/build_package.py \
  --chapter-workspace content/editorial/bhagavad-gita/chapter-01 \
  --package-id bhagavad-gita-chapter-01-v1 \
  --chapter-number 1 \
  --created-at 2026-08-04T00:00:00Z

# Tests (stdlib unittest only)
python3 -m unittest discover content/packages/tools/tests
```

## Backend importer

See `backend/src/main/java/com/antar/scripture/README.md` for dry-run and import
commands. Summary:

- Java Package Format v1 validation (parity-tested against this Python validator)
- Backend `./mvnw verify` requires Python 3 for the fail-closed Java/Python parity gate; runtime import does not spawn Python
- Requires importable + no warnings
- Rejects non-null transliteration in importer v1 (`UNSUPPORTED_CONTENT_LAYER`)
- Validation / CLI errors use stable path-free messages
- Dry-run failures retain `dryRun=true` and write nothing
- Never runs on normal application startup
- No public Reader import API
- Real Chapter 1 is still not importable (example remains `DRAFT`; no approved corpus)

```bash
cd backend
./mvnw -q exec:java \
  -Dexec.mainClass=com.antar.scripture.infrastructure.importcmd.ScripturePackageImportMain \
  -Dexec.args="--package-path /absolute/path/to/approved-package --dry-run"
```

## Example

`examples/bhagavad-gita-chapter-01-v1-example/` is a **synthetic DRAFT** package
using non-scriptural fixture text. It documents the format. It is not an
approved Bhagavad Gita corpus and must not be imported.

## Implementation status

| Item | Status |
|------|--------|
| Package format + schemas | Implemented |
| Builder / validator / tests | Implemented |
| Synthetic example package | Present (`DRAFT`, not importable) |
| Real Chapter 1 approved package | **Not present** (0 Verses approved) |
| Database importer | **Implemented** (admin CLI; synthetic fixtures in tests) |
| PostgreSQL production Sanskrit load | **Not performed** |
