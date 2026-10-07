// Shared layout helpers and the first set of looks: plate, answer, eyes, mood, poll, cover, button, ui.
// DESIGN RULES (v2, after the owner called v1 "bad design"; each one answers a specific v1 failure):
//  1. FULL-BLEED. The ground colour fills the whole canvas, including the story chrome bands. Text stays in the safe
//     zone; characters and shapes bleed into the unsafe bands. v1 left a bone void above and below every story.
//  2. SCALE. Headlines 800/900 weight and as big as the line count allows; support copy 54px; logo 72px in a pill.
//  3. ONE BIG CHARACTER per piece, large, face visible, bleeding off an edge. v1 characters were 120px decoration.
//  4. DEPTH. Key objects (question card, button, sheet, tag) carry a 4px ink outline and a hard offset shadow.
//  5. COLOUR. Saturated grounds rotate (orange, indigo, mint, ink, tint) so a feed is not one beige page.
import { C, textOn, subjectPalette } from '../src/tokens.mjs';
import { box, card, chip, esc, logoBar, frame } from '../src/kit.mjs';
import { arch, sun, lobe, eyes, scallop, badge, MOOD_FILL } from './characters.mjs';

export const INK = C.ink, BONE = C.page, LEMON = '#FFC700';
export const HS = (n = 8) => `0 0 0 4px ${INK},${n}px ${n + 2}px 0 4px ${INK}`;   // outline + hard offset shadow
export const D = `font-family:Archivo,Geist,sans-serif;font-stretch:104%;`;

// ---- canvas layout. Story chrome (IG header, reply bar) covers the top 250 and bottom 340 px. ------------------------
export function lay(canvas) {
  const W = canvas === 'K' ? 512 : 1080, H = canvas === 'S' ? 1920 : canvas === 'F' ? 1350 : canvas === 'C' ? 1920 : canvas === 'K' ? 512 : 1080;
  const story = canvas === 'S', pad = 56;
  const top = story ? 250 : 0, bot = story ? 340 : 0;
  const y0 = top + (story ? 26 : 48), y1 = H - bot - (story ? 26 : 48);
  return { W, H, canvas, story, Q: canvas === 'Q', pad, top, bot, y0, y1, cw: W - 2 * pad, safe: story ? { top: 250, bottom: 340 } : null };
}
const DEFAULT_GROUND = { plate: 'accent', answer: 'accent', eyes: 'accent', mood: 'mood', poll: 'accent', button: 'accent', ui: 'accent', bands: 'bone', brief: 'accent', card: 'bone', swarm: 'panel', chat: 'tint', calendar: 'tint', review: 'accent', tutor: 'accent', bento: 'bone' };
export function groundInfo(spec, F) {
  if (spec.subject) { const p = subjectPalette(spec.subject); return { bg: p.tint, kind: 'tint', fg: C.ink }; }
  const g = spec.ground || DEFAULT_GROUND[spec.look] || 'accent';
  const bg = g === 'bone' ? BONE : g === 'panel' ? C.panel : g === 'tint' ? F.tint : g === 'mood' ? MOOD_FILL[spec.mood] : F.a;
  return { bg, kind: g, fg: textOn(bg), dark: g === 'panel' };
}
export const groundOf = (spec, F) => groundInfo(spec, F).bg;
export const isDark = spec => spec.ground === 'panel';

// text box. Nest inside a card so the gate sees the right backing colour, or pass bg.
export function txt(tag, x, y, w, h, html, o = {}) {
  const { size = 40, weight = 500, color = INK, ls = '-.03em', lh = 1.1, align = 'left', fit = 14, grow = 0, extra = '', bg = '', cls = '' } = o;
  return `<div class="a ${cls}" data-tag="${tag}"${fit ? ` data-fit="${fit}"` : ''}${grow ? ` data-grow="${grow}"` : ''}${bg ? ` data-bg="${bg}"` : ''} style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;font-size:${size}px;font-weight:${weight};color:${color};letter-spacing:${ls};line-height:${lh};text-align:${align};${extra}">${html}</div>`;
}
export const arrowSvg = (s, c) => `<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="${c}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>`;

