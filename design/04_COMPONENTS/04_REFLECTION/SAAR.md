# SAAR

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Saar presents a concise distillation of the teaching after the reader has had an opportunity to encounter the scripture and reflect personally.

Its purpose is to reinforce understanding—not replace discovery.

Saar should feel like a quiet closing thought rather than the main event.

---

# Responsibility

Saar is responsible for:

* summarizing the teaching,
* reinforcing the central idea,
* remaining faithful to the scripture,
* providing a concise takeaway.

---

# Non-Responsibilities

Saar is not responsible for:

* translating scripture,
* replacing the original verse,
* interpreting the reader's reflection,
* offering life advice,
* generating personalized guidance,
* evaluating journal entries,
* or encouraging continued engagement.

---

# Usage

Saar appears after the Reflection Stack.

Typical locations:

* Verse
* Journey
* Selected teaching previews

It should not appear before the reader has encountered the scripture.

---

# Experience Principles

## Scripture Comes First

Readers should always encounter the original teaching before Saar.

---

## Reflection Comes Before Saar

Saar reinforces understanding after the reader has been invited to reflect.

It should never become a shortcut that encourages skipping reflection.

---

## Concise by Design

Saar should communicate one central idea.

It should resist the temptation to explain every nuance.

---

## Faithful, Not Creative

Saar represents the teaching.

It should not invent new ideas, emotional interpretations, or modern analogies.

---

# Content Model

Saar receives:

* verse identifier,
* reviewed Saar content,
* language,
* optional attribution metadata.

Version 1 should use curated content rather than dynamically generated AI summaries.

---

# Anatomy

Saar contains:

1. Saar Text

```text
Focus on your actions rather than attachment to their outcomes.
```

Nothing else belongs inside the component.

---

# Variants

## Standard

Displays one reviewed Saar.

---

## Compact

Used within Journey previews or similar condensed contexts.

The meaning should remain intact.

---

# States

## Ready

Saar is available.

---

## Unavailable

If reviewed Saar content is unavailable, omit the component.

Do not generate a replacement dynamically in Version 1.

---

# Interaction Behavior

Saar is read-only.

The component contains no actions.

Navigation belongs to Continue Reading.

Reflection belongs to Reflection Invitation and Journal Editor.

---

# Accessibility

Saar must:

* support Dynamic Type,
* expose semantic text,
* preserve logical reading order,
* remain distinguishable from scripture and translation,
* avoid relying on typography alone for meaning.

---

# Motion

No component-specific motion.

Saar should appear naturally as part of the reading flow.

---

# Design Token Dependencies

Uses:

* Typography System
* Color System
* Spacing System
* Accessibility System

No custom tokens.

---

# Engineering Boundaries

Saar may receive:

* reviewed Saar content,
* verse identifier,
* language.

It must not:

* generate summaries,
* analyze reader reflections,
* choose verses,
* determine placement,
* invoke AI.

---

# Good Examples

✓ One concise takeaway.

✓ Faithful to the teaching.

✓ Appears after reflection.

✓ Visually quieter than scripture.

---

# Anti-Patterns

Avoid:

✗ Turning Saar into commentary.

✗ Multiple paragraphs.

✗ Personalized advice.

✗ AI-generated life coaching.

✗ Presenting Saar before scripture.

✗ Replacing reflection.

---

# Confirmed Decisions

* Saar follows Reflection.
* Version 1 uses curated content.
* Saar never replaces scripture.
* Saar contains no actions.
* One teaching, one concise takeaway.

---

# Design Hypotheses

* What is the ideal maximum length?
* Does Saar add value after reflection?
* Should compact Saar appear in Journey previews?

---

# Validation Questions

* Does Saar reinforce rather than replace understanding?
* Is it concise enough to remain memorable?
* Do readers still engage with scripture before reading Saar?

---

# North Star

Saar succeeds when readers finish with one clear insight while still feeling that the wisdom came from the Bhagavad Gita itself—not from the summary.
