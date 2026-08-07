import { Pressable, StyleSheet, Text } from 'react-native';

import { color, homeSpacing, typography } from '../../../design-system';

type Props = {
  onPress: () => void;
};

/**
 * Quiet secondary path into Library. Never competes with Today's Invitation.
 */
export function BrowseBhagavadGita({ onPress }: Props) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel="Browse Bhagavad Gita"
      hitSlop={8}
      onPress={onPress}
      style={({ pressed }) => [
        styles.target,
        pressed ? styles.pressed : null,
      ]}
      testID="home-browse"
    >
      <Text style={styles.label}>Browse Bhagavad Gita →</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  target: {
    minHeight: homeSpacing.minTouchTarget,
    justifyContent: 'center',
    paddingHorizontal: homeSpacing.horizontalPadding,
    alignSelf: 'stretch',
  },
  pressed: {
    opacity: 0.55,
  },
  label: {
    ...typography.homeBrowse,
    color: color.textSecondary,
  },
});
