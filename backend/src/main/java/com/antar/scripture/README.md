# Scripture

## Purpose

Owns canonical Bhagavad Gita content and source metadata. Scripture is the source of truth for verses and chapters.

## Owned concepts

- Chapter
- Verse
- CanonicalReference
- Sanskrit text (nullable until licensed corpus import)
- Content package provenance (`content_packages`, `content_package_imports`)
- Transliteration, translation (not yet implemented)
- Translator and commentary source metadata (not yet implemented)
- Canonical relationships

## Implemented in this slice

- Chapter domain model (`Chapter`, `ChapterId`, `ChapterNumber`, `PublicationStatus`)
- Verse domain model (`Verse`, `VerseId`, `VerseNumber`, `CanonicalReference`)
- `scripture.chapters` and `scripture.verses` persistence via Flyway
- Seed of all 18 canonical Chapter metadata rows
- Seed of all Verse identities matching Chapter `verseCount` (700 total)
- Reader Chapter query APIs:
  - `GET /api/v1/scripture/chapters`
  - `GET /api/v1/scripture/chapters/{chapterId}`
  - `GET /api/v1/scripture/chapters/by-number/{chapterNumber}`
- Reader Chapter Verse listing API:
  - `GET /api/v1/scripture/chapters/{chapterId}/verses`
- Reader Verse detail API (Sanskrit-only MVP):
  - `GET /api/v1/scripture/verses/{verseId}`
  - Returns published Verse with imported Sanskrit only
  - 404 when Verse is unknown, unpublished, or Sanskrit is missing
- **Scripture Content Importer v1** (administrative, packages only):
  - Package Format v1 validation (Java mirror of the Python package contract; not a full JSON Schema engine)
  - Transactional, idempotent import of `APPROVED` / importable packages
  - Package + import provenance tables (`V006`); FAILED audits do **not** create `content_packages`
  - At most one active `APPROVED` package per scripture + Chapter (partial unique index)
  - Verse lineage columns (`source_package_id`, `source_package_checksum`) with FK to `content_packages`
  - Controlled CLI entry point (never runs on normal app startup)

## Temporary product data

- `sanskrit_text` is seeded as `NULL`. `NULL` means the approved Sanskrit corpus has not yet been imported. Engineering placeholder prose must never be stored in this column, indexed as Scripture, or returned as Reader Scripture. The Verse detail API returns 404 when Sanskrit is absent.
- Chapter-screen `previewText` is returned as the constant `Verse preview unavailable` until Translation content exists. It is not a persisted Verse column and must not be mistaken for Scripture.
- Chapter `shortIntent` remains the approved editorial orientation field (not renamed to `thematicIntroduction`).
- Verse detail MVP returns Sanskrit only — no Translation, Commentary, Transliteration, or personalization.

## Content package import

```text
Approved Package
  → Validate (Package Format v1)
  → Dry Run (optional; zero DB writes)
  → Transactional Import
  → Provenance Record
  → Verification
```

Rules:

- Only packages with `structurallyValid`, `editoriallyValid`, `importable`, and **no warnings** are accepted.
- `DRAFT` packages are rejected and never persisted.
- Package validation is **not** scholarly approval.
- The importer consumes **package directories only** — never raw sources, editorial workspaces, review files, or DRAFT packages.
- Non-null transliteration is rejected with `UNSUPPORTED_CONTENT_LAYER` until `scripture.transliterations` exists.
- Imports never run automatically at application startup.
- There is **no** public Reader HTTP import API.
- Seeded Verse rows keep `sanskrit_text` NULL until an approved package is imported via the CLI (for example Chapter 1). Editorial workspaces are never import inputs.

### Dry run / import commands

From the repository root (backend module), with local Compose Postgres/Redis available:

```bash
# Dry run (validation + change counts; zero database writes)
cd backend
./mvnw -q exec:java \
  -Dexec.mainClass=com.antar.scripture.infrastructure.importcmd.ScripturePackageImportMain \
  -Dexec.args="--package-path /absolute/path/to/approved-package --dry-run"

# Real import (single transaction on success)
./mvnw -q exec:java \
  -Dexec.mainClass=com.antar.scripture.infrastructure.importcmd.ScripturePackageImportMain \
  -Dexec.args="--package-path /absolute/path/to/approved-package"
```

Exit codes: `0` success (including successful dry-run), non-zero failure. Summary output excludes Verse text.

Optional Spring properties may still be passed as `--spring.*` / `--antar.*` for datasource overrides.

### Package Format v1 validation parity

Java validation mirrors Package Format v1 rules used by
`content/packages/tools/validate_package.py`. **Python 3 is required** for the
Java/Python parity gate during `./mvnw verify` (backend CI and local verification).
Runtime importer execution does **not** spawn Python. Normal application startup
does **not** run imports.

Validation and CLI failure messages use stable path-free text (no absolute paths,
no Verse payload dumps). Dry-run failures retain `dryRun=true` and perform zero
database writes.

Always treat the Python tool + schemas under `content/packages/` as the format
contract source.

```bash
python3 content/packages/tools/validate_package.py path/to/package --json
python3 -m unittest discover content/packages/tools/tests
```

## Future Verse Reader requirement

The Verse Reader slice must not display full Verse content until approved Sanskrit is present (non-`NULL` `sanskrit_text`) and licensed Translation / Transliteration content is available where the product requires them. Identity-only Verse rows are sufficient for Chapter listing; they are not sufficient for the Verse Reader.

## Expected dependencies

- Platform (shared Problem Details response model)
- Shared

Other modules consume Scripture through published query interfaces, never through infrastructure.

## Current status

Chapter and Verse identity persistence with Reader Chapter and Chapter-verse listing APIs are implemented. The content importer can load synthetic APPROVED packages in tests; production Sanskrit import awaits an approved immutable package. Full Verse reader content (licensed Transliteration, Translation), Verse-by-reference lookup, and commentary are not implemented yet.
