# Raw Dataset Inspection — Kaggle Tarun Tiwari Bhagavad Gita CSV

**Status:** inspection only. No normalization, import, or product-code changes were performed.

**Inspection date:** 2026-08-03

**Comparison sources:**

- `backend/src/main/resources/db/migration/V003__seed_scripture_chapters.sql`
- `backend/src/main/resources/db/migration/V004__create_scripture_verses.sql`
- `backend/src/main/resources/db/migration/V005__seed_scripture_verses.sql`

Antar seed structure (from V003 / V005): 18 Chapters, `verse_count` summing to **700**, with Verse identities `"{chapter}.{verse}"` and `sanskrit_text = NULL` until an approved corpus is imported.

---

## 1. Exact filename and path

**Requested path:**

```text
content/raw/sanskrit/kaggle-tarun-tiwari/bhagvad-gita.csv
```

**Actual file found:**

```text
content/raw/sanskrit/kaggle-tarun-tiwari/bhagavad-gita.csv
```

The requested spelling `bhagvad-gita.csv` does **not** exist. The on-disk filename is `bhagavad-gita.csv` (extra `a` in “bhagavad”). All findings below refer to the actual file.

Directory contains only this CSV (no accompanying license or README in that folder).

---

## 2. File size

| Metric | Value |
|--------|-------|
| Size (bytes) | `357624` |
| Size (human) | ~349 KiB |
| Physical lines (`wc -l`) | `3733` |

Physical line count exceeds record count because `devanagari` and `verse_text` embed LF newlines inside quoted CSV fields.

---

## 3. SHA-256 checksum

```text
85e0b8dc40ac29b4dc76828c69833c90ef4c99f615391101afe4ffc781bac1be
```

Command used:

```bash
shasum -a 256 content/raw/sanskrit/kaggle-tarun-tiwari/bhagavad-gita.csv
```

---

## 4. Detected encoding

| Check | Result |
|-------|--------|
| `file -I` | `text/csv; charset=utf-8` |
| UTF-8 decode | succeeds for entire file |
| BOM | **none** (file begins with `,title,...`) |
| NUL bytes | **none** |

Encoding is UTF-8 without BOM.

---

## 5. Delimiter and quoting behavior

| Property | Observation |
|----------|-------------|
| Delimiter | comma (`,`) |
| Quote character | double quote (`"`) |
| Header | `,title,devanagari,verse_text,verse_text_no_samdhis` |
| Embedded commas in fields | not required for parsing in observed data |
| Embedded newlines | present in `devanagari` (698/700 rows) and `verse_text` (700/700); fields are quoted |
| Escaped quotes (`""`) inside fields | **none** observed |
| `csv` module parse | all 700 data rows parse to exactly 5 fields |

Python `csv.Sniffer` reported `doublequote=False`; that is inconclusive here because no in-field quote escaping appears. Standard RFC-style CSV quoting for newlines is used.

---

## 6. Header names

Five columns:

| Position | Header name | Notes |
|----------|-------------|-------|
| 1 | *(empty string)* | Unnamed index column; values `0` … `699` |
| 2 | `title` | Intended Chapter.Verse identity string |
| 3 | `devanagari` | Devanagari Sanskrit text |
| 4 | `verse_text` | IAST-like transliteration (line-broken; often hyphenated) |
| 5 | `verse_text_no_samdhis` | Space-separated / sandhi-resolved transliteration |

There are **no** explicit columns named `chapter`, `verse`, `translation`, or `commentary`.

---

## 7. Number of data rows

**700** data rows (+ 1 header row).

All rows have exactly 5 fields. No truncated or over-wide records under Python’s `csv` reader.

---

## 8. First five records

Abbreviated; newlines shown as `\n`.

### Row 1 (index `0`)

