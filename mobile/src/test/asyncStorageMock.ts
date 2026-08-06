/**
 * Shared Jest AsyncStorage stand-in.
 * Reset between tests so suites do not leak progress documents.
 */

const store = new Map<string, string>();

function createGetItem() {
  return jest.fn(async (key: string): Promise<string | null> =>
    store.has(key) ? store.get(key)! : null,
  );
}

function createSetItem() {
  return jest.fn(async (key: string, value: string): Promise<void> => {
    store.set(key, value);
  });
}

function createRemoveItem() {
  return jest.fn(async (key: string): Promise<void> => {
    store.delete(key);
  });
}

function createClear() {
  return jest.fn(async (): Promise<void> => {
    store.clear();
  });
}

export const mockAsyncStorage = {
  getItem: createGetItem(),
  setItem: createSetItem(),
  removeItem: createRemoveItem(),
  clear: createClear(),
};

/** Clear stored values, failure overrides, and call history. */
export function resetAsyncStorageMock(): void {
  store.clear();
  mockAsyncStorage.getItem.mockReset();
  mockAsyncStorage.setItem.mockReset();
  mockAsyncStorage.removeItem.mockReset();
  mockAsyncStorage.clear.mockReset();
  mockAsyncStorage.getItem.mockImplementation(async (key: string) =>
    store.has(key) ? store.get(key)! : null,
  );
  mockAsyncStorage.setItem.mockImplementation(
    async (key: string, value: string) => {
      store.set(key, value);
    },
  );
  mockAsyncStorage.removeItem.mockImplementation(async (key: string) => {
    store.delete(key);
  });
  mockAsyncStorage.clear.mockImplementation(async () => {
    store.clear();
  });
}

/** Test helper for seeding the mock store. */
export function seedAsyncStorageMock(key: string, value: string): void {
  store.set(key, value);
}

/** Test helper for inspecting the mock store. */
export function peekAsyncStorageMock(key: string): string | null {
  return store.has(key) ? store.get(key)! : null;
}
