/**
 * Future boundary for sensitive local values such as auth tokens.
 * No authentication flow is implemented in the foundation milestone.
 */
export interface SecureStorage {
  getItem(key: string): Promise<string | null>;
  setItem(key: string, value: string): Promise<void>;
  deleteItem(key: string): Promise<void>;
}
