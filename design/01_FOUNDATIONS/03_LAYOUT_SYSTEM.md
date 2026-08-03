# LAYOUT SYSTEM

**Version:** 1.0
**Status:** Approved for Design Exploration
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

This document defines the foundational layout principles used throughout Antar.

Layout determines:

* where information appears,
* how attention moves through a screen,
* how relationships between content are communicated,
* and how users understand what to do next.

Layout is distinct from spacing.

Layout defines structure and attention flow.

Spacing defines the distance and rhythm within that structure.

---

# Why This Exists

Antar contains multiple types of experiences:

* browsing,
* reading,
* understanding,
* reflection,
* and remembering.

Without shared layout principles, these experiences could feel like separate products.

A consistent layout system ensures that every part of Antar feels familiar while still supporting the needs of each experience.

A successful layout should quietly answer:

> Where should I look next?

The user should not need to consciously think about the interface.

---

# Layout Philosophy

Antar organizes information around meaning rather than feature density.

The interface should guide attention through a clear and intentional sequence.

Layouts should support understanding, presence, and reflection rather than maximizing the quantity of information visible at one time.

The default experience should feel closer to moving through a thoughtfully composed page than navigating a software dashboard.

---

# Core Principles

## 1. Design for Attention Flow

Every screen should guide attention through an intentional sequence.

The user should understand:

* what matters most,
* what supports it,
* and what comes next.

Visual weight, placement, spacing, and typography should work together to create this flow.

---

## 2. One Primary Intention

Every screen should support one primary user intention.

Examples:

* Home helps the user begin.
* Library helps the user discover.
* Chapter helps the user prepare.
* Verse helps the user understand.
* Journal helps the user reflect.
* Journey helps the user remember.

A screen may contain multiple actions, but those actions should support the same primary intention.

---

## 3. Content Leads the Structure

The structure should emerge from the content and the user’s task.

Layouts should never force meaningful content into patterns simply because those patterns are visually fashionable or technically convenient.

When layout and content compete, content wins.

---

## 4. Reading Experiences Favor a Single Narrative Flow

Reading and reflection experiences should default to a clear top-to-bottom progression.

This supports:

* predictable attention,
* long-form reading,
* accessibility,
* Dynamic Type,
* and progressive understanding.

This principle applies primarily to reading-focused experiences.

It does not prohibit other structures when browsing, settings, larger devices, or accessibility needs justify them.

---

## 5. Progressive Disclosure

The interface should present only the information needed for the current moment.

Additional depth should appear when the user chooses to explore it.

Progressive disclosure protects the user from unnecessary cognitive load while allowing the product to support deeper study.

---

## 6. Preserve Context

Users should understand where they are and how they arrived there.

Navigation, headings, progress indicators, and transitions should preserve orientation without competing with the content.

Moving between systems should feel continuous rather than abrupt.

---

## 7. Relationships Before Decoration

Layout should communicate which pieces of information belong together.

Elements that are conceptually related should remain visually connected.

Distinct ideas should have enough separation to feel independent.

Borders, cards, containers, and backgrounds should not replace clear structural relationships.

---

## 8. Remove Before Compressing

When a screen feels crowded, the first response should be subtraction.

Do not solve excessive content by:

* shrinking text,
* reducing touch targets,
* collapsing essential breathing room,
* or increasing density without justification.

Simplify the experience before compressing it.

---

# Layout Decisions

## Vertical Progression

Antar generally favors vertical progression because it supports reading, reflection, and progressive depth.

Vertical progression should feel intentional.

Scrolling should reveal the next meaningful part of the experience rather than expose an endless stream of unrelated content.

---

## Visual Focal Point

Each screen should have a clear initial focal point.

Examples:

* Home: the best next step.
* Library: continue reading or chapter discovery.
* Chapter: chapter intent.
* Verse: the scripture.
* Journal: the reflection invitation.
* Journey: the user’s meaningful memories.

Supporting content should remain visually secondary.

---

## Navigation Placement

Navigation should remain predictable and reachable.

Primary navigation should help users move between Antar’s major systems.

Local navigation should support movement within the current experience.

Navigation controls should remain visually quieter than the content they serve.

---

## Scrolling

Scrolling is used to progress through meaningful content.

It should not be used to create:

* infinite feeds,
* arbitrary discovery loops,
* hidden navigation,
* or excessive content accumulation.

For the Verse experience, scrolling represents progression through:

Read → Understand → Reflect → Saar → Continue

---

## Horizontal Interaction

Horizontal gestures should not carry essential navigation or reading content unless the interaction is:

* discoverable,
* accessible,
* reversible,
* and clearly superior to vertical navigation.

Primary reading experiences should not depend on hidden horizontal gestures.

---

## Containers

Containers should be introduced only when they clarify:

* hierarchy,
* grouping,
* interaction,
* or state.

Not every piece of content requires a card.

Excessive containers fragment the experience and increase visual noise.

---

## Fixed and Floating Elements

Fixed or floating controls should be used sparingly.

They should never:

* cover reading content,
* compete with scripture,
* create persistent urgency,
* or reduce usable reading space.

A persistent element must provide clear and continuous value.

---

# Layout Density

Density should respond to the user’s task.

