# JOURNEY MEMORY

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Journey Memory reconnects readers with a previous moment in their personal journey through the Bhagavad Gita.

Its purpose is to surface past reflections and reading history in a way that encourages continued growth without judging progress or measuring achievement.

Journey Memory is an adapter component.

It adapts previously created reflection content into the Journey experience.

---

# Responsibility

Journey Memory is responsible for:

* representing a previous reflection,
* preserving its historical context,
* helping readers revisit earlier thoughts,
* providing navigation back into the original teaching.

---

# Non-Responsibilities

Journey Memory is not responsible for:

* evaluating growth,
* comparing reflections,
* generating summaries,
* editing reflections,
* creating new journal entries,
* recommending teachings,
* or measuring spiritual progress.

Those responsibilities belong to surrounding experiences and services.

---

# Usage

Journey Memory appears in:

* Journey
* Future reflection timelines
* Memory collections

It always represents a real historical interaction.

Journey Memory must never fabricate history.

---

# Experience Principles

## Memory Before Metrics

Journey exists to remember—not to measure.

Readers should reconnect with their own words rather than numbers or achievements.

---

## Preserve Original Context

A reflection should remain connected to:

* its verse,
* its chapter,
* and when it was written.

Context gives memory meaning.

---

## Reflection Belongs to the Reader

Journey Memory presents reflections exactly as they were originally written.

The component must never rewrite, summarize, or reinterpret the reader's words.

---

## Encourage Gentle Revisit

Journey should invite readers to revisit earlier moments without suggesting they were right, wrong, or incomplete.

---

# Component Composition

Journey Memory composes:

* Verse Item
* Reflection Preview

Optional supporting elements:

* Date
* Continue Reading

Journey Memory owns only contextual presentation.

---

# Anatomy

Journey Memory contains:

1. Verse Item
2. Reflection Preview
3. Date
4. Optional Continue Reading

Example

```text id="v6m9e2"
Chapter 2 • Verse 47

"At the time I felt completely overwhelmed..."

March 18, 2026

Continue Reading →
```

The reflection preview should remain visually primary.

---

# Variants

## Standard

Displays one historical reflection.

---

## Compact

Used within timelines or collections.

Shows a shorter reflection preview.

---

## Archived

Represents older memories while preserving readability.

No visual treatment should imply reduced importance.

---

# States

## Available

Reflection exists.

---

## Missing Reflection

If the original reflection has been deleted, the parent Journey experience determines whether the memory is omitted or represented differently.

Journey Memory should not invent placeholder content.

---

## Verse Unavailable

If scripture cannot be opened, the historical reflection may remain visible while navigation is disabled.

---

# Interaction Behavior

Selecting the Verse Item opens the associated Verse experience.

Selecting Continue Reading resumes reading from that teaching.

Journey Memory owns no routing logic.

The parent Journey experience controls navigation.

---

# Reflection Preview

The preview should:

* preserve the reader's wording,
* remain concise,
* avoid truncating meaning,
* never rewrite or summarize.

If truncation is necessary, it should occur visually rather than by rewriting content.

---

# Accessibility

Journey Memory must:

* expose Verse Item normally,
* expose reflection preview as semantic text,
* support Dynamic Type,
* preserve chronological reading order,
* support keyboard navigation.

Example announcement:

> Memory from March 18, 2026. Chapter 2, Verse 47. Reflection available. Opens verse.

---

# Motion

Journey Memory should use subtle list interaction only.

Avoid:

* timeline animations,
* celebration effects,
* animated memories,
* decorative transitions.

The memory should feel calm and timeless.

---

# Design Token Dependencies

Journey Memory uses:

* Typography System
* Color System
* Spacing System
* Accessibility System

Verse identity remains owned by Verse Item.

---

# Engineering Boundaries

Journey Memory receives:

* reflection identifier,
* Verse Item,
* reflection preview,
* creation date,
* navigation metadata.

It must not:

* edit reflections,
* generate summaries,
* compare reflections,
* calculate progress,
* or recommend teachings.

---

# Privacy Boundaries

Journey Memory displays only reflections the reader intentionally created.

It should never expose deleted, hidden, or private content unexpectedly.

Future sharing features must remain outside this component.

---

# Good Examples

✓ Original wording preserved.

✓ Verse remains linked.

✓ Reflection preview remains concise.

✓ Date provides historical context.

✓ Journey feels personal rather than analytical.

---

# Anti-Patterns

Avoid:

✗ Reflection scores.

✗ Growth percentages.

✗ AI summaries.

✗ Before-and-after comparisons.

✗ Streak indicators.

✗ "You have improved."

✗ Ranking memories.

✗ Highlighting "best" reflections.

---

# Confirmed Decisions

* Journey Memory is an adapter component.
* Original reflections remain unchanged.
* Context is preserved.
* Growth is implied through memory rather than measurement.
* Journey avoids gamification.

---

# Design Hypotheses

The following require validation:

* Whether chronological ordering is always preferred.
* Whether reflection previews should have a fixed length.
* Whether dates alone provide enough context.
* Whether multiple memories from the same verse require grouping.

---

# Validation Questions

* Does Journey feel reflective rather than analytical?
* Do readers recognize their own writing immediately?
* Does the component encourage revisiting scripture?
* Does the experience avoid measuring spiritual growth?

---

# North Star

Journey Memory succeeds when readers encounter an earlier version of themselves with honesty, context, and compassion, allowing the Bhagavad Gita to reveal growth through memory rather than measurement.
