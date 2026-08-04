# IIT Kanpur / Gita Supersite acquisition ethics

**Status:** Binding for Antar content acquisition  
**Last Updated:** August 2026

## Purpose

Acquire **minimal root-Sanskrit mool** evidence for secondary verification only.
This is not a corpus harvest and not an import source.

## Access pattern

| Rule | Requirement |
|------|-------------|
| Concurrency | Sequential only — one Verse request at a time |
| Delay | Conservative; default **10 seconds** to honor `Crawl-delay: 10` on `old.gitasupersite.in/robots.txt` (never below 2s) |
| Retries | Bounded transient failures only; max **3** attempts per Verse |
| Scope | `/srimad` mool pages only; never bulk HTML mirroring |
| Content | Root `मूल श्लोकः` only — no commentary, Translation, navigation, forms, audio |
| Auth | No authenticated or undocumented private APIs |
| Overwrite | Refuse silent overwrite of different evidence bytes |
| Blocking | Stop on repeated provider errors; require manual rerun |

## robots.txt assessment (legacy host)

Inspected `https://old.gitasupersite.in/robots.txt`:

- `User-agent: *`
- `Crawl-delay: 10`
- `/srimad` is **not** listed under `Disallow`
- Admin/search/user paths are disallowed (not used)

Sequential `/srimad?…show_mool=1` requests with ≥10s delay appear permissible under that robots policy.
If robots.txt or explicit site restrictions later prohibit this pattern, **stop and report** instead of continuing.

The modern SPA (`gitasupersite.iitk.ac.in` / `www.gitasupersite.in`) does not embed mool without authenticated API access; Antar does not use those private APIs.

## License / redistribution

- Role: `SECONDARY_VERIFICATION_REFERENCE`
- Status: `VERIFICATION_ONLY`
- License: `LICENSE_UNCONFIRMED_FOR_REDISTRIBUTION`
- No redistribution claim is made for the digital transcription
- Underlying ancient Sanskrit work is public domain; site packaging rights are unconfirmed
- IIT Kanpur / Gita Supersite does **not** endorse Antar

## Prohibited

- Canonical import into PostgreSQL / `scripture.verses`
- Marking IIT evidence `APPROVED_FOR_IMPORT`
- Bulk scraping or full-page archival
- Commentary / Translation collection
- Bypassing access restrictions
