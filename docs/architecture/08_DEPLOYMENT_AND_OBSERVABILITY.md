# Antar Deployment and Observability Architecture

**Version:** 1.0  
**Status:** Draft for Architecture Review  
**Owner:** Engineering  
**Last Updated:** August 2026

---

# 1. Purpose

This document defines how Antar is built, deployed, operated, monitored, recovered, and scaled.

It covers:

- runtime topology,
- environment strategy,
- application deployment,
- background processing,
- PostgreSQL,
- Redis,
- object storage,
- AI-provider connectivity,
- release pipelines,
- configuration and secrets,
- observability,
- service-level objectives,
- alerting,
- backups,
- disaster recovery,
- scaling,
- and cost controls.

The initial architecture favors operational simplicity.

Antar begins as a modular monolith and should not introduce distributed infrastructure before measured requirements justify it.

---

# 2. Operational Principles

## 2.1 One Deployable Application First

Antar V1 should begin with one primary backend deployable.

The application contains clearly separated modules:

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

These are domain modules, not independently deployed services.

This reduces:

- deployment coordination,
- distributed tracing complexity,
- network failure modes,
- duplicated infrastructure,
- and operational overhead.

---

## 2.2 Stateless Application Instances

Backend instances should not store durable state in local memory.

Durable state belongs in:

- PostgreSQL,
- approved object storage,
- or another explicitly owned persistent system.

Redis may store temporary state but is not the durable source of truth.

Stateless application instances allow:

- horizontal scaling,
- rolling deployments,
- rapid replacement,
- and simpler failure recovery.

---

## 2.3 Core Reading Must Survive AI Failure

Failures in Saar or an external AI provider must not prevent Readers from accessing:

- Home,
- Library,
- Chapters,
- Verses,
- Reflections,
- Journey,
- Search where non-AI,
- and published Understanding.

AI is isolated operationally even while it lives inside the initial application.

---

## 2.4 Observe User Journeys, Not Just Servers

Observability must explain whether Readers can successfully:

```text
Open Home
Browse Scripture
Read a Verse
Save a Reflection
Load Journey
View Understanding
Ask Saar
Receive a Grounded Response
```

CPU and memory alone do not demonstrate product health.

---

## 2.5 Automate Recovery Where Safe

The system should automatically recover from routine failures such as:

- application-instance termination,
- temporary provider unavailability,
- transient network errors,
- and failed background jobs.

Automation must remain bounded.

Do not create infinite retries or hidden failure loops.

---

## 2.6 Infrastructure Should Be Reproducible

Environment configuration should be defined through:

- infrastructure as code,
- version-controlled deployment configuration,
- repeatable database migrations,
- and automated release pipelines.

Production should not depend on undocumented manual setup.

---

# 3. Initial Runtime Topology

```text
                              ┌─────────────────────┐
                              │       Reader        │
                              └──────────┬──────────┘
                                         │ HTTPS
                                         ▼
                              ┌─────────────────────┐
                              │ CDN / Edge / WAF    │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   Load Balancer     │
                              └──────────┬──────────┘
                                         │
                      ┌──────────────────┴──────────────────┐
                      │                                     │
                      ▼                                     ▼
          ┌──────────────────────┐             ┌──────────────────────┐
          │ Antar Backend        │             │ Antar Backend        │
          │ Instance A           │             │ Instance B           │
          └──────────┬───────────┘             └──────────┬───────────┘
                     │                                     │
                     └──────────────────┬──────────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           │                            │                            │
           ▼                            ▼                            ▼
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│ PostgreSQL          │     │ Redis               │     │ Object Storage      │
│ + pgvector          │     │ Temporary State     │     │ Exports / Assets    │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
           │
           ▼
┌─────────────────────┐
│ Backup Storage      │
└─────────────────────┘

External dependencies:

┌─────────────────────┐
│ Authentication      │
│ Provider            │
└─────────────────────┘

┌─────────────────────┐
│ AI Provider         │
└─────────────────────┘

┌─────────────────────┐
│ Telemetry Backend   │
└─────────────────────┘
```

---

# 4. Deployment Model

The initial backend should be deployed as a containerized application.

Recommended artifact:

```text
antar-backend:<version>
```

The image should contain:

- compiled application,
- required runtime,
- health-check support,
- OpenTelemetry instrumentation,
- and no environment-specific secrets.

Environment-specific configuration is supplied at runtime.

---

# 5. Container Requirements

The production container should:

- use a minimal trusted base image,
- run as a non-root user,
- expose only the application port,
- contain no development tools,
- use a read-only filesystem where practical,
- write temporary data only to approved ephemeral paths,
- include health endpoints,
- and support graceful shutdown.

