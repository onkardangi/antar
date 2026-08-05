# Chapter 1 — Editorial Decisions

**Source:** Swami Swarupananda, *Srimad-Bhagavad-Gita*, First Edition 1909  
**Workspace:** `content/translation-editorial/swarupananda-1909/chapter-01/`  
**Date:** 2026-08-05

Decision template fields: **Context → Options → Choice → Rationale → Follow-up**.

---

## D1 — Fluent English vs word-by-word

**Context:** Each verse block prints Sanskrit, then interleaved Devanagari+gloss, then a separate fluent paragraph, then optional `[commentary]`.

**Options:** (A) Treat gloss lines as Translation (B) Use only the fluent paragraph (C) Merge both.

**Choice:** **B**.

**Rationale:** Product Translation is the publisher’s continuous English rendering. Gloss is a study aid, not the Translation unit.

**Follow-up:** Reviewers must confirm no gloss tokens remain in `translationText`.

---

## D2 — Bracketed commentary exclusion

**Context:** Commentary appears in square brackets, often smaller type, after the fluent unit.

**Choice:** Exclude all `[...]` commentary and footnote-style glosses (e.g. “Great-charioted”, Atatâyin notes) from `translationText`.

**Rationale:** Commentary is Understanding/guidance material, not Translation text.

---

## D3 — Combined labels preserved as single segments

**Context:** Phase 2 page-image inventory listed `I. 4. 5. 6.`, `I. 21—22.`, `I. 24—25.`, `I. 32—34.`, `I. 38. 39.`.

**Choice:** One segment per label; no artificial split; no silent duplication onto multiple Verse rows.

**Rationale:** Segmentation policy Option C (publisher-faithful segments).

---

## D4 — Pinned scan missing pages

**Context:** Consecutive BookReader leaves for the pinned master:

| Scan leaf | Printed page |
|-----------|--------------|
| 34 | 13 |
| 35 | 16 |
| 36 | 19 |
| 37 | 22 |
| 38 | 23 |

Missing printed pages: **14, 15, 17, 18, 20, 21**. DjVu OCR for the same item also jumps across these gaps.

**Options:** (A) Leave Verses uncovered (B) Stop Phase 4 (C) Provisional secondary PD text + `SOURCE_CONFLICT`.

**Choice:** **C**.

**Rationale:** Workspace must map 1.1–1.47 exactly once for editorial continuity, but must not pretend missing pages were image-verified.

**Follow-up:** Re-acquire a complete 1909 leaf set (or confirm JP2 ZIP somehow differs) before any approval.

---

## D5 — Verses 28–29 combined (secondary evidence)

**Context:** Pages 14–15 (where 28–29 fall) are missing from the pinned scan. Phase 2 combined-label list did not include 28–29 because those pages were not image-inspectable. Later Advaita Ashrama OCR shows fluent label **`28—29.`**; Sacred Texts 1909 etext prints one continuous block for the same content (numbered oddly as “29”).

**Options:** (A) Invent two 1→1 splits from the secondary paragraph (B) One N→1 segment `I. 28—29.` with `SOURCE_CONFLICT` (C) Leave uncovered.

**Choice:** **B**.

**Rationale:** Splitting would violate publisher-faithful policy. Secondary editions of the same translator tradition treat the unit as combined.

**Follow-up:** Confirm label typography on a complete 1909 page image before clearing `SOURCE_CONFLICT`.

---

## D6 — Why no publisher unit was split

Even where a multi-verse paragraph could be sentence-segmented, Antar forbids inventing Verse boundaries inside a publisher unit. Coverage is the label’s Verse set; Sanskrit Verse cards remain 1:1 via Scripture.

---

## D7 — Why N→1 remains non-packageable under package v1

Package format v1 stores one `translations.jsonl` row per `canonicalReference`. Honest N→1 storage would require either silent duplication (forbidden) or segment-aware packaging (not built). Therefore `packageReady=false` and `importReady=false` while any N→1 segment exists or any record is unapproved.

---

## D8 — Verse 20 fluent wording

**Context:** Vision/OCR briefly misread the fluent line near शस्त्रसंपाते.

**Choice:** Prefer page-image fluent wording **“the shooting about to begin”** (matching Sacred Texts / common printing), with word-by-word used only as locator (`discharge of missiles`).

**Follow-up:** Second-pass human check on leaf 32.

---

## D9 — Running headers are not combined labels

Headers such as `22-26]`, `36-41]`, `45-47]` are pagination aids only. Verses 45, 46, 47 remain separate segments (`I. 45.`, `I. 46.`, `I. 47.`).

---

## D10 — Spelling / punctuation

Do not modernize. Preserve circumflexes (â), spellings (`Thyself`, `eldest`, `yoked to`, `Oh Krishna` on 1.31), and parenthetical insertions `(are)`, `(Now)`, `(let me know)`.
