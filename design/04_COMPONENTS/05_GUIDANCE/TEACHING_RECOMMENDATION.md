# TEACHING RECOMMENDATION

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Teaching Recommendation connects a reader's life situation with one or more relevant teachings from the Bhagavad Gita.

Its purpose is to explain *why* a particular teaching is being surfaced and provide a clear path into scripture.

Teaching Recommendation is an adapter component.

It adapts existing scripture navigation into the Guidance experience without replacing the scripture itself.

---

# Responsibility

Teaching Recommendation is responsible for:

* presenting a relevant teaching,
* explaining its relevance,
* preserving the identity of the scripture,
* providing navigation into the Verse experience,
* helping readers understand the connection between their situation and the teaching.

---

# Non-Responsibilities

Teaching Recommendation is not responsible for:

* interpreting the reader,
* giving life advice,
* replacing scripture,
* generating commentary,
* evaluating journal entries,
* conducting AI conversations,
* or deciding which teaching should be recommended.

Those responsibilities belong to Guidance services and the parent Guidance experience.

---

# Usage

Teaching Recommendation appears only after Guidance Input has been completed.

Typical locations:

* Guidance
* Future daily reflection experiences
* Guided study experiences

It should never appear independently of scripture.

---

# Experience Principles

## Scripture Is the Destination

The recommendation exists to guide readers toward scripture.

It should never become more important than the teaching itself.

---

## Explain Why

Readers should understand why this teaching was selected.

A brief explanation builds trust.

It should remain concise and factual.

---

## Humility Before Certainty

Recommendations should never claim:

* this is the only relevant teaching,
* this is the correct answer,
* or this will solve the reader's problem.

Instead, Guidance should communicate that the teaching may offer perspective.

---

## Recommendation Before Interpretation

The component introduces the teaching.

Interpretation belongs to the reader.

---

# Component Composition

Teaching Recommendation composes:

* Verse Item

Optional supporting elements:

* Recommendation Reason
* Continue Reading

Verse Item remains responsible for scripture identity.

Teaching Recommendation owns only contextual framing.

---

# Anatomy

Teaching Recommendation contains:

1. Recommendation Reason
2. Verse Item
3. Optional Continue Reading

Example

```text id="4j7qv7"
This teaching explores acting without attachment to outcomes.

────────────────────

Chapter 2 • Verse 47

────────────────────

Continue Reading →
```

The recommendation reason should remain shorter than the scripture itself.

---

# Variants

## Single Teaching

One recommended verse.

Version 1 default.

---

## Multiple Teachings

Presents several related verses.

The ordering is determined by the Guidance service.

The component should not imply ranking through visual emphasis.

Future version.

---

## Saved Recommendation

Displays a previously generated recommendation while preserving the original context.

Future version.

---

# States

## Ready

A recommendation is available.

---

## Loading

The parent experience is preparing recommendations.

Teaching Recommendation itself should not invent placeholder teachings.

---

## Unavailable

If no suitable teaching is available, the parent Guidance experience should explain this outcome.

The component should not fabricate recommendations.

---

# Interaction Behavior

Selecting the Verse Item opens the Verse experience.

Continue Reading follows the standard navigation behavior.

Teaching Recommendation owns no routing logic.

The parent Guidance experience determines navigation.

---

# Recommendation Reason

The explanation should:

* remain concise,
* avoid psychological interpretation,
* avoid certainty,
* connect naturally to the teaching.

Good examples:

> This teaching explores acting without attachment to outcomes.

> This teaching reflects on responsibility during uncertainty.

Avoid:

> You are anxious.

> This verse will fix your problem.

> AI believes this is best for you.

> This is exactly what you need.

---

# Accessibility

Teaching Recommendation must:

* expose Recommendation Reason as semantic text,
* preserve Verse Item accessibility,
* support Dynamic Type,
* support keyboard navigation,
* maintain logical reading order.

Example announcement:

> Recommended teaching. This teaching explores acting without attachment to outcomes. Chapter 2, Verse 47. Opens verse.

---

# Motion

Motion should remain minimal.

Appropriate:

* standard appearance,
* navigation transition into Verse.

Avoid:

* animated recommendations,
* rotating suggestions,
* AI typing animations,
* decorative emphasis.

---

# Design Token Dependencies

Teaching Recommendation uses:

* Typography System
* Color System
* Spacing System
* Accessibility System

Verse identity remains owned by Verse Item.

---

# Engineering Boundaries

Teaching Recommendation receives:

* recommendation identifier,
* recommendation reason,
* Verse Item,
* optional navigation metadata,
* accessibility metadata.

It must not:

* rank teachings,
* invoke AI,
* generate explanations,
* determine recommendation logic,
* store reader input,
* or own navigation.

---

# Privacy Boundaries

Teaching Recommendation should never expose the reader's private Guidance input.

Recommendation reasons should reference the teaching rather than quoting personal situations.

For example:

Good:

> This teaching explores responsibility during uncertainty.

Avoid:

> Because you said your manager criticized you...

The component should minimize exposure of sensitive personal context.

---

# Good Examples

✓ One concise explanation.

✓ One Verse Item.

✓ Clear navigation.

✓ Scripture remains visually primary.

✓ Recommendation feels humble rather than authoritative.

---

# Anti-Patterns

Avoid:

✗ AI chat responses.

✗ Long essays.

✗ Personalized life coaching.

✗ Psychological diagnosis.

✗ Ranking teachings.

✗ "Best match."

✗ "95% confidence."

✗ Recommendation cards that dominate scripture.

---

# Confirmed Decisions

* Teaching Recommendation is an adapter component.
* Scripture remains the destination.
* Verse Item is reused.
* Recommendation reasons remain concise.
* The component never claims certainty.
* Personal input is not repeated back to the reader.

---

# Design Hypotheses

The following require validation:

* Whether one recommendation is sufficient for Version 1.
* Whether recommendation reasons increase trust.
* Whether multiple teachings add value or create choice overload.
* Whether Continue Reading belongs inside or outside the component.

---

# Validation Questions

* Do readers understand why this teaching was recommended?
* Does the recommendation encourage reading rather than replacing it?
* Does the component preserve humility?
* Is scripture still the primary focus?
* Does the recommendation respect reader privacy?

---

# North Star

Teaching Recommendation succeeds when readers understand why a teaching is relevant, trust the recommendation without treating it as absolute, and naturally continue into the Bhagavad Gita itself, where the scripture—not the recommendation—becomes the center of the experience.
