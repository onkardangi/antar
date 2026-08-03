# Antar Security and Privacy Architecture

**Version:** 1.0  
**Status:** Draft for Architecture Review  
**Owner:** Engineering  
**Last Updated:** August 2026

---

# 1. Purpose

This document defines the security and privacy architecture for Antar.

It establishes how the system protects:

- Reader identity,
- private Reflections,
- Reading history,
- Journey memories,
- Saar Conversations,
- AI context,
- canonical Scripture,
- curated content,
- administrative workflows,
- credentials,
- and operational infrastructure.

This document defines engineering requirements and security boundaries.

It is not a substitute for:

- legal review,
- a published privacy policy,
- regulatory analysis,
- formal threat modeling,
- penetration testing,
- or an incident-response program.

---

# 2. Security Objectives

Antar should protect five primary properties.

## 2.1 Confidentiality

Private Reader data must be accessible only to:

- the owning Reader,
- explicitly authorized system processes,
- and approved administrators operating under restricted procedures.

---

## 2.2 Integrity

The system must prevent unauthorized modification of:

- Scripture,
- Commentary attribution,
- curated Understanding,
- Reflections,
- Reading Progress,
- Conversations,
- Citations,
- and privacy preferences.

---

## 2.3 Availability

Core reading capabilities should remain usable when optional dependencies fail.

The following should not depend on Saar availability:

- Scripture browsing,
- Chapter reading,
- Verse reading,
- Reflection,
- Journey,
- Library,
- Search where non-AI,
- and published Understanding.

---

## 2.4 Privacy

Antar should collect and process only the Reader data needed to provide approved product capabilities.

Private writing should not become:

- training data,
- analytics content,
- shared retrieval material,
- advertising data,
- or behavioral profiling input

without a separate explicit decision and Reader consent.

---

## 2.5 Provenance

Readers must be able to distinguish:

```text
Scripture
    ↓
Translation
    ↓
Traditional Commentary
    ↓
Curated Understanding
    ↓
Saar Synthesis
```

Generated content must not be presented as canonical Scripture or attributed commentary.

---

# 3. Security Principles

## 3.1 Deny by Default

Access is denied unless explicitly allowed.

This applies to:

- API endpoints,
- administrative features,
- private resources,
- AI context,
- provider integrations,
- data exports,
- and internal service interfaces.

---

## 3.2 Least Privilege

Every identity receives only the permissions required for its role.

Examples:

- Reader APIs cannot publish Scripture.
- Saar cannot update Reflections.
- Search cannot mutate canonical content.
- indexing workers cannot access unrelated Reader data.
- administrators should not automatically access private Reflection content.

---

## 3.3 Reader Ownership Is Server-Derived

Reader ownership must come from the authenticated identity.

Clients must not establish ownership by submitting:

```text
userId
readerId
accountId
```

for normal Reader-owned operations.

---

## 3.4 Private Writing Is Highly Sensitive

Reflections and Saar Messages may contain:

- spiritual concerns,
- emotional disclosures,
- personal relationships,
- health information,
- work issues,
- or other intimate content.

They should be treated as sensitive private data even when no formal regulated category applies.

---

## 3.5 AI Receives Minimum Necessary Context

The AI provider should receive only the context required for one approved request.

Do not send:

- the full Reader profile,
- full Reflection history,
- complete Journey history,
- unrelated Conversations,
- or account metadata

unless a specific future use case requires it and is separately approved.

---

## 3.6 Security Controls Must Not Depend on the Model

The LLM is not a trusted authorization system.

The model cannot decide:

- which Reader owns a Reflection,
- which records it may access,
- whether content is published,
- whether a source is licensed,
- or whether a user is an administrator.

These decisions occur before model invocation.

---

## 3.7 Safe Failure

When authorization, provenance, grounding, or validation is uncertain, the system should fail closed.

A fluent response must never override a failed security check.

---

# 4. Data Classification

Antar uses the following data classes.

## 4.1 Public Canonical Content

Examples:

- published Chapters,
- published Verses,
- approved Sanskrit content,
- public source metadata.

Sensitivity:

```text
PUBLIC
```

---

## 4.2 Licensed or Attributed Content

Examples:

- Translations,
- Commentary passages,
- publication metadata,
- licensed excerpts.

Sensitivity:

