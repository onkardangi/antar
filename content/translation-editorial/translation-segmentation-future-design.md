# Translation Segmentation — Future Design Implications

**Status:** Design notes only — **no implementation in Phase 3**  
**Constraint:** Do not change package v1, importers, APIs, mobile, or V007 in this phase

---

## 1. Package implications (future)

Current package v1 (`translations.jsonl`) requires one record per `canonicalReference` with its own `translationText` ([`translation-record.schema.json`](../packages/translation/schema/translation-record.schema.json)). That shape **cannot** honestly represent N:1 Segments without Options A or B (both forbidden).

### Future package should represent (conceptual)

| Field | Purpose |
|-------|---------|
| `segmentId` | Stable id within package / source version |
| `coverage` | Ordered list of `canonicalReference` values (size ≥ 1) |
| `publisherLabel` | Exact label string when present (`I. 21-22.`) |
| `translationText` | Single publisher fluent unit |
| `editorialMetadata` | Decision id, approval checksum, evidence pointers |
| `sourceIds` / checksums | Unchanged provenance pattern |

### Compatibility sketch (not a schema change today)

```text
segments.jsonl
  { "segmentId": "...", "coverage": ["1.4","1.5","1.6"], "translationText": "...", ... }

verse_index.jsonl   # optional derived projection
  { "canonicalReference": "1.5", "segmentId": "..." }
```

**1:1** is just `coverage.length == 1`.

Package format version bump + ADR when implemented. **Do not redesign package v1 in this phase.**

### Until then

- Do not emit N:1 content into package v1.  
- Do not duplicate or split to fake compliance.

---

## 2. Importer implications (policy only)

When a future segment-aware package exists, the importer SHOULD:

1. Validate each Segment’s coverage references existing Scripture Verse identities.  
2. Reject coverage that invents Verses or mismatches Antar counts.  
3. Reject overlapping coverage within the same source version (two Segments claiming `1.5`) unless a future explicit multi-rendering model is approved.  
4. Persist Segment text **once**; persist verse→segment links as references.  
5. Fail closed on Options A/B smells (identical text forced onto adjacent Verses without segment metadata; fragmented sentences marked as independent Verses without evidence).  
6. Keep attribution on the Translation source / Segment.

Current importer (verse-row fixtures only): **unchanged**; must not be taught to duplicate combined English “to make tests green” for real corpora.

---

## 3. API implications (policy only)

Today: `GET /api/v1/translations/verses/{verseId}` returns one published translation row for that Verse (foundation).

### Future behaviour for N:1

When Verse `1.5` is covered by Segment `1.4–1.6`:

**Recommended approach — server expansion / resolution**

```text
GET .../verses/{verseId}
  → returns the covering Segment’s translationText
  → includes coverage metadata: from/to or list of references
  → includes segmentId
```

So the client asks by Verse (Reader-primary) and receives publisher-faithful text plus span metadata.

**Alternatives considered**

| Approach | Notes |
|----------|-------|
| Server expansion (recommended) | Matches Verse-addressable Read journey; one round trip |
| Segment-only API + client join | More flexible; heavier client; still need verse index |
| Client composition of three Verse payloads | Fails unless B-duplication exists — rejected |

Do not implement here. Explicit provider selection remains deferred (ADR-012).

---

## 4. Mobile / Reader implications (policy only)

For Verses `1.4`, `1.5`, `1.6` sharing one Segment:

1. Each Verse screen shows **that Verse’s Sanskrit** (Scripture).  
2. Translation panel shows the **same Segment English** on all three.  
3. UI SHOULD disclose coverage (“Translation covers 1.4–1.6”) so Readers are not misled.  
4. Client MUST NOT slice the English string per Verse.  
5. If Segment unpublished, show Translation unavailable — never invent filler.

Contemplative product fit: silence / unavailability > false precision.

---

## 5. Data-model implications (future; not V007 now)

Conceptual (not a migration):

```text
translation.translation_segments
  id, source_id, content_version, translation_text, publisher_label, ...

translation.translation_segment_verses
  segment_id, verse_id, ordinal_in_coverage
```

Or a single JSON coverage array if preferred later.

Current `translation.translations` verse-FK rows remain foundation; evolving them requires a deliberate ADR + migration **outside this phase**.

---

## 6. Future compatibility by candidate edition

| Source | Why Option C generalizes |
|--------|---------------------------|
| **Swarupananda 1909** | Explicit combined labels; mix of 1:1 and N:1 |
| **Besant & Das 1905** | Predominantly 1:1 free-translation lines; Segments mostly size 1; policy still holds |
| **Telang SBE 1882** | Prose may lack crisp labels; Segments only with documented evidence; may defer Verses rather than invent |
| **Arnold *Song Celestial*** | Not Verse-native; policy forbids inventing verse alignment — remains poor primary Verse Translation (Phase 1) |
| **Future licensed modern editions** | Whatever grouping the license/edition prints becomes Segment coverage |

---

## 7. Sequencing relative to product slices

```text
Policy (this phase)
  → segment-aware package design (future)
  → normalization of 1:1 then N:1 Segments
  → importer + persistence support
  → API coverage metadata
  → mobile disclosure UX
```

No step may reintroduce Option A or B.

---

## 8. Testing implications (future)

- Fixtures should include at least one N:1 Segment once format exists.  
- Validator rejects overlapping coverage and empty coverage.  
- Importer tests prove single text storage with multi-Verse resolution.  
- API tests prove `1.4`, `1.5`, `1.6` return identical `segmentId` and text.
