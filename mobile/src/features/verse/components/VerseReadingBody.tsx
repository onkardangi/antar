import { StyleSheet, Text, View } from 'react-native';

import { color, typography, verseSpacing } from '../../../design-system';

type Props = {
  chapterNumber: number;
  verseNumber: number;
  canonicalReference: string;
  sanskritText: string;
};

/**
 * Calm Sanskrit reading body for the Verse Reader.
 * No cards, icons, translation, or commentary.
 */
export function VerseReadingBody({
  chapterNumber,
  verseNumber,
  canonicalReference,
  sanskritText,
}: Props) {
  return (
    <View style={styles.container} testID="verse-reading-body">
      <Text
        accessibilityRole="header"
        style={styles.chapterLabel}
        testID="verse-chapter-label"
      >
        Chapter {chapterNumber}
      </Text>
      <Text style={styles.verseLabel} testID="verse-number-label">
        Verse {verseNumber}
      </Text>
      <Text style={styles.reference} testID="verse-canonical-reference">
        {canonicalReference}
      </Text>
      <Text style={styles.sanskrit} testID="verse-sanskrit-text">
        {sanskritText}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: verseSpacing.horizontalPadding,
    paddingTop: verseSpacing.contentTop,
    gap: verseSpacing.metaStackGap,
  },
  chapterLabel: {
    ...typography.sectionLabel,
    color: color.textSecondary,
  },
  verseLabel: {
    ...typography.chapterIntroductionName,
    color: color.text,
  },
  reference: {
    ...typography.caption,
    color: color.textTertiary,
    marginBottom: verseSpacing.metaToBodyGap - verseSpacing.metaStackGap,
  },
  sanskrit: {
    ...typography.sanskritBody,
    color: color.text,
  },
});
