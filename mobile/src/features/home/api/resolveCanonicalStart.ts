import { listChapterVerses } from '../../chapter/api/chapterDetailClient';
import type { VerseListItem } from '../../chapter/model/chapterTypes';
import { listChapters } from '../../library/api/chapterClient';
import type { Chapter } from '../../library/model/chapterTypes';
import type { InvitationVerseDestination } from '../model/todaysInvitation';

export type ResolveCanonicalStartDeps = {
  loadChapters?: () => Promise<Chapter[]>;
  loadChapterVerses?: (chapterId: string) => Promise<VerseListItem[]>;
};

/**
 * Resolves Bhagavad Gita 1.1 through existing Scripture list APIs.
 * Never hardcodes database UUIDs.
 *
 * Returns null when Chapter 1 or Verse 1 cannot be found (including network failure).
 */
export async function resolveCanonicalStart(
  deps: ResolveCanonicalStartDeps = {},
): Promise<InvitationVerseDestination | null> {
  const loadChapters = deps.loadChapters ?? listChapters;
  const loadChapterVerses = deps.loadChapterVerses ?? listChapterVerses;

  try {
    const chapters = await loadChapters();
    const chapterOne = chapters.find((chapter) => chapter.chapterNumber === 1);
    if (chapterOne == null) {
      return null;
    }

    const verses = await loadChapterVerses(chapterOne.id);
    const verseOne =
      verses.find((verse) => verse.verseNumber === 1) ??
      verses.find((verse) => verse.canonicalReference === '1.1');
    if (verseOne == null) {
      return null;
    }

    return {
      verseId: verseOne.id,
      verseNumber: verseOne.verseNumber,
      chapterNumber: chapterOne.chapterNumber,
    };
  } catch {
    return null;
  }
}
