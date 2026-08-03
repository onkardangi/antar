# VERSE-001 — Verse System

**Feature ID:** VERSE-001

**Priority:** P0 (Critical)

**Status:** Draft

**Owner:** Product

**Version:** 1.0

**Last Updated:** August 2026

---

# Guiding Principle

> **Every verse should leave the reader understanding one thing more clearly than when they arrived.**

The Verse System exists to create understanding.

Reading is only the beginning.

The ultimate goal is to help users carry timeless wisdom into everyday life.

---

# North Star

> **The Verse System is the heart of Antar. Every other system exists to help users arrive here prepared, present, and ready to understand.**

If the Verse experience succeeds, the product succeeds.

Everything else is designed to support this moment.

---

# Purpose

The Verse System transforms a single verse into a complete learning experience.

It creates the conditions for:

- Reading
- Understanding
- Reflection
- Application
- Growth

The Verse System is not designed to maximize the number of verses users complete.

It is designed to maximize the depth with which each verse is understood.

---

# Why This System Exists

Reading scripture is different from reading information.

Many applications stop after displaying the text.

Antar continues further.

The Verse System helps readers move from:

Reading

↓

Understanding

↓

Reflection

↓

Practice

↓

Growth

Without reflection, reading becomes information.

Without practice, reflection becomes intention.

The Verse System exists to bridge that gap.

---

# Design Objectives

Every design decision should support these objectives.

## Objective 1

Help users slow down.

---

## Objective 2

Protect the reading moment.

---

## Objective 3

Reduce cognitive load.

---

## Objective 4

Create understanding before interaction.

---

## Objective 5

Leave users with one memorable idea.

---

# Emotional Journey

The Verse experience is designed around emotional progression rather than navigation.

| Stage | User Emotion |
|---------|--------------|
| Arrival | Calm |
| Reading | Focus |
| Understanding | Curiosity |
| Reflection | Honesty |
| Saar | Clarity |
| Continue | Hope |

The interface should quietly support each emotional transition.

---

# Product Transformation

Every verse follows the same journey.

```
Read

↓

Understand

↓

Reflect

↓

Practice

↓

Grow
```

This transformation model guides every interaction within the Verse System.

---

# Responsibilities

The Verse System owns:

- Verse display
- Sanskrit text
- Transliteration
- English translation
- Hindi translation
- Verse metadata
- Understanding experience
- Traditional commentary
- AI understanding layer
- Reflection invitations
- Saar
- Related verses
- Share entry point
- Continue Reading entry point

The Verse System does NOT own:

- Journal persistence
- Bookmark persistence
- User authentication
- Reading progress calculation
- Analytics implementation

Those responsibilities belong to their respective systems.

---

# Anti-Goals

The Verse System should never become:

- A chatbot
- A social feed
- A productivity tool
- A gamified reading tracker
- An endless AI conversation
- A dense academic textbook

The verse must always remain the hero.

---

# System Lifecycle

```
User Opens Verse

↓

Arrival

↓

Reading

↓

Pause

↓

Understanding

↓

Reflection

↓

Saar

↓

Continue

↓

Exit Verse
```

Every stage should feel intentional.

Nothing should rush the user.

---

# Information Hierarchy

The Verse experience follows a fixed hierarchy.

```
Verse

↓

Translation

↓

Pause

↓

Understanding

↓

Reflection

↓

Saar

↓

Related Wisdom

↓

Continue Reading
```

This hierarchy should remain consistent throughout the application.

---

# Progressive Depth

Understanding should unfold gradually.

The Verse System should never overwhelm users with every layer of information at once.

Each layer answers a different question.

## Layer 1

### The Verse

What was originally spoken?

---

## Layer 2

### Translation

What does it literally say?

---

## Layer 3

### Understanding

What does it mean?

---

## Layer 4

### Reflection

What does this mean for me?

---

## Layer 5

### Saar

What should I carry into my life?

Users decide how deeply they wish to explore.

---

# Reading Layer

Purpose

Present the verse with complete respect and minimal distraction.

Displays

- Sanskrit
- Transliteration
- English
- Hindi

Business Rules

No AI.

No commentary.

No prompts.

No recommendations.

Only the verse.

---

# Pause

Reading deserves a moment of silence.

The application should never immediately begin explaining the verse.

Whitespace, typography, and pacing should encourage presence.

Understanding begins after reading.

---

# Understanding Layer

Purpose

Help users understand the teaching without replacing it.

Components

- Simple explanation
- Traditional commentary
- Historical context
- Related concepts
- AI understanding

The explanation should illuminate.

Never overshadow.

---

# AI Philosophy

AI exists to deepen understanding.

Not replace contemplation.

