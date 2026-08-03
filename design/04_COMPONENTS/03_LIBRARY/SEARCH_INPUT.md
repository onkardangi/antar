# SEARCH INPUT

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Search Input allows readers to intentionally locate chapters, verses, themes, and saved content within Antar.

Its purpose is to remove friction when the reader already has something specific in mind.

Search Input should support discovery without becoming the primary way readers understand the structure of the Bhagavad Gita.

---

# Responsibility

Search Input is responsible for:

* capturing a search query,
* communicating whether search is active,
* allowing the query to be cleared,
* supporting submission and query refinement,
* and preserving familiar platform search behavior.

---

# Non-Responsibilities

Search Input is not responsible for:

* executing search,
* interpreting query meaning,
* ranking results,
* presenting results,
* generating AI guidance,
* correcting theological terminology,
* recommending content,
* or storing search history.

Those responsibilities belong to Search services and the parent experience.

---

# Usage

Search Input may appear in:

* Library
* Search
* Journal archive
* Saved content
* Future Journey exploration

It should appear when readers have a clear reason to search.

Search should not replace canonical chapter browsing.

---

# Experience Principles

## Intentional Search

Search exists for readers who know what they want to locate or describe.

It should not encourage endless exploration or passive consumption.

---

## Familiar Before Custom

Use established platform search behavior wherever possible.

Readers should not need to learn a new search interaction for Antar.

---

## Search Is Not Guidance

Search finds content based on a query.

Guidance connects a life situation with relevant teachings.

The two experiences should remain distinct.

A query such as:

> Chapter 2, Verse 47

belongs to Search.

A situation such as:

> I am afraid of failing

belongs to Guidance.

---

## Preserve the Canonical Structure

Search results may surface content from across Antar, but Search Input should not imply that relevance replaces canonical chapter and verse organization.

---

# Anatomy

Search Input contains:

1. Search Field
2. Search Icon
3. Placeholder
4. Query Text
5. Clear Action
6. Optional Cancel Action

```text id="f6190e"
────────────────────────────

[ Search chapters, verses, or themes ]  ×

────────────────────────────
```

The clear action appears only when query text exists.

---

# Placeholder Guidance

Preferred default:

> Search chapters, verses, or themes

The placeholder should describe the searchable content clearly.

Alternative contextual placeholders may include:

* Search the Bhagavad Gita
* Search reflections
* Search saved teachings

Avoid:

* Ask anything
* What are you feeling?
* Find your answer
* Search with AI

Those phrases blur Search and Guidance.

---

# Variants

## Inline

Appears within Library or another discovery experience.

Search remains part of the surrounding page.

---

## Dedicated

Appears on a focused Search experience.

The field receives initial focus and may include a Cancel action.

---

## Scoped

Searches within a defined domain.

Examples:

* Search reflections
* Search saved teachings
* Search this chapter

The active scope must be clear to the reader.

---

# States

## Idle

No query exists.

Display the contextual placeholder.

---

## Focused

The field has input focus.

Focus treatment should be clear without becoming visually dominant.

---

## Query Entered

The field displays the reader’s text and exposes the Clear action.

---

## Searching

The query has been submitted or search results are updating.

The field remains editable.

Search should not lock the reader out while results load.

---

## No Results

Search Input preserves the entered query.

The parent experience displays Search Empty State.

---

## Offline

If local search is supported, Search continues across available downloaded content.

If search requires connectivity, the parent experience communicates the limitation without clearing the query.

---

## Error

The query remains intact.

The parent experience explains the failure and provides a retry path when appropriate.

---

# Interaction Behavior

## Focus

Selecting the field places the cursor at the expected position and opens the platform keyboard.

---

## Typing

The field should preserve standard platform editing behavior.

The product may update results while typing or after submission, depending on search architecture and validation.

The component does not determine the search strategy.

---

## Clear

Selecting Clear removes the query and returns Search to its initial state.

If focus remains in the field, the keyboard should remain available.

---

## Cancel

In the Dedicated variant, Cancel exits the focused Search experience and restores the previous context.

Cancel should not be used merely to clear text.

---

## Submission

The field should support the platform Search or Enter action.

