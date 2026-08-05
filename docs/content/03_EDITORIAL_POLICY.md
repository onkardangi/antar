# 03 — Editorial Policy

**Status:** Foundation (policy + Chapter 1 Sanskrit editorial approval complete; package built and imported)
**Owner:** Content / Product  
**Last Updated:** August 2026

---

## 1. Purpose

Define editorial principles for approving Scripture-related content into Antar.

Antar is contemplative and restraint-oriented. Editorial work protects:

- Scripture integrity,
- Reader trust,
- attribution,
- silence where content is not ready.

Related:

- ADR-010 — Scripture is the source of truth
- [`01_SCRIPTURE_PROVENANCE.md`](01_SCRIPTURE_PROVENANCE.md)
- [`02_CONTENT_PIPELINE.md`](02_CONTENT_PIPELINE.md)
- Domain Dictionary — Scripture, Chapter, Verse

---

## 2. Editorial workflow

```text
Candidate source inspected
    → Edition/numbering gate
    → License gate
    → Quality gate (Sanskrit / transliteration)
    → Normalization review (deterministic only)
    → Validation gate
    → Editorial sign-off record
    → APPROVED_FOR_IMPORT
```

### 2.1 Roles (logical)

| Role | Responsibility |
|------|----------------|
| Acquirer | Obtains raw bytes; does not edit them |
| Inspector | Documents structure and defects |
| Editor | Judges edition fitness, text quality, attribution |
| Approver | Sets registry status to `APPROVED_FOR_IMPORT` |
| Importer (future) | Loads only approved packages |

One person may hold multiple roles in early stages; the **decision record** must still exist.

### 2.2 Sign-off record (minimum)

For each approved package, record:

- corpus id + version,
- raw SHA-256,
- normalized SHA-256,
- edition confirmation (Ch. 1 = 47, Ch. 13 = 34, total 700),
- license clearance statement,
- known residual defects (if any) and why they are acceptable,
- approver name/date.

Store sign-off in the normalized package `NOTES.md` and/or registry `decision_summary` until a richer workflow exists.

---

## 3. Edition and segmentation rules

1. Antar’s approved tradition is **Chapter 1 = 47**, **Chapter 13 = 34**, **700** verses across **18** Chapters.
2. Alternate traditions (e.g. As It Is–style **46 / 35**) are legitimate historically but **not** Antar’s canonical import target.
3. **No automated splitting, joining, or renumbering** of canonical Sanskrit to coerce Antar counts.
4. If a source requires editorial splitting/merging of verses, that work needs an **explicit approved editorial process** (separate decision), not a normalization script.
5. Rejecting a source for numbering mismatch is **not** a claim that the source is inaccurate.

---

## 4. Sanskrit editorial standards

When Sanskrit is approved for import into `scripture.verses.sanskrit_text`:

1. Text must be real Scripture content, never placeholders.
2. Prefer a coherent edition; do not mix incompatible segmentations mid-corpus.
3. Preserve approved Unicode; reject literal escape garbage.
4. Speaker lines, dandas, and verse markers may be retained **only** if intentionally approved for Antar’s stored form.
5. Silence is acceptable: leaving `sanskrit_text` NULL is better than shipping unapproved text.

---

## 5. Transliteration editorial standards

1. Transliteration is not Sanskrit and not Translation.
2. Scheme must be labeled (`IAST`, `ISO_15919`, `SIMPLIFIED_LATIN`).
3. Sandhi-separated study forms, if kept, are a distinct field/layer — not a replacement for Sanskrit.
4. Hyphenation and avagraha conventions must be consistent within a source.

---

## 6. Future translation policy

1. Translations require identifiable sources (`scripture.translation_sources` fields: name, translator, publisher, edition, year, language, license).
2. **Do not import unlicensed Translation content.**
3. Every Translation row retains attribution; no anonymous “English meaning.”
4. Early product may ship with limited licensed Translation coverage; partial coverage is allowed if UX treats missing Translation as unavailable, not invented.
5. Reader preference for Translation is explicit (API/product model); do not silently substitute another edition’s wording.
6. AI must never author Translation presented as Scripture or as a traditional Translation source.

---

## 7. Future commentary policy

1. Commentary must be attributed (`commentary_sources` / `commentary_passages`).
2. Do not store unattributed text as traditional commentary.
3. License, tradition, and edition metadata are mandatory before publication.
4. Editorial summaries and Understanding articles are **not** commentary; keep them distinguishable.
5. Saar and generative output are **not** commentary and must never be imported into commentary tables.
6. Commentary is later than Sanskrit foundation; absence of commentary is an acceptable V1 state.

---

## 8. Hierarchy reminder (non-negotiable)

```text
Scripture
  → Traditional Commentary
    → Curated Understanding
      → Saar
```

Editorial mistakes that blur this hierarchy are product defects.

---

## 9. Rejection and restraint

Editorial refusal is a feature.

Valid refusal reasons include:

- edition/numbering mismatch with Antar seed,
- license insufficiency for distribution,
- irreproducible provenance,
- text quality defects that require non-deterministic invention,
- presence of Translation/Commentary without rights,
- pressure to “just import something” for demos.

The Tarun Tiwari Kaggle dataset remains `REJECTED_FOR_CANONICAL_IMPORT` under this policy: alternate numbering tradition; technical title/escape defects are secondary.

---

## 10. Implementation status

| Item | Status |
|------|--------|
| Editorial policy | Documented (this file) |
| Approved corpus editorial pass | **Complete for Chapter 1** — 47 Verses approved (34 normalization-match + 11 orthographic + 2 final-conflict); packaged as `bhagavad-gita-chapter-01-v1`; imported |
| Translation corpus | **Not started** |
| Commentary corpus | **Not started** |
| Database Scripture body text | **Imported** for Chapter 1 (47 Sanskrit Verses); Chapters 2–18 not imported |
