#!/usr/bin/env python3
"""Word timings of the voice montage without Whisper (model hosts blocked here): dynamic-programming alignment of the
text of build.py (SCENES) onto the phrases found by silence detection. Each phrase gets a run of consecutive words
whose syllable count matches its duration at the global speech rate; splits on punctuation are preferred.
Usage: python3 align.py [assets/audio/voix-montage.wav]  -> writes assets/audio/voix-montage-mots.json
Then: python3 build.py && bash build-mix.sh && bash assemble.sh"""
import json, re, subprocess, sys
from build import all_tokens, syl, display, SCENES
# chunk (from build.py SCENES) whose first word must start montage phrase n (onsets.py numbering), when the
# syllable fit alone picks the wrong split. Checked by ear and by the pauses on the voice of 2026-10-06.
ANCHORS = {}
wav = sys.argv[1] if len(sys.argv) > 1 else "assets/audio/voix-montage.wav"
words = all_tokens()
out = subprocess.run(["python3", "../.claude/skills/motion-design/scripts/onsets.py", wav, "--no-whisper"],
                     capture_output=True, text=True, check=True).stdout
spans = [(float(a), float(b)) for a, b in re.findall(r"^#\d+\s+([\d.]+) to\s+([\d.]+)", out, re.M)]
S = [syl(w) for w in words]
chunk_start, k = {}, 0
for sc in SCENES:
    for ch in sc["chunks"]:
        chunk_start.setdefault(ch, k); k += len([t for t in ch.split(" ") if t])
anchor = {chunk_start[c]: n for c, n in ANCHORS.items()}   # token index -> phrase number
punct = [bool(re.search(r"[.,:?!]$", display(w))) for w in words]
rate = sum(S) / sum(b - a for a, b in spans)
N, P = len(words), len(spans)
INF = float("inf")
cost = [[INF] * (P + 1) for _ in range(N + 1)]; back = [[0] * (P + 1) for _ in range(N + 1)]
cost[0][0] = 0
pre = [0]
for x in S: pre.append(pre[-1] + x)
for p in range(1, P + 1):
    d = spans[p - 1][1] - spans[p - 1][0]
    for i in range(1, N + 1):
        best, arg = INF, 0
        for j in range(max(0, i - 25), i):
            if cost[j][p - 1] == INF: continue
            if any((n == p and j != a) or (n != p and j < a < i) or (n != p and j == a) for a, n in anchor.items()): continue
            sy = pre[i] - pre[j]
            c = cost[j][p - 1] + ((sy - rate * d) ** 2) / max(1.0, rate * d) + (0 if punct[i - 1] else 1.5)
            if c < best: best, arg = c, j
        cost[i][p], back[i][p] = best, arg
print(f"{N} mots, {P} phrases, coût {cost[N][P]:.1f}")
i, groups = N, []
for p in range(P, 0, -1):
    j = back[i][p]; groups.append((j, i)); i = j
groups.reverse()
res = []
for (a, b), (j, i) in zip(spans, groups):
    tot = sum(S[j:i]); t = a; st = (b - a) / tot
    for k in range(j, i):
        res.append({"w": words[k], "start": round(t, 3), "end": round(t + S[k] * st, 3)}); t += S[k] * st
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav],
                           capture_output=True, text=True).stdout)
json.dump({"duration": round(dur, 3), "words": res}, open("assets/audio/voix-montage-mots.json", "w"), ensure_ascii=False, indent=1)
for (a, b), (j, i) in zip(spans, groups): print(f"  {a:6.2f}-{b:6.2f}  {' '.join(display(w) for w in words[j:i])}")
