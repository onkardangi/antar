# Acquisition Plan — Swarupananda 1909 (Not Executed)

**Status:** Planned only. **No download, scrape, OCR corpus build, or registry mutation in Phase 1.**

Recommended source: Swami Swarupananda, *Srimad-Bhagavad-Gita*, Advaita Ashrama, Mayavati, **1909**.

---

## Goals of future acquisition

1. Obtain **immutable raw bytes** of one pinned printing.  
2. Record provenance exactly as Scripture does (`docs/content/01_SCRIPTURE_PROVENANCE.md` pattern).  
3. Enable later verification against Antar verse counts — without bulk scraping mirrors.

---

## Preferred acquisition channel

| Priority | Channel | Role |
|----------|---------|------|
| **1 — primary raw** | Internet Archive (or Digital Library of India mirror on IA) scan of the **1909** Advaita Ashrama edition | Immutable PDF/DjVu + checksum |
| **2 — corroboration** | A second IA copy or library scan of the same edition if available | Spot-check OCR / missing pages |
| **3 — research only** | Sacred Texts HTML (`sacred-texts.com/hin/sbg/`) | Numbering/style reference; **not** redistribution master; **no bulk robot download** |
| **Avoid as master** | Random Gita aggregator sites, unattributed GitHub dumps, “complete Gita JSON” mirrors | Weak provenance; edition mixing risk |

Candidate IA starting points for *later* human selection (not downloaded here):

- Search IA for `Swarupananda Bhagavad` / `Srimad Bhagavad Gita Swarupananda 1909`  
- Prefer items with clear 1909 title-page evidence and complete 18 chapters  

---

## Proposed raw layout (future)

```text
content/raw/translation/swarupananda-1909/
  README.md                 # provenance
  metadata.json             # URL, date, license displayed, edition
  <original-filename>.pdf   # immutable bytes
```

Rules (same spirit as Sanskrit `content/raw/`):

- Never edit raw bytes in place  
- Register SHA-256 in `content/checksums/` and `content/registry/sources.json`  
- Status starts as `CANDIDATE`

---

## Acquisition steps (future checklist)

1. **Identify** one IA item with visible 1909 title page and complete Gita chapters.  
2. **Download once** via browser or documented one-shot fetch (not a scraper’s full-site crawl).  
3. **Write provenance README** beside the file (source title, creator, URL, acquisition date, displayed rights, edition notes).  
4. **Checksum** and register.  
5. **Inspect** structure: page completeness, OCR quality, verse number visibility, Chapter 1/13 counts.  
6. Decide `REJECTED_FOR_CANONICAL_IMPORT` vs `APPROVED_FOR_NORMALIZATION`.  
7. Only then begin normalization workspace (separate from raw).

---

## What not to do

| Forbidden in next acquisition phase | Why |
|-------------------------------------|-----|
| Bulk-scrape Sacred Texts / Wikisource | ToS, robots, Cloudflare; host-layer license complexity |
| Use Sacred Texts HTML as package input | ISTA commercial/attribution constraints on produced etexts |
| Download “all English Gitas” archives | Edition mixing; provenance collapse |
| OCR-correct inside `raw/` | Breaks immutability |
| AI-fill missing verses | Violates Translation authenticity policy |
| Touch Translation importer / V007 / API | Out of content-acquisition scope |

---

## Verification plan (after raw lands)

| Check | Pass criterion |
|-------|----------------|
| Edition identity | Title page matches Swarupananda / Advaita Ashrama / 1909 (or documented reprint of that text) |
| Completeness | Chapters 1–18 present |
| Chapter 1 count | **47** English verse units mappable to Antar |
| Chapter 13 count | **34** (if 35, stop — treat like Scripture numbering rejection) |
| Combined labels | Inventory of `n-m` headings; no silent split |
| Commentary separation | Footnotes identifiable and excludable |
| Encoding | UTF-8 normalization path defined without changing raw |

---

## Normalization / editorial handoff (future)

```text
raw (immutable)
  → inspection report (docs or content/editorial)
  → normalized verse JSON/JSONL (working)
  → editorial review (human)
  → translation package under content/packages/translation/
  → validate_package.py
  → importer (existing; unchanged in Phase 1)
```

First package target: **Chapter 1 only** (`expectedCount` 47), then expand.

---

## Fallback acquisition

If Swarupananda fails numbering or combined-verse density:

1. Stop Swarupananda canonical path (retain raw for provenance).  
2. Acquire **Besant & Das 1905** IA scan under `content/raw/translation/besant-das-1905/`.  
3. Extract **free English translation** layer only.  
4. Re-run the same verification gates.

---

## Effort estimate (planning only)

| Stage | Rough effort |
|-------|--------------|
| Pin IA item + download + provenance | Small |
| Chapter 1 verse inventory + OCR cleanup | Medium |
| Full 18-chapter normalization | Larger; chapter-sliced |
| Editorial review Chapter 1 | Medium (47 verses) |
| Package + import dry-run | Small once package builder exists for production |

No stage is started in this Phase 1 documentation set.
