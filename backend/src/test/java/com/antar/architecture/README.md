# Architecture Tests

These ArchUnit tests protect modular-monolith boundaries during implementation.

## Current suite

- `LayerDependencyTest` — future layer isolation (`domain`, `api`, `infrastructure`)
- `ModuleDependencyTest` — modules must not depend on foreign `infrastructure` packages
- `ModuleStructureTest` — non-vacuous foundation checks for module markers and Platform placement

## Temporary empty-package allowances

Several layer and foreign-infrastructure rules currently use:

```text
allowEmptyShould(true)
```

That is intentional for the repository foundation because most modules still contain only marker classes and README files. Empty-package success does **not** prove layer isolation.

When the first product slice introduces real layer packages:

1. Remove or narrow `allowEmptyShould(true)` in `LayerDependencyTest` and `ModuleDependencyTest`.
2. Expand `ModuleStructureTest` for the new package layout.
3. Keep CI green only when the tightened rules actually evaluate production classes.

## Infrastructure tests

Docker-backed Spring tests live under Surefire (`*Test`) and share JVM-scoped Testcontainers.
See `backend/README.md` for Docker requirements and the local opt-out property.
