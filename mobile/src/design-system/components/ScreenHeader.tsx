import { Pressable, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { color } from '../tokens/color';
import { librarySpacing, screenHeaderSpacing } from '../tokens/spacing';
import { typography } from '../tokens/typography';

export type ScreenHeaderLayout = 'stacked' | 'inline';

type Props = {
  /**
   * Header title. Defaults to `Antar`.
   * Pass `null` to omit the title entirely (Library: scripture owns page identity).
   */
  title?: string | null;
  /**
   * When provided, renders the Back action. Omit entirely when navigation
   * cannot go back — do not pass a no-op.
   */
  onBack?: () => void;
  /**
   * `stacked` (default): Back above title — Library’s reviewed layout.
   * `inline`: Back and title on one horizontal row — Chapter physical-device review.
   */
  layout?: ScreenHeaderLayout;
  /**
   * Padding below the header content before the following hairline.
   * Defaults to Library’s reviewed 16px. Chapter passes its own token.
   * Shared top/horizontal/gap metrics come from `screenHeaderSpacing`.
   */
  paddingBottom?: number;
  testID?: string;
};

export function ScreenHeader({
  title = 'Antar',
  onBack,
  layout = 'stacked',
  paddingBottom = librarySpacing.headerBottom,
  testID = 'screen-header',
}: Props) {
  const insets = useSafeAreaInsets();
  const showBack = typeof onBack === 'function';
  const showTitle = title != null;
  const inline = layout === 'inline' && showBack;

  const backControl = showBack ? (
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
  ) : null;

  const titleNode = showTitle ? (
    <Text accessibilityRole="header" style={styles.title}>
      {title}
    </Text>
  ) : null;

  return (
    <View
      style={[
        styles.container,
        {
          // Safe-area top is applied exactly once here — callers must not wrap
          // ScreenHeader in an additional full-screen SafeAreaView.
          paddingTop: insets.top + screenHeaderSpacing.headerContentTop,
          paddingBottom,
        },
        inline ? null : styles.stacked,
      ]}
      testID={testID}
    >
      {inline ? (
        <View style={styles.inlineRow} testID="screen-header-inline-row">
          {backControl}
          {titleNode}
        </View>
      ) : (
        <>
          {backControl}
          {titleNode}
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: screenHeaderSpacing.horizontalPadding,
  },
  stacked: {
    alignItems: 'flex-start',
    gap: screenHeaderSpacing.headerBackToTitleGap,
  },
  inlineRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    alignSelf: 'stretch',
    minHeight: screenHeaderSpacing.minTouchTarget,
  },
  backTarget: {
    minHeight: screenHeaderSpacing.minTouchTarget,
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