// logo in a bone pill, always (never white-inverted) + handle + optional page counter + optional top-right label
export function chrome(spec, L, F, G, o = {}) {
  const lh = L.story ? 72 : 60, lw = Math.round(lh * 252 / 92), py = 16, parts = [];
  const ly = L.story ? 262 : 44;
  if (o.logo !== false) {
    parts.push(box('logopill', L.pad, ly, lw + 52, lh + 2 * py, `background:${BONE};border-radius:999px;z-index:19;box-shadow:0 0 0 4px ${INK},5px 6px 0 4px ${INK}`));
    parts.push(logoBar(L.pad + 26, ly + py, lh));
  }
  const hy = L.H - L.bot - (L.story ? 68 : 62);
  if (o.handle !== false) parts.push(`<div class="a lab" data-tag="handle" data-bg="${G.bg}" style="left:${L.pad}px;top:${hy}px;color:${G.fg};z-index:20;font-size:30px;letter-spacing:.05em">shikshaq.in</div>`);
  if (spec.count) parts.push(`<div class="a lab" data-tag="count" data-bg="${G.bg}" style="left:${L.W - L.pad - 160}px;top:${hy}px;width:160px;text-align:right;color:${G.fg};z-index:20;font-size:30px;letter-spacing:.05em">${esc(spec.count)}</div>`);
  if (spec.tag) parts.push(`<div class="a" data-tag="eyebrow" style="right:${L.pad}px;top:${ly + (L.story ? 18 : 10)}px;z-index:20">${chip(spec.tag, BONE, { size: L.story ? 32 : 28, color: INK }).replace('<span style="', `<span style="box-shadow:0 0 0 3px ${INK},4px 5px 0 3px ${INK};`)}</div>`);
  return parts.join('');
}

// the one call to action: a chunky outlined button with a hard shadow, never a small black pill
export function ctaBtn(L, F, G, text, o = {}) {
  const S = L.story, h = o.h || (S ? 128 : (L.Q ? 112 : 108)), w = o.w || Math.round(L.cw * .62), x = o.x ?? L.pad;
  const y = o.y ?? (L.y1 - h - (S ? 76 : 70));
  const fill = o.fill || (G.kind === 'bone' || G.kind === 'tint' || G.kind === 'panel' ? F.a : BONE), fg = textOn(fill);
  return box('cta', x, y, w, h, `background:${fill};border-radius:999px;display:flex;align-items:center;justify-content:space-between;padding:0 ${Math.round(h * .22)}px 0 ${Math.round(h * .42)}px;z-index:6;box-shadow:${HS(8)}`,
    `<div data-fit="24" data-bg="${fill}" style="${D}color:${fg};font-size:${Math.round(h * .42)}px;font-weight:800;letter-spacing:-.04em;line-height:1.15;width:${w - h - 30}px;white-space:nowrap">${esc(text)}</div>
     <div style="width:${Math.round(h * .62)}px;height:${Math.round(h * .62)}px;border-radius:999px;background:${INK};display:flex;align-items:center;justify-content:center;flex:none">${arrowSvg(Math.round(h * .3), '#fff')}</div>`);
}

// ---- headline from segments: 'plain' | {b} | {tag, fill} | {pill, fill}. Tags and pills are the colour accents. -------
function segHtml(seg, ctx) {
  const { G, F } = ctx;
  const tagFill = seg.fill || (G.kind === 'accent' || G.kind === 'mood' ? BONE : F.a);
  const pillFill = seg.fill || (G.kind === 'accent' || G.kind === 'mood' ? INK : F.a);
  if (typeof seg === 'string') return `<span style="font-weight:600">${esc(seg)}</span>`;
  if (seg.b != null) return `<span style="font-weight:900;letter-spacing:-.06em">${esc(seg.b)}</span>`;
  if (seg.tag != null) return `<span data-bg="${tagFill}" style="display:inline-block;background:${tagFill};color:${textOn(tagFill)};font-weight:900;letter-spacing:-.06em;padding:.0em .16em .06em;border-radius:.16em;transform:rotate(${seg.rot ?? (seg.tag.length > 6 ? -1.5 : -3)}deg);box-shadow:0 0 0 .045em ${INK},.06em .08em 0 .045em ${INK}">${esc(seg.tag)}</span>`;
  if (seg.pill != null) return `<span data-bg="${pillFill}" style="display:inline-flex;align-items:center;gap:.14em;background:${pillFill};color:${textOn(pillFill)};font-weight:900;letter-spacing:-.06em;padding:.0em .2em .06em .3em;border-radius:999px;box-shadow:0 0 0 .045em ${INK},.06em .08em 0 .045em ${INK}">${esc(seg.pill)}<span style="display:inline-flex;width:.6em;height:.6em;border-radius:999px;background:${pillFill === INK ? BONE : INK};align-items:center;justify-content:center">${arrowSvg('.34em', pillFill === INK ? INK : '#fff')}</span></span>`;
  return '';
}
export const hs = (cap, availH, n, lh = 1.12) => Math.max(40, Math.min(cap, Math.floor(availH / (n * lh))));
export function headBlock(tag, x, y, w, lines, F, size, G, o = {}) {
  const hasTag = lines.flat().some(g => typeof g === 'object' && (g.tag != null || g.pill != null));
  const rows = lines.map(l => `<div style="display:flex;align-items:center;gap:.2em;white-space:nowrap;margin-bottom:${l.some(g => typeof g === 'object' && (g.tag || g.pill || '').length > 6) ? '.14em' : '.05em'};justify-content:${o.align === 'center' ? 'center' : 'flex-start'}">${l.map(s => segHtml(s, { G, F })).join('')}</div>`).join('');
  const pos = o.flow ? `position:relative;width:${w}px;` : `position:absolute;left:${x}px;top:${y}px;width:${w}px;`;
  return `<h1 data-tag="${tag}" data-fit="${o.min || 52}" data-bg="${G.bg}" style="${pos}font-size:${size}px;color:${G.fg};line-height:${o.lh || (hasTag ? 1.16 : 1.04)};letter-spacing:-.055em;${D}">${rows}</h1>`;
}

// ---- hero characters: big, face visible, bleeding off the right or bottom edge ----------------------------------------------
export function heroChar(spec, L, F, G, o = {}) {
  const m = spec.mascot; if (!m || L.Q) return '';
  const S = L.story, s = o.s || (S ? 660 : 470);
  const x = o.x ?? L.W - Math.round(s * .6), y = o.y ?? (S ? 1160 : L.H - Math.round(s * .82));
  const fill = m.fill;
  const html = m.kind === 'sun' ? sun('mas', x, y, s, fill || LEMON, m.rot ?? 8)
    : m.kind === 'lobe' ? lobe('mas', x, y, s, fill || '#5B7BD9', m.rot ?? -8)
    : m.kind === 'eyes' ? eyes('mas', x, y + s * .3, s, fill || (G.kind === 'accent' ? F.deep : F.a))
    : arch('mas', x, y, s, m.mood || 'good', m.rot ?? 6, fill || (m.mood ? undefined : F.a === G.bg ? '#FFFFFF' : F.a));
  return html.replace('style="', 'style="z-index:2;');
}

// ---- LOOK: plate. A giant statement, one word on a tag, one in a pill, a huge character, one button. ------------------
export function plate(spec, L, F) {
  const G = groundInfo(spec, F), S = L.story, Q = L.Q;
  const top = (S ? 262 : 44) + 72 + 56, hasCta = !!spec.cta;
  const ctaY = L.y1 - (S ? 128 : (Q ? 112 : 108)) - (S ? 76 : 70);
  const bottom = Q ? ctaY - 40 : (S ? 1130 : 930);
  const supH = spec.support ? (S ? 200 : (Q ? 150 : 140)) : 0, kickH = spec.kicker ? (S ? 110 : 90) : 0;
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, hs(S ? 300 : (Q ? 190 : 230), bottom - top - supH - kickH, spec.lines.length), G, { flow: true });
  const kick = spec.kicker ? `<div style="margin-bottom:${S ? 34 : 24}px">${chip(spec.kicker, spec.kickFill || BONE, { size: S ? 36 : 30, color: spec.kickFill ? undefined : INK }).replace('<span style="', `<span style="box-shadow:0 0 0 3px ${INK},4px 5px 0 3px ${INK};`)}</div>` : '';
  const sup = spec.support ? `<div data-tag="support" data-fit="22" data-bg="${G.bg}" style="font-size:${S ? 56 : (Q ? 40 : 44)}px;font-weight:600;line-height:1.16;letter-spacing:-.03em;color:${G.fg};margin-top:${S ? 44 : 26}px;max-width:${L.cw}px">${esc(spec.support)}</div>` : '';
  return [chrome(spec, L, F, G),
    `<div class="a" data-tag="region" style="left:${L.pad}px;top:${top}px;width:${L.cw}px;height:${bottom - top}px;display:flex;flex-direction:column;justify-content:${spec.valign || 'center'}">${kick}${head}${sup}</div>`,
    heroChar(spec, L, F, G),
    hasCta ? ctaBtn(L, F, G, spec.cta, { y: ctaY, w: Q ? L.cw : Math.round(L.cw * .62) }) : ''].join('');
}

