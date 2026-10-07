// Each assertion reproduces a failure this campaign build hit or exists to prevent. ONE pass banner, at the end.
import fs from 'node:fs';
import { chromium } from 'playwright-core';
import { CHROME, gate } from '../src/render.mjs';
import { L } from './catalog-util.mjs';
import { ITEMS, byId, expand } from './catalog.mjs';
import { WEEKS, RESERVE } from './plan.mjs';
import { PUSHES } from './wa.mjs';
import { CAPTIONS, HASHTAGS } from './captions.mjs';
import { validateSpec, validateAll, validateText } from './validate-campaign.mjs';
import { resolveItem, fillTokens } from './resolve.mjs';
import { pickSubject, byline, rows } from './wire-data.mjs';
import { feedPosts } from './texts.mjs';

let n = 0;
const ok = (c, m) => { n++; if (!c) { console.error(`FAIL ${n}: ${m}`); process.exit(1); } };
const bad = (spec, first = false) => validateSpec({ id: 'X', lines: [], ...spec }, { firstOfSequence: first });

// 1-9 the copy gate
ok(bad({ support: 'Learn — fast' }).some(e => /dash/.test(e)), 'an em dash must fail');
ok(bad({ support: 'Free for 3 families' }).some(e => /digit/.test(e)), 'a digit with no fact behind it must fail');
ok(bad({ support: 'Shikshaq connects families with tutors' }).some(e => /connects families|connecting every student/.test(e)), 'the owner banned "connects families"');
ok(bad({ support: 'Every tutor is verified' }).some(e => /verified/.test(e)), 'the owner ruled "verified" out in favour of "checked and selected"');
ok(bad({ support: 'Trusted by everyone' }).length >= 1, 'unsourced social proof must fail');
ok(bad({ support: 'A charity for poor children' }).length >= 1, 'the charity frame must not leak in');
ok(bad({ q: 'Is it a charity?' }).length === 0, 'the plan\'s own correction wording must pass');
ok(bad({ q: 'Is it a charity?' }, true).some(e => /first thing/.test(e)), 'the correction must never be the first thing a viewer sees');
ok(bad({ panels: [{ lines: [['x'.repeat(90)]] }] }).some(e => /headline/.test(e)), 'an over-long headline must fail');

// 10-11 the headline mini-language caught a real bug: a bold run split across two lines leaked a literal asterisk
let threw = false; try { L('Asked around. / *Got a number / that does not work.*'); } catch { threw = true; }
ok(threw, 'a bold run spanning two lines must be an error, not a literal asterisk on the poster');
ok(L('a / *b* / [c] d / {e}').length === 4 && L('x [t|#FFC700]')[0][1].fill === '#FFC700', 'the mini-language must read bold, tag, pill and a tag fill');

// 12-17 data binding: never invent copy, never ship a placeholder as final
const rev = byId('RV1'), tut = byId('MT1');
ok(resolveItem(rev, { reviews: [] }).placeholder === true, 'a review slot with no data must be a DRAFT');
ok(resolveItem(rev, { reviews: [{ id: 'r1', text: 'Real words.', first: 'A.', subject: 'Maths' }] }).placeholder === false, 'a review with a source id fills the slot');
ok(resolveItem(rev, { reviews: [{ text: 'No id, so no provenance.' }] }).placeholder === true, 'a review without a source id must not pass as real');
ok(resolveItem(tut, { tutors: [{ name: 'T', subject: 'Maths', quote: 'q', approved: false }] }).placeholder === true, 'a tutor who has not approved the post must stay a DRAFT');
ok(resolveItem(tut, { tutors: [{ name: 'T', subject: 'Maths', quote: 'q', approved: true }] }).placeholder === false, 'an approved tutor fills the slot');
ok(fillTokens('Hi {{review.0.text}}', { reviews: [] }).missing.length === 1, 'a WhatsApp token with no data must be reported missing');

