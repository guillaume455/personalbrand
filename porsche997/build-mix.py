#!/usr/bin/env python3
"""Mix of the Porsche reel: Guillaume's voice, the music bed and the sound effects (assets/audio/sfx-events.json,
written by build.py). The music supports and never leads: tension that rises during the warnings (it opens from a
muffled low-pass to full and comes up), a breath on the turnaround (back down, muffled), a steady bed under the
facts, a complete fall on the lesson (gone), and the CTA in silence. It ducks under the voice (attack 200 ms, release
400 ms). Output assets/audio/mix.wav, 48 kHz stereo, -14 LUFS once the voice is there.
Usage: python3 build-mix.py (MUS_START=<s> to start the track elsewhere)"""
import json, os, subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open("timings.json")); TOTAL = float(T["total"]); F = {f["id"]: f for f in T["frames"]}
VO = "assets/audio/voix-montage.wav"
MUSIC = "assets/music/musique.mp3"
SFX = "../.claude/skills/media-use/audio/assets/sfx"
MUS_START = float(os.environ.get("MUS_START", "0.0"))
w, r, les = F["02-warnings"], F["03-retournement"], F["09-lecon"]

# music level (dB) and « openness » (0 = muffled low-pass, 1 = full) along the film, piecewise linear
LEVEL = [(0, -90), (w["start"] - 0.3, -90), (w["start"] + 0.4, -24), (w["end"] - 0.5, -15), (r["start"] + 0.6, -25),
         (r["end"] - 0.6, -25), (r["end"] + 0.4, -19), (les["start"] - 0.2, -19), (les["start"] + 1.6, -90), (TOTAL, -90)]
OPEN = [(0, 0), (w["start"], 0), (w["end"] - 0.5, 1), (r["start"] + 0.6, 0.15), (r["end"] - 0.6, 0.15), (r["end"] + 0.4, 1), (TOTAL, 1)]


def lin(points, db=False):
    """ffmpeg expression of a piecewise-linear curve over t (in dB -> gain when db)"""
    val = (lambda x: f"pow(10,({x})/20)") if db else (lambda x: f"({x})")
    e = val(points[-1][1])
    for (a, va), (b, vb) in reversed(list(zip(points, points[1:]))):
        e = f"if(lt(t,{b:.3f}),{val(f'{va}+({vb}-({va}))*(t-{a:.3f})/{max(b - a, 1e-3):.3f}')},{e})"
    return e


lvl, opn = lin(LEVEL, db=True), lin(OPEN)
has_vo = os.path.exists(VO)
args = ["-i", VO] if has_vo else ["-f", "lavfi", "-t", str(TOTAL), "-i", "anullsrc=r=48000:cl=mono"]
args += ["-i", MUSIC]
events = json.load(open("assets/audio/sfx-events.json"))
fl = [f"[0]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={TOTAL},asplit=2[vo][key]",
      f"[1]atrim={MUS_START}:{MUS_START + TOTAL},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,asplit=2[ma][mb]",
      f"[ma]lowpass=f=900:p=2,volume='{lvl}*(1-{opn})':eval=frame[m1]",
      f"[mb]volume='{lvl}*{opn}':eval=frame[m2]",
      "[m1][m2]amix=inputs=2:normalize=0[mus]",
      "[mus][key]sidechaincompress=threshold=0.025:ratio=6:attack=200:release=400[duck]"]
mix = ["[vo]", "[duck]"]
for k, (name, t, vol) in enumerate(events):
    args += ["-i", f"{SFX}/{name}.mp3"]
    ms = int(t * 1000)
    fl.append(f"[{k + 2}]atrim=0:1.2,afade=t=out:st=0.9:d=0.3,aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={ms}|{ms}[s{k}]")
    mix.append(f"[s{k}]")
norm = "loudnorm=I=-14:TP=-1.5:LRA=11," if has_vo else ""
fl.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,{norm}aresample=48000,alimiter=limit=0.85:level=false[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", ";".join(fl), "-map", "[out]", "-t", str(TOTAL),
                "-ar", "48000", "-ac", "2", "assets/audio/mix.wav"], check=True)
if has_vo:
    # one-pass loudnorm lands within a dB: a last gain puts the film on -14 LUFS
    out = subprocess.run(["ffmpeg", "-i", "assets/audio/mix.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    gain = -14 - float(out.rsplit("I:", 1)[1].split("LUFS")[0])
    if abs(gain) > 0.2:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/audio/mix.wav", "-af", f"volume={gain:.2f}dB,alimiter=limit=0.89:level=false",
                        "-ar", "48000", "-ac", "2", "assets/audio/mix.tmp.wav"], check=True)
        os.replace("assets/audio/mix.tmp.wav", "assets/audio/mix.wav")
print(f"mix: assets/audio/mix.wav ({'voice' if has_vo else 'no voice yet'}, {len(events)} sound effects, {TOTAL} s)")
