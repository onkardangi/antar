# Content validation rules

These rules apply to any future normalized Scripture package before database import.

Derived from Antar Chapter seed (`V003`) and Verse identity seed (`V005`).

## Identity

1. Exactly **18** Chapters, numbers `1..18`.
2. Exactly **700** Verse records.
3. Chapter verse counts must match `antar_verse_counts.json` exactly.
4. Every Verse has canonical reference `"{chapter}.{verse}"` with no leading zeros.
5. Verse numbers within a Chapter are contiguous from `1` to that Chapter’s `verse_count`.
6. No duplicate `(chapter, verse)` identities.
7. No missing identities relative to the Antar seed set.

## Edition

8. `matches_antar_numbering` must be `true`.
9. Chapter 1 must contain **47** verses; Chapter 13 must contain **34** verses.
10. Automated split/merge/renumber to satisfy (8)–(9) is **forbidden** without approved editorial process.

## Sanskrit (when present)

11. `sanskrit_text` must be non-blank after trim when claimed present.
12. Encoding must be UTF-8.
13. Text must be NFC (or an explicitly documented approved form).
14. No literal escape artifacts (e.g. ASCII `\u200c` sequences) in Sanskrit fields.
15. No engineering placeholder prose.

## Transliteration (when present)

16. Scheme must be declared (`IAST`, `ISO_15919`, or `SIMPLIFIED_LATIN`).
17. Attribution / source id required.
18. Must map 1:1 to an Antar Verse identity.

## Translation / commentary (future)

19. Must reference a registered licensed source.
20. Must retain attribution fields required by the data model.
21. Unlicensed Translation or Commentary fails validation.

## Provenance

22. Raw SHA-256 must match `content/checksums/` and the registry entry.
23. License catalog entry must exist before `APPROVED_FOR_IMPORT`.
24. Registry status must be `APPROVED_FOR_IMPORT` (or `IMPORTED` for post-load verification).