```text
CONTROLLED_CONTENT
```

Protection concerns:

- licensing,
- attribution,
- redistribution,
- excerpt limits,
- and source integrity.

---

## 4.3 Private Reader Content

Examples:

- Quick Reflections,
- Deep Reflections,
- Saar Messages,
- Conversation history,
- Journey Memories,
- reading history.

Sensitivity:

```text
PRIVATE_READER_DATA
```

---

## 4.4 Account Data

Examples:

- email,
- external authentication subject,
- display name,
- preferences,
- account status.

Sensitivity:

```text
ACCOUNT_DATA
```

---

## 4.5 Security Data

Examples:

- access tokens,
- refresh tokens,
- provider credentials,
- encryption keys,
- administrative authentication factors,
- webhook secrets.

Sensitivity:

```text
SECRET
```

---

## 4.6 Operational Metadata

Examples:

- request IDs,
- latency,
- model name,
- token counts,
- error codes,
- safe pseudonymous identifiers.

Sensitivity:

```text
INTERNAL_OPERATIONAL
```

Operational metadata must not silently include private message content.

---

# 5. Trust Boundaries

```text
Reader Device
    │
    │ Untrusted Network
    ▼
Edge / Load Balancer
    │
    ▼
Antar Backend
    │
    ├── PostgreSQL
    ├── Redis
    ├── Object Storage
    ├── Authentication Provider
    └── AI Provider
```

Each boundary requires explicit:

- authentication,
- encryption,
- validation,
- timeout,
- error handling,
- and observability.

---

# 6. Threat Actors

The architecture should account for:

- unauthenticated attackers,
- authenticated malicious Readers,
- compromised Reader devices,
- credential-stuffing attackers,
- malicious automated clients,
- compromised third-party providers,
- overprivileged administrators,
- accidental internal misuse,
- prompt-injection attempts,
- content-ingestion attackers,
- and supply-chain compromise.

---

# 7. Primary Assets

Critical assets include:

```text
Reader Accounts
Private Reflections
Reading History
Journey Memories
Saar Conversations
Privacy Preferences
Scripture Integrity
Commentary Attribution
Curated Understanding
Provider Credentials
Encryption Keys
Administrative Access
Audit Records
```

---

# 8. Authentication Architecture

Antar should use a mature identity solution rather than implementing password authentication casually.

Potential approaches:

- external identity provider,
- managed OAuth/OIDC provider,
- or a carefully reviewed internal implementation.

The selected approach must support:

- secure login,
- account recovery,
- token revocation,
- email verification where used,
- multifactor authentication for administrators,
- and secure session lifecycle management.

---

# 9. Token Validation

The backend should validate bearer tokens for:

- signature,
- issuer,
- audience,
- expiration,
- not-before time,
- token type,
- and required claims.

Do not trust unsigned or client-decoded claims.

Token validation should occur before application use cases execute.

---

# 10. Session Security

Where browser sessions are used:

- cookies should be `Secure`,
- cookies should be `HttpOnly`,
- appropriate `SameSite` behavior should be configured,
- session identifiers should rotate after authentication,
- logout should invalidate the session where supported,
- and CSRF protection should be applied to cookie-authenticated mutations.

Where mobile bearer tokens are used:

- tokens should be stored in platform-secure storage,
- token lifetimes should remain bounded,
- refresh-token rotation should be considered,
- and tokens must never appear in logs.

---

# 11. Authorization Model

Initial roles may include:

```text
READER
CONTENT_EDITOR
CONTENT_REVIEWER
ADMINISTRATOR
SYSTEM_WORKER
```

Roles alone are insufficient for private data.

Reader-owned resources also require ownership checks.

Example:

```text
Role = READER
AND
resource.userId = authenticatedReader.id
```

---

# 12. Reader-Owned Resource Authorization

Ownership checks are required for:

- Reflections,
- Reflection revisions,
- Reading Progress,
- Reading Sessions,
- Bookmarks,
- Journey Memories,
- Guidance Sessions,
- Conversations,
- Messages,
- Exports,
- and account deletion.

Authorization should be enforced in application services, not only controllers.

Repository access patterns should make cross-user access difficult by default.

Prefer methods such as:

```text
findReflectionByIdAndUserId(...)
```

rather than:

```text
findById(...)
```

followed by an optional ownership check.

