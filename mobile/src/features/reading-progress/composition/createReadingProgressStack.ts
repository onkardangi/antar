import { AsyncStorageAdapter } from '../../../storage/local/AsyncStorageAdapter';
import type { LocalStorage } from '../../../storage/local/LocalStorage';
import {
  ReadingProgressService,
} from '../application/ReadingProgressService';
import type { Clock } from '../model/readingProgressTypes';
import { LocalReadingProgressRepository } from '../storage/LocalReadingProgressRepository';
import type { ReadingProgressRepository } from '../storage/ReadingProgressRepository';

export type CreateReadingProgressStackOptions = {
  storage?: LocalStorage;
  clock?: Clock;
  /**
   * Optional repository override for tests. Production omits this so a shared
   * LocalReadingProgressRepository is composed once for service + Home loader.
   */
  repository?: ReadingProgressRepository;
};

export type ReadingProgressStack = {
  service: ReadingProgressService;
  /**
   * Persistence port shared with Home's invitation loader only.
   * Not part of ReadingProgressService's public API.
   */
  repository: ReadingProgressRepository;
};

/**
 * Composes one repository + service pair so Verse mutations and Home's
 * invitation loader observe the same local document.
 */
export function createReadingProgressStack(
  options: CreateReadingProgressStackOptions = {},
): ReadingProgressStack {
  const storage = options.storage ?? new AsyncStorageAdapter();
  const repository =
    options.repository ?? new LocalReadingProgressRepository(storage);
  const clock = options.clock ?? (() => new Date());
  return {
    service: new ReadingProgressService(repository, clock),
    repository,
  };
}
