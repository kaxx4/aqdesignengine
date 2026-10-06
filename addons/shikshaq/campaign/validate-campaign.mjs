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
const SKIP = new Set(['id', 'family', 'dir', 'tag', 'count', 'look', 'canvas', 'accent', 'ground', 'post', 'aud', 'scheme', 'variant', 'mood', 'kind', 'fill', 'kickFill', 'disc', 'sticker', 'bind', 'gated', 'placeholder', 'subject', 'review', 'tutor', 'who', 'names', 'rot', 'char', 'valign', 'search', 'mascot', 'rows', 'notes', 'msgs', 'copy', 'lines', 'words', 'span', 'col', 'row']);
const SKIP_STRUCT = new Set(['rows', 'notes', 'msgs', 'copy', 'lines', 'words']);

const lineText = l => Array.isArray(l) ? l.map(s => typeof s === 'string' ? s : (s.b ?? s.tag ?? s.pill)).join(' ') : String(l);
export function visible(spec) {
  const out = [];
  const take = (k, v) => { if (typeof v === 'string' && v.trim()) out.push([k, v]); };
  for (const [k, v] of Object.entries(spec)) {
    if (SKIP.has(k) && !SKIP_STRUCT.has(k)) continue;
    if (typeof v === 'string') take(k, v);
  }
  (spec.lines || []).forEach(l => take('lines', lineText(l)));
  (spec.rows || []).forEach(r => take('rows', [r.pre, r.hl, r.post].filter(Boolean).join(' ')));
  (spec.notes || []).forEach(n => take('notes', n.t));
  (spec.msgs || []).forEach(m => take('msgs', m.t));
  (spec.words || []).forEach(w => take('words', w));
  if (spec.copy) Object.values(spec.copy).forEach(v => take('copy', v));
  return out;
}

// "charity" may appear only inside the plan's own correction beats.
const CHARITY_OK = /not a charity|a charity\?|charity or a class|some charity\?|charity class/i;
export function validateSpec(spec, { firstOfSequence = false } = {}) {
  const errors = [];
  for (const [k, s] of visible(spec)) {
    for (const [re, why] of BANNED) if (re.test(s)) errors.push(`${spec.id}.${k}: ${why}: "${s.slice(0, 60)}"`);
    if (/\d/.test(s)) errors.push(`${spec.id}.${k}: a digit in copy, and the facts file holds no figure for it: "${s.slice(0, 60)}"`);
    if (/charity/i.test(s) && !CHARITY_OK.test(s)) errors.push(`${spec.id}.${k}: "charity" outside the allowed correction wording: "${s.slice(0, 60)}"`);
    if (/charity/i.test(s) && firstOfSequence) errors.push(`${spec.id}.${k}: the correction must never be the first thing a viewer sees: "${s.slice(0, 60)}"`);
  }
  const hl = (spec.lines || []).map(lineText).join(' ');
  if (hl.length > 64) errors.push(`${spec.id}: headline is ${hl.length} characters, cap is 64`);
  return errors;
}
export function validateText(id, text, { cap = 900 } = {}) {
  const errors = [];
  for (const [re, why] of BANNED) if (re.test(text)) errors.push(`${id}: ${why}`);
  if (/\d/.test(text.replace(/\[[^\]]*\]/g, ''))) errors.push(`${id}: a digit in copy`);
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
