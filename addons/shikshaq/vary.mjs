#!/usr/bin/env node
// Random variations in the Shikshaq style. Usage:
//   node vary.mjs [--n 8] [--seed 7] [--template bento-board] [--energy playful] [--facts path]
// Educated-random: each variation draws a template, copy and a style recipe, renders it, and REJECTS
// any draw the layout gate fails (reporting why) rather than showing you a broken poster.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadBrain, planWeek, isoWeek } from './src/brain.mjs';
import { validatePlan } from './src/validate.mjs';
import { pickStyle, rng, ACCENT_FOR } from './src/style.mjs';
import { renderPlan, contactSheet } from './src/render.mjs';

const root = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2), opt = (f, d) => (args.includes(f) ? args[args.indexOf(f) + 1] : d);
const n = Number(opt('--n', 8)), seed = Number(opt('--seed', Date.now() % 100000));
const factsPath = opt('--facts', path.join(root, 'facts/facts.sample.json'));
const facts = JSON.parse(fs.readFileSync(factsPath, 'utf8'));
const brain = loadBrain(), r = rng(seed);
const TEMPLATE_PILLAR = { 'paper-spotlight': 'papers', 'subject-mosaic': 'papers', steps: 'tips', 'find-teacher': 'teachers', 'number-bento': 'trust', 'bento-board': 'teachers' };
const templates = opt('--template') ? [opt('--template')] : Object.keys(TEMPLATE_PILLAR);
const outDir = path.join(root, 'out', `vary-${seed}`);
const month = isoWeek(new Date()).month;
const kept = [], rejects = [];
let deck = [];
const nextTemplate = () => { if (!deck.length) { deck = [...templates]; for (let i = deck.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [deck[i], deck[j]] = [deck[j], deck[i]]; } } return deck.pop(); };

for (let i = 0; i < n; i++) {
  for (let attempt = 0; attempt < 6; attempt++) {
    const template = attempt === 0 ? nextTemplate() : templates[Math.floor(r() * templates.length)], pillar = TEMPLATE_PILLAR[template];
    const week = { id: `VAR-${seed}-${i}-${attempt}`, n: seed * 1000 + i * 10 + attempt, month };
    const one = { ...brain.pillars, slots: [{ day: `V${i + 1}`, pillar, template: [template], time: '19:30', cta: brain.pillars.slots.find(s => s.pillar === pillar)?.cta || 'See how it works' }] };
    let plan;
    try { plan = planWeek({ facts, week, brain: { ...brain, pillars: one, ledger: { weeks: [] } } }); } catch (e) { rejects.push(`${template}: ${e.message}`); continue; }
    const post = plan.posts[0];
    post.style = pickStyle({ template, energy: opt('--energy'), seed: Math.floor(r() * 4294967296) });
    const { errors } = validatePlan(plan, facts, { dry: true });
    if (errors.length) { rejects.push(`${template}/${post.style.id}: copy: ${errors[0]}`); continue; }
    const [res] = await renderPlan({ posts: [post] }, path.join(outDir, `_try-${i}-${attempt}`));
    if (res.issues.length) { rejects.push(`${template}/${post.style.id}: layout: ${res.issues[0]}`); continue; }
    const file = path.join(outDir, `${String(i + 1).padStart(2, '0')}-${template}-${post.style.id}.png`);
    fs.mkdirSync(outDir, { recursive: true }); fs.renameSync(res.file, file); post.file = file; kept.push(post); break;
  }
}
fs.readdirSync(outDir).filter(f => f.startsWith('_try')).forEach(f => fs.rmSync(path.join(outDir, f), { recursive: true, force: true }));
if (kept.length) await contactSheet(kept.map(p => p.file), path.join(outDir, '_variations.png'));
const brief = kept.map((p, i) => `${i + 1}. ${p.template} / ${p.style.id} (${p.style.energy}), accent ${p.accent} (semantic for ${p.pillar})\n   ${p.style.mechanism}\n   Recipe: ${p.style.recipe}\n   Headline: ${p.copy.plain} ${p.copy.bold}`).join('\n\n');
fs.writeFileSync(path.join(outDir, 'brief.md'), `# Variations, seed ${seed}\n\n${brief}\n\nRejected draws: ${rejects.length}\n${rejects.map(x => '- ' + x).join('\n')}\n`);
console.log(brief);
console.log(`\n${kept.length}/${n} kept, ${rejects.length} rejected draw(s). Seed ${seed}. Output: ${outDir}`);
rejects.slice(0, 8).forEach(x => console.log('  rejected: ' + x));
