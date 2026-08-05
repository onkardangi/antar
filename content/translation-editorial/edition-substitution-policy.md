# Antar Translation Edition Substitution & Source Recovery Policy

**Status:** Accepted (content policy)  
**Applies to:** All Translation sources Antar may acquire, recover, normalize, or publish  
**Does not:** Change runtime, packages, importers, APIs, databases, or existing workspace records in this phase  
**Companions:** [`edition-substitution-decision.md`](edition-substitution-decision.md), [`edition-substitution-faq.md`](edition-substitution-faq.md)  
**Related:** [`translation-segmentation-policy.md`](translation-segmentation-policy.md), [`docs/content/01_SCRIPTURE_PROVENANCE.md`](../../docs/content/01_SCRIPTURE_PROVENANCE.md), [`docs/content/02_CONTENT_PIPELINE.md`](../../docs/content/02_CONTENT_PIPELINE.md), [`docs/content/03_EDITORIAL_POLICY.md`](../../docs/content/03_EDITORIAL_POLICY.md), ADR-012

---

## 1. Purpose

Translation editions are historically layered: first printings, impressions, revised editions, reprints, host transcriptions, and OCR derivatives.

Physical and digital masters are sometimes **incomplete** (missing leaves, cropped pages, damaged scans). Antar must recover evidence without silently substituting a different edition’s wording as if it were the selected primary source.

This policy defines:

- how sources are classified,
- what “recovery,” “verification,” “substitution,” “normalization,” and “approval” mean,
- when a later edition may or may not fill gaps in an earlier edition,
- mandatory gates, overlap checks, review strength, and audit requirements.

The policy is **reusable for all future Translation work**. Examples may cite specific editions; rules are not edition-specific.

---

## 2. Scope

### In scope

- English and other-language Translation acquisitions under Translation BC (ADR-012)
- Page-image and structured Translation masters
- Supplemental scans, witnesses, OCR aids, and host transcriptions
- Editorial workspace drafts, status transitions, and provenance notes
- Decisions that affect whether gap text may enter normalized packages later

### Out of scope (this policy does not authorize)

- Changing Scripture Sanskrit / Verse identities
- Mixing commentary into Translation text
- AI-authored “in the style of” Translation
- Silent Reader substitution of another edition’s wording (see `03_EDITORIAL_POLICY.md` §6)
- Automated split/merge of publisher Translation units (see segmentation policy)

### Relationship to silence

Missing Translation for a Verse is an acceptable product state. **Silence beats substitution.**

---

## 3. Terminology

| Term | Meaning |
|------|---------|
| **Primary edition** | The edition/impression Antar selected as the Translation corpus target (e.g. a named first edition year) |
| **Pinned master** | The registered raw artifact (usually page-image PDF/scan) treated as authoritative for all **present** pages of the primary edition |
| **Gap** | Printed page(s), leaf(ves), or publisher unit(s) absent or illegible in the pinned master |
| **Overlap page** | A page present in both the pinned master and a candidate recovery source, used for identity comparison |
| **Publisher unit** | One fluent Translation prose block as printed for a labeled span (not gloss, not commentary) |
| **Recover** | Obtain page-image (or equivalent primary-class) evidence that makes a gap’s publisher unit readable |
| **Verify** | Confirm that candidate text/images match the intended edition identity and publisher unit boundaries |
| **Substitute** | Place wording from a non-primary edition/impression into records attributed to the primary edition |
| **Normalize** | Deterministic packaging of approved editorial text into Antar’s Translation package format (later stage) |
| **Approve** | Editorial sign-off that a Segment or corpus may proceed toward package/import (`APPROVED` / `APPROVED_FOR_IMPORT`) |
| **Edition substitution** | Any use of non-primary edition text as if it were primary-edition wording |

---

## 4. Source classes

Every Translation-related artifact used in editorial work must be labeled with exactly one primary class (and optional secondary roles).

### 4.1 `PRIMARY_SOURCE`

**What it is:** The selected edition’s registered master for the corpus effort.

