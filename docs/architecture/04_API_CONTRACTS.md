# Antar API Contracts

**Version:** 1.0  
**Status:** Draft for Architecture Review  
**Owner:** Engineering  
**Last Updated:** August 2026

---

# 1. Purpose

This document defines Antar’s external HTTP API surface for Version 1.

It establishes:

- API conventions,
- resource boundaries,
- endpoint responsibilities,
- request and response shapes,
- authentication behavior,
- pagination,
- validation,
- idempotency,
- concurrency control,
- error contracts,
- privacy boundaries,
- and domain-specific API contracts.

This document describes application-level contracts.

It does not define:

- Spring controller implementations,
- persistence entities,
- JPA mappings,
- database migrations,
- provider-specific AI payloads,
- or frontend component interfaces.

API contracts should expose product concepts rather than database structure.

---

# 2. API Design Principles

## 2.1 Domain-Oriented Resources

Endpoints should reflect Antar’s domain language.

Prefer:

```text
/reflections
/reading-progress
/understanding
/conversations
```

Avoid exposing persistence details such as:

```text
/reflection-entries-table
/reading-progress-records
/knowledge-source-rows
```

---

## 2.2 Persistence Entities Are Never API Models

Database entities must not be serialized directly.

Each endpoint should use explicit:

- request DTOs,
- response DTOs,
- command models,
- query models,
- and error models.

This protects clients from persistence changes and prevents accidental exposure of internal fields.

---

## 2.3 One Endpoint, One Application Responsibility

An endpoint should represent one clear use case.

For example:

```text
PUT /reflections/{reflectionId}
```

updates a Reflection.

It should not also:

- update Reading Progress,
- generate Journey content,
- invoke Saar,
- and send analytics events synchronously.

Related internal effects may occur through application workflows or domain events, but the contract should remain focused.

---

## 2.4 Scripture Is Read-Only Through Public APIs

Public Reader APIs may retrieve Scripture but may not mutate it.

Canonical content changes belong to controlled administrative or ingestion workflows outside the Reader API surface.

---

## 2.5 Private Data Requires Explicit Ownership Enforcement

Every Reader-owned resource must be scoped through the authenticated Reader.

A client must never be trusted to establish ownership by submitting a `userId`.

For example:

```text
GET /v1/reflections
```

returns reflections for the authenticated Reader.

Avoid:

```text
GET /v1/users/{userId}/reflections
```

unless the user identifier is needed for an approved administrative contract.

---

## 2.6 AI Contracts Must Preserve Grounding

Saar responses should expose:

- response text,
- citations,
- grounding status,
- source labels,
- and retryable failure information.

Do not return only unstructured generated text.

---

## 2.7 Backward Compatibility

Published API contracts should evolve compatibly within a major version.

Breaking changes require a new major version or a coordinated migration.

Avoid changing:

- field meaning,
- enum meaning,
- endpoint behavior,
- or ownership semantics

without explicit versioning.

---

# 3. Base URL and Versioning

Recommended base path:

```text
/api/v1
```

Example:

```text
GET /api/v1/scripture/chapters
```

Versioning is placed in the URL because it is:

- visible,
- easy to route,
- easy to document,
- and straightforward for mobile clients.

Only major contract versions belong in the URL.

Minor additive changes do not require a new URL version.

---

# 4. Media Types

Default request and response type:

```text
application/json
```

UTF-8 is assumed.

Potential future streaming type for Saar:

```text
text/event-stream
```

File exports may use:

```text
application/zip
application/json
text/markdown
text/html
```

---

# 5. Authentication

Reader-facing protected endpoints require a bearer token.

```http
Authorization: Bearer <access-token>
```

The backend validates:

- signature,
- issuer,
- audience,
- expiration,
- subject,
- and required claims.

The authenticated subject is resolved internally to the Antar Reader identity.

Clients should not send `userId` in normal Reader-owned mutation requests.

---

# 6. Authorization

Authorization is enforced at the application-service boundary.

Examples:

- a Reader may access only their Reflections,
- a Reader may access only their Conversations,
- a Reader may update only their Reading Preferences,
- published Scripture is readable by all authorized application clients,
- draft Understanding content is not visible to ordinary Readers.

Resource existence and authorization errors should avoid leaking another Reader’s resource identifiers.

Where appropriate, return:

```text
404 NOT_FOUND
```

rather than revealing that an inaccessible private resource exists.

---

# 7. Common Headers

## Request Correlation

Clients may send:

```http
X-Request-Id: <client-generated-id>
```

The server may generate one when absent.

The response should return:

```http
X-Request-Id: <resolved-id>
```

---

## Idempotency

Selected mutation endpoints accept:

```http
Idempotency-Key: <unique-key>
```

Recommended for:

- Reflection creation,
- Saar message submission,
- account deletion requests,
- and export requests.

---

## Optimistic Concurrency

Mutable resources may expose:

```http
ETag: "<resource-version>"
```

Updates may require:

```http
If-Match: "<resource-version>"
```

A stale update returns:

```text
412 PRECONDITION_FAILED
```

or:

```text
409 CONFLICT
```

Antar should choose one convention consistently.

Recommended:

```text
412 PRECONDITION_FAILED
```

for ETag mismatch.

---

# 8. Date and Time Format

All timestamps use ISO 8601 with a UTC offset.

Example:

```text
2026-08-03T16:30:00Z
```

Date-only values use:

```text
YYYY-MM-DD
```

Clients should not infer time zones from timestamp strings without offsets.

---

# 9. Identifier Format

Resource identifiers are UUID strings.

Example:

```text
018f45f1-5ef4-7d6b-bc41-a43c72b87d31
```

Canonical Verse references remain human-readable:

```text
2.47
```

Clients should treat identifiers as opaque strings.

---

# 10. Naming Conventions

JSON uses:

```text
camelCase
```

Examples:

```json
{
  "verseId": "018f...",
  "canonicalReference": "2.47",
  "createdAt": "2026-08-03T16:30:00Z"
}
```

Enums use uppercase snake case.

```text
QUICK
DEEP
PUBLISHED
ASK_SAAR
```

Booleans should use explicit names:

```text
showSanskrit
allowReflectionAiContext
```

Avoid ambiguous names such as:

```text
enabled
active
flag
```

without domain context.

---

# 11. Standard Response Envelope

Normal single-resource responses may return the resource directly.

Example:

```json
{
  "id": "018f...",
  "canonicalReference": "2.47"
}
```

Collection responses should use a consistent envelope.

```json
{
  "items": [],
  "page": {
    "nextCursor": null,
    "hasMore": false
  }
}
```

Do not wrap every response in generic fields such as:

```json
{
  "success": true,
  "data": {}
}
```

HTTP status already communicates transport success.

---

# 12. Error Contract

All errors use one structured shape.

```json
{
  "type": "https://antar.app/problems/validation-error",
  "title": "Request validation failed",
  "status": 400,
  "code": "VALIDATION_ERROR",
  "detail": "One or more request fields are invalid.",
  "instance": "/api/v1/reflections",
  "requestId": "req_01J...",
  "errors": [
    {
      "field": "content",
      "code": "CONTENT_TOO_LONG",
      "message": "Reflection content exceeds the allowed length."
    }
  ]
}
```

This follows the general structure of Problem Details while allowing Antar-specific codes.

---

# 13. Error Categories

Common error codes include:

```text
VALIDATION_ERROR
UNAUTHENTICATED
FORBIDDEN
RESOURCE_NOT_FOUND
RESOURCE_CONFLICT
PRECONDITION_FAILED
RATE_LIMIT_EXCEEDED
IDEMPOTENCY_CONFLICT
DEPENDENCY_UNAVAILABLE
AI_PROVIDER_UNAVAILABLE
GROUNDING_FAILED
CONTENT_NOT_PUBLISHED
REQUEST_TIMEOUT
INTERNAL_ERROR
```

Domain-specific codes may include:

```text
INVALID_VERSE_REFERENCE
REFLECTION_ORIGIN_MISMATCH
CONVERSATION_CLOSED
CITATION_VALIDATION_FAILED
GUIDANCE_SESSION_EXPIRED
```

---

# 14. Validation Errors

Field-level validation should identify the invalid field and stable machine-readable code.

Example:

```json
{
  "field": "reflectionType",
  "code": "UNSUPPORTED_REFLECTION_TYPE",
  "message": "reflectionType must be QUICK or DEEP."
}
```

Clients should not parse human-readable messages for business logic.

---

# 15. Pagination

Cursor pagination is recommended for mutable chronological collections.

Used for:

- Reflections,
- Journey Memories,
- Conversations,
- Messages,
- and Search results where appropriate.

Request:

```http
GET /api/v1/reflections?limit=20&cursor=<cursor>
```

Response:

```json
{
  "items": [],
  "page": {
    "nextCursor": "eyJ...",
    "hasMore": true
  }
}
```

The cursor must be opaque.

Default limit:

```text
20
```

Maximum limit:

```text
100
```

Canonical lists with small fixed size, such as 18 Chapters, do not require pagination.

---

# 16. Sorting

Supported sort orders should be explicit and limited.

Example:

```http
GET /api/v1/reflections?sort=createdAt,desc
```

Do not expose arbitrary database column sorting.

Canonical Scripture order must not be overridden by popularity or reading history.

---

# 17. Filtering

Filters should use stable product concepts.

Example:

```http
GET /api/v1/reflections?verseId=<id>&reflectionType=DEEP
```

Avoid generic filtering languages in V1.

---

# 18. Rate Limiting

Rate limits may vary by endpoint category.

Examples:

## Normal Reading APIs

High limits because these are low-cost and essential.

## Reflection Mutations

Moderate write limits to protect abuse without disrupting autosave.

## Search

Moderate query limits.

## Saar

Lower limits based on:

- token cost,
- provider quotas,
- abuse risk,
- and Reader plan.

Rate-limit responses use:

```text
429 TOO_MANY_REQUESTS
```

Recommended headers:

```http
RateLimit-Limit
RateLimit-Remaining
RateLimit-Reset
Retry-After
```

---

# 19. API Resource Overview

```text
/api/v1
├── /me
├── /preferences
├── /scripture
├── /reading
├── /invitations
├── /reflections
├── /journey
├── /guidance
├── /understanding
├── /saar
├── /search
└── /exports
```

---

# 20. Identity APIs

## 20.1 Get Current Reader

```http
GET /api/v1/me
```

Response:

```json
{
  "id": "018f...",
  "email": "reader@example.com",
  "displayName": "Onkar",
  "accountStatus": "ACTIVE",
  "createdAt": "2026-08-03T16:30:00Z"
}
```

Possible responses:

```text
200 OK
401 UNAUTHORIZED
```

---

## 20.2 Update Current Reader

```http
PATCH /api/v1/me
```

Request:

```json
{
  "displayName": "Onkar"
}
```

Response:

```text
200 OK
```

with the updated Reader resource.

Only explicitly mutable profile fields should be accepted.

Unknown or protected fields should be rejected or ignored according to one documented policy.

Recommended: reject unknown fields during early development to catch client mistakes.

---

## 20.3 Delete Account

```http
DELETE /api/v1/me
```

Recommended header:

```http
Idempotency-Key: <key>
```

Possible response:

```text
202 ACCEPTED
```

Response:

```json
{
  "deletionRequestId": "018f...",
  "status": "PENDING",
  "requestedAt": "2026-08-03T16:30:00Z"
}
```

Account deletion may be asynchronous if multiple private datasets require cleanup.

---

# 21. Preference APIs

## 21.1 Get Reading Preferences

```http
GET /api/v1/preferences/reading
```