---

# 13. Administrative Authorization

Administrative access should be separate from normal Reader access.

Administrative capabilities may include:

- importing Scripture,
- publishing Translations,
- managing Commentary sources,
- approving Understanding content,
- rebuilding retrieval projections,
- reviewing system health,
- and managing feature flags.

Administrative access should require:

- stronger authentication,
- multifactor authentication,
- role separation,
- restricted network or device controls where appropriate,
- detailed audit logging,
- and short session lifetimes.

Administrators should not receive automatic access to private Reflections or Conversations.

---

# 14. Separation of Duties

Sensitive publication workflows should separate responsibilities where practical.

Example:

```text
Content Editor
    ↓
Creates or edits draft

Content Reviewer
    ↓
Approves content

Publisher or Authorized Workflow
    ↓
Publishes content
```

One compromised account should not be able to silently alter canonical content and publish it without review.

---

# 15. Scripture Integrity

Canonical Scripture content should be:

- versioned,
- publication-controlled,
- immutable to Reader APIs,
- checksummed,
- attributed,
- and changed only through approved workflows.

Corrections should create an auditable content version.

Do not silently edit published Scripture without retaining the prior version and reason.

---

# 16. Curated Content Integrity

Understanding content and Traditional Insights should support:

```text
DRAFT
IN_REVIEW
APPROVED
PUBLISHED
RETIRED
```

Only published content may appear to Readers.

The system should record:

- author or editor,
- reviewer,
- approval time,
- publication version,
- and source references.

---

# 17. Input Validation

All external input must be validated.

Validation should include:

- type,
- length,
- required fields,
- enum values,
- canonical-reference syntax,
- ownership,
- state transitions,
- and content limits.

Do not depend only on frontend validation.

---

# 18. Output Encoding

Clients should safely render Reader-authored and imported content.

Web clients should avoid injecting untrusted HTML.

Markdown or rich-text rendering must use:

- restricted syntax,
- sanitization,
- safe link handling,
- and disallowed script execution.

Saar responses and Commentary imports are untrusted display input even when generated or administratively approved.

---

# 19. Injection Protection

## SQL Injection

Use parameterized queries and ORM bindings.

Never concatenate untrusted input into SQL.

## Command Injection

Do not invoke shell commands with untrusted text.

## Template Injection

Reader content must not be treated as executable template syntax.

## Prompt Injection

Reader Messages and retrieved sources must be treated as untrusted evidence, not system instructions.

---

# 20. Prompt Injection Architecture

The model must not receive authority to:

- query arbitrary data,
- change privacy settings,
- access other Readers,
- alter content,
- call arbitrary URLs,
- or execute tools autonomously in V1.

Prompt construction should separate:

```text
System Rules
Approved Sources
Private Reader Context
Conversation Text
Current Question
```

Retrieved text must be clearly delimited.

The prompt should state that source content cannot override system rules.

---

# 21. AI Context Authorization

Before including private Reflection context, the backend must verify:

```text
Authenticated Reader owns the Reflection
AND
Conversation belongs to the same Reader
AND
Privacy preference permits context use
AND
Request explicitly enables or requires context
AND
Reflection scope is relevant
```

The model must never receive arbitrary Reflection identifiers from the client without server verification.

---

# 22. Reflection Privacy

Reflections should not be:

- publicly searchable,
- included in shared embeddings,
- logged in full,
- used in product analytics,
- accessed by another Reader,
- or included in Saar context without approval.

Reflection content should be excluded from application error messages.

---

# 23. Conversation Privacy

Saar Conversations should be private by default.

The system should define:

- retention period,
- deletion behavior,
- export behavior,
- provider retention behavior,
- and whether Conversation history is used across sessions.

Conversation history should not automatically become permanent memory.

---

# 24. Provider Privacy Requirements

Before selecting an AI provider, document:

- training use of submitted data,
- prompt retention,
- response retention,
- regional processing,
- encryption,
- subprocessors,
- deletion support,
- incident notification,
- and enterprise privacy controls.

Provider configuration should disable training or optional retention where available and appropriate.

---

# 25. Data Minimization

Store only what is required.

Examples:

- avoid storing raw provider request payloads,
- avoid duplicating Reader Messages across diagnostic tables,
- avoid storing full source content in audit events,
- avoid storing search history by default,
- avoid retaining failed generation content unnecessarily,
- and avoid collecting precise behavioral data without product need.

