# Antar System Overview

**Version:** 1.0  
**Status:** Draft for Architecture Review  
**Owner:** Engineering  
**Last Updated:** August 2026

---

# 1. Purpose

This document defines the high-level engineering architecture for Antar.

It explains:

- the system’s major responsibilities,
- the initial deployment model,
- the primary domain boundaries,
- how data moves through the platform,
- where AI belongs,
- what is included in V1,
- and how the architecture may evolve as the product grows.

This document intentionally remains technology-aware but implementation-light.

Detailed schemas, APIs, retrieval strategies, and deployment decisions are documented separately.

---

# 2. Product Context

Antar is a contemplative reading and study platform centered on the Bhagavad Gita.

The product supports four primary modes of engagement:

```text
Read
    ↓
Reflect
    ↓
Study
    ↓
Discuss
```

Readers should be able to:

- browse chapters and verses,
- read Sanskrit, transliteration, and translation,
- preserve reading continuity,
- capture quick and deep reflections,
- revisit meaningful memories,
- explore curated explanations and commentary,
- and optionally speak with Saar, Antar’s conversational study companion.

The product must remain useful without conversational AI.

Reading, reflection, journey, library, search, and curated understanding are first-class product capabilities independent of Saar.

---

# 3. Architectural Principles

## 3.1 Begin as a Modular Monolith

Antar V1 will be implemented as a modular monolith.

The backend will be:

- one deployable application,
- one primary relational database,
- one codebase,
- and one operational unit.

Internally, the system will remain divided into clear domain modules.

This approach provides:

- simpler development,
- easier local setup,
- lower deployment complexity,
- reliable transactions,
- fewer network boundaries,
- and faster iteration during product discovery.

The modular monolith should preserve boundaries strong enough that selected modules can later be extracted into independent services.

---

## 3.2 Domain Boundaries Before Service Boundaries

A domain module is not automatically a microservice.

Modules should be separated by:

- responsibility,
- data ownership,
- use cases,
- and dependency direction.

A module should become an independent service only when there is a demonstrated reason such as:

- independent scaling,
- separate operational ownership,
- different availability requirements,
- security isolation,
- deployment independence,
- or meaningful technology divergence.

---

## 3.3 Scripture Is the Source of Truth

Antar presents several layers of knowledge:

```text
Scripture
    ↓
Traditional Commentary
    ↓
Curated Understanding
    ↓
Saar Synthesis
```

The system must preserve the distinction between these layers.

AI-generated content must never be stored or presented as scripture or authoritative commentary.

Every user-facing explanation should retain source provenance where applicable.

---

## 3.4 AI Is an Optional Capability

The platform must remain operational when:

- an AI provider is unavailable,
- vector retrieval is degraded,
- a generation request fails,
- or Saar is disabled.

The following capabilities must not depend on an LLM:

- authentication,
- scripture browsing,
- reading,
- search by canonical reference,
- reflections,
- journey history,
- bookmarks,
- reading progress,
- and curated understanding.

---

## 3.5 Privacy by Default

Reflections and Guidance input may contain sensitive personal information.

The architecture should:

- collect only necessary data,
- avoid sending private content to AI providers unless required and permitted,
- avoid using raw personal text for analytics,
- support deletion,
- preserve ownership boundaries,
- and clearly distinguish private user data from public scripture content.

---

## 3.6 Provenance Before Fluency

A fluent AI response is not sufficient.

Saar responses should be grounded in retrievable sources and should preserve:

- chapter and verse references,
- translation provenance,
- commentary provenance,
- and the distinction between retrieved content and generated synthesis.

If grounding cannot be established, Saar should respond conservatively rather than fabricate certainty.

---

## 3.7 Observability From the Beginning

The initial system should support:

- structured logs,
- request correlation,
- metrics,
- distributed tracing where external calls are involved,
- AI latency and token metrics,
- retrieval diagnostics,
- and error classification.

Observability is part of the architecture, not an afterthought.

---

# 4. V1 Technology Direction

The following stack is the initial recommendation.

## Client

Antar V1 is a mobile-first application.

The recommended client stack is:

```text
React Native
TypeScript
Expo
```

---

## Backend

```text
Java 21
Spring Boot
Spring Security
Spring Data JPA
```

The backend exposes versioned HTTP APIs.

Internal module interactions should primarily use application-service calls rather than HTTP.

---

## Primary Database

```text
PostgreSQL
```

PostgreSQL will store:

- users,
- scripture metadata,
- reading state,
- reflections,
- journey records,
- curated content,
- Saar conversations,
- citations,
- and operational metadata.

---

## Vector Retrieval

```text
pgvector
```

V1 should keep vector search within PostgreSQL unless scale or retrieval needs justify a dedicated vector database.

This keeps:

- transactional data,
- source metadata,
- and embeddings

within one operational system.

---

## Cache

```text
Redis
```

Redis may support:

- frequently accessed scripture content,
- reading-state acceleration,
- rate limiting,
- short-lived request state,
- idempotency,
- and AI response caching where appropriate.

Redis should not become the source of truth for durable user data.

---

## Search

V1 should use:

- exact canonical-reference lookup,
- PostgreSQL full-text search,
- metadata filtering,
- and vector similarity where semantic retrieval is required.

A separate search engine should not be introduced until justified by measured requirements.

---

## AI Provider

LLM access will be placed behind an internal abstraction.

The rest of Antar should not depend directly on a specific model vendor.

The abstraction should support:

- provider selection,
- request construction,
- timeouts,
- retries,
- token accounting,
- safety handling,
- and provider-specific response mapping.

---

## Object Storage

S3-compatible object storage may be introduced for:

- data exports,
- user-requested backups,
- generated reports,
- future audio,
- and large static content assets.

Object storage is optional for the earliest V1 slice.

---

## Observability

Recommended foundation:

```text
OpenTelemetry
Structured JSON logging
Application metrics
Trace correlation
```

The concrete observability backend may be selected during deployment design.

---

# 5. System Context

```text
┌─────────────────────────────┐
│          Reader             │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Web / Mobile Client    │
└──────────────┬──────────────┘
               │ HTTPS
               ▼
┌───────────────────────────────────────────┐
│              Antar Backend                │
│                                           │
│  Identity                                 │
│  Scripture                                │
│  Reading                                  │
│  Reflection                               │
│  Journey                                  │
│  Guidance                                 │
│  Understanding                            │
│  Saar                                     │
│  Search                                   │
└───────┬──────────────┬──────────────┬─────┘
        │              │              │
        ▼              ▼              ▼
┌────────────┐  ┌────────────┐  ┌───────────────┐
│ PostgreSQL │  │   Redis    │  │  LLM Provider │
│ + pgvector │  │            │  │               │
└────────────┘  └────────────┘  └───────────────┘
        │
        ▼
┌────────────────────┐
│ S3-Compatible Store│
│     Optional       │
└────────────────────┘
```

---

# 6. Primary Domain Modules

## 6.1 Identity

Identity owns:

- user accounts,
- authentication,
- authorization,
- account lifecycle,
- profile metadata,
- reading preferences,
- language preferences,
- and privacy preferences.

Identity does not own reflections, reading history, or conversations.

---

## 6.2 Scripture

Scripture owns canonical Sanskrit content and related Scripture-owned source
metadata.

It includes:

- chapters,
- verses,
- Sanskrit text,
- transliterations,
- chapter metadata,
- commentary sources,
- and canonical relationships.

Licensed translations are **not** owned by Scripture. Translation is a separate
bounded context (ADR-012) that references Verse identity only
(`scripture.verses.id`).

Scripture content is primarily read-only at runtime.

Changes should occur through controlled content-ingestion or administration workflows.

---

## 6.2a Translation

Translation owns licensed translation editions and per-Verse translation text.

It includes:

- translation sources / providers,
- translation rows,
- Translation package provenance and import audit,
- and the read-only Translation API.

Translation may reference Scripture Verse identity only. Scripture must not
depend on Translation. See ADR-012.

No real Translation corpus is claimed as imported in the current foundation;
synthetic fixture content supports the bounded-context slice.

---

## 6.3 Reading

Reading owns the reader’s navigation and continuity state.

It includes:

- current reading position,
- recently visited verses,
- reading sessions,
- chapter progress,
- bookmarks if included in V1,
- and continuation state.

Reading does not own scripture content.

It references canonical Scripture identifiers.

---

## 6.4 Reflection

Reflection owns reader-authored writing.

It includes:

- quick reflections,
- deep journal entries,
- drafts,
- persistence state,
- timestamps,
- and optional revision history.

Reflection content belongs to the reader.

It must never be modified, summarized, or analyzed silently.

---

## 6.5 Journey

Journey owns the presentation and retrieval of meaningful past moments.

It includes:

- chronological reflection history,
- journey memories,
- source references,
- revisit context,
- and timeline grouping.

