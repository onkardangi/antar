# Chapter 1 — Validation Report

**Workspace:** `content/translation-editorial/swarupananda-1909/chapter-01/`  
**Validator:** `content/translation-editorial/tools/validate_translation_segments.py`  
**Generated:** 2026-08-05

## Summary

| Check | Result |
|-------|--------|
| Validator `ok` | **true** |
| Verse coverage | **47 / 47** |
| Uncovered verses | **0** |
| Multiply covered verses | **0** |
| Segment count | **39** |
| 1→1 segments | **33** |
| N→1 segments | **6** |
| `APPROVED` count | **0** |
| `packageReady` | **false** |
| `importReady` | **false** |

## Status counts

| Status | Count |
|--------|-------|
| UNREVIEWED | 27 |
| SOURCE_CONFLICT | 12 |
| APPROVED | 0 |

## Multi-Verse segments

| Segment ID | Label | Coverage |
|------------|-------|----------|
| `swarupananda-1909-bg-1-004-006` | I. 4. 5. 6. | 1.4–1.6 |
| `swarupananda-1909-bg-1-021-022` | I. 21—22. | 1.21–1.22 |
| `swarupananda-1909-bg-1-024-025` | I. 24—25. | 1.24–1.25 |
| `swarupananda-1909-bg-1-028-029` | I. 28—29. | 1.28–1.29 |
| `swarupananda-1909-bg-1-032-034` | I. 32—34. | 1.32–1.34 |
| `swarupananda-1909-bg-1-038-039` | I. 38. 39. | 1.38–1.39 |

## Package readiness reasons

1. approved count is 0  
2. records are not APPROVED (or approval not authorized in this phase)  
3. package v1 cannot represent N→1 segments  
4. no Translation package built in this phase  
5. N→1 segments present: 6  

## Machine-readable snapshot

```json
{
  "ok": true,
  "segmentCount": 39,
  "oneToOneSegmentCount": 33,
  "multiVerseSegmentCount": 6,
  "coveredVerseCount": 47,
  "uncoveredVerses": [],
  "multiplyCoveredVerses": [],
  "approvedCount": 0,
  "packageReady": false,
  "importReady": false,
  "statusCounts": {
    "UNREVIEWED": 27,
    "SOURCE_CONFLICT": 12
  }
}
```

Re-run:

```bash
python3 content/translation-editorial/tools/validate_translation_segments.py \
  --workspace content/translation-editorial/swarupananda-1909/chapter-01
```
