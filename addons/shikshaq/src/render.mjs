// Render plan -> PNG with one browser, then run the DOM gates on what was DRAWN.
import fs from 'node:fs';
import { chromium } from 'playwright-core';
import { SIZES, contrast } from './tokens.mjs';

const TEMPLATES = {
  'number-bento': () => import('./templates/number-bento.mjs'),
  'paper-spotlight': () => import('./templates/paper-spotlight.mjs'),
  'subject-mosaic': () => import('./templates/subject-mosaic.mjs'),
  'steps': () => import('./templates/steps.mjs'),
  'find-teacher': () => import('./templates/find-teacher.mjs'),
  'bento-board': () => import('./templates/bento-board.mjs'),
};
export const CHROME = process.env.CHROME_PATH || ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome'].find(p => fs.existsSync(p));

// Runs in the page. Returns problems found in the real layout.
export function gate(W, H, safe, tol = 0) {
  const out = [];
  const rgb = s => { const m = s.match(/[\d.]+/g).map(Number); return { r: m[0], g: m[1], b: m[2], a: m[3] === undefined ? 1 : m[3] }; };
  const hex = c => '#' + [c.r, c.g, c.b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  const L = c => { const v = [c.r, c.g, c.b].map(x => { x /= 255; return x <= .03928 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4; }); return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]; };
  const ratio = (a, b) => { const [x, y] = [L(a), L(b)].sort((m, n) => n - m); return (x + .05) / (y + .05); };
  const bgOf = el => { for (let e = el; e; e = e.parentElement) { const c = rgb(getComputedStyle(e).backgroundColor); if (c.a > .95) return c; } return { r: 249, g: 245, b: 241, a: 1 }; };
  const name = el => el.dataset.tag || el.closest('[data-tag]')?.dataset.tag || el.tagName.toLowerCase();
  const leaves = [];
  document.querySelectorAll('.p *').forEach(el => {
    if (el.closest('[data-deco]') || /^(STYLE|SCRIPT)$/.test(el.tagName)) return;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) return;
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    leaves.push({ el, r, cs, txt: el.textContent.trim().slice(0, 30) });
    if (el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0 && cs.display !== 'inline') out.push(`CLIPPED-X ${name(el)} "${el.textContent.trim().slice(0, 24)}"`);
    if (el.scrollHeight > el.clientHeight + 2 + tol * parseFloat(cs.fontSize) && el.clientHeight > 0 && cs.display !== 'inline') out.push(`CLIPPED-Y ${name(el)} "${el.textContent.trim().slice(0, 24)}"`);
    if (safe && (r.top < safe.top || r.bottom > H - safe.bottom) && !el.closest('[data-bleed]')) out.push(`SAFE-ZONE ${name(el)} "${el.textContent.trim().slice(0, 24)}" [${Math.round(r.top)},${Math.round(r.bottom)}] story chrome covers y<${safe.top} and y>${H - safe.bottom}`);
    if (r.left < 24 || r.top < 24 || r.right > W - 24 || r.bottom > H - 24) out.push(`MARGIN ${name(el)} "${el.textContent.trim().slice(0, 24)}" [${Math.round(r.left)},${Math.round(r.top)},${Math.round(r.right)},${Math.round(r.bottom)}]`);
    const fg = rgb(cs.color), bg = el.dataset.bg ? (h => ({ r: parseInt(h.slice(1, 3), 16), g: parseInt(h.slice(3, 5), 16), b: parseInt(h.slice(5, 7), 16), a: 1 }))(el.dataset.bg) : bgOf(el), size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700;
    const eff = fg.a < 1 ? { r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a) } : fg;
    let need = (size >= 24 && bold) || size >= 32 ? 3 : 4.5; const got = ratio(eff, bg);
    // owner-approved: the brand orange payoff in a display headline (VISUAL_DIRECTION section 6). 2.2:1 floor, display sizes only.
    if (hex(eff) === '#ff8000' && size >= 56) need = 2.2;
    // owner-approved: white on #ff8000 (VISUAL_DIRECTION section 6, 'accepted accessibility exceptions'). Display sizes only.
    if (hex(eff) === '#ffffff' && hex(bg) === '#ff8000' && size >= 56) need = 2.0;
    if (cs.color !== 'rgba(0, 0, 0, 0)' && parseFloat(cs.opacity) > 0 && got < need && size > 1) out.push(`CONTRAST ${got.toFixed(2)}:1 < ${need} on "${el.textContent.trim().slice(0, 24)}" (${hex(eff)} on ${hex(bg)})`);
  });
  if (safe) document.querySelectorAll('img[data-tag="logo"]').forEach(el => { const r = el.getBoundingClientRect(); if (r.top < safe.top || r.bottom > H - safe.bottom) out.push(`SAFE-ZONE logo [${Math.round(r.top)},${Math.round(r.bottom)}]`); });
  document.querySelectorAll('[data-tag]').forEach(el => {
    const cs = getComputedStyle(el), own = rgb(cs.backgroundColor);
    if (own.a < .95 || el.tagName === 'svg' || el.tagName === 'IMG') return;
    const par = el.parentElement ? bgOf(el.parentElement) : { r: 249, g: 245, b: 241 };
    if (cs.boxShadow !== 'none' && /0px 0px 0px [2-9]px/.test(cs.boxShadow)) return;
    if (Math.hypot(own.r - par.r, own.g - par.g, own.b - par.b) < 14) out.push(`INVISIBLE-FILL ${el.dataset.tag} (${hex(own)} on ${hex(par)})`);
  });
  document.querySelectorAll('svg.a[data-tag]').forEach(sv => {
    if (/^n\d/.test(sv.dataset.tag)) return;
    let r = sv.getBoundingClientRect();
    // art that an overflow:hidden ancestor clips is not on top of anything the viewer can see
    for (let a = sv.parentElement; a && a !== document.body; a = a.parentElement) { if (/hidden|clip/.test(getComputedStyle(a).overflow)) { const q = a.getBoundingClientRect(); r = { left: Math.max(r.left, q.left), right: Math.min(r.right, q.right), top: Math.max(r.top, q.top), bottom: Math.min(r.bottom, q.bottom) }; } }
    leaves.forEach(l => {
      const ox = Math.min(r.right, l.r.right) - Math.max(r.left, l.r.left), oy = Math.min(r.bottom, l.r.bottom) - Math.max(r.top, l.r.top);
      if (ox > 8 && oy > 8) out.push(`ART-ON-TEXT ${sv.dataset.tag} x "${l.txt}" (${Math.round(ox)}x${Math.round(oy)})`);
    });
  });
  for (let i = 0; i < leaves.length; i++) for (let j = i + 1; j < leaves.length; j++) {
    const a = leaves[i], b = leaves[j];
    if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
    const ox = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left), oy = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
    if (ox > 8 && oy > 8) out.push(`COLLISION "${a.txt}" x "${b.txt}" (${Math.round(ox)}x${Math.round(oy)})`);
  }
  return out;
}

