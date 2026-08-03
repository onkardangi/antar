# COMPONENT INVENTORY

**Version:** 1.0
**Status:** Draft for Component Review
**Owner:** Product & Design
**Last Updated:** August 2026

---

# Decision Status

Component questions use the following labels:

* **Decided** — supported by approved product and design principles.
* **Prototype Validation** — requires layout or interaction testing.
* **Product Review** — requires a V1 scope or navigation decision.
* **Technical Design** — depends on data ownership, architecture, or implementation.
* **Deferred** — intentionally excluded from the current release.

An unresolved question should always have an owner and a resolution stage. Questions should not remain open without a defined path to closure.


# Purpose

This document identifies the reusable interface components that emerge from Antar’s approved Core Experiences.

It exists to answer:

> **What reusable building blocks does Antar actually need?**

The inventory is derived from:

* Home
* Library
* Verse
* Journal
* Journey
* Guidance

It should not become a generic list of components copied from an existing design system.

Every component must be justified by a real product experience.

---

# Inventory Principles

## Experiences Come First

Components exist to support approved experiences.

A component should not be created simply because other applications or design systems contain one.

---

## Reuse Must Be Real

Two elements that look similar are not automatically the same component.

A reusable component should share meaningful behavior, structure, responsibility, or interaction—not merely visual appearance.

---

## Responsibility Before Appearance

Each component should have one clear responsibility.

A component should not accumulate unrelated product behavior simply because several features appear in the same visual container.

---

## Compose Before Expanding

Complex experiences should be composed from smaller responsibilities.

## Compose Before Expanding

Complex experiences should be composed from smaller responsibilities.

Before creating a new component, first determine whether the experience can be assembled from existing components.

When a reusable abstraction emerges, responsibilities should move into that abstraction rather than remaining duplicated across multiple components.

As reusable components are introduced, parent components should become simpler—not more complex.

For example:

- Verse List organizes Verse Items.
- Verse Item composes Verse Reference.
- Search Result composes Chapter Item or Verse Item.

Avoid creating large components that own an entire screen or system.

## Adapt Before Rebuilding

Some components exist to adapt existing components into a new context.

These adapter components preserve the responsibilities and visual language of the components they compose while adding only the context required for the new experience.

Adapters may provide:

- highlighting,
- contextual metadata,
- navigation,
- contextual actions.

They should never duplicate or replace the responsibilities of the components they compose.

Examples:

- Search Result adapts Chapter Item and Verse Item.
- Teaching Recommendation adapts Verse Item.
- Continue Reading adapts Chapter Item or Verse Item.
- Journey Memory adapts existing reflection content.
---

## Semantic Before Generic

Prefer names that communicate product purpose.

For example:

* `Reflection Invitation`
* `Continue Reading`
* `Saar`

These are more meaningful than vague names such as:

* `Content Card`
* `Action Tile`
* `Info Box`

Generic primitives may still exist beneath semantic components.

---

## Accessibility From the Beginning

Every component must eventually define:

* semantic role,
* reading order,
* accessible label,
* interaction behavior,
* touch target,
* Dynamic Type behavior,
* focus behavior,
* and Reduced Motion behavior where relevant.

Accessibility is part of the component definition.

---

# Component Classification

Antar’s component system is divided into five families:

1. Core Reading
2. Reflection and Meaning
3. Discovery and Orientation
4. Journey and Memory
5. Interface Infrastructure

These groups describe responsibility rather than visual style.

---

# 1. Core Reading Components

These components support direct engagement with scripture.

They are the highest-priority components in Antar.

---

## Verse Block

### Purpose

Present the original Sanskrit verse clearly and respectfully.

### Used In

* Verse

### Responsibility

* Render Sanskrit scripture.
* Preserve verse structure.
* Support accessible reading.
* Support text scaling.
* Support selection where appropriate.

### Not Responsible For

