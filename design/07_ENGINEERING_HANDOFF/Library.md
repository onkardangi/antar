# Library Screen

**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-08-03
**Source:** Approved Figma Make Design
**Implementation Target:** React Native (Expo)

---

# Purpose

Library provides structured, unfiltered access to all eighteen chapters of the Bhagavad Gita.

It is the Reader's entry point into the scripture as a whole.

It does not personalise, recommend, prioritise, rank, filter, or interpret.

Its sole responsibility is to present the Bhagavad Gita in canonical order so the Reader can intentionally choose where to begin or continue.

---

# Design Principles

This screen follows Antar's core design philosophy.

- Scripture before interface.
- Calm over productivity.
- Typography over decoration.
- Whitespace creates hierarchy.
- Canonical order without personalization.
- No chapter is visually emphasized.
- Reading is the primary action.

---

# Screen Hierarchy

```
ScreenHeader

↓

Scripture Introduction

↓

Hairline Rule

↓

Chapter List (18 canonical chapters)
```

---

# Layout

The screen is a single vertical column.

There are:

- no cards
- no grids
- no horizontal scrolling
- no side panels
- no floating actions

All content is left aligned.

Horizontal padding is **28px** throughout the experience.

Sections are separated by full-width hairline rules.

The chapter list naturally scrolls beyond the fold.

Top-to-bottom layout:

1. Safe area inset
2. Screen Header
3. Hairline Rule
4. Scripture Introduction
5. Hairline Rule
6. Chapter List
7. Bottom padding

---

# Component Hierarchy

```
LibraryScreen

├── ScreenHeader
├── ScriptureIntroduction
├── HairlineRule
└── FlatList
      └── ChapterRow
```

---

# Components

## ScreenHeader

Purpose

Provides navigation context only.

Contains:

- Back navigation (only when the stack can go back)

Does **not** show the Antar application title on Library. After Home becomes
the landing experience, Library’s page identity is **Bhagavad Gita** via
ScriptureIntroduction — product branding steps back so scripture can lead.

States

- Default
- Pressed (Back button)

Interactions

Back returns to the previous screen (Home).

When Library is the root route, omit Back entirely. Do not reserve empty Back space.

---

## ScriptureIntroduction

Purpose

Introduces the Bhagavad Gita and explains that all chapters are available in canonical order.

This is Library’s primary visual identity (not a product wordmark).

States

Static.

Interactions

None.

---

## HairlineRule

Purpose

Separates major sections without introducing visual weight.

Used throughout the application.

Chapter list:

- One full-width hairline follows Scripture Introduction.
- `FlatList` `ItemSeparatorComponent` renders the same hairline between every ChapterRow.
- Color `#D4D4CC`, thickness `StyleSheet.hairlineWidth`.
- No trailing divider after the final chapter.

---

## ChapterRow

Purpose

Navigates to the selected Chapter.

States

- Default
- Pressed

No:

- selected state
- visited state
- disabled state

Interaction

Entire row is tappable.

No trailing arrow.

No disclosure icon.

Displays:

- Chapter Number
- Canonical Sanskrit Chapter Name
- Verse Count

---

# Data Requirements

Each ChapterRow requires exactly:

- id
- chapterNumber
- canonicalName
- verseCount

The Library screen must **not** depend on:

- Reading Progress
- Reflection
- Journey
- Guidance
- Understanding
- Saar
- User Preferences

---

# Typography

| Role | Typeface | Size | Weight | Style | Color |
|------|----------|------|--------|-------|-------|
| Application title | Lora | 18px | 400 | Normal | Primary |
| Back navigation | Source Sans 3 | 13px | 400 | Normal | Secondary |
| Scripture title | Lora | 24px | 400 | Normal | Primary |
| Introduction | Source Sans 3 | 14px | 400 | Normal | Secondary |
| Chapter number | Lora | 13px | 400 | Italic | Secondary |
| Chapter name | Lora | 15px | 400 | Normal | Primary |
| Verse count | Source Sans 3 | 11px | 400 | Normal | Secondary |

