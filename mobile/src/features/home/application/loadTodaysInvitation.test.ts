import { serializeReadingProgressDocument } from '../../reading-progress/storage/parseReadingProgressDocument';
import { LocalReadingProgressRepository } from '../../reading-progress/storage/LocalReadingProgressRepository';
import { MemoryLocalStorage } from '../../reading-progress/test/MemoryLocalStorage';
import { READING_PROGRESS_STORAGE_KEY } from '../../reading-progress/storage/readingProgressStorageKey';
import { loadTodaysInvitation } from './loadTodaysInvitation';

describe('loadTodaysInvitation', () => {
  it('resolves Begin Journey with canonical start destination', async () => {
    const state = await loadTodaysInvitation({
      loadProgress: async () => ({
        source: 'missing',
        document: {
          schemaVersion: 1,
          lastRead: null,
          chapters: {},
        },
      }),
      resolveCanonicalStart: async () => ({
        verseId: 'verse-1-1',
        verseNumber: 1,
        chapterNumber: 1,
      }),
    });

    expect(state).toEqual({
      kind: 'begin_journey',
      resolution: 'ready',
      destination: {
        verseId: 'verse-1-1',
        verseNumber: 1,
        chapterNumber: 1,
      },
    });
  });

  it('returns begin_journey unavailable when canonical start cannot resolve', async () => {
    const state = await loadTodaysInvitation({
      loadProgress: async () => ({
        source: 'missing',
        document: {
          schemaVersion: 1,
          lastRead: null,
          chapters: {},
        },
      }),
      resolveCanonicalStart: async () => null,
    });

    expect(state).toEqual({
      kind: 'begin_journey',
      resolution: 'unavailable',
    });
  });

  it('returns Continue Reading for lastRead destination', async () => {
    const state = await loadTodaysInvitation({
      loadProgress: async () => ({
        source: 'ok',
        document: {
          schemaVersion: 1,
          lastRead: {
            verseId: 'verse-12',
            chapterId: 'chapter-1',
            chapterNumber: 1,
            verseNumber: 12,
            canonicalReference: '1.12',
            openedAt: '2026-08-05T18:00:00.000Z',
          },
          chapters: {},
        },
      }),
      resolveCanonicalStart: async () => {
        throw new Error('should not resolve canonical start for continue');
      },
    });

    expect(state).toEqual({
      kind: 'continue_reading',
      destination: {
        verseId: 'verse-12',
        verseNumber: 12,
        chapterNumber: 1,
      },
    });
  });

  it('read_error → unavailable → recovery → Continue Reading for Verse 12 without destructive write', async () => {
    const storage = new MemoryLocalStorage();
    const document = {
      schemaVersion: 1 as const,
      lastRead: {
        verseId: 'verse-12',
        chapterId: 'chapter-1',
        chapterNumber: 1,
        verseNumber: 12,
        canonicalReference: '1.12',
        openedAt: '2026-08-05T18:00:00.000Z',
      },
      chapters: {
        'chapter-1': {
          chapterId: 'chapter-1',
          chapterNumber: 1,
          furthestVerseId: 'verse-40',
          furthestVerseNumber: 40,
          furthestCanonicalReference: '1.40',
          updatedAt: '2026-08-05T18:00:00.000Z',
        },
      },
    };
    storage.seed(
      READING_PROGRESS_STORAGE_KEY,
      serializeReadingProgressDocument(document),
    );

    const repository = new LocalReadingProgressRepository(storage);

    storage.getItemFailure = new Error('transient read failure');
    const setItemCallsBefore = storage.setItemCalls.length;

    const unavailable = await loadTodaysInvitation({
      loadProgress: () => repository.load(),
      resolveCanonicalStart: async () => ({
        verseId: 'verse-1-1',
        verseNumber: 1,
        chapterNumber: 1,
      }),
    });

    expect(unavailable).toEqual({ kind: 'progress_unavailable' });
    expect(storage.setItemCalls.length).toBe(setItemCallsBefore);
    expect(storage.peek(READING_PROGRESS_STORAGE_KEY)).toBe(
      serializeReadingProgressDocument(document),
    );

    storage.getItemFailure = null;

    const recovered = await loadTodaysInvitation({
      loadProgress: () => repository.load(),
      resolveCanonicalStart: async () => ({
        verseId: 'verse-1-1',
        verseNumber: 1,
        chapterNumber: 1,
      }),
    });

    expect(recovered).toEqual({
      kind: 'continue_reading',
      destination: {
        verseId: 'verse-12',
        verseNumber: 12,
        chapterNumber: 1,
      },
    });
    expect(storage.setItemCalls.length).toBe(setItemCallsBefore);
  });
});
