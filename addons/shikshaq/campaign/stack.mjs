// The panel-stack engine. The live site is a stack of big-radius panels (bone, tint, an orange or indigo slab, one dark),
// each carrying a numbered heading, an icon tile, a dotted card, highlighted pills. A poster is that stack, sized to the
// canvas. Panels FLOW, so content never lands on content; one fit pass picks the largest unit that fits, so nothing is
// cramped and nothing is left empty. Every size below is `calc(var(--k) * Npx)`.
import { textOn } from '../src/tokens.mjs';
import { esc } from '../src/kit.mjs';
import { INK, BONE, CARD, MUTED, HAIR, PANEL, LEMON, ORANGE, ORANGE_DEEP, ORANGE_TINT, INDIGO, INDIGO_DEEP, INDIGO_TINT, MINT, MINT_SOLID, MINT_DEEP, PEACH, ACC, ICONS, icon, iconTile, mascot, arch } from './kit3.mjs';
import { LOGO } from '../src/kit.mjs';

const px = n => `calc(var(--k) * ${n}px)`;
const FAM = `font-family:Archivo,Geist,sans-serif;font-stretch:108%;`;
const GEIST = `font-family:Geist,system-ui,sans-serif;`;
const SECOND = '#6A625A', PROSE = '#4A443E';   // the warm ramp, darkened one step so small type clears 4.5:1 on every tint

// ---- fills ---------------------------------------------------------------------------------------------------------------------
function fillOf(f, A) {
  const m = { bone: BONE, card: CARD, muted: MUTED, tint: A.tint, peach: PEACH, orange: ORANGE, indigo: INDIGO, mint: MINT_SOLID, mintTint: MINT, indigoTint: INDIGO_TINT, orangeTint: ORANGE_TINT, panel: PANEL, accent: A.a, lemon: LEMON };
  return m[f] || f || BONE;
}
const fgOn = bg => (bg === PANEL ? '#F9F5F1' : textOn(bg));
const payOf = (bg, A, pay) => pay === 'ink' ? INK : pay === 'white' ? '#FFFFFF' : pay === 'lemon' ? LEMON : (bg === ORANGE || bg === INDIGO || bg === MINT_SOLID) ? INK === fgOn(bg) ? '#FFFFFF' : LEMON : (bg === PANEL ? A.a : (pay === 'indigo' ? INDIGO : pay === 'mint' ? MINT_DEEP : (bg === ORANGE_TINT || bg === PEACH) ? ORANGE_DEEP : A.a === ORANGE ? ORANGE : A.a === INDIGO ? INDIGO : MINT_DEEP));

// ---- the mixed-weight headline: plain 400, {b} 800 payoff in colour, {hl} a highlighted pill, {tag} a marker tag ---------------
function seg(s, c) {
  if (s && s.pill != null && s.hl == null) s = { hl: s.pill, fill: s.fill };
  if (typeof s === 'string') return `<span style="font-weight:${c.plainW || 400}">${esc(s)}</span>`;
  if (s.b != null) return `<span style="font-weight:800;letter-spacing:-.06em;color:${s.c || c.pay}">${esc(s.b)}</span>`;
  if (s.hl != null) { const f = fillOf(s.fill || 'orange'); return `<span data-bg="${f}" style="display:inline-block;background:${f};color:${fgOn(f)};font-weight:800;letter-spacing:-.05em;padding:.02em .3em .1em;border-radius:999px;margin:0 .04em">${esc(s.hl)}</span>`; }
  if (s.tag != null) { const f = fillOf(s.fill || 'lemon'); return `<span data-bg="${f}" style="display:inline-block;background:${f};color:${fgOn(f)};font-weight:800;letter-spacing:-.06em;padding:0 .16em .06em;border-radius:.16em;transform:rotate(${s.rot ?? -2.5}deg);margin:0 .03em">${esc(s.tag)}</span>`; }
  return '';
}
export function mix(lines, { size = 110, fg = INK, pay = ORANGE, align = 'left', lh = 1.07, plainW = 400, indentLast = '' } = {}) {
  const c = { fg, pay, plainW };
  const txtOf = s => typeof s === 'string' ? s : (s.b ?? s.hl ?? s.tag ?? s.pill ?? '');
  const rows = lines.map((l, li) => { const segs = (Array.isArray(l) ? l : [l]); const inner = segs.map((s, si) => (si && !/^[?.,!:;)]/.test(txtOf(s)) ? ' ' : '') + seg(s, c)).join(''); return `<div data-fitw="1" data-nowrap="1" style="display:block;white-space:nowrap;text-align:${align === 'center' ? 'center' : 'left'};line-height:${lh};padding-bottom:.05em;${indentLast && li === lines.length - 1 && lines.length > 1 ? `padding-left:${indentLast}` : ''}">${inner}</div>`; }).join('');
  return `<div data-tag="headline" style="${FAM}font-size:${px(size)};color:${fg};letter-spacing:-.055em;margin:0">${rows}</div>`;
}
const eyebrow = (t, color, size = 40) => `<div style="${GEIST}font-size:${px(size)};font-weight:700;color:${color};letter-spacing:-.01em;margin-bottom:${px(14)}">${esc(t)}</div>`;
const label = (t, color, size = 26) => `<div style="${GEIST}font-size:${px(size)};font-weight:700;color:${color};letter-spacing:.06em;text-transform:uppercase">${esc(t)}</div>`;
const body = (t, color, size = 40, w = 500, extra = '') => `<div data-tag="body" style="${GEIST}font-size:${px(size)};font-weight:${w};color:${color};line-height:1.22;letter-spacing:-.02em;${extra}">${esc(t)}</div>`;
const chipEl = (t, fill, fg, size = 34) => `<span data-bg="${fill}" style="${GEIST}display:inline-block;background:${fill};color:${fg};font-size:${px(size)};font-weight:700;padding:${px(size * .3)} ${px(size * .78)};border-radius:999px;letter-spacing:-.01em;white-space:nowrap">${esc(t)}</span>`;
const pillBtn = (t, fill, fg, size = 44, arrow = true) => `<div data-bg="${fill}" style="${GEIST}display:inline-flex;align-items:center;gap:${px(16)};background:${fill};color:${fg};font-size:${px(size)};font-weight:700;padding:${px(size * .42)} ${px(size * .9)};border-radius:999px;letter-spacing:-.02em;white-space:nowrap">${esc(t)}${arrow ? icon('arrow', px(size * .9), fg, 2.6) : ''}</div>`;

