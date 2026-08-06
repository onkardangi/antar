import type { LocalStorage } from '../../../storage/local/LocalStorage';
import {
  emptyReadingProgressDocument,
  type ReadingProgressDocument,
  type ReadingProgressLoadResult,
} from '../model/readingProgressTypes';
import type { ReadingProgressRepository } from './ReadingProgressRepository';
import {
  parseReadingProgressDocument,
  serializeReadingProgressDocument,
} from './parseReadingProgressDocument';
import { READING_PROGRESS_STORAGE_KEY } from './readingProgressStorageKey';

/**
 * AsyncStorage-backed Reading Progress repository.
 *
 * Read failures and corrupt data never write an empty document back.
 */
export class LocalReadingProgressRepository implements ReadingProgressRepository {
  constructor(
    private readonly storage: LocalStorage,
    private readonly storageKey: string = READING_PROGRESS_STORAGE_KEY,
  ) {}

  async load(): Promise<ReadingProgressLoadResult> {
    let raw: string | null;
    try {
      raw = await this.storage.getItem(this.storageKey);
    } catch {
      return {
        document: emptyReadingProgressDocument(),
        source: 'read_error',
      };
    }

    if (raw == null) {
      return {
        document: emptyReadingProgressDocument(),
        source: 'missing',
      };
    }

    const parsed = parseReadingProgressDocument(raw);
    if (parsed == null) {
      return {
        document: emptyReadingProgressDocument(),
        source: 'corrupt',
      };
    }

    return {
      document: parsed,
      source: 'ok',
    };
  }

  async save(document: ReadingProgressDocument): Promise<void> {
    await this.storage.setItem(
      this.storageKey,
      serializeReadingProgressDocument(document),
    );
  }

  async clear(): Promise<void> {
    await this.storage.removeItem(this.storageKey);
  }
}
