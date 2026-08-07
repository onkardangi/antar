import { act, fireEvent, screen, waitFor } from '@testing-library/react-native';
import type { ComponentProps } from 'react';
import type { Metrics } from 'react-native-safe-area-context';

import { VerseScreen } from './VerseScreen';
import { ApiError } from '../../../services/api/apiError';
import {
  TEST_WINDOW_METRICS,
  renderWithProviders,
} from '../../../test/renderWithProviders';
import { verseSpacing } from '../../../design-system';
import type { ReadingProgressService } from '../../reading-progress/application/ReadingProgressService';
import type { VerseListItem } from '../../chapter/model/chapterTypes';
import type { VerseTranslation } from '../model/translationTypes';
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

const TRANSLATION_1: VerseTranslation = {
  id: 'translation-1',
  verseId: 'verse-1',
  language: 'en',
  provider: 'FIXTURE_PROVIDER',
  translationText: 'FIXTURE_TRANSLATION_VERSE_1',
  contentVersion: 1,
};

const TRANSLATION_2: VerseTranslation = {
  id: 'translation-2',
  verseId: 'verse-2',
  language: 'en',
  provider: 'ALPHA_PROVIDER',
  translationText: 'FIXTURE_TRANSLATION_VERSE_2',
  contentVersion: 1,
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

async function defaultUnavailableTranslation(): Promise<VerseTranslation> {
  throw new ApiError('Backend responded with HTTP 404.', {
    kind: 'http',
    status: 404,
  });
}

function renderVerse(
  options: {
    verseId?: string;
    verseNumber?: number;
    chapterNumber?: number;
    loadVerse?: (verseId: string) => Promise<VerseDetail>;
    loadTranslation?: (verseId: string) => Promise<VerseTranslation>;
    loadChapterVerses?: (chapterId: string) => Promise<VerseListItem[]>;
    navigation?: VerseProps['navigation'];
    readingProgressService?: ReadingProgressService;
    initialMetrics?: Metrics;
  } = {},
) {
  const navigation = options.navigation ?? createNavigationMock();
  const verseId = options.verseId ?? VERSE_1.id;
  const verseNumber = options.verseNumber ?? VERSE_1.verseNumber;
  const chapterNumber = options.chapterNumber ?? VERSE_1.chapterNumber;
  const readingProgressService =
    options.readingProgressService ?? createProgressServiceMock();
  const loadTranslation =
    options.loadTranslation ?? defaultUnavailableTranslation;

  return {
    navigation,
    readingProgressService,
    loadTranslation,
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
        loadTranslation={loadTranslation}
        loadChapterVerses={options.loadChapterVerses ?? (async () => VERSES)}
        readingProgressService={readingProgressService}
      />,
      {
        readingProgressService,
        initialMetrics: options.initialMetrics,
      },
    ),
  };
}

function scrollBottomPadding(node: { props: { contentContainerStyle?: unknown } }) {
  const style = node.props.contentContainerStyle;
  const styles = Array.isArray(style) ? style : [style];
  const withPadding = styles.find(
    (entry) =>
      entry != null &&
      typeof entry === 'object' &&
      'paddingBottom' in entry &&
      typeof (entry as { paddingBottom?: unknown }).paddingBottom === 'number',
  ) as { paddingBottom: number } | undefined;
  return withPadding?.paddingBottom;
}

