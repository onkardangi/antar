# TODAY'S INVITATION

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Today's Invitation is the single primary entry point on Home.

It presents the next meaningful step in the reader's journey through the Bhagavad Gita.

Today's Invitation is not limited to a daily curated verse, and it is not limited to resuming reading progress. Depending on the reader's context, the already-selected destination may be a starting point for a new reader, the next unread verse, a return to unfinished reading, a return to an unfinished reflection, or a curated teaching when appropriate.

Today's Invitation presents the destination. It does not select it.

---

# Used By

* Home

Today's Invitation is a Home composition. It is not a reusable component and does not appear in other experiences.

---

# Canonical Structure

```text
Contextual Invitation Label (optional)

↓

Destination Context

↓

Compact Preview
(appropriate to the selected destination)

↓

Continue Reading
```

---

# Composition Responsibilities

## Contextual Invitation Label

A gentle, optional line that frames the invitation when it adds clarity.

It should remain invitational rather than urgent.

---

## Destination Context

Enough context for the reader to understand where the invitation leads.

---

## Compact Preview

A small preview appropriate to the selected destination, such as a verse reference or a short line of scripture.

The preview should point toward scripture or scripture-rooted reflection.

---

## Continue Reading

One action that carries the reader into the selected destination.

Continue Reading remains a reusable navigation component. Today's Invitation composes it; it does not replace or merge with it.

---

# Destination States

Today's Invitation expresses one composition through contextual states. These are states of a single invitation, not separate components, and only one is presented at a time.

## Begin Journey

A starting point for a new reader.

---

## Continue Reading

A return to unfinished reading.

---

## Resume Reflection

A return to an unfinished reflection.

---

## Curated Teaching

An approved curated teaching, when appropriate.

---

# Selection Ownership

The destination is chosen by product and supporting services.

The composition receives an already-selected destination and presents it.

Today's Invitation does not:

* select its own destination,
* calculate reading progress,
* rank teachings,
* or generate recommendations.

The destination-selection algorithm is intentionally left undefined here.

---

# Forbidden Patterns

Do not:

* present more than one destination at a time,
* display multiple competing calls to action,
* duplicate a separate Continue Journey section,
* become a recommendation feed,
* introduce engagement mechanics,
* or become a generic wellness prompt.

---

# Engineering Notes

Today's Invitation owns only the composition.

Continue Reading and any preview components remain independently reusable.

A selection service determines the destination and supplies it to the composition.

---

# Validation Questions

* Does the invitation present exactly one destination?
* Can the reader understand where the invitation leads?
* Does every state lead toward scripture or scripture-rooted reflection?
* Does the invitation feel invitational rather than urgent?

---

# North Star

Today's Invitation succeeds when a reader opens Home, sees one meaningful next step, and continues into scripture without having to choose among competing options.
