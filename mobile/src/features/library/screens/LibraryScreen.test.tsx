import { act, fireEvent, render, screen, waitFor } from '@testing-library/react-native';
import type { ComponentProps } from 'react';
import type { Metrics } from 'react-native-safe-area-context';

import { LibraryScreen } from './LibraryScreen';
import { ChapterPlaceholderScreen } from './ChapterPlaceholderScreen';
import { AppProviders } from '../../../app/AppProviders';
import { renderWithProviders } from '../../../test/renderWithProviders';
import { librarySpacing } from '../../../design-system';
import { ApiError } from '../../../services/api/apiError';
import type { Chapter } from '../model/chapterTypes';

type LibraryProps = ComponentProps<typeof LibraryScreen>;
type ChapterPlaceholderProps = ComponentProps<typeof ChapterPlaceholderScreen>;

const CHAPTERS: Chapter[] = [
  {
    id: '018f0000-0000-7000-8000-000000000001',
    chapterNumber: 1,
    canonicalName: 'Arjuna Vishada Yoga',
    englishName: "The Yoga of Arjuna's Despair",
    shortIntent: 'A battlefield crisis becomes the beginning of inquiry.',
    verseCount: 47,
  },
  {
    id: '018f0000-0000-7000-8000-000000000002',
    chapterNumber: 2,
    canonicalName: 'Sankhya Yoga',
    englishName: 'The Yoga of Knowledge',
    shortIntent: 'Action, wisdom, duty, and steadiness.',
    verseCount: 72,
  },
];

function createAllChapters(): Chapter[] {
  return Array.from({ length: 18 }, (_, index) => {
    const chapterNumber = index + 1;
    const known = CHAPTERS.find((chapter) => chapter.chapterNumber === chapterNumber);
    if (known) {
      return known;
    }
    return {
      id: `018f0000-0000-7000-8000-0000000000${String(chapterNumber).padStart(2, '0')}`,
      chapterNumber,
      canonicalName: `Chapter ${chapterNumber} Yoga`,
      englishName: `English ${chapterNumber}`,
      shortIntent: `Intent ${chapterNumber}`,
      verseCount: 20 + chapterNumber,
    };
  });
}

function createLibraryNavigationMock(
  overrides: Partial<{ canGoBack: boolean }> = {},
): LibraryProps['navigation'] {
  const canGoBack = overrides.canGoBack ?? false;
  return {
    navigate: jest.fn(),
    goBack: jest.fn(),
    canGoBack: jest.fn(() => canGoBack),
  } as unknown as LibraryProps['navigation'];
}

function renderLibrary(
  loadChapters: () => Promise<Chapter[]>,
  navigation: LibraryProps['navigation'] = createLibraryNavigationMock(),
) {
  return {
    navigation,
    ...renderWithProviders(
      <LibraryScreen
        navigation={navigation}
        route={{ key: 'Library', name: 'Library', params: undefined }}
        loadChapters={loadChapters}
      />,
    ),
  };
}

