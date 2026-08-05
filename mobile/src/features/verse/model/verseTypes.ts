/**
 * Verse detail as returned by GET /api/v1/scripture/verses/{verseId}.
 *
 * Sanskrit-only MVP — no Translation, Commentary, or Transliteration.
 */
export type VerseDetail = {
  id: string;
  chapterId: string;
  chapterNumber: number;
  verseNumber: number;
  canonicalReference: string;
  sanskritText: string;
  contentVersion: number;
};
