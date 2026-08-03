export class ApiError extends Error {
  readonly status?: number;
  readonly kind: 'network' | 'http' | 'parse' | 'configuration';

  constructor(
    message: string,
    options?: {
      status?: number;
      kind?: 'network' | 'http' | 'parse' | 'configuration';
      cause?: unknown;
    },
  ) {
    super(message, options?.cause ? { cause: options.cause } : undefined);
    this.name = 'ApiError';
    this.status = options?.status;
    this.kind = options?.kind ?? 'network';
  }
}