Letter spacing:

- Chapter Number → 0.06em
- Verse Count → 0.06em

---

# Spacing

Horizontal padding:

28px

| Location | Value |
|-----------|------|
| Safe area | Platform inset (not a hardcoded status-bar spacer) |
| Header content top (below safe area) | 8px |
| Header Back → title gap | 4px (only when Back is present) |
| Header bottom (title → divider) | 16px |
| Scripture Introduction vertical | 30px |
| Chapter Row vertical | 20px |
| Number → Text gap | 20px |
| Title → Verse Count | 3px |
| Bottom padding | 64px |

Spacing values are fixed.

Maintain consistency rather than deriving spacing from a token scale.

Physical-device review (2026-08-03) tightened header, introduction, and ChapterRow
spacing from the original Figma Make values while preserving calm hierarchy.

---

# Colors

| Semantic Role | Value |
|--------------|-------|
| Background | #F9F9F7 |
| Primary Text | #1A1A18 |
| Secondary Text | #8A8A84 |
| Tertiary Text | #B4B4AE (reserved; Library quiet labels use Secondary for contrast) |
| Divider | #D4D4CC |
| Chapter number | #8A8A84 (Secondary) |
| Verse count | #8A8A84 (Secondary) |

No accent color.

No elevation.

No shadows.

No gradients.

---

# Accessibility

Every ChapterRow must expose:

```
Chapter 1,
Arjuna Vishada Yoga,
47 verses
```

Back navigation:

```
Go back
```

Requirements

- minimum 44px touch target
- visible keyboard focus
- logical reading order
- dynamic text support
- VoiceOver labels
- switch control compatible

Engineering may increase tertiary text contrast if required for WCAG compliance.

---

# Loading State

Keep the Scripture Introduction visible.

Replace ChapterRows with placeholder lines.

Render 8–10 placeholder rows.

No spinner.

No animated cards.

---

# Empty State

Not applicable.

Canonical chapter data always exists.

Failure to load is treated as an error.

---

# Error State

Show:

Scripture Introduction

↓

Hairline Rule

↓

Message

```
Unable to load chapters.

Please try again.
```

A quiet text retry action may be added.

No large error illustrations.

---

# Navigation

Arrives from

- Home
- Browse Bhagavad Gita →

Navigates to

- Chapter Screen

Pass:

```
chapterNumber
```

Does not navigate directly to:

- Verse
- Reflection
- Guidance
- Saar

---

# Performance Notes

Use FlatList.

Stable key:

```
chapter.id
```

No pagination.

No virtualization tuning.

Avoid unnecessary rerenders.

---

# Implementation Constraints

Do not add:

- cards
- icons
- gradients
- shadows
- illustrations
- chapter thumbnails
- progress indicators
- Continue Reading
- Recently Opened
- personalization
- search
- sorting
- filtering
- badges
- streaks
- AI
- animations beyond native press feedback

This screen intentionally presents only the canonical scripture structure.

---

# Engineering Notes

Reusable components:

- ScreenHeader
- HairlineRule
- ScriptureIntroduction
- ChapterRow
- VerseRow (future)

These components should be shared across:

- Library
- Chapter
- Verse
- Guidance
- Understanding

---

# Acceptance Criteria

- All 18 chapters render.
- Canonical ordering is preserved.
- Chapter rows are full-width tap targets.
- Tapping a chapter opens the Chapter screen.
- VoiceOver announces chapter number, title, and verse count.
- Loading state matches specification.
- Error state matches specification.
- No cards exist.
- No icons exist.
- No personalization exists.
- No bottom navigation exists.

---

# References

- docs/architecture/02_DOMAIN_MODEL.md
- docs/architecture/03_DATA_MODEL.md
- docs/architecture/04_API_CONTRACTS.md
- docs/architecture/09_REPOSITORY_STRUCTURE.md