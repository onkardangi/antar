# Antar MVP Implementation Plan

**Version:** 1.0  
**Status:** Draft for Architecture Review  
**Owner:** Engineering  
**Last Updated:** August 2026

---

# 1. Purpose

This document converts Antar’s approved product, design, domain, API, AI, data, security, deployment, and repository decisions into an executable MVP implementation plan.

It defines:

- implementation phases,
- vertical slices,
- dependencies,
- deliverables,
- acceptance criteria,
- required tests,
- deferred work,
- milestone exit conditions,
- and the recommended build order.

The plan is intentionally structured around end-to-end product capabilities rather than isolated backend, mobile, or database work.

Antar V1 consists of:

```text
Spring Boot Backend

+

React Native / Expo Mobile Application
```

A web client is outside the current V1 scope.

---

# 2. Implementation Philosophy

## 2.1 Build Vertically

Each phase should produce a working Reader experience across:

```text
Database
    ↓
Backend Domain
    ↓
Application Use Case
    ↓
HTTP API
    ↓
Mobile Integration
    ↓
Reader Experience
```

Avoid building:

- every database table first,
- every backend module first,
- or every mobile screen first

without end-to-end validation.

---

## 2.2 Validate Architecture Through Delivery

Architecture documents provide direction.

Implementation should validate whether those decisions work in practice.

When implementation reveals a meaningful architectural issue:

1. pause,
2. document the conflict,
3. update the relevant architecture document or ADR,
4. then continue.

Do not silently diverge from approved decisions.

---

## 2.3 Start With the Smallest Complete Product Loop

The first complete product slice is:

```text
Library
    ↓
Chapter
    ↓
Verse
```

This validates:

- canonical content storage,
- Flyway,
- PostgreSQL,
- backend module boundaries,
- API contracts,
- mobile navigation,
- API integration,
- the mobile design system,
- and the repository structure.

---

## 2.4 Delay Optional Infrastructure

Do not begin with:

- Kafka,
- microservices,
- multi-agent systems,
- Kubernetes,
- dedicated vector databases,
- advanced recommendation systems,
- or full offline synchronization.

Introduce complexity only when an approved product capability requires it.

---

## 2.5 Core Product Before AI

The build sequence remains:

```text
Read
    ↓
Reflect
    ↓
Study
    ↓
Discuss
```

Saar is implemented only after:

- Scripture,
- Reading,
- Reflection,
- Journey,
- Guidance,
- and Understanding

are functional.

---

# 3. MVP Scope

## 3.1 Included

The MVP includes:

- Reader authentication,
- mobile application for iOS and Android,
- Chapter browsing,
- Verse browsing,
- Sanskrit display,
- Transliteration display,
- Translation display,
- Reading Progress,
- Today’s Invitation,
- Quick Reflection,
- Deep Reflection,
- local draft preservation,
- Reflection autosave,
- Journey timeline,
- Guidance,
- Curated Understanding,
- Traditional Insights,
- Related Verses,
- basic Search,
- Saar Conversations,
- grounded Citations,
- privacy preferences,
- account deletion,
- basic data export,
- structured logs,
- metrics,
- tracing,
- backups,
- and a production-ready deployment baseline.

---

## 3.2 Deferred

The following are deferred:

- web application,
- social features,
- public Reflection sharing,
- community discussion,
- streaks,
- badges,
- progress scoring,
- advanced recommendations,
- push notifications unless later approved,
- full offline multi-device synchronization,
- voice input,
- voice conversations,
- multi-agent AI,
- autonomous tool use,
- model fine-tuning,
- dedicated search cluster,
- dedicated vector database,
- Kafka,
- microservices,
- Kubernetes,
- multi-region active-active deployment,
- and advanced administrative portals.

---

# 4. Delivery Structure

The MVP is divided into the following phases:

```text
Phase 0
Repository and Runtime Foundation

Phase 1
Scripture Vertical Slice

Phase 2
Reading Continuity and Home

Phase 3
Reflection

Phase 4
Journey

Phase 5
Guidance and Understanding

Phase 6
Search

Phase 7
Saar Foundation

Phase 8
RAG and Grounding

Phase 9
Security, Privacy, and Operations

Phase 10
Release Readiness
```

Each phase has explicit exit criteria.

---

# 5. Phase 0 — Repository and Runtime Foundation

## Objective

Create a reproducible development environment and establish enforceable backend and mobile architecture boundaries.

---

## Backend Deliverables

Create:

```text
backend/
```

### Completed in the initial repository foundation

```text
Java 21
Spring Boot
Maven
Spring Web
Spring Data JPA
Flyway
PostgreSQL Driver
pgvector support
Redis support
Testcontainers
ArchUnit
```

### Deferred Phase 0 hardening

These remain part of the broader Phase 0 / pre-production hardening track and are **not** required to mark the current uncommitted bootstrap complete:

```text
Spring Validation
Spring Security
OpenTelemetry foundation
dependency scanning
secret scanning
```

Guidance for when to add them:

- Spring Validation is added with the first request DTO that requires Bean Validation.
- Spring Security is added with Reader authentication in Phase 2.
- OpenTelemetry is added during the observability foundation or before staging deployment.
- Dependency and secret scanning are required before the first production deployment.

Do not mark deferred hardening items as completed merely because the repository foundation exists.

Create the initial package structure:

```text
com.antar
├── identity
├── scripture
├── reading
├── reflection
├── journey
├── guidance
├── understanding
├── saar
├── search
├── platform
└── shared
```

Create only:

- the Spring Boot entry point,
- module marker classes,
- module README files,
- architecture tests,
- and essential Platform configuration.

