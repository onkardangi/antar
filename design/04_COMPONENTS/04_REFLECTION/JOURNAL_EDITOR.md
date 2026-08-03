# JOURNAL EDITOR

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Journal Editor provides a calm, distraction-free space for readers to capture their personal reflections after engaging with a teaching from the Bhagavad Gita.

It exists to preserve the reader's own thoughts.

The editor should feel closer to writing in a journal than creating a document.

---

# Responsibility

Journal Editor is responsible for:

* capturing personal reflections,
* presenting existing reflections,
* supporting uninterrupted writing,
* preserving the reader's own words,
* maintaining a distraction-free writing experience.

---

# Non-Responsibilities

Journal Editor is not responsible for:

* creating the invitation to reflect,
* saving content,
* generating writing,
* correcting grammar,
* suggesting improvements,
* evaluating reflections,
* summarizing entries,
* recommending scripture,
* interpreting emotions,
* or navigating away from the experience.

Those responsibilities belong to surrounding Reflection components and supporting services.

---

# Usage

Journal Editor appears after Reflection Invitation.

Typical locations:

* Verse
* Journal
* Journey (editing an existing reflection)
* Future guided reflection experiences

The editor should never appear without meaningful context from the teaching.

---

# Experience Principles

## The Reader Owns the Words

Everything written belongs to the reader.

The editor should never modify, rewrite, or improve journal content automatically.

---

## Distraction-Free Writing

The editor should contain only the tools required for writing.

Formatting controls, toolbars, and advanced editing features are intentionally absent from Version 1.

---

## Preserve Flow

Writing should feel uninterrupted.

The interface should avoid unnecessary confirmations, interruptions, or mode changes while the reader is actively writing.

---

## Privacy by Default

The editor should reinforce that reflections are personal.

Readers should never feel that their writing is being evaluated or scored.

---

## Context Matters

The surrounding teaching provides meaning to the reflection.

The editor should not feel detached from the verse that inspired it.

---

# Content Model

Journal Editor may receive:

* reflection identifier,
* associated verse identifier,
* existing reflection text,
* creation timestamp,
* last modified timestamp,
* read-only state when appropriate.

The editor should treat journal content as plain text in Version 1.

---

# Anatomy

Journal Editor contains:

1. Writing Surface
2. Placeholder (when empty)
3. Caret
4. Optional Character Count (future consideration only)

```text id="m5z8gk"
────────────────────────────

Write here...

────────────────────────────
```

The writing surface is the primary focus.

No formatting toolbar is presented.

---

# Variants

## Empty

No reflection exists.

Display a calm placeholder that encourages writing without directing it.

Example:

> Write only if you wish.

---

## Existing Reflection

Display the reader's saved reflection exactly as it was written.

Do not alter spacing, punctuation, or wording.

---

## Read-Only

Used for exported or archived reflections.

Writing is disabled while preserving readability.

---

# States

## Ready

The editor is available for writing.

---

## Focused

The writing surface has focus.

The component should clearly communicate the active writing state without unnecessary decoration.

---

## Writing

The reader is actively entering text.

The experience should avoid interruptions while typing.

---

## Empty

No reflection has been written yet.

The placeholder should feel welcoming rather than instructional.

---

## Read-Only

The reflection is visible but cannot be edited.

---

# Interaction Behavior

Journal Editor supports:

* typing,
* deletion,
* cursor movement,
* selection,
* copy,
* paste,
* undo and redo using platform conventions.

The editor should not introduce custom editing behavior when platform expectations already exist.

The component does not own saving.

Save Status communicates persistence separately.

---

# Content Guidelines

Placeholder text should:

* feel calm,
* avoid pressure,
* reinforce optional participation.

Good examples:

* Write only if you wish.
* Your thoughts are yours.
* Begin whenever you're ready.

Avoid:

* Start typing...
* Tell us what you learned.
* Required.
* Minimum 50 characters.
* Great job!

---

# Formatting

Version 1 supports plain text only.

The editor intentionally excludes:

* bold,
* italics,
* headings,
* lists,
* colors,
* images,
* attachments,
* links,
* tables,
* markdown,
* rich text.

Readers should focus on reflection rather than formatting.

---

# Accessibility

Journal Editor must:

* support Dynamic Type,
* expose a standard multiline text field,
* preserve keyboard navigation,
* support VoiceOver and TalkBack,
* announce placeholder text correctly,
* maintain sufficient touch target size,
* preserve insertion point during autosave,
* support external keyboards where available.

The editor should not unexpectedly move focus while writing.

---

# Motion

Journal Editor introduces almost no motion.

Appropriate motion includes:

* caret movement,
* native text-selection handles,
* platform keyboard transitions.

Avoid:

* animated placeholders,
* writing celebrations,
* typing effects,
* autosave animations,
* distracting transitions.

---

# Design Token Dependencies

Journal Editor uses:

* Typography System
* Color System
* Spacing System
* Accessibility System

It should not introduce custom visual styling beyond semantic tokens.

---

# Engineering Boundaries

Journal Editor may receive:

* initial reflection text,
* editing enabled state,
* placeholder,
* focus state,
* accessibility metadata.

It should not:

* persist content,
* trigger autosave,
* calculate writing statistics,
* invoke AI,
* analyze sentiment,
* determine reflection quality,
* or navigate after writing.

Those responsibilities belong to surrounding systems.

---

# Privacy Principles

Journal Editor should never imply that reflections are reviewed, scored, or shared.

The component should not:

* display writing analytics,
* estimate emotional state,
* encourage public sharing,
* compare entries,
* or rank reflections.

Readers should feel complete ownership of their writing.

---

# Good Examples

✓ A reader quietly writes for several minutes without interruption.

✓ Existing reflections appear exactly as previously written.

✓ Platform copy and paste work naturally.

✓ Focus remains in the editor during autosave.

---

# Anti-Patterns

Avoid:

✗ Rich text formatting.

✗ AI-assisted writing.

✗ Grammar suggestions.

✗ Writing streaks.

✗ Reflection scores.

✗ Required minimum length.

✗ Decorative backgrounds.

✗ Multiple editing modes.

✗ Pop-ups while writing.

---

# Confirmed Decisions

* Plain text only in Version 1.
* Writing is always optional.
* Journal Editor owns writing—not saving.
* AI does not participate in writing.
* Existing reflections remain unchanged.
* Platform editing behavior is preferred over custom interactions.

---

# Design Hypotheses

The following require validation:

* Whether any placeholder text is better than none.
* Whether a visible caret alone is sufficient for orientation.
* Whether read-only mode should reuse the same component.
* Whether character count provides value or unnecessary pressure.

---

# Validation Questions

* Does the editor feel calmer than a traditional notes app?
* Can readers begin writing without hesitation?
* Does plain text reduce distraction?
* Do readers understand that their writing remains private?
* Does separating Save Status from the editor reduce cognitive load?
* Can long reflections remain comfortable to read and edit?

---

# North Star

Journal Editor succeeds when readers forget they are using an editor and instead feel as though they are simply writing down a personal conversation with the teaching. The interface should disappear, leaving only the reader and their reflection.
