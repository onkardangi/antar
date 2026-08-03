# Antar RAG Architecture

**Version:** 1.0  
**Status:** Draft for Architecture Review  
**Owner:** Engineering  
**Last Updated:** August 2026

---

# 1. Purpose

This document defines Antar’s Retrieval-Augmented Generation architecture.

It explains how approved knowledge is:

- acquired,
- validated,
- normalized,
- versioned,
- chunked,
- embedded,
- indexed,
- retrieved,
- reranked,
- selected,
- cited,
- evaluated,
- and rebuilt.

The RAG system exists to ground Saar responses in identifiable sources.

It does not make generated content authoritative.

The knowledge hierarchy remains:

```text
Scripture
    ↓
Traditional Commentary
    ↓
Curated Understanding
    ↓
Saar Synthesis
```

---

# 2. Scope

This document covers:

- source eligibility,
- content ingestion,
- licensing metadata,
- canonical identity,
- source normalization,
- knowledge projections,
- chunking,
- embeddings,
- full-text indexing,
- vector indexing,
- hybrid retrieval,
- metadata filtering,
- score normalization,
- reranking,
- prompt-source selection,
- citation provenance,
- reindexing,
- observability,
- evaluation,
- and failure recovery.

This document does not define:

- the final LLM provider,
- exact production prompts,
- frontend citation presentation,
- complete content-administration workflows,
- or the detailed security policy.

---

# 3. RAG Objectives

Antar’s RAG architecture should optimize for:

1. **Canonical correctness**
2. **Source provenance**
3. **Interpretive transparency**
4. **Retrieval relevance**
5. **Privacy**
6. **Operational simplicity**
7. **Rebuildability**
8. **Measured quality rather than architectural novelty**

Retrieval quality must not be judged only by semantic similarity.

A relevant source must also be:

- approved,
- attributable,
- licensed,
- current,
- correctly scoped,
- and suitable for the Reader’s question.

---

# 4. Non-Goals

V1 does not require:

- autonomous research agents,
- open-web retrieval,
- arbitrary internet search,
- knowledge graphs,
- graph RAG,
- multi-hop agent loops,
- model-generated SQL,
- self-modifying indexes,
- user-generated shared embeddings,
- or multiple dedicated vector databases.

The initial design should remain explainable and easy to operate.

---

# 5. Architectural Principles

## 5.1 Canonical Lookup Before Semantic Retrieval

A known Verse reference must be resolved directly.

Example:

```text
Bhagavad Gita 2.47
BG 2.47
Chapter 2 Verse 47
```

These should resolve to the same canonical Verse without vector search.

Semantic retrieval supplements canonical lookup.

It does not replace it.

---

## 5.2 Retrieval Uses Approved Knowledge Only

A source may enter the Reader-facing retrieval index only when it is:

- identified,
- licensed or otherwise legally approved,
- normalized,
- publication-approved,
- versioned,
- and attributable.

Draft, unlicensed, anonymous, or retired content must remain excluded.

---

## 5.3 Source Identity Survives Every Stage

A source must retain stable identity through:

```text
Owning Domain Record
    ↓
Knowledge Source Projection
    ↓
Knowledge Chunk
    ↓
Embedding
    ↓
Retrieval Result
    ↓
Prompt Source
    ↓
Citation
```

A Citation should always resolve back to the exact source version used during generation.

---

## 5.4 Search Projections Are Rebuildable

The Search domain does not own canonical content.

The following are projections:

- knowledge sources,
- chunks,
- search vectors,
- embeddings,
- normalized metadata,
- and retrieval indexes.

They must be rebuildable from authoritative domain records.

---

## 5.5 Private Reflection Is Not Shared Knowledge

Reader-authored Reflection content must not enter the shared knowledge index.

Private Reflection context may be loaded directly for one authorized request when:

- ownership is verified,
- Reader consent exists,
- privacy preferences permit it,
- and the product flow explicitly requires it.

It must remain isolated from other Readers.

---

## 5.6 Curated Relationships Outrank Inferred Similarity

A reviewed Related Verse connection should generally outrank a purely semantic relationship.

Curated knowledge expresses editorial intent.

Vector similarity expresses mathematical proximity.

Those signals are not equivalent.

---

## 5.7 Retrieval Must Be Explainable

For every selected source, the system should be able to report internally:

- why it was eligible,
- how it was retrieved,
- how it was scored,
- why it was selected,
- which source version was used,
- and where it appeared in the final response.

---

# 6. High-Level Architecture

```text
Authoritative Content
    │
    ├── Scripture
    ├── Translations
    ├── Commentary
    └── Curated Understanding
    │
    ▼
Content Ingestion
    ↓
Validation and Licensing Checks
    ↓
Normalization
    ↓
Knowledge Source Projection
    ↓
Chunking
    ↓
Full-Text Indexing
    ↓
Embedding Generation
    ↓
Vector Indexing
    ↓
Published Retrieval Corpus
```

