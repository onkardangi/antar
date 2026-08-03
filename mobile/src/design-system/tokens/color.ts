/**
 * Library handoff palette (design/07_ENGINEERING_HANDOFF/Library.md).
 *
 * textTertiary uses the approved secondary value (#8A8A84) instead of
 * handoff #B4B4AE — #B4B4AE on #F9F9F7 fails practical contrast for
 * 11–13px text. Deviation reported in the Library UI implementation.
 */
export const color = {
  background: '#F9F9F7',
  text: '#1A1A18',
  textSecondary: '#8A8A84',
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
