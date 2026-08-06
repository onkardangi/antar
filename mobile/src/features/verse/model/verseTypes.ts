/**
 * Verse detail as returned by GET /api/v1/scripture/verses/{verseId}.
 *
 * Sanskrit-only Scripture payload (ADR-012). Translation is fetched separately
 * via GET /api/v1/translations/verses/{verseId} and composed on the client.
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
