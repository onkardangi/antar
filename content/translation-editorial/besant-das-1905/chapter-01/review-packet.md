# Editorial Review Packet — Besant & Das 1905 Chapter 1 (flagged verses only)

**Status:** Review support only — **no approval**, **no JSONL edits**, **no package**.

**Authority:** Page images of `bhagavadgitawith00londiala`.

**Scope:** Verses with non-empty `reviewFlags` in `segment-draft.jsonl`.

**Method:** Source excerpts re-read from page images; OCR used only as a locator. No normalization applied in Diff.


**Total flagged verses:** 30

## Index by review-flag category

- **quotation** (4): 1.11, 1.21, 1.22, 1.23
- **diacritic** (8): 1.5, 1.8, 1.16, 1.17, 1.24, 1.30, 1.35, 1.41
- **speaker** (6): 1.1, 1.2, 1.21, 1.24, 1.28, 1.47
- **cross-page** (6): 1.20, 1.21, 1.27, 1.33, 1.34, 1.43
- **footnote-marker** (15): 1.2, 1.4, 1.5, 1.6, 1.8, 1.10, 1.14, 1.15, 1.16, 1.17, 1.24, 1.27, 1.31, 1.36, 1.40
- **label-quirk** (3): 1.1, 1.28, 1.33
- **italics** (1): 1.44

## Estimated review time

**~2 h 04 m** (~2 min × 12 provisional ACCEPT + ~5 min × 18 NEEDS_EDIT + ~10 min orientation), with page images open beside this packet.


## Recommendation summary (not approval)

- Provisional `ACCEPT`: **12**
- `NEEDS_EDIT`: **18**

`publicationStatus` remains `UNREVIEWED`. Footnote-marker-only deltas follow `decisions.md` D2 (markers omitted on purpose).


## Group: quotation

Verses with this flag: **4**

--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.11 |
| Printed page | 5 |
| Scan leaf | 51 |

**Review flags:**
- quotation (`QUOTATION_MARK_UNCERTAIN`)

**Source excerpt**
----------------
```
Therefore in the rank and file let all, standing firmly in their respective divisions, guard Bhîshma, even all ye Generals.”
```

**Current extracted text**
----------------------
```
Therefore in the rank and file let all, standing firmly in their respective divisions, guard Bhîshma, even all ye Generals.
```

**Diff**
----
- quotation: closing ” present on page; absent in extract
- other: length residual source_norm=124 extract=123

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Quotation marks/spacing on the page differ from the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.21 |
| Printed page | 10 |
| Scan leaf | 56 |

**Review flags:**
- speaker (`SPEAKER_ATTRIBUTION`)
- cross-page (`CROSS_PAGE_CONTINUATION`)
- quotation (`OPEN_QUOTATION_CONTINUES`)

**Source excerpt**
----------------
```
And spake this word to Hṛishîkesha, O Lord of earth:
Arjuna said :
“ In the midst, between the two armies, stay my chariot, O Achyuta,
```

**Current extracted text**
----------------------
```
And spake this word to Hrishîkesha, O Lord of earth:
Arjuna said :
"In the midst, between the two armies, stay my chariot, O Achyuta,
```

**Diff**
----
- diacritic: `Hṛishîkesha` → `Hrishîkesha`
- quotation: opening curly “ on page; extract uses different quote form or spacing
- spacing: page has space after opening quote (`“ In`); extract has `"In`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Quotation marks/spacing on the page differ from the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.22 |
| Printed page | 10 |
| Scan leaf | 56 |

**Review flags:**
- quotation (`OPEN_QUOTATION_CONTINUES`)

**Source excerpt**
----------------
```
That I may behold these standing, longing for battle, with whom I must strive in this out-breaking war ;
```

**Current extracted text**
----------------------
```
That I may behold these standing, longing for battle, with whom I must strive in this out-breaking war ;
```

**Diff**
----
IDENTICAL

**Reviewer recommendation:** `ACCEPT`

**Reason:** Source excerpt and extract match character-for-character.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.23 |
| Printed page | 11 |
| Scan leaf | 57 |

**Review flags:**
- quotation (`QUOTATION_MARK_UNCERTAIN`)

