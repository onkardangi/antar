import { Pressable, StyleSheet, Text, View } from 'react-native';

import { color, homeSpacing, typography } from '../../../design-system';
import type { HomeInvitationViewState } from '../model/todaysInvitation';
import {
  beginReadingAccessibilityLabel,
  continueReadingAccessibilityLabel,
  formatInvitationDestination,
} from '../model/todaysInvitation';

type Props = {
  state: HomeInvitationViewState;
  onContinueReading: (destination: {
    verseId: string;
    verseNumber: number;
    chapterNumber: number;
  }) => void;
  onBeginReading: (destination: {
    verseId: string;
    verseNumber: number;
    chapterNumber: number;
  }) => void;
  onRetryProgress?: () => void;
};

function SectionHeading() {
  return (
    <Text
      accessibilityRole="header"
      style={styles.sectionHeading}
      testID="home-invitation-heading"
    >
      Today’s Invitation
    </Text>
  );
}

function VersePreviewPlaceholder() {
  return (
    <View
      style={styles.previewSlot}
      testID="home-invitation-preview-placeholder"
      accessible={false}
      importantForAccessibility="no-hide-descendants"
    >
      <View style={[styles.previewLine, styles.previewLineLong]} />
      <View style={[styles.previewLine, styles.previewLineShort]} />
      <View style={[styles.previewLine, styles.previewLineMid]} />
    </View>
  );
}

/**
 * Today's Invitation — Home's sole primary action composition.
 *
 * Visual order (Figma-aligned):
 * section heading → destination → preview placeholder → action
 *
 * Hierarchy spacing uses marginTop tokens only (no container gap compounding).
 * Compact unavailable stacks use invitationStackGap alone.
 */
