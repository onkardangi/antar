# VERSE ITEM

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Verse Item represents a single verse as a navigable row within discovery experiences.

Its purpose is to help readers identify, locate, and open a verse without presenting the scripture itself.

Verse Item is a navigation component.

It is not a reading component.

---

# Responsibility

Verse Item is responsible for:

* identifying a verse,
* presenting minimal contextual information,
* communicating reading progress when available,
* providing a clear entry into the Verse experience.

---

# Non-Responsibilities

Verse Item is not responsible for:

* displaying scripture,
* rendering translations,
* presenting Saar,
* summarizing teachings,
* recommending verses,
* or interpreting meaning.

Those responsibilities belong to Scripture components and the Verse experience.

---

# Usage

Verse Item appears in:

* Verse List
* Search Results
* Continue Reading
* Journey references
* Guidance recommendations
* Future study experiences

Each Verse Item always represents one canonical verse.

---

# Experience Principles

## Recognition Before Detail

Readers should immediately understand:

* which verse this is,
* whether they have visited it,
* and that selecting it opens the complete Verse experience.

---

## Keep Discovery Lightweight

Verse Item should provide enough context to navigate confidently without replacing the reading experience.

---

## Canonical Identity

Verse identity should always come from the Verse Reference component.

Verse Item never invents or reformats canonical references.

---

## Calm Navigation

Verse Item should feel like browsing a table of contents rather than consuming content.

---

# Anatomy

Verse Item is composed of:

1. Verse Reference
2. Optional Reading Progress
3. Optional Current Verse Indicator
4. Navigation Affordance

Example

```text
Verse 47

━━━━━━━━━━━ 60%

>
```

Verse Item intentionally does **not** contain scripture or translation.

---

# Component Composition

Verse Item composes:

* Verse Reference

Optional supporting elements:

* Reading Progress Indicator
* Navigation Affordance

Verse Item does not own the behavior or presentation of Verse Reference.

---

# Variants

## Standard

Used within Verse Lists.

---

## Continue Reading

Highlights the current reading position.

---

## Search Result

Displays the same Verse Item while allowing matched terms to be highlighted by the parent Search experience.

---

## Recommendation

Used by Guidance or Journey to reference a verse without presenting the teaching itself.

---

# States

## Default

No reading history.

---

## In Progress

Reader has previously opened the verse.

---

## Completed

Quietly indicates completion.

Completion should never resemble an achievement.

---

## Disabled

Verse cannot currently be opened.

Used only when required by the parent experience.

---

# Interaction Behavior

Selecting a Verse Item opens the Verse experience.

Verse Item owns no routing logic.

The parent experience determines navigation.

---

# Accessibility

Verse Item must:

* support Dynamic Type,
* expose one accessible element,
* announce verse identity clearly,
* indicate progress when available,
* identify itself as interactive.

Example announcement:

> Chapter 2, Verse 47. In progress. Opens verse.

---

# Motion

Use only standard list interaction behavior.

Avoid:

* animated progress,
* animated numbering,
* decorative transitions,
* hover effects that compete for attention.

---

# Design Token Dependencies

Verse Item uses:

* Typography System
* Color System
* Spacing System
* Accessibility System

No unique visual tokens.

---

# Engineering Boundaries

Verse Item receives:

* verse identifier,
* Verse Reference,
* reading progress,
* completion state,
* availability.

It must not:

* load scripture,
* calculate progress,
* perform search,
* determine recommendations,
* or manage navigation.

---

# Good Examples

✓ Clear verse identity.

✓ Quiet progress indication.

✓ One tap opens the Verse experience.

✓ Consistent spacing across every list.

---

# Anti-Patterns

Avoid:

✗ Scripture previews.

✗ Translation snippets.

✗ Saar previews.

✗ AI summaries.

✗ Social indicators.

✗ Popular verses.

✗ Achievement badges.

---

# Confirmed Decisions

* Verse Item is reusable.
* Verse Reference owns canonical identity.
* Verse Item owns navigation.
* Scripture never appears inside Verse Item.
* Progress remains secondary.

---

# Design Hypotheses

* Is progress valuable in every context?
* Should recommendation contexts suppress progress?
* Does Verse Item provide enough information without previews?

---

# Validation Questions

* Can readers immediately identify the verse?
* Does the component encourage navigation rather than reading?
* Is Verse Reference sufficient as the primary identifier?
* Does the component remain reusable across Library, Journey, Guidance, and Search?

---

# North Star

Verse Item succeeds when readers can confidently navigate to any verse from anywhere in Antar while the interface remains quieter than the scripture it leads to.
