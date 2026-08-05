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

## Phase 2 pin

| Field | Value |
|-------|-------|
| Item | `in.ernet.dli.2015.386852` |
| Master | `2015.386852.Srimad-Bhagavad.pdf` |
| Rejected | `in.ernet.dli.2015.237563` (1967 tenth impression) |
