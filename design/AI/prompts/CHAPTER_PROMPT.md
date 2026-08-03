# CHAPTER_PROMPT.md

Before generating this screen, read **FIGMA_CONTEXT.md** completely.

This document defines the philosophy, architecture, and constraints of Antar.

Do not generate this screen without following those rules.

---

# Screen

Chapter

Version: 1.0

Purpose

The Chapter experience orients readers within a single chapter of the Bhagavad Gita before they begin reading individual verses.

Its purpose is navigation.

It is not a reading experience.

It should help readers understand where they are, what this chapter explores, and how to begin.

---

# Primary User Question

"What is this chapter about, and where should I begin reading?"

---

# Primary Goal

Help readers confidently choose a verse while preserving the canonical structure of the Bhagavad Gita.

---

# Approved Components

Top Navigation

Chapter Intent

Verse List

Continue Reading

Only use documented ADL components.

Do not invent additional sections.

---

# Information Hierarchy

The screen should follow this order exactly.

1. Top Navigation

2. Chapter Intent

3. Verse List

4. Continue Reading

No additional primary sections.

---

# Chapter Intent

Chapter Intent introduces the chapter.

It may contain:

- Chapter Number
- Canonical Chapter Name
- Brief Intent

It should orient the reader without replacing the chapter itself.

It should remain concise.

---

# Verse List

Verse List presents Verse Items in canonical order.

Verse List owns organization.

Verse Item owns navigation.

Do not redesign Verse Items.

Do not display scripture inside the list.

Each Verse Item should remain lightweight.

---

# Continue Reading

Continue Reading should quietly help readers resume where they previously stopped.

It should remain visually secondary.

---

# Layout Principles

Design for:

- orientation
- clarity
- calm
- rhythm
- whitespace

Readers should understand the structure of the chapter immediately.

---

# Visual Hierarchy

Chapter Intent

↓

Verse List

↓

Continue Reading

The Verse List should occupy most of the screen.

---

# Reading Philosophy

The Chapter screen is a table of contents.

It is not a preview of the teachings.

Avoid large scripture excerpts.

Avoid summaries that replace reading.

---

# Interaction Rules

Readers should naturally progress:

Understand the chapter

↓

Choose a verse

↓

Enter the Verse experience

The screen should support this flow without distraction.

---

# Forbidden Features

Do not generate:

- AI chat
- recommendations
- meditation exercises
- chapter ratings
- popular verses
- trending teachings
- social activity
- achievement badges
- streaks
- infinite scrolling
- dashboard widgets

---

# Wireframe Rules

Generate a grayscale wireframe only.

Use rectangles and placeholder text.

No colors.

No gradients.

No illustrations.

No shadows.

No polished UI.

Focus entirely on hierarchy and layout.

---

# Success Criteria

The screen succeeds when readers immediately understand:

- which chapter they are viewing,
- what the chapter broadly explores,
- and how to begin reading.

The interface should quietly guide readers into scripture without competing with it.