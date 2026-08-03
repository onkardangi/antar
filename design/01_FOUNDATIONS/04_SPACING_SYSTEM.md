# SPACING SYSTEM

**Version:** 1.0
**Status:** Approved for Design Exploration
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

This document defines how Antar uses space to create clarity, rhythm, comfort, and meaning.

Spacing determines:

* the distance between related elements,
* the separation between distinct ideas,
* the pace at which content is experienced,
* and the amount of breathing room available for reading and reflection.

Layout determines where information belongs.

Spacing determines how that structure feels.

---

# Why This Exists

Inconsistent spacing makes an interface feel accidental.

Overly compact spacing creates cognitive pressure.

Excessive spacing can weaken relationships, hide hierarchy, and make navigation inefficient.

Antar requires a spacing system that supports several different activities:

* quickly beginning a session,
* browsing chapters,
* reading scripture slowly,
* exploring deeper understanding,
* writing personal reflections,
* and revisiting meaningful memories.

The spacing system should help each experience establish the right pace without making Antar feel like several unrelated products.

---

# Guiding Principle

> **Space should give meaning room to breathe.**

Whitespace is not leftover space.

It is an active part of the reading and reflection experience.

Every spacing decision should support comprehension, emotional pacing, or interaction clarity.

---

# Spacing Philosophy

Antar uses space deliberately.

Distance communicates relationships.

Rhythm guides attention.

Breathing room supports reflection.

Spacing should never be added merely to make a screen appear elegant. It must help users understand which elements belong together, when one idea has ended, and where the next meaningful moment begins.

The product should feel open without feeling empty.

It should feel calm without becoming inefficient.

---

# Foundational Decisions

## Four-Point Base Grid

Antar uses a 4-point base grid.

All standard spacing values should be divisible by four.

This supports:

* precise mobile layouts,
* accessible control sizing,
* Dynamic Type,
* platform-specific adjustments,
* and consistent visual rhythm.

Most structural spacing should use multiples of eight.

Four-point increments should primarily support smaller internal adjustments and optical alignment.

---

## Semantic Tokens

Spacing should be selected according to meaning rather than arbitrary numeric preference.

Designers and engineers should think in terms such as:

* tightly related,
* related,
* separated,
* section boundary,
* experience boundary,

rather than choosing raw values independently.

Exact token values will be finalized in Figma Variables and implementation tokens.

---

## Tokens Are Defaults, Not Inflexible Laws

Spacing tokens create consistency.

They should be used by default.

Exceptions are permitted when required by:

* accessibility,
* native platform behavior,
* optical alignment,
* internationalization,
* unusually long content,
* or a documented experience need.

Exceptions should be intentional and uncommon.

They should never emerge from one-off visual tweaking without explanation.

---

# Core Principles

## 1. Proximity Communicates Relationship

Elements placed close together are interpreted as belonging together.

Elements placed farther apart are interpreted as separate ideas.

Spacing should communicate relationships before borders, background colors, or containers are introduced.

---

## 2. Sections Need Breathing Room

Major ideas should have enough separation to be experienced independently.

A verse, its translation, its explanation, its reflection, and its Saar should not visually collapse into one block.

Each deserves a distinct moment.

---

## 3. Reading Requires More Space Than Browsing

Browsing experiences can support moderate information density.

Reading experiences require greater separation, more stable rhythm, and fewer competing elements.

The spacing system should adapt to the task instead of applying one density everywhere.

---

## 4. Remove Before Compressing

When an interface feels crowded, remove unnecessary content before reducing spacing.

Do not preserve feature density by sacrificing:

* readability,
* touch-target comfort,
* section clarity,
* or emotional calm.

---

## 5. Space Creates Pace

Short distances create faster movement.

Larger distances encourage pause and contemplation.

Spacing should intentionally influence how quickly users move through each experience.

---

## 6. Consistency Builds Trust

Repeated relationships should use repeated spacing.

Similar components should not feel subtly different without a meaningful reason.

Predictable rhythm reduces the effort required to understand the interface.

---

## 7. Accessibility Overrides Visual Compactness

Spacing must remain resilient when:

* text becomes larger,
* content wraps,
* labels expand after translation,
* screen zoom is enabled,
* or assistive technologies change interaction behavior.

Content must be allowed to grow.

Fixed-height compositions should be avoided.

---

# Experience Density Modes

Antar uses three primary spacing modes.

These modes establish the general tempo of an experience. They do not replace component-level tokens.

---

## Browse Mode

Used when users are scanning, comparing, or discovering.

Examples:

