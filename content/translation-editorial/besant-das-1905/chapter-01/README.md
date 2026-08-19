# Besant & Das 1905 — Chapter 1 Translation Editorial Workspace

**Phase:** Production — approved, packaged, imported  
**Status:** 47/47 verses APPROVED — production Translation package built and imported  
**Source:** `bhagavad-gita-translation-en-besant-das-1905-v1`  
**Pinned master checksum:** `7fb78b0a6b004f195c3ca61c091501084e553627c51cde1c309f2d0620ea6115`

## Current state

- Source acquired and checksummed
- Chapter 1 structurally audited (47 ONE_TO_ONE verse units)
- Editorial extraction completed
- Human review completed (mechanical fixes + 4 residual editorial decisions)
- All 47 segments APPROVED with reviewer metadata
- Production package generated: `bhagavad-gita-translation-en-besant-das-1905-chapter-01-v1`
- Package validated: structurallyValid, editoriallyValid, importable
- Imported into local PostgreSQL (47 PUBLISHED Translation rows)
- API verified (correct verseId, provider, language, translationText)
- Mobile Verse Reader verified with real Chapter 1 Translation

## Scope limits

- Only Chapter 1 is production-ready
- Chapters 2–18 have NOT been editorially audited, approved, or imported
- Swarupananda 1909 remains a separate blocked/future edition
- Full-book Package Format v1 compatibility has NOT been proven beyond Chapter 1

## Chapter 1 as golden corpus

Chapter 1 serves as the reference/golden corpus for the Translation production
pipeline. Future chapters should follow the same flow:

`source → acquisition → editorial extraction → human review → approval → package → import → API → mobile`

## Files

| File | Role |
|------|------|
| `source-extraction.jsonl` | Extraction records (pages, notes, separation, flags) |
| `segment-draft.jsonl` | Approved segment records (47 APPROVED) |
| `coverage-map.json` | Verse↔segment map and package-v1 note |
| `SHA256SUMS` | Hashes of the three structured artifacts |
| `decisions.md` | Extraction / ambiguity decisions |
| `mechanical-fixes.md` | Page-faithful transcription corrections (18 verses) |
| `editorial-review.md` | Residual editorial decisions (4 verses) |
| `final-editorial-evidence.md` | Page-image verification evidence |
| `review-checklist.md` | Compact human review support |
| `validation-report.md` | Latest validator summary |

## Validation

```bash
python3 content/translation-editorial/tools/validate_translation_segments.py \
  --workspace content/translation-editorial/besant-das-1905/chapter-01 \
  --source-id bhagavad-gita-translation-en-besant-das-1905-v1 \
  --source-checksum 7fb78b0a6b004f195c3ca61c091501084e553627c51cde1c309f2d0620ea6115 \
  --registry content/registry/sources.json
```

## Policy reminders

- Fluent free translation only — no Sanskrit, gloss, footnotes, colophons, front matter.
- All Chapter 1 units are ONE_TO_ONE → Package Format v1 compatible.
- Swarupananda workspace remains a separate frozen future edition.
