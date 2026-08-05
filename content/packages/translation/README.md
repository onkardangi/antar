# Antar Translation Packages

Immutable release artifacts for approved Translation content.

Independent from Scripture packages. The Translation importer consumes **packages only**.

## Layout

```text
content/packages/translation/
├── README.md
├── schema/
├── tools/
└── fixtures/
    └── fixture-translation-en-chapter-01-v1/   # synthetic APPROVED fixture
```

Each package directory:

```text
<package-id>/
├── manifest.json
├── translations.jsonl
├── provenance.json
└── SHA256SUMS
```

## Rules

1. Packages are immutable release artifacts.
2. Only `APPROVED` packages may be imported.
3. Synthetic fixture text only in this foundation (`FIXTURE_TRANSLATION_VERSE_*`).
4. Never import a real translation corpus in this phase.
5. No commentary or notes fields.

## Checksums

- Algorithm: SHA-256, lowercase hex.
- `SHA256SUMS` lists `manifest.json`, `provenance.json`, `translations.jsonl`.
- Combined `packageChecksum` = SHA-256(bytes(translations.jsonl) || bytes(provenance.json)).

## Validate

```bash
python3 content/packages/translation/tools/validate_package.py \
  content/packages/translation/fixtures/fixture-translation-en-chapter-01-v1

python3 -m unittest discover content/packages/translation/tools/tests
```

## Package builder

Foundation packages are assembled as immutable directories matching the layout
above. Test packages are produced by
`SyntheticTranslationPackageFixtureBuilder` (Java). A production editorial
`build_package.py` for Translation is deferred; do not import editorial
workspaces directly.

Backend import commands: `backend/src/main/java/com/antar/translation/README.md`.