// ---- LOOK: answer (the FAQ). Question on a card, the answer huge on the ground, a big character. ---------------------------
export function answer(spec, L, F) {
  const G = groundInfo(spec, F), S = L.story;
  const top = (S ? 262 : 44) + 72 + 70, ctaY = L.y1 - (S ? 128 : 108) - (S ? 76 : 70);
  const bottom = S ? 1150 : 900;
  const qh = S ? 170 : 130;
  const q = `<div style="position:relative;margin-bottom:${S ? 56 : 38}px;align-self:flex-start;max-width:${L.cw - 40}px"><div data-tag="q" data-fit="26" data-bg="${BONE}" style="${D}background:${BONE};color:${INK};font-size:${S ? 54 : 44}px;font-weight:800;letter-spacing:-.04em;line-height:1.12;padding:${S ? 30 : 22}px ${S ? 40 : 30}px ${S ? 30 : 22}px ${S ? 120 : 96}px;border-radius:32px;box-shadow:${HS(8)};transform:rotate(-1.5deg)">${esc(spec.q)}</div><div data-tag="qb" data-bg="${INK}" style="${D}position:absolute;left:-14px;top:50%;margin-top:-${S ? 48 : 40}px;width:${S ? 96 : 80}px;height:${S ? 96 : 80}px;border-radius:999px;background:${INK};color:${BONE};display:flex;align-items:center;justify-content:center;font-size:${S ? 60 : 50}px;font-weight:900;box-shadow:0 0 0 5px ${BONE}">?</div></div>`;
  const supH = spec.support ? (S ? 210 : 150) : 0;
  const ansSize = hs(S ? 190 : 140, bottom - top - qh - 56 - supH, Math.max(2, Math.ceil(spec.answer.length / (S ? 11 : 13))), 1.06);
  const ans = `<div data-tag="answer" data-fit="40" data-grow="${S ? 230 : 170}" data-bg="${G.bg}" style="${D}font-size:${ansSize}px;font-weight:900;color:${G.fg};line-height:1.0;letter-spacing:-.06em;width:${L.cw}px;max-height:${bottom - top - qh - 56 - supH}px">${spec.answerHtml || esc(spec.answer)}</div>`;
  const sup = spec.support ? `<div data-tag="support" data-fit="22" data-bg="${G.bg}" style="font-size:${S ? 54 : 42}px;font-weight:600;line-height:1.16;letter-spacing:-.03em;color:${G.fg};margin-top:${S ? 36 : 24}px;max-width:${L.cw - (S ? 190 : 120)}px">${esc(spec.support)}</div>` : '';
  return [chrome(spec, L, F, G),
    `<div class="a" data-tag="region" style="left:${L.pad}px;top:${top}px;width:${L.cw}px;height:${bottom - top}px;display:flex;flex-direction:column;justify-content:flex-start">${q}${ans}${sup}</div>`,
    heroChar({ ...spec, mascot: spec.mascot || { kind: 'arch', mood: 'good' } }, L, F, G),
    spec.cta === false ? '' : ctaBtn(L, F, G, spec.cta || 'Find your tutor', { y: ctaY })].join('');
}