---

# 26. Encryption in Transit

All network communication should use TLS.

This includes:

- client-to-backend,
- backend-to-database,
- backend-to-Redis,
- backend-to-object storage,
- backend-to-auth provider,
- and backend-to-AI provider.

Plaintext external communication is not allowed.

---

# 27. Encryption at Rest

Use storage encryption for:

- PostgreSQL,
- Redis where durable or provider-supported,
- object storage,
- backups,
- and logs.

Highly sensitive fields may require application-level encryption if the threat model justifies it.

Application-level encryption should not be added casually because it affects:

- search,
- indexing,
- key rotation,
- recovery,
- and operational debugging.

---

# 28. Key Management

Secrets and encryption keys must not be stored in source control.

Use a managed secret-storage or key-management system.

Required capabilities:

- access controls,
- rotation,
- auditability,
- environment separation,
- and emergency revocation.

Secrets should be injected at runtime.

---

# 29. Secret Rotation

Define rotation procedures for:

- database credentials,
- Redis credentials,
- AI provider keys,
- authentication provider secrets,
- object-storage credentials,
- signing keys,
- and webhook secrets.

Rotation should not require long service downtime.

---

# 30. Environment Isolation

Use separate environments for:

```text
LOCAL
TEST
STAGING
PRODUCTION
```

Production data must not be copied casually into lower environments.

Tests and demos should use:

- synthetic Reader accounts,
- synthetic Reflections,
- and approved public content.

---

# 31. Database Security

Database access should follow least privilege.

Potential roles:

```text
antar_application
antar_migration
antar_readonly_operations
antar_backup
```

The application account should not own unrestricted administrative privileges.

Migration credentials should be separate where practical.

---

# 32. Schema Ownership

Domain schemas support logical separation.

Examples:

```text
identity
scripture
reading
reflection
guidance
understanding
saar
search
platform
```

Database privileges may reinforce module boundaries, though the modular monolith may initially use one application account.

Application architecture remains the primary boundary.

---

# 33. Redis Security

Redis should:

- require authentication where supported,
- use encryption in transit,
- remain inaccessible from the public internet,
- use bounded TTLs,
- avoid durable ownership of private data,
- and avoid storing unnecessary Reflection or Conversation content.

Redis keys should not contain raw email addresses, Reader Messages, or Reflection text.

---

# 34. Object Storage Security

Object storage should use:

- private buckets,
- encryption,
- short-lived signed URLs,
- restricted service identities,
- file-type validation,
- and lifecycle policies.

Exports should not be public.

Signed URLs should expire quickly.

---

# 35. File and Content Upload Security

If administrative uploads are introduced:

- validate file type,
- validate size,
- inspect content,
- reject executable formats where unnecessary,
- normalize filenames,
- avoid trusting supplied MIME type,
- and process files outside privileged application paths.

User uploads are outside initial V1 unless explicitly approved.

---

# 36. API Security

All APIs should include:

- authentication where required,
- authorization,
- request-size limits,
- validation,
- rate limiting,
- safe error responses,
- correlation IDs,
- and timeout handling.

Avoid exposing:

- stack traces,
- SQL errors,
- provider payloads,
- internal hostnames,
- or secrets.

---

# 37. Rate Limiting

Rate limits should protect:

- authentication,
- Reflection autosave abuse,
- Search,
- Saar Messages,
- export generation,
- and administrative endpoints.

Rate limits may be scoped by:

- Reader,
- IP address,
- client application,
- endpoint,
- and account tier.

Rate limiting should not block ordinary reading unnecessarily.

---

# 38. Abuse Prevention

Potential abuse cases include:

- automated Saar cost exhaustion,
- credential stuffing,
- Reflection spam,
- Search scraping,
- copyrighted-source extraction,
- prompt-injection attempts,
- and administrative brute force.

Controls may include:

- rate limits,
- anomaly detection,
- account cooldown,
- provider budget limits,
- output limits,
- and manual review.

---

# 39. Denial-of-Service Resilience

Protect against:

- oversized request bodies,
- very long Messages,
- excessive conversation history,
- expensive Search queries,
- large export requests,
- repeated generation retries,
- and unbounded pagination.

