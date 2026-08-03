import { listChapters } from './chapterClient';
import type { Chapter } from '../model/chapterTypes';

describe('chapterClient', () => {
  it('requests chapters and preserves canonical order', async () => {
    const chapters: Chapter[] = [
      {
        id: '2',
        chapterNumber: 2,
        canonicalName: 'Sankhya Yoga',
        englishName: 'The Yoga of Knowledge',
        shortIntent: 'Action, wisdom, duty, and steadiness.',
        verseCount: 72,
      },
      {
        id: '1',
        chapterNumber: 1,
        canonicalName: 'Arjuna Vishada Yoga',
        englishName: "The Yoga of Arjuna's Despair",
        shortIntent: 'A battlefield crisis becomes the beginning of inquiry.',
        verseCount: 47,
      },
    ];

    const fetchImpl = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ items: chapters }),
    });

    const result = await listChapters({
      baseUrl: 'http://localhost:8080',
      fetchImpl: fetchImpl as unknown as typeof fetch,
    });

    expect(fetchImpl).toHaveBeenCalledWith('http://localhost:8080/api/v1/scripture/chapters', {
      method: 'GET',
      headers: { Accept: 'application/json' },
    });
    expect(result.map((chapter) => chapter.chapterNumber)).toEqual([1, 2]);
  });
});
