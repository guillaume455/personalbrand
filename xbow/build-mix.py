#!/usr/bin/env python3
"""X-Bow mix: the voice, the music bed (low, ducked, none on the hook and the breath) and the sound of the car: the raw GoPro sound if it is ever
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
hook_end = HOOK_END = 3.0
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
# the music bed (« Running Night », alex_makemusic): none on the hook, low under the voice, almost gone on the 3 s
# breath, a little up on the last frame, faded out; ducked under the voice like the engine
MUSIC = "assets/music/musique.mp3"
MUS_IN = 0.6                                  # first note of the track (its file starts with silence)
bal = F["03-balades"]; les = F["05-lecon"]
words = json.load(open("assets/audio/voix-montage-mots.json"))["words"] if os.path.exists("assets/audio/voix-montage-mots.json") else []
last_word = words[-1]["end"] if words else TOTAL - 2.4
breath = [t for cid, t, d, sc in media if cid == "breath"][0]
M = [(0, -90), (HOOK_END - 0.05, -90), (HOOK_END + 0.25, -19), (breath - 0.2, -19), (breath + 0.4, -32), (bal["end"] - 0.3, -32),
     (bal["end"] + 0.3, -19), (last_word + 0.2, -19), (last_word + 0.6, -15), (TOTAL, -15)]


def ramp(points):
    """ffmpeg volume expression, piecewise linear in dB between the points"""
    e = f"{10 ** (points[-1][1] / 20):.6f}"
    for (a, da), (b, db_) in reversed(list(zip(points, points[1:]))):
        e = f"if(lt(t,{b:.3f}),pow(10,({da}+({db_}-({da}))*(t-{a:.3f})/{max(b - a, 1e-3):.3f})/20),{e})"
    return e


if segs:
    if not f:
        f = ";".join(fl) + ";"
        f += "".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,apad=whole_dur={TOTAL}[eng];"
    args += ["-i", MUSIC]
    m_idx = sum(1 for x in args if x == "-i") - 1
    f += f"[0]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={TOTAL},asplit=3[vo][key][key2];"
    f += (f"[{m_idx}:a]atrim={MUS_IN}:{MUS_IN + TOTAL},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
          f"adelay={int(HOOK_END * 1000)}|{int(HOOK_END * 1000)},atrim=0:{TOTAL},volume='{ramp(M)}':eval=frame,"
          f"afade=t=out:st={TOTAL - 1.8:.3f}:d=1.8[mus];")
    # engine and music duck under the voice, attack 200 ms, release 400 ms
    f += "[eng][key]sidechaincompress=threshold=0.03:ratio=4:attack=200:release=400[duck];"
    f += "[mus][key2]sidechaincompress=threshold=0.03:ratio=5:attack=200:release=400[mduck];"
    norm = "loudnorm=I=-14:TP=-1.5:LRA=11," if os.path.exists(VO) else ""   # no voice yet: keep the engine's own level
    f += f"[vo][duck][mduck]amix=inputs=3:normalize=0:duration=first,{norm}aresample=48000,alimiter=limit=0.85:level=false[out]"
elif os.path.exists(VO):
    f = f"[0]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={TOTAL},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.85:level=false[out]"
else:
    f = f"[0]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={TOTAL}[out]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", f, "-map", "[out]", "-t", str(TOTAL), "-ar", "48000",
                "-ac", "2", "assets/audio/mix.wav"], check=True)
src = "real sound" if HAS_REAL else "synthetic engine" if segs else "voice only"
print(f"mix: assets/audio/mix.wav ({src}, {TOTAL} s)")
if os.path.exists(VO):
    # one-pass loudnorm lands within a dB: a last gain puts the film on -14 LUFS
    out = subprocess.run(["ffmpeg", "-i", "assets/audio/mix.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    gain = -14 - float(out.rsplit("I:", 1)[1].split("LUFS")[0])
    if abs(gain) > 0.2:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/audio/mix.wav", "-af", f"volume={gain:.2f}dB,alimiter=limit=0.89:level=false",
                        "-ar", "48000", "-ac", "2", "assets/audio/mix.tmp.wav"], check=True)
        os.replace("assets/audio/mix.tmp.wav", "assets/audio/mix.wav")
        print(f"mix: gain {gain:+.2f} dB to -14 LUFS")