The image should not contain:

- secrets,
- local configuration files with credentials,
- database dumps,
- production content,
- or debugging certificates.

---

# 6. Application Process Model

The initial deployable may contain:

```text
HTTP API
Application Services
Domain Modules
Scheduled Maintenance
Background Job Consumers
```

However, long-running background work should eventually be separable from request-serving instances.

A practical V1 deployment may use two process roles from the same image:

```text
API Role
Worker Role
```

Example:

```text
ANTAR_PROCESS_ROLE=api
ANTAR_PROCESS_ROLE=worker
```

This preserves one codebase and image while allowing independent scaling.

---

# 7. API Role

The API process owns:

- HTTP requests,
- authentication entry points,
- synchronous domain workflows,
- Scripture reads,
- Reflection mutations,
- Journey queries,
- Understanding reads,
- Saar request acceptance,
- and generation-status queries.

The API process should not perform long AI generation inside the original HTTP transaction.

---

# 8. Worker Role

The Worker process may own:

- Saar retrieval and generation,
- embedding generation,
- search projection rebuilds,
- content indexing,
- export generation,
- retention cleanup,
- and selected asynchronous events.

Workers should use durable work records rather than relying only on in-memory queues.

---

# 9. Initial Background-Job Strategy

Kafka is not required for V1.

Recommended progression:

## Stage 1

Use PostgreSQL-backed durable jobs or explicit status tables.

Examples:

```text
saar.generation_runs
search.indexing_jobs
platform.export_jobs
```

Workers claim pending records using safe locking.

## Stage 2

Introduce a dedicated job queue when:

- throughput increases,
- scheduling becomes complex,
- visibility timeouts are needed,
- or database polling creates measurable contention.

## Stage 3

Introduce event streaming only if the system develops genuine streaming or cross-service requirements.

---

# 10. Job Claiming

A PostgreSQL-backed worker may claim work using patterns such as:

```text
SELECT ... FOR UPDATE SKIP LOCKED
```

The worker should:

1. Claim a bounded number of records.
2. Mark them running.
3. Commit the claim.
4. Perform external work outside the claim transaction.
5. Persist success or failure.
6. Retry only according to policy.

This prevents multiple workers from processing the same job simultaneously.

---

# 11. Job Lifecycle

Common states:

```text
PENDING
RUNNING
COMPLETED
FAILED
CANCELLED
DEAD_LETTERED
```

Recommended fields:

```text
attempt_count
next_attempt_at
locked_by
locked_at
started_at
completed_at
failure_code
```

A job should have a configured maximum attempt count.

After repeated failure, it should enter a terminal reviewable state.

---

# 12. Environment Strategy

Antar should maintain separate environments:

```text
LOCAL
TEST
STAGING
PRODUCTION
```

Optional:

```text
PREVIEW
```

for short-lived frontend or branch deployments.

Each environment must use isolated:

- databases,
- Redis instances or namespaces,
- object-storage buckets,
- secrets,
- authentication configuration,
- and AI credentials.

---

# 13. Local Environment

Local development should be reproducible through container orchestration or a documented equivalent.

Recommended dependencies:

```text
PostgreSQL
pgvector
Redis
Optional local object storage
Optional mock AI provider
```

A developer should be able to start the environment with one primary command.

Example:

```text
docker compose up
```

The application should support an AI mock mode so core development does not require external provider usage.

---

# 14. Test Environment

Automated tests should use isolated resources.

Recommended:

- PostgreSQL through Testcontainers,
- Redis through Testcontainers where needed,
- mock or recorded provider adapters,
- temporary object storage,
- and deterministic test data.

Tests must not depend on shared developer databases.

---

# 15. Staging Environment

Staging should resemble production in architecture while allowing smaller capacity.

Staging should support:

- end-to-end testing,
- migration validation,
- AI integration verification,
- observability verification,
- content publication testing,
- and release-candidate review.

Staging must not contain copied production Reflections or Conversations.

Use synthetic private content.

---

# 16. Production Environment

Production requires:

- private database networking,
- private Redis networking,
- controlled outbound provider access,
- encrypted storage,
- automated backups,
- multi-instance backend deployment where required,
- health-based routing,
- centralized telemetry,
- and audited administrative access.

---

# 17. Infrastructure as Code

Infrastructure should be provisioned through a declarative tool.

The exact tool remains open.

Infrastructure definitions should cover:

- networking,
- load balancing,
- application runtime,
- PostgreSQL,
- Redis,
- object storage,
- secret management,
- telemetry,
- alerts,
- and access policies.

Changes should be reviewed through source control.

---

# 18. Configuration

Configuration should follow precedence such as:

```text
Application Defaults
    ↓
Environment Configuration
    ↓
Runtime Environment Variables
    ↓
Secret References
```

Configuration should be typed and validated at startup.

The application should fail startup when required configuration is absent or invalid.

---

# 19. Secrets

Secrets include:

- database credentials,
- Redis credentials,
- AI-provider keys,
- authentication-provider secrets,
- signing keys,
- object-storage credentials,
- and telemetry credentials.

Secrets must come from an approved secret manager.

They must not be committed to source control or built into images.

---

# 20. Feature Flags

Feature flags support controlled rollout and emergency disablement.

Recommended flags:

```text
saar.enabled
saar.vectorRetrieval.enabled
saar.reflectionContext.enabled
saar.streaming.enabled
search.semantic.enabled
exports.enabled
understanding.enabled
```

Flags should have:

- an owner,
- a purpose,
- default behavior,
- expiration or review date,
- and auditability for critical changes.

Feature flags must not replace permanent authorization rules.

---

# 21. Deployment Pipeline

Recommended release flow:

```text
Pull Request
    ↓
Static Checks
    ↓
Unit Tests
    ↓
Integration Tests
    ↓
Security Scans
    ↓
Build Artifact
    ↓
Container Image
    ↓
Image Scan
    ↓
Publish Artifact
    ↓
Deploy to Staging
    ↓
Smoke Tests
    ↓
Approval
    ↓
Deploy to Production
    ↓
Post-Deployment Verification
```

---

# 22. Source-Control Checks

Pull requests should require:

- code review,
- formatting,
- compilation,
- unit tests,
- architecture or module-boundary checks,
- dependency scanning,
- secret scanning,
- and migration validation where applicable.

---

# 23. Artifact Versioning

Every deployment should identify:

```text
applicationVersion
gitCommit
buildTimestamp
databaseMigrationVersion
promptVersion
pipelineVersion
retrievalPolicyVersion
```

The running version should be available through a protected operational endpoint or telemetry metadata.

---

# 24. Database Migrations

Use Flyway or another approved migration tool.

Migration sequence:

```text
Acquire Migration Lock
    ↓
Validate Existing Schema
    ↓
Apply Pending Migrations
    ↓
Record Migration Result
    ↓
Start or Promote Application
```

The production application should use schema validation rather than automatic Hibernate schema updates.

---

# 25. Migration Compatibility

Deployments should prefer backward-compatible database changes.

Recommended expand-and-contract approach:

```text
1. Add new nullable structure.
2. Deploy code capable of using old and new structures.
3. Backfill data.
4. Switch reads and writes.
5. Verify.
6. Remove obsolete structure in a later release.
```

Avoid coupling a single deployment to an immediately destructive migration.

---

# 26. Deployment Strategy

Recommended initial strategy:

```text
Rolling Deployment
```

Requirements:

- backward-compatible migrations,
- graceful shutdown,
- health checks,
- and stateless instances.

Later, use blue-green or canary deployments when the operational benefit justifies the complexity.

---

# 27. Graceful Shutdown

On shutdown, an instance should:

1. Stop accepting new requests.
2. Mark readiness false.
3. Allow in-flight requests to complete within a bounded period.
4. Stop claiming new jobs.
5. Finish or release claimed work safely.
6. Flush telemetry.
7. Exit.

A terminated worker must not leave jobs permanently stuck.

---

# 28. Health Checks

Expose separate checks for:

## Liveness

Answers:

> Is the application process alive?

Liveness should not fail merely because an external provider is unavailable.

## Readiness

Answers:

> Can this instance safely receive traffic?

Readiness may verify essential dependencies such as:

- application initialization,
- database access,
- required configuration,
- and migration compatibility.

Redis or AI-provider failure should affect readiness only if the process role cannot serve its core responsibility without them.

---

# 29. Dependency Health

Dependency health should be represented separately.

Examples:

```text
postgres = UP
redis = DEGRADED
aiProvider = UNAVAILABLE
vectorRetrieval = DEGRADED
objectStorage = UP
```

Do not make the entire API unavailable because Saar is degraded.

---

# 30. PostgreSQL Deployment

PostgreSQL is the durable source of truth.

Production recommendations:

- managed service where practical,
- encrypted storage,
- automated backups,
- private networking,
- high availability appropriate to product stage,
- monitored connections,
- and point-in-time recovery.

---

