# Final Editorial Evidence — Chapter 1 Residual Decisions

**Status:** Evidence only — **no JSONL edits**, **no status changes**, **no approval**, **no package/import**.

**Verses:** 1.21, 1.22, 1.23, 1.44

**Images:** Local crops (not committed). Open the linked files beside this document.


====================================================

Verse:
1.21

Printed page:
10

Scan leaf:
56

Source page image
-----------------
![Verse 1.21 fluent English crop](/tmp/besant-final-evidence/verse_1.21_fluent.jpg)

Local path: `/tmp/besant-final-evidence/verse_1.21_fluent.jpg`

Note: 1.21 fluent unit is entirely on printed page 10 / leaf 56 (no second page).

Printed fluent translation
--------------------------
```
And spake this word to Hṛishîkesha, O Lord of earth:
Arjuna said :
“ In the midst, between the two armies, stay my chariot, O Achyuta,
```

Current extracted text
----------------------
```
And spake this word to Hrishîkesha, O Lord of earth:
Arjuna said :
"In the midst, between the two armies, stay my chariot, O Achyuta,
```

Character-level diff
--------------------
- **Unicode diacritic:** `Hrishîkesha` → `Hṛishîkesha`
- **quotation:** opening mark: ASCII `"` → curly `“`
- **spacing:** after opening quote: no space → one space (`“ In`)

Evidence
--------
✓ opening curly quotation mark present before In
✓ one space visible between opening quotation mark and In
✓ no closing quotation mark visible after Achyuta,
✓ circumflex present on î in Hṛishîkesha
✓ underdot present beneath r in Hṛishîkesha
✓ space before colon in Arjuna said :
✓ colon present after earth
✓ commas present after midst, armies, chariot, Achyuta
✓ no italics visible in this fluent block

Recommendation
--------------
CHANGE_TO_MATCH_PAGE

Justification (visible only): Page shows underdot on Hṛishîkesha and opening curly quote with following space; extract differs.

====================================================

Verse:
1.22

Printed page:
10

Scan leaf:
56

Source page image
-----------------
![Verse 1.22 fluent English crop](/tmp/besant-final-evidence/verse_1.22_fluent.jpg)

Local path: `/tmp/besant-final-evidence/verse_1.22_fluent.jpg`

Note: 1.22 fluent unit is entirely on printed page 10 / leaf 56.

Printed fluent translation
--------------------------
```
That I may behold these standing, longing for battle, with whom I must strive in this out-breaking war ;
```

Current extracted text
----------------------
```
That I may behold these standing, longing for battle, with whom I must strive in this out-breaking war ;
```

Character-level diff
--------------------
IDENTICAL (no character differences).

Evidence
--------
✓ no opening quotation mark visible
✓ no closing quotation mark visible
✓ space before semicolon: war ;
✓ hyphen present in out-breaking
✓ commas present after standing and battle
✓ no italics visible
✓ no Unicode diacritics visible in this fluent block

Recommendation
--------------
KEEP_AS_IS

Justification (visible only): Printed fluent characters match the stored translationText.

====================================================

Verse:
1.23

Printed page:
11

Scan leaf:
57

Source page image
-----------------
![Verse 1.23 fluent English crop](/tmp/besant-final-evidence/verse_1.23_fluent.jpg)

Local path: `/tmp/besant-final-evidence/verse_1.23_fluent.jpg`

Printed fluent translation
--------------------------
```
And gaze on those here gathered together, ready to fight, desirous of pleasing in battle the evil-minded son of Dhṛitarâshṭra.
```

Current extracted text
----------------------
```
And gaze on those here gathered together, ready to fight, desirous of pleasing in battle the evil-minded son of Dhritarâshtra.
```

Character-level diff
--------------------
- **Unicode diacritic:** `Dhritarâshtra` → `Dhṛitarâshṭra`

Evidence
--------
✓ no opening quotation mark visible
✓ no closing quotation mark visible
✓ period present after Dhṛitarâshṭra
✓ underdot present beneath r (ṛ)
✓ circumflex present on â
✓ underdot present beneath t (ṭ)
✓ hyphen present in evil-minded
✓ no italics visible

Recommendation
--------------
CHANGE_TO_MATCH_PAGE

Justification (visible only): Page shows underdots in Dhṛitarâshṭra; extract omits them. No quotation marks on page.

====================================================

Verse:
1.44

Printed page:
20

Scan leaf:
66

Source page image
-----------------
![Verse 1.44 fluent English crop](/tmp/besant-final-evidence/verse_1.44_fluent.jpg)

Local path: `/tmp/besant-final-evidence/verse_1.44_fluent.jpg`

Printed fluent translation
--------------------------
```
The abode of the men whose family customs are extinguished, . O Janârdana, is everlastingly in hell. Thus have we heard.
```

Italics: Janârdana is **not** italicized on the page (roman).


Current extracted text
----------------------
```
The abode of the men whose family customs are extinguished, O Janârdana, is everlastingly in hell. Thus have we heard.
```

Character-level diff
--------------------
- **punctuation:** after `extinguished,`: extract has space+`O`; page shows comma, space, period-sized mark, space, then `O`

Evidence
--------
✓ no italics visible on Janârdana (roman type)
✓ circumflex present on â in Janârdana
✓ comma present after extinguished
✓ period-sized ink mark visible between that comma and O
✓ comma present after Janârdana
✓ period present after hell
✓ period present after heard
✓ no quotation marks visible

Recommendation
--------------
CHANGE_TO_MATCH_PAGE

Justification (visible only): Page shows a period-sized mark between extinguished, and O; extract omits it. Janârdana is roman (not italic) on page.

====================================================

## Summary

| Verse | Recommendation | Reason |
|-------|----------------|--------|
| 1.21 | CHANGE_TO_MATCH_PAGE | Page shows underdot on Hṛishîkesha and opening curly quote with following space; extract differs. |
| 1.22 | KEEP_AS_IS | Printed fluent characters match the stored translationText. |
| 1.23 | CHANGE_TO_MATCH_PAGE | Page shows underdots in Dhṛitarâshṭra; extract omits them. No quotation marks on page. |
| 1.44 | CHANGE_TO_MATCH_PAGE | Page shows a period-sized mark between extinguished, and O; extract omits it. Janârdana is roman (not italic) on page. |
