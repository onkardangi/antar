import {
  READING_PROGRESS_SCHEMA_VERSION,
  emptyReadingProgressDocument,
  type ChapterReadingProgress,
  type LastReadVerse,
  type ReadingProgressDocument,
} from '../model/readingProgressTypes';

/** UTC ISO-8601 with optional millis, e.g. 2026-08-05T18:00:00.000Z */
const UTC_ISO_TIMESTAMP =
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?Z$/;

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isNonBlankString(value: unknown): value is string {
  return typeof value === 'string' && value.trim().length > 0;
}

function isPositiveInt(value: unknown): value is number {
  return (
    typeof value === 'number' &&
    Number.isFinite(value) &&
    Number.isInteger(value) &&
    value > 0
  );
}

function isUtcIsoTimestamp(value: unknown): value is string {
  if (!isNonBlankString(value)) {
    return false;
  }
  const trimmed = value.trim();
  if (!UTC_ISO_TIMESTAMP.test(trimmed)) {
    return false;
  }
  return Number.isFinite(Date.parse(trimmed));
}

function expectedCanonicalReference(
  chapterNumber: number,
  verseNumber: number,
): string {
  return `${chapterNumber}.${verseNumber}`;
}

function parseLastRead(value: unknown): LastReadVerse | null | undefined {
  if (value === null) {
    return null;
  }
  if (!isPlainObject(value)) {
    return undefined;
  }
  const {
    verseId,
    chapterId,
    chapterNumber,
    verseNumber,
    canonicalReference,
    openedAt,
  } = value;
  if (
    !isNonBlankString(verseId) ||
    !isNonBlankString(chapterId) ||
    !isPositiveInt(chapterNumber) ||
    !isPositiveInt(verseNumber) ||
    !isNonBlankString(canonicalReference) ||
    !isUtcIsoTimestamp(openedAt)
  ) {
    return undefined;
  }

  const trimmedReference = canonicalReference.trim();
  if (
    trimmedReference !==
    expectedCanonicalReference(chapterNumber, verseNumber)
  ) {
    return undefined;
  }

  return {
    verseId: verseId.trim(),
    chapterId: chapterId.trim(),
    chapterNumber,
    verseNumber,
    canonicalReference: trimmedReference,
    openedAt: openedAt.trim(),
  };
}

function parseChapterProgress(
  value: unknown,
): ChapterReadingProgress | undefined {
  if (!isPlainObject(value)) {
    return undefined;
  }
  const {
    chapterId,
    chapterNumber,
    furthestVerseId,
    furthestVerseNumber,
    furthestCanonicalReference,
    updatedAt,
  } = value;
  if (
    !isNonBlankString(chapterId) ||
    !isPositiveInt(chapterNumber) ||
    !isNonBlankString(furthestVerseId) ||
    !isPositiveInt(furthestVerseNumber) ||
    !isNonBlankString(furthestCanonicalReference) ||
    !isUtcIsoTimestamp(updatedAt)
  ) {
    return undefined;
  }

  const trimmedReference = furthestCanonicalReference.trim();
  if (
    trimmedReference !==
    expectedCanonicalReference(chapterNumber, furthestVerseNumber)
  ) {
    return undefined;
  }

  return {
    chapterId: chapterId.trim(),
    chapterNumber,
    furthestVerseId: furthestVerseId.trim(),
    furthestVerseNumber,
    furthestCanonicalReference: trimmedReference,
    updatedAt: updatedAt.trim(),
  };
}

/**
 * Parses and validates a stored JSON string into a v1 document.
 * Returns null when the payload is corrupt or incompatible.
 */
export function parseReadingProgressDocument(
  raw: string,
): ReadingProgressDocument | null {
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return null;
  }

  if (!isPlainObject(parsed)) {
    return null;
  }

  if (parsed.schemaVersion !== READING_PROGRESS_SCHEMA_VERSION) {
    return null;
  }

  const lastRead = parseLastRead(parsed.lastRead);
  if (lastRead === undefined) {
    return null;
  }

  if (!isPlainObject(parsed.chapters)) {
    return null;
  }

  const chapters: Record<string, ChapterReadingProgress> = {};
  for (const [key, entry] of Object.entries(parsed.chapters)) {
    const chapter = parseChapterProgress(entry);
    if (!chapter || chapter.chapterId !== key) {
      return null;
    }
    chapters[key] = chapter;
  }

  return {
    schemaVersion: READING_PROGRESS_SCHEMA_VERSION,
    lastRead,
    chapters,
  };
}

export function serializeReadingProgressDocument(
  document: ReadingProgressDocument,
): string {
  return JSON.stringify(document);
}

export { emptyReadingProgressDocument };
