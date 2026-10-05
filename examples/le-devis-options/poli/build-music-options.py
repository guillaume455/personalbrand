#!/usr/bin/env python3
"""Build the four music options of film C (same voice, same picture timing): the exact configuration of the film
published on entrepreneurs2-0.com (option M1). Generic version: .claude/skills/motion-design/templates/.

Every option shares the same edit logic, locked on the picture:
- the music is cut to silence on « Stop. » (14.02 s) with a low impact,
- it comes back on the light flash with its drop landing at 14.30 s,
- it ducks under the voice (sidechain compressor) and breathes in the gaps,
- it fades out on the end card; the whole mix is normalized for the web (-16 LUFS).

Usage: MUSIC_DIR=/path/to/tracks python3 build-music-options.py [M1 M2 ...]   (default: all)
Output: assets/audio/mix-C-<id>.wav, then MIX=mix-C-<id>.wav ./assemble.sh (here, in ../nuit or ../bureau).
Environment:
  MUSIC_DIR  folder with the 10 CC0 tracks (names and download links: .claude/skills/motion-design/references/music.md)
  SFX_DIR    sound effects, .wav or .mp3 (default: the Pixabay set of HeyGen's media-use skill in this repository)
  VOICE      voice montage (default: assets/audio/voix-C-devis-montage.wav here, else the one built by
             ../../le-devis/build-audio.sh)
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(HERE, "assets", "audio")
MUSIC = os.environ.get("MUSIC_DIR", os.path.join(HERE, "assets", "music"))
SFX_DIR = os.environ.get("SFX_DIR", os.path.join(HERE, "..", "..", "..", ".claude", "skills", "media-use", "audio", "assets", "sfx"))
VOICE = os.environ.get("VOICE") or next(
    (p for p in (os.path.join(AUDIO, "voix-C-devis-montage.wav"),
                 os.path.join(HERE, "..", "..", "le-devis", "assets", "audio", "voix-C-devis-montage.wav")) if os.path.exists(p)),
    os.path.join(AUDIO, "voix-C-devis-montage.wav"))
DUR = 43.2
STOP, LIGHT = 14.02, 14.30

# Music segments: (file, track_start, film_start, film_end, gain, fade_in, fade_out)
OPTIONS = {
    "M1": {
        "name": "tic-tac puis elan",
        "segments": [
            ("tension-waiting-tttt.mp3", 0.0, 0.0, STOP, 0.42, 0.4, 0.02),
            ("elan-dear-mr-super-computer.mp3", 5.59, LIGHT, DUR, 0.30, 0.0, 2.4),
        ],
        "riser": 0.18,
    },
    "M2": {
        "name": "retro synthe, drop sur la lumiere",
        "segments": [
            ("complet-retro-synths.mp3", 1.62, 0.0, STOP, 0.34, 0.6, 0.02),
            ("complet-retro-synths.mp3", 1.62 + LIGHT, LIGHT, DUR, 0.30, 0.0, 2.4),
        ],
        "riser": 0.0,
    },
    "M3": {
        "name": "montee electro, drop sur la lumiere",
        "segments": [
            ("complet-feels-good-to-be-alive.mp3", 0.0, 0.66, STOP, 0.30, 0.3, 0.02),
            ("complet-feels-good-to-be-alive.mp3", LIGHT - 0.66, LIGHT, DUR, 0.26, 0.0, 2.4),
        ],
        "riser": 0.0,
    },
    "M4": {
        "name": "cinema, nappe sombre puis piano",
        "segments": [
            ("tension-cyber-anxiety.mp3", 0.0, 0.0, STOP, 0.40, 0.5, 0.02),
            ("minimal-drifting-piano.mp3", 4.2, LIGHT, DUR, 0.62, 0.0, 2.8),
            ("minimal-ambiant-hope.mp3", 14.9, LIGHT, DUR, 0.30, 0.2, 2.8),
        ],
        "riser": 0.14,
    },
}

# Sound effects locked on the picture of C (film time): (name in SFX_DIR, time, gain)
SFX = [("whoosh-short", t, 0.16) for t in (5.70, 10.90, 17.32, 20.56, 25.94)] + [
    ("whoosh-short", 31.88, 0.10),
    ("pop", 0.24, 0.18), ("click", 1.20, 0.40), ("whoosh-short", 1.66, 0.20),
    ("pop", 2.70, 0.30), ("pop", 4.72, 0.28),
    ("error", 7.26, 0.22), ("impact-bass-2", 7.76, 0.30), ("click", 7.80, 0.30),
    ("ping", 8.94, 0.16),
    ("key-press", 9.68, 0.25), ("key-press", 10.04, 0.25), ("key-press", 10.40, 0.25),
    ("pop", 12.56, 0.14), ("pop", 12.80, 0.12), ("pop", 13.04, 0.12),
    # the pivot: low impact on « Stop. », light on the flash
    ("impact-bass-1", STOP, 0.34), ("click", 14.04, 0.30),
    ("sparkle", 14.26, 0.18), ("whoosh", 14.26, 0.22),
    ("pop", 16.02, 0.18), ("typing", 17.56, 0.20), ("typing", 18.56, 0.16),
    ("click", 19.46, 0.45), ("pop", 19.70, 0.26),
    ("click-soft", 21.80, 0.40), ("click-soft", 23.38, 0.40), ("click-soft", 25.26, 0.40),
    ("click-soft", 25.58, 0.25), ("whoosh-short", 28.06, 0.20),
    # « libre. », the peak: the card flies off, the giant pill lands
    ("whoosh-short", 30.68, 0.22), ("chime", 30.92, 0.22),
    ("ping", 35.02, 0.14),
    ("whoosh-cinematic", 35.95, 0.22), ("click", 41.35, 0.45),
]


def sfx(name):
    for ext in (".wav", ".mp3"):
        f = os.path.join(SFX_DIR, name + ext)
        if os.path.exists(f):
            return f
    sys.exit(f"build-music-options: sound effect '{name}' not found in {SFX_DIR}")


def build(oid):
    opt = OPTIONS[oid]
    if not os.path.exists(VOICE):
        sys.exit(f"build-music-options: voice montage {VOICE} not found (run ../../le-devis/build-audio.sh or set VOICE)")
    inputs = ["-i", VOICE]
    fc = ["[0]aformat=sample_rates=44100:channel_layouts=stereo,asplit=2[v][vsc]"]
    idx = 1
    mus = []
    for i, (f, ts, fs, fe, g, fi, fo) in enumerate(opt["segments"]):
        src = os.path.join(MUSIC, f)
        if not os.path.exists(src):
            sys.exit(f"build-music-options: {src} not found (set MUSIC_DIR)")
        inputs += ["-i", src]
        d = fe - fs
        chain = f"[{idx}]atrim=start={ts:.3f}:duration={d:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo"
        if fi > 0:
            chain += f",afade=t=in:d={fi}"
        chain += f",afade=t=out:st={max(d - fo, 0):.3f}:d={fo},volume={g},adelay={int(fs * 1000)}|{int(fs * 1000)},apad=whole_dur={DUR}[m{i}]"
        fc.append(chain)
        mus.append(f"[m{i}]")
        idx += 1
    if opt["riser"] > 0:
        rise_len = 3.2
        inputs += ["-i", sfx("riser")]
        st = STOP - rise_len
        fc.append(
            f"[{idx}]atrim=start={10.032 - rise_len:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo,"
            f"afade=t=in:d=1.2,afade=t=out:st={rise_len - 0.03:.3f}:d=0.03,volume={opt['riser']},adelay={int(st * 1000)}|{int(st * 1000)},apad=whole_dur={DUR}[mr]"
        )
        mus.append("[mr]")
        idx += 1
    fc.append("".join(mus) + f"amix=inputs={len(mus)}:normalize=0:duration=longest[mbus]")
    # duck the music under the voice, let it breathe in the gaps
    fc.append("[mbus][vsc]sidechaincompress=threshold=0.035:ratio=5:attack=25:release=420:makeup=1[mduck]")
    labels = ["[v]", "[mduck]"]
    for j, (name, t, g) in enumerate(SFX):
        inputs += ["-i", sfx(name)]
        fc.append(f"[{idx}]aformat=sample_rates=44100:channel_layouts=stereo,volume={g},adelay={int(t * 1000)}|{int(t * 1000)}[e{j}]")
        labels.append(f"[e{j}]")
        idx += 1
    # exact chain of the published film; the template adds level=disabled to the limiter to keep the true peak under
    # -1.5 dBTP (see references/music.md)
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{DUR},loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.89[out]")
    os.makedirs(AUDIO, exist_ok=True)
    out = os.path.join(AUDIO, f"mix-C-{oid}.wav")
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(fc), "-map", "[out]", "-ar", "44100", "-t", str(DUR), out]
    subprocess.run(cmd, check=True)
    print(f"{oid} ({opt['name']}) -> {out}")


if __name__ == "__main__":
    for oid in (sys.argv[1:] or list(OPTIONS)):
        if oid not in OPTIONS:
            sys.exit(f"unknown option {oid} (known: {', '.join(OPTIONS)})")
        build(oid)