* Translation
* Commentary
* AI explanation
* Bookmark persistence
* Reading progress
* Navigation

### Priority

**Tier 1 — Essential**

### V1

Yes

---

## Transliteration Block

### Purpose

Help readers pronounce or follow the Sanskrit verse using Latin script.

### Used In

* Verse

### Responsibility

* Render transliteration accurately.
* Support diacritics.
* Respect the user’s visibility preference.
* Remain visually secondary to scripture.

### Not Responsible For

* Translation
* Pronunciation audio
* Language preference management

### Priority

**Tier 2 — Important**

### V1

Yes, if trusted transliteration content is available.

---

## Translation Block

### Purpose

Present the active English or Hindi translation of a verse.

### Used In

* Verse
* Guidance teaching previews
* Search results, in abbreviated form

### Responsibility

* Render one primary translation.
* Support an optional secondary translation.
* identify translation language and source where required.
* Preserve long-form readability.

### Not Responsible For

* Commentary
* AI-generated meaning
* Language selection settings
* Scripture text

### Priority

**Tier 1 — Essential**

### V1

Yes

---

## Understanding Section

### Purpose

Introduce supporting explanation after the reader has encountered the verse and translation.

### Used In

* Verse
* Guidance after scripture selection

### Responsibility

* Contain approved explanatory content.
* Support progressive disclosure.
* Preserve the distinction between trusted commentary and AI assistance.
* Remain visually secondary to scripture.

### Not Responsible For

* Displaying the original verse
* Writing reflections
* AI conversation state
* Related-verse search

### Priority

**Tier 1 — Essential**

### V1

Yes

### Note

This may be an experience-level composition rather than a single implementation component. Component review must determine whether it should be decomposed into:

* Simple Explanation
* Traditional Commentary
* Context
* AI Entry

---

## Reading Progress Indicator

### Purpose

Provide quiet orientation within a chapter or reading sequence.

### Used In

* Verse
* Chapter
* Continue Reading

### Responsibility

* Communicate the reader’s current location.
* Preserve orientation.
* Avoid pressure or achievement framing.
* Remain visually secondary.

### Not Responsible For

* Calculating progress
* Saving progress
* Celebrating completion
* Streaks or goals

### Priority

**Tier 2 — Important**

### V1

Yes

---

## Continue Reading

### Purpose

Invite the reader to move to the next meaningful reading step.

### Used In

* Home
* Library
* Verse
* Chapter
* Journey

### Responsibility

* Communicate the next reading destination.
* Preserve continuity.
* Adapt its copy to context.
* Feel invitational rather than urgent.

### Not Responsible For

* Selecting recommendations
* Calculating reading state
* Managing navigation history
* Displaying unrelated discovery content

### Priority

**Tier 1 — Essential**

### V1

Yes

### Reuse Observation

This is the clearest cross-experience component in Antar.

Its presentation may vary by context, but its responsibility remains stable.

Potential variants:

* Compact inline action
* Home continuation card
* Library continuation card
* End-of-verse invitation

---

## Verse Reference

### Purpose

Identify a verse through chapter and verse information.

### Used In

* Verse
* Journal
* Journey
* Guidance
* Search
* Saved content

### Responsibility

* Display canonical reference information.
* Remain discoverable but visually quiet.
* Provide a consistent link back to the verse when interactive.

### Not Responsible For

* Rendering verse content
* Navigation implementation
* Bookmark state

### Priority

**Tier 1 — Essential**

### V1

Yes

---

# 2. Reflection and Meaning Components

These components support the movement from reading to personal understanding.

---

## Reflection Invitation

### Purpose

Invite the reader to notice what a teaching awakened within them.

### Used In

* Verse
* Journal
* Guidance
* Journey revisit moments

### Responsibility

* Present one gentle reflection question.
* Adapt to the source context.
* Remain optional.
* Avoid instructional or judgmental language.

### Not Responsible For

