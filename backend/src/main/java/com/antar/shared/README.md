# Shared

## Purpose

Holds intentionally small cross-module primitives that do not belong to a single business domain.

## Owned concepts

- Small shared value types and utilities used by multiple modules
- Kernel primitives that avoid domain ownership

## Expected dependencies

None on business modules. Shared must remain thin and must not become a dumping ground for domain logic.

## Current status

Module marker only. No product features implemented yet.
