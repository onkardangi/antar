# Antar Domain Model

**Version:** 1.0  
**Status:** Draft for Architecture Review  
**Owner:** Engineering  
**Last Updated:** August 2026

---

# 1. Purpose

This document defines Antar's business domain.

It identifies:

- Core business entities
- Aggregate boundaries
- Ownership
- Relationships
- Business invariants
- Lifecycle responsibilities

This document intentionally avoids implementation details.

It describes **what the business is**, not **how it is stored**.

---

# 2. Domain Philosophy

Antar is not an AI application.

Antar is a scripture-first learning platform.

Every domain exists to support one stage of the reader's journey.

```text
Read

↓

Reflect

↓

Study

↓

Discuss
```

Every business concept should reinforce this progression.

---

# 3. Bounded Contexts

The platform is divided into independent business domains.

```text
Identity

Scripture

Reading

Reflection

Journey

Guidance

Understanding

Saar

Search

Platform
```

Each domain owns:

- its business rules
- its language
- its data
- its invariants

---

# 4. Identity Domain

## Purpose

Manage reader identity.

---

## Aggregate Root

User

---

### Entities

User

ReadingPreferences

PrivacyPreferences

---

### Responsibilities

User owns:

- profile
- authentication identity
- preferences
- language
- personalization settings

---

### Invariants

A User always has:

- one identity
- one preference profile

Deleting a User removes ownership of personal content according to retention policies.

---

# 5. Scripture Domain

## Purpose

Represent the Bhagavad Gita.

This is Antar's canonical content.

---

## Aggregate Roots

Chapter

Verse

CommentarySource

---

### Chapter

Owns:

- chapter metadata
- ordering
- verse collection

---

### Verse

Owns:

- Sanskrit
- transliteration
- translations
- canonical identifiers

---

### Commentary Source

Represents:

- author
- tradition
- publication metadata

Commentary content references verses.

It never modifies scripture.

---

### Invariants

Verses belong to exactly one chapter.

Canonical scripture is immutable.

---

# 6. Reading Domain

## Purpose

Track reading continuity.

---

## Aggregate Root

ReadingProgress

---

### Entities

ReadingProgress

ReadingSession

Bookmark (optional)

---

### Responsibilities

Owns:

- current verse
- current chapter
- last opened location
- reading history
- continuation state

---

### Invariants

One active reading position per reader.

ReadingProgress references Scripture.

It never owns Scripture.

---

# 7. Reflection Domain

## Purpose

Capture personal reflection.

---

## Aggregate Root

ReflectionEntry

---

### Entities

ReflectionEntry

ReflectionRevision

---

### Types

Quick Reflection

Deep Reflection

Both are represented by one aggregate.

```text
ReflectionType

QUICK

DEEP
```

---

### Responsibilities

Owns:

- reflection text
- timestamps
- revision history
- publication state

---

### Invariants

A reflection always belongs to:

- one User
- one Verse

Reflection cannot exist without Verse context.

---

# 8. Journey Domain

## Purpose

Help readers revisit meaningful moments.

Journey is remembrance.

Not analytics.

---

## Aggregate Root

JourneyMemory

---

### Responsibilities

JourneyMemory represents:

- reflection reference
- verse reference
- revisit metadata
- chronological grouping

---

### Important Decision

JourneyMemory is a projection.

It is derived from:

Reflection

+

Scripture

Journey does not duplicate reflection content.

---

### Invariants

Journey never edits Reflection.

Journey never owns Verse.

---

# 9. Guidance Domain

## Purpose

Guide readers toward deeper study.

---

## Aggregate Root

GuidanceSession

---

### Entities

GuidancePathSelection

---

### Responsibilities

Owns:

- chosen study path
- transition into Understanding
- transition into Saar

---

### Supported Paths

Understand

Connect

Traditional Commentary

Ask Saar

---

### Invariants

Guidance never generates educational content.

It only routes the reader.

---

# 10. Understanding Domain

## Purpose

Present curated educational content.

---

## Aggregate Root

UnderstandingArticle

---

### Entities

KeyConcept

TraditionalInsight

RelatedVerseReference

---

### Responsibilities

Understanding owns:

- explanation
- key ideas
- commentary references
- related verses

---

### Invariants

Understanding content is reviewed.

Understanding distinguishes:

- scripture
- commentary
- editorial explanation

---

