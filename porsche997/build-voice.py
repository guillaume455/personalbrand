#!/usr/bin/env python3
"""Voice montage of the reel: every pause over MAXGAP is shortened to MAXGAP (cut in the middle of the silence,
5 ms fades), then the whole voice is sped up ×SPEED (pitch kept)
and a tail is added for the end card. Writes assets/audio/voix-montage.wav."""
import re, subprocess
SRC, OUT, SPEED, MAXGAP, TAIL = "assets/audio/voix.mp3", "assets/audio/voix-montage.wav", 1.0, 0.5, 1.6
KEEP_LONGER = {}   # {phrase end (s, rounded): longer pause}, e.g. a beat after « Erreur. »
out = subprocess.run(["python3", "../.claude/skills/motion-design/scripts/onsets.py", SRC, "--no-whisper"],
                     capture_output=True, text=True, check=True).stdout
spans = [(float(a), float(b)) for a, b in re.findall(r"^#\d+\s+([\d.]+) to\s+([\d.]+)", out, re.M)]
keep, cur = [], 0.0
for (a, b), (c, _) in zip(spans, spans[1:] + [(None, None)]):
    if c is None: keep.append((cur, b + 0.25)); break
    gap, want = c - b, KEEP_LONGER.get(round(b, 2), MAXGAP)
    if gap > want:
        keep.append((cur, b + want / 2)); cur = c - want / 2
keep[0] = (max(0.0, keep[0][0]), keep[0][1])
parts = [f"[0]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={b-a-0.005:.3f}:d=0.005[p{i}]" for i, (a, b) in enumerate(keep)]
g = ";".join(parts) + ";" + "".join(f"[p{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1,atempo={SPEED},apad=pad_dur={TAIL}[out]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", g, "-map", "[out]", "-ar", "44100", "-ac", "1", OUT], check=True)
d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", OUT], capture_output=True, text=True).stdout
print(f"{len(keep)} segments, montage {float(d):.2f} s")