Journey does not infer or score spiritual growth.

It presents memories rather than measurements.

---

## 6.6 Guidance

Guidance owns the reader’s choice of learning path after reading and reflection.

It may support paths such as:

- understand this verse,
- connect with other teachings,
- explore traditional commentaries,
- or ask Saar.

Guidance does not generate AI responses itself.

It coordinates the transition into the appropriate learning experience.

---

## 6.7 Understanding

Understanding owns curated educational content.

It includes:

- reviewed explanations,
- key concepts,
- traditional insights,
- related verses,
- and content provenance.

Understanding should remain useful without AI.

Its content may be editorially authored, imported, or generated offline and reviewed before publication.

---

## 6.8 Saar

Saar owns conversational AI behavior.

It includes:

- conversations,
- messages,
- retrieval requests,
- prompt assembly,
- provider invocation,
- citations,
- response validation,
- safety controls,
- and conversational state.

Saar is the only V1 domain that requires generative AI at runtime.

---

## 6.9 Search

Search owns content discovery across approved searchable domains.

It includes:

- canonical-reference parsing,
- keyword search,
- full-text search,
- semantic search where appropriate,
- result grouping,
- and result-ranking coordination.

Search does not own the content it returns.

---

## 6.10 Platform

Platform contains shared infrastructure concerns that do not represent business domains.

Examples:

- logging,
- metrics,
- tracing,
- feature flags,
- provider clients,
- email delivery,
- object storage,
- request correlation,
- rate limiting,
- and configuration.

Platform code must not absorb domain logic.

---

# 7. Dependency Direction

Dependencies should follow application boundaries rather than convenience.

A conceptual direction is:

```text
Platform
   ▲
   │
Application Modules
   ▲
   │
Domain Models
```

Business domains should not depend directly on:

- web controllers,
- database entities from unrelated modules,
- vendor-specific AI SDKs,
- or infrastructure implementation details.

Cross-module access should occur through explicit application interfaces.

Example:

```text
Saar
  ↓
Scripture Query Interface
  ↓
Scripture Module
```

Saar should not directly query Scripture tables through a shared repository.

---

# 8. Standard Request Flow

A typical authenticated request follows:

```text
Client
  ↓
HTTP Controller
  ↓
Authentication and Authorization
  ↓
Application Service
  ↓
Domain Logic
  ↓
Repository or External Port
  ↓
PostgreSQL / Redis / Provider
  ↓
Response Mapping
  ↓
Client
```

Controllers should remain thin.

They should own:

- request parsing,
- validation,
- authorization entry points,
- response status,
- and DTO mapping.

They should not own business workflows.

---

# 9. Core Product Flows

## 9.1 Browse Scripture

```text
Client
  ↓
Scripture API
  ↓
Scripture Application Service
  ↓
Chapter / Verse Repository
  ↓
PostgreSQL
  ↓
Client
```

Redis may cache frequently accessed immutable content.

---

## 9.2 Continue Reading

```text
Client
  ↓
Reading API
  ↓
Reading Application Service
  ↓
Resolve reader continuation state
  ↓
Fetch destination metadata from Scripture
  ↓
Return Today's Invitation destination
```

Today’s Invitation does not determine the destination.

Reading and product-selection logic provide an already-selected destination.

---

## 9.3 Save Reflection

```text
Client
  ↓
Reflection API
  ↓
Validate ownership and content limits
  ↓
Persist draft or journal entry
  ↓
Update timestamp and save state
  ↓
Optionally emit internal domain event
  ↓
Return persistence status
```

Reflection persistence should support idempotent updates where practical.

---

## 9.4 Load Journey

```text
Client
  ↓
Journey API
  ↓
Query reader-owned reflections
  ↓
Join canonical verse context
  ↓
Group chronologically
  ↓
Return Journey Memories
```

Journey must not expose another reader’s content.

---

## 9.5 Curated Understanding

```text
Client
  ↓
Understanding API
  ↓
Resolve verse
  ↓
Load reviewed explanation
  ↓
Load key concepts
  ↓
Load commentary references
  ↓
Load related verses
  ↓
Return source-aware content
```

This flow does not require an LLM at runtime.

---

# 10. Saar Request Flow