// ---- LOOK: eyes. The reference's big peeking eyes rising off the bottom of the canvas. ---------------------------------
export function eyesLook(spec, L, F) {
  const G = groundInfo(spec, F), S = L.story, Q = L.Q;
  const top = (S ? 262 : 44) + 72 + 56, ew = S ? 1240 : (Q ? 900 : 1100), eh = Math.round(ew * .62);
  const eyeTop = S ? 1010 : (Q ? L.H - eh * .86 : L.H - eh * .84);
  const dome = G.kind === 'accent' ? F.deep : F.a;
  const eyeSvg = eyes('eyesvg', -(ew - L.W) / 2, eyeTop, ew, dome).replace('class="a"', 'class="a" data-deco="1"');
  const fillBelow = `<div class="a" data-deco="1" style="left:0;top:${eyeTop + eh - 2}px;width:${L.W}px;height:${L.H - eyeTop - eh + 4}px;background:${dome}"></div>`;
  const bottom = eyeTop - (spec.cta ? (S ? 190 : 150) : 40), supH = spec.support ? (S ? 190 : 130) : 0;
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, hs(S ? 280 : 200, bottom - top - supH, spec.lines.length), G, { flow: true });
  const sup = spec.support ? `<div data-tag="support" data-fit="22" data-bg="${G.bg}" style="font-size:${S ? 56 : 42}px;font-weight:600;line-height:1.16;letter-spacing:-.03em;color:${G.fg};margin-top:${S ? 40 : 24}px">${esc(spec.support)}</div>` : '';
  return [chrome(spec, L, F, G, { handle: false }), fillBelow, eyeSvg,
    `<div class="a" data-tag="region" style="left:${L.pad}px;top:${top}px;width:${L.cw}px;height:${bottom - top}px;display:flex;flex-direction:column;justify-content:center">${head}${sup}</div>`,
    spec.cta ? ctaBtn(L, F, G, spec.cta, { y: eyeTop - (S ? 168 : 134), w: Math.round(L.cw * .7) }) : ''].join('');
}

