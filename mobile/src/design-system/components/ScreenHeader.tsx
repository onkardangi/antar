import { Pressable, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { color } from '../tokens/color';
import { librarySpacing } from '../tokens/spacing';
import { typography } from '../tokens/typography';

type Props = {
  title?: string;
  /**
   * When provided, renders the Back action. Omit entirely when navigation
   * cannot go back — do not pass a no-op.
   */
  onBack?: () => void;
  testID?: string;
};

export function ScreenHeader({
  title = 'Antar',
  onBack,
  testID = 'screen-header',
}: Props) {
  const insets = useSafeAreaInsets();
  const showBack = typeof onBack === 'function';

  return (
    <View
      style={[
        styles.container,
        {
          paddingTop: insets.top + librarySpacing.headerContentTop,
          paddingBottom: librarySpacing.headerBottom,
        },
      ]}
      testID={testID}
    >
      {showBack ? (
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Go back"
          hitSlop={8}
          onPress={onBack}
          style={({ pressed }) => [
            styles.backTarget,
            pressed ? styles.backPressed : null,
          ]}
          testID="screen-header-back"
        >
          <Text style={styles.backLabel}>Back</Text>
        </Pressable>
      ) : null}
      <Text accessibilityRole="header" style={styles.title}>
        {title}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: librarySpacing.horizontalPadding,
    alignItems: 'flex-start',
    gap: librarySpacing.headerBackToTitleGap,
  },
  backTarget: {
    minHeight: librarySpacing.minTouchTarget,
    justifyContent: 'center',
  },
  backPressed: {
    opacity: 0.55,
  },
  backLabel: {
    ...typography.backNavigation,
    color: color.textSecondary,
  },
  title: {
    ...typography.applicationTitle,
    color: color.text,
  },
});
