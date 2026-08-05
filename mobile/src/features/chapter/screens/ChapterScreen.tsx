import { useCallback, useEffect, useMemo, useState } from 'react';
import { FlatList, Pressable, StyleSheet, Text, View } from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import {
  ChapterIntroduction,
  HairlineRule,
  ScreenHeader,
  VerseRow,
  chapterSpacing,
  color,
  typography,
} from '../../../design-system';
import type { RootStackParamList } from '../../../navigation/types';
import { getChapter, listChapterVerses } from '../api/chapterDetailClient';
import type { ChapterDetail, VerseListItem } from '../model/chapterTypes';

type ChapterState =
  | { kind: 'loading' }
  | { kind: 'success'; chapter: ChapterDetail }
  | { kind: 'error' };

type VerseState =
  | { kind: 'loading' }
  | { kind: 'success'; verses: VerseListItem[] }
  | { kind: 'error' };

type Props = NativeStackScreenProps<RootStackParamList, 'Chapter'> & {
  loadChapter?: (chapterId: string) => Promise<ChapterDetail>;
  loadVerses?: (chapterId: string) => Promise<VerseListItem[]>;
};

const PLACEHOLDER_COUNT = 8;

function VerseListSeparator() {
  return <HairlineRule testID="verse-row-divider" />;
}

