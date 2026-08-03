# REFLECTION INVITATION

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Reflection Invitation creates a quiet moment between understanding a teaching and moving forward.

It invites the reader to notice what the teaching awakened within them without requiring a written response.

The component succeeds even when the reader chooses not to write.

Its responsibility is to create space for reflection—not to collect an answer.

---

# Responsibility

Reflection Invitation is responsible for:

* creating a natural pause after reading,
* inviting personal consideration,
* reducing the pressure associated with a blank journal,
* connecting reflection to the teaching,
* and making non-participation feel completely acceptable.

---

# Non-Responsibilities

Reflection Invitation is not responsible for:

* capturing writing,
* opening or managing the Journal Editor,
* saving reflection,
* evaluating whether the reader reflected,
* generating psychological conclusions,
* presenting Saar,
* selecting the next destination,
* or measuring engagement.

Those responsibilities belong to the parent experience, Reflection components, or supporting services.

---

# Usage

Reflection Invitation may appear in:

* Verse
* Journal
* Guidance
* Journey revisit moments
* future guided reading experiences

It should appear only after the reader has encountered the relevant teaching or reflection context.

It should not appear before scripture or translation.

---

# Experience Principles

## Invite, Never Require

The reader should always be free to:

* pause,
* write,
* continue,
* or return later.

The component must never imply that reflection is required to complete the experience.

---

## Questions Are Optional

A Reflection Invitation may use a question, but it does not need to.

Statements may create a gentler pause than direct questions.

Examples:

> Notice what stayed with you.

> Take a moment before continuing.

> You do not have to write anything.

Questions should be used only when they genuinely deepen reflection.

---

## Silence Is Valid

The absence of a response is not failure.

The component should not display:

* incomplete states,
* reminders,
* progress indicators,
* validation messages,
* or completion feedback.

---

## The Teaching Remains the Source

Reflection Invitations should emerge from or remain compatible with the teaching that precedes them.

They should never introduce an unrelated journaling topic.

---

## Predictability Before Personalization

Version 1 should use carefully reviewed invitation content.

The component should not depend on real-time AI generation.

A smaller trusted set is preferable to endless variation.

---

# Content Types

Reflection Invitation supports three content types.

## Quiet Invitation

Creates a pause without asking for a response.

Examples:

> Take a moment before continuing.

> Sit with this teaching for a while.

---

## Noticing Invitation

Encourages the reader to observe their response.

Examples:

> Notice what stayed with you.

> Notice where this teaching meets your life.

---

## Reflective Question

Asks one concise, open-ended question.

Examples:

> Did anything in this teaching surprise you?

> Where do you recognize this in your own life?

Questions should not suggest a correct answer.

---

# Content Model

The component may receive:

* invitation identifier,
* invitation text,
* invitation type,
* associated verse or teaching identifier,
* optional action configuration,
* accessibility label when needed.

Invitation content should come from a trusted, reviewed source.

---

# Anatomy

Reflection Invitation contains:

1. Invitation text
2. Optional reflection action

```text
────────────────────────────

Notice what stayed with you.

[ Reflect ]

────────────────────────────
```

The action is optional.

When the Journal Editor is already visible, the invitation should not repeat an additional reflection action.

---

# Variants

## Standalone

Displays only the invitation.

Used when the experience already provides a visible editor or natural continuation beneath it.

```text
Notice what stayed with you.
```

---

## With Reflection Action

Displays the invitation with one quiet action that opens or reveals the Journal Editor.

```text
Did anything in this teaching stay with you?

Reflect
```

The action must remain secondary to the invitation itself.

---

## Compact

Used in limited contexts such as Journey revisits or Guidance follow-through.

The compact variant should retain the full meaning of the invitation.

It should not truncate reflective language into vague labels.

---

# States

## Default

The invitation is visible and available.

---

## Pressed

Applies only when a reflection action is present.

Provide immediate, restrained feedback.

---

## Editor Open

When the reader chooses to write, the parent experience reveals or navigates to the Journal Editor.

The invitation may remain visible as context or become quieter.

It should not disappear abruptly if doing so would remove context.

---

## Dismissed

Version 1 should generally omit a dedicated dismiss control.

Readers dismiss the invitation naturally by continuing without interacting.

If an experience introduces explicit dismissal later, that preference should belong to the parent experience rather than the component.

---

## Content Unavailable

If a verse-specific invitation is unavailable, use a trusted general invitation or omit the component.

Do not generate an unreviewed replacement dynamically.

---

# Interaction Behavior

When the invitation has no action, it is read-only.

When an action is present, selecting it should:

1. preserve the current teaching context,
2. open or reveal the Journal Editor,
3. place focus appropriately,
4. avoid requiring additional confirmation.

The component should not decide:

* which editor mode opens,
* whether an existing reflection is restored,
* how writing is saved,
* or what happens after writing.

---

# Content Guidelines

Invitation copy should be:

* concise,
* open-ended,
* emotionally neutral,
* non-judgmental,
* and easy to understand.

Prefer:

* Notice what stayed with you.
* Take a moment before continuing.
* Where do you recognize this in your own life?
* Did anything challenge the way you see things?

Avoid:

* Write your reflection now.
* What did you learn?
* Complete today’s reflection.
* You should think about how this applies to you.
* Do not leave before writing.
* Great job reflecting!

The copy should not praise, score, pressure, diagnose, or direct the reader toward a predetermined conclusion.

---

# Invitation Library

