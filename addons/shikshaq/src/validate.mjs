// Copy gates. Run on the PLAN, before anything is drawn. Hard failures stop the week.
import { getFact, fmt } from './brain.mjs';

const BANNED = [
  [/[—–]/, 'em or en dash (site rule: none in copy)'],
  [/\b(guarantee[ds]?|cheapest|best (teacher|tutor)s?|top[- ]rated|number one|#1|100%)\b/i, 'unprovable superlative'],
  [/\b(thousands|lakhs?|millions?|trusted by|loved by|most popular|everyone)\b/i, 'unsourced social proof'],
  [/\b(ai[- ]powered|revolutionary|game[- ]chang\w+|unlock|supercharge)\b/i, 'brand-voice cliche'],
  [/\b(topper|toppers)\b/i, 'unsourced claim about toppers'],
];
const visibleStrings = post => {
  const c = post.copy, out = [c.plain, c.bold, c.sub, c.line, c.eyebrow, c.ask, c.bigLabel, c.bigDisplay, post.cta, post.caption, post.alt];
  (c.steps || []).forEach(s => out.push(s.t, s.b));
  return out.filter(Boolean);
};
function allowedNumbers(facts, post) {
  const ok = new Set(); // class numerals pass only in context ("Class 10"), see classCtx
  const add = v => { if (v != null) { ok.add(String(v)); if (typeof v === 'number') ok.add(fmt(v)); } };
  for (const k of ['teachers', 'papers', 'schools']) add(getFact(facts, 'counts.' + k));
  add(facts.constants.commission); add(facts.constants.freeQuestions);
  if (post.paper) { add(post.paper.cls); add(post.paper.year); }
  (facts.subjects || []).forEach(s => add(s.papers));
  return ok;
}
export function validatePlan(plan, facts, { dry = false } = {}) {
  const errors = [], warns = [];
  if (facts.mode === 'sample' && !dry) errors.push('sample facts used outside --dry: a real week needs live figures');
  if (facts.mode === 'sample') warns.push('SAMPLE FACTS: every number below is a stand-in for the dry run');
  for (const post of plan.posts) {
    const tag = `${post.day}/${post.template}`, ok = allowedNumbers(facts, post);
    for (const s of visibleStrings(post)) {
      for (const [re, why] of BANNED) if (re.test(s)) errors.push(`${tag}: ${why}: "${s.slice(0, 60)}"`);
      for (const m of s.matchAll(/₹?\d[\d,]*/g)) {
        const raw = m[0].replace('₹', '');
        const classCtx = new RegExp(`Class(es)? (${raw})\\b|\\b${raw} (Class|step)|IV to XII`).test(s);
        if (!ok.has(raw) && !ok.has(raw.replace(/,/g, '')) && !classCtx) errors.push(`${tag}: number "${raw}" does not trace to a fact: "${s.slice(0, 60)}"`);
      }
    }
    const hl = `${post.copy.plain} ${post.copy.bold}`;
    if (hl.length > 40) errors.push(`${tag}: headline ${hl.length} chars, cap is 40`);
    if (post.caption.length > 900) errors.push(`${tag}: caption ${post.caption.length} chars, cap is 900`);
    if (post.hashtags.length > 8) errors.push(`${tag}: ${post.hashtags.length} hashtags, cap is 8`);
  }
  const tpl = plan.posts.map(p => p.template), ac = plan.posts.map(p => p.accent);
  if (new Set(tpl).size < tpl.length) errors.push('two posts share a template this week');
  for (let i = 1; i < ac.length; i++) if (ac[i] === ac[i - 1]) warns.push(`${plan.posts[i].day}: same accent as the post before it`);
  return { errors, warns };
}
