import { Component, type ErrorInfo, type ReactNode } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import { color, spacing, typography } from '../design-system';

type Props = {
  children: ReactNode;
};

type State = {
  hasError: boolean;
  message: string;
};

export class AppErrorBoundary extends Component<Props, State> {
  state: State = {
    hasError: false,
    message: '',
  };

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      message: error.message || 'Unexpected application error',
    };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    console.error('AppErrorBoundary caught an error', error, info.componentStack);
  }

  private handleRetry = (): void => {
    this.setState({ hasError: false, message: '' });
  };

  render(): ReactNode {
    if (!this.state.hasError) {
      return this.props.children;
    }

    return (
      <View style={styles.container}>
        <Text style={styles.title}>Something went wrong</Text>
        <Text style={styles.body}>{this.state.message}</Text>
        <Pressable accessibilityRole="button" onPress={this.handleRetry} style={styles.button}>
          <Text style={styles.buttonLabel}>Retry</Text>
        </Pressable>
      </View>
    );
  }
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
