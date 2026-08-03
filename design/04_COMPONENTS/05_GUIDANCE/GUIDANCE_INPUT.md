# GUIDANCE INPUT

**Version:** 1.0
**Status:** Draft for Design Validation
**Owner:** Design
**Last Updated:** August 2026

---

# Purpose

Guidance Input gives readers a private, low-pressure way to describe a life situation they want to explore through the teachings of the Bhagavad Gita.

It exists to help Antar understand enough context to surface relevant scripture.

Guidance Input is not a general AI chat box.

Its purpose is to begin a path toward wisdom—not an open-ended conversation.

---

# Responsibility

Guidance Input is responsible for:

* capturing a reader’s situation or question,
* making the purpose of the input clear,
* supporting optional clarification,
* preserving the reader’s wording,
* communicating privacy and product boundaries,
* and allowing the reader to submit when ready.

---

# Non-Responsibilities

Guidance Input is not responsible for:

* interpreting the reader’s situation,
* diagnosing emotions,
* generating advice,
* selecting teachings,
* producing AI responses,
* creating journal entries,
* storing conversation history,
* or deciding whether clarification is required.

Those responsibilities belong to the Guidance experience and supporting services.

---

# Usage

Guidance Input appears in the Guidance experience.

It may be used for:

* an initial life situation,
* a focused follow-up question,
* a clarification request,
* or a revised description before teachings are surfaced.

It should not appear as a persistent input across the rest of Antar.

---

# Experience Principles

## Life Context, Not AI Conversation

The component should help readers share enough context for Antar to identify relevant teachings.

It should never imply that the reader is entering an unrestricted AI conversation.

---

## Wisdom Is the Destination

The input is the beginning of the experience.

The destination remains scripture.

The component should not encourage readers to continue typing when sufficient context already exists.

---

## Readers Do Not Need Perfect Words

Readers should feel free to write naturally.

They should not need to:

* use spiritual terminology,
* identify a theme,
* phrase a formal question,
* or explain every detail.

---

## Clarify Only When Necessary

Clarification should reduce harmful assumptions.

It should not extend the interaction unnecessarily.

The experience should ask at most one focused question at a time.

---

## Privacy Is Visible

The experience should communicate that personal situations are treated carefully.

Privacy expectations should be understandable before submission.

The component itself does not define storage or retention policy.

---

## Humility Before Certainty

Guidance Input should not suggest that Antar will provide the correct answer.

It should communicate that Antar will help readers explore relevant teachings.

---

# Anatomy

Guidance Input may contain:

1. Context Label
2. Supporting Description
3. Multiline Input
4. Placeholder
5. Optional Privacy Note
6. Submit Action
7. Optional Cancel or Back Action

```text
────────────────────────────

What is on your mind?

Share only what feels comfortable.
Antar will help you explore relevant teachings.

[ Multiline input                         ]
[                                         ]

Your words remain private.

[ Find Relevant Teachings ]

────────────────────────────
```

The exact supporting language may change depending on the final Guidance model.

---

# Variants

## Initial Situation

Used when the reader first enters Guidance.

Example context label:

> What is on your mind?

Example placeholder:

> Share a situation, question, or feeling you would like to reflect on.

---

## Clarification

Used when additional context is genuinely necessary.

Example:

> Is this mostly about uncertainty, responsibility, or fear of the outcome?

The clarification should remain narrowly connected to the reader’s original words.

---

## Theme Selection

Used if V1 adopts a theme-based Guidance model.

Instead of free-form writing, the component may present a concise set of approved themes.

Examples:

* Fear
* Anger
* Responsibility
* Grief
* Attachment
* Purpose

Theme Selection should remain a variant of the same Guidance entry responsibility rather than becoming a separate Clarifying Question component.

---

## Revision

Allows the reader to revise their situation before teachings are surfaced.

The original wording should remain intact until the reader changes it.

---

# Decision Boundary

The final V1 Guidance model remains unresolved:

* Theme-based Guidance
* Free-text Guidance

This component supports both models without choosing between them.

The product decision must be resolved before implementation.

---

# States

## Empty

No reader input or theme selection exists.

The Submit action remains unavailable or absent.

---

## Focused

The writing surface or selection control has focus.

The state should be clear without becoming visually dominant.

---

## Ready to Submit

Enough input exists for the parent experience to continue.

Guidance Input does not determine semantic sufficiency.

It only reflects the state provided by the parent experience.

---

## Submitting

The reader’s input is being processed.

The component should preserve their words and prevent accidental duplicate submission.

