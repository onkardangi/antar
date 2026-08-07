# Verse Reader

Mobile composition of the Scripture Stack for a single Verse.

## Composition (ADR-012)

```text
GET /api/v1/scripture/verses/{verseId}      → Sanskrit
GET /api/v1/translations/verses/{verseId}   → Translation (optional)
```

Mobile owns composition. Scripture APIs remain Translation-free. Translation
failures never become Verse errors.

## Current stack

```text
Quiet Verse Reference (`Chapter N · Verse N`)
→ Sanskrit
→ Translation when present (provider attribution + text)
→ Quiet Previous / Next
```

## Loading

Primary Sanskrit loading and success share one `ScrollView` document geometry.

```text
Reference (from route)
→ Sanskrit structural placeholder bars
→ Previous / Next (disabled until Sanskrit resolves)
```

Translation placeholders appear only after Sanskrit succeeds and a Translation
request is active. They use decorative bars (no prose). Unavailable Translation
collapses silently — no section, label, or error copy.

## Behavior

- Sanskrit remains readable when Translation is missing, unpublished, slow, or failing.
- V1 attribution uses Translation `provider` (no invented publication year).
- Reading Progress records only after accepted Sanskrit success; Translation does not write progress.
- Synthetic fixture content may be present locally for a few verses; most verses omit Translation until a licensed corpus is imported.

## Not in this slice

Transliteration, commentary, reflection, Saar, Home, Continue Reading, bookmarks, AI, search, or provider selection.
