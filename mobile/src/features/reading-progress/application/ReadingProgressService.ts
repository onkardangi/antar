import {
  emptyReadingProgressDocument,
  type ChapterReadingProgress,
  type Clock,
  type LastReadVerse,
  type ReadingProgressClearResult,
  type ReadingProgressDocument,
  type ReadingProgressMutationResult,
  type RecordVerseOpenedInput,
} from '../model/readingProgressTypes';
import type { ReadingProgressRepository } from '../storage/ReadingProgressRepository';

export class ReadingProgressValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ReadingProgressValidationError';
  }
}

/**
 * Application service for local-only Reading Progress.
 *
 * Mutations are serialized so rapid Previous/Next navigation cannot
 * lose a later open behind a slower earlier write.
 */
export class ReadingProgressService {
  private mutationTail: Promise<unknown> = Promise.resolve();

  constructor(
    private readonly repository: ReadingProgressRepository,
    private readonly clock: Clock = () => new Date(),
  ) {}

  async recordVerseOpened(
    input: RecordVerseOpenedInput,
  ): Promise<ReadingProgressMutationResult> {
    const validated = validateRecordVerseOpenedInput(input);
    return this.enqueueMutation(async () => {
      const loaded = await this.repository.load();

      if (loaded.source === 'read_error') {
        return {
          persisted: false,
          progress: emptyReadingProgressDocument(),
          reason: 'read_error',
        };
      }

      const now = this.clock().toISOString();
      const lastRead: LastReadVerse = {
        ...validated,
        openedAt: now,
      };

      const previousChapter = loaded.document.chapters[validated.chapterId];
      const shouldAdvanceFurthest =
        previousChapter == null ||
        validated.verseNumber > previousChapter.furthestVerseNumber;

      const chapterProgress: ChapterReadingProgress = shouldAdvanceFurthest
        ? {
            chapterId: validated.chapterId,
            chapterNumber: validated.chapterNumber,
            furthestVerseId: validated.verseId,
            furthestVerseNumber: validated.verseNumber,
            furthestCanonicalReference: validated.canonicalReference,
            updatedAt: now,
          }
        : previousChapter;

      const next: ReadingProgressDocument = {
        schemaVersion: 1,
        lastRead,
        chapters: {
          ...loaded.document.chapters,
          [validated.chapterId]: chapterProgress,
        },
      };

      try {
        await this.repository.save(next);
        return {
          persisted: true,
          progress: next,
        };
      } catch {
        return {
          persisted: false,
          progress: loaded.document,
          reason: 'write_error',
        };
      }
    });
  }

  async getReadingProgress(): Promise<ReadingProgressDocument> {
    const loaded = await this.repository.load();
    return loaded.document;
  }

  async getLastRead(): Promise<LastReadVerse | null> {
    const progress = await this.getReadingProgress();
    return progress.lastRead;
  }

  async getChapterProgress(
    chapterId: string,
  ): Promise<ChapterReadingProgress | null> {
    if (typeof chapterId !== 'string' || chapterId.trim().length === 0) {
      throw new ReadingProgressValidationError('chapterId must be nonblank');
    }
    const progress = await this.getReadingProgress();
    return progress.chapters[chapterId.trim()] ?? null;
  }

  async clearReadingProgress(): Promise<ReadingProgressClearResult> {
    return this.enqueueMutation(async () => {
      try {
        await this.repository.clear();
        return { cleared: true };
      } catch {
        return { cleared: false, reason: 'clear_error' };
      }
    });
  }

  private enqueueMutation<T>(operation: () => Promise<T>): Promise<T> {
    const run = this.mutationTail.then(operation, operation);
    this.mutationTail = run.then(
      () => undefined,
      () => undefined,
    );
    return run;
  }
}

function validateRecordVerseOpenedInput(
  input: RecordVerseOpenedInput,
): Omit<LastReadVerse, 'openedAt'> {
  if (input == null || typeof input !== 'object') {
    throw new ReadingProgressValidationError('input is required');
  }

  const verseId = requireNonBlank(input.verseId, 'verseId');
  const chapterId = requireNonBlank(input.chapterId, 'chapterId');
  const chapterNumber = requirePositiveInt(input.chapterNumber, 'chapterNumber');
  const verseNumber = requirePositiveInt(input.verseNumber, 'verseNumber');
  const canonicalReference = requireNonBlank(
    input.canonicalReference,
    'canonicalReference',
  );

  const expectedReference = `${chapterNumber}.${verseNumber}`;
  if (canonicalReference !== expectedReference) {
    throw new ReadingProgressValidationError(
      `canonicalReference must equal "${expectedReference}"`,
    );
  }

  return {
    verseId,
    chapterId,
    chapterNumber,
    verseNumber,
    canonicalReference,
  };
}

function requireNonBlank(value: unknown, field: string): string {
  if (typeof value !== 'string' || value.trim().length === 0) {
    throw new ReadingProgressValidationError(`${field} must be nonblank`);
  }
  return value.trim();
}

function requirePositiveInt(value: unknown, field: string): number {
  if (
    typeof value !== 'number' ||
    !Number.isFinite(value) ||
    !Number.isInteger(value) ||
    value <= 0
  ) {
    throw new ReadingProgressValidationError(
      `${field} must be a positive finite integer`,
    );
  }
  return value;
}

export { emptyReadingProgressDocument };
