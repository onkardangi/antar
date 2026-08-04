# 02 — Content Pipeline

**Status:** Foundation + Package Format importer v1 (no approved production corpus yet)  
**Owner:** Content / Engineering  
**Last Updated:** August 2026

---

## 1. Purpose

Define the Antar content pipeline that Scripture imports use:

```text
raw → inspect → approve → normalize → validate → editorial sign-off → package → import → publish
```

Immutable content packages under `content/packages/` are the only importer input.

**Still out of scope / not done:**

- approving real Chapter 1 Verses,
- loading a production Sanskrit corpus,
- Translation / Commentary / transliteration persistence,
- mobile changes,
- public Reader import APIs.

---

## 2. Directory roles

| Directory | Role | Mutability |
|-----------|------|------------|
| `content/raw/` | Source downloads | Immutable after checksum |
| `content/registry/` | Approval ledger | Append/update status only |
| `content/licenses/` | License catalog | Additive |
| `content/normalized/` | Deterministic packages | Versioned outputs |
| `content/validation/` | Rules + reports | Rules stable; reports additive |
| `content/checksums/` | SHA-256 manifests | Append; never silently rewrite history |

Policy companions:

- [`01_SCRIPTURE_PROVENANCE.md`](01_SCRIPTURE_PROVENANCE.md)
- [`03_EDITORIAL_POLICY.md`](03_EDITORIAL_POLICY.md)

---

## 3. Pipeline stages

### 3.1 Acquire (raw)

1. Download into `content/raw/<kind>/<source-slug>/`.
2. Keep original filename when practical.
3. Write local provenance `README.md`.
4. Compute SHA-256; append to `content/checksums/raw.sha256`.
5. Add/update `content/registry/sources.json` with status `CANDIDATE`.

### 3.2 Inspect

Document encoding, delimiter/schema, blank/duplicate analysis, chapter/verse counts, edition tradition, Unicode issues, and license display.

Inspection may conclude `REJECTED_FOR_CANONICAL_IMPORT` without further pipeline work.

### 3.3 Approve for normalization

Only if:

- edition matches Antar 47/34 tradition (or an **approved** editorial process has produced a matching package — not an automated silent remap),
- license is recorded,
- defects are catalogued and acceptable for deterministic repair (e.g. float-corrupted labels that do not require verse rewriting).

### 3.4 Normalize

Produce artifacts under `content/normalized/` from the registered raw checksum.

Normalization may:

- parse structured files,
- map columns to Antar fields,
- Unicode-normalize text to the approved form (NFC unless otherwise documented),
- trim unsafe control characters when policy allows,
- repair **deterministic label** defects (e.g. reconstruct identity from an unambiguous marker column),
- emit manifests with content version metadata.

Normalization must **not**:

- edit `content/raw/`,
- invent Translation or Commentary,
- split, join, or renumber Sanskrit verses to force Antar counts,
- drop or fabricate Verse identities,
- treat rejected sources as approved.

### 3.5 Validate

Apply `content/validation/rules.md` and `antar_verse_counts.json`.

Any failure blocks import approval.

### 3.6 Editorial sign-off

Human review per `03_EDITORIAL_POLICY.md`.

### 3.7 Import (backend Package Format importer v1)

Controlled administrative import updates `scripture.verses` Sanskrit and package
provenance from an **APPROVED**, importable Package Format v1 directory only.

```text
Approved Package
  → Validate
  → Dry Run (optional; zero DB writes)
  → Transactional Import
  → Provenance Record
  → Verification
```

Rules:

- Consumes packages only — never raw, editorial, review, or DRAFT inputs.
- Requires `structurallyValid`, `editoriallyValid`, `importable`, and no warnings.
- Successful mutation is one transaction; FAILED audit (if any) is a separate transaction after rollback and **does not** create `content_packages` rows.
- At most one active `APPROVED` package per scripture + Chapter (DB partial unique index).
- Dry run performs validation and counts with **zero** database writes. Dry-run failures still report `dryRun=true` and write nothing.
- Imports never run on normal application startup.
- No public Reader HTTP import endpoint.
- Non-null transliteration is rejected until transliteration persistence exists.
- Real Chapter 1 remains unimported (no approved package).
- Validation / CLI / FAILED audit messages use stable path-free text (no absolute paths or Verse dumps).
- Backend `./mvnw verify` requires Python 3 for the Java/Python Package Format v1 parity gate; runtime import does not spawn Python.

Commands (from `backend/`):

```bash
./mvnw -q exec:java \
  -Dexec.mainClass=com.antar.scripture.infrastructure.importcmd.ScripturePackageImportMain \
  -Dexec.args="--package-path /absolute/path/to/approved-package --dry-run"

./mvnw -q exec:java \
  -Dexec.mainClass=com.antar.scripture.infrastructure.importcmd.ScripturePackageImportMain \
  -Dexec.args="--package-path /absolute/path/to/approved-package"
```

See `backend/src/main/java/com/antar/scripture/README.md` and `content/packages/README.md`.

Until an approved production package is imported, `sanskrit_text` remains NULL by design (`V004` / `V005`).

### 3.8 Publish (future)

