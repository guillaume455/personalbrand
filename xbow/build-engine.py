#!/usr/bin/env python3
"""Synthetic sound of the X-Bow: a 2.0 turbo four-cylinder petrol engine, the wind of an open cockpit and the road, laid
on the film's timeline (assets/audio/engine.wav, 48 kHz stereo). The rush's own sound is the music of its first edit,
so the real engine is not available: this one is built from physics, kept discreet.

- engine: one exhaust pulse per firing (4 cylinders, 4 strokes: 2 per crank turn, 100 Hz at 3 000 rpm), small
  cycle-to-cycle and cylinder-to-cylinder variations (what makes an engine sound real and not like a synth), a softer
  pulse off throttle, a harder one under load, shaped by fixed exhaust resonances;
- intake rasp under load; turbo: a quiet whistle and whoosh that spool with a lag, a diverter « pff » at each
  shift and a short blow-off when the throttle closes after boost;
- wind and road noise, rising with speed.

The rpm, throttle and speed follow the cuts: a pull on the hook, a distant cruise under the photos, the 0 to 100 launch
on « en 3,9 s », cruising rides, two accelerations at the end of the rides and the 3 s breath, a lift-off at the end.
Usage: python3 build-engine.py (after build.py; build-mix.py uses the file when it exists)."""
import json, os, wave
import numpy as np

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
T = json.load(open("timings.json")); TOTAL = float(T["total"]); F = {f["id"]: f for f in T["frames"]}
C = T["engine_cues"]
M = {cid: (t, d) for cid, t, d, *_ in json.load(open("media.json"))}
N = int(TOTAL * SR); t = np.arange(N) / SR
rng = np.random.default_rng(7)

# ---------------------------------------------------------------------------------------------------------------------
# automation along the film: rpm, throttle (0-1), speed (0-1, wind), level (dB)
bal = F["03-balades"]; rev = F["04-revente"]; les = F["05-lecon"]
b8 = M["b8"][0]; br = M["breath"][0]; ck = M["cockpit"][0]; launch = C["launch"]; zero = C["zero"]


def pull(t0, r0, steps):
    """a pull through the gears: steps = [(duration, rpm at the top)]; each shift drops 30 % in 0.12 s"""
    keys, thr, x, r = [(t0, r0)], [(t0 - 0.05, 0.25), (t0 + 0.08, 1.0)], t0, r0
    for d, top in steps:
        x += d; keys.append((x, top))
        r = top * 0.7; keys.append((x + 0.12, r)); thr += [(x, 1.0), (x + 0.02, 0.1), (x + 0.16, 0.1), (x + 0.24, 1.0)]
        x += 0.12
    return keys[:-1], thr[:-3], x - 0.12


