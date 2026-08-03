# Antar AI Pipeline

**Version:** 1.0  
**Status:** Draft for Architecture Review  
**Owner:** Engineering  
**Last Updated:** August 2026

---

# 1. Purpose

This document defines the complete runtime pipeline used to produce a grounded Saar response.

It covers the lifecycle from the moment a Reader submits a message through:

- request acceptance,
- authorization,
- conversation loading,
- context resolution,
- retrieval,
- reranking,
- prompt construction,
- model invocation,
- structured parsing,
- citation validation,
- safety validation,
- persistence,
- delivery,
- observability,
- retries,
- and failure recovery.

This document defines application behavior and architectural boundaries.

It does not define:

- the final prompt wording,
- the selected model provider,
- the exact embedding model,
- the complete database schema,
- frontend presentation,
- or detailed retrieval algorithms.

Those concerns are documented separately.

---

# 2. Product Position

Saar is Antar’s conversational study companion.

It appears only after the Reader has had the opportunity to:

```text
Read
  ↓
Reflect
  ↓
Choose a Learning Path
  ↓
Explore Curated Understanding
  ↓
Optionally Ask Saar
```

Saar is not the first layer of interpretation.

It is the final optional conversational layer.

The pipeline must preserve the following knowledge hierarchy:

```text
Scripture
  ↓
Traditional Commentary
  ↓
Curated Understanding
  ↓
Saar Synthesis
```

A generated response must never blur these categories.

---

# 3. Core Pipeline Principles

## 3.1 Ground Before Generate

The system should retrieve relevant sources before requesting generation.

The model should not be expected to answer from general model memory when Antar-controlled sources are required.

---

## 3.2 Canonical Context First

The current Verse and Chapter context are loaded before semantic retrieval.

The current Verse is not discovered through vector search.

It is resolved through canonical identity.

---

## 3.3 Curated Sources Before Broad Retrieval

The pipeline should prefer:

1. Current Verse.
2. Approved Translation.
3. Published Understanding.
4. Approved Commentary.
5. Curated Related Verses.
6. Additional semantically retrieved sources.

This prevents weak semantic matches from displacing stronger canonical context.

---

## 3.4 Provenance Is Part of the Response

Citations are not decoration added after generation.

The pipeline must track source identity from retrieval through prompt construction and final response validation.

---

## 3.5 Private Context Is Opt-In

Reader Reflections may be used only when:

- the Reader explicitly requests or approves their use,
- privacy preferences permit it,
- the Reflection belongs to the same Reader,
- the Conversation is authorized,
- and the prompt clearly distinguishes Reader-authored content from Scripture and Commentary.

Private Reflection content should not enter retrieval indexes shared across Readers.

---

## 3.6 Fail Conservatively

When grounding, parsing, validation, or provider invocation fails, Saar should not fabricate a normal response.

The system should return a clear failure state or a limited source-aware response where approved.

---

## 3.7 AI Work Is Asynchronous

The API accepts a Reader Message and returns a generation identifier.

Retrieval and generation occur outside the original request transaction.

This avoids:

- long-held HTTP connections,
- open database transactions,
- duplicate provider requests,
- and poor failure recovery.

Streaming may be added later without changing the durable generation model.

---

# 4. High-Level Pipeline

```text
Reader Message
  ↓
Request Validation
  ↓
Authentication and Authorization
  ↓
Idempotency Resolution
  ↓
Persist Reader Message
  ↓
Create Generation Run
  ↓
Load Conversation Context
  ↓
Load Canonical Verse Context
  ↓
Resolve Privacy-Approved Reader Context
  ↓
Classify Reader Intent
  ↓
Build Retrieval Plan
  ↓
Retrieve Sources
  ├── Exact Canonical Sources
  ├── Curated Understanding
  ├── Commentary
  ├── Related Verses
  ├── Full-Text Search
  └── Vector Search
  ↓
Normalize and Deduplicate
  ↓
Rerank
  ↓
Select Prompt Sources
  ↓
Build Structured Prompt
  ↓
Invoke LLM Provider
  ↓
Parse Structured Response
  ↓
Validate Claims and Citations
  ↓
Apply Safety and Scope Rules
  ↓
Persist Saar Message and Citations
  ↓
Complete Generation Run
  ↓
Deliver Response
```

---

# 5. Pipeline Components

The pipeline is coordinated by a Saar application service but implemented through explicit ports and services.

Recommended logical components:

```text
SaarMessageApplicationService

ConversationContextLoader

VerseContextLoader

ReaderContextResolver

IntentClassifier

RetrievalPlanner

CanonicalSourceRetriever

FullTextRetriever

VectorRetriever

RelatedVerseRetriever

SourceNormalizer

SourceDeduplicator

SourceReranker

PromptSourceSelector

PromptBuilder

LlmGateway

ResponseParser

CitationValidator

GroundingValidator

SafetyValidator

ResponsePersistenceService

GenerationStatusPublisher
```

