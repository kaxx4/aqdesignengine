// Shikshaq tokens for posters. Values mirror src/index.css and
// src/lib/subject-palette.ts. If the site changes, change them here too;
// selftest.mjs compares them against the live source files.
export const C = {
  page: '#F9F5F1', card: '#FCFAF7', muted: '#F0EAE2', hairline: '#E7DFD5',
  ink: '#1F1F1F', prose: '#4A443E', secondary: '#7B736B', panel: '#1B1A18',
  orange: '#FF8000', orangeDeep: '#B35900', orangeTint: '#FFF4E8',
  indigo: '#4351FF', indigoDeep: '#2E3AD6', indigoTint: '#EDEEFF',
  mint: '#E3F7EC', mintSolid: '#34B268', peach: '#FCECDE',
};
export const SIZES = { feed: [1080, 1350], story: [1080, 1920], square: [1080, 1080] };

function hslToHex(h, s, l) {
  s /= 100; l /= 100;
  const k = n => (n + h / 30) % 12, a = s * Math.min(l, 1 - l);
  const f = n => l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
  return '#' + [f(0), f(8), f(4)].map(x => Math.round(x * 255).toString(16).padStart(2, '0')).join('').toUpperCase();
}
// VISUAL_LANGUAGE.md section 3. tint 93% L, text 26% L, meta 34% L.
export const SUBJECT_SEEDS = {
  Maths: { h: 28, s: 85, l: 65, dark: false }, Science: { h: 145, s: 55, l: 45, dark: true },
  English: { h: 180, s: 45, l: 50, dark: false }, Commerce: { h: 220, s: 60, l: 55, dark: true },
  Computer: { h: 280, s: 50, l: 55, dark: true }, Hindi: { h: 0, s: 65, l: 55, dark: true },
  History: { h: 35, s: 55, l: 50, dark: false }, Geography: { h: 160, s: 50, l: 45, dark: true },
};
export function subjectPalette(name) {
  const seed = SUBJECT_SEEDS[name];
  if (!seed) return { tint: C.muted, solid: C.secondary, text: C.ink, meta: C.secondary, badgeText: '#FFFFFF' };
  const { h, s, l, dark } = seed;
  return { tint: hslToHex(h, s, 93), solid: hslToHex(h, s, l), text: hslToHex(h, 45, 26),
           meta: hslToHex(h, 28, 34), badgeText: dark ? '#FFFFFF' : C.ink };
}
// WCAG contrast, used by the validator to measure rather than assume.
export function lum(hex) {
  const v = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map(c => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2];
}
export function contrast(a, b) {
  const [x, y] = [lum(a), lum(b)].sort((m, n) => n - m);
  return (x + 0.05) / (y + 0.05);
}
// Ink on brand orange (white is 2.5:1 and the site already moved to ink).
export const textOn = fill => (contrast(fill, C.ink) >= contrast(fill, '#FFFFFF') ? C.ink : '#FFFFFF');
