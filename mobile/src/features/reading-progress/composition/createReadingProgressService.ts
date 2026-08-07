import {
  createReadingProgressStack,
  type CreateReadingProgressStackOptions,
} from './createReadingProgressStack';
import type { ReadingProgressService } from '../application/ReadingProgressService';

export type CreateReadingProgressServiceOptions = CreateReadingProgressStackOptions;

/**
 * Central production composition for Reading Progress persistence.
 *
 * ReadingProgressService → LocalReadingProgressRepository → AsyncStorageAdapter
 *
 * Prefer `createReadingProgressStack` when Home also needs the shared repository
 * for invitation loading without expanding this service's public API.
 */
export function createReadingProgressService(
  options: CreateReadingProgressServiceOptions = {},
): ReadingProgressService {
  return createReadingProgressStack(options).service;
}
