// Copy gates for the campaign. Same house rules as src/validate.mjs, plus the campaign's own:
// no invented numbers, "charity" only where the plan allows it, never as a first impression, no "connects families".
const BANNED = [
  [/[—–]/, 'em or en dash (site rule: none in copy)'],
  [/\b(guarantee[ds]?|cheapest|best (teacher|tutor)s?|top[- ]rated|number one|#1|100%)\b/i, 'unprovable superlative'],
  [/\b(thousands|lakhs?|millions?|trusted by|loved by|most popular|everyone)\b/i, 'unsourced social proof'],
  [/\b(ai[- ]powered|revolutionary|game[- ]chang\w+|unlock|supercharge)\b/i, 'brand-voice cliche'],
  [/\bconnect(s|ing)? famil(y|ies)\b/i, 'owner ruling: say "connecting every student in Kolkata to teachers", never "connects families"'],
  [/\bverified\b/i, 'owner ruling: say "checked and selected by our team", not "verified"'],
  [/\b(underprivileged|needy|poor children|slum|orphan)\b/i, 'the charity frame this campaign exists to remove'],
];
// Everything visible in a spec, found by walking it. Structure keys are skipped; copy keys are collected.
const TOP_SKIP = new Set(['id', 'family', 'dir', 'look', 'canvas', 'accent', 'ground', 'post', 'aud', 'tag', 'count', 'sticker', 'bind', 'gated', 'placeholder', 'subject', 'review', 'tutor', 'mascot', 'disc', 'mood', 'char', 'fill', 'phrase_', 'handle']);
const NEST_SKIP = new Set(['type', 'fill', 'tfill', 'tileFill', 'icon', 'kind', 'mood', 'c', 'rot', 'size', 'grow', 'tone', 'pay', 'valign', 'solid', 'cols', 'on', 'h', 'span', 'col', 'row', 'rows_', 'ordinal', 'who', 'msize', 'csize', 'fs', 'psize', 'hsize', 'plainW', 'top', 'photo', 'bind', 'eyebrowC', 'toggle', 'mascot', 'word']);
export function visible(spec) {
  const out = [];
  const walk = (v, key, top) => {
    if (typeof v === 'string') { if (v.trim() && !(top ? TOP_SKIP : NEST_SKIP).has(key)) out.push([key, v]); return; }
    if (Array.isArray(v) && key === 'lines') { v.forEach(l => { const t = (Array.isArray(l) ? l : [l]).map(g => typeof g === 'string' ? g : (g.b ?? g.hl ?? g.tag ?? g.pill ?? '')).join(' ').replace(/ ([?.,!])/g, '$1'); if (t.trim()) out.push(['lines', t]); }); return; }
    if (Array.isArray(v)) { if (key === 'tiles' && v.every(x => typeof x === 'string')) return; if (key === 'on') return; v.forEach(x => walk(x, key, false)); return; }
    if (v && typeof v === 'object') { if (key === 'mascot' || key === 'review' || key === 'tutor' || key === 'bind' || key === 'sticker' && top) return; for (const [k, x] of Object.entries(v)) walk(x, k, false); }
  };
  for (const [k, v] of Object.entries(spec)) if (!TOP_SKIP.has(k) || k === 'phrase') walk(v, k === 'phrase_' ? 'phrase' : k, true);
  if (spec.phrase) out.push(['phrase', spec.phrase]);
  return out;
}
const DIGIT_OK = /Class(es)? \d+|₹0|\b(FAQ|Tutors?|For tutors) 0\d/g;
const hasDigit = s => /\d/.test(s.replace(DIGIT_OK, ''));

// "charity" may appear only inside the plan's own correction beats.
const CHARITY_OK = /not a charity|a charity\?|charity or a class|some charity\?|charity class/i;
export function validateSpec(spec, { firstOfSequence = false } = {}) {
  const errors = [];
  for (const [k, s] of visible(spec)) {
    for (const [re, why] of BANNED) if (re.test(s)) errors.push(`${spec.id}.${k}: ${why}: "${s.slice(0, 60)}"`);
    if (hasDigit(s)) errors.push(`${spec.id}.${k}: a digit in copy, and the facts file holds no figure for it: "${s.slice(0, 60)}"`);
    if (/charity/i.test(s) && !CHARITY_OK.test(s)) errors.push(`${spec.id}.${k}: "charity" outside the allowed correction wording: "${s.slice(0, 60)}"`);
    if (/charity/i.test(s) && firstOfSequence) errors.push(`${spec.id}.${k}: the correction must never be the first thing a viewer sees: "${s.slice(0, 60)}"`);
  }
  for (const p of spec.panels || []) { const hl = (p.lines || []).map(l => (Array.isArray(l) ? l : [l]).map(g => typeof g === 'string' ? g : (g.b ?? g.hl ?? g.tag ?? g.pill ?? '')).join(' ')).join(' '); if (hl.length > 78) errors.push(`${spec.id}: a headline is ${hl.length} characters, cap is 78`); }
  return errors;
}
export function validateText(id, text, { cap = 900 } = {}) {
  const errors = [];
  for (const [re, why] of BANNED) if (re.test(text)) errors.push(`${id}: ${why}`);
  if (hasDigit(text.replace(/\[[^\]]*\]/g, ''))) errors.push(`${id}: a digit in copy`);
  if (text.length > cap) errors.push(`${id}: ${text.length} characters, cap is ${cap}`);
  return errors;
}
export function validateAll(items) {
  const errors = [], firsts = new Set(items.filter(i => /-1$/.test(i.id) || ['FQ0', 'FQ1', 'H1', 'H2', 'H3'].includes(i.id)).map(i => i.id));
  const ids = new Set();
  for (const it of items) {
    if (ids.has(it.id)) errors.push(`duplicate id ${it.id}`); ids.add(it.id);
    errors.push(...validateSpec(it, { firstOfSequence: firsts.has(it.id) }));
  }
  return errors;
}
