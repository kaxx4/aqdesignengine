// Looks, part two: bands (V3), brief (V4), card (V5), swarm (V2), chat (V7), calendar (V1), review (V8), tutor (V5).
import { C, textOn, subjectPalette } from '../src/tokens.mjs';
import { box, card, chip, esc, glow } from '../src/kit.mjs';
import { eyes } from './characters.mjs';
import { arch, archInline, lift, sun, lobe, torn, badge, MOOD_FILL } from './characters.mjs';
import { txt, chrome, ctaPill, headBlock, isDark, hs } from './looks-core.mjs';

const D = `font-family:Archivo,Geist,sans-serif;font-stretch:104%;`;
const LEMON = '#FFC700';

// ---- LOOK: bands (V3). Three full-bleed bands with torn seams: question on dark, answer on bone, origin on accent. --
export function bands(spec, L, F) {
  const S = L.story, a = F.a;
  const b1 = L.y0 + (S ? 500 : 380), b3 = L.y1 - (S ? 330 : 250);
  const qSize = S ? 96 : 78;
  const band1 = box('band1', 0, 0, L.W, b1, `background:${C.panel}`,
    txt('q', L.pad, b1 - (S ? 400 : 290), L.cw, S ? 340 : 240, spec.qHtml || esc(spec.q), { size: qSize, weight: 800, color: '#FFFFFF', ls: '-.055em', lh: 1, fit: 40, grow: qSize + 20, bg: C.panel, extra: D + 'display:flex;align-items:flex-end;' }));
  const kick = spec.kicker ? `<div class="a" data-tag="kicker" style="left:${L.pad + 260}px;top:${L.y0 + 8}px;z-index:20">${chip(spec.kicker, '#2A2926', { size: 24, color: '#fff' })}</div>` : '';
  const seam1 = torn('seam1', 0, b1 - 2, L.W, C.panel, 3, 52);
  const ansTop = b1 + 80, ansH = b3 - ansTop - 70;
  const ans = txt('answer', L.pad, ansTop, L.cw, ansH, spec.aHtml || esc(spec.a), { size: S ? 100 : 80, weight: 800, color: C.ink, ls: '-.055em', lh: .98, fit: 38, grow: S ? 130 : 104, extra: D + 'display:flex;align-items:center;' });
  const seam3 = torn('seam3', 0, b3 - 50, L.W, a, 7, 52, false);
  const band3 = box('band3', 0, b3, L.W, L.H - b3, `background:${a}`,
    txt('foot', L.pad, 34, spec.mascot ? L.cw - (S ? 230 : 170) : L.cw, S ? 170 : 130, esc(spec.foot || ''), { size: S ? 50 : 40, weight: 700, color: textOn(a), ls: '-.04em', lh: 1.1, fit: 24, bg: a }));
  const m = spec.mascot ? sun('mas', L.W - L.pad - (S ? 190 : 140), b3 + 28, S ? 190 : 140, LEMON, 8) : '';
  return [band1, seam1, ans, seam3, band3, chrome({ ...spec, ground: 'panel', tag: null, count: null, handle: false }, L, F, { handle: false }), kick,
    `<div class="a lab" data-tag="handle" data-bg="${a}" style="left:${L.pad}px;top:${L.y1 - 26}px;color:${textOn(a)};font-size:24px;z-index:20">shikshaq.in</div>`,
    spec.count ? `<div class="a lab" data-tag="count" data-bg="${a}" style="left:${L.W - L.pad - 140}px;top:${L.y1 - 26}px;width:140px;text-align:right;color:${textOn(a)};font-size:24px;z-index:20">${esc(spec.count)}</div>` : '', m].join('');
}

