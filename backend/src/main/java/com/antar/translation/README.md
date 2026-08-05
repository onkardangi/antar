# Translation

## Purpose

Owns licensed translation editions and per-Verse translation text. References Scripture
Verse identity only (`scripture.verses.id`). Does not own Sanskrit, commentary, or Verse
Reader composition.

## Owned concepts

- Translation / TranslationId
- TranslationSource / TranslationProvider / TranslationLanguage
- TranslationText / TranslationVersion / TranslationStatus
- TranslationPackage provenance and import audit

## Implemented in this slice

- Translation domain model and `translation.*` persistence (Flyway `V007`)
- Translation Package Format v1 (`content/packages/translation/`)
- Synthetic approved fixture package only (no real translation corpus)
- Administrative importer (dry-run, transactional, idempotent, supersede, rollback)
- Read-only API: `GET /api/v1/translations/verses/{verseId}`
- Fail-closed Java/Python Package Format v1 parity gate (requires `python3`)

## V1 API limitation — provider selection

When multiple published translations exist for one Verse,
`findFirstByVerseIdAndPublicationStatusOrderByProviderAsc` returns the first row
ordered by `provider` ascending. Explicit language/provider query parameters are
deferred. Do not treat this as multi-edition product selection.

## Not in this slice

- Real English (or other) translation corpus
- Verse Reader / mobile consumption
- Commentary, notes, AI, search, guidance, journey, understanding, bookmarks, audio
- Scripture module or importer changes
- Explicit provider/language selection on the read API

## Import commands

```bash
cd backend
./mvnw -q exec:java \
  -Dexec.mainClass=com.antar.translation.infrastructure.importcmd.TranslationPackageImportMain \
  -Dexec.args="--package-path /absolute/path/to/approved-package --dry-run"

./mvnw -q exec:java \
  -Dexec.mainClass=com.antar.translation.infrastructure.importcmd.TranslationPackageImportMain \
  -Dexec.args="--package-path /absolute/path/to/approved-package"
```

Never runs on normal application startup. No public import HTTP API.
