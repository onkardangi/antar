import '@testing-library/react-native/matchers';

import { mockAsyncStorage, resetAsyncStorageMock } from './asyncStorageMock';

jest.mock('@react-native-async-storage/async-storage', () => ({
  __esModule: true,
  default: mockAsyncStorage,
}));

jest.mock('expo-font', () => ({
  useFonts: jest.fn(() => [true, null]),
  loadAsync: jest.fn(async () => undefined),
  isLoaded: () => true,
}));

beforeEach(() => {
  resetAsyncStorageMock();
});
