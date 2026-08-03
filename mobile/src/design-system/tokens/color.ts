/**
 * Shared palette from Library and Chapter handoffs.
 *
 * Library quiet labels use textSecondary (#8A8A84). Chapter editorial
 * introduction body uses textSupporting (#4A4A46) from CHAPTER.md Secondary
 * Text. Future verse translation previews also use textSupporting; the
 * temporary API string "Verse preview unavailable" uses textTertiary so it
 * stays quieter than real Chapter content.
 *
 * textTertiary uses #8A8A84 instead of Library handoff #B4B4AE — #B4B4AE on
 * #F9F9F7 fails practical contrast for 11–13px text.
 */
export const color = {
  background: '#F9F9F7',
  text: '#1A1A18',
  textSecondary: '#8A8A84',
  /** Chapter Secondary Text (#4A4A46) — supporting body / future verse preview. */
  textSupporting: '#4A4A46',
  textTertiary: '#8A8A84',
  divider: '#D4D4CC',
  /** Foundation / error-boundary surfaces only — not used by Library. */
  surface: '#FFFFFF',
  accent: '#1A1A18',
  /** @deprecated Prefer textSecondary. Kept for foundation screens. */
  textMuted: '#8A8A84',
  /** @deprecated Prefer divider. Kept for foundation screens. */
  border: '#D4D4CC',
  success: '#2F6B4F',
  danger: '#8A3B2E',
} as const;

export type ColorToken = keyof typeof color;
