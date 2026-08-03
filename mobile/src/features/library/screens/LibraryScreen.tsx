import { useCallback, useEffect, useMemo, useState } from 'react';
import { FlatList, Pressable, StyleSheet, Text, View } from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import {
  ChapterRow,
  HairlineRule,
  ScreenHeader,
  ScriptureIntroduction,
  color,
  librarySpacing,
  typography,
} from '../../../design-system';
import type { RootStackParamList } from '../../../navigation/types';
import { listChapters } from '../api/chapterClient';
import type { Chapter } from '../model/chapterTypes';

type LoadState =
  | { kind: 'loading' }
  | { kind: 'success'; chapters: Chapter[] }
  | { kind: 'error' };

type Props = NativeStackScreenProps<RootStackParamList, 'Library'> & {
  loadChapters?: () => Promise<Chapter[]>;
};

const PLACEHOLDER_COUNT = 9;

function ChapterListSeparator() {
  return <HairlineRule testID="chapter-row-divider" />;
}

export function LibraryScreen({ navigation, loadChapters = listChapters }: Props) {
  const insets = useSafeAreaInsets();
  const [state, setState] = useState<LoadState>({ kind: 'loading' });

  const refresh = useCallback(async () => {
    setState({ kind: 'loading' });
    try {
      // Backend contract returns canonical order; client sort is defensive only.
      const chapters = [...(await loadChapters())].sort(
        (left, right) => left.chapterNumber - right.chapterNumber,
      );
      if (chapters.length === 0) {
        // Canonical chapters must exist; treat empty as an invalid content error.
        setState({ kind: 'error' });
        return;
      }
      setState({ kind: 'success', chapters });
    } catch {
      setState({ kind: 'error' });
    }
  }, [loadChapters]);

  useEffect(() => {
    // Load the canonical Chapter list when Library opens.
    // eslint-disable-next-line react-hooks/set-state-in-effect -- intentional mount-time fetch
    void refresh();
  }, [refresh]);

  const listHeader = useMemo(
    () => (
      <View>
        <ScriptureIntroduction />
        <HairlineRule />
      </View>
    ),
    [],
  );

  const placeholderData = useMemo(
    () => Array.from({ length: PLACEHOLDER_COUNT }, (_, index) => index),
    [],
  );

  const listContentStyle = useMemo(
    () => [
      styles.listContent,
      { paddingBottom: librarySpacing.bottomPadding + insets.bottom },
    ],
    [insets.bottom],
  );

  const errorContentStyle = useMemo(
    () => [
      styles.errorContent,
      { paddingBottom: librarySpacing.bottomPadding + insets.bottom },
    ],
    [insets.bottom],
  );

  return (
    <View
      style={styles.container}
      testID={
        state.kind === 'loading'
          ? 'library-loading'
          : state.kind === 'error'
            ? 'library-error'
            : 'library-success'
      }
    >
      <ScreenHeader
        onBack={navigation.canGoBack() ? () => navigation.goBack() : undefined}
      />
      <HairlineRule />

      {state.kind === 'loading' ? (
        <FlatList
          style={styles.list}
          data={placeholderData}
          keyExtractor={(item) => `placeholder-${item}`}
          ListHeaderComponent={listHeader}
          ItemSeparatorComponent={ChapterListSeparator}
          contentContainerStyle={listContentStyle}
          renderItem={() => (
            <View style={styles.placeholderRow} testID="chapter-placeholder-row">
              <View style={styles.placeholderLine} />
            </View>
          )}
          scrollEnabled={false}
        />
      ) : null}

      {state.kind === 'error' ? (
        <View style={errorContentStyle} testID="library-error-content">
          {listHeader}
          <View style={styles.errorBlock} testID="library-error-message">
            <Text style={styles.errorText}>Unable to load chapters.</Text>
            <Text style={styles.errorText}>Please try again.</Text>
            <Pressable
              accessibilityRole="button"
              accessibilityLabel="Retry loading chapters"
              hitSlop={8}
              onPress={() => void refresh()}
              style={({ pressed }) => [
                styles.retryTarget,
                pressed ? styles.retryPressed : null,
              ]}
              testID="library-retry"
            >
              <Text style={styles.retryLabel}>Try again</Text>
            </Pressable>
          </View>
        </View>
      ) : null}

      {state.kind === 'success' ? (
        <FlatList
          style={styles.list}
          data={state.chapters}
          keyExtractor={(item) => item.id}
          ListHeaderComponent={listHeader}
          ItemSeparatorComponent={ChapterListSeparator}
          contentContainerStyle={listContentStyle}
          initialNumToRender={18}
          scrollEnabled
          testID="library-chapter-list"
          renderItem={({ item }) => (
            <ChapterRow
              chapterNumber={item.chapterNumber}
              canonicalName={item.canonicalName}
              verseCount={item.verseCount}
              onPress={() =>
                navigation.navigate('Chapter', {
                  chapterId: item.id,
                  chapterNumber: item.chapterNumber,
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
    paddingHorizontal: librarySpacing.horizontalPadding,
    paddingVertical: librarySpacing.chapterRowVertical,
    minHeight: librarySpacing.minTouchTarget,
    justifyContent: 'center',
  },
  placeholderLine: {
    height: 12,
    backgroundColor: color.divider,
    alignSelf: 'stretch',
  },
  errorBlock: {
    paddingHorizontal: librarySpacing.horizontalPadding,
    paddingTop: librarySpacing.chapterRowVertical,
    gap: 8,
  },
  errorText: {
    ...typography.introduction,
    color: color.textSecondary,
  },
  retryTarget: {
    marginTop: 12,
    minHeight: librarySpacing.minTouchTarget,
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
