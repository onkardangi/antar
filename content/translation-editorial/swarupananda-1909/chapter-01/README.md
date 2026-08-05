# Swarupananda 1909 — Chapter 1 Translation Editorial Workspace

**Phase:** Translation Editorial Phase 4  
**Status:** Draft workspace — **not approved**, **not packaged**, **not imported**  
**Source:** `bhagavad-gita-translation-en-swarupananda-1909-v1`  
**Pinned master checksum:** `ab9e38c2f252574de88d55374fb8c97c7c2998b4442e9e8f32cda8713a99315e`

## Purpose

Segment-oriented normalization workspace for Chapter 1 fluent English of Swami Swarupananda, First Edition 1909. One publisher translation unit → one segment; Verse coverage may be 1→1 or publisher-asserted N→1.

## Files

| File | Role |
|------|------|
| `source-extraction.jsonl` | Extraction records (pages, notes, separation) |
| `segment-draft.jsonl` | Segment draft records |
| `coverage-map.json` | Verse↔segment map and inventory |
| `decisions.md` | Extraction / ambiguity decisions |
| `review-checklist.md` | Per-segment review checklist (unchecked) |
| `validation-report.md` | Latest validator summary |

## Policy reminders

- Do not split, synthesize, or silently duplicate publisher units.
- Package format v1 remains 1:1 only → N→1 segments are **not packageable**.
- No `APPROVED` records in this phase.
- Do not build a Translation package or import.

## Scan gap (critical)

The pinned IA/DLI Image Container PDF **skips printed pages 14–15, 17–18, and 20–21** (BookReader leaves jump 34→35→36→37 = printed 13→16→19→22). Affected segments are `SOURCE_CONFLICT` with provisional secondary PD text.

## Regenerating structured files

```bash
python3 content/translation-editorial/tools/extract_swarupananda_chapter01.py
python3 content/translation-editorial/tools/validate_translation_segments.py \
  --workspace content/translation-editorial/swarupananda-1909/chapter-01
```
