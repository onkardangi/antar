# Import Report — `bhagavad-gita-chapter-01-v1`

**Status:** Successful controlled administrative import
**Report timestamp (UTC):** 2026-08-04T23:11:24Z
**Operator context:** Local Compose PostgreSQL/Redis + Spring `local` profile importer CLI

---

## Package

| Field | Value |
|-------|-------|
| Package ID | `bhagavad-gita-chapter-01-v1` |
| Package checksum | `d15ab8003a8a61db446e6dfb5f9da7233e631df04fb316010a378450c914e06a` |
| Package path | `content/packages/bhagavad-gita-chapter-01-v1` |
| Package status (manifest) | `APPROVED` |
| Chapter | 1 |
| Content version | 1 |
| Record count | 47 (`1.1`–`1.47`) |
| Transliteration | `null` on every record |

---

## Package validation result

Command:

```bash
python3 content/packages/tools/validate_package.py \
  content/packages/bhagavad-gita-chapter-01-v1 --json
```

Result:

| Check | Result |
|-------|--------|
| `structurallyValid` | `true` |
| `editoriallyValid` | `true` |
| `importable` | `true` |
| `warnings` | `[]` |
| `errors` | `[]` |
| Package checksum match | yes |
| `recordCount` | 47 |
| Canonical range | `1.1`–`1.47` |
| `packageStatus` | `APPROVED` |
| Non-null transliteration count | 0 |
| `SHA256SUMS` file verification | OK |

Independent combined digest recomputation matched the declared `packageChecksum`.

---

## Environment summary (no secrets)

| Item | Value |
|------|-------|
| Active Spring profile | `local` |
| Database host | `localhost` |
| Database port (host publish) | `5435` → container `5432` |
| Database name | `antar` |
| Database user | `antar` (password omitted) |
| Compose services | `antar-postgres` (`pgvector/pgvector:pg16`), `antar-redis` (`redis:7-alpine`) |
| PostgreSQL server version | 16.14 |
| Flyway library | `org.flywaydb:flyway-core:11.14.1` |
| Spring Boot | 4.0.7 |
| Java | 21.0.10 |
| Importer entry point | `com.antar.scripture.infrastructure.importcmd.ScripturePackageImportMain` |

### Pre-import database state

| Item | Value |
|------|-------|
| Current schema version | `005` (before importer startup) |
| `V006` applied | **false** before first importer run |
| Chapter 1 Verse identities | 47 |
| Chapter 1 verses with non-null Sanskrit | 0 |
| `content_packages` rows | table absent (pre-`V006`) |
| `content_package_imports` rows | table absent (pre-`V006`) |

Note: Flyway applied `V006__create_scripture_content_packages.sql` during dry-run application startup (schema only). That migration created empty provenance tables; it did not write package or Verse content.

---

## Dry-run result

Command (from `backend/`):

```bash
POSTGRES_PORT=5435 SPRING_PROFILES_ACTIVE=local ./mvnw -q exec:java \
  -Dexec.mainClass=com.antar.scripture.infrastructure.importcmd.ScripturePackageImportMain \
  -Dexec.args="--package-path ../content/packages/bhagavad-gita-chapter-01-v1 --dry-run --spring.profiles.active=local"
```

| Field | Value |
|-------|-------|
| Wall time (local) | 2026-08-04T17:59:31-05:00 |
| `importStatus` | `IMPORTED` (planned/validated success) |
| `dryRun` | `true` |
| `recordsRead` | 47 |
| `recordsValidated` | 47 |
| `recordsUpdated` | 47 |
| `recordsUnchanged` | 0 |
| `recordsRejected` | 0 |
| `packageId` | `bhagavad-gita-chapter-01-v1` |
| `packageChecksum` prefix | `d15ab8003a8a` |
| Failure code | none |
| Process exit | 0 |
| `structurallyValid` / `editoriallyValid` / `importable` | true / true / true |
| `warningCount` | 0 |

### Dry-run zero-write verification

After dry-run:

| Check | Result |
|-------|--------|
| `content_packages` row count | 0 |
| `content_package_imports` row count | 0 |
| Chapter 1 non-null Sanskrit | 0 |
| Any Verse `source_package_id` | 0 |
| Schema after dry-run startup | `006` applied (empty tables only) |

---

## Real import result

Command (from `backend/`):

```bash
POSTGRES_PORT=5435 SPRING_PROFILES_ACTIVE=local ./mvnw -q exec:java \
  -Dexec.mainClass=com.antar.scripture.infrastructure.importcmd.ScripturePackageImportMain \
  -Dexec.args="--package-path ../content/packages/bhagavad-gita-chapter-01-v1 --spring.profiles.active=local"
```

| Field | Value |
|-------|-------|
| Wall time (local) | 2026-08-04T17:59:44-05:00 |
| Completed at (DB UTC) | 2026-08-04T22:59:44.740856Z |
| `importStatus` | `IMPORTED` |
| `dryRun` | `false` |
| `recordsRead` | 47 |
| `recordsValidated` | 47 |
| `recordsUpdated` | 47 |
| `recordsUnchanged` | 0 |
| `recordsRejected` | 0 |
| `packageId` | `bhagavad-gita-chapter-01-v1` |
| Package checksum | `d15ab8003a8a61db446e6dfb5f9da7233e631df04fb316010a378450c914e06a` |
| Failure code | none |
| Duration | 311 ms |
| Process exit | 0 |

