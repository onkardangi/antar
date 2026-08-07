import { emptyReadingProgressDocument } from '../../reading-progress/model/readingProgressTypes';
import type { ReadingProgressLoadResult } from '../../reading-progress/model/readingProgressTypes';
import { interpretProgressLoad } from '../application/interpretProgressLoad';

describe('interpretProgressLoad', () => {
  it('maps missing progress to begin_journey', () => {
    const load: ReadingProgressLoadResult = {
      source: 'missing',
      document: emptyReadingProgressDocument(),
    };
    expect(interpretProgressLoad(load)).toEqual({ kind: 'begin_journey' });
  });

  it('maps corrupt progress to begin_journey without requiring lastRead', () => {
    const load: ReadingProgressLoadResult = {
      source: 'corrupt',
      document: emptyReadingProgressDocument(),
    };
    expect(interpretProgressLoad(load)).toEqual({ kind: 'begin_journey' });
  });

  it('maps valid lastRead to continue_reading using lastRead, not furthest', () => {
    const load: ReadingProgressLoadResult = {
      source: 'ok',
      document: {
        schemaVersion: 1,
        lastRead: {
          verseId: 'verse-12',
          chapterId: 'chapter-1',
          chapterNumber: 1,
          verseNumber: 12,
          canonicalReference: '1.12',
          openedAt: '2026-08-05T18:00:00.000Z',
        },
        chapters: {
          'chapter-1': {
            chapterId: 'chapter-1',
            chapterNumber: 1,
            furthestVerseId: 'verse-40',
            furthestVerseNumber: 40,
            furthestCanonicalReference: '1.40',
            updatedAt: '2026-08-05T18:00:00.000Z',
          },
        },
      },
    };

    expect(interpretProgressLoad(load)).toEqual({
      kind: 'continue_reading',
      destination: {
        verseId: 'verse-12',
        verseNumber: 12,
        chapterNumber: 1,
      },
    });
  });

  it('maps read_error to progress_unavailable, not begin_journey', () => {
    const load: ReadingProgressLoadResult = {
      source: 'read_error',
      document: emptyReadingProgressDocument(),
    };
    expect(interpretProgressLoad(load)).toEqual({
      kind: 'progress_unavailable',
    });
  });

  it('maps valid empty document to begin_journey', () => {
    const load: ReadingProgressLoadResult = {
      source: 'ok',
      document: emptyReadingProgressDocument(),
    };
    expect(interpretProgressLoad(load)).toEqual({ kind: 'begin_journey' });
  });
});
