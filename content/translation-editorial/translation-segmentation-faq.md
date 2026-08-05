# Translation Segmentation — FAQ

---

### Is combined English a numbering mismatch?

**No.** If Chapter 1 has 47 identities and Chapter 13 has 34, Antar numbering matches. Combined English is a **segmentation** issue.

---

### Why not just duplicate the paragraph onto each Verse?

Because that stores a lie: three “translations” that are one publisher unit. It poisons provenance, migrates poorly, and trains tooling to expand combined labels automatically. **Option B is forbidden** as permanent practice.

---

### Why not split the English so each Verse looks unique?

Because Antar must not invent punctuation or sentence boundaries the publisher did not print. Different editors would split differently. **Option A is forbidden.**

---

### What does the Reader see on Verse 1.5 if English covers 1.4–1.6?

The full publisher English for the Segment, with a clear note that it covers 1.4–1.6. Sanskrit on the card remains 1.5 only.

---

### Can we ship Chapter 1 Translation before segment packaging exists?

Only for Verses that have approved **1:1** Segments, if a later phase allows partial publish. Verses locked inside N:1 Segments stay unavailable until segment-aware packaging exists — **not** until someone duplicates/splits them.

---

### Does this change ADR-012?

**No.** Translation remains a separate bounded context referencing Verse identity only. This policy refines **content shape**, not module ownership. A future ADR may accompany package/schema evolution.

---

### Does package v1 become invalid?

Package v1 remains valid for **synthetic fixtures** and any future **true 1:1** Segments. It is **insufficient** for N:1 publisher units. Do not abuse v1 to fake N:1.

---

### What about word-by-word paraphrase under combined labels?

Still **not** Translation. Extract fluent English only. Word-by-word may span the same coverage but is out of scope for `translationText`.

---

### What if two combined ranges overlap?

Invalid for one source version. Inspection/editorial must resolve; importer should reject overlaps when segment packaging exists.

---

### What if the publisher prints `I. 4. 5. 6.` but separate English sentences with clear verse markers inside?

Only treat as multiple Segments if **edition-native** markers unambiguously bind each sentence to one Verse **without editorial invention**. When unsure, prefer one N:1 Segment (publisher label wins) or leave unpublished.

---

### Does this policy apply to non-English Translations later?

**Yes.** Segmentation is about Verse coverage vs publisher units, not about English specifically.

---

### Who approves an N:1 Segment?

Same Translation editorial authority as 1:1: identifiable source, license, human review, no AI authorship — plus explicit coverage evidence (combined label or signed rationale).

---

### Is Arnold usable under this policy?

Only if an external, documented alignment maps poem lines to Verse identities **without inventing text**. Phase 1 already rejected Arnold as primary Verse Translation; this policy does not revive it via creative splitting.
