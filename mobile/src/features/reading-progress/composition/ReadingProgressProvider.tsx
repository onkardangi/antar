import {
  createContext,
  useContext,
  useMemo,
  type ReactNode,
} from 'react';

import type { ReadingProgressService } from '../application/ReadingProgressService';
import { createReadingProgressService } from './createReadingProgressService';

const ReadingProgressContext = createContext<ReadingProgressService | null>(
  null,
);

type Props = {
  children: ReactNode;
  /**
   * Optional override for tests. Production omits this so the real
   * AsyncStorage-backed service is composed once.
   */
  service?: ReadingProgressService;
};

/**
 * Supplies the production Reading Progress service to the navigation tree.
 */
export function ReadingProgressProvider({ children, service }: Props) {
  const value = useMemo(
    () => service ?? createReadingProgressService(),
    [service],
  );

  return (
    <ReadingProgressContext.Provider value={value}>
      {children}
    </ReadingProgressContext.Provider>
  );
}

export function useReadingProgressService(): ReadingProgressService {
  const service = useContext(ReadingProgressContext);
  if (service == null) {
    throw new Error(
      'useReadingProgressService requires ReadingProgressProvider',
    );
  }
  return service;
}
