#!/usr/bin/env python3
"""X-Bow mix: the rush's own sound under every clip (engine, wind: a car with no roof), a road bed under the photos and
cards, the voice. No music (Guillaume's call): only the real sound, ducked under the voice (attack 200 ms, release 400 ms).
Hook engine alone at full level; cards and photos engine down; « balades » engine up front; lesson: engine gone. Output 48 kHz stereo, -14 LUFS."""
import json, os, subprocess
from shots import SHOTS, RUSHES, SRC

os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open("timings.json")); TOTAL = T["total"]; F = {f["id"]: f for f in T["frames"]}
# the rush's own sound (note: the Chambord video was already edited with a music bed; the raw GoPro files would
# carry the engine alone: drop them in RUSHES and point ENGINE_SRC at them)
ENGINE_SRC = f"{RUSHES}/{SRC}.mp4"
BED = 140.0                                   # source time of the road bed (straight road, steady engine)
t0 = {s[0]: s[2] for lst in SHOTS.values() for s in lst}
media = json.load(open("media.json"))
db = lambda d: 10 ** (d / 20)
ENGINE = {"01-opportunite": 0, "02-cestquoi": -14, "03-balades": 0}
segs = [(cid, t0[cid], t, d, ENGINE.get(sc, -14)) for cid, t, d, sc in media]
# road bed under the photos and the cards (sound of the rush kept everywhere), gone for the lesson
hook_end = 3.0
first_cockpit = [t for cid, t, d, sc in media if cid == "cockpit"][0]
segs += [("bed1", BED, hook_end, first_cockpit - hook_end, -16)]
rev = F["04-revente"]; segs += [("bed2", BED + 20, rev["start"], rev["dur"], -20)]

VO = "assets/audio/voix-montage.wav"
args, fl, mix = [], [], []
if os.path.exists(VO):
    args += ["-i", VO]
else:
    args += ["-f", "lavfi", "-t", str(TOTAL), "-i", "anullsrc=r=48000:cl=mono"]
for k, (cid, src_t, film_t, d, g) in enumerate(segs):
    args += ["-ss", f"{src_t:.3f}", "-t", f"{d:.3f}", "-i", ENGINE_SRC]
    ms = int(film_t * 1000)
    fl.append(f"[{k + 1}:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.03,afade=t=out:st={max(0, d - 0.06):.3f}:d=0.06,"
              f"volume={db(g):.4f},adelay={ms}|{ms}[e{k}]")
    mix.append(f"[e{k}]")
f = ";".join(fl) + ";"
f += "".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,apad=whole_dur={TOTAL}[eng];"
f += f"[0]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={TOTAL},asplit[vo][key];"
# the rush's sound only (no music): it ducks under the voice, attack 200 ms, release 400 ms
f += "[eng][key]sidechaincompress=threshold=0.03:ratio=4:attack=200:release=400[duck];"
f += "[vo][duck]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.85:level=false[out]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", f, "-map", "[out]", "-t", str(TOTAL), "-ar", "48000",
                "-ac", "2", "assets/audio/mix.wav"], check=True)
print(f"mix: assets/audio/mix.wav ({len(segs)} rush segments from {os.path.basename(ENGINE_SRC)}, {TOTAL} s)")
