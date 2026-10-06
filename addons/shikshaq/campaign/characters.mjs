// Characters for the campaign. Same vocabulary as the site's blob family
// (src/components/ui/blob.tsx): a flat body, two dots, one mouth, no gradients, mood carries meaning.
// The five site moods keep their fixed colours. Two shapes are added in the same flat vocabulary:
// a burst (sun) and a four-lobe X, per the owner's reference. No names: they are shapes, not mascots.
import { C } from '../src/tokens.mjs';

export const MOOD_FILL = { rough: '#D14545', meh: '#EFA063', fine: '#9B4FC4', good: '#3FAFA8', great: '#FF8000' };
const INK = C.ink;
const MOUTH = {
  rough: 'M36 68 L64 68', meh: 'M36 68 L64 68',
  fine: 'M37 63 Q50 76 63 63', good: 'M34 61 Q50 79 66 61', great: 'M34 60 Q50 80 66 60',
};
const dots = (cy = 50, ink = INK, r = 5) => `<circle cx="38" cy="${cy}" r="${r}" fill="${ink}"/><circle cx="62" cy="${cy}" r="${r}" fill="${ink}"/>`;
const mouth = (d, ink = INK) => `<path d="${d}" stroke="${ink}" stroke-width="4.5" fill="none" stroke-linecap="round"/>`;

const svg = (tag, x, y, w, h, vb, inner, rot = 0) =>
  `<svg class="a" data-tag="${tag}" viewBox="${vb}" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;transform:rotate(${rot}deg);overflow:visible">${inner}</svg>`;

