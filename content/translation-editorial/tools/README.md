# Translation Editorial Tools

Stdlib-only Python helpers for Translation segment workspaces.

| Script | Role |
|--------|------|
| `extract_swarupananda_chapter01.py` | Refresh Chapter 1 workspace JSON/JSONL from pinned extraction data |
| `validate_translation_segments.py` | Validate segment-draft + coverage-map integrity |

## Tests

```bash
python3 -m unittest discover content/translation-editorial/tools/tests
```

Offline fixtures only. No network. Does not modify `content/raw/`.
