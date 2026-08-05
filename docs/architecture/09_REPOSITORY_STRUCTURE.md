# Antar Repository Structure

**Version:** 1.1  
**Status:** Draft for Architecture Review  
**Owner:** Engineering  
**Last Updated:** August 2026

---

# 1. Purpose

This document defines the recommended repository structure for Antar.

It establishes:

- top-level project organization,
- backend modular-monolith boundaries,
- mobile application organization,
- package conventions,
- dependency rules,
- database migration ownership,
- test structure,
- shared infrastructure placement,
- architecture enforcement,
- and future service-extraction boundaries.

The repository should make the intended architecture visible.

A developer should be able to inspect the directory structure and understand:

- which business domains exist,
- which module owns a capability,
- which dependencies are allowed,
- where new code belongs,
- and how the mobile application maps to approved product experiences.

---

# 2. Repository Principles

## 2.1 Organize Around Business Domains

Production code should be organized primarily by domain.

Prefer:

```text
reflection/
    api/
    application/
    domain/
    infrastructure/
```

Avoid a global technical-layer structure such as:

```text
controllers/
services/
repositories/
entities/
```

A global technical-layer structure spreads one feature across unrelated directories and weakens domain ownership.

---

## 2.2 The Repository Must Reflect the Modular Monolith

Antar begins as one deployable backend containing clearly separated business modules.

The codebase should communicate:

```text
One Backend Deployment
Multiple Business Modules
Explicit Dependencies
Independent Ownership
```

A modular monolith is not one large package separated only by informal naming conventions.

Module boundaries should be visible, documented, and testable.

---

## 2.3 Antar V1 Is Mobile-First

Antar V1 uses one mobile client built with:

```text
React Native
TypeScript
Expo
```

The application targets:

```text
iOS
Android
```

A web or Next.js client is intentionally outside the V1 implementation scope.

The backend remains client-neutral so another client can be added later without changing domain ownership.

---

## 2.4 Separate Product Architecture From Implementation

The repository contains both:

- product and architecture documentation,
- production implementation.

Documentation defines approved intent.

Code implements it.

Suggested separation:

```text
docs/
design/
backend/
mobile/
infrastructure/
```

---

## 2.5 Shared Code Must Remain Small

A `shared` package should not become a place for code that developers do not know where to put.

Shared code should contain only genuinely cross-cutting primitives such as:

- common identifier abstractions,
- time abstractions,
- pagination primitives,
- domain-event interfaces,
- and stable error abstractions.

Business logic belongs to a domain module.

---

## 2.6 Infrastructure Depends on Domain Contracts

Domain logic should not depend directly on:

- Spring MVC,
- JPA,
- Redis clients,
- AI-provider SDKs,
- object-storage SDKs,
- HTTP clients,
- React Native,
- Expo,
- or mobile storage libraries.

Infrastructure implements ports defined by application or domain code.

---

## 2.7 Module Access Must Be Explicit

One backend module should not reach into another module’s internal packages.

For example:

```text
Saar
    ↓
ScriptureQuery
    ↓
Scripture Module
```

Saar should not import:

```text
scripture.infrastructure.persistence.VerseJpaRepository
```

Cross-module communication should occur through explicitly published interfaces.

---

## 2.8 Mobile Features Own Their Experience

Mobile code should be organized by approved product experience.

Examples:

```text
home
library
chapter
verse
reflection
journey
guidance
understanding
saar
search
settings
authentication
```

Each feature owns:

- screens,
- feature-specific components,
- state,
- API integration,
- navigation behavior,
- local persistence behavior,
- and tests.

---

# 3. Recommended Top-Level Structure

```text
antar/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── .editorconfig
├── .gitignore
├── compose.yaml
├── docs/
├── design/
├── backend/
├── mobile/
├── infrastructure/
├── scripts/
└── .github/
```

Responsibilities:

```text
docs/
    Product, architecture, ADRs, engineering decisions

design/
    Foundations, experiences, components, compositions,
    interaction blueprints, wireframes, and design prompts

backend/
    Java and Spring Boot modular-monolith implementation

mobile/
    React Native, TypeScript, and Expo application

infrastructure/
    Deployment and infrastructure-as-code definitions

scripts/
    Local development, validation, ingestion,
    indexing, and operational utilities

.github/
    Continuous integration and repository automation
```

---

# 4. Documentation Structure

Recommended documentation structure:

```text
docs/
├── README.md
├── architecture/
│   ├── 01_SYSTEM_OVERVIEW.md
│   ├── 02_DOMAIN_MODEL.md
│   ├── 03_DATA_MODEL.md
│   ├── 04_API_CONTRACTS.md
│   ├── 05_AI_PIPELINE.md
│   ├── 06_RAG_ARCHITECTURE.md
│   ├── 07_SECURITY_AND_PRIVACY.md
│   ├── 08_DEPLOYMENT_AND_OBSERVABILITY.md
│   ├── 09_REPOSITORY_STRUCTURE.md
│   ├── 10_MVP_IMPLEMENTATION_PLAN.md
│   ├── DOMAIN_DICTIONARY.md
│   └── adr/
│       ├── README.md
│       ├── ADR-001-home-primary-action.md
│       ├── ADR-002-todays-invitation-composition.md
│       ├── ADR-003-home-not-dashboard.md
│       ├── ADR-004-reflection-follows-reading.md
│       ├── ADR-005-ai-not-primary.md
│       ├── ADR-006-guidance-reader-intent.md
│       ├── ADR-007-curated-before-conversation.md
│       ├── ADR-008-saar-companion.md
│       ├── ADR-009-respect-silence.md
│       ├── ADR-010-scripture-source-of-truth.md
│       └── ADR-011-mobile-first-client.md
├── api/
│   ├── openapi.yaml
│   └── examples/
├── operations/
│   ├── runbooks/
│   ├── incident-response.md
│   └── data-recovery.md
└── product/
    ├── V1_SCOPE.md
    └── PRODUCT_SCENARIOS.md
```

Architecture documents should describe approved intent.

They should not unnecessarily duplicate generated implementation documentation.

---

# 5. Design Structure

The design documentation may remain under:

```text
design/
├── 01_FOUNDATIONS/
├── 02_EXPERIENCES/
├── 03_INTERACTION_BLUEPRINTS/
├── 04_COMPONENTS/
├── 06_DESIGN_REVIEWS/
├── 99_COMPOSITIONS/
└── AI/
```

The design repository and implementation repository should use the same canonical vocabulary.

Examples:

```text
Today's Invitation
Quick Reflection
Deep Reflection
Journey Memory
Understanding
Saar
```

Do not casually rename these concepts in code.

---

# 6. Backend Build Structure

Recommended backend root:

```text
backend/
├── pom.xml
├── README.md
├── Dockerfile
├── mvnw
├── mvnw.cmd
├── .mvn/
└── src/
```

Antar may begin as one Maven project.

A multi-module Maven build is optional.

The initial recommendation is:

```text
One Spring Boot application
+
Strong package-level modules
+
Automated architecture tests
```

This is simpler than introducing many build modules immediately while still preserving architectural boundaries.

---

# 7. Backend Base Package

Recommended Java base package:

```text
com.antar
```

Application entry point:

```text
com.antar.AntarApplication
```

Production modules:

```text
com.antar.identity
com.antar.scripture
com.antar.translation
com.antar.reading
com.antar.reflection
com.antar.journey
com.antar.guidance
com.antar.understanding
com.antar.saar
com.antar.search
com.antar.platform
com.antar.shared
```

---

# 8. Backend Source Tree

```text
backend/src/main/java/com/antar/
├── AntarApplication.java
├── identity/
├── scripture/
├── translation/
├── reading/
├── reflection/
├── journey/
├── guidance/
├── understanding/
├── saar/
├── search/
├── platform/
└── shared/
```

Resources:

```text
backend/src/main/resources/
├── application.yml
├── application-local.yml
├── application-test.yml
├── application-staging.yml
├── application-production.yml
├── db/
│   └── migration/
├── prompts/
├── content/
└── logback-spring.xml
```

Sensitive environment values must not be stored in these files.

---

# 9. Standard Backend Module Anatomy

Each business module should follow a consistent internal structure.

Example:

```text
reflection/
├── api/
├── application/
├── domain/
├── infrastructure/
└── ReflectionModule.java
```

These layers are internal to each module.

They are not global application folders.

---

# 10. API Package

The `api` package owns the module’s external transport boundary.

