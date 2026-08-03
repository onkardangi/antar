# CONTINUE READING

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Continue Reading preserves the reader's momentum by presenting the single most meaningful next step in their journey through the Bhagavad Gita.

It reduces decision-making by offering one clear action instead of multiple competing choices.

The component should always help the reader continue their journey with confidence.

---

# Responsibility

Continue Reading is responsible for:

* presenting the next meaningful reading action,
* providing enough context for the reader to understand where they will go,
* encouraging continuity without pressure,
* initiating navigation when selected.

---

# Non-Responsibilities

Continue Reading is not responsible for:

* determining what the next destination should be,
* recommending verses,
* calculating reading progress,
* persisting reading history,
* managing navigation state,
* displaying multiple competing actions.

Those responsibilities belong to navigation, recommendation, and reading services.

---

# Usage

Continue Reading appears whenever Antar can confidently suggest a single meaningful next step.

Typical locations include:

* Home
* Chapter
* Verse
* Journey
* Guidance (recommended verse)

If there is no meaningful next step, the component should not appear.

---

# Experience Principles

## One Action

The component always presents one primary action.

It should never become a list of recommendations or competing navigation choices.

---

## Preserve Momentum

Readers should feel that they are naturally continuing their journey rather than starting a new task.

---

## Confidence Before Curiosity

The destination should be understandable before the reader selects it.

Readers should never wonder where they are about to go.

---

## Invitation, Never Pressure

The component should gently invite continuation.

It should never use urgency, streaks, countdowns, or persuasive language.

---

# Variants

## Resume Reading

Used when the reader has unfinished progress.

Example:

Continue Reading

Chapter 3 • Verse 18

---

## Next Verse

Used after completing a verse.

Example:

Continue Reading

Chapter 2 • Verse 48

---

## Continue Chapter

Used when entering from a Chapter experience.

Example:

Continue Reading

Verse 12

---

## Recommended Teaching

Used after Guidance identifies a relevant teaching.

Example:

Continue Reading

Chapter 6 • Verse 5

---

## Return to Reading

Used after Journey encourages readers to continue their study.

Example:

Continue Reading

Resume where you left off

---

# Anatomy

The component consists of:

1. Primary Action Label
2. Optional Context
3. Optional Direction Indicator

```text
────────────────────────────

Continue Reading

Chapter 2 • Verse 48

>

────────────────────────────
```

The context is optional but recommended whenever it reduces uncertainty.

---

# States

## Default

The next destination is available.

---

## Pressed

Provide immediate visual feedback.

---

## Loading

Displayed only while determining the next destination.

Loading should be brief and should preserve the component's layout.

---

## Disabled

Rare.

Prefer hiding the component instead of presenting an unavailable primary action.

---

# Interaction Behavior

Selecting Continue Reading should immediately navigate to the predetermined destination.

The component should not display confirmation dialogs or additional decision points.

If the destination is unavailable, the experience—not the component—should explain why.

---

# Content Guidelines

The primary label is always:

**Continue Reading**

Supporting context should:

* identify the destination,
* reduce ambiguity,
* remain concise.

Good examples:

* Chapter 2 • Verse 48
* Resume where you left off
* Begin Chapter 5

Avoid:

* motivational phrases,
* promotional language,
* multiple destinations,
* vague labels such as "Keep Going."

---

# Accessibility

Continue Reading must:

* expose a descriptive accessibility label,
* announce the destination,
* remain fully keyboard accessible,
* support Dynamic Type,
* provide sufficient touch target size.

Example accessibility label:

> Continue Reading. Opens Chapter 2, Verse 48.

---

# Motion

Motion should reinforce continuity rather than attract attention.

Appropriate motion includes:

* subtle press feedback,
* smooth navigation transitions.

Avoid:

* pulsing,
* bouncing,
* celebratory animations,
* delayed navigation.

Motion must respect the Motion Foundation and Reduced Motion preferences.

---

# Design Token Dependencies

Continue Reading uses:

* Color System
* Typography System
* Spacing System
* Motion System
* Accessibility System

The component should not introduce custom visual tokens.

---

# Engineering Boundaries

Continue Reading may receive:

* destination title,
* destination reference,
* destination type,
* loading state,
* enabled state,
* accessibility label.

Continue Reading must not:

* calculate the next destination,
* query reading history,
* fetch content,
* determine recommendation logic,
* own navigation routing.

It renders and invokes an already-determined action.

---

# Good Examples

✓ Resume an unfinished chapter.

✓ Open the next verse after completing the current one.

✓ Continue from a Journey memory back into scripture.

✓ Open a verse recommended by Guidance.

---

# Anti-Patterns

Avoid:

✗ Presenting multiple "continue" options.

✗ Showing unrelated recommendations.

✗ Using urgency or persuasive copy.

✗ Displaying progress statistics within the component.

✗ Turning Continue Reading into a recommendation carousel.

---

# Confirmed Decisions

* One primary action only.
* Continue Reading never determines its own destination.
* Context is optional but encouraged.
* Navigation occurs immediately after selection.
* The component remains visually secondary to scripture.

---

# Design Hypotheses

The following require prototype validation:

* Does supporting context improve confidence without increasing visual weight?
* Is a directional indicator necessary or does the label provide enough clarity?
* Should the destination always include chapter and verse, or only when ambiguity exists?

---

# Validation Questions

* Do readers immediately understand where they will go?
* Does the component reduce decision fatigue?
* Does it preserve momentum across every experience?
* Does it feel encouraging without becoming persuasive?
* Can the same component support all five variants without losing clarity?

---

# North Star

Continue Reading succeeds when readers instinctively continue their journey without pausing to decide what to do next. It should quietly remove friction while keeping the Bhagavad Gita—not the navigation—the center of attention.