* Library
* Search
* Saved verses
* Chapter verse lists
* Settings

Browse Mode should feel:

* organized,
* efficient,
* calm,
* and easy to scan.

It may use moderately compact spacing, but must never feel crowded.

Related information should remain tightly grouped so lists can be understood quickly.

---

## Read Mode

Used when users are spending focused time with scripture or supporting content.

Examples:

* Chapter introduction
* Verse
* Commentary
* Saar
* Long-form guidance

Read Mode should feel:

* spacious,
* focused,
* steady,
* and contemplative.

It uses the greatest separation between major sections.

Controls should remain visually detached from the reading body unless they directly support the current content.

---

## Reflect Mode

Used when users are noticing, writing, or revisiting personal meaning.

Examples:

* Journal
* Reflection invitations
* Journey memories
* Letters to Yourself

Reflect Mode should feel:

* personal,
* safe,
* open,
* and intimate.

It should provide enough room for thought without presenting an intimidatingly empty canvas.

Prompts, writing areas, and supporting actions should remain gently connected.

---

# Spacing Scale

The final numeric assignments should be implemented as tokens.

The recommended conceptual scale is:

| Token        | Intended Relationship                    |
| ------------ | ---------------------------------------- |
| `space-none` | No separation                            |
| `space-2xs`  | Optical or micro adjustment              |
| `space-xs`   | Very tightly related elements            |
| `space-sm`   | Related elements within a component      |
| `space-md`   | Standard component separation            |
| `space-lg`   | Distinct groups within a section         |
| `space-xl`   | Section boundary                         |
| `space-2xl`  | Major experience transition              |
| `space-3xl`  | Deliberate pause or focal breathing room |

The scale should grow predictably.

The initial implementation may use values such as:

| Token        | Initial Value |
| ------------ | ------------: |
| `space-none` |             0 |
| `space-2xs`  |             4 |
| `space-xs`   |             8 |
| `space-sm`   |            12 |
| `space-md`   |            16 |
| `space-lg`   |            24 |
| `space-xl`   |            32 |
| `space-2xl`  |            48 |
| `space-3xl`  |            64 |

These values are design hypotheses until validated in Figma and on physical devices.

Token names and relationships are more important than preserving any individual number.

---

# Vertical Rhythm

Vertical rhythm controls the pace of a screen.

The same type of transition should generally use the same spacing relationship.

Examples:

* label to supporting value,
* heading to introductory paragraph,
* content block to related action,
* section to section,
* major experience stage to the next stage.

Vertical rhythm should feel deliberate rather than mathematically repetitive.

Not every gap needs to be identical.

The relationship between gaps should communicate hierarchy and pacing.

---

# Reading Rhythm

Reading experiences require their own rhythm.

The Verse experience should generally progress through:

Verse

↓

Translation

↓

Pause

↓

Understanding

↓

Reflection

↓

Saar

↓

Continue

Small gaps should connect content within a stage.

Large gaps should distinguish one mental stage from another.

The transition into Saar should receive enough space to communicate that the experience is reaching its emotional conclusion.

Continue Reading should remain close enough to feel available, but far enough from Saar that it does not compete with it.

---

# Section Spacing

A section is a meaningful group of related content.

Internal section spacing should be smaller than spacing between sections.

For example:

```
Section Heading
small relationship gap
Section Description
medium relationship gap
Section Content

large section boundary

Next Section
```

If all gaps are equal, relationships become unclear.

---

# Component Spacing

Components should define:

* external spacing,
* internal padding,
* text-to-icon spacing,
* label-to-value spacing,
* and action-group spacing.

Component spacing should be owned by the component rather than manually recreated on every screen.

Parent layouts should control the distance between components.

Components should control the distance within themselves.

---

# Container Padding

Containers should provide enough internal space to prevent content from feeling compressed.

Padding should reflect the component’s purpose.

Interactive controls may use more horizontal padding to support touch comfort.

Reading containers should prioritize line length and breathing room.

Compact metadata containers may use tighter spacing.

Large padding should not be used to disguise unnecessary containers.

---

# Screen Margins

Screen margins should provide consistent framing across the product.

Margins may adapt according to:

* device width,
* safe areas,
* reading mode,
* accessibility scaling,
* and platform conventions.

Reading experiences may use narrower content widths than browsing experiences even when the physical screen is large.

Large screens should gain comfortable margins rather than automatically displaying more content.

---

# Safe Areas

Spacing must respect:

* device notches,
* status areas,
* navigation indicators,
* platform bars,
* and system gestures.

Safe-area spacing should be handled systematically rather than independently on each screen.

