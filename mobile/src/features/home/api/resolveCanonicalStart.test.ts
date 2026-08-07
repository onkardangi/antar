import { resolveCanonicalStart } from './resolveCanonicalStart';

describe('resolveCanonicalStart', () => {
  it('resolves Chapter 1 Verse 1 from list APIs without hardcoded UUIDs', async () => {
    const destination = await resolveCanonicalStart({
      loadChapters: async () => [
        {
          id: 'chapter-id-from-api',
          chapterNumber: 2,
          canonicalName: 'Sankhya Yoga',
          englishName: 'Knowledge',
          shortIntent: 'Intent',
          verseCount: 72,
        },
        {
          id: 'chapter-1-from-api',
          chapterNumber: 1,
          canonicalName: 'Arjuna Vishada Yoga',
          englishName: 'Despair',
          shortIntent: 'Intent',
          verseCount: 47,
        },
      ],
      loadChapterVerses: async (chapterId) => {
        expect(chapterId).toBe('chapter-1-from-api');
        return [
          {
            id: 'verse-1-from-api',
            verseNumber: 1,
            canonicalReference: '1.1',
            previewText: 'preview',
          },
          {
            id: 'verse-2-from-api',
            verseNumber: 2,
            canonicalReference: '1.2',
            previewText: 'preview',
          },
        ];
      },
    });

    expect(destination).toEqual({
      verseId: 'verse-1-from-api',
      verseNumber: 1,
      chapterNumber: 1,
    });
  });

  it('returns null when chapter list fails', async () => {
    const destination = await resolveCanonicalStart({
      loadChapters: async () => {
        throw new Error('network');
      },
      loadChapterVerses: async () => [],
    });
    expect(destination).toBeNull();
  });

  it('returns null when verse 1 is missing', async () => {
    const destination = await resolveCanonicalStart({
      loadChapters: async () => [
        {
          id: 'chapter-1',
          chapterNumber: 1,
          canonicalName: 'Arjuna Vishada Yoga',
          englishName: 'Despair',
          shortIntent: 'Intent',
          verseCount: 47,
        },
      ],
      loadChapterVerses: async () => [
        {
          id: 'verse-2',
          verseNumber: 2,
          canonicalReference: '1.2',
          previewText: 'preview',
        },
      ],
    });
    expect(destination).toBeNull();
  });
});