| Column | Value |
|--------|-------|
| *(index)* | `0` |
| `title` | `1.1` |
| `devanagari` | `धृतराष्ट्र उवाच ।\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः\nमामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय ॥ १.१ ॥` |
| `verse_text` | `dhṛtarāṣṭra uvāca\ndharma-kṣetre kuru-kṣetre\nsamavetā yuyutsavaḥ\nmāmakāḥ pāṇḍavāś caiva\nkim akurvata sañjaya` |
| `verse_text_no_samdhis` | `dhṛtarāṣṭraḥ uvāca dharma kṣetre kuru kṣetre samavetāḥ yuyutsavaḥ māmakāḥ pāṇḍavāḥ ca eva kim akurvata sañjaya` |

### Row 2 (index `1`)

| Column | Value |
|--------|-------|
| `title` | `1.2` |
| Marker in Devanagari | `॥ १.२ ॥` |
| Content | Sanjaya opening; transliteration + sandhi-separated forms present |

### Row 3 (index `2`)

| Column | Value |
|--------|-------|
| `title` | `1.3` |
| Marker | `॥ १.३ ॥` |

### Row 4 (index `3`)

| Column | Value |
|--------|-------|
| `title` | `1.4` |
| Marker | `॥ १.४ ॥` |

### Row 5 (index `4`)

| Column | Value |
|--------|-------|
| `title` | `1.5` |
| Marker | `॥ १.५ ॥` |

---

## 9. Last five records

| Row # | index | `title` | Devanagari marker |
|------:|------:|---------|-------------------|
| 696 | 695 | `18.74` | `॥ १८.७४ ॥` |
| 697 | 696 | `18.75` | `॥ १८.७५ ॥` |
| 698 | 697 | `18.76` | `॥ १८.७६ ॥` |
| 699 | 698 | `18.77` | `॥ १८.७७ ॥` |
| 700 | 699 | `18.78` | `॥ १८.७८ ॥` |

Final verse (`18.78`) Devanagari ends with the traditional closing śloka including `यत्र योगेश्वरः कृष्णो…`.

---

## 10. Null or blank values by column

No SQL-null equivalent exists in CSV. Treated as empty / whitespace-only / literal null tokens:

| Column | Empty | Whitespace-only | Literal `null`/`none`/`NA` |
|--------|------:|----------------:|---------------------------:|
| *(index)* | 0 | 0 | 0 |
| `title` | 0 | 0 | 0 |
| `devanagari` | 0 | 0 | 0 |
| `verse_text` | 0 | 0 | 0 |
| `verse_text_no_samdhis` | 0 | 0 | 0 |

All 700 rows have non-blank values in every column.

---

## 11. Duplicate rows

**Exact full-row duplicates:** none (0 groups).

---

## 12. Duplicate chapter/verse identities

### 12.1 Using `title` as identity (as shipped)

**16 duplicate `title` values** (each appears twice), all content-distinct:

| Duplicate `title` | Occurrences | True identities (from Devanagari `॥ … ॥` marker) |
|-------------------|------------:|--------------------------------------------------|
| `3.1` | 2 | `3.1` and `3.10` |
| `3.2` | 2 | `3.2` and `3.20` |
| `3.3` | 2 | `3.3` and `3.30` |
| `3.4` | 2 | `3.4` and `3.40` |
| `4.1` | 2 | `4.1` and `4.10` |
| `4.2` | 2 | `4.2` and `4.20` |
| `4.3` | 2 | `4.3` and `4.30` |
| `4.4` | 2 | `4.4` and `4.40` |
| `7.1` | 2 | `7.1` and `7.10` |
| `7.2` | 2 | `7.2` and `7.20` |
| `7.3` | 2 | `7.3` and `7.30` |
| `8.1` | 2 | `8.1` and `8.10` |
| `8.2` | 2 | `8.2` and `8.20` |
| `9.1` | 2 | `9.1` and `9.10` |
| `9.2` | 2 | `9.2` and `9.20` |
| `9.3` | 2 | `9.3` and `9.30` |

**Root cause (high confidence):** `title` was float-coerced somewhere upstream.  
`float("3.10")` → `3.1` → string `"3.1"`. For every mismatch:

```text
float(title) == float(marker)  and  str(float(marker)) == title
```

**Unique `title` strings:** 684 (not 700).

### 12.2 Using Devanagari closing markers as identity