Version 1 should use a limited set of reviewed invitations.

The library may include:

* universal invitations,
* invitations associated with a verse,
* invitations associated with a chapter theme,
* revisit invitations for Journey.

Every invitation should be reviewed for:

* theological neutrality,
* emotional safety,
* clarity,
* localization,
* and compatibility with Antar’s Product Principles.

The invitation library should not become a content feed.

---

# AI Boundaries

Reflection Invitation does not require AI.

Version 1 should not generate invitation text dynamically through AI.

Future AI support may be explored only if it can:

* remain faithful to the teaching,
* avoid emotional inference,
* preserve consistency,
* and pass content review.

AI must never generate a question based on private journal content without explicit product, privacy, and user-consent decisions.

---

# Accessibility

Reflection Invitation must:

* appear after the related teaching in semantic reading order,
* expose invitation text as semantic text,
* clearly identify an optional action when present,
* support Dynamic Type,
* avoid fixed-height containers,
* preserve focus when opening the Journal Editor,
* and avoid announcing the invitation as a required form field.

For an action, prefer an accessibility label such as:

> Reflect on this teaching.

Avoid:

> Complete reflection.

The action must have a sufficient touch target even when visually quiet.

---

# Typography

Reflection Invitation should use the Reflection typography role.

It should feel:

* warm,
* personal,
* and visually quieter than scripture and translation.

Questions and statements should generally use the same style.

Punctuation and layout should not artificially dramatize the invitation.

Avoid:

* oversized quotation styling,
* decorative script fonts,
* excessive italics,
* bold motivational language,
* or ornamental quotation marks.

---

# Spacing

The component owns spacing between:

* invitation text,
* and its optional action.

The parent composition owns spacing:

* before the invitation,
* after the invitation,
* between the invitation and Journal Editor,
* and between reflection content and Saar.

The component should have enough breathing room to create a pause without becoming visually detached from the teaching.

---

# Color

Use standard reflective text and action colors from the Color System.

The component should not rely on:

* warning colors,
* success colors,
* completion states,
* or bright accents.

Reflection is not an alert or achievement.

---

# Motion

Reflection Invitation requires little motion.

When revealing the Journal Editor, motion may gently preserve continuity between invitation and writing.

Avoid:

* attention-seeking entrance effects,
* pulsing actions,
* bouncing indicators,
* animated typing,
* or motion that implies urgency.

The component must respect Reduced Motion preferences through the parent transition.

---

# Design Token Dependencies

Reflection Invitation should use semantic tokens from:

* Typography System
* Color System
* Spacing System
* Motion System
* Accessibility System

It should not introduce custom visual tokens.

---

# Engineering Boundaries

Reflection Invitation may receive:

* invitation content,
* invitation type,
* associated teaching identifier,
* optional action label,
* optional action callback,
* display variant,
* accessibility metadata.

It should not:

* generate invitation content,
* query journal history,
* infer emotional state,
* determine whether the reader should reflect,
* instantiate persistence,
* manage editor state,
* or record completion.

The parent experience owns action behavior and data.

---

# Analytics Boundaries

Reflection Invitation should not record:

* whether the reader paused,
* whether they thought about the invitation,
* emotional responses,
* completion,
* or reflection quality.

If product analytics record action selection, they should measure only whether the optional editor entry point was used.

The absence of interaction must not be treated as failure.

---

# Good Examples

✓ A Verse experience displays “Notice what stayed with you” after Translation Block.

✓ A reader ignores the invitation and continues without receiving a warning or reminder.

✓ Selecting “Reflect” opens the Journal Editor with the verse context preserved.

✓ Journal displays a verse-aware invitation above an empty editor.

✓ Journey uses a compact invitation to reconsider an earlier reflection.

---

# Anti-Patterns

Avoid:

✗ Requiring a response before Continue Reading becomes available.

✗ Displaying a completion checkbox.

✗ Using AI to generate emotionally personalized questions in V1.

✗ Praising readers for writing.

✗ Repeatedly reminding readers to reflect.

✗ Asking multiple questions at once.

✗ Evaluating or summarizing the reader’s response.

✗ Treating the invitation as a required form label.

✗ Showing an empty text field without any reflective context.

---

# Confirmed Decisions

* The canonical name is Reflection Invitation.
* Reflection Invitation appears after the teaching.
* It is present even when writing remains optional.
* Silence and non-participation are valid outcomes.
* Version 1 uses reviewed invitation content rather than generated AI content.
* The component does not own the Journal Editor or saving.
* A maximum of one invitation is shown at a time.
* The component never blocks continuation.

---

# Design Hypotheses

The following require validation:

* Whether statement-based invitations feel gentler than questions.
* Whether the optional Reflect action is necessary when the editor is not visible.
* Whether the invitation should remain visible after writing begins.
* How many universal invitations are required for V1.
* When verse-aware invitations provide enough additional value to justify their content cost.
* Whether readers understand that they may continue without responding.

---

# Validation Questions

* Does the invitation create a genuine pause without creating obligation?
* Do readers understand that writing is optional?
* Are statement-based invitations more comfortable than direct questions?
* Does the component reduce blank-page anxiety?
* Does one invitation provide enough guidance without becoming repetitive?
* Does the transition into Journal Editor preserve the teaching context?
* Can readers ignore the component without feeling that they skipped something required?

---

# North Star

Reflection Invitation succeeds when it creates enough quiet for the reader to notice their own response to the teaching—even if they choose not to write a single word.
