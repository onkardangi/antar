# 01 — Scripture Provenance

**Status:** Foundation (Chapter 1 production package built and imported)
**Owner:** Content / Scripture  
**Last Updated:** August 2026

---

## 1. Purpose

Define how Antar acquires, identifies, inspects, and approves (or rejects) Scripture sources before any database import.

Scripture is the source of truth (ADR-010). Provenance must remain auditable.

This document does **not** import Sanskrit. Verse identities exist in the database; Chapter 1 Sanskrit is loaded from package `bhagavad-gita-chapter-01-v1`, while other Chapters remain `sanskrit_text = NULL` until approved corpora are loaded.

---

## 2. Related artifacts

| Path | Role |
|------|------|
| `content/raw/` | Immutable downloads |
| `content/registry/sources.json` | Source approval status |
| `content/checksums/` | SHA-256 manifests |
| `content/licenses/` | License catalog |
| `docs/content/02_CONTENT_PIPELINE.md` | Pipeline, normalization, validation, versioning |
| `docs/content/03_EDITORIAL_POLICY.md` | Editorial and edition rules |
| `docs/content/DATASET_INSPECTION.md` | Example inspection + rejection |

---

## 3. Source approval process

### 3.1 Stages

```text
Identify candidate
    → Acquire raw artifact (unchanged)
    → Record checksum + provenance README
    → Register in sources.json (CANDIDATE)
    → Inspect (structure, identity, edition, license)
    → Decision:
         REJECTED_FOR_CANONICAL_IMPORT
         or APPROVED_FOR_NORMALIZATION
    → (later) Normalize → Validate → Editorial sign-off
    → APPROVED_FOR_IMPORT
    → Import under content version
    → IMPORTED
```

### 3.2 Required before `APPROVED_FOR_NORMALIZATION`

1. Raw file present under `content/raw/` and **byte-immutable**.
2. SHA-256 recorded in `content/checksums/raw.sha256` and `sources.json`.
3. Provenance README beside the raw artifact (or equivalent registry completeness).
4. Inspection document covering identity, chapter/verse counts, encoding, and defects.
5. License displayed at acquisition recorded in the registry and license catalog.
6. `matches_antar_numbering` evaluated explicitly.

### 3.3 Required before `APPROVED_FOR_IMPORT`

Everything above, plus:

1. Normalized package under `content/normalized/` with checksum.
2. Validation against `content/validation/` rules — **pass**.
3. Editorial sign-off per `03_EDITORIAL_POLICY.md`.
4. License clearance for Antar’s intended distribution (mobile + backend).
5. Explicit statement that no automated verse split/merge/renumber was used to force Antar numbering.

### 3.4 Rejection

A source may be accurate and still rejected for canonical import.

Example: Tarun Tiwari Kaggle corpus (`REJECTED_FOR_CANONICAL_IMPORT`) — legitimate As It Is–style 46/35 numbering; Antar requires 47/34.

Rejected sources:

- remain in `raw/` for provenance,
- must not load into `scripture.verses`,
- may remain research/reference candidates only.

---

## 4. Provenance requirements

Every raw Scripture artifact must record:

| Requirement | Description |
|-------------|-------------|
| Source title | Upstream name |
| Creator / publisher | Person or organization |
| Platform / channel | Where acquired |
| Source URL | Stable upstream link when available |
| Original filename | As downloaded |
| Acquisition date | When obtained |
| Displayed license | Exact label shown upstream |
| SHA-256 | Of the immutable bytes |
| Edition / numbering tradition | Especially Chapter 1 and 13 counts |
| Inspection link | Path to inspection notes |
| Approval status | Registry status vocabulary |

### 4.1 Immutability

- Never edit `content/raw/**` in place.
- Repairs happen only in documented pipeline outputs, never by silently rewriting the download.
- Checksum mismatch after registration is a **stop** condition.

### 4.2 Identity provenance

Antar canonical references follow:

```text
{chapter_number}.{verse_number}
```

as seeded in `V005` from `V003.verse_count`.

A candidate corpus must already align with those identities. Marker-derived or column-derived identities are acceptable **inputs to inspection**, but the approved package must emit Antar identities without editorial invention.

---

## 5. Antar numbering tradition (approved seed)

From `V003__seed_scripture_chapters.sql`:

| Chapter | Verses |
|--------:|-------:|
| 1 | **47** |
| 2 | 72 |
| 3 | 43 |
| 4 | 42 |
| 5 | 29 |
| 6 | 47 |
| 7 | 30 |
| 8 | 28 |
| 9 | 34 |
| 10 | 42 |
| 11 | 55 |
| 12 | 20 |
| 13 | **34** |
| 14 | 27 |
| 15 | 20 |
| 16 | 24 |
| 17 | 28 |
| 18 | 78 |
| **Total** | **700** |

The next corpus candidate **must already match** Chapter 1 = 47 and Chapter 13 = 34.

Machine-readable copy: `content/validation/antar_verse_counts.json`.

---

## 6. What provenance is not

- Provenance is not product copy.
- A public-domain label is not automatic import approval.
- Passing CSV parse checks is not edition approval.
- Research usefulness is not canonical Scripture status.

---

## 7. Implementation status

| Item | Status |
|------|--------|
| Provenance policy | Documented (this file) |
| Registry + checksums + licenses layout | Implemented under `content/` |
| Approved Sanskrit corpus package | **Present** — `content/packages/bhagavad-gita-chapter-01-v1` (Chapter 1, 47 Verses, content version 1, `APPROVED`, imported) |
| Database Sanskrit import | **Performed** for Chapter 1 (`bhagavad-gita-chapter-01-v1`; 47 Verses) |