// ---- LOOK: mood. The ground IS the mood colour; one huge blob with its face, one line of type. ------------------------
export function mood(spec, L, F) {
  const G = groundInfo(spec, F), S = L.story, Q = L.Q;
  const top = (S ? 262 : 44) + 72 + 56, bw = S ? 920 : (Q ? 560 : 760);
  const by = S ? 960 : (Q ? L.H - bw * .86 : L.H - bw * .8);
  const blob = arch('mas', (L.W - bw) / 2, by, bw, spec.mood, spec.rot ?? -4, '#FFFFFF');
  const bottom = by - 20, supH = spec.support ? (S ? 150 : 110) : 0;
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, hs(S ? 230 : 160, bottom - top - supH, spec.lines.length), G, { min: 44, flow: true });
  const sup = spec.support ? `<div data-tag="support" data-fit="22" data-bg="${G.bg}" style="font-size:${S ? 52 : 40}px;font-weight:600;line-height:1.16;letter-spacing:-.03em;color:${G.fg};margin-top:24px">${esc(spec.support)}</div>` : '';
  const fillBelow = `<div class="a" data-deco="1" style="left:${(L.W - bw) / 2 + bw * .06}px;top:${by + bw - 4}px;width:${bw * .88}px;height:${L.H - by - bw + 4}px;background:#FFFFFF"></div>`;
  return [chrome(spec, L, F, G, { handle: false }), blob, fillBelow,
    `<div class="a" data-tag="region" style="left:${L.pad}px;top:${top}px;width:${L.cw}px;height:${bottom - top}px;display:flex;flex-direction:column;justify-content:center">${head}${sup}</div>`].join('');
}

