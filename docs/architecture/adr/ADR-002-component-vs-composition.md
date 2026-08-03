# ADR-002 — Today's Invitation Is a Composition

## Status

Accepted

## Context

Today's Invitation was initially treated as a reusable component.

However it coordinates multiple reusable components and product decisions.

## Decision

Today's Invitation is an experience composition.

It assembles:

- Verse Context
- Continue Reading
- Context Label

It does not determine what should be shown.

That responsibility belongs to product services.

## Consequences

- Better separation of responsibilities.
- Cleaner component library.
- Reusable primitives remain independent.