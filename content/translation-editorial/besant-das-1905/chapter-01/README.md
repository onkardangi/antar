# Besant & Das 1905 — Chapter 1 Translation Editorial Workspace

**Phase:** Translation Editorial extraction  
**Status:** Draft workspace — **not approved**, **not packaged**, **not imported**  
**Source:** `bhagavad-gita-translation-en-besant-das-1905-v1`  
**Pinned master checksum:** `7fb78b0a6b004f195c3ca61c091501084e553627c51cde1c309f2d0620ea6115`

## Purpose

1→1 fluent English free-translation drafts for Chapter 1 (Verses `1.1`–`1.47`) of Annie Besant & Bhagavan Das, *The Bhagavad-Gita* (1905).

Page images of IA item `bhagavadgitawith00londiala` are authoritative. OCR is locator-only.

## Files

| File | Role |
|------|------|
| `source-extraction.jsonl` | Extraction records (pages, notes, separation, flags) |
| `segment-draft.jsonl` | Segment draft records (validator input) |
| `coverage-map.json` | Verse↔segment map and package-v1 note |
| `SHA256SUMS` | Hashes of the three structured artifacts |
| `decisions.md` | Extraction / ambiguity decisions |
| `review-checklist.md` | Compact human review support |
| `validation-report.md` | Latest validator summary |

## Regenerating structured files

```bash
python3 content/translation-editorial/tools/extract_besant_das_chapter01.py
python3 content/translation-editorial/tools/validate_translation_segments.py \
  --workspace content/translation-editorial/besant-das-1905/chapter-01 \
  --source-id bhagavad-gita-translation-en-besant-das-1905-v1 \
  --source-checksum 7fb78b0a6b004f195c3ca61c091501084e553627c51cde1c309f2d0620ea6115 \
  --registry content/registry/sources.json
```

Re-running without source changes must leave `segment-draft.jsonl`, `source-extraction.jsonl`, and `coverage-map.json` byte-identical (`SHA256SUMS`).

## Policy reminders

- Fluent free translation only — no Sanskrit, gloss, footnotes, colophons, front matter.
- All Chapter 1 units are **ONE_TO_ONE** → Package Format v1 compatible **after** approval.
- No `APPROVED` records in this phase.
- Do not build a Translation package or import.
- Swarupananda workspace remains a separate frozen future edition.