Do not create empty Controllers, Services, Repositories, or Entities for every future module.

---

## Mobile Deliverables

Create:

```text
mobile/
```

Initialize:

```text
React Native
TypeScript
Expo
```

Create the initial source structure:

```text
mobile/src/
├── app
├── navigation
├── features
├── design-system
├── services
├── shared
├── storage
└── test
```

Create:

- root providers,
- application bootstrap,
- error boundary,
- initial navigation shell,
- environment configuration,
- API client foundation,
- secure-storage abstraction,
- and test rendering utilities.

Do not build all future screens yet.

---

## Infrastructure Deliverables

Create local infrastructure using Docker Compose:

```text
PostgreSQL
pgvector
Redis
```

Optional local services:

- AI mock server,
- object-storage emulator.

Add:

```text
compose.yaml
```

Provide one documented local startup path.

Example:

```text
docker compose up
```

---

## CI Deliverables

Create initial workflows for:

### Backend

Completed in the initial repository foundation:

- compile,
- unit tests,
- integration tests,
- architecture tests,
- migration validation through Testcontainers-backed Flyway checks.

Deferred until pre-production hardening:

- dependency scan,
- secret scan.

### Mobile

- TypeScript check,
- lint,
- unit tests,
- component tests,
- Expo configuration validation.

---

## Required Tests

### Backend

- Spring application context starts.
- Architecture tests pass.
- PostgreSQL Testcontainer starts.
- Flyway migrations execute.
- Redis connectivity can be tested where enabled.
- Production packages obey dependency rules.

### Mobile

- application bootstrap renders,
- root navigation renders,
- API error mapping works,
- secure-storage abstraction can be mocked,
- TypeScript strict mode passes.

---

## Acceptance Criteria

Phase 0 is complete when:

- a new developer can clone the repository,
- start PostgreSQL and Redis,
- start the Spring Boot backend,
- start the Expo mobile application,
- run all tests,
- and understand the repository structure from documentation.

No product feature is required yet.

---

## Explicitly Deferred

- real authentication,
- Scripture tables,
- production deployment,
- Saar,
- vector search,
- detailed observability dashboards,
- Spring Security until Reader authentication,
- Spring Validation until the first validated request DTO,
- OpenTelemetry until observability foundation / staging readiness,
- dependency and secret scanning until pre-production hardening.

---

# 6. Phase 1 — Scripture Vertical Slice

## Objective

Deliver the first complete end-to-end Reader experience:

```text
Library
    ↓
Chapter
    ↓
Verse
```

---

## Domain Scope

Implement the Scripture module.

Core concepts:

```text
Chapter
Verse
CanonicalReference
TranslationSource
Translation
Transliteration
```

Commentary may remain deferred until the Understanding phase.

---

## Database Deliverables

Create Flyway migrations for:

```text
scripture.chapters
scripture.verses
scripture.transliterations
scripture.translation_sources
scripture.translations
```

Enforce:

- 18 Chapter range,
- canonical Chapter order,
- Verse uniqueness within Chapter,
- canonical reference uniqueness,
- Translation attribution,
- publication state,
- and content versioning.

---

## Content Deliverables

Import a small approved test corpus first.

Recommended development corpus:

```text
Chapter 1
Chapter 2
A representative subset of Verses
At least one Transliteration
At least one Translation
```

After the import path is stable, expand to all approved canonical Scripture content.

Do not import unlicensed Translation content.

---

## Backend Deliverables

Implement:

```text
GET /api/v1/scripture/chapters

GET /api/v1/scripture/chapters/{chapterId}

GET /api/v1/scripture/chapters/by-number/{chapterNumber}

GET /api/v1/scripture/chapters/{chapterId}/verses

GET /api/v1/scripture/verses/{verseId}

GET /api/v1/scripture/verses/by-reference/{reference}

GET /api/v1/scripture/translation-sources
```

Implement:

- canonical-reference parser,
- Chapter query service,
- Verse query service,
- Translation selection,
- previous and next Verse resolution,
- and publication filtering.

---

## Mobile Deliverables

Implement the approved:

```text
Library Screen
Chapter Screen
Verse Screen
```

Create mobile features:

```text
features/library
features/chapter
features/verse
```

Implement navigation:

```text
Library
    ↓
Chapter
    ↓
Verse
```

Implement:

- loading states,
- empty states,
- API failure states,
- canonical ordering,
- Sanskrit visibility,
- Transliteration visibility,
- Translation display,
- previous and next Verse navigation,
- and mobile accessibility.

---

## Design-System Deliverables

Create only the components needed for the slice.

Potential primitives and components:

```text
ScreenContainer
Text
Stack
Divider
PressableText
VerseReference
ChapterListItem
ScriptureSection
LoadingState
ErrorState
```

Avoid prematurely creating an exhaustive component library.

---

## Required Backend Tests

### Domain

- valid Chapter numbers,
- valid Verse references,
- CanonicalReference parsing,
- Chapter-to-Verse ownership.

### Persistence

- uniqueness constraints,
- canonical ordering,
- publication filtering,
- Translation attribution,
- navigation queries.

### API

- Chapter list,
- Chapter detail,
- Verse list,
- Verse detail,
- canonical reference resolution,
- invalid reference behavior,
- missing published content.

---

## Required Mobile Tests

- Library renders Chapters in canonical order.
- Selecting a Chapter opens Chapter.
- Selecting a Verse opens Verse.
- Verse renders Sanskrit, Transliteration, and Translation.
- Previous and next navigation work.
- accessibility semantics are present.
- network error produces a recoverable state.

---

## Acceptance Criteria

Phase 1 is complete when a Reader can:

1. open the mobile app,
2. browse the Library,
3. open a Chapter,
4. open a Verse,
5. read approved Scripture content,
6. move to the previous or next Verse,
7. and recover from normal loading and network failures.

The complete flow must use real backend APIs and PostgreSQL.

---

## Explicitly Deferred

- authentication,
- Reading Progress,
- Home,
- Reflection,
- Journey,
- Search,
- Commentary,
- Saar.

---

# 7. Phase 2 — Reading Continuity and Home

## Objective

Allow the Reader to resume reading through one calm primary Home action.

---

## Domain Scope

Implement:

```text
ReadingProgress
ReadingPosition
VerseOpened
TodayInvitation
```

Today’s Invitation remains a derived application result.

---

## Database Deliverables

Create:

```text
reading.reading_progress
reading.verse_visits
```

Reading Sessions may be deferred unless they are required for the approved product behavior.

Enforce:

```text
One Reading Progress record per Reader
```

---

## Authentication Foundation

Introduce Reader authentication before persisting private Reading Progress.

Implement:

- authentication-provider integration or approved temporary local identity,
- Reader resolution,
- protected Reader APIs,
- and mobile secure token storage.

If the final external provider is not selected, use an internal development adapter that preserves the intended identity boundary.

---

## Backend Deliverables

Implement:

```text
GET /api/v1/reading/progress

PUT /api/v1/reading/progress

POST /api/v1/reading/verse-opens

GET /api/v1/invitations/today
```

Initial Today’s Invitation states:

```text
BEGIN_JOURNEY
CONTINUE_READING
```

`RESUME_REFLECTION` is added in the Reflection phase.

`CURATED_TEACHING` may be added after Understanding exists.

---

## Mobile Deliverables

Implement:

```text
Home Screen
```

Use the approved hierarchy:

```text
Top Navigation
    ↓
Today’s Invitation
    ↓
Browse Bhagavad Gita
```

Implement:

- new Reader state,
- returning Reader state,
- Continue Reading,
- Begin Journey,
- Browse Bhagavad Gita,
- and reading-position restoration.

Do not add a separate Continue Journey section.

---

## Required Backend Tests

- one Reading Progress record per Reader,
- cross-user isolation,
- stale version handling,
- Verse open updates progress,
- invalid Verse rejected,
- new Reader invitation,
- returning Reader invitation,
- one invitation returned only.

---

## Required Mobile Tests

- new Reader sees Begin Journey,
- returning Reader sees Continue Reading,
- action opens correct Verse,
- Browse Bhagavad Gita opens Library,
- reading position restores after restart,
- stale or missing destination recovers safely.

---

## Acceptance Criteria

Phase 2 is complete when:

- a Reader can authenticate,
- open a Verse,
- leave the app,
- reopen it,
- and resume from Home through Today’s Invitation.

Home must retain one obvious primary action.

---

## Explicitly Deferred

- Resume Reflection state,
- Curated Teaching state,
- Bookmarks,
- notifications,
- reading analytics,
- streaks.

---

# 8. Phase 3 — Reflection

## Objective

Support immediate thought capture and optional deeper journaling.

---

## Domain Scope

Implement:

```text
ReflectionEntry
ReflectionType
ReflectionContent
ReflectionStatus
```

Types:

```text
QUICK
DEEP
```

Use one aggregate and one primary persistence model.

---

## Database Deliverables

Create:

```text
reflection.reflection_entries
```

Optional:

```text
reflection.reflection_revisions
```

Recommended V1 behavior:

- one Quick Reflection per Reader and Verse,
- multiple Deep Reflections allowed,
- optional origin relationship from Deep to Quick,
- optimistic locking,
- hard deletion.

---

## Backend Deliverables

Implement:

```text
POST /api/v1/reflections

GET /api/v1/reflections

GET /api/v1/reflections/{reflectionId}

PUT /api/v1/reflections/{reflectionId}

DELETE /api/v1/reflections/{reflectionId}

POST /api/v1/reflections/{reflectionId}/expand
```

Implement:

- idempotent creation,
- ownership,
- validation,
- optimistic concurrency,
- expand Quick into Deep,
- and save-state response.

Update Today’s Invitation to support:

```text
RESUME_REFLECTION
```

when an approved unfinished Deep Reflection exists.

---

## Mobile Deliverables

Refine Verse to include:

```text
Quick Reflection
Reflect More
Continue Reading
```

Implement the dedicated:

```text
Reflection Screen
```

Implement:

- short Quick Reflection input,
- Deep Reflection editor,
- local draft persistence,
- autosave,
- local versus server save status,
- safe conflict recovery,
- delete Reflection,
- and Continue Reading.

---

## Local Storage Deliverables

Implement:

```text
reflectionDraftStorage
```

Define:

- Reader ownership,
- Verse scope,
- Reflection type,
- local version,
- updated time,
- server resource ID where available,
- deletion behavior,
- and storage migrations.

---

## Required Backend Tests

- Quick Reflection uniqueness,
- multiple Deep Reflections allowed,
- origin belongs to same Reader,
- origin references same Verse,
- cross-user isolation,
- optimistic-lock conflict,
- idempotent creation,
- delete behavior,
- expansion does not delete Quick Reflection.

---

## Required Mobile Tests

- Quick Reflection can be saved from Verse.
- Reflect More opens Deep Reflection.
- local draft survives app restart.
- save status changes correctly.
- offline save remains visibly local.
- server conflict preserves local text.
- Continue Reading returns to correct Verse flow.
- delete removes local and server state.

---

## Acceptance Criteria

Phase 3 is complete when a Reader can:

1. read a Verse,
2. capture one quick thought,
3. optionally expand into a deeper Reflection,
4. leave and reopen the app without losing an unsaved draft,
5. persist the Reflection safely,
6. and resume an unfinished Reflection from Home.

---

## Explicitly Deferred

- AI rewriting,
- Reflection analysis,
- sentiment detection,
- public sharing,
- collaboration,
- advanced revision history unless approved.

---

# 9. Phase 4 — Journey

## Objective

Allow Readers to revisit previous Reflections as memory rather than progress analytics.

---

## Domain Scope

Implement Journey as a read projection.

Concept:

```text
JourneyMemory
```

Derived from:

```text
Reflection
+
Scripture
```

---

## Persistence Decision

Do not create a dedicated Journey table initially.

Build Journey from:

- Reflection entries,
- Verse context,
- chronological grouping.

Add a materialized projection only if measured performance requires it.

---

## Backend Deliverables

Implement:

```text
GET /api/v1/journey/memories
```

Support:

- reverse chronological ordering,
- monthly grouping,
- pagination,
- Verse filtering where approved,
- Reflection preview,
- and source identifiers.

Journey must update automatically when a Reflection is:

- created,
- edited,
- or deleted.

---

## Mobile Deliverables

Implement the approved:

```text
Journey Screen
```

Include:

- quiet introduction,
- month grouping,
- date,
- Verse reference,
- Reflection preview,
- reopen behavior,
- Continue Reading.

Do not add:

- charts,
- streaks,
- completion percentages,
- achievements,
- or spiritual scoring.

---

## Required Backend Tests

- Reader sees only their Journey,
- monthly grouping is correct,
- ordering is correct,
- deleted Reflection disappears,
- edited Reflection preview updates,
- pagination remains stable.

---

## Required Mobile Tests

- groups render in correct order,
- Reflection preview opens full Reflection,
- deleted content disappears after refresh,
- empty Journey state is calm and useful,
- Continue Reading opens current position.

---

## Acceptance Criteria

Phase 4 is complete when a Reader can revisit private Reflections grouped over time and reopen any Reflection safely.

Journey must feel like memory, not analytics.

---

# 10. Phase 5 — Guidance and Understanding

## Objective

Provide a structured study path after reading and reflection without requiring runtime AI.

---

## Domain Scope

Implement:

```text
GuidanceSession
GuidancePath
GuidanceSelection

UnderstandingArticle
KeyConcept
TraditionalInsight
RelatedVerse
PublicationStatus
```

---

## Database Deliverables

Create:

```text
guidance.guidance_sessions
guidance.path_selections

understanding.articles
understanding.key_concepts
understanding.traditional_insights
understanding.related_verses
```

Create Commentary storage if not already present:

```text
scripture.commentary_sources
scripture.commentary_passages
```

Enforce:

- publication workflow,
- source attribution,
- licensing metadata,
- content versioning,
- and published-only Reader access.

---

## Content Deliverables

Create a limited reviewed Understanding corpus.

Start with a small number of representative Verses.

Each published Understanding should include:

- explanation,
- Key Ideas,
- at least one source-aware Traditional Insight where available,
- and Related Verses.

Do not claim full coverage until the reviewed corpus exists.

---

## Backend Deliverables

Implement:

```text
POST /api/v1/guidance/sessions

GET /api/v1/guidance/sessions/{sessionId}

POST /api/v1/guidance/sessions/{sessionId}/selections

GET /api/v1/understanding/verses/{verseId}

GET /api/v1/understanding/verses/{verseId}/commentaries

GET /api/v1/understanding/verses/{verseId}/related-verses
```

Guidance returns a destination.

It does not generate educational content.

---

## Mobile Deliverables

Implement:

```text
Guidance Screen
Understanding Screen
```

Guidance paths:

```text
Understand this Verse

Connect with Other Teachings

Learn from Traditional Commentaries

Ask Saar
```

Keep Ask Saar visually secondary.

Understanding should include:

```text
Verse Context
Understanding
Key Ideas
Traditional Insight
Related Verses
Still Have Questions?
Ask Saar
```

---

## Required Backend Tests

- only published Understanding returned,
- draft content excluded,
- Commentary attribution required,
- license-restricted content handled,
- Related Verse uniqueness,
- Guidance ownership,
- Guidance path validation,
- destination mapping.

---

## Required Mobile Tests

- Guidance displays approved paths.
- Understand path opens Understanding.
- Commentary path loads Commentary.
- Related Teaching path opens related Verse content.
- missing Understanding produces a clear state.
- Ask Saar remains available but secondary.

---

## Acceptance Criteria

Phase 5 is complete when a Reader can:

1. finish reading,
2. choose a study direction,
3. view reviewed Understanding,
4. inspect attributed Commentary,
5. open Related Verses,
6. and complete the study flow without runtime AI.

---

## Explicitly Deferred

- live content generation,
- automatic Understanding fallback,
- personalized recommendations,
- unreviewed generated commentary,
- advanced editorial portal.

---

# 11. Phase 6 — Search

## Objective

Provide intentional access to Scripture through canonical and keyword search.

---

## Domain Scope

Implement:

```text
CanonicalReferenceResolver
SearchRequest
SearchResult
KnowledgeSource projection
```

Vector retrieval remains deferred until the RAG phase.

---

## Backend Deliverables

Implement:

```text
GET /api/v1/search/references/resolve

GET /api/v1/search/scripture
```

Initial Search supports:

- canonical references,
- Chapter names,
- Verse keywords,
- Translation text,
- published Understanding text where approved.

Use:

```text
PostgreSQL Full-Text Search
```

---

## Search Projection Deliverables