* Capturing long-form writing
* Selecting AI-generated conclusions
* Evaluating reflection quality
* Saving journal entries

### Priority

**Tier 1 — Essential**

### V1

Yes

### Potential Variants

* Quiet prompt
* One-sentence prompt
* Guided prompt
* Action reflection
* Revisit prompt

---

## Journal Editor

### Purpose

Provide a private writing surface for personal reflection.

### Used In

* Journal
* Verse inline reflection, if supported
* Guidance reflection flow

### Responsibility

* Capture plain-text reflection.
* Autosave drafts.
* Support offline writing.
* Preserve accessibility and keyboard comfort.
* Communicate save state quietly.

### Not Responsible For

* Rich document formatting
* AI-authored text
* Public sharing
* Journey pattern recognition
* Verse content rendering

### Priority

**Tier 1 — Essential**

### V1

Yes

---

## Save Status

### Purpose

Reassure the reader that personal writing has been preserved.

### Used In

* Journal Editor
* Future voice reflection

### Responsibility

* Communicate saving, saved, offline, and sync-pending states.
* Remain quiet and non-disruptive.
* Provide useful recovery information when saving fails.

### Not Responsible For

* Performing persistence
* Displaying general application alerts
* Encouraging completion

### Priority

**Tier 2 — Important**

### V1

Yes

---

## Saar

### Purpose

Present the single essence a reader may carry forward from a verse.

### Used In

* Verse
* Journey
* Home, only if surfaced intentionally
* Saved Saar collection

### Responsibility

* Present exactly one curated essence.
* Create a clear emotional conclusion.
* Remain typographic and distraction-free.
* Support revisiting and saving where appropriate.

### Not Responsible For

* Summarizing all commentary
* Generating multiple takeaways
* Replacing the verse
* Displaying unrelated actions
* AI interpretation

### Priority

**Tier 1 — Essential**

### V1

Yes

### Sacred Constraint

One verse has one Saar.

Saar should never become:

* a bullet list,
* a paragraph summary,
* a promotional card,
* or a collection of AI suggestions.

---

## Reflection Revisit

### Purpose

Reconnect the reader with a previous reflection related to the current teaching.

### Used In

* Verse
* Journal
* Journey

### Responsibility

* Surface relevant prior reflection.
* Communicate when it was written.
* Invite further reflection without pressure.
* Preserve privacy.

### Not Responsible For

* Deciding what the reflection means
* Psychological interpretation
* Automatically editing old entries
* Ranking reflections

### Priority

**Tier 3 — Later V1 or V2**

### V1

Optional

---

# 3. Discovery and Orientation Components

These components help readers begin, navigate, and discover content confidently.

---

## Greeting

### Purpose

Welcome the reader and establish Antar’s emotional tone.

### Used In

* Home
* First-time experiences
* Returning-reader states

### Responsibility

* Provide warm, concise context.
* Adapt carefully to time or return state.
* Avoid guilt, pressure, or excessive familiarity.

### Not Responsible For

* Notifications
* Personalized psychological statements
* Progress statistics
* Marketing messages

### Priority

**Tier 1 — Essential**

### V1

Yes

---

## Today’s Invitation

### Classification

Composition, not a reusable component. Documented in `99_COMPOSITIONS/TODAYS_INVITATION.md`.

### Purpose

Present the next meaningful step on Home.

### Used In

* Home

### Responsibility

* Present a single, already-selected destination.
* Support continuity, beginning, resumed reflection, or curated teaching as contextual states.
* Avoid randomness and algorithmic pressure.

### Not Responsible For

* Selecting its own destination
* Calculating reading progress
* Ranking teachings
* General recommendation feeds
* AI-first suggestions
* Multiple competing options
* Trending content

### Priority

**Tier 2 — Important**

### V1

Yes

---

## Chapter Item

### Purpose

Help readers understand and select a chapter.

### Used In

* Library
* Search
* Future thematic discovery

