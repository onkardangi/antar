# Translation Content Phase 1 — Selection Foundation

**Status:** Selection complete; Swarupananda 1909 **acquired & Chapter 1 inspected** (`NEEDS_MANUAL_SEGMENTATION_POLICY`). Still **no normalization, packaging, or import**.  
**Owner:** Content / Translation  
**Date:** August 2026  
**Scope:** Select and inspect the first English Bhagavad Gita Translation candidate

---

## Purpose

Document a licensing-safe, verse-mappable English Translation candidate for Antar’s first real Translation corpus.

This folder is **research and decision foundation only**. It does not acquire text, normalize content, build packages, or import into `translation.*`.

Related product/architecture constraints:

- Translation is a separate bounded context ([ADR-012](../../docs/architecture/adr/ADR-012-translation-bounded-context.md))
- Antar Verse identities remain Scripture-owned (`1.1` … `18.78`; Chapter 1 = 47, Chapter 13 = 34, 700 Verses)
- Do not import unlicensed Translation ([`docs/content/03_EDITORIAL_POLICY.md`](../../docs/content/03_EDITORIAL_POLICY.md))
- Existing Translation package format and importer remain fixture-only until a real package is approved

---

## Documents

| File | Role |
|------|------|
| [`candidate-comparison.md`](candidate-comparison.md) | Per-candidate research notes |
| [`recommendation.md`](recommendation.md) | Why one candidate wins |
| [`licensing.md`](licensing.md) | Copyright, PD, redistribution, attribution |
| [`acquisition-plan.md`](acquisition-plan.md) | How to acquire later (not executed here) |
| [`risk-analysis.md`](risk-analysis.md) | Risks and mitigations |
| [`decision.md`](decision.md) | Scored decision matrix + pipeline roadmap |
| [`swarupananda-1909-inspection.md`](swarupananda-1909-inspection.md) | Phase 2 acquisition + Chapter 1 inspection |
| [`swarupananda-1909-chapter-01-labels.json`](swarupananda-1909-chapter-01-labels.json) | Chapter 1 structural label inventory |

Raw acquisition: [`content/raw/translations/swarupananda-1909/`](../raw/translations/swarupananda-1909/)

---

## Recommendation (summary)

**Primary recommendation:** Swami Swarupananda — *Srimad-Bhagavad-Gita* (Advaita Ashrama, Mayavati, **1909**)

**Runner-up:** Annie Besant & Bhagavan Das — *The Bhagavad-Gita* (Theosophical Publishing Society, **1905**)

**Not recommended as first Translation:** Sir Edwin Arnold (*The Song Celestial*) — poetic paraphrase without reliable verse numbering.

---

## Explicit non-work (this phase)

| Item | Status |
|------|--------|
| Backend / mobile / API changes | Not done |
| Translation or Scripture importer changes | Not done |
| Database / V007 changes | Not done |
| Raw text acquisition (Swarupananda 1909) | Done — `ACQUIRED_UNREVIEWED` |
| Chapter 1 inspection | Done — `NEEDS_MANUAL_SEGMENTATION_POLICY` |
| Normalization / package generation | Not done |
| Editorial drafts of Translation text | Not done |
| Git commit | Not done |

---

## Next phase (planned only)

```text
Raw acquisition
  → Verification
  → Normalization
  → Editorial review
  → Translation package
  → Translation importer
  → Translation API (existing foundation; real corpus)
```

Details: [`decision.md`](decision.md) § Implementation roadmap and [`acquisition-plan.md`](acquisition-plan.md).