## Browsing Density

Browsing experiences may show more information because users are comparing and discovering.

Examples:

* Library
* Search
* Saved content

Browsing should still remain calm and readable.

---

## Reading Density

Reading experiences should use lower density and greater focus.

Examples:

* Chapter introductions
* Verse
* Commentary

Reading layouts should prioritize text comfort and uninterrupted flow.

---

## Reflection Density

Reflection experiences should feel personal and uncluttered.

Examples:

* Journal
* Reflection invitations

The writing surface should feel open without appearing unfinished or intimidating.

---

## Memory Density

Journey may present multiple meaningful moments, but should avoid becoming an analytics dashboard.

The layout should favor narrative and recollection over compact data presentation.

---

# Responsive Philosophy

Antar should preserve the same conceptual hierarchy across device sizes.

The experience may adapt through:

* wider reading margins,
* larger content areas,
* supplemental panels,
* or more comfortable navigation placement.

The structure may adapt, but the attention flow should remain recognizable.

Large screens should not be filled simply because space is available.

---

# Accessibility

Layouts must remain usable with:

* Dynamic Type,
* screen readers,
* zoom,
* high contrast,
* reduced motion,
* large touch targets,
* and alternate input methods.

Accessibility requirements may change the visual arrangement.

The intended reading order and meaning must remain intact.

Visual order and screen-reader order should agree.

---

# Layout Rules

## Rule 1

Every screen has one primary intention.

---

## Rule 2

The initial focal point should be immediately recognizable.

---

## Rule 3

Reading experiences default to a clear vertical narrative.

---

## Rule 4

Supporting actions should not compete with the primary content.

---

## Rule 5

Related content remains visually connected.

---

## Rule 6

Complexity should appear progressively.

---

## Rule 7

Crowded layouts should be simplified before they are compressed.

---

## Rule 8

Scrolling should reveal meaningful progression, not endless content.

---

## Rule 9

Navigation should preserve orientation without dominating attention.

---

## Rule 10

Layout must remain resilient under accessibility scaling.

---

# Anti-Patterns

Avoid:

* dashboard layouts for reflective experiences,
* multiple equal-weight focal points,
* excessive card-based composition,
* nested vertical scrolling,
* hidden essential actions,
* oversized floating controls,
* unexplained horizontal navigation,
* content placed above scripture that distracts from reading,
* dense grids for long-form content,
* and layouts designed primarily to look impressive in screenshots.

---

# Confirmed Principles

The following decisions are strong foundations and are unlikely to change:

* One primary intention per screen.
* Content leads the structure.
* Reading experiences favor a single narrative flow.
* Complexity should unfold progressively.
* Layout should preserve context.
* Remove before compressing.
* Accessibility may reshape the layout but must preserve meaning.

---

# Design Hypotheses

The following decisions should be validated during Figma exploration and usability testing:

* How much content should appear before the first scroll.
* Whether the Chapter experience needs collapsed sections.
* Whether Journey should use a continuous timeline or grouped periods.
* Whether secondary Verse actions remain inline or use a bottom sheet.
* How large-screen layouts should introduce supplementary content.
* Which controls, if any, should remain persistent while reading.

These hypotheses should not be treated as permanent rules until validated.

---

# Decision Framework

Before approving a layout, ask:

1. What is the user’s primary intention?

2. What should they notice first?

3. Is the next meaningful step visually clear?

4. Are related ideas grouped naturally?

5. Is anything competing unnecessarily for attention?

6. Can anything be removed?

7. Does the layout remain usable with large text?

8. Does scrolling represent meaningful progression?

If the answers are unclear, the layout requires further refinement.

---

# Design Implications

This layout system means:

* Verse should follow one uninterrupted narrative flow.
* Home should guide users toward a meaningful next step rather than summarize the entire application.
* Library may use greater density than Verse while remaining easy to scan.
* Journal should avoid intimidating empty canvases.
* Journey should favor narrative memory over statistics.
* Cards should be used intentionally rather than as the default container.
* Essential reading actions should remain accessible without crowding the text.
* Tablet layouts should add comfort and context rather than unnecessary content.

---

# Engineering Implications

Implementation should:

* support flexible vertical composition,
* avoid deeply nested scrolling containers,
* preserve semantic reading order,
* allow components to grow with Dynamic Type,
* avoid hard-coded content heights,
* separate screen structure from device-specific measurements,
* support safe areas consistently,
* and keep layout behavior predictable across iOS and Android.

Exact dimensions, breakpoints, and spacing values belong in implementation-focused design tokens and component specifications.

---

# Relationship to Other Documents

This document defines structure.

Related documents define:

* `04_SPACING_SYSTEM.md` — distance, rhythm, and breathing room.
* `05_TYPOGRAPHY.md` — textual hierarchy, readability, and pacing.
* `06_MOTION_SYSTEM.md` — transitions and spatial continuity.
* `09_ACCESSIBILITY.md` — detailed accessible layout requirements.
* Experience specifications — screen-specific applications of these foundations.

Experience-specific layouts should not be added to this foundational document.

---

# North Star

A user should never need to consciously decode the interface.

Layout should quietly guide attention from one meaningful moment to the next while allowing the content, not the structure, to remain in memory.
