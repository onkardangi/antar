import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { ChapterScreen } from '../features/chapter/screens/ChapterScreen';
import { FoundationStatusScreen } from '../features/foundation/screens/FoundationStatusScreen';
import { LibraryScreen } from '../features/library/screens/LibraryScreen';
import { VersePlaceholderScreen } from '../features/verse/screens/VersePlaceholderScreen';
import { color } from '../design-system';
import type { RootStackParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();

export function RootNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Library"
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: color.background },
        }}
      >
        <Stack.Screen name="Library" component={LibraryScreen} />
        <Stack.Screen name="Chapter" component={ChapterScreen} />
        <Stack.Screen name="VersePlaceholder" component={VersePlaceholderScreen} />
        <Stack.Screen name="FoundationStatus" component={FoundationStatusScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
