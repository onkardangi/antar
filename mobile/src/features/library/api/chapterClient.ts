import { apiGet, type ApiClientOptions } from '../../../services/api/apiClient';
import type { Chapter, ChapterListResponse } from '../model/chapterTypes';

/**
 * Fetches the canonical Chapter list.
 *
 * The API contract returns chapters in canonical order. The client still sorts
 * by chapterNumber as a defensive guard if that contract is violated.
 */
export async function listChapters(options: ApiClientOptions = {}): Promise<Chapter[]> {
  const response = await apiGet<ChapterListResponse>('/api/v1/scripture/chapters', options);
  return [...response.items].sort((left, right) => left.chapterNumber - right.chapterNumber);
}
