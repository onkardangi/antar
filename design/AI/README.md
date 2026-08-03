# AI Design Toolkit

Version: 1.0

---

# Purpose

This directory contains the prompts and context used to generate Antar's user interface with AI design tools such as:

- Figma AI
- Figma Agent
- ChatGPT
- Claude
- Future design assistants

The goal is **not** to allow AI to design Antar independently.

The goal is to ensure every AI generation follows the Antar Design Language (ADL) rather than inventing generic product patterns.

These prompts should be treated as implementation guides—not sources of product decisions.

Product decisions belong to the ADL.

---

# Philosophy

AI is a design assistant.

It is not the product designer.

The architecture, component system, interaction model, and philosophy have already been defined within the Antar Design Language.

AI should implement those decisions rather than invent new ones.

Whenever AI and the ADL disagree, the ADL always takes precedence.

---

# Directory Structure

```
AI/

README.md

FIGMA_CONTEXT.md

prompts/

    HOME_PROMPT.md

    VERSE_PROMPT.md

    LIBRARY_PROMPT.md

    GUIDANCE_PROMPT.md

    JOURNEY_PROMPT.md
```

---

# File Responsibilities

## FIGMA_CONTEXT.md

The global system prompt.

Defines:

- Antar philosophy
- Design principles
- Component hierarchy
- Product constraints
- Visual language
- Things AI must never generate

Every prompt assumes this file has already been read.

---

## prompts/

Each prompt defines a single experience.

A prompt specifies:

- screen purpose
- approved components
- compositions
- information hierarchy
- interaction goals
- forbidden UI
- success criteria

Prompts should never redefine global philosophy.

---

# Standard Workflow

For every screen:

## 1. Read FIGMA_CONTEXT.md

Establish product philosophy and design constraints.

---

## 2. Read the screen prompt

Understand the specific experience being generated.

---

## 3. Generate one screen only

Never generate multiple screens.

Never redesign the application.

---

## 4. Human review

Evaluate:

- information hierarchy
- spacing
- interaction
- clarity

Do not evaluate visual polish during wireframing.

---

## 5. Refine

Iterate through focused prompts.

Example:

- Increase spacing.
- Reduce emphasis.
- Simplify hierarchy.

Avoid regenerating the entire screen.

---

# Prompting Guidelines

Prefer:

> Refine the existing frame.

Instead of:

> Design a new screen.

Small iterations produce significantly better results than large prompts.

---

# Screen Order

Wireframes should be created in this order.

1. Home

2. Verse

3. Library

4. Guidance

5. Journey

This follows the primary reader journey through Antar.

---

# Wireframe Rules

Wireframes are intentionally low fidelity.

Use:

- grayscale
- rectangles
- placeholder text
- spacing
- hierarchy

Avoid:

- colors
- illustrations
- shadows
- branding
- polished UI

Beauty comes after interaction.

---

# AI Constraints

AI must never invent:

- new components
- new navigation
- new product philosophy
- engagement mechanics
- wellness features
- chat interfaces

If required information is missing:

Use placeholders.

Do not make assumptions.

---

# Definition of Success

A successful AI-generated screen:

- follows the Antar Design Language,
- uses only approved components,
- answers one primary user question,
- preserves scripture as the center of the experience,
- and requires only refinement rather than redesign.

The objective is consistency—not creativity.