export type RootStackParamList = {
  Library: undefined;
  Chapter: {
    chapterId: string;
    chapterNumber: number;
  };
  VerseReader: {
    verseId: string;
    verseNumber: number;
    chapterNumber: number;
  };
  FoundationStatus: undefined;
};
