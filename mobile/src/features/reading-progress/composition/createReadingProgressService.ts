import { AsyncStorageAdapter } from '../../../storage/local/AsyncStorageAdapter';
import type { LocalStorage } from '../../../storage/local/LocalStorage';
import {
  ReadingProgressService,
} from '../application/ReadingProgressService';
import type { Clock } from '../model/readingProgressTypes';
import { LocalReadingProgressRepository } from '../storage/LocalReadingProgressRepository';

export type CreateReadingProgressServiceOptions = {
  storage?: LocalStorage;
  clock?: Clock;
};

/**
 * Central production composition for Reading Progress persistence.
 *
 * ReadingProgressService → LocalReadingProgressRepository → AsyncStorageAdapter
 */
export function createReadingProgressService(
  options: CreateReadingProgressServiceOptions = {},
): ReadingProgressService {
  const storage = options.storage ?? new AsyncStorageAdapter();
  const repository = new LocalReadingProgressRepository(storage);
  const clock = options.clock ?? (() => new Date());
  return new ReadingProgressService(repository, clock);
}