Content should never appear visually trapped against system boundaries.

---

# Touch Spacing

Interactive controls require sufficient separation to prevent accidental activation.

Touch targets may extend beyond visible control bounds where appropriate.

Closely related actions must still remain distinguishable by:

* position,
* labels,
* visual treatment,
* and screen-reader descriptions.

Visual calm must not reduce interaction safety.

---

# Edge Spacing

Content should not feel pressed against the edge of the display.

Edge spacing provides:

* visual stability,
* reading comfort,
* gesture safety,
* and predictable alignment.

Intentional full-bleed content should be rare and must not compromise text readability.

---

# Spacing Rules

## Rule 1

Use spacing tokens instead of arbitrary values.

---

## Rule 2

Use smaller spacing within a relationship and larger spacing between ideas.

---

## Rule 3

Read Mode receives more breathing room than Browse Mode.

---

## Rule 4

Reflection should feel open but never abandoned.

---

## Rule 5

Remove content before compressing the interface.

---

## Rule 6

Components own internal spacing.

Layouts own spacing between components.

---

## Rule 7

Do not rely on empty space alone to preserve accessibility context.

---

## Rule 8

Spacing must support text wrapping and Dynamic Type.

---

## Rule 9

Major emotional transitions may use deliberate additional space.

---

## Rule 10

Spacing exceptions must have a clear reason.

---

# Anti-Patterns

Avoid:

* arbitrary spacing values,
* equal spacing between every element,
* reducing margins to fit more features,
* using blank space without structural purpose,
* oversized gaps that disconnect related content,
* cramped text inside visually large cards,
* fixed-height containers around dynamic text,
* excessive use of dividers where spacing would communicate grouping,
* inconsistent padding across equivalent components,
* and platform-specific spacing differences without a reason.

---

# Confirmed Principles

The following are strong foundations:

* Antar uses a 4-point base grid.
* Structural spacing generally favors multiples of eight.
* Spacing communicates relationships.
* Browse, Read, and Reflect require different density modes.
* Components own their internal spacing.
* Accessibility takes priority over compactness.
* Removing content is preferable to compressing it.
* Tokens are defaults with documented exceptions.

---

# Design Hypotheses

The following must be validated in Figma and on real devices:

* The initial numeric token values.
* The ideal screen margin for small phones.
* The ideal reading width on tablets.
* The amount of space preceding Saar.
* The spacing between Saar and Continue Reading.
* Whether Journey requires denser grouping for long histories.
* Whether Journal needs different spacing for short and long entries.
* How spacing should adapt at the largest accessibility text sizes.

These should not be treated as final until tested.

---

# Decision Framework

Before approving a spacing decision, ask:

1. What relationship is this distance communicating?

2. Does the spacing match the experience mode?

3. Is the content related or conceptually separate?

4. Does this gap improve reading rhythm?

5. Would a divider or container become unnecessary with better spacing?

6. Does the layout remain usable when text wraps?

7. Is the spacing value drawn from the shared token system?

8. Is an exception genuinely required?

---

# Design Implications

This spacing system means:

* Verse should use generous separation between mental stages.
* Library lists may use tighter internal grouping.
* Journal prompts should remain connected to the writing surface.
* Journey memories should feel distinct without becoming a fragmented card grid.
* Saar should receive deliberate breathing room.
* Navigation should remain comfortably separated from content.
* Empty states should feel welcoming rather than vacant.
* Cards should rely on internal spacing and hierarchy rather than decoration alone.

---

# Engineering Implications

Implementation should:

* expose spacing tokens through the shared theme,
* avoid scattered raw numeric spacing values,
* support responsive margins,
* allow content height to grow naturally,
* separate internal component padding from external layout gaps,
* support safe-area insets,
* test layouts at large text sizes,
* and document justified token exceptions.

Spacing tokens should be shared across iOS and Android while allowing platform-specific safe-area behavior.

---

# Relationship to Other Documents

This document defines distance and rhythm.

Related documents define:

* `03_LAYOUT_SYSTEM.md` — structure and attention flow.
* `05_TYPOGRAPHY.md` — textual pace, hierarchy, and readability.
* `06_MOTION_SYSTEM.md` — temporal rhythm and transitions.
* `09_ACCESSIBILITY.md` — detailed scaling and touch requirements.
* Component specifications — exact internal spacing assignments.
* Experience specifications — screen-level application of density modes.

---

# North Star

Space should never exist only to make Antar look refined.

It should help readers understand relationships, move at the right pace, and feel that every meaningful idea has enough room to be fully experienced.
