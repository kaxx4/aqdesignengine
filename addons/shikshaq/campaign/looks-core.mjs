// Shared layout helpers and the first set of looks: plate, answer, eyes, mood, poll, cover, button, ui.
// A look is (spec, L) -> html. Spec fields are plain data from catalog.mjs, so a look never holds copy.
import { C, textOn, subjectPalette } from '../src/tokens.mjs';
import { box, card, chip, esc, LOGO, logoBar, handle, glow, frame } from '../src/kit.mjs';
import { arch, sun, lobe, eyes, scallop, badge, MOOD_FILL } from './characters.mjs';

// ---- canvas layout. Story chrome (IG header, reply bar) covers the top 250 and bottom 340 px. ------------------------
export function lay(canvas) {
  const W = 1080, H = canvas === 'S' ? 1920 : canvas === 'F' ? 1350 : canvas === 'C' ? 1920 : 1080;
  const story = canvas === 'S', pad = 56;
  const top = story ? 250 : 0, bot = story ? 340 : 0;
  const y0 = top + (story ? 26 : 52), y1 = H - bot - (story ? 26 : 52);
  return { W, H, canvas, story, pad, top, bot, y0, y1, cw: W - 2 * pad, safe: story ? { top: 250, bottom: 340 } : null };
}
export const GROUND = { bone: C.page, panel: C.panel, muted: C.muted };
export const groundOf = (spec, F) => spec.subject ? subjectPalette(spec.subject).tint : spec.ground === 'panel' ? C.panel : spec.ground === 'tint' ? F.tint : spec.ground === 'accent' ? F.a : spec.ground === 'muted' ? C.muted : C.page;
export const isDark = spec => spec.ground === 'panel';

// text box. Nest inside a card so the gate sees the right backing colour, or pass bg.
export function txt(tag, x, y, w, h, html, o = {}) {
  const { size = 40, weight = 500, color = C.ink, ls = '-.03em', lh = 1.1, align = 'left', fit = 14, grow = 0, extra = '', bg = '', cls = '' } = o;
  return `<div class="a ${cls}" data-tag="${tag}"${fit ? ` data-fit="${fit}"` : ''}${grow ? ` data-grow="${grow}"` : ''}${bg ? ` data-bg="${bg}"` : ''} style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;font-size:${size}px;font-weight:${weight};color:${color};letter-spacing:${ls};line-height:${lh};text-align:${align};${extra}">${html}</div>`;
}
const arrowSvg = (s, c) => `<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="${c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>`;

// logo (a bone pill on dark grounds, never white-inverted) + handle + optional page counter
export function chrome(spec, L, F, o = {}) {
  const dark = isDark(spec), lh = L.story ? 60 : 64, lw = Math.round(lh * 252 / 92), parts = [];
  if (o.logo !== false) {
    if (dark || spec.ground === 'accent') parts.push(box('logopill', L.pad - 14, L.y0 - 12, lw + 28, lh + 24, `background:${C.page};border-radius:999px;z-index:19;box-shadow:0 0 0 2px ${C.hairline}`));
    parts.push(logoBar(L.pad, L.y0, lh));
  }
  if (o.handle !== false) parts.push(`<div class="a lab" data-tag="handle" ${dark ? '' : ''} style="left:${L.pad}px;top:${L.y1 - 26}px;color:${dark ? '#CFC7BD' : (spec.ground === 'accent' ? textOn(F.a) : C.secondary)};z-index:20;font-size:24px" ${spec.ground === 'accent' ? `data-bg="${F.a}"` : ''}>shikshaq.in</div>`);
  if (spec.count) parts.push(`<div class="a lab" data-tag="count" style="left:${L.W - L.pad - 140}px;top:${L.y1 - 26}px;width:140px;text-align:right;color:${dark ? '#CFC7BD' : C.secondary};z-index:20;font-size:24px">${esc(spec.count)}</div>`);
  if (spec.tag) { // top-right label chip, e.g. "FAQ 01"
    parts.push(`<div class="a" data-tag="eyebrow" style="right:${L.pad}px;top:${L.y0 + 8}px;z-index:20">${chip(spec.tag, dark ? '#2A2926' : C.muted, { size: 24, color: dark ? '#fff' : C.ink })}</div>`);
  }
  return parts.join('');
}
export function ctaPill(L, y, text, fill, o = {}) {
  const { x = L.pad, w = L.cw, h = L.story ? 124 : 112, dot = C.panel, ink } = o, fg = ink || textOn(fill);
  return box('cta', x, y, w, h, `background:${fill};border-radius:999px;display:flex;align-items:center;justify-content:space-between;padding:0 ${Math.round(h * .3)}px 0 ${Math.round(h * .46)}px;z-index:5;${o.shadow ? `box-shadow:${o.shadow};` : ''}`,
    `<div data-fit="22" style="color:${fg};font-size:${Math.round(h * .42)}px;font-weight:700;letter-spacing:-.04em;line-height:1;width:${w - h - 70}px;height:${Math.round(h * .5)}px;display:flex;align-items:center;white-space:nowrap">${esc(text)}</div>
     <div style="width:${Math.round(h * .66)}px;height:${Math.round(h * .66)}px;border-radius:999px;background:${dot};display:flex;align-items:center;justify-content:center;flex:none">${arrowSvg(Math.round(h * .3), dot === C.panel || dot === C.ink ? '#fff' : C.ink)}</div>`);
}