// ---- LOOK: poll. A frame for a native sticker: a bone card with hard shadow, eyes peeking over it. ----------------------
export function poll(spec, L, F) {
  const G = groundInfo(spec, F), S = L.story;
  const top = (S ? 262 : 44) + 72 + 56, zoneTop = S ? 840 : 600, zoneH = S ? 560 : 420;
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, hs(S ? 190 : 130, zoneTop - top - 120, spec.lines.length), G, { min: 46, flow: true });
  const zone = box('zone', L.pad, zoneTop, L.cw, zoneH, `background:${BONE};border-radius:32px;box-shadow:${HS(10)};z-index:3`);
  const peek = eyes('eyes', L.W - L.pad - (S ? 420 : 320), zoneTop - (S ? 250 : 190), S ? 420 : 320, INK).replace('style="', 'style="z-index:2;');
  const sunC = S ? sun('c1', -150, 1470, 430, LEMON, -10) : '';
  const archC = S ? arch('c2', 770, 1470, 400, 'great', 8, '#FFFFFF') : '';
  return [chrome(spec, L, F, G, { handle: false }),
    `<div class="a" data-tag="region" style="left:${L.pad}px;top:${top}px;width:${L.cw}px;height:${zoneTop - top - 120}px;display:flex;flex-direction:column;justify-content:center">${head}</div>`, peek, zone, sunC, archC].join('');
}

// ---- LOOK: cover (highlight cover, circle-safe, opaque and full-bleed). ---------------------------------------------------
export function cover(spec, L, F) {
  const cx = 540, cy = 930, w = 480;
  const ch = spec.char === 'sun' ? sun('mas', cx - w / 2, cy - w / 2 - 70, w, spec.fill || LEMON, 0) : spec.char === 'lobe' ? lobe('mas', cx - w / 2, cy - w / 2 - 70, w, '#5B7BD9', 0) : arch('mas', cx - w / 2, cy - w / 2 - 70, w, spec.mood || 'good', 0, spec.fill);
  const bg = spec.disc || F.tint;
  return [ch, `<div class="a d" data-tag="label" data-fit="40" data-bg="${bg}" data-bleed="1" style="left:${cx - 330}px;top:${cy + 200}px;width:660px;text-align:center;font-size:120px;color:${INK};line-height:1.2;letter-spacing:-.05em;white-space:nowrap">${esc(spec.label)}</div>`].join('');
}