Every `devanagari` value contains a closing marker `॥ {ch}.{verse} ॥` with Devanagari digits.

| Check | Result |
|-------|--------|
| Rows with parseable marker | 700 / 700 |
| Duplicate marker identities | **0** |
| Unique marker identities | **700** |
| Marker order | sorted ascending by (chapter, verse) |

**Reliable identity for this file is the Devanagari marker, not `title`.**

---

## 13. Chapter count

**18** distinct chapters (1–18), whether counted from corrected markers or from `title` chapter prefixes.

---

## 14. Verse count by Chapter

### 14.1 Counts from `title` (corrupted; do not trust for identity)

| Chapter | Rows whose `title` starts with that chapter | Unique `title` values |
|--------:|--------------------------------------------:|----------------------:|
| 1 | 46 | 46 |
| 2 | 72 | 72 |
| 3 | 43 | 39 |
| 4 | 42 | 38 |
| 5 | 29 | 29 |
| 6 | 47 | 47 |
| 7 | 30 | 27 |
| 8 | 28 | 26 |
| 9 | 34 | 31 |
| 10 | 42 | 42 |
| 11 | 55 | 55 |
| 12 | 20 | 20 |
| 13 | 35 | 35 |
| 14 | 27 | 27 |
| 15 | 20 | 20 |
| 16 | 24 | 24 |
| 17 | 28 | 28 |
| 18 | 78 | 78 |
| **Total** | **700** | **684** |

### 14.2 Counts from Devanagari markers (corrected identity)

| Chapter | Marker verse count | Contiguous `1..N`? |
|--------:|-------------------:|:------------------:|
| 1 | 46 | yes (1–46) |
| 2 | 72 | yes |
| 3 | 43 | yes |
| 4 | 42 | yes |
| 5 | 29 | yes |
| 6 | 47 | yes |
| 7 | 30 | yes |
| 8 | 28 | yes |
| 9 | 34 | yes |
| 10 | 42 | yes |
| 11 | 55 | yes |
| 12 | 20 | yes |
| 13 | 35 | yes (1–35) |
| 14 | 27 | yes |
| 15 | 20 | yes |
| 16 | 24 | yes |
| 17 | 28 | yes |
| 18 | 78 | yes |
| **Total** | **700** | |

---

## 15. Whether the corpus has exactly 18 Chapters and 700 Verses

| Question | Answer |
|----------|--------|
| Exactly 18 Chapters? | **Yes** |
| Exactly 700 verse **rows**? | **Yes** |
| 700 unique trustworthy identities via `title`? | **No** (684 unique titles) |
| 700 unique identities via Devanagari markers? | **Yes** |

Headline “18 × 700” is true at row/corpus level, but **not** if identity is taken from the corrupted `title` column.

---

## 16. Missing or unexpected chapter/verse references

### 16.1 Relative to Devanagari-marker identity vs Antar seed (V003)

Antar expected set: for each chapter `c`, verses `1..verse_count[c]` as seeded in V003.

| Kind | References |
|------|------------|
| Missing vs Antar | `1.47` |
| Unexpected vs Antar | `13.35` |

No other gaps once markers are used. The 16 float-truncated titles are **not** missing verses; they are mislabeled `*.10` / `*.20` / `*.30` / `*.40` rows.

### 16.2 Relative to `title` alone

Missing `title` strings (among others implied by duplicates):  
`3.10`, `3.20`, `3.30`, `3.40`, `4.10`, `4.20`, `4.30`, `4.40`, `7.10`, `7.20`, `7.30`, `8.10`, `8.20`, `9.10`, `9.20`, `9.30`, plus Antar’s `1.47`.

---

## 17. Match against Antar Chapter seed (`verse_count`)

V003 seed `verse_count` vs CSV marker counts:

| Chapter | CSV (marker) | Antar V003 | Match |
|--------:|-------------:|---------:|:-----:|
| 1 | 46 | 47 | **NO** |
| 2 | 72 | 72 | YES |
| 3 | 43 | 43 | YES |
| 4 | 42 | 42 | YES |
| 5 | 29 | 29 | YES |
| 6 | 47 | 47 | YES |
| 7 | 30 | 30 | YES |
| 8 | 28 | 28 | YES |
| 9 | 34 | 34 | YES |
| 10 | 42 | 42 | YES |
| 11 | 55 | 55 | YES |
| 12 | 20 | 20 | YES |
| 13 | 35 | 34 | **NO** |
| 14 | 27 | 27 | YES |
| 15 | 20 | 20 | YES |
| 16 | 24 | 24 | YES |
| 17 | 28 | 28 | YES |
| 18 | 78 | 78 | YES |
| **Sum** | **700** | **700** | sums match; distribution does not |

**Not silently fixed.** This is a known traditional numbering split that still totals 700:

- This CSV’s Chapter 1 ends at **1.46** (`एवमुक्त्वार्जुनः संख्ये…`). Antar expects **1.47**.
- This CSV’s Chapter 13 has **35** verses; `13.1` is Arjuna’s question (`प्रकृतिं पुरुषं चैव…`). Antar expects **34** verses in Chapter 13.

V005 generates Verse rows from `chapters.verse_count`, so a naive import keyed only by Antar’s `canonical_reference` would fail to align Chapter 1 / 13 without an explicit editorial mapping decision.

V004 allows `sanskrit_text` NULL until an approved corpus is imported; that does not resolve identity alignment.

---

## 18. Unicode normalization observations

### Devanagari (`devanagari`)

| Observation | Detail |
|-------------|--------|
| NFC | All 700 values already NFC |
| NFD | All 700 also equal to NFD for this text (typical for Devanagari + combining vowel signs as stored) |
| NFKC | No NFKC differences observed |
| Scripts / signs | Devanagari letters + vowel signs + virama; danda `।` / double danda `॥`; anusvara; avagraha `ऽ` (204); candrabindu (3); OM (2) |
| Verse markers | Devanagari digits in `॥ च.श् ॥` on all 700 rows |
| Speaker lines | `उवाच` present in 33 rows |

### Transliteration (`verse_text`, `verse_text_no_samdhis`)

| Observation | Detail |
|-------------|--------|
| Scheme | IAST-like Latin with precomposed diacritics |
| NFC | All 700 already NFC |
| NFD | **Differs** for all 700 (precomposed vs combining); stored form is precomposed |
| Combining marks in stored text | **0** |
| Anusvara analogue | `ṁ` (U+1E41 LATIN SMALL LETTER M WITH DOT ABOVE) used; **not** `ṃ` (dot below) |
| Avagraha analogue | U+2019 RIGHT SINGLE QUOTATION MARK (`’`), 204 occurrences — matches avagraha count in Devanagari |
| Other letters | ṛ ṝ ḷ ā ī ū ṅ ñ ṭ ḍ ṇ ś ṣ ḥ etc. |

### Malformed Unicode escapes in Devanagari

**13 rows** contain the **literal six-character sequence** `\u200c` (backslash + `u200c`) instead of a real U+200C ZWNJ:

| Data row | `title` | Marker |
|--------:|---------|--------|
| 22 | 1.22 | 1.22 |
| 211 | 5.8 | 5.8 |
| 220 | 5.17 | 5.17 |
| 255 | 6.23 | 6.23 |
| 257 | 6.25 | 6.25 |
| 266 | 6.34 | 6.34 |
| 272 | 6.40 | 6.40 |
| 510 | 13.22 | 13.22 |
| 570 | 15.20 | 15.20 |
| 580 | 16.10 | 16.10 |
| 603 | 17.9 | 17.9 |
| 637 | 18.15 | 18.15 |
| 685 | 18.63 | 18.63 |

Example (`6.23`): `विद्याद्\u200cदुःख…` — ASCII backslash artifacts inside Sanskrit. This is a dataset defect, not valid ZWNJ.

No real U+200C / U+200B / BOM characters were found.

---

## 19. Leading/trailing whitespace and line endings