// headline built from segments, so ONE word can ride a tilted tag and one a pill with an arrow.
// seg: 'plain' | {b} | {tag, fill} | {pill, fill}
function segHtml(seg, F, dark) {
  if (typeof seg === 'string') return `<span style="font-weight:400">${esc(seg)}</span>`;
  if (seg.b != null) return `<span style="font-weight:800;letter-spacing:-.06em">${esc(seg.b)}</span>`;
  if (seg.tag != null) {
    const fill = seg.fill || F.a;
    return `<span data-bg="${fill}" style="display:inline-block;background:${fill};color:${textOn(fill)};font-weight:800;letter-spacing:-.06em;padding:.02em .16em .08em;border-radius:.18em;transform:rotate(${seg.rot ?? (seg.tag.length > 6 ? -1.5 : -3)}deg);box-shadow:0 .06em 0 ${C.ink}">${esc(seg.tag)}</span>`;
  }
  if (seg.pill != null) {
    const fill = seg.fill || F.a;
    return `<span data-bg="${fill}" style="display:inline-flex;align-items:center;gap:.14em;background:${fill};color:${textOn(fill)};font-weight:800;letter-spacing:-.06em;padding:.0em .2em .06em .3em;border-radius:999px">${esc(seg.pill)}<span style="display:inline-flex;width:.62em;height:.62em;border-radius:999px;background:${C.ink};align-items:center;justify-content:center">${arrowSvg('.34em', '#fff')}</span></span>`;
  }
  return '';
}
export const hs = (cap, availH, n, lh = 1.1) => Math.max(40, Math.min(cap, Math.floor(availH / (n * lh))));
export function headBlock(tag, x, y, w, lines, F, size, dark, o = {}) {
  const color = dark ? '#FFFFFF' : C.ink;
  const rows = lines.map(l => `<div style="display:flex;align-items:center;gap:.2em;white-space:nowrap;margin-bottom:${l.some(g => typeof g === 'object' && (g.tag || g.pill || '').length > 6) ? '.14em' : '.06em'};justify-content:${o.align === 'center' ? 'center' : 'flex-start'}">${l.map(s => segHtml(s, F, dark)).join('')}</div>`).join('');
  const pos = o.flow ? `position:relative;width:${w}px;` : `position:absolute;left:${x}px;top:${y}px;width:${w}px;`;
  return `<h1 data-tag="${tag}" data-fit="${o.min || 52}" style="${pos}font-size:${size}px;color:${color};line-height:${o.lh || (lines.flat().some(g => typeof g === 'object' && (g.tag != null || g.pill != null)) ? 1.16 : 1.08)};letter-spacing:-.055em;font-family:Archivo,Geist,sans-serif;font-stretch:104%">${rows}</h1>`;
}

