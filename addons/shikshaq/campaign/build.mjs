// Build the whole campaign: validate copy, render every asset through the DOM gate, write sheets, previews, and every text deliverable.
//   node campaign/build.mjs                    everything
//   node campaign/build.mjs --family=faq       one family
//   node campaign/build.mjs --only=FQ1,FQ2     named assets
//   node campaign/build.mjs --final            refuse to finish while any slot still holds placeholder data
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { ITEMS, FAMILIES } from './catalog.mjs';
import { loadData, resolveItem } from './resolve.mjs';
import { validateAll } from './validate-campaign.mjs';
import { renderSpecs, sheet } from './renderer.mjs';
import { phoneSheet, waPreview } from './preview.mjs';
import { writeCaptions, writeSchedule, pushTexts, writeWhatsApp, writeVolunteer, writeReels, feedPosts } from './texts.mjs';

const arg = k => (process.argv.find(a => a.startsWith(`--${k}=`)) || '').split('=')[1];
const flag = k => process.argv.includes(`--${k}`);
const OUT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'out', 'campaign-what-is-shikshaq');
const only = arg('only')?.split(','), fam = arg('family')?.split(',');

const data = loadData();
const all = ITEMS.map(i => resolveItem(i, data));
const errors = [...validateAll(ITEMS)];

// text deliverables first: they are cheap and they gate
const { out: pushes, errors: pushErrors } = pushTexts(data);
errors.push(...pushErrors, ...writeCaptions(OUT + '/texts', all), ...writeSchedule(OUT + '/texts', all, data));
errors.push(...writeVolunteer(OUT + '/texts'), ...writeReels(OUT + '/texts'));
writeWhatsApp(OUT + '/texts', pushes);
if (errors.length && !flag('force')) { console.error(`COPY GATE FAILED (${errors.length})\n` + errors.map(e => '  ' + e).join('\n')); process.exit(1); }

const todo = all.filter(i => (!only || only.includes(i.id) || only.includes(i.post)) && (!fam || fam.includes(i.family)));
const results = await renderSpecs(todo, OUT);
const bad = results.filter(r => r.issues.length), draft = results.filter(r => r.placeholder);

for (const r of bad) console.error(`GATE ${r.id}\n    ${r.issues.slice(0, 8).join('\n    ')}`);

// contact sheets and phone-frame previews, per family
if (!flag('no-previews')) {
  for (const [f, label] of FAMILIES) {
    const rs = results.filter(r => r.family === f);
    for (const c of ['S', 'F', 'Q', 'C']) {
      const sub = rs.filter(r => r.canvas === c);
      if (sub.length) await sheet(sub.map(r => ({ ...r, canvas: c === 'C' ? 'S' : c })), `${OUT}/_sheets/${f}-${c}.png`, { cols: c === 'S' || c === 'C' ? 7 : 5, cell: c === 'S' || c === 'C' ? 260 : 330 });
    }
    const st = rs.filter(r => r.canvas === 'S');
    if (st.length) await phoneSheet(st, `${OUT}/_phones/${f}.png`, { cols: 6 });
  }
  const fileOf = id => { const it = all.find(i => i.id === id); const p = it && `${OUT}/${it.dir}/${id}.png`; return p && fs.existsSync(p) ? p : null; };
  for (const p of pushes) { const files = p.image.map(fileOf).filter(Boolean); if (files.length) await waPreview(p, files, p.text, `${OUT}/wa-preview/${p.id}.png`); }
}

// manifest: every asset, its post, audience and status
const manifest = all.map(i => ({ id: i.id, family: i.family, canvas: i.canvas, post: i.post, audience: i.aud, file: `${i.dir}/${i.id}.png`, status: i.placeholder ? 'draft: waiting on data' : (results.find(r => r.id === i.id)?.issues.length ? 'gate issues' : 'ok'), sticker: i.sticker || undefined, count: i.count }));
fs.writeFileSync(`${OUT}/manifest.json`, JSON.stringify(manifest, null, 1));
const tally = c => all.filter(i => i.canvas === c).length;
const summary = `# Campaign build\n\nAssets: ${all.length} (stories ${tally('S')}, feed ${tally('F')}, square ${tally('Q')}, covers ${tally('C')}). Posts: ${new Set(all.map(i => i.post)).size}. Feed or square posts: ${feedPosts().length}.\nRendered this run: ${results.length}. Gate issues: ${bad.length}. Draft (waiting on data): ${all.filter(i => i.placeholder).length}.\nWhatsApp pushes: ${pushes.length}. Data mode: ${data.mode}.\n`;
fs.writeFileSync(`${OUT}/SUMMARY.md`, summary);
console.log(summary);
if (bad.length) process.exit(1);
if (flag('final') && all.some(i => i.placeholder)) { console.error(`NOT FINAL: ${all.filter(i => i.placeholder).length} slots still hold placeholder data (${all.filter(i => i.placeholder).map(i => i.id).join(', ')})`); process.exit(2); }
