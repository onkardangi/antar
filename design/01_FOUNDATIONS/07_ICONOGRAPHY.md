# ICONOGRAPHY SYSTEM

**Version:** 1.0
**Status:** Approved for Design Exploration
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

This document defines how icons are used throughout Antar.

Icons exist to reduce cognitive effort by supporting navigation and interaction.

They should never compete with reading, reflection, or the teachings themselves.

---

# Why This Exists

Icons communicate meaning quickly.

When used thoughtfully, they reduce reading effort and improve recognition.

When overused, they create visual noise and distract from content.

Antar treats icons as supporting elements rather than visual decoration.

Users should remember the wisdom they encountered—not the iconography that surrounded it.

---

# Iconography Philosophy

Icons should quietly support understanding.

They should feel familiar, restrained, and timeless.

The closer users move toward scripture and reflection, the fewer icons they should encounter.

The interface should gradually disappear as users move deeper into the reading experience.

---

# Core Principles

## 1. Icons Reduce Reading Effort

Icons should simplify interaction.

They should never exist purely for decoration.

Every icon should help users recognize an action, destination, or state more quickly.

---

## 2. Words Matter More Than Symbols

Icons support language.

They do not replace it.

Whenever an icon could reasonably be misunderstood, pair it with text.

---

## 3. Reading Comes Before Interface

Reading experiences should contain very few icons.

The interface should gradually recede as users progress from:

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

By the time users reach Saar, the interface should be nearly invisible.

---

## 4. Familiar Before Novel

Antar should use widely understood visual metaphors.

Avoid inventing new icon meanings when established conventions already exist.

Learning wisdom should never require learning the interface.

---

## 5. Restraint Creates Clarity

Fewer icons create stronger recognition.

Only introduce icons that solve a genuine usability problem.

---

## 6. Universal Before Cultural

The teachings already provide cultural richness.

The interface should remain welcoming to everyone.

Avoid using religious or spiritual symbols as functional interface elements.

---

## 7. Accessibility Is Fundamental

Every icon must remain understandable through:

* accessible labels,
* sufficient touch targets,
* semantic descriptions,
* and supporting text where appropriate.

Icons should never rely solely on color or animation to communicate meaning.

---

# Visual Style

Icons should feel:

* lightweight,
* quiet,
* contemporary,
* and timeless.

They should avoid unnecessary detail while remaining immediately recognizable.

The icon system should prioritize consistency over visual personality.

---

# Stroke Philosophy

Outlined icons are the default.

Outlined icons carry less visual weight and better support Antar's calm aesthetic.

Filled icons should be reserved for meaningful state changes.

Examples:

* Active navigation
* Saved bookmark
* Selected item
* Completed state

Filled icons should communicate state—not style.

---

# Icon Categories

The icon library should remain intentionally small.

Primary categories include:

* Navigation
* Reading
* Journal
* Journey
* Search
* Settings
* System Feedback

Every new icon should justify its existence.

---

# Usage Guidelines

Icons are appropriate for:

* navigation,
* quick recognition,
* state indication,
* lightweight actions.

Icons should generally not appear within:

* scripture,
* translations,
* Saar,
* long-form commentary,
* or reflective writing.

Reading experiences should remain primarily typographic.

---

# Motion

Icons should animate only when supporting understanding.

Examples:

* bookmark fills,
* chevron rotates,
* disclosure expands.

Avoid:

* bouncing,
* spinning,
* looping,
* pulsing,
* decorative transitions.

Motion should communicate state—not entertain.

---

# Accessibility

Every icon must provide:

* semantic accessibility labels,
* sufficient touch targets,
* keyboard accessibility where applicable,
* screen reader descriptions,
* adequate contrast.

Icons should never become the sole method of communicating important information.

---

# Platform Consistency

Icons should feel native on both iOS and Android while maintaining Antar's identity.

Minor platform adaptations are acceptable when they improve usability.

The conceptual meaning of each icon should remain consistent across platforms.

---

# Future Icon Library

Antar should maintain a curated icon library rather than continuously expanding it.

When introducing a new icon, ask:

* Does an existing icon already communicate this idea?
* Would text communicate this more clearly?
* Is this interaction truly important enough to deserve an icon?

The default answer should favor simplicity.

---

# Icon Selection Criteria

Future icon families should provide:

* consistent stroke weight,
* clean geometry,
* multilingual friendliness,
* scalability,
* accessibility,
* open licensing,
* React Native compatibility,
* and long-term maintainability.

Any adopted icon family should reinforce Antar's calm visual language rather than establish its own personality.

---

# Anti-Patterns

Avoid:

* decorative icons,
* excessive icon usage,
* competing icon styles,
* religious symbols as interface controls,
* emoji-style icons,
* filled icons without meaning,
* icon-only interfaces,
* overly detailed illustrations,
* inconsistent stroke weights,
* and animated icons that compete with content.

---

# Confirmed Principles

The following decisions are foundational:

* Icons reduce reading effort.
* Icons become less prominent as users move deeper into the experience.
* Outlined icons are the default.
* Filled icons communicate state.
* Universal metaphors are preferred over custom symbolism.
* Text remains the primary communicator.
* Accessibility is mandatory.
* The icon library should remain intentionally small.

---

# Design Hypotheses

The following require validation:

* Primary icon family selection.
* Exact stroke width.
* Corner radius.
* Filled-state visual treatment.
* Platform-specific substitutions.
* Motion timing for state changes.

---

# Decision Framework

Before introducing an icon, ask:

1. Does this reduce cognitive effort?

2. Would text alone be clearer?

3. Is this icon universally understood?

4. Does it compete with the teaching?

5. Is it accessible?

6. Can an existing icon solve this instead?

7. Will users still understand the interface without it?

If the answer to these questions is unclear, the icon probably does not belong.

---

# Design Implications

This iconography system means:

* Home may use icons for orientation.
* Library may use icons to improve discoverability.
* Verse should contain almost no icons.
* Saar should remain completely typographic.
* Journal should rely primarily on language rather than symbols.
* Navigation should remain visually recognizable without becoming dominant.
* Icons should quietly disappear as users move deeper into reflection.

---

# Engineering Implications

Implementation should:

* expose icons through a shared design system,
* maintain consistent sizing,
* preserve accessibility metadata,
* support platform adaptations,
* avoid hard-coded icon assets,
* and centralize icon management.

Future icon replacements should require minimal implementation changes.

---

# Relationship to Other Documents

This document defines iconography.

Related documents define:

* `01_DESIGN_DNA.md` — overall design philosophy.
* `02_COLOR_SYSTEM.md` — visual emphasis.
* `03_LAYOUT_SYSTEM.md` — structural organization.
* `04_SPACING_SYSTEM.md` — spatial rhythm.
* `05_TYPOGRAPHY.md` — textual communication.
* `06_MOTION_SYSTEM.md` — motion and interaction.
* Component specifications — exact icon usage within individual components.

---

# North Star

Icons should quietly disappear behind understanding.

If users remember the teaching and effortlessly navigate the product without consciously noticing the symbols that guided them, the iconography system has succeeded.
