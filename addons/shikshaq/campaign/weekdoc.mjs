// node campaign/weekdoc.mjs   -> out/.../texts/week1.md ... week4.md: everything a person needs for each day, in posting order
import fs from 'node:fs';
import { WEEKS, REELS, AQUATERRA } from './plan.mjs';
import { expand, ITEMS } from './catalog.mjs';
import { PUSHES, ADMIN_ASK, FORMAT } from './wa.mjs';
import { CAPTIONS } from './captions.mjs';
import { hashtagsFor, altText } from './texts.mjs';
import { loadData, resolveItem, fillTokens } from './resolve.mjs';
const OUT = new URL('../out/campaign-what-is-shikshaq/texts', import.meta.url).pathname;
const data = loadData();
fs.mkdirSync(OUT, { recursive: true });
for (const wk of WEEKS) {
  let md = `# Week ${wk.n}: ${wk.theme}\n\nEverything for the week in posting order. Times are IST. Image files are in the family folders under \`out/campaign-what-is-shikshaq/\`.\n\n`;
  for (const d of wk.days) {
    md += `## ${d.d}${d.note ? `\n\n_${d.note}_` : ''}\n\n`;
    if (d.feed) {
      const imgs = expand(d.feed).map(i => resolveItem(i, data)), gated = imgs.some(i => i.placeholder);
      md += `### Feed post 19:30: ${d.feed}${gated ? ' (GATED: waits on real data)' : ''}${AQUATERRA.includes(d.feed) ? ' (also post on the AquaTerra account)' : ''}\n\nFiles: ${imgs.map(i => `${i.dir}/${i.id}.png`).join(', ')}\n\n**Caption**\n\n${CAPTIONS[d.feed]}\n\n${hashtagsFor(d.feed).join(' ')}\n\n**Alt text**\n\n${imgs.map(i => `- ${i.id}: ${altText(i)}`).join('\n')}\n\n`;
    }
    if (d.stories?.length) {
      md += `### Stories, through the day\n\n${d.stories.map(t => `- ${expand(t).map(i => `${i.dir}/${i.id}.png`).join(', ')}${expand(t).some(i => i.gated) ? ' (GATED)' : ''}`).join('\n')}\n\n`;
      if (d.rerun?.length) md += `Rerun: ${d.rerun.join(', ')}\n\n`;
    }
    for (const id of d.wa || []) {
      const p = PUSHES.find(x => x.id === id), { text } = fillTokens(p.message, data);
      md += `### WhatsApp ${p.time}: ${p.id}, ${p.to}\n\nImage: ${p.image.join(', ')}${p.gated ? ` (GATED on ${p.gated})` : ''}\n\n\`\`\`\n${text}\n\`\`\`\n\nReplies to expect:\n\n${p.replies.map(([q, a]) => `- "${q}" Reply: ${a}`).join('\n')}\n\n`;
    }
    if (d.reel) md += `### Reel: ${d.reel} ${REELS[d.reel]} (paused: reels are on hold)\n\n`;
  }
  fs.writeFileSync(`${OUT}/week${wk.n}.md`, md);
}
console.log('wrote week1..4.md');
