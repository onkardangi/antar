# VERSE BLOCK

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Verse Block presents the original Sanskrit scripture in a calm, readable, and respectful form.

It is the primary content component within the Verse experience.

The component should encourage attentive reading while allowing the surrounding interface to recede.

---

# Responsibility

Verse Block is responsible for:

* rendering the original Sanskrit verse,
* preserving line and stanza structure,
* supporting readable Devanagari typography,
* maintaining stable reading order,
* scaling with accessibility preferences,
* and presenting scripture without unrelated interface elements.

---

# Non-Responsibilities

Verse Block is not responsible for:

* displaying the chapter or verse reference,
* rendering transliteration,
* displaying translations,
* presenting commentary,
* generating explanations,
* showing Saar,
* capturing reflection,
* managing bookmarks,
* exposing sharing actions,
* or calculating reading progress.

Those responsibilities belong to separate Scripture, Reflection, Navigation, or service layers.

---

# Usage

Verse Block is used wherever the original Sanskrit verse is presented as primary reading content.

Primary use:

* Verse experience

Possible secondary uses:

* Guidance, after a teaching has been selected
* Saved scripture views
* Verse comparison, if introduced later
* Offline reading surfaces

Verse Block should not be used as a short preview when the full scripture is not intended to be read.

A preview should use a separate composition or truncation pattern defined by the consuming experience.

---

# Experience Principles

## Scripture Is Primary

Verse Block should receive the highest content emphasis within the Verse experience.

Supporting content may explain, translate, or contextualize the teaching, but it should not visually overpower the scripture.

---

## Typography Before Decoration

The component should rely on:

* type,
* line spacing,
* alignment,
* and surrounding whitespace.

It should not require:

* cards,
* borders,
* shadows,
* ornamental backgrounds,
* religious symbols,
* or decorative illustration.

---

## Preserve the Text

The component must respect the trusted source text.

It should not:

* rewrite,
* simplify,
* paraphrase,
* dynamically alter,
* or generate scripture.

Display transformations should be limited to presentation and accessibility.

---

## Stable During Reading

Scripture should remain visually stable.

Avoid controls, motion, or layout changes inside the component while the reader is engaging with it.

---

## One Verse at a Time

Verse Block presents one canonical verse unit.

It should not become:

* a chapter reader,
* a scrolling verse feed,
* a recommendation carousel,
* or a multi-verse comparison surface.

Experiences that present several verses should compose multiple Verse Blocks or use another purpose-built reading structure.

---

# Content Model

Verse Block should receive trusted, structured scripture content.

Recommended conceptual fields:

* verse identifier,
* language or script identifier,
* ordered text lines,
* optional stanza grouping,
* source attribution metadata outside the visible component when required.

The component should not infer line breaks from arbitrary visual width when trusted structural breaks are available.

---

# Anatomy

Verse Block contains:

1. Scripture text
2. Structural line breaks
3. Optional stanza separation

```text
कर्मण्येवाधिकारस्ते
मा फलेषु कदाचन ।

मा कर्मफलहेतुर्भूः
मा ते सङ्गोऽस्त्वकर्मणि ॥
```

The verse reference remains outside this component.

---

# Variants

## Standard Verse

Displays one complete Sanskrit verse using its trusted structural grouping.

This is the default variant.

---

## Long Verse

Supports verses with additional lines or greater visual height.

The component should grow naturally.

It must not:

* reduce type size automatically,
* collapse text,
* truncate scripture,
* or place the verse inside a fixed-height region.

---

## Grouped Stanza

Used when the source content defines meaningful stanza or line groupings.

Separation should preserve the supplied structure without adding decorative interpretation.

---

## Selectable Verse

Allows the reader to select scripture text when platform behavior, content licensing, and product requirements permit it.

Selection must not introduce persistent controls inside the component.

---

## Read-Only Verse

Prevents text selection where required by platform, licensing, or interaction constraints.

The visible presentation should otherwise remain identical.

---

# Text Structure

## Source Line Breaks

