import { ApiError } from '../../../services/api/apiError';
import { getVerseTranslation, parseVerseTranslation } from './translationClient';
import type { VerseTranslation } from '../model/translationTypes';

const TRANSLATION: VerseTranslation = {
  id: 'translation-1',
  verseId: 'verse-1',
  language: 'en',
  provider: 'FIXTURE_PROVIDER',
  translationText: 'FIXTURE_TRANSLATION_VERSE_1',
  contentVersion: 1,
};

describe('translationClient', () => {
  it('requests a translation by verse id', async () => {
    const fetchImpl = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => TRANSLATION,
    });

    const result = await getVerseTranslation('verse-1', {
      baseUrl: 'http://localhost:8080',
      fetchImpl: fetchImpl as unknown as typeof fetch,
    });

    expect(fetchImpl).toHaveBeenCalledWith(
      'http://localhost:8080/api/v1/translations/verses/verse-1',
      {
        method: 'GET',
        headers: { Accept: 'application/json' },
      },
    );
    expect(result).toEqual(TRANSLATION);
  });

  it('parses a successful response payload', () => {
    expect(parseVerseTranslation(TRANSLATION)).toEqual(TRANSLATION);
  });

  it('surfaces HTTP 404 as ApiError', async () => {
    const fetchImpl = jest.fn().mockResolvedValue({
      ok: false,
      status: 404,
      json: async () => ({ code: 'RESOURCE_NOT_FOUND' }),
    });

    await expect(
      getVerseTranslation('verse-missing', {
        baseUrl: 'http://localhost:8080',
        fetchImpl: fetchImpl as unknown as typeof fetch,
      }),
    ).rejects.toMatchObject({
      name: 'ApiError',
      kind: 'http',
      status: 404,
    } satisfies Partial<ApiError>);
  });

  it('surfaces network failure as ApiError', async () => {
    const fetchImpl = jest.fn().mockRejectedValue(new Error('offline'));

    await expect(
      getVerseTranslation('verse-1', {
        baseUrl: 'http://localhost:8080',
        fetchImpl: fetchImpl as unknown as typeof fetch,
      }),
    ).rejects.toMatchObject({
      name: 'ApiError',
      kind: 'network',
    } satisfies Partial<ApiError>);
  });

  it('rejects an invalid response shape as parse failure', () => {
    expect(() =>
      parseVerseTranslation({
        id: 'translation-1',
        verseId: 'verse-1',
        language: 'en',
        provider: 'FIXTURE_PROVIDER',
        // missing translationText
        contentVersion: 1,
      }),
    ).toThrow(ApiError);

    try {
      parseVerseTranslation({ id: 1 });
    } catch (error) {
      expect(error).toBeInstanceOf(ApiError);
      expect((error as ApiError).kind).toBe('parse');
    }
  });

  it('rejects a response verseId that does not match the requested verseId', async () => {
    const fetchImpl = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        ...TRANSLATION,
        verseId: 'verse-other',
      }),
    });

    await expect(
      getVerseTranslation('verse-1', {
        baseUrl: 'http://localhost:8080',
        fetchImpl: fetchImpl as unknown as typeof fetch,
      }),
    ).rejects.toMatchObject({
      name: 'ApiError',
      kind: 'parse',
    } satisfies Partial<ApiError>);
  });

  it('accepts a response verseId that matches the requested verseId', () => {
    expect(parseVerseTranslation(TRANSLATION, 'verse-1')).toEqual(TRANSLATION);
  });
});
