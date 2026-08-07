import type { ReadingProgressLoadResult } from '../../reading-progress/model/readingProgressTypes';
import type { InvitationVerseDestination } from '../model/todaysInvitation';

/**
 * Intermediate Home decision after reading local progress.
 * Not exported as an app-wide product vocabulary — used only by Home loaders.
 */
export type ProgressInvitationDecision =
  | { kind: 'progress_unavailable' }
  | {
      kind: 'continue_reading';
      destination: InvitationVerseDestination;
    }
  | { kind: 'begin_journey' };

/**
 * Maps a repository load result into a Home invitation decision.
 *
 * Storage sources stay inside this Home-owned interpreter. Callers and UI
 * never receive `missing` / `corrupt` / `read_error` enums.
 */
export function interpretProgressLoad(
  load: ReadingProgressLoadResult,
): ProgressInvitationDecision {
  if (load.source === 'read_error') {
    return { kind: 'progress_unavailable' };
  }

  const lastRead = load.document.lastRead;
  if (load.source === 'ok' && lastRead != null) {
    return {
      kind: 'continue_reading',
      destination: {
        verseId: lastRead.verseId,
        verseNumber: lastRead.verseNumber,
        chapterNumber: lastRead.chapterNumber,
      },
    };
  }

  // missing, corrupt, or valid empty document → Begin Journey
  return { kind: 'begin_journey' };
}