// ---- LOOK: brief (V4). A document sheet: title, rule, numbered rows with highlighter marks, a tilted note. -----------
export function brief(spec, L, F) {
  const S = L.story, a = F.a, dark = isDark(spec);
  const sheetTop = L.y0 + (S ? 110 : 96), sheetH = L.y1 - 130 - sheetTop;
  const tint = spec.hl || F.tint;
  const hl = t => `<span style="background:linear-gradient(transparent 52%,${tint} 52%);padding:0 .08em;font-weight:700">${esc(t)}</span>`;
  const row = (r, i) => `<div style="display:flex;gap:30px;align-items:flex-start"><div class="d" data-tag="n${i}" style="font-size:${S ? 64 : 52}px;color:${F.deep};min-width:${S ? 108 : 88}px;line-height:1">${esc(r.n || String(i + 1).padStart(2, '0'))}</div><div data-fit="22" style="font-size:${S ? 56 : 46}px;font-weight:500;line-height:1.14;letter-spacing:-.035em;color:${C.ink};flex:1">${r.pre ? esc(r.pre) + ' ' : ''}${r.hl ? hl(r.hl) : ''}${r.post ? ' ' + esc(r.post) : ''}</div></div>`;
  const head = `<div class="d" data-tag="title" data-fit="40" style="font-size:${S ? 104 : 84}px;color:${C.ink};line-height:.98;letter-spacing:-.055em;margin-bottom:${S ? 40 : 26}px">${esc(spec.title)}</div><div style="height:4px;background:${C.ink};margin-bottom:${S ? 56 : 38}px"></div>`;
  const sheet = card('sheet', L.pad, sheetTop, L.cw, sheetH, C.card, { r: 28, shadow: `0 0 0 3px ${C.ink},10px 12px 0 ${dark ? '#000' : C.ink}`, pad: S ? 56 : 44,
    inner: `<div style="position:absolute;left:-14px;top:120px;width:28px;height:28px;border-radius:999px;background:${dark ? C.panel : C.page}"></div><div style="position:absolute;left:-14px;top:${sheetH / 2}px;width:28px;height:28px;border-radius:999px;background:${dark ? C.panel : C.page}"></div><div style="display:flex;flex-direction:column;height:${sheetH - (S ? 112 : 88)}px">${head}<div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly">${spec.rows.map(row).join('')}</div></div>` });
  const note = spec.note ? `<div class="a" data-tag="note" style="right:${L.pad}px;top:${sheetTop - (S ? 54 : 46)}px;transform:rotate(5deg);z-index:12">${chip(spec.note, LEMON, { size: S ? 38 : 32, color: C.ink })}</div>` : '';
  return [chrome(spec, L, F), sheet, note, spec.cta ? ctaPill(L, L.y1 - (S ? 120 : 98), spec.cta, dark ? a : C.panel, { dot: dark ? C.panel : a, h: S ? 100 : 84 }) : ''].join('');
}

// ---- LOOK: card (V5). A big business-card tile in four colourways, same layout. ----------------------------------
export function cardLook(spec, L, F) {
  const S = L.story, Q = L.canvas === 'Q';
  const scheme = { bone: { bg: C.card, fg: C.indigoDeep, sub: C.prose, ring: true }, indigo: { bg: C.indigo, fg: '#FFFFFF', sub: '#FFFFFF' }, orange: { bg: C.orange, fg: C.ink, sub: '#2B1700' }, ink: { bg: C.panel, fg: '#F9F5F1', sub: '#CFC7BD' } }[spec.scheme || 'indigo'];
  const top = L.y0 + (S ? 110 : (Q ? 90 : 100)), h = L.y1 - 100 - top;
  const lines = spec.lines.map(l => `<div style="white-space:nowrap">${esc(l)}</div>`).join('');
  const inner =
    txt('ctop', 56, 56, L.cw - 112 - (S ? 230 : (Q ? 160 : 190)), S ? 150 : 110, esc(spec.small || ''), { size: S ? 38 : 30, weight: 800, color: scheme.fg, ls: '-.02em', lh: 1.1, fit: 18, bg: scheme.bg, extra: 'text-transform:uppercase;' + D })
    + `<div class="a" data-tag="cbig" data-fit="40" data-bg="${scheme.bg}" style="left:56px;top:${S ? 240 : 170}px;width:${L.cw - 112}px;font-size:${S ? 230 : (Q ? 130 : (spec.lines.length <= 3 ? 190 : 150))}px;font-weight:800;color:${scheme.fg};line-height:.92;letter-spacing:-.06em;${D}">${lines}</div>`
    + txt('cfoot', 56, h - (S ? 110 : 90), 420, S ? 70 : 56, esc(spec.foot || ''), { size: S ? 40 : 32, weight: 500, color: scheme.sub, ls: '-.02em', lh: 1.1, fit: 18, bg: scheme.bg });
  const sz = S ? 190 : (Q ? 120 : 118), star = spec.star === false ? '' : (spec.scheme === 'orange' ? lobe('mas', L.cw - 56 - sz, 30, sz, C.ink, 0) : sun('mas', L.cw - 56 - sz, 30, sz, scheme.fg === C.indigoDeep ? C.indigo : LEMON, 10));
  const tile = box('tile', L.pad, top, L.cw, h, `background:${scheme.bg};border-radius:32px;overflow:hidden;box-shadow:${scheme.ring ? `0 0 0 2px ${C.hairline},` : ''}${glow(scheme.bg === C.card ? C.indigo : scheme.bg)};transform:rotate(${spec.rot ?? 0}deg)`, inner + lift(star));
  return [chrome(spec, L, F, { logo: spec.logo !== false }), tile].join('');
}

