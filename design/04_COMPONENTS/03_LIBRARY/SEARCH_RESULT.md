# SEARCH RESULT

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Search Result represents a single search match within Antar.

Its purpose is to help readers quickly identify relevant content and navigate directly to it while preserving the identity of the underlying content type.

Search Result is an organizational and navigational component.

It is not a content component.

---

# Responsibility

Search Result is responsible for:

* presenting a matched search result,
* identifying the result type,
* highlighting relevant query matches,
* providing clear navigation to the destination,
* preserving the hierarchy of the underlying content.

---

# Non-Responsibilities

Search Result is not responsible for:

* executing search,
* ranking relevance,
* generating summaries,
* rendering scripture,
* interpreting teachings,
* recommending content,
* or managing search state.

Those responsibilities belong to Search services and the parent Search experience.

---

# Usage

Search Result appears in:

* Dedicated Search
* Library Search
* Future scoped searches

Each Search Result represents exactly one destination.

---

# Experience Principles

## Preserve Identity

A search result should still feel like the thing it represents.

Searching for a chapter should look like a Chapter.

Searching for a verse should look like a Verse.

Search should never flatten everything into identical cards.

---

## Search Organizes

Search surfaces content.

It does not reinterpret it.

The underlying component remains responsible for presentation.

---

## Highlight, Don't Distract

Matched text should be emphasized just enough to help recognition.

Highlighting should never dominate the result.

---

## Honest Search

Search should show why something matched.

Readers should never wonder why a result appeared.

---

# Result Types

Version 1 supports:

* Chapter
* Verse
* Reflection
* Saved Teaching

Future versions may include:

* Saar
* Guidance History
* Journey Memories

Each type should preserve its own identity.

---

# Component Composition

Search Result composes existing components whenever possible.

Examples:

Chapter Result

```text
Search Result
        ↓
Chapter Item
```

Verse Result

```text
Search Result
        ↓
Verse Item
```

Reflection Result

```text
Search Result
        ↓
Reflection Preview
```

Search Result owns only:

* highlighting,
* result context,
* navigation.

---

# Anatomy

Search Result contains:

1. Underlying Component
2. Match Highlight
3. Optional Match Context

Example

```text
Chapter 2

Sankhya Yoga

Matches:
"action"
```

The underlying component remains visually primary.

---

# Variants

## Chapter Result

Composes Chapter Item.

---

## Verse Result

Composes Verse Item.

---

## Reflection Result

Composes Reflection Preview.

---

## Saved Teaching

Composes the corresponding saved-content representation.

---

# States

## Default

Match available.

---

## Highlighted

Matching text is visually emphasized.

---

## Selected

Keyboard or accessibility selection.

---

## Unavailable

Destination exists but cannot currently be opened.

---

# Interaction Behavior

Selecting a Search Result opens the represented destination.

Search Result owns no routing logic.

The parent Search experience determines navigation.

---

# Highlighting

Highlighting should:

* preserve readability,
* avoid changing layout,
* support accessibility,
* remain consistent across result types.

Highlight only the matched portion.

Do not highlight entire paragraphs.

---

# Accessibility

Search Result must:

* announce the content type,
* announce the destination,
* expose highlighted content without altering meaning,
* support Dynamic Type,
* support keyboard navigation.

Example:

> Verse. Chapter 2, Verse 47. Matches "action". Opens verse.

---

# Motion

Motion should remain minimal.

Use:

* standard list interaction,
* platform navigation transitions.

Avoid:

* animated highlighting,
* resorting animations,
* decorative transitions.

---

# Design Token Dependencies

Search Result uses:

* Typography System
* Color System
* Spacing System
* Accessibility System

Underlying visual presentation belongs to the composed component.

---

# Engineering Boundaries

Search Result receives:

* result type,
* composed component,
* matched ranges,
* destination metadata,
* accessibility metadata.

It must not:

* execute search,
* calculate ranking,
* rewrite result content,
* generate previews,
* or determine navigation.

---

# Good Examples

✓ Chapter search displays a Chapter Item.

✓ Verse search displays a Verse Item.

✓ Matching text is highlighted subtly.

✓ Result type remains obvious.

---

# Anti-Patterns

Avoid:

✗ Generic cards for every result.

✗ AI-generated summaries.

✗ Large preview excerpts.

✗ Ranking labels.

✗ Popular result indicators.

✗ Decorative highlight colors.

✗ Flattening all content into one presentation style.

---

# Confirmed Decisions

* Search Result composes existing components.
* Search Result owns highlighting only.
* Every result preserves its original identity.
* Search remains a discovery tool, not a recommendation engine.
* One Search Result represents one destination.

---

# Design Hypotheses

The following require validation:

* Whether result grouping improves scanning.
* Whether contextual snippets are necessary for verse searches.
* Whether multiple highlights reduce readability.

---

# Validation Questions

* Can readers immediately recognize each result type?
* Does highlighting improve recognition without distraction?
* Does Search feel consistent with the rest of Antar?
* Are destinations obvious before selection?

---

# North Star

Search Result succeeds when readers immediately recognize what they found, why it matched, and where it will take them—without Search creating a new visual language separate from the rest of Antar.
