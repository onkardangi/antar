# Translation Segmentation — Examples

Illustrative only. **No Translation text is approved or normalized here.**  
Publisher wording below is paraphrased/placeholder where needed; use the 1909 scan for real extraction later.

Source context: Swami Swarupananda 1909, Chapter 1  
Inspection: `content/translation-selection/swarupananda-1909-inspection.md`

---

## Example 1 — 1:1 Segment (singleton label)

**Publisher label:** `I. 1.`  
**Coverage:** `{1.1}`  
**Segment type:** 1:1  

```text
Segment S-1.1
  coverage: [1.1]
  publisherLabel: "I. 1."
  translationText: «fluent English for verse 1 only»
  excludes: word-by-word, [commentary], Sanskrit
```

**Reader for Verse 1.1:** show `S-1.1` text; optional badge unnecessary (single Verse).

---

## Example 2 — N:1 Segment (Swarupananda 4–6)

**Publisher label:** `I. 4. 5. 6.`  
**Coverage:** `{1.4, 1.5, 1.6}`  
**Segment type:** N:1  

```text
Segment S-1.4-6
  coverage: [1.4, 1.5, 1.6]
  publisherLabel: "I. 4. 5. 6."
  translationText: «one fluent English unit covering the three ślokas»
  evidence: page image / combined label
```

### Forbidden Option A (split)

Do **not** invent:

```text
1.4 → first invented sentence
1.5 → second invented sentence
1.6 → third invented sentence
```

### Forbidden Option B (duplicate)

Do **not** store:

```text
1.4.translationText = FULL_UNIT
1.5.translationText = FULL_UNIT
1.6.translationText = FULL_UNIT
```

as three independent translations.

### Required Option C

One Segment; Verses 1.4, 1.5, and 1.6 all resolve to it.

**Reader behaviour:**

| Open Verse | Translation shown | UI hint |
|------------|-------------------|---------|
| 1.4 | Full unit of `S-1.4-6` | “Covers 1.4–1.6” |
| 1.5 | Same full unit | Same |
| 1.6 | Same full unit | Same |

Sanskrit on each Verse card remains the single Verse’s Sanskrit (Scripture), independent of Translation span.

---

## Example 3 — N:1 Segment (21–22)

**Publisher label:** `I. 21-22.`  
**Coverage:** `{1.21, 1.22}`  

Arjuna’s request spanning two ślokas is one English speech unit in this edition.

```text
Segment S-1.21-22
  coverage: [1.21, 1.22]
  publisherLabel: "I. 21-22."
```

---

## Example 4 — N:1 Segment (24–25)

**Publisher label:** `I. 24—25.`  
**Coverage:** `{1.24, 1.25}`  
**Notes:** Sanjaya narrative unit; speaker labels stay with the Segment’s prose as printed.

---

## Example 5 — N:1 Segment (32–34)

**Publisher label:** `I. 32—34.`  
**Coverage:** `{1.32, 1.33, 1.34}`  

Sanskrit block still marks `॥३२॥` `॥३३॥` `॥३४॥` separately; English is combined. Scripture identities remain three Verses; Translation is one Segment.

---

## Example 6 — N:1 Segment (38–39)

**Publisher label:** `I. 38. 39.`  
**Coverage:** `{1.38, 1.39}`  

---

## Example 7 — Chapter 1 inventory pattern

Conceptual inventory (not a package):

| Kind | Verses | Action under this policy |
|------|--------|--------------------------|
| 1:1 | e.g. 1.1, 1.2, 1.7, 1.40, 1.47, … | Future Segment per Verse |
| N:1 | 4–6, 21–22, 24–25, 32–34, 38–39 | Future one Segment each |
| Running header `45-47]` | — | Ignore (not a Segment) |

Until segment-aware packaging exists, N:1 Verses stay unpublished rather than forced into package v1.

---

## Example 8 — Wrong evidence

**Not a Segment trigger:** page header `8-10]` while body shows `I. 8.`, `I. 9.`, `I. 10.` as separate units.

**Correct:** three 1:1 Segments (if each has its own fluent English), not one N:1 Segment.

---

## Example 9 — Cross-edition generalization (sketch)

| Edition | Typical pattern | Policy application |
|---------|-----------------|--------------------|
| Swarupananda | Mix of 1:1 and N:1 labels | As above |
| Besant & Das | Mostly 1:1 free translation lines | Almost all 1:1 Segments; N:1 only if edition groups |
| Telang (SBE) | Continuous prose, weak inline numbers | Segments defined only with explicit editorial mapping evidence; may require larger N:1 units or defer |
| Arnold | Poetic chapters without verse numbers | Usually **not** Verse-mappable without invention → poor Verse Translation candidate (Phase 1); if ever used, only with external scholarly alignment evidence — never Option A invention |

---

## Example 10 — Reader composition (Verse 1.5)

```text
Scripture card: Sanskrit for 1.5 only
Translation card: Segment S-1.4-6 full English
Attribution: Swarupananda 1909
Note: Translation covers Verses 1.4–1.6
```

No client-side splitting of the English string.