Response:

```json
{
  "preferredLanguage": "en",
  "translationId": "018f...",
  "showSanskrit": true,
  "showTransliteration": true,
  "textScale": "MEDIUM",
  "theme": "SYSTEM",
  "version": 3
}
```

---

## 21.2 Update Reading Preferences

```http
PUT /api/v1/preferences/reading
```

Request:

```json
{
  "preferredLanguage": "en",
  "translationId": "018f...",
  "showSanskrit": true,
  "showTransliteration": false,
  "textScale": "LARGE",
  "theme": "DARK"
}
```

Recommended:

```http
If-Match: "3"
```

Response:

```text
200 OK
```

with updated preferences and a new ETag.

---

## 21.3 Get Privacy Preferences

```http
GET /api/v1/preferences/privacy
```

Response:

```json
{
  "allowReflectionAiContext": false,
  "conversationRetention": "UNTIL_DELETED",
  "analyticsConsent": false,
  "version": 1
}
```

---

## 21.4 Update Privacy Preferences

```http
PUT /api/v1/preferences/privacy
```

Request:

```json
{
  "allowReflectionAiContext": true,
  "conversationRetention": "THIRTY_DAYS",
  "analyticsConsent": false
}
```

Privacy changes should be auditable without storing private content.

---

# 22. Scripture APIs

## 22.1 List Chapters

```http
GET /api/v1/scripture/chapters
```

Response:

```json
{
  "items": [
    {
      "id": "018f...",
      "chapterNumber": 1,
      "canonicalName": "Arjuna Vishada Yoga",
      "englishName": "The Yoga of Arjuna's Despair",
      "shortIntent": "A battlefield crisis becomes the beginning of inquiry.",
      "verseCount": 47
    }
  ]
}
```

Chapters are returned in canonical order.

No pagination is necessary for 18 chapters.

---

## 22.2 Get Chapter

```http
GET /api/v1/scripture/chapters/{chapterId}
```

Response:

```json
{
  "id": "018f...",
  "chapterNumber": 2,
  "canonicalName": "Sankhya Yoga",
  "englishName": "The Yoga of Knowledge",
  "shortIntent": "Action, wisdom, duty, and steadiness.",
  "verseCount": 72
}
```

---

## 22.3 Get Chapter by Number

```http
GET /api/v1/scripture/chapters/by-number/{chapterNumber}
```

This provides stable canonical lookup without requiring clients to know internal UUIDs.

---

## 22.4 List Chapter Verses

```http
GET /api/v1/scripture/chapters/{chapterId}/verses
```

Optional query parameters:

```text
translationId
language
includeProgress
```

Response:

```json
{
  "items": [
    {
      "id": "018f...",
      "verseNumber": 1,
      "canonicalReference": "2.1",
      "translationPreview": "Sanjaya said...",
      "readingState": "UNREAD"
    }
  ]
}
```

`readingState` may be omitted for anonymous or non-personalized clients.

Canonical ordering is mandatory.

---

## 22.5 Get Verse

```http
GET /api/v1/scripture/verses/{verseId}
```

Query parameters:

```text
translationId
includeTransliteration
```

Response:

```json
{
  "id": "018f...",
  "chapter": {
    "id": "018f...",
    "chapterNumber": 2,
    "canonicalName": "Sankhya Yoga"
  },
  "verseNumber": 47,
  "canonicalReference": "2.47",
  "sanskrit": {
    "content": "..."
  },
  "transliterations": [
    {
      "scheme": "IAST",
      "content": "...",
      "source": {
        "id": "018f...",
        "name": "Approved transliteration source"
      }
    }
  ],
  "translation": {
    "id": "018f...",
    "language": "en",
    "content": "...",
    "source": {
      "id": "018f...",
      "translator": "...",
      "edition": "...",
      "licenseReference": "..."
    }
  },
  "navigation": {
    "previousVerseId": "018f...",
    "nextVerseId": "018f..."
  }
}
```

---

## 22.6 Get Verse by Canonical Reference

```http
GET /api/v1/scripture/verses/by-reference/{reference}
```

Example:

```http
GET /api/v1/scripture/verses/by-reference/2.47
```

Invalid references return:

```text
400 INVALID_VERSE_REFERENCE
```

Missing canonical content returns:

```text
404 RESOURCE_NOT_FOUND
```

---

## 22.7 List Translation Sources

```http
GET /api/v1/scripture/translation-sources
```

Response:

```json
{
  "items": [
    {
      "id": "018f...",
      "name": "Edition Name",
      "translator": "Translator Name",
      "languageCode": "en",
      "publicationYear": 1980,
      "licenseType": "LICENSED"
    }
  ]
}
```

Only approved, published, and licensed sources are returned.

---

# 23. Reading APIs

## 23.1 Get Reading Progress

```http
GET /api/v1/reading/progress
```

Response:

```json
{
  "currentChapterId": "018f...",
  "currentVerseId": "018f...",
  "canonicalReference": "2.47",
  "lastOpenedAt": "2026-08-03T16:30:00Z",
  "lastCompletedVerseId": "018f...",
  "version": 5
}
```

For a new Reader:

```text
204 NO_CONTENT
```

or a default representation may be returned.

Recommended: return `200` with a meaningful empty state.

```json
{
  "currentChapterId": null,
  "currentVerseId": null,
  "canonicalReference": null,
  "lastOpenedAt": null,
  "lastCompletedVerseId": null,
  "version": 0
}
```

---

## 23.2 Update Reading Position

```http
PUT /api/v1/reading/progress
```

Request:

```json
{
  "currentVerseId": "018f...",
  "lastCompletedVerseId": "018f..."
}
```

The server resolves the Chapter through Scripture.

Do not accept contradictory Chapter and Verse identifiers from the client.

Recommended header:

```http
If-Match: "5"
```

---

## 23.3 Open Verse

```http
POST /api/v1/reading/verse-opens
```

