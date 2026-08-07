/**
 * Exact Library spacing after physical-device review
 * (design/07_ENGINEERING_HANDOFF/Library.md).
 *
 * Chapter spacing follows design/07_ENGINEERING_HANDOFF/CHAPTER.md and is kept
 * separate so Library’s reviewed values are not silently overwritten.
 *
 * Shared ScreenHeader metrics (horizontal padding, content top, Back→title gap,
 * min touch target) live in `screenHeaderSpacing` so Library and Chapter do not
 * diverge accidentally. Feature-specific header bottom padding stays on each
 * feature token and is passed into ScreenHeader via `paddingBottom`.
 */
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
} as const;

/** Shared ScreenHeader layout metrics used by Library and Chapter. */
export const screenHeaderSpacing = {
  horizontalPadding: 28,
  /** Content padding below safe-area inset, before the title / Back. */
  headerContentTop: 8,
  /** Gap between Back and application title when Back is present. */
  headerBackToTitleGap: 4,
  minTouchTarget: 44,
} as const;

export const librarySpacing = {
  ...screenHeaderSpacing,
  /** Padding from application title to the header divider. */
  headerBottom: 16,
  scriptureIntroductionVertical: 30,
  chapterRowVertical: 20,
  numberToContentGap: 20,
  titleToVerseCountGap: 3,
  bottomPadding: 64,
} as const;

export const chapterSpacing = {
  ...screenHeaderSpacing,
  /**
   * Padding below the inline header row to the divider.
   * Physical-device review (2026-08-03): 28 → 20 with inline Back + title.
   */
  headerBottom: 20,
  /**
   * Vertical padding for ChapterIntroduction.
   * Physical-device review (2026-08-03): 44 → 34.
   */
  chapterIntroductionVertical: 34,
  /** Gap between section label, name, and shortIntent. */
  introductionStackGap: 12,
  /**
   * Vertical padding for VerseRow (each side).
   * Physical-device review (2026-08-03): 22 → 18 (−8px total).
   */
  verseRowVertical: 18,
  /**
   * Gap between verse number and preview columns.
   * Physical-device review (2026-08-03): 20 → 12.
   */
  verseNumberToPreviewGap: 12,
  bottomPadding: 64,
} as const;

/** Verse Reader spacing — reuses shared header metrics; reading-specific gaps only. */
export const verseSpacing = {
  ...screenHeaderSpacing,
  headerBottom: 20,
  /** Top padding before the quiet Verse Reference (Back → reference). */
  contentTop: 12,
  /** Small/medium pause between Reference and Sanskrit. */
  referenceToBodyGap: 16,
  /** Generous section pause between Sanskrit and Translation. */
  bodyToTranslationGap: 40,
  translationStackGap: 8,
  /** Generous section pause before Previous / Next. */
  bodyToNavGap: 40,
  navGap: 24,
  bottomPadding: 64,
} as const;

export type SpacingToken = keyof typeof spacing;
