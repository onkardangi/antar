# ILLUSTRATION SYSTEM

**Version:** 1.0
**Status:** Approved for Design Exploration
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

This document defines the philosophy and use of illustrations throughout Antar.

Illustrations exist to make the product feel more human and approachable.

They should reduce emotional friction, provide warmth, and support understanding without distracting from the teachings.

Illustrations are part of the atmosphere—not the content.

---

# Why This Exists

Reading wisdom can sometimes feel intimidating.

An empty journal can feel overwhelming.

A first launch can feel unfamiliar.

Illustrations soften these moments.

They welcome users without demanding attention.

Unlike typography or layout, illustrations are not essential to using Antar.

Their role is to quietly improve the emotional experience.

---

# Illustration Philosophy

Illustrations should create emotional atmosphere rather than visual excitement.

They should never become the center of attention.

The closer users move toward scripture and reflection, the less illustration should appear.

Illustrations support the journey into wisdom.

They never become part of the teaching itself.

---

# Core Principles

## 1. Illustrations Reduce Emotional Friction

Illustrations should make experiences feel welcoming rather than intimidating.

They are especially valuable during:

* onboarding,
* empty states,
* waiting states,
* first-time experiences,
* and gentle celebrations.

---

## 2. Support, Never Interpret

Illustrations must never explain or interpret the Bhagavad Gita.

The teachings belong to the reader.

Visuals should not suggest how a verse should be imagined or understood.

Meaning should emerge through reading and reflection—not artwork.

---

## 3. Less as Users Go Deeper

Illustrations become progressively less visible throughout the reading journey.

Typical progression:

Home

↓

Library

↓

Chapter

↓

Verse

↓

Reflection

↓

Saar

By the time users reach Saar, illustrations should have disappeared completely.

---

## 4. Nature Before People

Nature communicates warmth without imposing identity.

Illustrations should favor:

* light,
* trees,
* paper,
* water,
* leaves,
* stone,
* mountains,
* sky,
* seasons,
* quiet interiors.

Human figures should be used sparingly, if at all.

This keeps Antar welcoming across cultures and backgrounds.

---

## 5. Editorial Rather Than Decorative

Illustrations should feel like part of a thoughtfully designed book.

They should never resemble marketing artwork or decorative wallpaper.

Large empty areas are encouraged.

Negative space is part of the composition.

---

## 6. Timeless Before Trendy

Illustrations should remain appropriate many years from now.

Avoid styles that depend on current illustration trends.

The visual language should age gracefully.

---

## 7. Quiet Before Clever

Illustrations should support the experience without trying to surprise users.

Subtlety creates trust.

Restraint creates longevity.

---

# Where Illustrations Belong

Illustrations are appropriate in:

* onboarding,
* welcome screens,
* empty states,
* success states,
* offline experiences,
* educational introductions,
* seasonal experiences,
* and selected guidance experiences.

Illustrations should generally not appear within:

* scripture,
* translations,
* Saar,
* journal writing,
* long-form commentary,
* or extended reading sessions.

---

# Visual Language

Illustrations should feel:

* warm,
* calm,
* spacious,
* organic,
* timeless,
* and understated.

Composition should prioritize simplicity over detail.

Illustrations should never visually dominate surrounding content.

---

# Color

Illustrations inherit Antar's color philosophy.

They should use:

* restrained palettes,
* soft neutrals,
* muted accents,
* and gentle contrast.

Bright, saturated colors should remain rare.

Illustrations should feel integrated with the interface rather than sitting above it.

---

# Motion

Illustrations may include subtle movement when it strengthens atmosphere.

Examples:

* soft light,
* slow cloud movement,
* gentle leaves,
* shifting shadows.

Avoid:

* looping attention-grabbing animations,
* bouncing,
* spinning,
* decorative transitions.

Motion should remain nearly invisible.

---

# Seasonal Adaptation

Future versions of Antar may allow illustrations to reflect the passage of time.

Examples include:

