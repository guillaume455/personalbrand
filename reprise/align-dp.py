#!/usr/bin/env python3
"""Word timings without Whisper (model hosts blocked here): dynamic-programming alignment of the known text onto the
phrases found by silence detection. Each phrase gets a run of consecutive words whose syllable count matches its
duration at the global speech rate; splits that fall on punctuation are preferred.
Usage: python3 align-dp.py <wav> <version: longue|courte>  -> prints the cost, writes <wav>-mots.json"""
import json, re, subprocess, sys
wav, version = sys.argv[1], sys.argv[2]
s = open("SCRIPT.md").read()
blocks = dict(zip(["longue", "courte"], re.findall(r"```\n(.*?)```", s, re.S)))
words = [w for w in blocks[version].split() if re.search(r"\w", w)]
out = subprocess.run(["python3", "../.claude/skills/motion-design/scripts/onsets.py", wav, "--no-whisper"],
                     capture_output=True, text=True, check=True).stdout
spans = [(float(a), float(b)) for a, b in re.findall(r"^#\d+\s+([\d.]+) to\s+([\d.]+)", out, re.M)]
syl = lambda w: max(1, len(re.findall(r"[aeiouyàâéèêëîïôûùü]+", w.lower().rstrip("es").rstrip("e") or w.lower())))
S = [syl(w) for w in words]
punct = [bool(re.search(r"[.,:?!]$", w)) for w in words]
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
            sy = pre[i] - pre[j]
            c = cost[j][p - 1] + ((sy - rate * d) ** 2) / max(1.0, rate * d) + (0 if punct[i - 1] else 1.5)
            if c < best: best, arg = c, j
        cost[i][p], back[i][p] = best, arg
total = cost[N][P]
print(f"{version}: {N} mots, {P} phrases, coût {total:.1f}")
i, groups = N, []
for p in range(P, 0, -1):
    j = back[i][p]; groups.append((j, i)); i = j
groups.reverse()
res = []
for (a, b), (j, i) in zip(spans, groups):
    tot = sum(S[j:i]); t = a; st = (b - a) / tot
    for k in range(j, i):
        res.append({"w": words[k], "start": round(t, 2), "end": round(t + S[k] * st, 2)}); t += S[k] * st
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav],
                           capture_output=True, text=True).stdout)
json.dump({"duration": round(dur, 2), "words": res}, open(wav.rsplit(".", 1)[0] + "-mots.json", "w"), ensure_ascii=False, indent=1)
for (a, b), (j, i) in zip(spans, groups): print(f"  {a:6.2f}-{b:6.2f}  {' '.join(words[j:i])}")
