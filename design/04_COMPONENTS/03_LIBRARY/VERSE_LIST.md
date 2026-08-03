# VERSE LIST

**Version:** 1.1
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Verse List organizes the verses of a single chapter into their canonical sequence.

Its purpose is to help readers navigate through a chapter while preserving the structure of the Bhagavad Gita.

Verse List is an organizational component.

It is not a reading component.

---

# Responsibility

Verse List is responsible for:

* presenting an ordered collection of Verse Items,
* preserving canonical verse order,
* organizing navigation within a chapter,
* maintaining consistent spacing and hierarchy between Verse Items.

---

# Non-Responsibilities

Verse List is not responsible for:

* displaying scripture,
* rendering translations,
* presenting Saar,
* identifying verses,
* communicating verse progress,
* searching,
* recommending verses,
* or determining reading order.

Those responsibilities belong to Verse Item, Verse Reference, Scripture components, and the parent Chapter experience.

---

# Usage

Verse List appears in:

* Chapter
* Search navigation
* Future study experiences

A Verse List always represents the verses belonging to one canonical chapter.

---

# Experience Principles

## Preserve Canonical Order

Verses are always presented in ascending canonical order.

The list must never reorder verses based on:

* popularity,
* recommendations,
* bookmarks,
* recent activity,
* reading history.

Canonical order is immutable.

---

## Organization Before Presentation

Verse List organizes content.

Individual Verse Items determine how each verse is presented.

This separation keeps navigation reusable and consistent throughout Antar.

---

## Calm Navigation

Verse List should feel like browsing a table of contents.

It should never resemble an infinite content feed.

---

## Predictable Structure

Every chapter should use the same organizational pattern.

Readers should immediately understand how to navigate regardless of chapter length.

---

# Anatomy

Verse List contains one or more Verse Items.

```text
Verse Item

Verse Item

Verse Item

Verse Item

Verse Item
```

Verse Item is the reusable navigation component.

Verse List is responsible only for organizing Verse Items into canonical chapter order.

---

# Component Composition

Verse List composes:

* Verse Item

Verse List owns:

* ordering,
* grouping,
* spacing,
* scrolling behavior.

Verse Item owns:

* verse identity,
* progress indication,
* interaction,
* navigation affordances.

---

# Variants

## Standard

Displays every Verse Item within a chapter.

---

## Continue Reading

Automatically scrolls to the reader's current Verse Item while preserving canonical order.

---

## Search Navigation

Displays only Verse Items matching the current search while preserving their canonical order.

---

# States

## Default

All Verse Items are available.

---

## Empty

If no verses are available, the parent experience should present an unavailable-content state.

Verse List should not invent placeholder verses.

---

## Loading

When verse metadata is loading, the parent experience may display a structural loading state.

Verse List itself owns no loading behavior beyond preserving layout continuity.

---

# Interaction Behavior

Verse List itself has no direct interaction.

Interaction belongs entirely to individual Verse Items.

Scrolling follows standard platform conventions.

The parent experience determines navigation behavior.

---

# Accessibility

Verse List must:

* preserve canonical reading order,
* expose Verse Items in the correct sequence,
* support Dynamic Type,
* support keyboard navigation,
* maintain logical accessibility grouping.

Each Verse Item remains an independent accessible element.

---

# Motion

Verse List should use only standard scrolling behavior.

Avoid:

* animated sorting,
* animated reordering,
* decorative transitions,
* movement that changes canonical order.

---

# Design Token Dependencies

Verse List uses semantic tokens from:

* Spacing System
* Layout System
* Accessibility System

Typography and interaction belong primarily to Verse Item.

---

# Engineering Boundaries

Verse List receives:

* chapter identifier,
* ordered Verse Item collection.

It must not:

* calculate progress,
* identify verses,
* fetch scripture,
* perform search,
* determine recommendations,
* manage navigation.

Those responsibilities belong to child components and parent experiences.

---

# Good Examples

✓ Canonical ordering.

✓ Consistent spacing between Verse Items.

✓ Predictable navigation.

✓ One reusable Verse Item per row.

✓ Simple organizational responsibility.

---

# Anti-Patterns

Avoid:

✗ Scripture previews.

✗ Translation snippets.

✗ Progress calculations.

✗ AI summaries.

✗ Recommendation logic.

✗ Reordering verses.

✗ Social engagement indicators.

✗ Duplicate presentation logic already owned by Verse Item.

---

# Confirmed Decisions

* Verse List is an organizational component.
* Verse Item is the reusable navigation component.
* Canonical order is immutable.
* Verse List owns only organization and layout.
* Verse Item owns identity and interaction.

---

# Design Hypotheses

The following require validation:

* Whether automatic scrolling to the current Verse Item improves orientation.
* Whether extremely long chapters require section navigation in future versions.
* Whether Verse List should support future filtering without violating canonical order.

---

# Validation Questions

* Can readers quickly understand the chapter structure?
* Does Verse List remain visually simple?
* Are responsibilities clearly separated from Verse Item?
* Does the component remain reusable across every Chapter experience?

---

# North Star

Verse List succeeds when readers effortlessly navigate a chapter through a calm, predictable organization of Verse Items while the structure of the Bhagavad Gita remains more prominent than the interface itself.
