// Reel engine. A reel is a list of BEATS. Each beat is one spoken line over one card of panels (the same panel specs the posters use).
// Frames are drawn by the browser at an exact time t (nothing runs on its own clock), piped to ffmpeg, and muxed with audio when it exists.
//   Audio: reels/audio/<reel>/b01.mp3 ... one file per beat (ElevenLabs). A beat lasts as long as its audio. With no audio the beat is timed
//   from its word count, so a silent cut already has the final pacing. Optional reels/audio/<reel>/b01.json = [{w,s,e}] word times in seconds.
import fs from 'node:fs';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright-core';
import { CHROME } from '../../src/render.mjs';
import { page, frame, esc } from '../../src/kit.mjs';
import { stackLook } from '../stack.mjs';
import { BONE, INK, ORANGE, INDIGO, MINT_SOLID, ACC } from '../kit3.mjs';
import { textOn } from '../../src/tokens.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const AUDIO = path.join(HERE, 'audio');
export const W = 1080, H = 1920, FPS = 30, CARD_Y = 210, CARD_H = 1130, CAP_Y = 1380;
const WPS = 2.55;                       // words per second for the silent estimate (ElevenLabs reads about 2.4 to 2.8)

export const wordsOf = t => t.trim().split(/\s+/).filter(Boolean);
export const probe = f => { const r = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], { encoding: 'utf8' }); return parseFloat(r.stdout) || 0; };
export const audioOf = (reel, i) => { const b = path.join(AUDIO, reel, `b${String(i + 1).padStart(2, '0')}`); const f = ['.mp3', '.wav', '.m4a'].map(e => b + e).find(fs.existsSync); return f ? { file: f, dur: probe(f), words: fs.existsSync(b + '.json') ? JSON.parse(fs.readFileSync(b + '.json', 'utf8')) : null } : null; };

// word times inside a beat: real ones if given, else spread by character weight across the speech
export function wordTimes(text, speechDur, lead, real) {
  if (real) return real.map(x => ({ w: x.w, s: lead + x.s, e: lead + x.e }));
  const ws = wordsOf(text), wt = ws.map(w => w.length + 2), tot = wt.reduce((a, b) => a + b, 0);
  let t = lead; return ws.map((w, i) => { const d = speechDur * wt[i] / tot, o = { w, s: t, e: t + d }; t += d; return o; });
}

export function beatPlan(reel, beats) {
  return beats.map((b, i) => {
    const a = audioOf(reel, i), lead = .3, tail = b.tail ?? .45;
    const speech = a ? a.dur : Math.max(1.1, wordsOf(b.say).length / WPS);
    return { ...b, i, audio: a, lead, speech, dur: lead + speech + tail, words: wordTimes(b.say, speech, lead, a?.words) };
  });
}

function pageFor(beat, accent, total) {
  const A = ACC[accent] || ACC.orange, F = frame(accent);
  const L = { W, H: CARD_H, canvas: 'R', story: false, Q: false, safe: null };
  const spec = { id: 'reel', accent, panels: beat.panels, handle: false, decor: false };
  const inner = stackLook(spec, L, F);
  const capFill = A.a, capFg = textOn(capFill);
  const css = `<style>
#card{position:absolute;left:0;top:${CARD_Y}px;width:${W}px;height:${CARD_H}px;border-radius:44px;overflow:hidden;background:${BONE};box-shadow:0 0 0 3px ${INK},10px 12px 0 ${INK}}
#card .stack{border-radius:44px}
svg.a{animation:bob 2.6s ease-in-out infinite}
@keyframes bob{0%,100%{translate:0 0}50%{translate:0 -16px}}
#cap{position:absolute;left:40px;width:${W - 80}px;top:${CAP_Y}px;height:150px;display:flex;flex-wrap:nowrap;gap:6px 12px;align-items:center;justify-content:center;font:900 62px/1 Archivo,Geist,sans-serif;font-stretch:112%;letter-spacing:-.04em;color:${INK};text-align:center}
#cap span{display:inline-block;padding:2px 18px 8px;border-radius:26px;transition:none}
#cap span.on{background:${capFill};color:${capFg};box-shadow:0 0 0 3px ${INK},5px 6px 0 ${INK}}
</style>`;
  const body = `${css}<div id="card">${inner}</div><div id="cap"></div>`;
  const words = beat.words.map(x => x.w);
  const chunks = []; let cur = [];
  beat.words.forEach((x, k) => { cur.push(k); if (cur.length >= 4 || /[.?!,:]$/.test(x.w)) { chunks.push(cur); cur = []; } });
  if (cur.length) chunks.push(cur);
  const js = `<script>(function(){
var BEAT=${JSON.stringify({ words: beat.words, chunks, dur: beat.dur })};
var EOB=function(x){return 1-Math.pow(1-x,3)};var BACK=function(x){var c=1.35;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
var cl=function(x){return Math.max(0,Math.min(1,x))};
function items(){var pn=[].slice.call(document.querySelectorAll('.pn'));return pn.map(function(p){return{p:p,kids:[].slice.call(p.children).filter(function(c){return getComputedStyle(c).position!=='absolute'}),lines:[].slice.call(p.querySelectorAll('[data-tag=headline]>div'))}})}
var IT=null;
window.__t=function(t){
 if(!IT)IT=items();
 IT.forEach(function(o,i){var r=.12+i*.24,p=cl((t-r)/.5),e=BACK(p);
  o.p.style.transform='translateY('+((1-e)*1500)+'px)';o.p.style.opacity=p>0?1:0;
  o.kids.forEach(function(k,j){var rr=r+.3+j*.16,q=cl((t-rr)/.4);if(k.getAttribute('data-tag')==='headline')return;k.style.opacity=q;k.style.transform='translateY('+((1-EOB(q))*40)+'px)'});
  o.lines.forEach(function(l,j){var rr=r+.25+j*.18,q=cl((t-rr)/.42);l.style.opacity=q;l.style.transform='translateY('+((1-EOB(q))*46)+'px)'});
 });
 document.getAnimations().forEach(function(a){try{a.pause();a.currentTime=t*1000}catch(e){}});
 var cap=document.getElementById('cap'),ch=null,k=-1;
 for(var i=0;i<BEAT.words.length;i++){if(t>=BEAT.words[i].s)k=i}
 if(k>=0){for(var c=0;c<BEAT.chunks.length;c++){if(BEAT.chunks[c].indexOf(k)>=0)ch=BEAT.chunks[c]}}
 var h='';if(ch)ch.forEach(function(w){var a=BEAT.words[w],on=(t>=a.s&&t<a.e+.05);var pop=on?1+.06*Math.sin(cl((t-a.s)/.18)*Math.PI):1;h+='<span class="'+(on?'on':'')+'" style="transform:scale('+pop+')">'+a.w.replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</span>'});
 if(cap.dataset.h!==h){cap.innerHTML=h;cap.dataset.h=h}
 else if(ch){[].slice.call(cap.children).forEach(function(s,n){var a=BEAT.words[ch[n]];var on=(t>=a.s&&t<a.e+.05);var pop=on?1+.06*Math.sin(cl((t-a.s)/.18)*Math.PI):1;s.style.transform='scale('+pop+')'})}
};
})();</script>`;
  return page(W, H, body, BONE).replace('<script>', '<script>window.__fitTol=.16;</script><script>').replace('</body>', `${js}</body>`);
}