// ---- LOOK: button. A gridded colour field, one enormous button, a big character. ---------------------------------------
export function button(spec, L, F) {
  const G = groundInfo(spec, F), S = L.story, a = F.a;
  const grid = `repeating-linear-gradient(0deg,rgba(31,31,31,.28) 0 3px,transparent 3px 120px),repeating-linear-gradient(90deg,rgba(31,31,31,.28) 0 3px,transparent 3px 120px)`;
  const field = `<div class="a" data-deco="1" style="left:0;top:0;width:${L.W}px;height:${L.H}px;background-image:${grid}"></div>`;
  const top = (S ? 262 : 44) + 72 + 60;
  const lead = txt('lead', L.pad, top, L.cw - (S ? 300 : 230), S ? 330 : 230, esc(spec.lead || ''), { size: S ? 104 : 80, weight: 900, color: G.fg, ls: '-.055em', lh: 1.02, fit: 40, bg: a, extra: D });
  const bd = badge('badge', L.W - L.pad - (S ? 290 : 220), top - 10, S ? 290 : 220, BONE, esc(spec.badge || 'Free'), INK, 10);
  const btnH = S ? 250 : 190, btnY = S ? top + 420 : top + 270, btnW = L.cw;
  const btn = box('button', L.pad, btnY, btnW, btnH, `background:${LEMON};border-radius:999px;box-shadow:${HS(14)};display:flex;align-items:center;justify-content:center;gap:26px;z-index:6`,
    `<div data-fit="26" data-bg="${LEMON}" style="${D}font-weight:900;font-size:${S ? 98 : 74}px;letter-spacing:-.055em;color:${INK};white-space:nowrap;line-height:1.15;width:${btnW - btnH * .6 - 150}px;text-align:center">${esc(spec.button)}</div><div style="width:${Math.round(btnH * .46)}px;height:${Math.round(btnH * .46)}px;border-radius:999px;background:${INK};display:flex;align-items:center;justify-content:center;flex:none">${arrowSvg(Math.round(btnH * .22), '#fff')}</div>`);
  const body = txt('body', L.pad, btnY + btnH + (S ? 90 : 60), S ? L.cw - 300 : L.cw - 230, S ? 300 : 190, esc(spec.body), { size: S ? 60 : 46, weight: 700, color: G.fg, ls: '-.035em', lh: 1.12, fit: 24, bg: a });
  const ch = arch('mas', L.W - Math.round((S ? 640 : 440) * .62), S ? 1180 : L.H - 340, S ? 640 : 440, 'great', 8, '#FFFFFF');
  return [field, chrome(spec, L, F, G), lead, bd, btn, body, ch].join('');
}

