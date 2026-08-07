import { act, fireEvent, screen, waitFor } from '@testing-library/react-native';
import type { ComponentProps } from 'react';

import { homeSpacing } from '../../../design-system';
import { renderWithProviders } from '../../../test/renderWithProviders';
import type { TodaysInvitationState } from '../model/todaysInvitation';
import {
  beginReadingAccessibilityLabel,
  continueReadingAccessibilityLabel,
} from '../model/todaysInvitation';
import { HomeScreen } from './HomeScreen';

type HomeProps = ComponentProps<typeof HomeScreen>;

function createHomeNavigationMock() {
  const listeners = new Map<string, () => void>();
  return {
    navigate: jest.fn(),
    goBack: jest.fn(),
    canGoBack: jest.fn(() => false),
    addListener: jest.fn((event: string, callback: () => void) => {
      listeners.set(event, callback);
      if (event === 'focus') {
        callback();
      }
      return jest.fn(() => {
        listeners.delete(event);
      });
    }),
  } as unknown as HomeProps['navigation'];
}

function renderHome(loadTodaysInvitation: () => Promise<TodaysInvitationState>) {
  const navigation = createHomeNavigationMock();
  const result = renderWithProviders(
    <HomeScreen
      navigation={navigation}
      route={{ key: 'Home', name: 'Home', params: undefined }}
      loadTodaysInvitation={loadTodaysInvitation}
    />,
  );
  return { navigation, ...result };
}

