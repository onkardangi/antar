import { apiGet, type ApiClientOptions } from './apiClient';

export type FoundationStatus = {
  status: string;
  service: string;
};

export function getFoundationStatus(options?: ApiClientOptions): Promise<FoundationStatus> {
  return apiGet<FoundationStatus>('/api/internal/foundation/status', options);
}
