import { act, fireEvent, screen, waitFor } from '@testing-library/react-native';
import type { ComponentProps } from 'react';

import { VerseScreen } from './VerseScreen';
import { renderWithProviders } from '../../../test/renderWithProviders';
import type { ReadingProgressService } from '../../reading-progress/application/ReadingProgressService';
import type { VerseListItem } from '../../chapter/model/chapterTypes';
import type { VerseDetail } from '../model/verseTypes';

type VerseProps = ComponentProps<typeof VerseScreen>;

const VERSE_1: VerseDetail = {
  id: 'verse-1',
  chapterId: 'chapter-1',
  chapterNumber: 1,
  verseNumber: 1,
  canonicalReference: '1.1',
  sanskritText: 'धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।',
  contentVersion: 2,
};

const VERSE_2: VerseDetail = {
  id: 'verse-2',
  chapterId: 'chapter-1',
  chapterNumber: 1,
  verseNumber: 2,
  canonicalReference: '1.2',
  sanskritText: 'सञ्जय उवाच दृष्ट्वा तु पाण्डवानीकम्।',
  contentVersion: 2,
};

const VERSES: VerseListItem[] = [
  {
    id: 'verse-1',
    verseNumber: 1,
    canonicalReference: '1.1',
    previewText: 'Verse preview unavailable',
  },
  {
    id: 'verse-2',
    verseNumber: 2,
    canonicalReference: '1.2',
    previewText: 'Verse preview unavailable',
  },
  {
    id: 'verse-3',
    verseNumber: 3,
    canonicalReference: '1.3',
    previewText: 'Verse preview unavailable',
  },
];

function createProgressServiceMock(): ReadingProgressService {
  return {
    recordVerseOpened: jest.fn(async () => ({
      persisted: true as const,
      progress: {
        schemaVersion: 1 as const,
        lastRead: null,
        chapters: {},
      },
    })),
    getReadingProgress: jest.fn(),
    getLastRead: jest.fn(),
    getChapterProgress: jest.fn(),
    clearReadingProgress: jest.fn(),
  } as unknown as ReadingProgressService;
}

function createNavigationMock(
  overrides: Partial<{ canGoBack: boolean; setParams: jest.Mock }> = {},
): VerseProps['navigation'] {
  const canGoBack = overrides.canGoBack ?? true;
  return {
    navigate: jest.fn(),
    goBack: jest.fn(),
    setParams: overrides.setParams ?? jest.fn(),
    canGoBack: jest.fn(() => canGoBack),
  } as unknown as VerseProps['navigation'];
}

function renderVerse(
  options: {
    verseId?: string;
    verseNumber?: number;
    chapterNumber?: number;
    loadVerse?: (verseId: string) => Promise<VerseDetail>;
    loadChapterVerses?: (chapterId: string) => Promise<VerseListItem[]>;
    navigation?: VerseProps['navigation'];
    readingProgressService?: ReadingProgressService;
  } = {},
) {
  const navigation = options.navigation ?? createNavigationMock();
  const verseId = options.verseId ?? VERSE_1.id;
  const verseNumber = options.verseNumber ?? VERSE_1.verseNumber;
  const chapterNumber = options.chapterNumber ?? VERSE_1.chapterNumber;
  const readingProgressService =
    options.readingProgressService ?? createProgressServiceMock();

  return {
    navigation,
    readingProgressService,
    ...renderWithProviders(
      <VerseScreen
        navigation={navigation}
        route={{
          key: 'VerseReader',
          name: 'VerseReader',
          params: { verseId, verseNumber, chapterNumber },
        }}
        loadVerse={
          options.loadVerse
          ?? (async (id) => (id === VERSE_2.id ? VERSE_2 : VERSE_1))
        }
        loadChapterVerses={options.loadChapterVerses ?? (async () => VERSES)}
        readingProgressService={readingProgressService}
      />,
      { readingProgressService },
    ),
  };
}