// ---- LOOK: ui. Generic product pictures on a hard-shadow sheet. No invented names, ratings or photos. ------------------
export function ui(spec, L, F) {
  const G = groundInfo(spec, F), S = L.story, a = F.a;
  const top = (S ? 262 : 44) + 72 + 56, headH = S ? 470 : 340;
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, hs(S ? 200 : 140, headH, spec.lines.length), G, { min: 46, flow: true });
  const cardTop = top + headH + (S ? 50 : 30), cardH = L.y1 - (S ? 40 : 40) - cardTop, W2 = L.cw;
  let body = '';
  const skel = (w, h = 26, c = C.hairline) => `<div style="height:${h}px;width:${w}%;border-radius:999px;background:${c}"></div>`;
  if (spec.variant === 'search') {
    const sb = `<div style="position:absolute;left:40px;top:44px;width:${W2 - 80}px;height:120px;border-radius:999px;background:#fff;display:flex;align-items:center;padding:0 44px;gap:22px;box-shadow:0 0 0 4px ${INK}"><svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="${INK}" stroke-width="2.6" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg><span data-fit="22" style="font-size:44px;font-weight:600;color:${C.secondary};letter-spacing:-.02em;white-space:nowrap">${esc(spec.query || 'Subject, class, board, area')}</span></div>`;
    const chips = ['Subject', 'Class', 'Board', 'Area'].map((t, i) => chip(t, [C.orangeTint, C.indigoTint, C.mint, C.peach][i], { size: S ? 42 : 34, color: INK })).join('');
    const rows = [0, 1, 2].map(i => `<div style="display:flex;gap:26px;align-items:center;margin-top:${i ? 26 : 0}px"><div style="width:110px;height:110px;border-radius:28px;background:repeating-linear-gradient(45deg,#F2ECE4 0 8px,${BONE} 8px 16px);flex:none;box-shadow:0 0 0 3px ${INK}"></div><div style="flex:1">${skel([62, 48, 70][i], 30, C.hairline)}<div style="height:8px"></div>${skel([40, 55, 35][i], 22, C.muted)}</div></div>`).join('');
    body = `${sb}<div style="position:absolute;left:40px;top:200px;display:flex;gap:16px;flex-wrap:wrap;width:${W2 - 80}px">${chips}</div><div style="position:absolute;left:40px;top:${S ? 350 : 330}px;width:${W2 - 80}px">${rows}</div>`;
  } else if (spec.variant === 'profile') {
    const fields = [['Subject', C.orangeTint], ['Board', C.indigoTint], ['Area', C.mint]].map(([t, c]) => `<div style="display:flex;align-items:center;gap:22px;margin-top:20px"><div style="min-width:${S ? 230 : 190}px">${chip(t, c, { size: S ? 40 : 32, color: INK })}</div><div style="flex:1">${skel(100, 26)}</div></div>`).join('');
    body = `<div style="position:absolute;left:40px;top:40px;width:170px;height:170px;border-radius:999px;background:repeating-linear-gradient(45deg,#F2ECE4 0 8px,${BONE} 8px 16px);box-shadow:0 0 0 4px ${INK}"></div><div style="position:absolute;left:240px;top:70px;width:${W2 - 300}px">${skel(70, 38)}<div style="height:18px"></div>${skel(45, 24, C.muted)}</div><div style="position:absolute;left:40px;top:240px;width:${W2 - 80}px">${fields}</div><div style="position:absolute;left:40px;bottom:44px">${chip(spec.tail || 'Experience, qualifications and reviews', a, { size: S ? 38 : 30 })}</div>`;
  } else if (spec.variant === 'whatsapp') {
    const bub = (t, right) => `<div data-bg="${right ? '#D9FDD3' : '#FFFFFF'}" style="max-width:80%;margin-${right ? 'left' : 'right'}:auto;background:${right ? '#D9FDD3' : '#fff'};border-radius:34px;padding:30px 38px;font-size:${S ? 50 : 40}px;font-weight:600;line-height:1.2;color:${INK};letter-spacing:-.025em;margin-top:28px;box-shadow:0 0 0 3px ${INK}">${esc(t)}</div>`;
    body = `<div style="position:absolute;left:40px;top:40px;right:40px">${chip('WhatsApp chat with the tutor', '#25D366', { size: S ? 38 : 30, color: INK })}${bub(spec.m1 || 'Hello, is the Maths slot on Saturday free?', true)}${bub(spec.m2 || 'Yes. Let us talk about the batch.', false)}</div>`;
  }
  const sheet = box('panel', L.pad, cardTop, W2, cardH, `background:${BONE};border-radius:32px;box-shadow:${HS(12)};z-index:3;overflow:visible`, body);
  const stepTag = spec.tag ? `<div class="a" data-tag="steptag" style="right:${L.pad + 20}px;top:${cardTop - (S ? 52 : 40)}px;transform:rotate(4deg);z-index:9">${chip(spec.tag, LEMON, { size: S ? 44 : 34, color: INK }).replace('<span style="', `<span style="box-shadow:0 0 0 3px ${INK},4px 5px 0 3px ${INK};`)}</div>` : '';
  const ch = spec.mascot === false ? '' : (S ? arch('mas', -120, cardTop + cardH - 250, 330, 'good', -8, '#FFFFFF').replace('style="', 'style="z-index:4;') : '');
  return [chrome({ ...spec, tag: null }, L, F, G), `<div class="a" data-tag="region" style="left:${L.pad}px;top:${top}px;width:${L.cw}px;height:${headH}px;display:flex;flex-direction:column;justify-content:center">${head}</div>`, sheet, stepTag, ch].join('');
}
