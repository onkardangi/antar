# VERSE REFERENCE

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Verse Reference identifies the canonical location of a teaching within the Bhagavad Gita.

It gives readers enough context to understand where a verse belongs and provides a consistent way to return to the full teaching.

Verse Reference should remain easy to find without competing with the scripture itself.

---

# Responsibility

Verse Reference is responsible for:

* identifying the chapter and verse,
* presenting canonical reference information consistently,
* preserving orientation across experiences,
* linking back to the complete Verse experience when interactive,
* and remaining understandable outside its original context.

---

# Non-Responsibilities

Verse Reference is not responsible for:

* rendering scripture,
* displaying a translation,
* summarizing a teaching,
* explaining why a verse is relevant,
* managing navigation,
* calculating reading progress,
* storing bookmarks,
* or presenting chapter commentary.

Those responsibilities belong to Scripture components, Experiences, or supporting services.

---

# Usage

Verse Reference may appear in:

* Verse
* Journal
* Journey
* Guidance
* Search
* Saved content
* Saar Collection
* Teaching recommendations
* Reflection previews

It should be included whenever scripture is presented outside the complete Verse experience and the reader may need orientation or a path back to the original teaching.

---

# Experience Principles

## Canonical Before Conversational

Verse Reference should use the established chapter and verse structure.

It should not replace canonical information with informal labels such as:

* Today’s verse
* Your courage verse
* A teaching for anxiety

Contextual descriptions may accompany the reference, but they do not replace it.

---

## Quiet but Discoverable

The reference is supporting information.

It should remain visually secondary to scripture, translation, Saar, and personal reflection.

Secondary does not mean hidden or difficult to read.

---

## Consistent Everywhere

The same verse should be identified the same way across every experience.

A reader should not encounter different reference formats in Journal, Guidance, Journey, and Verse.

---

## Meaning Survives Context

A Verse Reference should remain understandable when:

* copied,
* announced by a screen reader,
* displayed in a saved item,
* shown within a Journey memory,
* or presented in Guidance.

It should not depend on nearby content for basic identification.

---

# Canonical Format

The preferred visible format is:

```text
Chapter 2 · Verse 47
```

This format should remain readable, localizable, and understandable to readers unfamiliar with abbreviated scripture references.

A compact format may be used when space is genuinely constrained:

```text
2.47
```

The compact format should not be the default for first-time readers or accessibility labels.

---

# Anatomy

Verse Reference may contain:

1. Chapter number
2. Verse number
3. Optional chapter name
4. Optional interaction affordance

```text
Chapter 2 · Verse 47
```

Expanded form:

```text
Chapter 2 — Sankhya Yoga
Verse 47
```

The expanded form should be used only when the chapter name improves orientation.

---

# Variants

## Standard

Used in most reading and reflective contexts.

Example:

```text
Chapter 2 · Verse 47
```

Typical uses:

* Verse
* Journal
* Journey
* Saved content

---

## Compact

Used when the surrounding context already makes the meaning clear and space is limited.

Example:

```text
2.47
```

Typical uses:

* Dense search results
* Compact metadata
* Internal cross-references

Compact references must still expose a complete accessibility label.

---

## Expanded

Used when chapter context is important.

Example:

```text
Chapter 2 — Sankhya Yoga
Verse 47
```

Typical uses:

* Chapter transitions
* First-time orientation
* Teaching recommendations
* Search results requiring additional context

---

## Interactive

Used when selecting the reference opens the complete Verse experience.

The interaction should be discoverable without making the reference resemble a primary call to action.

An Interactive Verse Reference may use:

* subtle emphasis,
* a familiar direction indicator,
* or an explicit contextual label.

It should not rely on color alone to communicate interactivity.

---

## Static

Used when the reference provides context but is not selectable.

Typical uses:

* Current Verse header
* Journal entry context
* Printed or exported reflection

Static references should not use visual affordances associated with links or buttons.

---

# States

## Default

The complete reference is available and readable.

---

## Pressed

Used only for the Interactive variant.

Provide immediate, restrained feedback.

---

## Focused

Keyboard or assistive-technology focus should be clearly visible when the reference is interactive.

---

## Unavailable Destination

If the reference is known but the full teaching cannot currently be opened, preserve the reference as static text.

Do not hide canonical information because navigation is unavailable.

---

## Incomplete Metadata

If either the chapter or verse number is missing, do not invent a reference.

The surrounding experience should present an appropriate content-unavailable state.

Avoid displaying malformed values such as:

```text
Chapter 2 · Verse —
```

---

# Interaction Behavior

Selecting an Interactive Verse Reference opens the corresponding Verse experience.

The destination is predetermined by the parent experience or content model.

Verse Reference does not determine:

* which translation opens,
* which reading position is restored,
* whether commentary is expanded,
* or whether the verse is bookmarked.

The destination experience owns those decisions.

---

# Content Guidelines

Use complete, plain language by default.

Prefer:

* Chapter 2 · Verse 47
* Chapter 6 · Verse 5
* Chapter 12 — Bhakti Yoga · Verse 13

Avoid:

* Ch. 2 V. 47
* Gita 2:47, unless required for an external citation convention
* Verse #47
* 2/47
* Today’s Verse, without the canonical reference

The exact separator may adapt by locale, but the information hierarchy should remain stable.

---

# Localization

Verse Reference must support:

* translated labels for Chapter and Verse,
* localized numeral systems where product requirements support them,
* longer chapter names,
* right-to-left interface environments in future languages,
* and accessible pronunciation of numbers and names.

Canonical identity must remain stable regardless of display language.

The underlying chapter and verse identifiers should not depend on translated display strings.

---

# Accessibility

Verse Reference must:

* expose the complete chapter and verse in its accessibility label,
* identify itself as interactive only when it is selectable,
* provide a sufficient touch target when interactive,
* support Dynamic Type,
* remain readable at high contrast,
* preserve logical reading order,
* and avoid ambiguous abbreviated announcements.

Preferred accessibility label:

> Chapter 2, Verse 47.

For an interactive reference:

> Chapter 2, Verse 47. Open verse.

When a chapter name is shown:

> Chapter 2, Sankhya Yoga, Verse 47.

Avoid labels such as:

> Two dot forty-seven.

The visible reference may be compact, but the accessibility label should remain complete.

---

# Motion

Verse Reference requires little or no motion.

Appropriate motion includes:

* subtle press feedback,
* a standard navigation transition after selection.

Avoid:

* pulsing,
* highlighting loops,
* animated numbering,
* decorative entrance effects,
* or motion intended to draw attention away from scripture.

---

# Design Token Dependencies

Verse Reference should use semantic tokens from:

* Typography System
* Color System
* Spacing System
* Accessibility System
* Iconography System, only when an interaction indicator is required

The component should not introduce unique visual tokens.

Metadata typography should remain quiet while maintaining sufficient readability and contrast.

---

# Engineering Boundaries

Verse Reference may receive:

* chapter identifier,
* verse identifier,
* localized chapter label,
* localized verse label,
* optional chapter name,
* display variant,
* interaction state,
* navigation callback,
* accessibility label override when necessary.

Verse Reference should not:

* fetch scripture,
* resolve translations,
* calculate the next verse,
* own navigation routing,
* manage bookmarks,
* infer missing identifiers,
* or format canonical identity solely from localized strings.

The chapter and verse identifiers should be structured data.

Display text should be derived from those identifiers and the active locale.

---

# Good Examples

✓ A Journal entry displays `Chapter 2 · Verse 47` above the reflection invitation.

✓ A Journey Memory uses an interactive reference to return to the original verse.

✓ Guidance displays the expanded chapter name when it helps explain where a recommended teaching belongs.

✓ A compact search result shows `2.47` visually but announces `Chapter 2, Verse 47`.

✓ The current Verse experience displays the reference quietly before the scripture.

---

# Anti-Patterns

Avoid:

✗ Replacing the canonical reference with a personalized theme label.

✗ Using different formats in Journal, Journey, and Guidance without a contextual reason.

✗ Making every reference visually resemble a primary button.

✗ Displaying incomplete or inferred verse information.

✗ Using abbreviations that first-time readers may not understand.

✗ Embedding translation, commentary, or Saar inside Verse Reference.

✗ Making the reference responsible for restoring reading state.

---

# Confirmed Decisions

* Verse Reference is separate from Verse Block.
* Chapter and verse identity use structured canonical data.
* The standard format is `Chapter N · Verse N`.
* Compact references remain available for constrained contexts.
* Accessibility labels use complete spoken language.
* Interactive references open the complete Verse experience.
* Verse Reference provides orientation but remains visually secondary.

---

# Design Hypotheses

The following require validation:

* Whether the standard separator should be a middle dot, comma, or line break.
* When chapter names improve orientation versus adding visual weight.
* Whether Interactive references require a direction indicator.
* Whether Verse should place the reference within Top Navigation or directly above Verse Block.
* Whether compact references are needed in V1.

---

# Validation Questions

* Can first-time readers immediately understand the reference format?
* Does the component remain discoverable without competing with scripture?
* Is the distinction between Interactive and Static variants clear?
* Does the reference remain understandable in Journal, Journey, Guidance, and Search?
* Does the component work with long chapter names and large text?
* Do screen readers announce compact references naturally?

---

# North Star

Verse Reference succeeds when readers always know where a teaching belongs and can return to it confidently, without the reference competing with the teaching itself.
