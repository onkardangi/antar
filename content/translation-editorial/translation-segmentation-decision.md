# Translation Segmentation — Decision Record

**Status:** Accepted  
**Date:** August 2026  
**Decision:** Adopt **Option C — Translation Segments spanning Verse identities** as Antar’s permanent policy

---

## 1. Options evaluated

### Option A — Artificial split

Split one publisher English paragraph into several Verse-aligned Translation strings (invented boundaries / punctuation).

| Pros | Cons |
|------|------|
| Fits naive 1 row per Verse packaging | Invents structure the publisher did not print |
| Simple Reader mental model (“each Verse has unique English”) | Violates “never invent boundaries” |
| | Unstable under editorial review; different editors split differently |
| | Breaks provenance (“this sentence is Antar’s, not Swarupananda’s unit”) |

**Verdict:** **Rejected permanently.**

### Option B — Duplicate paragraph into multiple Verse rows

Store the same English paragraph as `translationText` on each covered Verse row (`1.4`, `1.5`, `1.6` all identical).

| Pros | Cons |
|------|------|
| Preserves wording | Misrepresents publisher structure as three independent translations |
| Works with current package v1 shape | Pollutes provenance / checksum stories (three rows, one unit) |
| Easy short-term ship | Migration to honest segments becomes cleanup debt |
| | UX may hide multiplicity but data model lies |
| | Encourages tooling that “expands” combined labels automatically |

**Verdict:** **Rejected as permanent practice.** Not an approved interim for Antar.

### Option C — Translation Segment spanning Verses

One Segment object holds one publisher unit and a coverage set of Verse identities. Reader/API resolve by Verse to the covering Segment.

| Pros | Cons |
|------|------|
| Publisher-faithful | Requires future package/API awareness beyond v1 row-per-Verse |
| Durable across editions | Reader must learn “this English covers 1.4–1.6” |
| Clean provenance | Until packaging exists, N:1 Verses stay unpublished |
| Generalizes to Besant/Telang/Arnold edge cases | Slightly richer domain model |

**Verdict:** **Accepted.**

---

## 2. Chosen policy

**Canonical Translation content is segment-oriented and publisher-faithful.**

- Allowed: 1:1 and N:1 (publisher-asserted) Segments.  
- Forbidden: inventing splits (A) or silent duplication (B).  
- Verse-addressable access is a **resolution layer**, not the canonical storage truth for N:1 units.

Normative text: [`translation-segmentation-policy.md`](translation-segmentation-policy.md).

---

## 3. Rationale (why C wins for years)

1. **Honesty.** Antar’s content philosophy rejects invented Scripture boundaries; the same restraint applies to Translation.  
2. **Provenance.** One checksummable publisher unit maps to one Segment.  
3. **Generalization.** Combined labels (Swarupananda), layered free translations (Besant), continuous scholarly prose (Telang), and poetic spans (Arnold) all reduce to Segments with coverage sets — including size 1.  
4. **Product clarity.** Partial coverage and “Translation unavailable” already exist as acceptable UX; waiting on N:1 packaging is better than shipping false 1:1 rows.  
5. **Future cost.** Option B looks cheap now and expensive forever; Option C looks slightly expensive now and cheap forever.

---

## 4. Allowed relationship matrix (decision)

| Mapping | Decision |
|---------|----------|
| 1 → 1 | Allowed |
| N → 1 | Allowed when publisher-asserted |
| 1 → N (same source version) | Disallowed for V1 product sources |
| Artificial split | Disallowed |
| Silent duplicate rows | Disallowed |

---

## 5. Canonical: segment-oriented (not verse-oriented storage)

**Verse-oriented storage** (one independent text blob per Verse as the only model) fails N:1 editions without A or B.

**Segment-oriented storage** with Verse coverage succeeds for all examined candidates and keeps Scripture Verse identity authoritative.

Reader journeys remain Verse-primary (`Read` on a Verse); Translation is companion text that may span neighbors.

---

## 6. Immediate operational consequence

Phase 2 result `NEEDS_MANUAL_SEGMENTATION_POLICY` is satisfied by **this document set**.

Normalization of Swarupananda Chapter 1:

- may plan 1:1 Segments for singleton labels,  
- must represent combined ranges as N:1 Segments,  
- must **not** begin package v1 import of N:1 units via A or B,  
- awaits segment-aware packaging (future phase) for those Verses’ publication.

---

## 7. Non-goals of this decision

- No package schema change in this phase  
- No importer/API/mobile implementation  
- No approval of any Translation wording  
- No ADR supersession of ADR-012 (ownership unchanged); a future ADR may extend data shape when packaging is designed
