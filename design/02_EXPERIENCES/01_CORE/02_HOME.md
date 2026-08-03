# HOME EXPERIENCE

**Version:** 1.0
**Status:** Approved for Design Exploration
**Owner:** Product & Design
**Last Updated:** August 2026

---

# Vision

Home is the doorway into Antar.

It welcomes readers back, helps them regain context, and gently guides them toward the next meaningful step in their journey.

It is not a dashboard.

It is the beginning of today's reading experience.

---

# Purpose

The purpose of Home is to remove uncertainty.

Readers should never wonder:

> "What should I do next?"

Home should quietly answer that question within a few seconds.

---

# Experience Promise

Home promises:

> **"I will gently guide you toward your next meaningful step."**

It does not attempt to summarize Antar.

It simply helps readers begin.

---

# Primary User Question

> **Where should I begin today?**

Every element on Home should help answer this question.

If something does not help readers begin, it likely does not belong on Home.

---

# Why This Exists

Opening Antar should feel calming rather than demanding.

Many products greet users with dashboards, notifications, metrics, or decisions.

Antar intentionally avoids this.

Readers come seeking clarity, not another inbox.

Home exists to reduce decision fatigue and create a smooth transition into reading.

---

# Experience Philosophy

Home should feel like opening a book where someone has already placed a bookmark for you.

The experience should feel welcoming, calm, and intentional.

Rather than presenting everything Antar can do, Home should present what matters most right now.

The fewer decisions readers need to make before reading, the better.

---

# User Journey

The intended journey through Home is:

Launch Antar

↓

Feel Welcome

↓

Regain Context

↓

Recognize the Next Step

↓

Begin Reading

Home succeeds when readers naturally continue into the reading experience without hesitation.

---

# Experience Goals

Home should:

* welcome readers warmly,
* restore continuity,
* reduce decision-making,
* encourage consistent reading,
* and prepare readers for the Verse experience.

It should never overwhelm users with options.

---

# Emotional Arc

The intended emotional progression is:

Arrival

↓

Comfort

↓

Orientation

↓

Confidence

↓

Beginning

Readers should feel ready to continue—not pressured to perform.

---

# Experience Responsibilities

Home is responsible for:

* welcoming readers,
* remembering progress,
* suggesting the next meaningful step,
* providing gentle orientation,
* and offering access to exploration.

---

# Non-Responsibilities

Home is not responsible for:

* analytics,
* productivity dashboards,
* achievement tracking,
* notifications,
* social updates,
* AI recommendations,
* trending content,
* or teaching scripture.

Those responsibilities belong elsewhere—or not at all.

---

# Information Architecture

The Home experience should prioritize information in this order:

1. Greeting
2. Today's Invitation
3. Explore Library

Today's Invitation is the single primary action. Continuity, beginning, resumed reflection, and curated teaching are presented as contextual states of Today's Invitation rather than as separate sections.

Everything else should remain secondary.

---

# Greeting Philosophy

The greeting establishes emotional tone.

It should feel warm without becoming overly familiar.

Examples include:

* Good morning.
* Welcome back.
* Ready to continue?
* Your reading is waiting whenever you're ready.

Greeting copy should never:

* create guilt,
* imply failure,
* pressure readers,
* or reward streaks.

The product should always meet readers with acceptance.

---

# Continue Reading

Continue Reading is the reusable navigation component used within Today's Invitation when the reader has an unfinished chapter or verse.

When continuity exists, Today's Invitation prioritizes helping readers resume.

Readers should not need to remember where they left off.

Continuity is an act of respect.

Continuity is one state of Today's Invitation, not a separate competing section.

---

# Today's Invitation

Today's Invitation is the single primary action on Home. It presents an already-selected next step; product and supporting services choose the destination.

Today's Invitation is not a "Verse of the Day."

Instead, it gently presents a meaningful next step.

Examples:

* Continue Chapter 2.
* Begin Chapter 5.
* Reflect on yesterday's reading.
* Explore a teaching about courage.

Invitations should remain contextual rather than random.

---

# Exploration

Home should provide a quiet path to discovery through the Library.

Exploration should remain available without competing with the primary reading path.

Reading remains the preferred action.

