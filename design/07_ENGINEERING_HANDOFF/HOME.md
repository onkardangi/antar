# Home Screen

**Status:** Approved for Milestone A (simulator-reviewed)
**Version:** 1.0
**Last Updated:** 2026-08-07
**Source:** Approved Home Experience V1 proposal + iOS simulator review
**Implementation Target:** React Native (Expo)

---

# Purpose

Home is the calm doorway into Antar.

It welcomes the Reader, surfaces local reading continuity, and offers one
obvious next step into scripture — without becoming a dashboard.

---

# Design Principles

- Calm before content.
- One primary action only (Today’s Invitation).
- Browse remains secondary.
- Typography and whitespace create hierarchy — not cards or metrics.
- Continuity is respect, not a scoreboard.
- Storage sources are never product vocabulary on Home.

---

# Screen Hierarchy

```text
ScreenHeader (Antar title; no Back on root)

↓

Hairline Rule

↓

Today’s Invitation
  TODAY’S INVITATION (section heading)
  Chapter N · Verse N
  Verse preview placeholder (quiet lines; no invented scripture)
  Continue Reading → / Begin Reading →

↓

Hairline Rule

↓

Browse Bhagavad Gita →
```

Greeting is **deferred** (Milestone B). It is not rendered on the shipped Home
screen. The section heading frames the invitation instead.

---

# Initial Route Ownership

`RootNavigator` sets `initialRouteName` to `Home` (`ROOT_INITIAL_ROUTE_NAME`).

Primary flows:

```text
Home
  ├── Today’s Invitation → VerseReader
  └── Browse Bhagavad Gita → Library → Chapter → VerseReader
```

Back uses normal stack history:

- Library → Home (when entered from Home)
- Chapter → Library
- VerseReader → previous screen (Home or Chapter)

No bottom tabs. No new app shell.

---

# Invitation States (Milestone A)

Only two productive invitation kinds:

| State | When | Primary action |
| --- | --- | --- |
| Begin Journey | No usable `lastRead` | Begin Reading → Chapter 1 · Verse 1 |
| Continue Reading | Valid `lastRead` | Continue Reading → exact lastRead verse |

Additional UI phases:

| State | When | Behavior |
| --- | --- | --- |
| Loading | Invitation resolving | Structural skeleton in invitation slot only |
| Progress unavailable | Transient progress load failure | Quiet message + Try again; Browse remains |
| Begin unavailable | Canonical 1.1 cannot resolve | Quiet message; Browse remains |

Forbidden in Milestone A:

- Resume Reflection
- Curated Teaching
- Preview text
- Timestamps, %, streaks, history lists
- AI / Saar / Search / Bookmarks / recommendations

---

# Reading Progress Semantics

Home does **not** call `ReadingProgressService` storage-source APIs.

Architecture:

```text
ReadingProgressRepository.load()
  → loadTodaysInvitation (Home-owned)
  → TodaysInvitationState
  → HomeScreen
```

Interpretation rules (inside Home loader only):

- usable `lastRead` → Continue Reading (never furthest)
- missing / corrupt / empty valid document → Begin Journey
- transient `read_error` → progress unavailable (**not** Begin Journey)
- read_error path performs **no** storage write/clear

`ReadingProgressService` public API remains unchanged for Verse mutations and
collapsed reads.

---

# Begin Journey Resolution

Canonical start is resolved through existing clients:

1. `listChapters()` → `chapterNumber === 1`
2. `listChapterVerses(chapterId)` → `verseNumber === 1`

No hardcoded UUIDs. No new backend endpoint.

If resolution fails, invitation shows a quiet unavailable state; Browse stays usable.

---

# Browse Behavior

Label: **Browse Bhagavad Gita**

Opens Library. Does not embed chapter rows on Home. Does not surface Reading
Progress inside Library.

---

# Components

## TodaysInvitation

Home’s sole primary composition. Visual order:

1. Section heading (`TODAY’S INVITATION` via `sectionLabel`)
2. Destination (`Chapter N · Verse N`)
3. Quiet preview placeholder bars (no invented verse text)
4. Action (`Continue Reading →` or `Begin Reading →`) — invitation weight, not a page heading

## BrowseBhagavadGita

Quiet secondary Pressable into Library, labeled `Browse Bhagavad Gita →`.
Preceded by a hairline divider.

---

# Spacing / Typography

Uses design-system tokens:

- `homeSpacing` (shared `screenHeaderSpacing` + Home hierarchy gaps)
- `typography.homeInvitationDestination`
- `typography.homeInvitationAction`
- `typography.homeInvitationContext`
- `typography.homeBrowse`
- `color.background` / `color.text` / `color.textSecondary` / `color.divider`

Horizontal padding: **28px** (shared with Library/Chapter).

Min touch target: **44pt**.

No fixed text heights; Dynamic Type-friendly line heights only.

---

# Loading / Failure

- No full-screen spinner.
- Browse remains visible while the invitation slot loads (structural skeleton
  in the invitation slot only).
- Decorative invitation skeletons are hidden from accessibility.
- Backend/content failures for Verse open remain owned by Verse Reader.
- Home itself stays usable when scripture APIs fail for Begin Journey resolution.

---

# Accessibility Order

1. Application title (ScreenHeader)
2. Today’s Invitation section heading
3. Destination context
4. Primary action (label includes destination)
5. Browse Bhagavad Gita

Example primary labels:

- `Continue Reading. Opens Chapter 1, Verse 12.`
- `Begin Reading. Opens Chapter 1, Verse 1.`

---

# Simulator Observations (2026-08-07)

Device: iPhone 16 Pro simulator via Expo Go. Backend: `localhost:8082`.

**Milestone A functional review**

- App opens on Home (not Library).
- Cleared progress → Begin Reading for Chapter 1 · Verse 1.
- Seeded `lastRead` Verse 12 with furthest Verse 40 → Continue Reading for Chapter 1 · Verse 12 (lastRead, not furthest).

**Visual alignment pass**

- No Greeting on Home; `TODAY’S INVITATION` section heading is the frame.
- Destination (`Chapter N · Verse N`) leads; action is `Continue Reading →` / `Begin Reading →`.
- Quiet preview placeholder bars reserve verse-preview space (no invented scripture).
- Hairline divider precedes `Browse Bhagavad Gita →`.
- Increased vertical whitespace matches Figma invitation hierarchy.

Expo Go may show a floating developer Settings control — **not** part of product Home.

Not claimed: physical-device review.

---

# Deferred (Milestone B / C)

**Milestone B**

- Greeting (atmosphere copy; not a competing CTA)
- Compact scripture preview
- Time-of-day greeting variants
- Stronger stale-destination recovery polish

**Milestone C**

- Resume Reflection invitation state
- Server Reading Progress + Today’s Invitation API
- Curated Teaching state
- Auth / sync

---

# Implementation Notes

Feature root: `mobile/src/features/home/`

Key files:

- `screens/HomeScreen.tsx`
- `application/loadTodaysInvitation.ts`
- `application/interpretProgressLoad.ts`
- `api/resolveCanonicalStart.ts`
- `composition/HomeInvitationProvider.tsx`

Shared stack composition: `createReadingProgressStack()` in AppProviders so Verse
and Home share one repository without expanding the service public API.