RPM, THR, SPD, LVL = [], [], [], []
# hook: rolling, then a pull
RPM += [(0, 2900), (0.55, 2950)]; THR += [(0, 0.3), (0.5, 0.3)]
k, th, e = pull(0.6, 2950, [(1.55, 5300), (0.7, 4600)]); RPM += k; THR += th + [(3.0, 1.0)]
SPD += [(0, 0.55), (3.0, 0.7)]; LVL += [(0, 0), (2.85, 0)]
# photos and titles: a distant cruise
RPM += [(3.3, 2700), (ck - 0.2, 2650)]; THR += [(3.3, 0.3), (ck - 0.2, 0.3)]; SPD += [(3.3, 0.5), (ck, 0.5)]
LVL += [(3.25, -19), (ck - 0.3, -19)]
# the open cockpit, rolling, then idle before the launch
RPM += [(ck, 3000), (zero - 0.6, 3300), (zero - 0.2, 1500), (launch - 0.45, 1000), (launch - 0.3, 1000)]
THR += [(ck, 0.4), (zero - 0.6, 0.45), (zero - 0.5, 0.0), (launch - 0.3, 0.0)]
SPD += [(ck, 0.6), (zero - 0.6, 0.6), (zero, 0.0), (launch, 0.0)]
LVL += [(ck, -10), (zero - 0.6, -10), (zero - 0.2, -8)]
# 0 to 100: launch on « en », two shifts, the first frame of the rides keeps pulling
k, th, e = pull(launch - 0.25, 3800, [(0.85, 6600), (0.95, 6500), (0.9, 6200)]); RPM += k; THR += th
SPD += [(launch + 0.3, 0.2), (e, 0.95)]; LVL += [(launch - 0.3, -4), (e, -4)]
# the rides: cruising, slower in the village, the forest acceleration after the KTM photo, the breath
v1 = M["b6"][0]
RPM += [(e + 0.5, 3600), (bal["start"] + 2.0, 3000), (v1, 2700), (v1 + 1.2, 2300), (M["b7"][0], 2900), (b8 + 1.5, 2900)]
THR += [(e + 0.4, 0.5), (bal["start"] + 2.0, 0.35), (v1, 0.2), (M["b7"][0], 0.45), (b8 + 1.5, 0.45)]
SPD += [(e + 0.5, 0.85), (bal["start"] + 2.0, 0.75), (v1, 0.55), (v1 + 1.2, 0.45), (M["b7"][0], 0.7), (b8 + 1.5, 0.75)]
LVL += [(e + 0.5, -2), (bal["start"] + 0.5, 0)]
k, th, e = pull(b8 + 1.7, 3000, [(1.6, 5800), (1.0, 5000)]); RPM += k; THR += th
RPM += [(br - 0.15, 3600)]; THR += [(br - 0.3, 0.3)]
SPD += [(br, 0.9)]
k, th, e = pull(br + 0.05, 3400, [(1.4, 6300), (1.1, 5900)]); RPM += k; THR += th
RPM += [(e + 0.5, 3800), (bal["end"] + 0.2, 3300)]; THR += [(e + 0.02, 0.0), (bal["end"], 0.0)]
SPD += [(e, 1.0), (bal["end"], 0.95)]; LVL += [(bal["end"] - 0.6, 0), (bal["end"], -30)]
# the resale: a far cruise, very low; the lesson: nothing
RPM += [(rev["start"], 2600), (rev["end"], 2600)]; THR += [(rev["start"], 0.3), (rev["end"], 0.3)]
SPD += [(rev["start"], 0.5), (rev["end"], 0.5)]
LVL += [(rev["start"], -24), (rev["end"] - 0.6, -24), (rev["end"], -90), (TOTAL, -90)]


def env(keys):
    keys = sorted(keys)
    return np.interp(t, [k[0] for k in keys], [k[1] for k in keys])


def smooth(x, sec):
    """centred moving average (cumulative sum: fast on long windows)"""
    n = max(1, int(sec * SR)); h = n // 2
    c = np.cumsum(np.pad(x, (h + 1, n - h), mode="edge"))
    return (c[n:n + len(x)] - c[:len(x)]) / n


# a real foot is never still: slow rpm wander (±1.5 %) and throttle wander when cruising
wander = smooth(rng.standard_normal(N), 0.6) * 55
rpm = smooth(env(RPM), 0.05) * (1 + 0.015 * np.clip(wander, -1, 1)); thr = smooth(env(THR), 0.03)
thr = np.clip(thr + 0.06 * np.clip(smooth(rng.standard_normal(N), 0.4) * 45, -1, 1) * (thr < 0.7) * (thr > 0.05), 0, 1); spd = smooth(env(SPD), 0.4)
lvl = 10 ** (smooth(env(LVL), 0.15) / 20)
# boost: follows throttle and rpm with a lag (spool up 0.6 s, down 0.25 s)
target = np.clip(thr, 0, 1) * np.clip((rpm - 2200) / 2500, 0, 1)
boost = np.zeros(N); b = 0.0; up, dn = 1 / (0.6 * SR), 1 / (0.25 * SR)
step = 64
for i in range(0, N, step):
    tg = target[i]; b += (tg - b) * (up if tg > b else dn) * step * 3; b = min(max(b, 0), 1); boost[i:i + step] = b


def fftfilt(x, resp):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * resp(f), len(x))


def band(f, lo, hi, order=2):
    h = 1 / np.sqrt(1 + (f / hi) ** (2 * order))
    return h * (1 - 1 / np.sqrt(1 + (f / max(lo, 1e-3)) ** (2 * order))) if lo > 0 else h


def peak(f, f0, q, g):
    return 1 + (g - 1) / (1 + ((f - f0) / (f0 / q)) ** 2)


