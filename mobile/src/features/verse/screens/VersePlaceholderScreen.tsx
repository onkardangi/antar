import { StyleSheet, Text, View } from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';

import {
  ScreenHeader,
  chapterSpacing,
  color,
  typography,
} from '../../../design-system';
import type { RootStackParamList } from '../../../navigation/types';

type Props = NativeStackScreenProps<RootStackParamList, 'VersePlaceholder'>;

/**
 * Temporary navigation target for Chapter → Verse until the Verse Reader slice.
 * Displays only enough information to verify navigation params.
 */
export function VersePlaceholderScreen({ navigation, route }: Props) {
  const { chapterNumber, verseNumber, verseId } = route.params;

  return (
    <View
      style={styles.container}
      testID="verse-placeholder"
      accessibilityLabel={`Chapter ${chapterNumber}, Verse ${verseNumber}`}
    >
      <ScreenHeader
        onBack={navigation.canGoBack() ? () => navigation.goBack() : undefined}
      />
      <View style={styles.body}>
        <Text style={styles.heading}>
          Chapter {chapterNumber} · Verse {verseNumber}
        </Text>
        <Text style={styles.caption}>Verse reading will arrive in a later increment.</Text>
        <Text style={styles.meta} testID="verse-placeholder-id">
          {verseId}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: color.background,
  },
  body: {
    paddingHorizontal: chapterSpacing.horizontalPadding,
    paddingTop: chapterSpacing.chapterIntroductionVertical,
    gap: 12,
  },
  heading: {
    ...typography.chapterIntroductionName,
    color: color.text,
  },
  caption: {
    ...typography.introduction,
    color: color.textSupporting,
  },
  meta: {
    ...typography.caption,
    color: color.textTertiary,
  },
});
