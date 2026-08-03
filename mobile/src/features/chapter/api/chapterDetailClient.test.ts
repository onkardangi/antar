import { getChapter, listChapterVerses } from './chapterDetailClient';
import type { ChapterDetail, VerseListItem } from '../model/chapterTypes';

describe('chapterDetailClient', () => {
  it('requests a chapter by id', async () => {
    const chapter: ChapterDetail = {
      id: 'chapter-2',
      chapterNumber: 2,
      canonicalName: 'Sankhya Yoga',
      englishName: 'The Yoga of Knowledge',
      shortIntent: 'Action, wisdom, duty, and steadiness.',
      verseCount: 72,
    };

    const fetchImpl = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => chapter,
    });

    const result = await getChapter('chapter-2', {
      baseUrl: 'http://localhost:8080',
      fetchImpl: fetchImpl as unknown as typeof fetch,
    });

    expect(fetchImpl).toHaveBeenCalledWith(
      'http://localhost:8080/api/v1/scripture/chapters/chapter-2',
      {
        method: 'GET',
        headers: { Accept: 'application/json' },
      },
    );
    expect(result).toEqual(chapter);
  });

  it('requests verses and preserves backend order without client sorting', async () => {
    const verses: VerseListItem[] = [
      {
        id: 'v-3',
        verseNumber: 3,
        canonicalReference: '2.3',
        previewText: 'Verse preview unavailable',
      },
      {
        id: 'v-1',
        verseNumber: 1,
        canonicalReference: '2.1',
        previewText: 'Verse preview unavailable',
      },
      {
        id: 'v-2',
        verseNumber: 2,
        canonicalReference: '2.2',
        previewText: 'Verse preview unavailable',
      },
    ];

    const fetchImpl = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ items: verses }),
    });

    const result = await listChapterVerses('chapter-2', {
      baseUrl: 'http://localhost:8080',
      fetchImpl: fetchImpl as unknown as typeof fetch,
    });

    expect(fetchImpl).toHaveBeenCalledWith(
      'http://localhost:8080/api/v1/scripture/chapters/chapter-2/verses',
      {
        method: 'GET',
        headers: { Accept: 'application/json' },
      },
    );
    // Unordered API input stays unordered so an ordering regression remains visible.
    expect(result.map((verse) => verse.verseNumber)).toEqual([3, 1, 2]);
  });
});