Example:

```text
reflection/api/
├── ReflectionController.java
├── CreateReflectionRequest.java
├── UpdateReflectionRequest.java
├── ReflectionResponse.java
├── ReflectionSummaryResponse.java
└── ReflectionApiMapper.java
```

Responsibilities:

- HTTP routing,
- request parsing,
- request validation,
- response mapping,
- HTTP status selection,
- authentication entry-point integration,
- ETag handling,
- idempotency headers,
- and transport-specific errors.

The API package must not own:

- aggregate rules,
- database queries,
- transaction workflows,
- or infrastructure calls.

Controllers should call application use cases.

---

# 11. Application Package

The `application` package coordinates use cases.

Example:

```text
reflection/application/
├── create/
│   ├── CreateReflectionCommand.java
│   ├── CreateReflectionResult.java
│   └── CreateReflectionUseCase.java
├── update/
│   ├── UpdateReflectionCommand.java
│   ├── UpdateReflectionResult.java
│   └── UpdateReflectionUseCase.java
├── expand/
│   ├── ExpandReflectionCommand.java
│   └── ExpandReflectionUseCase.java
├── query/
│   ├── GetReflectionQuery.java
│   ├── ListReflectionsQuery.java
│   └── ReflectionQueryService.java
├── port/
│   ├── ReflectionRepository.java
│   ├── ScriptureReferencePort.java
│   ├── ReflectionEventPublisher.java
│   └── ClockPort.java
└── ReflectionApplicationService.java
```

Responsibilities:

- use-case orchestration,
- transaction boundaries,
- authorization checks,
- invoking domain behavior,
- coordinating module ports,
- publishing domain events,
- and returning application results.

The application layer should not contain HTTP-specific behavior.

---

# 12. Domain Package

The `domain` package contains business rules.

Example:

```text
reflection/domain/
├── ReflectionEntry.java
├── ReflectionId.java
├── ReflectionType.java
├── ReflectionStatus.java
├── ReflectionContent.java
├── ReflectionRevision.java
├── ReflectionCreated.java
├── ReflectionUpdated.java
└── ReflectionDomainException.java
```

Responsibilities:

- aggregate behavior,
- invariants,
- entities,
- value objects,
- domain events,
- and domain-specific exceptions.

The domain package should remain free of:

- Spring MVC,
- JPA entities,
- controller DTOs,
- Redis clients,
- provider SDKs,
- and HTTP clients.

Limited framework annotations may be accepted only when the tradeoff is deliberate and documented.

---

# 13. Infrastructure Package

The `infrastructure` package implements application ports.

Example:

```text
reflection/infrastructure/
├── persistence/
│   ├── ReflectionJpaEntity.java
│   ├── ReflectionSpringDataRepository.java
│   ├── ReflectionRepositoryAdapter.java
│   └── ReflectionPersistenceMapper.java
├── events/
│   └── ReflectionSpringEventPublisher.java
└── config/
    └── ReflectionConfiguration.java
```

Responsibilities:

- JPA persistence,
- Redis caching,
- external service adapters,
- framework configuration,
- messaging,
- and implementation-specific mapping.

Infrastructure should depend inward on application and domain contracts.

---

# 14. Published Module Interfaces

Each backend module should publish only a small API for other modules.

Example:

```text
scripture/application/publicapi/
├── ScriptureQuery.java
├── VerseDetails.java
├── ChapterSummary.java
└── ScriptureReference.java
```

An alternative structure may be:

```text
scripture/
├── publicapi/
└── internal/
```

The exact naming may vary, but the principle is required:

```text
Published Interface
Internal Implementation
```

Other modules may depend only on the published interface.

---

# 15. Internal Package Visibility

Java does not provide module-private packages by default.

Boundaries should therefore be enforced through:

- package conventions,
- architecture tests,
- constructor visibility,
- package-private classes,
- Spring Modulith where appropriate,
- and build-time checks.

Do not rely solely on developer discipline.

---

# 16. Module Marker

Each module may include a marker type.

Example:

```java
package com.antar.reflection;

public final class ReflectionModule {

    private ReflectionModule() {
    }
}
```

Marker types may support:

- architecture tests,
- package scanning,
- module documentation,
- and Spring Modulith configuration.

---

# 17. Identity Module Structure

```text
identity/
├── api/
│   ├── CurrentReaderController.java
│   └── PreferencesController.java
├── application/
│   ├── profile/
│   ├── preferences/
│   ├── privacy/
│   ├── deletion/
│   └── publicapi/
├── domain/
│   ├── User.java
│   ├── UserId.java
│   ├── ReadingPreferences.java
│   ├── PrivacyPreferences.java
│   └── AccountStatus.java
└── infrastructure/
    ├── authentication/
    ├── persistence/
    └── config/
```

Identity publishes:

- authenticated Reader identity,
- privacy preference queries,
- and account lifecycle interfaces.

It should not expose persistence entities.

---

# 18. Scripture Module Structure

```text
scripture/
├── api/                         # Reader Chapter/Verse query APIs (no import HTTP)
├── application/
│   ├── chapter/query/
│   ├── verse/query/
│   ├── imports/                 # ImportScripturePackageUseCase + mutation + probe
│   └── port/                    # PackageFormatValidator, ContentPackageRepository, …
├── domain/
│   ├── Chapter.java / Verse.java / CanonicalReference.java
│   ├── ContentVersionPolicy.java
│   └── ImportFailureCode.java / ContentPackageStatus.java / ImportExecutionStatus.java
└── infrastructure/
    ├── persistence/             # JPA + content package/import adapters
    ├── packageformat/           # Package Format v1 validator + filesystem reader
    ├── importcmd/               # ScripturePackageImportMain (WebApplicationType.NONE)
    └── config/
```

**Implemented now:** Chapter/Verse identity APIs, Package Format importer v1 (admin CLI only).

**Not implemented yet:** Commentary APIs, public ingestion HTTP, transliteration
persistence, Reader Verse-by-reference full content. Translation is a separate
bounded context (see Translation Module Structure).

Scripture should publish stable query contracts used by:

- Reading,
- Reflection,
- Journey,
- Understanding,
- Saar,
- and Search.

---

# 18a. Translation Module Structure

```text
translation/
├── api/                         # GET /api/v1/translations/verses/{verseId}
├── application/
│   ├── query/                   # TranslationQueryService
│   ├── imports/                 # ImportTranslationPackageUseCase + mutation + probe
│   └── port/                    # PackageFormatValidator, repositories, readers
├── domain/
│   ├── Translation.java / TranslationSource.java / TranslationPackage.java
│   ├── ContentVersionPolicy.java
│   └── ImportFailureCode.java / ContentPackageStatus.java / ImportExecutionStatus.java
└── infrastructure/
    ├── persistence/             # JPA + content package/import adapters (translation.*)
    ├── packageformat/           # Translation Package Format v1 validator + filesystem reader
    ├── importcmd/               # TranslationPackageImportMain (WebApplicationType.NONE)
    └── config/
```

**Implemented now:** `translation.*` persistence (Flyway V007), Package Format v1
importer (admin CLI), synthetic fixture packages, read-only Translation API.

**Not implemented yet:** real translation corpus, language/provider query selection,
Verse Reader composition, commentary/notes, public import HTTP.

V1 published lookup returns the first published row for a Verse ordered by
`provider` ascending (stable tie-break). Explicit provider/language selection is
deferred; do not redesign the API in this foundation.

Translation references Scripture Verse identity only (`scripture.verses.id` FK).
Scripture must not depend on Translation (ADR-012).

---

# 19. Reading Module Structure

```text
reading/
├── api/
│   ├── ReadingProgressController.java
│   ├── ReadingSessionController.java
│   └── TodayInvitationController.java
├── application/
│   ├── progress/
│   ├── sessions/
│   ├── visits/
│   ├── bookmarks/
│   ├── invitation/
│   └── publicapi/
├── domain/
│   ├── ReadingProgress.java
│   ├── ReadingSession.java
│   ├── ReadingPosition.java
│   ├── Bookmark.java
│   └── InvitationType.java
└── infrastructure/
    ├── persistence/
    ├── cache/
    └── config/
```

Today’s Invitation resolution belongs to the Reading application boundary unless a later product-selection module is introduced.

Today’s Invitation remains a derived result rather than an aggregate.

---

# 20. Reflection Module Structure

