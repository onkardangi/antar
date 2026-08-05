import { getVerse } from './verseClient';
import type { VerseDetail } from '../model/verseTypes';

describe('verseClient', () => {
  it('requests a verse by id', async () => {
    const verse: VerseDetail = {
      id: 'verse-1',
      chapterId: 'chapter-1',
      chapterNumber: 1,
      verseNumber: 1,
      canonicalReference: '1.1',
      sanskritText: 'धर्मक्षेत्रे कुरुक्षेत्रे',
      contentVersion: 2,
    };

    const fetchImpl = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => verse,
    });

    const result = await getVerse('verse-1', {
      baseUrl: 'http://localhost:8080',
      fetchImpl: fetchImpl as unknown as typeof fetch,
    });

    expect(fetchImpl).toHaveBeenCalledWith(
      'http://localhost:8080/api/v1/scripture/verses/verse-1',
      {
        method: 'GET',
        headers: { Accept: 'application/json' },
      },
    );
    expect(result).toEqual(verse);
  });
});