**Source excerpt**
----------------
```
And gaze on those here gathered together, ready to fight, desirous of pleasing in battle the evil-minded son of Dhṛitarâshṭra.
```

**Current extracted text**
----------------------
```
And gaze on those here gathered together, ready to fight, desirous of pleasing in battle the evil-minded son of Dhritarâshtra.
```

**Diff**
----
- diacritic: `Dhṛitarâshṭra` → `Dhritarâshtra`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------



## Group: diacritic

Verses with this flag: **8**

--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.5 |
| Printed page | 3 |
| Scan leaf | 49 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
Dhṛishṭaketu, Chekitâna, and the valiant Râjâ of Kâshî; Purujit and Kuntibhoja, and Shaibya, bull ¹ among men ;
```

**Current extracted text**
----------------------
```
Dhrishtaketu, Chekitâna, and the valiant Râjâ of Kâshî ; Purujit and Kuntibhoja, and Shaibya, bull among men ;
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…and Shaibya, bull ¹…`)
- diacritic: `Dhṛishṭaketu` → `Dhrishtaketu`
- other: residual difference near index 54: normalized-source `…â of Kâshî; Purujit …` vs extract `…â of Kâshî ; Purujit…`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.8 |
| Printed page | 4 |
| Scan leaf | 50 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
Thou, lord and Bhîshma, and Karṇa, and Kṛipa, conquering in battle ; Ashvatthâmâ, Vikarṇa, and Saumadatti ¹ also ;
```

**Current extracted text**
----------------------
```
Thou, lord and Bhîshma, and Karna, and Kripa, conquering in battle ; Ashvatthâmâ, Vikarna, and Saumadatti also ;
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…a, and Saumadatti ¹…`)
- diacritic: `Karṇa` → `Karna`
- diacritic: `Kṛipa` → `Kripa`
- diacritic: `Vikarṇa` → `Vikarna`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.16 |
| Printed page | 8 |
| Scan leaf | 54 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
The Râjâ Yudhishṭhira, the son of Kuntî, blew Anantavijaya ; Nakula and Sahadeva, Sughosha and Maṇipushpaka.¹
```

**Current extracted text**
----------------------
```
The Râjâ Yudhishthira, the son of Kuntî, blew Anantavijaya ; Nakula and Sahadeva, Sughosha and Manipushpaka.
```

**Diff**
----
- footnote-marker: omitted `¹` (near `… and Maṇipushpaka.¹…`)
- diacritic: `Yudhishṭhira` → `Yudhishthira`
- diacritic: `Maṇipushpaka` → `Manipushpaka`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.17 |
| Printed page | 8 |
| Scan leaf | 54 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
And Kâshya,² of the great bow, and Shikhanḍî, the mighty car-warrior, Dhṛishṭadyumna and Virâṭa and Sâtyaki, the unconquered.
```

**Current extracted text**
----------------------
```
And Kâshya, of the great bow, and Shikhandî, the mighty car-warrior, Dhrishtadyumna and Virâta and Sâtyaki, the unconquered.
```

**Diff**
----
- footnote-marker: omitted `²` (near `…And Kâshya,²…`)
- diacritic: `Virâṭa` → `Virâta`
- diacritic: `Shikhanḍî` → `Shikhandî`
- diacritic: `Dhṛishṭadyumna` → `Dhrishtadyumna`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.24 |
| Printed page | 11 |
| Scan leaf | 57 |

**Review flags:**
- speaker (`SPEAKER_ATTRIBUTION`)
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
Sañjaya said :
Thus addressed by Guḍâkesha,¹ Hṛishîkesha, O Bhârata, having stayed that best of chariots in the midst, between the two armies,
```

**Current extracted text**
----------------------
```
Sañjaya said :
Thus addressed by Gudâkesha, Hrishîkesha, O Bhârata, having stayed that best of chariots in the midst, between the two armies,
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…ssed by Guḍâkesha,¹…`)
- diacritic: `Hṛishîkesha` → `Hrishîkesha`
- diacritic: `Guḍâkesha` → `Gudâkesha`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.30 |
| Printed page | 14 |
| Scan leaf | 60 |

**Review flags:**
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
Gândîva slips from my hand, and my skin burns all over ; I am not able to stand, and my mind is whirling,
```

