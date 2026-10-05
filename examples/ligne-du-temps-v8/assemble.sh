#!/bin/bash
# Assemble ligne-du-temps-v8 (« La ligne du temps », the reference film of the method): storyboard statuses, HeyGen
# assembler + transitions (all cuts: continuity is made by the camera handoffs between sequences), then the
# orchestrator's own layer: the audio mix at the root (voice + music + SFX, 49.52 s, built by build-audio-v8.py), lint.
# Run it from anywhere: bash examples/ligne-du-temps-v8/assemble.sh (MIX=mix-v8-M1.wav for a tension option).
set -e
cd "$(dirname "$0")"
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
S=../../.claude/skills/product-launch-video/scripts
sed -i '' 's/^- status: outline$/- status: animated/' STORYBOARD.md
node $S/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes . | tail -3
node $S/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes . | tail -2
node $S/transitions.mjs verify --storyboard ./STORYBOARD.md --index ./index.html | tail -1
python3 - <<'PY'
import os, re
MIX = os.environ.get('MIX', 'mix-v8.wav')
p = 'index.html'; s = open(p).read()
last = [m.start() for m in re.finditer(r'data-composition-id="', s)][-1]
end = s.index('></div>', last) + len('></div>')
dur = re.search(r'data-duration="([0-9.]+)"', s[s.index('<div id="root"') if '<div id="root"' in s else 0:]).group(1)
audio = '''
      <audio id="mix" data-start="0" data-duration="''' + dur + '''" data-track-index="11" src="assets/audio/''' + MIX + '''" data-volume="1"></audio>
'''
s = s[:end] + audio + s[end:]
open(p, 'w').write(s)
print('orchestrator layer patched (audio ' + MIX + ', ' + dur + ' s)')
PY
npx hyperframes lint 2>&1 | grep -E "✗|error\(s\)"
