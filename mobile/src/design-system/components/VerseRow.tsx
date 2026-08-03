import { Pressable, StyleSheet, Text } from 'react-native';

import { color } from '../tokens/color';
import { chapterSpacing } from '../tokens/spacing';
import { typography } from '../tokens/typography';

/** Literal temporary Chapter-slice preview from the Scripture API. */
export const TEMPORARY_VERSE_PREVIEW_TEXT = 'Verse preview unavailable';

export type VerseRowProps = {
  chapterNumber: number;
  verseNumber: number;
  previewText: string;
  onPress: () => void;
  testID?: string;
};

export function formatVerseNumber(verseNumber: number): string {
  return String(verseNumber).padStart(2, '0');
}

export function verseRowAccessibilityLabel(
  chapterNumber: number,
  verseNumber: number,
): string {
  return `Chapter ${chapterNumber}, Verse ${verseNumber}`;
}

export function VerseRow({
  chapterNumber,
  verseNumber,
  previewText,
  onPress,
  testID,
}: VerseRowProps) {
  const isTemporaryPreview = previewText === TEMPORARY_VERSE_PREVIEW_TEXT;

  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={verseRowAccessibilityLabel(chapterNumber, verseNumber)}
      onPress={onPress}
      style={({ pressed }) => [styles.row, pressed ? styles.pressed : null]}
      testID={testID ?? `verse-row-${verseNumber}`}
    >
      <Text style={styles.number} testID="verse-row-number">
        {formatVerseNumber(verseNumber)}
      </Text>
      <Text
        style={[styles.preview, isTemporaryPreview ? styles.previewTemporary : null]}
        testID="verse-row-preview"
      >
        {previewText}
      </Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: chapterSpacing.horizontalPadding,
    paddingVertical: chapterSpacing.verseRowVertical,
    minHeight: chapterSpacing.minTouchTarget,
    gap: chapterSpacing.verseNumberToPreviewGap,
  },
  pressed: {
    opacity: 0.55,
  },
  number: {
    ...typography.verseNumber,
    color: color.textTertiary,
    width: 28,
  },
  preview: {
    ...typography.versePreview,
    color: color.textSupporting,
    flex: 1,
  },
  previewTemporary: {
    ...typography.versePreviewTemporary,
    color: color.textTertiary,
  },
});
