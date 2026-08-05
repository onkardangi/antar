import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react-native';
import type { ComponentProps } from 'react';
import { ScrollView } from 'react-native';
import type { Metrics } from 'react-native-safe-area-context';

import { ChapterScreen } from './ChapterScreen';
import { AppProviders } from '../../../app/AppProviders';
import { renderWithProviders } from '../../../test/renderWithProviders';
import { chapterSpacing, TEMPORARY_VERSE_PREVIEW_TEXT } from '../../../design-system';
import { ApiError } from '../../../services/api/apiError';
import type { ChapterDetail, VerseListItem } from '../model/chapterTypes';

type ChapterProps = ComponentProps<typeof ChapterScreen>;

const CHAPTER: ChapterDetail = {
  id: '018f0000-0000-7000-8000-000000000002',
  chapterNumber: 2,
  canonicalName: 'Sankhya Yoga',
  englishName: 'The Yoga of Knowledge',
  shortIntent: 'Action, wisdom, duty, and steadiness.',
  verseCount: 3,
};

const VERSES: VerseListItem[] = [
  {
    id: 'verse-1',
    verseNumber: 1,
    canonicalReference: '2.1',
    previewText: TEMPORARY_VERSE_PREVIEW_TEXT,
  },
  {
    id: 'verse-2',
    verseNumber: 2,
    canonicalReference: '2.2',
    previewText: TEMPORARY_VERSE_PREVIEW_TEXT,
  },
  {
    id: 'verse-3',
    verseNumber: 3,
    canonicalReference: '2.3',
    previewText: TEMPORARY_VERSE_PREVIEW_TEXT,
  },
];

function createNavigationMock(
  overrides: Partial<{ canGoBack: boolean }> = {},
): ChapterProps['navigation'] {
  const canGoBack = overrides.canGoBack ?? true;
  return {
    navigate: jest.fn(),
    goBack: jest.fn(),
    canGoBack: jest.fn(() => canGoBack),
  } as unknown as ChapterProps['navigation'];
}

function renderChapter(
  options: {
    loadChapter?: (chapterId: string) => Promise<ChapterDetail>;
    loadVerses?: (chapterId: string) => Promise<VerseListItem[]>;
    navigation?: ChapterProps['navigation'];
    chapterNumber?: number;
  } = {},
) {
  const navigation = options.navigation ?? createNavigationMock();
  return {
    navigation,
    ...renderWithProviders(
      <ChapterScreen
        navigation={navigation}
        route={{
          key: 'Chapter',
          name: 'Chapter',
          params: {
            chapterId: CHAPTER.id,
            chapterNumber: options.chapterNumber ?? CHAPTER.chapterNumber,
          },
        }}
        loadChapter={options.loadChapter ?? (async () => CHAPTER)}
        loadVerses={options.loadVerses ?? (async () => VERSES)}
      />,
    ),
  };
}

