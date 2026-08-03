import { StatusBar } from 'expo-status-bar';

import { RootNavigator } from '../navigation/RootNavigator';
import { AppProviders } from './AppProviders';

export function AppBootstrap() {
  return (
    <AppProviders>
      <StatusBar style="dark" />
      <RootNavigator />
    </AppProviders>
  );
}
