# `content/registry/`

Source registry for Antar content candidates.

## Files

| File | Role |
|------|------|
| `sources.json` | Authoritative list of known sources and approval statuses |
| `schema.md` | Field definitions for registry entries |

## Status vocabulary

| Status | Meaning |
|--------|---------|
| `CANDIDATE` | Downloaded or identified; inspection incomplete |
| `VERIFICATION_ONLY` | Secondary verification reference; must not be used for canonical import |
| `ACQUIRED_UNREVIEWED` | Raw snapshot preserved; not yet approved for normalization/import |
| `INSPECTED` | Inspection documented; no approval decision |
| `REJECTED_FOR_CANONICAL_IMPORT` | Must not enter `scripture.*` as canonical content |
| `APPROVED_FOR_NORMALIZATION` | May enter the normalization pipeline |
| `NORMALIZED` | Normalized artifacts exist and checksummed |
| `APPROVED_FOR_IMPORT` | Editorial + license clearance for database import |
| `IMPORTED` | Loaded into the product database under a content version |
| `RETIRED` | Superseded; retained for provenance only |

Update `sources.json` when status changes. Do not imply database import from registry status alone.
