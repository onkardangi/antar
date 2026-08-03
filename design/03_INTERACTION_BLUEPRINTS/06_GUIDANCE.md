# GUIDANCE INTERACTION BLUEPRINT

**Experience:** Guidance
**Version:** 1.0
**Status:** Draft
**Owner:** Design
**Last Updated:** August 2026

---

# Decision Deferred

Future product decision:

* Theme-based Guidance
* Free-text AI Guidance

The choice between these models is intentionally deferred.

---

# Mission

The Guidance experience exists to help readers connect their present life circumstances with relevant teachings from the Bhagavad Gita.

Guidance does not exist to provide answers or replace personal judgment.

Its purpose is to gently lead readers toward scripture that may help them reflect on their situation.

AI serves as a guide, not as the destination.

---

# Modes of Arrival

| Arrival    | Experience Responsibility                                                             |
| ---------- | ------------------------------------------------------------------------------------- |
| Home       | Provide a thoughtful starting point when readers seek wisdom for a current situation. |
| Navigation | Offer a dedicated space to ask questions rooted in life's challenges.                 |
| Verse      | Allow readers to explore related teachings more deeply.                               |
| Journey    | Connect past reflections with present questions.                                      |

---

# Reader Mindset

Readers arrive carrying something real.

It may be uncertainty, conflict, grief, gratitude, fear, or curiosity.

The experience should acknowledge that every reader's situation is unique without assuming it fully understands them.

Guidance should create confidence that the Bhagavad Gita contains wisdom worth exploring, rather than confidence that AI has the right answer.

---

# Success Definition

The experience is successful when the reader:

* feels understood without feeling analyzed,
* discovers a relevant teaching,
* spends more time with scripture than with AI,
* leaves with greater perspective rather than definitive answers,
* continues their journey through the Bhagavad Gita.

---

# Interaction Timeline

## Stage 1 — Share

### Intent

Invite the reader to describe their situation.

### Design Decision

Input should feel conversational, private, and free of pressure.

Readers should never feel they need to phrase their situation perfectly.

### Components

* Guidance Input

---

## Stage 2 — Clarify

### Intent

Reduce assumptions before recommending scripture.

### Design Decision

Ask at most one or two clarifying questions only when necessary.

Silence is preferable to unnecessary conversation.

### Components

* Clarifying Question

---

## Stage 3 — Recommend

### Intent

Present one or a small number of relevant teachings.

### Design Decision

Recommendations should explain why a teaching may be relevant while making it clear that the reader—not the AI—discovers its meaning.

### Components

* Teaching Recommendation
* Verse Reference
* Translation Block

---

## Stage 4 — Read

### Intent

Transition naturally into the Verse experience.

### Design Decision

The recommendation should feel like the beginning of the journey rather than the conclusion.

The Bhagavad Gita becomes the primary focus from this point forward.

### Components

* Continue Reading

---

# Screen Blueprint

```text
────────────────────────────

What is on your mind?

[ Guidance Input ]

────────────────────────────

(Optional)

Clarifying Question

────────────────────────────

Suggested Teaching

Verse Reference

Translation Block

Why this may help

────────────────────────────

Read the Verse

────────────────────────────
```

---

# States & Recovery

## First Question

Present a welcoming input with clear privacy expectations.

---

## Clarification Needed

Ask one focused follow-up question before making recommendations.

---

## Recommendation Ready

Present teachings with brief context and a clear path into the Verse experience.

---

## No Confident Recommendation

Acknowledge uncertainty.

Offer a small set of foundational teachings rather than pretending confidence.

---

## Offline

Clearly explain that Guidance requires connectivity while allowing readers to continue browsing the Library or resume previous reading.

---

## AI Unavailable

Do not replace AI with fabricated confidence.

Explain that Guidance is temporarily unavailable and encourage readers to explore the Library directly.

---

# Component Extraction

## Reusable Components

* Guidance Input
* Clarifying Question
* Teaching Recommendation
* Verse Reference
* Translation Block
* Continue Reading

---

## Experience Compositions

* Recommendation Summary

---

## Open Component Questions

* Should recommendations always include more than one verse?
* How much explanation is helpful before readers begin reading?
* Should readers be able to save guidance sessions for future reflection?

---

# Accessibility Considerations

* Ensure the input experience supports voice dictation and keyboard navigation.
* Announce recommendations in a clear reading order.
* Preserve a simple interaction flow for screen-reader users.
* Ensure that clarifying questions do not trap focus or create unnecessary interaction loops.

---

# Validation Questions

* Do readers understand that AI is guiding them toward scripture rather than providing answers?
* Does limiting clarification reduce friction without reducing relevance?
* Does the recommendation provide enough context without replacing the teaching itself?
* Do readers naturally continue into the Verse experience?

---

# Outputs

This Blueprint defines:

* the canonical Guidance experience,
* the relationship between AI and scripture,
* reusable Guidance components,
* experience-level compositions,
* and validation questions for future prototypes.

---

# North Star

The Guidance experience succeeds when readers leave believing they discovered wisdom within the Bhagavad Gita—not that they received the perfect answer from an AI system.
