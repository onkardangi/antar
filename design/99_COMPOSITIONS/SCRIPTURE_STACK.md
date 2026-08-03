# SCRIPTURE STACK

**Version:** 1.1
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Scripture Stack defines the canonical presentation of a teaching within Antar.

It establishes the approved hierarchy for presenting scripture and its supporting reading content while preserving the Bhagavad Gita as the center of the experience.

The Scripture Stack ends once the reader has sufficient context to understand the teaching.

Personal reflection begins in a separate composition.

---

# Used By

The Scripture Stack may be used by:

* Verse
* Guidance
* Journal (reference context)
* Journey (memory previews)
* Future teaching-focused experiences

Experiences may omit optional elements, but they should preserve the established hierarchy.

---

# Canonical Structure

```text
Verse Reference
        ↓
Verse Block
        ↓
Transliteration Block (Optional)
        ↓
Translation Block
```

---

# Component Responsibilities

## Verse Reference

Provides orientation.

Readers understand where the teaching belongs.

---

## Verse Block

Presents the original Sanskrit scripture.

This is the primary content of the experience.

---

## Transliteration Block

Optional.

Supports pronunciation and accessibility without replacing the original Sanskrit.

---

## Translation Block

Provides a faithful translation of the original text.

Translation explains what the words say.

It does not interpret, summarize, or apply the teaching.

---

# Design Principles

## Scripture First

The Bhagavad Gita remains the visual and conceptual center of the stack.

Supporting layers exist only to improve understanding.

---

## Progressive Understanding

Each layer answers the reader's next natural question.

```text
Where am I?
        ↓
What does the scripture say?
        ↓
How do I pronounce it?
        ↓
What does it mean?
```

No layer should answer questions that belong to reflection or interpretation.

---

## Separation of Responsibilities

The Scripture Stack exists to help the reader understand the teaching.

Reflection belongs to a separate composition.

Navigation belongs to Navigation components.

No component should cross those boundaries.

---

## Calm Reading Rhythm

The stack should encourage uninterrupted reading.

Nothing inside the stack should pressure the reader to continue, respond, or interact.

---

# Optional Elements

Experiences may omit:

* Transliteration Block

The remaining order should never change.

---

# Forbidden Patterns

Do not:

* present Translation before Verse Block,
* insert AI explanations before scripture,
* insert commentary between scripture and translation,
* mix reflection invitations into the Scripture Stack,
* insert Saar before translation,
* interrupt scripture with promotional content.

---

# Engineering Notes

The Scripture Stack is a composition.

It owns:

* hierarchy,
* ordering,
* composition.

It does not own:

* state,
* navigation,
* business logic,
* preferences,
* visibility rules.

Each child component remains independently reusable.

---

# Validation Questions

* Does this hierarchy feel natural to first-time readers?
* Does separating reflection from scripture improve clarity?
* Does optional Transliteration add value without increasing complexity?
* Does the stack preserve scripture as the primary focus?

---

# North Star

The Scripture Stack succeeds when readers naturally progress from orientation to scripture to understanding without the interface competing for attention. Every layer should support the Bhagavad Gita while allowing the teaching itself to remain the center of the experience.
