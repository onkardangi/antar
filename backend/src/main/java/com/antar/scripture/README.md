# Scripture

## Purpose

Owns canonical Bhagavad Gita content and source metadata. Scripture is the source of truth for verses and chapters.

## Owned concepts

- Chapter
- Verse
- CanonicalReference
- Sanskrit text (nullable until licensed corpus import)
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

## Temporary product data

- `sanskrit_text` is seeded as `NULL`. `NULL` means the approved Sanskrit corpus has not yet been imported. Engineering placeholder prose must never be stored in this column, indexed as Scripture, or returned by future canonical-content queries.
- Chapter-screen `previewText` is returned as the constant `Verse preview unavailable` until Translation content exists. It is not a persisted Verse column and must not be mistaken for Scripture.
- Chapter `shortIntent` remains the approved editorial orientation field (not renamed to `thematicIntroduction`).

## Future Verse Reader requirement

The Verse Reader slice must not display full Verse content until approved Sanskrit is present (non-`NULL` `sanskrit_text`) and licensed Translation / Transliteration content is available where the product requires them. Identity-only Verse rows are sufficient for Chapter listing; they are not sufficient for the Verse Reader.

## Expected dependencies

- Platform (shared Problem Details response model)
- Shared

Other modules consume Scripture through published query interfaces, never through infrastructure.

## Current status

Chapter and Verse identity persistence with Reader Chapter and Chapter-verse listing APIs are implemented. Full Verse reader content (licensed Sanskrit, Transliteration, Translation), Verse-by-reference lookup, and commentary are not implemented yet.