The reader should still understand what was submitted.

---

## Clarification Requested

The parent experience has determined that one additional question is required.

The original situation should remain visible or recoverable so context is not lost.

---

## Error

The reader’s words remain intact.

The experience explains the failure and allows retry without requiring the reader to rewrite anything.

---

## Offline

If Guidance requires connectivity, preserve the reader’s draft locally when allowed by the privacy architecture.

Clearly explain that relevant teachings cannot currently be generated through Guidance.

Offer a path to Library or previously downloaded scripture.

---

## Completed

Relevant teachings have been surfaced.

The input should no longer compete visually with the recommendation.

It may remain available in a quiet, collapsed, or reviewable state.

---

# Interaction Behavior

## Writing

The component should use standard multiline text-editing behavior.

Readers may:

* type,
* delete,
* select,
* copy,
* paste,
* use dictation,
* and edit with platform conventions.

---

## Submission

Submission sends the reader’s current input or theme selection to the parent Guidance experience.

The component does not:

* construct an AI prompt,
* select an AI provider,
* interpret the situation,
* or determine the next teaching.

---

## Clarification

When clarification is requested:

1. Preserve the original input.
2. Present one focused follow-up.
3. Avoid repeating information already provided.
4. Allow the reader to skip or revise where product policy permits.
5. Continue toward relevant teachings as soon as enough context exists.

---

## Cancellation

Leaving Guidance should not imply judgment or failure.

If a draft is retained, the privacy and retention behavior must be explicitly defined elsewhere.

The component should not assume drafts are permanently stored.

---

# Content Guidelines

Guidance copy should be:

* calm,
* clear,
* humble,
* non-diagnostic,
* and free of exaggerated promises.

Prefer:

* What is on your mind?
* Share only what feels comfortable.
* Antar can help you explore relevant teachings.
* Could you tell me a little more about what feels uncertain?
* Find Relevant Teachings

Avoid:

* Ask me anything.
* I can solve this.
* Tell me exactly how you feel.
* Get your answer.
* Let AI guide your life.
* What is wrong?
* Start therapy.
* Submit your problem.

---

# Placeholder Guidance

A placeholder should help readers understand the expected input without suggesting a required format.

Preferred:

> Share a situation, question, or feeling you would like to reflect on.

Alternative:

> Describe what you are facing in your own words.

Avoid:

* Type your prompt.
* Ask AI.
* Enter problem.
* Tell us everything.
* Minimum 50 characters.

Placeholder text must not be the only accessible label.

---

# Clarification Content

Clarification should:

* ask one question at a time,
* use the reader’s own context when appropriate,
* reduce ambiguity,
* avoid emotional diagnosis,
* and remain easy to skip when possible.

Good:

> Is your concern mostly about taking action or accepting the outcome?

Avoid:

> Are you experiencing anxiety caused by a fear of failure?

The second statement assumes a diagnosis and causal interpretation.

---

# Privacy Boundaries

Guidance Input may contain sensitive personal information.

The component should not imply that input is:

* permanently stored,
* used to train models,
* visible to other readers,
* added to Journal automatically,
* or analyzed for emotional profiling.

The product must define:

* retention,
* deletion,
* encryption,
* provider handling,
* and consent

before free-text Guidance is released.

The component may display approved privacy language but does not own privacy policy.

---

# Safety Boundaries

Guidance Input is not a medical, legal, financial, or crisis-support interface.

The parent Guidance experience must own safety detection and response behavior.

The component should not independently:

* classify risk,
* diagnose the reader,
* provide emergency guidance,
* block input based on emotional language,
* or present authoritative intervention.

When the parent experience needs to surface a safety response, the reader’s original words should remain treated with dignity and care.

---

# Accessibility

Guidance Input must:

* expose a clear input label,
* support multiline Dynamic Type,
* support VoiceOver and TalkBack,
* support dictation,
* support external keyboards,
* preserve focus during clarification,
* announce errors clearly,
* and avoid relying on placeholder text as the accessible name.

Preferred accessibility label:

> Describe the situation you would like to explore through the Bhagavad Gita.

For Theme Selection:

> Choose a life theme to explore.

The Submit action should communicate its purpose:

> Find relevant teachings.

Avoid:

> Send.

The accessible label should make the destination clear.

---

# Keyboard Behavior

The component should support:

* multiline entry,
* predictable return-key behavior,
* external keyboard shortcuts where appropriate,
* keyboard dismissal,
* standard selection and editing,
* and visible focus.

