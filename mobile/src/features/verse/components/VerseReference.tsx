import { StyleSheet, Text } from 'react-native';

import { color, typography } from '../../../design-system';

type Props = {
  chapterNumber: number;
  verseNumber: number;
};

/**
 * Static Standard Verse Reference for the Verse Reader.
 * Quiet orientation only — one combined announcement, no interaction.
 */
export function VerseReference({ chapterNumber, verseNumber }: Props) {
  return (
    <Text
      style={styles.reference}
      testID="verse-reference"
      accessibilityLabel={`Chapter ${chapterNumber}, Verse ${verseNumber}`}
    >
      {`Chapter ${chapterNumber} · Verse ${verseNumber}`}
    </Text>
  );
}

const styles = StyleSheet.create({
  reference: {
    ...typography.verseCount,
    color: color.textSecondary,
  },
});
