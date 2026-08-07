import { Pressable, StyleSheet, Text, View } from 'react-native';

import { color, typography, verseSpacing } from '../../../design-system';

type Props = {
  previousEnabled: boolean;
  nextEnabled: boolean;
  onPrevious: () => void;
  onNext: () => void;
};

/**
 * In-chapter Previous / Next controls for the Verse Reader.
 * Visually quiet page-turn affordances; disabled at chapter ends.
 */
export function VerseNavigation({
  previousEnabled,
  nextEnabled,
  onPrevious,
  onNext,
}: Props) {
  return (
    <View style={styles.row} testID="verse-navigation">
      <Pressable
        accessibilityRole="button"
        accessibilityLabel="Previous verse"
        accessibilityState={{ disabled: !previousEnabled }}
        disabled={!previousEnabled}
        hitSlop={8}
        onPress={onPrevious}
        style={({ pressed }) => [
          styles.target,
          !previousEnabled ? styles.disabled : null,
          pressed && previousEnabled ? styles.pressed : null,
        ]}
        testID="verse-previous"
      >
        <Text style={styles.label}>Previous</Text>
      </Pressable>
      <Pressable
        accessibilityRole="button"
        accessibilityLabel="Next verse"
        accessibilityState={{ disabled: !nextEnabled }}
        disabled={!nextEnabled}
        hitSlop={8}
        onPress={onNext}
        style={({ pressed }) => [
          styles.target,
          !nextEnabled ? styles.disabled : null,
          pressed && nextEnabled ? styles.pressed : null,
        ]}
        testID="verse-next"
      >
        <Text style={styles.label}>Next</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: verseSpacing.horizontalPadding,
    gap: verseSpacing.navGap,
  },
  target: {
    minHeight: verseSpacing.minTouchTarget,
    minWidth: verseSpacing.minTouchTarget,
    justifyContent: 'center',
  },
  label: {
    ...typography.caption,
    color: color.textTertiary,
  },
  disabled: {
    opacity: 0.18,
  },
  pressed: {
    opacity: 0.55,
  },
});