### Responsibility

* Display chapter number.
* Display chapter name.
* Communicate chapter intent or concise theme.
* Show reading state where appropriate.
* Preserve canonical ordering.

### Not Responsible For

* Rendering the full chapter introduction
* Reordering chapters
* AI recommendations
* Calculating progress

### Priority

**Tier 1 — Essential**

### V1

Yes

### Naming Note

Use `Chapter Item` until Figma determines whether the visual treatment is genuinely a card.

Do not assume every chapter requires a bordered container.

---

## Chapter Intent

### Purpose

Provide a concise invitation into the chapter’s central teaching.

### Used In

* Chapter
* Library, abbreviated
* Guidance, when recommending a chapter

### Responsibility

* Present one approved chapter-level idea.
* Inspire curiosity without replacing reading.
* Remain distinct from Saar.

### Not Responsible For

* Verse summary
* AI generation at runtime
* Full chapter commentary

### Priority

**Tier 2 — Important**

### V1

Yes

---

## Search Field

### Purpose

Allow readers to intentionally locate scripture and related content.

### Used In

* Library
* Search
* Saved content
* Journal archive, future

### Responsibility

* Capture search input.
* Communicate state clearly.
* Support keyboard and screen-reader interaction.
* Provide predictable clearing and submission behavior.

### Not Responsible For

* Search ranking
* Search result rendering
* Query interpretation
* AI guidance

### Priority

**Tier 2 — Important**

### V1

Yes

---

## Search Result

### Purpose

Present a relevant chapter, verse, theme, or saved item.

### Used In

* Search
* Library search

### Responsibility

* Identify result type.
* Show sufficient context.
* Link clearly to the destination.
* Avoid overstating relevance.

### Not Responsible For

* Search ranking
* AI explanation
* Full verse rendering

### Priority

**Tier 2 — Important**

### V1

Depends on Search scope.

---

## Theme Chip

### Purpose

Represent a life theme or teaching topic in a compact form.

### Used In

* Library
* Guidance
* Journey
* Search

### Responsibility

* Display one approved theme.
* Support filtering or exploration when interactive.
* Remain readable and accessible.

### Not Responsible For

* Inferring user identity
* Emotional diagnosis
* Ranking themes
* Acting as decorative metadata

### Priority

**Tier 3 — Supporting**

### V1

Only if Theme Exploration is included.

---

# 4. Journey and Memory Components

These components support long-term reflection without turning growth into measurement.

---

## Growth Story

### Purpose

Introduce a human-readable view of meaningful patterns across the reader’s journey.

### Used In

* Journey

### Responsibility

* Present evidence-based observations.
* Connect meaningful moments.
* Maintain humility and uncertainty.
* Point toward continued reflection.

### Not Responsible For

* Defining who the reader is
* Scoring growth
* Psychological profiling
* Generating authoritative conclusions

### Priority

**Tier 2 — Important**

### V1

Potentially limited in initial release.

### Note

This may be an experience-level composition rather than a reusable component.

Validate before formalizing it as a component.

---

## Journey Memory

### Purpose

Surface one meaningful past moment.

### Used In

* Journey
* Home, future
* Verse revisit

### Responsibility

* Present a reflection, Saar, chapter moment, or meaningful return.
* Preserve source context.
* Communicate time gently.
* Support revisiting the original source.

### Not Responsible For

* Interpreting the memory
* Ranking memories
* Creating achievements
* Public sharing

### Priority

**Tier 2 — Important**

### V1

Yes, if Journey is in V1.

---

## Journey Theme

### Purpose

Show a recurring idea the reader has explored over time.

### Used In

* Journey

### Responsibility

* Present theme evidence.
* Communicate recency or recurrence without scoring.
* Invite exploration.

### Not Responsible For

* Diagnosing the reader
* Claiming personal growth
* Gamifying recurrence
* Producing personality labels

### Priority

