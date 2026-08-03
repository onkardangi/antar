export type Chapter = {
  id: string;
  chapterNumber: number;
  canonicalName: string;
  englishName: string;
  shortIntent: string;
  verseCount: number;
};

export type ChapterListResponse = {
  items: Chapter[];
};