// ---- panel types -----------------------------------------------------------------------------------------------------------------
const mas = (m, size, pos) => m ? mascot(m, `position:absolute;${pos};width:${px(size)};height:${px(size)}`, 'mas') : '';

const TYPES = {
  // numbered heading + mixed headline (+ optional mascot): the home page's opening
  head(p, A, ctx) {
    const bg = fillOf(p.fill || 'card', A), fg = fgOn(bg), pay = payOf(bg, A, p.pay);
    const ord = p.ordinal ? `<span style="${GEIST}font-size:${px(26)};font-weight:700;color:${SECOND};letter-spacing:.07em;position:absolute;left:0;bottom:${px(14)}">${esc(p.ordinal)}</span>` : '';
    const h = p.ordinal ? `<div style="position:relative">${ord}${mix(p.lines, { size: p.size || 112, fg, pay, plainW: p.plainW, indentLast: px(Math.round((p.size || 112) * .5)) })}</div>` : mix(p.lines, { size: p.size || 112, fg, pay, plainW: p.plainW, align: p.align });
    const m = p.mascot ? mas(p.mascot, Math.min(p.mascot.size || 300, 280), `right:${px(-70)};bottom:${px(-80)};z-index:1`) : '';
    return { bg, html: `${p.eyebrow ? eyebrow(p.eyebrow, p.eyebrowC || (A.a === ORANGE ? ORANGE_DEEP : A.deep)) : ''}${h}${p.sub ? body(p.sub, bg === PANEL ? '#CFC7BD' : SECOND, 42, 500, `margin-top:${px(24)};max-width:${p.mascot ? '66%' : '100%'}`) : ''}${m}`, padR: p.mascot ? px(210) : 0 };
  },
  // tint panel: icon tile, small label, a bold payoff beside plain words ("Message them yourself, free")
  tile(p, A) {
    const bg = fillOf(p.fill || 'tint', A), tileFill = p.tileFill || A.a;
    const pay = p.pay === 'ink' ? INK : (bg === ORANGE_TINT || bg === PEACH ? ORANGE_DEEP : (bg === INDIGO_TINT ? INDIGO_DEEP : (bg === MINT ? MINT_DEEP : A.deep)));
    const m = p.mascot ? mas(p.mascot, Math.min(p.mascot.size || 300, 300), `right:${px(-70)};top:50%;margin-top:${px(-150)};z-index:1`) : '';
    return { bg, html: `<div style="display:flex;align-items:center;gap:${px(24)};margin-bottom:${px(22)}">${iconTile(p.icon || 'users', 122, { fill: tileFill, stroke: textOn(tileFill) === INK ? INK : '#fff', radius: .28 }, px)}${p.label ? `<div style="${GEIST}font-size:${px(40)};font-weight:500;color:${SECOND}">${esc(p.label)}</div>` : ''}</div>${mix(p.lines, { size: p.size || 104, fg: INK, pay })}${p.sub ? body(p.sub, PROSE, 42, 500, `margin-top:${px(22)};max-width:72%`) : ''}${m}`, padR: p.mascot ? px(180) : 0 };
  },
  // the dotted empty-state card with the outlined icon tile, a title and a button
  dots(p, A) {
    const bg = fillOf(p.fill || 'bone', A);
    const tile = iconTile(p.icon || 'users', 150, { fill: p.tileFill || ORANGE_TINT, stroke: A.a === INDIGO ? INDIGO : ORANGE, ring: true, rot: -3, radius: .28 }, px);
    const card = `<div style="background:${CARD};background-image:radial-gradient(rgba(31,31,31,.09) ${px(2.4)},transparent ${px(2.8)});background-size:${px(22)} ${px(22)};border-radius:${px(36)};box-shadow:0 0 0 2px ${HAIR};padding:${px(54)} ${px(44)};display:flex;flex-direction:column;align-items:center;text-align:center;gap:${px(22)}"><div style="margin-bottom:${px(14)}">${tile}</div><div data-tag="dtitle" data-fitw="1" style="${FAM}font-size:${px(p.size || 76)};font-weight:800;letter-spacing:-.05em;color:${INK};line-height:1.04;max-width:100%">${esc(p.title)}</div>${p.sub ? `<div style="${GEIST}font-size:${px(40)};font-weight:400;color:${SECOND};line-height:1.3;max-width:90%">${esc(p.sub)}</div>` : ''}${p.button ? `<div data-bg="${A.a}" style="${GEIST}background:${A.a};color:${fgOn(A.a)};font-size:${px(42)};font-weight:700;padding:${px(26)} ${px(62)};border-radius:${px(26)};margin-top:${px(10)};white-space:nowrap">${esc(p.button)}</div>` : ''}</div>`;
    return { bg, html: `${p.heading ? mix(p.heading, { size: p.hsize || 84, fg: INK, pay: INK, plainW: 800 }) + '<div style="height:' + px(30) + '"></div>' : ''}${card}`, padR: 0 };
  },
  // dark panel: a sentence with highlighted pills (the home footer paragraph)
  pills(p, A) {
    const bg = PANEL;
    const runs = p.runs.map((r, ri) => { const t = typeof r === 'string' ? r : r.t; const lead = ri && !/^[?.,!:;)]/.test(t) ? ' ' : ''; return lead + (typeof r === 'string' ? esc(r) : `<span data-bg="${fillOf(r.fill || 'orange', A)}" style="display:inline-block;line-height:1.25;background:${fillOf(r.fill || 'orange', A)};color:${fgOn(fillOf(r.fill || 'orange', A))};font-weight:700;padding:${px(2)} ${px(20)} ${px(8)};border-radius:999px;margin:${px(8)} ${px(2)}">${esc(r.t)}</span>`); }).join('');
    const head = p.lines ? mix(p.lines, { size: p.size || 90, fg: '#FFFFFF', pay: '#FFFFFF', plainW: 700 }) : '';
    return { bg, html: `${p.eyebrow ? eyebrow(p.eyebrow, A.a, 32) : ''}${head}<div data-tag="para" style="${GEIST}font-size:${px(p.psize || 52)};font-weight:500;color:#F9F5F1;line-height:1.9;letter-spacing:-.015em;margin-top:${head ? px(34) : 0}">${runs}</div>${p.foot ? body(p.foot, '#A39A90', 38, 500, `margin-top:${px(30)}`) : ''}` };
  },
  // saturated slab with three icon rows (Tell us the subject / Compare real profiles / Message on WhatsApp)
  steps(p, A) {
    const bg = fillOf(p.fill || 'orange', A), fg = fgOn(bg);
    const rows = p.rows.map(r => `<div style="display:flex;gap:${px(30)};align-items:flex-start;margin-top:${px(34)}">${iconTile(r.icon || 'search', 104, { fill: 'rgba(31,31,31,.13)', stroke: fg, radius: .3 }, px)}<div><div style="${FAM}font-size:${px(58)};font-weight:800;letter-spacing:-.045em;color:${fg};line-height:1.05">${esc(r.t)}</div>${r.b ? `<div style="${GEIST}font-size:${px(40)};font-weight:500;color:${fg};opacity:.88;line-height:1.24;margin-top:${px(8)}">${esc(r.b)}</div>` : ''}</div></div>`).join('');
    return { bg, html: `${p.ordinal ? label(p.ordinal, fg === INK ? 'rgba(31,31,31,.6)' : 'rgba(255,255,255,.7)', 26) : ''}${mix(p.lines, { size: p.size || 100, fg, pay: fg, plainW: 800 })}${rows}${p.foot ? body(p.foot, fg, 42, 700, `margin-top:${px(40)}`) : ''}` };
  },
  // class tiles 1..12 on a bone card (the "by the class they are sitting" grid)
  grid(p, A) {
    const bg = fillOf(p.fill || 'card', A), n = p.tiles.length, cols = p.cols || (n > 8 ? 3 : 4);
    const tiles = p.tiles.map((t, i) => { const on = p.on === t || (Array.isArray(p.on) && p.on.includes(t)); const f = on ? A.a : MUTED; return `<div data-bg="${f}" style="${FAM}background:${f};color:${on ? fgOn(f) : INK};font-size:${px(68)};font-weight:800;letter-spacing:-.04em;border-radius:${px(30)};padding:${px(26)} 0;text-align:center;font-variant-numeric:tabular-nums">${esc(t)}</div>`; }).join('');
    return { bg, html: `${p.eyebrow ? eyebrow(p.eyebrow, A.a === ORANGE ? ORANGE_DEEP : A.deep) : ''}${mix(p.lines, { size: p.size || 88, fg: INK, pay: INK, plainW: 800 })}<div style="display:grid;grid-template-columns:repeat(${cols},1fr);gap:${px(18)};margin-top:${px(34)}">${tiles}</div>${p.foot ? body(p.foot, SECOND, 38, 500, `margin-top:${px(26)}`) : ''}` };
  },
  // the sentence builder: "I need a [+ subject] teacher for [+ class] near [+ area]" then a pill
  builder(p, A) {
    const bg = fillOf(p.fill || 'orange', A), fg = fgOn(bg);
    const t = (w, rot) => `<span data-bg="rgba(31,31,31,.14)" style="${FAM}display:inline-flex;align-items:center;gap:${px(14)};background:rgba(31,31,31,.14);color:${fg};font-weight:800;letter-spacing:-.04em;font-size:${px(88)};padding:${px(8)} ${px(30)} ${px(18)};border-radius:${px(28)};transform:rotate(${rot}deg);box-shadow:inset 0 0 0 ${px(3)} rgba(31,31,31,.12)"><span style="font-weight:400;font-size:.8em">+</span>${esc(w)}</span>`;
    const lines = p.lines.map(l => `<div style="${FAM}font-size:${px(88)};font-weight:800;letter-spacing:-.045em;color:${fg};line-height:1.35;display:flex;align-items:center;gap:${px(22)};white-space:nowrap;justify-content:center;margin-bottom:${px(30)}" data-fitw="1" data-nowrap="1">${l.map((x, i) => typeof x === 'string' ? `<span>${esc(x)}</span>` : t(x.t, x.rot ?? [-4, 3, -2][i % 3])).join('')}</div>`).join('');
    return { bg, html: `<div style="text-align:center">${p.title ? mix(p.title, { size: 96, fg, pay: fg, plainW: 800, align: 'center' }) + `<div style="height:${px(14)}"></div>` : ''}${p.sub ? body(p.sub, fg, 42, 500, `text-align:center;margin-bottom:${px(30)}`) : ''}${lines}<div style="margin-top:${px(44)};display:flex;justify-content:center">${pillBtn(p.button || 'Find them', 'rgba(249,245,241,.95)', INK, 46, false).replace('background:rgba', 'background:rgba')}</div></div>` };
  },
  // WhatsApp-style conversation with the site's blob avatars
  chat(p, A) {
    const bg = fillOf(p.fill || 'card', A);
    const av = (who) => `<svg viewBox="0 0 100 100" style="width:${px(104)};height:${px(104)};flex:none;display:block"><path d="M6 100 L6 54 C6 24 26 4 50 4 C74 4 94 24 94 54 L94 100 Z" fill="${who === 'S' ? ORANGE : '#9B4FC4'}"/><circle cx="38" cy="52" r="5" fill="${INK}"/><circle cx="62" cy="52" r="5" fill="${INK}"/><path d="${who === 'S' ? 'M34 61 Q50 79 66 61' : 'M37 63 Q50 76 63 63'}" stroke="${INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/></svg>`;
    const msgs = p.msgs.map(m => { const r = m.who === 'S', f = r ? A.a : '#FFFFFF'; return `<div style="display:flex;gap:${px(20)};align-items:flex-end;justify-content:${r ? 'flex-end' : 'flex-start'};flex-direction:${r ? 'row-reverse' : 'row'}">${av(m.who)}<div data-bg="${f}" style="${GEIST}max-width:76%;background:${f};color:${fgOn(f)};font-size:${px(p.fs || 46)};font-weight:500;line-height:1.2;letter-spacing:-.025em;padding:${px(26)} ${px(38)};border-radius:${px(46)} ${px(r ? 14 : 46)} ${px(r ? 46 : 14)} ${px(46)};box-shadow:0 0 0 ${px(2)} ${r ? 'transparent' : HAIR}">${esc(m.t)}</div></div>`; }).join('');
    return { bg, html: `<div style="display:flex;flex-direction:column;gap:${px(26)}">${msgs}</div>` };
  },
  // numbered index with a different colour per number (the Design Brief device)
  index(p, A) {
    const bg = fillOf(p.fill || 'card', A), cols = [ORANGE, INDIGO, MINT_DEEP, ORANGE_DEEP, INDIGO_DEEP];
    const rows = p.rows.map((r, i) => `<div style="display:flex;gap:${px(34)};align-items:flex-start;padding:${px(26)} 0;border-top:${i ? `${px(3)} solid ${HAIR}` : '0'}"><div style="${FAM}font-size:${px(104)};font-weight:900;letter-spacing:-.06em;color:${cols[i % cols.length]};line-height:.9;min-width:${px(150)};font-variant-numeric:tabular-nums">${esc(r.n || String(i + 1).padStart(2, '0'))}</div><div><div style="${FAM}font-size:${px(60)};font-weight:800;letter-spacing:-.045em;color:${INK};line-height:1.08">${esc(r.t)}</div>${r.b ? `<div style="${GEIST}font-size:${px(40)};font-weight:500;color:${SECOND};line-height:1.22;margin-top:${px(8)}">${esc(r.b)}</div>` : ''}</div></div>`).join('');
    return { bg, html: `${p.eyebrow ? eyebrow(p.eyebrow, A.a === ORANGE ? ORANGE_DEEP : A.deep) : ''}${p.lines ? mix(p.lines, { size: p.size || 92, fg: INK, pay: A.a === ORANGE ? ORANGE : A.a === INDIGO ? INDIGO : MINT_DEEP }) : ''}<div style="margin-top:${px(20)}">${rows}</div>` };
  },
  // a huge answer on a saturated slab
  answer(p, A) {
    const bg = fillOf(p.fill || 'accent', A), fg = fgOn(bg), hl = bg === PANEL ? A.a : (bg === MINT_SOLID ? INK : fg === INK ? '#FFFFFF' : LEMON);
    return { bg, html: `${p.eyebrow ? label(p.eyebrow, fg === INK ? 'rgba(31,31,31,.62)' : 'rgba(255,255,255,.75)', 28) : ''}<div style="height:${px(14)}"></div>${mix(p.lines, { size: p.size || 150, fg, pay: hl, plainW: 800, lh: 1.06 })}${p.sub ? body(p.sub, fg, 50, 600, `margin-top:${px(34)};max-width:${p.mascot ? '62%' : '100%'}`) : ''}${p.mascot ? mas(p.mascot, Math.min(p.mascot.size || 300, 260), `right:${px(-90)};bottom:${px(-120)};z-index:1`) : ''}`, padR: p.mascot ? px(130) : 0 };
  },
  // a coupon-shaped call to action
  ticket(p, A) {
    const bg = fillOf(p.fill || 'bone', A), f = fillOf(p.tfill || 'accent', A);
    const mask = `-webkit-mask:radial-gradient(circle ${px(34)} at 0 50%,#0000 98%,#000) left/51% 100% no-repeat,radial-gradient(circle ${px(34)} at 100% 50%,#0000 98%,#000) right/51% 100% no-repeat;mask:radial-gradient(circle ${px(34)} at 0 50%,#0000 98%,#000) left/51% 100% no-repeat,radial-gradient(circle ${px(34)} at 100% 50%,#0000 98%,#000) right/51% 100% no-repeat`;
    return { bg, html: `<div style="position:relative;filter:drop-shadow(0 ${px(14)} ${px(22)} rgba(31,31,31,.22))"><div data-bg="${f}" style="background:${f};${mask};padding:${px(54)} ${px(90)};text-align:left"><div style="${GEIST}font-size:${px(30)};font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:${fgOn(f)};opacity:.7">${esc(p.kicker || 'Tap to start')}</div><div data-fitw="1" data-nowrap="1" style="${FAM}font-size:${px(p.size || 110)};font-weight:900;letter-spacing:-.06em;color:${fgOn(f)};line-height:1.02;margin-top:${px(10)};white-space:nowrap">${esc(p.title)}</div>${p.sub ? body(p.sub, fgOn(f), 42, 600, `margin-top:${px(14)};opacity:.92`) : ''}<div style="margin-top:${px(26)};border-top:${px(4)} dashed ${fgOn(f) === INK ? 'rgba(31,31,31,.35)' : 'rgba(255,255,255,.5)'};padding-top:${px(22)};${GEIST}font-size:${px(40)};font-weight:700;color:${fgOn(f)}">${esc(p.foot || 'shikshaq.in')}</div></div></div>` };
  },
  // bento tiles with oversized words
  bento(p, A) {
    const bg = fillOf(p.fill || 'bone', A);
    const tiles = p.tiles.map(t => { const f = fillOf(t.fill || 'card', A), fg = f === CARD || f === BONE || f === MUTED || f === PEACH || f === MINT || f === ORANGE_TINT || f === INDIGO_TINT ? INK : fgOn(f); const ring = (f === CARD || f === BONE) ? `box-shadow:0 0 0 ${px(2)} ${HAIR};` : ''; return `<div data-bg="${f}" style="background:${f};${ring}border-radius:${px(34)};padding:${px(34)};display:flex;flex-direction:column;justify-content:space-between;min-height:${px(t.h || 280)};position:relative">${t.icon ? iconTile(t.icon, 84, { fill: 'rgba(31,31,31,.1)', stroke: fg, radius: .3 }, px) : '<div></div>'}<div><div style="${GEIST}font-size:${px(30)};font-weight:600;color:${fg};opacity:.72;margin-bottom:${px(6)}">${esc(t.label || '')}</div><div data-fitw="1" data-nowrap="1" style="${FAM}font-size:${px(t.size || 108)};font-weight:900;letter-spacing:-.06em;color:${fg};line-height:1">${esc(t.big)}</div></div></div>`; }).join('');
    return { bg, html: `${p.lines ? mix(p.lines, { size: p.size || 84, fg: INK, pay: A.a === ORANGE ? ORANGE : INDIGO, plainW: 800 }) + `<div style="height:${px(26)}"></div>` : ''}<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:${px(20)}">${tiles}</div>` };
  },
  // a thin saturated band of repeating words
  marquee(p, A) {
    const bg = fillOf(p.fill || 'accent', A), fg = fgOn(bg);
    const t = Array.from({ length: 8 }, () => p.words.map(w => `<span>${esc(w)}</span><span style="opacity:.6;padding:0 ${px(26)}">+</span>`).join('')).join('');
    return { bg, thin: true, html: `<div data-deco="1" style="${FAM}white-space:nowrap;overflow:hidden;font-size:${px(54)};font-weight:900;letter-spacing:-.03em;color:${fg};text-transform:uppercase">${t}</div>` };
  },
  // centred, full-bleed, loud: the onboarding screen (circle face, giant type, a pill)
  loud(p, A) {
    const bg = fillOf(p.fill || 'accent', A), fg = fgOn(bg), pay = bg === ORANGE ? INK : bg === INDIGO ? '#FFFFFF' : INK;
    const m = p.mascot !== false ? `<div style="display:flex;justify-content:center;margin-bottom:${px(50)}">${mascot(p.mascot || { kind: 'smile' }, `position:relative;width:${px(p.msize || 460)};height:${px(p.msize || 460)}`, 'mas')}</div>` : '';
    return { bg, center: true, html: `${m}${mix(p.lines, { size: p.size || 150, fg, pay: fg, plainW: 800, align: 'center', lh: 1.0 })}${p.sub ? body(p.sub, fg, 52, 500, `text-align:center;margin:${px(34)} auto 0;max-width:92%;opacity:.92`) : ''}${p.button ? `<div style="margin-top:${px(54)};display:flex;justify-content:center">${pillBtn(p.button, BONE, INK, 56)}</div>` : ''}` };
  },
  // a review, quoted exactly (gated), on its subject's tint
  quote(p, A, ctx) {
    const bg = fillOf(p.fill || 'card', A);
    return { bg, html: `<div data-deco="1" style="${FAM}font-size:${px(210)};font-weight:900;color:${p.c || ORANGE};line-height:.75;margin-bottom:${px(-30)}">&ldquo;</div><div data-tag="quote" style="${GEIST}font-size:${px(p.size || 60)};font-weight:500;color:${INK};line-height:1.2;letter-spacing:-.03em;margin-top:${px(10)}">${esc(p.text)}</div><div style="display:flex;align-items:center;gap:${px(22)};margin-top:${px(36)}"><div style="${FAM}width:${px(84)};height:${px(84)};border-radius:999px;background:${p.c || ORANGE};color:${fgOn(p.c || ORANGE)};display:flex;align-items:center;justify-content:center;font-size:${px(44)};font-weight:900">${esc((p.who || '?')[0])}</div><div><div style="${GEIST}font-size:${px(40)};font-weight:700;color:${INK}">${esc(p.who || '')}</div><div style="${GEIST}font-size:${px(30)};font-weight:500;color:${SECOND}">${esc(p.what || '')}</div></div></div>` };
  },
  // a tutor card with a stripe-placeholder photo (gated)
  tutor(p, A) {
    const bg = fillOf(p.fill || 'card', A), c = p.c || ORANGE;
    const photo = p.photo ? `<img src="${p.photo}" style="width:100%;height:${px(420)};object-fit:cover;border-radius:${px(28)}">` : `<div style="height:${px(420)};border-radius:${px(28)};background:repeating-linear-gradient(45deg,${c}33 0 ${px(16)},${MUTED} ${px(16)} ${px(32)});display:flex;align-items:center;justify-content:center;${FAM}font-size:${px(230)};font-weight:900;color:${c};opacity:.8" data-deco="1">${esc((p.name || '?')[0])}</div>`;
    return { bg, html: `${photo}<div style="margin-top:${px(26)};display:flex;align-items:center;gap:${px(18)}">${chipEl(p.subject || 'Subject', c, fgOn(c), 34)}${chipEl('Checked and selected', MINT, MINT_DEEP, 30)}</div><div style="${FAM}font-size:${px(72)};font-weight:800;letter-spacing:-.05em;color:${INK};margin-top:${px(22)};line-height:1">${esc(p.name || '')}</div><div data-tag="quote" style="${GEIST}font-size:${px(44)};font-weight:500;color:${PROSE};line-height:1.22;margin-top:${px(16)}">${esc(p.quote || '')}</div>` };
  },
  // a week grid with taped notes (the Linkedist calendar, made ours)
  calendar(p, A) {
    const bg = fillOf(p.fill || 'card', A), rows = p.rows || 2;
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const head = days.map(d => `<div style="${GEIST}flex:1;text-align:center;font-size:${px(28)};font-weight:700;color:${SECOND}">${d}</div>`).join('');
    const pal = [ORANGE_TINT, INDIGO_TINT, MINT, PEACH, '#FFF3C2'], dots = [ORANGE, INDIGO, MINT_SOLID, '#EF8A4F', LEMON];
    const cells = Array.from({ length: rows * 7 }, () => `<div style="border-left:${px(2)} solid ${HAIR};border-top:${px(2)} solid ${HAIR}"></div>`).join('');
    const notes = (p.notes || []).map((n, i) => `<div data-bg="${pal[i % 5]}" style="${GEIST}position:absolute;left:${Math.min((n.col / 7) * 100 + 0.8, 100 - ((n.span || 2.4) / 7 * 100 - 1.6) - 1.5)}%;top:${(n.row / rows) * 100 + 7}%;width:${(n.span || 2.4) / 7 * 100 - 1.6}%;background:${pal[i % 5]};border-radius:${px(18)};padding:${px(18)} ${px(20)};font-size:${px(34)};font-weight:700;letter-spacing:-.02em;line-height:1.1;color:${INK};transform:rotate(${[-4, 3, -3, 5, -2][i % 5]}deg);box-shadow:0 0 0 ${px(3)} ${INK},${px(6)} ${px(7)} 0 ${INK};z-index:${3 + i}"><span style="position:absolute;left:50%;top:${px(-16)};width:${px(24)};height:${px(24)};margin-left:${px(-12)};border-radius:999px;background:${dots[i % 5]};box-shadow:0 0 0 ${px(3)} ${INK}"></span>${esc(n.t)}</div>`).join('');
    return { bg, html: `${p.lines ? mix(p.lines, { size: p.size || 90, fg: INK, pay: A.a === ORANGE ? ORANGE : INDIGO }) + `<div style="height:${px(26)}"></div>` : ''}<div style="background:${BONE};border-radius:${px(30)};box-shadow:0 0 0 ${px(2)} ${HAIR};padding:${px(20)} 0 0;position:relative"><div style="display:flex;border-bottom:${px(2)} solid ${HAIR};padding-bottom:${px(16)}">${head}</div><div style="position:relative;height:${px(rows * 250)}"><div style="position:absolute;inset:0;display:grid;grid-template-columns:repeat(7,1fr);grid-template-rows:repeat(${rows},1fr)">${cells}</div>${notes}</div></div>${p.foot ? label(p.foot, SECOND, 26).replace('<div ', `<div style="margin-top:${px(20)}" `).replace('style="margin-top', 'data-x style="margin-top') : ''}` };
  },
  // a post with pointed plates (subject, board, class): the wayfinding metaphor
  signpost(p, A) {
    const bg = fillOf(p.fill || 'bone', A), cols = [ORANGE, INDIGO, MINT_SOLID, LEMON, '#9F53C6', '#D74242'];
    const plates = p.plates.map((pl, i) => { const f = fillOf(pl.fill || cols[i % cols.length], A), left = pl.dir === 'left'; const path = left ? 'M8 2 L100 2 L100 98 L8 98 L0 50 Z' : 'M0 2 L92 2 L100 50 L92 98 L0 98 Z'; return `<div style="position:relative;width:${pl.w || 86}%;margin:${px(14)} ${left ? 'auto 0 0' : '0 0 auto'};margin-left:${left ? 'auto' : '0'};margin-right:${left ? '0' : 'auto'};transform:rotate(${pl.rot ?? (i % 2 ? 2 : -2)}deg)"><svg viewBox="0 0 100 100" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%;overflow:visible;filter:drop-shadow(${px(8)} ${px(9)} 0 ${INK})"><path d="${path}" fill="${f}" stroke="${INK}" stroke-width="${7}" vector-effect="non-scaling-stroke" stroke-linejoin="round"/></svg><div data-bg="${f}" style="${FAM}position:relative;background:${f};clip-path:polygon(${left ? '8% 2%,100% 2%,100% 98%,8% 98%,0 50%' : '0 2%,92% 2%,100% 50%,92% 98%,0 98%'});padding:${px(26)} ${px(left ? 68 : 36)} ${px(26)} ${px(left ? 36 : 36)};font-size:${px(pl.size || 72)};font-weight:900;letter-spacing:-.05em;color:${fgOn(f)};line-height:1.05;text-align:${left ? 'right' : 'left'}"><span data-fitw="1" data-nowrap="1" style="display:block;white-space:nowrap">${esc(pl.t)}</span></div></div>`; }).join('');
    return { bg, html: `${p.lines ? mix(p.lines, { size: p.size || 92, fg: INK, pay: A.a === ORANGE ? ORANGE : INDIGO }) + `<div style="height:${px(22)}"></div>` : ''}${plates}${p.sub ? body(p.sub, PROSE, 42, 500, `margin-top:${px(26)}`) : ''}` };
  },
  // a row of pill chips (Class 10 / Maths / Home tuition) and an optional search pill
  search(p, A) {
    const bg = fillOf(p.fill || 'card', A);
    const toggle = `<div style="display:inline-flex;background:${MUTED};border-radius:999px;padding:${px(8)};box-shadow:inset 0 0 0 ${px(2)} ${HAIR}">${(p.toggle || ['Teachers', 'Past papers']).map((t, i) => `<span data-bg="${i ? MUTED : PANEL}" style="${GEIST}background:${i ? 'transparent' : PANEL};color:${i ? SECOND : '#fff'};font-size:${px(38)};font-weight:700;padding:${px(18)} ${px(40)};border-radius:999px">${esc(t)}</span>`).join('')}</div>`;
    const bar = `<div style="background:${MUTED};border-radius:999px;padding:${px(14)} ${px(14)} ${px(14)} ${px(44)};display:flex;align-items:center;gap:${px(22)};margin-top:${px(26)}">${icon('search', px(52), SECOND, 2.2)}<span data-fitw="1" data-nowrap="1" style="${GEIST}flex:1;min-width:0;overflow:hidden;font-size:${px(44)};font-weight:500;color:${SECOND};white-space:nowrap">${esc(p.query || 'Subject, class, area')}</span><span data-bg="${ORANGE}" style="${GEIST}background:${ORANGE};color:${INK};font-size:${px(44)};font-weight:800;padding:${px(28)} ${px(46)};border-radius:999px;display:inline-flex;gap:${px(14)};align-items:center">${icon('arrow', px(44), INK, 2.8)}Search</span></div>`;
    const chips = `<div style="display:flex;gap:${px(18)};flex-wrap:wrap;margin-top:${px(26)}">${(p.chips || []).map(c => chipEl(c, MUTED, INK, 40)).join('')}</div>`;
    return { bg, html: `${p.lines ? mix(p.lines, { size: p.size || 92, fg: INK, pay: ORANGE }) + `<div style="height:${px(24)}"></div>` : ''}${p.toggle !== false ? toggle : ''}${bar}${chips}` };
  },
  // a plain call-to-action panel (orange slab, a bone pill, a character)
  cta(p, A) {
    const bg = fillOf(p.fill || 'accent', A), fg = fgOn(bg);
    return { bg, html: `${p.lines ? mix(p.lines, { size: p.size || 104, fg, pay: fg, plainW: 800 }) : ''}${p.sub ? body(p.sub, fg, 46, 500, `margin-top:${px(24)};max-width:${p.mascot ? '66%' : '100%'}`) : ''}<div style="margin-top:${px(40)}">${pillBtn(p.button || 'Find your tutor', BONE, INK, 50)}</div>${p.mascot ? mas(p.mascot, Math.min(p.mascot.size || 300, 300), `right:${px(-80)};bottom:${px(-150)};z-index:1`) : ''}` };
  },
  // a wrap of big pill chips (the filter chips: Class 10, Maths, Home tuition)
  chips(p, A) {
    const bg = fillOf(p.fill || 'card', A), tints = [ORANGE_TINT, INDIGO_TINT, MINT, PEACH, MUTED];
    const chips = p.chips.map((c, i) => chipEl(c, p.solid ? [ORANGE, INDIGO, MINT_SOLID, LEMON, '#9F53C6'][i % 5] : tints[i % 5], p.solid ? fgOn([ORANGE, INDIGO, MINT_SOLID, LEMON, '#9F53C6'][i % 5]) : INK, p.csize || 46)).join('');
    return { bg, html: `${p.eyebrow ? eyebrow(p.eyebrow, A.a === ORANGE ? ORANGE_DEEP : A.deep) : ''}${p.lines ? mix(p.lines, { size: p.size || 92, fg: INK, pay: A.a === ORANGE ? ORANGE : A.a === INDIGO ? INDIGO : MINT_DEEP }) : ''}<div style="display:flex;flex-wrap:wrap;gap:${px(18)};margin-top:${px(30)}">${chips}</div>${p.foot ? body(p.foot, SECOND, 40, 500, `margin-top:${px(26)}`) : ''}` };
  },
  // an empty dotted card: the room a native poll or question sticker will sit in
  zone(p, A) {
    const bg = fillOf(p.fill || 'bone', A);
    return { bg, html: `${p.lines ? mix(p.lines, { size: p.size || 110, fg: INK, pay: A.a === ORANGE ? ORANGE : A.a === INDIGO ? INDIGO : MINT_DEEP }) + `<div style="height:${px(36)}"></div>` : ''}<div style="background:${CARD};background-image:radial-gradient(rgba(31,31,31,.1) ${px(2.4)},transparent ${px(2.8)});background-size:${px(22)} ${px(22)};border-radius:${px(40)};box-shadow:0 0 0 2px ${HAIR};height:${px(p.h || 520)};display:flex;align-items:center;justify-content:center">${p.icon ? iconTile(p.icon, 150, { fill: p.tileFill || ORANGE_TINT, stroke: A.a === INDIGO ? INDIGO : ORANGE, ring: true, rot: -3, radius: .28 }, px) : ''}</div>` };
  },
  // a message to copy: the drafted bubble, big, with a "copy this" tag
  copy(p, A) {
    const bg = fillOf(p.fill || 'tint', A), f = A.a;
    return { bg, html: `<div style="display:flex;align-items:center;justify-content:space-between;gap:${px(20)};margin-bottom:${px(30)}">${p.eyebrow ? eyebrow(p.eyebrow, A.a === ORANGE ? ORANGE_DEEP : A.deep) : '<span></span>'}<div style="transform:rotate(4deg);flex:none">${chipEl('Copy this', INK, '#fff', 34)}</div></div><div data-bg="${f}" style="background:${f};color:${fgOn(f)};border-radius:${px(44)} ${px(14)} ${px(44)} ${px(44)};padding:${px(46)} ${px(50)};${GEIST}font-size:${px(p.size || 58)};font-weight:600;line-height:1.24;letter-spacing:-.025em;margin-left:${px(60)};box-shadow:${px(8)} ${px(10)} 0 ${INK},0 0 0 ${px(3)} ${INK}" data-tag="draft">${esc(p.text)}</div>${p.foot ? body(p.foot, bg === PANEL ? '#CFC7BD' : SECOND, 40, 500, `margin-top:${px(40)}`) : ''}` };
  },
};

