# Platform

## Purpose

Contains shared infrastructure concerns that are not business domains: observability, configuration, and technical adapters.

## Owned concepts

- Logging, metrics, and tracing foundations
- Feature flags
- Provider client adapters
- Rate limiting and request correlation
- Cross-cutting configuration

## Expected dependencies

- Shared (small primitives only)

Platform must not absorb domain logic from Identity, Scripture, Reflection, or Saar.

## Current status

Foundation infrastructure only:

- Temporary operational endpoint `GET /api/internal/foundation/status`
  - profile-gated to `local` and `test`
  - not a product API
  - intended only for initial mobile-to-backend connectivity validation
- No product APIs, entities, or tables owned by Platform yet
