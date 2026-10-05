#!/usr/bin/env node
// Usage: node run-week.mjs [--dry] [--week 2026-W41] [--facts path] [--commit]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadBrain, planWeek, isoWeek, mondayOf } from './src/brain.mjs';
import { validatePlan } from './src/validate.mjs';
import { renderPlan, contactSheet } from './src/render.mjs';

const root = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2), flag = f => args.includes(f), opt = f => (args.includes(f) ? args[args.indexOf(f) + 1] : null);
const dry = flag('--dry');
const week = opt('--week') ? (() => { const id = opt('--week'), m = mondayOf(id); return { id, n: Number(id.replace('-W', '')), month: m.getUTCMonth() + 1 }; })() : isoWeek(new Date());
const factsPath = opt('--facts') || path.join(root, dry ? 'facts/facts.sample.json' : 'facts/facts.live.json');
if (!fs.existsSync(factsPath)) { console.error(`No facts at ${factsPath}. Run: node src/fetch-facts.mjs`); process.exit(2); }
const facts = JSON.parse(fs.readFileSync(factsPath, 'utf8'));
const brain = loadBrain();

const plan = planWeek({ facts, week, brain });
const { errors, warns } = validatePlan(plan, facts, { dry });
console.log(`\nPLAN ${plan.week} (${dry ? 'DRY RUN' : 'LIVE'}), season ${plan.season}`);
plan.log.forEach(l => console.log('  ' + l));
warns.forEach(w => console.log('  WARN ' + w));
if (errors.length) { console.error('\nCOPY GATE FAILED:'); errors.forEach(e => console.error('  ' + e)); process.exit(1); }
console.log('  copy gate: clean');

const outDir = path.join(root, 'out', plan.week + (dry ? '-dry' : ''));
const results = await renderPlan(plan, outDir);
let bad = 0;
for (const r of results) { console.log(`  ${r.day}: ${path.basename(r.file)} ${r.issues.length ? '' : 'clean'}`); r.issues.forEach(i => { bad++; console.log('     ' + i); }); }
await contactSheet(plan.posts.map(p => p.file), path.join(outDir, '_week.png'));

const md = [`# Shikshaq week ${plan.week}${dry ? ' (DRY RUN, sample facts)' : ''}`, '', `Season: ${plan.season}`, '',
  ...plan.posts.flatMap(p => [`## ${p.day} ${p.time} IST · ${p.pillar} · ${p.template}`, '', `![](${path.basename(p.file)})`, '', '```', p.caption, '```', '', `Alt text: ${p.alt}`, ''])];
fs.writeFileSync(path.join(outDir, 'week.md'), md.join('\n'));
fs.writeFileSync(path.join(outDir, 'plan.json'), JSON.stringify({ ...plan, posts: plan.posts.map(p => ({ ...p, file: path.basename(p.file) })) }, null, 2));

if (flag('--commit') && !dry && !bad) {
  brain.ledger.weeks.push({ id: plan.week, n: week.n, posts: plan.posts.map(p => ({ copy: p.copyId, subject: p.subject || null, paperId: p.paperId || null, template: p.template, accent: p.accent, style: p.style && p.style.id })) });
  brain.ledger.weeks = brain.ledger.weeks.slice(-26);
  fs.writeFileSync(path.join(root, 'brain/ledger.json'), JSON.stringify(brain.ledger, null, 2));
  console.log('  ledger updated');
}
console.log(`\n${bad ? bad + ' layout issue(s), fix before posting' : 'all layout gates clean'}. Output: ${outDir}`);
process.exit(bad ? 1 : 0);
