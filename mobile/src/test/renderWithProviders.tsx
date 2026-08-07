import type { ReactElement, ReactNode } from 'react';
import { render, type RenderOptions } from '@testing-library/react-native';
import type { Metrics } from 'react-native-safe-area-context';

import { AppProviders } from '../app/AppProviders';
import type { LoadTodaysInvitationFn } from '../features/home/composition/HomeInvitationProvider';
import type { ReadingProgressService } from '../features/reading-progress/application/ReadingProgressService';
import type { ReadingProgressRepository } from '../features/reading-progress/storage/ReadingProgressRepository';

export const TEST_WINDOW_METRICS: Metrics = {
  frame: { x: 0, y: 0, width: 390, height: 844 },
  insets: { top: 0, left: 0, right: 0, bottom: 0 },
};

type TestProviderOptions = {
  readingProgressService?: ReadingProgressService;
  readingProgressRepository?: ReadingProgressRepository;
  loadTodaysInvitation?: LoadTodaysInvitationFn;
  /** Optional SafeArea metrics override (defaults to TEST_WINDOW_METRICS). */
  initialMetrics?: Metrics;
};

function TestProviders({
  children,
  readingProgressService,
  readingProgressRepository,
  loadTodaysInvitation,
  initialMetrics = TEST_WINDOW_METRICS,
}: { children: ReactNode } & TestProviderOptions) {
  return (
    <AppProviders
      initialMetrics={initialMetrics}
      skipFontLoading
      readingProgressService={readingProgressService}
      readingProgressRepository={readingProgressRepository}
      loadTodaysInvitation={loadTodaysInvitation}
    >
      {children}
    </AppProviders>
  );
}

export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'> & TestProviderOptions,
) {
  const {
    readingProgressService,
    readingProgressRepository,
    loadTodaysInvitation,
    initialMetrics,
    ...renderOptions
  } = options ?? {};
  return render(ui, {
    wrapper: ({ children }) => (
      <TestProviders
        readingProgressService={readingProgressService}
        readingProgressRepository={readingProgressRepository}
        loadTodaysInvitation={loadTodaysInvitation}
        initialMetrics={initialMetrics}
      >
        {children}
      </TestProviders>
    ),
    ...renderOptions,
  });
}