describe('VerseScreen', () => {
  it('uses structural loading in the same ScrollView instead of a full-screen spinner', async () => {
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
    expect(screen.getByTestId('verse-scroll')).toBeTruthy();
    expect(screen.getByTestId('verse-loading-skeleton')).toBeTruthy();
    expect(screen.getByLabelText('Loading verse')).toBeTruthy();
    expect(screen.getAllByLabelText('Loading verse')).toHaveLength(1);
    expect(screen.queryByTestId('verse-loading-indicator')).toBeNull();
    expect(screen.queryByText(/loading translation/i)).toBeNull();
    expect(screen.queryByTestId('verse-translation-loading')).toBeNull();
    expect(screen.queryByTestId('verse-translation-block')).toBeNull();
    expect(screen.getByTestId('verse-reference')).toHaveTextContent(
      'Chapter 1 · Verse 1',
    );
    expect(
      screen.getByTestId('verse-sanskrit-skeleton', {
        includeHiddenElements: true,
      }),
    ).toBeTruthy();
    expect(screen.getByLabelText('Previous verse')).toBeDisabled();
    expect(screen.getByLabelText('Next verse')).toBeDisabled();
    expect(progress.recordVerseOpened).not.toHaveBeenCalled();

    await act(async () => {
      resolveVerse?.(VERSE_1);
    });
    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });

    expect(screen.getByTestId('verse-scroll')).toBeTruthy();
    expect(screen.queryByTestId('verse-loading-skeleton')).toBeNull();
    expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(
      VERSE_1.sanskritText,
    );
  });

  it('hides decorative Sanskrit loading bars from accessibility', async () => {
    const pending = new Promise<VerseDetail>(() => {});
    renderVerse({ loadVerse: () => pending });

    const skeleton = screen.getByTestId('verse-sanskrit-skeleton', {
      includeHiddenElements: true,
    });
    expect(skeleton.props.accessibilityElementsHidden).toBe(true);
    expect(skeleton.props.importantForAccessibility).toBe('no');
  });

  it('renders a quiet combined reference then Sanskrit, with Previous disabled on the first verse', async () => {
    renderVerse();

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });

    expect(screen.getByTestId('verse-reference')).toHaveTextContent(
      'Chapter 1 · Verse 1',
    );
    expect(screen.getByLabelText('Chapter 1, Verse 1')).toBeTruthy();
    expect(screen.queryByTestId('verse-chapter-label')).toBeNull();
    expect(screen.queryByTestId('verse-number-label')).toBeNull();
    expect(screen.queryByTestId('verse-canonical-reference')).toBeNull();
    expect(screen.queryByText('1.1')).toBeNull();
    expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(
      VERSE_1.sanskritText,
    );
    expect(screen.getByLabelText('Previous verse')).toBeDisabled();
    expect(screen.getByLabelText('Next verse')).toBeEnabled();
    expect(screen.queryByText('Verse reading will arrive')).toBeNull();
    expect(screen.queryByText(/commentary/i)).toBeNull();
    expect(screen.queryByText(/saar/i)).toBeNull();
    expect(screen.queryByText(/reflect/i)).toBeNull();
    expect(screen.queryByText(/home/i)).toBeNull();
    expect(screen.queryByText(/transliteration/i)).toBeNull();
  });

  it('renders Sanskrit then Translation with provider attribution', async () => {
    renderVerse({
      loadTranslation: async () => TRANSLATION_1,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-translation-text')).toBeTruthy();
    });

    expect(screen.getByTestId('verse-reading-body')).toBeTruthy();
    expect(screen.getByTestId('verse-sanskrit-text')).toBeTruthy();
    expect(screen.getByTestId('verse-translation-block')).toBeTruthy();
    expect(screen.getByTestId('verse-translation-label')).toHaveTextContent(
      'Translation',
    );
    expect(screen.getByTestId('verse-translation-provider')).toHaveTextContent(
      'FIXTURE_PROVIDER',
    );
    expect(screen.getByTestId('verse-translation-text')).toHaveTextContent(
      'FIXTURE_TRANSLATION_VERSE_1',
    );
    expect(screen.getByTestId('verse-navigation')).toBeTruthy();

    expect(screen.queryByTestId('verse-error')).toBeNull();
    expect(screen.queryByText(/commentary/i)).toBeNull();
    expect(screen.queryByText(/saar/i)).toBeNull();
    expect(screen.queryByText(/reflect/i)).toBeNull();
    expect(screen.queryByText(/continue reading/i)).toBeNull();
  });

  it('shows structural Translation loading under Sanskrit without prose or blocking nav', async () => {
    let resolveTranslation: ((value: VerseTranslation) => void) | undefined;
    const pending = new Promise<VerseTranslation>((resolve) => {
      resolveTranslation = resolve;
    });

    renderVerse({
      loadTranslation: () => pending,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });

    expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(
      VERSE_1.sanskritText,
    );
    const translationLoading = screen.getByTestId('verse-translation-loading', {
      includeHiddenElements: true,
    });
    expect(translationLoading.props.accessibilityElementsHidden).toBe(true);
    expect(translationLoading.props.importantForAccessibility).toBe('no');
    expect(screen.queryByText(/loading translation/i)).toBeNull();
    expect(screen.queryByTestId('verse-translation-label')).toBeNull();
    expect(screen.queryByLabelText('Loading verse')).toBeNull();
    expect(screen.getByLabelText('Previous verse')).toBeDisabled();
    expect(screen.getByLabelText('Next verse')).toBeEnabled();

    await act(async () => {
      resolveTranslation?.(TRANSLATION_1);
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-translation-text')).toBeTruthy();
    });
    expect(screen.getByTestId('verse-translation-label')).toHaveTextContent(
      'Translation',
    );
    expect(screen.getByTestId('verse-translation-provider')).toHaveTextContent(
      'FIXTURE_PROVIDER',
    );
  });

  it('keeps long content in one scroll document with bottom safe-area padding', async () => {
    const longSanskrit =
      'धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।\n'.repeat(12);
    const bottomInset = 34;
    renderVerse({
      loadVerse: async () => ({
        ...VERSE_1,
        sanskritText: longSanskrit,
      }),
      loadTranslation: async () => ({
        ...TRANSLATION_1,
        translationText: `${TRANSLATION_1.translationText}\n`.repeat(8),
      }),
      initialMetrics: {
        ...TEST_WINDOW_METRICS,
        insets: { ...TEST_WINDOW_METRICS.insets, bottom: bottomInset },
      },
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
    });

    const scroll = screen.getByTestId('verse-scroll');
    expect(scrollBottomPadding(scroll)).toBe(
      verseSpacing.bottomPadding + bottomInset,
    );
    expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(
      longSanskrit.trim(),
    );
    expect(screen.getByTestId('verse-translation-text')).toBeTruthy();
    expect(screen.getByTestId('verse-navigation')).toBeTruthy();
    expect(screen.queryByTestId('verse-loading-indicator')).toBeNull();
    expect(
      screen.getByTestId('verse-sanskrit-text').props.style,
    ).not.toEqual(
      expect.objectContaining({
        height: expect.any(Number),
      }),
    );
  });

  it('collapses Translation silently when Translation returns 404', async () => {
    const loadTranslation = jest.fn(async () => {
      throw new ApiError('Backend responded with HTTP 404.', {
        kind: 'http',
        status: 404,
      });
    });
    const progress = createProgressServiceMock();

    renderVerse({
      loadTranslation,
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
      expect(screen.getByTestId('verse-navigation')).toBeTruthy();
      expect(screen.queryByTestId('verse-translation-block')).toBeNull();
    });

    expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(
      VERSE_1.sanskritText,
    );
    expect(screen.queryByTestId('verse-translation-unavailable')).toBeNull();
    expect(screen.queryByText(/translation unavailable/i)).toBeNull();
    expect(screen.queryByTestId('verse-error')).toBeNull();
    expect(progress.recordVerseOpened).toHaveBeenCalledTimes(1);
  });

  it('maps Translation network failure to silent collapse without Verse error UI', async () => {
    const progress = createProgressServiceMock();
    renderVerse({
      loadTranslation: async () => {
        throw new ApiError('Unable to reach the Antar backend.', {
          kind: 'network',
        });
      },
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
      expect(screen.getByTestId('verse-navigation')).toBeTruthy();
      expect(screen.queryByTestId('verse-translation-block')).toBeNull();
    });

    expect(screen.getByTestId('verse-sanskrit-text')).toBeTruthy();
    expect(screen.queryByText(/translation unavailable/i)).toBeNull();
    expect(screen.queryByTestId('verse-error')).toBeNull();
    expect(screen.queryByText('Unable to load this verse.')).toBeNull();
    expect(progress.recordVerseOpened).toHaveBeenCalledTimes(1);
  });

  it('maps Translation HTTP 500 to silent collapse without Verse error UI', async () => {
    const progress = createProgressServiceMock();
    renderVerse({
      loadTranslation: async () => {
        throw new ApiError('Backend responded with HTTP 500.', {
          kind: 'http',
          status: 500,
        });
      },
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
      expect(screen.getByTestId('verse-navigation')).toBeTruthy();
      expect(screen.queryByTestId('verse-translation-block')).toBeNull();
    });

    expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(
      VERSE_1.sanskritText,
    );
    expect(screen.queryByText(/translation unavailable/i)).toBeNull();
    expect(screen.queryByTestId('verse-error')).toBeNull();
    expect(progress.recordVerseOpened).toHaveBeenCalledTimes(1);
  });

  it('maps Translation parse failure to silent collapse without Verse error UI', async () => {
    const progress = createProgressServiceMock();
    renderVerse({
      loadTranslation: async () => {
        throw new ApiError('Backend returned an unreadable translation response.', {
          kind: 'parse',
        });
      },
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-success')).toBeTruthy();
      expect(screen.getByTestId('verse-navigation')).toBeTruthy();
      expect(screen.queryByTestId('verse-translation-block')).toBeNull();
    });

    expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(
      VERSE_1.sanskritText,
    );
    expect(screen.queryByText(/translation unavailable/i)).toBeNull();
    expect(screen.queryByTestId('verse-error')).toBeNull();
    expect(progress.recordVerseOpened).toHaveBeenCalledTimes(1);
  });

  it('does not write extra Reading Progress when Translation succeeds', async () => {
    const progress = createProgressServiceMock();
    renderVerse({
      loadTranslation: async () => TRANSLATION_1,
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-translation-text')).toBeTruthy();
    });

    expect(progress.recordVerseOpened).toHaveBeenCalledTimes(1);
  });

  it('does not fetch Translation when Sanskrit fails', async () => {
    const loadTranslation = jest.fn(async () => TRANSLATION_1);
    const progress = createProgressServiceMock();

    renderVerse({
      loadVerse: async () => {
        throw new Error('RESOURCE_NOT_FOUND');
      },
      loadTranslation,
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-error')).toBeTruthy();
    });

    expect(loadTranslation).not.toHaveBeenCalled();
    expect(screen.queryByTestId('verse-translation-block')).toBeNull();
    expect(progress.recordVerseOpened).not.toHaveBeenCalled();
  });

  it('ignores a stale Translation response after navigating to another Verse', async () => {
    let resolveFirstTranslation: ((value: VerseTranslation) => void) | undefined;
    const firstPending = new Promise<VerseTranslation>((resolve) => {
      resolveFirstTranslation = resolve;
    });

    let translationCall = 0;
    const loadTranslation = jest.fn(async (id: string) => {
      translationCall += 1;
      if (translationCall === 1) {
        return firstPending;
      }
      return id === VERSE_2.id ? TRANSLATION_2 : TRANSLATION_1;
    });

    const loadVerse = jest.fn(async (id: string) =>
      id === VERSE_2.id ? VERSE_2 : VERSE_1,
    );

    const { rerender, readingProgressService } = renderVerse({
      loadVerse,
      loadTranslation,
    });

    await waitFor(() => {
      expect(
        screen.getByTestId('verse-translation-loading', {
          includeHiddenElements: true,
        }),
      ).toBeTruthy();
    });

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
        loadTranslation={loadTranslation}
        loadChapterVerses={async () => VERSES}
        readingProgressService={readingProgressService}
      />,
    );

    await waitFor(() => {
      expect(screen.getByTestId('verse-translation-text')).toHaveTextContent(
        TRANSLATION_2.translationText,
      );
    });
    expect(screen.getByTestId('verse-sanskrit-text')).toHaveTextContent(
      VERSE_2.sanskritText,
    );

    await act(async () => {
      resolveFirstTranslation?.(TRANSLATION_1);
    });

    expect(screen.getByTestId('verse-translation-text')).toHaveTextContent(
      TRANSLATION_2.translationText,
    );
    expect(screen.queryByText(TRANSLATION_1.translationText)).toBeNull();
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
    const loadTranslation = jest.fn(async () => TRANSLATION_1);
    const progress = createProgressServiceMock();
    renderVerse({
      loadVerse: async () => ({ ...VERSE_1, sanskritText: '   ' }),
      loadTranslation,
      readingProgressService: progress,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-error')).toBeTruthy();
    });
    expect(progress.recordVerseOpened).not.toHaveBeenCalled();
    expect(loadTranslation).not.toHaveBeenCalled();
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

  it('keeps Previous / Next usable while Translation loads', async () => {
    const setParams = jest.fn();
    const navigation = createNavigationMock({ setParams });
    const pending = new Promise<VerseTranslation>(() => {});

    renderVerse({
      navigation,
      loadTranslation: () => pending,
    });

    await waitFor(() => {
      expect(
        screen.getByTestId('verse-translation-loading', {
          includeHiddenElements: true,
        }),
      ).toBeTruthy();
    });

    expect(screen.getByLabelText('Next verse')).toBeEnabled();
    fireEvent.press(screen.getByLabelText('Next verse'));
    expect(setParams).toHaveBeenCalledWith({
      verseId: 'verse-2',
      verseNumber: 2,
      chapterNumber: 1,
    });
  });

  it('does not navigate while Sanskrit is still loading', async () => {
    const setParams = jest.fn();
    const navigation = createNavigationMock({ setParams });
    const pending = new Promise<VerseDetail>(() => {});

    renderVerse({
      navigation,
      loadVerse: () => pending,
    });

    expect(screen.getByLabelText('Next verse')).toBeDisabled();
    fireEvent.press(screen.getByLabelText('Next verse'));
    expect(setParams).not.toHaveBeenCalled();
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

    const { rerender, readingProgressService, loadTranslation } = renderVerse({
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
        loadTranslation={loadTranslation}
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

  it('exposes Back, one combined Verse reference, and Translation accessibility', async () => {
    const navigation = createNavigationMock();
    renderVerse({
      navigation,
      loadTranslation: async () => TRANSLATION_1,
    });

    await waitFor(() => {
      expect(screen.getByTestId('verse-translation-text')).toBeTruthy();
    });

    expect(screen.getByLabelText('Go back')).toBeTruthy();
    expect(screen.getByLabelText('Chapter 1, Verse 1')).toBeTruthy();
    expect(screen.getAllByLabelText('Chapter 1, Verse 1')).toHaveLength(1);
    expect(screen.queryByRole('header', { name: 'Chapter 1' })).toBeNull();
    expect(screen.getByRole('header', { name: 'Translation' })).toBeTruthy();
    expect(screen.getByLabelText('Provider FIXTURE_PROVIDER')).toBeTruthy();
    fireEvent.press(screen.getByLabelText('Go back'));
    expect(navigation.goBack).toHaveBeenCalled();
  });
});
