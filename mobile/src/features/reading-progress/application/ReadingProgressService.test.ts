import {
  ReadingProgressService,
  ReadingProgressValidationError,
} from './ReadingProgressService';
import type { ReadingProgressDocument } from '../model/readingProgressTypes';
import { LocalReadingProgressRepository } from '../storage/LocalReadingProgressRepository';
import { serializeReadingProgressDocument } from '../storage/parseReadingProgressDocument';
import { READING_PROGRESS_STORAGE_KEY } from '../storage/readingProgressStorageKey';
import { MemoryLocalStorage } from '../test/MemoryLocalStorage';

const FIXED_NOW = new Date('2026-08-05T18:00:00.000Z');
const LATER_NOW = new Date('2026-08-05T19:00:00.000Z');

async function waitForCondition(
  predicate: () => boolean,
  attempts = 50,
): Promise<void> {
  for (let i = 0; i < attempts; i += 1) {
    if (predicate()) {
      return;
    }
    await new Promise<void>((resolve) => {
      setImmediate(resolve);
    });
  }
  throw new Error('Condition not met in time');
}

function createService(storage = new MemoryLocalStorage(), now = FIXED_NOW) {
  const repository = new LocalReadingProgressRepository(storage);
  const service = new ReadingProgressService(repository, () => now);
  return { storage, repository, service };
}

const VERSE_1_1 = {
  verseId: 'verse-1',
  chapterId: 'chapter-1',
  chapterNumber: 1,
  verseNumber: 1,
  canonicalReference: '1.1',
};

const VERSE_1_2 = {
  verseId: 'verse-2',
  chapterId: 'chapter-1',
  chapterNumber: 1,
  verseNumber: 2,
  canonicalReference: '1.2',
};

const VERSE_2_1 = {
  verseId: 'verse-c2-1',
  chapterId: 'chapter-2',
  chapterNumber: 2,
  verseNumber: 1,
  canonicalReference: '2.1',
};

const MULTI_CHAPTER_DOCUMENT: ReadingProgressDocument = {
  schemaVersion: 1,
  lastRead: {
    ...VERSE_2_1,
    openedAt: '2026-08-05T17:00:00.000Z',
  },
  chapters: {
    'chapter-1': {
      chapterId: 'chapter-1',
      chapterNumber: 1,
      furthestVerseId: 'verse-2',
      furthestVerseNumber: 2,
      furthestCanonicalReference: '1.2',
      updatedAt: '2026-08-05T16:00:00.000Z',
    },
    'chapter-2': {
      chapterId: 'chapter-2',
      chapterNumber: 2,
      furthestVerseId: 'verse-c2-1',
      furthestVerseNumber: 1,
      furthestCanonicalReference: '2.1',
      updatedAt: '2026-08-05T17:00:00.000Z',
    },
  },
};