describe('HomeScreen', () => {
  it('shows Begin Journey when there is no progress', async () => {
    renderHome(async () => ({
      kind: 'begin_journey',
      resolution: 'ready',
      destination: {
        verseId: 'verse-1',
        verseNumber: 1,
        chapterNumber: 1,
      },
    }));

    await waitFor(() => {
      expect(screen.getByTestId('home-invitation-begin')).toBeTruthy();
    });
    expect(screen.getByTestId('home-invitation-heading')).toBeTruthy();
    expect(screen.getByText('Begin Reading →')).toBeTruthy();
    expect(screen.getByText('Chapter 1 · Verse 1')).toBeTruthy();
    expect(
      screen.getByTestId('home-invitation-preview-placeholder', {
        includeHiddenElements: true,
      }),
    ).toBeTruthy();
    expect(screen.getByText('Browse Bhagavad Gita →')).toBeTruthy();
    expect(screen.queryByTestId('home-invitation-continue')).toBeNull();
    expect(screen.queryByTestId('home-greeting')).toBeNull();
  });

  it('shows Continue Reading for lastRead and opens VerseReader with those params', async () => {
    const { navigation } = renderHome(async () => ({
      kind: 'continue_reading',
      destination: {
        verseId: 'verse-12',
        verseNumber: 12,
        chapterNumber: 1,
      },
    }));

    await waitFor(() => {
      expect(screen.getByTestId('home-invitation-continue')).toBeTruthy();
    });

    expect(screen.getByTestId('home-invitation-heading')).toBeTruthy();
    expect(
      screen.getByLabelText(continueReadingAccessibilityLabel(1, 12)),
    ).toBeTruthy();
    expect(screen.getByText('Chapter 1 · Verse 12')).toBeTruthy();
    expect(screen.getByText('Continue Reading →')).toBeTruthy();

    fireEvent.press(screen.getByTestId('home-invitation-continue'));
    expect(navigation.navigate).toHaveBeenCalledWith('VerseReader', {
      verseId: 'verse-12',
      verseNumber: 12,
      chapterNumber: 1,
    });
  });

  it('Begin Reading opens canonical start VerseReader params', async () => {
    const { navigation } = renderHome(async () => ({
      kind: 'begin_journey',
      resolution: 'ready',
      destination: {
        verseId: 'verse-1-id',
        verseNumber: 1,
        chapterNumber: 1,
      },
    }));

    await waitFor(() => {
      expect(screen.getByTestId('home-invitation-begin')).toBeTruthy();
    });

    expect(
      screen.getByLabelText(beginReadingAccessibilityLabel(1, 1)),
    ).toBeTruthy();

    fireEvent.press(screen.getByTestId('home-invitation-begin'));
    expect(navigation.navigate).toHaveBeenCalledWith('VerseReader', {
      verseId: 'verse-1-id',
      verseNumber: 1,
      chapterNumber: 1,
    });
  });

  it('Browse opens Library and shows divider before Browse', async () => {
    const { navigation } = renderHome(async () => ({
      kind: 'begin_journey',
      resolution: 'ready',
      destination: {
        verseId: 'verse-1',
        verseNumber: 1,
        chapterNumber: 1,
      },
    }));

    await waitFor(() => {
      expect(screen.getByTestId('home-browse')).toBeTruthy();
    });

    expect(
      screen.getByTestId('home-browse-divider', { includeHiddenElements: true }),
    ).toBeTruthy();
    fireEvent.press(screen.getByTestId('home-browse'));
    expect(navigation.navigate).toHaveBeenCalledWith('Library');
  });

  it('read_error invitation keeps Browse and does not claim Begin Journey', async () => {
    renderHome(async () => ({ kind: 'progress_unavailable' }));

    await waitFor(() => {
      expect(screen.getByTestId('home-invitation-unavailable')).toBeTruthy();
    });

    expect(screen.getByTestId('home-browse')).toBeTruthy();
    expect(screen.getByTestId('home-invitation-heading')).toBeTruthy();
    expect(screen.queryByTestId('home-invitation-begin')).toBeNull();
    expect(screen.queryByText('Begin Reading →')).toBeNull();
    expect(screen.queryByText('Begin your reading')).toBeNull();
  });

  it('progress_unavailable Try again reloads the invitation', async () => {
    let calls = 0;
    renderHome(async () => {
      calls += 1;
      if (calls === 1) {
        return { kind: 'progress_unavailable' };
      }
      return {
        kind: 'continue_reading',
        destination: {
          verseId: 'verse-12',
          verseNumber: 12,
          chapterNumber: 1,
        },
      };
    });

    await waitFor(() => {
      expect(screen.getByTestId('home-invitation-retry')).toBeTruthy();
    });
    expect(screen.getByText('Try again')).toBeTruthy();
    expect(calls).toBe(1);

    fireEvent.press(screen.getByTestId('home-invitation-retry'));

    await waitFor(() => {
      expect(screen.getByTestId('home-invitation-continue')).toBeTruthy();
    });
    expect(calls).toBe(2);
    expect(screen.getByText('Continue Reading →')).toBeTruthy();
  });

  it('begin_journey unavailable shows quiet copy without Begin Reading; Browse still works', async () => {
    const { navigation } = renderHome(async () => ({
      kind: 'begin_journey',
      resolution: 'unavailable',
    }));

    await waitFor(() => {
      expect(screen.getByTestId('home-invitation-begin-unavailable')).toBeTruthy();
    });

    expect(
      screen.getByText('Chapter 1 · Verse 1 is unavailable right now.'),
    ).toBeTruthy();
    expect(screen.getByText('Browse the Gita when you’re ready.')).toBeTruthy();
    expect(screen.queryByTestId('home-invitation-begin')).toBeNull();
    expect(screen.queryByText('Begin Reading →')).toBeNull();

    fireEvent.press(screen.getByTestId('home-browse'));
    expect(navigation.navigate).toHaveBeenCalledWith('Library');
  });

  it('shows structural invitation loading without a full-screen spinner', async () => {
    let resolveLoad: ((value: TodaysInvitationState) => void) | undefined;
    const pending = new Promise<TodaysInvitationState>((resolve) => {
      resolveLoad = resolve;
    });

    renderHome(() => pending);

    expect(screen.getByTestId('home-browse')).toBeTruthy();
    expect(screen.getByTestId('home-invitation-loading')).toBeTruthy();
    expect(screen.getByTestId('home-invitation-heading')).toBeTruthy();
    expect(screen.queryByLabelText(/loading/i)).toBeNull();
    expect(screen.queryByText(/loading/i)).toBeNull();

    await act(async () => {
      resolveLoad?.({
        kind: 'begin_journey',
        resolution: 'ready',
        destination: {
          verseId: 'verse-1',
          verseNumber: 1,
          chapterNumber: 1,
        },
      });
    });

    await waitFor(() => {
      expect(screen.getByTestId('home-invitation-begin')).toBeTruthy();
    });
  });

  it('exposes only one primary invitation action and no deferred chrome', async () => {
    renderHome(async () => ({
      kind: 'continue_reading',
      destination: {
        verseId: 'verse-3',
        verseNumber: 3,
        chapterNumber: 2,
      },
    }));

    await waitFor(() => {
      expect(screen.getByTestId('home-invitation-continue')).toBeTruthy();
    });

    expect(screen.getAllByTestId('home-invitation-continue')).toHaveLength(1);
    expect(screen.queryByText(/%/)).toBeNull();
    expect(screen.queryByText(/streak/i)).toBeNull();
    expect(screen.queryByText(/ago/i)).toBeNull();
    expect(screen.queryByText(/bookmark/i)).toBeNull();
    expect(screen.queryByText(/search/i)).toBeNull();
    expect(screen.queryByText(/saar/i)).toBeNull();
    expect(screen.queryByText(/reflect/i)).toBeNull();
    expect(screen.queryByText(/recommend/i)).toBeNull();
  });

  it('keeps Continue Reading as an action, not a page heading', async () => {
    renderHome(async () => ({
      kind: 'continue_reading',
      destination: {
        verseId: 'verse-3',
        verseNumber: 3,
        chapterNumber: 2,
      },
    }));

    await waitFor(() => {
      expect(screen.getByText('Continue Reading →')).toBeTruthy();
    });

    const action = screen.getByText('Continue Reading →');
    expect(action.props.accessibilityRole).not.toBe('header');
    const heading = screen.getByTestId('home-invitation-heading');
    expect(heading.props.accessibilityRole).toBe('header');
  });

  it('uses minimum 44pt touch targets for invitation and browse', () => {
    expect(homeSpacing.minTouchTarget).toBeGreaterThanOrEqual(44);
  });

  it('does not use fixed-height clipping on invitation labels', async () => {
    renderHome(async () => ({
      kind: 'continue_reading',
      destination: {
        verseId: 'verse-3',
        verseNumber: 3,
        chapterNumber: 2,
      },
    }));

    await waitFor(() => {
      expect(screen.getByText('Continue Reading →')).toBeTruthy();
    });

    const action = screen.getByText('Continue Reading →');
    const style = Array.isArray(action.props.style)
      ? Object.assign({}, ...action.props.style)
      : action.props.style;
    expect(style.height).toBeUndefined();
    expect(action.props.numberOfLines).toBeUndefined();
  });
});
