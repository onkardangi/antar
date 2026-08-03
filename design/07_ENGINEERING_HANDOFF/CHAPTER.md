# Chapter Screen

**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-08-03
**Source:** Approved Figma Design
**Implementation Target:** React Native (Expo)

---

# Purpose

The Chapter screen prepares the Reader to enter a chapter of the Bhagavad Gita.

It presents the chapter's identity, its thematic introduction, and the complete list of verses in canonical order.

The Reader's only action is to intentionally select a verse and begin reading.

The screen exists to orient before reading—not to interpret, recommend, or summarize.

---

# Design Principles

The Chapter screen follows Antar's core design philosophy.

- Scripture before interface.
- Orientation before navigation.
- Verse before interpretation.
- Typography over decoration.
- Whitespace creates hierarchy.
- Every verse is treated equally.
- Reading is the only primary action.

---

# Screen Hierarchy

```
ScreenHeader

↓

Chapter Introduction

↓

Hairline Rule

↓

Verse List
```

---

# Layout

The screen is a single vertical column.

There are:

- no cards
- no grids
- no side panels
- no horizontal scrolling

The entire screen scrolls as one continuous document.

The header is not sticky.

Horizontal padding remains **28px** throughout the experience.

The layout respects the platform safe area rather than relying on fixed device offsets.

Sections are separated by full-width hairline rules.

---

# Component Hierarchy

```
ChapterScreen

├── ScreenHeader
├── ChapterIntroduction
├── HairlineRule
└── VerseList
      └── VerseRow
```

---

# Components

## ScreenHeader

Purpose

Provides navigation context.

Contains:

- Back navigation
- Application title

States

- Default
- Pressed (Back button)

Interactions

Back returns to the previous screen.

---

## ChapterIntroduction

Purpose

Introduces the chapter before reading begins.

Displays:

- Chapter label
- Canonical Sanskrit chapter name
- Editorial thematic introduction

States

Static.

Interactions

None.

---

## HairlineRule

Purpose

Separates major sections while preserving a document-like reading experience.

Used throughout the application.

---

## VerseRow

Purpose

Represents a single verse within the selected chapter.

The entire row is tappable.

States

- Default
- Pressed

No:

- selected state
- visited state
- disabled state

Displays:

- Verse Number
- Verse Preview

---

# Data Requirements

The Chapter screen requires:

- chapterNumber
- canonicalName
- thematicIntroduction

Each VerseRow requires:

- verseNumber
- previewText (or temporary placeholder during the Verse implementation slice)

The Chapter screen must not depend on:

- Reading Progress
- Reflection
- Journey
- Guidance
- Understanding
- Saar
- Reader Preferences

---

# Typography

| Role | Typeface | Size | Weight | Style | Color |
|------|----------|------|--------|-------|-------|
| Application title | Lora | 18px | 400 | Normal | Primary |
| Back navigation | Source Sans 3 | 13px | 400 | Normal | Tertiary |
| Section label | Source Sans 3 | 11px | 500 | Uppercase | Tertiary |
| Chapter name | Lora | 24px | 400 | Normal | Primary |
| Verse number | Lora | 13px | 400 | Italic | Tertiary |
| Verse preview | Source Sans 3 | 14px | 400 | Normal | Secondary |

---

# Spacing

Horizontal padding:

28px

| Location | Value |
|-----------|------|
| Header bottom | 28px |
| Chapter Introduction vertical | 44px |
| Verse Row vertical | 22px |
| Verse Number → Preview | 20px |
| Bottom padding | 64px |

Spacing values are fixed.

Maintain consistency rather than deriving spacing from a token scale.

---

# Colors

| Semantic Role | Value |
|--------------|-------|
| Background | #F9F9F7 |
| Primary Text | #1A1A18 |
| Secondary Text | #4A4A46 |
| Tertiary Text | #8A8A84 |
| Divider | #D4D4CC |

No accent colors.

No gradients.

No shadows.

No elevation.

---

# Accessibility

Requirements

- Minimum 44px touch target
- Logical reading order
- Dynamic text support
- VoiceOver-compatible verse labels
- Visible keyboard focus
- Decorative elements hidden from the accessibility tree

Back navigation announces:

```
Go back
```

Verse rows announce:

```
Chapter {chapterNumber},
Verse {verseNumber}
```

---

# Loading State

Not explicitly designed.

Engineering should preserve layout stability while verse content loads.

The visual language should remain consistent with the approved application loading pattern.

---

# Empty State

Not applicable.

Canonical verse content always exists.

Failure to load is treated as an error.

---

# Error State

Not explicitly designed.

The Chapter Introduction should remain visible.

Below the divider display:

```
Unable to load verses.

Please try again.
```

Any retry action should remain visually quiet and consistent with the rest of the application.

---

# Navigation

Arrives from

- Library

Navigates to

- Verse Screen

Passes:

- chapterNumber
- verseNumber

No other navigation is introduced.

---

# Implementation Constraints

Do not add:

- cards
- shadows
- gradients
- icons
- verse thumbnails
- bookmarks
- highlights
- progress indicators
- search
- sorting
- filtering
- AI summaries
- commentary
- animations beyond native press feedback

The Chapter screen exists only to orient the Reader and lead naturally into the scripture.

---

# Engineering Notes

Reusable components:

- ScreenHeader
- ChapterIntroduction
- HairlineRule
- VerseRow

These components should be shared across:

- Chapter
- Verse
- Guidance
- Understanding

---

# Acceptance Criteria

- Chapter title renders correctly.
- Editorial introduction renders correctly.
- Canonical verse ordering is preserved.
- Every verse row is a full-width tap target.
- Verse rows contain no icons.
- Hairline dividers separate every verse.
- The screen scrolls as one continuous document.
- VoiceOver announces chapter and verse correctly.
- No cards exist.
- No shadows exist.
- No personalization exists.
- Navigation enters the Verse screen with the correct chapter and verse.

---

# References

- docs/architecture/02_DOMAIN_MODEL.md
- docs/architecture/03_DATA_MODEL.md
- docs/architecture/04_API_CONTRACTS.md
- docs/architecture/09_REPOSITORY_STRUCTURE.md