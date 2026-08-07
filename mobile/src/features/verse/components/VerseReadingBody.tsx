import { StyleSheet, Text, View } from 'react-native';

import { color, typography, verseSpacing } from '../../../design-system';
import { VerseReference } from './VerseReference';

type Props = {
  chapterNumber: number;
  verseNumber: number;
  sanskritText: string;
};

/**
 * Calm Sanskrit reading body for the Verse Reader.
 * Quiet reference → Sanskrit. Translation is composed separately.
 */
export function VerseReadingBody({
  chapterNumber,
  verseNumber,
  sanskritText,
}: Props) {
  return (
    <View style={styles.container} testID="verse-reading-body">
      <VerseReference
        chapterNumber={chapterNumber}
        verseNumber={verseNumber}
      />
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
    gap: verseSpacing.referenceToBodyGap,
  },
  sanskrit: {
    ...typography.sanskritBody,
    color: color.text,
  },
});
