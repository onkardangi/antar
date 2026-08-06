# ADR-012 — Translation Is a Separate Bounded Context

## Status

Accepted

## Context

Earlier architecture drafts placed translation tables under the `scripture`
schema (`scripture.translation_sources`, `scripture.translations`) and embedded
translation in Scripture Verse responses.

Implementing Translation as Scripture-owned tables would couple Sanskrit corpus
import, Verse Reader APIs, and licensed translation editions in one module.

The Translation vertical-slice foundation requires an independent package format,
importer, persistence, and read API using synthetic fixture content only.

## Decision

Translation is a separate bounded context:

```text
com.antar.translation
translation.* schema
```

Rules:

- Scripture must not depend on Translation.
- Translation may reference Verse identity only (`scripture.verses.id` FK).
- Translation owns its package format, validator, importer, provenance, and
  read-only API (`GET /api/v1/translations/verses/{verseId}`).
- No commentary, notes, AI, or Verse Reader coupling in this foundation.

Where this ADR conflicts with older draft API contracts that still embed
translation under Scripture endpoints, this ADR is canonical for Translation
ownership until those contracts are revised for Verse Reader composition.

## Consequences

- Flyway `V007` creates the `translation` schema and Translation-owned tables:
  `translation_sources`, `translations`, `content_packages`,
  `content_package_imports`. There is no `scripture.translations` table.
- `docs/architecture/03_DATA_MODEL.md` and `09_REPOSITORY_STRUCTURE.md` describe
  Translation as an implemented module owning `translation.*`.
- Mobile Verse Reader now composes Scripture and Translation independently via
  two API calls (`GET /api/v1/scripture/verses/{verseId}` and
  `GET /api/v1/translations/verses/{verseId}`). Scripture remains
  Translation-free. Translation remains optional and subordinate; missing
  Translation never blocks Scripture. No Translation ownership moved into
  Scripture. Provider/language selection remains deferred.
- V1 read API returns one published translation per Verse via stable
  provider-asc ordering; explicit language/provider selection is deferred.