Runtime:

```text
Reader Question
    ↓
Canonical Context Resolution
    ↓
Retrieval Plan
    ↓
Metadata Filtering
    ↓
Exact Retrieval
    +
Full-Text Retrieval
    +
Vector Retrieval
    +
Curated Relationship Retrieval
    ↓
Deduplication
    ↓
Score Normalization
    ↓
Reranking
    ↓
Prompt-Source Selection
    ↓
Saar Generation
    ↓
Citation Validation
```

---

# 7. Knowledge Source Types

Approved V1 source types may include:

```text
VERSE
TRANSLATION
TRANSLITERATION
COMMENTARY_PASSAGE
UNDERSTANDING_ARTICLE
UNDERSTANDING_SECTION
TRADITIONAL_INSIGHT
RELATED_VERSE_EXPLANATION
CHAPTER_INTENT
```

Not all source types should be eligible for every question.

Examples:

- Sanskrit Verse content supports canonical grounding.
- Translation supports Reader-language explanation.
- Commentary supports traditional interpretation.
- Understanding supports reviewed educational explanation.
- Chapter Intent supports orientation but should not be presented as Scripture.

---

# 8. Authoritative Source Ownership

| Source Type | Owning Domain |
|---|---|
| Chapter | Scripture |
| Verse | Scripture |
| Transliteration | Scripture |
| Translation | Scripture |
| Commentary Passage | Scripture |
| Understanding Article | Understanding |
| Key Concept | Understanding |
| Traditional Insight | Understanding |
| Related Verse Relationship | Understanding |

The Search domain stores projections only.

It must never become the editing surface for authoritative content.

---

# 9. Source Eligibility

A source is eligible for Reader-facing retrieval only when all applicable checks pass.

```text
publicationStatus = PUBLISHED
licenseStatus = APPROVED
contentVersion is active
language is supported
source attribution is complete
content is non-empty
source is not retired
```

Commentary additionally requires:

- identifiable author or tradition,
- edition or publication metadata where available,
- and clear distinction between original passage and editorial summary.

---

# 10. Content Ingestion Pipeline

```text
Source Submission
    ↓
Format Validation
    ↓
Metadata Validation
    ↓
License Review
    ↓
Canonical Mapping
    ↓
Content Normalization
    ↓
Editorial Review
    ↓
Publication Approval
    ↓
Projection Creation
    ↓
Chunking
    ↓
Indexing
```

Ingestion may be:

- manually initiated,
- administrative,
- batch-based,
- or imported from an approved structured source.

Reader-facing retrieval must never index content directly from an unreviewed upload.

---

# 11. Ingestion States

Suggested lifecycle:

```text
RECEIVED
VALIDATING
REQUIRES_REVIEW
APPROVED
INDEXING
PUBLISHED
FAILED
RETIRED
```

A source becomes retrievable only after:

```text
APPROVED
    ↓
Successfully Indexed
    ↓
PUBLISHED
```

The system should not expose partially indexed publication states.

---

# 12. Canonical Mapping

Every source must be mapped to stable domain identity.

Examples:

```text
Translation
    → Verse 2.47
    → Translation Source A
    → Content Version 3
```

```text
Commentary Passage
    → Verse 2.47
    → Commentary Source B
    → Passage Order 1
```

A failed canonical mapping blocks publication.

The system should never guess Verse associations through semantic similarity during ingestion.

---

# 13. Content Normalization

Normalization should preserve meaning while creating predictable indexable content.

Potential normalization steps:

- Unicode normalization,
- line-ending normalization,
- whitespace cleanup,
- heading preservation,
- removal of import artifacts,
- normalized canonical references,
- language-code normalization,
- transliteration-scheme labeling,
- source-attribution attachment,
- and safe markup conversion.

Normalization must not:

- rewrite Commentary,
- paraphrase Scripture,
- remove meaningful punctuation,
- merge distinct sources,
- or silently translate content.

The original approved content should remain preserved separately from normalized retrieval text where needed.

---

# 14. Content Hashing

Every projected source and chunk should have a deterministic content hash.

Example inputs:

```text
sourceType
sourceEntityId
sourceVersion
normalizedContent
normalizationVersion
chunkingVersion
```

The hash supports:

- duplicate detection,
- indexing idempotency,
- embedding reuse,
- change detection,
- and rebuild validation.

---

# 15. Knowledge Source Projection

Recommended structure:

```text
KnowledgeSource
---------------
id
sourceType
sourceEntityId
sourceVersion
languageCode
title
canonicalReference
normalizedContent
publicationStatus
licenseStatus
contentHash
metadata
createdAt
updatedAt
```

`KnowledgeSource` is one logical retrievable document before chunking.

Examples:

- one Verse,
- one Translation,
- one Commentary Passage,
- one Understanding Article.

---

# 16. Metadata Model

Metadata enables retrieval filtering and provenance.