---

## Idempotency result

Second real import of the same package:

| Observation | Result |
|-------------|--------|
| Use-case log counts | `updated=0`, `unchanged=47`, `status=IMPORTED`, `failureCode=null` |
| CLI stdout summary | Re-emitted the original successful execution summary (`recordsUpdated=47`, `recordsUnchanged=0`) rather than the new zero-update plan |
| Process exit | 0 |
| `content_packages` rows | still 1 |
| Successful `IMPORTED` execution rows | still 1 |
| `FAILED` executions | 0 |
| Package status | remains `APPROVED` |
| Verse lineage fingerprint (id/text/version/package/checksum/`updated_at`) | unchanged |

Documented behavior: on an already-imported identical package, the importer succeeds idempotently without rewriting Verses or inserting a second successful audit row; the CLI summary may replay the original `IMPORTED` result while application logs show the no-op mutation counts.

---

## Database verification counts

### Chapter 1 Verses

| Check | Result |
|-------|--------|
| Verse identities | 47 |
| Non-null Sanskrit | 47 |
| Blank Sanskrit | 0 |
| Distinct canonical references | 47 |
| Missing/unexpected refs vs `1.1`–`1.47` | 0 / 0 |
| `content_version = 1` | 47 / 47 |
| `source_package_id = bhagavad-gita-chapter-01-v1` | 47 / 47 |
| `source_package_checksum` matches package | 47 / 47 |

### Scope safety

| Check | Result |
|-------|--------|
| Chapters 2–18 non-null Sanskrit | 0 |
| Other Chapter package rows | 0 |
| Total `content_packages` rows | 1 |
| Translation / Commentary / transliteration tables | not present (none added) |

### Package provenance row

| Field | Value |
|-------|-------|
| `package_id` | `bhagavad-gita-chapter-01-v1` |
| `package_status` | `APPROVED` |
| `chapter_number` | 1 |
| `content_version` | 1 |
| `package_checksum` | `d15ab8003a8a61db446e6dfb5f9da7233e631df04fb316010a378450c914e06a` |
| `source_registry_references` count | 50 (populated) |
| `first_imported_at` | 2026-08-04T22:59:44.740856Z |
| `last_verified_at` | 2026-08-04T22:59:44.740856Z |

Note: `scripture.content_packages` has no `record_count` column. Record count is evidenced by the package manifest (`recordCount=47`), Verse row counts (47), and the import execution `records_read=47`.

### Import execution summary

| Field | Value |
|-------|-------|
| Successful `IMPORTED` rows for package | 1 |
| `FAILED` rows for package | 0 |
| `records_read` / `validated` / `updated` / `unchanged` / `rejected` | 47 / 47 / 47 / 0 / 0 |
| `failure_code` | null |

---

## API smoke-test result

Backend restarted after import with profile `local`, `POSTGRES_PORT=5435`, `server.port=8082`.

| Check | Result |
|-------|--------|
| `GET /api/v1/scripture/chapters` | HTTP 200 |
| `GET /api/v1/scripture/chapters/{chapterId}/verses` (Chapter 1) | HTTP 200 |
| Item count | 47 |
| Response keys per item | `id`, `verseNumber`, `canonicalReference`, `previewText` |
| Sanskrit exposed in listing | no |
| `previewText` | `Verse preview unavailable` for all items |
| Canonical refs | exactly `1.1`–`1.47` |
| `GET /api/v1/scripture/verses/by-reference/1.1` | HTTP 404 (Verse-detail API not implemented in this slice) |
| Direct DB spot-check for `1.1` | non-null Sanskrit length present; lineage package/checksum/version correct |

---

## Known limitations

- Transliteration remains absent (`null` in package; no transliteration persistence).
- Translation remains absent.
- Only Chapter 1 was imported; Chapters 2–18 Sanskrit remain null.
- Chapter Verse listing still returns identity + placeholder `previewText` only; full Verse Reader content APIs are not implemented.
- Documentation elsewhere that still says “not imported” may lag this report until separately updated.

---

## Source / editorial / package immutability confirmation

During this import task:

- No backend source files were modified.
- No mobile source files were modified.
- No editorial workspace files were modified by the importer.
- The package directory was not rebuilt; `SHA256SUMS` verification remained OK and `packageChecksum` remained unchanged.
- The only documentation file created for this task is this import report.

---

## Post-import schema

| Item | Value |
|------|-------|
| Current Flyway schema version | `006` |
| `V006` applied | true |

---

## Backend verification suite

```bash
cd backend && ./mvnw --batch-mode clean verify
```

| Result | Value |
|--------|-------|
| Build | `BUILD SUCCESS` |
| Tests | 133 run, 0 failures, 0 errors, 0 skipped |
| Finished at (local) | 2026-08-04T18:12:06-05:00 |

Importer and existing API suites remained green after the local import. No migrations were modified.
