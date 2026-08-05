# Antar content acquisition tooling

Scripts that fetch immutable raw source snapshots for editorial review.

## Rules

- Prefer official MediaWiki APIs over HTML scraping.
- Never mutate an existing raw revision snapshot silently.
- Record User-Agent, URL, page ID, revision ID, and retrieval time.
- Acquisition does not approve or import content.

## User-Agent

Default (override with `--user-agent` or env `ANTAR_CONTENT_USER_AGENT`):

```text
AntarContentAcquisition/0.1 (+https://github.com/antar-project/antar; content-acquisition@antar.example)
```

Replace the placeholder repository/contact with project-owned values before production automation.

## Commands

```bash
python3 content/acquisition/fetch_wikisource_page.py \
  --title 'भगवद्गीता/अर्जुनविषादयोगः' \
  --page-id 164 \
  --revision-id 343151 \
  --output-dir content/raw/sanskrit/wikisource/chapter-01

# Single Verse IIT mool verification (default delay 10s; Crawl-delay honor)
python3 content/acquisition/fetch_iitk_verse.py --chapter 1 --verse 2

# Batch sequential acquisition
python3 content/acquisition/fetch_iitk_chapter.py \
  --chapter 1 --verse-start 2 --verse-end 47 --resume

# Integrate into editorial workspace (never approves; never edits canonical-draft)
python3 content/acquisition/integrate_iitk_workspace.py \
  --verse-start 2 --verse-end 47 \
  --manifest content/raw/sanskrit/iit-kanpur/chapter-01-manifest.json

python3 -m unittest discover content/acquisition/tests

# Translation (Internet Archive) — see content/acquisition/translation/README.md
python3 content/acquisition/translation/fetch_internet_archive_item.py \
  --item-id in.ernet.dli.2015.386852 \
  --output-dir content/raw/translations/swarupananda-1909

python3 -m unittest discover content/acquisition/translation/tests
```

See `IITK_ACQUISITION_ETHICS.md` for robots/delay/redistribution rules.
Translation IA acquisition: `content/acquisition/translation/README.md`.