// ---- LOOK: plate (V6). A giant headline, one word on a tag, one in a pill, a mascot, a button. -----------------
export function plate(spec, L, F) {
  const dark = isDark(spec), S = L.story, Q = L.canvas === 'Q';
  const ctaH = S ? 124 : 112;
  const ctaY = L.y1 - ctaH - 44; // leaves room for the handle row
  const sup = spec.support ? `<div data-tag="support" data-fit="22" style="font-size:${S ? 46 : 38}px;font-weight:500;line-height:1.18;letter-spacing:-.03em;color:${dark ? '#E7DFD5' : C.prose};max-width:${L.cw}px;margin-top:${S ? 46 : 30}px">${esc(spec.support)}</div>` : '';
  const kick = spec.kicker ? `<div style="margin-bottom:${S ? 36 : 24}px">${chip(spec.kicker, spec.kickFill || F.tint, { size: S ? 30 : 26, color: spec.kickFill ? undefined : F.deep })}</div>` : '';
  const regionTop = L.y0 + (S ? 60 : 64) + 36, regionBot = (spec.cta ? ctaY : L.y1 - 60) - (spec.mascot ? (S ? 312 : (Q ? 0 : 236)) : 24);
  const supH = spec.support ? (S ? 190 : 140) : 0, kickH = spec.kicker ? (S ? 100 : 76) : 0;
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, hs(S ? 250 : (Q ? 150 : 170), regionBot - regionTop - supH - kickH, spec.lines.length), dark, { flow: true });
  const m = spec.mascot;
  let mas = '';
  if (m && !Q) {
    const ms = S ? 250 : 190, mx = L.W - L.pad - ms - (m.dx || 0), my = (spec.cta ? ctaY : L.y1 - 40) - ms - 24;
    mas = ({ arch: () => arch('mas', mx, my, ms, m.mood || 'good', m.rot || 0, m.fill), sun: () => sun('mas', mx, my, ms, m.fill || '#FFC700', m.rot || 0), lobe: () => lobe('mas', mx, my, ms, m.fill || '#5B7BD9', m.rot || 0), eyes: () => eyes('mas', mx, my + ms * .3, ms, m.fill || F.a) }[m.kind] || (() => ''))();
  }
  return [
    chrome(spec, L, F),
    `<div class="a" data-tag="region" style="left:${L.pad}px;top:${regionTop}px;width:${L.cw}px;height:${regionBot - regionTop}px;display:flex;flex-direction:column;justify-content:${spec.valign || 'center'}">${kick}${head}${sup}</div>`,
    mas,
    spec.cta ? ctaPill(L, ctaY, spec.cta, dark ? F.a : C.panel, { dot: dark ? C.panel : F.a }) : '',
  ].join('');
}