Trusted line breaks should be preserved when they carry textual or poetic structure.

Responsive layout may wrap individual lines when necessary, but the component should retain the original sequence and grouping.

---

## Punctuation

Traditional punctuation, including danda and double danda characters, should be preserved exactly as supplied by the trusted content source.

The component must not replace them with Latin punctuation for visual convenience.

---

## Whitespace

Whitespace within the trusted verse should be normalized only when required for reliable display.

Do not remove meaningful stanza separation.

Do not add arbitrary blank lines solely for decoration.

---

# Alignment

Verse Block should default to left alignment for consistency, readability, and accessibility.

Centered presentation may be explored only if prototype validation demonstrates that it improves the reading experience without harming:

* long-verse readability,
* Dynamic Type behavior,
* screen-reader order,
* or multilingual consistency.

Long scripture passages should not use full justification.

---

# States

## Ready

The complete trusted scripture is available.

---

## Loading

Reserve the expected reading area without simulating scripture through misleading placeholder text.

A quiet structural placeholder may be used if loading cannot be avoided.

The experience should prioritize local or cached scripture so loading is rare.

---

## Unavailable

If the original scripture cannot be displayed, the component should not fabricate, paraphrase, or substitute generated content.

The parent experience should present a clear content-unavailable state.

---

## Invalid Content

If structured scripture data is malformed or incomplete, do not render partial text as though it were canonical.

The parent experience should handle the failure and preserve navigation to other available content.

---

# Interaction Behavior

Verse Block is primarily read rather than operated.

Optional supported interactions may include:

* native text selection,
* copy, if allowed,
* screen-reader navigation by line or text unit.

The component should not include embedded actions such as:

* Bookmark
* Share
* Ask AI
* Reflect
* Play audio
* Continue Reading

Those actions belong outside the scripture component.

---

# Accessibility

Verse Block must receive exceptional accessibility care because it contains Antar’s primary source content.

It must:

* identify the content language correctly,
* preserve logical line order,
* support Dynamic Type,
* avoid fixed heights,
* prevent clipping of Devanagari marks,
* remain readable at high zoom,
* support VoiceOver and TalkBack,
* expose the verse as text rather than as an image,
* and avoid inserting decorative elements into the semantic reading order.

## Language Metadata

The component should expose the correct Sanskrit language or script metadata supported by the platform.

Fallback behavior should be tested because assistive-technology pronunciation of Sanskrit may vary by device and installed voice.

The product must not claim accurate spoken Sanskrit pronunciation unless it has been deliberately validated.

---

## Screen-Reader Flow

Verse Reference should be announced before Verse Block by the parent experience.

Within Verse Block, the scripture should be read in canonical sequence.

If punctuation produces unnatural announcements, accessibility-specific text may be considered only if it preserves the exact meaning and does not alter the visible scripture.

Any such behavior requires content and accessibility review.

---

## Dynamic Type

The component must grow vertically as text scales.

It must not:

* truncate,
* shrink automatically,
* introduce internal scrolling,
* or overlap adjacent content.

The parent layout should preserve enough spacing around the expanded verse.

---

## Devanagari Rendering

Typography and line height must allow sufficient vertical room for:

* matras,
* conjuncts,
* vowel marks,
* and other script features.

Testing must use real verses rather than placeholder Latin text.

---

# Typography

Verse Block depends on the Scripture typography role defined in the Typography System.

It should use:

* a carefully selected Devanagari reading face,
* regular or appropriate reading weight,
* generous line height,
* sufficient size for sustained reading,
* and stable visual hierarchy.

Avoid:

* decorative spiritual typefaces,
* artificial italics,
* compressed line height,
* excessive bold weight,
* or Latin-oriented fonts with weak Devanagari support.

Exact type tokens should be validated in Figma and on physical devices.

---

# Spacing

The component owns spacing between its own scripture lines and stanza groups.

The parent experience owns spacing:

* before Verse Block,
* after Verse Block,
* between Verse Block and Transliteration,
* and between Verse Block and Translation.