// ---- LOOK: swarm (V2). Die-cut word stickers around one giant headline on a dark ground. ------------------------
export function swarm(spec, L, F) {
  const S = L.story, Q = L.canvas === 'Q';
  const fills = [F.a, C.indigo, C.mintSolid, LEMON, '#F9F5F1', C.peach, C.orange];
  const shapes = [999, 26, 999, 14, 40, 999, 20];
  const stick = (w, i) => `<span data-bg="${fills[i % fills.length]}" style="display:inline-block;background:${fills[i % fills.length]};color:${textOn(fills[i % fills.length])};font-size:${S ? 54 : 44}px;font-weight:800;letter-spacing:-.04em;padding:.28em .7em;border-radius:${shapes[i % shapes.length]}px;transform:rotate(${[-7, 5, -3, 8, -5, 4, -9][i % 7]}deg);box-shadow:0 0 0 7px #F9F5F1,6px 8px 0 7px ${C.ink};margin:20px 22px;white-space:nowrap;${D}">${esc(w)}</span>`;
  const words = spec.words, half = Math.ceil(words.length / 2);
  const row = (ws, off) => `<div style="display:flex;flex-wrap:wrap;justify-content:center;align-items:center;width:${L.cw + 40}px">${ws.map((w, i) => stick(w, i + off)).join('')}</div>`;
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, S ? 180 : (Q ? 120 : 148), true, { align: 'center', flow: true });
  const top = L.y0 + 100, bot = L.y1 - 40;
  return [chrome({ ...spec, ground: 'panel' }, L, F),
    `<div class="a" data-tag="region" style="left:${L.pad - 20}px;top:${top}px;width:${L.cw + 40}px;height:${bot - top}px;display:flex;flex-direction:column;justify-content:space-evenly;align-items:center">${spec.q ? `<div data-tag="q" style="align-self:flex-start;margin-left:20px">${chip(spec.q, '#F9F5F1', { size: S ? 40 : 34, color: C.ink })}</div>` : ''}${row(words.slice(0, half), 0)}<div style="width:${L.cw}px">${head}</div>${row(words.slice(half), half)}</div>`].join('');
}