describe('LibraryScreen', () => {
  it('keeps Scripture Introduction visible and shows restrained placeholder rows while loading', async () => {
    let resolveRequest: ((value: Chapter[]) => void) | undefined;
    const pending = new Promise<Chapter[]>((resolve) => {
      resolveRequest = resolve;
    });

    renderLibrary(() => pending);

    expect(screen.getByTestId('library-loading')).toBeTruthy();
    expect(screen.getByTestId('scripture-introduction')).toBeTruthy();
    expect(screen.getByText('Bhagavad Gita')).toBeTruthy();
    expect(screen.queryByLabelText('Loading chapters')).toBeNull();
    expect(screen.queryByText('Loading chapters…')).toBeNull();
    expect(screen.getAllByTestId('chapter-placeholder-row')).toHaveLength(9);

    await act(async () => {
      resolveRequest?.(CHAPTERS);
    });

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });
  });

  it('renders chapters in canonical order with handoff accessibility labels', async () => {
    renderLibrary(async () => [...CHAPTERS].reverse());

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    expect(screen.getByText('01')).toBeTruthy();
    expect(screen.getByText('02')).toBeTruthy();
    expect(screen.getByText('Arjuna Vishada Yoga')).toBeTruthy();
    expect(screen.getByText('Sankhya Yoga')).toBeTruthy();
    expect(screen.getByText('47 verses')).toBeTruthy();
    expect(screen.getByText('72 verses')).toBeTruthy();
    expect(
      screen.getByLabelText('Chapter 1, Arjuna Vishada Yoga, 47 verses'),
    ).toBeTruthy();
    expect(screen.getByLabelText('Chapter 2, Sankhya Yoga, 72 verses')).toBeTruthy();
  });

  it('formats chapter numbers with zero padding', async () => {
    renderLibrary(async () => CHAPTERS);

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    expect(screen.getByText('01')).toBeTruthy();
    expect(screen.getByText('02')).toBeTruthy();
    expect(screen.queryByText('Chapter 1')).toBeNull();
  });

  it('renders all 18 chapters when supplied', async () => {
    const chapters = createAllChapters();
    renderLibrary(async () => chapters);

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    for (const chapter of chapters) {
      expect(
        screen.getByLabelText(
          `Chapter ${chapter.chapterNumber}, ${chapter.canonicalName}, ${chapter.verseCount} verses`,
        ),
      ).toBeTruthy();
    }
  });

  it('shows a quiet retryable error state', async () => {
    const loadChapters = jest
      .fn()
      .mockRejectedValueOnce(new ApiError('Unable to reach the Antar backend.', { kind: 'network' }))
      .mockResolvedValueOnce(CHAPTERS);

    renderLibrary(loadChapters);

    await waitFor(() => {
      expect(screen.getByTestId('library-error')).toBeTruthy();
    });

    expect(screen.getByTestId('scripture-introduction')).toBeTruthy();
    expect(screen.getByText('Unable to load chapters.')).toBeTruthy();
    expect(screen.getByText('Please try again.')).toBeTruthy();

    fireEvent.press(screen.getByLabelText('Retry loading chapters'));

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    expect(loadChapters).toHaveBeenCalledTimes(2);
  });

  it('applies bottom safe-area padding to the error container', async () => {
    const metrics: Metrics = {
      frame: { x: 0, y: 0, width: 390, height: 844 },
      insets: { top: 0, left: 0, right: 0, bottom: 34 },
    };

    render(
      <AppProviders initialMetrics={metrics} skipFontLoading>
        <LibraryScreen
          navigation={createLibraryNavigationMock()}
          route={{ key: 'Library', name: 'Library', params: undefined }}
          loadChapters={async () => {
            throw new ApiError('Unable to reach the Antar backend.', { kind: 'network' });
          }}
        />
      </AppProviders>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('library-error')).toBeTruthy();
    });

    expect(screen.getByTestId('library-error-content')).toHaveStyle({
      paddingBottom: librarySpacing.bottomPadding + 34,
    });
  });

  it('treats an empty chapter response as an error state', async () => {
    renderLibrary(async () => []);

    await waitFor(() => {
      expect(screen.getByTestId('library-error')).toBeTruthy();
    });

    expect(screen.getByText('Unable to load chapters.')).toBeTruthy();
    expect(screen.queryByText('No chapters available')).toBeNull();
  });

  it('hides Back when Library is the root route', async () => {
    renderLibrary(async () => CHAPTERS, createLibraryNavigationMock({ canGoBack: false }));

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    expect(screen.getByText('Antar')).toBeTruthy();
    expect(screen.queryByLabelText('Go back')).toBeNull();
    expect(screen.queryByTestId('screen-header-back')).toBeNull();
    expect(screen.queryByText('Back')).toBeNull();
  });

  it('renders Back and invokes goBack when navigation can go back', async () => {
    const navigation = createLibraryNavigationMock({ canGoBack: true });
    renderLibrary(async () => CHAPTERS, navigation);

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    expect(screen.getByText('Antar')).toBeTruthy();
    fireEvent.press(screen.getByLabelText('Go back'));
    expect(navigation.goBack).toHaveBeenCalledTimes(1);
  });

  it('does not render a Settings action from application code', async () => {
    renderLibrary(async () => CHAPTERS);

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    expect(screen.queryByLabelText(/settings/i)).toBeNull();
    expect(screen.queryByText(/settings/i)).toBeNull();
    expect(screen.queryByTestId(/settings/i)).toBeNull();
  });

  it('navigates to the Chapter placeholder when a chapter is pressed', async () => {
    const { navigation } = renderLibrary(async () => CHAPTERS);

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    fireEvent.press(screen.getByTestId('chapter-row-2'));

    expect(navigation.navigate).toHaveBeenCalledWith('ChapterPlaceholder', {
      chapterId: '018f0000-0000-7000-8000-000000000002',
      chapterNumber: 2,
    });

    const placeholderRoute: ChapterPlaceholderProps['route'] = {
      key: 'ChapterPlaceholder',
      name: 'ChapterPlaceholder',
      params: {
        chapterId: '018f0000-0000-7000-8000-000000000002',
        chapterNumber: 2,
      },
    };

    renderWithProviders(
      <ChapterPlaceholderScreen
        navigation={
          {
            goBack: jest.fn(),
            canGoBack: jest.fn(() => true),
          } as unknown as ChapterPlaceholderProps['navigation']
        }
        route={placeholderRoute}
      />,
    );

    expect(screen.getByTestId('chapter-placeholder')).toBeTruthy();
    expect(screen.getByText('Chapter 2')).toBeTruthy();
    expect(screen.getByLabelText('Go back')).toBeTruthy();
  });

  it('keeps ChapterRow fully pressable with complete accessibility labels', async () => {
    const { navigation } = renderLibrary(async () => CHAPTERS);

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    const row = screen.getByLabelText('Chapter 1, Arjuna Vishada Yoga, 47 verses');
    fireEvent.press(row);

    expect(navigation.navigate).toHaveBeenCalledWith('ChapterPlaceholder', {
      chapterId: '018f0000-0000-7000-8000-000000000001',
      chapterNumber: 1,
    });
  });

  it('does not render a trailing navigation icon', async () => {
    renderLibrary(async () => CHAPTERS);

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    expect(screen.queryByText('›')).toBeNull();
    expect(screen.queryByText('>')).toBeNull();
    expect(screen.queryByText('→')).toBeNull();
  });

  it('renders a scroll-enabled chapter FlatList in the success state', async () => {
    renderLibrary(async () => createAllChapters());

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    expect(screen.getByTestId('library-chapter-list')).toBeTruthy();
    // All 18 rows are present; FlatList remains the scroll container (not a static View).
    expect(screen.getByLabelText('Chapter 18, Chapter 18 Yoga, 38 verses')).toBeTruthy();
    expect(screen.getByLabelText('Chapter 1, Arjuna Vishada Yoga, 47 verses')).toBeTruthy();
  });

  it('separates every ChapterRow with a full-width hairline divider', async () => {
    renderLibrary(async () => createAllChapters());

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    // 17 separators between 18 chapters (no trailing divider after the last row).
    // HairlineRule is decorative (accessibilityElementsHidden), so include hidden nodes.
    expect(
      screen.getAllByTestId('chapter-row-divider', { includeHiddenElements: true }),
    ).toHaveLength(17);
    expect(
      screen.getAllByTestId('hairline-rule', { includeHiddenElements: true }).length,
    ).toBeGreaterThanOrEqual(2);
  });

  it('does not render personalization or progress UI', async () => {
    renderLibrary(async () => CHAPTERS);

    await waitFor(() => {
      expect(screen.getByTestId('library-success')).toBeTruthy();
    });

    expect(screen.queryByText(/continue reading/i)).toBeNull();
    expect(screen.queryByText(/recently opened/i)).toBeNull();
    expect(screen.queryByText(/progress/i)).toBeNull();
    expect(screen.queryByText(/search/i)).toBeNull();
    expect(screen.queryByText(/%/)).toBeNull();
    const firstChapter = CHAPTERS[0]!;
    expect(screen.queryByText(firstChapter.shortIntent)).toBeNull();
    expect(screen.queryByText(firstChapter.englishName)).toBeNull();
  });
});
