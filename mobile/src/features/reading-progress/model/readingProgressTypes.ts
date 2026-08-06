/**
 * Local-only Reading Progress document (schema v1).
 *
 * No Sanskrit, Translation, notes, or Reader identity are stored.
 */
export const READING_PROGRESS_SCHEMA_VERSION = 1 as const;

export type LastReadVerse = {
  verseId: string;
  chapterId: string;
  chapterNumber: number;
  verseNumber: number;
  canonicalReference: string;
  /** UTC ISO-8601 */
  openedAt: string;
};

export type ChapterReadingProgress = {
  chapterId: string;
  chapterNumber: number;
  furthestVerseId: string;
  furthestVerseNumber: number;
  furthestCanonicalReference: string;
  /** UTC ISO-8601 */
  updatedAt: string;
};

export type ReadingProgressDocument = {
  schemaVersion: typeof READING_PROGRESS_SCHEMA_VERSION;
  lastRead: LastReadVerse | null;
  chapters: Record<string, ChapterReadingProgress>;
};

export type RecordVerseOpenedInput = {
  verseId: string;
  chapterId: string;
  chapterNumber: number;
  verseNumber: number;
  canonicalReference: string;
};

export type ReadingProgressLoadSource =
  | 'ok'
  | 'missing'
  | 'corrupt'
  | 'read_error';

export type ReadingProgressLoadResult = {
  document: ReadingProgressDocument;
  source: ReadingProgressLoadSource;
};

/**
 * Truthful outcome of a Reading Progress mutation.
 * `persisted` is true only after storage save succeeds.
 */
export type ReadingProgressMutationResult =
  | {
      persisted: true;
      progress: ReadingProgressDocument;
    }
  | {
      persisted: false;
      progress: ReadingProgressDocument;
      reason: 'read_error' | 'write_error';
    };

/**
 * Truthful outcome of clearReadingProgress.
 * `cleared` is true only after storage remove succeeds.
 */
export type ReadingProgressClearResult =
  | { cleared: true }
  | { cleared: false; reason: 'clear_error' };

export function emptyReadingProgressDocument(): ReadingProgressDocument {
  return {
    schemaVersion: READING_PROGRESS_SCHEMA_VERSION,
    lastRead: null,
    chapters: {},
  };
}

export type Clock = () => Date;
