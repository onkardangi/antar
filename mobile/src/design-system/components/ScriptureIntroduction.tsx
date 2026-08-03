import { StyleSheet, Text, View } from 'react-native';

import { color } from '../tokens/color';
import { librarySpacing } from '../tokens/spacing';
import { typography } from '../tokens/typography';

type Props = {
  title?: string;
  body?: string;
  testID?: string;
};

export function ScriptureIntroduction({
  title = 'Bhagavad Gita',
  body = 'All eighteen chapters are available in their canonical order.',
  testID = 'scripture-introduction',
}: Props) {
  return (
    <View style={styles.container} testID={testID}>
      <Text accessibilityRole="header" style={styles.title}>
        {title}
      </Text>
      <Text style={styles.body}>{body}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: librarySpacing.horizontalPadding,
    paddingVertical: librarySpacing.scriptureIntroductionVertical,
    gap: 12,
  },
  title: {
    ...typography.scriptureTitle,
    color: color.text,
  },
  body: {
    ...typography.introduction,
    color: color.textSecondary,
  },
});
