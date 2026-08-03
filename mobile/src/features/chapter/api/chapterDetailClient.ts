import { apiGet, type ApiClientOptions } from '../../../services/api/apiClient';
import type {
  ChapterDetail,
  VerseListItem,
  VerseListResponse,
} from '../model/chapterTypes';

/**
 * Fetches a single Chapter by id.
 */
export async function getChapter(
  chapterId: string,
  options: ApiClientOptions = {},
): Promise<ChapterDetail> {
  return apiGet<ChapterDetail>(`/api/v1/scripture/chapters/${chapterId}`, options);
}

/**
 * Fetches verses for a Chapter.
 *
 * Backend canonical order is authoritative. This client does not re-sort items
 * so an ordering regression from the API remains visible to the UI and tests.
 */
export async function listChapterVerses(
  chapterId: string,
  options: ApiClientOptions = {},
): Promise<VerseListItem[]> {
  const response = await apiGet<VerseListResponse>(
    `/api/v1/scripture/chapters/${chapterId}/verses`,
    options,
  );
  return response.items;
}
