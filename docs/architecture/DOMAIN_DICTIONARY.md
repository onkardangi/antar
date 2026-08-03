# Antar Domain Dictionary

**Version:** 1.0  
**Status:** Canonical  
**Owner:** Architecture  
**Last Updated:** August 2026

---

# Purpose

This document defines the canonical business vocabulary used throughout Antar.

These terms should be used consistently across:

- Product documentation
- Design
- Engineering
- APIs
- Database schema
- AI prompts
- Analytics
- Testing

Avoid creating synonyms for concepts already defined here.

---

# Core Philosophy

The language of Antar should reflect the reader's journey rather than technical implementation.

Whenever possible, choose words that are meaningful to readers instead of engineering jargon.

---

# Reader

The individual using Antar.

The term "Reader" is preferred over:

- Customer
- Client
- Consumer
- End User

A Reader interacts with scripture through reading, reflection, study, and conversation.

---

# Scripture

The canonical content of the Bhagavad Gita.

Scripture includes:

- Chapters
- Verses
- Sanskrit
- Transliterations
- Translations

Scripture is immutable.

No generated content should ever be considered Scripture.

---

# Chapter

A canonical division of the Bhagavad Gita.

A Chapter owns an ordered collection of Verses.

---

# Verse

The smallest canonical unit of scripture.

A Verse includes:

- Reference
- Sanskrit
- Transliteration
- Translation

Every Verse belongs to exactly one Chapter.

---

# Commentary

An interpretation written by an identifiable teacher or tradition.

Commentary is not scripture.

Every Commentary should retain attribution.

---

# Traditional Insight

A curated summary inspired by one or more traditional commentaries.

Traditional Insight is editorial content.

It should never be presented as canonical scripture.

---

# Reading

The act of engaging with scripture.

Reading focuses on experiencing the verse itself.

Reading is distinct from study.

---

# Reading Progress

The reader's current position within scripture.

Reading Progress represents continuity.

It is not a measure of achievement.

---

# Today's Invitation

The single primary action on the Home screen.

Today's Invitation presents one already-selected next meaningful step.

It does not determine the destination.

Possible states include:

- Begin Journey
- Continue Reading
- Resume Reflection
- Curated Teaching

Today's Invitation is a composition.

It is not a reusable UI component.

---

# Reflection

Personal writing created by the Reader after engaging with scripture.

Reflection belongs to the Reader.

Reflection is never modified by AI without explicit user intent.

---

# Quick Reflection

A short thought captured immediately after reading.

Quick Reflection exists within the Verse experience.

Its purpose is immediate capture rather than extended writing.

---

# Deep Reflection

A longer journal entry.

Deep Reflection exists within the Reflection experience.

Its purpose is thoughtful exploration.

---

# Journey

The Reader's chronological history of reflections.

Journey exists to support remembrance rather than measurement.

Journey is intentionally not:

- analytics
- productivity
- gamification
- progress tracking

---

# Journey Memory

A representation of one meaningful moment in the Reader's Journey.

Journey Memory references:

- Reflection
- Verse
- Date

Journey Memory is a projection.

It is not an independent source of truth.

---

# Guidance

The experience that follows Reflection.

Guidance helps Readers choose how they would like to continue learning.

Guidance does not generate explanations.

It routes Readers toward the appropriate learning experience.

---

# Study Path

A learning direction selected from Guidance.

Examples include:

- Understand this Verse
- Connect with Other Teachings
- Learn from Traditional Commentaries
- Ask Saar

Study Paths represent reader intention rather than content categories.

---

# Understanding

A curated educational experience.

Understanding presents:

- Explanation
- Key Ideas
- Traditional Insight
- Related Verses

Understanding remains fully functional without AI.

---

# Key Idea

A concise concept extracted from a Verse.

Examples:

- Duty
- Wisdom
- Detachment
- Compassion

Key Ideas support understanding.

They do not replace explanation.

---

# Related Verse

A Verse connected through theme or teaching.

Related Verses help Readers continue studying scripture.

They are not recommendations.

---

# Saar

Antar's conversational study companion.

Saar is not:

- a teacher
- a guru
- an authority
- a search engine

Saar exists to deepen understanding after reading and study.

---

# Conversation

A sequence of interactions between the Reader and Saar.

Conversation is scoped to learning.

It is not intended to become open-ended social chat.

---

# Message

One unit of communication within a Conversation.

Messages may originate from:

- Reader
- Saar

---

# Citation

A reference supporting part of Saar's response.

Citations may point to:

- Scripture
- Commentary
- Curated Understanding

Every citation should preserve provenance.

---

# Retrieval

The process of locating relevant knowledge before AI generation.

Retrieval is not visible to Readers.

Its purpose is grounding.

---

# Curated Understanding

Educational content reviewed before publication.

Curated Understanding is distinct from AI-generated synthesis.

---

# Provenance

The origin of displayed knowledge.

Readers should always be able to distinguish:

Scripture

↓

Commentary

↓

Curated Understanding

↓

Saar Synthesis

---

# Source of Truth

The authoritative origin of information.

For Antar:

Scripture is the primary source of truth.

Traditional Commentary provides historical interpretation.

Curated Understanding provides reviewed educational content.

Saar provides conversational synthesis.

---

# Design Principles

Timeless rules that guide product design.

Examples:

- Scripture Before Interface
- Reading Before Reflection
- One Responsibility Per Screen
- AI Is a Companion

Design Principles influence every experience.

---

# Architecture Decision Record (ADR)

A documented architectural decision.

ADRs explain:

- Context
- Decision
- Consequences

ADRs preserve architectural reasoning over time.

---

# Projection

A derived representation built from one or more aggregates.

Examples:

Journey Memory

Today's Invitation

Projections improve experiences without becoming authoritative data.

---

# Aggregate

A consistency boundary within the domain model.

Every Aggregate owns:

- business rules
- invariants
- lifecycle

Aggregates should not modify one another directly.

---

# Canonical Vocabulary

The following terms are preferred throughout Antar.

✓ Reader

✓ Verse

✓ Chapter

✓ Reflection

✓ Journey

✓ Guidance

✓ Understanding

✓ Saar

✓ Conversation

✓ Citation

✓ Reading Progress

✓ Commentary

✓ Related Verse

✓ Today's Invitation

Avoid introducing alternate names unless they represent genuinely different business concepts.

---

# Naming Principles

When introducing a new concept, ask:

1. Does this already exist under another name?

2. Does this term reflect the Reader's experience?

3. Is this term understandable outside engineering?

4. Will this still make sense five years from now?

If the answer is "no," reconsider the name before adding it to the domain.