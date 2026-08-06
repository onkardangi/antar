# Reading Progress (Phase 1)

Local-only foundation for remembering the Reader’s Verse position on device.

## Scope

**Implemented**

- Versioned local Reading Progress document (schema v1)
- Storage port + AsyncStorage adapter
- `ReadingProgressService` with serialized mutations
- Verse Reader recording after a successful Sanskrit load

**Not implemented**

- Backend / account sync
- Authentication
- Home / Continue Reading UI
- Chapter progress indicators
- Bookmarks, streaks, analytics, notifications

## Storage

| Concern | Value |
| --- | --- |
| Key | `antar.reading-progress.v1` |
| Backend | `@react-native-async-storage/async-storage` via `AsyncStorageAdapter` |
| SecureStore | Not used (progress is not a secret) |

## Schema v1

```json
{
  "schemaVersion": 1,
  "lastRead": {
    "verseId": "...",
    "chapterId": "...",
    "chapterNumber": 1,
    "verseNumber": 12,
    "canonicalReference": "1.12",
    "openedAt": "2026-08-05T18:00:00.000Z"
  },
  "chapters": {
    "<chapterId>": {
      "chapterId": "...",
      "chapterNumber": 1,
      "furthestVerseId": "...",
      "furthestVerseNumber": 12,
      "furthestCanonicalReference": "1.12",
      "updatedAt": "2026-08-05T18:00:00.000Z"
    }
  }
}
```

No Sanskrit, Translation, notes, or Reader identity are stored.

Loaded documents must keep `canonicalReference` / `furthestCanonicalReference`
equal to `chapterNumber.verseNumber` (or furthest verse number). Map keys must
match `chapterId`. Timestamps must be UTC ISO-8601 ending in `Z`.

## Semantics

- **lastRead** — most recently successfully loaded Verse (always updated on open).
- **furthest per Chapter** — advances only when the opened `verseNumber` is greater than the saved furthest; reopening an earlier Verse does not reduce it.
- Timestamps are UTC ISO-8601 from an injectable clock.

## Mutation results

`recordVerseOpened` returns a typed result:

```ts
type ReadingProgressMutationResult =
  | { persisted: true; progress: ReadingProgressDocument }
  | {
      persisted: false;
      progress: ReadingProgressDocument;
      reason: 'read_error' | 'write_error';
    };
```

| Outcome | `persisted` | `progress` |
| --- | --- | --- |
| Save succeeded | `true` | newly saved document |
| `load.source === 'read_error'` | `false` | empty v1 document; **no write** |
| Save threw | `false` | previously loaded persisted document (not the unsaved optimistic update) |

`clearReadingProgress` returns:

```ts
type ReadingProgressClearResult =
  | { cleared: true }
  | { cleared: false; reason: 'clear_error' };
```

`getReadingProgress()` remains the authoritative read API. Verse Reader ignores
mutation outcomes; persistence failure never blocks Scripture.

## Failure behavior

| Situation | Behavior |
| --- | --- |
| Missing key | Empty valid v1 document; later opens may write a fresh document |
| Corrupt / incompatible JSON | Empty valid v1 document on load; **does not** overwrite storage on read; a later successful open may replace corrupt data |
| Storage read exception (`read_error`) | Empty document to callers; **no** `setItem` / `removeItem`; prior stored bytes kept; mutation queue continues |
| Storage write exception | Non-fatal; previous stored document preserved; result `persisted=false`; mutation queue continues |
| Verse Reader | Scripture still renders if progress persistence fails |

## Composition

```text
createReadingProgressService()
  ReadingProgressService
    → LocalReadingProgressRepository
      → AsyncStorageAdapter
```

`ReadingProgressProvider` in `AppProviders` supplies the real service to production navigation. Tests may inject a mock service.

## Future consumers

- Continue Reading
- Chapter progress indication
- Home
- Optional account sync (not in this phase)

## Clearing

`clearReadingProgress()` exists for tests and a future Settings action. No Settings UI is shipped here.
