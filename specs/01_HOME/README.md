# HOME-001 — Home System

**Feature ID:** HOME-001

**Priority:** P0 (Critical)

**Status:** Draft

**Owner:** Product

**Version:** 2.0

**Last Updated:** August 2026

---

> **Status: Superseded — Pending Rewrite**
>
> This specification describes an earlier Home model based on separate Continue Journey, Today’s Reflection, and Yesterday’s Reflection cards.
>
> The approved Home architecture now uses Today’s Invitation as the single primary composition, followed by one compact Browse Bhagavad Gita entry.
>
> Today’s Invitation presents one already-selected next meaningful step, which may represent beginning, continuing reading, resuming reflection, or an approved curated teaching.
>
> Do not use this specification for new design or implementation work.
>
> Canonical references:
>
> - `design/02_EXPERIENCES/01_CORE/02_HOME.md`
> - `design/03_INTERACTION_BLUEPRINTS/01_HOME.md`
> - `design/99_COMPOSITIONS/TODAYS_INVITATION.md`
> - `design/AI/prompts/HOME_PROMPT.md`

---

# Purpose

Home is the beginning of every user's daily journey.

It is not a dashboard.

It is not a feed.

It is not a launcher for every feature in the application.

Home exists for one reason:

> Help the user begin a meaningful session in less than ten seconds.

Everything shown on Home should reduce decision fatigue and gently guide the user toward the next meaningful step in their relationship with the Bhagavad Gita.

When someone opens Antar, they should immediately feel:

- Welcome
- Calm
- Present
- Ready to continue

---

# Responsibilities

The Home System is responsible for orchestrating the beginning of a session.

It owns:

- Greeting
- Continue Journey
- Yesterday's Reflection
- Today's Reflection
- Browse Entry Point

Home does NOT own:

- Reading
- Search
- Journal
- AI Conversations
- Settings
- Authentication

Those systems remain responsible for their own business logic.

Home only composes their outputs.

---

# System Lifecycle

The Home System follows this lifecycle every time the application opens.

```

Application Launch

↓

Authentication

↓

Load User Profile

↓

Load User Preferences

↓

Load Journey Summary

↓

Load Today's Reflection

↓

Compose Home Experience

↓

Render UI

↓

User Interaction

↓

Persist Session

```

Home never generates business data.

It requests information from other systems and presents it in a meaningful order.

---

# Inputs

The Home System depends on data produced by other systems.

| Data | Source |
|------|--------|
| User Name | User Profile |
| Time of Day | Device |
| Preferred Language | Preferences |
| Last Chapter | Journey |
| Last Verse | Journey |
| Reading Progress | Journey |
| Yesterday's Reflection | Journal |
| Today's Reflection | Reflection Service |
| Cached Data | Local Storage |

---

# Outputs

The Home System produces:

- Greeting
- Continue Journey Card
- Yesterday's Reflection Card
- Today's Reflection Card
- Browse Entry Point

No additional content should appear without a documented product decision.

---

# System Dependencies

Home depends on:

- Authentication
- User Profile
- Preferences
- Journey
- Reflection
- Local Cache

Home should remain independent from implementation details.

It should consume interfaces rather than direct implementations.

---

# User Journeys

## Returning User

Launch App

↓

Greeting

↓

Continue Journey

↓

Verse

↓

Reflection

↓

Journal (Optional)

↓

Close App

---

## First-Time User

Launch App

↓

Greeting

↓

Today's Reflection

↓

Read First Verse

↓

Optional Bookmark

↓

Close App

---

## Offline User

Launch App

↓

Greeting

↓

Continue Journey (Cached)

↓

Previously Viewed Verse

↓

Close App

---

# Product Rules

These rules are non-negotiable.

## Rule 1

There is always exactly one primary action.

---

## Rule 2

Continue Journey always takes priority over discovery.

---

## Rule 3

AI never appears before scripture.

---

## Rule 4

Home never becomes a dashboard.

---

## Rule 5

Home never becomes an infinite feed.

---

## Rule 6

Cards should not unexpectedly reorder between sessions.

Consistency builds trust.

---

## Rule 7

Users should begin reading with one tap.

---

## Rule 8

Home exists to start a session.

Not to keep users scrolling.

---

# Component Ownership

| Component | Owner |
|-----------|-------|
| Greeting | Home |
| Continue Journey | Journey |
| Today's Reflection | Reflection |
| Yesterday's Reflection | Journal |
| Browse | Reading |

Home orchestrates.

It does not own business logic.

---

# State Management

## Initial State

Loading placeholders.

---

## Ready State

All available content displayed.

---

## Partial State

Reflection unavailable.

Continue Journey available.

Greeting available.

---

## Offline State

Cached content.

No network requests.

---

## Error State

Graceful degradation.

Users should always have something meaningful to read.

---

# Failure Modes

## Failure

Users don't know what to do.

### Prevention

One primary action.

---

## Failure

Home feels overwhelming.

### Prevention

Limit visible components.

---

## Failure

AI overshadows scripture.

### Prevention

AI is contextual only.

---

## Failure

Personalization feels unpredictable.

### Prevention

Stable layout.

Consistent hierarchy.

---

## Failure

No internet connection.

### Prevention

Cached content.

Offline reading.

---

# Product Metrics

Primary Metrics

- Home Open
- Continue Journey Click Rate
- Reading Start Rate
- Reflection Completion Rate

Secondary Metrics

- Browse Click Rate
- Home Load Time
- Return Rate

Success is measured by meaningful engagement, not time spent.

---

# Definition of Ready

Before implementation begins:

- Product RFC approved
- User flows reviewed
- Business rules finalized
- Dependencies identified
- Edge cases documented
- Success metrics defined

---

# Definition of Done

The Home System is complete when:

- Users understand what to do within ten seconds.
- Continue Journey functions correctly.
- Home works offline.
- Accessibility requirements pass.
- Analytics events are implemented.
- Performance goals are met.
- No critical defects remain.

---

# Open Questions

Should users be able to customize Home?

Should Today's Reflection be curated, generated, or hybrid?

Should Home adapt based on reading patterns over time?

---

# North Star

Home should never ask:

"What do you want to do?"

Instead, it should quietly answer:

"Here's the most meaningful place to continue your journey."