Common metadata:

```text
chapterNumber
verseNumber
canonicalReference
languageCode
sourceType
author
translator
tradition
publication
edition
publicationYear
relationshipType
publicationStatus
licenseStatus
contentVersion
```

Optional semantic metadata:

```text
keyConcepts
themes
relatedVerseReferences
editorialTopics
```

Semantic metadata should be editorially approved or clearly marked as generated.

Generated metadata must not silently become canonical.

---

# 17. Chunking Philosophy

Chunking should preserve coherent meaning.

The chunk should be large enough to retain context and small enough to retrieve precisely.

Do not optimize chunk size only for embedding benchmarks.

The correct unit depends on source type.

---

# 18. Source-Specific Chunking

## 18.1 Verse

Recommended:

```text
One Verse = One Chunk
```

A Verse chunk may include:

- canonical reference,
- Sanskrit,
- selected Transliteration,
- and one approved Translation

only if the retrieval use case benefits from a combined representation.

Alternatively, preserve each as separate source types and combine them after retrieval.

Recommended V1 approach:

- keep Verse and Translation as distinct Knowledge Sources,
- retrieve the current Verse canonically,
- and avoid depending on vector search for its identity.

---

## 18.2 Translation

Recommended:

```text
One Verse Translation = One Chunk
```

Do not merge many Verses into one Translation chunk.

This preserves precise citation and canonical identity.

---

## 18.3 Commentary

Commentary passages may be longer.

Chunk boundaries should prefer:

1. Author-defined paragraphs.
2. Section boundaries.
3. Thematic continuity.
4. Sentence-safe token boundaries.

Suggested initial target:

```text
300–700 tokens
```

with modest overlap only where required.

Overlap should not cause repeated citations or duplicated prompt content.

---

## 18.4 Understanding Article

Chunk by semantic section:

```text
Overview
Understanding
Key Ideas
Traditional Insight
Related Verses
```

Do not split a Key Idea explanation across chunks where avoidable.

A section should retain:

- article identity,
- section type,
- Verse identity,
- and content version.

---

## 18.5 Chapter Intent

Usually one short chunk per Chapter.

Chapter Intent is editorial orientation.

It must not be labeled as Scripture.

---

# 19. Chunk Representation

```text
KnowledgeChunk
--------------
id
knowledgeSourceId
chunkIndex
sectionType
content
tokenCount
contentHash
metadata
createdAt
```

Chunk identity must remain stable when the underlying source and chunking version are unchanged.

---

# 20. Chunk Overlap

Overlap may help preserve context across boundaries but creates duplication.

Use overlap conservatively.

Recommended starting policy:

- no overlap for Verse or Translation,
- small sentence-aware overlap for long Commentary,
- no overlap between clearly independent Understanding sections.

The retrieval pipeline should deduplicate near-identical overlapping chunks.

---

# 21. Chunking Version

Every chunk should record:

```text
chunkingPolicyVersion
normalizationVersion
```

A chunking-policy change requires rebuilding affected chunks and embeddings.

Do not update chunk content in place while preserving an outdated hash or version.

---

# 22. Embedding Strategy

Embeddings support semantic retrieval.

They do not determine authority.

Each embedding record should include:

```text
knowledgeChunkId
embeddingModel
embeddingDimension
embedding
contentHash
embeddingPolicyVersion
createdAt
```

An embedding is valid only for the exact chunk content hash and model.

---

# 23. Embedding Input

The embedding text may include selected structured context.

Example:

```text
Source Type: Commentary
Verse: Bhagavad Gita 2.47
Author: [Name]
Tradition: [Tradition]

[Chunk content]
```

This may improve semantic precision.

However, the input format must be consistent and versioned.

Do not include:

- publication status noise,
- internal database identifiers,
- private Reader data,
- or unrelated operational metadata.

---

# 24. Embedding Model Selection

The final model remains open.

Selection criteria should include:

- retrieval quality,
- supported languages,
- Sanskrit and transliteration behavior,
- embedding dimension,
- cost,
- latency,
- provider data handling,
- model stability,
- and migration complexity.

The system must support re-embedding with a new model.

Business logic must not assume one fixed vector dimension.

---

# 25. Multilingual Considerations

Antar may contain:

- Sanskrit,
- transliteration,
- English Translation,
- and future additional languages.

V1 should explicitly test whether the selected embedding model handles:

- Sanskrit script,
- Romanized Sanskrit,
- theological terminology,
- translated conceptual questions,
- and cross-language retrieval.

Possible strategies:

1. One multilingual embedding model.
2. Separate language indexes.
3. Retrieval primarily over translated content.
4. Hybrid exact lookup plus language-specific semantic search.

This decision should be evidence-based.

---

# 26. Vector Index

V1 uses pgvector.

Potential index types:

```text
HNSW
IVFFlat
```

The choice should be based on:

- corpus size,
- write frequency,
- query latency,
- recall requirements,
- memory,
- and PostgreSQL version.

HNSW is a likely initial candidate for a moderate read-heavy corpus, but the decision must be benchmarked.

Exact vector search may be sufficient for a very small initial corpus.

---

# 27. Full-Text Index

Each searchable chunk may contain a PostgreSQL `tsvector`.

The configuration should match the source language where practical.

Full-text retrieval is particularly valuable for:

- specific terms,
- names,
- phrases,
- canonical concepts,
- and Commentary references.

A GIN index should support efficient search.

---

# 28. Canonical Reference Parser

Canonical reference parsing occurs before full-text or vector retrieval.

Supported examples may include:

```text
2.47
BG 2.47
Bhagavad Gita 2:47
Chapter 2 Verse 47
Gita 2.47
```

Parsing result:

```text
resolved = true
chapterNumber = 2
verseNumber = 47
```

Ambiguous or invalid references must not be force-resolved.

---

# 29. Runtime Retrieval Inputs

The retrieval request may include:

```text
Reader Question
Current Verse
Conversation Scope
Intent
Language
Translation Preference
Requested Tradition
Requested Author
Approved Source Types
Token Budget
Maximum Results
```

It must not accept arbitrary client-defined SQL, index filters, or provider instructions.

---

# 30. Retrieval Plan

A `RetrievalPlan` defines exactly what the pipeline will search.

Conceptual model:

```text
RetrievalPlan
- canonicalSources
- requiredSourceTypes
- optionalSourceTypes
- metadataFilters
- fullTextQuery
- semanticQuery
- curatedRelations
- limitsBySourceType
- totalResultLimit
- language
- tokenBudget
```

The plan should be persistable or reproducible for debugging.

---

# 31. Retrieval Modes

## Exact Retrieval

Used for:

- current Verse,
- explicit Verse references,
- named Commentary sources,
- specific Understanding content,
- and curated relationships.

## Full-Text Retrieval

Used for:

- exact concepts,
- phrases,
- names,
- and terminology.

## Vector Retrieval

Used for:

- semantic similarity,
- paraphrased concepts,
- and broader thematic questions.

## Curated Relationship Retrieval

Used for:

- Related Verses,
- reviewed Commentary links,
- Key Ideas,
- and editorial study paths.

---

# 32. Hybrid Retrieval

Hybrid retrieval combines results from multiple retrieval modes.

Conceptually:

```text
Exact Sources
    +
Curated Sources
    +
Full-Text Results
    +
Vector Results
    ↓
Unified Candidate Set
```

The system must retain the retrieval method for every candidate.

A source retrieved through multiple methods should remain one candidate with combined evidence.

---

# 33. Metadata Filtering

Filter before vector retrieval where supported.

Required filters may include:

```text
publicationStatus = PUBLISHED
licenseStatus = APPROVED
languageCode = selected language
sourceType in allowed types
contentVersion = active
```

Question-specific filters may include:

```text
author = requested author
tradition = requested tradition
chapterNumber = current chapter
canonicalReference = explicit reference
```

Retrieval must not depend on post-filtering unapproved sources from a broad result set where preventable.

---

# 34. Candidate Result Model

```text
RetrievalCandidate
------------------
knowledgeSourceId
knowledgeChunkId
sourceType
sourceVersion
content
metadata
retrievalMethods
exactMatch
curatedRelation
fullTextScore
vectorScore
sourceAuthorityScore
intentMatchScore
normalizedScore
finalRank
```

---

# 35. Deduplication

Deduplicate using:

1. Stable chunk identity.
2. Stable source identity.
3. Content hash.
4. Near-duplicate detection where overlap exists.

When one chunk is retrieved by multiple methods:

- preserve all retrieval methods,
- retain the best raw score from each method,
- and calculate one final candidate score.

---

# 36. Score Normalization

Raw scores from different systems are not directly comparable.

Examples:

- PostgreSQL text rank,
- cosine similarity,
- curated-priority weight,
- exact-match indicator.

Each score should be normalized into a common range.

Conceptual normalized fields:

```text
exactMatchScore
curatedRelationScore
fullTextNormalized
vectorNormalized
authorityScore
intentAlignmentScore
languageMatchScore
```

The exact formulas must be versioned and tested.

---

# 37. Initial Deterministic Scoring

A transparent V1 scoring model may use weighted signals.

Conceptual example:

```text
finalScore =
    exactMatchWeight
  + curatedRelationshipWeight
  + sourceAuthorityWeight
  + intentAlignmentWeight
  + fullTextWeight
  + vectorWeight
  + languageMatchWeight
```

This formula is illustrative only.

The actual values should be derived through evaluation.

Hard rules should override score where appropriate.

Examples:

- current Verse is always included,
- unapproved content is always excluded,
- requested named Commentary outranks generic semantic matches,
- and wrong-language content is excluded unless fallback is explicitly allowed.

---

# 38. Source Authority