Create:

```text
search.knowledge_sources
search.knowledge_chunks
```

Initial projections may cover:

- Verse,
- Translation,
- Understanding,
- Commentary where licensed and approved.

Create full-text vectors and GIN indexes.

---

## Mobile Deliverables

Implement:

```text
Search Screen
Search Results
```

Support:

- search input,
- canonical reference resolution,
- Verse result,
- Chapter result,
- Understanding result where approved,
- empty state,
- and direct navigation.

Search should remain secondary to Library.

---

## Required Backend Tests

- reference variants resolve,
- invalid reference does not misresolve,
- keyword matching,
- publication filtering,
- attribution preservation,
- result-type identity,
- pagination,
- private data exclusion.

---

## Required Mobile Tests

- reference search opens correct Verse,
- keyword result opens destination,
- empty results display calmly,
- loading and retry behavior work,
- no private Reflection content appears.

---

## Acceptance Criteria

Phase 6 is complete when a Reader can intentionally locate Scripture or approved study material by reference or keyword.

---

## Explicitly Deferred

- personalized ranking,
- search history,
- advanced filters,
- vector-only Search,
- web search,
- open internet retrieval.

---

# 12. Phase 7 — Saar Foundation

## Objective

Implement the durable Conversation lifecycle and provider-neutral AI boundary before advanced RAG.

---

## Domain Scope

Implement:

```text
Conversation
Message
MessageRole
GenerationRun
Citation
GroundingStatus
```

Conversations are Verse-scoped by default.

---

## Database Deliverables

Create:

```text
saar.conversations
saar.messages
saar.citations
saar.generation_runs
saar.retrieval_runs
saar.retrieval_results
```

Initial Retrieval records may remain limited until RAG is implemented.

---

## Backend Deliverables

Implement:

```text
POST /api/v1/saar/conversations

GET /api/v1/saar/conversations

GET /api/v1/saar/conversations/{conversationId}

DELETE /api/v1/saar/conversations/{conversationId}

GET /api/v1/saar/conversations/{conversationId}/messages

POST /api/v1/saar/conversations/{conversationId}/messages

GET /api/v1/saar/generations/{generationId}

POST /api/v1/saar/generations/{generationId}/retry

POST /api/v1/saar/conversations/{conversationId}/close
```

---

## AI Provider Abstraction

Create an internal port such as:

```text
LlmGateway
```

Create two implementations:

```text
MockLlmGateway
RealProviderLlmGateway
```

Begin with the mock implementation for deterministic development.

The provider integration should support:

- timeout,
- usage metadata,
- structured output,
- safe error mapping,
- and model configuration.

---

## Background Processing

Implement durable asynchronous generation using PostgreSQL-backed work.

Flow:

```text
Persist Reader Message
    ↓
Create Generation Run
    ↓
Worker Claims Run
    ↓
Load Context
    ↓
Generate
    ↓
Validate
    ↓
Persist Saar Message
```

Do not hold the original HTTP request open for the provider call.

---

## Initial Grounding

Before full hybrid RAG, use a bounded approved context:

```text
Current Verse
Selected Translation
Published Understanding
Direct Commentary
Curated Related Verses
```

This allows grounded Conversation before vector retrieval.

---

## Mobile Deliverables

Implement:

```text
Saar Conversation Screen
```

The screen should include:

- Verse context,
- existing Messages,
- Reader input,
- generation status,
- citations,
- retryable failure,
- and return-to-Scripture behavior.

Avoid:

- generic AI branding,
- avatars,
- prompt carousels,
- aggressive suggested questions,
- and open-ended assistant framing.

---

## Required Backend Tests

- Conversation ownership,
- closed Conversation rejects Messages,
- idempotent Message submission,
- Generation state transitions,
- worker claim safety,
- provider timeout,
- retry classification,
- Message ordering,
- Citation ownership,
- deletion,
- private Reflection context disabled by default.

---

## Required Mobile Tests

- start Conversation from Guidance or Understanding,
- submit Message,
- display pending state,
- poll Generation,
- render final Message,
- render Citations,
- retry failure,
- close Conversation,
- preserve prior Messages.

---

## Acceptance Criteria

Phase 7 is complete when a Reader can ask Saar a question about the current Verse and receive a structured, source-aware response through the durable asynchronous pipeline.

The response may use only canonical and curated direct context at this stage.

---

## Explicitly Deferred

- vector retrieval,
- advanced reranking,
- streaming,
- provider fallback,
- conversation summarization,
- autonomous tools.

---

# 13. Phase 8 — RAG and Grounding

## Objective

Add hybrid retrieval, source versioning, embeddings, reranking, and stronger Citation validation.

---

## Data Deliverables

Complete:

```text
search.knowledge_sources
search.knowledge_chunks
search.knowledge_embeddings
```

Add:

- content hashes,
- chunking version,
- embedding model,
- embedding policy version,
- corpus version,
- retrieval policy version.

---

## Indexing Deliverables

Implement jobs for:

```text
Project Knowledge Source
Normalize
Chunk
Build Full-Text Vector
Generate Embedding
Validate
Activate Projection
Retire Prior Projection
```

Index only:

- approved,
- licensed,
- published,
- attributable content.

Exclude all private Reader content.

---

## Retrieval Deliverables

Implement:

```text
Exact Retrieval
Curated Relationship Retrieval
Full-Text Retrieval
Vector Retrieval
Deduplication
Score Normalization
Deterministic Reranking
Prompt Source Selection
```

Canonical Verse resolution must always precede semantic retrieval.

---

## Citation Deliverables

Implement:

- prompt-local source identifiers,
- durable source mapping,
- source-version preservation,
- canonical-reference validation,
- attribution validation,
- and grounding-status calculation.

Initial grounding statuses:

```text
GROUNDED
PARTIALLY_GROUNDED
UNGROUNDED
VALIDATION_FAILED
```

Do not deliver a normal Saar answer when the response is ungrounded.

---

## Evaluation Deliverables

Create a versioned evaluation dataset.

Include:

- exact Verse questions,
- Verse meaning,
- term definition,
- Commentary questions,
- named tradition,
- Related Verses,
- ambiguous questions,
- unsupported questions,
- and no-grounding cases.

Measure:

```text
Exact Reference Accuracy
Required Source Inclusion
Prohibited Source Rate
Recall at K
Precision at K
Citation Correctness
Grounding Status
Latency
Cost
```

---

## Required Tests

### Indexing

- idempotent projection,
- source publication filtering,
- content-hash changes trigger rebuild,
- embeddings match model and dimension,
- retired sources are excluded.

### Retrieval

- exact reference outranks semantic match,
- curated Related Verse outranks inferred match,
- wrong-language sources excluded,
- named Commentary resolved correctly,
- duplicate chunks removed,
- no private Reflection enters shared retrieval.

### Citation

- unknown prompt source rejected,
- incorrect canonical reference rejected,
- source version preserved,
- unsupported claim lowers grounding status.

---

## Acceptance Criteria

Phase 8 is complete when Saar can:

1. resolve canonical context,
2. retrieve approved supporting sources,
3. combine exact, full-text, vector, and curated signals,
4. select a bounded source set,
5. generate a structured response,
6. validate Citations,
7. and expose a trustworthy grounding status.

---

## Explicitly Deferred

- learned reranker,
- graph RAG,
- open-web Search,
- multi-agent retrieval,
- automated content publication,
- personalized embedding memory.

---

# 14. Phase 9 — Security, Privacy, and Operations

## Objective

Complete the controls required for safe production use.

---

## Identity and Authorization Deliverables

Finalize:

- authentication provider,
- token validation,
- Reader account resolution,
- secure mobile token storage,
- administrator role separation,
- and ownership enforcement.

---

## Privacy Deliverables

Implement:

```text
Reading Preferences
Privacy Preferences
Reflection AI Context Setting
Conversation Retention
Account Deletion
Conversation Deletion
Reflection Deletion
Data Export
```

Defaults:

```text
Reflection AI Context = OFF
Search History = Not Retained
Private Reader Content = Not Training Data
```

---

## Rate Limiting

Add limits for:

- authentication,
- Reflection mutation,
- Search,
- Saar Conversation,
- retry,
- and export generation.

---

## Audit Deliverables

Implement safe audit events for:

- privacy preference changes,
- account deletion,
- export request,
- content publication,
- administrative login,
- feature-flag change,
- and provider configuration change.

Do not include full private content.

---

## Observability Deliverables

Implement:

```text
Structured JSON Logs
OpenTelemetry Traces
Metrics
Correlation IDs
Health Checks
Dependency Health
```

Create dashboards for:

- product flow,
- API health,
- Reflection durability,
- AI health,
- retrieval health,
- worker health,
- database health,
- and cost.

---

## Alerting Deliverables

Create alerts for:

- core API availability,
- Reflection save failures,
- PostgreSQL failure,
- backup failure,
- cross-user authorization failure,
- worker backlog,
- provider outage,
- grounding failure spike,
- Citation validation failure spike,
- and AI budget breach.

---

## Backup and Recovery Deliverables

Implement:

- automated PostgreSQL backups,
- point-in-time recovery where supported,
- backup encryption,
- restore procedure,
- restore test,
- search-index rebuild procedure,
- and application rollback procedure.

---

## Deployment Deliverables

Implement:

- backend container build,
- API and Worker process roles,
- staging deployment,
- production deployment,
- managed secrets,
- backward-compatible migrations,
- rolling deployment,
- mobile preview build,
- mobile production build,
- and release metadata.

---

## Required Security Tests

- cross-user Reflection access,
- cross-user Conversation access,
- cross-user export access,
- Reflection context opt-in,
- deleted data inaccessible,
- private content absent from logs,
- private content absent from shared retrieval,
- admin routes protected,
- prompt injection does not alter authorization,
- mobile bundle contains no privileged secrets.

---

## Acceptance Criteria

Phase 9 is complete when the system has:

- production authentication,
- private-data ownership controls,
- deletion,
- export,
- privacy preferences,
- rate limits,
- auditability,
- backups,
- restore testing,
- observability,
- alerts,
- and safe deployment workflows.

---

# 15. Phase 10 — Release Readiness

## Objective

Validate the complete V1 product and operating model before broader release.

---

## End-to-End Reader Journeys

Validate:

### Journey A — New Reader

```text
Install App
    ↓
Create Account
    ↓
Open Home
    ↓
Begin Journey
    ↓
Browse Chapter
    ↓
Read Verse
```

### Journey B — Returning Reader

```text
Open App
    ↓
Today’s Invitation
    ↓
Continue Reading
```

### Journey C — Quick Reflection

```text
Read Verse
    ↓
Capture Quick Reflection
    ↓
Continue Reading
```

### Journey D — Deep Reflection

```text
Read Verse
    ↓
Reflect More
    ↓
Write Deep Reflection
    ↓
Close App
    ↓
Resume Reflection
```

### Journey E — Journey

```text
Open Journey
    ↓
Browse Month
    ↓
Reopen Reflection
```

### Journey F — Study

```text
Read Verse
    ↓
Guidance
    ↓
Understanding
    ↓
Traditional Insight
    ↓
Related Verse
```