Request:

```json
{
  "verseId": "018f...",
  "readingSessionId": "018f..."
}
```

This use case may:

- update last-opened position,
- record a deduplicated visit,
- and return resolved reading context.

Response:

```text
201 CREATED
```

or:

```text
204 NO_CONTENT
```

Prefer returning a small result only if the client needs updated state.

---

## 23.4 Start Reading Session

```http
POST /api/v1/reading/sessions
```

Response:

```text
201 CREATED
```

```json
{
  "id": "018f...",
  "status": "ACTIVE",
  "startedAt": "2026-08-03T16:30:00Z",
  "startingVerseId": "018f..."
}
```

Reading Sessions may be omitted from the public client contract if managed automatically by the backend.

---

## 23.5 Complete Reading Session

```http
POST /api/v1/reading/sessions/{sessionId}/complete
```

Request:

```json
{
  "endingVerseId": "018f..."
}
```

Response:

```text
200 OK
```

---

# 24. Today’s Invitation API

Today’s Invitation is a derived Home response.

## 24.1 Get Today’s Invitation

```http
GET /api/v1/invitations/today
```

Response:

```json
{
  "invitationType": "CONTINUE_READING",
  "contextLabel": "Continue where you left off",
  "destination": {
    "type": "VERSE",
    "id": "018f...",
    "canonicalReference": "2.47"
  },
  "preview": {
    "type": "VERSE_TRANSLATION",
    "content": "..."
  },
  "action": {
    "label": "Continue Reading",
    "type": "OPEN_VERSE"
  }
}
```

Possible `invitationType` values:

```text
BEGIN_JOURNEY
CONTINUE_READING
RESUME_REFLECTION
CURATED_TEACHING
```

The endpoint returns one invitation only.

It does not expose the internal selection algorithm.

---

# 25. Reflection APIs

## 25.1 Create Reflection

```http
POST /api/v1/reflections
```

Recommended header:

```http
Idempotency-Key: <key>
```

Request:

```json
{
  "verseId": "018f...",
  "reflectionType": "QUICK",
  "content": "Detachment does not mean avoiding responsibility.",
  "originReflectionId": null
}
```

Response:

```text
201 CREATED
```

```json
{
  "id": "018f...",
  "verseId": "018f...",
  "canonicalReference": "2.47",
  "reflectionType": "QUICK",
  "content": "Detachment does not mean avoiding responsibility.",
  "entryStatus": "SAVED",
  "originReflectionId": null,
  "createdAt": "2026-08-03T16:30:00Z",
  "updatedAt": "2026-08-03T16:30:00Z",
  "version": 0
}
```

---

## 25.2 List Reflections

```http
GET /api/v1/reflections
```

Supported filters:

```text
verseId
reflectionType
createdFrom
createdTo
limit
cursor
```

Response:

```json
{
  "items": [
    {
      "id": "018f...",
      "verseId": "018f...",
      "canonicalReference": "2.47",
      "reflectionType": "DEEP",
      "preview": "I noticed that...",
      "createdAt": "2026-08-03T16:30:00Z",
      "updatedAt": "2026-08-03T16:35:00Z"
    }
  ],
  "page": {
    "nextCursor": null,
    "hasMore": false
  }
}
```

Collection responses should use previews rather than returning every full Reflection body.

---

## 25.3 Get Reflection

```http
GET /api/v1/reflections/{reflectionId}
```

Response includes full Reader-authored content.

---

## 25.4 Update Reflection

```http
PUT /api/v1/reflections/{reflectionId}
```

Request:

```json
{
  "content": "Updated reflection...",
  "entryStatus": "SAVED"
}
```

Recommended:

```http
If-Match: "3"
```

Response:

```text
200 OK
```

with new version.

---

## 25.5 Delete Reflection

```http
DELETE /api/v1/reflections/{reflectionId}
```

Response:

```text
204 NO_CONTENT
```

Deletion removes or invalidates:

- Journey projections,
- cached previews,
- and AI context references where applicable.

It must not alter Scripture.

---

## 25.6 Expand Quick Reflection

```http
POST /api/v1/reflections/{reflectionId}/expand
```

Creates a Deep Reflection from a Quick Reflection.

Request:

```json
{
  "content": "Expanded reflection content..."
}
```

Response:

```text
201 CREATED
```

The Quick Reflection remains unchanged.

---

## 25.7 Get Reflection Revisions

Only if revision history is included.

```http
GET /api/v1/reflections/{reflectionId}/revisions
```

---

## 25.8 Restore Reflection Revision

```http
POST /api/v1/reflections/{reflectionId}/revisions/{revisionId}/restore
```

This creates a new current revision rather than mutating history.

---

# 26. Reflection Autosave Contract

Autosave may reuse:

```http
PUT /api/v1/reflections/{reflectionId}
```

with:

```http
Idempotency-Key
If-Match
```

The client may display local states such as:

```text
SAVING
SAVED_LOCALLY
SAVED_TO_SERVER
SYNC_FAILED
```

The server response should expose only durable persistence state.

Example:

```json
{
  "id": "018f...",
  "saveStatus": "SAVED_TO_SERVER",
  "updatedAt": "2026-08-03T16:35:00Z",
  "version": 4
}
```

The server must never claim the Reflection is saved when persistence failed.

---

# 27. Journey APIs

## 27.1 List Journey Memories

```http
GET /api/v1/journey/memories
```

Supported parameters:

```text
limit
cursor
year
month
verseId
```

Response:

```json
{
  "groups": [
    {
      "label": "July 2026",
      "year": 2026,
      "month": 7,
      "items": [
        {
          "reflectionId": "018f...",
          "verseId": "018f...",
          "canonicalReference": "2.47",
          "reflectionType": "DEEP",
          "preview": "I noticed that...",
          "createdAt": "2026-07-28T14:00:00Z"
        }
      ]
    }
  ],
  "page": {
    "nextCursor": null,
    "hasMore": false
  }
}
```