// Render one reel to out/<id>.mp4 (silent when there is no audio) and, with scratch, <id>.scratch.mp4 carrying the guide voice.
export async function renderReel(reel, outDir, { scratch = null, fps = FPS, onlyBeat = null, stills = false } = {}) {
  const plan = beatPlan(reel.id, reel.beats);
  fs.mkdirSync(outDir, { recursive: true });
  const total = plan.reduce((a, b) => a + b.dur, 0);
  const silent = path.join(outDir, `${reel.id}.silent.mp4`);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'fast', '-movflags', '+faststart', silent], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise(r => ff.on('close', r));
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const stillDir = stills ? path.join(outDir, `${reel.id}-stills`) : null; if (stillDir) fs.mkdirSync(stillDir, { recursive: true });
  try {
    for (const b of plan) {
      if (onlyBeat != null && b.i !== onlyBeat) continue;
      const pg = await ctx.newPage();
      await pg.setContent(pageFor(b, b.accent || reel.accent, total), { waitUntil: 'load' });
      await pg.evaluate(() => document.fonts.ready);
      await pg.waitForFunction(() => document.body.getAttribute('data-ready') === '1', null, { timeout: 8000 }).catch(() => {});
      const n = Math.round(b.dur * fps);
      for (let f = 0; f < n; f++) {
        const t = f / fps; await pg.evaluate(t => window.__t(t), t);
        const buf = await pg.screenshot({ type: 'jpeg', quality: 92 });
        if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
        if (stillDir && (f === Math.round(n * .55))) fs.writeFileSync(path.join(stillDir, `b${String(b.i + 1).padStart(2, '0')}.jpg`), buf);
      }
      await pg.close();
    }
  } finally { ff.stdin.end(); await done; await browser.close(); }

  // audio: place each beat's file at the beat's start; with no files there is no audio stream
  const mux = (tracks, out) => {
    const args = ['-y', '-loglevel', 'error', '-i', silent]; const fl = [];
    tracks.forEach((t, k) => { args.push('-i', t.file); fl.push(`[${k + 1}:a]adelay=${Math.round(t.at * 1000)}|${Math.round(t.at * 1000)}[a${k}]`); });
    fl.push(tracks.map((_, k) => `[a${k}]`).join('') + `amix=inputs=${tracks.length}:normalize=0[aout]`);
    args.push('-filter_complex', fl.join(';'), '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', out);
    const r = spawnSync('ffmpeg', args, { encoding: 'utf8' }); if (r.status) throw new Error(r.stderr);
  };
  let at = 0; const real = [], guide = [];
  for (const b of plan) { if (b.audio) real.push({ file: b.audio.file, at: at + b.lead }); if (scratch && fs.existsSync(path.join(scratch, reel.id, `b${String(b.i + 1).padStart(2, '0')}.wav`))) guide.push({ file: path.join(scratch, reel.id, `b${String(b.i + 1).padStart(2, '0')}.wav`), at: at + b.lead }); at += b.dur; }
  const outputs = { silent, total };
  if (real.length) { outputs.final = path.join(outDir, `${reel.id}.mp4`); mux(real, outputs.final); }
  else { outputs.final = path.join(outDir, `${reel.id}.mp4`); fs.copyFileSync(silent, outputs.final); }
  if (guide.length) { outputs.scratch = path.join(outDir, `${reel.id}.scratch.mp4`); mux(guide, outputs.scratch); }
  return { plan, ...outputs };
}
