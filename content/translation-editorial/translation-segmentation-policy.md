# Antar Translation Segmentation Policy

**Status:** Accepted (content policy)  
**Applies to:** All Translation sources Antar may import  
**Does not:** Change package v1, importers, APIs, or database in this phase

---

## 1. Purpose

Scripture Verse identities in Antar are fixed (`chapter.verse`, Chapter 1 = 47, Chapter 13 = 34, 700 Verses).

Traditional Translation editions do not always emit one English paragraph per Verse. Some print **combined labels** (e.g. Swarupananda `I. 21-22.`) with a single English rendering covering several ślokas.

That is an **editorial segmentation** fact, not a numbering-tradition mismatch.

This policy defines how Antar represents such text without inventing wording or boundaries.

---

## 2. Definitions

| Term | Meaning |
|------|---------|
| **Verse identity** | Antar canonical reference `C.V` owned by Scripture |
| **Publisher unit** | The English (or other) Translation prose block as printed for a labeled span — fluent rendering only; not word-by-word gloss, not commentary |
| **Translation Segment** | Antar’s canonical unit of Translation content: exactly one publisher unit + provenance + the set of Verse identities it covers |
| **Coverage set** | Ordered list of Verse identities covered by one Segment (size ≥ 1) |
| **1:1 Segment** | Coverage set size = 1 |
| **N:1 Segment** | Coverage set size > 1 (many Verses → one Segment) |
| **Combined label** | Publisher label such as `I. 32—34.` asserting an N:1 unit |

---

## 3. Allowed relationships

| Relationship | Allowed? | When |
|--------------|----------|------|
| One Verse → one Segment | **Yes** | Default for most Verses in most editions |
| Many Verses → one Segment | **Yes** | Only when the **publisher** presents one English unit for that span (combined label or equivalent explicit grouping) |
| One Verse → many Segments (same source, same language, same edition) | **No** (V1 product rule) | Do not store alternate wordings of the same Verse as multiple Segments within one Translation source version |
| Mixed 1:1 and N:1 within one source | **Yes** | Normal (e.g. Swarupananda Chapter 1) |
| Artificial split of one publisher paragraph into several Verse texts | **No** | Forever forbidden |
| Silent duplication of one paragraph into several Verse rows as if independent | **No** | Forbidden as permanent practice |

### Normative statement

```text
Allowed:  1 Verse ↔ 1 Segment
Allowed:  N Verses ↔ 1 Segment   (publisher-asserted)
Forbidden: inventing M Segments from 1 publisher unit
Forbidden: inventing 1 Verse text from a fragment of an N:1 unit
```

---

## 4. Chosen representation (summary)

Antar’s **canonical Translation content model is segment-oriented**.

Access for Readers remains **Verse-addressable**: requesting Translation for Verse `1.5` returns the Segment whose coverage includes `1.5` (which may also cover `1.4` and `1.6`).

See [`translation-segmentation-decision.md`](translation-segmentation-decision.md) for Option A/B/C comparison.

---

## 5. Editorial integrity rules

### 5.1 MUST

1. Preserve publisher wording of the fluent Translation unit (modulo encoding/normalization that does not change meaning — defined in a later normalization policy).  
2. Preserve provenance: source id, checksum, page/leaf evidence, publisher label string.  
3. Record the full coverage set on the Segment.  
4. Separate fluent Translation from word-by-word paraphrase, commentary, headers, and front matter (Phase 2 separation rules).  
5. Treat partial coverage as acceptable product state: a Verse may have no published Translation until its Segment is approved.

### 5.2 MUST NOT

1. **Must not** synthesize Translation text (including AI “in the style of” the translator).  
2. **Must not** split a publisher paragraph into multiple Verse translations by inventing sentence breaks or punctuation.  
3. **Must not** infer Verse boundaries inside an English unit when the publisher did not mark them.  
4. **Must not** silently duplicate one publisher paragraph into multiple Verse rows presented as independent translations.  
5. **Must not** drop Verses from a coverage set to force 1:1 packaging convenience.  
6. **Must not** merge adjacent 1:1 publisher units into an N:1 Segment unless the publisher explicitly groups them.  
7. **Must not** treat running headers (`45-47]`, `[ Chap. I.`) as combined Translation labels.  
8. **Must not** store commentary, gloss, or Sanskrit as `translationText`.  
9. **Must not** renumber Verses to match another tradition.  
10. **Must not** claim a Segment is 1:1 when the publisher label is combined.

### 5.3 Evidence required for N:1 Segments

At least one of:

- Explicit combined label in the edition (`I. 21-22.`, `I. 4. 5. 6.`, etc.), or  
- Publisher-equivalent structural grouping documented in inspection (rare; requires editorial sign-off and rationale)

Absence of evidence ⇒ treat as unknown; do not invent N:1 or 1:1 splits.

---

## 6. Canonical model: segment-oriented with Verse index

### Canonical

- The **Segment** is the durable content object (text + coverage + provenance).  
- Scripture remains the durable identity object for Verses.  
- Translation never owns Verse identity; it only references coverage.

### Verse-oriented access (derived)

- Indexes / APIs / Reader resolve `verseId` → covering Segment for a source.  
- Derived verse→segment links are projections, not a license to rewrite text per Verse.

### Consequences

| Concern | Consequence |
|---------|-------------|
| Integrity | One checksummable publisher unit stays one object |
| Provenance | Combined label evidence attaches to the Segment |
| Partial publish | A Segment is published as a whole or not at all |
| Migration | Future package formats store Segments natively |
| Current package v1 | Verse-per-row only — **insufficient** for N:1; see future design |

---

## 7. Gate on normalization (binding until segment packaging exists)

Until a future package format (or approved interim mechanism consistent with this policy) can represent N:1 Segments **without** Options A or B:

1. **1:1 Segments** may be prepared for normalization under later phases.  
2. **N:1 Segments** must not be force-fit into package v1 by splitting or duplicating.  
3. Verses that only appear inside unpublished N:1 Segments remain **Translation unavailable** in product UX.

This continues the Phase 2 suitability outcome `NEEDS_MANUAL_SEGMENTATION_POLICY` until packaging catches up — the policy here **is** that manual/segmentation policy.

---

## 8. Attribution and product copy

- Attribution names the translator / edition, not “Antar’s wording.”  
- UI may indicate when a Translation covers multiple Verses (e.g. “Verses 1.4–1.6”).  
- Do not imply each covered Verse has a distinct English sentence when the publisher printed one unit.

---

## 9. Relation to Scripture numbering

If an edition’s **Verse count tradition** mismatches Antar (e.g. Chapter 1 = 46), that remains a **numbering rejection** under Scripture provenance rules — outside this policy.

If counts match but English is combined, this segmentation policy applies.

---

## 10. Document control

| Artifact | Path |
|----------|------|
| Decision | `translation-segmentation-decision.md` |
| Examples | `translation-segmentation-examples.md` |
| Future design | `translation-segmentation-future-design.md` |
| FAQ | `translation-segmentation-faq.md` |

Supersession requires an explicit content/architecture decision; do not reverse this policy in an importer “for convenience.”
