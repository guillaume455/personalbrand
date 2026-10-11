#!/usr/bin/env python3
"""Places the voice montage on the film: the hook lasts at least HOOK seconds (a silence after its line if needed), and
PAUSE_AFTER adds silences after the last word of a scene (the text card « je n'ai pas acheté un compteur » after the
Car-Pass). Rewrites assets/audio/voix-montage.wav and the word timings (voix-montage-mots.json) in place, once (the json
is marked « placed »).
Order: python3 build-voice.py && python3 align.py && python3 place-voice.py && python3 build.py && bash assemble.sh"""
import json, os, subprocess
from build import SCENES, scene_tokens, HOOK, PAUSE_AFTER

WAV, JS = "assets/audio/voix-montage.wav", "assets/audio/voix-montage-mots.json"
d = json.load(open(JS, encoding="utf-8"))
if d.get("placed"):
    raise SystemExit("place-voice: already placed (re-run build-voice.py and align.py first)")
w = d["words"]
ends, k = {}, 0
for sc in SCENES:
    k += len(scene_tokens(sc)); ends[sc["id"]] = k          # index of the first word after the scene
inserts = []                                                # (word index, seconds of silence before it)
n1 = ends[SCENES[0]["id"]]
if HOOK + 0.10 - w[n1]["start"] > 0:
    inserts.append((n1, HOOK + 0.10 - w[n1]["start"]))
inserts += [(ends[sid], sec) for sid, sec in PAUSE_AFTER.items()]
inserts.sort()
parts, cur, shift = [], 0.0, 0.0
for i, sec in inserts:
    cut = (w[i - 1]["end"] + w[i]["start"]) / 2
    parts.append((cur, cut, 0.0)); parts.append((None, None, sec)); cur = cut
parts.append((cur, None, 0.0))
for i, sec in inserts:
    for x in w[i:]:
        x["start"] = round(x["start"] + sec, 3); x["end"] = round(x["end"] + sec, 3)
fl, lab = [], []
for n, (a, b, sec) in enumerate(parts):
    if a is None:
        fl.append(f"aevalsrc=0:d={sec:.3f}:s=44100[s{n}]")
    else:
        fl.append(f"[0]atrim={a:.3f}" + (f":{b:.3f}" if b else "") + f",asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=mono[s{n}]")
    lab.append(f"[s{n}]")
g = ";".join(fl) + ";" + "".join(lab) + f"concat=n={len(parts)}:v=0:a=1[out]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", WAV, "-filter_complex", g, "-map", "[out]", "-ar", "44100", "-ac", "1",
                WAV + ".tmp.wav"], check=True)
os.replace(WAV + ".tmp.wav", WAV)
d.update(duration=round(d["duration"] + sum(s for _, s in inserts), 3), words=w, placed=True)
json.dump(d, open(JS, "w"), ensure_ascii=False, indent=1)
print("voice placed:", ", ".join(f"+{s:.2f} s before word {i}" for i, s in inserts), f"-> {d['duration']} s")
