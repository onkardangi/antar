# 06_INFORMATION_ARCHITECTURE.md

**Version:** 0.1  
**Status:** Living Document  
**Last Updated:** August 2026

---

# Information Architecture

## Purpose

Information Architecture defines how Antar is organized.

It answers one question:

> **Where does every piece of information belong?**

Good information architecture makes software feel intuitive.

Users should never wonder:

- "Where do I find this?"
- "What should I do next?"
- "Why is this here?"

Instead, every feature should have a clear responsibility and a natural place within the product.

---

# Design Philosophy

Antar is not organized around features.

It is organized around the user's journey.

Every part of the application exists to help users move from:

**Noise → Pause → Reflection → Understanding → Clarity → Action**

The application should feel simple because every system has one responsibility.

---

# Product Systems

Antar is composed of five primary systems.

```
Antar

├── Home
├── Library
├── Guidance
├── Journey
└── Settings
```

Each system owns a unique responsibility.

Responsibilities should never overlap.

---

# System Overview

| System | Responsibility |
|----------|----------------|
| Home | Begin today's journey |
| Library | Read and study the Bhagavad Gita |
| Guidance | Find teachings for real-life situations |
| Journey | Personal growth and reflection |
| Settings | Personal preferences |

---

# System Details

---

# Home

## Purpose

Help users begin today's journey.

Home is **not** a dashboard.

It is a starting point.

Every element on Home should answer:

> **What is the best thing for this person to do right now?**

---

## Primary User

Every returning user.

---

## Inputs

- Time of day
- Last reading session
- Previous reflection
- Reading progress
- Bookmarked verses
- Preferred language
- Personalized recommendations

---

## Outputs

- Personalized greeting
- Today's Invitation
- Browse the Gita

---

## Success

Users begin a meaningful session within ten seconds.

---

# Library

## Purpose

Provide the best digital reading experience for the Bhagavad Gita.

Reading is the heart of Antar.

Nothing should compete with the scripture.

---

## Responsibilities

- Browse chapters
- Browse verses
- Read translations
- Read explanations
- Highlight verses
- Bookmark verses
- Continue reading
- Verse sharing

---

## Principles

Reading comes before AI.

Typography before decoration.

Content before interface.

---

## Success

Users can comfortably discover, read, and understand any verse.

---

# Guidance

## Purpose

Help users discover teachings relevant to their current situation.

Guidance begins with life.

Not with search.

Users should feel like they are asking:

> "What wisdom can help me today?"

---

## Responsibilities

Browse by themes.

Examples:

- Stress
- Anxiety
- Purpose
- Discipline
- Anger
- Relationships
- Fear
- Grief
- Leadership
- Decision Making

Each topic connects users to:

- Relevant verses
- Explanations
- Reflection invitations
- Contextual AI guidance

---

## Principles

Guide people toward scripture.

Never replace scripture.

---

## Success

Users quickly find teachings relevant to their lives.

---

# Journey

## Purpose

Help users see their personal growth over time.

Journey is not about completion.

It is about consistency.

---

## Responsibilities

- Reading history
- Saved verses
- Personal journal
- Reflections
- Recently explored topics
- Personal insights
- Journey timeline

---

## Principles

Growth is personal.

Never competitive.

Celebrate consistency.

Never create pressure.

---

## Success

Users feel encouraged to continue their journey.

---

# Settings

## Purpose

Give users control over their experience.

Settings should remain minimal.

Only preferences belong here.

---

## Responsibilities

- Language
- Theme
- Font size
- Reading preferences
- Accessibility
- Notifications
- Account
- Sync

---

## Principles

Settings should rarely be visited.

Everything important should happen elsewhere.

---

# Navigation Model

Bottom Navigation

```
🏠 Home

📖 Library

🧭 Guidance

🌿 Journey
```

Settings is accessed from the profile/avatar.

This keeps the primary navigation focused on experiences rather than configuration.

---

# Cross-System Services

These services support the entire application.

They are not primary navigation destinations.

---

## Search

Search should be accessible globally.

Users can search by:

- Chapter
- Verse
- Keyword
- Theme
- Sanskrit
- English
- Hindi

Search belongs to the entire application.

Not one specific system.

---

## AI

AI is a supporting capability.

It is **not** a destination.

AI appears contextually throughout Antar.

Examples:

- Explain this verse
- Simplify this teaching
- Ask a question about this verse
- How can I apply this teaching?

AI should always begin from scripture.

Never from an empty chat.

---

## Notifications

Notifications exist to invite.

Never interrupt.

Examples:

✅ "Today's reflection is waiting whenever you're ready."

Not:

❌ "You missed today's reading."

---

## Authentication

Authentication should stay invisible.

Its purpose is continuity.

Not friction.

Users should feel like their journey continues naturally across devices.

---

# Information Hierarchy

```
Home
│
├── Today's Invitation
└── Browse

Library
│
├── Chapters
│     ├── Chapter Details
│     └── Verses
│
├── Verse
│     ├── Translation
│     ├── Commentary
│     ├── AI Explanation
│     ├── Bookmark
│     └── Share
│
└── Search

Guidance
│
├── Themes
│
├── Life Situations
│
├── Recommended Verses
│
└── AI Guidance

Journey
│
├── Reading History
├── Saved Verses
├── Reflections
├── Journal
├── Personal Insights
└── Journey Timeline

Settings
│
├── Language
├── Theme
├── Accessibility
├── Notifications
├── Account
└── About
```

---

# MVP Scope

Version 1 includes:

- Home
- Library
- Guidance
- Journey
- Settings
- Global Search
- Contextual AI
- Authentication
- Notifications
- Bookmarks
- Journal
- Reading Progress

---

# Future Expansion

The architecture intentionally allows future systems such as:

- Audio Reading
- Daily Plans
- Family Mode
- Community Discussions
- Teacher Collections
- Offline AI
- Widgets
- Apple Watch / Wear OS
- Voice Conversations
- Smart Recommendations

These should integrate into existing systems rather than introducing unnecessary top-level navigation.

---

# Architecture Decisions

## Decision 001

### AI is not a primary navigation item.

**Reason**

Reading is the core experience.

AI exists to deepen understanding rather than compete for attention.

**Implications**

- Cleaner navigation
- Stronger product identity
- Less cognitive load
- Reading remains the hero

---

## Decision 002

### Home is not a dashboard.

**Reason**

Users should immediately know what meaningful action to take.

Home exists to begin the day's journey, not display information.

---

## Decision 003

### Journey focuses on growth rather than achievement.

**Reason**

Growth is personal.

Competition contradicts Antar's philosophy.

No leaderboards.

No streak pressure.

Only thoughtful progress.

---

## Decision 004

### Search is a global capability.

**Reason**

Users should be able to find knowledge from anywhere in the application.

Search belongs to the platform, not an individual feature.

---

## Decision 005

### Every system owns one responsibility.

**Reason**

Clear ownership reduces complexity, improves scalability, and keeps the product intuitive as it grows.

---

# Success Criteria

A new user should understand the structure of Antar within their first session.

A returning user should reach the next meaningful action in fewer than ten seconds.

Every piece of content should have a clear, discoverable home.

As Antar evolves, new features should integrate into the existing architecture rather than expanding the primary navigation.

---

# North Star

A user should never wonder where something is.

They should simply continue their journey.