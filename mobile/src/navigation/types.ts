export type RootStackParamList = {
  Home: undefined;
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