### Journey G — Saar

```text
Read
    ↓
Reflect
    ↓
Study
    ↓
Ask Saar
    ↓
Receive Grounded Response
    ↓
Open Citation
    ↓
Return to Scripture
```

---

## Quality Review

Review:

- typography,
- spacing,
- accessibility,
- navigation,
- empty states,
- loading states,
- offline behavior,
- autosave,
- privacy copy,
- Citation presentation,
- and error recovery.

---

## Content Review

Before release, verify:

- Scripture accuracy,
- Translation attribution,
- Commentary attribution,
- Understanding review,
- licensing,
- Related Verse curation,
- and representative Saar responses.

Qualified content review is required.

---

## Performance Review

Test:

- Chapter and Verse load,
- Reflection save,
- Journey query,
- Search,
- Saar request acceptance,
- retrieval,
- generation,
- and mobile startup.

---

## Reliability Review

Test:

- Redis outage,
- AI-provider outage,
- vector retrieval failure,
- worker restart,
- backend rolling deployment,
- database failover where supported,
- mobile network loss,
- Reflection conflict,
- and restore procedure.

---

## Security Review

Complete:

- dependency scan,
- secret scan,
- authorization review,
- prompt-injection test,
- logging review,
- data-export review,
- account-deletion verification,
- and external security assessment when appropriate.

---

## App Distribution Review

Complete:

- iOS signing,
- Android signing,
- privacy disclosures,
- store metadata,
- screenshots,
- support contact,
- release notes,
- and staged rollout plan.

---

## Acceptance Criteria

V1 is release-ready when:

- all critical Reader journeys pass,
- core reading works without AI,
- private writing survives normal failure conditions,
- Saar responses meet grounding quality thresholds,
- content is approved and licensed,
- production recovery is tested,
- no critical security issues remain,
- and the mobile application is ready for controlled distribution.

---

# 16. Vertical Slice Order

The canonical implementation order is:

```text
1. Repository Foundation

2. Library → Chapter → Verse

3. Reading Progress → Home

4. Quick Reflection → Deep Reflection

5. Journey

6. Guidance → Understanding

7. Search

8. Saar Conversation Foundation

9. Hybrid RAG

10. Security and Production Readiness
```

Do not reorder Saar ahead of Reflection or Understanding.

---

# 17. First Implementation Sprint

The first implementation sprint should focus only on repository foundation and Scripture.

## Sprint Goal

Deliver a mobile application that loads real Chapter and Verse content from the Spring Boot backend.

---

## Sprint Deliverables

### Repository

- create `backend/`,
- create `mobile/`,
- create local infrastructure,
- create CI skeleton.

### Backend

- initialize Spring Boot,
- add module markers,
- add ArchUnit,
- add Flyway,
- create Scripture schema,
- seed small approved corpus,
- implement Chapter list,
- implement Chapter detail,
- implement Verse detail.

### Mobile

- initialize Expo,
- create navigation shell,
- create design-system tokens,
- implement Library,
- implement Chapter,
- implement Verse,
- connect to local backend.

### Tests

- Scripture domain tests,
- repository integration tests,
- API tests,
- mobile screen tests,
- navigation test.

---

## Sprint Exit Condition

The sprint is complete only when the following real flow works:

```text
Open Mobile App
    ↓
Load Chapters From PostgreSQL
    ↓
Open Chapter Through Spring API
    ↓
Open Verse Through Spring API
    ↓
Render Scripture on Mobile
```

Mock-only UI does not satisfy the exit condition.

---

# 18. Definition of Done — Backend Slice

A backend vertical slice is complete when:

- domain language is correct,
- module ownership is clear,
- application use case exists,
- persistence is implemented,
- Flyway migration exists,
- API contract is implemented,
- validation exists,
- authorization exists where required,
- logs contain no private content,
- metrics exist where meaningful,
- unit tests pass,
- integration tests pass,
- architecture tests pass,
- and documentation is updated.

---

# 19. Definition of Done — Mobile Slice

A mobile vertical slice is complete when:

- the screen fulfills its approved responsibility,
- navigation works,
- API integration uses the real backend,
- loading state exists,
- empty state exists,
- error and retry states exist,
- accessibility is reviewed,
- intermittent connectivity is handled appropriately,
- private local storage is safe,
- telemetry contains no private content,
- and meaningful tests pass.

---

# 20. Definition of Done — AI Slice

An AI slice is complete when:

- Reader Message is persisted before generation,
- Generation is asynchronous,
- provider call occurs outside a database transaction,
- source context is approved,
- structured output is parsed,
- Citations resolve,
- grounding status is calculated,
- unsafe or ungrounded output is not delivered normally,
- retries are bounded,
- cost and latency are observable,
- and tests include adversarial cases.

---

# 21. Milestone Dependencies

```text
Phase 0
    ↓
Phase 1
    ↓
Phase 2
    ↓
Phase 3
    ↓
Phase 4
    ↓
Phase 5
    ├── Phase 6
    └── Phase 7
            ↓
        Phase 8
            ↓
        Phase 9
            ↓
        Phase 10
```

Phase 6 and Phase 7 may overlap only after Understanding source models are stable.

Phase 8 depends on:

- approved corpus,
- Search projections,
- Saar foundation,
- and Citation persistence.

---

# 22. Risk Register

## Risk: Content Licensing Delays

Impact:

- Translation,
- Commentary,
- and Saar grounding may be blocked.

Mitigation:

- start licensing review early,
- build with a small approved corpus,
- keep source metadata mandatory,
- and avoid unlicensed placeholder content entering production.

---

## Risk: Mobile Scope Expansion