```text
reflection/
├── api/
├── application/
│   ├── create/
│   ├── update/
│   ├── delete/
│   ├── expand/
│   ├── revision/
│   ├── query/
│   └── publicapi/
├── domain/
│   ├── ReflectionEntry.java
│   ├── ReflectionId.java
│   ├── ReflectionType.java
│   ├── ReflectionContent.java
│   ├── ReflectionStatus.java
│   └── ReflectionRevision.java
└── infrastructure/
    ├── persistence/
    ├── events/
    └── config/
```

Reflection publishes read-only summary access to Journey.

Saar may access Reflection only through an explicit privacy-aware context interface.

---

# 21. Journey Module Structure

```text
journey/
├── api/
│   └── JourneyController.java
├── application/
│   ├── query/
│   ├── grouping/
│   └── publicapi/
├── domain/
│   ├── JourneyMemory.java
│   └── JourneyPeriod.java
└── infrastructure/
    ├── projection/
    └── config/
```

Journey may begin as a query module rather than a persistence-heavy domain.

Its infrastructure should use approved Reflection interfaces or projections.

It should not access Reflection tables directly merely because they share a database.

---

# 22. Guidance Module Structure

```text
guidance/
├── api/
├── application/
│   ├── session/
│   ├── selection/
│   └── publicapi/
├── domain/
│   ├── GuidanceSession.java
│   ├── GuidancePath.java
│   ├── GuidanceSelection.java
│   └── GuidanceSessionStatus.java
└── infrastructure/
    ├── persistence/
    └── config/
```

Guidance owns Reader intent and routing.

It does not own Understanding content or Saar generation.

---

# 23. Understanding Module Structure

```text
understanding/
├── api/
├── application/
│   ├── article/
│   ├── commentary/
│   ├── relatedverse/
│   ├── publication/
│   └── publicapi/
├── domain/
│   ├── UnderstandingArticle.java
│   ├── UnderstandingArticleId.java
│   ├── KeyConcept.java
│   ├── TraditionalInsight.java
│   ├── RelatedVerse.java
│   └── PublicationStatus.java
└── infrastructure/
    ├── persistence/
    ├── publication/
    ├── projection/
    └── config/
```

Understanding publishes source-aware educational content to:

- the mobile application,
- Search,
- and Saar retrieval.

---

# 24. Saar Module Structure

```text
saar/
├── api/
│   ├── ConversationController.java
│   ├── MessageController.java
│   └── GenerationController.java
├── application/
│   ├── conversation/
│   ├── message/
│   ├── generation/
│   ├── retrieval/
│   ├── prompt/
│   ├── validation/
│   └── publicapi/
├── domain/
│   ├── Conversation.java
│   ├── ConversationId.java
│   ├── Message.java
│   ├── MessageRole.java
│   ├── Citation.java
│   ├── GenerationRun.java
│   ├── GroundingStatus.java
│   └── RetrievalRun.java
└── infrastructure/
    ├── persistence/
    ├── provider/
    ├── worker/
    ├── telemetry/
    └── config/
```

Provider-specific SDK code belongs under:

```text
saar/infrastructure/provider/
```

Business code must depend on an internal LLM port.

---

# 25. Search Module Structure

```text
search/
├── api/
│   ├── ScriptureSearchController.java
│   └── ReferenceResolverController.java
├── application/
│   ├── indexing/
│   ├── retrieval/
│   ├── canonical/
│   ├── fulltext/
│   ├── vector/
│   ├── reranking/
│   └── publicapi/
├── domain/
│   ├── KnowledgeSource.java
│   ├── KnowledgeChunk.java
│   ├── RetrievalCandidate.java
│   ├── RetrievalPlan.java
│   └── SearchResult.java
└── infrastructure/
    ├── persistence/
    ├── pgvector/
    ├── embedding/
    ├── worker/
    └── config/
```

Search projections remain rebuildable.

Search should depend on published source interfaces rather than persistence internals.

---

# 26. Platform Structure

```text
platform/
├── authentication/
├── authorization/
├── database/
├── cache/
├── events/
├── jobs/
├── idempotency/
├── observability/
├── storage/
├── configuration/
├── featureflags/
├── web/
└── security/
```

Platform contains shared infrastructure implementations.

Platform must not become a business domain.

Examples of valid Platform code:

- correlation-ID filter,
- OpenTelemetry configuration,
- Redis rate-limit adapter,
- object-storage client,
- job-claiming framework,
- shared Problem Details mapping.

Examples of invalid Platform code:

- selecting Today’s Invitation,
- determining Reflection ownership,
- building Journey Memories,
- choosing Guidance paths,
- interpreting Verse meaning.

---

# 27. Shared Structure

```text
shared/
├── domain/
│   ├── DomainEvent.java
│   ├── AggregateRoot.java
│   └── DomainException.java
├── application/
│   ├── PageCursor.java
│   ├── PageResult.java
│   └── UseCase.java
└── time/
    └── TimeProvider.java
```

Keep this package intentionally small.

A class belongs in `shared` only when:

1. it is genuinely domain-neutral,
2. at least two modules require it,
3. its semantics are identical across those modules,
4. and moving it does not create business coupling.

---

# 28. Backend Dependency Rules

Recommended high-level rule:

```text
api
    ↓
application
    ↓
domain

infrastructure
    ↓
application
    ↓
domain
```

The domain layer depends on no outer layer.

The application layer may depend on domain.

The API and infrastructure layers may depend on application and domain.

---

# 29. Forbidden Backend Dependencies

The following should be prohibited:

```text
domain → api
domain → infrastructure
domain → Spring MVC
domain → provider SDK
application → controller DTOs
application → JPA repositories
one module → another module's infrastructure
one module → another module's persistence entities
```

Examples:

```text
saar.application
    must not import
scripture.infrastructure.persistence.VerseJpaEntity
```

```text
journey.application
    must not import
reflection.infrastructure.persistence.ReflectionJpaRepository
```

---

# 30. Allowed Cross-Module Dependencies

Cross-module access should use public application contracts.

Example:

```text
Reflection Application
    ↓
ScriptureReferenceQuery
```

Allowed concepts include:

- immutable query results,
- intentionally exposed commands,
- domain events,
- stable identifiers,
- and module-neutral value types.

Avoid sharing mutable aggregates across modules.

---

# 31. Module Dependency Direction

A possible dependency graph:

```text
Identity
    ▲
    │
Reading ───────► Scripture
    │
    └──────────► Identity

Reflection ────► Scripture
Reflection ────► Identity

Journey ───────► Reflection
Journey ───────► Scripture

Guidance ──────► Scripture
Guidance ──────► Identity

Understanding ─► Scripture

Search ────────► Scripture
Search ────────► Understanding

Saar ──────────► Scripture
Saar ──────────► Understanding
Saar ──────────► Search
Saar ──────────► Identity
Saar ──────────► Reflection through a privacy-aware public interface
```

Circular dependencies are not allowed.

---

# 32. Avoiding Circular Dependencies

When two modules appear to require each other, reconsider ownership.

Possible solutions:

- introduce a published query interface,
- publish a domain event,
- move a concept to the correct owning module,
- create an application-level orchestration use case,
- or derive a read projection.

Do not solve circular dependencies by importing internals in both directions.

---

# 33. Application Orchestration

Some workflows involve several modules.

Example:

```text
Resolve Today’s Invitation
    ↓
Reading queries progress
    ↓
Reflection checks unfinished draft
    ↓
Scripture loads destination preview
```

The orchestration should live in the module owning the use case.

For Today’s Invitation, Reading is the likely owner.

It calls public interfaces from Reflection and Scripture.

---

# 34. Domain Events

Domain events should be defined by the module that owns the event.

Example:

```text
reflection/domain/ReflectionCreated.java
```

Potential events:

```text
VerseOpened
ReadingPositionUpdated
ReflectionCreated
ReflectionUpdated
ReflectionDeleted
GuidancePathSelected
UnderstandingViewed
SaarResponseGenerated
```

Events should describe completed business facts.

Avoid imperative event names such as:

```text
UpdateJourneyNow
```

Prefer:

```text
ReflectionCreated
```

---

# 35. Event Delivery Structure

Initial in-process event delivery may use:

```text
platform/events/
├── DomainEventPublisher.java
├── SpringDomainEventPublisher.java
└── TransactionalEventHandler.java
```

Business modules define events.

Platform implements delivery.

Events should not expose JPA entities.

---

# 36. Worker Structure

Background work should be organized around application use cases.

