# TYPOGRAPHY SYSTEM

**Version:** 1.0
**Status:** Approved for Design Exploration
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

This document defines the typography system used throughout Antar.

Typography is the primary medium through which users experience the product.

Unlike many applications where typography supports interface elements, typography is the interface.

The goal of this system is to maximize reading comfort, reduce cognitive effort, and create an intentional reading rhythm that supports understanding and reflection.

---

# Why This Exists

People come to Antar to spend meaningful time with wisdom.

That means typography is not simply a branding decision.

It is a product decision.

Good typography disappears.

Readers stop noticing fonts and begin noticing ideas.

Every typographic decision should reduce friction between the reader and the teaching.

---

# Typography Philosophy

Typography should never compete with understanding.

It should quietly guide attention, establish rhythm, communicate hierarchy, and create an environment where reading feels natural.

The best typography is not the most expressive.

It is the least distracting.

The interface should never feel designed around text.

It should feel designed for reading.

---

# Core Principles

## 1. Reading Comes Before Branding

Typography exists to improve comprehension.

Brand identity should emerge from consistency rather than decorative styling.

---

## 2. Typography Creates Pace

Typography influences how quickly people move through an experience.

Large type, generous spacing, and comfortable line lengths encourage contemplation.

Compact typography encourages scanning.

Antar intentionally adjusts reading pace depending on the experience.

---

## 3. Hierarchy Should Feel Natural

Users should immediately understand:

* what to read first,
* what supports it,
* and what comes next.

Hierarchy should emerge through typography, spacing, and placement rather than excessive color or decoration.

---

## 4. Reading Comfort Is Beautiful

The typography system should optimize for extended reading sessions.

Comfort always takes priority over novelty.

---

## 5. Respect Every Language

English, Hindi, and Sanskrit deserve equal consideration.

No language should feel like an afterthought.

Typography should respect the natural rhythm and structure of each writing system.

---

## 6. Consistency Builds Trust

Equivalent content should receive equivalent typographic treatment.

Readers should quickly develop subconscious familiarity with Antar's visual language.

---

## 7. Accessibility Is Fundamental

Typography must remain readable across:

* Dynamic Type
* Screen zoom
* Large accessibility sizes
* Screen readers
* High contrast settings

Accessibility is part of the design system.

Not an enhancement.

---

# Typography Roles

Typography is organized around meaning rather than visual appearance.

---

## Scripture

Purpose:

Present the original Bhagavad Gita verses.

Characteristics:

* Highest reading importance
* Generous breathing room
* Comfortable line height
* Clear distinction from translations
* Never decorative

---

## Translation

Purpose:

Communicate the meaning of scripture.

Characteristics:

* Long-form reading
* Book-like rhythm
* Comfortable measure
* Easy to sustain over extended sessions

---

## Understanding

Purpose:

Support learning through commentary and AI explanations.

Characteristics:

* Slightly more compact than scripture
* Clearly secondary
* Optimized for explanation rather than contemplation

---

## Reflection

Purpose:

Support personal expression.

Includes:

* Journal prompts
* Personal writing
* Saar
* Journey memories

Reflection typography should feel personal, warm, and approachable.

---

## Interface

Purpose:

Support interaction.

Includes:

* Buttons
* Labels
* Navigation
* Settings
* Metadata
* Search

Interface typography should remain quiet and functional.

---

# Reading Rhythm

Different experiences require different reading speeds.

| Experience | Reading Velocity |
| ---------- | ---------------- |
| Home       | Quick            |
| Library    | Comfortable      |
| Chapter    | Steady           |
| Verse      | Slow             |
| Journal    | User-controlled  |
| Journey    | Reflective       |

Typography should reinforce these different rhythms rather than treating every screen identically.

---

# Reading Measure

Long-form reading should avoid excessively long lines.

Reading width should prioritize comfort over filling available screen space.

Large displays should increase margins before increasing line length.

Reading measure should remain consistent enough that users quickly become comfortable.

Exact measurements will be defined within implementation tokens after validation.

---

# Line Height

Different typography roles require different vertical rhythm.

Scripture requires generous breathing room.

Translation should feel open and book-like.

Understanding may become slightly more compact.

Interface typography may prioritize efficiency while remaining comfortable.

One universal line height should not be applied across every content type.

---

# Alignment

Reading experiences should default to left alignment.

Centered alignment should be reserved for intentional moments such as:

* Saar
* Short chapter introductions
* Empty states

Long-form content should remain left aligned.

Full justification should not be used.

---

# Font Strategy

Antar intentionally separates reading typography from interface typography.

