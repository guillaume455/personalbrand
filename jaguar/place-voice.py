#!/usr/bin/env python3
"""Places the voice montage on the film: the chunks marked ✂ in SCENES (said in the recording, cut for length) are
taken out, the hook lasts at least HOOK seconds (a silence after its line if needed), and PAUSE_AFTER adds silences
after the last word of a scene. Rewrites assets/audio/voix-montage.wav and the word timings (voix-montage-mots.json) in place, once (the json
is marked « placed »).
Order: python3 build-voice.py && python3 align.py && python3 place-voice.py && python3 build.py && bash assemble.sh"""
import json, os, subprocess
from build import SCENES, scene_tokens, HOOK, PAUSE_AFTER, CUT

WAV, JS = "assets/audio/voix-montage.wav", "assets/audio/voix-montage-mots.json"
d = json.load(open(JS, encoding="utf-8"))
if d.get("placed"):
    raise SystemExit("place-voice: already placed (re-run build-voice.py and align.py first)")
w = d["words"]


def render(parts, src, dst):
    """parts: [(a, b) source span | (None, seconds) silence] -> dst"""
    fl, lab = [], []
    for n, (a, b) in enumerate(parts):
        if a is None:
            fl.append(f"aevalsrc=0:d={b:.3f}:s=44100[s{n}]")
        else:
            fl.append(f"[0]atrim={a:.3f}" + (f":{b:.3f}" if b else "") + f",asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=mono[s{n}]")
        lab.append(f"[s{n}]")
    g = ";".join(fl) + ";" + "".join(lab) + f"concat=n={len(parts)}:v=0:a=1[out]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", g, "-map", "[out]", "-ar", "44100", "-ac", "1", dst], check=True)


# 1. the cut chunks (✂): said in the recording, taken out of the film, cut in the middle of the pauses around them
flags = [ch.startswith(CUT) for sc in SCENES for ch in sc["chunks"] for t in ch.lstrip(CUT).split(" ") if t]
assert len(flags) == len(w), "place-voice: the word timings do not carry the text of SCENES (re-run align.py)"
runs, i = [], 0
while i < len(w):
    if flags[i]:
        j = i
        while j + 1 < len(w) and flags[j + 1]: j += 1
        runs.append((i, j)); i = j + 1
    else:
        i += 1
cut_total = 0.0
if runs:
    parts, cur, removed = [], 0.0, []
    for i0, i1 in runs:
        a = (w[i0 - 1]["end"] + w[i0]["start"]) / 2 if i0 else 0.0
        b = (w[i1]["end"] + w[i1 + 1]["start"]) / 2 if i1 + 1 < len(w) else d["duration"]
        parts.append((cur, a)); removed.append((a, b)); cur = b
    parts.append((cur, None))
    render(parts, WAV, WAV + ".tmp.wav"); os.replace(WAV + ".tmp.wav", WAV)
    keep = []
    for k, x in enumerate(w):
        if flags[k]:
            continue
        sh = sum(b - a for a, b in removed if b <= x["start"] + 1e-6)
        keep.append({**x, "start": round(x["start"] - sh, 3), "end": round(x["end"] - sh, 3)})
    cut_total = sum(b - a for a, b in removed)
    w = keep; d["duration"] = round(d["duration"] - cut_total, 3)
    print(f"cut: {len(runs)} passages, {cut_total:.2f} s")

# 2. silences: the hook held, the pauses after some scenes
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
if inserts:
    render([(a, b) if a is not None else (None, sec) for a, b, sec in parts], WAV, WAV + ".tmp.wav")
    os.replace(WAV + ".tmp.wav", WAV)
d.update(duration=round(d["duration"] + sum(s for _, s in inserts), 3), words=w, placed=True)
json.dump(d, open(JS, "w"), ensure_ascii=False, indent=1)
print("voice placed:", ", ".join(f"+{s:.2f} s before word {i}" for i, s in inserts), f"-> {d['duration']} s")
