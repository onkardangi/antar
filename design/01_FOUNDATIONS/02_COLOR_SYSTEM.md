# COLOR SYSTEM

**Version:** 1.0

**Status:** Draft

**Owner:** Design

---

# Purpose

This document defines the philosophy behind color in Antar.

It does not define implementation values or design tokens.

Instead, it establishes why colors exist, what they communicate, and how they should be used throughout the product.

Every future color decision should reinforce these principles.

---

# Why This Exists

Color is one of the first things people feel before they consciously notice it.

In Antar, color should never compete with wisdom.

It should quietly support reading, reflection, and understanding.

The role of color is not to impress.

The role of color is to create an emotional environment where learning and reflection naturally occur.

---

# Color Philosophy

Antar uses color to create emotional atmosphere rather than visual excitement.

Color should feel calm, warm, and timeless.

Instead of drawing attention to the interface, color should help attention settle on the teachings.

The application should feel less like software and more like opening a meaningful book in the quiet hours of the morning.

---

# Design Inspiration

The color system is inspired by four materials.

## Paper

Paper represents learning, history, and contemplation.

Backgrounds should feel soft rather than perfectly white.

---

## Morning Light

Morning light represents hope, clarity, and new beginnings.

Accent colors should carry this warmth without becoming energetic.

---

## Ink

Ink represents knowledge.

Primary reading text should feel rich and comfortable rather than harsh.

Pure black should be avoided whenever possible.

---

## Earth

Clay, wood, stone, and natural materials inspire supporting colors.

These colors should feel grounded and age gracefully over time.

---

# Emotional Goals

Color should create these feelings.

- Warmth
- Calm
- Presence
- Hope
- Reflection

Color should never create:

- Urgency
- Pressure
- Competition
- Distraction
- Overstimulation

---

# Color Principles

## Warm Before Bright

Warm colors create trust.

Bright colors create excitement.

Antar prioritizes warmth.

---

## Neutral Before Colorful

Most of the interface should rely on restrained neutrals.

Accent colors become more meaningful when used sparingly.

---

## Typography Leads

Typography creates hierarchy.

Spacing creates rhythm.

Color provides subtle emphasis.

The interface should never depend on color alone to establish importance.

---

## Emotion Before Branding

Colors exist to support emotional experience.

Brand recognition should emerge naturally rather than through aggressive visual identity.

---

## Timeless Before Trendy

Color choices should still feel appropriate many years from now.

Avoid colors that feel tied to temporary design trends.

---

# Material Palette

The interface should evoke the feeling of:

- Warm paper
- Morning sunlight
- Soft charcoal ink
- Natural earth
- Quiet spaces

Every future color token should be traceable to one of these materials.

---

# Semantic Color Roles

Rather than defining colors as Primary or Secondary, Antar organizes color around purpose.

## Foundation

Application backgrounds.

Surface colors.

Containers.

Large visual areas.

Foundation colors should quietly disappear behind the content.

---

## Reading

Primary text.

Secondary text.

Dividers.

Supporting typography.

Reading colors exist to maximize long-form reading comfort.

---

## Reflection

Journal prompts.

Reflection cards.

Personal writing.

Reflection colors should feel thoughtful and gentle.

---

## Guidance

Related teachings.

AI guidance.

Supporting educational content.

Guidance colors should illuminate rather than dominate.

---

## Action

Primary actions.

Navigation.

Interactive elements.

Action colors should remain restrained and predictable.

---

## Feedback

Success.

Warning.

Error.

Offline.

Feedback colors should clearly communicate state while remaining consistent with Antar's calm visual language.

---

# Accent Strategy

Antar should have one primary accent color.

The accent exists to gently guide attention.

It should never become decorative.

Accent colors should remain uncommon enough that they retain meaning.

---

# Light Appearance

Light appearance represents the beginning of the day.

It should feel:

- Open
- Warm
- Airy
- Hopeful
- Peaceful

Large bright surfaces should avoid harsh contrast.

Reading comfort always takes priority over visual purity.

---

# Evening Appearance

Dark mode represents the quiet of the evening.

Internally, we refer to it as **Evening**.

Evening should feel:

- Warm
- Restful
- Comfortable
- Quiet

Avoid pure black backgrounds.

Prefer deep neutral surfaces that reduce eye fatigue during extended reading.

The emotional identity should remain identical to the light experience.

Only the lighting changes.

---

# Accessibility

Color should never become the only method of communicating information.

Every interface must maintain sufficient contrast while preserving Antar's calm aesthetic.

Accessibility is a design requirement.

Not an enhancement.

---

# Decision Framework

Before introducing a new color, ask:

- Does this support understanding?
- Does this reduce visual noise?
- Does this feel warm?
- Does this belong in the physical world that inspires Antar?
- Would removing this color improve clarity?

If the answer is yes to the final question, the color probably does not belong.

---

# What We Avoid

The Antar color system intentionally avoids:

- Neon colors
- Highly saturated palettes
- Multiple competing accent colors
- Excessive gradients
- Decorative rainbow palettes
- Visual noise

Restraint creates confidence.

---

# Design Implications

This philosophy influences every future design decision.

It means:

- Backgrounds should feel like paper rather than blank digital canvases.
- Reading surfaces should reduce fatigue during long sessions.
- Accent colors should guide rather than attract attention.
- Journal experiences should feel softer than navigation experiences.
- Guidance should feel illuminated rather than highlighted.
- Light and Evening appearances should feel like different times of the same day instead of separate themes.

---

# Future Implementation

Implementation details belong in the design token system.

Future work includes:

- Foundation color tokens
- Semantic color tokens
- Light appearance tokens
- Evening appearance tokens
- Accessibility validation
- Component color mappings

This document should remain implementation-independent.

---

# North Star

People should not remember Antar because of its colors.

They should remember how those colors made them feel.

The ideal experience should resemble the quiet feeling of opening a meaningful book at sunrise, where the interface disappears and the wisdom becomes the focus.