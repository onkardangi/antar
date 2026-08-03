# REFLECTION STACK

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Reflection Stack defines the canonical transition from understanding scripture to responding personally.

Unlike the Scripture Stack, which focuses on understanding the Bhagavad Gita, the Reflection Stack focuses on the reader's relationship with the teaching.

It begins only after the reader has encountered and understood the scripture.

---

# Used By

The Reflection Stack is used by:

* Verse
* Journal
* Journey

Experiences may omit optional elements but should preserve the established hierarchy.

---

# Canonical Structure

```text
Reflection Invitation

↓

Journal Editor

↓

Save Status

↓

Saar

↓

Continue Reading
```

---

# Component Responsibilities

## Reflection Invitation

Creates space for personal thought.

Reflection is always optional.

---

## Saar

Provides a concise takeaway after the reader has had an opportunity to reflect.

Saar reinforces understanding without replacing the reader's own interpretation.

---

## Continue Reading

Provides one meaningful next step.

Navigation should feel like a natural continuation rather than a call to action.

---

# Design Principles

## Reflection Before Guidance

Readers should be given an opportunity to think before encountering distilled guidance.

---

## Invite, Never Demand

Reflection is encouraged but never required.

Readers should never feel obligated to write or respond.

---

## Personal Meaning

The Reflection Stack supports the reader's own understanding.

It should never evaluate, score, or judge their response.

---

## Gentle Continuation

The experience should conclude by quietly inviting the reader back into scripture.

Navigation should never compete with reflection.

---

# Forbidden Patterns

Do not:

* present Saar before Reflection Invitation,
* require reflection before continuing,
* interrupt reflection with AI conversations,
* introduce achievements, streaks, or progress metrics,
* display multiple competing continuation actions.

---

# Engineering Notes

The Reflection Stack owns only the composition.

Each child component remains independently reusable.

Experiences determine visibility and data.

---

# Validation Questions

* Does Reflection before Saar encourage deeper engagement?
* Is Saar concise enough to reinforce rather than replace reflection?
* Does Continue Reading feel like a natural conclusion?
* Do readers understand that reflection is optional?

---

# North Star

The Reflection Stack succeeds when readers move naturally from understanding to personal reflection and then quietly return to their journey through the Bhagavad Gita.