**Tier 3 — Supporting**

### V1

Potentially limited.

---

## Journey Timeline Entry

### Purpose

Represent a meaningful moment within the reader’s long-term journey.

### Used In

* Journey

### Responsibility

* Display one curated event.
* Preserve chronology where helpful.
* Support different memory types.
* Avoid activity-log density.

### Not Responsible For

* Recording every interaction
* Displaying raw analytics
* Achievement celebration
* Social sharing

### Priority

**Tier 2 — Important**

### V1

Yes

---

## Quiet Recognition

### Purpose

Acknowledge a meaningful commitment or return without gamification.

### Used In

* Journey
* Home, occasionally
* Completion moments

### Responsibility

* Recognize a meaningful event.
* Use humble, encouraging language.
* Avoid urgency, badges, XP, or confetti.

### Not Responsible For

* Achievement systems
* Streaks
* Competitive milestones
* Push-notification pressure

### Priority

**Tier 3 — Supporting**

### V1

Optional

---

# 5. Guidance Components

These components connect a reader’s present situation with relevant scripture.

---

## Guidance Input

### Purpose

Allow the reader to share a life question or situation.

### Used In

* Guidance

### Responsibility

* Capture free-form input.
* Communicate privacy and purpose.
* Support accessibility and keyboard comfort.
* Avoid suggesting that the system provides professional advice.

### Not Responsible For

* Journal writing
* Diagnosing emotional state
* Search execution
* AI response generation

### Priority

**Tier 1 — Essential for Guidance**

### V1

Yes, if Guidance is in V1.

---

## Clarifying Question

### Purpose

Invite the reader to provide additional context before teachings are surfaced.

### Used In

* Guidance

### Responsibility

* Ask one concise and relevant question.
* Reduce assumptions.
* Support simple response options or free text.
* Preserve conversational continuity.

### Not Responsible For

* Conducting an endless chat
* Therapy intake
* Emotional diagnosis
* Giving advice

### Priority

**Tier 2 — Important for Guidance**

### V1

Yes

---

## Teaching Recommendation

### Purpose

Present a relevant verse or chapter as a path back to scripture.

### Used In

* Guidance
* Search, potentially
* Home, future

### Responsibility

* Identify the recommended teaching.
* Explain relevance briefly and humbly.
* Provide a clear path into Verse.
* Avoid claiming certainty.

### Not Responsible For

* Replacing scripture with an AI summary
* Giving life advice
* Ranking verses as universally correct answers
* Starting an endless conversation

### Priority

**Tier 1 — Essential for Guidance**

### V1

Yes

---

## Guidance Response

### Purpose

Provide concise context around why a teaching may be relevant.

### Used In

* Guidance

### Responsibility

* Acknowledge the reader’s question.
* Introduce relevant themes.
* Preserve humility.
* Lead toward scripture.

### Not Responsible For

* Acting as the final answer
* Diagnosing the user
* Replacing Verse
* Producing unrestricted AI chat

### Priority

**Tier 2 — Important for Guidance**

### V1

Yes

### Note

This may remain experience-specific rather than become a broadly reusable component.

---

# 6. Interface Infrastructure Components

These are generic building blocks required across experiences.

They are important, but they do not define Antar’s identity on their own.

---

## Button

### Purpose

Allow the reader to perform a clear action.

### Initial Variants

* Primary
* Secondary
* Quiet
* Destructive
* Text action

### V1

Yes

---

## Icon Button

### Purpose

Provide a familiar compact action when text would create unnecessary visual weight.

### Initial Uses

* Back
* Bookmark
* Overflow
* Close
* Clear search

### V1

Yes

---

## Top Navigation

### Purpose

Preserve orientation and provide local navigation.

### V1

Yes

---

## Bottom Navigation

### Purpose

Provide predictable access to Antar’s primary destinations.

### V1

Likely

### Open Question

The final destination set must be confirmed before documenting this component.