Every endpoint should define:

- maximum payload,
- timeout,
- maximum page size,
- and operation budget.

---

# 40. AI Cost Abuse

Saar requires explicit cost controls.

Controls may include:

```text
Per-Reader Request Limit
Per-Conversation Message Limit
Maximum Input Tokens
Maximum Output Tokens
Daily Budget Limit
Provider Quota Alert
Global Kill Switch
Retry Limit
```

Cost failure should affect Saar only, not core reading.

---

# 41. Citation Security

Citation identifiers must be resolved server-side.

The client must not be able to:

- attach arbitrary Citations,
- claim unsupported Commentary,
- or convert Saar synthesis into Scripture references.

Every Citation should point to a source actually included in the generation context.

---

# 42. Licensing Enforcement

The security model must enforce content-license restrictions.

Potential restrictions include:

- internal retrieval allowed,
- public excerpt limited,
- full-text display forbidden,
- attribution required,
- commercial use restricted,
- or redistribution prohibited.

Licensing metadata should influence:

- indexing,
- prompt inclusion,
- output excerpt length,
- and citation presentation.

---

# 43. Logging Policy

Never log full content for:

- Reflections,
- Reader Messages,
- Saar responses,
- Guidance free text,
- access tokens,
- exports,
- or private AI prompts.

Safe fields may include:

```text
requestId
readerPseudonymousId
resourceType
resourceId
statusCode
errorCode
latency
provider
model
tokenCounts
groundingStatus
```

---

# 44. Log Redaction

Central logging should redact:

- bearer tokens,
- cookies,
- email addresses where unnecessary,
- provider keys,
- signed URLs,
- Reflection content,
- Message content,
- and sensitive query parameters.

Redaction should be tested.

---

# 45. Pseudonymous Identifiers

Observability systems may use a stable or rotating pseudonymous Reader identifier.

Do not use:

- raw email,
- display name,
- or external authentication subject

as a metric label or ordinary log value.

The mapping should be inaccessible to most operators.

---

# 46. Metrics Privacy

Metrics labels must remain low-cardinality and non-personal.

Never label metrics with:

- Reader ID,
- Conversation ID,
- Reflection ID,
- Verse query text,
- Message content,
- or email.

Detailed debugging belongs in controlled traces or durable records with access restrictions.

---

# 47. Trace Privacy

Distributed traces should include operational metadata, not content.

Avoid placing:

- prompt text,
- Reader Message,
- full source excerpts,
- model output,
- or Reflection content

inside trace attributes.

---

# 48. Error Privacy

Errors returned to clients should be useful without exposing internal details.

Example:

```json
{
  "code": "RESOURCE_NOT_FOUND",
  "detail": "The requested reflection could not be found."
}
```

Avoid revealing whether another Reader owns the resource.

---

# 49. Audit Logging

Security-sensitive actions should create audit events.

Examples:

```text
ACCOUNT_DELETION_REQUESTED
PRIVACY_PREFERENCE_CHANGED
ADMIN_LOGIN_SUCCEEDED
ADMIN_LOGIN_FAILED
SCRIPTURE_CONTENT_PUBLISHED
UNDERSTANDING_CONTENT_APPROVED
COMMENTARY_SOURCE_ADDED
EXPORT_CREATED
FEATURE_FLAG_CHANGED
PROVIDER_KEY_ROTATED
```

Audit events must not contain full private content.

---

# 50. Audit Log Protection

Audit records should be:

- append-oriented,
- access-controlled,
- tamper-resistant,
- retained according to policy,
- and monitored for suspicious patterns.

Administrative access to audit data should itself be auditable.

---

# 51. Data Retention Categories

Retention should be defined explicitly.

## Account Data

Retained while the account is active and during a limited deletion workflow.

## Reading Progress

Retained until Reader deletion or explicit clearing.

## Reflection

Retained until the Reader deletes it or deletes the account.

## Journey

Derived from Reflection and removed when the source Reflection is deleted.

## Conversation

Retained according to Reader privacy preference and product policy.

## Retrieval Diagnostics

Shorter retention than Reader-visible Conversation content.

## Operational Logs

Limited retention based on security and operational need.

## Audit Logs

Retained according to security and legal requirements without preserving unnecessary private content.

---

# 52. Conversation Retention Options

Potential Reader-facing choices:

```text
SESSION_ONLY
THIRTY_DAYS
UNTIL_DELETED
```

The final set remains a product and privacy decision.

Retention behavior should be understandable and consistently enforced.

---

# 53. Deletion Architecture

Deletion must be:

- authenticated,
- authorized,
- idempotent,
- observable,
- and verifiable.

Deleting a Reflection should remove:

- the Reflection,
- revisions where applicable,
- Journey projections,
- cached previews,
- and future AI-context eligibility.

It should not alter Scripture or Commentary.

---

# 54. Account Deletion

A possible sequence:

```text
Mark Account Deletion Pending
    ↓
Revoke Sessions
    ↓
Delete Saar Conversations
    ↓
Delete Guidance Sessions
    ↓
Delete Reflections
    ↓
Delete Journey Projections
    ↓
Delete Reading Data
    ↓
Delete Preferences
    ↓
Delete or Anonymize Account Record
    ↓
Invalidate Caches and Exports
    ↓
Complete Audit Event
```

The workflow should tolerate retries.

---

# 55. Backup Deletion Limitations

Published privacy documentation should accurately explain backup behavior.

Deleted content may remain in protected backups until backup expiration.

Backups should:

- be encrypted,
- have limited access,
- have defined retention,
- and not be restored selectively into production except through approved recovery procedures.

---

# 56. Data Export

Reader exports should require recent authentication or equivalent verification.

Exports may include:

- profile,
- preferences,
- Reading Progress,
- Bookmarks,
- Reflections,
- Conversation history,
- and Reader-visible Citations.

Exports should exclude:

- system prompts,
- internal safety data,
- provider secrets,
- unrelated operational records,
- and other Readers’ content.

---

# 57. Export Delivery

Exports should be:

- generated asynchronously,
- encrypted at rest,
- available through short-lived signed URLs,
- deleted automatically after expiration,
- and accessible only to the owning Reader.

Export URLs must not be logged in full.

---

# 58. Search Privacy

Raw Search history should not be retained by default.

Operational diagnostics may retain:

- normalized query hash,
- result count,
- latency,
- method,
- and safe error code.

If future product features require Search history, that decision needs separate approval.

---

# 59. Analytics Privacy

Analytics should use event metadata, not private content.

Allowed example:

```text
ReflectionSaved
- reflectionType
- success
- latencyBucket
```

Not allowed:

```text
ReflectionSaved
- content
- emotional sentiment
- spiritual topic inferred from writing
```

---

# 60. No Hidden Profiling

Antar should not create hidden profiles such as:

- spiritual maturity score,
- emotional vulnerability score,
- ideological category,
- religious commitment score,
- or inferred mental-health state.

Any future personalization should use transparent, minimal signals.

---

# 61. Reflection AI Use

AI should not:

- rewrite a Reflection automatically,
- summarize private writing without request,
- infer personality from Reflections,
- use Reflections to train a shared model,
- or share Reflection content between Conversations without approval.

---

# 62. AI Output Safety

Saar should not present itself as:

- a guru,
- a therapist,
- a physician,
- a lawyer,
- a financial advisor,
- or an unquestionable spiritual authority.

Responses should acknowledge limitations and distinguish interpretation from fact.

---

# 63. Sensitive Disclosures

Readers may disclose personal crisis information.

The product must define a safe response policy before launch.

Saar should not attempt to provide unsupported crisis counseling.

When immediate safety concerns are detected, the experience should:

- respond calmly,
- avoid judgment,
- encourage contacting appropriate real-world support,
- and provide localized crisis resources when supported.

Detailed crisis behavior requires separate safety review.

---

# 64. Prompt and Response Retention

The system should avoid storing raw provider payloads by default.

Persist Reader-visible records and required operational metadata.

Possible retained fields:

```text
Reader Message
Final Saar Message
Citations
Provider
Model
Prompt Version
Token Counts
Generation Status
Safe Failure Code
```

Avoid retaining:

- full assembled prompt,
- hidden system instruction,
- temporary private context copies,
- and malformed partial output

unless required for a limited debugging workflow.

---

# 65. Model Training Policy

Antar should not use private Reader content to train or fine-tune models without:

- a separate explicit product decision,
- clear Reader consent,
- privacy review,
- legal review,
- withdrawal mechanisms,
- and strict data governance.