**Current extracted text**
----------------------
```
Gândîva slips from my hand, and my skin burns all over ; I am not able to stand, and my mind is whirling,
```

**Diff**
----
IDENTICAL

**Reviewer recommendation:** `ACCEPT`

**Reason:** Source excerpt and extract match character-for-character.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.35 |
| Printed page | 16 |
| Scan leaf | 62 |

**Review flags:**
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
These I do not wish to kill, though myself slain, O Madhusûdana, even for the sake of the kingship of the three worlds; how then for earth?
```

**Current extracted text**
----------------------
```
These I do not wish to kill, though myself slain, O Madhusûdana, even for the sake of the kingship of the three worlds; how then for earth?
```

**Diff**
----
IDENTICAL

**Reviewer recommendation:** `ACCEPT`

**Reason:** Source excerpt and extract match character-for-character.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.41 |
| Printed page | 19 |
| Scan leaf | 65 |

**Review flags:**
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
Owing to predominance of lawlessness, O Kṛishṇa, the women of the family become corrupt; women corrupted, O Vârshṇeya, there ariseth caste-confusion;
```

**Current extracted text**
----------------------
```
Owing to predominance of lawlessness, O Krishna, the women of the family become corrupt; women corrupted, O Vârshneya, there ariseth caste-confusion;
```

**Diff**
----
- diacritic: `Kṛishṇa` → `Krishna`
- diacritic: `Vârshṇeya` → `Vârshneya`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------



## Group: speaker

Verses with this flag: **6**

--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.1 |
| Printed page | 1 |
| Scan leaf | 47 |

**Review flags:**
- label-quirk (`LABEL_QUIRK_NO_ARABIC`)
- speaker (`SPEAKER_ATTRIBUTION`)

**Source excerpt**
----------------
```
Dhṛitarâshṭra said :
On the holy plain, on the field of Kuru, gathered together, eager for battle, what did they, O Sañjaya, my people and the Pâṇḍavas?
```

**Current extracted text**
----------------------
```
Dhritarâshtra said :
On the holy plain, on the field of Kuru, gathered together, eager for battle, what did they, O Sañjaya, my people and the Pândavas?
```

**Diff**
----
- diacritic: `Dhṛitarâshṭra` → `Dhritarâshtra`
- diacritic: `Pâṇḍavas` → `Pândavas`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.2 |
| Printed page | 2 |
| Scan leaf | 48 |

**Review flags:**
- speaker (`SPEAKER_ATTRIBUTION`)
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)

**Source excerpt**
----------------
```
Sañjaya said :
Having seen arrayed the army of the Pâṇḍavas, the Râjâ Duryodhana approached his teacher,¹ and spake these words :
```

**Current extracted text**
----------------------
```
Sañjaya said :
Having seen arrayed the army of the Pândavas, the Râjâ Duryodhana approached his teacher, and spake these words :
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…ached his teacher,¹…`)
- diacritic: `Pâṇḍavas` → `Pândavas`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.21 |
| Printed page | 10 |
| Scan leaf | 56 |

**Review flags:**
- speaker (`SPEAKER_ATTRIBUTION`)
- cross-page (`CROSS_PAGE_CONTINUATION`)
- quotation (`OPEN_QUOTATION_CONTINUES`)

**Source excerpt**
----------------
```
And spake this word to Hṛishîkesha, O Lord of earth:
Arjuna said :
“ In the midst, between the two armies, stay my chariot, O Achyuta,
```

**Current extracted text**
----------------------
```
And spake this word to Hrishîkesha, O Lord of earth:
Arjuna said :
"In the midst, between the two armies, stay my chariot, O Achyuta,
```

**Diff**
----
- diacritic: `Hṛishîkesha` → `Hrishîkesha`
- quotation: opening curly “ on page; extract uses different quote form or spacing
- spacing: page has space after opening quote (`“ In`); extract has `"In`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Quotation marks/spacing on the page differ from the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.24 |
| Printed page | 11 |
| Scan leaf | 57 |

