import type { ReadingProgressDocument } from '../model/readingProgressTypes';
import { LocalReadingProgressRepository } from './LocalReadingProgressRepository';
import {
  parseReadingProgressDocument,
  serializeReadingProgressDocument,
} from './parseReadingProgressDocument';
import { READING_PROGRESS_STORAGE_KEY } from './readingProgressStorageKey';
import { MemoryLocalStorage } from '../test/MemoryLocalStorage';

const VALID_DOCUMENT: ReadingProgressDocument = {
  schemaVersion: 1,
  lastRead: {
    verseId: 'verse-1',
    chapterId: 'chapter-1',
    chapterNumber: 1,
    verseNumber: 1,
    canonicalReference: '1.1',
    openedAt: '2026-08-05T18:00:00.000Z',
  },
  chapters: {
    'chapter-1': {
      chapterId: 'chapter-1',
      chapterNumber: 1,
      furthestVerseId: 'verse-1',
      furthestVerseNumber: 1,
      furthestCanonicalReference: '1.1',
      updatedAt: '2026-08-05T18:00:00.000Z',
    },
  },
};

describe('parseReadingProgressDocument', () => {
  it('round-trips a valid v1 document', () => {
    const raw = serializeReadingProgressDocument(VALID_DOCUMENT);
    expect(parseReadingProgressDocument(raw)).toEqual(VALID_DOCUMENT);
  });

  it('rejects incompatible schema versions', () => {
    const raw = JSON.stringify({ ...VALID_DOCUMENT, schemaVersion: 2 });
    expect(parseReadingProgressDocument(raw)).toBeNull();
  });

  it('rejects malformed JSON and incomplete shapes', () => {
    expect(parseReadingProgressDocument('not-json')).toBeNull();
    expect(parseReadingProgressDocument('[]')).toBeNull();
    expect(
      parseReadingProgressDocument(
        JSON.stringify({ schemaVersion: 1, lastRead: null }),
      ),
    ).toBeNull();
  });

  it('rejects mismatched lastRead canonicalReference', () => {
    const raw = serializeReadingProgressDocument({
      ...VALID_DOCUMENT,
      lastRead: {
        ...VALID_DOCUMENT.lastRead!,
        canonicalReference: '1.2',
      },
    });
    expect(parseReadingProgressDocument(raw)).toBeNull();
  });

  it('rejects mismatched furthestCanonicalReference', () => {
    const raw = serializeReadingProgressDocument({
      ...VALID_DOCUMENT,
      chapters: {
        'chapter-1': {
          ...VALID_DOCUMENT.chapters['chapter-1']!,
          furthestCanonicalReference: '1.9',
        },
      },
    });
    expect(parseReadingProgressDocument(raw)).toBeNull();
  });

  it('rejects invalid numeric values', () => {
    const raw = JSON.stringify({
      ...VALID_DOCUMENT,
      lastRead: {
        ...VALID_DOCUMENT.lastRead,
        verseNumber: 0,
        canonicalReference: '1.0',
      },
    });
    expect(parseReadingProgressDocument(raw)).toBeNull();
  });

  it('rejects blank IDs', () => {
    const raw = serializeReadingProgressDocument({
      ...VALID_DOCUMENT,
      lastRead: {
        ...VALID_DOCUMENT.lastRead!,
        verseId: '   ',
      },
    });
    expect(parseReadingProgressDocument(raw)).toBeNull();
  });

  it('rejects chapter map key mismatch', () => {
    const raw = JSON.stringify({
      schemaVersion: 1,
      lastRead: null,
      chapters: {
        'wrong-key': VALID_DOCUMENT.chapters['chapter-1'],
      },
    });
    expect(parseReadingProgressDocument(raw)).toBeNull();
  });

  it('rejects non-UTC ISO timestamps', () => {
    const raw = serializeReadingProgressDocument({
      ...VALID_DOCUMENT,
      lastRead: {
        ...VALID_DOCUMENT.lastRead!,
        openedAt: '2026-08-05T18:00:00+00:00',
      },
    });
    expect(parseReadingProgressDocument(raw)).toBeNull();
  });
});

describe('LocalReadingProgressRepository', () => {
  it('uses the stable storage key', async () => {
    const storage = new MemoryLocalStorage();
    const repository = new LocalReadingProgressRepository(storage);
    await repository.save(VALID_DOCUMENT);
    expect(storage.setItemCalls[0]?.key).toBe(READING_PROGRESS_STORAGE_KEY);
  });

  it('returns missing source for an absent key without writing', async () => {
    const storage = new MemoryLocalStorage();
    const repository = new LocalReadingProgressRepository(storage);
    const loaded = await repository.load();
    expect(loaded.source).toBe('missing');
    expect(loaded.document).toEqual({
      schemaVersion: 1,
      lastRead: null,
      chapters: {},
    });
    expect(storage.setItemCalls).toHaveLength(0);
  });

  it('returns corrupt source without overwriting storage', async () => {
    const storage = new MemoryLocalStorage();
    storage.seed(READING_PROGRESS_STORAGE_KEY, '{"schemaVersion":99}');
    const repository = new LocalReadingProgressRepository(storage);
    const loaded = await repository.load();
    expect(loaded.source).toBe('corrupt');
    expect(loaded.document.lastRead).toBeNull();
    expect(storage.setItemCalls).toHaveLength(0);
    expect(storage.peek(READING_PROGRESS_STORAGE_KEY)).toBe(
      '{"schemaVersion":99}',
    );
  });

  it('returns read_error without calling setItem', async () => {
    const storage = new MemoryLocalStorage();
    storage.getItemFailure = new Error('io');
    const repository = new LocalReadingProgressRepository(storage);
    const loaded = await repository.load();
    expect(loaded.source).toBe('read_error');
    expect(loaded.document).toEqual({
      schemaVersion: 1,
      lastRead: null,
      chapters: {},
    });
    expect(storage.setItemCalls).toHaveLength(0);
  });

  it('loads a previously saved document', async () => {
    const storage = new MemoryLocalStorage();
    const repository = new LocalReadingProgressRepository(storage);
    await repository.save(VALID_DOCUMENT);
    const loaded = await repository.load();
    expect(loaded.source).toBe('ok');
    expect(loaded.document).toEqual(VALID_DOCUMENT);
  });

  it('clear removes the stored document', async () => {
    const storage = new MemoryLocalStorage();
    const repository = new LocalReadingProgressRepository(storage);
    await repository.save(VALID_DOCUMENT);
    await repository.clear();
    const loaded = await repository.load();
    expect(loaded.source).toBe('missing');
  });

  it('treats inconsistent references as corrupt without writing', async () => {
    const storage = new MemoryLocalStorage();
    storage.seed(
      READING_PROGRESS_STORAGE_KEY,
      JSON.stringify({
        ...VALID_DOCUMENT,
        lastRead: {
          ...VALID_DOCUMENT.lastRead,
          canonicalReference: '9.9',
        },
      }),
    );
    const repository = new LocalReadingProgressRepository(storage);
    const loaded = await repository.load();
    expect(loaded.source).toBe('corrupt');
    expect(storage.setItemCalls).toHaveLength(0);
  });
});
