import { StyleSheet, Text, View } from 'react-native';

import { color, typography, verseSpacing } from '../../../design-system';
import type { VerseTranslation } from '../model/translationTypes';

export type TranslationBlockState =
  | { kind: 'loading' }
  | { kind: 'ready'; translation: VerseTranslation }
  | { kind: 'unavailable' };

type Props = {
  state: TranslationBlockState;
};

/**
 * Subordinate Translation layer of the Verse Reader Scripture Stack.
 * Visually quieter than Sanskrit. No cards, icons, or callouts.
 */
export function TranslationBlock({ state }: Props) {
  return (
    <View
      style={styles.container}
      testID="verse-translation-block"
      accessibilityLabel="Translation"
    >
      <Text
        style={styles.label}
        testID="verse-translation-label"
        accessibilityRole="header"
      >
        Translation
      </Text>

      {state.kind === 'loading' ? (
        <Text
          style={styles.placeholder}
          testID="verse-translation-loading"
          accessibilityLabel="Loading translation"
        >
          Loading translation…
        </Text>
      ) : null}

      {state.kind === 'unavailable' ? (
        <Text
          style={styles.placeholder}
          testID="verse-translation-unavailable"
          accessibilityLabel="Translation unavailable"
        >
          Translation unavailable.
        </Text>
      ) : null}

      {state.kind === 'ready' ? (
        <>
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
        </>
      ) : null}
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
  placeholder: {
    ...typography.versePreviewTemporary,
    color: color.textTertiary,
  },
});