# 31. PostgreSQL Availability

Initial production may use:

```text
Primary
+
Synchronous or Managed Standby
```

The exact topology depends on the selected platform and budget.

Failover behavior must be tested.

---

# 32. Connection Pooling

The application should use a bounded database connection pool.

Pool sizing must account for:

```text
Number of Application Instances
+
Worker Instances
+
Migration Processes
+
Administrative Connections
```

Total configured connections must remain below PostgreSQL capacity with operational headroom.

Do not maximize each application pool independently.

---

# 33. Connection-Pool Metrics

Monitor:

```text
active connections
idle connections
pending acquisition requests
acquisition latency
connection timeouts
maximum pool utilization
```

Sustained pending acquisition is an operational warning.

---

# 34. Database Query Observability

Monitor:

- slow queries,
- query latency by operation,
- lock waits,
- deadlocks,
- transaction duration,
- index usage,
- sequential scans,
- table growth,
- vacuum health,
- and replication lag.

Private content must not appear in query logs.

---

# 35. Database Performance Boundaries

The application should avoid:

- unbounded result sets,
- N+1 queries,
- long transactions,
- provider calls inside transactions,
- and synchronous full-corpus rebuilds in request paths.

---

# 36. Read Replicas

Read replicas are deferred until measured load justifies them.

Potential future replica uses:

- Scripture reads,
- Understanding reads,
- search projections,
- and selected operational queries.

Reader-owned data requiring immediate read-after-write consistency should normally use the primary.

---

# 37. Redis Deployment

Redis may support:

- caching,
- rate limiting,
- temporary idempotency data,
- distributed coordination,
- and short-lived operational state.

Redis must not own durable:

- Reflections,
- Reading Progress,
- Conversations,
- or Citations.

---

# 38. Redis Failure Behavior

When Redis is unavailable:

- Scripture reads may fall back to PostgreSQL.
- Idempotency may use durable PostgreSQL where required.
- Rate limiting may use a conservative fallback.
- Private durable state remains intact.
- The system may run in degraded mode.

Redis failure should not corrupt business data.

---

# 39. Cache Policy

Each cache entry should define:

```text
owner
source of truth
key structure
TTL
invalidating event
privacy classification
maximum size
```

Cache keys should include relevant content versions.

Examples:

```text
scripture:verse:{verseId}:translation:{translationId}:v{contentVersion}
understanding:verse:{verseId}:v{contentVersion}
```

---

# 40. Cache Safety

Shared caches must not expose Reader-owned content across users.

Avoid caching private resources globally.

Where private caching is justified, include the authenticated Reader identity in the key and use short TTLs.

---

# 41. Object Storage

Object storage may support:

- Reader exports,
- static approved content assets,
- future audio,
- and large generated artifacts.

Buckets should remain private.

Access should use short-lived signed URLs.

---

# 42. AI Provider Connectivity

AI-provider calls should use:

- explicit connect and response timeouts,
- bounded retries,
- circuit breaking,
- usage accounting,
- request correlation,
- and safe error translation.

Provider health must remain independent from core application health.

---

# 43. Circuit Breaker

A circuit breaker may protect against repeated provider failures.

Conceptual states:

```text
CLOSED
OPEN
HALF_OPEN
```

When open:

- new Saar generation requests fail quickly with a retryable status,
- queued work may be delayed according to policy,
- and curated Understanding remains available.

---

# 44. AI Concurrency Control

The system should bound concurrent provider requests.

Controls may exist:

- globally,
- by application instance,
- by Reader,
- and by provider.

This protects:

- cost,
- provider quotas,
- latency,
- and application stability.

---

# 45. Indexing Workers

Search and embedding workers should be independently scalable from API traffic.

They process:

```text
Knowledge Projection
Chunking
Full-Text Vector Construction
Embedding Generation
Projection Validation
Activation
Retirement
```

Index builds must not block ordinary Scripture reading.

---

# 46. Observability Architecture

Antar should use OpenTelemetry-compatible instrumentation.

Telemetry categories:

```text
Logs
Metrics
Traces
```

All three should share common correlation metadata.

---

# 47. Resource Attributes

Every telemetry signal should identify:

```text
service.name
service.version
deployment.environment
process.role
region
instance.id
```

Avoid high-cardinality or private resource attributes.

---

# 48. Correlation Identifiers

Important identifiers include:

```text
requestId
traceId
conversationId
generationId
retrievalRunId
jobId
```

A Reader-facing request ID should be returned to clients where useful for support.

Private text must not be used as a correlation value.

---

# 49. Structured Logging