Journey Memories are read projections.

They do not have independent mutation endpoints.

---

# 28. Guidance APIs

## 28.1 Start Guidance Session

```http
POST /api/v1/guidance/sessions
```

Request:

```json
{
  "verseId": "018f..."
}
```

Response:

```text
201 CREATED
```

```json
{
  "id": "018f...",
  "verseId": "018f...",
  "status": "ACTIVE",
  "availablePaths": [
    {
      "type": "UNDERSTAND",
      "title": "Understand this Verse",
      "description": "Gain a guided explanation of the verse."
    },
    {
      "type": "CONNECT",
      "title": "Connect with Other Teachings",
      "description": "Explore related verses."
    },
    {
      "type": "TRADITIONAL_COMMENTARY",
      "title": "Learn from Traditional Commentaries",
      "description": "Read established interpretations."
    },
    {
      "type": "ASK_SAAR",
      "title": "Ask Saar",
      "description": "Have a thoughtful conversation."
    }
  ],
  "createdAt": "2026-08-03T16:30:00Z"
}
```

---

## 28.2 Select Guidance Path

```http
POST /api/v1/guidance/sessions/{sessionId}/selections
```

Request:

```json
{
  "path": "UNDERSTAND"
}
```

Response:

```json
{
  "selectionId": "018f...",
  "path": "UNDERSTAND",
  "destination": {
    "type": "UNDERSTANDING",
    "verseId": "018f..."
  },
  "selectedAt": "2026-08-03T16:31:00Z"
}
```

Guidance chooses a path.

It does not return the full Understanding content or Saar response in this operation.

---

## 28.3 Get Guidance Session

```http
GET /api/v1/guidance/sessions/{sessionId}
```

Only the owning Reader may access the session.

---

# 29. Understanding APIs

## 29.1 Get Understanding for Verse

```http
GET /api/v1/understanding/verses/{verseId}
```

Response:

```json
{
  "id": "018f...",
  "verse": {
    "id": "018f...",
    "canonicalReference": "2.47",
    "translationPreview": "..."
  },
  "title": "Understanding Bhagavad Gita 2.47",
  "understanding": "A reviewed explanation...",
  "keyConcepts": [
    {
      "name": "Duty",
      "description": "..."
    },
    {
      "name": "Detachment",
      "description": "..."
    }
  ],
  "traditionalInsights": [
    {
      "summary": "...",
      "source": {
        "id": "018f...",
        "authorName": "...",
        "tradition": "...",
        "title": "..."
      }
    }
  ],
  "relatedVerses": [
    {
      "verseId": "018f...",
      "canonicalReference": "3.19",
      "relationshipType": "REINFORCES",
      "reason": "..."
    }
  ],
  "contentVersion": 2,
  "publishedAt": "2026-08-01T12:00:00Z"
}
```

Only published content is returned.

If no reviewed Understanding exists:

```text
404 CONTENT_NOT_PUBLISHED
```

Do not generate content at request time as an invisible fallback.

---

## 29.2 Get Traditional Commentary for Verse

```http
GET /api/v1/understanding/verses/{verseId}/commentaries
```

Response:

```json
{
  "items": [
    {
      "source": {
        "id": "018f...",
        "authorName": "...",
        "tradition": "...",
        "title": "..."
      },
      "passage": "...",
      "licenseReference": "..."
    }
  ]
}
```

---

## 29.3 Get Related Verses

```http
GET /api/v1/understanding/verses/{verseId}/related-verses
```

Response remains curated and source-aware.

This is not a personalized recommendation endpoint.

---

# 30. Saar Conversation APIs

## 30.1 Start Conversation

```http
POST /api/v1/saar/conversations
```

Recommended header:

```http
Idempotency-Key: <key>
```

Request:

```json
{
  "verseId": "018f...",
  "guidanceSessionId": "018f...",
  "includeReflectionContext": false
}
```

If `includeReflectionContext` is `true`, the backend must also confirm the Reader’s privacy preference permits it.

Response:

```text
201 CREATED
```

```json
{
  "id": "018f...",
  "verseId": "018f...",
  "canonicalReference": "2.47",
  "status": "ACTIVE",
  "startedAt": "2026-08-03T16:30:00Z"
}
```

---

## 30.2 List Conversations

```http
GET /api/v1/saar/conversations
```

Response:

```json
{
  "items": [
    {
      "id": "018f...",
      "canonicalReference": "2.47",
      "status": "ACTIVE",
      "lastMessagePreview": "One way to understand...",
      "lastMessageAt": "2026-08-03T16:40:00Z"
    }
  ],
  "page": {
    "nextCursor": null,
    "hasMore": false
  }
}
```

---

## 30.3 Get Conversation

```http
GET /api/v1/saar/conversations/{conversationId}
```

Response:

```json
{
  "id": "018f...",
  "verse": {
    "id": "018f...",
    "canonicalReference": "2.47"
  },
  "status": "ACTIVE",
  "startedAt": "2026-08-03T16:30:00Z",
  "lastMessageAt": "2026-08-03T16:40:00Z"
}
```

---

## 30.4 List Conversation Messages

```http
GET /api/v1/saar/conversations/{conversationId}/messages
```

Response:

```json
{
  "items": [
    {
      "id": "018f...",
      "role": "READER",
      "content": "What does detachment mean here?",
      "status": "COMPLETED",
      "sequenceNumber": 1,
      "createdAt": "2026-08-03T16:32:00Z"
    },
    {
      "id": "018f...",
      "role": "SAAR",
      "content": "One way to understand...",
      "status": "COMPLETED",
      "sequenceNumber": 2,
      "groundingStatus": "GROUNDED",
      "citations": [
        {
          "id": "018f...",
          "label": "Bhagavad Gita 2.47",
          "sourceType": "VERSE",
          "sourceId": "018f...",
          "validationStatus": "VALID"
        }
      ],
      "createdAt": "2026-08-03T16:32:05Z"
    }
  ],
  "page": {
    "nextCursor": null,
    "hasMore": false
  }
}
```