**Review flags:**
- speaker (`SPEAKER_ATTRIBUTION`)
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
Sañjaya said :
Thus addressed by Guḍâkesha,¹ Hṛishîkesha, O Bhârata, having stayed that best of chariots in the midst, between the two armies,
```

**Current extracted text**
----------------------
```
Sañjaya said :
Thus addressed by Gudâkesha, Hrishîkesha, O Bhârata, having stayed that best of chariots in the midst, between the two armies,
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…ssed by Guḍâkesha,¹…`)
- diacritic: `Hṛishîkesha` → `Hrishîkesha`
- diacritic: `Guḍâkesha` → `Gudâkesha`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.28 |
| Printed page | 13 |
| Scan leaf | 59 |

**Review flags:**
- label-quirk (`LABEL_QUIRK_NO_ARABIC`)
- speaker (`SPEAKER_ATTRIBUTION`)

**Source excerpt**
----------------
```
Deeply moved to pity, this uttered in sadness :
Arjuna said :
Seeing these, my kinsmen, O Kṛishṇa, arrayed eager to fight,
```

**Current extracted text**
----------------------
```
Deeply moved to pity, this uttered in sadness :
Arjuna said :
Seeing these, my kinsmen, O Krishna, arrayed eager to fight,
```

**Diff**
----
- diacritic: `Kṛishṇa` → `Krishna`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.47 |
| Printed page | 21 |
| Scan leaf | 67 |

**Review flags:**
- speaker (`SPEAKER_ATTRIBUTION`)

**Source excerpt**
----------------
```
Sañjaya said :
Having thus spoken on the battle-field, Arjuna sank down on the seat of the chariot, casting away his bow and arrow, his mind overborne by grief.
```

**Current extracted text**
----------------------
```
Sañjaya said :
Having thus spoken on the battle-field, Arjuna sank down on the seat of the chariot, casting away his bow and arrow, his mind overborne by grief.
```

**Diff**
----
IDENTICAL

**Reviewer recommendation:** `ACCEPT`

**Reason:** Source excerpt and extract match character-for-character.

--------------------------------------------------------



## Group: cross-page

Verses with this flag: **6**

--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.20 |
| Printed page | 9 |
| Scan leaf | 55 |

**Review flags:**
- cross-page (`CROSS_PAGE_CONTINUATION`)

**Source excerpt**
----------------
```
Then, beholding the sons of Dhritarâshṭra standing arrayed, and the flight of missiles about to begin, he whose crest is an ape, the son of Pâṇḍu, took up his bow,
```

**Current extracted text**
----------------------
```
Then, beholding the sons of Dhritarâshtra standing arrayed, and the flight of missiles about to begin, he whose crest is an ape, the son of Pându, took up his bow,
```

**Diff**
----
- diacritic: `Pâṇḍu` → `Pându`
- other: residual difference near index 38: normalized-source `…Dhritarâshṭra standi…` vs extract `…Dhritarâshtra standi…`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.21 |
| Printed page | 10 |
| Scan leaf | 56 |

**Review flags:**
- speaker (`SPEAKER_ATTRIBUTION`)
- cross-page (`CROSS_PAGE_CONTINUATION`)
- quotation (`OPEN_QUOTATION_CONTINUES`)

**Source excerpt**
----------------
```
And spake this word to Hṛishîkesha, O Lord of earth:
Arjuna said :
“ In the midst, between the two armies, stay my chariot, O Achyuta,
```

**Current extracted text**
----------------------
```
And spake this word to Hrishîkesha, O Lord of earth:
Arjuna said :
"In the midst, between the two armies, stay my chariot, O Achyuta,
```

**Diff**
----
- diacritic: `Hṛishîkesha` → `Hrishîkesha`
- quotation: opening curly “ on page; extract uses different quote form or spacing
- spacing: page has space after opening quote (`“ In`); extract has `"In`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Quotation marks/spacing on the page differ from the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.27 |
| Printed page | 13 |
| Scan leaf | 59 |

**Review flags:**
- cross-page (`CROSS_PAGE_CONTINUATION`)
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)

