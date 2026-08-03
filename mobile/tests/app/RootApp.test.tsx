import { render, screen, waitFor } from '@testing-library/react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { AppBootstrap } from '../../src/app/AppBootstrap';
import { TEST_WINDOW_METRICS } from '../../src/test/renderWithProviders';

jest.mock('../../src/features/library/api/chapterClient', () => ({
  listChapters: jest.fn(
    () =>
      new Promise(() => {
        // Keep Library on the loading state for this render assertion.
      }),
  ),
}));

jest.mock('../../src/design-system/fonts/AppFonts', () => ({
  AppFonts: ({ children }: { children: React.ReactNode }) => children,
}));

describe('application shell', () => {
  it('renders the Library navigation shell as the primary route', async () => {
    render(
      <SafeAreaProvider initialMetrics={TEST_WINDOW_METRICS}>
        <AppBootstrap />
      </SafeAreaProvider>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('library-loading')).toBeTruthy();
    });
    expect(screen.getByTestId('scripture-introduction')).toBeTruthy();
    expect(screen.getByText('Bhagavad Gita')).toBeTruthy();
  });
});
