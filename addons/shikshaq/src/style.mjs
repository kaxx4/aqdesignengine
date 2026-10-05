// Educated-random style draw, after the AQ engine's stylebank.pick(): every filter NARROWS and falls
// back rather than returning nothing, each relaxation is reported, weights make it educated not uniform,
// and a seed makes it reproducible. A style is choices inside the brand, never a way around it.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { DEFAULT_STYLE } from './kit.mjs';

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
export const loadBank = () => JSON.parse(fs.readFileSync(path.join(root, 'brain/style_bank.json'), 'utf8'));
export function rng(seed) { // mulberry32
  let t = seed >>> 0;
  return () => { t += 0x6D2B79F5; let x = Math.imul(t ^ (t >>> 15), 1 | t); x ^= x + Math.imul(x ^ (x >>> 7), 61 | x); return ((x ^ (x >>> 14)) >>> 0) / 4294967296; };
}
const SHAPES = ['squircle', 'flower', 'burst', 'cloud'], MOODS = ['calm', 'happy', 'wink', 'cheer'];
const shuffle = (a, r) => { const b = [...a]; for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };

// Hard brand rule, not a style choice (AQ's accent_for): the mode colours from VISUAL_LANGUAGE 2.2.
export const ACCENT_FOR = { papers: 'indigo', teachers: 'orange', tips: 'mint', trust: 'orange' };

export function pickStyle({ template, ground, energy, seed = 1, ledger = { weeks: [] }, nowN = 0, bank = loadBank() } = {}) {
  const r = rng(seed), relaxed = [];
  let pool = bank.styles;
  const narrow = (pred, label) => { const got = pool.filter(pred); if (got.length) pool = got; else relaxed.push(label); };
  if (template) narrow(s => s.templates === 'any' || s.templates.includes(template), `template=${template}`);
  if (ground) narrow(s => s.ground === ground, `ground=${ground}`);
  if (energy) narrow(s => s.energy === energy, `energy=${energy}`);
  // educated weights: the owner's base weight, a penalty for being used recently, a boost when a style is built FOR this template
  const recent = id => { let worst = 0; for (const w of ledger.weeks) for (const p of w.posts) if (p.style === id) worst = Math.max(worst, Math.max(0, 1 - Math.max(1, nowN - w.n) / 6)); return worst; };
  const weight = s => s.weight * (1 - 0.8 * recent(s.id)) * (Array.isArray(s.templates) ? 1.6 : 1);
  let acc = 0; const ws = pool.map(s => (acc += weight(s))); const x = r() * acc;
  const s = pool[ws.findIndex(w => x <= w)] || pool[0];
  return { ...realize(s, bank, r, seed), relaxed };
}

export function realize(s, bank, r, seed) {
  const k = bank.kits[s.kit];
  const kit = k.shapes === 'random'
    ? { shapes: shuffle(SHAPES, r), moods: shuffle(MOODS, r), rot: [0, 1, 2, 3].map(() => Math.round((r() * 2 - 1) * 10)) }
    : { shapes: k.shapes, moods: k.moods, rot: k.rot };
  return { ...DEFAULT_STYLE, id: s.id, ground: s.ground, cta: s.cta, radius: s.radius, flip: s.flip, shuffle: s.shuffle, stickerSign: s.stickerSign, kit, seed, mechanism: s.mechanism, recipe: s.recipe, energy: s.energy };
}