export function TodaysInvitation({
  state,
  onContinueReading,
  onBeginReading,
  onRetryProgress,
}: Props) {
  if (state.kind === 'loading') {
    return (
      <View style={styles.slot} testID="home-invitation-loading">
        <SectionHeading />
        <View
          accessible={false}
          importantForAccessibility="no-hide-descendants"
          style={styles.destinationSkeleton}
        />
        <VersePreviewPlaceholder />
        <View
          accessible={false}
          importantForAccessibility="no-hide-descendants"
          style={styles.actionSkeleton}
        />
      </View>
    );
  }

  if (state.kind === 'progress_unavailable') {
    return (
      <View style={styles.compactSlot} testID="home-invitation-unavailable">
        <SectionHeading />
        <Text style={styles.quietText}>
          Unable to restore your reading right now.
        </Text>
        {typeof onRetryProgress === 'function' ? (
          <Pressable
            accessibilityRole="button"
            accessibilityLabel="Try restoring reading again"
            hitSlop={8}
            onPress={onRetryProgress}
            style={({ pressed }) => [
              styles.retryTarget,
              pressed ? styles.pressed : null,
            ]}
            testID="home-invitation-retry"
          >
            <Text style={styles.retryLabel}>Try again</Text>
          </Pressable>
        ) : null}
      </View>
    );
  }

  if (state.kind === 'continue_reading') {
    const { chapterNumber, verseNumber } = state.destination;
    const destinationLabel = formatInvitationDestination(
      chapterNumber,
      verseNumber,
    );
    return (
      <View style={styles.slot} testID="home-invitation-continue-block">
        <SectionHeading />
        <Text style={styles.destinationLabel}>{destinationLabel}</Text>
        <VersePreviewPlaceholder />
        <Pressable
          accessibilityRole="button"
          accessibilityLabel={continueReadingAccessibilityLabel(
            chapterNumber,
            verseNumber,
          )}
          hitSlop={8}
          onPress={() => onContinueReading(state.destination)}
          style={({ pressed }) => [
            styles.actionTarget,
            pressed ? styles.pressed : null,
          ]}
          testID="home-invitation-continue"
        >
          <Text style={styles.actionLabel}>Continue Reading →</Text>
        </Pressable>
      </View>
    );
  }

  if (state.resolution === 'unavailable') {
    return (
      <View style={styles.slot} testID="home-invitation-begin-unavailable">
        <SectionHeading />
        <Text style={styles.destinationLabel}>Chapter 1 · Verse 1</Text>
        <VersePreviewPlaceholder />
        <View style={styles.unavailableCopy}>
          <Text style={styles.quietText}>
            Chapter 1 · Verse 1 is unavailable right now.
          </Text>
          <Text style={styles.quietText}>
            Browse the Gita when you’re ready.
          </Text>
        </View>
      </View>
    );
  }

  const { chapterNumber, verseNumber } = state.destination;
  const destinationLabel = formatInvitationDestination(
    chapterNumber,
    verseNumber,
  );
  return (
    <View style={styles.slot} testID="home-invitation-begin-block">
      <SectionHeading />
      <Text style={styles.destinationLabel}>{destinationLabel}</Text>
      <VersePreviewPlaceholder />
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={beginReadingAccessibilityLabel(
          chapterNumber,
          verseNumber,
        )}
        hitSlop={8}
        onPress={() => onBeginReading(state.destination)}
        style={({ pressed }) => [
          styles.actionTarget,
          pressed ? styles.pressed : null,
        ]}
        testID="home-invitation-begin"
      >
        <Text style={styles.actionLabel}>Begin Reading →</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  /** Productive / loading hierarchy — spacing via marginTop tokens only. */
  slot: {
    paddingHorizontal: homeSpacing.horizontalPadding,
  },
  /** Compact progress-unavailable stack — invitationStackGap only. */
  compactSlot: {
    paddingHorizontal: homeSpacing.horizontalPadding,
    gap: homeSpacing.invitationStackGap,
  },
  sectionHeading: {
    ...typography.sectionLabel,
    color: color.textSecondary,
  },
  destinationLabel: {
    ...typography.homeInvitationDestination,
    color: color.text,
    marginTop: homeSpacing.sectionToDestinationGap,
  },
  previewSlot: {
    marginTop: homeSpacing.destinationToPreviewGap,
    gap: homeSpacing.skeletonLineGap,
  },
  previewLine: {
    height: homeSpacing.skeletonLineHeight,
    backgroundColor: color.divider,
    alignSelf: 'flex-start',
    borderRadius: 0,
  },
  /** Organic prose rhythm: medium-long → shorter → medium. */
  previewLineLong: {
    width: '82%',
  },
  previewLineShort: {
    width: '48%',
  },
  previewLineMid: {
    width: '68%',
  },
  actionTarget: {
    marginTop: homeSpacing.previewToActionGap,
    minHeight: homeSpacing.minTouchTarget,
    justifyContent: 'center',
    alignSelf: 'flex-start',
  },
  actionLabel: {
    ...typography.homeInvitationAction,
    color: color.textSupporting,
  },
  quietText: {
    ...typography.homeInvitationContext,
    color: color.textSecondary,
  },
  unavailableCopy: {
    marginTop: homeSpacing.invitationStackGap,
    gap: homeSpacing.invitationStackGap,
  },
  retryTarget: {
    minHeight: homeSpacing.minTouchTarget,
    justifyContent: 'center',
    alignSelf: 'flex-start',
  },
  retryLabel: {
    ...typography.homeInvitationContext,
    color: color.textSecondary,
    textDecorationLine: 'underline',
  },
  pressed: {
    opacity: 0.55,
  },
  destinationSkeleton: {
    marginTop: homeSpacing.sectionToDestinationGap,
    height: homeSpacing.skeletonLineHeight,
    width: '42%',
    backgroundColor: color.divider,
    alignSelf: 'flex-start',
  },
  actionSkeleton: {
    marginTop: homeSpacing.previewToActionGap,
    height: homeSpacing.skeletonLineHeight,
    width: '48%',
    backgroundColor: color.divider,
    alignSelf: 'flex-start',
  },
});
