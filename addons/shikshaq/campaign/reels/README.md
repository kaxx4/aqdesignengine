# Reels

A reel is a list of beats: one spoken line over one card of panels (the same panel specs the posters use). Scripts live in `scripts.mjs`.

```
node campaign/reels/build-reels.mjs R1            render one reel to out/campaign-what-is-shikshaq/reels/R1.mp4
node campaign/reels/build-reels.mjs R1 --stills   also keep one still per beat
node campaign/reels/build-reels.mjs R1 --scratch  also make R1.scratch.mp4 with a local Kokoro guide voice (set KOKORO_DIR). Never shipped.
node campaign/reels/build-reels.mjs --scripts     write elevenlabs-scripts.md
```

## Adding the ElevenLabs voice
Generate one audio file per line from `elevenlabs-scripts.md` and save it as `campaign/reels/audio/<reel>/b01.mp3`, `b02.mp3` and so on.
Rebuild the reel: each beat then lasts as long as its file and the audio is mixed in. With no audio the beats are timed from their word count,
so a silent cut already has near-final pacing. An optional `b01.json` of `[{"w":"word","s":0.0,"e":0.3}]` gives exact caption timing.
No music is mixed in. Add trending audio inside Instagram.

Frames are drawn at exact times by the browser and piped to ffmpeg. Output is 1080x1920, 30 fps, h264. Captions sit above Instagram's bottom UI.
