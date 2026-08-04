# Source registry schema

Each entry in `sources.json` uses these fields.

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Stable slug, e.g. `kaggle-tarun-tiwari-bhagavad-gita` |
| `title` | yes | Human-readable source title |
| `creator` | yes | Author / publisher / dataset owner |
| `platform` | no | Acquisition platform (Kaggle, publisher site, etc.) |
| `source_url` | no | Canonical upstream URL |
| `license_displayed` | yes | License as displayed at acquisition time |
| `license_catalog_id` | no | Key into `content/licenses/` when recorded |
| `content_kinds` | yes | Array: `sanskrit`, `transliteration`, `translation`, `commentary`, `other` |
| `edition_tradition` | no | Numbering/edition note (e.g. `as-it-is-46-35`, `antar-47-34`) |
| `chapter_1_verse_count` | no | Observed or claimed Chapter 1 count |
| `chapter_13_verse_count` | no | Observed or claimed Chapter 13 count |
| `total_verses` | no | Observed or claimed total |
| `matches_antar_numbering` | yes | `true` / `false` / `unknown` |
| `raw_path` | no | Repo-relative path under `content/raw/` |
| `original_filename` | no | Upstream filename |
| `sha256` | yes when raw present | Hex SHA-256 of the immutable raw artifact |
| `status` | yes | See `README.md` status vocabulary |
| `inspection_doc` | no | Path to inspection notes |
| `decision_summary` | no | Short reason for current status |
| `updated_at` | yes | ISO-8601 date of last registry update |

Unknown licensing must block `APPROVED_FOR_IMPORT`.