**Source excerpt**
----------------
```
Fathers-in-law and friends also in both armies. Seeing all these kinsmen, thus standing arrayed, Kaunteya,¹
```

**Current extracted text**
----------------------
```
Fathers-in-law and friends also in both armies. Seeing all these kinsmen, thus standing arrayed, Kaunteya,
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…arrayed, Kaunteya,¹…`)

**Reviewer recommendation:** `ACCEPT`

**Reason:** Only intentional footnote-marker omission differs (decisions.md D2); wording matches.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.33 |
| Printed page | 15 |
| Scan leaf | 61 |

**Review flags:**
- label-quirk (`LABEL_QUIRK_NO_ARABIC`)
- cross-page (`CROSS_PAGE_CONTINUATION`)

**Source excerpt**
----------------
```
Those for whose sake we desire kingdom, enjoyments and pleasures, they stand here in battle, abandoning life and riches—
```

**Current extracted text**
----------------------
```
Those for whose sake we desire kingdom, enjoyments and pleasures, they stand here in battle, abandoning life and riches—
```

**Diff**
----
IDENTICAL

**Reviewer recommendation:** `ACCEPT`

**Reason:** Source excerpt and extract match character-for-character.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.34 |
| Printed page | 16 |
| Scan leaf | 62 |

**Review flags:**
- cross-page (`CROSS_PAGE_CONTINUATION`)

**Source excerpt**
----------------
```
Teachers, fathers, sons, as well as grandfathers, mother's brothers, fathers-in-law, grandsons, brothers-in-law, and other relatives.
```

**Current extracted text**
----------------------
```
Teachers, fathers, sons, as well as grandfathers, mother's brothers, fathers-in-law, grandsons, brothers-in-law, and other relatives.
```

**Diff**
----
IDENTICAL

**Reviewer recommendation:** `ACCEPT`

**Reason:** Source excerpt and extract match character-for-character.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.43 |
| Printed page | 20 |
| Scan leaf | 66 |

**Review flags:**
- cross-page (`CROSS_PAGE_CONTINUATION`)

**Source excerpt**
----------------
```
By these caste-confusing misdeeds of the slayers of the family, the everlasting caste customs and family customs are abolished.
```

**Current extracted text**
----------------------
```
By these caste-confusing misdeeds of the slayers of the family, the everlasting caste customs and family customs are abolished.
```

**Diff**
----
IDENTICAL

**Reviewer recommendation:** `ACCEPT`

**Reason:** Source excerpt and extract match character-for-character.

--------------------------------------------------------



## Group: footnote-marker

Verses with this flag: **15**

--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.2 |
| Printed page | 2 |
| Scan leaf | 48 |

**Review flags:**
- speaker (`SPEAKER_ATTRIBUTION`)
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)

**Source excerpt**
----------------
```
Sañjaya said :
Having seen arrayed the army of the Pâṇḍavas, the Râjâ Duryodhana approached his teacher,¹ and spake these words :
```

**Current extracted text**
----------------------
```
Sañjaya said :
Having seen arrayed the army of the Pândavas, the Râjâ Duryodhana approached his teacher, and spake these words :
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…ached his teacher,¹…`)
- diacritic: `Pâṇḍavas` → `Pândavas`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.4 |
| Printed page | 2 |
| Scan leaf | 48 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)

**Source excerpt**
----------------
```
Heroes are these, mighty bowmen, to Bhîma and Arjuna equal in battle; Yuyudhâna, Virâṭa, and Drupada of the great car :²
```

**Current extracted text**
----------------------
```
Heroes are these, mighty bowmen, to Bhîma and Arjuna equal in battle ; Yuyudhâna, Virâta, and Drupada of the great car :
```

