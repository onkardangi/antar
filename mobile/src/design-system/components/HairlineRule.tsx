import { StyleSheet, View } from 'react-native';

import { color } from '../tokens/color';

type Props = {
  testID?: string;
};

export function HairlineRule({ testID = 'hairline-rule' }: Props) {
  return <View accessibilityElementsHidden importantForAccessibility="no" style={styles.rule} testID={testID} />;
}

const styles = StyleSheet.create({
  rule: {
    height: StyleSheet.hairlineWidth,
    backgroundColor: color.divider,
    alignSelf: 'stretch',
  },
});
