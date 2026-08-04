# Chapter 1 editorial workspace

Controlled workspace for Antar’s **47** Chapter 1 Verse identities (`1.1`–`1.47`).

## Status

| Item | State |
|------|-------|
| Identities scaffolded | Yes (47) |
| Wikisource source acquired | Yes (rev `343151`, `ACQUIRED_UNREVIEWED`) |
| Extraction JSONL | Yes (`wikisource-extraction.jsonl`, 47 verses) |
| Source comparison populated | Yes (1.1 has 2 sources; 1.2–1.47 Wikisource-only) |
| Automated comparison | Yes (`NORMALIZATION_MATCH` × 34; `SOURCE_CONFLICT` × 13) |
| IIT secondary verification | Yes (Verses 1.1–1.47, `VERIFICATION_ONLY`) |
| Human approval prep | Yes (34 batch candidates + 13 conflict analyses; all `PENDING`) |
| Sanskrit in canonical draft | No (`null`) |
| Records approved | 0 |
| Import readiness | `NOT_READY` |
| Database import | Not performed |

## Files

| File | Purpose |
|------|---------|
| `source-comparison.jsonl` | Per-Verse source evidence |
| `wikisource-extraction.jsonl` | Deterministic extraction from preserved revision |
| `canonical-draft.jsonl` | Canonical draft records (still unapproved / text `null`) |
| `automated-comparison-report.jsonl` | Phase 2 deterministic comparison results |
| `automated-comparison-run-meta.json` | Run timestamps / report checksum (non-deterministic metadata) |
| `audit-sample.json` | Deterministic audit-sample references |
| `automated-review-summary.md` | Human-readable Chapter batch summary |
| `normalization-match-approval-candidate.jsonl` | 34 PENDING batch-approval candidates (Wikisource exact text) |
| `normalization-match-review.md` | Pattern-grouped human review table |
| `source-conflict-analysis.jsonl` | 13 conflict analyses |
| `orthographic-patterns.md` | Orthographic cluster report (no rules added) |
| `third-reference-queue.json` | Verses needing a third witness |
| `chapter-01-approval-manifest.json` | Chapter approval manifest (`PENDING_EDITORIAL_REVIEW`) |
| `decisions.md` | Edition decisions and discrepancy log template |
| `review-checklist.md` | Human review checklist per Verse |
| `validation-report.md` | Acquisition + structural validation report |

Verse review decision history: [`content/editorial/reviews/1.1.md`](../../reviews/1.1.md)

## Policies

- [`docs/content/01_SCRIPTURE_PROVENANCE.md`](../../../docs/content/01_SCRIPTURE_PROVENANCE.md)
- [`docs/content/02_CONTENT_PIPELINE.md`](../../../docs/content/02_CONTENT_PIPELINE.md)
- [`docs/content/03_EDITORIAL_POLICY.md`](../../../docs/content/03_EDITORIAL_POLICY.md)
- [`content/editorial/AUTOMATED_REVIEW_POLICY.md`](../../AUTOMATED_REVIEW_POLICY.md)
- [`content/editorial/normalization-policy.json`](../../normalization-policy.json)

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

# Validate
python3 content/validation/validate_chapter01_workspace.py
python3 content/validation/validate_chapter_draft.py \
  content/editorial/bhagavad-gita/chapter-01/canonical-draft.jsonl

# Tests (offline)
python3 -m unittest discover content/editorial/tools/tests
python3 -m unittest discover content/validation/tests
python3 -m unittest discover content/acquisition/tests
python3 -m unittest discover content/normalization/tests
```

## Hard constraints

- Antar Chapter 1 expects **47** Verses (V003 seed).
- Do not mark `APPROVED` without human review.
- Do not modify `canonical-draft.jsonl` during source acquisition or automated comparison.
- Do not import into PostgreSQL from this workspace yet.
- Automated comparison is not scholarly approval.