// The site blob: an ARCH, flat bottom, domed top. `great` is a circle (the one celebratory face).
export function arch(tag, x, y, w, mood = 'good', rot = 0, fill) {
  const f = fill || MOOD_FILL[mood];
  const body = mood === 'great'
    ? `<circle cx="50" cy="50" r="46" fill="${f}"/>`
    : `<path d="M6 100 L6 54 C6 24 26 4 50 4 C74 4 94 24 94 54 L94 100 Z" fill="${f}"/>`;
  const eyes = mood === 'rough' ? dots(54) : dots(mood === 'great' ? 44 : 52);
  return svg(tag, x, y, w, w, '0 0 100 100', body + eyes + mouth(MOUTH[mood]), rot);
}
// Burst: a spiky sun with squinting happy eyes (the reference's sun).
export function sun(tag, x, y, w, fill = '#FFC700', rot = 0) {
  let p = '';
  for (let i = 0; i < 28; i++) { const a = i / 28 * Math.PI * 2, r = i % 2 ? 41 : 49; p += (i ? 'L' : 'M') + (50 + r * Math.cos(a)).toFixed(1) + ' ' + (50 + r * Math.sin(a)).toFixed(1); }
  const face = `<path d="M30 44 L40 49 L30 54" stroke="${INK}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M70 44 L60 49 L70 54" stroke="${INK}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M38 62 Q50 72 62 62" stroke="${INK}" stroke-width="4" fill="none" stroke-linecap="round"/>`;
  return svg(tag, x, y, w, w, '0 0 100 100', `<path d="${p}Z" fill="${fill}"/>` + face, rot);
}
// Four-lobe X: soft diagonal lobes around a centre.
export function lobe(tag, x, y, w, fill = '#5B7BD9', rot = 0) {
  const l = a => `<ellipse cx="50" cy="50" rx="15" ry="46" fill="${fill}" transform="rotate(${a} 50 50)"/>`;
  return svg(tag, x, y, w, w, '0 0 100 100', l(45) + l(135) + `<circle cx="50" cy="50" r="22" fill="${fill}"/>` + dots(48) + mouth('M40 60 Q50 68 60 60'), rot);
}
// Peeking eyes on a dome, the reference's big eyes. White sclera, ink pupils with a notch.
export function eyes(tag, x, y, w, fill) {
  const h = Math.round(w * .62);
  return svg(tag, x, y, w, h, '0 0 200 124',
    `<path d="M0 124 C0 56 44 0 100 0 C156 0 200 56 200 124Z" fill="${fill}"/>
     <ellipse cx="68" cy="78" rx="30" ry="34" fill="#fff"/><ellipse cx="132" cy="78" rx="30" ry="34" fill="#fff"/>
     <ellipse cx="74" cy="82" rx="17" ry="22" fill="${INK}"/><ellipse cx="138" cy="82" rx="17" ry="22" fill="${INK}"/>
     <circle cx="68" cy="72" r="6" fill="#fff"/><circle cx="132" cy="72" r="6" fill="#fff"/>`);
}
// Scalloped edge strip: n bumps along the top of a w x h band (the reference's scalloped slab).
export function scallop(tag, x, y, w, h, fill, n = 8, flip = false) {
  const bw = w / n; let d = `M0 ${h} L0 ${h * .45}`;
  for (let i = 0; i < n; i++) d += ` Q${bw * (i + .5)} ${-h * .1} ${bw * (i + 1)} ${h * .45}`;
  d += ` L${w} ${h} Z`;
  return `<svg class="a" data-tag="${tag}" data-deco="1" viewBox="0 0 ${w} ${h}" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;${flip ? 'transform:scaleY(-1);' : ''}"><path d="${d}" fill="${fill}"/></svg>`;
}
// Torn edge: a jagged horizontal seam, seeded so a series stays consistent.
export function torn(tag, x, y, w, fill, seed = 1, h = 44, down = true) {
  let t = seed >>> 0; const r = () => { t += 0x6D2B79F5; let q = Math.imul(t ^ (t >>> 15), 1 | t); q ^= q + Math.imul(q ^ (q >>> 7), 61 | q); return ((q ^ (q >>> 14)) >>> 0) / 4294967296; };
  let d = `M0 0 L0 ${h * .5}`; const step = 26;
  for (let px = 0; px <= w; px += step) d += ` L${px} ${(h * .35 + r() * h * .6).toFixed(1)}`;
  d += ` L${w} 0 Z`;
  return `<svg class="a" data-tag="${tag}" data-deco="1" viewBox="0 0 ${w} ${h}" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;${down ? '' : 'transform:scaleY(-1);'}"><path d="${d}" fill="${fill}"/></svg>`;
}
// A rounded burst badge for stickers ("Free", etc).
export function badge(tag, x, y, w, fill, text, color = INK, rot = 8) {
  let p = '';
  for (let i = 0; i < 20; i++) { const a = i / 20 * Math.PI * 2, r = i % 2 ? 41 : 49; p += (i ? 'L' : 'M') + (50 + r * Math.cos(a)).toFixed(1) + ' ' + (50 + r * Math.sin(a)).toFixed(1); }
  return `<div class="a" data-tag="${tag}" style="left:${x}px;top:${y}px;width:${w}px;height:${w}px;transform:rotate(${rot}deg;z-index:8">
  <svg viewBox="0 0 100 100" style="position:absolute;inset:0;width:100%;height:100%"><path d="${p}Z" fill="${fill}"/></svg>
  <div data-fit="14" data-bg="${fill}" style="position:absolute;left:14%;top:30%;width:72%;height:40%;display:flex;align-items:center;justify-content:center;text-align:center;font-family:Archivo,Geist,sans-serif;font-stretch:112%;font-weight:900;letter-spacing:-.03em;line-height:.95;font-size:${Math.round(w * (String(text).length > 10 ? .135 : .2))}px;color:${color}">${text}</div></div>`.replace('rotate(' + rot + 'deg;', 'rotate(' + rot + 'deg);');
}

// Inline (in-flow) arch for use inside flex rows: chat avatars, review ghosts.
export function archInline(w, mood = 'good', fill) {
  const f = fill || MOOD_FILL[mood];
  const body = mood === 'great' ? `<circle cx="50" cy="50" r="46" fill="${f}"/>` : `<path d="M6 100 L6 54 C6 24 26 4 50 4 C74 4 94 24 94 54 L94 100 Z" fill="${f}"/>`;
  const e = mood === 'rough' ? dots(54) : dots(mood === 'great' ? 44 : 52);
  return `<svg data-deco="1" viewBox="0 0 100 100" style="width:${w}px;height:${w}px;flex:none;display:block">${body}${e}${mouth(MOUTH[mood])}</svg>`;
}
// Put a z-index on an absolutely positioned svg returned by the helpers above.
export const lift = (html, z = 3) => html.replace('style="', `style="z-index:${z};`);