// 18-24 the catalog is internally consistent
ok(new Set(ITEMS.map(i => i.id)).size === ITEMS.length, 'asset ids must be unique');
ok(validateAll(ITEMS).length === 0, 'the whole catalog must pass the copy gate: ' + validateAll(ITEMS).slice(0, 3).join(' | '));
const planned = WEEKS.flatMap(w => w.days.flatMap(d => [d.feed, ...(d.feed2 ? [d.feed2] : []), ...(d.stories || [])])).concat(RESERVE);
ok(planned.every(t => /best performing/.test(t) || expand(t).length), 'every plan token must name a real asset or post: ' + planned.filter(t => !expand(t).length).join(','));
ok(WEEKS.length === 4 && WEEKS.every(w => w.days.length === 7), 'a four-week plan with seven days each');
ok(PUSHES.every(p => p.image.every(id => byId(id))), 'every WhatsApp push must name real images');
ok(feedPosts().every(p => CAPTIONS[p]), 'every feed post needs a caption: ' + feedPosts().filter(p => !CAPTIONS[p]).join(','));
ok(Object.values(CAPTIONS).every(c => validateText('c', c).length === 0) && Object.values(HASHTAGS).every(a => a.length <= 8), 'captions must pass the gate and stay under the hashtag cap');
ok(ITEMS.filter(i => i.canvas === 'S').length === 101 && ITEMS.filter(i => i.canvas === 'C').length === 9 && ITEMS.length === 240, 'the catalog totals drifted from the signed-off list (240: 101 stories, 9 covers)');
// the plan and the pushes must agree about who sends what, when
const dayOf = Object.fromEntries(WEEKS.flatMap(w => w.days.flatMap(d => (d.wa || []).map(id => [id, `${w.n} ${d.d}`]))));
ok(PUSHES.every(p => dayOf[p.id] === `${p.week} ${p.day}`), 'every WhatsApp push must sit on the plan day it names: ' + PUSHES.filter(p => dayOf[p.id] !== `${p.week} ${p.day}`).map(p => p.id).join(','));
ok(Object.keys(dayOf).every(id => PUSHES.some(p => p.id === id)), 'the plan names a WhatsApp push that does not exist');
const allTok = WEEKS.flatMap(w => w.days.flatMap(d => [d.feed, ...(d.feed2 ? [d.feed2] : []), ...(d.stories || [])])).concat(RESERVE);
ok(new Set(allTok).size === allTok.length, 'an asset sits in two plan slots: ' + allTok.filter((t, i) => allTok.indexOf(t) !== i).join(','));
ok(WEEKS.every(w => w.days.every(d => d.feed)), 'every day has a main feed post');
ok(WEEKS.flatMap(w => w.days).every(d => !d.feed2 || d.feed2 !== d.feed), 'a day cannot repeat its own post');

// 25-28 the data importer
ok(pickSubject('Mathematics, Physics') === 'Maths' && pickSubject('Biology') === 'Maths', 'subject mapping falls back to Maths rather than inventing one');
ok(byline({ full_name: 'Riya Sen', is_anonymous: false }, 'initial') === 'R.', 'a reviewer who is a school student shows as an initial by default');
ok(byline({ full_name: 'Riya Sen', is_anonymous: true }, 'first') === 'A parent', 'an anonymous review must stay anonymous in every mode');
ok(Array.isArray(rows('/nonexistent')) === false, 'a missing export reads as null, not an empty success');

// 29-30 the story safe zone caught nothing before it existed
const b = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
const pg = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await pg.setContent('<body style="margin:0"><div class="p" style="position:relative;width:1080px;height:1920px"><div style="position:absolute;left:100px;top:120px;font-size:60px">Under the story header</div><div style="position:absolute;left:100px;top:900px;font-size:60px">Safe</div></div></body>');
const issues = await pg.evaluate(`(${gate.toString()})(1080,1920,{top:250,bottom:340},.16)`);
ok(issues.some(i => /SAFE-ZONE.*Under the story/.test(i)), 'text under the story header must report SAFE-ZONE');
ok(!issues.some(i => /SAFE-ZONE.*"Safe"/.test(i)), 'text inside the safe zone must not');
await b.close();

console.log(`ALL ${n} ASSERTIONS PASSED`);