describe('ChapterScreen', () => {
  it('shows CHAPTER label from the route and structural placeholders while chapter detail loads', async () => {
    let resolveChapter: ((value: ChapterDetail) => void) | undefined;
    const pendingChapter = new Promise<ChapterDetail>((resolve) => {
      resolveChapter = resolve;
    });
    let resolveVerses: ((value: VerseListItem[]) => void) | undefined;
    const pendingVerses = new Promise<VerseListItem[]>((resolve) => {
      resolveVerses = resolve;
    });

    renderChapter({
      loadChapter: () => pendingChapter,
      loadVerses: () => pendingVerses,
    });

    expect(screen.getByTestId('chapter-loading')).toBeTruthy();
    expect(screen.getByText('CHAPTER 2')).toBeTruthy();
    expect(
      screen.getByTestId('chapter-introduction-name-placeholder', {
        includeHiddenElements: true,
      }),
    ).toBeTruthy();
    expect(
      screen.getByTestId('chapter-introduction-intent-placeholder', {
        includeHiddenElements: true,
      }),
    ).toBeTruthy();
    expect(screen.queryByText('Sankhya Yoga')).toBeNull();
    expect(screen.queryByText(CHAPTER.shortIntent)).toBeNull();
    expect(screen.queryByText('Loading')).toBeNull();
    expect(
      screen.getAllByTestId('verse-placeholder-row', { includeHiddenElements: true }),
    ).toHaveLength(8);

    await act(async () => {
      resolveChapter?.(CHAPTER);
      resolveVerses?.(VERSES);
    });

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });
  });

  it('does not invent canonicalName or shortIntent from the route while loading', async () => {
    let resolveChapter: ((value: ChapterDetail) => void) | undefined;
    const pendingChapter = new Promise<ChapterDetail>((resolve) => {
      resolveChapter = resolve;
    });

    renderChapter({
      loadChapter: () => pendingChapter,
      loadVerses: async () => VERSES,
      chapterNumber: 2,
    });

    expect(screen.queryByText('Sankhya Yoga')).toBeNull();
    expect(screen.queryByText(/Action, wisdom/)).toBeNull();
    expect(screen.getByText('CHAPTER 2')).toBeTruthy();

    await act(async () => {
      resolveChapter?.(CHAPTER);
    });

    await waitFor(() => {
      expect(screen.getByText('Sankhya Yoga')).toBeTruthy();
    });
  });

  it('renders chapter introduction and verses in backend order', async () => {
    renderChapter({
      loadVerses: async () => [...VERSES].reverse(),
    });

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });

    expect(screen.getByText('CHAPTER 2')).toBeTruthy();
    expect(screen.getByText('Sankhya Yoga')).toBeTruthy();
    expect(screen.getByText(CHAPTER.shortIntent)).toBeTruthy();

    // Tree order must match the API sequence (3 → 2 → 1), not a client sort.
    const rowTestIds = screen
      .getAllByTestId(/^verse-row-\d+$/)
      .map((row) => row.props.testID);
    expect(rowTestIds).toEqual(['verse-row-3', 'verse-row-2', 'verse-row-1']);
    expect(screen.getAllByText(TEMPORARY_VERSE_PREVIEW_TEXT)).toHaveLength(3);
  });

  it('renders a scroll-enabled verse FlatList as one continuous document', async () => {
    const metrics: Metrics = {
      frame: { x: 0, y: 0, width: 390, height: 844 },
      insets: { top: 0, left: 0, right: 0, bottom: 34 },
    };

    render(
      <AppProviders initialMetrics={metrics} skipFontLoading>
        <ChapterScreen
          navigation={createNavigationMock()}
          route={{
            key: 'Chapter',
            name: 'Chapter',
            params: {
              chapterId: CHAPTER.id,
              chapterNumber: CHAPTER.chapterNumber,
            },
          }}
          loadChapter={async () => CHAPTER}
          loadVerses={async () => VERSES}
        />
      </AppProviders>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });

    const list = screen.getByTestId('chapter-verse-list');
    expect(list.props.scrollEnabled).toBe(true);
    expect(list.props.contentContainerStyle).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          paddingBottom: chapterSpacing.bottomPadding + 34,
        }),
      ]),
    );

    // Header + introduction live in the FlatList header — not fixed above it.
    const listHeader = within(list).getByTestId('chapter-list-header');
    expect(within(listHeader).getByTestId('screen-header')).toBeTruthy();
    expect(within(listHeader).getByTestId('chapter-introduction')).toBeTruthy();

    // Verse rows are FlatList items in the same scroll container.
    expect(within(list).getByTestId('verse-row-1')).toBeTruthy();
    expect(within(list).getByTestId('verse-row-2')).toBeTruthy();
    expect(within(list).getByTestId('verse-row-3')).toBeTruthy();

    // The only ScrollView under success is the verse FlatList itself —
    // no separate outer vertical ScrollView wraps the document.
    const success = screen.getByTestId('chapter-success');
    const scrollViews = within(success).UNSAFE_queryAllByType(ScrollView);
    expect(scrollViews).toHaveLength(1);
    expect(scrollViews[0]?.props.testID).toBe('chapter-verse-list');
    expect(scrollViews[0]?.props.scrollEnabled).toBe(true);
  });

  it('renders backend previewText literally in the success state', async () => {
    renderChapter();

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });

    expect(screen.getAllByText(TEMPORARY_VERSE_PREVIEW_TEXT)).toHaveLength(3);
    expect(screen.queryByTestId('verse-placeholder-row')).toBeNull();
  });

  it('keeps restrained verse placeholders while verses load after chapter identity resolves', async () => {
    let resolveVerses: ((value: VerseListItem[]) => void) | undefined;
    const pendingVerses = new Promise<VerseListItem[]>((resolve) => {
      resolveVerses = resolve;
    });

    renderChapter({
      loadChapter: async () => CHAPTER,
      loadVerses: () => pendingVerses,
    });

    await waitFor(() => {
      expect(screen.getByText('Sankhya Yoga')).toBeTruthy();
    });

    expect(screen.getByTestId('chapter-loading')).toBeTruthy();
    expect(screen.getByText(CHAPTER.shortIntent)).toBeTruthy();
    expect(
      screen.getAllByTestId('verse-placeholder-row', { includeHiddenElements: true }),
    ).toHaveLength(8);
    expect(screen.queryByTestId('chapter-verse-list')).toBeNull();

    await act(async () => {
      resolveVerses?.(VERSES);
    });

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });
  });

  it('does not display a completed verse list before chapter identity resolves', async () => {
    let resolveChapter: ((value: ChapterDetail) => void) | undefined;
    const pendingChapter = new Promise<ChapterDetail>((resolve) => {
      resolveChapter = resolve;
    });

    renderChapter({
      loadChapter: () => pendingChapter,
      loadVerses: async () => VERSES,
    });

    expect(screen.queryByTestId('chapter-verse-list')).toBeNull();
    expect(
      screen.getAllByTestId('verse-placeholder-row', { includeHiddenElements: true }).length,
    ).toBeGreaterThan(0);

    await act(async () => {
      resolveChapter?.(CHAPTER);
    });

    await waitFor(() => {
      expect(screen.getByTestId('chapter-verse-list')).toBeTruthy();
    });
  });

  it('shows a chapter-level error without inventing chapter content', async () => {
    const loadChapter = jest
      .fn()
      .mockRejectedValueOnce(new ApiError('Unable to reach the Antar backend.', { kind: 'network' }))
      .mockResolvedValueOnce(CHAPTER);
    const loadVerses = jest.fn().mockResolvedValue(VERSES);

    renderChapter({ loadChapter, loadVerses });

    await waitFor(() => {
      expect(screen.getByTestId('chapter-error')).toBeTruthy();
    });

    expect(screen.getByText('CHAPTER 2')).toBeTruthy();
    expect(screen.queryByText('Sankhya Yoga')).toBeNull();
    expect(screen.queryByTestId('chapter-introduction-name-placeholder')).toBeNull();
    expect(screen.getByText('Unable to load chapter.')).toBeTruthy();
    expect(screen.getByText('Please try again.')).toBeTruthy();
    expect(screen.queryByTestId('chapter-verse-list')).toBeNull();

    fireEvent.press(screen.getByLabelText('Retry loading chapter'));

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });

    expect(loadChapter).toHaveBeenCalledTimes(2);
  });

  it('preserves a loaded chapter introduction when verses fail and retries verses only', async () => {
    const loadChapter = jest.fn().mockResolvedValue(CHAPTER);
    const loadVerses = jest
      .fn()
      .mockRejectedValueOnce(new ApiError('Unable to reach the Antar backend.', { kind: 'network' }))
      .mockResolvedValueOnce(VERSES);

    renderChapter({ loadChapter, loadVerses });

    await waitFor(() => {
      expect(screen.getByTestId('chapter-verse-error')).toBeTruthy();
    });

    expect(screen.getByText('Sankhya Yoga')).toBeTruthy();
    expect(screen.getByText(CHAPTER.shortIntent)).toBeTruthy();
    expect(screen.getByText('Unable to load verses.')).toBeTruthy();
    expect(screen.getByText('Please try again.')).toBeTruthy();

    fireEvent.press(screen.getByLabelText('Retry loading verses'));

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });

    expect(loadChapter).toHaveBeenCalledTimes(1);
    expect(loadVerses).toHaveBeenCalledTimes(2);
  });

  it('applies bottom safe-area padding to the verse error container', async () => {
    const metrics: Metrics = {
      frame: { x: 0, y: 0, width: 390, height: 844 },
      insets: { top: 0, left: 0, right: 0, bottom: 34 },
    };

    render(
      <AppProviders initialMetrics={metrics} skipFontLoading>
        <ChapterScreen
          navigation={createNavigationMock()}
          route={{
            key: 'Chapter',
            name: 'Chapter',
            params: {
              chapterId: CHAPTER.id,
              chapterNumber: CHAPTER.chapterNumber,
            },
          }}
          loadChapter={async () => CHAPTER}
          loadVerses={async () => {
            throw new ApiError('Unable to reach the Antar backend.', { kind: 'network' });
          }}
        />
      </AppProviders>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('chapter-verse-error')).toBeTruthy();
    });

    expect(screen.getByTestId('chapter-verse-error-content')).toHaveStyle({
      paddingBottom: chapterSpacing.bottomPadding + 34,
    });
  });

  it('treats an empty verse response as an error state', async () => {
    renderChapter({
      loadVerses: async () => [],
    });

    await waitFor(() => {
      expect(screen.getByTestId('chapter-verse-error')).toBeTruthy();
    });

    expect(screen.getByText('Unable to load verses.')).toBeTruthy();
    expect(screen.queryByText('No verses available')).toBeNull();
  });

  it('exposes verse accessibility labels and supports full-row press', async () => {
    const { navigation } = renderChapter();

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });

    const row = screen.getByLabelText('Chapter 2, Verse 1');
    fireEvent.press(row);

    expect(navigation.navigate).toHaveBeenCalledWith('VerseReader', {
      verseId: 'verse-1',
      verseNumber: 1,
      chapterNumber: 2,
    });
  });

  it('navigates to the Verse Reader with the expected params', async () => {
    const { navigation } = renderChapter();

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });

    fireEvent.press(screen.getByTestId('verse-row-2'));

    expect(navigation.navigate).toHaveBeenCalledWith('VerseReader', {
      verseId: 'verse-2',
      verseNumber: 2,
      chapterNumber: 2,
    });
  });

  it('renders Back and Antar on one inline header row inside the FlatList header', async () => {
    renderChapter();

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });

    const list = screen.getByTestId('chapter-verse-list');
    const listHeader = within(list).getByTestId('chapter-list-header');
    const header = within(listHeader).getByTestId('screen-header');
    const inlineRow = within(header).getByTestId('screen-header-inline-row');

    expect(inlineRow).toHaveStyle({ flexDirection: 'row' });
    expect(within(inlineRow).getByLabelText('Go back')).toBeTruthy();
    expect(within(inlineRow).getByText('Antar')).toBeTruthy();
    expect(within(inlineRow).getByText('Antar').props.accessibilityRole).toBe('header');
  });

  it('keeps VerseRow touch targets, row structure, and quiet temporary preview', async () => {
    renderChapter();

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });

    const row = screen.getByTestId('verse-row-1');
    expect(row).toHaveStyle({
      flexDirection: 'row',
      minHeight: chapterSpacing.minTouchTarget,
      paddingVertical: chapterSpacing.verseRowVertical,
      gap: chapterSpacing.verseNumberToPreviewGap,
    });
    expect(within(row).getByTestId('verse-row-number')).toHaveTextContent('01');
    expect(within(row).getByTestId('verse-row-preview')).toHaveTextContent(
      TEMPORARY_VERSE_PREVIEW_TEXT,
    );
    expect(within(row).getByTestId('verse-row-preview')).toHaveStyle({
      fontStyle: 'italic',
    });
  });

  it('renders Back and invokes goBack', async () => {
    const navigation = createNavigationMock({ canGoBack: true });
    renderChapter({ navigation });

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });

    fireEvent.press(screen.getByLabelText('Go back'));
    expect(navigation.goBack).toHaveBeenCalledTimes(1);
  });

  it('separates every VerseRow with a full-width hairline divider', async () => {
    renderChapter();

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });

    expect(
      screen.getAllByTestId('verse-row-divider', { includeHiddenElements: true }),
    ).toHaveLength(2);
    expect(
      screen.getAllByTestId('hairline-rule', { includeHiddenElements: true }).length,
    ).toBeGreaterThanOrEqual(2);
  });

  it('does not render icons, cards, or personalization', async () => {
    renderChapter();

    await waitFor(() => {
      expect(screen.getByTestId('chapter-success')).toBeTruthy();
    });

    expect(screen.queryByText('›')).toBeNull();
    expect(screen.queryByText('>')).toBeNull();
    expect(screen.queryByText('→')).toBeNull();
    expect(screen.queryByText(/continue reading/i)).toBeNull();
    expect(screen.queryByText(/progress/i)).toBeNull();
    expect(screen.queryByText(/bookmark/i)).toBeNull();
    expect(screen.queryByText(/search/i)).toBeNull();
    expect(screen.queryByText(CHAPTER.englishName)).toBeNull();
  });

  it('hides decorative verse placeholders from accessibility', async () => {
    let resolveVerses: ((value: VerseListItem[]) => void) | undefined;
    const pendingVerses = new Promise<VerseListItem[]>((resolve) => {
      resolveVerses = resolve;
    });

    renderChapter({
      loadChapter: async () => CHAPTER,
      loadVerses: () => pendingVerses,
    });

    await waitFor(() => {
      expect(screen.getByText('Sankhya Yoga')).toBeTruthy();
    });

    expect(screen.queryByLabelText('Loading verses')).toBeNull();
    const placeholders = screen.getAllByTestId('verse-placeholder-row', {
      includeHiddenElements: true,
    });
    expect(placeholders.length).toBeGreaterThan(0);

    await act(async () => {
      resolveVerses?.(VERSES);
    });
  });
});