---

## 30.5 Submit Reader Message

```http
POST /api/v1/saar/conversations/{conversationId}/messages
```

Recommended header:

```http
Idempotency-Key: <key>
```

Request:

```json
{
  "content": "How is detachment different from indifference?"
}
```

Initial asynchronous response:

```text
202 ACCEPTED
```

```json
{
  "readerMessage": {
    "id": "018f...",
    "role": "READER",
    "content": "How is detachment different from indifference?",
    "status": "COMPLETED",
    "sequenceNumber": 3,
    "createdAt": "2026-08-03T16:35:00Z"
  },
  "generation": {
    "id": "018f...",
    "status": "PENDING"
  }
}
```

This avoids holding the HTTP request open for a potentially long provider call.

A synchronous or streaming contract may also be supported later.

---

## 30.6 Get Generation Status

```http
GET /api/v1/saar/generations/{generationId}
```

Pending response:

```json
{
  "id": "018f...",
  "status": "PENDING",
  "startedAt": "2026-08-03T16:35:00Z"
}
```

Completed response:

```json
{
  "id": "018f...",
  "status": "COMPLETED",
  "assistantMessageId": "018f...",
  "completedAt": "2026-08-03T16:35:04Z"
}
```

Failed response:

```json
{
  "id": "018f...",
  "status": "FAILED",
  "failure": {
    "code": "AI_PROVIDER_UNAVAILABLE",
    "retryable": true
  }
}
```

---

## 30.7 Streaming Saar Response

Potential later endpoint:

```http
POST /api/v1/saar/conversations/{conversationId}/messages:stream
```

Response type:

```text
text/event-stream
```

Possible events:

```text
message.accepted
response.delta
citation.available
response.completed
response.failed
```

Streaming is deferred until the non-streaming contract is stable.

The persisted final Message remains authoritative.

---

## 30.8 Retry Failed Generation

```http
POST /api/v1/saar/generations/{generationId}/retry
```

The retry must use controlled semantics.

Do not silently retry indefinitely.

Response:

```text
202 ACCEPTED
```

---

## 30.9 Close Conversation

```http
POST /api/v1/saar/conversations/{conversationId}/close
```

Response:

```json
{
  "id": "018f...",
  "status": "CLOSED",
  "closedAt": "2026-08-03T16:45:00Z"
}
```

A closed Conversation rejects new Reader Messages unless reopened through an explicit use case.

---

## 30.10 Delete Conversation

```http
DELETE /api/v1/saar/conversations/{conversationId}
```

Response:

```text
204 NO_CONTENT
```

Deletion should follow the Reader’s retention settings and privacy policy.

---

# 31. Saar Grounding Contract

Assistant messages should expose a grounding status.

Possible values:

```text
GROUNDED
PARTIALLY_GROUNDED
UNGROUNDED
VALIDATION_FAILED
```

Recommended public behavior:

- `GROUNDED`: display normally with citations.
- `PARTIALLY_GROUNDED`: clearly communicate limited sourcing.
- `UNGROUNDED`: do not present as a normal authoritative response.
- `VALIDATION_FAILED`: return a recoverable failure state.

Example:

```json
{
  "groundingStatus": "PARTIALLY_GROUNDED",
  "groundingNotice": "This response includes interpretation beyond the cited sources."
}
```

The system should not expose internal retrieval scores directly to Readers.

---

# 32. Search APIs

## 32.1 Search Scripture

```http
GET /api/v1/search/scripture?q={query}
```

Supported parameters:

```text
q
type
chapter
language
limit
cursor
```

Possible types:

```text
ALL
CHAPTER
VERSE
COMMENTARY
UNDERSTANDING
```

Response:

```json
{
  "query": "action without attachment",
  "items": [
    {
      "resultType": "VERSE",
      "destination": {
        "type": "VERSE",
        "id": "018f..."
      },
      "canonicalReference": "2.47",
      "title": "Chapter 2 · Verse 47",
      "preview": "...",
      "matchedRanges": [
        {
          "start": 15,
          "end": 21
        }
      ]
    }
  ],
  "page": {
    "nextCursor": null,
    "hasMore": false
  }
}
```

Search must preserve content identity.

A Chapter result should remain recognizably a Chapter.

A Verse result should remain recognizably a Verse.

---

## 32.2 Resolve Canonical Reference

```http
GET /api/v1/search/references/resolve?q=BG%202.47
```

Response:

```json
{
  "resolved": true,
  "canonicalReference": "2.47",
  "verseId": "018f..."
}
```

If no unambiguous reference exists:

```json
{
  "resolved": false
}
```

Reference parsing should occur before semantic search.

---

# 33. Bookmark APIs

Only include if Bookmarks remain in V1.

## 33.1 Create Bookmark

```http
POST /api/v1/bookmarks
```

Request:

```json
{
  "verseId": "018f..."
}
```

Response:

```text
201 CREATED
```

---

## 33.2 List Bookmarks

```http
GET /api/v1/bookmarks
```

---

## 33.3 Delete Bookmark

```http
DELETE /api/v1/bookmarks/{bookmarkId}
```

---

# 34. Export APIs

## 34.1 Request Reader Data Export

```http
POST /api/v1/exports
```

Request:

```json
{
  "format": "ZIP",
  "include": [
    "PROFILE",
    "READING_PROGRESS",
    "REFLECTIONS",
    "CONVERSATIONS"
  ]
}
```

Response:

```text
202 ACCEPTED
```

```json
{
  "id": "018f...",
  "status": "PENDING",
  "requestedAt": "2026-08-03T16:30:00Z"
}
```

---

## 34.2 Get Export Status

```http
GET /api/v1/exports/{exportId}
```