Logs should use structured JSON.

Recommended common fields:

```text
timestamp
level
service
environment
requestId
traceId
operation
status
durationMs
errorCode
resourceType
safeResourceId
```

---

# 50. Logging Levels

## ERROR

Unexpected failures requiring attention.

## WARN

Recoverable abnormal conditions.

## INFO

Important lifecycle events.

## DEBUG

Detailed development or controlled diagnostic information.

Production DEBUG logging should be temporary and narrowly scoped.

---

# 51. Logging Privacy

Do not log:

- Reflection content,
- Reader Messages,
- Saar responses,
- full prompts,
- access tokens,
- cookies,
- signed URLs,
- provider credentials,
- or raw search queries where sensitive.

Logging rules should be enforced through tested redaction.

---

# 52. Metrics

Metrics should describe system behavior without exposing private data.

Categories:

```text
Traffic
Errors
Latency
Saturation
Business Flow
AI
Retrieval
Cost
```

---

# 53. HTTP Metrics

Recommended:

```text
http_server_requests_total
http_server_request_duration
http_server_errors_total
http_server_in_flight_requests
```

Dimensions may include:

```text
route
method
status_class
environment
```

Do not label by raw URL containing resource IDs.

---

# 54. Product-Flow Metrics

Recommended:

```text
home_invitation_resolved_total
scripture_chapter_loaded_total
scripture_verse_loaded_total
reading_progress_updated_total
reflection_saved_total
reflection_save_failed_total
journey_loaded_total
understanding_loaded_total
guidance_path_selected_total
```

These should not contain private text.

---

# 55. AI Metrics

Recommended:

```text
saar_generation_started_total
saar_generation_completed_total
saar_generation_failed_total
saar_generation_duration
saar_provider_duration
saar_input_tokens_total
saar_output_tokens_total
saar_estimated_cost_total
saar_grounding_status_total
saar_citation_validation_total
```

---

# 56. Retrieval Metrics

Recommended:

```text
rag_retrieval_duration
rag_candidates_retrieved
rag_sources_selected
rag_empty_retrieval_total
rag_exact_match_total
rag_fulltext_match_total
rag_vector_match_total
rag_required_source_missing_total
```

---

# 57. Worker Metrics

Recommended:

```text
jobs_pending
jobs_running
jobs_completed_total
jobs_failed_total
jobs_dead_lettered_total
job_processing_duration
job_oldest_pending_age
```

The age of the oldest pending job is often more useful than queue depth alone.

---

# 58. Infrastructure Metrics

Monitor:

## Application

```text
CPU
Memory
Garbage Collection
Thread Pools
Heap
Process Restarts
```

## PostgreSQL

```text
Connections
Query Latency
Disk Usage
Replication Lag
Lock Waits
Deadlocks
Transaction Rate
```

## Redis

```text
Memory
Evictions
Hit Rate
Connections
Command Latency
```

## Storage

```text
Capacity
Request Errors
Signed URL Failures
```

---

# 59. Distributed Tracing

Traces should cover significant request paths.

Example Reflection save:

```text
HTTP Request
    ↓
Authorization
    ↓
Reflection Application Service
    ↓
Repository
    ↓
PostgreSQL
```

Example Saar generation:

```text
Message Accepted
    ↓
Context Load
    ↓
Retrieval
    ↓
Reranking
    ↓
Prompt Build
    ↓
Provider Call
    ↓
Citation Validation
    ↓
Persistence
```

---

# 60. Trace Privacy

Do not include private content in:

- span names,
- span attributes,
- events,
- or errors.

Record identifiers, counts, status, and safe classifications instead.

---

# 61. Trace Sampling

Recommended approach:

- retain all errors,
- retain latency outliers,
- sample ordinary successful requests,
- and apply higher sampling to new or unstable features.

AI traces may use separate sampling due to cost and sensitivity.

---

# 62. Dashboards

Initial dashboards should include:

## Product Health

- Home invitation success.
- Verse load success.
- Reflection save success.
- Journey load success.
- Understanding availability.

## API Health

- request rate,
- error rate,
- latency percentiles,
- saturation.

## AI Health

- generation success,
- provider latency,
- grounding distribution,
- citation failures,
- token usage,
- cost.

## Data Health

- database connections,
- slow queries,
- storage growth,
- backup status.

## Worker Health

- pending jobs,
- oldest job age,
- failure count,
- retry volume.

---

# 63. Service-Level Indicators

Recommended SLIs:

```text
Availability
Successful Request Rate
Latency
Reflection Durability
Saar Completion Rate
Grounded Saar Response Rate
Job Completion Delay
```

