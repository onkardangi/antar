import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import {
  ScreenHeader,
  color,
  typography,
  verseSpacing,
} from '../../../design-system';
import type { RootStackParamList } from '../../../navigation/types';
import { listChapterVerses } from '../../chapter/api/chapterDetailClient';
import type { VerseListItem } from '../../chapter/model/chapterTypes';
import { getVerse } from '../api/verseClient';
import { VerseNavigation } from '../components/VerseNavigation';
import { VerseReadingBody } from '../components/VerseReadingBody';
import type { VerseDetail } from '../model/verseTypes';

type VerseState =
  | { kind: 'loading' }
  | { kind: 'success'; verse: VerseDetail }
  | { kind: 'error' };

type NeighborsState =
  | { kind: 'idle' }
  | { kind: 'ready'; previous: VerseListItem | null; next: VerseListItem | null };

type Props = NativeStackScreenProps<RootStackParamList, 'VerseReader'> & {
  loadVerse?: (verseId: string) => Promise<VerseDetail>;
  loadChapterVerses?: (chapterId: string) => Promise<VerseListItem[]>;
};

export function VerseScreen({
  navigation,
  route,
  loadVerse = getVerse,
  loadChapterVerses = listChapterVerses,
}: Props) {
  const { verseId, chapterNumber, verseNumber } = route.params;
  const insets = useSafeAreaInsets();
  const [verseState, setVerseState] = useState<VerseState>({ kind: 'loading' });
  const [neighbors, setNeighbors] = useState<NeighborsState>({ kind: 'idle' });

  const refreshVerse = useCallback(async () => {
    setVerseState({ kind: 'loading' });
    setNeighbors({ kind: 'idle' });
    try {
      const verse = await loadVerse(verseId);
      setVerseState({ kind: 'success', verse });

      try {
        const verses = await loadChapterVerses(verse.chapterId);
        const index = verses.findIndex((item) => item.id === verse.id);
        if (index < 0) {
          setNeighbors({ kind: 'ready', previous: null, next: null });
          return;
        }
        setNeighbors({
          kind: 'ready',
          previous: index > 0 ? verses[index - 1]! : null,
          next: index < verses.length - 1 ? verses[index + 1]! : null,
        });
      } catch {
        // Detail succeeded; neighbor failure only disables Previous/Next.
        setNeighbors({ kind: 'ready', previous: null, next: null });
      }
    } catch {
      setVerseState({ kind: 'error' });
      setNeighbors({ kind: 'idle' });
    }
  }, [loadChapterVerses, loadVerse, verseId]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- intentional mount/param fetch
    void refreshVerse();
  }, [refreshVerse]);

  const goToNeighbor = useCallback(
    (neighbor: VerseListItem) => {
      navigation.setParams({
        verseId: neighbor.id,
        verseNumber: neighbor.verseNumber,
        chapterNumber,
      });
    },
    [chapterNumber, navigation],
  );

  const scrollContentStyle = useMemo(
    () => [
      styles.scrollContent,
      { paddingBottom: verseSpacing.bottomPadding + insets.bottom },
    ],
    [insets.bottom],
  );

  const previousEnabled = neighbors.kind === 'ready' && neighbors.previous != null;
  const nextEnabled = neighbors.kind === 'ready' && neighbors.next != null;

  return (
    <View
      style={styles.container}
      testID={
        verseState.kind === 'loading'
          ? 'verse-loading'
          : verseState.kind === 'error'
            ? 'verse-error'
            : 'verse-success'
      }
      accessibilityLabel={`Chapter ${chapterNumber}, Verse ${verseNumber}`}
    >
      <ScreenHeader
        layout="inline"
        paddingBottom={verseSpacing.headerBottom}
        onBack={navigation.canGoBack() ? () => navigation.goBack() : undefined}
      />

      {verseState.kind === 'loading' ? (
        <View style={styles.centered} testID="verse-loading-indicator">
          <ActivityIndicator
            accessibilityLabel="Loading verse"
            color={color.textSecondary}
          />
        </View>
      ) : null}

      {verseState.kind === 'error' ? (
        <View style={styles.errorBlock} testID="verse-error-message">
          <Text style={styles.errorText}>Unable to load this verse.</Text>
          <Text style={styles.errorText}>Please try again.</Text>
          <Pressable
            accessibilityRole="button"
            accessibilityLabel="Retry loading verse"
            hitSlop={8}
            onPress={() => void refreshVerse()}
            style={({ pressed }) => [
              styles.retryTarget,
              pressed ? styles.retryPressed : null,
            ]}
            testID="verse-retry"
          >
            <Text style={styles.retryLabel}>Try again</Text>
          </Pressable>
        </View>
      ) : null}

      {verseState.kind === 'success' ? (
        <ScrollView
          style={styles.scroll}
          contentContainerStyle={scrollContentStyle}
          testID="verse-scroll"
        >
          <VerseReadingBody
            chapterNumber={verseState.verse.chapterNumber}
            verseNumber={verseState.verse.verseNumber}
            canonicalReference={verseState.verse.canonicalReference}
            sanskritText={verseState.verse.sanskritText}
          />
          <View style={styles.navWrap}>
            <VerseNavigation
              previousEnabled={previousEnabled}
              nextEnabled={nextEnabled}
              onPrevious={() => {
                if (neighbors.kind === 'ready' && neighbors.previous) {
                  goToNeighbor(neighbors.previous);
                }
              }}
              onNext={() => {
                if (neighbors.kind === 'ready' && neighbors.next) {
                  goToNeighbor(neighbors.next);
                }
              }}
            />
          </View>
        </ScrollView>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: color.background,
  },
  scroll: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
  },
  centered: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  errorBlock: {
    paddingHorizontal: verseSpacing.horizontalPadding,
    paddingTop: verseSpacing.contentTop,
    gap: 8,
  },
  errorText: {
    ...typography.introduction,
    color: color.textSecondary,
  },
  retryTarget: {
    marginTop: 12,
    minHeight: verseSpacing.minTouchTarget,
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
  navWrap: {
    marginTop: verseSpacing.bodyToNavGap,
  },
});
