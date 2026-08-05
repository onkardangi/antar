# Chapter 1 editorial workspace

Controlled workspace for Antar’s **47** Chapter 1 Verse identities (`1.1`–`1.47`).

## Status

| Item | State |
|------|-------|
| Identities scaffolded | Yes (47) |
| Wikisource source acquired | Yes (rev `343151`, `ACQUIRED_UNREVIEWED`) |
| Extraction JSONL | Yes (`wikisource-extraction.jsonl`, 47 verses) |
| Source comparison populated | Yes (Wikisource + IIT for 1.1–1.47) |
| Automated comparison | Yes (`NORMALIZATION_MATCH` × 34; `SOURCE_CONFLICT` × 13 historical) |
| IIT secondary verification | Yes (Verses 1.1–1.47, `VERIFICATION_ONLY`) |
| Human approval prep | Yes (34 batch candidates + 13 conflict analyses) |
| Batch normalization-match approval | Yes — **34 APPROVED** (`2026-08-04`, reviewer `onkar-dangi`) |
| Orthographic conflict resolution | Yes — **11 APPROVED** (`2026-08-04`, reviewer `onkar-dangi`) |
| Sanskrit in canonical draft | Yes for **47** approved Verses (exact Wikisource copy) |
| Transliteration | `null` (not populated) |
| Records approved | **47** |
| Unresolved SOURCE_CONFLICT | **0** |
| Chapter status | `APPROVED` |
| Import readiness | `READY` (editorial; transliteration still null; package not built; no DB import) |
| Content package | **Not built** |
| Database import | **Not performed** |

## Batch approval record (2026-08-04)

Controlled `BATCH_NORMALIZATION_MATCH_APPROVAL` of the 34 `NORMALIZATION_MATCH` candidates:

- Selected canonical source: Wikisource `PRIMARY_TRANSCRIPTION_CANDIDATE`
- IIT role: `SECONDARY_VERIFICATION_REFERENCE` / verification only (not imported)
- Proposed Sanskrit: exact Wikisource copy (no synthesis / rewrite)
- Verse 1.1: front matter retained as present in Wikisource poem body (explicit retention; no silent strip)
- 13 `SOURCE_CONFLICT` Verses left unresolved and unapproved at this step
- No scholarly consensus claimed beyond the recorded two-source comparison

```bash
python3 content/editorial/tools/approve_normalization_matches.py \
  --chapter 1 \
  --reviewer-id onkar-dangi \
  --reviewer-name "Onkar Dangi" \
  --decision-date 2026-08-04 \
  --dry-run

python3 content/editorial/tools/approve_normalization_matches.py \
  --chapter 1 \
  --reviewer-id onkar-dangi \
  --reviewer-name "Onkar Dangi" \
  --decision-date 2026-08-04 \
  --apply
```

## Final conflict resolution (2026-08-04)

Controlled `FINAL_CHAPTER01_CONFLICT_RESOLUTION` for **1.20** and **1.22** after third-witness acquisition:

- Third witness: Sanskrit Documents `bhagvadnew` (`THIRD_EDITORIAL_VERIFICATION_REFERENCE`, Ch.1=47)
- Selected canonical source: Wikisource exact copy (no synthesis)
- IIT + Sanskrit Documents: verification only
- Evidence: `final-conflict-resolution-candidates.jsonl`, `final-conflict-resolution-result.jsonl`
- Tool: `content/editorial/tools/approve_final_chapter01_conflicts.py`

```bash
python3 content/editorial/tools/approve_final_chapter01_conflicts.py \
  --reviewer-id onkar-dangi \
  --reviewer-name "Onkar Dangi" \
  --decision-date 2026-08-04 \
  --dry-run

python3 content/editorial/tools/approve_final_chapter01_conflicts.py \
  --reviewer-id onkar-dangi \
  --reviewer-name "Onkar Dangi" \
  --decision-date 2026-08-04 \
  --apply
```

## Orthographic conflict resolution (2026-08-04)

Controlled `ORTHOGRAPHIC_SOURCE_CONFLICT_RESOLUTION` for **11** orthographic-only conflicts:

- References: `1.2, 1.8, 1.15, 1.24, 1.26, 1.28, 1.34, 1.41, 1.42, 1.43, 1.47`
- Policy: `content/editorial/orthographic-resolution-policy.json` (Chapter 1 scoped; comparison-only; not auto-applied to other chapters)
- Selected canonical source: Wikisource exact copy (no hybrid / synthesis)
- IIT: verification only
- Left unresolved: `1.20`, `1.22` (substantive / third-witness required)
- Evidence: `orthographic-resolution-result.jsonl`
- SOURCE_CONFLICT history retained in `source-conflict-analysis.jsonl` and review Differences

