# ADR-011 — Antar V1 Is Mobile-First

## Status

Accepted

## Context

Antar’s primary experiences are contemplative reading, quick reflection, deeper journaling, reading continuity, Journey revisiting, and optional conversation with Saar.

These experiences are intended to be available during personal reading moments and benefit from native mobile capabilities such as secure storage, notifications if later approved, platform accessibility, and local draft preservation.

Supporting both web and mobile during the first implementation phase would divide engineering effort and introduce multiple presentation and state-management surfaces before the core experience has been validated in production.

## Decision

Antar V1 will be implemented as a mobile-first application using:

```text
React Native
TypeScript
Expo
```