/**
 * Home-level Today's Invitation state (Milestone A).
 *
 * Storage load sources are never part of this contract.
 */

export type InvitationVerseDestination = {
  verseId: string;
  verseNumber: number;
  chapterNumber: number;
};

/**
 * Resolved invitation ready for HomeScreen.
 * Begin Journey always carries a resolution substate after canonical-start lookup.
 */
export type TodaysInvitationState =
  | { kind: 'progress_unavailable' }
  | {
      kind: 'continue_reading';
      destination: InvitationVerseDestination;
    }
  | {
      kind: 'begin_journey';
      resolution: 'ready';
      destination: InvitationVerseDestination;
    }
  | {
      kind: 'begin_journey';
      resolution: 'unavailable';
    };

/** UI phase including structural loading before interpretation finishes. */
export type HomeInvitationViewState =
  | { kind: 'loading' }
  | TodaysInvitationState;

export function formatInvitationDestination(
  chapterNumber: number,
  verseNumber: number,
): string {
  return `Chapter ${chapterNumber} · Verse ${verseNumber}`;
}

export function continueReadingAccessibilityLabel(
  chapterNumber: number,
  verseNumber: number,
): string {
  return `Continue Reading. Opens Chapter ${chapterNumber}, Verse ${verseNumber}.`;
}

export function beginReadingAccessibilityLabel(
  chapterNumber: number,
  verseNumber: number,
): string {
  return `Begin Reading. Opens Chapter ${chapterNumber}, Verse ${verseNumber}.`;
}
