# ACCESSIBILITY SYSTEM

**Version:** 1.0
**Status:** Approved for Design Exploration
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

This document defines Antar's philosophy of accessibility.

Accessibility ensures that every person has the opportunity to engage meaningfully with wisdom, regardless of ability, language, environment, device, or circumstance.

Accessibility is not a separate mode of the product.

It is part of the product itself.

---

# Why This Exists

The Bhagavad Gita has endured because its wisdom speaks across generations, cultures, and circumstances.

Antar should reflect that same inclusivity.

Every design and engineering decision should remove unnecessary barriers between the reader and the teaching.

The goal is not merely to satisfy accessibility standards.

The goal is to preserve the experience for everyone.

---

# Accessibility Philosophy

Accessibility means more than making Antar usable.

It means making Antar welcoming.

Whether someone reads with large text, a screen reader, one hand, a slow internet connection, or in a second language, they should experience the same sense of calm, presence, and reflection.

The interface may adapt.

The experience should remain constant.

---

# Core Principles

## 1. Remove Barriers

Accessibility removes obstacles rather than reducing the depth of the teachings.

The wisdom remains unchanged.

The path to it becomes more accessible.

---

## 2. Preserve the Experience

Accessibility adaptations should preserve Antar's emotional identity.

Changing interaction methods should never diminish the product's sense of calm, clarity, or presence.

---

## 3. Design Beyond Disability

Accessibility includes:

* physical ability,
* vision,
* hearing,
* cognition,
* language,
* literacy,
* emotional state,
* environment,
* connectivity,
* and technology.

Design decisions should consider all of these dimensions.

---

## 4. Reading Comes First

Reading experiences should remain comfortable under:

* Dynamic Type,
* screen zoom,
* VoiceOver,
* TalkBack,
* high contrast,
* reduced motion,
* and alternative input methods.

---

## 5. Offline Is Accessibility

Meaningful reading should not depend on network connectivity.

Users should be able to continue reading and reflecting wherever they are.

---

## 6. Language Is Accessibility

Language should never become a barrier to wisdom.

The product should support multilingual experiences with equal care and quality.

Future languages should integrate naturally into the existing design system.

---

## 7. Emotional Accessibility

The product should never create unnecessary guilt, anxiety, or pressure.

Examples:

Instead of:

"You missed today's reading."

Prefer:

"Your reading will be here whenever you're ready."

Every piece of copy should invite rather than judge.

---

# Accessibility Requirements

The product should support:

* Dynamic Type
* VoiceOver
* TalkBack
* Keyboard navigation where applicable
* High contrast
* Reduced Motion
* Large touch targets
* Screen zoom
* Offline reading
* Multilingual typography
* Flexible layouts

These capabilities should be considered foundational.

---

# Reading Preferences

Future versions of Antar should allow readers to adjust:

* text size,
* reading margins,
* line spacing,
* translation,
* transliteration,
* appearance,
* and reading comfort preferences.

Customization exists to improve understanding rather than personalization.

---

# Accessibility Rules

## Rule 1

Accessibility is part of every feature.

---

## Rule 2

Essential information should never rely on color alone.

---

## Rule 3

Reading order must remain logical for assistive technologies.

---

## Rule 4

Large text must not break the experience.

---

## Rule 5

Offline reading should remain meaningful.

---

## Rule 6

Accessibility adaptations should preserve emotional continuity.

---

## Rule 7

Copy should encourage rather than pressure.

---

## Rule 8

Every major interaction should remain possible using assistive technologies.

---

## Rule 9

Layouts must adapt before content is truncated.

---

## Rule 10

Accessibility should be validated continuously rather than added at the end.

---

# Good Examples

✓ Dynamic Type preserves reading rhythm.

✓ VoiceOver announces scripture before supporting controls.

✓ Journal remains comfortable at large text sizes.

✓ Offline reading functions without interruption.

✓ Reduced Motion preserves calm transitions.

✓ One-handed navigation remains comfortable.

✓ Reading outdoors remains possible through sufficient contrast.

---

# Anti-Patterns

Avoid:

✗ Accessibility modes that feel like separate products.

✗ Clipped text.

✗ Color-only meaning.

✗ Hidden keyboard focus.

✗ Motion that cannot be disabled.

✗ Internet-dependent reading.

✗ Judgmental notification language.

✗ Tiny touch targets.

✗ Screen-reader order that differs from visual order.

✗ Accessibility treated as a post-release task.

---

# Confirmed Principles

* Accessibility removes barriers.
* The experience should remain emotionally consistent.
* Offline reading is foundational.
* Language accessibility matters.
* Emotional accessibility matters.
* Accessibility begins on day one.

---

# Design Hypotheses

The following require validation:

* User-adjustable line spacing.
* Margin controls.
* Reading preference presets.
* Voice reading features.
* Future dyslexia-friendly typography.
* Offline synchronization behavior.

---

# Decision Framework

Before approving a feature, ask:

1. Can someone with assistive technology complete this?

2. Does large text remain readable?

3. Does this work offline where appropriate?

4. Is the language welcoming?

5. Does this preserve Antar's emotional experience?

6. Have unnecessary barriers been removed?

---

# Design Implications

This accessibility philosophy means:

* Every experience should remain usable with Dynamic Type.
* Reading order should be preserved for assistive technologies.
* Offline support should be considered from the beginning.
* Notifications should remain compassionate.
* Multilingual experiences should feel first-class.
* Motion should respect Reduced Motion settings.
* Typography, spacing, and layout should adapt gracefully as user needs change.

---

# Engineering Implications

Implementation should:

* follow semantic accessibility APIs,
* support platform accessibility settings,
* preserve focus order,
* expose accessibility labels and hints,
* avoid fixed dimensions that break with large text,
* cache essential reading content for offline use,
* and test regularly with assistive technologies.

Accessibility requirements should be part of the definition of done for every feature.

---

# Relationship to Other Documents

This document completes the Design Foundations.

It reinforces every preceding document by ensuring that Antar's philosophy, visual language, and interactions remain accessible to all readers.

---

# North Star

Every person should be able to experience Antar with the same sense of calm, dignity, and presence.

The interface may adapt.

The wisdom should remain equally accessible.
