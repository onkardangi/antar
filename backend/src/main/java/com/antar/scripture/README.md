# Scripture

## Purpose

Owns canonical Bhagavad Gita content and source metadata. Scripture is the source of truth for verses and chapters.

## Owned concepts

- Chapter
- Verse (not yet implemented)
- Sanskrit text, transliteration, translation (not yet implemented)
- Translator and commentary source metadata (not yet implemented)
- Canonical relationships

## Implemented in this slice

- Chapter domain model (`Chapter`, `ChapterId`, `ChapterNumber`, `PublicationStatus`)
- `scripture.chapters` persistence via Flyway
- Seed of all 18 canonical Chapter metadata rows
- Reader Chapter query APIs:
  - `GET /api/v1/scripture/chapters`
  - `GET /api/v1/scripture/chapters/{chapterId}`
  - `GET /api/v1/scripture/chapters/by-number/{chapterNumber}`

## Expected dependencies

- Platform (shared Problem Details response model)
- Shared

Other modules consume Scripture through published query interfaces, never through infrastructure.

## Current status

Chapter persistence and Reader Chapter retrieval APIs are implemented. Verse persistence and Verse APIs are not implemented yet.
