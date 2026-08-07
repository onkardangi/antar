import type { ReadingProgressLoadResult } from '../../reading-progress/model/readingProgressTypes';
import { resolveCanonicalStart } from '../api/resolveCanonicalStart';
import type { TodaysInvitationState } from '../model/todaysInvitation';
import { interpretProgressLoad } from './interpretProgressLoad';

export type LoadTodaysInvitationDeps = {
  /**
   * Home-bound progress load. Production wires repository.load().
   * The LoadResult type is an implementation detail of this loader — not a
   * HomeScreen or cross-feature contract.
   */
  loadProgress: () => Promise<ReadingProgressLoadResult>;
  resolveCanonicalStart?: typeof resolveCanonicalStart;
};

/**
 * Loads and interprets local Reading Progress into Home invitation state.
 *
 * Does not write or clear storage. Transient read failures become
 * `progress_unavailable`, never Begin Journey.
 */
export async function loadTodaysInvitation(
  deps: LoadTodaysInvitationDeps,
): Promise<TodaysInvitationState> {
  const load = await deps.loadProgress();
  const decision = interpretProgressLoad(load);

  if (decision.kind === 'progress_unavailable') {
    return { kind: 'progress_unavailable' };
  }

  if (decision.kind === 'continue_reading') {
    return {
      kind: 'continue_reading',
      destination: decision.destination,
    };
  }

  const resolveStart = deps.resolveCanonicalStart ?? resolveCanonicalStart;
  const destination = await resolveStart();
  if (destination == null) {
    return { kind: 'begin_journey', resolution: 'unavailable' };
  }

  return {
    kind: 'begin_journey',
    resolution: 'ready',
    destination,
  };
}