# ---------------------------------------------------------------------------------------------------------------------
# engine: firing pulses
ff = rpm / 60 * 2
ph = np.cumsum(ff / SR)
fire = np.flatnonzero(np.diff(np.floor(ph)) > 0) + 1
cyl = np.arange(len(fire)) % 4
amp = (1 + 0.05 * rng.standard_normal(len(fire))) * np.array([1.0, 0.94, 1.04, 0.97])[cyl]
load = thr[fire]
amp *= 0.35 + 0.65 * load
jit = (rng.standard_normal(len(fire)) * 0.00012 * SR).astype(int)
idx = np.clip(fire + jit, 0, N - 1)
soft = np.zeros(N); hard = np.zeros(N)
np.add.at(soft, idx, amp * (1 - load)); np.add.at(hard, idx, amp * load)
kt = np.arange(int(0.018 * SR)) / SR
k_soft = np.exp(-kt / 0.0035) * np.sin(2 * np.pi * 140 * kt) + 0.15 * np.exp(-kt / 0.002) * rng.standard_normal(len(kt))
k_hard = (np.exp(-kt / 0.0025) * np.sin(2 * np.pi * 210 * kt) + 0.45 * np.exp(-kt / 0.0018) * rng.standard_normal(len(kt))
          + 0.5 * np.exp(-kt / 0.006) * np.sin(2 * np.pi * 95 * kt))


def conv(x, k):
    n = 1 << int(np.ceil(np.log2(len(x) + len(k))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(k, n), n)[:len(x)]


eng = conv(soft, k_soft) + conv(hard, k_hard)
# exhaust: body around 80-120 Hz, pipe resonances, a muffler that cuts the top
eng = fftfilt(eng, lambda f: band(f, 30, 2600, 2) * peak(f, 95, 1.5, 2.2) * peak(f, 260, 2.5, 1.6) * peak(f, 640, 3, 1.3))
eng = np.tanh(eng / (np.percentile(np.abs(eng), 99.5) + 1e-9) * 1.3) * 0.5
# intake rasp under load: noise gated by the firing phase
rasp = fftfilt(rng.standard_normal(N), lambda f: band(f, 900, 3200, 2))
rasp *= (0.55 + 0.45 * np.sin(2 * np.pi * ph)) * thr ** 1.5 * np.clip(rpm / 6500, 0, 1) * 0.16
# turbo: whistle (two partials) and whoosh, both following the boost
wf = 3300 + 3800 * boost
wph = np.cumsum(wf / SR)
whistle = (np.sin(2 * np.pi * wph) + 0.4 * np.sin(2 * np.pi * 1.5 * wph + 1.0)) * boost ** 2 * 0.010
whoosh = fftfilt(rng.standard_normal(N), lambda f: band(f, 1500, 6000, 2)) * boost ** 1.5 * 0.03
# diverter valve: a small puff at each shift, a longer blow-off when the throttle closes after boost
dthr = np.diff(thr, prepend=thr[0]) * SR
puff = np.zeros(N)
events = np.flatnonzero((dthr[1:] < -20) & (dthr[:-1] >= -20)) + 1
noise_bo = fftfilt(rng.standard_normal(N), lambda f: band(f, 700, 5500, 2) * peak(f, 2200, 1.2, 1.8))
last = -SR
for i in events:
    if i - last < 0.3 * SR or boost[i] < 0.35:
        continue
    last = i
    longer = thr[min(N - 1, i + int(0.3 * SR))] < 0.05      # throttle stays closed: a real blow-off
    d = 0.38 if longer else 0.12
    n = int(d * SR); e = np.arange(min(n, N - i)) / SR
    shape = (1 - np.exp(-e / 0.008)) * np.exp(-e / (d / 3))
    puff[i:i + len(e)] += noise_bo[i:i + len(e)] * shape * boost[i] * (0.09 if longer else 0.04)
# wind (open cockpit) and road
gust = 1 + smooth(rng.standard_normal(N), 0.8) * 40
windL = fftfilt(rng.standard_normal(N), lambda f: band(f, 40, 700, 1) * peak(f, 1600, 1, 1.4))
windR = fftfilt(rng.standard_normal(N), lambda f: band(f, 40, 700, 1) * peak(f, 1600, 1, 1.4))
road = fftfilt(rng.standard_normal(N), lambda f: band(f, 35, 160, 2))
w = spd ** 2 * gust
mono = eng * 0.9 + rasp + whistle + whoosh + puff
L = (mono + windL * w * 0.11 + road * spd * 0.12) * lvl
R = (mono * 0.97 + windR * w * 0.11 + road * spd * 0.12) * lvl
st = np.stack([L, R], 1)
st *= 0.5 / (np.abs(st).max() + 1e-9)
fade = int(0.01 * SR); st[:fade] *= np.linspace(0, 1, fade)[:, None]
os.makedirs("assets/audio", exist_ok=True)
with wave.open("assets/audio/engine.wav", "wb") as wv:
    wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR)
    wv.writeframes((st * 32767).astype("<i2").tobytes())
print(f"engine: assets/audio/engine.wav ({TOTAL} s, launch at {launch:.2f} s)")
