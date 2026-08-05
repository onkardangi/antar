import { fireEvent, screen, waitFor } from '@testing-library/react-native';
import type { ComponentProps } from 'react';

import { VerseScreen } from './VerseScreen';
import { renderWithProviders } from '../../../test/renderWithProviders';
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
  } = {},
) {
  const navigation = options.navigation ?? createNavigationMock();
  const verseId = options.verseId ?? VERSE_1.id;
  const verseNumber = options.verseNumber ?? VERSE_1.verseNumber;
  const chapterNumber = options.chapterNumber ?? VERSE_1.chapterNumber;

  return {
    navigation,
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
      />,
    ),
  };
}

describe('VerseScreen', () => {
  it('shows a centered loading state while the verse loads', async () => {
    let resolveVerse: ((value: VerseDetail) => void) | undefined;
    const pending = new Promise<VerseDetail>((resolve) => {
      resolveVerse = resolve;
    });

    renderVerse({ loadVerse: () => pending });

    expect(screen.getByTestId('verse-loading')).toBeTruthy();
    expect(screen.getByLabelText('Loading verse')).toBeTruthy();

    resolveVerse?.(VERSE_1);
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
