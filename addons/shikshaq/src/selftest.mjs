// Each assertion reproduces a failure this engine exists to prevent. One pass banner, at the end.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { subjectPalette, C, contrast } from './tokens.mjs';
import { planWeek, loadBrain } from './brain.mjs';
import { validatePlan } from './validate.mjs';
import { pickStyle, ACCENT_FOR, loadBank } from './style.mjs';

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
let n = 0;
const ok = (c, m) => { n++; if (!c) { console.error(`FAIL ${n}: ${m}`); process.exit(1); } };
const facts = JSON.parse(fs.readFileSync(path.join(root, 'facts/facts.sample.json'), 'utf8'));
const week = { id: '2026-W41', n: 202641, month: 10 };

// 1-4 tokens still match the site
const siteCss = path.join(process.env.SHIKSHAQ_REPO || path.join(root, '..'), 'src/index.css');
const css = fs.existsSync(siteCss) ? fs.readFileSync(siteCss, 'utf8').toUpperCase() : null; // skipped when no Shikshaq checkout is beside this copy
for (const k of ['page', 'card', 'muted', 'hairline', 'panel']) ok(!css || css.includes(C[k].toUpperCase()), `token ${k} ${C[k]} missing from src/index.css`);
const spec = { Maths: ['#FCECDE', '#F2A15A'], Science: ['#E3F7EC', '#34B268'], Commerce: ['#E2EAF8', '#4775D1'], Hindi: ['#F9E2E2', '#D74242'] };
for (const [s, [t, sol]] of Object.entries(spec)) { const p = subjectPalette(s); ok(p.tint === t && p.solid === sol, `${s} palette drifted from VISUAL_LANGUAGE section 3`); }
ok(contrast(C.ink, C.orange) > 4.5, 'ink on orange must pass AA');

// plan + gates
const brain = loadBrain(), plan = planWeek({ facts, week, brain });
ok(plan.posts.length === 3, 'a week is three posts');
ok(new Set(plan.posts.map(p => p.template)).size === 3, 'three different templates');
ok(JSON.stringify(plan) === JSON.stringify(planWeek({ facts, week, brain })), 'planning must be deterministic');
const clean = validatePlan(plan, facts, { dry: true });
ok(clean.errors.length === 0, 'baseline plan should pass the copy gate: ' + clean.errors.join('; '));
ok(validatePlan(plan, facts, { dry: false }).errors.some(e => /sample facts/.test(e)), 'sample facts must be refused outside --dry');

// the validator catches the historical failure classes
const bad = (mut) => { const p = structuredClone(plan); mut(p.posts[0]); return validatePlan(p, facts, { dry: true }).errors; };
ok(bad(p => { p.copy.sub = 'Learn — fast'; }).some(e => /dash/.test(e)), 'em dash must fail');
ok(bad(p => { p.caption += ' Trusted by thousands of parents.'; }).length >= 1, 'social proof must fail');
ok(bad(p => { p.caption += ' We have 9,999 papers.'; }).some(e => /9,999|9999/.test(e)), 'an untraceable number must fail');
ok(bad(p => { p.copy.sub = 'The best teacher guaranteed.'; }).length >= 1, 'superlative must fail');

// rotation: the same week planned after a ledger entry must not repeat its copy
const ledger = { weeks: [{ id: '2026-W40', n: 202640, posts: plan.posts.map(p => ({ copy: p.copyId, subject: p.subject || null, paperId: p.paperId || null })) }] };
const next = planWeek({ facts, week: { id: '2026-W42', n: 202642, month: 10 }, brain: { ...brain, ledger } });
const same = next.posts.filter((p, i) => p.copyId === plan.posts[i].copyId).length;
ok(same <= 1, `rotation repeated ${same} of 3 copy entries from last week`);


// style draw: reproducible, never empty, relaxations reported, semantic accent is not a style choice
ok(JSON.stringify(pickStyle({ template: 'steps', seed: 5 })) === JSON.stringify(pickStyle({ template: 'steps', seed: 5 })), 'style draw must be reproducible for a seed');
const impossible = pickStyle({ template: 'steps', ground: 'nonexistent', seed: 3 });
ok(impossible.id && impossible.relaxed.includes('ground=nonexistent'), 'an over-specified draw must relax and say so, never return nothing');
ok(pickStyle({ template: 'subject-mosaic', seed: 9, bank: { ...loadBank(), styles: loadBank().styles.filter(s => s.id === 'mirror-bento') } }).relaxed.some(r => r.startsWith('template=')), 'a template no style allows must relax, not crash');
ok(plan.posts.every(p => p.style && p.style.id), 'every planned post carries a drawn style');
ok(plan.posts.every(p => p.accent === ACCENT_FOR[p.pillar]), 'accent is semantic per pillar, a hard rule no style can change');
const only = id => loadBank().styles.filter(s => s.id === id || s.id === 'punch');
const recentLedger = { weeks: [{ id: 'x', n: 99, posts: [{ style: 'punch' }] }] };
let punchNow = 0, punchRecent = 0;
for (let sd = 1; sd <= 200; sd++) { if (pickStyle({ seed: sd }).id === 'punch') punchNow++; if (pickStyle({ seed: sd, ledger: recentLedger, nowN: 100 }).id === 'punch') punchRecent++; }
ok(punchRecent < punchNow, 'a style used last week must be drawn less often');

// brand rule: no em or en dashes anywhere the engine can publish from
for (const f of ['brain/pillars.json', 'brain/calendar.json', 'facts/facts.sample.json']) ok(!/[—–]/.test(fs.readFileSync(path.join(root, f), 'utf8')), `${f} contains an em or en dash`);
console.log(`ALL ${n} ASSERTIONS PASSED`);
