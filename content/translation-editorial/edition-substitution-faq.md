# Edition Substitution & Source Recovery — FAQ

**Policy:** [`edition-substitution-policy.md`](edition-substitution-policy.md)  
**Current-case decision:** [`edition-substitution-decision.md`](edition-substitution-decision.md)

---

## Why not simply use the later edition?

Because Antar selected a **specific primary edition**. A later revised edition is a different published object—even from the same translator and house. Using it quietly as if it were the primary misstates provenance and can change wording Readers believe is the chosen edition.

If the later edition should become the corpus, that is a **corpus reselection**, not gap-fill.

---

## Why isn’t overlap enough?

Overlap proves similarity on **pages that exist in both scans**. It does not prove the **missing** pages were never revised. When a later edition states it was “revised in places,” gap pages are exactly where hidden revisions may live.

```text
Matching overlaps ≠ identical book
```

---

## What if no first-edition complete scan exists?

Allowed paths, in order of preference:

1. Keep searching reputable repositories for a same-edition scan.  
2. Leave gaps as `SOURCE_CONFLICT` / unpublished (silence).  
3. Explicit audited **substitution** decision with stronger review.  
4. **Reselect** a complete edition as the new primary corpus.

There is no path that invents text or launders a host transcription into the primary.

---

## Can Sacred Texts fill gaps?

**No** as recovery master. Sacred Texts (and similar hosts) are `HOST_TRANSCRIPTION`: useful as a locator or cross-check, never as the authoritative page evidence for clearing conflicts or approving Segments.

---

## Can OCR become canonical?

**No.** OCR is an `OCR_AID`. Canonical Translation text requires human confirmation against page images of an allowed source class.

---

## Can later punctuation be copied?

Not into primary-attributed records without following variant classes:

- Accidental line-break hyphens → resolve from images (`TYPOGRAPHIC_VARIANT`).  
- Published punctuation differences (`EDITORIAL_VARIANT`) → require review; do not silently adopt the later form while claiming the earlier edition.  
- Wording changes → `SUBSTANTIVE_VARIANT`; blocked unless substitution decision.

Do not “modernize” older punctuation to match a later edition.

---

## What is the difference between recovering and substituting?

| | Recover | Substitute |
|-|---------|------------|
| Source class | Same edition (supplemental scan) preferred | Non-primary edition/impression used for primary-attributed text |
| Claim | “This is the primary edition’s missing page” | “We knowingly use another edition’s page for this gap” |
| Default when preface says “revised” | Not available from that witness | Requires explicit decision |

---

## Does recovering a page approve it?

**No.** Recovery can at most support moving toward `READY_FOR_REVIEW` after gates. `APPROVED`, packaging, and import are separate steps.

---

## Is a corrected impression the same as a revised edition?

No. A **corrected impression** claims errata fixes within an edition lineage. A **revised edition** claims broader textual change. Both need review; revised editions default to witness-only for gap-fill.

---

## When is one reviewer enough?

When gap text comes from a **same-edition** supplemental page image, gates pass with only `IDENTICAL` / resolved typographic issues, and no revised-edition substitution is involved—and only for moving to `READY_FOR_REVIEW`, not automatic `APPROVED`.

---

## When are two reviewers mandatory?

Whenever revised-edition substitution is proposed; any accepted `EDITORIAL_VARIANT` / `SUBSTANTIVE_VARIANT`; thin overlap evidence; or combined-label coverage for gaps depends heavily on a non-primary witness.

Edition substitution always needs **stronger** review than ordinary normalization.

---

## Can we mix the best wording from 1909 and 1926?

**No.** Composite text is forbidden. One publisher unit from one allowed source class, with audit.

---

## What if the primary and witness use different combined labels?

Do not invent splits to reconcile them. Record the conflict. Prefer primary-edition page evidence. If only the witness shows a combined label for missing primary pages, keep `SOURCE_CONFLICT` until same-edition evidence or an explicit substitution decision addresses the label.

---

## Does registering a supplemental scan change the primary source?

**No.** Supplemental registration must not alter the primary source role. Classes and permitted uses are recorded separately.

---

## What should Readers see for conflicted Verses?

Unavailable / silent Translation for those Verses (or Segments), not guessed text and not unlabeled later-edition wording.

---

## How does this relate to segmentation policy?

Segmentation policy forbids inventing splits/duplicates of publisher units. Edition-substitution policy forbids inventing **which edition** the unit came from. Both protect publisher-faithful provenance.

---

## Current Swarupananda status in one line?

**1909 remains primary; 1926 is an editorial witness; conflicts stay conflicts until a further explicit decision.**
