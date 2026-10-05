import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { C, textOn } from './tokens.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const b64 = f => fs.readFileSync(path.join(here, '..', 'assets', f)).toString('base64');
export const LOGO = 'data:image/svg+xml;base64,' + b64('shikshaq-logo.svg');
const FONT_CSS = `
@font-face{font-family:'Geist';src:url(data:font/woff2;base64,${b64('fonts/geist-latin.woff2')}) format('woff2');font-weight:100 900}
@font-face{font-family:'Archivo';src:url(data:font/woff2;base64,${b64('fonts/archivo-latin.woff2')}) format('woff2');font-weight:100 900;font-stretch:62% 125%}`;

export const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export function page(W, H, inner, bg = C.page) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>${FONT_CSS}
*{box-sizing:border-box;margin:0;padding:0}
body{width:${W}px;height:${H}px;overflow:hidden;background:${bg};font-family:Geist,system-ui,sans-serif;color:${C.ink};-webkit-font-smoothing:antialiased}
.p{position:relative;width:${W}px;height:${H}px;overflow:hidden}
.a{position:absolute}
h1,h2,h3{letter-spacing:-0.055em;text-wrap:balance;line-height:.95}
.lab{font-size:22px;font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.d{font-family:Archivo,Geist,sans-serif;font-stretch:112%;font-weight:900;letter-spacing:-.04em}
</style></head><body><div class="p" data-root>${inner}</div><script>
document.fonts.ready.then(function(){(function(){document.querySelectorAll('[data-grow]').forEach(function(e){var s=parseFloat(getComputedStyle(e).fontSize),cap=parseFloat(e.dataset.grow);while(s<cap){e.style.fontSize=(s+4)+'px';if(e.scrollWidth>e.clientWidth+1||e.scrollHeight>e.clientHeight+1){e.style.fontSize=s+'px';break;}s+=4;}});document.querySelectorAll('[data-settle]').forEach(function(e){var r=document.createRange();r.selectNodeContents(e);var th=r.getBoundingClientRect().height,d=e.clientHeight-th;if(d>40){e.style.top=(e.offsetTop+d-6)+'px';e.style.height=(e.clientHeight-d+6)+'px';}});document.querySelectorAll('[data-fit]').forEach(function(e){var s=parseFloat(getComputedStyle(e).fontSize),min=parseFloat(e.dataset.fit)||12;while(s>min&&(e.scrollWidth>e.clientWidth+1||e.scrollHeight>e.clientHeight+1)){s-=2;e.style.fontSize=s+'px';}});})();});
</script></body></html>`;
}

// Absolutely positioned box. tag is read by the DOM gate.
export function box(tag, x, y, w, h, style, inner = '') {
  return `<div class="a" data-tag="${tag}" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;${style}">${inner}</div>`;
}
// Rounded slab/card. Radii come from the site scale: 32 slab, 28, 20 card.
export function card(tag, x, y, w, h, fill, { r = 32, ring = false, shadow = '', pad = 0, inner = '', extra = '' } = {}) {
  const ringCss = ring ? `box-shadow:0 0 0 2px ${C.hairline}${shadow ? ',' + shadow : ''};` : (shadow ? `box-shadow:${shadow};` : '');
  return box(tag, x, y, w, h, `background:${fill};border-radius:${r}px;padding:${pad}px;overflow:hidden;${ringCss}${extra}`, inner);
}
export const glow = c => `0 18px 40px ${c}47`; // matches the site's 0 14px 34px rgba(...,.28)

export function chip(text, fill, { size = 24, color } = {}) {
  return `<span style="display:inline-block;background:${fill};color:${color || textOn(fill)};font-size:${size}px;font-weight:700;padding:${Math.round(size * .32)}px ${Math.round(size * .8)}px;border-radius:999px;letter-spacing:-.01em;white-space:nowrap">${esc(text)}</span>`;
}
// Tilted overhanging sticker (VISUAL_LANGUAGE 1.5). Alternating rotations.
export function sticker(tag, x, y, text, fill, rot = 5, size = 26) {
  return `<div class="a" data-tag="${tag}" style="left:${x}px;top:${y}px;transform:rotate(${rot}deg);z-index:9">${chip(text, fill, { size })}</div>`;
}
export function logoBar(x, y, h = 66) {
  return `<img class="a" data-tag="logo" src="${LOGO}" style="left:${x}px;top:${y}px;height:${h}px;width:auto;z-index:20">`;
}
export function handle(x, y, color = C.secondary, text = 'shikshaq.in') {
  return `<div class="a lab" data-tag="handle" style="left:${x}px;top:${y}px;color:${color};z-index:20;font-size:24px">${esc(text)}</div>`;
}

