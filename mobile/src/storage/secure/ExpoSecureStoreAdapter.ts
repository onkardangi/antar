import * as ExpoSecureStore from 'expo-secure-store';

import type { SecureStorage } from './SecureStorage';

/**
 * Expo SecureStore adapter.
 *
 * Added so future authentication can store credentials outside AsyncStorage
 * without introducing auth flows in this foundation milestone.
 */
export class ExpoSecureStoreAdapter implements SecureStorage {
  getItem(key: string): Promise<string | null> {
    return ExpoSecureStore.getItemAsync(key);
  }

  setItem(key: string, value: string): Promise<void> {
    return ExpoSecureStore.setItemAsync(key, value);
  }

  deleteItem(key: string): Promise<void> {
    return ExpoSecureStore.deleteItemAsync(key);
  }
}