describe('VerseScreen', () => {
  it('shows a centered loading state while the verse loads', async () => {
    let resolveVerse: ((value: VerseDetail) => void) | undefined;
    const pending = new Promise<VerseDetail>((resolve) => {
      resolveVerse = resolve;
    });
    const progress = createProgressServiceMock();

    renderVerse({
      loadVerse: () => pending,
      readingProgressService: progress,
    });

    expect(screen.getByTestId('verse-loading')).toBeTruthy();
    expect(screen.getByLabelText('Loading verse')).toBeTruthy();
    expect(progress.recordVerseOpened).not.toHaveBeenCalled();

    await act(async () => {
      resolveVerse?.(VERSE_1);
    });
    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });
  });

  it('renders Sanskrit and disables Previous on the first verse', async () => {
    renderVerse();

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });

    expect(screen.getByTestId('verse-chapter-label')).toHaveTextContent('Chapter 1');
    expect(screen.getByTestId('verse-number-label')).toHaveTextContent('Verse 1');
    expect(screen.getByTestId('verse-canonical-reference')).toHaveTextContent('1.1');
    expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(VERSE_1.sanskritText);
    expect(screen.getByLabelText('Previous verse')).toBeDisabled();
    expect(screen.getByLabelText('Next verse')).toBeEnabled();
    expect(screen.queryByText('Verse reading will arrive')).toBeNull();
  });

  it('records progress after a successful Verse load', async () => {
    const progress = createProgressServiceMock();
    renderVerse({
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });

    expect(progress.recordVerseOpened).toHaveBeenCalledTimes(1);
    expect(progress.recordVerseOpened).toHaveBeenCalledWith({
      verseId: 'verse-1',
      chapterId: 'chapter-1',
      chapterNumber: 1,
      verseNumber: 1,
      canonicalReference: '1.1',
    });
  });

  it('does not record progress while loading', async () => {
    const progress = createProgressServiceMock();
    const pending = new Promise<VerseDetail>(() => {});
    renderVerse({
      loadVerse: () => pending,
      readingProgressService: progress,
    });

    expect(screen.getByTestId('verse-loading')).toBeTruthy();
    expect(progress.recordVerseOpened).not.toHaveBeenCalled();
  });

  it('does not record progress on API failure', async () => {
    const progress = createProgressServiceMock();
    renderVerse({
      loadVerse: async () => {
        throw new Error('RESOURCE_NOT_FOUND');
      },
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-error')).toBeTruthy();
    });
    expect(progress.recordVerseOpened).not.toHaveBeenCalled();
  });

  it('does not record progress when Sanskrit is missing', async () => {
    const progress = createProgressServiceMock();
    renderVerse({
      loadVerse: async () => ({ ...VERSE_1, sanskritText: '   ' }),
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-error')).toBeTruthy();
    });
    expect(progress.recordVerseOpened).not.toHaveBeenCalled();
  });

  it('navigates to the next verse within the chapter', async () => {
    const setParams = jest.fn();
    const navigation = createNavigationMock({ setParams });

    renderVerse({ navigation });

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });

    fireEvent.press(screen.getByLabelText('Next verse'));

    expect(setParams).toHaveBeenCalledWith({
      verseId: 'verse-2',
      verseNumber: 2,
      chapterNumber: 1,
    });
  });

  it('records progress for a newly loaded Verse after Previous/Next', async () => {
    const progress = createProgressServiceMock();
    const navigation = createNavigationMock();

    const first = renderVerse({
      navigation,
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });
    expect(progress.recordVerseOpened).toHaveBeenLastCalledWith(
      expect.objectContaining({ canonicalReference: '1.1' }),
    );

    first.unmount();

    renderVerse({
      verseId: VERSE_2.id,
      verseNumber: 2,
      navigation,
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(
        VERSE_2.sanskritText,
      );
    });
    expect(progress.recordVerseOpened).toHaveBeenLastCalledWith(
      expect.objectContaining({
        verseId: 'verse-2',
        canonicalReference: '1.2',
      }),
    );
  });

  it('ignores a stale Verse response and does not record it', async () => {
    const progress = createProgressServiceMock();
    let resolveFirst: ((value: VerseDetail) => void) | undefined;
    const firstPending = new Promise<VerseDetail>((resolve) => {
      resolveFirst = resolve;
    });

    let call = 0;
    const loadVerse = jest.fn(async (id: string) => {
      call += 1;
      if (call === 1) {
        return firstPending;
      }
      return id === VERSE_2.id ? VERSE_2 : VERSE_1;
    });

    const { rerender, readingProgressService } = renderVerse({
      loadVerse,
      readingProgressService: progress,
    });

    expect(screen.getByTestId('verse-loading')).toBeTruthy();

    rerender(
      <VerseScreen
        navigation={createNavigationMock()}
        route={{
          key: 'VerseReader',
          name: 'VerseReader',
          params: {
            verseId: VERSE_2.id,
            verseNumber: 2,
            chapterNumber: 1,
          },
        }}
        loadVerse={loadVerse}
        loadChapterVerses={async () => VERSES}
        readingProgressService={readingProgressService}
      />,
    );

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });
    expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(
      VERSE_2.sanskritText,
    );
    expect(progress.recordVerseOpened).toHaveBeenCalledTimes(1);
    expect(progress.recordVerseOpened).toHaveBeenCalledWith(
      expect.objectContaining({ canonicalReference: '1.2' }),
    );

    await act(async () => {
      resolveFirst?.(VERSE_1);
    });

    expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(
      VERSE_2.sanskritText,
    );
    expect(progress.recordVerseOpened).toHaveBeenCalledTimes(1);
  });

  it('still renders Sanskrit when progress storage fails', async () => {
    const progress = createProgressServiceMock();
    (progress.recordVerseOpened as jest.Mock).mockRejectedValue(
      new Error('storage down'),
    );

    renderVerse({
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });
    expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(
      VERSE_1.sanskritText,
    );
  });

  it('does not add Reading Progress UI', async () => {
    renderVerse();

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });

    expect(screen.queryByText(/continue reading/i)).toBeNull();
    expect(screen.queryByTestId(/progress/i)).toBeNull();
  });

  it('disables Next on the last verse and enables Previous', async () => {
    renderVerse({
      verseId: 'verse-3',
      verseNumber: 3,
      loadVerse: async () => ({
        ...VERSE_1,
        id: 'verse-3',
        verseNumber: 3,
        canonicalReference: '1.3',
        sanskritText: 'पश्यैतां पाण्डुपुत्राणाम्।',
      }),
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });

    expect(screen.getByLabelText('Previous verse')).toBeEnabled();
    expect(screen.getByLabelText('Next verse')).toBeDisabled();
  });

  it('shows a friendly error with retry and no raw backend message', async () => {
    const loadVerse = jest
      .fn()
      .mockRejectedValueOnce(new Error('RESOURCE_NOT_FOUND: boom'))
      .mockResolvedValueOnce(VERSE_1);

    renderVerse({ loadVerse });

    await waitFor(() => {
      expect(screen.getByTestId('verse-error')).toBeTruthy();
    });

    expect(screen.getByText('Unable to load this verse.')).toBeTruthy();
    expect(screen.getByText('Please try again.')).toBeTruthy();
    expect(screen.queryByText(/RESOURCE_NOT_FOUND/)).toBeNull();
    expect(screen.queryByText(/boom/)).toBeNull();

    fireEvent.press(screen.getByTestId('verse-retry'));

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });
    expect(loadVerse).toHaveBeenCalledTimes(2);
  });

  it('exposes Back and heading accessibility', async () => {
    const navigation = createNavigationMock();
    renderVerse({ navigation });

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });

    expect(screen.getByLabelText('Go back')).toBeTruthy();
    expect(screen.getByRole('header', { name: 'Chapter 1' })).toBeTruthy();
    fireEvent.press(screen.getByLabelText('Go back'));
    expect(navigation.goBack).toHaveBeenCalled();
  });
});
