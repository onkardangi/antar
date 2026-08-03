export const color = {
  background: '#F7F4EF',
  surface: '#FFFFFF',
  text: '#1F1A14',
  textMuted: '#6B635A',
  border: '#D9D1C7',
  success: '#2F6B4F',
  danger: '#8A3B2E',
  accent: '#4A5D4E',
} as const;

export type ColorToken = keyof typeof color;