Example:

```text
saar/infrastructure/worker/
├── SaarGenerationWorker.java
└── GenerationJobClaimRepository.java
```

The worker:

1. claims work,
2. invokes an application use case,
3. records safe operational status.

The worker should not contain the complete generation workflow itself.

---

# 37. Prompt Storage

Versioned Saar prompts may live under:

```text
backend/src/main/resources/prompts/saar/
├── system/
│   └── v1.txt
├── response/
│   └── v1-schema.json
└── README.md
```

They may alternatively live as source-controlled templates inside the Saar module.

Every production prompt should have:

- a stable version,
- an owner,
- a review history,
- and corresponding tests.

Do not edit production prompts through undocumented manual configuration.

---

# 38. Database Migration Structure

Recommended pattern (module-owned, global Flyway sequence):

```text
backend/src/main/resources/db/migration/
├── V001__initialize_database_extensions.sql
├── V002__create_scripture_chapters.sql
├── V003__seed_scripture_chapters.sql
├── V004__create_scripture_verses.sql
├── V005__seed_scripture_verses.sql
├── V006__create_scripture_content_packages.sql
└── … later module migrations as slices land
```

**Implemented today (Scripture foundation):** V001–V006 as listed above.

`V006` owns package import provenance (`content_packages`, `content_package_imports`) and Verse
lineage columns. It is **not** the historical placeholder `create_understanding_schema` name from
earlier planning sketches.

A global Flyway sequence is simplest for one deployable application.

Each migration should clearly state its owning module.

---

# 39. Migration Ownership

The module owning a table owns its migrations.

Example:

```text
Reflection module
    owns
reflection.reflection_entries
```

Even when migrations share one global folder, naming and review should preserve module ownership.

Do not allow unrelated modules to alter another module’s tables casually.

---

# 40. Migration Rules

Migrations should be:

- forward-only after deployment,
- deterministic,
- tested,
- backward-compatible during rolling releases,
- and safe against production data volume.

Do not rely on:

```text
spring.jpa.hibernate.ddl-auto=update
```

outside disposable local experiments.

Production should use:

```text
validate
```

or equivalent schema validation.

---

# 41. Persistence Mapping

Domain objects and JPA entities may be separate.

Example:

```text
ReflectionEntry
    domain aggregate

ReflectionJpaEntity
    persistence model
```

Advantages:

- domain does not require JPA annotations,
- storage can evolve independently,
- persistence relationships do not define business ownership,
- and lazy-loading concerns remain outside domain logic.

This introduces mapping code but preserves architectural clarity.

---

# 42. Repository Interfaces

Repository contracts belong to application or domain code.

Example:

```java
public interface ReflectionRepository {

    Optional<ReflectionEntry> findOwnedBy(
        ReflectionId reflectionId,
        UserId userId
    );

    ReflectionEntry save(ReflectionEntry reflection);
}
```

Implementations belong in infrastructure.

Avoid exposing:

- `JpaRepository`,
- `EntityManager`,
- or database-specific query objects

to application use cases.

---

# 43. Query Models

Read-heavy endpoints may use dedicated query services and projections.

Examples:

```text
JourneyMemoryView
ChapterVerseListItem
ConversationSummary
```

A query model need not reconstruct a full aggregate when no business mutation occurs.

This is a practical form of CQRS inside the modular monolith.

Do not create separate infrastructure merely to claim full CQRS.

---

# 44. Transaction Boundaries

Transactions belong primarily in application use cases.

Example:

```text
CreateReflectionUseCase
    starts transaction
    validates Verse
    creates aggregate
    persists Reflection
    publishes event
    commits
```

External calls must not occur inside long database transactions.

Examples to keep outside transactions:

- AI-provider invocation,
- embedding generation,
- object-storage upload,
- notification delivery,
- and long-running indexing.

---

# 45. Mobile Application Root Structure

Antar V1 uses a mobile-first React Native application.

Recommended root:

```text
mobile/
├── README.md
├── package.json
├── package-lock.json
├── app.json
├── eas.json
├── babel.config.js
├── metro.config.js
├── tsconfig.json
├── assets/
├── src/
├── tests/
└── tooling/
```

Depending on the chosen Expo routing strategy, the project may also contain a root-level:

```text
app/
```

directory.

The project should choose one routing convention and use it consistently.

---

# 46. Mobile Technology Direction

Recommended V1 stack:

```text
React Native
TypeScript
Expo
```

Expo is the initial recommendation because it provides:

- faster project initialization,
- shared iOS and Android tooling,
- managed development builds,
- simpler signing and distribution,
- Expo Application Services integration,
- and reduced native-configuration overhead.

Expo should be reconsidered only when a validated product requirement requires unsupported native behavior or tighter native control.

---

# 47. Mobile Source Structure

Recommended source structure:

```text
mobile/src/
├── app/
├── navigation/
├── features/
├── design-system/
├── services/
├── shared/
├── storage/
└── test/
```

Responsibilities:

```text
app/
    application initialization,
    global providers,
    error boundaries,
    and startup coordination

navigation/
    route definitions,
    navigation stacks,
    deep links,
    and navigation guards

features/
    product experiences organized by responsibility

design-system/
    tokens, foundations, primitives,
    components, and compositions

services/
    generated and handwritten backend clients

shared/
    cross-feature infrastructure
    with no product ownership

storage/
    secure storage,
    local drafts,
    local cache,
    and storage migrations

test/
    shared test builders,
    fixtures,
    and rendering utilities
```

---

# 48. Mobile Feature Organization

Organize the application around approved product experiences.

```text
mobile/src/features/
├── authentication/
├── home/
├── library/
├── chapter/
├── verse/
├── reflection/
├── journey/
├── guidance/
├── understanding/
├── saar/
├── search/
└── settings/
```

Each feature owns:

- screens,
- feature-specific components,
- hooks,
- state,
- feature API calls,
- navigation integration,
- local storage behavior where applicable,
- and tests.

---

# 49. Mobile Feature Anatomy

Example:

```text
features/reflection/
├── api/
│   ├── reflectionClient.ts
│   └── reflectionQueries.ts
├── components/
│   ├── QuickReflection.tsx
│   ├── JournalEditor.tsx
│   └── SaveStatus.tsx
├── model/
│   ├── reflectionTypes.ts
│   ├── reflectionState.ts
│   └── reflectionValidation.ts
├── hooks/
│   ├── useReflection.ts
│   └── useReflectionAutosave.ts
├── screens/
│   └── ReflectionScreen.tsx
├── navigation/
│   └── reflectionRoutes.ts
└── tests/
    ├── ReflectionScreen.test.tsx
    └── useReflectionAutosave.test.ts
```

Feature-internal code should remain colocated.

Do not create global folders containing all:

- hooks,
- screens,
- models,
- or state.

---

# 50. Mobile Application Initialization

Recommended:

```text
mobile/src/app/
├── AppProviders.tsx
├── AppBootstrap.tsx
├── AppErrorBoundary.tsx
├── QueryProvider.tsx
├── AuthenticationProvider.tsx
├── ThemeProvider.tsx
└── AccessibilityProvider.tsx
```

Startup responsibilities may include:

- loading secure authentication state,
- loading reading preferences,
- initializing API clients,
- restoring safe local drafts,
- applying storage migrations,
- registering deep links,
- and initializing privacy-safe telemetry.

Business logic should remain inside features or domain-facing services.

---

# 51. Mobile Navigation Structure

Recommended conceptual navigation:

```text
Root Navigator
├── Authentication Flow
└── Application Flow
    ├── Home
    ├── Library
    ├── Chapter
    ├── Verse
    ├── Reflection
    ├── Journey
    ├── Guidance
    ├── Understanding
    ├── Saar
    ├── Search
    └── Settings
```

The exact navigation library remains an implementation decision.

The navigation architecture should support:

- deep links to canonical Verses,
- restoration of reading position,
- protected Reader-owned screens,
- passing stable resource identifiers,
- and platform back-navigation behavior.

Bottom navigation should not be introduced unless later product validation explicitly requires it.

---

# 52. Navigation Ownership

Global navigation configuration belongs under:

```text
mobile/src/navigation/
```

Feature-specific navigation metadata belongs inside each feature.

Example:

```text
features/reflection/navigation/reflectionRoutes.ts
```

The global navigator composes feature routes.

Feature screens should not depend on unrelated navigation internals.

---

# 53. Deep Linking

The mobile application should eventually support deep links such as:

```text
antar://verse/2.47
antar://reflection/{reflectionId}
antar://journey
```

Canonical Verse links should resolve through the backend or a trusted local Scripture map.

Deep links must not bypass:

- authentication,
- ownership checks,
- or publication status.

---

# 54. Mobile Design System

Recommended:

```text
mobile/src/design-system/
├── tokens/
│   ├── typography.ts
│   ├── spacing.ts
│   ├── color.ts
│   ├── radius.ts
│   └── motion.ts
├── foundations/
│   ├── ThemeProvider.tsx
│   ├── accessibility.ts
│   └── responsiveText.ts
├── primitives/
├── components/
├── compositions/
└── index.ts
```

The implementation hierarchy mirrors the design language:

```text
Foundations
    ↓
Primitives
    ↓
Components
    ↓
Compositions
    ↓
Experiences
```

Today’s Invitation belongs under compositions.

---

# 55. Design-System Boundaries

The design system should contain reusable visual behavior.

It should not own feature-specific business rules.

Valid design-system examples:

```text
Text
Stack
Divider
PressableText
ScreenContainer
SaveStatusIndicator
VerseReference
```

Feature-owned examples:

```text
Today's Invitation selection
Reflection autosave workflow
Journey monthly grouping
Saar grounding behavior
```

A component may be visually reusable while its business orchestration remains feature-owned.

---

# 56. Mobile API Client Structure

Recommended:

```text
mobile/src/services/
├── api/
│   ├── apiClient.ts
│   ├── authenticationInterceptor.ts
│   ├── errorMapper.ts
│   └── requestId.ts
├── generated/
└── configuration/
```

OpenAPI may generate:

- TypeScript request types,
- response types,
- and low-level clients.

Generated code should live under:

```text
mobile/src/services/generated/
```

Handwritten product-facing clients should wrap generated clients where necessary.

Do not place handwritten product behavior inside generated files.

---

# 57. Feature API Integration

Feature-specific API wrappers should remain in the feature.

Example:

```text
features/reflection/api/reflectionClient.ts
```

It may call:

```text
services/generated/ReflectionsApi
```

and translate backend models into feature models.

This protects the feature from direct coupling to generated transport details.

---

# 58. Mobile State Management

State should be owned at the narrowest practical level.

Potential state categories:

```text
Server State
Feature UI State
Authentication State
Navigation State
Local Draft State
Global Preferences
```

Do not introduce one global application store for all state by default.

Recommended principles:

- server state uses a query and caching layer,
- feature UI state remains local where possible,
- authentication has one controlled global provider,
- local Reflection drafts use a dedicated persistence abstraction,
- and design-system state does not absorb product state.

The exact state-management libraries remain implementation decisions.

---

# 59. Mobile Storage Structure

Recommended:

```text
mobile/src/storage/
├── secure/
│   ├── secureStorage.ts
│   └── authenticationStorage.ts
├── drafts/
│   ├── reflectionDraftStorage.ts
│   └── draftTypes.ts
├── cache/
│   ├── scriptureCache.ts
│   └── cachePolicy.ts
├── migrations/
│   ├── storageMigration.ts
│   └── versions/
└── index.ts
```

---

# 60. Secure Storage

Use platform-secure storage for:

- authentication tokens,
- refresh tokens where applicable,
- sensitive session material,
- and approved private secrets.

Do not store authentication tokens in ordinary unencrypted local storage.

Storage implementations should remain behind interfaces so they can be tested and replaced.

---

# 61. Reflection Draft Storage

Reflection drafts may be stored locally to survive:

- temporary network loss,
- application backgrounding,
- process termination,
- and interrupted autosave.

The implementation must define:

- whether drafts are encrypted,
- when drafts expire,
- how drafts are associated with a Reader and Verse,
- how drafts are deleted after server persistence,
- and how conflicts are handled.

The user interface should distinguish:

```text
Saved locally
Saving
Saved to server
Sync failed
```

The server remains the source of truth for durable saved Reflections.

---

# 62. Offline and Intermittent Connectivity

V1 does not require complete offline synchronization.

The mobile client should still support graceful intermittent connectivity.

Initial behavior may include:

- cached published Scripture,
- preserved local Reflection drafts,
- retry of pending saves,
- visible synchronization state,
- and safe conflict recovery.

Do not queue arbitrary mutations indefinitely without visibility.

---

# 63. Scripture Caching

Published Scripture is a strong candidate for local caching because it is:

- read-heavy,
- versioned,
- and mostly immutable.

The cache should store:

- content version,
- Translation source,
- language,
- and retrieval time.

The application should invalidate or refresh content when versions change.

Private Reflections and Saar Conversations should not use the same cache policy as public Scripture.

---

# 64. Mobile Error Handling

Recommended:

```text
mobile/src/shared/errors/
├── AppError.ts
├── ApiProblem.ts
├── errorMapper.ts
├── RetryPolicy.ts
└── ErrorState.tsx
```

The client should distinguish:

- validation errors,
- authentication failures,
- authorization failures,
- offline state,
- stale version conflicts,
- provider unavailability,
- grounding failures,
- and unexpected errors.

Do not show raw backend stack traces or provider errors.

---

# 65. Optimistic Concurrency in Mobile

Mutable server resources such as Reflections may use:

```text
ETag
If-Match
```

or equivalent version fields.

When a stale Reflection update occurs, the mobile application should:

- preserve the local text,
- avoid silent overwrite,
- reload the server version where appropriate,
- and offer a safe recovery path.

Private writing should never be discarded automatically.

---

# 66. Mobile Authentication Structure

Recommended:

```text
mobile/src/features/authentication/
├── api/
├── components/
├── hooks/
├── model/
├── screens/
├── navigation/
└── tests/
```

Secure token persistence remains under:

```text
mobile/src/storage/secure/
```

Authentication business flow belongs to the feature.

Storage implementation belongs to the storage layer.

---

# 67. Mobile Accessibility

The client must support:

- screen-reader semantics,
- dynamic text sizing,
- adequate touch targets,
- logical focus order,
- reduced motion,
- clear save-status announcements,
- semantic scripture structure,
- and sufficient contrast in final visual design.

Accessibility belongs in both the design system and individual features.

---

# 68. Mobile Platform-Specific Code

Platform-specific behavior should be isolated.

Example:

```text
mobile/src/shared/platform/
├── ios/
├── android/
└── common/
```

Prefer React Native or Expo abstractions when they satisfy the requirement.

Use platform-specific implementations only where necessary.

Avoid scattering platform checks throughout product features.

---

# 69. Native Modules

Native modules should be introduced only when:

- Expo or React Native does not provide the required capability,
- the requirement is validated,
- security and maintenance implications are understood,
- and the dependency is isolated behind an application interface.

Native code should not leak directly into feature business logic.

---

# 70. Mobile Configuration

Recommended:

```text
mobile/src/services/configuration/
├── environment.ts
├── apiConfiguration.ts
├── featureFlags.ts
└── buildInfo.ts
```

Configuration may include:

```text
API base URL
Environment name
App version
Build number
Safe feature flags
Telemetry configuration
```

Do not include production secrets inside the mobile bundle.

Anything shipped in the application must be treated as publicly discoverable.

---

# 71. Mobile Environment Files

Potential environment separation:

```text
development
preview
staging
production
```

Environment configuration should alter:

- API endpoints,
- telemetry environment,
- authentication configuration,
- and feature rollout.

It should not alter core domain behavior.

---

# 72. Expo Configuration

Recommended project files:

```text
app.json
eas.json
```

They may define:

- application identifiers,
- versioning,
- build profiles,
- platform permissions,
- icons and splash assets,
- deep linking,
- and release channels.

Permissions should be minimal.

Do not request access to:

- contacts,
- location,
- camera,
- microphone,
- notifications,
- or other device capabilities

without an approved product need.

---

# 73. Mobile Delivery

Recommended delivery flow:

```text
Pull Request
    ↓
TypeScript Check
    ↓
Lint
    ↓
Unit and Component Tests
    ↓
Mobile Build Validation
    ↓
Internal Development Build
    ↓
Staging API Validation
    ↓
Preview Distribution
    ↓
App Store / Play Store Release
```

Expo Application Services may support:

- development builds,
- preview builds,
- production builds,
- signing,
- and controlled over-the-air updates.

---

# 74. Over-the-Air Updates

Over-the-air updates may be used for compatible JavaScript and asset changes where approved.

