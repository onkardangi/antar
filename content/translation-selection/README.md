# Translation Content — Selection & Inspection

**Status:** Besant & Das 1905 selected as **PRIMARY_TRANSLATION_CANDIDATE** for first production corpus (`ACQUIRED_UNREVIEWED`; Chapter 1 inspected). Swarupananda 1909 remains frozen as a separate future edition. Still **no normalization, packaging, or import**.  
**Owner:** Content / Translation  
**Date:** August 2026  

---

## Purpose

Document licensing-safe, verse-mappable English Translation candidates for Antar’s first real Translation corpus.

Related constraints:

- Translation is a separate bounded context ([ADR-012](../../docs/architecture/adr/ADR-012-translation-bounded-context.md))
- Antar Verse identities remain Scripture-owned (`1.1` … `18.78`; Chapter 1 = 47, Chapter 13 = 34, 700 Verses)
- Do not import unlicensed Translation ([`docs/content/03_EDITORIAL_POLICY.md`](../../docs/content/03_EDITORIAL_POLICY.md))

---

## Documents

| File | Role |
|------|------|
| [`candidate-comparison.md`](candidate-comparison.md) | Per-candidate research notes |
| [`recommendation.md`](recommendation.md) | Original Phase 1 recommendation (Swarupananda primary; Besant fallback) |
| [`licensing.md`](licensing.md) | Copyright, PD, redistribution, attribution |
| [`acquisition-plan.md`](acquisition-plan.md) | Original Swarupananda acquisition plan |
| [`risk-analysis.md`](risk-analysis.md) | Risks and mitigations |
| [`decision.md`](decision.md) | Scored decision matrix + pipeline roadmap |
| [`swarupananda-1909-inspection.md`](swarupananda-1909-inspection.md) | Swarupananda acquisition + Chapter 1 inspection (blocked gaps) |
| [`swarupananda-1909-chapter-01-labels.json`](swarupananda-1909-chapter-01-labels.json) | Swarupananda Chapter 1 label inventory |
| [`besant-das-1905-inspection.md`](besant-das-1905-inspection.md) | **Current primary** acquisition + Chapter 1 inspection |
| [`besant-das-1905-chapter01-inspection.json`](besant-das-1905-chapter01-inspection.json) | Full 47-Verse page-image audit |

Raw acquisitions:

- [`content/raw/translations/besant-das-1905/`](../raw/translations/besant-das-1905/) — **PRIMARY_TRANSLATION_CANDIDATE**
- [`content/raw/translations/swarupananda-1909/`](../raw/translations/swarupananda-1909/) — frozen future edition

---

## Current production path (summary)

**Decision:** `KEEP_SWARUPANANDA_BLOCKED_AND_SELECT_BESANT_DAS_V1`

| Rank | Candidate | Role |
|------|-----------|------|
| **1** | **Besant & Das 1905** | **PRIMARY_TRANSLATION_CANDIDATE** (acquired; Ch.1 audited) |
| — | Swarupananda 1909 | Frozen future edition (incomplete pinned scan / SOURCE_CONFLICT) |

---

## Explicit non-work (current phase)

| Item | Status |
|------|--------|
| Backend / mobile / API changes | Not done |
| Translation or Scripture importer changes | Not done |
| Database / V007 changes | Not done |
| Besant & Das raw acquisition | Done — `ACQUIRED_UNREVIEWED` |
| Besant Chapter 1 full label audit | Done — Package v1 compatible |
| Normalization / package generation | Not done |
| Editorial approval of Translation text | Not done |
| Git commit | Not done |

---

## Next phase (planned only)

```text
Editorial extraction (fluent free translation only)
  → Editorial review
  → Translation package (Chapter 1)
  → validate_package.py
  → Translation importer (existing)
  → Translation API serves real corpus
```