// ---- mascots: original blob characters in the site palette -------------------
// Same idea as the reference's friendly blobs: a saturated body, a simple face.
const face = (mood, ink = C.ink) => ({
  happy: `<circle cx="40" cy="48" r="5" fill="${ink}"/><circle cx="60" cy="48" r="5" fill="${ink}"/><path d="M40 60 Q50 70 60 60" stroke="${ink}" stroke-width="4" fill="none" stroke-linecap="round"/>`,
  wink: `<path d="M35 49 L45 47" stroke="${ink}" stroke-width="4" stroke-linecap="round"/><circle cx="60" cy="48" r="5" fill="${ink}"/><path d="M40 60 Q50 70 60 60" stroke="${ink}" stroke-width="4" fill="none" stroke-linecap="round"/>`,
  cheer: `<path d="M34 50 Q40 43 46 50" stroke="${ink}" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M54 50 Q60 43 66 50" stroke="${ink}" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M38 58 Q50 74 62 58 Z" fill="${ink}"/>`,
  none: '',
  calm: `<circle cx="40" cy="50" r="4.5" fill="${ink}"/><circle cx="60" cy="50" r="4.5" fill="${ink}"/><circle cx="50" cy="61" r="3" fill="${ink}"/>`,
}[mood]);
const BODY = {
  squircle: 'M50 6 C66 4 80 8 90 22 C98 34 96 66 88 80 C78 94 62 96 50 94 C36 96 20 92 12 80 C4 66 2 34 10 22 C20 8 34 4 50 6Z',
  flower: 'M50 4 C60 4 62 22 76 24 C90 26 96 36 94 50 C96 64 90 74 76 76 C62 78 60 96 50 96 C40 96 38 78 24 76 C10 74 4 64 6 50 C4 36 10 26 24 24 C38 22 40 4 50 4Z',
  burst: (() => { let p = ''; for (let i = 0; i < 24; i++) { const a = i / 24 * Math.PI * 2, r = i % 2 ? 40 : 49; p += (i ? 'L' : 'M') + (50 + r * Math.cos(a)).toFixed(1) + ' ' + (50 + r * Math.sin(a)).toFixed(1); } return p + 'Z'; })(),
  cloud: 'M26 78 C10 78 4 60 16 52 C12 36 28 26 40 32 C46 18 70 18 76 34 C92 32 98 52 86 60 C94 74 80 82 68 78 C58 86 40 86 26 78Z',
};
export function mascot(tag, kind, x, y, size, fill, mood = 'happy', rot = 0) {
  return `<svg class="a" data-tag="${tag}" viewBox="0 0 100 100" style="left:${x}px;top:${y}px;width:${size}px;height:${size}px;transform:rotate(${rot}deg);overflow:visible"><path d="${BODY[kind]}" fill="${fill}"/>${face(mood)}</svg>`;
}
// The reference's "big eyes peeking" move, as a dome with two eyes.
export function peeker(tag, x, y, w, fill) {
  const h = Math.round(w * .62);
  return `<svg class="a" data-tag="${tag}" viewBox="0 0 200 124" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px"><path d="M0 124 C0 56 44 0 100 0 C156 0 200 56 200 124Z" fill="${fill}"/>
  <ellipse cx="68" cy="78" rx="30" ry="34" fill="#fff"/><ellipse cx="132" cy="78" rx="30" ry="34" fill="#fff"/>
  <ellipse cx="74" cy="82" rx="17" ry="22" fill="${C.ink}"/><ellipse cx="138" cy="82" rx="17" ry="22" fill="${C.ink}"/>
  <circle cx="68" cy="72" r="6" fill="#fff"/><circle cx="132" cy="72" r="6" fill="#fff"/></svg>`;
}

// ---- shared chrome used by every template -----------------------------------
export function headline(x, y, w, plain, bold, size = 112, color = C.ink, h = null) {
  const hh = h || Math.round(size * 2 * 1.06);
  return `<h1 class="a" data-tag="headline" data-fit="56" data-grow="136" data-settle="1" style="left:${x}px;top:${y}px;width:${w}px;height:${hh}px;font-size:${size}px;font-weight:400;color:${color}">${esc(plain)} <span style="font-weight:800;letter-spacing:-.06em">${esc(bold)}</span></h1>`;
}
export function ctaBar(y, text, accent, { x = 48, w = 984, h = 150, variant = 'panel' } = {}) {
  const fg = textOn(accent);
  const v = { panel: { bg: C.panel, ring: '', txt: '#fff', dot: accent, arrow: fg },
              accent: { bg: accent, ring: '', txt: textOn(accent), dot: C.panel, arrow: '#fff' },
              ring: { bg: C.card, ring: `box-shadow:0 0 0 2px ${C.hairline};`, txt: C.ink, dot: accent, arrow: fg } }[variant] || null;
  return box('cta', x, y, w, h, `background:${v.bg};${v.ring}border-radius:32px;display:flex;align-items:center;justify-content:space-between;padding:0 44px;z-index:5`,
    `<div data-fit="30" style="color:${v.txt};font-size:50px;font-weight:700;letter-spacing:-.04em;line-height:1;max-width:760px;height:60px;display:flex;align-items:center">${esc(text)}</div>
     <div style="width:78px;height:78px;border-radius:999px;background:${v.dot};display:flex;align-items:center;justify-content:center;flex:none"><svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="${v.arrow}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>`);
}
// A style is a set of CHOICES inside the brand, never a way around it (see brain/BRAIN.md).
export const DEFAULT_STYLE = { id: 'calm-bone', ground: 'bone', cta: 'panel', radius: 32, flip: false, shuffle: false, stickerSign: 1,
  kit: { shapes: ['squircle', 'flower', 'burst', 'cloud'], moods: ['calm', 'happy', 'wink', 'cheer'], rot: [0, 6, -8, 6] } };
export function ground(S, accentName) {
  if (!S || S.ground === 'bone') return C.page;
  if (S.ground === 'muted') return C.muted;
  return frame(accentName).tint;
}
export function frame(accentName) {
  const a = accentName === 'indigo' ? C.indigo : accentName === 'mint' ? C.mintSolid : C.orange;
  const tint = accentName === 'indigo' ? C.indigoTint : accentName === 'mint' ? C.mint : C.orangeTint;
  const deep = accentName === 'indigo' ? C.indigoDeep : accentName === 'mint' ? '#24603D' : C.orangeDeep;
  return { a, tint, deep };
}