describe('ReadingProgressService', () => {
  it('starts with an empty valid v1 document', async () => {
    const { service } = createService();
    const progress = await service.getReadingProgress();
    expect(progress).toEqual({
      schemaVersion: 1,
      lastRead: null,
      chapters: {},
    });
    expect(await service.getLastRead()).toBeNull();
  });

  it('records the first Verse opened with persisted=true', async () => {
    const { service } = createService();
    const result = await service.recordVerseOpened(VERSE_1_1);

    expect(result.persisted).toBe(true);
    expect(result.progress.lastRead).toEqual({
      ...VERSE_1_1,
      openedAt: '2026-08-05T18:00:00.000Z',
    });
    expect(result.progress.chapters['chapter-1']).toEqual({
      chapterId: 'chapter-1',
      chapterNumber: 1,
      furthestVerseId: 'verse-1',
      furthestVerseNumber: 1,
      furthestCanonicalReference: '1.1',
      updatedAt: '2026-08-05T18:00:00.000Z',
    });
  });

  it('advances furthest when a later Verse is opened', async () => {
    const { service } = createService();
    await service.recordVerseOpened(VERSE_1_1);
    const result = await service.recordVerseOpened(VERSE_1_2);

    expect(result.persisted).toBe(true);
    expect(result.progress.lastRead?.canonicalReference).toBe('1.2');
    expect(result.progress.chapters['chapter-1']?.furthestVerseNumber).toBe(2);
    expect(result.progress.chapters['chapter-1']?.furthestCanonicalReference).toBe(
      '1.2',
    );
  });

  it('updates lastRead but not furthest when reopening an earlier Verse', async () => {
    let now = FIXED_NOW;
    const storage = new MemoryLocalStorage();
    const repository = new LocalReadingProgressRepository(storage);
    const service = new ReadingProgressService(repository, () => now);

    await service.recordVerseOpened(VERSE_1_1);
    await service.recordVerseOpened(VERSE_1_2);

    now = LATER_NOW;
    const result = await service.recordVerseOpened(VERSE_1_1);

    expect(result.persisted).toBe(true);
    expect(result.progress.lastRead).toEqual({
      ...VERSE_1_1,
      openedAt: '2026-08-05T19:00:00.000Z',
    });
    expect(result.progress.chapters['chapter-1']?.furthestVerseNumber).toBe(2);
    expect(result.progress.chapters['chapter-1']?.furthestVerseId).toBe(
      'verse-2',
    );
    expect(result.progress.chapters['chapter-1']?.updatedAt).toBe(
      '2026-08-05T18:00:00.000Z',
    );
  });

  it('preserves progress for multiple Chapters', async () => {
    const { service } = createService();
    await service.recordVerseOpened(VERSE_1_2);
    const result = await service.recordVerseOpened(VERSE_2_1);

    expect(result.progress.chapters['chapter-1']?.furthestVerseNumber).toBe(2);
    expect(result.progress.chapters['chapter-2']?.furthestVerseNumber).toBe(1);
    expect(result.progress.lastRead?.canonicalReference).toBe('2.1');
  });

  it('reopening the same Verse is idempotent except timestamp', async () => {
    let now = FIXED_NOW;
    const storage = new MemoryLocalStorage();
    const repository = new LocalReadingProgressRepository(storage);
    const service = new ReadingProgressService(repository, () => now);

    const first = await service.recordVerseOpened(VERSE_1_1);
    now = LATER_NOW;
    const second = await service.recordVerseOpened(VERSE_1_1);

    expect(second.progress.lastRead?.openedAt).toBe(
      '2026-08-05T19:00:00.000Z',
    );
    expect(second.progress.lastRead?.verseId).toBe(
      first.progress.lastRead?.verseId,
    );
    expect(second.progress.chapters['chapter-1']?.furthestVerseNumber).toBe(1);
  });

  it('resets safely when stored data is corrupt without writing on load', async () => {
    const storage = new MemoryLocalStorage();
    storage.seed(READING_PROGRESS_STORAGE_KEY, '{not-json');
    const { service } = createService(storage);

    const progress = await service.getReadingProgress();
    expect(progress).toEqual({
      schemaVersion: 1,
      lastRead: null,
      chapters: {},
    });
    expect(storage.setItemCalls).toHaveLength(0);
    expect(storage.peek(READING_PROGRESS_STORAGE_KEY)).toBe('{not-json');
  });

  it('returns empty progress on storage read failure without writing', async () => {
    const storage = new MemoryLocalStorage();
    storage.seed(
      READING_PROGRESS_STORAGE_KEY,
      JSON.stringify({
        schemaVersion: 1,
        lastRead: null,
        chapters: {},
      } satisfies ReadingProgressDocument),
    );
    storage.getItemFailure = new Error('disk unavailable');
    const { service } = createService(storage);

    const progress = await service.getReadingProgress();
    expect(progress.lastRead).toBeNull();
    expect(storage.setItemCalls).toHaveLength(0);
  });

  it('does not write after read_error and preserves seeded multi-chapter JSON', async () => {
    const storage = new MemoryLocalStorage();
    const seededJson = serializeReadingProgressDocument(MULTI_CHAPTER_DOCUMENT);
    storage.seed(READING_PROGRESS_STORAGE_KEY, seededJson);
    const { service } = createService(storage);

    storage.getItemFailure = new Error('transient read');
    const failed = await service.recordVerseOpened(VERSE_1_1);

    expect(failed).toEqual({
      persisted: false,
      progress: {
        schemaVersion: 1,
        lastRead: null,
        chapters: {},
      },
      reason: 'read_error',
    });
    expect(storage.setItemCalls).toHaveLength(0);
    expect(storage.peek(READING_PROGRESS_STORAGE_KEY)).toBe(seededJson);

    storage.getItemFailure = null;
    const recovered = await service.recordVerseOpened(VERSE_1_2);

    expect(recovered.persisted).toBe(true);
    expect(recovered.progress.lastRead?.canonicalReference).toBe('1.2');
    expect(recovered.progress.chapters['chapter-1']?.furthestVerseNumber).toBe(
      2,
    );
    expect(recovered.progress.chapters['chapter-2']?.furthestVerseNumber).toBe(
      1,
    );
    expect(recovered.progress.chapters['chapter-2']?.furthestCanonicalReference).toBe(
      '2.1',
    );
  });

  it('returns persisted=false with prior document on write failure', async () => {
    const storage = new MemoryLocalStorage();
    const { service } = createService(storage);
    const first = await service.recordVerseOpened(VERSE_1_1);
    expect(first.persisted).toBe(true);

    const before = storage.peek(READING_PROGRESS_STORAGE_KEY);
    storage.setItemFailure = new Error('write failed');

    const failed = await service.recordVerseOpened(VERSE_1_2);

    expect(failed.persisted).toBe(false);
    if (failed.persisted) {
      throw new Error('expected write_error result');
    }
    expect(failed.reason).toBe('write_error');
    expect(failed.progress).toEqual(first.progress);
    expect(failed.progress.lastRead?.canonicalReference).toBe('1.1');
    expect(storage.peek(READING_PROGRESS_STORAGE_KEY)).toBe(before);
  });

  it('continues the mutation queue after a failed write', async () => {
    const storage = new MemoryLocalStorage();
    const repository = new LocalReadingProgressRepository(storage);
    const service = new ReadingProgressService(repository, () => FIXED_NOW);
    await service.recordVerseOpened(VERSE_1_1);

    let releaseFailingSave: (() => void) | undefined;
    const failingSaveGate = new Promise<void>((resolve) => {
      releaseFailingSave = resolve;
    });
    let saveAttempts = 0;
    const originalSave = repository.save.bind(repository);
    repository.save = async (document) => {
      saveAttempts += 1;
      if (saveAttempts === 1) {
        await failingSaveGate;
        throw new Error('transient');
      }
      await originalSave(document);
    };

    const failing = service.recordVerseOpened(VERSE_1_2);
    const recovering = service.recordVerseOpened(VERSE_2_1);

    await waitForCondition(() => saveAttempts === 1);
    releaseFailingSave!();

    const failed = await failing;
    expect(failed.persisted).toBe(false);
    if (!failed.persisted) {
      expect(failed.reason).toBe('write_error');
      expect(failed.progress.lastRead?.canonicalReference).toBe('1.1');
    }

    const recovered = await recovering;
    expect(recovered.persisted).toBe(true);
    expect(recovered.progress.lastRead?.canonicalReference).toBe('2.1');
    expect(recovered.progress.chapters['chapter-2']?.furthestVerseNumber).toBe(
      1,
    );
    expect(recovered.progress.chapters['chapter-1']?.furthestVerseNumber).toBe(
      1,
    );

    const persisted = JSON.parse(
      storage.peek(READING_PROGRESS_STORAGE_KEY)!,
    ) as ReadingProgressDocument;
    expect(persisted.lastRead?.canonicalReference).toBe('2.1');
  });

  it('serializes overlapping recordVerseOpened calls in invocation order', async () => {
    const storage = new MemoryLocalStorage();
    const saveOrder: string[] = [];
    const repository = new LocalReadingProgressRepository(storage);

    let releaseFirstSave: (() => void) | undefined;
    const firstSaveGate = new Promise<void>((resolve) => {
      releaseFirstSave = resolve;
    });
    let saveCount = 0;

    const originalSave = repository.save.bind(repository);
    repository.save = async (document) => {
      saveCount += 1;
      saveOrder.push(document.lastRead!.canonicalReference);
      if (saveCount === 1) {
        await firstSaveGate;
      }
      await originalSave(document);
    };

    const service = new ReadingProgressService(repository, () => FIXED_NOW);

    const first = service.recordVerseOpened(VERSE_1_1);
    const second = service.recordVerseOpened(VERSE_1_2);

    await waitForCondition(() => saveOrder.length === 1);
    expect(saveOrder).toEqual(['1.1']);

    releaseFirstSave!();
    await first;
    await second;

    expect(saveOrder).toEqual(['1.1', '1.2']);
    const progress = await service.getReadingProgress();
    expect(progress.lastRead?.canonicalReference).toBe('1.2');
    expect(progress.chapters['chapter-1']?.furthestVerseNumber).toBe(2);
  });

  it('clearReadingProgress returns cleared=true and resets state', async () => {
    const { service } = createService();
    await service.recordVerseOpened(VERSE_1_1);
    const cleared = await service.clearReadingProgress();
    expect(cleared).toEqual({ cleared: true });
    expect(await service.getReadingProgress()).toEqual({
      schemaVersion: 1,
      lastRead: null,
      chapters: {},
    });
  });

  it('clearReadingProgress returns cleared=false on storage failure', async () => {
    const storage = new MemoryLocalStorage();
    const { service } = createService(storage);
    await service.recordVerseOpened(VERSE_1_1);
    storage.removeItemFailure = new Error('clear failed');

    const result = await service.clearReadingProgress();
    expect(result).toEqual({ cleared: false, reason: 'clear_error' });
    expect(storage.peek(READING_PROGRESS_STORAGE_KEY)).not.toBeNull();
  });

  it('uses UTC ISO-8601 timestamps from the injected clock', async () => {
    const { service } = createService();
    const result = await service.recordVerseOpened(VERSE_1_1);
    expect(result.progress.lastRead?.openedAt).toBe(
      '2026-08-05T18:00:00.000Z',
    );
    expect(result.progress.lastRead?.openedAt.endsWith('Z')).toBe(true);
  });

  it('rejects invalid inputs before touching storage', async () => {
    const storage = new MemoryLocalStorage();
    const { service } = createService(storage);

    await expect(
      service.recordVerseOpened({
        ...VERSE_1_1,
        verseId: '  ',
      }),
    ).rejects.toBeInstanceOf(ReadingProgressValidationError);

    await expect(
      service.recordVerseOpened({
        ...VERSE_1_1,
        chapterNumber: 0,
      }),
    ).rejects.toBeInstanceOf(ReadingProgressValidationError);

    await expect(
      service.recordVerseOpened({
        ...VERSE_1_1,
        verseNumber: Number.NaN,
      }),
    ).rejects.toBeInstanceOf(ReadingProgressValidationError);

    await expect(
      service.recordVerseOpened({
        ...VERSE_1_1,
        canonicalReference: '1.2',
      }),
    ).rejects.toBeInstanceOf(ReadingProgressValidationError);

    expect(storage.setItemCalls).toHaveLength(0);
  });

  it('getChapterProgress returns null for unknown chapters', async () => {
    const { service } = createService();
    await service.recordVerseOpened(VERSE_1_1);
    expect(await service.getChapterProgress('missing')).toBeNull();
    expect(await service.getChapterProgress('chapter-1')).toMatchObject({
      furthestVerseNumber: 1,
    });
  });
});