They must not be used to:

- bypass native store requirements,
- ship incompatible native-code assumptions,
- change critical privacy behavior without review,
- or create uncontrolled version fragmentation.

Every update should retain:

- release version,
- runtime compatibility,
- source commit,
- and rollback capability.

---

# 75. Mobile Version Compatibility

Mobile clients may remain installed after the backend changes.

The backend must account for version skew.

The mobile client should send safe metadata such as:

```text
appVersion
buildNumber
platform
operatingSystemVersion
apiVersion
```

The backend should preserve a reasonable compatibility window.

The application should handle unsupported-version behavior gracefully.

---

# 76. Mobile Telemetry

Mobile telemetry may include:

- application start success,
- screen load timing,
- network failure category,
- crash metadata,
- safe build information,
- and approved feature events.

Do not include:

- Reflection content,
- Saar Message content,
- search queries,
- access tokens,
- full URLs containing private identifiers,
- or private local drafts.

Crash reports must not contain private Reader content.

---

# 77. Mobile Testing Structure

Recommended:

```text
mobile/tests/
├── integration/
├── navigation/
├── accessibility/
└── end-to-end/
```

Feature-local tests remain inside each feature.

Shared test utilities:

```text
mobile/src/test/
├── renderWithProviders.tsx
├── factories/
├── fixtures/
├── mocks/
└── assertions/
```

---

# 78. Mobile Unit Tests

Unit tests should cover:

- feature models,
- validation,
- state transitions,
- local draft behavior,
- error mapping,
- and deterministic formatting.

Unit tests should avoid rendering the entire application when not necessary.

---

# 79. Mobile Component Tests

Component tests should verify:

- rendering,
- accessibility labels,
- interaction,
- loading states,
- save states,
- error states,
- and feature behavior.

Examples:

```text
QuickReflection.test.tsx
JournalEditor.test.tsx
TodayInvitation.test.tsx
SaarCitation.test.tsx
```

---

# 80. Mobile Navigation Tests

Navigation tests should verify:

- authentication guards,
- deep links,
- back-navigation behavior,
- Verse-to-Reflection flow,
- Guidance-to-Understanding flow,
- and ownership-dependent routes.

---

# 81. Mobile End-to-End Tests

End-to-end tests should cover critical Reader journeys.

Examples:

```text
Open Home
    ↓
Open Today’s Invitation
    ↓
Read Verse
    ↓
Save Quick Reflection
    ↓
Continue Reading
```

```text
Open Verse
    ↓
Reflect More
    ↓
Save Deep Reflection
    ↓
Open Journey
    ↓
Reopen Reflection
```

```text
Read Verse
    ↓
Open Guidance
    ↓
View Understanding
    ↓
Ask Saar
    ↓
Receive cited response
```

---

# 82. Mobile Accessibility Tests

Automated and manual accessibility review should verify:

- screen-reader traversal,
- dynamic text,
- focus order,
- touch targets,
- reduced motion,
- button and text-action semantics,
- and form announcements.

---

# 83. Infrastructure Structure

Recommended:

```text
infrastructure/
├── README.md
├── environments/
│   ├── local/
│   ├── staging/
│   └── production/
├── modules/
│   ├── network/
│   ├── application/
│   ├── postgres/
│   ├── redis/
│   ├── storage/
│   ├── observability/
│   └── secrets/
├── deployment/
└── policies/
```

The exact structure depends on the selected infrastructure-as-code tool.

Mobile store configuration and Expo deployment configuration remain inside `mobile/` unless shared release automation justifies another location.

---

# 84. Local Development Infrastructure

```text
infrastructure/environments/local/
├── compose.yaml
├── postgres/
├── redis/
└── mock-services/
```

A root `compose.yaml` may reference these definitions for convenience.

Local infrastructure should include pgvector support.

The mobile application should connect to the local backend through environment-specific configuration.

---

# 85. Scripts Structure

```text
scripts/
├── development/
│   ├── start-local.sh
│   ├── stop-local.sh
│   └── reset-database.sh
├── database/
│   ├── verify-migrations.sh
│   └── seed-scripture.sh
├── content/
│   ├── validate-source-metadata.py
│   └── import-scripture.py
├── search/
│   ├── rebuild-index.sh
│   └── verify-corpus.sh
├── mobile/
│   ├── create-development-build.sh
│   ├── run-ios.sh
│   ├── run-android.sh
│   └── verify-mobile-config.sh
└── release/
    └── smoke-test.sh
```

Scripts should be:

- documented,
- safe by default,
- environment-aware,
- and resistant to accidental production execution.

---

# 86. Backend Test Structure

```text
backend/src/test/java/com/antar/
├── architecture/
├── identity/
├── scripture/
├── reading/
├── reflection/
├── journey/
├── guidance/
├── understanding/
├── saar/
├── search/
├── platform/
└── support/
```

Tests should mirror production module ownership.

---

# 87. Backend Unit Tests

Unit tests should live near the module they validate.

Examples:

```text
reflection/domain/ReflectionEntryTest.java
reading/domain/ReadingProgressTest.java
saar/application/RetrievalPlannerTest.java
```

Unit tests should avoid starting the full Spring context.

They should validate:

- domain invariants,
- value objects,
- application workflows,
- mapping,
- and deterministic policies.

---

# 88. Backend Integration Tests

Integration tests should validate real infrastructure behavior.

Examples:

```text
reflection/infrastructure/ReflectionRepositoryIntegrationTest.java
search/infrastructure/PgVectorRetrievalIntegrationTest.java
platform/idempotency/IdempotencyIntegrationTest.java
```

Use:

- PostgreSQL Testcontainers,
- Redis Testcontainers where needed,
- and AI provider fakes.

Do not use H2 as the primary substitute for PostgreSQL-specific behavior.

---

# 89. Backend API Tests

Controller or HTTP integration tests should validate:

- routes,
- authentication,
- authorization,
- validation,
- status codes,
- serialization,
- idempotency,
- ETag behavior,
- and Problem Details.

Example:

```text
reflection/api/ReflectionApiIntegrationTest.java
```

---

# 90. Security Tests

Create explicit security test suites.

```text
backend/src/test/java/com/antar/security/
├── CrossUserReflectionAccessTest.java
├── CrossUserConversationAccessTest.java
├── ReflectionAiContextAuthorizationTest.java
├── AdminAuthorizationTest.java
└── PrivateLoggingTest.java
```

Cross-user isolation should never be assumed from ordinary feature tests.

---

# 91. Architecture Tests

Recommended package:

```text
backend/src/test/java/com/antar/architecture/
├── ModuleDependencyTest.java
├── LayerDependencyTest.java
├── DomainPurityTest.java
├── ControllerBoundaryTest.java
└── PersistenceBoundaryTest.java
```

Potential tools:

- ArchUnit,
- Spring Modulith,
- or custom build checks.

---

# 92. Example Architecture Rules

Possible rules:

```text
domain packages must not depend on api packages

domain packages must not depend on infrastructure packages

application packages must not depend on Spring MVC

modules must not access another module’s infrastructure package

controllers must not access repositories directly

JPA entities must remain inside infrastructure persistence packages

provider SDKs must remain inside provider adapters
```

These rules should fail the build when violated.

---

# 93. Spring Modulith

Spring Modulith may be evaluated to:

- describe application modules,
- validate module dependencies,
- test module boundaries,
- and produce module documentation.

It should support the architecture rather than dictate domain design.

Its adoption remains an implementation decision.

---

# 94. Naming Conventions

Use business language consistently.

Preferred:

```text
ReflectionEntry
JourneyMemory
UnderstandingArticle
ReadingProgress
GuidancePath
Conversation
Citation
```

Avoid generic classes such as:

```text
DataManager
CommonService
UtilityService
Helper
Processor
Thing
RecordData
```

Names should communicate ownership and behavior.

---

# 95. Use-Case Naming

Prefer verb-oriented application use cases.

Examples:

```text
CreateReflectionUseCase
UpdateReadingProgressUseCase
ResolveTodayInvitationUseCase
SelectGuidancePathUseCase
SubmitSaarMessageUseCase
```

Avoid one oversized service such as:

```text
ReflectionService
```

containing every operation without clear use-case boundaries.

A module-level facade may exist, but internal use cases should remain explicit.

---

# 96. DTO Naming

Transport models should be explicit.

Examples:

```text
CreateReflectionRequest
ReflectionResponse
ReflectionSummaryResponse
UpdateReadingPreferencesRequest
SaarMessageResponse
```

