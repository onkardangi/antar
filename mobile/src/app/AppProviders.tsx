import { useCallback, useMemo, type ReactNode } from 'react';
import { SafeAreaProvider, type Metrics } from 'react-native-safe-area-context';

import { AppFonts } from '../design-system/fonts/AppFonts';
import { loadTodaysInvitation } from '../features/home/application/loadTodaysInvitation';
import {
  HomeInvitationProvider,
  type LoadTodaysInvitationFn,
} from '../features/home/composition/HomeInvitationProvider';
import type { ReadingProgressService } from '../features/reading-progress/application/ReadingProgressService';
import { ReadingProgressProvider } from '../features/reading-progress/composition/ReadingProgressProvider';
import { createReadingProgressStack } from '../features/reading-progress/composition/createReadingProgressStack';
import type { ReadingProgressRepository } from '../features/reading-progress/storage/ReadingProgressRepository';
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
  /**
   * Optional Reading Progress service override for tests (e.g. Verse).
   */
  readingProgressService?: ReadingProgressService;
  /**
   * Optional shared repository for tests that need Home loader + service
   * against the same storage.
   */
  readingProgressRepository?: ReadingProgressRepository;
  /**
   * Optional Home invitation loader override for tests.
   */
  loadTodaysInvitation?: LoadTodaysInvitationFn;
};

export function AppProviders({
  children,
  initialMetrics,
  skipFontLoading = false,
  readingProgressService: serviceOverride,
  readingProgressRepository: repositoryOverride,
  loadTodaysInvitation: loadOverride,
}: Props) {
  const productionStack = useMemo(() => {
    if (serviceOverride != null && repositoryOverride == null) {
      return null;
    }
    if (serviceOverride != null && repositoryOverride != null) {
      return {
        service: serviceOverride,
        repository: repositoryOverride,
      };
    }
    return createReadingProgressStack({
      repository: repositoryOverride,
    });
  }, [serviceOverride, repositoryOverride]);

  const service = serviceOverride ?? productionStack?.service;
  if (service == null) {
    throw new Error('AppProviders could not resolve ReadingProgressService');
  }

  const composedLoad = useCallback<LoadTodaysInvitationFn>(() => {
    const repository = productionStack?.repository ?? repositoryOverride;
    if (repository == null) {
      throw new Error(
        'Home invitation loader requires a Reading Progress repository',
      );
    }
    return loadTodaysInvitation({
      loadProgress: () => repository.load(),
    });
  }, [productionStack, repositoryOverride]);

  const loadInvitation = loadOverride ?? composedLoad;

  const content = skipFontLoading ? children : <AppFonts>{children}</AppFonts>;

  return (
    <SafeAreaProvider {...(initialMetrics ? { initialMetrics } : {})}>
      <AppErrorBoundary>
        <ReadingProgressProvider service={service}>
          <HomeInvitationProvider loadTodaysInvitation={loadInvitation}>
            {content}
          </HomeInvitationProvider>
        </ReadingProgressProvider>
      </AppErrorBoundary>
    </SafeAreaProvider>
  );
}
