# Guide voice only: a local Kokoro model reads each beat so the pacing can be heard. The shipped voice is ElevenLabs.
import json, sys, os
import soundfile as sf
from kokoro_onnx import Kokoro
job = json.load(open(sys.argv[1]))
k = Kokoro(os.path.join(job['kdir'], 'kokoro.onnx'), os.path.join(job['kdir'], 'voices.bin'))
for i, t in enumerate(job['lines']):
    s, sr = k.create(t, voice=job['voice'], speed=1.0, lang='en-us')
    sf.write(os.path.join(job['out'], f'b{i+1:02d}.wav'), s, sr)
