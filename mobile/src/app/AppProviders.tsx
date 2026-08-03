import type { ReactNode } from 'react';
import { SafeAreaProvider, type Metrics } from 'react-native-safe-area-context';

import { AppFonts } from '../design-system/fonts/AppFonts';
import { AppErrorBoundary } from './AppErrorBoundary';

type Props = {
  children: ReactNode;
  /**
   * Test-only safe-area metrics. Production and normal local runs omit this so
   * SafeAreaProvider measures the real window.
   */
  initialMetrics?: Metrics;
  /** Skip font loading gate in unit tests that do not need typefaces. */
  skipFontLoading?: boolean;
};

export function AppProviders({
  children,
  initialMetrics,
  skipFontLoading = false,
}: Props) {
  const content = skipFontLoading ? children : <AppFonts>{children}</AppFonts>;

  return (
    <SafeAreaProvider {...(initialMetrics ? { initialMetrics } : {})}>
      <AppErrorBoundary>{content}</AppErrorBoundary>
    </SafeAreaProvider>
  );
}
