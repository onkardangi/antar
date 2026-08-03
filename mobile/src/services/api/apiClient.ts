import { ApiError } from './apiError';
import { getApiBaseUrl } from './configuration';

export type ApiClientOptions = {
  baseUrl?: string;
  fetchImpl?: typeof fetch;
};

export async function apiGet<T>(path: string, options: ApiClientOptions = {}): Promise<T> {
  const baseUrl = options.baseUrl ?? getApiBaseUrl();
  const fetchImpl = options.fetchImpl ?? fetch;
  const url = `${baseUrl}${path.startsWith('/') ? path : `/${path}`}`;

  let response: Response;
  try {
    response = await fetchImpl(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    });
  } catch (cause) {
    throw new ApiError('Unable to reach the Antar backend.', {
      kind: 'network',
      cause,
    });
  }

  if (!response.ok) {
    throw new ApiError(`Backend responded with HTTP ${response.status}.`, {
      kind: 'http',
      status: response.status,
    });
  }

  try {
    return (await response.json()) as T;
  } catch (cause) {
    throw new ApiError('Backend returned an unreadable response.', {
      kind: 'parse',
      cause,
    });
  }
}
