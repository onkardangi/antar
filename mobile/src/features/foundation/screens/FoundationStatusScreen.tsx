import { useCallback, useEffect, useState } from 'react';
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from 'react-native';

import { color, spacing, typography } from '../../../design-system';
import { ApiError } from '../../../services/api/apiError';
import { getApiBaseUrl } from '../../../services/api/configuration';
import {
  getFoundationStatus,
  type FoundationStatus,
} from '../../../services/api/foundationClient';

type LoadState =
  | { kind: 'loading' }
  | { kind: 'success'; status: FoundationStatus; baseUrl: string }
  | { kind: 'error'; message: string; baseUrl: string };

type Props = {
  loadStatus?: () => Promise<FoundationStatus>;
};

export function FoundationStatusScreen({ loadStatus = getFoundationStatus }: Props) {
  const [state, setState] = useState<LoadState>({ kind: 'loading' });

  const refresh = useCallback(async () => {
    const baseUrl = getApiBaseUrl();
    setState({ kind: 'loading' });

    try {
      const status = await loadStatus();
      setState({ kind: 'success', status, baseUrl });
    } catch (error) {
      const message =
        error instanceof ApiError
          ? error.message
          : 'Unable to verify backend connectivity.';
      setState({ kind: 'error', message, baseUrl });
    }
  }, [loadStatus]);

  useEffect(() => {
    // Initial connectivity check for the foundation shell.
    // eslint-disable-next-line react-hooks/set-state-in-effect -- intentional mount-time fetch
    void refresh();
  }, [refresh]);

  if (state.kind === 'loading') {
    return (
      <View style={styles.container} testID="foundation-loading">
        <ActivityIndicator color={color.accent} />
        <Text style={styles.body}>Checking backend connectivity…</Text>
      </View>
    );
  }

  if (state.kind === 'error') {
    return (
      <View style={styles.container} testID="foundation-error">
        <Text style={styles.title}>Backend unreachable</Text>
        <Text style={styles.body}>{state.message}</Text>
        <Text style={styles.caption}>API base URL: {state.baseUrl}</Text>
        <Pressable accessibilityRole="button" onPress={() => void refresh()} style={styles.button}>
          <Text style={styles.buttonLabel}>Retry</Text>
        </Pressable>
      </View>
    );
  }

  return (
    <View style={styles.container} testID="foundation-success">
      <Text style={styles.title}>Backend reachable</Text>
      <Text style={styles.body}>
        {state.status.service} reports {state.status.status}.
      </Text>
      <Text style={styles.caption}>API base URL: {state.baseUrl}</Text>
      <Pressable accessibilityRole="button" onPress={() => void refresh()} style={styles.button}>
        <Text style={styles.buttonLabel}>Refresh</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: color.background,
    justifyContent: 'center',
    padding: spacing.lg,
    gap: spacing.md,
  },
  title: {
    ...typography.title,
    color: color.text,
  },
  body: {
    ...typography.body,
    color: color.textMuted,
  },
  caption: {
    ...typography.caption,
    color: color.textMuted,
  },
  button: {
    alignSelf: 'flex-start',
    backgroundColor: color.accent,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
  },
  buttonLabel: {
    ...typography.body,
    color: color.surface,
  },
});
