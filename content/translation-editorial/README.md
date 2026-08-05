# Translation Editorial

**Owner:** Content / Translation  
**Date:** August 2026

## Phase 3 — Segmentation policy (design)

**Status:** Policy defined — **no packaging or import**

Canonical Translation content is **segment-oriented and publisher-faithful:** one Translation Segment holds one publisher English unit and may cover one or many Verse identities. Antar must not invent splits or silently duplicate paragraphs.

| File | Role |
|------|------|
| [`translation-segmentation-policy.md`](translation-segmentation-policy.md) | Normative policy |
| [`translation-segmentation-decision.md`](translation-segmentation-decision.md) | Options evaluated + chosen decision |
| [`translation-segmentation-examples.md`](translation-segmentation-examples.md) | Worked examples (Swarupananda Ch1) |
| [`translation-segmentation-future-design.md`](translation-segmentation-future-design.md) | Package / importer / API / mobile implications (no implementation) |
| [`translation-segmentation-faq.md`](translation-segmentation-faq.md) | FAQ |

## Edition substitution & source recovery (policy)

**Status:** Policy defined — **no acquisition, workspace edits, or approvals in this documentation pass**

Governs when a later edition may (or may not) fill gaps in a selected primary Translation edition. Reusable for all future Translation sources.

| File | Role |
|------|------|
| [`edition-substitution-policy.md`](edition-substitution-policy.md) | Normative policy (source classes, gates, matrix) |
| [`edition-substitution-decision.md`](edition-substitution-decision.md) | Current Swarupananda application (1909 vs 1926) |
| [`edition-substitution-faq.md`](edition-substitution-faq.md) | FAQ |

## Phase 4 — Chapter 1 workspace (draft extraction)

**Status:** Draft segment workspace — **not approved**, **not packaged**, **not imported**

| Path | Role |
|------|------|
| [`swarupananda-1909/chapter-01/`](swarupananda-1909/chapter-01/) | Chapter 1 segment drafts + coverage map |
| [`tools/`](tools/) | Extract/validate helpers + offline tests |

Related:

- Phase 1 selection: [`content/translation-selection/`](../translation-selection/)
- Phase 2 inspection: [`../translation-selection/swarupananda-1909-inspection.md`](../translation-selection/swarupananda-1909-inspection.md)
- ADR-012: Translation bounded context
- Editorial policy: [`docs/content/03_EDITORIAL_POLICY.md`](../../docs/content/03_EDITORIAL_POLICY.md)

## Explicit non-work

| Item | Status |
|------|--------|
| Backend / mobile / API / DB / V007 | Unchanged |
| Translation / Scripture importers | Unchanged |
| Package schema / builders | Unchanged |
| Translation package build / import | Not done |
| Editorial approval of Translation text | Not done (`APPROVED` = 0) |
| Edition substitution / gap acquisition | Policy only — no acquisition or workspace clearance |
| Git commit | Not done |