**Diff**
----
- footnote-marker: omitted `²` (near `…of the great car :²…`)
- diacritic: `Virâṭa` → `Virâta`
- punctuation/spacing: `battle;` → `battle ;`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.5 |
| Printed page | 3 |
| Scan leaf | 49 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
Dhṛishṭaketu, Chekitâna, and the valiant Râjâ of Kâshî; Purujit and Kuntibhoja, and Shaibya, bull ¹ among men ;
```

**Current extracted text**
----------------------
```
Dhrishtaketu, Chekitâna, and the valiant Râjâ of Kâshî ; Purujit and Kuntibhoja, and Shaibya, bull among men ;
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…and Shaibya, bull ¹…`)
- diacritic: `Dhṛishṭaketu` → `Dhrishtaketu`
- other: residual difference near index 54: normalized-source `…â of Kâshî; Purujit …` vs extract `…â of Kâshî ; Purujit…`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.6 |
| Printed page | 3 |
| Scan leaf | 49 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)

**Source excerpt**
----------------
```
Yudhâmanyu the strong, and Uttamaujâ the brave; Saubhadra, and the Draupadeyas,² all of great cars.
```

**Current extracted text**
----------------------
```
Yudhâmanyu the strong, and Uttamaujâ the brave ; Saubhadra and the Draupadeyas, all of great cars.
```

**Diff**
----
- footnote-marker: omitted `²` (near `…d the Draupadeyas,²…`)
- punctuation/spacing: `Saubhadra, and` → `Saubhadra and`
- other: residual difference near index 46: normalized-source `… the brave; Saubhadr…` vs extract `… the brave ; Saubhad…`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.8 |
| Printed page | 4 |
| Scan leaf | 50 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
Thou, lord and Bhîshma, and Karṇa, and Kṛipa, conquering in battle ; Ashvatthâmâ, Vikarṇa, and Saumadatti ¹ also ;
```

**Current extracted text**
----------------------
```
Thou, lord and Bhîshma, and Karna, and Kripa, conquering in battle ; Ashvatthâmâ, Vikarna, and Saumadatti also ;
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…a, and Saumadatti ¹…`)
- diacritic: `Karṇa` → `Karna`
- diacritic: `Kṛipa` → `Kripa`
- diacritic: `Vikarṇa` → `Vikarna`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.10 |
| Printed page | 5 |
| Scan leaf | 51 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)

**Source excerpt**
----------------
```
Yet insufficient seems this army of ours, though marshalled by Bhîshma, while that army of theirs seems sufficient, though marshalled by Bhîma;¹
```

**Current extracted text**
----------------------
```
Yet insufficient seems this army of ours, though marshalled by Bhîshma, while that army of theirs seems sufficient, though marshalled by Bhîma;
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…rshalled by Bhîma;¹…`)

**Reviewer recommendation:** `ACCEPT`

**Reason:** Only intentional footnote-marker omission differs (decisions.md D2); wording matches.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.14 |
| Printed page | 7 |
| Scan leaf | 53 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)

**Source excerpt**
----------------
```
Then, stationed in their great war-chariot, yoked to white horses, Mâdhava¹ and the son of Pâṇḍu² blew their divine conches,
```

**Current extracted text**
----------------------
```
Then, stationed in their great war-chariot, yoked to white horses, Mâdhava and the son of Pându blew their divine conches,
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…te horses, Mâdhava¹…`)
- footnote-marker: omitted `²` (near `…d the son of Pâṇḍu²…`)
- diacritic: `Pâṇḍu` → `Pându`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.15 |
| Printed page | 7 |
| Scan leaf | 53 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)

**Source excerpt**
----------------
```
Pâñchajanya by Hṛishîkesha, and Devadatta by Dhananjaya.³ Vṛikodara,⁴ of terrible deeds, blew his mighty conch, Paundra ;
```

**Current extracted text**
----------------------
```
Pânchajanya by Hrishîkesha, and Devadatta by Dhananjaya. Vrikodara, of terrible deeds, blew his mighty conch, Paundra ;
```