These may initially live in one deployable application while remaining separated by interfaces.

---

# 6. Request Acceptance

## 6.1 Submit Message

The Reader submits:

```text
conversationId
messageContent
idempotencyKey
```

The server derives:

- Reader identity,
- Conversation ownership,
- current Verse scope,
- privacy settings,
- and conversation status.

The client must not submit:

- system prompts,
- source IDs to force inclusion,
- model names,
- temperature,
- raw provider configuration,
- or another Reader’s Reflection identifiers.

---

## 6.2 Request Validation

Validate:

- message is not blank,
- message length is within configured limits,
- Conversation exists,
- Conversation is active,
- Conversation belongs to the authenticated Reader,
- Verse context remains valid,
- rate limits permit processing,
- and the Idempotency Key is valid where required.

Rejected requests do not invoke retrieval or generation.

---

## 6.3 Idempotency

The same Reader, operation, Idempotency Key, and request body should return the original accepted result.

The same Idempotency Key with different content returns:

```text
IDEMPOTENCY_CONFLICT
```

Idempotency protects against:

- client retries,
- network timeouts,
- repeated taps,
- and duplicate mobile submissions.

---

# 7. Persistence Before Generation

The pipeline first persists:

1. Reader Message.
2. Generation Run in `PENDING` state.

This occurs in one local transaction.

Conceptually:

```text
Conversation
  ↓
Append Reader Message
  ↓
Create Generation Run
  ↓
Commit
```

Only after commit should retrieval and model invocation begin.

The provider call must never occur inside this transaction.

---

# 8. Generation Lifecycle

Possible generation states:

```text
PENDING
RETRIEVING
BUILDING_PROMPT
GENERATING
VALIDATING
COMPLETED
FAILED
CANCELLED
```

Recommended state progression:

```text
PENDING
  ↓
RETRIEVING
  ↓
BUILDING_PROMPT
  ↓
GENERATING
  ↓
VALIDATING
  ↓
COMPLETED
```

Failures preserve the last known stage.

Example:

```text
status = FAILED
failureStage = RETRIEVING
failureCode = GROUNDING_SOURCE_UNAVAILABLE
retryable = true
```

---

# 9. Conversation Context Loading

The pipeline loads a bounded conversation window.

Potential context includes:

- current Reader Message,
- selected prior Reader Messages,
- selected prior Saar Messages,
- current Verse identity,
- Guidance Session reference,
- and prior conversation summary where supported.

Do not send unlimited Conversation history to the model.

Reasons:

- token cost,
- privacy,
- relevance dilution,
- latency,
- and prompt injection risk.

Recommended V1 approach:

- include the latest small number of turns,
- preserve the original Conversation question where relevant,
- and omit irrelevant older turns.

Conversation summarization may be introduced later but must remain distinguishable from Reader-authored content.

---

# 10. Canonical Verse Context

The current Conversation is Verse-scoped.

The pipeline loads canonical context directly by identifier.

Required context:

```text
Chapter Number
Chapter Name
Verse Number
Canonical Reference
Sanskrit
Selected Transliteration
Selected Translation
Translation Source
```

Optional context:

```text
Chapter Intent
Previous Verse
Next Verse
Published Understanding
```

The current Verse must always be included in the prompt unless the Conversation has entered an explicitly supported broader study mode.

---

# 11. Reader Reflection Context

Reflection context is optional.

It may be included only when:

```text
Conversation requests Reflection context
AND
Reader privacy preference allows it
AND
Reflection ownership is verified
AND
Reflection references the same Verse or approved related context
```

The pipeline should include only the minimum necessary Reflection content.

Prefer:

- selected Quick Reflection,
- selected Deep Reflection excerpt,
- or a Reader-approved excerpt.

Avoid including the Reader’s full Reflection history by default.

Reflection must be labeled inside the prompt as:

```text
Reader-authored private reflection
```

It must never be treated as source material for factual or theological claims.

---

# 12. Intent Classification

Intent Classification determines what retrieval strategy is needed.

It does not determine truth.

Possible intent categories:

```text
CLARIFICATION
VERSE_MEANING
TERM_DEFINITION
TRADITIONAL_INTERPRETATION
RELATED_TEACHINGS
PRACTICAL_REFLECTION
COMPARE_INTERPRETATIONS
CONVERSATION_FOLLOW_UP
OUT_OF_SCOPE
SAFETY_SENSITIVE
```

The classifier may use:

- deterministic rules,
- a lightweight model,
- or a structured LLM call.

V1 should prefer simple rules where reliable.

Examples:

```text
"Where else does Krishna discuss action?"
→ RELATED_TEACHINGS

"What does detachment mean?"
→ TERM_DEFINITION

"What does Shankara say about this?"
→ TRADITIONAL_INTERPRETATION
```

Intent Classification should be observable and testable.

---

# 13. Retrieval Planning