// ---- LOOK: chat (V7). A conversation as rounded pills with avatar chips. -----------------------------------------
export function chat(spec, L, F) {
  const S = L.story, a = F.a, dark = isDark(spec);
  const fsz = S ? 54 : 46, av = S ? 112 : 96;
  const names = spec.names || { S: 'Me', P: 'Ma' };
  const avatar = who => archInline(av, who === 'S' ? 'great' : 'fine');
  const bubble = m => {
    const right = m.who === 'S', fill = right ? a : '#FFFFFF', fg = right ? textOn(a) : C.ink;
    return `<div style="display:flex;gap:22px;align-items:flex-end;justify-content:${right ? 'flex-end' : 'flex-start'};flex-direction:${right ? 'row-reverse' : 'row'}">${avatar(m.who)}<div data-bg="${fill}" style="max-width:${L.cw - av - 90}px;background:${fill};color:${fg};font-size:${fsz}px;font-weight:500;line-height:1.16;letter-spacing:-.03em;padding:${S ? 34 : 28}px ${S ? 46 : 38}px;border-radius:${S ? 52 : 44}px ${right ? 16 : (S ? 52 : 44)}px ${right ? (S ? 52 : 44) : 16}px ${S ? 52 : 44}px;box-shadow:0 0 0 2px ${right ? 'transparent' : C.hairline}">${esc(m.t)}</div></div>`;
  };
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, S ? 104 : 88, dark, { flow: true, min: 40 });
  const top = L.y0 + 100, bot = L.y1 - (spec.cta ? (S ? 150 : 120) : 50);
  return [chrome(spec, L, F),
    `<div class="a" data-tag="region" style="left:${L.pad}px;top:${top}px;width:${L.cw}px;height:${bot - top}px;display:flex;flex-direction:column;justify-content:space-between"><div>${head}</div><div style="display:flex;flex-direction:column;gap:${S ? 34 : 24}px">${spec.msgs.map(bubble).join('')}</div></div>`,
    spec.cta ? ctaPill(L, L.y1 - (S ? 140 : 108), spec.cta, C.panel, { dot: a, h: S ? 108 : 88 }) : ''].join('');
}

// ---- LOOK: calendar (V1). A week/month grid with tilted note cards and pins. ------------------------------------
export function calendar(spec, L, F) {
  const S = L.story, a = F.a;
  const gTop = L.y0 + (S ? 420 : 330);
  const head = headBlock('headline', L.pad, 0, L.cw, spec.lines, F, hs(S ? 120 : 100, gTop - L.y0 - 140, spec.lines.length), false, { flow: true, min: 44 });
  const gH = L.y1 - 150 - gTop, rows = spec.rows || (S ? 3 : 2), cols = 7;
  const cw = (L.cw - 2) / cols, hdr = 70, rh = (gH - hdr) / rows;
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  let cells = `<div style="position:absolute;left:0;top:0;width:100%;height:${hdr}px;display:flex;border-bottom:2px solid ${C.hairline}">${days.map(d => `<div style="flex:1;display:flex;align-items:center;justify-content:center;font-size:${S ? 28 : 26}px;font-weight:700;color:${C.secondary};letter-spacing:.02em" data-tag="day">${d}</div>`).join('')}</div>`;
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) cells += `<div style="position:absolute;left:${c * cw}px;top:${hdr + r * rh}px;width:${cw}px;height:${rh}px;border-left:${c ? 2 : 0}px solid ${C.hairline};border-top:${r ? 2 : 0}px solid ${C.hairline}"></div>`;
  const pal = [C.orangeTint, C.indigoTint, C.mint, C.peach, '#FFF3C2'];
  const solid = [C.orange, C.indigo, C.mintSolid, '#EF8A4F', LEMON];
  const notes = (spec.notes || []).map((n, i) => {
    const nw = Math.min(cw * (n.span || 2.6), L.cw - 40), nx = Math.max(10, Math.min(L.cw - nw - 10, n.col * cw + 8)), ny = hdr + n.row * rh + rh * .12;
    return `<div class="a" data-tag="note${i}" data-bg="${pal[i % 5]}" style="left:${nx}px;top:${ny}px;width:${nw}px;padding:${S ? 22 : 16}px ${S ? 24 : 18}px;background:${pal[i % 5]};border-radius:18px;transform:rotate(${[-5, 4, -3, 6, -4][i % 5]}deg);box-shadow:0 0 0 2px ${C.ink},5px 6px 0 ${C.ink};font-size:${S ? 46 : 32}px;font-weight:700;line-height:1.1;letter-spacing:-.03em;color:${C.ink};z-index:${4 + i}"><span style="position:absolute;left:50%;top:-16px;width:24px;height:24px;border-radius:999px;background:${solid[i % 5]};box-shadow:0 0 0 3px ${C.ink};margin-left:-12px"></span>${esc(n.t)}</div>`;
  }).join('');
  const grid = card('grid', L.pad, gTop, L.cw, gH, C.card, { r: 28, ring: true, inner: cells + notes });
  const label = `<div class="a lab" data-tag="eg" style="left:${L.pad}px;top:${gTop + gH + 22}px;color:${C.secondary};font-size:24px">${esc(spec.label || 'An example week')}</div>`;
  return [chrome(spec, L, F),
    `<div class="a" data-tag="region" style="left:${L.pad}px;top:${L.y0 + 100}px;width:${L.cw}px;height:${gTop - L.y0 - 130}px;display:flex;flex-direction:column;justify-content:center">${head}</div>`,
    grid, label, spec.cta ? ctaPill(L, L.y1 - (S ? 120 : 96), spec.cta, C.panel, { x: L.W - L.pad - 520, w: 520, dot: a, h: S ? 100 : 80 }) : ''].join('');
}