```bash
python3 content/editorial/tools/resolve_orthographic_conflicts.py \
  --chapter 1 \
  --reviewer-id onkar-dangi \
  --reviewer-name "Onkar Dangi" \
  --decision-date 2026-08-04 \
  --dry-run

python3 content/editorial/tools/resolve_orthographic_conflicts.py \
  --chapter 1 \
  --reviewer-id onkar-dangi \
  --reviewer-name "Onkar Dangi" \
  --decision-date 2026-08-04 \
  --apply
```

## Files

| File | Purpose |
|------|---------|
| `source-comparison.jsonl` | Per-Verse source evidence (immutable comparison bytes) |
| `wikisource-extraction.jsonl` | Deterministic extraction from preserved revision |
| `canonical-draft.jsonl` | Canonical draft (**47 APPROVED**; transliteration null) |
| `automated-comparison-report.jsonl` | Phase 2 deterministic comparison results |
| `automated-comparison-run-meta.json` | Run timestamps / report checksum (non-deterministic metadata) |
| `audit-sample.json` | Deterministic audit-sample references |
| `automated-review-summary.md` | Human-readable Chapter batch summary |
| `normalization-match-approval-candidate.jsonl` | 34 PENDING prep candidates (historical; draft holds approvals) |
| `normalization-match-review.md` | Pattern-grouped human review table |
| `normalization-match-approval-result.jsonl` | Deterministic approval evidence for 34 Verses |
| `orthographic-resolution-result.jsonl` | Deterministic evidence for 11 orthographic conflict resolutions |
| `source-conflict-analysis.jsonl` | 13 conflict analyses (history retained; 11 resolved in draft/reviews) |
| `orthographic-patterns.md` | Orthographic cluster report (no rules added) |
| `third-reference-queue.json` | Verses needing a third witness |
| `chapter-01-approval-manifest.json` | Chapter approval manifest (`APPROVED`, importReady=true) |
| `decisions.md` | Edition decisions and discrepancy log |
| `review-checklist.md` | Human review checklist per Verse |
| `validation-report.md` | Acquisition + structural validation report |

Verse review decision history: [`content/editorial/reviews/`](../../reviews/)

## Policies

- [`docs/content/01_SCRIPTURE_PROVENANCE.md`](../../../docs/content/01_SCRIPTURE_PROVENANCE.md)
- [`docs/content/02_CONTENT_PIPELINE.md`](../../../docs/content/02_CONTENT_PIPELINE.md)
- [`docs/content/03_EDITORIAL_POLICY.md`](../../../docs/content/03_EDITORIAL_POLICY.md)
- [`content/editorial/AUTOMATED_REVIEW_POLICY.md`](../../AUTOMATED_REVIEW_POLICY.md)
- [`content/editorial/normalization-policy.json`](../../normalization-policy.json)
- [`content/editorial/batch-normalization-match-approval-policy.json`](../../batch-normalization-match-approval-policy.json)

## Commands

```bash
# Fetch (network; pinned revision; refuses silent overwrite of different bytes)
python3 content/acquisition/fetch_wikisource_page.py \
  --title 'भगवद्गीता/अर्जुनविषादयोगः' \
  --page-id 164 \
  --revision-id 343151 \
  --output-dir content/raw/sanskrit/wikisource/chapter-01

# Checksums
shasum -a 256 -c content/checksums/raw.sha256

# Parse preserved snapshot
python3 content/normalization/parse_wikisource_chapter.py \
  --snapshot content/raw/sanskrit/wikisource/chapter-01/sa-wikisource-bg-chapter-01-revision-343151.json \
  --source-id bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151 \
  --output content/editorial/bhagavad-gita/chapter-01/wikisource-extraction.jsonl

# Phase 2 automated comparison (never approves)
python3 content/editorial/tools/compare_sources.py \
  --chapter-dir content/editorial/bhagavad-gita/chapter-01
python3 content/editorial/tools/validate_automated_comparison.py --check-determinism

# Validate workspace + post-approval state
python3 content/validation/validate_chapter01_workspace.py
python3 content/validation/validate_chapter_draft.py \
  content/editorial/bhagavad-gita/chapter-01/canonical-draft.jsonl
python3 content/editorial/tools/validate_normalization_match_approval.py
python3 content/editorial/tools/validate_orthographic_resolution.py

# Tests (offline)
python3 -m unittest discover content/editorial/tools/tests
python3 -m unittest discover content/validation/tests
python3 -m unittest discover content/acquisition/tests
python3 -m unittest discover content/normalization/tests
```

## Hard constraints

- Antar Chapter 1 expects **47** Verses (V003 seed).
- Do not mark remaining conflicts `APPROVED` without explicit human resolution.
- Do not invent, merge, split, reconstruct, or rewrite Sanskrit.
- Do not build an importable package until all 47 are approved and policy gates pass.
- Do not import into PostgreSQL from this workspace yet.
- Automated comparison is not scholarly approval.