// ---- LOOK: answer (the FAQ story). Small question sticker over a big answer slab. -------------------------------
export function answer(spec, L, F) {
  const dark = isDark(spec), S = L.story;
  const slabX = L.pad, slabW = L.cw;
  const qTop = L.y0 + (S ? 120 : 110);
  const qh = S ? 120 : 104;
  const slabTop = qTop + qh + (S ? 56 : 44);
  const slabH = (spec.cta === false ? L.y1 - 60 : L.y1 - (S ? 250 : 210)) - slabTop;
  const fillBg = spec.slab || F.a, fg = textOn(fillBg);
  const ans = txt('answer', 56, 60, slabW - 112, slabH - (spec.support ? 370 : 150) - (spec.mascot && !spec.support ? (S ? 170 : 130) : 0), spec.answerHtml || esc(spec.answer), { size: S ? 120 : 96, weight: 800, color: fg, ls: '-.055em', lh: .98, fit: 38, grow: S ? 150 : 120, bg: fillBg, extra: `font-family:Archivo,Geist,sans-serif;font-stretch:104%;` });
  const supHtml = spec.support ? txt('support', 56, slabH - 250, slabW - 112 - (spec.mascot ? (S ? 230 : 170) : 0), 190, esc(spec.support), { size: S ? 44 : 36, weight: 500, color: fg, ls: '-.025em', lh: 1.2, fit: 22, bg: fillBg, extra: 'opacity:.96;' }) : '';
  const slab = card('slab', slabX, slabTop, slabW, slabH, fillBg, { r: 32, shadow: glow(fillBg), inner: ans + supHtml });
  const q = `<div class="a" data-tag="q" style="left:${L.pad + (S ? 96 : 84)}px;top:${qTop}px;z-index:9;transform:rotate(-2.5deg);transform-origin:left center">${chip(spec.q, C.panel, { size: S ? 44 : 38, color: '#fff' })}</div>`;
  const qBadge = `<div class="a d" data-tag="qb" data-bg="${F.a}" style="left:${L.pad - 12}px;top:${qTop - 18}px;width:${S ? 92 : 80}px;height:${S ? 92 : 80}px;border-radius:999px;background:${F.a};color:${textOn(F.a)};display:flex;align-items:center;justify-content:center;font-size:${S ? 56 : 48}px;z-index:10;box-shadow:0 0 0 6px ${C.page}">?</div>`;
  const m = spec.mascot; let mas = '';
  if (m) { const ms = S ? 250 : 190; const mx = L.W - L.pad - ms - 16, my = slabTop + slabH - ms * .62; mas = m.kind === 'sun' ? sun('mas', mx, my, ms, m.fill, m.rot || 8) : m.kind === 'lobe' ? lobe('mas', mx, my, ms, m.fill, m.rot || -8) : arch('mas', mx, my, ms, m.mood || 'good', m.rot || 6, m.fill); }
  return [chrome(spec, L, F), q, qBadge, slab, mas, spec.cta === false ? '' : ctaPill(L, L.y1 - (S ? 150 : 118), spec.cta || 'Find your tutor', dark ? F.a : C.panel, { dot: dark ? C.panel : F.a, h: S ? 110 : 92 })].join('');
}

