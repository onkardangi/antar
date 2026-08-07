import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { ChapterScreen } from '../features/chapter/screens/ChapterScreen';
import { FoundationStatusScreen } from '../features/foundation/screens/FoundationStatusScreen';
import { HomeScreen } from '../features/home/screens/HomeScreen';
import { LibraryScreen } from '../features/library/screens/LibraryScreen';
import { VerseScreen } from '../features/verse/screens/VerseScreen';
import { color } from '../design-system';
import type { RootStackParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();

/** Product initial route — Home Experience V1 Milestone A. */
export const ROOT_INITIAL_ROUTE_NAME: keyof RootStackParamList = 'Home';

export function RootNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName={ROOT_INITIAL_ROUTE_NAME}
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: color.background },
        }}
      >
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Library" component={LibraryScreen} />
        <Stack.Screen name="Chapter" component={ChapterScreen} />
        <Stack.Screen name="VerseReader" component={VerseScreen} />
        <Stack.Screen name="FoundationStatus" component={FoundationStatusScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