Authority is not global truth.

It is a product retrieval priority.

Example source tiers:

```text
Tier 1
Canonical Scripture

Tier 2
Approved direct Translation and Commentary

Tier 3
Published Curated Understanding

Tier 4
Curated Related Verse explanations

Tier 5
Additional approved semantic matches
```

The score should not imply that all interpretations within one tier are equivalent.

---

# 39. Intent Alignment

Different questions require different sources.

Examples:

## Verse Meaning

Prefer:

- current Verse,
- Translation,
- Understanding,
- direct Commentary.

## Traditional Interpretation

Prefer:

- requested commentator,
- requested tradition,
- direct Commentary passage.

## Related Teachings

Prefer:

- curated Related Verses,
- exact concept matches,
- then semantic Verse retrieval.

## Practical Reflection

Prefer:

- current Verse,
- curated Understanding,
- limited related teaching context.

Do not retrieve unrelated personal-development content.

---

# 40. Reranking

Reranking refines the unified candidate set.

V1 should begin with deterministic reranking.

Possible future rerankers:

- cross-encoder,
- lightweight classification model,
- or structured LLM reranker.

A learned reranker should not override source approval or canonical rules.

---

# 41. Reranking Inputs

Potential signals:

- exact canonical match,
- current Verse relationship,
- explicit Reader reference,
- source type,
- curated relationship,
- intent alignment,
- language,
- named author or tradition,
- full-text relevance,
- vector similarity,
- chunk completeness,
- and content recency/version.

---

# 42. Diversity Constraints

The final source set should avoid unnecessary repetition.

Possible constraints:

- maximum Commentary passages per source,
- maximum chunks from one article,
- minimum presence of canonical Scripture,
- and optional source-type diversity.

Diversity should not force weak sources into the prompt.

Quality and direct relevance remain primary.

---

# 43. Prompt-Source Selection

After reranking, select a bounded source set.

Conceptual limits:

```text
Current Verse: 1
Selected Translation: 1
Understanding Sections: 1–3
Commentary Passages: 1–3
Related Verses: 0–3
Additional Semantic Chunks: 0–3
```

The exact count depends on the question and token budget.

Do not fill every category for every request.

---

# 44. Selection Rules

Always include:

- current Verse identity,
- selected Translation,
- and provenance metadata.

Include Understanding when:

- published,
- relevant,
- and appropriate to the intent.

Include Commentary when:

- directly relevant,
- explicitly requested,
- or needed for interpretive grounding.

Include semantic results only when they add value beyond curated sources.

---

# 45. Context Compression

Long sources may require compression before prompt assembly.

Preferred order:

1. Select a smaller complete chunk.
2. Select a relevant subsection.
3. Use an editorially prepared summary.
4. Apply controlled extractive compression.

Avoid model-generated compression of authoritative source material in the critical retrieval path unless its provenance and accuracy are validated.

Direct source text is preferable when licensing permits.

---

# 46. Citation Provenance

Each prompt source receives a local identifier.

Example:

```text
S1
S2
S3
```

Mapping:

```text
S1
→ knowledgeChunkId
→ knowledgeSourceId
→ sourceEntityId
→ sourceVersion
→ owning domain
```

The model may cite only identifiers included in the prompt.

---

# 47. Citation Record

A durable Citation should preserve:

```text
messageId
knowledgeSourceId
knowledgeChunkId
sourceType
sourceEntityId
sourceVersion
promptSourceLabel
citationLabel
quotedExcerpt
claimSummary
validationStatus
displayOrder
```

The system should be able to recreate the exact source used at generation time.

---

# 48. Citation Validation

Validation should confirm:

- the cited label existed in the prompt,
- the source was approved,
- the source version matches,
- the claim is reasonably supported,
- canonical references are correct,
- attribution is correct,
- and excerpts comply with licensing constraints.

A citation to a source does not automatically validate every sentence near it.

---

# 49. Attribution Rules

## Scripture

Display:

```text
Bhagavad Gita 2.47
```

Include Translation attribution when the translated wording is shown.

## Commentary

Display:

- author,
- tradition where relevant,
- title or edition where appropriate,
- and Verse reference.

## Curated Understanding

Clearly label as reviewed Antar educational content.

## Saar Synthesis

Never present generated synthesis as a direct source.

---

# 50. Knowledge Publication Workflow

A source should follow:

```text
Draft
    ↓
Editorial Review
    ↓
Licensing Approval
    ↓
Technical Validation
    ↓
Publication Approval
    ↓
Index Build
    ↓
Retrieval Verification
    ↓
Published
```

Publication should be atomic from the Reader’s perspective.

A source should not become visible before its retrieval projection is ready where retrieval depends on it.

---

# 51. Reindexing Triggers

Reindex when:

- canonical content changes,
- source publication status changes,
- translation or Commentary is corrected,
- Understanding content is republished,
- chunking policy changes,
- normalization policy changes,
- embedding model changes,
- metadata affecting filtering changes,
- or retrieval projection corruption is detected.