**Diff**
----
- footnote-marker: omitted `³` (near `…tta by Dhananjaya.³…`)
- footnote-marker: omitted `⁴` (near `…njaya.³ Vṛikodara,⁴…`)
- diacritic: `Hṛishîkesha` → `Hrishîkesha`
- diacritic: `Pâñchajanya` → `Pânchajanya`
- diacritic: `Vṛikodara` → `Vrikodara`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.16 |
| Printed page | 8 |
| Scan leaf | 54 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
The Râjâ Yudhishṭhira, the son of Kuntî, blew Anantavijaya ; Nakula and Sahadeva, Sughosha and Maṇipushpaka.¹
```

**Current extracted text**
----------------------
```
The Râjâ Yudhishthira, the son of Kuntî, blew Anantavijaya ; Nakula and Sahadeva, Sughosha and Manipushpaka.
```

**Diff**
----
- footnote-marker: omitted `¹` (near `… and Maṇipushpaka.¹…`)
- diacritic: `Yudhishṭhira` → `Yudhishthira`
- diacritic: `Maṇipushpaka` → `Manipushpaka`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.17 |
| Printed page | 8 |
| Scan leaf | 54 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
And Kâshya,² of the great bow, and Shikhanḍî, the mighty car-warrior, Dhṛishṭadyumna and Virâṭa and Sâtyaki, the unconquered.
```

**Current extracted text**
----------------------
```
And Kâshya, of the great bow, and Shikhandî, the mighty car-warrior, Dhrishtadyumna and Virâta and Sâtyaki, the unconquered.
```

**Diff**
----
- footnote-marker: omitted `²` (near `…And Kâshya,²…`)
- diacritic: `Virâṭa` → `Virâta`
- diacritic: `Shikhanḍî` → `Shikhandî`
- diacritic: `Dhṛishṭadyumna` → `Dhrishtadyumna`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.24 |
| Printed page | 11 |
| Scan leaf | 57 |

**Review flags:**
- speaker (`SPEAKER_ATTRIBUTION`)
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)
- diacritic (`DIACRITIC_COMPLEXITY`)

**Source excerpt**
----------------
```
Sañjaya said :
Thus addressed by Guḍâkesha,¹ Hṛishîkesha, O Bhârata, having stayed that best of chariots in the midst, between the two armies,
```

**Current extracted text**
----------------------
```
Sañjaya said :
Thus addressed by Gudâkesha, Hrishîkesha, O Bhârata, having stayed that best of chariots in the midst, between the two armies,
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…ssed by Guḍâkesha,¹…`)
- diacritic: `Hṛishîkesha` → `Hrishîkesha`
- diacritic: `Guḍâkesha` → `Gudâkesha`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.27 |
| Printed page | 13 |
| Scan leaf | 59 |

**Review flags:**
- cross-page (`CROSS_PAGE_CONTINUATION`)
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)

**Source excerpt**
----------------
```
Fathers-in-law and friends also in both armies. Seeing all these kinsmen, thus standing arrayed, Kaunteya,¹
```

**Current extracted text**
----------------------
```
Fathers-in-law and friends also in both armies. Seeing all these kinsmen, thus standing arrayed, Kaunteya,
```

**Diff**
----
- footnote-marker: omitted `¹` (near `…arrayed, Kaunteya,¹…`)

**Reviewer recommendation:** `ACCEPT`

**Reason:** Only intentional footnote-marker omission differs (decisions.md D2); wording matches.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.31 |
| Printed page | 14 |
| Scan leaf | 60 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)

**Source excerpt**
----------------
```
And I see adverse omens, O Keshava.¹ Nor do I foresee any advantage from slaying kinsmen in battle.
```

**Current extracted text**
----------------------
```
And I see adverse omens, O Keshava. Nor do I foresee any advantage from slaying kinsmen in battle.
```

**Diff**
----
- footnote-marker: omitted `¹` (near `… omens, O Keshava.¹…`)

**Reviewer recommendation:** `ACCEPT`

**Reason:** Only intentional footnote-marker omission differs (decisions.md D2); wording matches.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.36 |
| Printed page | 16 |
| Scan leaf | 62 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)

**Source excerpt**
----------------
```
Slaying these sons of Dhṛitarâshṭra, what pleasure can be ours, O Janârdana?² killing these desperadoes sin will but take hold of us.
```

**Current extracted text**
----------------------
```
Slaying these sons of Dhritarâshtra, what pleasure can be ours, O Janârdana? killing these desperadoes sin will but take hold of us.
```

