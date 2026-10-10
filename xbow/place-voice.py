#!/usr/bin/env python3
"""Places the voice montage on the film: HOOK seconds of silence before the first word (the hook: engine alone) and
BREATH seconds after the last word of « les balades » (3 s of engine alone). Rewrites assets/audio/voix-montage.wav and
the word timings (voix-montage-mots.json) in place, once (the json is marked « placed »).
Order: python3 build-voice.py && python3 align.py && python3 place-voice.py && python3 build.py && bash assemble.sh"""
import json, subprocess
from build import SCENES, scene_tokens, HOOK, BREATH

WAV, JS = "assets/audio/voix-montage.wav", "assets/audio/voix-montage-mots.json"
d = json.load(open(JS, encoding="utf-8"))
if d.get("placed"):
    raise SystemExit("place-voice: already placed (re-run build-voice.py and align.py first)")
w = d["words"]
n3 = sum(len(scene_tokens(sc)) for sc in SCENES[:3])           # words up to the end of « les balades »
cut = (w[n3 - 1]["end"] + w[n3]["start"]) / 2                  # in the middle of the pause after it
for i, x in enumerate(w):
    sh = HOOK + (BREATH if i >= n3 else 0)
    x["start"] = round(x["start"] + sh, 3); x["end"] = round(x["end"] + sh, 3)
g = (f"[0]atrim=0:{cut:.3f},asetpts=PTS-STARTPTS,adelay={int(HOOK * 1000)}[a];"
     f"[0]atrim={cut:.3f},asetpts=PTS-STARTPTS,adelay={int(BREATH * 1000)}[b];[a][b]concat=n=2:v=0:a=1[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", WAV, "-filter_complex", g, "-map", "[out]", "-ar", "44100", "-ac", "1",
                WAV + ".tmp.wav"], check=True)
import os
os.replace(WAV + ".tmp.wav", WAV)
d.update(duration=round(d["duration"] + HOOK + BREATH, 3), words=w, placed=True)
json.dump(d, open(JS, "w"), ensure_ascii=False, indent=1)
print(f"voice placed: +{HOOK} s before, +{BREATH} s after « {w[n3 - 1]['w']} » ({cut:.2f} s), {d['duration']} s")