Impact:

- delayed core delivery.

Mitigation:

- one mobile client only,
- no web V1,
- no bottom navigation without validation,
- no full offline synchronization,
- no notifications without approved use case.

---

## Risk: Reflection Data Loss

Impact:

- severe loss of Reader trust.

Mitigation:

- local draft preservation,
- autosave,
- optimistic locking,
- idempotency,
- clear save state,
- and end-to-end failure testing.

---

## Risk: AI Hallucination

Impact:

- theological misinformation and trust damage.

Mitigation:

- curated Understanding first,
- approved corpus,
- canonical context,
- Citation validation,
- grounding status,
- conservative failure,
- and content review.

---

## Risk: Premature Infrastructure Complexity

Impact:

- slower delivery,
- harder debugging,
- higher operating cost.

Mitigation:

- modular monolith,
- PostgreSQL-backed jobs,
- pgvector,
- managed containers,
- and extraction only after measurement.

---

## Risk: Incomplete Understanding Coverage

Impact:

- inconsistent Reader experience.

Mitigation:

- transparently limit supported Verse coverage,
- do not generate silent fallback content,
- prioritize representative Chapters,
- and publish reviewed content incrementally.

---

## Risk: Authentication Blocks Early Development

Impact:

- delayed feature work.

Mitigation:

- use a local authentication adapter behind the final identity boundary,
- preserve server-derived Reader ownership,
- replace the adapter once the provider decision is made.

---

# 23. Delivery Metrics

Track implementation progress using outcomes rather than file count.

Examples:

```text
Reader Journeys Completed

Vertical Slices Accepted

Architecture Tests Passing

Cross-User Security Tests Passing

Approved Scripture Coverage

Published Understanding Coverage

Grounded Saar Evaluation Rate

Reflection Save Reliability

Mobile Crash-Free Session Rate
```

Do not measure progress by:

- number of empty packages,
- number of generated classes,
- number of endpoints without clients,
- or infrastructure introduced.

---

# 24. Change-Control Rules

A change requires an ADR or architecture update when it:

- introduces a new primary database,
- introduces a new service,
- introduces Kafka,
- changes the mobile-first decision,
- introduces a web client,
- changes the Reflection ownership model,
- changes the Scripture source-of-truth hierarchy,
- allows Saar tool access,
- uses private Reflections for model training,
- changes Conversation retention defaults,
- or changes the approved product flow.

---

# 25. Initial Team Ownership

For an early small team or single-developer project, one person may own multiple areas.

The logical ownership boundaries should still remain:

```text
Backend Platform
Scripture and Content
Reading and Reflection
Mobile Experience
AI and Retrieval
Security and Operations
```

Ownership should follow domain responsibility, not technical convenience.

---

# 26. Recommended First Pull Requests

The first pull requests should remain small and ordered.

## PR 1

```text
Initialize repository and backend
```

Includes:

- root structure,
- Spring Boot application,
- module markers,
- ArchUnit,
- base CI.

## PR 2

```text
Add local PostgreSQL, pgvector, Redis, and Flyway
```

## PR 3

```text
Initialize React Native and Expo mobile application
```

Includes:

- navigation shell,
- providers,
- test setup,
- environment config.

## PR 4

```text
Create Scripture Chapter persistence and API
```

## PR 5

```text
Create Verse persistence and API
```

## PR 6

```text
Implement mobile Library
```

## PR 7

```text
Implement mobile Chapter and Verse flow
```

Each PR should end in a usable and tested state.

---

# 27. Decisions

The MVP implementation plan adopts these decisions:

- V1 uses Spring Boot and React Native with Expo.
- V1 has no web client.
- Implementation proceeds through vertical slices.
- The first product slice is Library → Chapter → Verse.
- Core Reading precedes Reflection.
- Reflection precedes Journey.
- Journey precedes Guidance and Understanding.
- Understanding precedes Saar.
- Saar foundation precedes advanced RAG.
- RAG uses PostgreSQL and pgvector first.
- Security and privacy are implemented incrementally and completed before release.
- Full offline synchronization is deferred.
- Kafka, microservices, Kubernetes, and dedicated vector infrastructure are deferred.
- Architecture documents are updated when implementation materially changes a decision.

---

# 28. Open Decisions

The following remain unresolved:

- final authentication provider,
- exact Expo routing approach,
- final mobile navigation library,
- server-state library,
- local draft encryption,
- whether Reflection revisions are V1,
- whether Bookmarks are V1,
- initial approved Translation,
- initial approved Commentary corpus,
- final AI provider,
- final embedding model,
- exact Saar polling behavior,
- exact deployment platform,
- infrastructure-as-code tool,
- production budget,
- and beta launch size.

These decisions should be resolved only when their implementation phase approaches.

---

# 29. Immediate Next Action

The architecture phase is complete enough to begin implementation.

The next action is:

```text
Initialize the repository foundation
```

Start with:

```text
PR 1
Initialize repository and Spring Boot backend
```

Then:

```text
PR 2
Add local PostgreSQL, pgvector, Redis, and Flyway
```

Then:

```text
PR 3
Initialize the React Native and Expo mobile app
```

After the foundation is stable, begin the first vertical slice:

```text
Library
    ↓
Chapter
    ↓
Verse
```

---

# 30. North Star

The MVP plan succeeds when every implementation phase produces a coherent Reader capability rather than a disconnected collection of backend classes, mobile screens, tables, and infrastructure.

The engineering sequence should preserve Antar’s product philosophy:

```text
Read
    ↓
Reflect
    ↓
Study
    ↓
Discuss
```

The product should become more technically sophisticated only as the Reader journey requires it.