---

## Bottom Sheet

### Purpose

Present secondary actions or supporting detail without losing context.

### Potential Uses

* Reading preferences
* Translation selection
* Secondary Verse actions
* Filters

### V1

Likely

---

## Dialog

### Purpose

Request explicit confirmation for high-consequence actions.

### Potential Uses

* Delete journal entry
* Discard unrecoverable local data
* Sign out
* Permanent account deletion

### V1

Yes, but rare.

---

## Toast or Status Message

### Purpose

Communicate lightweight, temporary feedback.

### Potential Uses

* Saved
* Copied
* Offline
* Sync restored

### V1

Yes

### Constraint

Never interrupt reading unnecessarily.

---

## Loading Placeholder

### Purpose

Preserve layout and communicate loading without creating visual noise.

### V1

Yes

---

## Empty State

### Purpose

Explain why content is absent and provide a clear next step.

### Used In

* Journal
* Journey
* Search
* Saved content
* Offline unavailable state

### V1

Yes

---

## Error State

### Purpose

Explain failure clearly while preserving access to available content.

### V1

Yes

---

## Offline State

### Purpose

Communicate network limitations without making the product feel broken.

### V1

Yes

---

## Divider

### Purpose

Create subtle separation when spacing alone is insufficient.

### V1

Yes, but use sparingly.

---

## Metadata Text

### Purpose

Present verse references, dates, sources, status, and secondary information consistently.

### V1

Yes

---

## Chip

### Purpose

Represent a compact selectable option, filter, or theme.

### V1

Only where supported by a real experience.

---

## Toggle

### Purpose

Control a persistent binary preference.

### Potential Uses

* Transliteration visibility
* Evening appearance
* Offline download setting

### V1

Yes

---

## Selection Control

### Purpose

Choose one option from a defined set.

### Potential Uses

* Language
* Translation
* Appearance
* Reading preferences

### V1

Yes

---

# Cross-Experience Reuse Matrix

| Component               |   Home   | Library |   Verse  | Journal | Journey | Guidance |
| ----------------------- | :------: | :-----: | :------: | :-----: | :-----: | :------: |
| Greeting                |     ✓    |         |          |         |         |          |
| Continue Reading        |     ✓    |    ✓    |     ✓    |         |    ✓    |          |
| Chapter Item            |          |    ✓    |          |         |         |          |
| Search Field            |          |    ✓    |          |         |         |          |
| Verse Reference         |          |         |     ✓    |    ✓    |    ✓    |     ✓    |
| Verse Block             |          |         |     ✓    |         |         |     ✓    |
| Transliteration Block   |          |         |     ✓    |         |         |          |
| Translation Block       |          |         |     ✓    |         |         |     ✓    |
| Understanding Section   |          |         |     ✓    |         |         |     ✓    |
| Reflection Invitation   |          |         |     ✓    |    ✓    |    ✓    |     ✓    |
| Journal Editor          |          |         | Optional |    ✓    |         | Optional |
| Save Status             |          |         |          |    ✓    |         |          |
| Saar                    | Optional |         |     ✓    |         |    ✓    |          |
| Journey Memory          |  Future  |         | Optional |         |    ✓    |          |
| Journey Theme           |          |         |          |         |    ✓    |          |
| Timeline Entry          |          |         |          |         |    ✓    |          |
| Guidance Input          |          |         |          |         |         |     ✓    |
| Clarifying Question     |          |         |          |         |         |     ✓    |
| Teaching Recommendation |  Future  |         |          |         |         |     ✓    |

---

# Priority Tiers

## Tier 1 — Product-Defining

These components are necessary for Antar’s core identity and primary V1 flows.

* Verse Block
* Translation Block
* Verse Reference
* Understanding Section
* Reflection Invitation
* Journal Editor
* Saar
* Continue Reading
* Greeting
* Chapter Item
* Guidance Input
* Teaching Recommendation

