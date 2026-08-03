/**
 * Chapter detail as returned by GET /api/v1/scripture/chapters/{chapterId}.
 *
 * UI maps shortIntent to the ChapterIntroduction editorial body.
 * thematicIntroduction is intentionally not used — the approved API field is shortIntent.
 */
export type ChapterDetail = {
  id: string;
  chapterNumber: number;
  canonicalName: string;
  englishName: string;
  shortIntent: string;
  verseCount: number;
};

/**
 * Verse list item as returned by the temporary Chapter-slice response
 * (docs/architecture/04_API_CONTRACTS.md § Temporary implementation status).
 *
 * previewText is rendered literally in the loaded success state — including
 * the temporary value "Verse preview unavailable".
 */
export type VerseListItem = {
  id: string;
  verseNumber: number;
  canonicalReference: string;
  previewText: string;
};

export type VerseListResponse = {
  items: VerseListItem[];
};
