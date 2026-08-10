# Category B — Human editorial decisions (residual)

**Workspace:** `content/translation-editorial/besant-das-1905/chapter-01/`  
**Status:** Review only — **no approval**; **no package**; **no JSONL status change**.

## What this file contains

Only verses that **still require genuine editorial judgment** after Category A mechanical fixes are imagined applied.

Verses whose remaining flags are fully covered by already-recorded policy (`decisions.md` D2–D5) and have **no open text ambiguity** are **omitted** here.

## Omitted after mechanical fixes (no open judgment)

These still carry review flags in JSONL, but the open work is either mechanical (Category A) or settled policy sign-off:

- **Footnote markers (D2 omit):** 1.2, 1.4, 1.5, 1.6, 1.8, 1.10, 1.14, 1.15, 1.16, 1.17, 1.24, 1.27, 1.31, 1.36, 1.40
- **Speaker retention (D3 keep):** 1.1, 1.2, 1.21, 1.24, 1.28, 1.47 — pending only packaging/product presentation, not transcription ambiguity
- **Label quirks (D4):** 1.1, 1.28, 1.33
- **Cross-page soft-hyphen joins / provenance (D5):** 1.20, 1.21, 1.27, 1.33, 1.34, 1.43 — no competing fluent text once mechanical diacritics applied
- **No residual text delta:** 1.22 (text IDENTICAL), 1.30, 1.35 — flags only / IDENTICAL in packet
- **Mechanical-only after A:** 1.1, 1.2, 1.4, 1.5, 1.6, 1.8, 1.11, 1.14, 1.15, 1.16, 1.17, 1.20, 1.23 (diacritic), 1.24, 1.28, 1.36, 1.41

## Open decisions (4 verse units)

### 1.21 — Opening quote form + speech continuation

Printed page **10**, scan leaf **56**.

**After Category A:** restore `Hṛishîkesha`, page opening quote `“ In` (curly + space).

**Still open:**
- Does Arjuna’s speech remain an open quotation through 1.22–1.23 with **no** closing quote on 1.21?
- Confirm publisher unit still includes Sanjaya lead-in (“And spake…”) + `Arjuna said :` under `(21)` (structural audit / D3 / D5).

**Current extract:**
```
And spake this word to Hrishîkesha, O Lord of earth:
Arjuna said :
"In the midst, between the two armies, stay my chariot, O Achyuta,
```

**Decision needed:** Keep open-quote continuation (D6) vs close quote on a later verse — do not invent closure here without page evidence.

### 1.22 — Open quotation continues

Printed page **10**, scan leaf **56**.

**Category A:** none — packet Diff is **IDENTICAL**.

**Still open:**
- Fluent block has no quotation marks; speech began in 1.21.
- Human must decide whether 1.22 correctly remains unmarked continuation, or whether the page expects any quote punctuation not visible in the extract.

**Current extract:**
```
That I may behold these standing, longing for battle, with whom I must strive in this out-breaking war ;
```

### 1.23 — Speech closure ambiguity

Printed page **11**, scan leaf **57**.

**After Category A:** restore `Dhṛitarâshṭra` underdots.

**Still open:**
- Packet source excerpt ends with a period and **no** closing quotation mark.
- Original D6 flagged closure across 1.21–1.23 as uncertain.
- Human must decide: leave without closing `”`, or add closing `”` only if re-verified on the page image.

**Current extract:**
```
And gaze on those here gathered together, ready to fight, desirous of pleasing in battle the evil-minded son of Dhritarâshtra.
```

**Page-faithful body after mechanical diacritic only (no invented closing quote):**
```
And gaze on those here gathered together, ready to fight, desirous of pleasing in battle the evil-minded son of Dhṛitarâshṭra.
```

### 1.44 — Italics presentation

Printed page **20**, scan leaf **66**.

**Category A:** none — letter text matches the page (packet IDENTICAL).

**Still open (D7):**
- Page prints *Janârdana* in italics.
- Extract is plain `Janârdana` with `ITALICS_PRESENTATION_DEFERRED`.
- Human must choose encoding for Translation package v1 (plain text vs future markup) — do not invent a markup scheme in JSONL in this pass.

**Current extract:**
```
The abode of the men whose family customs are extinguished, O Janârdana, is everlastingly in hell. Thus have we heard.
```

## Counts

- Residual editorial verse units: **4** (1.21, 1.22, 1.23, 1.44)
- Mechanical-fix list: see `mechanical-fixes.md`
- Approvals / package / importer / `publicationStatus`: **unchanged**