| Check | Result |
|-------|--------|
| Record line endings | **LF only** (`\n`); **0** CRLF; **0** bare CR |
| Leading/trailing whitespace on parsed field values | **none** on any column |
| Physical lines with trailing space | **1** (a wrapped `verse_text` continuation line ending with a space): `rasa-varjaṁ raso ’py asya ` |
| `title` whitespace | none |

Embedded newlines inside quoted fields are intentional poetic line breaks, not record separators.

---

## 20. Malformed records or parsing concerns

| Concern | Severity | Notes |
|---------|----------|-------|
| Float-corrupted `title` | **High** | 16 identities wrong; duplicates under `title` |
| Literal `\u200c` in Devanagari | **High** for Sanskrit quality | 13 verses |
| Chapter 1 / 13 numbering vs Antar | **High** for import alignment | 46↔47 and 35↔34 |
| Unnamed index column | Low | Redundant with row order |
| Filename mismatch vs requested path | Low (process) | `bhagavad` vs `bhagvad` |
| Multiline quoted fields | Low | Handled by compliant CSV parsers |
| No `chapter` / `verse` integer columns | Medium | Identity must be parsed |
| `title` not sorted when read as floats/strings | Low | Marker order is sorted; `title` sort is wrong because of truncation |
| Two Devanagari rows lack embedded `\n` | Info | `4.31`, `6.23` — still valid single-line ślokas |
| Trailing space on one physical continuation line | Info | Inside `verse_text` |

CSV parsing itself is clean: no field-count mismatches, no unreadable rows.

---

## 21. Column roles

| Column | Appears to contain |
|--------|--------------------|
| *(empty header / index)* | **Unrelated metadata** — sequential row index `0..699` |
| `title` | **Canonical identity (intended, corrupted)** — `"{chapter}.{verse}"` string; **not trustworthy** for `*.10`/`*.20`/`*.30`/`*.40` |
| `devanagari` | **Devanagari Sanskrit** — includes speaker lines, dandas, and embedded `॥ ch.verse ॥` identity; also the only reliable identity source |
| `verse_text` | **Transliteration** — IAST-like, line-broken; hyphens often mark compounds (543/700 rows contain `-`) |
| `verse_text_no_samdhis` | **Sandhi-separated text** (transliteration) — single line, space-separated stems; no hyphens observed |
| *(absent)* | **Translation** — not present |
| *(absent)* | **Commentary** — not present |

Identity encoding without explicit Chapter/Verse columns:

```text
title          ≈  "{chapter}.{verse}"   (string; float-damaged)
devanagari     ⊃  "॥ {DEV_DIGITS chapter}.{DEV_DIGITS verse} ॥"
```

**Reliable normalization of identity is possible** if derived from the Devanagari closing marker (or an externally repaired `title`), not from raw `title` as shipped.

---

## 22. Recommended approved fields for Antar

Pending license/provenance approval and editorial numbering decision. Candidate mappings only:

| Source field | Antar target (planned model) | Recommendation |
|--------------|------------------------------|----------------|
| Identity from Devanagari marker (repaired) | `scripture.verses.canonical_reference` / `(chapter_number, verse_number)` | **Candidate** after repair + Chapter 1/13 policy |
| `devanagari` (after fixing literal `\u200c`) | `scripture.verses.sanskrit_text` | **Candidate** for approved Sanskrit corpus |
| `verse_text` | `scripture.transliterations` (scheme-labeled IAST-like, hyphenated display form) | **Candidate** if transliteration is approved |
| `verse_text_no_samdhis` | separate transliteration or study aid field — **only if** product explicitly wants sandhi-separated form | Optional / later; not required by current V004 Verse table |

Do **not** treat this file as an approved Antar corpus solely because inspection passed structurally.

---

## 23. Fields that must be excluded

| Field / content | Reason |
|-----------------|--------|
| Unnamed index column | Non-scripture metadata |
| Raw `title` as shipped | Corrupted identities; unsafe as primary key |
| Any inferred translation/commentary | Not in file; must not be invented |
| Unlicensed third-party meaning layers | Out of scope; MVP plan forbids unlicensed translation import |
| Literal `\u200c` sequences | Must not be stored as Sanskrit |