---

## Tier 2 — Important Supporting Components

These improve continuity, understanding, and usability.

* Transliteration Block
* Reading Progress Indicator
* Save Status
* Chapter Intent
* Search Field
* Search Result
* Journey Memory
* Journey Timeline Entry
* Clarifying Question
* Guidance Response

---

## Tier 3 — Supporting or Later Components

These should be introduced only when a validated experience requires them.

* Reflection Revisit
* Theme Chip
* Journey Theme
* Quiet Recognition
* Growth Story as a reusable component
* Advanced reading-preference controls
* Seasonal or personalized components

---

# V1 Component Candidates

The initial V1 component system should likely include:

## Reading

* Verse Block
* Transliteration Block
* Translation Block
* Verse Reference
* Understanding Section
* Reading Progress Indicator
* Continue Reading
* Saar

## Reflection

* Reflection Invitation
* Journal Editor
* Save Status

## Discovery

* Greeting
* Chapter Item
* Chapter Intent
* Search Field
* Search Result

## Journey

* Journey Memory
* Journey Timeline Entry

## Guidance

* Guidance Input
* Clarifying Question
* Teaching Recommendation
* Guidance Response

## Infrastructure

* Button
* Icon Button
* Top Navigation
* Bottom Navigation
* Bottom Sheet
* Dialog
* Status Message
* Loading Placeholder
* Empty State
* Error State
* Offline State
* Metadata Text
* Toggle
* Selection Control

This list remains subject to prototype validation.

---

# Components That Should Not Exist

The following should not be introduced unless the product philosophy changes through an explicit decision:

* Streak Counter
* XP Indicator
* Leaderboard
* Like Button
* Comment Thread
* Trending Card
* Popular Verse Card
* Recommendation Carousel
* Engagement Timer
* Achievement Badge
* Social Share Prompt
* AI Chat Bubble as a persistent global component
* Mood Score
* Growth Score
* Productivity Dashboard
* Infinite Content Feed

These patterns conflict with Antar’s current Product Principles and Experience Architecture.

---

# Candidates Requiring Decomposition Review

The following may be experience compositions rather than reusable components:

* Understanding Section
* Growth Story
* Guidance Response

Today’s Invitation has been resolved as a Home composition (see `99_COMPOSITIONS/TODAYS_INVITATION.md`) rather than a reusable component.

Before documenting them as components, determine whether they represent:

1. A reusable structure with stable behavior, or
2. An experience-specific composition of smaller components.

Do not create abstractions prematurely.

---

# Candidates Requiring Naming Review

The following names should be validated during Figma exploration:

* `Chapter Item` versus `Chapter Card`
* `Journey Memory` versus `Memory Entry`
* `Today’s Invitation` versus `Daily Invitation`
* `Status Message` versus `Toast`
* `Understanding Section` versus separate explanation components
* `Teaching Recommendation` versus `Teaching Path`

Names should describe responsibility rather than visual treatment.

---

# Ownership Rules

## Experiences Own

* Human outcomes
* Emotional progression
* Information hierarchy
* Product behavior
* Success and failure criteria

## Components Own

* Reusable visual and interaction behavior
* Anatomy
* Variants
* States
* Accessibility behavior
* Token usage
* Content constraints

## Services Own

* Data
* Persistence
* Recommendations
* Search execution
* AI responses
* Reading progress calculation
* Synchronization

A component may display service-owned data.

It should not silently own the business logic that creates it.

---

# Documentation Order

Components should be documented in the following order:

## Phase 1 — Product-Defining Reading Components

1. Verse Block
2. Translation Block
3. Saar
4. Reflection Invitation
5. Continue Reading
6. Journal Editor

## Phase 2 — Discovery and Orientation

7. Chapter Item
8. Greeting
9. Today’s Invitation (composition — see `99_COMPOSITIONS/TODAYS_INVITATION.md`)
10. Search Field
11. Search Result

