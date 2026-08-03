# CHAPTER INTERACTION BLUEPRINT

**Experience:** Chapter
**Version:** 1.0
**Status:** Draft
**Owner:** Design
**Last Updated:** August 2026

---

# Mission

The Chapter experience exists to help readers understand the context, purpose, and structure of a chapter before entering individual verses.

Its primary responsibility is to orient readers within a chapter before reading individual verses.

The chapter provides enough context to choose a verse confidently without replacing the act of reading. Scripture always remains the destination.

---

# Modes of Arrival

| Arrival          | Experience Responsibility                                        |
| ---------------- | ---------------------------------------------------------------- |
| Library          | Enter a chapter chosen during discovery.                         |
| Continue Reading | Return to the chapter the reader is currently progressing through. |
| Search           | Arrive directly at a chapter from a known destination.           |
| Verse            | Step back to understand the surrounding chapter.                 |

---

# Reader Mindset

Readers arrive wanting orientation.

Some are beginning a chapter for the first time.

Others are resuming where they previously stopped.

The experience should communicate where this chapter sits and how it is structured, without overwhelming the reader or delaying their reading.

The interface should reward curiosity, not speed.

---

# Success Definition

The experience is successful when the reader:

* understands the chapter's purpose,
* recognizes how the chapter is structured,
* knows where to begin or resume,
* enters a verse with confidence and minimal friction.

---

# Interaction Timeline

## Stage 1 — Orient

### Intent

Establish where the reader is.

### Design Decision

The chapter should immediately communicate its identity and central teaching before presenting a list of verses.

### Components

* Top Navigation
* Chapter Intent

---

## Stage 2 — Understand the Arc

### Intent

Convey the chapter's purpose.

### Design Decision

Provide concise context that helps readers understand the chapter's central idea without replacing the verses themselves.

### Components

* Chapter Intent

---

## Stage 3 — Choose a Verse

### Intent

Help the reader select where to read.

### Design Decision

Present verses in canonical order with quiet orientation about progress, allowing the reader to begin or resume without pressure.

### Components

* Verse Reference
* Reading Progress Indicator

---

## Stage 4 — Begin or Resume

### Intent

Transition the reader into the Verse experience.

### Design Decision

Entering a verse should feel like continuing naturally into the teaching rather than opening another application screen.

### Components

* Continue Reading

---

# Screen Blueprint

```text
────────────────────────────

Top Navigation

────────────────────────────

Chapter 2

Chapter Intent

────────────────────────────

Reading Progress

────────────────────────────

Verse 1

Verse 2

Verse 3

...

────────────────────────────

Continue Reading

────────────────────────────
```

---

# States & Recovery

## First-Time in Chapter

Present the chapter intent and the full verse list from the beginning.

---

## Returning

Surface Continue Reading so the reader can resume the next unread verse without searching.

---

## Offline

Allow access to downloaded verses.

Clearly distinguish unavailable verses without blocking access to what is already available.

---

# Component Extraction

## Reusable Components

* Top Navigation
* Chapter Intent
* Verse Reference
* Reading Progress Indicator
* Continue Reading

---

## Experience Compositions

* Verse List

---

## Open Component Questions

* Should Chapter Intent be expandable into a fuller introduction?
* How much chapter structure aids orientation before it delays reading?

---

# Accessibility Considerations

* Announce the chapter reference and intent before the verse list.
* Preserve canonical verse order for assistive technologies.
* Ensure Continue Reading is reachable without traversing the entire verse list.
* Support Dynamic Type without truncating verse references or chapter intent.

---

# Validation Questions

* Does chapter-level orientation reduce the sense of being overwhelmed before reading?
* Does Chapter Intent aid understanding without replacing the verses?
* Is Continue Reading discoverable when a chapter is only partially read?

---

# Outputs

This Blueprint defines:

* the canonical Chapter experience,
* the transition from discovery into focused reading,
* reusable orientation components,
* experience-level compositions,
* and validation questions for future prototypes.

---

# North Star

The Chapter experience succeeds when readers feel oriented and ready to enter a verse with intention, understanding where a teaching sits within the larger chapter without the interface competing with scripture.
