# SEARCH EMPTY STATE

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Search Empty State guides readers when a search returns no matching results.

Its purpose is to help readers recover naturally without making the search feel like a failure.

Search Empty State should reduce uncertainty while encouraging refinement rather than abandonment.

---

# Responsibility

Search Empty State is responsible for:

* communicating that no results were found,
* preserving the reader's search query,
* encouraging query refinement,
* providing calm recovery guidance.

---

# Non-Responsibilities

Search Empty State is not responsible for:

* modifying the search query,
* suggesting AI guidance,
* recommending unrelated teachings,
* automatically expanding the search,
* or navigating elsewhere.

Those responsibilities belong to Search services and the parent Search experience.

---

# Usage

Search Empty State appears only after a completed search returns no results.

It should never appear while a search is still loading.

---

# Experience Principles

## No Results Is Not Failure

Readers should feel encouraged to try another search.

The interface should never imply that they searched incorrectly.

---

## Preserve Intent

The original search query should remain visible.

Readers should not have to type it again.

---

## Gentle Recovery

Offer simple, actionable guidance.

Examples:

* Try a different word.
* Search by chapter or verse.
* Search a broader topic.

Avoid overwhelming readers with numerous suggestions.

---

## Stay Within Search

Search Empty State should help readers continue searching.

It should not redirect them into Guidance or unrelated experiences.

---

# Anatomy

Search Empty State contains:

1. Title
2. Supporting Message
3. Optional Search Tips

Example

```text
No results found

Try searching by chapter, verse, or a broader topic.
```

---

# Variants

## Standard

Used throughout Library search.

---

## Scoped

Adjusts guidance to match the current search scope.

Example:

Searching reflections may suggest:

> Try another keyword from your reflection.

---

# States

## Empty

No matching results.

This is the primary state.

---

## Offline

If search is limited because content is unavailable offline, the parent experience may provide an additional contextual message.

---

# Interaction Behavior

Search Empty State owns no direct interaction.

Readers continue interacting through Search Input.

---

# Accessibility

Search Empty State must:

* announce that no results were found,
* preserve focus on Search Input,
* support Dynamic Type,
* remain readable with screen readers.

The component should never unexpectedly move focus away from the search field.

---

# Motion

No component-specific motion.

Search Empty State should appear naturally when the search completes.

Avoid dramatic transitions or animations that emphasize failure.

---

# Design Token Dependencies

Uses:

* Typography System
* Color System
* Spacing System
* Accessibility System

---

# Engineering Boundaries

Search Empty State receives:

* search query,
* search scope,
* optional contextual guidance.

It must not:

* execute another search,
* modify the query,
* generate recommendations,
* or navigate.

---

# Good Examples

✓ "No results found."

✓ "Try searching by chapter or verse."

✓ Original query remains visible.

✓ Search Input stays focused.

---

# Anti-Patterns

Avoid:

✗ "Nothing exists."

✗ "Search failed."

✗ Automatically clearing the query.

✗ Redirecting readers to AI Guidance.

✗ Displaying unrelated recommendations.

✗ Treating empty search as an error.

---

# Confirmed Decisions

* Empty search is a valid outcome.
* Queries remain visible.
* Recovery guidance is concise.
* Search and Guidance remain separate.

---

# Design Hypotheses

* Do search tips improve recovery?
* Is one recovery suggestion sufficient?
* Should scoped searches have custom empty messages?

---

# Validation Questions

* Do readers understand that no content matched?
* Can readers recover without frustration?
* Does the component encourage refinement rather than abandonment?

---

# North Star

Search Empty State succeeds when readers naturally refine their search without feeling that they have reached a dead end.
