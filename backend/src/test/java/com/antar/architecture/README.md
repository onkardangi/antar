# Architecture Tests

These ArchUnit tests protect modular-monolith boundaries during implementation.

## Current suite

- `LayerDependencyTest` — layer isolation (`domain`, `api`, `application`, `infrastructure`)
- `ModuleDependencyTest` — modules must not depend on foreign `infrastructure` packages; Platform must not depend on Scripture
- `ModuleStructureTest` — module markers, marker-only modules, Scripture persistence boundaries, Platform foundation probe placement

## First product slice tightening

Scripture introduced real layer packages. Temporary `allowEmptyShould(true)` allowances were removed from layer and module dependency rules so CI fails on real boundary violations.

Remaining marker-only modules stay listed in `ModuleStructureTest` until their vertical slices begin.
