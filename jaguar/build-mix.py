#!/usr/bin/env python3
"""Mix of the Jaguar reel: Guillaume's voice, the music bed and the sound effects (assets/audio/sfx-events.json,
written by build.py). The music supports and never leads. It is cut from the track in two pieces so that its drops
land on the story: the build-up of the track under the hook and « why everyone runs » (tension), its first drop
exactly on the Car-Pass (the clean switch), a muffled build again under the real margin (tension, opening up), its
second drop on « 13,4 % », then a complete fall on the lesson, back softly under « who I am », faded out at the end.
It ducks under the voice (attack 200 ms, release 400 ms). Output assets/audio/mix.wav, 48 kHz stereo, -14 LUFS.
Usage: python3 build-mix.py"""
import json, os, subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open("timings.json")); TOTAL = float(T["total"]); F = {f["id"]: f for f in T["frames"]}
VO = "assets/audio/voix-montage.wav"
MUSIC = "assets/music/musique.mp3"
SFX = "../.claude/skills/media-use/audio/assets/sfx"
DROP1, DROP2 = 18.0, 69.9      # the two drops of the track (s)
hk, cp, vm, rd, les, cta = (F[k] for k in ("01-hook", "03-carpass", "07-vraie-marge", "08-rendement", "09-lecon", "10-cta"))
# two pieces of the track: (film start, film end, track time at film start)
PIECES = [(0.0, vm["start"], DROP1 - cp["start"]), (vm["start"], TOTAL, DROP2 - (rd["start"] - vm["start"]))]

# music level (dB) and « openness » (0 = muffled low-pass, 1 = full) along the film, piecewise linear
LEVEL = [(0, -17), (cp["start"] - 0.4, -17), (cp["start"] - 0.05, -30), (cp["start"] + 0.05, -16), (cp["start"] + 1.5, -19),
         (vm["start"], -19), (rd["start"] - 0.3, -16), (rd["start"] + 0.8, -18), (les["start"] - 0.2, -19), (les["start"] + 1.6, -90),
         (cta["start"] - 0.1, -90), (cta["start"] + 0.9, -21), (TOTAL - 1.3, -21), (TOTAL, -90)]
OPEN = [(0, 0.35), (cp["start"] - 0.3, 0.75), (cp["start"], 1), (vm["start"], 1), (vm["start"] + 0.3, 0.15), (rd["start"] - 0.2, 0.9),
        (rd["start"], 1), (TOTAL, 1)]


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
      "[1]asplit=2[t0][t1]",
      *[f"[t{i}]atrim={max(0, o):.3f}:{max(0, o) + (b - a) + 0.15:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
        f"afade=t=in:d=0.04,afade=t=out:st={b - a:.3f}:d=0.12,adelay={int(a * 1000)}|{int(a * 1000)}[q{i}]" for i, (a, b, o) in enumerate(PIECES)],
      f"[q0][q1]amix=inputs=2:normalize=0,apad=whole_dur={TOTAL},atrim=0:{TOTAL},asplit=2[ma][mb]",
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
for _ in range(3 if has_vo else 0):
    # one-pass loudnorm lands within a dB: a last gain (repeated, the limiter eats a little) puts the film on -14 LUFS
    out = subprocess.run(["ffmpeg", "-i", "assets/audio/mix.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    gain = -14 - float(out.rsplit("I:", 1)[1].split("LUFS")[0])
    if abs(gain) > 0.1:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/audio/mix.wav", "-af", f"volume={gain:.2f}dB,alimiter=limit=0.89:level=false",
                        "-ar", "48000", "-ac", "2", "assets/audio/mix.tmp.wav"], check=True)
        os.replace("assets/audio/mix.tmp.wav", "assets/audio/mix.wav")
print(f"mix: assets/audio/mix.wav ({'voice' if has_vo else 'no voice yet'}, {len(events)} sound effects, {TOTAL} s)")
