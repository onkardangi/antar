# CHAPTER ITEM

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Chapter Item represents a single chapter of the Bhagavad Gita within discovery experiences.

Its purpose is to help readers understand what a chapter is about and confidently choose where to begin reading.

Chapter Item is a navigation component, not a reading component.

---

# Responsibility

Chapter Item is responsible for:

* identifying a chapter,
* presenting enough context for informed navigation,
* communicating reading progress when available,
* providing a clear entry into the Chapter experience.

---

# Non-Responsibilities

Chapter Item is not responsible for:

* displaying verses,
* summarizing every teaching,
* rendering scripture,
* searching,
* recommending chapters,
* or managing reading progress.

Those responsibilities belong to the Library experience or supporting services.

---

# Usage

Chapter Item appears in:

* Library
* Search results
* Continue Reading recommendations
* Future collections

Each Chapter Item always represents one canonical chapter.

---

# Experience Principles

## Chapters Are Destinations

A Chapter Item should encourage intentional reading rather than endless browsing.

---

## Recognition Before Detail

Readers should immediately recognize:

* chapter number,
* chapter title,
* overall theme.

Additional metadata should remain secondary.

---

## Calm Discovery

The component should feel like browsing a bookshelf rather than scrolling a social feed.

No popularity indicators.

No trending labels.

No recommendations competing for attention.

---

## Respect Canonical Order

Default ordering follows the Bhagavad Gita.

Personalization should never replace the canonical sequence.

---

# Anatomy

A Chapter Item contains:

1. Chapter Number
2. Chapter Name
3. Brief Intent
4. Optional Reading Progress
5. Navigation Affordance

Example

```text
Chapter 2

Sankhya Yoga

Duty, action, and wisdom.

━━━━━━━━━━━━━━ 45%

>
```

---

# Variants

## Standard

The default presentation used in Library.

---

## Continue Reading

Displays existing progress.

---

## Search Result

Highlights matching search terms while preserving the standard hierarchy.

---

# States

## Default

No progress.

---

## In Progress

Displays reading progress.

---

## Completed

Communicates completion quietly.

Completion should never become a badge or achievement.

---

## Disabled

Used only if content is temporarily unavailable.

---

# Interaction Behavior

Selecting a Chapter Item opens the Chapter experience.

The component owns no routing logic.

The parent experience determines the destination.

---

# Accessibility

Must support:

* Dynamic Type,
* screen readers,
* keyboard navigation,
* large touch targets,
* meaningful accessibility labels.

Preferred announcement:

> Chapter 2. Sankhya Yoga. In progress. Opens chapter.

---

# Motion

Use standard list interaction feedback only.

Avoid:

* animated progress,
* hover effects that dominate,
* decorative transitions.

---

# Engineering Boundaries

Receives:

* chapter identifier,
* title,
* subtitle,
* progress,
* availability.

Does not:

* load verses,
* calculate progress,
* own navigation.

---

# Good Examples

✓ Clear chapter hierarchy.

✓ Quiet progress indicator.

✓ Consistent spacing.

✓ Canonical ordering.

---

# Anti-Patterns

Avoid:

✗ Trending.

✗ Recommended.

✗ Most Popular.

✗ Achievement badges.

✗ Completion celebrations.

✗ Verse previews inside the component.

---

# Confirmed Decisions

* One Chapter Item represents one canonical chapter.
* Progress remains secondary.
* Navigation is its primary responsibility.
* Canonical ordering takes precedence.

---

# Design Hypotheses

* Is the chapter intent sufficient without verse previews?
* Does quiet progress encourage return visits?
* Should completed chapters remain visually identical apart from progress?

---

# Validation Questions

* Can a first-time reader confidently choose a chapter?
* Does progress help without distracting?
* Does the component encourage intentional reading?

---

# North Star

Chapter Item succeeds when readers immediately understand where a chapter fits within the Bhagavad Gita and feel confident beginning their reading journey without the interface competing for their attention.
