/**
 * Typography roles from Library.md and CHAPTER.md.
 *
 * Custom faces resolve after AppFonts loads Lora and Source Sans 3.
 * When those faces are unavailable (load failure), React Native Text falls
 * back to the platform system typeface for the same roles — safe and non-blocking.
 */
export const fontFamily = {
  lora: 'Lora_400Regular',
  loraItalic: 'Lora_400Regular_Italic',
  sourceSans: 'SourceSans3_400Regular',
  sourceSansMedium: 'SourceSans3_500Medium',
} as const;

export const typography = {
  applicationTitle: {
    fontFamily: fontFamily.lora,
    fontSize: 18,
    fontWeight: '400' as const,
    lineHeight: 24,
  },
  backNavigation: {
    fontFamily: fontFamily.sourceSans,
    fontSize: 13,
    fontWeight: '400' as const,
    lineHeight: 18,
  },
  scriptureTitle: {
    fontFamily: fontFamily.lora,
    fontSize: 24,
    fontWeight: '400' as const,
    lineHeight: 32,
  },
  introduction: {
    fontFamily: fontFamily.sourceSans,
    fontSize: 14,
    fontWeight: '400' as const,
    lineHeight: 22,
  },
  chapterNumber: {
    fontFamily: fontFamily.loraItalic,
    fontSize: 13,
    fontWeight: '400' as const,
    fontStyle: 'italic' as const,
    lineHeight: 18,
    letterSpacing: 0.78, // 0.06em at 13px
  },
  chapterName: {
    fontFamily: fontFamily.lora,
    fontSize: 15,
    fontWeight: '400' as const,
    lineHeight: 22,
  },
  verseCount: {
    fontFamily: fontFamily.sourceSans,
    fontSize: 11,
    fontWeight: '400' as const,
    lineHeight: 16,
    letterSpacing: 0.66, // 0.06em at 11px
  },
  /** CHAPTER.md section label (e.g. CHAPTER 2). */
  sectionLabel: {
    fontFamily: fontFamily.sourceSansMedium,
    fontSize: 11,
    fontWeight: '500' as const,
    lineHeight: 16,
    letterSpacing: 0.88, // ~0.08em at 11px
    textTransform: 'uppercase' as const,
  },
  /** CHAPTER.md canonical chapter name in ChapterIntroduction. */
  chapterIntroductionName: {
    fontFamily: fontFamily.lora,
    fontSize: 24,
    fontWeight: '400' as const,
    lineHeight: 32,
  },
  /** CHAPTER.md verse number in VerseRow. */
  verseNumber: {
    fontFamily: fontFamily.loraItalic,
    fontSize: 13,
    fontWeight: '400' as const,
    fontStyle: 'italic' as const,
    lineHeight: 18,
    letterSpacing: 0.78, // 0.06em at 13px
  },
  /** CHAPTER.md verse preview in VerseRow (future translation preview). */
  versePreview: {
    fontFamily: fontFamily.sourceSans,
    fontSize: 14,
    fontWeight: '400' as const,
    lineHeight: 22,
  },
  /**
   * Temporary Chapter-slice preview when API returns
   * "Verse preview unavailable" — quieter than real preview copy.
   */
  versePreviewTemporary: {
    fontFamily: fontFamily.sourceSans,
    fontSize: 14,
    fontWeight: '400' as const,
    fontStyle: 'italic' as const,
    lineHeight: 22,
  },
  /** Legacy roles retained for foundation screens. */
  title: {
    fontFamily: fontFamily.lora,
    fontSize: 22,
    fontWeight: '400' as const,
    lineHeight: 28,
  },
  body: {
    fontFamily: fontFamily.sourceSans,
    fontSize: 16,
    fontWeight: '400' as const,
    lineHeight: 22,
  },
  caption: {
    fontFamily: fontFamily.sourceSans,
    fontSize: 13,
    fontWeight: '400' as const,
    lineHeight: 18,
  },
} as const;
