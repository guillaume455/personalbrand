#!/usr/bin/env python3
"""Mix of the reference film « La ligne du temps » (ligne-du-temps-v8), voice Eleven v4, 49.52 s.

Same recipe as film C (music option M1 « tic-tac puis élan »):
- the tension music runs under the problem and is cut to silence right after « Il est temps de changer. » (STOP),
  with a low impact; a riser climbs into the cut,
- silence, then the light: the élan music comes back with its drop on « Aujourd'hui » (LIGHT),
- the music ducks under the voice (sidechain) and breathes in the gaps; fade out on the end card,
- sound effects locked on the picture (film time), notification two-tone as the signature (the silent gag),
- loudness normalized for the web (-16 LUFS, -1.5 dBTP).

Usage: python3 build-audio-v8.py        ->  assets/audio/mix-v8.wav (the mix of the delivered film)
       python3 build-audio-v8.py M2     ->  assets/audio/mix-v8-M2.wav (one of the four tension options below)
Environment:
  VOICE      the voice montage, 49.52 s (default assets/audio/voix-v8.wav: drop your own there, not included)
  MUSIC_DIR  folder of the CC0 tracks (default assets/music; names and download links:
             .claude/skills/motion-design/references/music.md)
  SFX_DIR    sound effects, .wav or .mp3 (default: the Pixabay set of HeyGen's media-use skill in this repository)
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(HERE, "assets", "audio")
MUSIC = os.environ.get("MUSIC_DIR", os.path.join(HERE, "assets", "music"))
SFX_DIR = os.environ.get("SFX_DIR", os.path.join(HERE, "..", "..", ".claude", "skills", "media-use", "audio", "assets", "sfx"))
VOICE = os.environ.get("VOICE", os.path.join(AUDIO, "voix-v8.wav"))
DUR = 49.52
STOP, LIGHT = 23.40, 25.12

SEGMENTS = [  # (file, track_start, film_start, film_end, gain, fade_in, fade_out)
    ("tension-waiting-tttt.mp3", 0.0, 0.0, STOP, 0.40, 0.4, 0.02),
    ("elan-dear-mr-super-computer.mp3", 5.59, LIGHT, DUR, 0.30, 0.0, 2.6),
]
RISER = 0.16

# Feedback on the delivered film: « the start is a bit soft ». With the sparse intro of « waiting », the tension sat at
# -31.8 LUFS against -21.3 for the élan (10 dB under). Four options for the tension music (0 to STOP), all set near
# -23 LUFS, 2 dB under the élan: (file, start in the track, gain). « python3 build-audio-v8.py M2 » writes
# assets/audio/mix-v8-M2.wav.
TENSION_OPTIONS = {
    "M1": ("tension-waiting-tttt.mp3", 72.0, 0.525),          # same music, its full section
    "M2": ("tension-cyber-anxiety.mp3", 52.0, 0.285),         # pulsed tension
    "M3": ("complet-machines-with-feelings.mp3", 42.0, 0.272),  # electro that moves forward
    "M4": ("tension-time-attack-research.mp3", 0.0, 0.724),   # action pulse
}


def sfx(name):
    for ext in (".wav", ".mp3"):
        f = os.path.join(SFX_DIR, name + ext)
        if os.path.exists(f):
            return f
    sys.exit(f"build-audio-v8: sound effect '{name}' not found in {SFX_DIR} (.wav or .mp3)")


SFX = [  # (name in SFX_DIR, film time, gain)
    # 1. Lundi / Mercredi : the request on the real site, the quote drops on its day
    ("click", 1.56, 0.35), ("whoosh-short", 3.00, 0.18), ("pop", 4.92, 0.30),
    # 2. Vendredi, then the silent gag : read, ticks turn blue, the only answer comes in
    ("whoosh-short", 5.90, 0.18), ("pop", 8.30, 0.14),
    ("notification", 8.80, 0.30),
    # 3. Sois honnête : the keyword box
    ("whoosh-short", 10.24, 0.16), ("click-soft", 12.84, 0.35),
    # 4. the three waits, one station per « chaque », the automation breaks
    ("whoosh-short", 15.02, 0.16), ("pop", 15.28, 0.10), ("whoosh-short", 16.72, 0.16), ("error", 17.40, 0.18),
    ("whoosh-short", 18.12, 0.16),
    # 5. the years (notifications pile up), then black : « Il est temps de changer. »
    ("whoosh", 19.84, 0.20),
    ("notification", 20.50, 0.12), ("notification", 20.95, 0.12), ("notification", 21.40, 0.12),
    ("pop", 21.70, 0.08), ("pop", 21.85, 0.08), ("pop", 22.00, 0.08),
    ("click", 22.56, 0.30),
    ("impact-bass-1", STOP, 0.34),
    ("sparkle", 24.94, 0.18), ("whoosh", 24.94, 0.20),
    # 6. Aujourd'hui : the request typed in plain words, three checks on « elle le fait »
    ("typing", 30.00, 0.18), ("click", 31.40, 0.40),
    ("click-soft", 31.76, 0.40), ("click-soft", 31.94, 0.40), ("click-soft", 32.10, 0.40),
    # 7. Terminé, les devis / l'attente, then the ideas fly
    ("whoosh-short", 32.28, 0.22), ("whoosh-short", 33.96, 0.18),
    ("chime", 35.18, 0.18), ("pop", 35.45, 0.10), ("pop", 35.70, 0.10), ("pop", 35.95, 0.10),
    # 8. the fine line, « t'en servir correctement »
    ("whoosh-short", 37.70, 0.12), ("chime", 41.10, 0.14),
    # 9. end card, the direct click
    ("whoosh-cinematic", 42.20, 0.22), ("click", 46.60, 0.45),
]


def build(opt=None):
    segments = list(SEGMENTS)
    if opt:
        f, ts, g = TENSION_OPTIONS[opt]
        segments[0] = (f, ts, 0.0, STOP, g, 0.05, 0.02)
    inputs = ["-i", VOICE]
    fc = ["[0]aformat=sample_rates=44100:channel_layouts=stereo,asplit=2[v][vsc]"]
    idx, mus = 1, []
    for i, (f, ts, fs, fe, g, fi, fo) in enumerate(segments):
        inputs += ["-i", os.path.join(MUSIC, f)]
        d = fe - fs
        chain = f"[{idx}]atrim=start={ts:.3f}:duration={d:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo"
        if fi > 0:
            chain += f",afade=t=in:d={fi}"
        chain += f",afade=t=out:st={max(d - fo, 0):.3f}:d={fo},volume={g},adelay={int(fs * 1000)}|{int(fs * 1000)},apad=whole_dur={DUR}[m{i}]"
        fc.append(chain); mus.append(f"[m{i}]"); idx += 1
    rise_len = 3.2
    inputs += ["-i", sfx("riser")]
    st = STOP - rise_len
    fc.append(f"[{idx}]atrim=start={10.032 - rise_len:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo,"
              f"afade=t=in:d=1.2,afade=t=out:st={rise_len - 0.03:.3f}:d=0.03,volume={RISER},adelay={int(st * 1000)}|{int(st * 1000)},apad=whole_dur={DUR}[mr]")
    mus.append("[mr]"); idx += 1
    fc.append("".join(mus) + f"amix=inputs={len(mus)}:normalize=0:duration=longest[mbus]")
    fc.append("[mbus][vsc]sidechaincompress=threshold=0.035:ratio=5:attack=25:release=420:makeup=1[mduck]")
    labels = ["[v]", "[mduck]"]
    for j, (name, t, g) in enumerate(SFX):
        inputs += ["-i", sfx(name)]
        fc.append(f"[{idx}]aformat=sample_rates=44100:channel_layouts=stereo,volume={g},adelay={int(t * 1000)}|{int(t * 1000)}[e{j}]")
        labels.append(f"[e{j}]"); idx += 1
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{DUR},loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.89:level=disabled[out]")
    os.makedirs(AUDIO, exist_ok=True)
    out = os.path.join(AUDIO, "mix-v8.wav" if not opt else "mix-v8-%s.wav" % opt)
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(fc), "-map", "[out]", "-ar", "44100", "-t", str(DUR), out], check=True)
    print("mix ->", out)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else None)
