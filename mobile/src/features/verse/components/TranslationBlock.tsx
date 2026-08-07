import { StyleSheet, Text, View } from 'react-native';

import { color, typography, verseSpacing } from '../../../design-system';
import type { VerseTranslation } from '../model/translationTypes';

export type TranslationBlockState =
  | { kind: 'loading' }
  | { kind: 'ready'; translation: VerseTranslation };

type Props = {
  state: TranslationBlockState;
};

/**
 * Subordinate Translation layer of the Verse Reader Scripture Stack.
 * Visually quieter than Sanskrit. No cards, icons, or callouts.
 * Unavailable Translation is omitted entirely by the parent (silent collapse).
 * Loading reserves space with decorative bars only — no prose, no label.
 */
export function TranslationBlock({ state }: Props) {
  if (state.kind === 'loading') {
    return (
      <View
        accessibilityElementsHidden
        importantForAccessibility="no"
        style={styles.container}
        testID="verse-translation-loading"
      >
        <View style={[styles.loadingBar, styles.loadingBarWide]} />
        <View style={[styles.loadingBar, styles.loadingBarMedium]} />
      </View>
    );
  }

  return (
    <View style={styles.container} testID="verse-translation-block">
      <Text
        style={styles.label}
        testID="verse-translation-label"
        accessibilityRole="header"
      >
        Translation
      </Text>
      <Text
        style={styles.provider}
        testID="verse-translation-provider"
        accessibilityLabel={`Provider ${state.translation.provider}`}
      >
        {state.translation.provider}
      </Text>
      <Text
        style={styles.body}
        testID="verse-translation-text"
        accessibilityLabel={state.translation.translationText}
      >
        {state.translation.translationText}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: verseSpacing.horizontalPadding,
    marginTop: verseSpacing.bodyToTranslationGap,
    gap: verseSpacing.translationStackGap,
  },
  label: {
    ...typography.sectionLabel,
    color: color.textSecondary,
  },
  provider: {
    ...typography.caption,
    color: color.textTertiary,
  },
  body: {
    ...typography.versePreview,
    color: color.textSupporting,
  },
  loadingBar: {
    height: verseSpacing.skeletonLineHeight,
    backgroundColor: color.divider,
  },
  loadingBarWide: {
    alignSelf: 'stretch',
  },
  loadingBarMedium: {
    width: '70%',
    alignSelf: 'flex-start',
  },
});
