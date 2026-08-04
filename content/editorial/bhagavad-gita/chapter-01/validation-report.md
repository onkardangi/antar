# Chapter 1 validation report

**Workspace:** `content/editorial/bhagavad-gita/chapter-01/`  
**Date:** 2026-08-04

## Distinction of validation layers

| Layer | Result |
|-------|--------|
| Source acquisition validated | **Yes** — revision `343151` preserved, checksum registered |
| Structural extraction validated | **Yes** — exactly 47 Verse poems `1.1`–`1.47` |
| Textual accuracy editorially approved | **No** — human review still required |
| Canonical draft approved / import-ready | **No** |

## Source acquisition

| Field | Value |
|-------|-------|
| Source ID | `bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151` |
| Page ID | `164` |
| Revision ID | `343151` |
| Revision timestamp | `2022-08-10T14:13:52Z` |
| Retrieval timestamp | `2026-08-04T13:10:42Z` |
| Raw snapshot | `content/raw/sanskrit/wikisource/chapter-01/sa-wikisource-bg-chapter-01-revision-343151.json` |
| Raw SHA-256 | `b2df3556998a3a18dd3fe12269d491887a21bc8791cb1b918cd226aff75b8321` |
| Registry status | `ACQUIRED_UNREVIEWED` |

## Structural extraction

| Check | Result |
|-------|--------|
| Extracted Verse count | `47` |
| Canonical references | `1.1` through `1.47` |
| Duplicate references | `0` |
| Missing references | `0` |
| Sanskrit nonblank | `47` / `47` |
| Transliteration | all `null` |
| Commentary templates included | `0` (excluded) |

## Source-comparison status counts

| Status | Count |
|--------|------:|
| `READY_FOR_REVIEW` | 47 |
| `SOURCE_MISSING` | 0 |
| `SOURCE_CONFLICT` | 0 |
| `UNREVIEWED` | 0 |
| `APPROVED` | 0 |
| `REJECTED` | 0 |

## Canonical draft (unchanged gate)

| Check | Result |
|-------|--------|
| Approved records | `0` |
| Sanskrit-populated records | `0` |
| Transliteration-populated records | `0` |
| Import readiness | `false` / `NOT_READY` |

## Normalization operations recorded

Applied during extraction (not Sanskrit rewriting):

- excluded `[[File:…]]` audio/file links
- excluded navigation template `{{भगवद्गीतायाः अध्यायाः}}`
- excluded `{{व्याख्या}}` commentary templates (47)
- removed wikitext bold delimiters `'''…'''` while preserving inner text
- trimmed surrounding whitespace
- Unicode form: NFC (input already NFC for this revision; operation recorded when a change occurs)
- line endings: LF

### Verse 1.1 front-matter note

The complete source poem body is preserved, including pre-Verse material (`ॐ`, salutations, chapter title). No editorial strip was performed. A `parsingNotes` entry flags this for human review.

## Commands

```bash
# Verify raw checksums
shasum -a 256 -c content/checksums/raw.sha256

# Parse preserved revision (deterministic)
python3 content/normalization/parse_wikisource_chapter.py \
  --snapshot content/raw/sanskrit/wikisource/chapter-01/sa-wikisource-bg-chapter-01-revision-343151.json \
  --source-id bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151 \
  --output content/editorial/bhagavad-gita/chapter-01/wikisource-extraction.jsonl

# Validate Chapter 1 workspace
python3 content/validation/validate_chapter01_workspace.py
python3 content/validation/validate_chapter_draft.py \
  content/editorial/bhagavad-gita/chapter-01/canonical-draft.jsonl

# Offline tests
python3 -m unittest discover content/validation/tests
python3 -m unittest discover content/acquisition/tests
python3 -m unittest discover content/normalization/tests
```

Acquisition (network; run only when intentionally refreshing provenance — refuses silent mutation of a different snapshot):

```bash
python3 content/acquisition/fetch_wikisource_page.py \
  --title 'भगवद्गीता/अर्जुनविषादयोगः' \
  --page-id 164 \
  --revision-id 343151 \
  --output-dir content/raw/sanskrit/wikisource/chapter-01
```
