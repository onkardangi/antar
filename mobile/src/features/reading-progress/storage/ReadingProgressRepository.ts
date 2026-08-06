import type {
  ReadingProgressDocument,
  ReadingProgressLoadResult,
} from '../model/readingProgressTypes';

/**
 * Persistence port for the versioned Reading Progress document.
 */
export interface ReadingProgressRepository {
  load(): Promise<ReadingProgressLoadResult>;
  save(document: ReadingProgressDocument): Promise<void>;
  clear(): Promise<void>;
}
