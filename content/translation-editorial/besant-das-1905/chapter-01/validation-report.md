# Chapter 1 — Validation Report

**Workspace:** `content/translation-editorial/besant-das-1905/chapter-01/`  
**Validator:** `content/translation-editorial/tools/validate_translation_segments.py`  
**Generated:** 2026-08-07

## Summary

| Check | Result |
|-------|--------|
| Validator `ok` | **true** |
| Verse coverage | **47 / 47** |
| Uncovered verses | **0** |
| Multiply covered | **0** |
| Segment count | **47** |
| 1→1 segments | **47** |
| N→1 segments | **0** |
| `APPROVED` count | **0** |
| `packageReady` | **false** |
| `importReady` | **false** |

## Status counts

- `UNREVIEWED`: 47

## Package readiness notes

Coverage map records `packageFormatV1Compatible: true` because Chapter 1 is all ONE_TO_ONE.
Validator still reports `packageReady: false` until editorial approval and package build.

## Machine-readable snapshot

```json
{
  "approvedCount": 0,
  "coveredVerseCount": 47,
  "deterministicKeyOrder": [
    "segmentId",
    "coveredVerseNumbers",
    "coveredCanonicalReferences"
  ],
  "errors": [],
  "expectedVerseCount": 47,
  "extractionUnitCount": 47,
  "importReady": false,
  "multiVerseSegmentCount": 0,
  "multiVerseSegmentIds": [],
  "multiplyCoveredVerses": [],
  "ok": true,
  "oneToOneSegmentCount": 47,
  "packageReadinessReasons": [
    "approved count is 0",
    "records are not APPROVED (or approval not authorized in this phase)",
    "no Translation package built in this phase",
    "structurally packageFormatV1Compatible, but not packageReady until APPROVED + package build"
  ],
  "packageReady": false,
  "segmentCount": 47,
  "statusCounts": {
    "UNREVIEWED": 47
  },
  "uncoveredVerses": [],
  "warnings": [],
  "workspace": "content/translation-editorial/besant-das-1905/chapter-01"
}
```