```text
Reader Question
  ↓
Saar API
  ↓
Authentication and Authorization
  ↓
Conversation Context Loader
  ↓
Verse Context Loader
  ↓
Retrieval Orchestrator
  ├── Canonical metadata filtering
  ├── Full-text retrieval
  ├── Vector similarity retrieval
  └── Related-verse retrieval
  ↓
Reranking
  ↓
Prompt Builder
  ↓
LLM Provider
  ↓
Structured Response Parser
  ↓
Citation Validator
  ↓
Safety and Provenance Validation
  ↓
Persist Message and Citations
  ↓
Return Response
```

A response should not be presented as fully grounded if its citations cannot be validated.

---

# 11. AI Boundary

The AI provider boundary should expose an application-level contract rather than vendor-specific request objects.

Conceptually:

```text
GenerateStudyResponseCommand
- conversation context
- reader question
- verse context
- retrieved sources
- response constraints
- safety context
```

```text
GenerateStudyResponseResult
- generated answer
- source references
- uncertainty indicators
- token usage
- provider metadata
- validation status
```

Provider-specific translation occurs inside the Platform layer.

This enables:

- provider replacement,
- multi-provider fallback,
- model upgrades,
- testing without external calls,
- and centralized cost controls.

---

# 12. Data Ownership

Each domain should own its data and repository interfaces.

Conceptual ownership:

| Domain | Owned Data |
|---|---|
| Identity | users, credentials, preferences |
| Scripture | chapters, verses, transliterations, commentaries |
| Translation | translation sources, translations, translation packages / import audit |
| Reading | reading positions, sessions, bookmarks |
| Reflection | quick reflections, journal entries, revisions |
| Journey | derived memory metadata and revisit state |
| Guidance | learning-path selections and workflow state |
| Understanding | curated explanations and related content |
| Saar | conversations, messages, retrieval records, citations |
| Search | indexes or search projections where needed |

In a modular monolith, these records may share one PostgreSQL database while still maintaining logical ownership.

One module should not write directly to another module’s tables.

---

# 13. Internal Events

V1 does not require Kafka.

Domain events may initially be implemented in-process.

Potential events include:

```text
VerseOpened
ReadingPositionUpdated
ReflectionCreated
ReflectionUpdated
ReflectionDeleted
JourneyMemoryEligible
GuidancePathSelected
SaarConversationStarted
SaarResponseGenerated
```

These events can support:

- decoupled internal workflows,
- auditability,
- future projections,
- and eventual service extraction.

Events must not be introduced where a direct synchronous call is simpler and more correct.

---

# 14. Consistency Model

Use strong consistency for:

- account ownership,
- reflection updates,
- deletion,
- reading position,
- bookmarks,
- conversation persistence,
- and privacy changes.

Eventual consistency may be acceptable for:

- search indexes,
- journey projections,
- analytics,
- derived recommendations,
- and cached content.

The user’s private writing must not appear lost or stale because of avoidable eventual-consistency decisions.

---

# 15. Caching Strategy

Candidates for caching include:

- chapter metadata,
- verses,
- translations,
- transliterations,
- curated understanding,
- commentary metadata,
- and frequently requested related-verse mappings.

Avoid caching private reflection or conversation content unless:

- there is a clear performance need,
- the data is encrypted or otherwise protected,
- ownership is enforced,
- and expiration is explicit.

Cache invalidation should follow content-version changes rather than arbitrary time where practical.

---

# 16. Security Boundaries

At minimum, V1 should include:

- secure authentication,
- authorization on all user-owned data,
- encryption in transit,
- encrypted secrets,
- input validation,
- rate limiting,
- AI-provider timeout controls,
- audit logging for sensitive changes,
- data-deletion support,
- and strict source-content administration.

Private reflections must never be accessible through public Scripture or Search APIs.

---

# 17. Failure Handling

The system should degrade gracefully.

## AI Provider Failure

- preserve the user’s question where allowed,
- return a calm retryable state,
- keep curated Understanding available,
- and do not fabricate a response.

## Vector Retrieval Failure

- fall back to metadata and full-text retrieval where safe,
- or return an explicit inability to ground the response.

## Redis Failure

- fall back to PostgreSQL where supported,
- avoid treating cached state as durable truth.

## Search Failure

- preserve the query,
- keep canonical browsing available.

## Offline Client State

- preserve drafts locally where product and privacy rules allow,
- synchronize when connectivity returns,
- and clearly distinguish local save from server synchronization.

---

# 18. Scalability Approach

The initial architecture should scale vertically and through stateless application replicas.

```text
Load Balancer
  ↓
Multiple Antar Backend Instances
  ↓
PostgreSQL
Redis
External AI Provider
```