Avoid reusing:

- persistence entities,
- domain aggregates,
- or one generic DTO

across unrelated contracts.

---

# 97. Mapping

Keep mappings explicit.

Examples:

```text
ReflectionApiMapper
ReflectionPersistenceMapper
VerseResponseMapper
```

Mapping code is acceptable when it protects boundaries.

Avoid large reflection-based mapping frameworks that obscure behavior unless the tradeoff is justified.

---

# 98. Exception Structure

Domain exceptions:

```text
ReflectionContentEmpty
ConversationClosed
InvalidCanonicalReference
```

Application exceptions:

```text
ReflectionNotFound
ReflectionAccessDenied
PublishedUnderstandingUnavailable
```

Transport mapping:

```text
ProblemDetailsExceptionHandler
```

Avoid throwing raw persistence or provider exceptions through controllers.

---

# 99. Configuration Structure

Backend configuration classes should remain near the infrastructure they configure.

Examples:

```text
saar/infrastructure/config/SaarProviderConfiguration.java
search/infrastructure/config/PgVectorConfiguration.java
reflection/infrastructure/config/ReflectionConfiguration.java
```

Global configuration belongs under Platform only when genuinely global.

Mobile configuration remains under:

```text
mobile/src/services/configuration/
```

---

# 100. Package and Module Visibility

Prefer:

- package-private backend implementation classes,
- public interfaces only where required,
- narrow constructors,
- immutable application results,
- immutable value objects,
- and non-exported mobile feature internals.

Not every class, component, function, or hook needs to be globally exported.

---

# 101. Backend Build Profiles

The backend may support profiles such as:

```text
local
test
staging
production
ai-mock
```

Profiles should alter configuration, not domain behavior.

Avoid placing product rules behind Spring-profile conditionals.

Use feature flags or explicit application configuration for approved behavior differences.

---

# 102. Mobile Build Profiles

Expo or equivalent mobile build profiles may include:

```text
development
preview
staging
production
```

Profiles may alter:

- API base URL,
- application identifier,
- signing configuration,
- telemetry environment,
- and approved feature flags.

They must not contain secrets that cannot safely exist in a distributed application bundle.

---

# 103. Seed Data

Backend seed data should remain separate from production migrations.

Recommended:

```text
backend/src/test/resources/fixtures/
scripts/content/
```

Local seed workflows may import:

- sample Chapters,
- sample Verses,
- sample Translations,
- sample Understanding content,
- and synthetic Reader data.

Do not place large production Scripture content inside ad hoc development migrations without a defined content strategy.

---

# 104. Content Repository Consideration

Antar may eventually separate reviewed content from application source code.

Potential future structure:

```text
content/
├── scripture/
├── translations/
├── commentary/
├── understanding/
├── licenses/
└── manifests/
```

This decision depends on:

- content volume,
- licensing,
- editorial workflows,
- and publication process.

For V1, approved content may be imported through controlled files and scripts.

---

# 105. Generated Files

Generated files should be identifiable and isolated.

Examples:

```text
mobile/src/services/generated/
backend/target/
docs/api/generated/
```

Do not manually edit generated files.

Generation commands should be documented.

---

# 106. Repository Automation

Recommended `.github` structure:

```text
.github/
├── workflows/
│   ├── backend-ci.yml
│   ├── mobile-ci.yml
│   ├── security-scan.yml
│   ├── backend-container-build.yml
│   ├── mobile-preview-build.yml
│   └── deploy-staging.yml
├── pull_request_template.md
├── CODEOWNERS
└── dependabot.yml
```

---

# 107. Code Ownership

A future `CODEOWNERS` file may assign review ownership by domain.

Example:

```text
/backend/src/main/java/com/antar/scripture/    @scripture-reviewers
/backend/src/main/java/com/antar/saar/         @ai-reviewers
/mobile/src/features/reflection/               @mobile-reviewers
/docs/architecture/                            @architecture-reviewers
/design/                                       @design-reviewers
```

In an early single-developer project, this structure still documents intended future ownership.

---

# 108. Pull Request Scope

Prefer focused pull requests.

Examples:

```text
Add Verse canonical-reference resolver

Add Reflection optimistic locking

Add Journey monthly grouping query

Add Saar generation persistence

Add mobile Quick Reflection autosave

Add mobile Verse deep-link handling
```

Avoid mixing:

- design rewrites,
- database migrations,
- backend architecture changes,
- and unrelated mobile work

without a clear reason.

---

# 109. Module README Files

Each backend module should include a short README.

Example:

```text
backend/src/main/java/com/antar/reflection/README.md
```

It should explain:

- purpose,
- owned concepts,
- published interfaces,
- dependencies,
- data ownership,
- important invariants,
- and current implementation status.

Mobile features may also include a short README when behavior is complex.

Example:

```text
mobile/src/features/saar/README.md
```

Avoid duplicating full architecture documents.

---

# 110. Repository README

The root `README.md` should provide:

- product summary,
- architecture summary,
- repository map,
- local setup,
- primary commands,
- documentation links,
- testing instructions,
- and current milestone.

It should not attempt to contain every detail from the architecture documents.

---

# 111. Developer Commands

Provide a small stable command surface.

Potential backend commands:

```text
cd backend
./mvnw test
./mvnw verify
./mvnw spring-boot:run
```

Potential infrastructure command:

```text
docker compose up
```

Potential mobile commands:

```text
cd mobile
npm install
npx expo start
npm test
npm run typecheck
```

A task runner or Makefile may be added if it improves consistency.

---

# 112. Static Analysis

Backend checks may include:

- compiler warnings,
- Checkstyle or equivalent,
- SpotBugs,
- dependency vulnerability scans,
- ArchUnit,
- and test coverage.

Mobile checks may include:

- TypeScript strict mode,
- ESLint,
- formatting,
- unit tests,
- component tests,
- and accessibility checks.

Static analysis should catch meaningful problems rather than produce routinely ignored noise.

---

# 113. Dependency Management

Backend:

- use Maven dependency management,
- pin direct dependencies where practical,
- review major upgrades,
- and avoid unnecessary framework overlap.

Mobile:

- commit the package lock file,
- review dependency additions,
- avoid redundant UI libraries,
- monitor security advisories,
- and prefer Expo-compatible dependencies where practical.

Do not introduce dependencies merely to avoid writing a small amount of clear code.

---

# 114. Avoiding Premature Backend Multi-Module Builds

A Maven multi-module build is not required initially.

Consider splitting build modules when:

- compile times become substantial,
- teams require independent ownership,
- architecture tests are insufficient,
- a module becomes independently deployable,
- or dependency isolation requires stronger enforcement.

Package boundaries plus architecture tests are sufficient for the initial modular monolith.

---

# 115. Future Backend Multi-Module Structure

A future structure may become:

```text
backend/
├── pom.xml
├── antar-application/
├── antar-identity/
├── antar-scripture/
├── antar-reading/
├── antar-reflection/
├── antar-journey/
├── antar-guidance/
├── antar-understanding/
├── antar-saar/
├── antar-search/
└── antar-platform/
```

This should be introduced only when it materially improves the system.

---

# 116. Future Service Extraction

The package structure should support extraction.

Example Saar extraction:

```text
com.antar.saar
    ↓
future saar-service
```

Extraction is easier when Saar already owns:

- application workflows,
- provider adapters,
- persistence,
- public interfaces,
- and observability.

Extraction is harder when Saar imports another module’s repositories and entities directly.

---

# 117. Extraction Compatibility Rules

To preserve extraction options:

- cross-module references use stable identifiers,
- public interfaces use transport-neutral models,
- no shared JPA entities exist,
- no cross-module table writes occur,
- external provider logic remains isolated,
- and events describe business facts.

Do not distort V1 with distributed-system complexity solely for possible future extraction.

---

# 118. Repository Security

The repository must not contain:

- production secrets,
- private keys,
- database dumps with Reader data,
- unlicensed source content,
- private Reader exports,
- provider request logs,
- mobile signing secrets,
- or production authentication tokens.

Secret scanning should run in CI.

Large approved content files should retain licensing metadata.

---

# 119. Mobile Secret Boundaries

The mobile application bundle is distributed to Reader devices.

Values inside the bundle must not be treated as secret.

Do not place:

- AI provider keys,
- database credentials,
- privileged backend tokens,
- signing secrets,
- or administrative credentials