**May be used for:** Establishing publisher units; page evidence for present leaves; normalization and eventual approval of text taken from its images.

**Must not be used for:** Inventing missing leaves; being silently overwritten by later editions.

**Rule:** Preserve the pinned master byte-immutable. Gaps stay gaps until policy-compliant recovery.

---

### 4.2 `SUPPLEMENTAL_VERIFICATION_SOURCE`

**What it is:** An independently digitized scan of the **same** edition/impression (or an approved corrected impression of that edition), acquired to confirm or restore pages missing from the pinned master.

**May be used for:** Filling gaps **only after** identity gates pass; page-image verification; correcting OCR misreads against images of the **same** edition.

**Must not be used for:** Replacing the primary source role; normalizing as a different edition without a separate corpus decision; clearing conflicts when revision statements or overlap checks fail.

---

### 4.3 `EDITORIAL_WITNESS`

**What it is:** A related but **not identical** printing—typically a later revised edition of the same translator/publisher tradition—consulted to understand likely wording, labels, or structure while primary pages are missing.

**May be used for:** Informing hypotheses; locating combined labels; drafting provisional text that remains `SOURCE_CONFLICT`; planning recovery.

**Must not be used for:** Automatically clearing `SOURCE_CONFLICT`; serving as normalization master for a primary-edition corpus; Reader-facing text attributed solely to the primary edition without an explicit substitution decision and stronger review.

---

### 4.4 `SECONDARY_REFERENCE`

**What it is:** Catalog records, bibliographies, WorldCat/Hathi listings, publisher histories, inspection notes—not page images of the Translation body.

**May be used for:** Edition identification, dating, license context, finding candidates.

**Must not be used for:** Establishing fluent Translation wording.

---

### 4.5 `OCR_AID`

**What it is:** Machine OCR (DjVuTXT, Abbyy, etc.) derived from a scan.

**May be used for:** Locating pages/labels; drafting candidates for human image check.

**Must not be used for:** Canonical Translation text; approving Segments; resolving conflicts without page-image confirmation.

---

### 4.6 `HOST_TRANSCRIPTION`

**What it is:** Third-party HTML/etext (e.g. Sacred Texts, Gutenberg-style hosts) claiming to represent an edition.

**May be used for:** Cross-check hints; searchability; provisional drafts marked conflicted.

**Must not be used for:** Recovery master; primary evidence; automatic approval; sole basis for edition substitution.

---

### 4.7 `COMMENTARY_SOURCE`

**What it is:** Bracketed notes, footnotes, introductions, or separate commentary volumes.

**May be used for:** Understanding BC / commentary pipeline (separate policies).

**Must not be used for:** `translationText` of Translation Segments.

---

## 5. Distinguishing editorial actions

| Action | Changes workspace text? | Clears conflict by itself? | Implies Reader publish? | Implies package/import? |
|--------|-------------------------|----------------------------|-------------------------|-------------------------|
| **Recover** | May, if image-verified under policy | No | No | No |
| **Verify** | No (or annotations only) | No | No | No |
| **Substitute** | Yes (explicit, audited) | Only after gates + stronger review | No until approve | No until approve |
| **Normalize** | Produces package artifacts | Requires prior approval path | No | Prerequisite only |
| **Approve** | Status → approved forms | Yes (for that unit) | Enables publish path | Enables import path |

**Normative:** A recovered page is **not** automatically approved. Recovery ≠ substitution ≠ normalization ≠ approval.

---

## 6. Edition relationship classes

For each candidate relative to the primary edition, classify the relationship, then apply the matrix in §10.

