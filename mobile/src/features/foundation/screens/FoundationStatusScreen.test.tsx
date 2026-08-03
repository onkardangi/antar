import { act, fireEvent, screen, waitFor } from '@testing-library/react-native';

import { FoundationStatusScreen } from './FoundationStatusScreen';
import { renderWithProviders } from '../../../test/renderWithProviders';
import { ApiError } from '../../../services/api/apiError';

describe('FoundationStatusScreen', () => {
  it('shows a loading state while the backend request is in flight', async () => {
    let resolveRequest: ((value: { status: string; service: string }) => void) | undefined;
    const pending = new Promise<{ status: string; service: string }>((resolve) => {
      resolveRequest = resolve;
    });

    renderWithProviders(<FoundationStatusScreen loadStatus={() => pending} />);

    expect(screen.getByTestId('foundation-loading')).toBeTruthy();
    expect(screen.getByText('Checking backend connectivity…')).toBeTruthy();

    await act(async () => {
      resolveRequest?.({ status: 'UP', service: 'antar-backend' });
    });

    await waitFor(() => {
      expect(screen.getByTestId('foundation-success')).toBeTruthy();
    });
  });

  it('shows a success state when the backend responds', async () => {
    renderWithProviders(
      <FoundationStatusScreen
        loadStatus={async () => ({ status: 'UP', service: 'antar-backend' })}
      />,
    );

    await waitFor(() => {
      expect(screen.getByTestId('foundation-success')).toBeTruthy();
    });

    expect(screen.getByText('Backend reachable')).toBeTruthy();
    expect(screen.getByText('antar-backend reports UP.')).toBeTruthy();
  });

  it('shows a retryable failure state when the backend request fails', async () => {
    const loadStatus = jest
      .fn()
      .mockRejectedValueOnce(new ApiError('Unable to reach the Antar backend.', { kind: 'network' }))
      .mockResolvedValueOnce({ status: 'UP', service: 'antar-backend' });

    renderWithProviders(<FoundationStatusScreen loadStatus={loadStatus} />);

    await waitFor(() => {
      expect(screen.getByTestId('foundation-error')).toBeTruthy();
    });

    expect(screen.getByText('Backend unreachable')).toBeTruthy();
    fireEvent.press(screen.getByText('Retry'));

    await waitFor(() => {
      expect(screen.getByTestId('foundation-success')).toBeTruthy();
    });

    expect(loadStatus).toHaveBeenCalledTimes(2);
  });
});
