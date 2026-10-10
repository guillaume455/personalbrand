#!/usr/bin/env python3
"""X-Bow mix, no music at all (Guillaume's call). The voice and the sound of the car: the raw GoPro sound if it is ever
supplied, else the synthetic engine of build-engine.py (assets/audio/engine.wav). With the GoPro sound: hook engine alone, cards and photos engine down, « balades » engine up front, lesson engine gone,
ducked under the voice (attack 200 ms, release 400 ms). Output 48 kHz stereo, -14 LUFS."""
import json, os, subprocess
from shots import SHOTS, RUSHES, SRC

os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open("timings.json")); TOTAL = T["total"]; F = {f["id"]: f for f in T["frames"]}
# The sound of « Chambord xbow 190715.mp4 » is the music of its original edit (it plays over the title cards and the
# still photos too): none of it is used. Only the raw GoPro sound would be the real engine: put it in RUSHES as
# <SRC>-son-reel.wav (same timeline as the video) and the rush segments come back on their own.
ENGINE_SRC = f"{RUSHES}/{SRC}-son-reel.wav"
HAS_REAL = os.path.exists(ENGINE_SRC)
BED = 140.0                                   # source time of the road bed (straight road, steady engine)
t0 = {s[0]: s[2] for lst in SHOTS.values() for s in lst}
media = json.load(open("media.json"))
db = lambda d: 10 ** (d / 20)
ENGINE = {"01-opportunite": 0, "02-cestquoi": -14, "03-balades": 0}
segs = [(cid, t0[cid], t, d, ENGINE.get(sc, -14)) for cid, t, d, sc in media] if HAS_REAL else []
# road bed under the photos and the cards (sound of the rush kept everywhere), gone for the lesson
hook_end = 3.0
first_cockpit = [t for cid, t, d, sc in media if cid == "cockpit"][0]
if HAS_REAL: segs += [("bed1", BED, hook_end, first_cockpit - hook_end, -16)]
if HAS_REAL: rev = F["04-revente"]; segs += [("bed2", BED + 20, rev["start"], rev["dur"], -20)]

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
ENGINE_WAV = "assets/audio/engine.wav"     # build-engine.py: the synthetic engine, wind and road on the film timeline
if not segs and os.path.exists(ENGINE_WAV):
    # the hook (engine alone) at -17 LUFS; the rest of the file keeps its levels relative to it
    out = subprocess.run(["ffmpeg", "-t", "3", "-i", ENGINE_WAV, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    hook_lufs = float(out.rsplit("I:", 1)[1].split("LUFS")[0])
    args += ["-i", ENGINE_WAV]
    fl = [f"[1:a]aresample=48000,volume={-17 - hook_lufs:.2f}dB[eng]"]
    segs = [("engine", 0, 0, TOTAL, 0)]
    f = ";".join(fl) + ";"
else:
    f = ""
if segs:
    if not f:
        f = ";".join(fl) + ";"
        f += "".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,apad=whole_dur={TOTAL}[eng];"
    f += f"[0]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={TOTAL},asplit[vo][key];"
    # the engine ducks under the voice, attack 200 ms, release 400 ms
    f += "[eng][key]sidechaincompress=threshold=0.03:ratio=4:attack=200:release=400[duck];"
    norm = "loudnorm=I=-14:TP=-1.5:LRA=11," if os.path.exists(VO) else ""   # no voice yet: keep the engine's own level
    f += f"[vo][duck]amix=inputs=2:normalize=0:duration=first,{norm}aresample=48000,alimiter=limit=0.85:level=false[out]"
elif os.path.exists(VO):
    f = f"[0]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={TOTAL},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.85:level=false[out]"
else:
    f = f"[0]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={TOTAL}[out]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", f, "-map", "[out]", "-t", str(TOTAL), "-ar", "48000",
                "-ac", "2", "assets/audio/mix.wav"], check=True)
src = "real sound" if HAS_REAL else "synthetic engine" if segs else "voice only"
print(f"mix: assets/audio/mix.wav ({src}, {TOTAL} s)")
