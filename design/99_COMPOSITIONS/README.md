# COMPONENT COMPOSITIONS

## Purpose

Component Compositions define the approved ways reusable components are assembled to create consistent product experiences.

Components describe individual building blocks.

Interaction Blueprints describe complete reader journeys.

Compositions bridge the two.

They ensure that common patterns are implemented consistently across Antar without duplicating interaction logic in multiple experiences.

---

# Relationship

```text
Interaction Blueprint
        ↓
Composition
        ↓
Components
        ↓
Foundations
```

A composition is not a reusable component.

It is an approved arrangement of reusable components.

---

# Why Compositions Exist

Without compositions:

* every engineer assembles components differently,
* every designer invents slightly different layouts,
* consistency slowly disappears.

Compositions define the canonical arrangement for recurring product patterns.

---

# Principles

A composition should:

* solve one recurring interaction pattern,
* reuse existing components,
* avoid introducing new responsibilities,
* remain independent of implementation,
* remain independent of styling,
* document hierarchy rather than appearance.

---

# Planned Compositions

## Scripture Stack

Canonical presentation of a teaching.

## Reflection Stack

Canonical transition from scripture into reflection.

## Guidance Recommendation

Canonical presentation of AI-guided recommendations.

## Today's Invitation

Canonical Home composition that presents the next meaningful step. It is specific to Home rather than reused across experiences.

Additional compositions should only be added when a pattern appears in multiple experiences.

---

# Non-Responsibilities

Compositions do not:

* replace components,
* replace interaction blueprints,
* define implementation,
* introduce unique visual styling,
* own business logic.

---

# North Star

A composition succeeds when every implementation of the same interaction pattern feels identical regardless of where it appears in Antar.
