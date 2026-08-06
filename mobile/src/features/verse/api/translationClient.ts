import { ApiError } from '../../../services/api/apiError';
import { apiGet, type ApiClientOptions } from '../../../services/api/apiClient';
import type { VerseTranslation } from '../model/translationTypes';

function isNonEmptyString(value: unknown): value is string {
  return typeof value === 'string' && value.trim().length > 0;
}

function isFiniteNumber(value: unknown): value is number {
  return typeof value === 'number' && Number.isFinite(value);
}

/**
 * Validates the Translation API payload shape. Malformed success bodies are
 * treated as client parse failures so VerseScreen can map them to unavailable.
 *
 * When `expectedVerseId` is provided, a response whose `verseId` does not match
 * is rejected as a parse failure (wrong Translation must never render).
 */
export function parseVerseTranslation(
  payload: unknown,
  expectedVerseId?: string,
): VerseTranslation {
  if (payload == null || typeof payload !== 'object') {
    throw new ApiError('Backend returned an unreadable translation response.', {
      kind: 'parse',
    });
  }

  const record = payload as Record<string, unknown>;
  if (
    !isNonEmptyString(record.id) ||
    !isNonEmptyString(record.verseId) ||
    !isNonEmptyString(record.language) ||
    !isNonEmptyString(record.provider) ||
    !isNonEmptyString(record.translationText) ||
    !isFiniteNumber(record.contentVersion)
  ) {
    throw new ApiError('Backend returned an unreadable translation response.', {
      kind: 'parse',
    });
  }

  if (
    expectedVerseId != null &&
    record.verseId !== expectedVerseId
  ) {
    throw new ApiError(
      'Backend returned a translation for a different verse.',
      { kind: 'parse' },
    );
  }

  return {
    id: record.id,
    verseId: record.verseId,
    language: record.language,
    provider: record.provider,
    translationText: record.translationText,
    contentVersion: record.contentVersion,
  };
}

/**
 * Fetches the published Translation for a Verse (ADR-012).
 *
 * Callers must treat failures as subordinate to Sanskrit — never as a Verse
 * error. Missing / unpublished translations return HTTP 404 via ApiError.
 * Response `verseId` must match the requested id or the call fails as parse.
 */
export async function getVerseTranslation(
  verseId: string,
  options: ApiClientOptions = {},
): Promise<VerseTranslation> {
  const payload = await apiGet<unknown>(
    `/api/v1/translations/verses/${verseId}`,
    options,
  );
  return parseVerseTranslation(payload, verseId);
}