// ---- LOOK: review (V8). One REAL review, quoted exactly, on its subject's tint. ---------------------------------
export function review(spec, L, F) {
  const S = L.story, r = spec.review, pal = subjectPalette(r.subject);
  const top = L.y0 + (S ? 130 : 110), h = L.y1 - 150 - top;
  const ghost = i => `<div style="position:absolute;left:${i ? 90 : 0}px;right:${i ? 0 : 90}px;top:${i ? h - 240 : -70}px;height:150px;border-radius:999px;background:${C.card};box-shadow:0 0 0 2px ${C.hairline};display:flex;align-items:center;padding:0 34px;gap:22px">${archInline(86, i ? 'good' : 'fine')}<div style="flex:1"><div style="height:22px;width:${i ? 60 : 72}%;border-radius:999px;background:${C.hairline}"></div></div></div>`;
  const cardIn =
    `<div class="d" data-deco="1" style="position:absolute;left:34px;top:-26px;font-size:${S ? 300 : 240}px;color:${pal.solid};opacity:.9;line-height:1">&ldquo;</div>`
    + txt('quote', 56, S ? 250 : 200, L.cw - 112, h - 180 - (S ? 250 : 200) - (S ? 150 : 130) - 20, esc(r.text), { size: S ? 62 : 52, weight: 500, color: pal.text, ls: '-.035em', lh: 1.14, fit: 26, grow: S ? 76 : 64, bg: pal.tint })
    + `<div style="position:absolute;left:56px;bottom:56px;display:flex;align-items:center;gap:22px"><div class="d" data-tag="ini" data-bg="${pal.solid}" style="width:84px;height:84px;border-radius:999px;background:${pal.solid};color:${textOn(pal.solid)};display:flex;align-items:center;justify-content:center;font-size:44px">${esc((r.first || '?')[0])}</div><div><div data-tag="who" data-bg="${pal.tint}" style="font-size:${S ? 40 : 34}px;font-weight:700;color:${pal.text};letter-spacing:-.03em">${esc(r.first || '')}</div><div data-tag="whatsub" data-bg="${pal.tint}" style="font-size:${S ? 30 : 26}px;font-weight:500;color:${pal.meta};letter-spacing:-.02em">${esc([r.subject, r.cls].filter(Boolean).join(' · '))}</div></div></div>`;
  return [chrome(spec, L, F),
    `<div class="a" data-tag="wall" style="left:${L.pad}px;top:${top}px;width:${L.cw}px;height:${h}px">${ghost(0)}${ghost(1)}</div>`,
    card('rcard', L.pad + 20, top + 90, L.cw - 40, h - 180, pal.tint, { r: 32, shadow: `0 0 0 2px ${C.hairline},${glow(pal.solid)}`, inner: cardIn }),
    `<div class="a" data-tag="stk" style="left:${L.W - L.pad - 330}px;top:${top + 56}px;transform:rotate(5deg);z-index:12">${chip(spec.sticker || 'A real review', C.panel, { size: S ? 34 : 28, color: '#fff' })}</div>`,
    spec.cta ? ctaPill(L, L.y1 - (S ? 130 : 100), spec.cta, C.panel, { dot: F.a, h: S ? 100 : 84 }) : ''].join('');
}