### Important Principle

Understanding should remain fully functional without AI.

---

# 11. Saar Domain

## Purpose

Provide conversational study.

---

## Aggregate Root

Conversation

---

### Entities

Message

Citation

RetrievalRecord

---

### Responsibilities

Conversation owns:

- message history
- retrieval context
- citations
- AI responses

---

### Citation

Represents:

- verse references
- commentary references
- grounding information

---

### RetrievalRecord

Represents:

- retrieved passages
- similarity metadata
- ranking metadata

This entity exists for explainability.

---

### Invariants

Every assistant response should reference:

- scripture
- commentary
- or both

Messages never become canonical content.

---

# 12. Search Domain

## Purpose

Locate scripture.

---

## Aggregate Root

SearchRequest

---

### Responsibilities

Owns:

- query parsing
- ranking
- filtering
- result grouping

---

### Search Types

Reference

Keyword

Semantic

---

### Invariants

Search never owns content.

It only discovers content.

---

# 13. Platform Domain

## Purpose

Shared infrastructure.

Examples

Logging

Tracing

Metrics

Caching

Email

Storage

Configuration

Feature Flags

Platform contains no business logic.

---

# 14. Aggregate Relationships

```text
User

├── ReadingProgress

├── ReflectionEntry

├── Conversation

└── Preferences

ReflectionEntry

↓

Verse

↓

Chapter

Conversation

↓

Verse

↓

Citation

↓

Commentary
```

---

# 15. Ownership

```text
Identity

owns User

Reading

owns ReadingProgress

Reflection

owns ReflectionEntry

Journey

owns JourneyMemory

Scripture

owns Chapter

owns Verse

owns CommentarySource

Understanding

owns UnderstandingArticle

Saar

owns Conversation

owns Citation

owns RetrievalRecord
```

No aggregate writes directly into another aggregate.

Communication occurs through application services.

---

# 16. Cross-Domain References

Modules reference aggregates by identity.

Example

ReadingProgress

references

Verse

It does not embed Verse.

Reflection references Verse.

Conversation references Verse.

Journey references Reflection.

Understanding references Verse.

This preserves ownership.

---

# 17. Domain Events

Potential business events.

```text
UserRegistered

VerseOpened

ReadingPositionUpdated

ReflectionCreated

ReflectionUpdated

ReflectionDeleted

JourneyMemoryCreated

GuidancePathChosen

UnderstandingViewed

ConversationStarted

MessageGenerated

ConversationEnded
```

V1 events remain in-process.

---

# 18. Lifecycle Overview

```text
User

↓

Read Verse

↓

ReadingProgress Updated

↓

Reflection Created

↓

Journey Projection Updated

↓

Guidance Selected

↓

Understanding Viewed

↓

Conversation Started

↓

Conversation Completed
```

This represents the canonical learning journey.

---

# 19. Ubiquitous Language

The following terms are canonical across engineering, design, and product.

Reader

Verse

Chapter

Reflection

Journey

Guidance

Understanding

Saar

Conversation

Citation

Reading Progress

Today's Invitation

Commentary

Traditional Insight

Related Verse

These names should remain consistent across:

- APIs
- Documentation
- Code
- UI
- Database
- Analytics

---

# 20. Business Invariants

The following rules define Antar's core behavior.

- Every Verse belongs to one Chapter.
- Every Reflection belongs to one User and one Verse.
- ReadingProgress belongs to one User.
- Journey is derived from Reflection.
- Guidance does not own educational content.
- Understanding precedes Saar.
- Saar never becomes scripture.
- Commentary never modifies scripture.
- AI responses always remain distinguishable from canonical content.
- The Bhagavad Gita remains the primary source of truth.

---

# 21. Future Evolution

Potential future aggregates.

ReadingGoal

Collection

StudyPlan

NotificationPreference

SharedReflection

CommunityDiscussion

VoiceConversation

TeacherProfile

These are intentionally excluded from V1.

---

# 22. Domain Summary

The Antar domain model is intentionally centered around the reader's journey.

Reading establishes context.

Reflection captures personal understanding.

Journey preserves meaningful memories.

Guidance offers learning paths.

Understanding provides curated educational material.

Saar extends the experience through grounded conversation.

Every domain exists to support the reader's engagement with scripture while preserving the distinction between canonical text, traditional interpretation, curated knowledge, and AI-assisted discussion.