---

# 52. Incremental Reindexing

Normal content updates should reindex only affected sources.

Process:

```text
Detect Changed Source
    ↓
Create New Projection Version
    ↓
Create New Chunks
    ↓
Generate Search Vector
    ↓
Generate Embeddings
    ↓
Validate
    ↓
Atomically Activate New Version
    ↓
Retire Old Projection
```

Readers should not see a partially indexed source.

---

# 53. Full Rebuild

A full rebuild may be required for:

- embedding-model migration,
- chunking-policy migration,
- normalization changes,
- index corruption,
- or major metadata redesign.

Recommended process:

```text
Build New Index Version
    ↓
Run Validation
    ↓
Compare Retrieval Quality
    ↓
Switch Active Index Alias or Version
    ↓
Retain Rollback Window
    ↓
Retire Old Index
```

With PostgreSQL, this may use versioned projection rows or parallel tables.

---

# 54. Index Versioning

Track:

```text
corpusVersion
normalizationVersion
chunkingPolicyVersion
embeddingModel
embeddingPolicyVersion
retrievalPolicyVersion
```

Every Retrieval Run should record the versions used.

This makes evaluation and rollback possible.

---

# 55. Rebuildability

The following must be reproducible from authoritative sources:

- knowledge sources,
- chunks,
- search vectors,
- embeddings,
- vector indexes,
- and source metadata projections.

Backups remain important, but correctness must not depend on preserving a non-rebuildable search projection.

---

# 56. Index Validation

Before activation, verify:

- all expected published sources are present,
- retired sources are absent,
- content hashes match,
- chunk counts are plausible,
- embeddings exist,
- vector dimensions match,
- canonical references resolve,
- language metadata exists,
- and sample queries return expected results.

---

# 57. Retrieval Failure Handling

## Exact Source Missing

Return a canonical-content failure.

Do not substitute a semantically similar Verse.

## Full-Text Failure

Continue with exact, curated, and vector retrieval if sufficient.

## Vector Failure

Continue with exact, curated, and full-text retrieval if sufficient.

## Index Version Mismatch

Reject affected candidates and surface an operational error.

## No Relevant Sources

Do not generate a normal grounded Saar answer.

Return a limitation or invite the Reader to clarify.

---

# 58. Empty Retrieval Behavior

An empty semantic result does not imply that canonical context is absent.

The system may still answer from:

- current Verse,
- Translation,
- Understanding,
- or direct Commentary.

However, if the Reader asks for material not supported by available sources, Saar should acknowledge the limitation.

---

# 59. Privacy and Reader Data

Shared indexes must exclude:

- Reflections,
- private Saar Messages,
- Guidance free text,
- account data,
- and reading history.

Reader-specific context should be loaded through authorized domain services at request time.

It must not be persisted as a shared Knowledge Source.

---

# 60. Prompt Injection in Indexed Sources

All indexed text is treated as untrusted evidence.

During prompt assembly:

- delimit source content,
- label source type,
- prohibit source text from overriding system instructions,
- exclude executable markup,
- remove unsafe import artifacts,
- and validate structured output.

An approved source may still contain prose resembling instructions.

Approval does not convert it into system behavior.

---

# 61. Licensing

Every non-original source should retain:

- rights status,
- license type,
- attribution requirements,
- excerpt limits,
- redistribution restrictions,
- source URL or publication reference,
- and approval record.

Retrieval and citation behavior may differ by license.

Example:

- full text may be retrievable internally,
- but only a short excerpt may be displayable publicly.

Licensing rules must be enforced before final response presentation.

---

# 62. Copyright-Aware Prompting

The Prompt Source Selector may include longer source context internally where legally permitted.

The response validator should prevent excessive reproduction of copyrighted Commentary.

Prefer:

- paraphrase with attribution,
- concise excerpts,
- and citation links or source labels

over long reproduction.

---

# 63. Evaluation Strategy

RAG quality should be evaluated independently from generation style.

Core dimensions:

```text
Canonical Accuracy
Retrieval Recall
Retrieval Precision
Source Authority
Citation Correctness
Attribution Correctness
Coverage
Groundedness
Interpretive Relevance
Latency
Cost
```

---

# 64. Evaluation Dataset

Build a versioned evaluation set containing representative questions.

Categories:

- direct Verse reference,
- Verse meaning,
- term definition,
- traditional interpretation,
- named commentator,
- related teaching,
- comparison,
- chapter context,
- ambiguous question,
- unsupported claim,
- and no-answer scenario.

Each test case should define:

```text
question
currentVerse
intent
requiredSources
acceptableSources
prohibitedSources
expectedCanonicalReferences
notes
```

---

# 65. Golden Retrieval Cases

Examples:

## Case 1

Question:

```text
What does Bhagavad Gita 2.47 say about results?
```