inside the mobile application.

Mobile API requests should use Reader authentication and backend-controlled capabilities.

---

# 120. Branch Strategy

A simple strategy is sufficient.

Recommended:

```text
main
+
short-lived feature branches
```

Requirements:

- protected `main`,
- pull-request review where practical,
- required CI checks,
- and no direct production deployment from unverified branches.

Avoid complex long-lived branching models without need.

---

# 121. Release Tags

Production releases should receive immutable tags.

Example:

```text
v0.1.0
v0.2.0
v1.0.0
```

The backend deployed artifact should record:

- release tag,
- Git commit,
- migration version,
- prompt version,
- and retrieval-policy version.

The mobile release should record:

- release tag,
- Git commit,
- app version,
- build number,
- platform,
- and compatible API version.

---

# 122. Architecture Decision Workflow

When a meaningful architectural choice changes, create or update an ADR.

Examples:

- changing from PostgreSQL jobs to a queue,
- extracting Saar,
- introducing AI streaming,
- changing the vector platform,
- enabling Reflection AI context by default,
- altering the source-of-truth hierarchy,
- changing from Expo to a custom native setup,
- or introducing a web client.

Do not bury major decisions only inside pull-request discussion.

---

# 123. Definition of Done for a Backend Feature

A backend feature is complete when the appropriate items are satisfied:

- domain rules implemented,
- application use case implemented,
- API contract aligned,
- persistence implemented,
- authorization enforced,
- validation added,
- unit tests added,
- integration tests added,
- architecture rules pass,
- observability added,
- documentation updated,
- migrations included,
- and private content excluded from logs.

Not every feature requires every item, but omissions should be intentional.

---

# 124. Definition of Done for a Mobile Experience

A mobile experience is complete when:

- it fulfills the approved screen responsibility,
- it uses documented design-system components,
- loading, empty, error, and recovery states exist,
- accessibility is verified,
- API behavior is integrated,
- intermittent connectivity is handled appropriately,
- private data is stored safely,
- local and server save states are distinguishable,
- telemetry excludes private content,
- and tests cover meaningful behavior.

---

# 125. Initial Repository Creation Sequence

Recommended sequence:

```text
1. Create top-level repository structure.

2. Create backend Spring Boot application.

3. Add package-level domain modules.

4. Add backend architecture tests.

5. Add PostgreSQL, pgvector, and Redis local setup.

6. Add Flyway.

7. Create the React Native and Expo mobile application.

8. Create the mobile design-system foundations.

9. Implement Scripture backend.

10. Implement Library, Chapter, and Verse mobile experiences.

11. Add Reading Progress and Today’s Invitation.

12. Implement Home mobile experience.

13. Add Reflection backend.

14. Implement Quick and Deep Reflection mobile experiences.

15. Add Journey backend projection and mobile experience.

16. Add Understanding and Guidance.

17. Add Search projections and mobile Search.

18. Add Saar pipeline and mobile Conversation experience.

19. Add Settings and privacy preferences.

20. Add deployment, observability, and release infrastructure.
```

---

# 126. Initial Backend Skeleton

```text
backend/src/main/java/com/antar/
├── AntarApplication.java
├── identity/
│   └── IdentityModule.java
├── scripture/
│   └── ScriptureModule.java
├── reading/
│   └── ReadingModule.java
├── reflection/
│   └── ReflectionModule.java
├── journey/
│   └── JourneyModule.java
├── guidance/
│   └── GuidanceModule.java
├── understanding/
│   └── UnderstandingModule.java
├── saar/
│   └── SaarModule.java
├── search/
│   └── SearchModule.java
├── platform/
│   └── PlatformModule.java
└── shared/
```

Each module may begin with only:

- marker type,
- README,
- package documentation,
- and architecture tests.

Do not generate empty controller, service, repository, and entity files merely to fill the structure.

---

# 127. Initial Mobile Skeleton

```text
mobile/src/
├── app/
│   ├── AppBootstrap.tsx
│   ├── AppProviders.tsx
│   └── AppErrorBoundary.tsx
├── navigation/
│   ├── RootNavigator.tsx
│   ├── AuthenticationNavigator.tsx
│   └── ApplicationNavigator.tsx
├── features/
│   ├── authentication/
│   ├── home/
│   ├── library/
│   ├── chapter/
│   ├── verse/
│   ├── reflection/
│   ├── journey/
│   ├── guidance/
│   ├── understanding/
│   ├── saar/
│   ├── search/
│   └── settings/
├── design-system/
│   ├── tokens/
│   ├── foundations/
│   ├── primitives/
│   ├── components/
│   └── compositions/
├── services/
│   ├── api/
│   ├── generated/
│   └── configuration/
├── shared/
│   ├── errors/
│   ├── platform/
│   ├── formatting/
│   └── accessibility/
├── storage/
│   ├── secure/
│   ├── drafts/
│   ├── cache/
│   └── migrations/
└── test/
    ├── factories/
    ├── fixtures/
    ├── mocks/
    └── renderWithProviders.tsx
```

Do not generate empty implementation files for every directory immediately.

Create structure as each vertical slice begins.

---

# 128. Architecture Enforcement Example

Conceptual ArchUnit rules:

```java
@AnalyzeClasses(packages = "com.antar")
class ModuleDependencyTest {

    @ArchTest
    static final ArchRule domainsDoNotDependOnInfrastructure =
        noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAPackage("..infrastructure..");

    @ArchTest
    static final ArchRule controllersDoNotAccessRepositories =
        noClasses()
            .that().resideInAPackage("..api..")
            .should().dependOnClassesThat()
            .haveSimpleNameEndingWith("Repository");

    @ArchTest
    static final ArchRule modulesDoNotAccessOtherModuleInfrastructure =
        // Implement through module-specific package rules.
}
```

The exact implementation should remain readable and maintainable.

---

# 129. Decisions

The V1 repository adopts these decisions:

- One repository contains design, documentation, backend, mobile, and infrastructure.
- Antar V1 is mobile-first.
- The mobile client uses React Native, TypeScript, and Expo.
- A Next.js or other web client is deferred.
- Backend begins as one Spring Boot deployable.
- Backend production code is organized by business domain.
- Each backend module contains its own API, application, domain, and infrastructure layers.
- Backend modules publish explicit interfaces.
- Cross-module infrastructure access is forbidden.
- Domain logic remains independent of frameworks where practical.
- JPA entities stay inside infrastructure.
- API DTOs remain separate from persistence and domain objects.
- Database migrations use one globally ordered Flyway sequence.
- Journey may begin as a derived query module.
- Search projections remain rebuildable.
- Saar provider integrations remain isolated.
- Shared backend code remains intentionally small.
- Architecture rules are enforced through automated tests.
- Mobile code is organized by approved product experience.
- Mobile feature code owns its screens, state, API integration, storage behavior, and tests.
- Authentication secrets use secure device storage.
- Reflection drafts may use explicit local persistence with clear synchronization states.
- The mobile application does not contain privileged backend secrets.
- Full offline synchronization is deferred.
- Kubernetes, microservices, a web client, and a complex Maven build remain deferred.

---

# 130. Open Decisions

The following remain unresolved:

- final Expo routing approach,
- final mobile navigation library,
- final server-state library,
- final local-storage libraries,
- final authentication provider,
- whether Spring Modulith is adopted,
- Maven single-module versus a later multi-module build,
- final infrastructure-as-code tool,
- exact OpenAPI generation strategy,
- content-storage location,
- whether prompt templates live in resources or a prompt registry,
- whether Reflection revisions are implemented in V1,
- whether Bookmarks are included,
- local Reflection draft encryption behavior,
- initial offline Scripture caching scope,
- end-to-end mobile testing tools,
- and the exact CI and mobile-release configuration.

These decisions can be resolved during repository initialization and the first implementation slices.

---

# 131. North Star

Antar’s repository succeeds when the codebase teaches the architecture.

A new developer should be able to determine:

- which domain owns a concept,
- where business logic belongs,
- which dependencies are permitted,
- where private data crosses boundaries,
- how the mobile experience maps to the product architecture,
- and how a module could evolve independently.

The repository should resist becoming:

```text
A collection of controllers,
services,
repositories,
screens,
hooks,
and utilities
with unclear ownership.
```

Its structure should preserve the same clarity found in the product:

```text
Read
Reflect
Study
Discuss
```

Clear responsibility in the Reader experience should be matched by clear responsibility in both backend and mobile code.