import { useCallback, useContext, useEffect, useState } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import {
  HairlineRule,
  ScreenHeader,
  color,
  homeSpacing,
} from '../../../design-system';
import type { RootStackParamList } from '../../../navigation/types';
import { BrowseBhagavadGita } from '../components/BrowseBhagavadGita';
import { TodaysInvitation } from '../components/TodaysInvitation';
import {
  HomeInvitationContext,
  type LoadTodaysInvitationFn,
} from '../composition/HomeInvitationProvider';
import type {
  HomeInvitationViewState,
  InvitationVerseDestination,
  TodaysInvitationState,
} from '../model/todaysInvitation';

type Props = NativeStackScreenProps<RootStackParamList, 'Home'> & {
  /**
   * Test override. Production uses HomeInvitationProvider.
   */
  loadTodaysInvitation?: LoadTodaysInvitationFn;
};

export function HomeScreen({
  navigation,
  loadTodaysInvitation: loadOverride,
}: Props) {
  const insets = useSafeAreaInsets();
  const contextLoad = useContext(HomeInvitationContext);
  const loadTodaysInvitation = loadOverride ?? contextLoad;

  if (loadTodaysInvitation == null) {
    throw new Error(
      'HomeScreen requires HomeInvitationProvider or loadTodaysInvitation',
    );
  }

  const [invitation, setInvitation] = useState<HomeInvitationViewState>({
    kind: 'loading',
  });

  const refreshInvitation = useCallback(async () => {
    setInvitation({ kind: 'loading' });
    try {
      const next: TodaysInvitationState = await loadTodaysInvitation();
      setInvitation(next);
    } catch {
      setInvitation({ kind: 'progress_unavailable' });
    }
  }, [loadTodaysInvitation]);

  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', () => {
      void refreshInvitation();
    });
    return unsubscribe;
  }, [navigation, refreshInvitation]);

  const openVerse = useCallback(
    (destination: InvitationVerseDestination) => {
      navigation.navigate('VerseReader', {
        verseId: destination.verseId,
        verseNumber: destination.verseNumber,
        chapterNumber: destination.chapterNumber,
      });
    },
    [navigation],
  );

  return (
    <View style={styles.container} testID="home-screen">
      <ScreenHeader />
      <HairlineRule />

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={[
          styles.content,
          { paddingBottom: homeSpacing.bottomPadding + insets.bottom },
        ]}
        testID="home-scroll"
      >
        <View style={styles.invitationBlock} testID="home-invitation-slot">
          <TodaysInvitation
            state={invitation}
            onContinueReading={openVerse}
            onBeginReading={openVerse}
            onRetryProgress={() => void refreshInvitation()}
          />
        </View>

        <View style={styles.browseSection}>
          <HairlineRule testID="home-browse-divider" />
          <View style={styles.browseBlock}>
            <BrowseBhagavadGita
              onPress={() => navigation.navigate('Library')}
            />
          </View>
        </View>
      </ScrollView>
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
  content: {
    flexGrow: 1,
  },
  invitationBlock: {
    paddingTop: homeSpacing.contentTop,
  },
  browseSection: {
    marginTop: homeSpacing.invitationToBrowseGap,
  },
  browseBlock: {
    paddingTop: homeSpacing.browseTop,
  },
});
