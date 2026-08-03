# SAVE STATUS

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Save Status quietly reassures readers that their reflections have been preserved.

It exists to build confidence without interrupting the writing experience.

Readers should never have to wonder whether their thoughts have been saved.

---

# Responsibility

Save Status is responsible for:

* communicating persistence state,
* reducing anxiety around data loss,
* remaining visible without becoming distracting,
* reflecting the current save lifecycle.

---

# Non-Responsibilities

Save Status is not responsible for:

* performing saves,
* scheduling autosave,
* retrying synchronization,
* resolving conflicts,
* evaluating journal content,
* displaying writing statistics,
* or requesting user confirmation.

Those responsibilities belong to persistence and synchronization services.

---

# Usage

Save Status appears whenever the Journal Editor is editable.

Typical locations:

* Verse
* Journal
* Journey

It should remain close enough to the editor that readers naturally associate it with their writing.

---

# Experience Principles

## Quiet Confidence

Readers should notice Save Status only when reassurance is needed.

The component should fade into the background during uninterrupted writing.

---

## No Celebration

Saving is expected behavior.

The component should not congratulate the reader or celebrate successful persistence.

---

## Honest Communication

Never imply that writing has been saved when it has not.

Uncertainty should be communicated clearly and calmly.

---

## Minimize Interruption

Status changes should not steal focus from the editor.

Readers should remain free to continue writing.

---

# Anatomy

Save Status contains:

1. Status Label
2. Optional Timestamp
3. Optional Sync Indicator

Example:

```text
Saved

Saved 2 minutes ago

Saving...

Unable to sync
```

---

# States

## Saving

Changes are being persisted.

---

## Saved

All known changes have been successfully saved.

---

## Offline

Writing continues locally.

Synchronization will resume automatically when possible.

---

## Sync Pending

Changes are stored locally but have not yet synchronized.

---

## Sync Failed

Saving could not be completed.

The reader's local work should remain protected whenever possible.

---

# Interaction Behavior

Save Status is primarily informational.

Version 1 contains no direct actions.

Future versions may expose retry behavior only if required.

---

# Accessibility

Save Status must:

* announce meaningful state changes without excessive repetition,
* avoid interrupting active writing,
* support Dynamic Type,
* remain understandable without icons alone,
* preserve semantic status announcements.

---

# Motion

State transitions should remain subtle.

Avoid:

* checkmark celebrations,
* confetti,
* large animations,
* repeated flashing.

---

# Engineering Boundaries

Save Status receives:

* persistence state,
* synchronization state,
* optional timestamp.

It must not:

* trigger persistence,
* own retry logic,
* detect connectivity,
* or determine conflict resolution.

---

# Good Examples

✓ Saved

✓ Saving…

✓ Saved locally. Waiting to sync.

✓ Unable to sync. Your writing remains on this device.

---

# Anti-Patterns

Avoid:

✗ Great job! Saved!

✗ Animated success celebrations.

✗ Blocking writing while saving.

✗ Modal dialogs for successful saves.

✗ Hiding failures.

---

# Confirmed Decisions

* Autosave is the default.
* Save Status communicates only persistence.
* It never interrupts writing.
* Saving is expected, not celebrated.
* Local writing is always prioritized over synchronization.

---

# Design Hypotheses

* Is a timestamp valuable or unnecessary?
* Should "Saved" fade after several seconds?
* Is a persistent status clearer than a transient one?

---

# Validation Questions

* Do readers trust that their writing is safe?
* Does the component remain unobtrusive?
* Are failures communicated clearly without creating panic?

---

# North Star

Save Status succeeds when readers never think about saving because they trust their reflections are quietly being preserved.