---

## 24. Risks or uncertainties

1. **Identity corruption in `title`** — float truncation; importing by `title` would collide and drop/misassign verses.
2. **Numbering scheme mismatch with Antar V003** — Chapter 1 (46 vs 47) and Chapter 13 (35 vs 34). Requires an explicit product/content ADR before import; do not silently remap.
3. **Devanagari ZWNJ serialization bugs** — 13 verses contain ASCII `\u200c` junk.
4. **Provenance / license unknown** in-repo — folder has no license file; Kaggle source licensing must be verified before any approval.
5. **Editorial text quality** — not exhaustively proofread against a critical edition; only structural/Unicode inspection was done.
6. **Transliteration conventions** — `ṁ` vs `ṃ`, U+2019 for avagraha, hyphenation in `verse_text`; scheme must be labeled if stored.
7. **Speaker lines and verse markers inside `devanagari`** — may or may not match Antar’s desired `sanskrit_text` editorial format (V004 comments mention verse markers “where approved”).
8. **Filename path drift** — docs/scripts must use `bhagavad-gita.csv`, not `bhagvad-gita.csv`.

---

## Verdict

| Criterion | Result |
|-----------|--------|
| Parseable UTF-8 CSV | Yes |
| 18 chapters / 700 rows | Yes |
| Edition / numbering tradition | Bhagavad-gītā As It Is (Ch. 1 = 46, Ch. 13 = 35) |
| Safe `title`-based identity | **No** |
| Marker-based unique identity | Yes |
| Matches Antar V003 verse_count distribution | **No** (ch. 1 and 13) |
| Sanskrit field clean | **No** (13× literal `\u200c`) |
| Contains translation/commentary | No |

---

## Final decision

### Status

`REJECTED_FOR_CANONICAL_IMPORT`

### Reason

The corpus uses a different verse-segmentation tradition than Antar’s approved Chapter seed and canonical-reference model. Importing it would require editorial splitting and merging of Sanskrit verses in Chapters 1 and 13, which is outside a deterministic normalization pipeline.

### Clarifications

- The dataset is **not** being rejected as inaccurate.
- It represents a **legitimate alternate edition/numbering tradition** (Bhagavad-gītā As It Is style: Chapter 1 = 46 records, Chapter 13 = 35 records). Antar’s approved seed uses the **47 / 34** tradition. Both total 700 verses; verse segmentation differs.
- Float-corrupted `title` values and literal `\u200c` escape sequences are **technically repairable**, but repairs do **not** solve the edition mismatch.
- The raw file **must remain unchanged** for provenance.
- This file **must not** be loaded into `scripture.verses`.
- It may remain a **research / reference candidate** only.
- Antar’s next corpus candidate **must already match** Chapter 1 = 47 and Chapter 13 = 34.
- **No** automated splitting, joining, or renumbering of canonical Sanskrit is permitted without an approved editorial process.

Provenance notes for this download live alongside the raw file at [`content/raw/sanskrit/kaggle-tarun-tiwari/README.md`](../../content/raw/sanskrit/kaggle-tarun-tiwari/README.md).

---

## Commands / scripts used

Inspection was performed with read-only shell utilities and an ephemeral Python 3 analysis (not saved as a repo script):

```bash
ls -la content/raw/sanskrit/kaggle-tarun-tiwari/
file -I content/raw/sanskrit/kaggle-tarun-tiwari/bhagavad-gita.csv
shasum -a 256 content/raw/sanskrit/kaggle-tarun-tiwari/bhagavad-gita.csv
wc -l -c content/raw/sanskrit/kaggle-tarun-tiwari/bhagavad-gita.csv
xxd -l 80 content/raw/sanskrit/kaggle-tarun-tiwari/bhagavad-gita.csv
python3  # csv + unicodedata + hashlib analysis against V003 counts
```

Comparison constants taken from V003 `verse_count` values (sum 700) and V005’s generation of `canonical_reference` as `chapter_number || '.' || verse_number`.