Completed response may include a short-lived signed download URL.

```json
{
  "id": "018f...",
  "status": "COMPLETED",
  "downloadUrl": "<signed-url>",
  "expiresAt": "2026-08-03T17:30:00Z"
}
```

---

# 35. Administrative APIs

Reader-facing contracts should remain separate from content-administration APIs.

Potential base path:

```text
/api/admin/v1
```

Administrative APIs may support:

- importing Scripture,
- publishing translations,
- managing commentary sources,
- reviewing Understanding content,
- rebuilding search projections,
- and regenerating embeddings.

These contracts require separate authorization and should not share ordinary Reader roles.

Detailed administrative APIs are deferred.

---

# 36. Webhook APIs

V1 does not require public webhooks.

Internal provider callbacks may use dedicated protected endpoints if required.

Examples:

- asynchronous AI provider completion,
- authentication provider lifecycle events,
- or export completion.

Every webhook must include:

- signature validation,
- replay protection,
- idempotency,
- timestamp validation,
- and safe logging.

---

# 37. Asynchronous Operation Contract

Long-running operations should use a common status pattern.

Possible statuses:

```text
PENDING
RUNNING
COMPLETED
FAILED
CANCELLED
```

Example resource:

```json
{
  "id": "018f...",
  "status": "RUNNING",
  "createdAt": "2026-08-03T16:30:00Z",
  "startedAt": "2026-08-03T16:30:01Z",
  "completedAt": null,
  "failure": null
}
```

This pattern may be reused for:

- Saar generation,
- exports,
- content ingestion,
- and embedding rebuilds.

---

# 38. Idempotency Behavior

When an endpoint supports `Idempotency-Key`:

1. The key is scoped to the authenticated Reader and operation.
2. The same key and same request return the original result.
3. The same key with a different request returns:

```text
409 IDEMPOTENCY_CONFLICT
```

4. Keys expire according to operation-specific retention.
5. Provider retries must not create duplicate durable messages or Reflections.

---

# 39. Concurrency Conflict Contract

A stale Reflection update may return:

```json
{
  "type": "https://antar.app/problems/precondition-failed",
  "title": "Reflection has changed",
  "status": 412,
  "code": "PRECONDITION_FAILED",
  "detail": "The reflection was updated after the version you edited.",
  "requestId": "req_01J...",
  "currentVersion": 5
}
```

The client may then:

- reload,
- compare,
- preserve the local draft,
- or offer conflict recovery.

The server must not silently overwrite newer private writing.

---

# 40. Privacy Boundaries

API responses must not expose:

- raw provider prompts,
- system instructions,
- private reflections without ownership,
- unapproved AI context,
- internal safety classifications,
- raw retrieval scores,
- provider credentials,
- or private content in operational errors.

Reflection content should enter Saar context only when:

1. the Reader explicitly requests it or the approved product flow requires it,
2. privacy preferences permit it,
3. the Conversation is owned by the same Reader,
4. and the request clearly communicates the context use.

---

# 41. Logging Boundaries

Do not log full request bodies for:

- Reflections,
- Guidance free text,
- Saar Reader Messages,
- Saar responses,
- account exports,
- or privacy updates.

Safe logs may include:

- endpoint,
- status,
- latency,
- request ID,
- Reader pseudonymous identifier,
- resource type,
- result count,
- provider,
- model,
- token counts,
- and safe error code.

---

# 42. Caching Semantics

Public immutable Scripture responses may use HTTP caching.

Example:

```http
Cache-Control: public, max-age=3600
ETag: "<content-version>"
```

Private Reader data should use:

```http
Cache-Control: private, no-store
```

unless a carefully defined client-cache policy exists.

Saar and Reflection responses should default to private and non-shared caching.

---

# 43. Localization

Content responses should expose language metadata.

Example:

```json
{
  "languageCode": "en"
}
```

Potential request header:

```http
Accept-Language: en-US
```

However, the selected translation remains an explicit preference rather than being inferred solely from locale.

API error messages may be localized later.

Stable error codes remain language-independent.

---

# 44. Accessibility Metadata

API contracts should not embed presentation-specific accessibility labels by default.

Clients can derive labels from semantic content.

Exceptions may exist where server-provided copy is editorially controlled and required for consistent meaning.

Avoid coupling backend contracts to one platform’s accessibility API.

---

# 45. Analytics Boundaries

Reader-facing APIs do not return internal engagement analytics.

The backend may emit privacy-safe product events such as:

```text
VerseOpened
ReflectionSaved
GuidancePathSelected
UnderstandingViewed
SaarConversationStarted
```

Raw private content must not be included.

Analytics behavior should not alter API semantics.

---

# 46. API Documentation

Use OpenAPI 3.1 for machine-readable API documentation.

The OpenAPI definition should include:

- schemas,
- examples,
- auth requirements,
- error responses,
- pagination,
- idempotency headers,
- and enum descriptions.

Generated documentation must not replace architecture review.

The OpenAPI contract should be treated as a build artifact or source-controlled contract depending on the implementation approach.

---

# 47. Contract Testing

API contracts should be tested at multiple levels.

## Controller Tests

Verify:

- routing,
- request validation,
- status codes,
- serialization,
- headers,
- and authorization entry points.

## Application Tests

Verify:

- use-case behavior,
- ownership,
- invariants,
- and dependency interactions.

## Integration Tests

Use PostgreSQL Testcontainers and real HTTP boundaries where valuable.

Verify:

- persistence,
- optimistic locking,
- idempotency,
- cross-user isolation,
- and transactional behavior.

## Consumer Contract Tests

May be introduced when multiple independently deployed clients or services require stronger compatibility guarantees.

---

# 48. API Evolution Rules

Within `/api/v1`, additive changes are generally safe:

- adding optional response fields,
- adding new endpoints,
- adding new enum values only when clients are tolerant,
- and adding optional request fields with defaults.

