import type { ReactElement, ReactNode } from 'react';
import { render, type RenderOptions } from '@testing-library/react-native';
import type { Metrics } from 'react-native-safe-area-context';

import { AppProviders } from '../app/AppProviders';

export const TEST_WINDOW_METRICS: Metrics = {
  frame: { x: 0, y: 0, width: 390, height: 844 },
  insets: { top: 0, left: 0, right: 0, bottom: 0 },
};

function TestProviders({ children }: { children: ReactNode }) {
  return (
    <AppProviders initialMetrics={TEST_WINDOW_METRICS} skipFontLoading>
      {children}
    </AppProviders>
  );
}

export function renderWithProviders(ui: ReactElement, options?: Omit<RenderOptions, 'wrapper'>) {
  return render(ui, {
    wrapper: TestProviders,
    ...options,
  });
}
