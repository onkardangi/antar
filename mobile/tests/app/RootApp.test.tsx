import { render, screen, waitFor } from '@testing-library/react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { AppBootstrap } from '../../src/app/AppBootstrap';
import { TEST_WINDOW_METRICS } from '../../src/test/renderWithProviders';

jest.mock('../../src/features/library/api/chapterClient', () => ({
  listChapters: jest.fn(
    () =>
      new Promise(() => {
        // Keep Begin Journey canonical-start resolution pending.
      }),
  ),
}));

jest.mock('../../src/design-system/fonts/AppFonts', () => ({
  AppFonts: ({ children }: { children: React.ReactNode }) => children,
}));

describe('application shell', () => {
  it('renders the Home navigation shell as the primary route', async () => {
    render(
      <SafeAreaProvider initialMetrics={TEST_WINDOW_METRICS}>
        <AppBootstrap />
      </SafeAreaProvider>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('home-screen')).toBeTruthy();
    });
    expect(screen.getByTestId('home-invitation-heading')).toBeTruthy();
    expect(screen.getByTestId('home-browse')).toBeTruthy();
    expect(screen.getByTestId('home-invitation-loading')).toBeTruthy();
  });
});
