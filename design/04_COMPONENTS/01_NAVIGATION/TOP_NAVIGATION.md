# TOP NAVIGATION

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Top Navigation preserves orientation and provides access to essential local actions without competing with the primary content.

It should help readers understand:

* where they are,
* how to return,
* and which secondary actions are available.

Top Navigation is supporting interface.

It should never become the visual focus of an experience.

---

# Responsibility

Top Navigation is responsible for:

* identifying the current location when needed,
* providing predictable backward navigation,
* presenting a limited number of local actions,
* respecting device safe areas,
* and preserving context between related experiences.

---

# Non-Responsibilities

Top Navigation is not responsible for:

* primary product navigation,
* displaying reading content,
* presenting promotional messages,
* exposing every available action,
* managing navigation history,
* displaying progress unless explicitly required by the experience,
* or becoming a persistent toolbar of unrelated controls.

Primary destination navigation belongs to Bottom Navigation or another product-level navigation system.

---

# Used By

Top Navigation may appear in:

* Library
* Chapter
* Verse
* Journal
* Journey
* Guidance
* Search
* Settings

Its exact composition depends on the experience.

Not every experience requires every element.

---

# Experience Principles

## Orientation Before Control

Top Navigation should first help readers understand where they are.

Actions are secondary.

---

## Predictability Before Novelty

Back navigation and familiar actions should behave according to established platform expectations.

Antar should not invent new navigation metaphors when existing ones are already understood.

---

## Content Remains Primary

The navigation region should carry less visual weight than the content below it.

Within Verse, scripture must remain more prominent than:

* the chapter title,
* verse number,
* bookmark action,
* overflow action,
* or back control.

---

## Minimal by Default

Only actions required in the current context should appear.

Additional actions should be placed in a secondary surface rather than permanently occupying the navigation region.

---

## Context Must Survive Navigation

Returning from Journal, Guidance, Journey, or reading preferences should preserve the reader’s previous location and reading state.

Top Navigation exposes the return action.

It does not own state restoration.

---

# Anatomy

Top Navigation may contain:

1. Leading Action
2. Context
3. Trailing Actions

```text
────────────────────────────────

[ Leading ]    [ Context ]    [ Actions ]

────────────────────────────────
```

Each region is optional depending on the experience.

---

## Leading Action

The leading position usually contains:

* Back
* Close
* Cancel, only when abandoning a temporary task

The action must clearly communicate what will happen.

Use familiar platform symbols and accessible labels.

---

## Context

Context may include:

* destination title,
* chapter title,
* verse reference,
* or a short task label.

Context should be concise.

Long titles should wrap only when doing so preserves clarity. Otherwise, the experience should use a shorter local title while presenting the full content elsewhere.

---

## Trailing Actions

Trailing actions may include:

* Bookmark
* Reading preferences
* Search
* Overflow
* Done, when completing a temporary task

The number of visible trailing actions should remain intentionally limited.

When multiple secondary actions exist, use an overflow action or contextual bottom sheet rather than crowding the navigation region.

---

# Variants

## Root Variant

Used for a primary destination where backward navigation is not required.

Typical anatomy:

```text
[ Optional Context ]          [ Optional Action ]
```

Examples:

* Library
* Journey
* Guidance

---

## Back Variant

Used when the reader enters a child experience.

Typical anatomy:

```text
[ Back ]       [ Context ]       [ Optional Action ]
```

Examples:

* Chapter
* Verse
* Search results
* Journal entered from Verse

---

## Close Variant

Used for temporary or focused experiences presented over the current context.

Typical anatomy:

```text
[ Close ]      [ Context ]       [ Optional Done ]
```

Examples:

* Reading preferences
* Translation selection
* Secondary action sheet presented as a full-screen surface

---

## Focused Reading Variant

Used within Verse or another long-form reading experience.

Typical anatomy:

```text
[ Back ]    [ Quiet Reference ]    [ Minimal Actions ]
```

This variant should carry the least visual weight.

Controls may become less prominent while scrolling, but essential navigation must remain discoverable and accessible.

Any collapsing or fading behavior requires prototype validation.

---

# States

## Default

All required navigation elements are visible and available.

---

## Pressed

Provide immediate visual feedback without exaggerated animation.

---

## Disabled

Use only when an action must remain visible but cannot currently be completed.

Prefer removing an unavailable optional action rather than presenting unnecessary disabled controls.

---

## Scrolled

Some experiences may reduce the visual prominence of Top Navigation after the reader begins scrolling.

This behavior must:

* preserve access to backward navigation,
* avoid sudden movement,
* respect Reduced Motion,
* and restore context predictably.

This remains a design hypothesis until validated.

---

## Offline

Navigation remains functional.

Actions requiring connectivity should communicate their unavailable state only when selected or when the limitation must be known beforehand.

The entire navigation region should not appear disabled merely because the device is offline.

---

# Interaction Behavior

## Back

Back returns the reader to the immediately preceding meaningful context.

It should preserve:

* scroll position where appropriate,
* selected chapter or verse,
* unsaved local writing,
* and the reader’s place in the originating experience.

Platform-standard back gestures should remain supported.

---

## Close

Close dismisses a temporary experience and restores the underlying context.

Close must not imply that saved work will be discarded.

When closing could cause data loss, the experience—not Top Navigation—must provide confirmation.

---

## Bookmark

Bookmark communicates the saved state of the current teaching.

The icon may transition between outlined and filled states.

Top Navigation displays and triggers the action.

It does not own persistence.

---

## Overflow

Overflow reveals actions that are useful but not central to the current experience.

Potential actions include:

* Share
* Copy reference
* Report content issue
* Open reading preferences

Overflow must not become a container for unrelated features.

---

# Content Guidance

Navigation labels should be:

* concise,
* familiar,
* descriptive,
* and easy to announce with assistive technology.

Prefer:

* Back
* Close
* Done
* Library
* Chapter 2
* Verse 47

Avoid:

* clever labels,
* vague actions,
* unexplained abbreviations,
* or emotionally persuasive copy.

The navigation region is functional, not conversational.

---

# Accessibility

Top Navigation must:

* appear early in the semantic reading order,
* expose clear accessibility labels,
* identify icon-only actions by purpose,
* provide sufficient touch targets,
* support Dynamic Type,
* support keyboard focus where applicable,
* preserve platform back behavior,
* and maintain sufficient contrast in all appearances.

For icon-only actions, the accessibility label should describe the action rather than the icon.

Prefer:

> Back to Chapter 2

Over:

> Left arrow

For Verse, the reading order should be:

1. Navigation and orientation
2. Verse reference
3. Scripture
4. Supporting reading content

Top Navigation must not cause assistive technology to repeatedly announce decorative or unchanged information.

---

# Motion

Motion should remain subtle and functional.

Appropriate motion includes:

* bookmark state change,
* quiet navigation transition,
* chevron or disclosure rotation,
* gradual prominence changes during scrolling.

Avoid:

* bouncing controls,
* attention-seeking pulses,
* delayed back navigation,
* or dramatic collapsing headers.

Motion behavior must follow the Motion System and respect Reduced Motion.

---

# Design Token Dependencies

Top Navigation should use semantic tokens from:

* Color System
* Typography System
* Spacing System
* Iconography System
* Motion System
* Accessibility System

Exact assignments should be finalized in Figma and the implementation token system.

The component should not introduce unique colors, type styles, spacing values, or motion curves without a documented reason.

---

# Engineering Boundaries

Top Navigation may receive:

* title or contextual label,
* leading action configuration,
* trailing actions,
* current action states,
* accessibility labels,
* safe-area information,
* optional scroll state.

Top Navigation should not:

* calculate navigation history,
* persist bookmarks,
* determine available product features,
* fetch content,
* own reading progress,
* or decide whether unsaved work may be discarded.

Those responsibilities belong to navigation, state, content, and persistence services.

---

# Good Examples

✓ Verse uses Back, a quiet verse reference, and a bookmark action.

✓ Chapter uses Back and the chapter title without unnecessary trailing actions.

✓ Journal uses Back or Close while autosave handles preservation independently.

✓ Library uses a simple title and Search action.

✓ Secondary reading actions are placed behind Overflow instead of crowding the navigation region.

---

# Anti-Patterns

Avoid:

✗ A persistent row containing Bookmark, Share, Copy, AI, Notes, Settings, and More.

✗ A large decorative title that competes with scripture.

✗ Custom back behavior that differs from platform expectations.

✗ Navigation controls that disappear completely during reading.

✗ Using the top region for promotions, streaks, notifications, or achievement messages.

✗ Placing the primary Continue Reading action inside Top Navigation.

✗ Making Top Navigation responsible for saving, routing, or business logic.

---

# Confirmed Decisions

* Top Navigation is visually secondary to content.
* Back behavior follows platform expectations.
* Visible actions remain intentionally limited.
* Additional secondary actions use Overflow or another contextual surface.
* The focused reading variant carries minimal visual weight.
* Top Navigation presents state but does not own business logic.
* Generic headers and Library-specific headers should use this shared component rather than separate abstractions.

---

# Design Hypotheses

The following require low-fidelity or Figma validation:

* Whether focused reading navigation remains fixed while scrolling.
* Whether its context fades, collapses, or remains fully visible.
* The maximum number of visible trailing actions.
* Whether Verse displays the verse reference within Top Navigation or immediately below it.
* Whether larger devices require a different context arrangement.

---

# Validation Questions

* Can readers immediately understand how to return?
* Does the component preserve orientation without competing with content?
* Are secondary actions discoverable without becoming visually dominant?
* Does the focused reading variant remain usable during long reading sessions?
* Does the component remain stable with large text and long translated titles?
* Can the same component support Library, Chapter, Verse, Journal, Journey, and Guidance without accumulating unrelated behavior?

---

# North Star

Top Navigation succeeds when readers always understand where they are and how to return, while barely noticing the interface that provides that orientation.
