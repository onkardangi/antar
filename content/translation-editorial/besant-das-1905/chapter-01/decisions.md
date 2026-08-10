# Chapter 1 — Editorial Decisions (Besant & Das 1905)

**Source:** Annie Besant & Bhagavan Das, *The Bhagavad-Gita*, 1905  
**Workspace:** `content/translation-editorial/besant-das-1905/chapter-01/`  
**Date:** 2026-08-07

Decision template: **Context → Options → Choice → Rationale → Follow-up**.

---

## D1 — Fluent English vs word-by-word

**Context:** Each Verse prints Sanskrit, fluent free translation, then a dense word-by-word gloss; footnotes sit at page bottoms.

**Options:** (A) Gloss as Translation (B) Fluent free translation only (C) Merge both.

**Choice:** **B**.

**Rationale:** Matches ADR-012 Translation BC and prior Besant inspection content-layer rules.

**Follow-up:** Reviewers confirm no gloss tokens / Devanagari leakage in `translationText`.

---

## D2 — Footnote markers

**Context:** Superscript footnote markers appear inside fluent blocks (e.g. after teacher, bull, Keshava).

**Choice:** Omit superscript markers from `translationText`; record `FOOTNOTE_MARKER_STRIPPED` in `reviewFlags`. Keep footnote prose out of Translation.

**Rationale:** Footnotes are editorial apparatus, not free translation.

---

## D3 — Speaker attributions

**Context:** English “X said :” lines introduce some Verse free renderings (1.1, 1.2, 1.21, 1.24, 1.28, 1.47). Swarupananda Chapter 1 drafts retained analogous lines.

**Options:** (A) Always strip (B) Retain as printed with the Verse free unit (C) Move to a separate field.

**Choice:** **B** for this draft phase.

**Rationale:** Publisher-faithful Verse unit; matches existing Swarupananda draft convention. Flagged `SPEAKER_ATTRIBUTION` for packaging/product copy review.

**Follow-up:** Product may later strip or restyle speaker lines without changing provenance text if a presentation policy is accepted.

---

## D4 — Label quirks 1.1 / 1.28 / 1.33

**Context:** Structural audit: Arabic `(N)` may be absent on the fluent block.

**Choice:** Accept Sanskrit `॥ N ॥` (and page position) as publisher identity; record `LABEL_QUIRK_NO_ARABIC`.

**Rationale:** Audit already verified ONE_TO_ONE mapping; do not invent labels.

---

## D5 — Cross-page fluent continuations

**Context:** Several free translations span page breaks (e.g. 1.20→1.21 sense continuation; 1.27; 1.33→1.34; 1.43).

**Choice:** Join soft hyphens; keep hard hyphens; assign `sourcePage` to the printed page where the Verse’s fluent unit primarily completes / is labeled; flag `CROSS_PAGE_CONTINUATION` where relevant.

**Rationale:** One Verse → one Segment; page provenance points to the completion/label page used in the structural audit.

---

## D6 — Quotation marks in Arjuna’s speech (1.21–1.23) and 1.11

**Context:** Opening quote begins in 1.21; closure across 1.22–1.23 is slightly ambiguous on IIIF reads. Closing quote after 1.11 Generals is disputed (OCR lacks it).

**Choice:** Retain opening quote on 1.21; do not invent closing quote on 1.11; flag `QUOTATION_MARK_UNCERTAIN` / `OPEN_QUOTATION_CONTINUES`.

**Rationale:** Silence beats inventing punctuation.

---

## D7 — Italics

**Context:** 1.44 prints *Janârdana* in italics.

**Choice:** Plain-text `Janârdana` without markup; flag `ITALICS_PRESENTATION_DEFERRED`.

**Rationale:** No approved italics encoding in Translation package v1.

---

## D8 — Diacritic fidelity

**Context:** IIIF vision transcriptions occasionally disagree on underdots vs circumflex-only forms.

**Choice:** Prefer circumflex long vowels (`â`, `î`, `û`) and common printed forms; flag `DIACRITIC_COMPLEXITY` where underdots were ambiguous.

**Follow-up:** Human reviewer should spot-check flagged Verses against page images before approval.