// ---- LOOK: eyes (V9). A slab with big peeking eyes, a question card, one answer line. ---------------------------
export function eyesLook(spec, L, F) {
  const S = L.story;
  const slabTop = L.y0 + (S ? 560 : 460), slabH = L.y1 - slabTop - (spec.cta ? (S ? 160 : 130) : 0);
  const ew = Math.min(L.cw - 40, S ? 820 : 640), eh = Math.round(ew * .62);
  const slab = box('slab', L.pad, slabTop, L.cw, slabH, `background:${F.a};border-radius:32px;overflow:hidden;box-shadow:${glow(F.a)}`, eyes('eyesvg', (L.cw - ew) / 2, slabH - eh + 4, ew, F.a === C.orange ? '#FF9A3D' : F.a).replace('class="a"', 'class="a" data-deco="1"').replace(/<path d="M0 124[^>]*fill="[^"]*"\/>/, m => m.replace(/fill="[^"]*"/, `fill="${F.deep}"`)));
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, hs(S ? 230 : 150, slabTop - L.y0 - 140 - (spec.support ? (S ? 150 : 110) : 0), spec.lines.length), false, { flow: true });
  const sup = spec.support ? `<div data-tag="support" data-fit="22" style="font-size:${S ? 44 : 36}px;font-weight:500;line-height:1.18;letter-spacing:-.03em;color:${C.prose};margin-top:${S ? 36 : 24}px">${esc(spec.support)}</div>` : '';
  return [chrome(spec, L, F),
    `<div class="a" data-tag="region" style="left:${L.pad}px;top:${L.y0 + 100}px;width:${L.cw}px;height:${slabTop - L.y0 - 140}px;display:flex;flex-direction:column;justify-content:center">${head}${sup}</div>`,
    slab,
    spec.cta ? ctaPill(L, L.y1 - (S ? 140 : 112), spec.cta, C.panel, { dot: F.a, h: S ? 110 : 92 }) : ''].join('');
}

// ---- LOOK: mood (character stories). One blob, one situation, one line. ------------------------------------------
export function mood(spec, L, F) {
  const S = L.story, f = MOOD_FILL[spec.mood] || F.a, dark = false;
  const slabTop = L.y0 + 110, slabH = (L.y1 - 200) - slabTop - (S ? 400 : 300);
  const bw = Math.min(L.cw - 120, S ? 560 : 420);
  const slab = card('slab', L.pad, slabTop, L.cw, slabH, f, { r: 32, shadow: glow(f) });
  const bl = arch('mas', L.pad + (L.cw - bw) / 2, slabTop + (slabH - bw) / 2, bw, spec.mood, spec.rot ?? -4, f === MOOD_FILL.great ? '#FFFFFF' : '#FFFFFF').replace(/fill="#FFFFFF"/, `fill="#FFFFFF"`);
  const lineTop = slabTop + slabH + (S ? 56 : 40);
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, hs(S ? 190 : 120, L.y1 - 60 - lineTop - (spec.support ? (S ? 110 : 90) : 0), spec.lines.length), false, { min: 44, flow: true });
  return [chrome(spec, L, F), slab, bl,
    `<div class="a" data-tag="region" style="left:${L.pad}px;top:${lineTop}px;width:${L.cw}px;height:${L.y1 - 60 - lineTop}px;display:flex;flex-direction:column;justify-content:flex-start">${head}${spec.support ? `<div data-tag="support" data-fit="22" style="font-size:${S ? 48 : 36}px;font-weight:500;line-height:1.2;letter-spacing:-.03em;color:${C.prose};margin-top:28px">${esc(spec.support)}</div>` : ''}</div>`].join('');
}

// ---- LOOK: poll (interactive frame). Leaves a clean zone for the native sticker added in the app. -------------------
export function poll(spec, L, F) {
  const S = L.story;
  const zoneTop = L.y0 + (S ? 520 : 400), zoneH = (S ? 520 : 400);
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, hs(S ? 140 : 110, zoneTop - L.y0 - 260, spec.lines.length), false, { min: 46, flow: true });
  const zone = card('zone', L.pad, zoneTop, L.cw, zoneH, C.muted, { r: 32, ring: true });
  const m = spec.mascot ? eyes('eyes', L.W - L.pad - 360, zoneTop - 150, 360, F.a) : '';
  return [chrome(spec, L, F),
    `<div class="a" data-tag="region" style="left:${L.pad}px;top:${L.y0 + 110}px;width:${L.cw}px;height:${zoneTop - L.y0 - 260}px;display:flex;flex-direction:column;justify-content:center">${head}</div>`,
    zone, m].join('');
}

// ---- LOOK: cover (highlight cover, circle-safe). -----------------------------------------------------------------
export function cover(spec, L, F) {
  // Opaque and full-bleed: a highlight cover is cropped to a circle by the app, so the whole canvas carries the colour.
  const cx = 540, cy = 930, w = 480;
  const ch = spec.char === 'sun' ? sun('mas', cx - w / 2, cy - w / 2 - 70, w, spec.fill || '#FFC700', 0) : spec.char === 'lobe' ? lobe('mas', cx - w / 2, cy - w / 2 - 70, w, '#5B7BD9', 0) : arch('mas', cx - w / 2, cy - w / 2 - 70, w, spec.mood || 'good', 0, spec.fill);
  const bg = spec.disc || F.tint;
  return [ch, `<div class="a d" data-tag="label" data-fit="40" data-bg="${bg}" data-bleed="1" style="left:${cx - 330}px;top:${cy + 200}px;width:660px;text-align:center;font-size:120px;color:${C.ink};line-height:1.2;letter-spacing:-.05em;white-space:nowrap">${esc(spec.label)}</div>`].join('');
}

