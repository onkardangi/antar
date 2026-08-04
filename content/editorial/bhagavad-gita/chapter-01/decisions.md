# Chapter 1 editorial decisions

## Standing decisions

### Antar Chapter 1 verse count

Antar expects **47** Verses for Chapter 1 (`1.1` through `1.47`), matching `V003__seed_scripture_chapters.sql` and `content/validation/antar_verse_counts.json`.

### Rejected Kaggle source (46 records)

The Tarun Tiwari Kaggle corpus (`kaggle-tarun-tiwari-bhagavad-gita`) contains **46** Chapter 1 records. Registry status: `REJECTED_FOR_CANONICAL_IMPORT`.

It is a legitimate alternate numbering tradition (As It Is–style), not an inaccurate text. It is **not** approved for canonical import and must not be loaded into `scripture.verses`.

### No automated reconstruction

No automated split, merge, renumber, or rewrite of source verses is permitted to turn 46 records into 47 Antar identities. Every canonical Verse must be supported by approved source evidence through human editorial work.

### Source evidence required

- Every canonical Verse must eventually cite approved source evidence in `source-comparison.jsonl`.
- Source differences must be documented per Verse.
- Editorial approval is human-controlled.
- Do not copy text from rejected or unapproved sources into the canonical draft.

### Canonical draft import gate

`canonical-draft.jsonl` remains **non-importable** until all **47** records are `APPROVED` with non-blank Sanskrit and transliteration.

### Separate layers

Translation and Commentary remain separate layers and are out of scope for this Chapter 1 workspace.

---

## Open editorial work

1. Human-review Wikisource extraction for textual accuracy (not yet approved).
2. Decide how Verse **1.1** front matter (ॐ / salutations / chapter title) should appear in the eventual canonical draft — extraction currently preserves the full poem body with a parsing note; no silent strip was performed.
3. Confirm speaker-label retention policy for canonical storage.
4. Complete checklist and only then populate `canonical-draft.jsonl`.
5. Do not import until all 47 draft records are `APPROVED`.

Until then: `canonical-draft.jsonl` remains unapproved with `null` Sanskrit/transliteration.

### Source acquisition note (2026-08-04)

Sanskrit Wikisource Chapter 1 revision `343151` acquired as `PRIMARY_TRANSCRIPTION_CANDIDATE` (`ACQUIRED_UNREVIEWED`). See `content/raw/sanskrit/wikisource/chapter-01/README.md` and registry id `bhagavad-gita-sanskrit-wikisource-sa-chapter-01-r343151`.

---

## Decision-log template

Copy for each discrepancy:

```markdown
## Decision BG-1-XXX

Canonical reference:

Sources compared:

Observed difference:

Decision:

Reason:

Reviewer:

Date:

Status:
```

### Status values for decisions

Use clear human statuses such as: `OPEN`, `RESOLVED`, `DEFERRED`, `REJECTED_SOURCE`.

---

## Decision log

_No Verse-level discrepancy decisions recorded yet. Workspace initialized with identities only._
