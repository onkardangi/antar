import { StyleSheet, View } from 'react-native';

import { color, verseSpacing } from '../../../design-system';

/**
 * Decorative Sanskrit reading-slot reserve while the Verse loads.
 * Neutral divider bars only — never fake scripture text.
 */
export function VerseSanskritSkeleton() {
  return (
    <View
      accessibilityElementsHidden
      importantForAccessibility="no"
      style={styles.stack}
      testID="verse-sanskrit-skeleton"
    >
      <View style={[styles.line, styles.lineWide]} />
      <View style={[styles.line, styles.lineMedium]} />
      <View style={[styles.line, styles.lineNarrow]} />
    </View>
  );
}

const styles = StyleSheet.create({
  stack: {
    gap: verseSpacing.skeletonLineGap,
  },
  line: {
    height: verseSpacing.skeletonLineHeight,
    backgroundColor: color.divider,
  },
  lineWide: {
    alignSelf: 'stretch',
  },
  lineMedium: {
    width: '84%',
    alignSelf: 'flex-start',
  },
  lineNarrow: {
    width: '62%',
    alignSelf: 'flex-start',
  },
});
