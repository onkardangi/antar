import { Pressable, StyleSheet, Text, View } from 'react-native';

import { color } from '../tokens/color';
import { librarySpacing } from '../tokens/spacing';
import { typography } from '../tokens/typography';

export type ChapterRowProps = {
  chapterNumber: number;
  canonicalName: string;
  verseCount: number;
  onPress: () => void;
  testID?: string;
};

export function formatChapterNumber(chapterNumber: number): string {
  return String(chapterNumber).padStart(2, '0');
}

export function chapterRowAccessibilityLabel(
  chapterNumber: number,
  canonicalName: string,
  verseCount: number,
): string {
  return `Chapter ${chapterNumber}, ${canonicalName}, ${verseCount} verses`;
}

export function ChapterRow({
  chapterNumber,
  canonicalName,
  verseCount,
  onPress,
  testID,
}: ChapterRowProps) {
  const paddedNumber = formatChapterNumber(chapterNumber);

  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={chapterRowAccessibilityLabel(
        chapterNumber,
        canonicalName,
        verseCount,
      )}
      onPress={onPress}
      style={({ pressed }) => [styles.row, pressed ? styles.pressed : null]}
      testID={testID ?? `chapter-row-${chapterNumber}`}
    >
      <Text style={styles.number}>{paddedNumber}</Text>
      <View style={styles.content}>
        <Text style={styles.name}>{canonicalName}</Text>
        <Text style={styles.verseCount}>{verseCount} verses</Text>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: librarySpacing.horizontalPadding,
    paddingVertical: librarySpacing.chapterRowVertical,
    minHeight: librarySpacing.minTouchTarget,
    gap: librarySpacing.numberToContentGap,
  },
  pressed: {
    opacity: 0.55,
  },
  number: {
    ...typography.chapterNumber,
    color: color.textSecondary,
    width: 28,
  },
  content: {
    flex: 1,
    gap: librarySpacing.titleToVerseCountGap,
  },
  name: {
    ...typography.chapterName,
    color: color.text,
  },
  verseCount: {
    ...typography.verseCount,
    color: color.textSecondary,
  },
});
