// Kit v3: what the live site actually uses, read off its own screenshots and components (not invented).
//  - circle mascots with tall eyes (EyesPanel) and the white smiling face (onboarding), plus the site's arch blobs
//  - stroke icons in the site's icon-tile treatment (a tilted rounded square with a thick dark outline)
//  - the dotted card ground, the highlighted-pill phrase, the numbered heading, the pill chip
import { C } from '../src/tokens.mjs';
import { arch, sun, lobe, MOOD_FILL } from './characters.mjs';

export const INK = C.ink, BONE = C.page, CARD = C.card, MUTED = C.muted, HAIR = C.hairline, PANEL = C.panel;
export const LEMON = '#FFC700';
export const ORANGE = C.orange, ORANGE_DEEP = C.orangeDeep, ORANGE_TINT = C.orangeTint;
export const INDIGO = C.indigo, INDIGO_DEEP = C.indigoDeep, INDIGO_TINT = C.indigoTint;
export const MINT = C.mint, MINT_SOLID = C.mintSolid, MINT_DEEP = '#24603D', PEACH = C.peach;
export const ACC = {
  orange: { a: ORANGE, deep: ORANGE_DEEP, tint: ORANGE_TINT, onA: INK },
  indigo: { a: INDIGO, deep: INDIGO_DEEP, tint: INDIGO_TINT, onA: '#FFFFFF' },
  mint: { a: MINT_SOLID, deep: MINT_DEEP, tint: MINT, onA: INK },
};

// 24-unit stroke icons (lucide-style paths, the family the site uses)
export const ICONS = {
  search: '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
  users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
  chat: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
  shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
  book: '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
  pin: '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
  file: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/>',
  cap: '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
  heart: '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
  clock: '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
  star: '<path d="m12 2 3 7 7 .6-5.3 4.7 1.6 7.2L12 17.8l-6.3 3.7 1.6-7.2L2 9.6 9 9z"/>',
  check: '<path d="M20 6 9 17l-5-5"/>',
  arrow: '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
  cal: '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
  phone: '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>',
  home: '<path d="m3 11 9-8 9 8"/><path d="M5 10v10h14V10"/>',
  edit: '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
  gift: '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v9H5v-9M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
};
export const icon = (name, size, stroke = INK, sw = 2.2) => {
  const dim = typeof size === 'string' ? `style="width:${size};height:${size};flex:none;display:block"` : `width="${size}" height="${size}" style="flex:none;display:block"`;
  return `<svg ${dim} viewBox="0 0 24 24" fill="none" stroke="${stroke}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${ICONS[name] || ICONS.star}</svg>`;
};

// The site's icon tile: a rounded square, tilted, ringed in near-black (empty states) or a flat solid tile (benefit rows).
export function iconTile(name, size, { fill, stroke, ring = false, rot = 0, radius = .3 } = {}, U = n => `${n}px`) {
  const rs = ring ? `box-shadow:0 0 0 ${U(Math.max(4, Math.round(size * .045)))} ${BONE},0 0 0 ${U(Math.max(8, Math.round(size * .09)))} ${INK};` : '';
  return `<div style="width:${U(size)};height:${U(size)};border-radius:${U(Math.round(size * radius))};background:${fill};display:flex;align-items:center;justify-content:center;flex:none;transform:rotate(${rot}deg);${rs}">${icon(name, U(Math.round(size * .5)), stroke || INK)}</div>`;
}

// ---- circle mascots (the site's own): tall-eyed, smiling, sleeping ------------------------------------------------------------
const svg = (cls, tag, style, vb, inner) => `<svg class="${cls}" data-tag="${tag}" viewBox="${vb}" style="${style};overflow:visible">${inner}</svg>`;
export function capSvg(x, y, s, fill = INK) {
  return `<g transform="translate(${x} ${y}) scale(${s / 24})"><path d="M2 9 12 4l10 5-10 5z" fill="${fill}"/><path d="M6 12v4c3 2.6 9 2.6 12 0v-4" fill="${fill}"/></g>`;
}
// orange circle, two tall dark eyes in lighter sockets, a mortarboard at the lower right
export function faceEyes(style, fill = ORANGE, { cap = true, tag = 'mas' } = {}) {
  const socket = fill === ORANGE ? '#E07000' : 'rgba(31,31,31,.18)';
  return svg('a', tag, style, '0 0 100 100',
    `<circle cx="50" cy="50" r="48" fill="${fill}"/>
     <ellipse cx="36" cy="46" rx="9.5" ry="15" fill="${socket}"/><ellipse cx="64" cy="46" rx="9.5" ry="15" fill="${socket}"/>
     <ellipse cx="36" cy="47" rx="4.6" ry="8.4" fill="${INK}"/><ellipse cx="64" cy="47" rx="4.6" ry="8.4" fill="${INK}"/>
     <circle cx="34.6" cy="43" r="1.8" fill="#fff"/><circle cx="62.6" cy="43" r="1.8" fill="#fff"/>${cap ? capSvg(66, 70, 20) : ''}`);
}
// white circle, shining eyes, a wide smile (the onboarding face)
export function faceSmile(style, fill = CARD, { tag = 'mas' } = {}) {
  return svg('a', tag, style, '0 0 100 100',
    `<circle cx="50" cy="50" r="48" fill="${fill}"/>
     <ellipse cx="37" cy="42" rx="8.5" ry="11" fill="rgba(31,31,31,.07)"/><ellipse cx="63" cy="42" rx="8.5" ry="11" fill="rgba(31,31,31,.07)"/>
     <circle cx="37" cy="43" r="5.6" fill="${INK}"/><circle cx="63" cy="43" r="5.6" fill="${INK}"/>
     <circle cx="35.2" cy="40.6" r="1.9" fill="#fff"/><circle cx="61.2" cy="40.6" r="1.9" fill="#fff"/>
     <path d="M29 59 Q50 83 71 59 Q50 66 29 59Z" fill="${INK}" stroke="${INK}" stroke-width="3" stroke-linejoin="round"/>`);
}
// indigo circle asleep with a trail of z
export function faceSleep(style, fill = INDIGO, { tag = 'mas' } = {}) {
  return svg('a', tag, style, '0 0 100 100',
    `<circle cx="50" cy="50" r="48" fill="${fill}"/>
     <path d="M26 50 Q36 58 46 50" stroke="${INK}" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M54 50 Q64 58 74 50" stroke="${INK}" stroke-width="4" fill="none" stroke-linecap="round"/>
     <path d="M82 18h9l-9 10h9M92 4h6l-6 7h6" stroke="${INK}" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`);
}
// the whole family behind one name; `m` is {kind, mood, fill}; `style` carries position and (possibly calc()) size
export function mascot(m, style, tag = 'mas') {
  const k = m.kind;
  if (k === 'eyes') return faceEyes(style, m.fill || ORANGE, { tag });
  if (k === 'smile') return faceSmile(style, m.fill || CARD, { tag });
  if (k === 'sleep') return faceSleep(style, m.fill || INDIGO, { tag });
  const html = k === 'sun' ? sun(tag, 0, 0, 100, m.fill || LEMON, m.rot ?? 8) : k === 'lobe' ? lobe(tag, 0, 0, 100, m.fill || '#5B7BD9', m.rot ?? -8) : arch(tag, 0, 0, 100, m.mood || 'good', m.rot ?? 6, m.fill);
  const rot = (html.match(/rotate\(([-\d.]+)deg\)/) || [])[1] || 0;
  return html.replace(/style="[^"]*"/, `style="${style};transform:rotate(${rot}deg);overflow:visible"`);
}
export { arch, sun, lobe, MOOD_FILL };
