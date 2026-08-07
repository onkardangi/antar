import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
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
import type { ReadingProgressService } from '../../reading-progress/application/ReadingProgressService';
import { useReadingProgressService } from '../../reading-progress/composition/ReadingProgressProvider';
import { listChapterVerses } from '../../chapter/api/chapterDetailClient';
import type { VerseListItem } from '../../chapter/model/chapterTypes';
import { getVerseTranslation } from '../api/translationClient';
import { getVerse } from '../api/verseClient';
import {
  TranslationBlock,
  type TranslationBlockState,
} from '../components/TranslationBlock';
import { VerseNavigation } from '../components/VerseNavigation';
import { VerseReadingBody } from '../components/VerseReadingBody';
import type { VerseTranslation } from '../model/translationTypes';
import type { VerseDetail } from '../model/verseTypes';

type VerseState =
  | { kind: 'loading' }
  | { kind: 'success'; verse: VerseDetail }
  | { kind: 'error' };

type TranslationState =
  | { kind: 'idle' }
  | { kind: 'loading' }
  | { kind: 'ready'; translation: VerseTranslation }
  | { kind: 'unavailable' };

type NeighborsState =
  | { kind: 'idle' }
  | { kind: 'ready'; previous: VerseListItem | null; next: VerseListItem | null };

type Props = NativeStackScreenProps<RootStackParamList, 'VerseReader'> & {
  loadVerse?: (verseId: string) => Promise<VerseDetail>;
  loadTranslation?: (verseId: string) => Promise<VerseTranslation>;
  loadChapterVerses?: (chapterId: string) => Promise<VerseListItem[]>;
  /**
   * Test override. Production always receives the real service from
   * ReadingProgressProvider — this prop is never required at runtime.
   */
  readingProgressService?: ReadingProgressService;
};

function hasRealSanskrit(verse: VerseDetail): boolean {
  return (
    typeof verse.sanskritText === 'string' && verse.sanskritText.trim().length > 0
  );
}

function toTranslationBlockState(
  state: TranslationState,
): TranslationBlockState | null {
  if (state.kind === 'loading') {
    return { kind: 'loading' };
  }
  if (state.kind === 'ready') {
    return { kind: 'ready', translation: state.translation };
  }
  // idle + unavailable: omit Translation section entirely (silent collapse).
  return null;
}

export function VerseScreen({
  navigation,
  route,
  loadVerse = getVerse,
  loadTranslation = getVerseTranslation,
  loadChapterVerses = listChapterVerses,
  readingProgressService: readingProgressOverride,
}: Props) {
  const { verseId, chapterNumber } = route.params;
  const insets = useSafeAreaInsets();
  const contextReadingProgress = useReadingProgressService();
  const readingProgressService =
    readingProgressOverride ?? contextReadingProgress;

  const [verseState, setVerseState] = useState<VerseState>({ kind: 'loading' });
  const [translationState, setTranslationState] = useState<TranslationState>({
    kind: 'idle',
  });
  const [neighbors, setNeighbors] = useState<NeighborsState>({ kind: 'idle' });
  const [retryToken, setRetryToken] = useState(0);
  const loadGenerationRef = useRef(0);

  useEffect(() => {
    const generation = ++loadGenerationRef.current;
    // eslint-disable-next-line react-hooks/set-state-in-effect -- intentional mount/param fetch
    setVerseState({ kind: 'loading' });
    setTranslationState({ kind: 'idle' });
    setNeighbors({ kind: 'idle' });

    let cancelled = false;

    void (async () => {
      try {
        const verse = await loadVerse(verseId);
        if (cancelled || generation !== loadGenerationRef.current) {
          return;
        }

        if (!hasRealSanskrit(verse)) {
          setVerseState({ kind: 'error' });
          setTranslationState({ kind: 'idle' });
          setNeighbors({ kind: 'idle' });
          return;
        }

        setVerseState({ kind: 'success', verse });
        void readingProgressService
          .recordVerseOpened({
            verseId: verse.id,
            chapterId: verse.chapterId,
            chapterNumber: verse.chapterNumber,
            verseNumber: verse.verseNumber,
            canonicalReference: verse.canonicalReference,
          })
          .catch(() => {
            // Persistence must never block Scripture rendering.
          });

        setTranslationState({ kind: 'loading' });
        void (async () => {
          try {
            const translation = await loadTranslation(verse.id);
            if (cancelled || generation !== loadGenerationRef.current) {
              return;
            }
            setTranslationState({ kind: 'ready', translation });
          } catch {
            if (cancelled || generation !== loadGenerationRef.current) {
              return;
            }
            setTranslationState({ kind: 'unavailable' });
          }
        })();

        try {
          const verses = await loadChapterVerses(verse.chapterId);
          if (cancelled || generation !== loadGenerationRef.current) {
            return;
          }
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
          if (cancelled || generation !== loadGenerationRef.current) {
            return;
          }
          setNeighbors({ kind: 'ready', previous: null, next: null });
        }
      } catch {
        if (cancelled || generation !== loadGenerationRef.current) {
          return;
        }
        setVerseState({ kind: 'error' });
        setTranslationState({ kind: 'idle' });
        setNeighbors({ kind: 'idle' });
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [
    loadChapterVerses,
    loadTranslation,
    loadVerse,
    readingProgressService,
    retryToken,
    verseId,
  ]);

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
  const translationBlockState = toTranslationBlockState(translationState);

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
            onPress={() => setRetryToken((token) => token + 1)}
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
            sanskritText={verseState.verse.sanskritText}
          />
          {translationBlockState != null ? (
            <TranslationBlock state={translationBlockState} />
          ) : null}
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