The default assumption is:

```text
Private Reader content is not training data.
```

---

# 66. Third-Party Dependency Security

Third-party services may include:

- authentication provider,
- AI provider,
- email provider,
- cloud infrastructure,
- observability provider,
- and object storage.

Each dependency should be reviewed for:

- data access,
- security controls,
- retention,
- incident history,
- availability,
- regional processing,
- and exit strategy.

---

# 67. Supply-Chain Security

Dependencies should be:

- version-pinned where practical,
- scanned for known vulnerabilities,
- updated regularly,
- sourced from trusted registries,
- and reviewed before major introduction.

Build systems should generate dependency inventories where feasible.

---

# 68. Build and Deployment Security

The deployment pipeline should protect:

- source-control access,
- CI credentials,
- artifact integrity,
- production secrets,
- and deployment permissions.

Production deployments should require controlled authorization.

Build artifacts should not include plaintext secrets.

---

# 69. Container Security

If containers are used:

- use minimal base images,
- avoid running as root,
- remove unnecessary tools,
- scan images,
- pin base versions,
- use read-only filesystems where practical,
- and limit Linux capabilities.

---

# 70. Network Security

Production infrastructure should restrict network access.

Examples:

- databases are not publicly reachable,
- Redis is private,
- administrative interfaces are restricted,
- outbound calls are limited to approved providers,
- and security groups or firewall rules follow least privilege.

---

# 71. SSRF Prevention

Any server-side URL fetching must use an allowlist or controlled connector.

Saar should not browse arbitrary URLs in V1.

Content-ingestion URLs should be validated against:

- allowed protocols,
- permitted hosts,
- redirects,
- private IP ranges,
- and response-size limits.

---

# 72. Webhook Security

Any webhook endpoint must use:

- signature verification,
- timestamp validation,
- replay protection,
- idempotency,
- bounded payload size,
- and safe logging.

Webhook payloads should not be trusted merely because they reach a hidden URL.

---

# 73. Feature-Flag Security

Security-critical flags should include:

```text
saar.enabled
saar.reflectionContext.enabled
saar.streaming.enabled
admin.contentPublishing.enabled
exports.enabled
```

Flag changes should be audited.

Security controls must not be bypassable through ordinary client flags.

---

# 74. Incident Response

Antar should establish an incident-response process covering:

```text
Detection
Triage
Containment
Eradication
Recovery
Reader Communication
Post-Incident Review
```

Incidents may include:

- unauthorized private-data access,
- leaked credentials,
- malicious content publication,
- AI provider exposure,
- data corruption,
- and prolonged service outage.

---

# 75. Security Alerting

Alert on events such as:

- repeated failed administrator logins,
- unusual Saar request volume,
- export abuse,
- repeated authorization failures,
- unexpected cross-user access attempts,
- content publication outside expected workflow,
- provider credential failure,
- and audit pipeline disruption.

---

# 76. Vulnerability Management

The engineering process should include:

- dependency scanning,
- static analysis,
- secret scanning,
- container scanning,
- infrastructure review,
- regular patching,
- and vulnerability triage.

Critical vulnerabilities should have defined response timelines.

---

# 77. Security Testing

## Unit Tests

Verify:

- ownership rules,
- input validation,
- state transitions,
- context-permission logic,
- and redaction functions.

## Integration Tests

Verify:

- authentication,
- authorization,
- cross-user isolation,
- deletion,
- database constraints,
- provider timeout behavior,
- and private cache boundaries.

## Adversarial Tests

Verify:

- prompt injection,
- fabricated citations,
- cross-user identifiers,
- oversized inputs,
- duplicate idempotency keys,
- stale versions,
- malicious markup,
- and unauthorized administrative access.

## Penetration Testing

Perform before broad production launch and after major security-boundary changes.

---

# 78. Cross-User Isolation Tests

The test suite must explicitly verify that Reader A cannot:

- read Reader B’s Reflection,
- update Reader B’s Reflection,
- retrieve Reader B’s Journey,
- open Reader B’s Conversation,
- access Reader B’s export,
- or use Reader B’s Reflection as Saar context.

These should be first-class security tests, not incidental coverage.

---

# 79. Privacy Testing

Tests should verify:

