import { apiGet, type ApiClientOptions } from '../../../services/api/apiClient';
import type { VerseDetail } from '../model/verseTypes';

/**
 * Fetches a single published Verse with imported Sanskrit.
 */
export async function getVerse(
  verseId: string,
  options: ApiClientOptions = {},
): Promise<VerseDetail> {
  return apiGet<VerseDetail>(`/api/v1/scripture/verses/${verseId}`, options);
}