The Return key should create a new line unless a clearly supported platform convention provides another accessible submission method.

Submission should use an explicit action rather than making the reader guess whether Return sends the input.

---

# Motion

Guidance Input should use restrained, functional motion.

Appropriate motion includes:

* focus transition,
* expansion from initial to clarification state,
* quiet submission feedback.

Avoid:

* animated AI indicators inside the input,
* pulsing submit actions,
* typing simulations,
* attention-seeking gradients,
* or transitions that make Guidance feel like a chatbot.

The parent experience controls transitions into recommendations.

---

# Design Token Dependencies

Guidance Input should use semantic tokens from:

* Typography System
* Color System
* Spacing System
* Motion System
* Accessibility System
* Iconography System, when necessary

It should not introduce a visually separate “AI interface” language.

Guidance should still feel like Antar.

---

# Engineering Boundaries

Guidance Input may receive:

* input mode,
* text value,
* available themes,
* selected theme,
* supporting copy,
* privacy copy,
* placeholder,
* enabled state,
* submitting state,
* error state,
* change callback,
* submit callback,
* cancel callback,
* accessibility metadata.

It must not:

* construct AI requests,
* send data directly to model providers,
* determine whether input is safe,
* classify emotional state,
* choose teachings,
* store conversation history,
* manage retention,
* or own navigation.

The parent experience and Guidance services own those responsibilities.

---

# Analytics Boundaries

Guidance Input should not collect:

* raw personal input as analytics,
* inferred emotional state,
* psychological categories,
* sensitive topic labels,
* or text-level behavior such as copied phrases.

Acceptable product analytics may include:

* Guidance opened,
* Guidance submitted,
* theme selected,
* recommendation reached,
* Verse opened from Guidance.

Any analytics involving raw reader text require an explicit privacy decision and should be avoided by default.

---

# Good Examples

✓ A reader describes a concern in their own words and receives relevant teachings.

✓ A theme-based V1 lets readers choose “Responsibility” without writing personal details.

✓ One focused clarification is asked because the original situation is ambiguous.

✓ An error preserves the reader’s input.

✓ Guidance Input becomes visually quiet after recommendations appear.

✓ The reader can leave Guidance without being pressured to continue.

---

# Anti-Patterns

Avoid:

✗ A persistent AI-chat composer across Antar.

✗ “Ask me anything” language.

✗ Unlimited conversational clarification.

✗ Diagnosing the reader’s emotional condition.

✗ Automatically saving Guidance input into Journal.

✗ Clearing personal text after an error.

✗ Using reader input for personalization without consent.

✗ Suggesting that AI provides spiritual authority.

✗ Requiring deeply personal disclosure before surfacing scripture.

✗ Treating short input as invalid merely because it lacks detail.

---

# Confirmed Decisions

* Guidance Input begins a path toward scripture.
* It is not a general-purpose AI chat component.
* Readers may use natural language without special terminology.
* Clarification is limited and purposeful.
* One focused clarification is shown at a time.
* Input is preserved during errors and retries.
* The component does not own interpretation, AI requests, or recommendation logic.
* Theme-based and free-text entry remain supported possibilities until V1 scope is resolved.
* Raw personal input is not assumed to be stored or analyzed.
* Guidance must remain visually consistent with Antar rather than adopting chatbot conventions.

---

# Design Hypotheses

The following require validation:

* Whether V1 should use themes, free text, or a hybrid.
* Whether readers understand the difference between Search and Guidance.
* Whether the supporting privacy message increases trust or creates anxiety.
* How much free-text space feels sufficient without resembling a Journal Editor.
* Whether a visible character limit is necessary.
* Whether one clarification is usually enough.
* Whether the input should collapse after recommendations appear.
* Whether readers prefer “Find Relevant Teachings” or a quieter action label.

---

# Validation Questions

* Do readers understand that Guidance leads to scripture rather than AI advice?
* Can readers describe a situation without feeling that they must disclose too much?
* Does the component feel distinct from Search and Journal Editor?
* Is the purpose clear before submission?
* Does clarification feel helpful rather than intrusive?
* Do readers trust how their personal input will be handled?
* Does the component avoid creating expectations of unlimited conversation?
* Can readers recover from an error without losing their words?
* Does the component remain accessible with dictation, large text, and external keyboards?

---

# North Star

Guidance Input succeeds when readers can share only as much as they choose, feel understood without feeling analyzed, and move naturally toward relevant teachings from the Bhagavad Gita rather than deeper into conversation with an AI.
