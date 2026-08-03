# TRANSLITERATION BLOCK

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Transliteration Block presents the Sanskrit verse using the Latin alphabet, allowing readers who cannot read Devanagari to pronounce and follow the original scripture.

It exists as a bridge between the original Sanskrit text and the reader.

The component supports learning and pronunciation while preserving the original scripture as the primary reading experience.

---

# Responsibility

Transliteration Block is responsible for:

* displaying the Sanskrit verse in a standardized Latin transliteration,
* preserving the order and structure of the original verse,
* maintaining readability,
* supporting pronunciation,
* remaining visually secondary to the original scripture.

---

# Non-Responsibilities

Transliteration Block is not responsible for:

* displaying Devanagari,
* translating meaning,
* explaining vocabulary,
* teaching Sanskrit grammar,
* generating pronunciation,
* rendering commentary,
* presenting Saar,
* or replacing the original scripture.

---

# Usage

Transliteration Block appears only after the Verse Block.

It is optional.

Readers who do not enable transliteration should never encounter it.

Typical locations:

* Verse
* Guided pronunciation experiences (future)
* Offline reading

It should not appear independently of the corresponding Verse Block.

---

# Experience Principles

## Scripture Comes First

The original Sanskrit always precedes Transliteration.

Readers should never encounter Transliteration before the original text.

---

## Learning Without Distraction

Transliteration supports readers who wish to engage with Sanskrit pronunciation.

It should remain visually quieter than the Verse Block and should never become the focal point of the experience.

---

## Preserve Canonical Structure

Every line, stanza, and ordering should mirror the original scripture.

The component should never merge, split, or rearrange verses for readability.

---

## Optional by Design

Readers who do not need Transliteration should not experience additional visual complexity.

Visibility should be controlled by reading preferences rather than by individual experiences.

---

# Content Model

The component should receive:

* canonical verse identifier,
* standardized transliterated text,
* ordered lines,
* optional stanza grouping,
* language metadata.

Transliteration should originate from a trusted source rather than being generated dynamically.

---

# Anatomy

Transliteration Block contains:

1. Transliterated verse text
2. Canonical line structure

```text id="v1abce"
karmaṇy evādhikāras te

mā phaleṣu kadācana

mā karma-phala-hetur bhūr

mā te saṅgo 'stv akarmaṇi
```

Verse Reference remains outside the component.

---

# Variants

## Standard

Displays the complete transliterated verse.

---

## Long Verse

Supports verses with additional lines while preserving readability.

---

## Read-Only

Default variant.

Readers consume the transliteration without editing.

---

## Selectable

Allows platform-native text selection when enabled.

Selection should not introduce additional controls inside the component.

---

# States

## Ready

Complete transliteration is available.

---

## Hidden

The reader has disabled transliteration in reading preferences.

The parent experience omits the component entirely.

---

## Unavailable

If trusted transliteration data is unavailable, omit the component rather than generating one automatically.

The Verse experience should continue normally.

---

# Interaction Behavior

Transliteration Block is primarily read.

It should not contain:

* bookmark actions,
* AI actions,
* pronunciation controls,
* sharing,
* reflection,
* or navigation.

Future pronunciation features should compose this component rather than expanding it.

---

# Typography

Transliteration should use a highly readable Latin typeface with support for diacritical marks.

Typography should clearly distinguish Transliteration from both Verse Block and Translation Block while remaining harmonious with the overall reading experience.

---

# Accessibility

The component must:

* preserve logical reading order,
* support Dynamic Type,
* expose text rather than images,
* correctly announce Latin characters,
* remain keyboard accessible,
* preserve line structure.

Accessibility labels should identify the content as transliteration rather than translation.

---

# Motion

No component-specific motion.

The block should appear naturally as part of the reading flow.

---

# Design Token Dependencies

Uses semantic tokens from:

* Typography System
* Color System
* Spacing System
* Accessibility System

No unique visual tokens should be introduced.

---

# Engineering Boundaries

Transliteration Block may receive:

* verse identifier,
* transliterated text,
* line grouping,
* visibility preference,
* accessibility metadata.

It must not:

* generate transliteration,
* infer pronunciation,
* fetch scripture,
* calculate visibility rules,
* own reading preferences.

---

# Good Examples

✓ Appears immediately after Verse Block when enabled.

✓ Preserves line structure exactly.

✓ Uses readable typography with correct diacritics.

✓ Can be omitted without affecting the reading experience.

---

# Anti-Patterns

Avoid:

✗ Showing Transliteration without the original Sanskrit.

✗ Automatically generating transliteration using AI.

✗ Mixing translation and transliteration into one component.

✗ Adding pronunciation buttons inside the component.

✗ Giving Transliteration greater visual emphasis than Verse Block.

---

# Confirmed Decisions

* Transliteration is optional.
* Verse Block always precedes Transliteration.
* Canonical structure is preserved.
* Transliteration never replaces scripture.
* Reading preferences determine visibility.

---

# Design Hypotheses

The following require validation:

* Which transliteration standard should Antar adopt consistently.
* Whether readers benefit from selectable transliteration in V1.
* Whether transliteration should use slightly reduced visual emphasis compared to scripture.

---

# Validation Questions

* Do readers understand the difference between transliteration and translation?
* Does the component help readers engage with Sanskrit without distracting from the original scripture?
* Is the visual hierarchy sufficiently clear?
* Do diacritical marks remain readable across supported platforms?

---

# North Star

Transliteration Block succeeds when readers who cannot read Devanagari feel welcomed into the original Sanskrit without the transliteration ever becoming more important than the scripture itself.
