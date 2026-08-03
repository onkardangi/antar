# TRANSLATION BLOCK

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Translation Block presents a faithful translation of the Sanskrit scripture in the reader's preferred language.

Its purpose is to make the original teaching understandable without interpreting, summarizing, or applying it.

Translation is the bridge from the original language to comprehension.

---

# Responsibility

Translation Block is responsible for:

* displaying the translated verse,
* preserving the meaning of the selected translation,
* maintaining readability,
* clearly identifying the active translation,
* supporting multilingual reading.

---

# Non-Responsibilities

Translation Block is not responsible for:

* rendering Sanskrit,
* transliteration,
* commentary,
* AI explanations,
* personal reflection,
* Saar,
* chapter summaries,
* navigation,
* or scripture interpretation.

Those responsibilities belong to separate components or compositions.

---

# Usage

Translation Block appears immediately after the Scripture portion of the reading experience.

Typical usage:

* Verse
* Guidance
* Offline reading
* Saved scripture

Translation Block should never appear before Verse Block.

---

# Experience Principles

## Faithful Before Simplified

The component presents an approved translation.

It should never paraphrase, summarize, or simplify the translation dynamically.

---

## Translation Is Not Commentary

Translation communicates the words.

It does not explain them.

Interpretation belongs elsewhere.

---

## Reader Choice

Readers may choose their preferred translation in Reading Preferences.

Translation Block simply renders the selected translation.

It does not determine which translation should be used.

---

## Consistent Presentation

The same translation should be rendered consistently throughout Antar.

Typography, spacing, and attribution should remain predictable.

---

# Content Model

Translation Block receives:

* verse identifier,
* translation identifier,
* translated text,
* translator attribution,
* language metadata.

Translation data should originate from trusted, versioned sources.

---

# Anatomy

Translation Block contains:

1. Translation Text
2. Translation Attribution

```text
You have a right to perform your prescribed duty,
but you are not entitled to the fruits of your actions.

— Swami Gambirananda
```

Attribution should remain visually secondary to the translation itself.

---

# Variants

## Standard

Displays one selected translation.

This is the only V1 variant.

---

## Comparison (Future)

Displays multiple approved translations for study purposes.

Not included in V1.

---

# States

## Ready

Translation is available.

---

## Loading

Reserve the expected reading area while loading.

Loading should be rare when scripture is cached.

---

## Unavailable

If the selected translation is unavailable, the parent experience should present an appropriate content state.

Translation Block should never fabricate or generate a replacement translation.

---

# Interaction Behavior

Translation Block is read rather than operated.

The component should not contain:

* AI actions,
* commentary,
* reflection,
* sharing,
* bookmarking,
* navigation,
* or translation switching controls.

Translation selection belongs to Reading Preferences.

---

# Typography

Translation should use the application's primary reading typeface.

It should remain:

* highly readable,
* visually quieter than Verse Block,
* comfortably spaced for sustained reading.

Attribution should use a secondary typography role.

---

# Accessibility

Translation Block must:

* support Dynamic Type,
* expose translated text as semantic text,
* preserve reading order,
* identify the translation attribution,
* support screen readers,
* avoid truncation.

Accessibility should not rely on typography alone to distinguish attribution from translated content.

---

# Motion

Translation Block introduces no component-specific motion.

Appearance should feel calm and continuous within the reading experience.

---

# Design Token Dependencies

Translation Block uses:

* Typography System
* Color System
* Spacing System
* Accessibility System

No custom visual tokens should be introduced.

---

# Engineering Boundaries

Translation Block may receive:

* verse identifier,
* translation identifier,
* translated text,
* translator name,
* language,
* accessibility metadata.

It must not:

* choose translations,
* generate translations,
* fetch scripture,
* interpret meaning,
* manage preferences,
* or own navigation.

---

# Good Examples

✓ Displays one approved translation.

✓ Clearly identifies the translator.

✓ Preserves readability across Dynamic Type sizes.

✓ Appears immediately after Verse Block (and Transliteration when enabled).

---

# Anti-Patterns

Avoid:

✗ Mixing commentary into the translation.

✗ Omitting translator attribution.

✗ Presenting multiple translations in V1.

✗ Generating AI translations.

✗ Placing Translation before the original Sanskrit.

✗ Embedding reflection or navigation controls.

---

# Confirmed Decisions

* Translation follows Verse Block.
* Translation remains distinct from interpretation.
* Reader preferences determine the active translation.
* One translation is shown in V1.
* Translator attribution is always displayed.

---

# Design Hypotheses

The following require validation:

* Whether translator attribution should always remain visible.
* Whether long translations require additional spacing.
* Whether translation comparison belongs in a future release.

---

# Validation Questions

* Do readers clearly distinguish translation from interpretation?
* Is translator attribution noticeable without competing with the content?
* Does the component remain comfortable to read over long passages?
* Is one translation sufficient for V1?

---

# North Star

Translation Block succeeds when readers understand the original teaching in their preferred language while recognizing that the translation is a faithful rendering of the scripture—not its interpretation.
