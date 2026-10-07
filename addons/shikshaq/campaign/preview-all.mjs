// Render every asset (or a family) and write sheets. For design review while the text deliverables are rewritten.
import { renderSpecs, sheet } from './renderer.mjs';
import { ITEMS, FAMILIES } from './catalog.mjs';
import { loadData, resolveItem } from './resolve.mjs';
const fam = (process.argv.find(a => a.startsWith('--family=')) || '').split('=')[1]?.split(',');
const data = loadData();
const items = ITEMS.filter(i => !fam || fam.includes(i.family)).map(i => resolveItem(i, data));
const out = new URL('../out/campaign-what-is-shikshaq', import.meta.url).pathname;
const res = await renderSpecs(items, out);
for (const r of res) if (r.issues.length) console.log(r.id, '\n   ', r.issues.slice(0, 5).join('\n    '));
for (const [f] of FAMILIES) for (const c of ['S', 'F', 'Q', 'C', 'K']) {
  const sub = res.filter(r => r.family === f && r.canvas === c); if (!sub.length) continue;
  await sheet(sub.map(r => ({ ...r, canvas: c === 'C' ? 'S' : c === 'K' ? 'Q' : c })), `${out}/_sheets/${f}-${c}.png`, { cols: c === 'S' || c === 'C' ? 7 : (c === 'K' ? 6 : 5), cell: c === 'S' || c === 'C' ? 260 : 330 });
}
console.log('rendered', res.length, 'issues', res.filter(r => r.issues.length).length);
