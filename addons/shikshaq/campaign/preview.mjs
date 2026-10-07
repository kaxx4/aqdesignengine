// Framing previews. A story is shown inside a generic phone with the story chrome drawn over it, so the safe zones are
// visible to a reviewer. A WhatsApp push is shown as a chat bubble: the image with its message as the caption.
import fs from 'node:fs';
import { chromium } from 'playwright-core';
import { CHROME } from '../src/render.mjs';

const b64 = f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export async function phoneSheet(results, out, { cols = 6 } = {}) {
  const W = 270, H = Math.round(W * 1920 / 1080);
  const phones = results.map(r => `<div style="width:${W + 30}px"><div style="position:relative;width:${W + 30}px;height:${H + 30}px;border-radius:46px;background:#1B1A18;padding:15px;box-shadow:0 10px 24px rgba(0,0,0,.18)">
    <div style="position:relative;width:${W}px;height:${H}px;border-radius:32px;overflow:hidden;background:#fff"><img src="${b64(r.file)}" style="width:${W}px;height:${H}px;display:block">
      <div style="position:absolute;left:10px;right:10px;top:12px;height:3px;border-radius:2px;background:rgba(255,255,255,.35)"><div style="width:35%;height:100%;border-radius:2px;background:#fff"></div></div>
      <div style="position:absolute;left:12px;top:26px;display:flex;gap:8px;align-items:center"><div style="width:26px;height:26px;border-radius:99px;background:#FF8000;box-shadow:0 0 0 2px #fff"></div><div style="font:700 12px Geist,Arial,sans-serif;color:#1F1F1F;text-shadow:0 0 4px #fff">shikshaq</div></div>
      <div style="position:absolute;left:12px;right:12px;bottom:14px;height:36px;border-radius:99px;box-shadow:0 0 0 1.5px rgba(31,31,31,.5);background:rgba(255,255,255,.65);font:500 12px Geist,Arial,sans-serif;color:#555;display:flex;align-items:center;padding-left:14px">Send message</div></div></div>
    <div style="font:600 13px/1.3 monospace;color:#4A443E;margin-top:8px;text-align:center">${r.id}</div></div>`).join('');
  const b = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const pg = await b.newPage({ viewport: { width: cols * (W + 70) + 40, height: 900 } });
  await pg.setContent(`<body style="margin:0;background:#EDE7DF;display:flex;flex-wrap:wrap;gap:26px;padding:26px;align-items:flex-start">${phones}</body>`);
  await pg.screenshot({ path: out, fullPage: true });
  await b.close();
}

export async function waPreview(push, files, text, out) {
  const imgs = files.length === 1
    ? `<img src="${b64(files[0])}" style="width:100%;border-radius:10px;display:block">`
    : `<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px">${files.map(f => `<img src="${b64(f)}" style="width:100%;border-radius:8px;display:block">`).join('')}</div>`;
  const html = `<body style="margin:0;width:760px;background:#EFE7DC;font-family:Geist,Arial,sans-serif">
   <div style="background:#1B1A18;color:#fff;padding:22px 26px;display:flex;align-items:center;gap:18px"><div style="font-size:30px">&#8592;</div><div style="width:54px;height:54px;border-radius:99px;background:#FF8000"></div><div><div style="font-size:26px;font-weight:700">${esc(push.to)}</div><div style="font-size:18px;color:#CFC7BD">${esc(push.id)} . Week ${push.week} ${push.day} ${push.time}</div></div></div>
   <div style="padding:34px 26px 60px"><div style="margin-left:auto;width:560px;background:#D9FDD3;border-radius:18px 4px 18px 18px;padding:8px 8px 10px;box-shadow:0 1px 2px rgba(0,0,0,.18)">
     ${imgs}<div style="padding:12px 10px 4px;font-size:24px;line-height:1.35;color:#1F1F1F;white-space:pre-wrap">${esc(text)}</div><div style="text-align:right;font-size:16px;color:#667781;padding:4px 8px 0">${esc(push.time)} &#10003;&#10003;</div></div></div></body>`;
  const b = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const pg = await b.newPage({ viewport: { width: 760, height: 900 } });
  await pg.setContent(html);
  await pg.screenshot({ path: out, fullPage: true });
  await b.close();
}
