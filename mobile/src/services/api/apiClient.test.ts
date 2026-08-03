import { apiGet } from './apiClient';
import { ApiError } from './apiError';

describe('apiGet', () => {
  it('maps a successful JSON response', async () => {
    const fetchImpl = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'UP', service: 'antar-backend' }),
    });

    const result = await apiGet<{ status: string; service: string }>(
      '/api/internal/foundation/status',
      {
        baseUrl: 'http://example.test',
        fetchImpl,
      },
    );

    expect(fetchImpl).toHaveBeenCalledWith('http://example.test/api/internal/foundation/status', {
      method: 'GET',
      headers: { Accept: 'application/json' },
    });
    expect(result).toEqual({ status: 'UP', service: 'antar-backend' });
  });

  it('maps network failures to ApiError', async () => {
    const fetchImpl = jest.fn().mockRejectedValue(new Error('offline'));

    await expect(
      apiGet('/api/internal/foundation/status', {
        baseUrl: 'http://example.test',
        fetchImpl,
      }),
    ).rejects.toEqual(
      expect.objectContaining({
        name: 'ApiError',
        kind: 'network',
      }),
    );
  });

  it('maps non-OK responses to ApiError', async () => {
    const fetchImpl = jest.fn().mockResolvedValue({
      ok: false,
      status: 503,
      json: async () => ({}),
    });

    await expect(
      apiGet('/api/internal/foundation/status', {
        baseUrl: 'http://example.test',
        fetchImpl,
      }),
    ).rejects.toBeInstanceOf(ApiError);
  });
});
