import AsyncStorage from '@react-native-async-storage/async-storage';

import type { LocalStorage } from './LocalStorage';

/**
 * Expo-compatible AsyncStorage adapter for non-secret local persistence.
 */
export class AsyncStorageAdapter implements LocalStorage {
  getItem(key: string): Promise<string | null> {
    return AsyncStorage.getItem(key);
  }

  setItem(key: string, value: string): Promise<void> {
    return AsyncStorage.setItem(key, value);
  }

  removeItem(key: string): Promise<void> {
    return AsyncStorage.removeItem(key);
  }
}