// ---- LOOK: button (V10). A hard-shadow pill button on a gridded slab with a scalloped edge and a burst badge. -------
export function button(spec, L, F) {
  const S = L.story, a = F.a;
  const slabH = S ? 760 : 520, slabTop = L.y0 + (S ? 110 : 96);
  const grid = `repeating-linear-gradient(0deg,rgba(31,31,31,.35) 0 3px,transparent 3px 120px),repeating-linear-gradient(90deg,rgba(31,31,31,.35) 0 3px,transparent 3px 120px)`;
  const slab = box('slab', L.pad, slabTop, L.cw, slabH, `background:${a};background-image:${grid};border-radius:32px 32px 0 0;overflow:hidden`);
  const btnH = S ? 220 : 168, btnW = L.cw - 120, btnY = slabTop + (S ? 330 : 250);
  const btn = box('button', L.pad + 60, btnY, btnW, btnH, `background:#FFC700;border-radius:999px;box-shadow:0 12px 0 ${C.ink},0 0 0 6px ${C.ink};display:flex;align-items:center;justify-content:center;gap:24px;z-index:6`,
    `<div data-fit="26" data-bg="#FFC700" style="font-family:Archivo,Geist,sans-serif;font-stretch:104%;font-weight:800;font-size:${S ? 84 : 64}px;letter-spacing:-.05em;color:${C.ink};white-space:nowrap;line-height:1.15;width:${btnW - (S ? 96 : 76) - 110}px;text-align:center">${esc(spec.button)}</div><div style="width:${S ? 96 : 76}px;height:${S ? 96 : 76}px;border-radius:999px;background:${C.ink};display:flex;align-items:center;justify-content:center;flex:none">${arrowSvg(S ? 46 : 36, '#fff')}</div>`);
  const sc = scallop('scal', L.pad, slabTop + slabH - 2, L.cw, 56, C.page, 9).replace('data-deco="1"', 'data-deco="1"');
  const bd = badge('badge', L.W - L.pad - (S ? 250 : 210), slabTop + (S ? 60 : 24), S ? 230 : 190, '#FFFFFF', esc(spec.badge || 'Free'), C.ink, 10);
  const lead = txt('lead', L.pad + 60, slabTop + 90, S ? 560 : 520, S ? 200 : 150, esc(spec.lead || ''), { size: S ? 58 : 48, weight: 700, color: textOn(a), ls: '-.04em', lh: 1.06, fit: 26, bg: a });
  const tail = L.y1 - (S ? 300 : 200);
  const body = txt('body', L.pad, slabTop + slabH + 96, L.cw - (S ? 260 : 200), S ? 210 : 170, esc(spec.body), { size: S ? 56 : 44, weight: 500, color: C.ink, ls: '-.035em', lh: 1.12, fit: 24 });
  const mas = spec.mascot === false ? '' : arch('mas', L.W - L.pad - (S ? 230 : 170), slabTop + slabH - (S ? 150 : 110), S ? 230 : 170, 'great', 8);
  return [chrome(spec, L, F), slab, lead, bd, btn, sc, body, mas].join('');
}