Required:

- Verse 2.47,
- selected Translation.

Preferred:

- published Understanding,
- direct Commentary.

## Case 2

Question:

```text
Where else is action without attachment discussed?
```

Required:

- current Verse,
- curated Related Verses.

Preferred:

- semantically similar approved Verses.

## Case 3

Question:

```text
What does Shankara say about this Verse?
```

Required:

- matching approved Commentary source.

Prohibited:

- attribution to another commentator.

---

# 66. Retrieval Metrics

Offline metrics may include:

```text
Recall@K
Precision@K
Mean Reciprocal Rank
nDCG
Exact Reference Accuracy
Required Source Inclusion Rate
Prohibited Source Rate
Citation Source Match Rate
```

One metric should not hide canonical failures.

Exact-reference accuracy should be measured separately.

---

# 67. Human Evaluation

Qualified reviewers should assess:

- whether selected sources answer the question,
- whether traditions are represented accurately,
- whether relevant Commentary is omitted,
- whether semantic matches are misleading,
- and whether source ordering reflects the product’s hierarchy.

Technical similarity alone cannot validate interpretive quality.

---

# 68. Online Quality Signals

Potential privacy-safe signals:

- Reader opens cited Verse,
- Reader opens Commentary source,
- Reader reports incorrect citation,
- Reader marks response as unhelpful,
- retrieval returns no sources,
- and response fails grounding validation.

Do not infer theological correctness from engagement time.

---

# 69. A/B Testing Boundaries

A/B tests may compare:

- retrieval weights,
- source limits,
- reranking policies,
- and prompt-source formatting.

Do not experiment invisibly with:

- source authority hierarchy,
- citation visibility,
- Reader privacy,
- or the distinction between Scripture and Saar synthesis.

These are product principles, not optimization variables.

---

# 70. Observability

Recommended trace spans:

```text
rag.plan
rag.retrieve.exact
rag.retrieve.curated
rag.retrieve.fulltext
rag.retrieve.vector
rag.deduplicate
rag.normalize
rag.rerank
rag.select
rag.citation.resolve
```

Each Retrieval Run should record:

```text
corpusVersion
retrievalPolicyVersion
queryIntent
candidateCount
selectedCount
methodsUsed
latency
failureCode
```

---

# 71. Metrics

## Indexing

```text
rag_sources_indexed_total
rag_chunks_created_total
rag_embeddings_created_total
rag_index_failures_total
rag_index_duration
```

## Retrieval

```text
rag_retrieval_requests_total
rag_candidates_returned
rag_candidates_selected
rag_empty_results_total
rag_retrieval_duration
```

## Methods

```text
rag_exact_matches_total
rag_fulltext_matches_total
rag_vector_matches_total
rag_curated_matches_total
```

## Quality

```text
rag_required_source_inclusion_rate
rag_invalid_source_total
rag_citation_resolution_failures_total
```

Metric labels must remain low-cardinality.

---

# 72. Logging

Safe fields:

```text
retrievalRunId
conversationId
generationId
currentVerseId
intent
corpusVersion
retrievalPolicyVersion
sourceTypesRequested
candidateCount
selectedCount
methodsUsed
latencyMs
failureCode
```

Do not log:

- full Reader question,
- private Reflection,
- full source content,
- embeddings,
- or prompt text.

---

# 73. Performance Targets

Initial targets should be measured and revised.

Conceptual V1 goals:

```text
Canonical lookup:
tens of milliseconds

Full-text retrieval:
low hundreds of milliseconds or less

Vector retrieval:
low hundreds of milliseconds or less

Combined retrieval and reranking:
under one second at normal load
```

Retrieval should consume a minority of total Saar latency.

Correctness takes priority over aggressive latency optimization.

---

# 74. Caching

Potential cache candidates:

- canonical Verse lookup,
- published Understanding,
- direct Commentary by Verse,
- curated Related Verse mappings,
- and stable query-independent source projections.

Avoid globally caching retrieval responses tied to:

- private Reader questions,
- Conversation context,
- or Reflection context.

Cache keys must include relevant:

- source versions,
- language,
- translation,
- and retrieval-policy version.

---

# 75. Scaling Strategy

V1 begins with PostgreSQL and pgvector.

Scale in stages:

## Stage 1

- one PostgreSQL primary,
- indexed full-text search,
- pgvector,
- bounded corpus.

## Stage 2

- read replicas where appropriate,
- background indexing workers,
- optimized vector indexes,
- query caching,
- and connection-pool tuning.

## Stage 3

Consider a dedicated search or vector platform only when:

- corpus size,
- latency,
- filtering,
- write throughput,
- or operational isolation

cannot be met reasonably in PostgreSQL.

Migration should preserve stable Knowledge Source and Citation identities.

---

# 76. Background Processing

Indexing should run outside Reader-facing request transactions.

Potential jobs:

```text
ProjectKnowledgeSource
ChunkKnowledgeSource
BuildSearchVector
GenerateEmbedding
ValidateProjection
ActivateProjectionVersion
RetireOldProjection
```

V1 may use:

- scheduled jobs,
- Spring task execution,
- or a database-backed job queue.

Kafka is not required.

---

# 77. Idempotent Indexing

Each indexing step should be idempotent.

Given the same:

```text
sourceId
sourceVersion
contentHash
normalizationVersion
chunkingVersion
embeddingModel
```

the pipeline should not create duplicate active projections.

Retries must be safe.

---

# 78. Concurrency During Publication

Two content versions must not become active simultaneously for the same canonical publication slot unless the product explicitly supports editions.

Use:

- optimistic locking,
- unique active-version constraints,
- or transactional activation.

Readers should receive one consistent published version per request.

---

# 79. Rollback

A new corpus or source version should be reversible.

Rollback may:

- reactivate the previous projection version,
- restore the previous active corpus version,
- and invalidate caches.

Citation history for previously generated Messages must continue resolving to the source version originally used.

---

# 80. Data Retention

Active projections remain while sources are published.

Retired projection versions may be retained for:

- Citation resolution,
- auditability,
- and rollback.

Embeddings for unused old versions may be deleted after the required retention window, provided old Citations can still resolve to non-embedding source content.

Retrieval diagnostics may use limited retention.

---

# 81. Initial V1 Retrieval Policy

Recommended first implementation:

```text
1. Resolve current Verse directly.

2. Resolve explicit canonical references directly.

3. Load selected Translation.

4. Load published Understanding.

5. Load direct approved Commentary.

6. Load curated Related Verses.

7. Run bounded full-text retrieval when needed.

8. Run bounded vector retrieval when needed.

9. Deduplicate candidates.

10. Apply deterministic reranking.

11. Select a small source-aware prompt set.

12. Preserve exact source identity for Citations.
```

Do not begin with vector search as the only retrieval method.

---

# 82. Initial V1 Corpus

A practical first corpus should include:

- all 18 Chapters,
- all canonical Verses,
- one approved Transliteration,
- one or more legally approved Translations,
- a limited approved Commentary set,
- published Understanding content for the initial supported Verses,
- and curated Related Verse mappings.

Saar coverage should be limited transparently if the approved corpus is incomplete.

---

# 83. Implementation Sequence

## Phase 1 — Canonical Corpus

- Scripture projection
- exact Verse lookup
- Translation retrieval
- source identity
- Citation mapping

## Phase 2 — Curated Study

- Understanding projection
- Commentary projection
- Related Verse retrieval
- deterministic source selection

## Phase 3 — Search

- full-text chunk index
- canonical-reference parser
- metadata filters

## Phase 4 — Semantic Retrieval

- embedding generation
- pgvector index
- hybrid retrieval
- score normalization

## Phase 5 — Evaluation

- golden dataset
- retrieval metrics
- human review
- version comparison

---

# 84. Decisions

The V1 RAG architecture adopts these decisions:

- PostgreSQL and pgvector are the initial retrieval platform.
- Canonical reference resolution precedes semantic retrieval.
- Search data is a rebuildable projection.
- Only approved, licensed, published sources enter the corpus.
- Source identity is preserved end to end.
- Verse and Translation remain precisely scoped.
- Commentary uses source-aware semantic chunking.
- Understanding is chunked by meaningful section.
- Reader Reflection is excluded from shared indexes.
- Retrieval is hybrid rather than vector-only.
- Curated relationships outrank inferred semantic similarity.
- V1 reranking is deterministic and explainable.
- Prompt source selection is bounded by relevance and token budget.
- Citations resolve to exact source versions.
- Corpus, chunking, embedding, and retrieval policies are versioned.
- Reindexing is incremental and idempotent.
- A full parallel rebuild supports major model or policy migrations.
- Retrieval quality is evaluated separately from generation fluency.

---

# 85. Open Decisions

The following remain unresolved:

- initial approved Translation sources,
- initial approved Commentary sources,
- licensing limits,
- selected embedding model,
- vector dimension,
- multilingual retrieval approach,
- HNSW versus IVFFlat,
- exact chunk-size ranges,
- overlap policy,
- score-normalization formulas,
- reranking weights,
- whether a cross-encoder is required later,
- exact source limits per intent,
- Citation claim-validation depth,
- retention of historical projection versions,
- and deployment strategy for background indexing workers.

These should be resolved through small corpus experiments and formal evaluation.

---

# 86. North Star

Antar’s RAG system succeeds when Saar can answer from a small, high-quality, clearly attributable body of knowledge rather than a large, opaque pool of semantically similar text.

The system should always know:

- what source was used,
- who created it,
- which version was retrieved,
- why it was selected,
- what claim it supports,
- and where Saar’s own synthesis begins.

Retrieval exists to make AI accountable to Scripture and approved study material—not merely to make responses sound informed.