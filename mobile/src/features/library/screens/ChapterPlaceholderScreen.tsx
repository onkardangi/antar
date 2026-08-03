import { StyleSheet, Text, View } from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';

import {
  ScreenHeader,
  color,
  librarySpacing,
  typography,
} from '../../../design-system';
import type { RootStackParamList } from '../../../navigation/types';

type Props = NativeStackScreenProps<RootStackParamList, 'ChapterPlaceholder'>;

export function ChapterPlaceholderScreen({ navigation, route }: Props) {
  const { chapterNumber } = route.params;

  return (
    <View
      style={styles.container}
      testID="chapter-placeholder"
      accessibilityLabel={`Chapter ${chapterNumber}`}
    >
      <ScreenHeader
        onBack={navigation.canGoBack() ? () => navigation.goBack() : undefined}
      />
      <View style={styles.body}>
        <Text style={styles.number}>Chapter {chapterNumber}</Text>
        <Text style={styles.caption}>
          Verse reading will arrive in a later increment.
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
    paddingHorizontal: librarySpacing.horizontalPadding,
    paddingTop: librarySpacing.scriptureIntroductionVertical,
    gap: 12,
  },
  number: {
    ...typography.scriptureTitle,
    color: color.text,
  },
  caption: {
    ...typography.introduction,
    color: color.textSecondary,
  },
});
