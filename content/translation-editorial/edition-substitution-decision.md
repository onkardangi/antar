# Edition Substitution — Decision Record

**Status:** Accepted (policy application for current Translation effort)  
**Date:** August 2026  
**Policy:** [`edition-substitution-policy.md`](edition-substitution-policy.md)  
**Scope of this record:** Apply the general policy to the Swarupananda English Translation selection; **do not** change workspace text, registry, or raw acquisitions in this documentation-only phase.

---

## 1. Context

| Item | State |
|------|-------|
| Selected primary edition | Swami Swarupananda, *Srimad-Bhagavad-Gita*, **First Edition 1909**, Prabuddha Bharata Press / Mayavati |
| Primary registry role | `PRIMARY_TRANSLATION_CANDIDATE` (`bhagavad-gita-translation-en-swarupananda-1909-v1`) |
| Pinned master | IA/DLI `in.ernet.dli.2015.386852` |
| Known defect | Printed pages **14–15, 17–18, 20–21** absent from pinned scan leaves |
| Chapter 1 workspace | Draft segments; **12** records at `SOURCE_CONFLICT` (provisional secondary evidence) |
| Candidate complete scan | IA/DLI `in.ernet.dli.2015.20768` — **Fourth Edition, 1926**, Advaita Ashrama Mayavati |
| 1926 preface fact | States the book has been **“slightly revised in places.”** |

No Translation Segments are approved. No Translation package is built. Package v1 still cannot honestly represent N→1 segments.

---

## 2. Options evaluated

### Option A — Treat 1926 as automatic gap-fill for 1909

Acquire 1926 pages, copy fluent English into 1909-attributed Segments, clear `SOURCE_CONFLICT`.

| Pros | Cons |
|------|------|
| Fast completeness | Violates edition identity |
| Pages exist | Preface admits revision |
| | Overlap success cannot prove gap identity |
| | Misattributes revised wording as First Edition |

**Verdict:** **Rejected.**

### Option B — Reselect 1926 Fourth Edition as the primary Translation corpus

Abandon 1909 as corpus target; run selection/inspection for 1926 as primary.

| Pros | Cons |
|------|------|
| Complete page images available | Different edition than Phase 1/2 decision |
| Clear provenance if done openly | Requires new selection/licensing/inspection cycle |
| | “Slightly revised” may still need editorial characterization |
| | Throws away 1909 work already done on present pages |

**Verdict:** **Deferred** — valid future path, **not** chosen now. Would be a **corpus reselection**, not silent substitution.

### Option C — Classify 1926 as `EDITORIAL_WITNESS`; keep conflicts

Do not clear conflicts. Keep 1909 as primary. Use 1926 only as witness / planning aid until same-edition recovery or an explicit substitution decision.

| Pros | Cons |
|------|------|
| Honest provenance | Gaps remain unpublished |
| Aligns with silence-over-substitution | Editorial pressure to “just finish Chapter 1” |
| Preserves Phase 1 edition choice | Requires patience / further search |

**Verdict:** **Accepted for current status.**

### Option D — Explicit substitution decision for named gaps only

After full policy gates, two-reviewer sign-off, and audit, allow 1926 wording into primary-attributed gap Segments with permanent disclosure.

| Pros | Cons |
|------|------|
| Could unblock gaps if no 1909 scan appears | Still not First Edition text |
| Auditable | Stronger review + ongoing disclosure burden |
| | Overlap-insufficient risk remains |

**Verdict:** **Not authorized in this documentation phase.** May be proposed later only under [`edition-substitution-policy.md`](edition-substitution-policy.md) §6–12. **Not** automatic upon acquiring 1926 images.

---

## 3. Decision (normative for current case)

1. **Primary edition remains** Swarupananda **First Edition 1909**.  
2. **Pinned 1909 master remains** authoritative for all **present** pages.  
3. The **1926 Fourth Edition is currently only an `EDITORIAL_WITNESS`** (and/or prospective supplemental candidate pending registration).  
4. It does **not** automatically clear `SOURCE_CONFLICT` records.  
5. Chapter 1 affected Segments **remain `SOURCE_CONFLICT`** until:
   - a same-edition complete scan recovers the pages under policy, **or**
   - an explicit substitution decision (Option D) is separately accepted with stronger review and audit, **or**
   - a corpus reselection (Option B) is separately accepted.  
6. **Additional editorial decision is required** before any normalization changes that replace provisional gap text with 1926 page-image text attributed as 1909.  
7. Host transcriptions / OCR remain aids only; not recovery masters.  
8. **No approvals** are granted by this record.

---

## 4. Why overlap checking alone is insufficient here

Even if fluent English on shared pages (e.g. printed 13, 16, 19, 22) matches between 1909 and 1926:

- The 1926 preface **admits non-zero revision**.  
- Revisions may concentrate on pages **absent** from the 1909 pin.  
- Combined labels and punctuation on missing leaves (notably the disputed **28—29** grouping) cannot be proven from 1909 images that do not exist.  
- Therefore: **overlap IDENTICAL ⇏ gap pages are First Edition text.**

---

## 5. Why missing pages cannot automatically be accepted from 1926

Accepting them automatically would:

- perform **silent edition substitution**,  
- mislabel revised-edition wording as First Edition 1909,  
- violate Reader-trust and provenance rules in `03_EDITORIAL_POLICY.md`,  
- convert an `EDITORIAL_WITNESS` into a de facto primary without selection.

Silence / `SOURCE_CONFLICT` is the correct interim product state.

---

## 6. What additional editorial decision is required

Before any workspace normalization that clears these conflicts using 1926 images, editors must produce a **separate, signed decision** that chooses one of:

| Path | Required artifacts |
|------|-------------------|
| **Same-edition recovery** | Registered 1909-complete supplemental scan; overlap gates; image-verified units |
| **Explicit substitution** | Written acceptance of 1926-for-gap under primary attribution; two reviewers; full audit; Reader/provenance disclosure plan |
| **Corpus reselection** | New primary = 1926 (or other); Phase 1-style selection update; re-inspection |

Until that decision exists, **do not** change Segment statuses to `READY_FOR_REVIEW` solely because 1926 pages are available.

---

## 7. Source-class assignment (current)

| Artifact | Class |
|----------|-------|
| 1909 pinned IA master | `PRIMARY_SOURCE` |
| 1926 Fourth Edition scan (if/when acquired) | `EDITORIAL_WITNESS` until a later decision reclasses it |
| Sacred Texts / similar HTML | `HOST_TRANSCRIPTION` |
| DjVu/Abbyy OCR | `OCR_AID` |
| Phase 4 provisional gap text | Draft under `SOURCE_CONFLICT` — not approved |

---

## 8. Affected scope (informational)

Gap-dependent Chapter 1 work includes Segments covering Verses in ranges that fall on missing printed pages (approximately **1.26–1.30**, **1.32–1.37**, **1.41–1.44**, and related partial units), including the provisional **I. 28—29.** combined label. Exact Segment IDs live in the Chapter 1 workspace; this decision record does **not** edit them.

---

## 9. Explicit non-work (this phase)

| Item | Status |
|------|--------|
| Acquire 1926 files into `content/raw/` | Not done by this document |
| Registry supplement entry | Not done by this document |
| Workspace text / status updates | Not done by this document |
| Approvals / packages / imports | Not done |
| Backend / mobile / DB / V007 | Unchanged |

---

## 10. Future applicability

This decision is an **instance** of the general policy. Any future Translation with an incomplete primary and a revised later edition follows the same default: **witness-only until explicit further decision.**
