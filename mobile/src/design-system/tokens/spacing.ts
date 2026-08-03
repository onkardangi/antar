/**
 * Exact Library spacing after physical-device review
 * (design/07_ENGINEERING_HANDOFF/Library.md).
 */
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
} as const;

export const librarySpacing = {
  horizontalPadding: 28,
  /** Content padding below safe-area inset, before the title / Back. */
  headerContentTop: 8,
  /** Padding from application title to the header divider. */
  headerBottom: 16,
  /** Gap between Back and application title when Back is present. */
  headerBackToTitleGap: 4,
  scriptureIntroductionVertical: 30,
  chapterRowVertical: 20,
  numberToContentGap: 20,
  titleToVerseCountGap: 3,
  bottomPadding: 64,
  minTouchTarget: 44,
} as const;

export type SpacingToken = keyof typeof spacing;
