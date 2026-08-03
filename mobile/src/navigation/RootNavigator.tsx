import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { FoundationStatusScreen } from '../features/foundation/screens/FoundationStatusScreen';
import { color } from '../design-system';
import type { RootStackParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();

export function RootNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerStyle: { backgroundColor: color.background },
          headerTintColor: color.text,
          contentStyle: { backgroundColor: color.background },
        }}
      >
        <Stack.Screen
          name="FoundationStatus"
          component={FoundationStatusScreen}
          options={{ title: 'Foundation Status' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
