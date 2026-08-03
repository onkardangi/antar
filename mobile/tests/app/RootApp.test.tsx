import { render, screen } from '@testing-library/react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { AppBootstrap } from '../../src/app/AppBootstrap';
import { TEST_WINDOW_METRICS } from '../../src/test/renderWithProviders';

jest.mock('../../src/services/api/foundationClient', () => ({
  getFoundationStatus: jest.fn(
    () =>
      new Promise(() => {
        // Keep the shell on the loading state for this render assertion.
      }),
  ),
}));

describe('application shell', () => {
  it('renders the foundation navigation shell', () => {
    render(
      <SafeAreaProvider initialMetrics={TEST_WINDOW_METRICS}>
        <AppBootstrap />
      </SafeAreaProvider>,
    );

    expect(screen.getByTestId('foundation-loading')).toBeTruthy();
    expect(screen.getByText('Checking backend connectivity…')).toBeTruthy();
  });
});
