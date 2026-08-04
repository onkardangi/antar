# IIT Kanpur / Gita Supersite — Verse 1.1 verification evidence

## Role

`SECONDARY_VERIFICATION_REFERENCE` only.

IIT Kanpur Gita Supersite is used to **verify** Wikisource Verse 1.1 root Sanskrit. It is **not** Antar’s import corpus.

## URLs

| Kind | URL |
|------|-----|
| Requested page URL | https://www.gitasupersite.iitk.ac.in/srimad?choose=1&field_chapter_value=1&field_nsutra_value=1&language=dv&show_mool=1 |
| Retrieval URL (embedded mool HTML) | https://old.gitasupersite.in/srimad?choose=1&language=dv&field_chapter_value=1&field_nsutra_value=1&show_mool=1 |

The modern SPA at `gitasupersite.iitk.ac.in` / `www.gitasupersite.in` does not embed Verse text without authenticated API access. Minimal mool evidence was taken from the legacy Drupal page that still exposes `मूल श्लोकः`.

## Status

`VERIFICATION_ONLY` / `VERIFICATION_ONLY_NOT_APPROVED_FOR_REDISTRIBUTION`

## License

| Layer | Status |
|-------|--------|
| Underlying ancient Sanskrit work | Public domain (ancient work) |
| IIT / Gita Supersite digital transcription | **LICENSE_UNCONFIRMED_FOR_REDISTRIBUTION** |
| Redistribution of this site’s HTML/API corpus | Not established by this task |

Do not claim redistribution rights that are not explicitly documented. IIT Kanpur does **not** endorse Antar.

## What is stored

- `verse-1.1-mool-evidence.json` — minimal observed root Sanskrit + metadata
- `metadata.json` — provenance summary
- `SHA256SUMS`

The **full HTML page is not preserved**. Only the extracted `मूल श्लोकः` root text needed for an auditable comparison is stored.

## What is excluded

- Sanskrit commentary
- English Translation / commentary
- Navigation, forms, audio
- Bulk corpus extraction

## Prohibited uses

- Canonical import into `scripture.verses`
- Bulk corpus harvesting
- Commentary / Translation import

## Editorial workspace

See [`content/editorial/reviews/1.1.md`](../../../editorial/reviews/1.1.md).
