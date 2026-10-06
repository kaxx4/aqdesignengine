// One browser, many specs. Each render runs the shared DOM gate (clipped, margin, contrast, collisions,
// invisible fills) PLUS the story safe-zone rule, on what was actually drawn.
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright-core';
import { CHROME, gate } from '../src/render.mjs';
import { renderHtml } from './looks.mjs';

export async function renderSpecs(items, outRoot, { onlyIds } = {}) {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const results = [];
  try {
    const ctxs = {};
    for (const it of items) {
      if (onlyIds && !onlyIds.includes(it.id)) continue;
      let { html, L } = renderHtml(it);
      if (it.placeholder) html = html.replace('<script>', `<div data-deco="1" style="position:absolute;left:-60px;top:44%;width:1300px;transform:rotate(-12deg);background:#D14545;color:#fff;font:800 56px Archivo,Geist,sans-serif;text-align:center;padding:16px 0;z-index:999;letter-spacing:.04em;opacity:.93">DRAFT . PLACEHOLDER DATA . DO NOT POST</div><script>`);
      const key = L.W + 'x' + L.H;
      ctxs[key] = ctxs[key] || await browser.newContext({ viewport: { width: L.W, height: L.H }, deviceScaleFactor: 1 });
      const pg = await ctxs[key].newPage();
      await pg.setContent(html, { waitUntil: 'load' });
      await pg.evaluate(() => document.fonts.ready);
      await pg.waitForTimeout(80);
      const file = path.join(outRoot, it.dir || '', it.id + '.png');
      fs.mkdirSync(path.dirname(file), { recursive: true });
      await pg.screenshot({ path: file, clip: { x: 0, y: 0, width: L.W, height: L.H }, omitBackground: it.look === 'cover' });
      const issues = it.look === 'cover' ? [] : await pg.evaluate(`(${gate.toString()})(${L.W},${L.H},${JSON.stringify(L.safe)},.16)`);
      await pg.close();
      results.push({ id: it.id, file, canvas: it.canvas, issues, placeholder: !!it.placeholder, family: it.family });
    }
  } finally { await browser.close(); }
  return results;
}

// A contact sheet: files in a wrapped grid, each scaled to a fixed cell, labelled by id.
export async function sheet(results, out, { cols = 6, cell = 300 } = {}) {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const imgs = results.map(r => {
    const h = r.canvas === 'S' ? cell * 1920 / 1080 : r.canvas === 'F' ? cell * 1350 / 1080 : cell;
    return `<div style="width:${cell}px"><img src="data:image/png;base64,${fs.readFileSync(r.file).toString('base64')}" style="width:${cell}px;height:${h}px;border-radius:10px;box-shadow:0 0 0 1px #E7DFD5;display:block"><div style="font:600 13px/1.3 monospace;color:${r.issues.length ? '#B00020' : '#4A443E'};margin-top:6px">${r.id}${r.issues.length ? ' !' + r.issues.length : ''}</div></div>`;
  }).join('');
  const pg = await browser.newPage({ viewport: { width: cols * (cell + 20) + 20, height: 800 } });
  await pg.setContent(`<body style="margin:0;background:#EDE7DF;display:flex;flex-wrap:wrap;gap:20px;padding:20px;align-items:flex-start">${imgs}</body>`);
  await pg.screenshot({ path: out, fullPage: true });
  await browser.close();
}