Verse Block should not embed large external margins that make composition difficult.

---

# Color

Scripture should use a high-readability semantic text color.

It should not rely on accent color, gradients, or decorative highlights to establish importance.

Importance comes from hierarchy, placement, typography, and space.

Any selected-text treatment should preserve contrast and readability.

---

# Motion

Verse Block should remain still.

Appropriate motion is limited to:

* the standard appearance of content when an experience loads,
* native selection behavior,
* or a quiet transition controlled by the parent experience.

Avoid:

* animated line reveals,
* pulsing text,
* parallax,
* scroll-linked scripture effects,
* word-by-word animation,
* or decorative entrance motion.

The scripture should never perform for the reader.

---

# Design Token Dependencies

Verse Block should use semantic tokens from:

* Typography System
* Color System
* Spacing System
* Accessibility System

It should not introduce:

* custom backgrounds,
* unique shadow tokens,
* component-specific gradients,
* or ornamental styling tokens.

---

# Engineering Boundaries

Verse Block may receive:

* canonical verse identifier,
* ordered scripture lines,
* stanza grouping,
* language metadata,
* text-selection configuration,
* accessibility text override when explicitly approved.

Verse Block should not:

* fetch scripture,
* choose a verse,
* infer missing content,
* generate scripture,
* translate text,
* calculate reading progress,
* persist bookmarks,
* trigger AI,
* or own navigation.

The parent experience or content service must provide validated scripture data.

---

# Content Integrity

Scripture content must come from an approved, trusted source.

Engineering should preserve:

* Unicode characters,
* punctuation,
* line ordering,
* and verse identity.

Content normalization, database import, and rendering pipelines must be tested for accidental character changes.

Visual snapshots alone are insufficient.

Automated content-integrity checks should compare stored and rendered source values where practical.

---

# Good Examples

✓ A complete Sanskrit verse presented with generous line height and no decorative container.

✓ A long verse grows vertically while preserving readable structure.

✓ VoiceOver reaches the scripture after announcing its Verse Reference.

✓ The component preserves danda punctuation and trusted stanza grouping.

✓ Bookmark and AI actions remain outside the Verse Block.

---

# Anti-Patterns

Avoid:

✗ Rendering scripture as an image.

✗ Placing Save, Share, AI, or Reflection actions inside the component.

✗ Automatically reducing the font size to fit a fixed height.

✗ Truncating long verses.

✗ Applying decorative mandalas, gradients, shadows, or religious imagery behind the text.

✗ Replacing trusted punctuation or line structure.

✗ Using generated or paraphrased text when scripture content is unavailable.

✗ Treating Transliteration or Translation as Verse Block variants.

---

# Confirmed Decisions

* Verse Block presents only the original scripture.
* Verse Reference remains a separate component.
* Transliteration remains a separate component.
* Translation remains a separate component.
* Trusted textual structure is preserved.
* Scripture is rendered as accessible text.
* The component has no embedded reading actions.
* The component grows naturally with content and Dynamic Type.
* Motion remains absent or nearly invisible.

---

# Design Hypotheses

The following require validation:

* Final Devanagari font family.
* Exact type size and line height.
* Left alignment versus limited centered presentation.
* Whether text selection belongs in V1.
* Whether stanza grouping requires dedicated spacing tokens.
* How Sanskrit screen-reader pronunciation behaves on supported devices.
* Whether loading placeholders are ever necessary when scripture is cached.

---

# Validation Questions

* Can readers comfortably spend extended time with the scripture?
* Does Verse Block remain the clear focal point without decorative styling?
* Are long verses readable on small devices and at large text sizes?
* Does Devanagari render correctly across supported iOS and Android versions?
* Does preserving source line structure create any unacceptable wrapping behavior?
* Can screen-reader users navigate and understand the verse in the intended order?
* Does removing all embedded actions improve focus without harming discoverability elsewhere?

---

# North Star

Verse Block succeeds when the scripture feels complete, stable, and worthy of attention on its own—without needing decoration, interaction, or explanation to justify its presence.
