import type { LocalStorage } from '../../../storage/local/LocalStorage';

/**
 * In-memory LocalStorage for unit tests.
 */
export class MemoryLocalStorage implements LocalStorage {
  private readonly values = new Map<string, string>();
  getItemFailure: Error | null = null;
  setItemFailure: Error | null = null;
  removeItemFailure: Error | null = null;
  setItemCalls: Array<{ key: string; value: string }> = [];

  async getItem(key: string): Promise<string | null> {
    if (this.getItemFailure) {
      throw this.getItemFailure;
    }
    return this.values.has(key) ? this.values.get(key)! : null;
  }

  async setItem(key: string, value: string): Promise<void> {
    this.setItemCalls.push({ key, value });
    if (this.setItemFailure) {
      throw this.setItemFailure;
    }
    this.values.set(key, value);
  }

  async removeItem(key: string): Promise<void> {
    if (this.removeItemFailure) {
      throw this.removeItemFailure;
    }
    this.values.delete(key);
  }

  seed(key: string, value: string): void {
    this.values.set(key, value);
  }

  peek(key: string): string | null {
    return this.values.has(key) ? this.values.get(key)! : null;
  }
}
