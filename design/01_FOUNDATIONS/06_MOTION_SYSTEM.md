# MOTION SYSTEM

**Version:** 1.0
**Status:** Approved for Design Exploration
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

This document defines how motion is used throughout Antar.

Motion exists to preserve continuity, reduce cognitive effort, reinforce reading rhythm, and provide meaningful feedback.

Motion is part of the reading experience.

It should never become the focus of the experience.

---

# Why This Exists

Movement influences how people perceive transitions, relationships, and continuity.

Poor motion creates distraction.

Excessive motion competes with attention.

Absent motion can make interfaces feel abrupt and disconnected.

Antar uses motion intentionally to help users move through wisdom with clarity and calm.

---

# Motion Philosophy

Motion should feel like turning the next page of a book.

It should never feel like changing applications.

Transitions should be quiet, predictable, and purposeful.

The user should rarely notice animation itself.

Instead, they should notice that the experience feels natural.

---

# Core Principles

## 1. Preserve Context

Motion should help users understand:

* where they came from,
* what changed,
* and where they are going.

Transitions should maintain continuity rather than creating surprise.

---

## 2. Reduce Cognitive Load

Animation should simplify understanding.

Movement should clarify relationships between interface elements.

Users should never spend mental effort interpreting an animation.

---

## 3. Reinforce Reading Rhythm

Motion should support the emotional pace of the current experience.

Reading experiences should feel slower than browsing experiences.

Reflection should feel calmer than navigation.

---

## 4. Reward Intention

Motion should occur because the user intentionally interacted with the product.

Animation should not exist solely to attract attention.

---

## 5. Respect Stillness

Not every change requires movement.

Stillness is an intentional design decision.

During reading and reflection, unnecessary animation should disappear.

---

## 6. Motion Should Never Compete

The teaching remains the visual focus.

Whenever motion risks distracting from content, motion should yield.

---

# Motion Families

Antar uses three primary motion families.

---

## Continue

Purpose:

Maintain uninterrupted flow.

Examples:

* Verse → Understanding
* Reflection → Saar
* Continue Reading

These transitions should feel continuous, as though the reader is progressing through the same experience.

---

## Reveal

Purpose:

Introduce additional depth.

Examples:

* Expand commentary
* Show AI guidance
* Reveal notes
* Display related verses

Reveal animations should unfold naturally.

Information should appear rather than suddenly arrive.

---

## Return

Purpose:

Restore context.

Examples:

* Back navigation
* Closing a bottom sheet
* Leaving Journal
* Returning to Library

Return animations should reinforce orientation and preserve mental context.

---

# Motion Tempo

Motion should match the pace of the experience.

---

## Fast

Used for:

* Button feedback
* Small interactions
* Toggle changes
* Interface responses

Fast motion communicates responsiveness.

---

## Moderate

Used for:

* Navigation
* Bottom sheets
* Cards
* Dialogs

Moderate motion preserves continuity without delaying interaction.

---

## Slow

Used for:

* Verse transitions
* Reflection
* Saar
* Journey

Slow motion encourages presence and contemplation.

---

# Reading Transitions

Reading should feel uninterrupted.

Transitions between reading stages should resemble progression through ideas rather than movement between screens.

Whenever possible, transitions should preserve scroll position, visual continuity, and contextual awareness.

---

# Progressive Disclosure

Additional information should unfold naturally.

Users should never feel overwhelmed by large amounts of content appearing simultaneously.

Supporting information should arrive only when requested.

---

# Haptic Philosophy

Haptics complement meaningful interactions.

They should remain subtle and infrequent.

Examples:

* Bookmark saved
* Reflection saved
* Important confirmation

Reading itself should not trigger haptic feedback.

Silence is part of the experience.

---

# Reduced Motion

Users who enable Reduced Motion should receive:

* simplified transitions,
* reduced movement,
* preserved orientation,
* and unchanged usability.

Reducing animation should never reduce understanding.

---

# Motion Rules

## Rule 1

Every animation must have a purpose.

---

## Rule 2

Motion should preserve context.

---

## Rule 3

Animation should reinforce—not interrupt—the reading experience.

---

## Rule 4

Stillness is preferable to decorative animation.

---

## Rule 5

Motion should reward user intention rather than demand attention.

---

## Rule 6

Reading experiences should use calmer motion than browsing experiences.

---

## Rule 7

Haptics should reinforce meaningful actions, not routine reading.

---

## Rule 8

Reduced Motion must preserve the same conceptual experience.

---

## Rule 9

Motion should remain consistent across equivalent interactions.

---

## Rule 10

Animation should never delay understanding.

---

# Anti-Patterns

Avoid:

* bouncing elements,
* looping animations,
* pulsing controls,
* celebratory effects,
* excessive parallax,
* decorative motion,
* automatic content movement,
* distracting loading animations,
* exaggerated spring physics,
* and motion that competes with scripture.

---

# Confirmed Principles

The following decisions are foundational:

* Motion preserves context.
* Motion reduces cognitive load.
* Motion reinforces reading rhythm.
* Motion rewards intention.
* Stillness is part of the experience.
* Motion should never compete with content.
* Three motion families: Continue, Reveal, Return.
* Haptics remain subtle and purposeful.

---

# Design Hypotheses

The following require validation:

* Animation durations.
* Easing curves.
* Shared element transitions.
* Tablet-specific motion.
* Interactive gesture behavior.
* Scroll-linked transitions.
* Haptic intensity.

These should be refined during prototyping.

---

# Decision Framework

Before approving motion, ask:

1. What purpose does this animation serve?

2. Does it preserve context?

3. Does it reduce cognitive effort?

4. Does it support the emotional pace?

5. Would removing it improve the experience?

6. Does it compete with reading?

7. Does it respect Reduced Motion?

8. Does it reward intentional interaction?

---

# Design Implications

This motion system means:

* Verse transitions should feel continuous.
* Reflection should emerge gently.
* AI should reveal itself rather than interrupt.
* Navigation should preserve orientation.
* Reading should remain visually stable.
* Decorative animation should remain extremely rare.
* Motion should quietly reinforce the emotional rhythm established by layout, spacing, and typography.

---

# Engineering Implications

Implementation should:

* use semantic motion tokens rather than hard-coded durations,
* separate motion specifications from component logic,
* support Reduced Motion system settings,
* provide consistent transition behavior,
* avoid unnecessary layout reflows,
* preserve accessibility focus during transitions,
* and maintain smooth performance on supported devices.

Exact timing values, easing curves, and haptic configurations belong in implementation-level design tokens.

---

# Relationship to Other Documents

This document defines motion.

Related documents define:

* `01_DESIGN_DNA.md` — overarching design philosophy.
* `03_LAYOUT_SYSTEM.md` — structural flow.
* `04_SPACING_SYSTEM.md` — reading rhythm through space.
* `05_TYPOGRAPHY.md` — reading rhythm through text.
* `09_ACCESSIBILITY.md` — accessibility adaptations.
* Experience specifications — motion applied to individual screens.

---

# North Star

Motion should never make Antar feel more exciting.

It should make Antar feel more continuous.

The best animation is the one that quietly helps the user move from one meaningful moment to the next without ever interrupting the relationship between the reader and the teaching.