---

# 64. Service-Level Objectives

Initial SLOs should be treated as targets and refined using real traffic.

## Core Reading Availability

```text
99.9% monthly successful availability
```

for:

- Chapter retrieval,
- Verse retrieval,
- Reading Progress,
- Reflection reads,
- and Journey reads.

## Reflection Save Reliability

```text
99.95% successful durable save rate
```

excluding rejected validation and authorization requests.

## Core API Latency

Conceptual target:

```text
95% of ordinary non-AI requests under 500 ms
```

## Saar Generation Completion

Conceptual target:

```text
95% of accepted generation requests complete successfully
```

excluding safety rejection and unsupported requests.

## Saar Latency

Conceptual target:

```text
95% complete within 15 seconds
```

This should be measured and revised.

---

# 65. Grounding Quality Objective

A separate quality objective should track:

```text
Percentage of delivered Saar responses classified GROUNDED
```

A response should not be counted successful merely because the provider returned text.

---

# 66. Error Budgets

Each SLO creates an error budget.

If the system exceeds its budget:

- prioritize reliability work,
- slow risky releases,
- investigate recurring failure modes,
- and avoid adding operational complexity until stability returns.

---

# 67. Alerting Philosophy

Alerts should represent actionable conditions.

Do not alert on every individual failure.

Good alerts answer:

- Is the Reader experience meaningfully impaired?
- Is data at risk?
- Is recovery required?
- Is cost running out of control?
- Is a security boundary failing?

---

# 68. Critical Alerts

Examples:

```text
Core API availability below threshold
Reflection save failure spike
PostgreSQL unavailable
Database storage critically low
Backup failure
Cross-user authorization failure detected
Scripture publication integrity failure
Secret or credential failure
```

---

# 69. High-Priority Alerts

Examples:

```text
Saar provider failure rate elevated
Grounding validation failure spike
Oldest generation job exceeds threshold
Redis unavailable
Database connection pool saturation
Search corpus indexing failed
AI daily cost budget exceeded
```

---

# 70. Warning Alerts

Examples:

```text
Latency degradation
Growing retry volume
Increased partial grounding
Storage growth above forecast
Cache hit rate decline
Worker backlog increasing
```

Warnings should support investigation without unnecessary paging.

---

# 71. Alert Routing

Alerts should route according to ownership.

Examples:

```text
Core Backend
AI and Retrieval
Content Publication
Security
Infrastructure
```

Every alert needs:

- owner,
- severity,
- runbook,
- and escalation path.

---

# 72. Runbooks

Runbooks should exist for at least:

```text
PostgreSQL unavailable
Redis unavailable
AI provider unavailable
Saar queue backlog
Failed database migration
High Reflection save failures
Search index corruption
Grounding validation spike
Expired credentials
Backup restore
Account deletion failure
```

A runbook should contain:

1. Symptoms.
2. Impact.
3. Verification steps.
4. Immediate mitigation.
5. Recovery.
6. Follow-up actions.

---

# 73. Backup Strategy

PostgreSQL backups should include:

- automated snapshots,
- transaction-log or equivalent point-in-time recovery,
- encrypted backup storage,
- retention policy,
- and restore testing.

Backups are not complete until restoration has been verified.

---

# 74. Backup Categories

## PostgreSQL

Durable business state.

## Object Storage

Exports and approved assets.

## Configuration

Infrastructure code, application configuration, and deployment manifests.

## Search Projections

Rebuildable and not necessarily backed up as authoritative data.

## Redis

Generally rebuildable unless a future durable Redis use case is explicitly approved.

---

# 75. Backup Retention

Exact retention remains open.

A conceptual policy may include:

```text
Daily backups for a short operational window
Weekly backups for a longer window
Monthly backups where required
Point-in-time recovery for recent periods
```

Privacy and legal requirements must inform the final policy.

---

# 76. Restore Testing

Restore tests should occur regularly.

They should verify:

- database restoration,
- migration compatibility,
- application startup,
- Scripture integrity,
- Reflection availability,
- Conversation availability,
- and private-data isolation.

Restore testing should use a protected non-production environment.

---

# 77. Recovery Objectives

Initial targets should be explicitly approved.

Conceptual:

```text
Recovery Time Objective: 4 hours
Recovery Point Objective: 15 minutes
```

These are starting points, not commitments until infrastructure and business requirements are confirmed.

---

# 78. Disaster-Recovery Scenarios

Plan for:

- application-region outage,
- PostgreSQL corruption,
- accidental deletion,
- failed deployment,
- credential compromise,
- object-storage loss,
- and AI-provider extended outage.