The Retrieval Planner converts intent and context into a bounded retrieval plan.

Example plan:

```text
Current Verse: required
Published Understanding: required if available
Traditional Commentary: top 3 approved sources
Related Verses: top 3 curated relationships
Semantic Retrieval: maximum 5 chunks
Conversation Context: latest 4 turns
Reader Reflection: excluded
```

The plan should specify:

- source types,
- metadata filters,
- retrieval methods,
- source limits,
- language,
- approved editions,
- and token budget.

Retrieval must not fetch all available content.

---

# 14. Source Priority

Recommended priority:

```text
Priority 1
Current Verse and selected Translation

Priority 2
Published Understanding for current Verse

Priority 3
Direct Commentary passages for current Verse

Priority 4
Curated Related Verses

Priority 5
Full-text matches from approved sources

Priority 6
Semantic matches from approved sources
```

Lower-priority retrieval should supplement rather than displace higher-priority sources.

---

# 15. Exact Canonical Retrieval

Canonical retrieval supports:

- current Verse,
- explicitly referenced Verse,
- Chapter reference,
- Commentary source named by the Reader,
- and canonical cross-references.

Exact matches should bypass vector similarity.

Example:

```text
Reader asks about Bhagavad Gita 3.19
  ↓
Resolve 3.19 exactly
  ↓
Load Verse and approved Translation
```

Do not use semantic retrieval to guess when a canonical reference is unambiguous.

---

# 16. Curated Understanding Retrieval

When a published Understanding Article exists for the current Verse, it should be retrieved before broad semantic content.

Potential content:

- reviewed explanation,
- Key Ideas,
- Traditional Insights,
- Related Verses,
- and source metadata.

Only `PUBLISHED` content may enter Reader-facing generation.

Draft or unreviewed material must remain excluded.

---

# 17. Commentary Retrieval

Commentary retrieval must filter by:

- approved publication status,
- license status,
- Verse,
- language,
- and source identity.

Commentary passages must retain:

```text
Author
Tradition
Title
Edition
Passage Identifier
Verse Reference
```

The prompt should never present an editorial summary as a direct quote from a commentator.

---

# 18. Full-Text Retrieval

Full-text retrieval is appropriate for:

- exact terms,
- named concepts,
- distinctive phrases,
- and keyword-oriented questions.

It should use:

- approved knowledge chunks,
- language-aware text search,
- metadata filtering,
- and bounded result counts.

Full-text scores are not directly comparable with vector scores until normalized.

---

# 19. Vector Retrieval

Vector retrieval is appropriate for:

- conceptual similarity,
- paraphrased questions,
- themes,
- and related teachings not expressed through exact keywords.

Vector search must filter by approved metadata before or during retrieval.

Potential filters:

```text
publicationStatus = PUBLISHED
languageCode = selected language
sourceType in approved source types
licenseApproved = true
```

Private Reader content must not be part of the shared vector index.

---

# 20. Related Verse Retrieval

Related Verses should first use curated relationships.

Example relationship types:

```text
REINFORCES
CONTRASTS
EXPANDS
APPLIES
CONTEXTUALIZES
```

Semantic discovery may suggest future editorial relationships, but unreviewed relationships should not silently appear as curated Related Verses.

---

# 21. Retrieval Result Model

Each retrieved unit should include:

```text
knowledgeSourceId
knowledgeChunkId
sourceType
sourceEntityId
sourceVersion
title
content
canonicalReference
author
tradition
language
publicationStatus
retrievalMethod
initialRank
retrievalScore
metadata
```

The pipeline must retain this identity through generation and citation validation.

---

# 22. Deduplication

The same source may appear through multiple retrieval methods.

Example:

```text
Commentary passage retrieved by:
- exact Verse lookup,
- full-text search,
- vector search
```

Deduplicate using stable source or chunk identity.

When duplicates exist:

- preserve the strongest retrieval evidence,
- merge retrieval-method metadata,
- and avoid repeating identical content in the prompt.

---

# 23. Source Normalization

Scores from different retrieval systems are not directly comparable.

The pipeline should normalize:

- keyword score,
- vector similarity,
- curated-priority weight,
- canonical match weight,
- and source-quality weight.

The exact formula belongs in `06_RAG_ARCHITECTURE.md`.

The normalized representation should support deterministic debugging.

---

# 24. Reranking

Reranking orders retrieved candidates by final usefulness.

Potential signals:

- current Verse match,
- explicit Reader reference,
- intent alignment,
- source authority,
- publication status,
- language match,
- canonical relationship,
- keyword score,
- vector score,
- and chunk completeness.

The reranker may be:

- deterministic,
- cross-encoder based,
- LLM based,
- or hybrid.

V1 should begin with a transparent deterministic strategy unless measured quality requires more complexity.

---

# 25. Source Selection

The Prompt Source Selector chooses a bounded final set.

Selection must satisfy:

- token budget,
- source diversity,
- canonical context inclusion,
- provenance completeness,
- and intent relevance.

Example final source set:

```text
1 Current Verse
1 Selected Translation
1 Published Understanding excerpt
2 Commentary passages
2 Related Verses
```

Do not include sources merely because space remains.

---

# 26. Prompt Budgeting

The prompt should have explicit token budgets.

Conceptual allocation:

```text
System and Behavioral Instructions
Conversation Context
Current Verse Context
Retrieved Sources
Reader Question
Output Schema
Reserved Output Tokens
```

When the budget is exceeded, remove content in this order:

1. Lowest-ranked semantic sources.
2. Redundant Commentary.
3. Older Conversation turns.
4. Long secondary excerpts.
5. Optional editorial context.

Never remove:

- current Reader Question,
- current Verse identity,
- core safety rules,
- source labels,
- or output schema requirements.

---

# 27. Prompt Assembly

The Prompt Builder creates a structured provider-neutral prompt model.

Conceptually:

```text
SaarPrompt
- behavioral instructions
- scope rules
- current verse
- selected translation
- curated understanding
- commentary sources
- related verses
- optional reader reflection
- bounded conversation history
- current reader question
- output schema
```

Provider-specific formatting occurs inside the AI provider adapter.

---

# 28. Prompt Sections

Recommended prompt order:

```text
1. Saar Role and Boundaries
2. Response Requirements
3. Current Scripture Context
4. Curated Understanding
5. Traditional Commentary Sources
6. Related Scripture
7. Optional Reader Reflection
8. Conversation Context
9. Current Reader Question
10. Structured Output Schema
```

This ordering places stable instructions and source material before the final question.

---

# 29. Source Labels in Prompt

Every source should have a stable prompt-local identifier.

Example:

```text
[S1] Bhagavad Gita 2.47 — Sanskrit
[S2] Translation by Approved Source
[S3] Published Understanding v2
[S4] Commentary by Author A
[S5] Bhagavad Gita 3.19
```

The model must cite these identifiers in structured output.

Prompt-local source identifiers are later resolved to durable Citation records.

---

# 30. Prompt Injection Defense

Retrieved text is untrusted input.

Commentary, imported content, and Reader Messages may contain instructions that conflict with system behavior.

The pipeline must:

- clearly delimit source content,
- state that source text is evidence rather than instruction,
- prevent retrieved text from changing Saar’s role,
- restrict tool access,
- validate output against the expected schema,
- and avoid passing unnecessary hidden configuration.

Reader text must never be interpolated into system instructions.

---

# 31. Model Invocation

The LLM Gateway receives a provider-neutral request.

Conceptual request:

```text
GenerateStudyResponseCommand
- prompt
- modelClass
- maximumOutputTokens
- temperaturePolicy
- timeout
- structuredOutputSchema
- traceContext
```

The gateway handles:

- provider mapping,
- authentication,
- timeout,
- retry classification,
- response metadata,
- usage accounting,
- and provider error translation.

---

# 32. Model Selection

Model routing may consider:

- question complexity,
- context length,
- latency requirement,
- cost,
- structured-output support,
- and safety needs.

V1 may use one primary model.

The application should still avoid embedding provider-specific model names in business logic.

Model choice belongs to configuration or a routing policy.

---

# 33. Generation Parameters

Saar should favor consistency and groundedness over creativity.

Recommended policy characteristics:

- low-to-moderate temperature,
- bounded output length,
- structured output,
- no autonomous tool execution in V1,
- and explicit citation requirements.

Exact parameters depend on the provider and should be tested empirically.

---

# 34. Timeout Policy

Provider calls must have explicit timeouts.

Conceptual limits:

```text
Connection Timeout
Response Timeout
Overall Generation Deadline
```

Timeout should result in:

```text
AI_PROVIDER_TIMEOUT
```

The Generation Run remains retryable where appropriate.

Do not wait indefinitely for a provider response.

---

# 35. Retry Policy

Retry only transient failures.

Potentially retryable:

- connection reset,
- provider overload,
- temporary rate limit,
- gateway timeout,
- and selected 5xx responses.

Not automatically retryable:

- invalid request,
- prompt too large,
- policy rejection,
- malformed schema after repeated attempts,
- unsupported model,
- and permanent authorization failure.

Use bounded exponential backoff with jitter.

Do not retry indefinitely.

---

# 36. Provider Fallback

Provider fallback is optional in V1.

If implemented, fallback must preserve:

- the same source context,
- the same response schema,
- prompt version,
- and generation lineage.

A fallback attempt should create a new provider attempt record under the same Generation Run.

Do not mix partial outputs from different providers.

---

# 37. Structured Response

The model should return a structured object.

Conceptual schema:

```json
{
  "answer": "One way to understand this verse is...",
  "sourceUses": [
    {
      "sourceId": "S1",
      "claimSummary": "The verse distinguishes action from attachment to results."
    }
  ],
  "interpretiveNotes": [
    {
      "type": "MULTIPLE_INTERPRETATIONS",
      "text": "Different traditions emphasize different aspects of detachment."
    }
  ],
  "reflectionInvitation": "What changes when you separate effort from outcome?",
  "returnToScripture": {
    "recommended": true,
    "reference": "2.47"
  }
}
```

The exact schema will evolve, but generation should not rely on parsing arbitrary prose for citations.

---

# 38. Response Parsing

The Response Parser validates:

- valid structured format,
- required fields,
- output length,
- known source identifiers,
- supported note types,
- and safe string values.

Malformed output may trigger one controlled repair attempt.

The repair attempt should receive:

- the malformed response,
- schema errors,
- and the required schema.

It should not perform new retrieval.

---

# 39. Citation Resolution

The model references prompt-local source identifiers such as `S1`.

The Citation Resolver maps them back to:

- Knowledge Source,
- Knowledge Chunk,
- source version,
- canonical reference,
- and attribution metadata.

Unknown source identifiers invalidate the affected Citation.

The model may not invent a durable source identifier.

---

# 40. Citation Validation

Citation validation checks:

1. The source exists.
2. The source version matches.
3. The source was included in the prompt.
4. The cited claim is reasonably supported by the source.
5. The source type is allowed.
6. Attribution is complete.
7. The excerpt is within policy and licensing limits.

Validation results:

```text
VALID
PARTIAL
INVALID
UNSUPPORTED
```

A Message grounding status is derived from Citation results.

---

# 41. Grounding Status

Possible public grounding states:

```text
GROUNDED
PARTIALLY_GROUNDED
UNGROUNDED
VALIDATION_FAILED
```

Suggested rules:

## GROUNDED

All material factual or interpretive claims are supported by valid approved sources.

## PARTIALLY_GROUNDED

Core explanation is supported, but some synthesis or application extends beyond direct source support.

## UNGROUNDED

The response lacks sufficient source support.

The response should not be presented as a normal answer.

## VALIDATION_FAILED

The system could not reliably evaluate grounding.

Return a recoverable failure state or carefully limited response.

---

# 42. Claim Validation

Citation presence alone is not enough.

The pipeline should identify major claims and verify that:

- quoted claims match the source,
- attributed interpretations belong to the stated commentator,
- canonical references are correct,
- and the response does not elevate Saar synthesis into Scripture.

V1 may use:

- deterministic checks,
- source-text overlap,
- canonical-reference validation,
- and a separate validation model where justified.

---

# 43. Source Separation

The final response should preserve distinctions such as:

```text
From the Verse
Traditional Commentary
Saar’s Synthesis
Reflection Invitation
```

The client may present these visually.

The stored response should retain enough structure to support this distinction.

Avoid returning only one undifferentiated string where provenance matters.

---

# 44. Safety Validation

Safety validation occurs after parsing and before persistence.

It evaluates whether the response:

- stays within Saar’s scope,
- avoids medical diagnosis,
- avoids legal or financial authority,
- avoids crisis mishandling,
- avoids spiritual coercion,
- avoids manipulative dependency,
- avoids certainty beyond sources,
- and respects Reader autonomy.

Safety validation may result in:

```text
ALLOW
ALLOW_WITH_NOTICE
REPLACE_WITH_SAFE_RESPONSE
REJECT
ESCALATE
```

The exact safety policy belongs in `07_SECURITY_AND_PRIVACY.md` and Saar guardrail documents.

---

# 45. Scope Validation

Saar should refuse or redirect requests outside its role.

Examples:

- medical diagnosis,
- legal advice,
- financial directives,
- requests to act as an absolute spiritual authority,
- unrelated general-purpose assistance,
- and requests to override Scripture or source constraints.

The response should remain calm and useful without pretending expertise.

---

# 46. Reflection Preservation

When a Reader shares their interpretation, Saar should not immediately overwrite it.

The response should:

- acknowledge the Reader’s reflection without exaggerated praise,
- distinguish their interpretation from source material,
- offer additional perspective,
- and return agency to the Reader.

The pipeline should not transform Reflection content into a hidden psychological profile.

---

# 47. Respecting Silence

Some questions may benefit from a limited response that encourages contemplation.

The pipeline may support a response mode such as:

```text
CONTEMPLATIVE_PAUSE
```

Example output:

```text
This question may be worth sitting with before adding another interpretation.

You may wish to reread Bhagavad Gita 2.47 and notice what changes when attention moves from the outcome back to the action itself.
```

This behavior must not be used to avoid valid questions arbitrarily.

---

# 48. Persistence of Completed Response

After successful validation, persist in one transaction:

```text
Saar Message
Citations
Generation Run completion
Provider usage metadata
Grounding status
```

Conceptually:

```text
Append Saar Message
  +
Persist Citations
  +
Complete Generation Run
  +
Update Conversation lastMessageAt
  ↓
Commit
```

