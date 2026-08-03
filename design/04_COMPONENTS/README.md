# COMPONENT SYSTEM

This directory defines the reusable interface building blocks used to construct Antar's experiences.

Components are not experiences.

An experience answers:

> What should the reader experience?

A component answers:

> What reusable interface behavior helps create that experience?

## Component Principles

Every component should:

- have one clear responsibility,
- support a recognizable user intention,
- remain composable,
- use semantic design tokens,
- support accessibility from the beginning,
- define its states and behavior,
- and avoid accumulating unrelated product logic.

## Component Documentation

Each component specification should define:

1. Purpose
2. Responsibility
3. Non-responsibilities
4. Usage
5. Anatomy
6. Variants
7. States
8. Interaction behavior
9. Content guidance
10. Accessibility
11. Motion
12. Design tokens
13. Engineering notes
14. Good examples
15. Anti-patterns
16. Open questions

## Relationship to Other Design Layers

- Foundations define cross-product visual and interaction rules.
- Experiences define reader-facing outcomes and emotional journeys.
- Components provide reusable building blocks.
- Prototypes validate how these layers work together.

Do not create a new component merely because a screen contains a visually distinct element.

Create a component when the behavior or pattern is reusable, independently understandable, and meaningfully governed.

## Component Families

```text
04_COMPONENTS/
├── 00_COMPONENT_INVENTORY.md
├── 01_NAVIGATION/
├── 02_SCRIPTURE/
├── 03_LIBRARY/
├── 04_REFLECTION/
├── 05_GUIDANCE/
└── 06_JOURNEY/
```

* `01_NAVIGATION/` — orientation and continuation.
* `02_SCRIPTURE/` — scripture and supporting reading content.
* `03_LIBRARY/` — chapter, verse, and search discovery.
* `04_REFLECTION/` — prompts, writing, and reflection history.
* `05_GUIDANCE/` — life-context input and paths back to scripture.
* `06_JOURNEY/` — meaningful memories and long-term reflection.