// ---- LOOK: tutor (V5). Meet a tutor: photo (or the site's stripe placeholder), name, subject, one quote. ------------
export function tutor(spec, L, F) {
  const S = L.story, t = spec.tutor, pal = subjectPalette(t.subject);
  const top = L.y0 + (S ? 120 : 100), h = L.y1 - 140 - top, ph = S ? 520 : 380;
  const photo = t.photo
    ? `<img data-tag="photo" src="${t.photo}" style="position:absolute;left:0;top:0;width:100%;height:${ph}px;object-fit:cover;border-radius:32px 32px 0 0">`
    : `<div style="position:absolute;left:0;top:0;width:100%;height:${ph}px;background:repeating-linear-gradient(45deg,${pal.solid}33 0 16px,${pal.tint} 16px 32px)"></div><div class="d" data-deco="1" style="position:absolute;left:0;top:0;width:100%;height:${ph}px;display:flex;align-items:center;justify-content:center;font-size:${S ? 300 : 220}px;color:${pal.solid};opacity:.55">${esc((t.name || '?')[0])}</div>`;
  const inner = photo
    + `<div class="a" data-tag="subj" style="left:40px;top:${ph - 34}px;transform:rotate(-4deg);z-index:6">${chip(t.subject || 'Subject', pal.solid, { size: S ? 36 : 30, color: textOn(pal.solid) })}</div>`
    + txt('tname', 44, ph + 44, L.cw - 88, S ? 80 : 64, esc(t.name || 'Name'), { size: S ? 64 : 52, weight: 800, color: pal.text, ls: '-.05em', lh: 1, fit: 28, bg: C.card, extra: D })
    + txt('tquote', 44, ph + (S ? 150 : 124), L.cw - 88, h - ph - (S ? 300 : 250), esc(t.quote || ''), { size: S ? 48 : 40, weight: 500, color: C.prose, ls: '-.03em', lh: 1.16, fit: 22, bg: C.card })
    + `<div style="position:absolute;left:44px;bottom:40px">${chip('Checked and selected by our team', C.mint, { size: S ? 30 : 26, color: '#24603D' })}</div>`;
  return [chrome(spec, L, F), card('tcard', L.pad, top, L.cw, h, C.card, { r: 32, shadow: `0 0 0 2px ${C.hairline},${glow(pal.solid)}`, inner }), spec.cta ? ctaPill(L, L.y1 - (S ? 120 : 96), spec.cta, C.panel, { dot: F.a, h: S ? 100 : 80 }) : ''].join('');
}

