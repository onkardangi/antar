# `content/normalized/`

Deterministic, reviewable artifacts produced from **approved** raw sources.

## Purpose

Hold import-ready content packages after:

1. source approval,
2. provenance recording,
3. deterministic normalization,
4. validation against Antar’s Chapter/Verse identity model,
5. editorial sign-off.

## Rules

- Create normalized output **only** for sources with registry status `APPROVED_FOR_NORMALIZATION` or later.
- Normalization must be reproducible from the registered raw checksum.
- Do not place rejected-source repairs here as if they were approved Antar Scripture.
- Do not invent missing verses or merge/split Sanskrit to force Antar numbering.

## Current contents

Empty. No normalized Scripture corpus exists yet.

## Expected future layout (not created yet)

```text
normalized/
└── scripture/
    └── <corpus-id>/
        ├── manifest.json
        ├── chapters.json
        ├── verses.json
        └── NOTES.md
```