Potentially breaking changes include:

- removing fields,
- changing field meaning,
- changing requiredness,
- changing default behavior,
- changing enum semantics,
- and changing status codes relied upon by clients.

Enums should be treated carefully because older mobile clients may not understand new values.

Clients should implement unknown-enum fallback behavior where practical.

---

# 49. Initial Endpoint Summary

## Identity

```text
GET    /api/v1/me
PATCH  /api/v1/me
DELETE /api/v1/me
```

## Preferences

```text
GET /api/v1/preferences/reading
PUT /api/v1/preferences/reading

GET /api/v1/preferences/privacy
PUT /api/v1/preferences/privacy
```

## Scripture

```text
GET /api/v1/scripture/chapters
GET /api/v1/scripture/chapters/{chapterId}
GET /api/v1/scripture/chapters/by-number/{chapterNumber}
GET /api/v1/scripture/chapters/{chapterId}/verses
GET /api/v1/scripture/verses/{verseId}
GET /api/v1/scripture/verses/by-reference/{reference}
GET /api/v1/scripture/translation-sources
```

## Reading

```text
GET  /api/v1/reading/progress
PUT  /api/v1/reading/progress
POST /api/v1/reading/verse-opens
POST /api/v1/reading/sessions
POST /api/v1/reading/sessions/{sessionId}/complete
```

## Invitation

```text
GET /api/v1/invitations/today
```

## Reflection

```text
POST   /api/v1/reflections
GET    /api/v1/reflections
GET    /api/v1/reflections/{reflectionId}
PUT    /api/v1/reflections/{reflectionId}
DELETE /api/v1/reflections/{reflectionId}
POST   /api/v1/reflections/{reflectionId}/expand
```

## Journey

```text
GET /api/v1/journey/memories
```

## Guidance

```text
POST /api/v1/guidance/sessions
GET  /api/v1/guidance/sessions/{sessionId}
POST /api/v1/guidance/sessions/{sessionId}/selections
```

## Understanding

```text
GET /api/v1/understanding/verses/{verseId}
GET /api/v1/understanding/verses/{verseId}/commentaries
GET /api/v1/understanding/verses/{verseId}/related-verses
```

## Saar

```text
POST   /api/v1/saar/conversations
GET    /api/v1/saar/conversations
GET    /api/v1/saar/conversations/{conversationId}
DELETE /api/v1/saar/conversations/{conversationId}

GET  /api/v1/saar/conversations/{conversationId}/messages
POST /api/v1/saar/conversations/{conversationId}/messages

GET  /api/v1/saar/generations/{generationId}
POST /api/v1/saar/generations/{generationId}/retry
POST /api/v1/saar/conversations/{conversationId}/close
```

## Search

```text
GET /api/v1/search/scripture
GET /api/v1/search/references/resolve
```

## Exports

```text
POST /api/v1/exports
GET  /api/v1/exports/{exportId}
```

---

# 50. V1 Endpoint Prioritization

## Phase A — Scripture Reading

```text
GET /scripture/chapters
GET /scripture/chapters/{chapterId}
GET /scripture/chapters/{chapterId}/verses
GET /scripture/verses/{verseId}
GET /reading/progress
PUT /reading/progress
GET /invitations/today
```

## Phase B — Reflection and Journey

```text
POST /reflections
GET /reflections
GET /reflections/{reflectionId}
PUT /reflections/{reflectionId}
DELETE /reflections/{reflectionId}
POST /reflections/{reflectionId}/expand
GET /journey/memories
```

## Phase C — Understanding and Guidance

```text
POST /guidance/sessions
POST /guidance/sessions/{sessionId}/selections
GET /understanding/verses/{verseId}
GET /understanding/verses/{verseId}/commentaries
GET /understanding/verses/{verseId}/related-verses
```

## Phase D — Saar

```text
POST /saar/conversations
GET /saar/conversations/{conversationId}
POST /saar/conversations/{conversationId}/messages
GET /saar/generations/{generationId}
GET /saar/conversations/{conversationId}/messages
```

## Phase E — Supporting Capabilities

```text
Search
Preferences
Bookmarks
Exports
Administrative content workflows
```

---

# 51. Decisions

The V1 API adopts these decisions:

- REST-style HTTP APIs under `/api/v1`.
- Explicit API DTOs separate from persistence entities.
- Reader ownership is derived from authentication.
- Scripture is read-only through Reader APIs.
- Today’s Invitation is exposed as one derived response.
- Reflection mutations support idempotency and optimistic concurrency.
- Journey exposes derived read projections only.
- Guidance selects paths but does not return generated content.
- Understanding is curated and available without AI.
- Saar message submission is asynchronous by default.
- Saar responses expose citations and grounding status.
- Canonical reference lookup precedes semantic search.
- Private content is excluded from logs and analytics.
- OpenAPI documents the published contract.
- Mobile compatibility constrains breaking evolution.

---

# 52. Open Decisions

The following remain unresolved:

- final authentication provider and token claims,
- whether anonymous Scripture browsing is permitted,
- whether Reading Sessions are explicitly client-managed,
- whether Bookmarks are included in V1,
- whether Reflection revisions are exposed in V1,
- exact Reflection content limits,
- whether Saar uses polling, streaming, or both,
- whether Conversation titles exist,
- exact rate limits,
- exact Conversation retention behavior,
- whether Search includes Commentary in V1,
- export format and delivery mechanism,
- and whether administrative APIs live in the same deployable application.

These decisions should be resolved before implementation of the affected endpoints.

---

# 53. North Star

Antar’s API succeeds when clients can build a calm, scripture-centered experience without knowing how the database, retrieval system, or AI provider is implemented.

The contracts should make:

- Scripture stable,
- Reader ownership explicit,
- Reflection safe,
- Journey predictable,
- Understanding transparent,
- and Saar grounded.

The API should expose Antar’s product language—not its internal machinery.