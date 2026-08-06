import AsyncStorage from '@react-native-async-storage/async-storage';

import {
  peekAsyncStorageMock,
  seedAsyncStorageMock,
} from '../../../test/asyncStorageMock';
import { READING_PROGRESS_STORAGE_KEY } from './readingProgressStorageKey';

describe('AsyncStorage Jest mock isolation', () => {
  it('starts empty after setup beforeEach reset', async () => {
    expect(await AsyncStorage.getItem(READING_PROGRESS_STORAGE_KEY)).toBeNull();
    expect(peekAsyncStorageMock(READING_PROGRESS_STORAGE_KEY)).toBeNull();
  });

  it('does not leak a prior test seed into the next test', async () => {
    seedAsyncStorageMock(READING_PROGRESS_STORAGE_KEY, '{"leaked":true}');
    expect(await AsyncStorage.getItem(READING_PROGRESS_STORAGE_KEY)).toBe(
      '{"leaked":true}',
    );
  });

  it('confirms the previous test seed was cleared by beforeEach', async () => {
    expect(await AsyncStorage.getItem(READING_PROGRESS_STORAGE_KEY)).toBeNull();
    expect(peekAsyncStorageMock(READING_PROGRESS_STORAGE_KEY)).toBeNull();
    expect(AsyncStorage.setItem).toHaveBeenCalledTimes(0);
  });
});
