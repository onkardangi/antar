# Swarupananda 1909 — Acquisition & Chapter 1 Inspection

**Date:** 2026-08-05  
**Registry id:** `bhagavad-gita-translation-en-swarupananda-1909-v1`  
**Raw path:** `content/raw/translations/swarupananda-1909/`  
**Status after acquisition:** `ACQUIRED_UNREVIEWED`  
**Suitability decision:** `NEEDS_MANUAL_SEGMENTATION_POLICY`

**Policy resolution (Phase 3):** Canonical Translation content is **segment-oriented** (publisher-faithful N:1 allowed; no artificial split; no silent duplication). See [`content/translation-editorial/`](../translation-editorial/). Normalization of N:1 units still awaits segment-aware packaging — this policy forbids Options A/B stopgaps.

---

## 1. Exact source identity

| Field | Value |
|-------|-------|
| Internet Archive item | `in.ernet.dli.2015.386852` |
| Title | Srimad Bhagavad Gita / *Srimad-Bhagavad-Gita* |
| Translator | Swami Swarupananda |
| Edition | **First Edition, 1909** |
| Publisher | Prabuddha Bharata Press, Mayavati, Almora, Himalayas |
| Printer | Mohan Lal Sah Chowdhari |
| Series | Himalayan Series — No. XX |
| Pinned master | `2015.386852.Srimad-Bhagavad.pdf` |
| Item URL | https://archive.org/details/in.ernet.dli.2015.386852 |

### Rejected alternate

| Item | Reason |
|------|--------|
| `in.ernet.dli.2015.237563` | Title page / OCR evidence shows **Tenth Impression, 1967** despite misleading `date: 1909` metadata |

---

## 2. Retained files and checksums

From `content/raw/translations/swarupananda-1909/SHA256SUMS` (verified locally):

| File | SHA-256 |
|------|---------|
| `2015.386852.Srimad-Bhagavad.pdf` | `ab9e38c2f252574de88d55374fb8c97c7c2998b4442e9e8f32cda8713a99315e` |
| `in.ernet.dli.2015.386852_meta.xml` | `2af6b1375b96105b2694b30dc080c8893452f3b91953a8b06cd615aabc817517` |
| `in.ernet.dli.2015.386852_files.xml` | `bca41683208aa7d04df0af57c23495c5e7a5a0ad0e0bc8180c4ec53582f3d7d8` |
| `2015.386852.Srimad-Bhagavad_djvu.txt` | `9d9433da635d1f92284c391b734632a58d42b70b1a1579e6b86587ac6410b477` |
| `2015.386852.Srimad-Bhagavad_page_numbers.json` | `4832b8c615ae1f15d88d94f0e0f0dcff12a447ab652d2bbfd32e2be8852e1f53` |
| `2015.386852.Srimad-Bhagavad_scandata.xml` | `f16f7e68df6b4dd7d6b6be2fcc06d3b8d7506ebbe168533d3c5bd342a0ea5b9d` |
| `ia-metadata-api.json` | `b14c3a2a68469637dba08cf2ff5c7ca2d0dfce2d2363933754da65baa526c58b` |
| `metadata.json` | see current `SHA256SUMS` (updated after edition-verification fields) |

Master size: **25,704,747 bytes**.

Not retained: Additional Text PDF, JP2 ZIP, Sacred Texts HTML, Gutenberg text, 1967 reprint item.

---

## 3. Edition verification (scan)

Verified **directly from page images** of the pinned PDF via Internet Archive IIIF leaf renders (inspection aids; not retained as raw masters):

**Title leaf (IIIF leaf 0):**

- Himalayan Series — No. XX  
- SRIMAD-BHAGAVAD-GITA  
- By The Swami Swarupananda  
- **FIRST EDITION** / **1909**  
- Price line present  

**Imprint leaf (IIIF leaf 1):**

- Printed by Mohan Lal Sah Chowdhari  
- Published by the **Prabuddha Bharata Press**  
- **Mayavati, Almora, Himalayas**  

**Preface leaf:** Advaita Ashrama / Prabuddha Bharata compilation history matching selection docs.

**Edition identity:** **PASS** (1909 first edition; not the 1967 reprint).

---

## 4. Chapter 1 page range

| Finding | Value |
|---------|-------|
| Chapter title | *The Grief of Arjuna* / प्रथम अध्याय (First Chapter) |
| TOC (scan) | Chap. I begins printed page **1**; Chap. II begins printed page **24** |
| Scan leaves (IIIF / leafNum) | Chapter 1 body observed on leaves **22–38**; Chapter 2 begins leaf **39** |
| Printed pages (body) | Running headers / end leaf show Chapter 1 through printed page **23** |
| Source page range (reported) | Printed **1–23** (body); leaves **22–38** |

IA `page_numbers.json` OCR for some mid-chapter leaves is imperfect (skipped/misread printed numbers). Leaf range and chapter boundaries were confirmed from page images.

---

## 5. Scan-quality observations

- Image Container PDF is page-image based (no usable embedded text layer for label extraction).  
- Contrast generally high; English serif text legible.  
- Typical archival speckles / minor bleed-through on some leaves.  
- Slight skew on some pages; does not block reading verse labels.  
- Suitable for human transcription / careful OCR of English translation blocks.

---

## 6. OCR-quality observations

- Retained `*_djvu.txt` is **noisy** (mixed Devanagari/Latin; many broken tokens).  
- Automated OCR label harvest **cannot** be trusted as a complete inventory (many false misses / false “combined” hits from running headers like `8-10]`).  
- OCR used only to locate candidate regions; **final label conclusions come from page images**.

---

## 7. Chapter 1 Verse-count result