Browsing remains optional.

---

# Returning Readers

Home should acknowledge continuity.

The experience should remember where readers left off and gently reconnect them with their journey.

Returning readers should feel recognized without feeling monitored.

The product remembers progress.

It does not keep score.

---

# First-Time Readers

First-time readers require additional guidance.

Home should introduce Antar with clarity rather than feature lists.

The experience should answer:

* What is Antar?
* Where should I begin?
* What happens next?

The first experience should feel welcoming rather than instructional.

---

# Visual Hierarchy

Visual attention should naturally follow this order:

Greeting

↓

Today's Invitation

↓

Explore Library

↓

Supporting Navigation

Everything else should remain visually secondary.

---

# Interaction Principles

Readers should reach their next reading experience with minimal effort.

Interactions should remain:

* predictable,
* quiet,
* and purposeful.

Scrolling should be minimal.

The primary action should remain visible without overwhelming the experience.

---

# Motion

Motion should reinforce arrival.

Transitions into Home should feel welcoming.

Transitions out of Home should feel like naturally opening the next page.

Animations should remain subtle and never delay reading.

---

# Accessibility

Home should remain fully usable with:

* Dynamic Type,
* VoiceOver,
* TalkBack,
* reduced motion,
* high contrast,
* keyboard navigation where applicable,
* and offline mode.

Greeting copy and primary actions should remain clear regardless of accessibility preferences.

---

# Engineering Responsibilities

Home should:

* restore reading progress,
* determine the next recommended action,
* support offline continuation,
* load quickly,
* gracefully handle missing data,
* and remain independent from AI availability.

Home should never become tightly coupled to recommendation systems.

---

# Analytics Philosophy

Analytics should improve the experience rather than maximize engagement.

Appropriate measurements include:

* Continue Reading usage,
* Today's Invitation acceptance,
* offline starts,
* accessibility preference usage.

Avoid measuring:

* time spent on Home,
* repeated refreshes,
* unnecessary engagement loops.

Success is measured by helping readers begin—not by keeping them on Home.

---

# Success Criteria

The Home experience succeeds if:

* readers immediately know what to do next,
* the experience feels welcoming,
* progress feels continuous,
* decisions feel effortless,
* readers naturally move into Verse or Library,
* and Home never feels overwhelming.

---

# Failure Modes

The Home experience fails if:

* it becomes a dashboard,
* readers must decide among too many options,
* metrics become more prominent than reading,
* AI becomes the primary recommendation,
* notifications dominate the experience,
* or exploration replaces meaningful continuation.

---

# Anti-Patterns

Avoid:

* achievement widgets,
* streak counters,
* productivity metrics,
* trending verses,
* recommendation feeds,
* excessive personalization,
* promotional banners,
* pop-ups,
* advertisements,
* or feature announcements.

Home should remain a calm beginning—not an attention marketplace.

---

# Future Evolution

Future versions may explore:

* seasonal greetings,
* adaptive invitations,
* Journey milestones,
* contextual reading suggestions,
* richer offline experiences,
* and personalized reading preferences.

Future additions should never compromise the simplicity of beginning.

---

# Design Decisions

### Today's Invitation is the single primary action.

**Reason**

Continuity, beginning, resumed reflection, and curated teaching are presented as states of one invitation rather than competing sections, so readers face one clear next step.

---

### Today's Invitation is contextual.

**Reason**

Meaningful guidance is more valuable than random recommendations.

---

### Greeting avoids guilt.

**Reason**

Readers should always feel welcomed back regardless of how long they have been away.

---

### Exploration remains secondary.

**Reason**

The primary purpose of Home is helping readers begin, not encouraging browsing.

---

# Open Questions

The following require validation through design and user testing:

* Should Journey Highlights appear on Home in Version 1?
* Should readers be able to dismiss Today's Invitation?
* How much personalization is helpful before it feels intrusive?
* How should Home adapt for tablets?
* Should morning and evening greetings differ visually?

---

# North Star

When readers open Antar, they should immediately feel welcomed, regain their place, and know exactly how to continue their journey.

Home should quietly remove uncertainty so that attention can return to what matters most—the wisdom waiting to be read.
