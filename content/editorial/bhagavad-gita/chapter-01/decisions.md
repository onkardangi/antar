# Chapter 1 editorial decisions

## Standing decisions

### Antar Chapter 1 verse count

Antar expects **47** Verses for Chapter 1 (`1.1` through `1.47`), matching `V003__seed_scripture_chapters.sql` and `content/validation/antar_verse_counts.json`.

### Rejected Kaggle source (46 records)

The Tarun Tiwari Kaggle corpus (`kaggle-tarun-tiwari-bhagavad-gita`) contains **46** Chapter 1 records. Registry status: `REJECTED_FOR_CANONICAL_IMPORT`.

It is a legitimate alternate numbering tradition (As It Is–style), not an inaccurate text. It is **not** approved for canonical import and must not be loaded into `scripture.verses`.

### No automated reconstruction

No automated split, merge, renumber, or rewrite of source verses is permitted to turn 46 records into 47 Antar identities. Every canonical Verse must be supported by approved source evidence through human editorial work.

### Source evidence required

- Every canonical Verse must eventually cite approved source evidence in `source-comparison.jsonl`.
- Source differences must be documented per Verse.
- Editorial approval is human-controlled.
- Do not copy text from rejected or unapproved sources into the canonical draft.

### Canonical draft import gate

`canonical-draft.jsonl` remains **non-importable** until all **47** records are `APPROVED` with non-blank Sanskrit and transliteration.

As of 2026-08-04, Chapter 1 is `PARTIALLY_APPROVED`: **45** Sanskrit-only approvals (transliteration still `null`) and **2** unresolved conflicts (`1.20`, `1.22`). Import readiness remains false.

### Separate layers

Translation and Commentary remain separate layers and are out of scope for this Chapter 1 workspace.

---

## Open editorial work

1. Resolve remaining Verses **`1.20`** and **`1.22`** (substantive / segmentation differences; third-reference queue).
2. Populate transliteration (currently `null`) before any import-ready claim.
3. Only after all **47** draft records are `APPROVED` with required fields: build package, then consider database import.

### Resolved: Verse 1.1 front matter (2026-08-04)

**Decision:** Retain Wikisource poem front matter (`ॐ` / salutations / chapter title) in the canonical draft for `1.1`.

**Reason:** Batch candidate `proposedSanskritText` is an exact Wikisource copy including front matter. Controlled `BATCH_NORMALIZATION_MATCH_APPROVAL` selected that text without silent strip or rewrite. IIT mool block lacks front matter and remains verification-only.

**Reviewer:** Onkar Dangi (`onkar-dangi`)
**Date:** 2026-08-04
**Status:** `RESOLVED`

### Source acquisition note (2026-08-04)

Sanskrit Wikisource Chapter 1 revision `343151` acquired as `PRIMARY_TRANSCRIPTION_CANDIDATE` (`ACQUIRED_UNREVIEWED`). See `content/raw/sanskrit/wikisource/chapter-01/README.md` and registry id `bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151`.

### Batch NORMALIZATION_MATCH approval note (2026-08-04)

34 `NORMALIZATION_MATCH` Verses promoted to `APPROVED` in `canonical-draft.jsonl` via:

```bash
python3 content/editorial/tools/approve_normalization_matches.py \
  --chapter 1 --reviewer-id onkar-dangi --reviewer-name "Onkar Dangi" \
  --decision-date 2026-08-04 --apply
```

Manifest status: `PARTIALLY_APPROVED`. Chapter remains **not** import-ready. No package built. No PostgreSQL import.

---

## Decision-log template

Copy for each discrepancy:

```markdown
## Decision BG-1-XXX

Canonical reference:

Sources compared:

Observed difference:

Decision:

Reason:

Reviewer:

Date:

Status:
```

### Status values for decisions

Use clear human statuses such as: `OPEN`, `RESOLVED`, `DEFERRED`, `REJECTED_SOURCE`.

---

## Decision log

### Decision BG-1-001 — Retain 1.1 Wikisource front matter

Canonical reference: `1.1`

Sources compared: Wikisource primary; IIT verification-only

Observed difference: Wikisource includes pre-Verse front matter; IIT mool block does not

Decision: Retain exact Wikisource text (including front matter) as canonical Sanskrit

Reason: Explicit batch-candidate proposed text; no silent strip; IIT not an import source

Reviewer: Onkar Dangi (`onkar-dangi`)

Date: 2026-08-04

Status: `RESOLVED`

### Decision BG-1-002 — Batch approve 34 NORMALIZATION_MATCH Verses

Canonical references: 34 Verses listed in `normalization-match-approval-result.jsonl`

Sources compared: Wikisource + IIT (two-source comparison only)

Observed difference: Documented comparison-only normalization categories (whitespace / marker / danda; plus approved orthography and front matter on `1.1`)

Decision: Approve Wikisource exact copies into canonical draft; leave 13 conflicts unresolved

Reason: Controlled human batch path after eligibility validation; no Sanskrit invention

Reviewer: Onkar Dangi (`onkar-dangi`)

Date: 2026-08-04

Status: `RESOLVED` (partial Chapter; conflicts remain `OPEN`)

### Decision BG-1-003 — Resolve 11 orthographic-only SOURCE_CONFLICT Verses

Canonical references: `1.2, 1.8, 1.15, 1.24, 1.26, 1.28, 1.34, 1.41, 1.42, 1.43, 1.47`

Sources compared: Wikisource primary; IIT verification-only

Observed difference: Orthographic-only presentation (anusvāra↔homorganic nasal / ñ-cluster, avagraha presence/absence, vocalic ṝ↔ṛ+nukta, speaker-label संजय↔सञ्जय) with no lexical / segmentation / word-order change after scoped folds

Decision: Accept as orthographic equivalence; select exact Wikisource text as canonical; leave `1.20` and `1.22` unresolved

Reason: Conflict analyses flag `orthographicOnly=true`; scoped Chapter 1 comparison-only rules in `orthographic-resolution-policy.json`; no hybrid synthesis; Unicode similarity alone insufficient without fold-match + human `--apply`

Reviewer: Onkar Dangi (`onkar-dangi`)

Date: 2026-08-04

Status: `RESOLVED` (Chapter still partial; `1.20`/`1.22` remain `OPEN`)


## Final conflict resolution (1.20 / 1.22) — 2026-08-04

Third witness: Sanskrit Documents bhagvadnew (May 15, 2021), role `THIRD_EDITORIAL_VERIFICATION_REFERENCE`.

- **1.20:** `2_OF_3` on decisive compounded `व्यवस्थितान्दृष्ट्वा` (Wikisource + Sanskrit Documents). Selected exact Wikisource. Segmentation resolved for that conflict.
- **1.22:** `MIXED_2_OF_3`. IIT+Sanskrit Documents prefer `निरीक्षे` / non-ZWJ `योद्धु…`; Wikisource+Sanskrit Documents prefer spaced `अस्मिन् रण`. Selected exact Wikisource for Chapter edition coherence with explicit `humanAcceptsMinorityPrimaryReading=true` caveat. No synthesis.

Manifest: `APPROVED` (47/0), `importReady=true`. Transliteration remains null. No package built. No PostgreSQL import.