The final persisted Message is authoritative.

---

# 49. Persistence of Failed Response

On failure, persist:

- Generation status,
- failure stage,
- safe failure code,
- retryable flag,
- provider attempt metadata where safe,
- and completion timestamp.

Do not persist partial provider output as a normal Saar Message.

Partial text may be retained temporarily for debugging only if privacy and retention policies permit it.

---

# 50. Delivery

The client may obtain the result through:

- polling,
- push update,
- WebSocket,
- or server-sent events.

V1 default:

```text
Submit Message
  ↓
Receive Generation ID
  ↓
Poll Generation Status
  ↓
Fetch Completed Message
```

Streaming can later improve perceived latency while preserving the same durable model.

---

# 51. Streaming Considerations

If streaming is added:

- partial text is provisional,
- citations may arrive after relevant claims,
- the final persisted Message remains authoritative,
- unsafe or invalid output must be suppressible,
- and the client must handle stream failure.

A stream-completed event should include the final Message identifier.

Do not treat streamed tokens as durable truth before validation.

---

# 52. Retry Semantics

A Reader may retry a failed Generation.

A retry should:

- reuse the same Reader Message,
- create a new attempt,
- preserve the original Generation history,
- rerun retrieval if source freshness or failure stage requires it,
- and avoid creating another Reader Message.

Retrying a completed response should instead create an explicit regeneration use case, if supported.

---

# 53. Regeneration

Regeneration is not required for V1.

If introduced later, it should:

- create a new Saar Message version or sibling response,
- preserve the original response,
- disclose that a new answer was generated,
- and avoid becoming an engagement mechanic.

Regeneration should not silently replace history.

---

# 54. Cancellation

A pending Generation may support cancellation.

Cancellation is best-effort.

Possible behavior:

```text
PENDING or RETRIEVING
→ cancel immediately

GENERATING
→ request provider cancellation if supported

VALIDATING
→ finish validation or mark cancellation pending
```

Cancelled Generations do not create completed Saar Messages.

---

# 55. Conversation Closure

A closed Conversation:

- preserves existing Messages according to retention policy,
- rejects new Messages,
- and may still be viewed by the owning Reader.

Closing a Conversation does not delete it.

Deletion is a separate privacy operation.

---

# 56. Caching

Potential cache candidates:

- published Understanding,
- approved Commentary retrieval,
- canonical Verse context,
- Related Verse mappings,
- and retrieval results for common source-only questions.

Avoid caching responses that include:

- private Reflection context,
- sensitive Reader Messages,
- or personalized Conversation context

unless the cache is private, securely scoped, and explicitly justified.

Exact generated-response caching is not recommended by default.

---

# 57. Retrieval Freshness

Every retrievable source should have:

```text
sourceVersion
contentHash
publicationStatus
```

The retrieval projection must be refreshed when source content changes.

Embeddings and chunks should be invalidated when:

- source content changes,
- chunking changes,
- embedding model changes,
- or metadata affecting retrieval changes.

The final response records the source version used.

---

# 58. Prompt Versioning

Every Generation Run should record:

```text
promptVersion
pipelineVersion
retrievalPolicyVersion
model
provider
```

This supports:

- debugging,
- quality comparison,
- reproducibility,
- rollback,
- and evaluation.

Prompt text itself may live in source control or a controlled prompt registry.

Production prompts should not be edited manually without versioning.

---

# 59. Evaluation Hooks

The pipeline should capture data needed for offline evaluation without storing unnecessary private content.

Potential evaluation fields:

- intent classification,
- selected source types,
- selected source identifiers,
- retrieval ranks,
- Citation validity,
- grounding status,
- latency,
- token usage,
- failure stage,
- and Reader feedback where explicitly provided.

Evaluation datasets containing Reader content require privacy review.

---

# 60. Observability

Every Generation should have one correlation identifier spanning:

```text
API Request
Reader Message
Generation Run
Retrieval Run
Provider Attempt
Saar Message
```

Recommended traces:

```text
saar.message.accept
saar.context.load
saar.intent.classify
saar.retrieve.canonical
saar.retrieve.fulltext
saar.retrieve.vector
saar.rerank
saar.prompt.build
saar.provider.generate
saar.response.parse
saar.citation.validate
saar.safety.validate
saar.response.persist
```

---

# 61. Metrics

Recommended metrics:

## Volume

```text
saar_messages_submitted_total
saar_generations_started_total
saar_generations_completed_total
saar_generations_failed_total
```

## Latency

```text
saar_generation_duration
saar_retrieval_duration
saar_provider_duration
saar_validation_duration
```

## Retrieval

```text
saar_sources_retrieved
saar_sources_selected
saar_retrieval_empty_total
saar_retrieval_method_total
```

## Grounding

```text
saar_grounding_status_total
saar_citation_valid_total
saar_citation_invalid_total
```

## Cost