## Phase 3 — Journey and Guidance

12. Journey Memory
13. Journey Timeline Entry
14. Guidance Input
15. Clarifying Question
16. Teaching Recommendation

## Phase 4 — Interface Infrastructure

17. Button
18. Icon Button
19. Navigation
20. Bottom Sheet
21. Feedback States
22. Selection Controls

The order may change after prototyping reveals stronger dependencies.

---

# Component Review Questions

Before approving a component candidate, ask:

1. Which approved experience requires it?

2. What single responsibility does it own?

3. Is the pattern reused meaningfully?

4. Could it remain local to one experience?

5. Is the proposed name semantic or merely visual?

6. Does it contain business logic that belongs to a service?

7. Does it remain understandable independently?

8. How does it behave with Dynamic Type and assistive technology?

9. Does it introduce an interaction that contradicts Antar’s principles?

10. Would the product become less coherent if this component did not exist?

---

# Current Decisions

## Decision 1 — Experiences determine the component inventory.

Components will not be copied from a generic design-system checklist.

---

## Decision 2 — Components compose through layered responsibilities.

Generic primitives compose semantic components.

Semantic components compose larger product components.

Adapter components reuse existing semantic components without redefining their responsibilities.

For example:

- Verse Item composes Verse Reference.
- Verse List composes Verse Items.
- Search Result adapts Verse Item.
- Continue Reading adapts Chapter Item.
- Teaching Recommendation adapts Verse Item.

---

## Decision 3 — Visual similarity alone does not create reuse.

A Chapter Item and Journey Memory may both appear as rounded containers but should not become one generic `Card` unless their behavior and responsibility genuinely align.

---

## Decision 4 — Product-defining components are documented before generic primitives.

The first component specifications should focus on the reading and reflection experience rather than Button or Divider.

---

## Decision 5 — Component status remains provisional until prototyping.

This inventory identifies candidates.

Figma exploration and prototype testing will determine final boundaries, variants, and composition.

---

# Open Decisions

Open decisions are tracked according to where they must be resolved.

## Resolve During Low-Fidelity Prototyping

* How should the Understanding experience decompose into reusable content blocks?
* Should Reflection Invitation and Clarifying Question share a lower-level presentation primitive?
* Should Chapter Item and Search Result share a reusable content-row primitive?
* Which Continue Reading variants are visually necessary across Home, Library, Verse, and Journey?

## Resolve During V1 Product Review

* Which destinations belong in Bottom Navigation?
* Whether Guidance is included in the initial V1 release.
* Which reading preferences belong in V1 beyond language, transliteration, text size, and appearance.
* Whether Theme Exploration is included in Library V1.

## Resolve During Technical Design

* The minimum offline and synchronization state model.
* Ownership of save, bookmark, and progress actions surrounding semantic content components.
* How content-source attribution is represented across translations and commentary.
* Whether generated Journey observations are stored, recomputed, or both.

## Decisions Already Made

* Understanding is an experience-level composition until prototyping proves a stable reusable boundary.
* Continue Reading is one semantic component with contextual variants.
* Saar does not own persistence or save behavior.
* Reflection Invitation and Clarifying Question remain separate semantic components.
* Journey V1 begins with meaningful memories and timeline entries rather than theme analysis or generated Growth Stories.
* Visual similarity alone does not justify merging Chapter Item and Search Result.


---

# Next Step

The next step is not to document every component.

The next step is to validate this inventory against low-fidelity experience layouts.

Begin with the Verse experience and confirm:

* which elements are independently reusable,
* which remain part of the experience composition,
* which states are missing,
* and whether the proposed component boundaries reduce or increase complexity.

After that validation, document the first product-defining component:

> **Verse Block**

---

# North Star

Antar’s component system should feel like a natural consequence of the reader’s journey.

Every component should earn its place by making an approved experience clearer, calmer, more accessible, or more meaningful.
