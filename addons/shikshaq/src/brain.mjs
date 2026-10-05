// The marketing brain: turns (facts, ledger, calendar, pillars) into a week plan.
// Deterministic for a given week and ledger, so a dry run predicts the real run.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { SUBJECT_SEEDS } from './tokens.mjs';
import { pickStyle, ACCENT_FOR } from './style.mjs';

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const readJson = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
export const loadBrain = () => ({ pillars: readJson('brain/pillars.json'), calendar: readJson('brain/calendar.json'), ledger: readJson('brain/ledger.json') });

export function isoWeek(d = new Date()) {
  const t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  const day = t.getUTCDay() || 7; t.setUTCDate(t.getUTCDate() + 4 - day);
  const y = t.getUTCFullYear(), w = Math.ceil(((t - Date.UTC(y, 0, 1)) / 864e5 + 1) / 7);
  return { id: `${y}-W${String(w).padStart(2, '0')}`, n: y * 100 + w, month: d.getMonth() + 1 };
}
export function mondayOf(id) { // ISO week id -> Monday date
  const [y, w] = id.split('-W').map(Number), j4 = new Date(Date.UTC(y, 0, 4)), d = j4.getUTCDay() || 7;
  const m = new Date(j4); m.setUTCDate(j4.getUTCDate() - d + 1 + (w - 1) * 7); return m;
}
const hash = s => { let h = 2166136261; for (const c of s) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return (h >>> 0) / 4294967296; };

export function getFact(facts, p) {
  const parts = p.split('.');
  let v = facts;
  for (const k of parts) { if (v == null) return null; v = v[k]; }
  if (v && typeof v === 'object' && 'value' in v) v = v.value;
  return v === undefined ? null : v;
}
export const fmt = n => (typeof n === 'number' ? n.toLocaleString('en-IN') : String(n));

function fill(str, facts) {
  return str.replace(/\{(\w+)\}/g, (_, k) => {
    const map = { freeWord: 'constants.freeWord', classes: 'constants.classes', teachers: 'counts.teachers', papers: 'counts.papers' };
    const v = getFact(facts, map[k] || k);
    if (v == null) throw new Error(`copy token {${k}} has no fact`);
    return fmt(v);
  });
}
const recencyPenalty = (ledger, kind, key, nowN) => {
  let worst = 0;
  for (const w of ledger.weeks) for (const p of w.posts) if (p[kind] === key) { const age = Math.max(1, nowN - w.n); worst = Math.max(worst, Math.max(0, 1 - age / 8)); }
  return worst;
};
function leastRecent(options, kind, ledger, week, seed) {
  return [...options].sort((a, b) => (recencyPenalty(ledger, kind, a, week.n) + hash(seed + a) * 0.01) - (recencyPenalty(ledger, kind, b, week.n) + hash(seed + b) * 0.01));
}

export function planWeek({ facts, week, brain = loadBrain() }) {
  const { pillars, calendar, ledger } = brain;
  const season = calendar.months[String(week.month)], sdef = calendar.seasons[season];
  const log = [`Week ${week.id}, season "${season}". Pillar boosts: ${JSON.stringify(sdef.pillar_boost)}`];
  const used = new Set(), posts = [];
  const subjects = Object.keys(SUBJECT_SEEDS);
  const subjOrder = leastRecent(subjects, 'subject', ledger, week, week.id);
  let subjPtr = 0;

  pillars.slots.forEach((slot0, i) => {
    let slot = slot0;
    const tpls = [].concat(slot.template);
    let template = null, eligible = [];
    for (let k = 0; k < tpls.length && !eligible.length; k++) {
      template = tpls[(week.n + k) % tpls.length];
      eligible = pillars.copy[template].filter(e => (e.needs || []).every(n => getFact(facts, n) != null) && !used.has(e.id));
      if (!eligible.length) log.push(`${slot.day}: ${template} has no copy the facts support, trying the next layout`);
    }
    if (!eligible.length) throw new Error(`no eligible copy for ${tpls.join('/')}; missing facts?`);
    slot = { ...slot, template };
    const scored = eligible.map(e => {
      const themeBoost = e.theme && sdef.tip_themes.includes(e.theme) ? 2.5 : 0;
      const score = 1 + themeBoost - 3 * recencyPenalty(ledger, 'copy', e.id, week.n) + hash(week.id + e.id) * 0.5;
      return { e, score };
    }).sort((a, b) => b.score - a.score);
    const e = scored[0].e; used.add(e.id);
    log.push(`${slot.day} ${slot.template}: chose "${e.id}" (score ${scored[0].score.toFixed(2)}) over ${scored.length - 1} other(s)${e.theme ? `, theme ${e.theme} ${sdef.tip_themes.includes(e.theme) ? 'matches' : 'does not match'} the season` : ''}`);

    const copy = { ...e };
    for (const k of ['plain', 'bold', 'sub', 'line', 'eyebrow', 'caption', 'ask']) if (copy[k]) copy[k] = fill(copy[k], facts);
    if (copy.big) {
      const v = getFact(facts, copy.big);
      copy.bigDisplay = (copy.bigPrefix || '') + fmt(v);
    }
    const accent = ACCENT_FOR[slot.pillar] || 'orange'; // semantic, like AQ's accent_for(dept)
    const post = { day: slot.day, time: slot.time, pillar: slot.pillar, template: slot.template, accent, cta: slot.cta, copy: { ...copy }, copyId: e.id };

    post.style = pickStyle({ template: slot.template, seed: Math.floor(hash(week.id + slot.day) * 4294967296), ledger, nowN: week.n });
    log.push(`${slot.day} style: ${post.style.id} (${post.style.energy})${post.style.relaxed.length ? ', relaxed ' + post.style.relaxed.join(',') : ''}`);
    if (slot.template === 'paper-spotlight') {
      const seen = new Set(ledger.weeks.flatMap(w => w.posts.map(p => p.paperId)).filter(Boolean));
      const paper = facts.newPapers.find(p => !seen.has(p.id)) || facts.newPapers[0];
      post.paper = paper; post.paperId = paper.id; post.subject = paper.subject;
    }
    if (slot.template === 'subject-mosaic') {
      post.featuredSubject = subjOrder[subjPtr++ % 8]; post.subject = post.featuredSubject;
      post.subjectCounts = Object.fromEntries(facts.subjects.filter(s => s.papers != null).map(s => [s.name, fmt(s.papers)]));
    }
    if (slot.template === 'steps') {
      post.stepSubjects = [0, 1, 2].map(() => subjOrder[subjPtr++ % 8]);
      post.subject = post.stepSubjects[0];
    }
    if (slot.template === 'find-teacher' || slot.template === 'bento-board') {
      const s = pillars.search_examples, pick = (a, k) => a[Math.floor(hash(week.id + k) * a.length)];
      post.search = { subject: pick(s.subjects, 's'), cls: pick(s.classes, 'c'), area: pick(s.areas, 'a') };
    }
    const tags = [...new Set([...pillars.hashtags.core, ...(pillars.hashtags[slot.pillar] || [])])].slice(0, 8);
    post.hashtags = tags;
    post.caption = `${copy.caption}\n\n${slot.cta}: ${facts.constants.site}\n\n${tags.join(' ')}`;
    post.alt = `Shikshaq poster. ${copy.plain} ${copy.bold}${copy.sub ? ' ' + copy.sub : ''}`.replace(/\s+/g, ' ');
    posts.push(post);
  });
  return { week: week.id, season, posts, log };
}