// the site's Sticker: a tilted pill that overhangs the top-right of a block, sentence case, one per panel
function stickerEl(st, first, S) {
  if (!st) return '';
  const tone = { dark: [PANEL, '#FFFFFF'], brand: [ORANGE, INK], papers: [INDIGO, '#FFFFFF'], bone: [CARD, INK], lemon: [LEMON, INK], mint: [MINT_SOLID, INK] }[st.tone || 'dark'];
  return `<div data-bg="${tone[0]}" style="${GEIST}position:absolute;right:${px(54)};${first ? `bottom:${px(26)}` : `top:${px(st.top ?? 24)}`};z-index:5;background:${tone[0]};color:${tone[1]};font-size:${px(st.size || 32)};font-weight:800;letter-spacing:.01em;padding:${px(14)} ${px(30)};border-radius:999px;transform:rotate(${st.rot ?? 5}deg);box-shadow:0 0 0 ${px(2)} ${INK},0 ${px(6)} ${px(12)} rgba(31,31,31,.2);white-space:nowrap">${esc(st.t)}</div>`;
}

// ---- the engine ----------------------------------------------------------------------------------------------------------------------
export function stackLook(spec, L, F) {
  const A = ACC[spec.accent || 'orange'] || ACC.orange, S = L.story, n = spec.panels.length;
  const scale = S ? 1 : (L.Q ? .74 : .82), R = 40;
  const built = spec.panels.map(p => ({ p, ...TYPES[p.type](p, A, {}) }));
  const topPad = S ? 262 + 72 + 36 : 44 + 60 + 30, botPad = S ? 340 + 100 : 48 + 60;
  const panels = built.map((b, i) => {
    const first = i === 0, last = i === n - 1, thin = b.thin;
    const r = `${first ? 0 : R}px ${first ? 0 : R}px ${last ? 0 : R}px ${last ? 0 : R}px`;
    const pt = first ? `${topPad}px` : (thin ? px(14) : px(54)), pb = last ? `${botPad}px` : (thin ? px(14) : px(54));
    const grow = b.p.grow ?? (thin ? 0 : 1);
    return `<section class="pn" data-bg="${b.bg}" style="background:${b.bg};border-radius:${r};padding:${pt} 56px ${pb} 56px;padding-right:calc(56px + ${b.padR || '0px'});flex:${grow} 1 auto;display:flex;flex-direction:column;justify-content:${b.p.valign || 'center'};position:relative;overflow:hidden;color:${fgOn(b.bg)}">${b.html}${stickerEl(b.p.sticker, first, S)}</section>`;
  }).join('');
  const css = `<style>.stack{position:absolute;left:0;top:0;width:${L.W}px;height:${L.H}px;display:flex;flex-direction:column;background:${BONE};--s:${scale};--u:1;--k:calc(var(--u) * var(--s));overflow:hidden}.pn{min-height:min-content}.pn>*{position:relative;z-index:2}.pn>svg.a,.pn>div:has(>svg.a){z-index:1}</style>`;
  // the fit: the largest unit at which nothing overflows, then shrink any single line that is still too wide
  const js = `<script>(function(){function run(){var st=document.querySelector('.stack');if(!st)return;var H=st.clientHeight;function ok(){if(st.scrollHeight>H+1)return false;return true}var lo=.4,hi=1.7;for(var i=0;i<16;i++){var m=(lo+hi)/2;st.style.setProperty('--u',m);if(ok())lo=m;else hi=m}st.style.setProperty('--u',lo);document.querySelectorAll('[data-fitw]').forEach(function(e){var s=parseFloat(getComputedStyle(e).fontSize),g=0;while(e.scrollWidth>e.clientWidth+1&&g++<40){s*=.97;e.style.fontSize=s+'px'}});document.body.setAttribute('data-ready','1')}document.fonts.ready.then(function(){requestAnimationFrame(run)})})();</script>`;
  // chrome over the stack: logo pill (always), handle, counter, label
  const lh = S ? 72 : 60, lw = Math.round(lh * 252 / 92), ly = S ? 262 : 44, py = 16;
  const lastFg = fgOn(built[n - 1].bg), hy = L.H - (S ? 340 : 0) - (S ? 72 : 66);
  const logo = `<div class="a" data-tag="logopill" style="left:56px;top:${ly}px;width:${lw + 52}px;height:${lh + 2 * py}px;background:${BONE};border-radius:999px;z-index:30;box-shadow:0 0 0 3px ${INK}"></div><img class="a" data-tag="logo" src="${LOGO}" style="left:${56 + 26}px;top:${ly + py}px;height:${lh}px;width:auto;z-index:31">`;
  const handle = spec.handle === false ? '' : `<div class="a" data-tag="handle" data-bg="${built[n - 1].bg}" style="left:56px;top:${hy}px;font:700 30px/1 Geist,sans-serif;letter-spacing:.05em;text-transform:uppercase;color:${lastFg};opacity:.8;z-index:30">shikshaq.in</div>`;
  const count = '';
  const tagText = spec.tag || spec.count;
  const tag = tagText ? `<div class="a" data-tag="eyebrow" data-bg="${BONE}" style="right:56px;top:${ly + (S ? 18 : 10)}px;z-index:30;background:${BONE};color:${INK};font:700 ${S ? 32 : 28}px/1 Geist,sans-serif;padding:${S ? 20 : 16}px ${S ? 30 : 24}px;border-radius:999px;box-shadow:0 0 0 3px ${INK}">${esc(tagText)}</div>` : '';
  // the unsafe bands (story header and reply bar) carry art instead of copy: a character peeks in from the top and rises from the bottom
  let decor = '';
  if (S && spec.decor !== false && built[0].p.type !== 'loud') {
    const topK = { orange: { kind: 'eyes' }, indigo: { kind: 'sleep' }, mint: { kind: 'arch', mood: 'good' } }[spec.accent || 'orange'];
    decor += mascot(topK, `position:absolute;left:${(L.W - 400) / 2 + 40}px;top:-150px;width:400px;height:400px;z-index:25;transform:rotate(8deg)`, 'decor');
    const lb = built[n - 1].bg, bm = lb === PANEL ? { kind: 'eyes' } : (lb === ORANGE ? { kind: 'smile' } : lb === INDIGO ? { kind: 'sun' } : lb === MINT_SOLID ? { kind: 'smile' } : { kind: 'eyes' });
    decor += mascot(bm, `position:absolute;left:-150px;top:${L.H - 330}px;width:500px;height:500px;z-index:25;transform:rotate(-8deg)`, 'decor');
  }
  return `${css}<div class="stack">${panels}</div>${decor}${logo}${handle}${count}${tag}${js}`;
}
export { TYPES };
