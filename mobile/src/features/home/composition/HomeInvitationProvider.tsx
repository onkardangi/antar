import {
  createContext,
  useContext,
  useMemo,
  type ReactNode,
} from 'react';

import type { TodaysInvitationState } from '../model/todaysInvitation';

export type LoadTodaysInvitationFn = () => Promise<TodaysInvitationState>;

export const HomeInvitationContext =
  createContext<LoadTodaysInvitationFn | null>(null);

type Props = {
  children: ReactNode;
  loadTodaysInvitation: LoadTodaysInvitationFn;
};

/**
 * Supplies the Home-level invitation loader to HomeScreen.
 * The loader returns TodaysInvitationState only — never storage sources.
 */
export function HomeInvitationProvider({
  children,
  loadTodaysInvitation,
}: Props) {
  const value = useMemo(() => loadTodaysInvitation, [loadTodaysInvitation]);

  return (
    <HomeInvitationContext.Provider value={value}>
      {children}
    </HomeInvitationContext.Provider>
  );
}

export function useLoadTodaysInvitation(): LoadTodaysInvitationFn {
  const load = useContext(HomeInvitationContext);
  if (load == null) {
    throw new Error(
      'useLoadTodaysInvitation requires HomeInvitationProvider',
    );
  }
  return load;
}
