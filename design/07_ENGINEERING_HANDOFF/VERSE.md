# Verse Screen

**Status:** Approved (Milestone B reading-quality handoff)
**Version:** 1.0
**Last Updated:** 2026-08-07
**Source:** Implemented Verse Reader + iOS Simulator review
**Implementation Target:** React Native (Expo)

---

# Purpose

The Verse screen presents one canonical teaching for calm reading.

It shows Sanskrit first, optional Translation when published content is available,
and quiet in-chapter Previous / Next controls.

It does not interpret, recommend, reflect, or invoke AI.

---

# Review status

| Kind | Status |
|------|--------|
| Implemented | Yes — Milestone B structural loading, scroll geometry, Translation loading bars, a11y order |
| Simulator-reviewed | Yes — iPhone 16 Pro simulator via Expo Go (`exp://127.0.0.1:8081`), API `http://localhost:8082` |
| Physical-device-reviewed | No — not performed in this milestone |
| Deferred | Listed at end |

---

# Design Principles

- Scripture before interface.
- One continuous reading document.
- Typography and whitespace over decoration.
- Translation is optional — never implied when absent.
- Loading preserves page geometry; it does not invent scripture.

---

# Screen Hierarchy

```
ScreenHeader (inline Back + Antar)

↓

Verse Reference

↓

Sanskrit

↓

Translation (only when loading or ready)

↓

Previous / Next
```

---

# Layout

The reading document is a **single vertical `ScrollView`**.

There are:

- no cards
- no nested `ScrollView`
- no fixed content heights for scripture or Translation
- no full-screen spinner as the primary loading pattern

Horizontal padding is **28px** throughout the reading body.

Primary Sanskrit loading and success share the same `ScrollView` and the same
bottom content padding formula.

---

# Component Hierarchy

```
VerseScreen

├── ScreenHeader (layout="inline")
└── ScrollView
      ├── loading:
      │     VerseReference (route chapter/verse)
      │     VerseSanskritSkeleton (decorative)
      │     VerseNavigation (disabled)
      └── success:
            VerseReadingBody
              ├── VerseReference
              └── Sanskrit Text
            TranslationBlock (optional)
            VerseNavigation
```

`VerseBlock` was **not** extracted. `VerseReadingBody` already composes
Reference → Sanskrit without extra design-system surface area.

---

# Scrolling structure

| Concern | Implemented behavior |
|---------|----------------------|
| Ownership | One `ScrollView` (`testID="verse-scroll"`) for loading + success |
| Nested scroll | None |
| Long Sanskrit | Grows naturally; document scrolls |
| Navigation reachability | Previous / Next remain in the same scroll document after long content |
| Header | Outside scroll; not sticky |

---

# Safe-area ownership

| Edge | Owner |
|------|--------|
| Top | `ScreenHeader` once (`insets.top + headerContentTop`) |
| Bottom (reading document) | `verseSpacing.bottomPadding + insets.bottom` on scroll `contentContainerStyle` |
| Horizontal | `verseSpacing.horizontalPadding` (28) |

Callers must not wrap `ScreenHeader` in an additional full-screen `SafeAreaView`.

---

# Spacing

Horizontal padding: **28px**

| Location | Value | Status |
|----------|------:|--------|
| Header content top (below safe area) | 8 | Shared `screenHeaderSpacing` |
| Header bottom (inline row → content) | 20 | Implemented |
| Content top (header → reference) | 12 | Implemented; simulator-reviewed calm gap |
| Reference → Sanskrit | 16 | Implemented |
| Sanskrit → Translation | 40 | Implemented (when Translation section present) |
| Translation stack gap | 8 | Implemented |
| Body / Translation → navigation | 40 | Implemented |
| Nav horizontal gap | 24 | Implemented |
| Bottom padding (before safe-area inset) | 64 | Implemented |
| Skeleton line height | 12 | Implemented (matches Library/Chapter bars) |
| Sanskrit skeleton line gap | 12 | Implemented |
| Min touch target | 44 | Implemented |

Spacing values are fixed tokens in `verseSpacing`. They were not re-derived from
Figma in this milestone.

---

# Typography

| Role | Token / face | Size | Line height | Color | Status |
|------|--------------|-----:|------------:|-------|--------|
| Application title | Lora / `applicationTitle` | 18 | 24 | Primary `#1A1A18` | Shared header |
| Back | Source Sans 3 / `backNavigation` | 13 | 18 | Secondary `#8A8A84` | Shared header |
| Verse reference | Source Sans 3 / `verseCount` | 11 | 16 | Secondary `#8A8A84` | Implemented; simulator-reviewed quiet + readable |
| Sanskrit body | Platform Devanagari / `sanskritBody` | 22 | 36 | Primary `#1A1A18` | Implemented; no dedicated Devanagari face |
| Translation label | Source Sans 3 Medium / `sectionLabel` | 11 | 16 | Secondary | Ready state only |
| Translation provider | Source Sans 3 / `caption` | 13 | 18 | Tertiary `#8A8A84` | Ready state only |
| Translation body | Source Sans 3 / `versePreview` | 14 | 22 | Supporting `#4A4A46` | Ready state only |
| Previous / Next | Source Sans 3 / `caption` | 13 | 18 | Tertiary | Implemented |

Dynamic Type:

- No `adjustsFontSizeToFit`
- No fixed-height text containers
- Simulator review at `accessibility-extra-large`: Sanskrit scaled, wrapped into
  scroll, Devanagari marks not observed clipped
