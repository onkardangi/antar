import { Platform } from 'react-native';

/**
 * Resolves the backend base URL for the current runtime.
 *
 * Prefer EXPO_PUBLIC_API_BASE_URL.
 * Without it, development defaults are:
 * - Android emulator: http://10.0.2.2:8080
 * - iOS simulator / other: http://localhost:8080
 *
 * Physical devices must set EXPO_PUBLIC_API_BASE_URL to the
 * development machine LAN address or an approved tunnel URL.
 */
export function getApiBaseUrl(): string {
  const configured = process.env.EXPO_PUBLIC_API_BASE_URL?.trim();
  if (configured) {
    return configured.replace(/\/$/, '');
  }

  if (Platform.OS === 'android') {
    return 'http://10.0.2.2:8080';
  }

  return 'http://localhost:8080';
}