| Relationship | Meaning | Default stance |
|--------------|---------|----------------|
| **Same printing / same digitization** | Same physical book campaign, same IA/DLI item family | Use as primary or re-pin only with checksum discipline |
| **Same edition, different scan** | Same edition statement; independent digitization | Preferred recovery path (`SUPPLEMENTAL_VERIFICATION_SOURCE`) |
| **Same edition, different impression** | Same edition designation; later impression without claimed textual revision | Allowed with review + overlap |
| **Corrected impression** | Errata/corrections announced; same edition lineage | Allowed only with review; document each correction |
| **Revised edition** | Explicit revision language (“revised,” “enlarged,” “fourth edition… slightly revised”) | **Witness by default**; substitution only via explicit decision |
| **Different publisher** | Publisher/imprint changed | Forbidden as silent fill; requires new corpus decision |
| **Modern reprint** | Contemporary commercial reprint of PD text | Forbidden as recovery master unless page-identical to primary and licensed/cleared |
| **Translation rewrite** | Different translator or substantially new English | Forbidden for filling the primary corpus |

### 6.1 Per-relationship outcomes

| Relationship | Recover gap text into primary-attributed records? | Notes |
|--------------|---------------------------------------------------|-------|
| Same edition, different scan | **Allowed** after identity + overlap gates | Preferred |
| Same edition, different impression | **Allowed only with review** | Two-reviewer if any doubt |
| Corrected impression | **Allowed only with review** | List corrections touching affected Verses |
| Revised edition | **Forbidden by default**; **Allowed only with review** after explicit substitution decision | Stronger review mandatory |
| Different publisher | **Forbidden** for primary attribution | Start separate source selection |
| Modern reprint | **Forbidden** as master unless proven page-identical + rights | Usually reject |
| Translation rewrite | **Forbidden** | Different corpus |

---

## 7. Acceptable recovery

Recovery is acceptable when **all** of the following hold:

1. The pinned primary master remains unchanged and cited for all present pages.  
2. The recovery artifact is registered with checksums and class (`SUPPLEMENTAL_VERIFICATION_SOURCE` or, after explicit decision, a documented substitution from an `EDITORIAL_WITNESS`).  
3. Gap pages are visible as **page images** (not OCR-only, not host HTML-only).  
4. Edition identity gates (§8) pass for the intended use.  
5. Overlap comparison (§9) does not show `SUBSTANTIVE_VARIANT` on required overlaps—or an explicit substitution decision accepts residual risk with audit.  
6. Fluent English is separable from gloss/commentary.  
7. Status remains below `APPROVED` until ordinary (or stronger) approval workflow completes.  
8. Package/import readiness stays false until packaging policy and approval allow.

### Unacceptable “recovery”

- Quietly pasting Sacred Texts / OCR into primary records as if scanned from the primary  
- Replacing the primary source role with a later edition without a corpus re-selection  
- Harmonizing primary and witness wording (“best of both”)  
- Clearing `SOURCE_CONFLICT` solely because a later edition “looks complete”

---

## 8. Mandatory gates

Before any gap text attributed to the primary edition may move from `SOURCE_CONFLICT` to `READY_FOR_REVIEW` (or stronger), record pass/fail for:

| Gate | Requirement |
|------|-------------|
| **Edition identity** | Candidate’s edition/impression statement matches the intended recovery class |
| **Publisher identity** | Publisher/imprint consistent with class rules (§6) |
| **Translator identity** | Same named translator (or explicit corpus change) |
| **Overlap comparison** | Required overlaps evaluated and classified (§9) |
| **Revision statement review** | Any “revised,” “enlarged,” “corrected,” or impression preface reviewed and filed |
| **Text comparison** | Affected publisher units compared; differences logged |
| **Reviewer approval** | Review strength per §11 satisfied for the intended status |
| **Audit trail** | Permanent record per §12 |

Failure of any gate ⇒ keep `SOURCE_CONFLICT` (or reject the candidate).

---

## 9. Overlap check

### 9.1 Choosing overlap pages

Prefer pages that:

1. Exist in the **pinned primary** and the candidate,  
2. Are adjacent to gaps when possible (context continuity),  
3. Include both 1:1 and N:1 publisher units if the chapter has both,  
4. Include speaker changes and distinctive orthography (diacritics, archaisms).

