import { Text, View } from 'react-native';
import { render, screen } from '@testing-library/react-native';
import { useFonts } from 'expo-font';

import { AppFonts } from './AppFonts';

jest.mock('expo-font', () => ({
  useFonts: jest.fn(),
}));

const mockUseFonts = useFonts as jest.MockedFunction<typeof useFonts>;

describe('AppFonts', () => {
  afterEach(() => {
    mockUseFonts.mockReset();
  });

  it('renders children when fonts load successfully', () => {
    mockUseFonts.mockReturnValue([true, null]);

    render(
      <AppFonts>
        <Text testID="app-shell">Antar</Text>
      </AppFonts>,
    );

    expect(screen.getByTestId('app-shell')).toBeTruthy();
    expect(screen.queryByTestId('app-fonts-loading')).toBeNull();
  });

  it('shows a controlled loading surface while fonts are still loading', () => {
    mockUseFonts.mockReturnValue([false, null]);

    render(
      <AppFonts>
        <Text testID="app-shell">Antar</Text>
      </AppFonts>,
    );

    expect(screen.getByTestId('app-fonts-loading')).toBeTruthy();
    expect(screen.queryByTestId('app-shell')).toBeNull();
  });

  it('renders children with system-font fallback when font loading fails', () => {
    mockUseFonts.mockReturnValue([false, new Error('Font download failed')]);

    render(
      <AppFonts>
        <View testID="app-shell">
          <Text>Antar</Text>
        </View>
      </AppFonts>,
    );

    expect(screen.getByTestId('app-shell')).toBeTruthy();
    expect(screen.queryByTestId('app-fonts-loading')).toBeNull();
  });
});