* changing seasons,
* morning and evening light,
* subtle environmental variation.

These adaptations should reinforce presence rather than novelty.

Seasonal changes should never alter functionality or distract from reading.

---

# Accessibility

Illustrations must never communicate essential information by themselves.

Every experience should remain fully understandable without artwork.

Users should always be able to complete their goals regardless of whether illustrations are visible.

---

# Illustration Rules

## Rule 1

Illustrations support emotion, not instruction.

---

## Rule 2

Never illustrate scripture.

---

## Rule 3

Use illustrations sparingly.

---

## Rule 4

Prefer nature over people.

---

## Rule 5

Illustrations should become less prominent as contemplation increases.

---

## Rule 6

Color should remain restrained.

---

## Rule 7

Motion should remain subtle.

---

## Rule 8

Illustrations should never compete with typography.

---

## Rule 9

Every illustration must justify its existence.

---

## Rule 10

Removing an illustration should never reduce understanding.

---

# Good Examples

✓ A softly lit bookshelf welcoming a first-time reader.

✓ Morning light falling across an open notebook in the Journal empty state.

✓ Gentle leaves accompanying a successful reading milestone.

✓ A quiet landscape introducing Journey without becoming the focus.

✓ A subtle seasonal change on the Home screen that reflects time passing.

---

# Anti-Patterns

Avoid:

✗ Illustrations of Krishna or Arjuna accompanying verses.

✗ Religious symbols used as decorative backgrounds.

✗ Cartoon characters.

✗ Meditation mascots.

✗ Decorative mandalas behind scripture.

✗ Highly detailed fantasy artwork.

✗ Loud gradients.

✗ Emoji-style illustrations.

✗ Illustrations that prescribe a particular interpretation of a teaching.

✗ Artwork that competes with the reading experience.

---

# Confirmed Principles

The following decisions are foundational:

* Illustrations reduce emotional friction.
* Illustrations never interpret scripture.
* Nature is preferred over human figures.
* Illustrations become less prominent as reading deepens.
* Editorial simplicity is preferred over decorative richness.
* Motion remains minimal.
* Every illustration must earn its place.

---

# Design Hypotheses

The following require validation:

* Exact illustration style.
* Line weight.
* Texture treatment.
* Seasonal adaptations.
* Integration with motion.
* Empty-state illustration density.
* Illustration behavior in dark appearance.

---

# Decision Framework

Before introducing an illustration, ask:

1. Does this make the experience feel more welcoming?

2. Would removing it reduce emotional comfort?

3. Does it compete with the teaching?

4. Does it suggest an interpretation?

5. Is it timeless?

6. Is it accessible?

7. Is it visually quieter than the surrounding typography?

If the answer to any question is uncertain, reconsider the illustration.

---

# Design Implications

This illustration system means:

* Home may use subtle atmospheric artwork.
* Library may use illustrations for empty states.
* Journal may use illustrations to reduce writing anxiety.
* Verse should remain almost entirely illustration-free.
* Saar should never include decorative artwork.
* Reading experiences prioritize typography over imagery.
* Future seasonal updates should enhance atmosphere without changing interaction.

---

# Engineering Implications

Implementation should:

* load illustrations efficiently,
* support light and Evening appearances,
* allow future seasonal assets,
* maintain accessibility,
* avoid blocking interactions,
* and ensure illustrations remain optional decorative assets rather than functional requirements.

Illustration rendering should remain independent from content logic.

---

# Relationship to Other Documents

This document defines illustration philosophy.

Related documents define:

* `01_DESIGN_DNA.md`
* `02_COLOR_SYSTEM.md`
* `05_TYPOGRAPHY.md`
* `06_MOTION_SYSTEM.md`
* Experience specifications for screen-level illustration usage.

---

# North Star

Illustrations should make Antar feel more welcoming without becoming memorable themselves.

If users leave remembering the wisdom they encountered rather than the artwork they saw, the illustration system has succeeded.