Minimum for a multi-page gap cluster: **at least two** non-trivial overlap pages bracketing the gap when available; otherwise the nearest available overlaps plus an explicit risk note.

### 9.2 What to compare

On each overlap page, compare:

- source labels (including combined labels),  
- fluent `translationText` wording,  
- spelling and diacritics,  
- punctuation and italics/emphasis if meaning-bearing,  
- paragraph/unit boundaries,  
- exclusion of gloss and commentary.

Do **not** require identical running headers, page numbers, or printer ornaments.

### 9.3 Variant classes

| Class | Definition | Effect on recovery |
|-------|------------|--------------------|
| **IDENTICAL** | Fluent unit matches character-for-character (allowing Unicode normalization that does not change visible spelling) | Supports recovery |
| **TYPOGRAPHIC_VARIANT** | Broken type, OCR noise in *candidate aid*, hyphenation across line breaks, or scan artifacts—not a different published wording | Supports recovery after image confirmation of intended spelling |
| **EDITORIAL_VARIANT** | Intentional but minor published difference (comma vs semicolon, “O” vs “Oh,” hyphenation of compounds) without semantic change | Blocks automatic clear; requires documented review |
| **SUBSTANTIVE_VARIANT** | Word substitution, omission, addition, reordering, or changed coverage/labels | Blocks primary-attributed recovery unless an explicit substitution decision accepts it with stronger review |

### 9.4 Why overlap alone is insufficient for revised editions

Overlap pages can match while **gap pages were revised**. A preface that admits revision (“slightly revised in places”) is direct evidence that identity is **not** page-global. Therefore:

```text
Overlap IDENTICAL ⇏  Gap pages are primary-edition text
```

Revised-edition candidates remain `EDITORIAL_WITNESS` until an explicit editorial decision authorizes substitution (or a same-edition complete scan is acquired).

---

## 10. Decision matrix

| Case | Recover? | Verify? | Normalize as primary? | Approve as primary? |
|------|----------|---------|-------------------------|---------------------|
| Same edition, different scan (complete gap pages) | Yes (after gates) | Yes | Only after approval workflow | Only after approval |
| Same edition, different impression | Yes w/ review | Yes | Only after approval | Two-reviewer if any `EDITORIAL_VARIANT` |
| Corrected impression | Yes w/ review | Yes | Only after listing corrections | Two-reviewer recommended |
| Later **revised** edition | No by default; Yes only after explicit substitution decision | Yes (as witness always) | No unless substitution decision + stronger review | Stronger review mandatory |
| Publisher changed | No | Secondary only | No | No (new selection) |
| Translator changed | No | No for wording | No | No |
| Missing pages only (same edition scan) | Yes | Yes | After approval | After approval |
| OCR only | No | Locator only | No | No |
| Host transcription only | No | Aid only | No | No |
| Modern copyrighted reprint | No | No | No | No |
| Partial illegible primary page | Prefer same-edition supplemental image | Yes | After approval | After approval |

Legend: **Normalize/Approve** columns assume a **primary-edition corpus**. Choosing a later edition as a **new primary corpus** is a separate selection decision, not gap-fill.

---

## 11. Reviewer responsibilities

### 11.1 Ordinary normalization / draft review (no edition substitution)

One qualified reviewer may move Segments to `READY_FOR_REVIEW` when:

- text is from the pinned primary or an approved same-edition supplemental scan,  
- gates pass with only `IDENTICAL` / resolved `TYPOGRAPHIC_VARIANT`,  
- no revised-edition substitution is involved.

`APPROVED` still follows the ordinary Translation approval policy (separate from this document’s recovery rules) and must not be automatic.

### 11.2 Stronger review (mandatory two reviewers)

Require **two independent reviewers** when any of:

- recovering from a **revised edition** under an explicit substitution decision,  
- any `EDITORIAL_VARIANT` or `SUBSTANTIVE_VARIANT` is accepted into primary-attributed text,  
- overlap set is thinner than policy minimum,  
- revision statements exist and gaps are filled from that witness,  
- combined-label coverage for gap Verses is inferred partly from a non-primary witness.