export async function renderPlan(plan, outDir, sizeKey = 'feed') {
  const [W, H] = SIZES[sizeKey];
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const results = [];
  try {
    for (const [i, post] of plan.posts.entries()) {
      const mod = await TEMPLATES[post.template]();
      const html = mod.render(post, W, H);
      const pg = await ctx.newPage();
      await pg.setContent(html, { waitUntil: 'load' });
      await pg.evaluate(() => document.fonts.ready);
      await pg.waitForTimeout(60);
      const file = `${outDir}/${String(i + 1).padStart(2, '0')}-${post.day.toLowerCase()}-${post.template}.png`;
      await pg.screenshot({ path: file, clip: { x: 0, y: 0, width: W, height: H } });
      const real = await pg.evaluate(`(${gate.toString()})(${W},${H})`);
      await pg.close();
      post.file = file; results.push({ day: post.day, file, issues: real });
    }
  } finally { await browser.close(); }
  return results;
}

// One contact sheet so the whole week is judged side by side, like a feed grid.
export async function contactSheet(files, out, W = 1080, H = 1350) {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const pg = await browser.newPage({ viewport: { width: files.length * 360 + (files.length + 1) * 16, height: 480 + 32 } });
  const imgs = files.map(f => `<img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}" style="width:360px;height:450px;border-radius:12px;box-shadow:0 0 0 1px #E7DFD5">`).join('');
  await pg.setContent(`<body style="margin:0;background:#EDE7DF;display:flex;gap:16px;padding:16px">${imgs}</body>`);
  await pg.screenshot({ path: out });
  await browser.close();
}
