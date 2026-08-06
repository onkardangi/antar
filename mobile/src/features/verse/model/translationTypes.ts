/**
 * Published Translation as returned by
 * GET /api/v1/translations/verses/{verseId}.
 *
 * ADR-012: owned by the Translation bounded context. Mobile composes this
 * with Sanskrit; Scripture APIs remain Translation-free.
 *
 * V1 attribution uses `provider`. `sourceName` is deferred until the read
 * API exposes existing source metadata without a schema change.
 */
export type VerseTranslation = {
  id: string;
  verseId: string;
  language: string;
  provider: string;
  translationText: string;
  contentVersion: number;
};