// ---- LOOK: ui (generic product pictures, no fabricated names, ratings or photos). ------------------------------
export function ui(spec, L, F) {
  const S = L.story, a = F.a, dark = isDark(spec);
  const topY = L.y0 + 110;
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, hs(S ? 128 : 108, (S ? 400 : 310), spec.lines.length), dark, { min: 46, flow: true });
  const headEl = `<div class="a" data-tag="region" style="left:${L.pad}px;top:${topY}px;width:${L.cw}px;display:flex;flex-direction:column">${head}</div>`;
  const cardTop = topY + (S ? 420 : 330), cardH = L.y1 - 160 - cardTop;
  let body = '';
  if (spec.variant === 'search') {
    const sb = `<div style="position:absolute;left:44px;top:50px;width:${L.cw - 88}px;height:112px;border-radius:999px;background:#fff;display:flex;align-items:center;padding:0 40px;gap:20px;box-shadow:0 0 0 2px ${C.hairline}"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="${C.secondary}" stroke-width="2.4" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg><span data-fit="22" style="font-size:40px;font-weight:500;color:${C.secondary};letter-spacing:-.02em;white-space:nowrap">${esc(spec.query || 'Subject, class, board, area')}</span></div>`;
    const chips = ['Subject', 'Class', 'Board', 'Area'].map((t, i) => chip(t, [C.orangeTint, C.indigoTint, C.mint, C.peach][i], { size: S ? 38 : 32, color: C.ink })).join('');
    const rows = [0, 1, 2].map(i => `<div style="display:flex;gap:22px;align-items:center;margin-top:${i ? 22 : 0}px"><div style="width:96px;height:96px;border-radius:24px;background:repeating-linear-gradient(45deg,#F2ECE4 0 8px,${C.page} 8px 16px);flex:none"></div><div style="flex:1"><div style="height:26px;width:${[62, 48, 70][i]}%;border-radius:999px;background:${C.hairline}"></div><div style="height:20px;width:${[40, 55, 35][i]}%;border-radius:999px;background:${C.muted};margin-top:14px"></div></div></div>`).join('');
    body = card('panel', L.pad, cardTop, L.cw, cardH, C.card, { r: 32, ring: true, inner: sb + `<div style="position:absolute;left:44px;top:200px;display:flex;gap:16px;flex-wrap:wrap;width:${L.cw - 88}px">${chips}</div><div style="position:absolute;left:44px;top:${S ? 330 : 310}px;width:${L.cw - 88}px">${rows}</div>` });
  } else if (spec.variant === 'profile') {
    const fields = [['Subject', C.orangeTint], ['Board', C.indigoTint], ['Area', C.mint], ['Reviews', C.peach]].slice(0, 3).map(([t, c]) => `<div style="display:flex;align-items:center;gap:20px;margin-top:14px"><div style="min-width:${S ? 200 : 170}px">${chip(t, c, { size: S ? 34 : 28, color: C.ink })}</div><div style="flex:1;height:22px;border-radius:999px;background:${C.hairline}"></div></div>`).join('');
    body = card('panel', L.pad, cardTop, L.cw, cardH, C.card, { r: 32, ring: true, inner:
      `<div style="position:absolute;left:44px;top:44px;width:150px;height:150px;border-radius:999px;background:repeating-linear-gradient(45deg,#F2ECE4 0 8px,${C.page} 8px 16px)"></div><div style="position:absolute;left:224px;top:70px;width:${L.cw - 280}px"><div style="height:34px;width:70%;border-radius:999px;background:${C.hairline}"></div><div style="height:22px;width:45%;border-radius:999px;background:${C.muted};margin-top:20px"></div></div><div style="position:absolute;left:44px;top:196px;width:${L.cw - 88}px">${fields}</div><div style="position:absolute;left:44px;bottom:44px;width:${L.cw - 88}px">${chip(spec.tail || 'Experience and qualifications on the profile', a, { size: S ? 36 : 30 })}</div>` });
  } else if (spec.variant === 'whatsapp') {
    const bub = (t, right) => `<div style="max-width:78%;margin-${right ? 'left' : 'right'}:auto;background:${right ? '#D9FDD3' : '#fff'};border-radius:30px;padding:26px 32px;font-size:${S ? 44 : 36}px;font-weight:500;line-height:1.2;color:${C.ink};letter-spacing:-.02em;margin-top:22px;box-shadow:0 0 0 2px ${C.hairline}" data-bg="${right ? '#D9FDD3' : '#FFFFFF'}">${esc(t)}</div>`;
    body = card('panel', L.pad, cardTop, L.cw, cardH, '#EFE7DC', { r: 32, inner: `<div style="position:absolute;left:44px;top:34px;right:44px">${chip('WhatsApp chat with the tutor', '#25D366', { size: S ? 34 : 28, color: C.ink })}${bub(spec.m1 || 'Hello, is the Maths slot on Saturday free?', true)}${bub(spec.m2 || 'Yes. Let us talk about the batch.', false)}</div>` });
  }
  return [chrome(spec, L, F), headEl, body, spec.cta ? ctaPill(L, L.y1 - (S ? 140 : 108), spec.cta, C.panel, { dot: a, h: S ? 108 : 88 }) : ''].join('');
}