**Diff**
----
- footnote-marker: omitted `²` (near `…ours, O Janârdana?²…`)
- diacritic: `Dhṛitarâshṭra` → `Dhritarâshtra`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.40 |
| Printed page | 18 |
| Scan leaf | 64 |

**Review flags:**
- footnote-marker (`FOOTNOTE_MARKER_STRIPPED`)

**Source excerpt**
----------------
```
In the destruction of a family the immemorial family traditions¹ perish ; in the perishing of traditions lawlessness overcomes the whole family ;
```

**Current extracted text**
----------------------
```
In the destruction of a family the immemorial family traditions perish ; in the perishing of traditions lawlessness overcomes the whole family ;
```

**Diff**
----
- footnote-marker: omitted `¹` (near `… family traditions¹…`)

**Reviewer recommendation:** `ACCEPT`

**Reason:** Only intentional footnote-marker omission differs (decisions.md D2); wording matches.

--------------------------------------------------------



## Group: label-quirk

Verses with this flag: **3**

--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.1 |
| Printed page | 1 |
| Scan leaf | 47 |

**Review flags:**
- label-quirk (`LABEL_QUIRK_NO_ARABIC`)
- speaker (`SPEAKER_ATTRIBUTION`)

**Source excerpt**
----------------
```
Dhṛitarâshṭra said :
On the holy plain, on the field of Kuru, gathered together, eager for battle, what did they, O Sañjaya, my people and the Pâṇḍavas?
```

**Current extracted text**
----------------------
```
Dhritarâshtra said :
On the holy plain, on the field of Kuru, gathered together, eager for battle, what did they, O Sañjaya, my people and the Pândavas?
```

**Diff**
----
- diacritic: `Dhṛitarâshṭra` → `Dhritarâshtra`
- diacritic: `Pâṇḍavas` → `Pândavas`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.28 |
| Printed page | 13 |
| Scan leaf | 59 |

**Review flags:**
- label-quirk (`LABEL_QUIRK_NO_ARABIC`)
- speaker (`SPEAKER_ATTRIBUTION`)

**Source excerpt**
----------------
```
Deeply moved to pity, this uttered in sadness :
Arjuna said :
Seeing these, my kinsmen, O Kṛishṇa, arrayed eager to fight,
```

**Current extracted text**
----------------------
```
Deeply moved to pity, this uttered in sadness :
Arjuna said :
Seeing these, my kinsmen, O Krishna, arrayed eager to fight,
```

**Diff**
----
- diacritic: `Kṛishṇa` → `Krishna`

**Reviewer recommendation:** `NEEDS_EDIT`

**Reason:** Page-image diacritics and/or punctuation are not fully preserved in the extract.

--------------------------------------------------------


--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.33 |
| Printed page | 15 |
| Scan leaf | 61 |

**Review flags:**
- label-quirk (`LABEL_QUIRK_NO_ARABIC`)
- cross-page (`CROSS_PAGE_CONTINUATION`)

**Source excerpt**
----------------
```
Those for whose sake we desire kingdom, enjoyments and pleasures, they stand here in battle, abandoning life and riches—
```

**Current extracted text**
----------------------
```
Those for whose sake we desire kingdom, enjoyments and pleasures, they stand here in battle, abandoning life and riches—
```

**Diff**
----
IDENTICAL

**Reviewer recommendation:** `ACCEPT`

**Reason:** Source excerpt and extract match character-for-character.

--------------------------------------------------------



## Group: italics

Verses with this flag: **1**

--------------------------------------------------------

| Field | Value |
|-------|-------|
| Verse | 1.44 |
| Printed page | 20 |
| Scan leaf | 66 |

**Review flags:**
- italics (`ITALICS_PRESENTATION_DEFERRED`)

**Source excerpt**
----------------
```
The abode of the men whose family customs are extinguished, O Janârdana, is everlastingly in hell. Thus have we heard.
```

**Current extracted text**
----------------------
```
The abode of the men whose family customs are extinguished, O Janârdana, is everlastingly in hell. Thus have we heard.
```

**Diff**
----
IDENTICAL

**Reviewer recommendation:** `ACCEPT`

**Reason:** Letters match the page; italics remain presentation-only.

--------------------------------------------------------