// ---- LOOK: bento (V9). The mascot bento board, rebuilt for the tutor campaign: no papers, no tips tiles. -----------
export function bento(spec, L, F) {
  const a = F.a, G = 20, X = 48, T = 130;
  const wa = 300, wb = 300, wc = L.W - 2 * X - wa - wb - 2 * G, xb = X + wa + G, xc = xb + wb + G;
  const chips = ['Maths', 'Science', 'English', 'Commerce'].map((t, i) => chip(t, ['#fff', '#fff', '#fff', '#fff'][i], { size: 24, color: C.ink })).join('');
  const parts = [chrome({ ...spec, ground: 'bone' }, L, F),
    card('chars', X, T, wa + G + wb, 250, C.card, { r: 32, ring: true }),
    arch('c1', X + 40, T + 60, 120, 'great', -4), sun('c2', X + 220, T + 56, 130, '#FFC700', 6), lobe('c3', X + 410, T + 60, 130, '#5B7BD9', -6),
    card('subj', X, T + 270, wa, 330, C.peach, { r: 28, inner: txt('st', 24, 28, 252, 70, 'Every subject', { size: 38, weight: 800, color: '#7A3E00', ls: '-.045em', lh: 1, fit: 22, bg: C.peach }) + `<div style="position:absolute;left:24px;top:116px;display:flex;flex-direction:column;gap:12px;align-items:flex-start">${chips}</div>` }),
    card('free', xb, T + 270, wb, 330, a, { r: 32, shadow: glow(a), inner: txt('ft', 28, 40, 244, 150, 'Free for families.', { size: 56, weight: 800, color: textOn(a), ls: '-.055em', lh: .98, fit: 30, bg: a, extra: D }) + txt('fs', 28, 214, 244, 90, 'No commission. Ever.', { size: 28, weight: 600, color: textOn(a), ls: '-.02em', lh: 1.15, fit: 16, bg: a }) }),
    card('search', X, T + 620, wa, 490, C.indigoTint, { r: 28, inner: txt('qs', 24, 36, 252, 100, 'Where are you looking?', { size: 38, weight: 800, color: C.indigoDeep, ls: '-.045em', lh: 1, fit: 22, bg: C.indigoTint })
      + `<div style="position:absolute;left:20px;top:170px;width:260px;height:76px;border-radius:999px;background:#fff;display:flex;align-items:center;padding:0 20px;gap:10px"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="${C.secondary}" stroke-width="2.4" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg><span data-fit="12" style="font-size:22px;font-weight:500;color:${C.secondary};white-space:nowrap">Subject, class, area</span></div>`
      + `<div style="position:absolute;left:24px;top:290px;display:flex;flex-direction:column;gap:12px;align-items:flex-start">${chip('Board', '#fff', { size: 22, color: C.ink })}${chip('Class', '#fff', { size: 22, color: C.ink })}</div>` }),
    card('checked', xb, T + 620, wb, 490, C.mint, { r: 32, inner: txt('ct', 28, 36, 244, 170, 'Checked and selected.', { size: 52, weight: 800, color: '#24603D', ls: '-.055em', lh: .98, fit: 28, bg: C.mint, extra: D }) + txt('cs', 28, 230, 244, 110, 'Every tutor, by our team.', { size: 28, weight: 600, color: '#24603D', ls: '-.02em', lh: 1.15, fit: 16, bg: C.mint }) + arch('n9', 118, 352, 124, 'good', 4) }),
    card('tall', xc, T, wc, 1110, C.card, { r: 32, ring: true, inner: eyes('eyesvg', 8, 1110 - Math.round((wc - 16) * .62) + 2, wc - 16, a) }),
    arch('cm', xc + (wc - 120) / 2, T + 40, 120, 'good', 0),
    `<h1 class="a" data-tag="headline" data-fit="40" style="left:${xc + 24}px;top:${T + 190}px;width:${wc - 48}px;height:380px;font-size:104px;font-weight:400;color:${C.ink};text-align:center;line-height:1.02;letter-spacing:-.055em">${esc(spec.copy.plain)} <span style="font-weight:800;letter-spacing:-.06em">${esc(spec.copy.bold)}</span></h1>`,
    txt('sub', xc + 24, T + 590, wc - 48, 120, esc(spec.copy.sub), { size: 26, weight: 500, color: C.prose, ls: '-.02em', lh: 1.25, fit: 16, align: 'center' }),
    `<div class="a" data-tag="ctachip" style="left:${xc + 30}px;top:${T + 730}px;width:${wc - 60}px;height:84px;border-radius:999px;background:${C.panel};display:flex;align-items:center;justify-content:center"><div data-fit="14" style="width:${wc - 100}px;text-align:center;font-size:30px;font-weight:700;color:#fff;letter-spacing:-.03em;white-space:nowrap">${esc(spec.cta || 'Find your tutor')}</div></div>`,
  ];
  return parts.join('');
}
