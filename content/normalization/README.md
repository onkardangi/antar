# Antar content normalization tooling

Scripts that read **preserved raw snapshots** and emit deterministic extraction
artifacts for editorial comparison.

Normalization does not approve content and does not write to PostgreSQL.

## Commands

```bash
python3 content/normalization/parse_wikisource_chapter.py \
  --snapshot content/raw/sanskrit/wikisource/chapter-01/sa-wikisource-bg-chapter-01-revision-343151.json \
  --source-id bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151 \
  --output content/editorial/bhagavad-gita/chapter-01/wikisource-extraction.jsonl

python3 -m unittest discover content/normalization/tests
```
