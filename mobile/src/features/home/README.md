# Home (Milestone A)

Calm entry point that surfaces local Reading Progress continuity.

## Implemented

- Home as the initial route
- Today's Invitation with two states only:
  - Begin Journey / Begin Reading (no `lastRead`)
  - Continue Reading (exact `lastRead`)
- Browse Bhagavad Gita → Library
- Home-owned invitation loader/interpreter (storage sources stay internal)

Shipped hierarchy:

```text
ScreenHeader
  → Today's Invitation
  → Browse Bhagavad Gita
```

Greeting is **not** rendered in Milestone A (deferred to Milestone B).

## Not implemented (deferred)

- Milestone B: greeting, preview text, time-of-day greeting variants, invitation payload shaping
- Milestone C: Resume Reflection, Curated Teaching, server invitation API
- Auth, sync, AI, Saar, Search, Bookmarks, streaks, tabs, notifications

## Architecture

```text
ReadingProgressRepository.load()
  → loadTodaysInvitation (Home)
  → TodaysInvitationState
  → HomeScreen
```

`HomeScreen` depends only on Home invitation state/actions. It does not import
the repository, AsyncStorage, LocalStorage, or load-source enums.

`ReadingProgressService` public API is unchanged (Verse mutations / collapsed reads).

## Composition

`AppProviders` creates one `createReadingProgressStack()` so Verse and Home
share the same repository instance. Home receives `loadTodaysInvitation` via
`HomeInvitationProvider`.
