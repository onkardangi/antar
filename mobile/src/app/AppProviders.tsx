import type { ReactNode } from 'react';
import { SafeAreaProvider, type Metrics } from 'react-native-safe-area-context';

import { AppErrorBoundary } from './AppErrorBoundary';

type Props = {
  children: ReactNode;
  /**
   * Test-only safe-area metrics. Production and normal local runs omit this so
   * SafeAreaProvider measures the real window.
   */
  initialMetrics?: Metrics;
};

export function AppProviders({ children, initialMetrics }: Props) {
  return (
    <SafeAreaProvider {...(initialMetrics ? { initialMetrics } : {})}>
      <AppErrorBoundary>{children}</AppErrorBoundary>
    </SafeAreaProvider>
  );
}