---

# 79. Application Rollback

A failed application release should support rapid rollback to the prior artifact.

Rollback must consider database compatibility.

Do not roll application code backward if irreversible migrations make the old version unsafe.

---

# 80. Database Recovery

Database recovery options may include:

- managed failover,
- point-in-time restore,
- snapshot restore,
- and corrective forward migration.

The recovery process must preserve auditability.

---

# 81. Search Index Recovery

Search indexes and embeddings are rebuildable.

Recovery:

```text
Restore Canonical Database
    ↓
Rebuild Knowledge Sources
    ↓
Rebuild Chunks
    ↓
Rebuild Full-Text Vectors
    ↓
Regenerate Embeddings
    ↓
Validate Corpus
    ↓
Activate
```

During rebuild, canonical Scripture browsing should remain available.

---

# 82. AI Provider Outage

During an AI-provider outage:

- accept or reject new Saar requests according to queue policy,
- expose a clear retryable state,
- preserve Reader Messages where approved,
- keep Understanding available,
- avoid unlimited queue growth,
- and activate provider fallback only if tested.

---

# 83. Capacity Planning

Capacity planning should consider:

```text
Active Readers
Verse Reads per Second
Reflection Writes per Second
Concurrent Saar Generations
Average Prompt Tokens
Average Output Tokens
Embedding Corpus Size
Database Growth
Conversation Retention
```

---

# 84. Horizontal Scaling

API and worker processes should scale independently.

Potential scaling signals:

## API

- CPU,
- request concurrency,
- latency,
- and connection utilization.

## Workers

- pending jobs,
- oldest pending age,
- provider concurrency,
- and generation latency.

Do not scale workers beyond provider or database capacity.

---

# 85. Database Scaling

Scale PostgreSQL in this order:

1. Query optimization.
2. Correct indexing.
3. Connection-pool tuning.
4. Increased instance capacity.
5. Caching for stable read-heavy content.
6. Read replicas where appropriate.
7. Partitioning only when measured.
8. Service extraction only when necessary.

---

# 86. Cost Categories

Major operating-cost categories:

```text
Application Compute
PostgreSQL
Redis
Object Storage
Data Transfer
Observability
Authentication
AI Generation
Embedding Generation
Backup Storage
```

AI may become the most variable category.

---

# 87. AI Cost Controls

Required controls:

- per-Reader rate limits,
- input token limits,
- output token limits,
- source-count limits,
- bounded conversation history,
- retry limits,
- provider budgets,
- daily cost monitoring,
- and an emergency disable flag.

---

# 88. Cost Metrics

Track:

```text
Cost per Saar Generation
Cost per Active Reader
Input Tokens per Request
Output Tokens per Request
Embedding Cost per Corpus Version
Failed Generation Cost
Retry Cost
Provider Cost by Model
```

Do not label cost metrics by Reader identity.

---

# 89. Cost Alerts

Examples:

```text
Daily AI spend exceeds budget
Cost per generation increases sharply
Retry cost exceeds threshold
Embedding rebuild exceeds estimate
Observability ingestion exceeds budget
Database storage growth exceeds forecast
```

---

# 90. Observability Cost Controls

Telemetry volume should be bounded.

Controls:

- trace sampling,
- log-level management,
- metric-cardinality limits,
- retention tiers,
- and exclusion of oversized content.

More telemetry is not always better.

---

# 91. Release Verification

After every production deployment, verify:

```text
Application version
Health checks
Database migration version
Chapter endpoint
Verse endpoint
Reflection save
Journey load
Understanding load
Saar acceptance
Telemetry delivery
```

Saar provider invocation may use a controlled synthetic test rather than a real Reader account.

---

# 92. Synthetic Monitoring

Synthetic checks may cover:

```text
Load Chapter List
Load Canonical Verse
Resolve Canonical Reference
Save and Delete Synthetic Reflection
Load Published Understanding
Submit Synthetic Saar Question
Validate Citation Presence
```

Synthetic private content must remain isolated from real Reader data.

---

# 93. Operational Access

Production access should be:

- role-based,
- time-bounded where practical,
- audited,
- and limited to approved personnel.

Direct database access should be exceptional.

Routine support should use controlled application tooling.

---

# 94. Production Debugging

Production debugging should rely on:

- request IDs,
- traces,
- safe logs,
- metrics,
- and controlled administrative diagnostics.

Avoid inspecting private Reflection or Conversation content unless:

- strictly necessary,
- authorized,
- audited,
- and consistent with policy.

---

