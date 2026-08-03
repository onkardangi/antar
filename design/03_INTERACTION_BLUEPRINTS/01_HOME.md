# HOME INTERACTION BLUEPRINT

**Experience:** Home
**Version:** 1.0
**Status:** Draft
**Owner:** Design
**Last Updated:** August 2026

---

# Mission

The Home experience exists to welcome the reader back to Antar and gently guide them toward their next meaningful interaction.

Rather than presenting features or information, Home should reduce decision-making by offering a clear and calm place to begin.

The experience should feel familiar, welcoming, and intentionally uncluttered.

---

# Modes of Arrival

| Arrival                    | Experience Responsibility                          |
| -------------------------- | -------------------------------------------------- |
| First Launch               | Introduce Antar without overwhelming the reader.   |
| Returning Reader           | Restore continuity and help them resume naturally. |
| Completed Previous Reading | Offer a meaningful next step.                      |
| Returning After Time Away  | Welcome without guilt or pressure.                 |

---

# Reader Mindset

Readers arrive with different intentions.

Some have only a few minutes.

Some are continuing yesterday's reading.

Some simply want a quiet moment.

The Home experience should acknowledge these differences without forcing personalization or making assumptions about the reader's emotional state.

It should create confidence that the next meaningful step is immediately available.

---

# Success Definition

The experience is successful when the reader:

* immediately understands where they are,
* feels welcomed rather than managed,
* identifies one obvious next meaningful action,
* enters another experience without hesitation,
* never feels overwhelmed by choice.

---

# Canonical Home Hierarchy

Home presents one primary action, in this fixed order:

1. Top Navigation
2. Today's Invitation
3. Browse Bhagavad Gita

No other primary sections should be introduced. Continuity is handled as one possible state of Today's Invitation, not as a separate section.

---

# Interaction Timeline

## Stage 1 — Welcome

### Intent

Create a warm, calm beginning.

### Design Decision

Greeting should feel human and timeless rather than algorithmic or overly personalized.

### Components

* Top Navigation
* Greeting

---

## Stage 2 — Invite

### Intent

Present the next meaningful step in the reader's journey.

### Design Decision

Present a single invitation rather than multiple competing recommendations. Today's Invitation presents whatever the reader's context makes most meaningful next—beginning, continuing an unfinished reading, resuming an unfinished reflection, or an approved curated teaching. Continuity is one possible state of this single invitation, not a separate competing section.

### Components

* Today's Invitation

---

## Stage 3 — Explore

### Intent

Allow readers to intentionally discover content.

### Design Decision

Exploration should remain available without distracting from the primary path.

### Components

* Browse Bhagavad Gita

---

# Screen Blueprint

```text
────────────────────────────

Top Navigation

────────────────────────────

Greeting

────────────────────────────

Today's Invitation
(one contextual state at a time)

────────────────────────────

Browse Bhagavad Gita

────────────────────────────
```

---

# States & Recovery

## First-Time Reader

Today's Invitation presents a gentle introduction and a first reading starting point.

---

## Returning Reader

Today's Invitation resumes from the most meaningful continuation point.

---

## No Reading History

Today's Invitation offers a starting point or, when appropriate, an approved curated teaching.

---

## Offline

Allow access to downloaded content.

If nothing is available offline, clearly explain the limitation while preserving navigation.

---

# Component Extraction

## Reusable Components

* Top Navigation
* Greeting
* Continue Reading
* Browse Bhagavad Gita

---

## Experience Compositions

* Today's Invitation

---

## Open Component Questions

* Should Greeting adapt to time of day or remain timeless?
* Should Today's Invitation always recommend scripture, or may it occasionally recommend Journey or Guidance?

---

# Accessibility Considerations

* Greeting should be announced first.
* Primary action should immediately follow the greeting in reading order.
* Navigation targets must have clear accessible labels.
* The primary path should remain obvious regardless of Dynamic Type size.

---

# Validation Questions

* Does presenting only one primary action reduce decision fatigue?
* Does Today's Invitation feel genuinely helpful rather than random?
* Can first-time and returning readers both understand the screen within a few seconds?
* Does Home encourage calm rather than urgency?

---

# Outputs

This Blueprint defines:

* the canonical Home experience,
* the reader's primary entry into Antar,
* reusable Home components,
* validation questions for future prototypes,
* and the behavioral contract for the Home experience.

---

# North Star

The Home experience succeeds when readers feel quietly welcomed and instinctively know where to begin, without being distracted by unnecessary choices or competing priorities.
