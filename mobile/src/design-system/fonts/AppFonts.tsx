import type { ReactNode } from 'react';
import { View } from 'react-native';
import { useFonts } from 'expo-font';
import { Lora_400Regular } from '@expo-google-fonts/lora/400Regular';
import { Lora_400Regular_Italic } from '@expo-google-fonts/lora/400Regular_Italic';
import { SourceSans3_400Regular } from '@expo-google-fonts/source-sans-3/400Regular';

import { color } from '../tokens/color';

type Props = {
  children: ReactNode;
};

/**
 * Loads Library handoff typefaces before rendering the product shell.
 *
 * While fonts are still loading (and there is no error), renders an empty
 * background. If loading fails, renders children immediately so the app is
 * never blocked — Text uses system typefaces when custom faces are unavailable.
 */
export function AppFonts({ children }: Props) {
  const [loaded, error] = useFonts({
    Lora_400Regular,
    Lora_400Regular_Italic,
    SourceSans3_400Regular,
  });

  if (!loaded && !error) {
    return <View style={{ flex: 1, backgroundColor: color.background }} testID="app-fonts-loading" />;
  }

  return <>{children}</>;
}
