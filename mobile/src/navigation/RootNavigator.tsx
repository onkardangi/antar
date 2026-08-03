import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { FoundationStatusScreen } from '../features/foundation/screens/FoundationStatusScreen';
import { ChapterPlaceholderScreen } from '../features/library/screens/ChapterPlaceholderScreen';
import { LibraryScreen } from '../features/library/screens/LibraryScreen';
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
        <Stack.Screen name="ChapterPlaceholder" component={ChapterPlaceholderScreen} />
        <Stack.Screen name="FoundationStatus" component={FoundationStatusScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
