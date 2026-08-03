# JOURNAL INTERACTION BLUEPRINT

**Experience:** Journal
**Version:** 1.0
**Status:** Draft
**Owner:** Design
**Last Updated:** August 2026

---

# Mission

The Journal experience exists to help readers capture their personal response to a teaching from the Bhagavad Gita.

Rather than serving as a general-purpose notebook, the Journal preserves the conversation between the reader and the teaching.

Every journal entry should remain rooted in scripture, encouraging reflection without prescribing what the reader should think or write.

---

# Modes of Arrival

| Arrival          | Experience Responsibility                            |
| ---------------- | ---------------------------------------------------- |
| Verse            | Continue naturally from reading into reflection.     |
| Journey          | Revisit and expand a previous reflection.            |
| Saved Reflection | Resume unfinished writing or revisit a past insight. |

---

# Reader Mindset

Readers arrive ready to pause rather than consume.

Some will have immediate thoughts.

Others may simply want to sit with the teaching.

The Journal should welcome both.

Silence is as valid as writing.

The interface should never pressure the reader to produce an entry.

---

# Success Definition

The experience is successful when the reader:

* feels invited rather than obligated to write,
* easily connects their reflection to the teaching,
* trusts that their writing is private,
* leaves with the feeling that their thoughts have been preserved—not evaluated.

---

# Interaction Timeline

## Stage 1 — Return to the Teaching

### Intent

Reconnect the reader with the verse that inspired the reflection.

### Design Decision

The teaching should remain visible so reflection always has context.

### Components

* Verse Reference
* Verse Preview

---

## Stage 2 — Reflect

### Intent

Create space for genuine personal reflection.

### Design Decision

Offer one gentle prompt that encourages thought without directing the response.

### Components

* Reflection Invitation

---

## Stage 3 — Write

### Intent

Capture the reader's own words.

### Design Decision

Writing should feel uninterrupted, calm, and free from unnecessary formatting or distractions.

### Components

* Journal Editor
* Save Status

---

## Stage 4 — Preserve

### Intent

Quietly reassure the reader that their reflection has been saved.

### Design Decision

Saving should happen automatically whenever possible.

The interface should communicate confidence without interrupting the writing process.

### Components

* Save Status

---

# Screen Blueprint

```text
────────────────────────────

Verse Reference

Verse Preview

────────────────────────────

Reflection Invitation

────────────────────────────

Journal Editor

────────────────────────────

Saved

────────────────────────────
```

---

# States & Recovery

## New Reflection

Present the verse and reflection invitation with an empty editor.

---

## Existing Reflection

Restore the previous entry exactly as the reader left it.

---

## Saving

Autosave quietly in the background while indicating save progress in a non-intrusive way.

---

## Offline

Allow writing to continue.

Synchronize automatically when connectivity returns.

---

## Sync Failure

Never risk losing the reader's writing.

Clearly communicate that changes are stored locally and will synchronize when possible.

---

# Component Extraction

## Reusable Components

* Verse Reference
* Verse Preview
* Reflection Invitation
* Journal Editor
* Save Status

---

## Experience Compositions

* Reflection Context

---

## Open Component Questions

* Should Verse Preview be expandable to the full verse?
* Should readers be able to create journal entries without an associated verse?
* Should multiple reflections on the same verse be supported?

---

# Accessibility Considerations

* Ensure the verse context is announced before the editor.
* Preserve logical keyboard navigation.
* Support Dynamic Type within both the verse preview and editor.
* Autosave announcements should not interrupt active writing.

---

# Validation Questions

* Does anchoring every entry to a verse create a stronger sense of reflection?
* Is one reflection invitation enough, or should readers be able to hide it?
* Does autosave create sufficient confidence without becoming distracting?
* Do readers understand that their journal is private?

---

# Outputs

This Blueprint defines:

* the canonical Journal experience,
* the transition from reading to reflection,
* reusable reflection components,
* experience-level compositions,
* and validation questions for future prototypes.

---

# North Star

The Journal succeeds when readers feel that they are recording a conversation with the teaching rather than simply writing notes. Every entry should preserve both the wisdom that inspired it and the personal reflection it awakened.