```text
saar_input_tokens_total
saar_output_tokens_total
saar_estimated_cost_total
```

Metric labels must remain low-cardinality.

Do not use Reader IDs, Message IDs, or raw query text as metric labels.

---

# 62. Logging

Safe structured log fields may include:

```text
requestId
conversationId
generationId
readerPseudonymousId
verseId
canonicalReference
pipelineStage
provider
model
promptVersion
retrievedSourceCount
selectedSourceCount
groundingStatus
failureCode
latencyMs
```

Do not log:

- full Reader Message,
- full Reflection,
- full Saar Response,
- provider prompt,
- system prompt,
- access tokens,
- or private source excerpts.

---

# 63. Trace Sampling

AI traces may be expensive.

Recommended policy:

- retain all failed Generation traces,
- retain sampled successful traces,
- retain latency outliers,
- and avoid storing private prompt content inside trace spans.

Trace metadata should be sufficient to correlate durable records.

---

# 64. Failure Categories

## Request Failures

```text
VALIDATION_ERROR
UNAUTHENTICATED
FORBIDDEN
CONVERSATION_CLOSED
RATE_LIMIT_EXCEEDED
```

## Context Failures

```text
VERSE_NOT_FOUND
TRANSLATION_NOT_AVAILABLE
PRIVACY_CONTEXT_DENIED
CONVERSATION_CONTEXT_UNAVAILABLE
```

## Retrieval Failures

```text
NO_GROUNDING_SOURCES
RETRIEVAL_TIMEOUT
VECTOR_STORE_UNAVAILABLE
FULL_TEXT_SEARCH_FAILED
RERANK_FAILED
```

## Prompt Failures

```text
PROMPT_TOO_LARGE
PROMPT_BUILD_FAILED
UNSUPPORTED_SOURCE_TYPE
```

## Provider Failures

```text
AI_PROVIDER_TIMEOUT
AI_PROVIDER_RATE_LIMITED
AI_PROVIDER_UNAVAILABLE
AI_PROVIDER_REJECTED
AI_PROVIDER_INVALID_RESPONSE
```

## Validation Failures

```text
RESPONSE_PARSE_FAILED
CITATION_VALIDATION_FAILED
GROUNDING_FAILED
SAFETY_VALIDATION_FAILED
```

## Persistence Failures

```text
MESSAGE_PERSISTENCE_FAILED
GENERATION_STATE_CONFLICT
```

---

# 65. Graceful Degradation

## Understanding Available, Saar Unavailable

Return:

- provider unavailable state,
- retry path,
- and continued access to Understanding.

## Vector Retrieval Unavailable

Fallback to:

- canonical Verse,
- published Understanding,
- direct Commentary,
- curated Related Verses,
- and full-text retrieval.

Only proceed if grounding remains sufficient.

## Commentary Unavailable

Proceed with Scripture and curated Understanding when the Reader’s question does not specifically require Commentary.

If Commentary was explicitly requested, return a limitation.

## No Understanding Article

Use canonical Scripture and approved Commentary.

Do not silently generate an Understanding Article.

## No Grounding Sources

Do not generate a normal Saar answer.

Encourage returning to the Verse or trying a more specific question.

---

# 66. Security Boundaries

The AI pipeline must not receive direct database access through generated tool calls in V1.

All source retrieval occurs through controlled application interfaces.

The model cannot:

- query arbitrary tables,
- retrieve another Reader’s Reflection,
- modify Scripture,
- update Reflection,
- change privacy settings,
- or invoke external tools autonomously.

Any future tool use requires separate architecture and authorization review.

---

# 67. Data Minimization

Send only the data required for the current response.

Avoid sending:

- full Reader history,
- unrelated Reflections,
- entire Commentary books,
- all translations,
- full account profile,
- or hidden analytics.

Prompt construction should be reviewable and explainable.

---

# 68. Provider Data Handling

The provider integration must document:

- whether prompts are retained,
- whether data is used for training,
- regional processing,
- encryption,
- retention duration,
- sub-processors,
- and deletion mechanisms.

Provider settings should disable training or retention where available and required.

The final provider decision belongs in `07_SECURITY_AND_PRIVACY.md`.

---

# 69. Cost Controls

Cost controls may include:

- per-Reader rate limits,
- input token limits,
- output token limits,
- source-count limits,
- Conversation history limits,
- model routing,
- daily budget alerts,
- provider quota monitoring,
- and administrative kill switches.

Cost limits should degrade Saar gracefully without affecting Reading or Reflection.

---

# 70. Feature Flags

Useful flags:

```text
saar.enabled
saar.reflectionContext.enabled
saar.vectorRetrieval.enabled
saar.providerFallback.enabled
saar.streaming.enabled
saar.contemplativePause.enabled
```

Flags should not create untested combinations without ownership.

Critical AI functionality must have a rapid disable path.

---

# 71. Quality Gates

A Saar response may be persisted as completed only when:

1. Structured parsing succeeds.
2. Required fields exist.
3. Source identifiers resolve.
4. Grounding validation meets the required threshold.
5. Citation validation succeeds sufficiently.
6. Safety validation allows the response.
7. The response remains within output limits.
8. Persistence succeeds.

Failure at any gate prevents normal completed delivery.

---

# 72. Testing Strategy

## Unit Tests

Test:

- intent classification,
- retrieval planning,
- score normalization,
- deduplication,
- prompt budgeting,
- source-label construction,
- response parsing,
- Citation mapping,
- grounding status calculation,
- and failure classification.

## Integration Tests

Test:

- PostgreSQL persistence,
- pgvector retrieval,
- full-text search,
- provider adapter behavior,
- timeout handling,
- idempotency,
- retry behavior,
- and transaction boundaries.

## Golden Tests

Maintain approved examples for:

- simple Verse clarification,
- Commentary comparison,
- Related Verse discovery,
- ambiguous interpretation,
- Reflection-aware response,
- unsupported question,
- and no-grounding scenario.

## Adversarial Tests

Test:

- prompt injection,
- fabricated citations,
- incorrect Verse references,
- source-attribution confusion,
- requests for absolute spiritual authority,
- sensitive personal disclosures,
- and attempts to access another Reader’s data.

---

# 73. Offline Evaluation

Potential quality dimensions:

```text
Groundedness
Citation correctness
Verse-reference correctness
Source attribution
Interpretive humility
Relevance
Conciseness
Reader agency
Return-to-scripture behavior
Safety
```

Evaluation should compare pipeline and prompt versions.

One aggregate score should not hide failures in Citation correctness or safety.

---

# 74. Human Review

Before production launch, representative responses should be reviewed by:

- product,
- engineering,
- safety or privacy reviewers,
- and qualified Bhagavad Gita content reviewers.

Technical groundedness does not guarantee theological or interpretive quality.

Content review criteria should remain explicit.

---

# 75. Initial V1 Pipeline

The recommended first implementation is:

```text
Persist Reader Message
  ↓
Load Current Verse
  ↓
Load Published Understanding
  ↓
Load Direct Commentary
  ↓
Load Curated Related Verses
  ↓
Optional Full-Text Retrieval
  ↓
Optional Vector Retrieval
  ↓
Deterministic Reranking
  ↓
Build Structured Prompt
  ↓
Invoke One LLM Provider
  ↓
Parse Structured Response
  ↓
Validate Source IDs
  ↓
Validate Canonical References
  ↓
Apply Safety Rules
  ↓
Persist Message and Citations
```

Do not begin with:

- multi-agent orchestration,
- autonomous tools,
- model-generated retrieval plans,
- multiple provider voting,
- fine-tuning,
- or complex graph retrieval.

---

# 76. Future Evolution

Potential later capabilities:

- streaming responses,
- provider fallback,
- cross-encoder reranking,
- Conversation summarization,
- multilingual retrieval,
- commentary comparison mode,
- source-aware follow-up suggestions,
- advanced claim validation,
- human review queues,
- and evaluation-driven model routing.

Each should be added only after measured need.

---

# 77. Decisions

The V1 pipeline adopts these decisions:

- Reader Messages are persisted before generation.
- Generation is asynchronous.
- Conversations are Verse-scoped by default.
- Canonical Verse context is loaded directly.
- Retrieval is source-filtered and publication-aware.
- Curated Understanding precedes broad semantic retrieval.
- Commentary retains attribution.
- Reader Reflection context is opt-in.
- Retrieval results are normalized, deduplicated, and reranked.
- Prompt sources use stable local identifiers.
- Model output is structured.
- Citations are validated before normal delivery.
- Grounding status is part of the Message contract.
- Provider calls occur outside database transactions.
- Failed generations do not create normal Saar Messages.
- Saar remains usable only when sufficient grounding exists.
- Reading, Reflection, Library, Journey, and Understanding remain operational without AI.

---

# 78. Open Decisions

The following remain unresolved:

- final LLM provider,
- final model,
- final embedding model,
- exact token budgets,
- intent-classification implementation,
- whether vector retrieval is required in the first vertical slice,
- initial Commentary source set,
- reranking formula,
- claim-validation depth,
- whether one repair attempt is permitted,
- polling versus streaming timeline,
- provider fallback,
- exact grounding threshold,
- retention of Retrieval and Generation diagnostics,
- and human-review workflow.

These should be resolved through implementation experiments and measurable evaluation.

---

# 79. North Star

Antar’s AI pipeline succeeds when every Saar response is:

- grounded in approved sources,
- explicit about provenance,
- humble about interpretation,
- safe with Reader-owned context,
- operationally observable,
- recoverable when dependencies fail,
- and clearly secondary to Scripture and curated learning.

The pipeline should make Saar trustworthy not because the model sounds confident, but because the system can explain where the response came from, what supported it, and where its certainty ends.