Edition substitution requires **stronger review than ordinary normalization**.

### 11.3 Reviewer duties

Reviewers must:

1. Inspect page images (not OCR alone),  
2. Confirm source class and gates,  
3. Confirm commentary/gloss exclusion,  
4. Confirm coverage sets and labels,  
5. Refuse clearance when silence is safer,  
6. Sign the audit record.

---

## 12. Audit requirements

For every gap recovery or substitution decision, permanently record:

| Field | Content |
|-------|---------|
| Original gap | Printed pages / leaves / Segment IDs / Verse refs |
| Replacement source | Registry id, class, checksums, URL |
| Reason | Why recovery/substitution was attempted |
| Overlap results | Pages compared + variant class per unit |
| Revision statements | Quoted/cited |
| Decision | Recover / witness-only / substitute / reject / defer |
| Reviewers | Names/ids + dates |
| Affected Verses | Canonical references |
| Reversibility | How to revert to pre-recovery text and restore `SOURCE_CONFLICT` |

Store under Translation editorial docs / registry decision fields / workspace recovery reports as applicable. Do not delete prior conflict notes; append resolution history.

---

## 13. Allowed outcomes

| Outcome | Meaning |
|---------|---------|
| **DEFER** | Keep `SOURCE_CONFLICT`; silence for publish |
| **WITNESS_ONLY** | Consult later edition; do not clear conflicts |
| **RECOVER_SAME_EDITION** | Fill from same-edition supplemental scan; then ordinary review path |
| **SUBSTITUTE_WITH_DECISION** | Explicit audited use of non-primary edition text for named gaps |
| **RESELECT_CORPUS** | Abandon primary edition as corpus target; start selection for another edition |
| **REJECT_CANDIDATE** | Candidate unusable for recovery |

---

## 14. Forbidden practices

1. Silent edition substitution into primary-attributed records.  
2. Clearing `SOURCE_CONFLICT` because a later edition is complete.  
3. Treating overlap matches as proof that revised-edition gap pages match the primary.  
4. Using host transcription or OCR as recovery master.  
5. Merging wording from multiple sources into a composite “improved” Translation.  
6. Modernizing spelling/punctuation while attributing an older edition.  
7. Approving recovered text in the same step as first sight of a supplemental image.  
8. Changing the primary source role without registry process.  
9. Building/importing packages from unresolved conflict text.  
10. Presenting witness text to Readers as the primary edition.

---

## 15. Special case pattern (incomplete primary + revised later edition)

When:

- primary edition pinned master is incomplete, and  
- a later edition exists and states revision,

then **by default**:

1. Classify the later edition as `EDITORIAL_WITNESS`.  
2. Keep affected Segments at `SOURCE_CONFLICT`.  
3. Do not treat acquisition of the later edition as conflict clearance.  
4. Prefer searching for a complete **same-edition** scan.  
5. Only an explicit substitution decision (with stronger review and full audit) may authorize primary-attributed use of witness wording for named gaps—or a corpus reselection may adopt the later edition as a **new** primary.

This pattern is general; a concrete application appears in [`edition-substitution-decision.md`](edition-substitution-decision.md).

---

## 16. Status transitions (recovery-related)

```text
SOURCE_CONFLICT
  → (same-edition image recovery + gates) → READY_FOR_REVIEW
  → (ordinary approval) → APPROVED   [separate approval policy]

SOURCE_CONFLICT
  → (witness only / failed gates) → SOURCE_CONFLICT (unchanged)

SOURCE_CONFLICT
  → (explicit substitution decision + stronger review) → READY_FOR_REVIEW
```

No path jumps to `APPROVED` from recovery alone.

---

## 17. Implementation status

| Item | Status |
|------|--------|
| This policy | Documented |
| Runtime / packages / importers | Unchanged by this document |
| Any specific corpus recovery acquisition | Not authorized by this document alone |
| Approvals | None granted by this document |