Reading experiences may use a contemplative serif family.

Interface experiences should use a highly readable sans-serif family.

Sanskrit and Hindi should use a carefully selected Devanagari typeface optimized for clarity rather than ornamentation.

Typography should feel unified even when multiple font families are used.

---

# Multilingual Support

Typography must fully support:

* English
* Hindi
* Sanskrit

The system should accommodate:

* Devanagari conjuncts
* Transliteration diacritics
* Mixed-language content
* Language-specific line heights
* Variable word lengths
* Dynamic language switching

No language should feel visually inferior.

---

# Dynamic Type

Typography should scale naturally.

Large accessibility sizes should preserve:

* reading order,
* hierarchy,
* spacing,
* interaction comfort,
* and overall rhythm.

Layouts must adapt rather than truncate content.

---

# Emphasis

Emphasis should remain restrained.

Preferred methods:

* hierarchy
* spacing
* weight
* placement

Avoid relying on:

* excessive bold text,
* bright colors,
* decorative treatments,
* or oversized typography.

The teaching should naturally command attention.

---

# Numbers and Metadata

Metadata should remain present without competing with reading content.

Examples:

* Verse numbers
* Reading progress
* Dates
* Journey timestamps

Metadata should always remain discoverable while visually secondary.

---

# Typography Rules

## Rule 1

Typography serves understanding before branding.

---

## Rule 2

Reading experiences prioritize comfort over density.

---

## Rule 3

Interface typography should remain visually quiet.

---

## Rule 4

Typography should communicate hierarchy before color.

---

## Rule 5

Reading width should remain comfortable regardless of screen size.

---

## Rule 6

Accessibility should never be compromised for visual consistency.

---

## Rule 7

Equivalent content should always receive equivalent typography.

---

## Rule 8

No language should feel secondary.

---

## Rule 9

Decorative typography should never compete with scripture.

---

## Rule 10

Typography should encourage presence rather than speed.

---

# Anti-Patterns

Avoid:

* decorative display fonts,
* excessive font families,
* justified paragraphs,
* narrow reading columns,
* oversized headlines competing with scripture,
* all-caps body text,
* inconsistent hierarchy,
* fixed-height text containers,
* truncating meaningful content,
* and treating translations as visually less important than interface elements.

---

# Confirmed Principles

The following decisions are considered foundational.

* Typography serves understanding.
* Reading comes before branding.
* Five semantic typography roles.
* Reading and interface typography remain distinct.
* Multilingual support is fundamental.
* Typography establishes reading rhythm.
* Accessibility is non-negotiable.

---

# Design Hypotheses

The following require validation during design exploration.

* Final reading typeface selection.
* Final interface typeface selection.
* Sanskrit typeface selection.
* Exact reading widths.
* Exact line heights.
* Typography scale.
* Responsive scaling behavior.
* Optional user-adjustable reading preferences.

---

# Decision Framework

Before approving typography, ask:

1. Does this improve understanding?

2. Can someone comfortably read this for thirty minutes?

3. Is the hierarchy immediately clear?

4. Does this typography reduce or increase cognitive effort?

5. Does it support every language equally?

6. Does it remain readable at accessibility sizes?

7. Is branding competing with readability?

8. Would simplifying this improve the experience?

---

# Design Implications

This typography system means:

* Verse becomes the visual center of Antar.
* Home remains welcoming rather than dense.
* Library supports efficient scanning.
* Journal feels personal rather than academic.
* Journey feels reflective rather than analytical.
* Saar receives enough typographic distinction to feel like the emotional conclusion of a reading session.
* Reading experiences prioritize rhythm over information density.

---

# Engineering Implications

Implementation should:

* expose typography through semantic design tokens,
* avoid hard-coded font sizes,
* support Dynamic Type,
* support multilingual font fallback,
* preserve semantic text styles,
* avoid fixed-height text containers,
* and allow future reading preference customization without redesigning layouts.

Typography should remain consistent across iOS and Android while respecting platform accessibility conventions.

---

# Relationship to Other Documents

This document defines typography.

Related documents define:

* `01_DESIGN_DNA.md` — overarching design principles.
* `02_COLOR_SYSTEM.md` — emotional use of color.
* `03_LAYOUT_SYSTEM.md` — structure and attention flow.
* `04_SPACING_SYSTEM.md` — rhythm and breathing room.
* `06_MOTION_SYSTEM.md` — temporal rhythm.
* Experience specifications — application of typography within individual screens.

---

# North Star

Typography should quietly disappear behind the wisdom it presents.

When users finish reading, they should remember the teaching—not the font that delivered it.