- **No typography / line-height token changes** in Milestone B — fixed
  `lineHeight` did not present a proven clipping or shrink-to-fit problem

---

# Colors

| Semantic Role | Value |
|--------------|-------|
| Background | `#F9F9F7` |
| Primary text | `#1A1A18` |
| Secondary text | `#8A8A84` |
| Supporting text | `#4A4A46` |
| Tertiary text | `#8A8A84` |
| Divider / skeleton bars | `#D4D4CC` |

No accent color on the Verse reading surface.
No elevation, shadows, or gradients on reading content.

(Expo Go developer chrome may appear over the simulator; it is not part of the
product UI.)

---

# Loading placeholder structure

## Primary Sanskrit loading

Same `ScrollView` geometry as success:

```
Verse Reference (from route params — real orientation)
→ 3 neutral divider bars (Sanskrit slot)
→ Previous / Next (both disabled)
```

Rules:

- one accessibility announcement: `Loading verse` (`accessibilityState.busy`)
- decorative bars: `accessibilityElementsHidden` / `importantForAccessibility="no"`
- no fake Sanskrit text
- no Translation section during primary loading (Translation is optional)

## Translation loading

Rendered only after Sanskrit success while a Translation request is active:

```
Reference
→ Sanskrit
→ 2 decorative bars (no Translation label, no prose)
→ Previous / Next (normal neighbor semantics)
```

On failure: section collapses silently.
On success: label → provider → body.

---

# Navigation

| State | Previous | Next |
|-------|----------|------|
| Sanskrit loading | Disabled | Disabled |
| First verse (neighbors ready) | Disabled | Enabled |
| Middle verse | Enabled | Enabled |
| Last verse | Enabled | Disabled |
| Neighbors unresolved / failed | Disabled | Disabled |

Targets: `minHeight` / `minWidth` **44**.

---

# Accessibility order

Success reading order:

1. Back (`Go back`)
2. One Verse reference (`Chapter N, Verse N`)
3. Sanskrit text
4. Translation label / provider / body when present
5. Previous / Next

Loading:

- exactly one loading announcement
- decorative placeholders hidden
- do not claim OS Sanskrit pronunciation accuracy
- no Sanskrit language metadata invented in this milestone

---

# Partial-content / Translation behavior

| Condition | Behavior |
|-----------|----------|
| Sanskrit success, Translation loading | Sanskrit + nav usable; decorative Translation bars only |
| Translation 404 / network / parse / 5xx | Silent collapse — no section, no error copy |
| Translation ready | Label → provider → body |
| Sanskrit missing / Verse error | Friendly Verse error + retry; Translation not fetched |

---

# Reading Progress interaction

- Records **once** after accepted Sanskrit success
- Does not wait for Translation
- Persistence failures never block Sanskrit rendering
- Stale Verse / Translation responses ignored via load-generation guard

---

# Simulator review notes (2026-08-07)

Environment:

- iPhone 16 Pro simulator (iOS 18.6)
- Expo Go + Metro on port 8081
- Backend API base URL: `http://localhost:8082`

Observed:

- Verse **1.1** (longest Chapter 1 Sanskrit in this corpus): quiet reference,
  multi-line Sanskrit, no clipping, Previous disabled appearance, Next present,
  clear bottom padding above home indicator
- Translation for Chapter 1 verses returned **404** from local API — silent
  collapse confirmed (no Translation label / unavailable copy)
- Large accessibility text (`accessibility-extra-large`): Sanskrit enlarged and
  required scrolling; no shrink-to-fit; marks remained legible in the visible
  viewport
- Primary loading skeleton was not captured visually (loads quickly); covered by
  automated tests sharing the same `ScrollView`

Not observed on simulator in this session:

- Published Translation ready UI (no local published Translation rows for
  Chapter 1)
- Physical Expo Go device

Automated tests cover Translation ready order, Translation loading bars, first /
last nav enablement, stale-response guards, and bottom padding including inset.

---

# Acceptance criteria

- Primary loading uses structural placeholders in the same scroll document
- No full-screen spinner as the primary loading pattern
- Translation is never implied during Sanskrit loading
- Long content remains in one scroll document
- Bottom padding includes safe-area inset
- Previous / Next retain ≥44pt targets
- VoiceOver order remains calm and non-repetitive for loading placeholders
- Reading Progress still records once after Sanskrit success

---

# Deferred

- Dedicated Devanagari font
- Real Translation typography tuning (book-like sustained reading)
- Transliteration
- Reflection
- Saar
- Commentary
- Continue Reading
- Home
- Provider selector
- Physical-device spacing fine-tuning
- Offline / cached scripture loading
- Milestone C Translation corpus work

---

# Implementation constraints

Do not add:

- cards, icons, gradients, shadows
- shimmer dependencies
- fake scripture or Translation prose
- user-facing font-size preference UI
- Reflection / Saar / AI / bookmarks / search chrome

---

# References

- `docs/03_EXPERIENCE_BIBLE.md`
- `design/02_EXPERIENCES/01_CORE/01_VERSE.md`
- `design/04_COMPONENTS/02_SCRIPTURE/`
- `design/07_ENGINEERING_HANDOFF/Library.md`
- `design/07_ENGINEERING_HANDOFF/CHAPTER.md`
- `mobile/src/features/verse/`
