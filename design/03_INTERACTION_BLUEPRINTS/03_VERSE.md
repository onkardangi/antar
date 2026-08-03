# VERSE INTERACTION BLUEPRINT

**Experience:** Verse
**Version:** 1.0
**Status:** Draft
**Owner:** Design
**Last Updated:** August 2026

---

# Mission

The Verse experience exists to create a calm, focused encounter with a single teaching from the Bhagavad Gita.

Every element of the experience exists to deepen understanding of the teaching without competing for the reader's attention.

Scripture always comes first. Supporting content—including translations, explanations, AI assistance, and reflection—exists only to help the reader understand the teaching more deeply, never to replace or overshadow it.

---

# Modes of Arrival

| Arrival          | Experience Responsibility                                                                      |
| ---------------- | ---------------------------------------------------------------------------------------------- |
| Continue Reading | Restore context immediately so the reader can resume without friction.                         |
| Chapter          | Continue naturally from chapter exploration into focused reading of an individual verse.       |
| Guidance         | Transition naturally from a life situation into scripture without making AI the destination.   |
| Journey          | Reconnect the reader with a previously meaningful teaching while allowing fresh understanding. |
| Search           | Minimize friction between discovery and reading.                                               |

---

# Reader Mindset

Readers may arrive with curiosity, uncertainty, gratitude, grief, hope, or simply the intention to continue reading.

The experience should not assume why they arrived.

Instead, it should create enough clarity and stillness that every reader can encounter the teaching without unnecessary interruption.

---

# Success Definition

The experience is successful when the reader:

* encounters the verse without distraction,
* understands its core teaching,
* feels invited—not pressured—to reflect,
* leaves with greater clarity than when they arrived,
* and naturally knows what to do next.

---

# Interaction Timeline

## Stage 1 — Arrive

### Intent

Orient the reader.

### Design Decision

The experience should immediately establish where the reader is without overwhelming them with choices.

### Components

* Top Navigation
* Verse Reference

---

## Stage 2 — Encounter

### Intent

Present the teaching.

### Design Decision

The verse is always encountered before interpretation.

Nothing should compete with scripture.

### Components

* Verse Block
* Transliteration (optional)
* Translation

---

## Stage 3 — Understand

### Intent

Deepen understanding.

### Design Decision

Supporting content should expand the reader's understanding while remaining visually and conceptually secondary to the teaching itself.

### Components

* Understanding Section
* Commentary
* Context
* AI Guidance (when appropriate)

---

## Stage 4 — Reflect

### Intent

Invite personal reflection.

### Design Decision

Reflection is always optional.

The experience encourages contemplation but never requires participation.

### Components

* Reflection Invitation
* Saar

---

## Stage 5 — Continue

### Intent

Maintain momentum.

### Design Decision

Readers should leave with one obvious next step.

The experience should avoid overwhelming readers with competing actions.

### Components

* Continue Reading

---

# Screen Blueprint

```text
────────────────────────────

← Chapter 2

Verse 47

────────────────────────────

Verse Block

────────────────────────────

Transliteration (Optional)

────────────────────────────

Translation

────────────────────────────

Understanding

────────────────────────────

Reflection Invitation

────────────────────────────

Saar

────────────────────────────

Continue Reading

────────────────────────────
```

---

# States & Recovery

## Loading

Display a lightweight loading state that preserves the expected reading structure.

---

## Offline

If the verse is available locally, allow uninterrupted reading.

If not, clearly communicate that internet access is required while preserving navigation.

---

## Translation Unavailable

Continue presenting the original verse and clearly communicate that the selected translation is unavailable.

---

## AI Unavailable

Remove AI guidance entirely.

The teaching must remain complete without AI assistance.

---

## Commentary Unavailable

Present the verse, translation, and Saar without interruption.

Readers should never lose access to scripture because supplementary content is unavailable.

---

# Component Extraction

## Reusable Components

* Verse Block
* Verse Reference
* Translation Block
* Reflection Invitation
* Saar
* Continue Reading

---

## Experience Compositions

* Understanding Section

The Understanding Section is a composition of multiple content blocks rather than a reusable component.

---

## Open Component Questions

* Should Commentary and AI Guidance remain separate content blocks?
* Does Transliteration belong inside Verse Block or exist independently?

---

# Accessibility Considerations

* Preserve a logical reading order.
* Support Dynamic Type without compromising scripture readability.
* Ensure VoiceOver announces verse reference before verse content.
* Decorative elements must never interrupt reading.
* Reflection invitations should remain reachable but never interrupt screen reader flow.

---

# Validation Questions

* Does placing Reflection before Saar help the reader arrive at the essence more naturally?
* Should Understanding be expanded by default or remain collapsed?
* Does Transliteration improve readability for new readers or create unnecessary visual weight?
* Is Continue Reading sufficiently visible without competing with reflection?

---

# Outputs

This Blueprint defines:

* the canonical Verse interaction flow,
* the primary reading sequence,
* reusable component candidates,
* experience-level compositions,
* validation questions for future prototypes,
* and the behavioral contract between Product, Design, and Engineering.

---

# North Star

The Verse experience succeeds when the interface quietly disappears, allowing the teaching—not the application—to become the center of the reader's attention.
