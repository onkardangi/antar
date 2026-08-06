/**
 * Ordinary durable local key-value storage.
 *
 * Use for non-secret Reader state such as Reading Progress.
 * Authentication secrets remain on the SecureStorage boundary.
 */
export interface LocalStorage {
  getItem(key: string): Promise<string | null>;
  setItem(key: string, value: string): Promise<void>;
  removeItem(key: string): Promise<void>;
}
