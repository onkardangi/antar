/**
 * Typography roles from design/07_ENGINEERING_HANDOFF/Library.md.
 *
 * Custom faces resolve after AppFonts loads Lora and Source Sans 3.
 * When those faces are unavailable (load failure), React Native Text falls
 * back to the platform system typeface for the same roles — safe and non-blocking.
 */
export const fontFamily = {
  lora: 'Lora_400Regular',
  loraItalic: 'Lora_400Regular_Italic',
  sourceSans: 'SourceSans3_400Regular',
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