Application instances should avoid storing durable session state in memory.

Potential future extraction candidates include:

- Saar generation and retrieval,
- search indexing,
- content ingestion,
- notification delivery,
- and export processing.

Extraction should be driven by measured constraints rather than architectural fashion.

---

# 19. Service Extraction Criteria

A module may be considered for service extraction when one or more conditions are consistently true:

1. It requires independent scaling.
2. It has different uptime or latency requirements.
3. It requires independent deployments.
4. It uses a substantially different technology stack.
5. It contains a clear data-ownership boundary.
6. It creates operational contention inside the monolith.
7. It requires stronger security isolation.
8. A separate team owns its roadmap and operations.

The likely first extraction candidate is Saar because it may require:

- independent scaling,
- provider-specific resilience,
- longer-running requests,
- token and cost controls,
- retrieval infrastructure,
- and separate observability.

This remains a future option, not a V1 requirement.

---

# 20. V1 Scope

## Included

- authentication and account lifecycle,
- reading preferences,
- canonical chapter and verse browsing,
- Sanskrit, transliteration, and translation,
- reading continuation,
- Today’s Invitation resolution,
- quick reflection,
- deep reflection,
- save status,
- Journey timeline,
- curated Understanding,
- related verses,
- Guidance path selection,
- Saar conversations,
- grounded citations,
- basic canonical and keyword search,
- privacy-aware data deletion,
- structured logging and metrics.

---

## Deferred

- microservices,
- Kafka,
- complex event streaming,
- social features,
- public sharing,
- real-time collaboration,
- multi-agent AI workflows,
- fine-tuned models,
- advanced recommendation systems,
- multiple vector databases,
- complex analytics dashboards,
- gamification,
- voice conversations,
- full offline synchronization across devices,
- and automatic psychological or spiritual profiling.

---

# 21. Architecture Risks

## AI Hallucination

Mitigation:

- grounded retrieval,
- source constraints,
- citation validation,
- conservative response behavior,
- and clear source separation.

---

## Sensitive Personal Data Exposure

Mitigation:

- data minimization,
- explicit AI boundaries,
- authorization,
- redaction where appropriate,
- retention controls,
- and avoiding raw-text analytics.

---

## Premature Complexity

Mitigation:

- modular monolith,
- PostgreSQL-first strategy,
- in-process events,
- and extraction only after measurement.

---

## Content Provenance Confusion

Mitigation:

- explicit source models,
- content-type labels,
- immutable canonical scripture,
- reviewed curated content,
- and AI synthesis clearly identified.

---

## AI Provider Dependency

Mitigation:

- provider abstraction,
- timeout and retry policies,
- fallback behavior,
- and non-AI product functionality.

---

## Unbounded AI Cost

Mitigation:

- rate limits,
- token budgets,
- prompt-size controls,
- conversation limits,
- model routing,
- retrieval limits,
- caching where safe,
- and cost observability.

---

# 22. Architecture Decision Summary

The initial engineering direction is:

```text
Modular Monolith
Java 21
Spring Boot
PostgreSQL
pgvector
Redis
HTTP APIs
Provider-Agnostic AI Boundary
OpenTelemetry
```

The architecture intentionally prioritizes:

- product iteration,
- clear domain ownership,
- explainable AI,
- source provenance,
- privacy,
- and operational simplicity.

---

# 23. Related Documents

The following documents should build on this overview:

```text
02_DOMAIN_MODEL.md
03_DATA_MODEL.md
04_API_CONTRACTS.md
05_AI_PIPELINE.md
06_RAG_ARCHITECTURE.md
07_SECURITY_AND_PRIVACY.md
08_DEPLOYMENT_AND_OBSERVABILITY.md
09_REPOSITORY_STRUCTURE.md
10_MVP_IMPLEMENTATION_PLAN.md
```

---

# 24. Open Decisions

The following remain unresolved:

- final React Native and Expo configuration
- authentication provider,
- final LLM provider,
- embedding model,
- commentary licensing and approved sources,
- whether bookmarks are included in V1,
- offline-draft behavior,
- conversation retention duration,
- exact search scope,
- and deployment platform.

These decisions should be resolved in the relevant architecture documents rather than inside this overview.

---

# 25. North Star

Antar’s architecture succeeds when it supports a calm, trustworthy, scripture-centered experience without making the product operationally complex before that complexity is justified.

The system should make reading reliable, reflection private, curated understanding transparent, and AI grounded.

Technology should support the reader’s journey without becoming the center of it.