Publication status transitions remain a product/backend concern (`DRAFT` → … → `PUBLISHED`) and are out of scope for this foundation slice.

---

## 4. Normalization rules

1. **Input immutability** — raw bytes unchanged; normalize by writing new files.
2. **Reproducibility** — same raw checksum + same rules → same normalized checksum.
3. **Identity fidelity** — output Verse set must equal Antar’s seeded identity set.
4. **No edition coercion** — if source Chapter 1 ≠ 47 or Chapter 13 ≠ 34, stop; do not auto-fix.
5. **UTF-8** — all text artifacts UTF-8 without BOM unless an exception is documented.
6. **Unicode** — store Devanagari/Latin text in NFC unless an approved exception is recorded in the package NOTES.
7. **No placeholders** — never emit engineering placeholder prose as Sanskrit.
8. **Field separation** — Sanskrit, transliteration, translation, and commentary remain distinct.
9. **Attribution** — every non-Sanskrit layer carries source identity.
10. **Deterministic repairs only** — allowed examples: parse fixes, reconstructing `3.10` from a marker when `title` was float-truncated **and** the underlying verse text already corresponds to that identity. Disallowed: merging two ślokas into one Antar verse by algorithm.

---

## 5. Validation rules

Authoritative checklist: `content/validation/rules.md`.

Minimum gate for Scripture packages:

| Gate | Requirement |
|------|-------------|
| Chapters | 18 |
| Total verses | 700 |
| Chapter 1 | 47 |
| Chapter 13 | 34 |
| Contiguous verse numbers | per Chapter |
| Unique canonical references | yes |
| Raw checksum match | yes |
| License recorded | yes |
| Registry status | `APPROVED_FOR_IMPORT` before load |

---

## 6. Versioning policy

### 6.1 Content version

- Align with `content_version` on Scripture tables (monotonic positive integer per record lineage).
- A new approved corpus import that changes Sanskrit text increments content version for affected Verses.
- Package manifests should declare `corpus_id` and `corpus_version` strings for humans and tooling.

### 6.2 Package versioning

```text
content/normalized/scripture/<corpus-id>/v<n>/
```

Never overwrite a prior `v<n>` directory after checksum registration. Publish `v<n+1>` instead.

### 6.3 Registry vs database

| Layer | Version meaning |
|-------|-----------------|
| Registry `updated_at` | Metadata change time |
| Normalized `corpus_version` | Package generation |
| DB `content_version` | Product record version after import |

Do not claim DB versions advanced until import actually runs.

---

## 7. Checksum policy

1. Algorithm: **SHA-256**, lowercase hexadecimal.
2. Manifest format (`shasum -a 256` compatible):

   ```text
   <sha256>  <repo-relative-path>
   ```

3. Every raw artifact used for decisions must appear in `content/checksums/raw.sha256`.
4. Every normalized package root artifact set must appear in `content/checksums/normalized.sha256`.
5. Registry `sha256` must equal the manifest entry for that path.
6. Verification command:

   ```bash
   shasum -a 256 -c content/checksums/raw.sha256
   ```

7. On mismatch: **halt**. Investigate; do not “fix” by editing raw bytes.
8. Replacing a source requires a new path (or clearly versioned filename) and a new manifest line; retain the old line for provenance when the old file remains.

---

## 8. Future translation policy (pipeline view)

Translations are **not** Scripture. Pipeline implications:

1. Separate raw/normalized trees or clearly separated package sections (`translations/`).
2. Require `translation_sources` metadata: translator, edition, language, license.
3. Validate 1:1 Verse mapping to Antar identities.
4. **Do not import unlicensed Translation content** (MVP plan).
5. Attribution must survive into `scripture.translations` / `scripture.translation_sources`.
6. Prefer one approved Translation source for early product surfaces; additional sources are additive.

Detailed editorial rules: `03_EDITORIAL_POLICY.md`.

---

## 9. Future commentary policy (pipeline view)

Commentary is traditional attribution, not Verse text.

1. Separate sources (`commentary_sources`) and passages (`commentary_passages`).
2. No unattributed “traditional commentary.”
3. License and tradition fields mandatory before import approval.
4. Editorial summaries (Understanding) must remain distinguishable from attributed commentary (data model).
5. Commentary import is later-phase relative to Sanskrit + Translation foundation.

---

## 10. Explicit non-goals (current slice)

| Non-goal | Status |
|----------|--------|
| Production Sanskrit corpus import | Not done (no approved package) |
| Translation / Commentary import | Not built |
| Transliteration persistence | Not built (importer rejects non-null transliteration) |
| Public import API | Not built (and not planned for Reader surface) |
| Mobile changes | Not done |
| Startup auto-import | Forbidden |

---

## 11. Implementation status

| Item | Status |
|------|--------|
| Pipeline policy | Documented (this file) |
| `content/` directory roles | Implemented |
| Validation rule stubs | Implemented |
| Checksum manifests | Implemented (raw entry for rejected corpus only) |
| Immutable content packages | Implemented (`content/packages/`) |
| Package Format importer v1 | Implemented (backend administrative CLI + tests) |
| Normalization tooling | **Deferred** |
| Approved Chapter 1 package | **Not present** |
| Production PostgreSQL Sanskrit load | **Not performed** |
