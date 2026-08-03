import { StyleSheet, Text, View } from 'react-native';

import { color } from '../tokens/color';
import { chapterSpacing } from '../tokens/spacing';
import { typography } from '../tokens/typography';

export type ChapterIntroductionProps = {
  chapterNumber: number;
  /** When omitted and showContentPlaceholders is true, a structural bar is shown. */
  canonicalName?: string;
  /** When omitted and showContentPlaceholders is true, a structural bar is shown. */
  shortIntent?: string;
  /**
   * When true (default) and name/intent are missing, render restrained placeholders.
   * Set false for Chapter-level error so the UI does not look like loading.
   */
  showContentPlaceholders?: boolean;
  testID?: string;
};

export function chapterIntroductionLabel(chapterNumber: number): string {
  return `CHAPTER ${chapterNumber}`;
}

export function ChapterIntroduction({
  chapterNumber,
  canonicalName,
  shortIntent,
  showContentPlaceholders = true,
  testID = 'chapter-introduction',
}: ChapterIntroductionProps) {
  const showName = typeof canonicalName === 'string' && canonicalName.length > 0;
  const showIntent = typeof shortIntent === 'string' && shortIntent.length > 0;

  return (
    <View style={styles.container} testID={testID}>
      <Text style={styles.label}>{chapterIntroductionLabel(chapterNumber)}</Text>

      {showName ? (
        <Text accessibilityRole="header" style={styles.name}>
          {canonicalName}
        </Text>
      ) : showContentPlaceholders ? (
        <View
          accessibilityElementsHidden
          importantForAccessibility="no"
          style={styles.namePlaceholder}
          testID="chapter-introduction-name-placeholder"
        />
      ) : null}

      {showIntent ? (
        <Text style={styles.intent}>{shortIntent}</Text>
      ) : showContentPlaceholders ? (
        <View
          accessibilityElementsHidden
          importantForAccessibility="no"
          style={styles.intentPlaceholder}
          testID="chapter-introduction-intent-placeholder"
        />
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: chapterSpacing.horizontalPadding,
    paddingVertical: chapterSpacing.chapterIntroductionVertical,
    gap: chapterSpacing.introductionStackGap,
  },
  label: {
    ...typography.sectionLabel,
    color: color.textTertiary,
  },
  name: {
    ...typography.chapterIntroductionName,
    color: color.text,
  },
  intent: {
    ...typography.introduction,
    color: color.textSupporting,
  },
  namePlaceholder: {
    height: 24,
    backgroundColor: color.divider,
    alignSelf: 'stretch',
  },
  intentPlaceholder: {
    height: 14,
    width: '72%',
    backgroundColor: color.divider,
    alignSelf: 'flex-start',
  },
});
