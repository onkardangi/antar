# Besant & Das 1905 — Acquisition & Chapter 1 Inspection

**Date:** 2026-08-07  
**Registry id:** `bhagavad-gita-translation-en-besant-das-1905-v1`  
**Raw path:** `content/raw/translations/besant-das-1905/`  
**Status after acquisition:** `ACQUIRED_UNREVIEWED`  
**Suitability decision:** `SAFE_TO_NORMALIZE_AFTER_EDITORIAL_REVIEW`  
**Package Format v1 (Chapter 1):** **Compatible** (all 47 units `ONE_TO_ONE`)

Swarupananda 1909 remains frozen as a separate future edition under
`content/raw/translations/swarupananda-1909/` (untouched by this acquisition).

---

## 1. Exact source identity

| Field | Value |
|-------|-------|
| Internet Archive item | `bhagavadgitawith00londiala` |
| Title | *The Bhagavad-Gita: with Samskrit text, free translation into English, a word-for-word translation, and an Introduction on Samskrit Grammar* |
| Translators | Annie Besant & Bhagavan Das |
| Edition | 1905 joint scholarly edition |
| Publisher | Theosophical Publishing Society, London and Benares |
| Printer | Freeman & Co. Ltd., Tara Printing Works, Benares |
| Pagination | xxxiii, 348 p. |
| Contributor | University of California Libraries |
| Pinned master | `bhagavadgitawith00londiala.pdf` |
| Item URL | https://archive.org/details/bhagavadgitawith00londiala |
| Master SHA-256 | `7fb78b0a6b004f195c3ca61c091501084e553627c51cde1c309f2d0620ea6115` |
| Master size | 26,498,477 bytes |

### Rejected alternates

| Item | Reason |
|------|--------|
| `bhagavadgitaorlo00besa` | Besant-only Natesan Madras **1922** reprint |
| `wg1100` | Folkscanomy upload; weaker provenance than UC Libraries pin |

---

## 2. Edition verification (page images)

Verified from IA IIIF leaf renders of the pinned item (inspection aids; not retained as raw masters):

**Title leaf (leaf 5):**

- THE BHAGAVAD-GÎTÂ  
- With Samskṛit Text, free translation into English, a word-for-word translation, and an Introduction on Samskṛit Grammar  
- BY ANNIE BESANT AND BHAGAVÂN DÂS  
- THEOSOPHICAL PUBLISHING SOCIETY / LONDON AND BENARES / **1905**

**Imprint leaf (leaf 6):**

- PRINTED BY FREEMAN & CO. LTD., AT THE TARA PRINTING WORKS, BENARES  
- All Rights Reserved  
- Registered under Act XXV of 1867  

**Edition identity:** **PASS**

---

## 3. Chapter 1 page / leaf mapping

| Finding | Value |
|---------|-------|
| Mapping rule | `scanLeaf = 46 + printedPage` for arabic body pages on this item |
| Chapter 1 printed pages | **1–22** |
| Chapter 1 scan leaves | **47–68** |
| Chapter 2 boundary | Printed page **23** / leaf **69** — heading `SECOND DISCOURSE.` |
| Opening | Leaf 47: Om + “HERE THE BLESSED LORD'S SONG IS BEGUN.” + Verse 1 |
| Closing | Leaf 67–68: Verse 47 fluent text + gloss; leaf 68 colophon *THE YOGA OF THE DESPONDENCY OF ARJUNA* |

TOC (page images): Chap. I = pages 1–22; Chap. II = 23–56.

Machine-readable audit: [`besant-das-1905-chapter01-inspection.json`](besant-das-1905-chapter01-inspection.json)

---

## 4. Full 47-label audit result

| Check | Result |
|-------|--------|
| Expected identities | **47** (`1.1` … `1.47`) |
| Observed unique identities | **47** |
| Missing labels | **None** |
| Duplicate labels | **None** |
| Combined / N→1 publisher labels | **None** |
| Segmentation | **47 × ONE_TO_ONE** |
| Fluent translation present | **47 / 47** |
| Word-by-word gloss present | Typical for each Verse (exclude from Translation) |

Publisher identity markers are primarily:

- Sanskrit `॥ N ॥` at end of Devanagari verse  
- Arabic `(N)` at end of fluent English free translation (most Verses)

Exceptions (still ONE_TO_ONE; identity from Sanskrit numeral + position):

- **1.1** — fluent block without trailing `(1)`  
- **1.28** — speech unit tied to `॥ २८ ॥` without the usual right-margin `(28)`  
- **1.33** — fluent ends with dash into 1.34 list; Arabic `(33)` not observed  

These are **not** missing Verses and **not** combined labels.

---

## 5. Running-header / false-positive notes

Do **not** treat as Verse labels:

- Centered page numbers `( N )` / `[ N ]`  
- `SECOND DISCOURSE.` on page 23  
- Occasional signature marks (e.g. bottom `2`)  
- Footnote superscripts (`¹`, `²`) inside fluent text  

---

## 6. Speaker-label behavior

Speaker lines appear in Sanskrit (`उवाच`) and English (“X said :”) and are separable from fluent Translation prose.

Observed Chapter 1 speakers (non-exhaustive of every continuation page): Dhṛitarāṣṭra (1.1), Sañjaya (1.2, 1.24, 1.47), Arjuna (1.21, 1.28).

Speaker attributions are **not** part of canonical `translationText` unless a future editorial policy explicitly includes them as part of the free rendering (current rule: exclude as labels).

---

## 7. Content-layer separation (extraction rules only)

### Canonical (future Translation text)

- Fluent English **free translation** associated with Verse N

### Exclude

- Sanskrit / Devanagari  
- Word-by-word gloss  
- Grammar notes inside gloss  
- Footnotes and footnote markers  
- Commentary  
- Running headers / page numbers  
- Chapter colophon (Sanskrit + English)  
- Front matter (grammar introduction, Māhātmyam, Nyāsa, Dhyānam)  
- Translator/editor notes not part of the Verse free rendering  

**No normalized production text was extracted in this phase.**

---

## 8. Package Format v1 compatibility

| Question | Answer |
|----------|--------|
| Any publisher N→1 in Chapter 1? | **No** |
| Can Package Format v1 represent Chapter 1 faithfully? | **Yes** |
| Reason | All 47 units are `ONE_TO_ONE`; verse-per-row `translations.jsonl` can map without split or duplicate |

Do not invent splits or duplicates. If a later chapter reveals N→1, stop and require segment-aware packaging for that unit.

---

## 9. License

Underlying 1905 printing: **US public domain** (`us-pd-pre-1931`).  
IA evidence: `NOT_IN_COPYRIGHT`; stated date 1905.  
Historical imprint rights notices do not defeat that US classification for this printing.

---

## 10. Chapter 13 spot-check

OCR-aided + free-translation evidence: Chapter 13 ends at verse **(34)** with field/knower colophon before Chapter 14 (~p.249). **Antar-compatible (34).** Full Chapter 13 page-image audit is deferred.

---

## 11. Explicit non-actions (this phase)

- No Translation text normalized or approved  
- No Translation package built  
- No importer run / no database writes  
- No backend / mobile / V007 / API / package-schema changes  
- Swarupananda raw/editorial artifacts untouched  
- No git commit  