| Check | Result |
|-------|--------|
| Antar expected | **47** |
| Chapter opens | `I. 1.` with Sanskrit `॥१॥` |
| Chapter closes | `I. 47.` with Sanskrit `॥४७॥` + chapter-end formula on printed page 23 |
| Identity scheme | **Aligns with Antar Chapter 1 = 47** |

This is **not** a 46-verse As It Is–style Chapter 1.

---

## 8. Observed Verse labels (structural)

English labels use forms such as `I. N.` / `I. N—M.` alongside Devanagari `॥N॥` in the Sanskrit block.

**Confirmed combined English editorial labels** (page-image inspection; not running headers):

| Combined label | Verses covered | Notes |
|----------------|----------------|-------|
| `I. 4. 5. 6.` | 4–6 | Shared word-by-word + shared English rendering unit |
| `I. 21-22.` | 21–22 | Explicit combined label |
| `I. 24—25.` | 24–25 | Explicit combined label |
| `I. 32—34.` | 32–34 | Explicit combined label |
| `I. 38. 39.` | 38–39 | Explicit combined label |

**Not combined labels:** running headers such as `8-10]`, `45-47]`, `[ Chap. I.` — these are pagination aids only (prohibited extraction fields).

**Sample singleton labels confirmed on-image:** `I. 1.`, `I. 2.`, `I. 3.`, `I. 7.`, `I. 8.`, `I. 9.`, `I. 10.`, `I. 11.`, `I. 12.`, `I. 13.`, `I. 14.`, `I. 15.`, `I. 16.`, `I. 17.`, `I. 18.`, `I. 19.`, `I. 20.`, `I. 23.`, `I. 26.`, `I. 40.`, `I. 46.`, `I. 47.` (non-exhaustive list of singletons; full mechanical OCR inventory unreliable).

Machine-readable structural summary: `swarupananda-1909-chapter-01-labels.json`.

---

## 9. Missing / duplicate labels

| Kind | Result |
|------|--------|
| Missing identities in 1…47 scheme | **None observed** at chapter boundaries; edition completes at 47 |
| Duplicate `I. N.` identity labels | **None observed** in sampled pages |
| Gaps in English *row* coverage | Combined ranges share one English rendering block — see combined list |

Do **not** invent splits for combined English blocks in this phase.

---

## 10. Speaker-label structure

Speaker lines appear in Sanskrit (e.g. `धृतराष्ट्र उवाच`, `संजय उवाच`, `अर्जुन उवाच`) and are repeated in word-by-word / translation (“Dhritaráshtra said :”, “Sanjaya said :”, “Arjuna said :”). Speakers are separable from translation prose.

---

## 11. Translation / commentary separation

Per-verse apparatus is layered and **visually separable**:

1. Sanskrit (Devanagari) + `॥N॥`  
2. English label `I. N.` (or combined)  
3. Word-by-word paraphrase (Sanskrit word + English gloss) — **not** product Translation  
4. Fluent English rendering (often in quotes) — **candidate Translation field**  
5. Bracketed comments `[ ... ]` — **commentary; prohibited for Translation rows**  

Also exclude: preface/foreword/meditation/invocation, running headers/footers, page numbers, chapter-end colophons, indexes.

---

## 12. Pagination / header / footer concerns

- Running headers alternate book title / chapter title.  
- Verse-range headers (`22-26]`) must not be parsed as combined verse labels.  
- Printer signatures / speckles occasional.  
- Do not import header/footer text into Translation rows.

---

## 13. Chapter 13 count observation

| Evidence | Result |
|----------|--------|
| TOC | Chap. XIII starts printed page **252**; Chap. XIV at **270** |
| Scan leaf for chapter end | Printed page **269** shows `XIII. 34.` and chapter-end formula for *Discrimination of the Kshetra and the Kshetrajna* |
| Next leaf | **Fourteenth Chapter** begins |

**Chapter 13 ends at verse 34** in this edition (Antar-compatible; not the 35-verse tradition).

Confidence: **high** (page-image confirmation of `XIII. 34.` + chapter end).

---

## 14. Suitability decision

### `NEEDS_MANUAL_SEGMENTATION_POLICY`

**Why not `SAFE_TO_NORMALIZE` yet**

- Chapter 1 identity scheme matches Antar (**47**), and Chapter 13 appears to match (**34**).  
- However, multiple **combined English labels** (`4–6`, `21–22`, `24–25`, `32–34`, `38–39`) prevent naive 1:1 `translations.jsonl` emission without an explicit editorial segmentation policy.  
- Antar forbids inventing verse boundaries / silent splits.

**Why not rejected**

- Not a numbering-tradition mismatch (47/34 aligned).  
- Scan quality is adequate.  
- Translation prose is separable from commentary when policy is applied.

**Gate for later normalization**

1. Written policy for combined labels (e.g. publish one Translation row per Antar Verse only when an edition-native separable English unit exists; otherwise leave unpublished / apply approved human segmentation rules without inventing wording).  
2. Then proceed leaf-by-leaf extraction for Chapter 1 only.

---

## 15. Risks and unresolved questions

| Risk / question | Note |
|-----------------|------|
| Combined-label inventory completeness | Confirmed set above from page images; a full second-pass human leaf audit should precede normalization |
| OCR unreliability | Do not drive package text from DjVuTXT |
| Word-by-word vs fluent English | Product Translation must use fluent rendering only |
| Diacritic normalization | Later normalization concern (`â`, etc.) |
| International copyright edge cases | US PD conclusion recorded; counsel if needed for other jurisdictions |
| Ephemeral IIIF inspection images | Used for inspection; not retained as raw provenance masters |

---

## 16. Explicit non-actions (this phase)

- No Translation text normalized or approved  
- No importable Translation package created  
- No importer run / no database writes  
- No backend / mobile / V007 / API / package-builder changes  