# 95. Data-Quality Monitoring

Monitor invariants such as:

```text
Every Verse belongs to one Chapter
Published Translations retain attribution
Journey Memories resolve to Reflections
Citations resolve to source versions
Published Understanding has review metadata
Active embeddings match active source hashes
```

Data quality is part of operational health.

---

# 96. Content-Publication Monitoring

Alert or block when:

- a published source lacks attribution,
- a content hash changes unexpectedly,
- a search projection is missing,
- an embedding dimension is invalid,
- or a retired source remains retrievable.

---

# 97. V1 Deployment Recommendation

A practical initial topology:

```text
Managed Container Runtime
    ├── 2 API Instances
    └── 1 Worker Instance

Managed PostgreSQL
    ├── pgvector
    ├── automated backups
    └── point-in-time recovery

Managed Redis

Private Object Storage

Managed Secret Store

OpenTelemetry Collector

Managed Logs / Metrics / Traces
```

For an early private beta, capacity may be smaller while preserving the same architecture.

---

# 98. Kubernetes Position

Kubernetes is not required for V1.

It should be considered only when Antar needs:

- greater workload diversity,
- advanced scheduling,
- operational standardization,
- multi-service deployment,
- or team expertise that justifies it.

A managed container platform is likely simpler initially.

---

# 99. Multi-Region Position

Multi-region active-active deployment is deferred.

Initial resilience should prioritize:

- reliable single-region operation,
- database backups,
- tested restoration,
- and documented regional recovery.

Multi-region complexity should be introduced only after availability requirements demand it.

---

# 100. Initial Implementation Sequence

## Phase 1 — Local Runtime

- Containerize backend.
- Add PostgreSQL and pgvector.
- Add Redis.
- Add local AI mock.
- Add health endpoints.
- Add structured logs.

## Phase 2 — Continuous Integration

- Compile.
- Unit tests.
- Testcontainers integration tests.
- Security scans.
- Build container.
- Publish versioned artifact.

## Phase 3 — Staging

- Provision infrastructure.
- Run migrations.
- Deploy API and Worker roles.
- Configure telemetry.
- Add smoke tests.

## Phase 4 — Production Baseline

- Private networking.
- Managed secrets.
- Backups.
- alerts.
- SLO dashboards.
- deployment rollback.
- incident runbooks.

## Phase 5 — Operational Hardening

- load testing,
- restore testing,
- failure injection,
- cost controls,
- and provider-outage testing.

---

# Mobile Application Delivery

The React Native application is built and distributed separately from the backend.

Recommended initial workflow:

```text
Pull Request
    ↓
TypeScript Checks
    ↓
Unit and Component Tests
    ↓
Mobile Build Validation
    ↓
Internal Development Build
    ↓
Staging API Validation
    ↓
Test Distribution
    ↓
App Store / Play Store Release

---

# 101. Decisions

The V1 deployment and observability architecture adopts these decisions:

- Antar begins as one modular-monolith codebase.
- The application is containerized.
- API and Worker roles may use the same image.
- Application instances remain stateless.
- PostgreSQL is the durable source of truth.
- Redis is optional supporting infrastructure.
- Long-running AI work executes asynchronously.
- Kafka is not required.
- Managed infrastructure is preferred where practical.
- Deployment begins with rolling releases.
- Database changes use backward-compatible migrations.
- OpenTelemetry provides unified telemetry.
- Logs exclude private content.
- Product journeys receive first-class monitoring.
- Core reading health is separated from Saar health.
- Backups and restore testing are required.
- Search projections are rebuildable.
- AI cost is explicitly measured and controlled.
- Kubernetes and multi-region deployment are deferred.

---

# 102. Open Decisions

The following remain unresolved:

- cloud provider,
- container runtime,
- infrastructure-as-code tool,
- telemetry backend,
- exact PostgreSQL topology,
- exact Redis provider,
- final backup retention,
- final RTO and RPO,
- production instance sizes,
- autoscaling thresholds,
- deployment approval model,
- staging-data policy,
- job-queue implementation,
- alert-routing platform,
- and initial production budget.

These decisions should be resolved during implementation planning and infrastructure experiments.

---

# 103. North Star

Antar’s deployment architecture succeeds when the system is:

- easy to deploy,
- easy to understand,
- easy to observe,
- safe to recover,
- inexpensive to operate at early scale,
- and capable of growing without premature distribution.

Operational complexity should never become more sophisticated than the product requires.

A Reader should be able to open Scripture, save a Reflection, and return to their Journey even when AI, caching, or nonessential infrastructure is degraded.