# REPOSITORY ARCHITECTURE

**Version:** 1.0
**Status:** Approved
**Owner:** Product & Engineering
**Last Updated:** August 2026

---

# Purpose

This document defines how knowledge is organized within the Antar repository.

It is the architectural guide for documentation—not for software.

Every document should have one clear responsibility and one authoritative location.

The goal is to ensure the repository remains understandable, maintainable, and scalable as Antar grows.

---

# Philosophy

The repository is organized by layers of abstraction.

Each layer answers a different question.

No layer should duplicate or redefine another.

Knowledge should exist in exactly one authoritative location.

---

# Repository Layers

## Layer 1 — Product

**Question**

> Why does Antar exist?

Contains:

* Product Bible
* Product Principles
* Vision
* Personas
* Information Architecture
* Product Specifications

Defines:

* philosophy,
* product direction,
* experience goals,
* business scope.

Does not define:

* interaction details,
* reusable UI,
* engineering implementation.

---

## Layer 2 — Experiences

**Question**

> What should the reader experience?

Contains:

* Home
* Library
* Verse
* Journal
* Journey
* Guidance

Defines:

* emotional intent,
* reader goals,
* information hierarchy,
* success criteria,
* experience philosophy.

Does not define:

* reusable components,
* design tokens,
* implementation details.

---

## Layer 3 — Interaction Blueprints

**Question**

> How should this experience behave?

Contains:

* interaction flows,
* screen blueprints,
* attention hierarchy,
* state transitions,
* component extraction,
* accessibility flow,
* edge cases.

Defines:

* user interaction.

Does not define:

* colors,
* typography,
* component anatomy,
* engineering implementation.

---

## Layer 4 — Components

**Question**

> What reusable building blocks create these experiences?

Contains:

* reusable interface components,
* anatomy,
* variants,
* states,
* accessibility,
* interaction behavior,
* token usage.

Defines:

* reusable UI behavior.

Does not define:

* product philosophy,
* experience goals,
* business logic.

---

## Layer 5 — Prototypes

**Question**

> Does this design work?

Contains:

* low-fidelity explorations,
* high-fidelity mockups,
* interaction validation,
* usability experiments.

Defines:

* design validation.

Does not become the source of truth.

Approved decisions must flow back into Experiences or Components.

---

## Layer 6 — Engineering

**Question**

> How is Antar built?

Contains:

* architecture,
* APIs,
* data models,
* ADRs,
* implementation guides,
* deployment.

Defines:

* technical implementation.

Does not redefine product or design decisions.

---

# Dependency Rules

Knowledge flows downward.

```text
Product
    ↓
Experiences
    ↓
Interaction Blueprints
    ↓
Components
    ↓
Prototypes
    ↓
Engineering
```

Lower layers may reference higher layers.

Lower layers may never redefine higher layers.

---

# Source of Truth

Every concept must have one authoritative owner.

Examples:

| Concept            | Source                 |
| ------------------ | ---------------------- |
| Product Principles | Product                |
| Typography         | Design Foundations     |
| Verse Experience   | Experiences            |
| Continue Reading   | Components             |
| Reading Flow       | Interaction Blueprints |
| Navigation API     | Engineering            |

Duplicate definitions should be avoided.

---

# Documentation Rules

Every document should answer exactly one primary question.

If a document begins answering multiple questions, the content likely belongs in different layers.

Documents should reference other layers rather than duplicate them.

---

# Decision Ownership

Product owns:

* vision,
* philosophy,
* reader outcomes.

Design owns:

* experiences,
* foundations,
* interaction,
* reusable components.

Engineering owns:

* implementation,
* architecture,
* infrastructure,
* deployment.

Cross-functional decisions should be documented through Architecture Decision Records (ADRs) rather than duplicated.

---

# Repository Principles

1. One concept. One owner.
2. One source of truth.
3. References instead of duplication.
4. Higher layers guide lower layers.
5. Lower layers never redefine higher layers.
6. Reusable knowledge belongs in reusable documents.
7. Product decisions precede implementation decisions.

---

# Change Process

When introducing new documentation:

1. Identify which question it answers.
2. Determine the appropriate repository layer.
3. Check whether an authoritative source already exists.
4. Create the smallest document necessary.
5. Reference existing documentation instead of copying it.

---

# Success Criteria

The repository succeeds when:

* new contributors know where information belongs,
* duplicate documentation is rare,
* product philosophy remains consistent,
* implementation follows approved decisions,
* and every document has a clear purpose.

---

A lower-layer document should only restate information from a higher layer when the application of that principle is unique to the current context. Otherwise, it should reference the higher-layer document rather than duplicate it.

---

# North Star

Every document should make Antar easier to understand—not simply increase the number of files.

The repository should evolve as a coherent knowledge system where every layer supports the one below it, and every decision has one clear home.