Submitting should not dismiss the keyboard automatically unless doing so improves result visibility without harming refinement.

---

# Query Content

Search Input should accept natural text, references, and known names.

Examples:

* Chapter 2
* Verse 47
* 2.47
* karma
* courage
* Sankhya Yoga
* action without attachment

Search behavior and synonym interpretation belong to the search system, not this component.

---

# Accessibility

Search Input must:

* expose a clear search-field role,
* provide an accessible label independent of placeholder text,
* announce the Clear action,
* support Dynamic Type,
* support keyboard navigation,
* preserve focus during result updates,
* and avoid announcing every result change excessively.

Preferred accessibility label:

> Search the Bhagavad Gita.

For scoped search:

> Search journal reflections.

Placeholder text should not be the only accessible label.

---

# Keyboard Behavior

Search Input should support:

* platform Search or Enter action,
* Escape or equivalent dismissal where available,
* predictable tab order,
* external keyboards,
* text selection and editing shortcuts.

Focus should not jump unexpectedly when results update.

---

# Motion

Search Input should use only functional motion.

Appropriate examples:

* Clear action appearing when text exists,
* subtle focus transition,
* standard transition into a dedicated Search experience.

Avoid:

* animated placeholder text,
* pulsing icons,
* excessive result-loading motion,
* or transitions that delay typing.

---

# Design Token Dependencies

Search Input uses semantic tokens from:

* Typography System
* Color System
* Spacing System
* Iconography System
* Motion System
* Accessibility System

The component should not introduce custom search-specific colors or shadows without validation.

---

# Engineering Boundaries

Search Input may receive:

* query value,
* placeholder,
* search scope,
* focused state,
* searching state,
* clear callback,
* query-change callback,
* submit callback,
* cancel callback,
* accessibility metadata.

It must not:

* execute queries,
* debounce according to business rules,
* rank results,
* interpret user intent,
* generate recommendations,
* store search history,
* or route to result destinations.

The parent experience and search service own those responsibilities.

---

# Privacy Boundaries

Search queries should be treated according to Antar’s privacy principles.

Search Input should not imply that queries are:

* public,
* used for personalization,
* stored permanently,
* or interpreted as emotional disclosures.

Any search-history behavior requires a separate explicit product decision.

---

# Good Examples

✓ A reader searches `Chapter 2` and receives chapter and verse results.

✓ A reader clears the query without leaving Search.

✓ A no-results state preserves the original query for easy refinement.

✓ Library search remains secondary to canonical chapter browsing.

✓ Journal archive uses a clearly scoped placeholder.

---

# Anti-Patterns

Avoid:

✗ Using `Ask anything` as the placeholder.

✗ Routing emotional questions into AI without the reader choosing Guidance.

✗ Clearing the query after an error.

✗ Replacing canonical browsing with a search-only experience.

✗ Showing search-history suggestions without an approved privacy decision.

✗ Automatically rewriting the reader’s query without explanation.

✗ Moving focus whenever results update.

✗ Embedding search results inside the input component.

---

# Confirmed Decisions

* Search Input is separate from Search Result.
* Search and Guidance remain distinct.
* Placeholder text describes the searchable domain.
* Query text remains intact during empty and error states.
* Clear removes text but does not necessarily exit Search.
* Search Input owns input behavior, not search execution.
* Search history is not assumed in Version 1.

---

# Design Hypotheses

The following require validation:

* Whether Library search updates while typing or after submission.
* Whether the Inline variant should expand into a Dedicated Search experience.
* Whether result updates should preserve the keyboard by default.
* Whether reference formats such as `2.47` are understood by readers.
* Whether a visible search icon adds clarity or unnecessary decoration.
* Whether scoped search is required in Version 1.

---

# Validation Questions

* Can readers distinguish Search from Guidance?
* Is the searchable content clear before typing?
* Can readers refine a query without losing focus or context?
* Does Search remain useful without dominating Library?
* Is the Clear action understandable and accessible?
* Does the component behave predictably with large text and external keyboards?

---

# North Star

Search Input succeeds when readers can express exactly what they are trying to find without learning a new interaction, losing context, or mistaking search for guidance.