AI should never be the primary focus of the Verse experience.

Suggested actions include:

- Explain Simply
- Modern Meaning
- Apply to My Life
- Compare Translations
- Ask a Question

Users initiate deeper exploration.

AI never interrupts.

---

# Reflection Layer

Purpose

Help readers connect the teaching to their own lives.

Reflection is optional.

Reflection is personal.

Reflection may be:

- Mental
- Choice-based
- Written
- Action-oriented

The Verse System should never force journaling.

---

# Saar Layer

Saar represents the essence of the verse.

Every verse has exactly one Saar.

Never multiple.

Never paragraphs.

Never bullet points.

The purpose of Saar is to leave the reader with one memorable thought they can carry into the day.

Example

```
Saar

Today's Essence

Act sincerely.

Release the outcome.
```

Saar is the final teaching before the user leaves the verse.

---

# Continue Layer

Continue Reading is an invitation.

Never a demand.

Instead of encouraging speed, it encourages readiness.

Example

"When you're ready..."

Continue to Verse 2.48 →

The Verse experience should conclude with Saar.

Continue Reading should quietly follow.

---

# Product Rules

## Rule 1

Reading always comes before AI.

---

## Rule 2

The verse is always the visual focus.

---

## Rule 3

Protect the reading moment.

---

## Rule 4

Understanding unfolds progressively.

---

## Rule 5

Reflection remains optional.

---

## Rule 6

Every verse has one Saar.

---

## Rule 7

Continue Reading should never overshadow Saar.

---

## Rule 8

The Verse System optimizes for presence, not completion.

---

# Data Requirements

The Verse System requires:

| Data | Source |
|------|--------|
| Verse Text | Content Service |
| Translations | Content Service |
| Transliteration | Content Service |
| Commentary | Content Service |
| Historical Context | Content Service |
| AI Explanation | AI Service |
| Reflection Invitation | Content Service |
| Saar | Content Service |
| Related Verses | Content Service |
| Continue Reading | Journey Service |

The Verse System composes these sources into a single experience.

---

# State Management

## Loading

Display lightweight skeletons.

Preserve layout.

---

## Ready

Display complete experience.

---

## Offline

Display cached verses and previously downloaded explanations.

---

## Partial

AI unavailable.

Reading remains fully functional.

---

## Error

Never prevent access to the verse.

Gracefully hide unavailable enhancements.

---

# Failure Modes

Failure

Users immediately scroll.

Cause

Information overload.

---

Failure

Users skip the verse.

Cause

Explanation appears too early.

---

Failure

Reflection feels like homework.

Cause

Large writing prompts.

---

Failure

AI becomes the focus.

Cause

Overly prominent interface.

---

Failure

Users remember the explanation but not the verse.

Cause

Poor visual hierarchy.

---

# Product Metrics

Primary

- Verse Open Rate
- Verse Completion
- Understanding Expansion Rate
- Reflection Rate
- Saar Viewed

Secondary

- Continue Reading Rate
- Related Verse Usage
- AI Interaction Rate

Success is measured by meaningful engagement rather than time spent.

---

# Accessibility

The Verse System must support:

- Dynamic Type
- VoiceOver / TalkBack
- High Contrast
- Reduced Motion
- Adjustable line spacing
- Adjustable reading width
- Large touch targets

Reading comfort takes priority over visual density.

---

# Dependencies

The Verse System depends on:

- Chapter System
- Journey System
- AI System
- Journal System
- Bookmark System
- Content Service

The Verse System orchestrates these systems into one uninterrupted experience.

---

# Security & Privacy

Personal reflections remain private.

AI conversations are never used to alter the scripture.

The integrity of the original verse must always be preserved.

---

# Definition of Ready

Before implementation:

- Verse content finalized
- Saar approved
- Reflection invitations reviewed
- AI behavior defined
- Product principles validated

---

# Definition of Done

The Verse System is complete when:

- Every verse can be read without distraction.
- Progressive understanding functions correctly.
- Reflection is available but optional.
- Every verse includes one Saar.
- AI remains contextual.
- Accessibility requirements pass.
- Offline reading works.
- Performance goals are met.

---

# Future Enhancements

Version 2+

- Audio recitation
- Guided meditation
- Scholar perspectives
- Voice conversations
- Comparative traditions
- Personalized reflections

---

# Open Questions

Should Saar always be manually authored?

Should multiple trusted commentaries be available?

How should AI indicate uncertainty when interpreting philosophical questions?

Should users be able to save Saar independently of bookmarks?

---

# North Star Reminder

The Verse System should never ask:

> "How quickly can someone finish reading?"

Instead it should ask:

> **"How deeply can someone understand one verse today?"**