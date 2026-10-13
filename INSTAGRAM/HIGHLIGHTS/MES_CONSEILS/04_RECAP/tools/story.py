#!/usr/bin/env python3
"""Builds one story of the « Mes conseils » highlight from the final export of a Reel.
Each passage is given in Reel seconds (approximate); both ends are snapped to the middle of the pause after a
sentence (voice word timings of the Reel), so a cut never falls inside a word. Passages that follow each other in the
Reel are joined as is; distant passages are joined by a 0.2 s cross-dissolve (image and sound). 40 ms audio fades on
every cut, 0.4 s fade out at the end, then the whole story is put back on -14 LUFS.
MASK=x:y:w:h:from erases, from <from> seconds of the story, a Reel overlay that means nothing outside the Reel (the
running TOTAL of pire-marge): delogo interpolates it from its edges, clean on the plain dark background.
Usage: [MASK=...] python3 story.py <reel folder> <out.mp4> <a-b> [<a-b> ...]     (run from the repository root)"""
import json, os, subprocess, sys

reel, out, spans = sys.argv[1], sys.argv[2], [tuple(map(float, s.split("-"))) for s in sys.argv[3:]]
SRC = f"{reel}/renders/" + {"jaguar": "jaguar.mp4", "porsche997": "porsche997.mp4", "xbow": "xbow.mp4"}.get(reel, f"reel-{reel}.mp4")
w = json.load(open(f"{reel}/assets/audio/voix-montage-mots.json"))["words"]
total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC],
                             capture_output=True, text=True).stdout)
# cut points: only the pauses that end a sentence (a word ending in . ? ! :), never inside a sentence
gaps = [0.0] + [(a["end"] + b["start"]) / 2 for a, b in zip(w, w[1:]) if a["w"].rstrip("~").endswith((".", "?", "!", ":", "…"))] + [total]


def snap(t):
    return min(gaps, key=lambda g: abs(g - t))


spans = [(snap(a), snap(b)) for a, b in spans]
# merge passages that touch in the Reel
merged = [list(spans[0])]
for a, b in spans[1:]:
    if abs(a - merged[-1][1]) < 0.05:
        merged[-1][1] = b
    else:
        merged.append([a, b])
X, F = 0.2, 0.04
fl, n = [], len(merged)
for i, (a, b) in enumerate(merged):
    # one input per passage, seeked: passages can come in any order without buffering the Reel in memory
    fl.append(f"[{i}:v]setpts=PTS-STARTPTS,fps=30,format=yuv420p[v{i}]")
    fl.append(f"[{i}:a]asetpts=PTS-STARTPTS,aresample=48000,"
              f"afade=t=in:d={F if i else 0.01},afade=t=out:st={b - a - F:.3f}:d={F}[a{i}]")
v, a, length = "v0", "a0", merged[0][1] - merged[0][0]
for i in range(1, n):
    off = length - X
    fl.append(f"[{v}][v{i}]xfade=transition=fade:duration={X}:offset={off:.3f}[vx{i}]")
    fl.append(f"[{a}][a{i}]acrossfade=d={X}:c1=tri:c2=tri[ax{i}]")
    v, a, length = f"vx{i}", f"ax{i}", off + merged[i][1] - merged[i][0]
if os.environ.get("MASK"):
    x, y, mw, mh, t0 = os.environ["MASK"].split(":")
    fl.append(f"[{v}]delogo=x={x}:y={y}:w={mw}:h={mh}:enable='gte(t,{t0})'[vm]"); v = "vm"
fl.append(f"[{a}]afade=t=out:st={length - 0.4:.3f}:d=0.4[aend]")
tmp = out + ".tmp.mp4"
ins = [x for a, b in merged for x in ("-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", SRC)]
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", f"[{v}]", "-map", "[aend]",
                "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
                "-c:a", "pcm_s16le", tmp], check=True)
# loudness: two-pass loudnorm to -14 LUFS, true peak -1.5
st = subprocess.run(["ffmpeg", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
m = json.loads(st[st.rindex("{"):st.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-c:v", "copy", "-af", ln + ",alimiter=limit=0.82:level=false,aresample=48000", "-c:a", "aac", "-b:a", "192k",
                "-ar", "48000", "-ac", "2", "-movflags", "+faststart", out], check=True)
subprocess.run(["rm", tmp])
print(out, " | ".join(f"{a:.2f}-{b:.2f}" for a, b in merged), f"-> {length:.2f} s")