export function ChapterScreen({
  navigation,
  route,
  loadChapter = getChapter,
  loadVerses = listChapterVerses,
}: Props) {
  const { chapterId, chapterNumber } = route.params;
  const insets = useSafeAreaInsets();
  const [chapterState, setChapterState] = useState<ChapterState>({ kind: 'loading' });
  const [verseState, setVerseState] = useState<VerseState>({ kind: 'loading' });

  const refreshChapter = useCallback(async () => {
    setChapterState({ kind: 'loading' });
    try {
      const chapter = await loadChapter(chapterId);
      setChapterState({ kind: 'success', chapter });
    } catch {
      setChapterState({ kind: 'error' });
    }
  }, [chapterId, loadChapter]);

  const refreshVerses = useCallback(async () => {
    setVerseState({ kind: 'loading' });
    try {
      const verses = await loadVerses(chapterId);
      if (verses.length === 0) {
        // Canonical verses must exist; treat empty as an invalid content error.
        setVerseState({ kind: 'error' });
        return;
      }
      setVerseState({ kind: 'success', verses });
    } catch {
      setVerseState({ kind: 'error' });
    }
  }, [chapterId, loadVerses]);

  useEffect(() => {
    // Independent Chapter and Verse fetches — do not collapse into one boolean.
    // eslint-disable-next-line react-hooks/set-state-in-effect -- intentional mount-time fetch
    void refreshChapter();
    void refreshVerses();
  }, [refreshChapter, refreshVerses]);

  const listContentStyle = useMemo(
    () => [
      styles.listContent,
      { paddingBottom: chapterSpacing.bottomPadding + insets.bottom },
    ],
    [insets.bottom],
  );

  const errorContentStyle = useMemo(
    () => [
      styles.errorContent,
      { paddingBottom: chapterSpacing.bottomPadding + insets.bottom },
    ],
    [insets.bottom],
  );

  const placeholderData = useMemo(
    () => Array.from({ length: PLACEHOLDER_COUNT }, (_, index) => index),
    [],
  );

  const listHeader = useMemo(() => {
    const intro =
      chapterState.kind === 'success' ? (
        <ChapterIntroduction
          chapterNumber={chapterState.chapter.chapterNumber}
          canonicalName={chapterState.chapter.canonicalName}
          shortIntent={chapterState.chapter.shortIntent}
        />
      ) : (
        <ChapterIntroduction chapterNumber={chapterNumber} />
      );

    return (
      <View testID="chapter-list-header">
        <ScreenHeader
          layout="inline"
          paddingBottom={chapterSpacing.headerBottom}
          onBack={navigation.canGoBack() ? () => navigation.goBack() : undefined}
        />
        <HairlineRule />
        {intro}
        <HairlineRule />
      </View>
    );
  }, [chapterNumber, chapterState, navigation]);

  const showVersePlaceholders =
    chapterState.kind !== 'error' &&
    (chapterState.kind === 'loading' || verseState.kind === 'loading');

  const showVerseList =
    chapterState.kind === 'success' && verseState.kind === 'success';

  const showVerseError =
    chapterState.kind === 'success' && verseState.kind === 'error';

  const showChapterError = chapterState.kind === 'error';

  return (
    <View
      style={styles.container}
      testID={
        showChapterError
          ? 'chapter-error'
          : showVerseError
            ? 'chapter-verse-error'
            : showVerseList
              ? 'chapter-success'
              : 'chapter-loading'
      }
    >
      {showChapterError ? (
        <View style={errorContentStyle} testID="chapter-error-content">
          <ScreenHeader
            layout="inline"
            paddingBottom={chapterSpacing.headerBottom}
            onBack={navigation.canGoBack() ? () => navigation.goBack() : undefined}
          />
          <HairlineRule />
          <ChapterIntroduction
            chapterNumber={chapterNumber}
            showContentPlaceholders={false}
          />
          <HairlineRule />
          <View style={styles.errorBlock} testID="chapter-error-message">
            <Text style={styles.errorText}>Unable to load chapter.</Text>
            <Text style={styles.errorText}>Please try again.</Text>
            <Pressable
              accessibilityRole="button"
              accessibilityLabel="Retry loading chapter"
              hitSlop={8}
              onPress={() => {
                void refreshChapter();
                if (verseState.kind === 'error') {
                  void refreshVerses();
                }
              }}
              style={({ pressed }) => [
                styles.retryTarget,
                pressed ? styles.retryPressed : null,
              ]}
              testID="chapter-retry"
            >
              <Text style={styles.retryLabel}>Try again</Text>
            </Pressable>
          </View>
        </View>
      ) : null}

      {showVerseError ? (
        <View style={errorContentStyle} testID="chapter-verse-error-content">
          {listHeader}
          <View style={styles.errorBlock} testID="chapter-verse-error-message">
            <Text style={styles.errorText}>Unable to load verses.</Text>
            <Text style={styles.errorText}>Please try again.</Text>
            <Pressable
              accessibilityRole="button"
              accessibilityLabel="Retry loading verses"
              hitSlop={8}
              onPress={() => void refreshVerses()}
              style={({ pressed }) => [
                styles.retryTarget,
                pressed ? styles.retryPressed : null,
              ]}
              testID="chapter-verse-retry"
            >
              <Text style={styles.retryLabel}>Try again</Text>
            </Pressable>
          </View>
        </View>
      ) : null}

      {showVersePlaceholders ? (
        <FlatList
          style={styles.list}
          data={placeholderData}
          keyExtractor={(item) => `placeholder-${item}`}
          ListHeaderComponent={listHeader}
          ItemSeparatorComponent={VerseListSeparator}
          contentContainerStyle={listContentStyle}
          scrollEnabled={false}
          renderItem={() => (
            <View
              accessibilityElementsHidden
              importantForAccessibility="no"
              style={styles.placeholderRow}
              testID="verse-placeholder-row"
            >
              <View style={styles.placeholderLine} />
            </View>
          )}
        />
      ) : null}

      {showVerseList ? (
        <FlatList
          style={styles.list}
          data={verseState.verses}
          keyExtractor={(item) => item.id}
          ListHeaderComponent={listHeader}
          ItemSeparatorComponent={VerseListSeparator}
          contentContainerStyle={listContentStyle}
          initialNumToRender={24}
          scrollEnabled
          testID="chapter-verse-list"
          renderItem={({ item }) => (
            <VerseRow
              chapterNumber={chapterState.chapter.chapterNumber}
              verseNumber={item.verseNumber}
              previewText={item.previewText}
              onPress={() =>
                navigation.navigate('VerseReader', {
                  verseId: item.id,
                  verseNumber: item.verseNumber,
                  chapterNumber: chapterState.chapter.chapterNumber,
                })
              }
            />
          )}
        />
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: color.background,
  },
  list: {
    flex: 1,
  },
  listContent: {
    flexGrow: 1,
  },
  errorContent: {
    flexGrow: 1,
  },
  placeholderRow: {
    paddingHorizontal: chapterSpacing.horizontalPadding,
    paddingVertical: chapterSpacing.verseRowVertical,
    minHeight: chapterSpacing.minTouchTarget,
    justifyContent: 'center',
  },
  placeholderLine: {
    height: 12,
    backgroundColor: color.divider,
    alignSelf: 'stretch',
  },
  errorBlock: {
    paddingHorizontal: chapterSpacing.horizontalPadding,
    paddingTop: chapterSpacing.verseRowVertical,
    gap: 8,
  },
  errorText: {
    ...typography.introduction,
    color: color.textSecondary,
  },
  retryTarget: {
    marginTop: 12,
    minHeight: chapterSpacing.minTouchTarget,
    justifyContent: 'center',
    alignSelf: 'flex-start',
  },
  retryPressed: {
    opacity: 0.55,
  },
  retryLabel: {
    ...typography.introduction,
    color: color.textSecondary,
    textDecorationLine: 'underline',
  },
});
