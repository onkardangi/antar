# Translation acquisition tooling

Scripts that fetch and inspect Internet Archive Translation scan candidates.

## Rules

- Prefer Internet Archive item files + metadata API over HTML scrape mirrors.
- Never mutate an existing raw artifact silently.
- Record User-Agent, item ID, URLs, retrieval time, and SHA-256.
- OCR aids are **not** authoritative transcriptions.
- Acquisition/inspection does **not** approve, normalize, package, or import Translation.

## User-Agent

Default (override with `--user-agent` or env `ANTAR_CONTENT_USER_AGENT`):

```text
AntarContentAcquisition/0.1 (+https://github.com/antar-project/antar; content-acquisition@antar.example)
```

## Commands

```bash
# Acquire pinned Swarupananda 1909 first-edition scan set
python3 content/acquisition/translation/fetch_internet_archive_item.py \
  --item-id in.ernet.dli.2015.386852 \
  --output-dir content/raw/translations/swarupananda-1909

# OCR label candidates only (read-only; never rewrites raw/)
python3 content/acquisition/translation/inspect_translation_labels.py \
  --ocr-file content/raw/translations/swarupananda-1909/2015.386852.Srimad-Bhagavad_djvu.txt

python3 -m unittest discover content/acquisition/translation/tests
```

## Current production pin (Besant & Das 1905)

```bash
python3 content/acquisition/translation/fetch_internet_archive_item.py \
  --item-id bhagavadgitawith00londiala \
  --output-dir content/raw/translations/besant-das-1905 \
  --pinned-master bhagavadgitawith00londiala.pdf \
  --file bhagavadgitawith00londiala.pdf \
  --file bhagavadgitawith00londiala_meta.xml \
  --file bhagavadgitawith00londiala_files.xml \
  --file bhagavadgitawith00londiala_djvu.txt \
  --file bhagavadgitawith00londiala_page_numbers.json
```

| Field | Value |
|-------|-------|
| Item | `bhagavadgitawith00londiala` |
| Master | `bhagavadgitawith00londiala.pdf` |
| Role | `PRIMARY_TRANSLATION_CANDIDATE` |
| Rejected | `bhagavadgitaorlo00besa` (Natesan 1922); `wg1100` (folkscanomy) |

## Frozen future edition (Swarupananda 1909)

| Field | Value |
|-------|-------|
| Item | `in.ernet.dli.2015.386852` |
| Master | `2015.386852.Srimad-Bhagavad.pdf` |
| Rejected | `in.ernet.dli.2015.237563` (1967 tenth impression) |
| Note | Incomplete pinned scan; do not silently repair from later editions |
