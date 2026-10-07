// node campaign/weekset.mjs 1   -> out/.../_weeks/week1-feed.png, week1-stories.png (planned assets for that week, in plan order)
import fs from 'node:fs';
import path from 'node:path';
import { WEEKS } from './plan.mjs';
import { ITEMS, expand } from './catalog.mjs';
import { sheet } from './renderer.mjs';
const OUT = new URL('../out/campaign-what-is-shikshaq', import.meta.url).pathname;
const n = +process.argv[2], wk = WEEKS.find(w => w.n === n);
const pick = toks => toks.flatMap(t => expand(t)).map(i => ({ ...i, file: path.join(OUT, i.dir || '', i.id + '.png') })).filter(r => fs.existsSync(r.file)).map(r => ({ ...r, issues: [] }));
const feed = pick(wk.days.flatMap(d => d.feed ? [d.feed] : []));
const stories = pick(wk.days.flatMap(d => d.stories || []));
fs.mkdirSync(OUT + '/_weeks', { recursive: true });
await sheet(feed.map(r => ({ ...r, canvas: r.canvas })), `${OUT}/_weeks/week${n}-feed.png`, { cols: 4, cell: 480 });
await sheet(stories.map(r => ({ ...r, canvas: 'S' })), `${OUT}/_weeks/week${n}-stories.png`, { cols: 7, cell: 260 });
console.log(feed.length, 'feed', stories.length, 'stories');
