// node campaign/reels/build-reels.mjs R1            render one reel
// node campaign/reels/build-reels.mjs R1 --stills   also keep one still per beat (for review without opening the video)
// node campaign/reels/build-reels.mjs R1 --scratch  also make <id>.scratch.mp4 with a Kokoro guide voice (NOT the final voice)
// node campaign/reels/build-reels.mjs --scripts     write every ElevenLabs script sheet and stop
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { REELS } from './scripts.mjs';
import { renderReel, beatPlan, wordsOf } from './engine.mjs';
import { validateText } from '../validate-campaign.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, '..', '..', 'out', 'campaign-what-is-shikshaq', 'reels');
const args = process.argv.slice(2), ids = args.filter(a => !a.startsWith('--')), flag = k => args.includes('--' + k);

const errors = [];
for (const r of Object.values(REELS)) for (const [i, b] of r.beats.entries()) errors.push(...validateText(`${r.id}.b${i + 1}`, b.say, { cap: 300 }));
if (errors.length) { console.error('COPY GATE FAILED\n' + errors.join('\n')); process.exit(1); }

// the sheet the voice person pastes from: one line per file, the exact name to save it under
export function writeScriptSheets() {
  fs.mkdirSync(OUT, { recursive: true });
  let all = '# ElevenLabs script sheets\n\nOne audio file per line. Save each as `campaign/reels/audio/<reel>/bNN.mp3` (NN is the line number below). The build re-times every beat to its file, so pacing follows the voice.\n\n**Settings to start from:** a calm, warm, young voice; stability about 45; speed 1.0; no background music (music is added in Instagram). Read numbers as words. Say "Shikshaq" as "shik-shack" (the last syllable like "shack"). Generate each line separately so a retake costs one line.\n\n';
  for (const r of Object.values(REELS)) {
    all += `## ${r.id}: ${r.title}\n\nVoice: ${r.voice}. ${r.notes || ''}\n\n| File | Line |\n|---|---|\n` + r.beats.map((b, i) => `| b${String(i + 1).padStart(2, '0')}.mp3 | ${b.say} |`).join('\n') + `\n\nEstimated length with no audio: ${beatPlan(r.id, r.beats).reduce((a, b) => a + b.dur, 0).toFixed(1)} seconds.\n\n`;
  }
  fs.writeFileSync(path.join(OUT, 'elevenlabs-scripts.md'), all);
  return path.join(OUT, 'elevenlabs-scripts.md');
}
if (flag('scripts') || !ids.length) { console.log('wrote', writeScriptSheets()); if (!ids.length) process.exit(0); }

// optional guide voice from Kokoro (a local model): only for hearing the pacing, never shipped
const KOKORO = process.env.KOKORO_DIR;
function guide(r) {
  if (!KOKORO || !fs.existsSync(path.join(KOKORO, 'v/bin/python'))) { console.log('no KOKORO_DIR, skipping the guide voice'); return null; }
  const dir = path.join(OUT, '_guide'); fs.mkdirSync(path.join(dir, r.id), { recursive: true });
  const job = path.join(dir, r.id + '.json'); fs.writeFileSync(job, JSON.stringify({ out: path.join(dir, r.id), lines: r.beats.map(b => b.say), voice: process.env.GUIDE_VOICE || 'af_heart', kdir: KOKORO }));
  const py = spawnSync(path.join(KOKORO, 'v/bin/python'), [path.join(HERE, 'guide-voice.py'), job], { encoding: 'utf8' });
  if (py.status) { console.error(py.stderr.slice(-400)); return null; }
  return dir;
}

for (const id of ids) {
  const r = REELS[id]; if (!r) { console.error('unknown reel', id); process.exit(1); }
  const t0 = Date.now();
  const scratch = flag('scratch') ? guide(r) : null;
  const res = await renderReel(r, OUT, { scratch, stills: flag('stills') });
  console.log(`${id}: ${res.total.toFixed(1)}s, ${res.plan.length} beats, ${((Date.now() - t0) / 1000).toFixed(0)}s to render -> ${res.final}${res.scratch ? ' and ' + res.scratch : ''}${res.plan.some(b => b.audio) ? '' : '  (silent: no ElevenLabs audio yet)'}`);
}