- disabled Reflection context is not sent to the provider,
- deleted Reflections disappear from Journey,
- deleted Conversations are inaccessible,
- retention policies execute,
- logs exclude private content,
- exports contain only Reader-owned data,
- and private data is absent from shared retrieval indexes.

---

# 80. Content Security Testing

Tests should verify:

- only published Scripture is returned,
- retired Commentary is excluded,
- incomplete attribution blocks publication,
- license restrictions affect output,
- and generated content cannot masquerade as Scripture.

---

# 81. Secure Defaults

Recommended defaults:

```text
Reflection AI Context = OFF
Analytics Consent = OFF where required by policy
Conversation Sharing = OFF
Public Reflection Sharing = Unsupported
Search History = Not Retained
AI Provider Training = Disabled
Administrative Access = MFA Required
```

Defaults should favor privacy over convenience.

---

# 82. Threat Model Summary

| Threat | Primary Controls |
|---|---|
| Cross-user private-data access | Authentication, ownership checks, repository scoping, tests |
| Credential theft | Secure token handling, bounded sessions, MFA for admins |
| Prompt injection | Context separation, no autonomous tools, output validation |
| AI hallucination | Retrieval grounding, citations, validation |
| Scripture tampering | Controlled publication, versioning, audit logs |
| Provider data exposure | Data minimization, provider review, retention controls |
| Logging leakage | Redaction, safe structured logs, content exclusions |
| Cost exhaustion | Rate limits, token limits, budgets, kill switch |
| Administrative misuse | Least privilege, separation of duties, auditability |
| Data retention failure | Explicit policies, deletion jobs, verification |
| Copyright misuse | License metadata, excerpt limits, attribution |
| Supply-chain compromise | Scanning, pinned dependencies, controlled builds |

---

# 83. Initial V1 Security Baseline

Before the first production release, Antar should have:

```text
Authenticated Reader sessions
Application-level ownership authorization
TLS everywhere
Encrypted managed storage
Secret management
Private database and Redis networking
Input validation
Output sanitization
Rate limiting
Reflection and Conversation log redaction
AI provider privacy configuration
Prompt-injection defenses
Citation validation
Administrative MFA
Content publication audit logs
Account deletion
Reflection deletion
Conversation deletion
Data export
Dependency scanning
Security integration tests
Incident-response contacts
```

---

# 84. Deferred Security Capabilities

Potential later enhancements:

- field-level encryption for selected content,
- hardware-backed key isolation,
- advanced anomaly detection,
- device management,
- enterprise identity federation,
- dedicated security-event platform,
- content watermarking,
- user-visible session management,
- and regional data residency.

These should be added based on risk and product maturity.

---

# 85. Decisions

The V1 security and privacy architecture adopts these decisions:

- Reader ownership is derived from authentication.
- Application services enforce authorization.
- Reflections and Conversations are treated as sensitive private data.
- Reader content is excluded from shared retrieval indexes.
- Reflection context for Saar is opt-in.
- Private Reader content is not model-training data by default.
- Saar has no autonomous database or tool access in V1.
- Scripture and curated content use controlled publication workflows.
- AI providers receive minimum necessary context.
- Full private content is excluded from logs, metrics, and traces.
- Security-sensitive actions are audited.
- Core reading remains available when Saar fails.
- Account deletion and export are V1 requirements.
- Universal soft deletion is rejected.
- Secure, privacy-preserving defaults are preferred.
- Administrative access requires stronger controls than Reader access.

---

# 86. Open Decisions

The following remain unresolved:

- final authentication provider,
- exact session and token lifetimes,
- whether anonymous reading is supported,
- final Conversation retention choices,
- jurisdiction-specific legal requirements,
- data residency requirements,
- AI provider and contractual controls,
- exact administrative role model,
- whether application-level Reflection encryption is required,
- backup retention period,
- audit retention period,
- crisis-response behavior,
- export format,
- and timing of external penetration testing.

These decisions require product, engineering, privacy, legal, and security review.

---

# 87. North Star

Antar’s security architecture succeeds when Readers can trust that:

- their reflections remain theirs,
- their conversations remain private,
- their data is not quietly repurposed,
- Scripture cannot be silently altered,
- AI receives only approved context,
- sources remain attributable,
- and failures do not expose sensitive information.

Privacy is not a feature layered onto Antar.

It is part of respecting the Reader.