#!/usr/bin/env python3
"""Places the voice montage on the film: the hook lasts HOOK seconds whatever the voice, so a silence is inserted after
« L'annonce que personne ne voulait. » for the next scene to start at HOOK. Rewrites assets/audio/voix-montage.wav and
the word timings (voix-montage-mots.json) in place, once (the json is marked « placed »).
Order: python3 build-voice.py && python3 align.py && python3 place-voice.py && python3 build.py && bash assemble.sh"""
import json, os, subprocess
from build import SCENES, scene_tokens, HOOK

WAV, JS = "assets/audio/voix-montage.wav", "assets/audio/voix-montage-mots.json"
d = json.load(open(JS, encoding="utf-8"))
if d.get("placed"):
    raise SystemExit("place-voice: already placed (re-run build-voice.py and align.py first)")
w = d["words"]
n1 = len(scene_tokens(SCENES[0]))
gap = HOOK + 0.10 - w[n1]["start"]          # scene 2 starts 0.10 s before its first word
if gap > 0:
    cut = (w[n1 - 1]["end"] + w[n1]["start"]) / 2
    for x in w[n1:]:
        x["start"] = round(x["start"] + gap, 3); x["end"] = round(x["end"] + gap, 3)
    g = (f"[0]atrim=0:{cut:.3f},asetpts=PTS-STARTPTS[a];"
         f"[0]atrim={cut:.3f},asetpts=PTS-STARTPTS,adelay={int(gap * 1000)}[b];[a][b]concat=n=2:v=0:a=1[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", WAV, "-filter_complex", g, "-map", "[out]", "-ar", "44100", "-ac", "1",
                    WAV + ".tmp.wav"], check=True)
    os.replace(WAV + ".tmp.wav", WAV)
    d["duration"] = round(d["duration"] + gap, 3)
d.update(words=w, placed=True)
json.dump(d, open(JS, "w"), ensure_ascii=False, indent=1)
print(f"voice placed: hook {HOOK} s ({max(gap, 0):.2f} s of silence after it), {d['duration']} s")
