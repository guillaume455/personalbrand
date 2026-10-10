#!/usr/bin/env python3
"""Reel « X-Bow » : one source for the whole film.

Every animation of every scene is placed on a WORD of the voice (at("virement"), at("même", 2)...), never on a fixed
second. The word timings come from one file:
  - assets/audio/voix-montage-mots.json when the real voice is there (align.py writes it), or
  - a provisional timing spread over the brief's windows (0-5, 5-18, 18-28, 28-36, 36-44, 44-52, 52-56 s).
So when the final voice arrives (or changes), run: python3 align.py && python3 build.py && bash assemble.sh
and every scene, cut, subtitle and sound effect lands back on the voice.

Usage: python3 build.py [--provisional]
Writes: compositions/frames/*.html, STORYBOARD.md, timings.json, assets/audio/sfx-events.json
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
REAL = "assets/audio/voix-montage-mots.json"
TAIL = 2.4          # hold after the last word (end card)
FPS = 30

# ---------------------------------------------------------------------------------------------------------------------
# The voice, scene by scene, cut into subtitle chunks (2 to 5 words). *word* = key word (orange). ~ glues two tokens
# into one subtitle word (« 10~000 », « voitures~? »). Numbers are spoken « dix mille », « deux mille vingt-six ».
SCENES = [
 dict(id="01-opportunite", name="Hook et opportunité", window=(0, 12), speak=(3.1, 12), chunks=[
   "On me propose", "une KTM *X-Bow*.", "Je n'en cherchais pas,", "je n'en avais jamais conduit.", "40~000~euros.",
   "J'ai dit oui."]),
 dict(id="02-cestquoi", name="C'est quoi", window=(12, 24), chunks=[
   "KTM fait des motos.", "Ça, c'est leur", "*première~voiture*.", "Monocoque *carbone*,", "790~kilos,", "pas de toit,",
   "pas de pare-brise.", "Et dessous, le moteur", "d'une Golf~GTI."]),
 dict(id="03-balades", name="Les balades", window=(24, 42), speak=(24.1, 39), chunks=[
   "Je m'en suis servi", "presque *tous~les~jours*,", "un été entier.", "Le bureau", "quand il faisait beau,",
   "les bords de Loire,", "*Chambord* avec des copains", "qui suivaient en moto.", "Une voiture de circuit,",
   "utilisée comme une voiture", "de tous les jours."]),
 dict(id="04-revente", name="La revente", window=(42, 50), chunks=[
   "Et puis une société", "me la rachète", "*49~000~euros*,", "pour l'exploiter", "en location sur circuit."]),
 dict(id="05-lecon", name="La leçon et CTA", window=(50, 60), speak=(50.1, 57.4), chunks=[
   "Je ne l'ai pas cherchée,", "elle s'est présentée.", "Comme presque toutes", "mes bonnes opérations.",
   "Mais on ne propose pas", "une voiture à quelqu'un", "qu'on ne connaît pas."]),
]
SPOKEN_SYL = {"40000euros": 5, "premièrevoiture": 5, "790kilos": 8, "golfgti": 4, "touslesjours": 3, "49000euros": 7,
              "x-bow": 2, "ktm": 3}
HOOK = 3.0        # the hook: raw rush, no voice (the voice montage starts after it)
BREATH = 3.0      # engine only, no text, at the end of « les balades »


def norm(tok):
    return re.sub(r"[^\w'’-]", "", tok.lower().replace("*", "").replace("~", ""))


def display(tok):
    return tok.replace("*", "").replace("~", " ")


def syl(tok):
    n = norm(tok)
    if n in SPOKEN_SYL:
        return SPOKEN_SYL[n]
    w = n.rstrip("s").rstrip("e") or n
    return max(1, len(re.findall(r"[aeiouyàâéèêëîïôûùü]+", w)))


def scene_tokens(sc):
    return [t for ch in sc["chunks"] for t in ch.split(" ") if t]


def all_tokens():
    """the whole voice text as tokens, in order (align.py uses it)"""
    return [t for sc in SCENES for t in scene_tokens(sc)]


def provisional():
    words = []
    for sc in SCENES:
        a, b = sc.get("speak", sc["window"])
        toks = scene_tokens(sc)
        pause = [0.30 if re.search(r"[.?!:]$", display(t)) else 0.14 if display(t).endswith(",") else 0 for t in toks]
        pause[-1] = 0
        lead, tail = 0.15, 0.35
        per = (b - a - lead - tail - sum(pause)) / sum(syl(t) for t in toks)
        t = a + lead
        for tok, p in zip(toks, pause):
            d = syl(tok) * per
            words.append({"w": tok, "start": round(t, 3), "end": round(t + d, 3)})
            t += d + p
    return {"duration": SCENES[-1]["window"][1], "words": words}


def snap(t):
    return round(round(t * FPS) / FPS, 3)


def load_words():
    if "--provisional" not in sys.argv and os.path.exists(REAL):
        d = json.load(open(REAL, encoding="utf-8"))
        toks = all_tokens()
        if [norm(w["w"]) for w in d["words"]] != [norm(t) for t in toks]:
            raise SystemExit(f"build: {REAL} does not carry the text of SCENES (re-run align.py)")
        return d, False
    return provisional(), True


def boundaries(d, prov):
    words = d["words"]
    starts, k = [], 0
    for sc in SCENES:
        n = len(scene_tokens(sc))
        starts.append((k, k + n)); k += n
    if prov:
        b = [sc["window"][0] for sc in SCENES] + [SCENES[-1]["window"][1]]
    else:
        b = [0.0]
        for (i, j), (i2, _) in zip(starts, starts[1:]):
            prev_end, nxt = words[j - 1]["end"], words[i2]["start"]
            b.append(snap(max(prev_end + 0.03, nxt - 0.10)))
        b.append(snap(words[-1]["end"] + TAIL))
    return b, starts


# ---------------------------------------------------------------------------------------------------------------------
# shared components (§ = the frame's id prefix, r1- ... r8-)

SHARED_CSS = r"""
    @font-face { font-family: "Anton"; src: url("assets/fonts/Anton-400.woff2") format("woff2"); font-weight: 400; }
    @font-face { font-family: "Instrument Sans"; src: url("assets/fonts/InstrumentSans-700.woff2") format("woff2"); font-weight: 700; }
    @font-face { font-family: "Instrument Sans"; src: url("assets/fonts/InstrumentSans-600.woff2") format("woff2"); font-weight: 600; }
    #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; color: #ffffff;
      font-family: "Instrument Sans", sans-serif; -webkit-font-smoothing: antialiased; }
    .§ground { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; background: transparent; overflow: hidden; }
    .§halo { position: absolute; width: 1200px; height: 1200px; margin: -600px 0 0 -600px; border-radius: 50%;
      background: radial-gradient(closest-side, rgba(251,128,0,0.15) 0%, rgba(251,128,0,0.09) 38%, rgba(251,128,0,0.03) 70%, rgba(251,128,0,0) 100%); }
    .§grain { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0.04; mix-blend-mode: screen; pointer-events: none;
      background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='g'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%25' height='100%25' filter='url(%23g)'/></svg>");
      background-size: 240px 240px; }
    .§cam { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 540px 900px; }
    .§hudcam { transform-origin: 540px 600px; }
    .§abs { position: absolute; }

    /* title: Anton caps, white, centred (title zone y 260-640), orange stroke drawn under the last line */
    .§title { position: absolute; left: 60px; width: 960px; text-align: center; font-family: "Anton", sans-serif; line-height: 1.2;
      text-transform: uppercase; color: #ffffff; white-space: nowrap; }
    .§tline { position: relative; display: inline-block; opacity: 0; }
    .§stilt { position: absolute; left: -0.078em; right: -0.078em; bottom: -0.02em; height: 0.11em; display: block;
      transform: rotate(-1.5deg); transform-origin: 0 50%; }
    .§stk { position: absolute; left: 0; top: 0; width: 100%; height: 100%; display: block; background: #FB8000;
      border-radius: 999px; clip-path: polygon(0 0, 100% 32%, 100% 68%, 0 100%); transform-origin: 0 50%; transform: scaleX(0); }

    /* cash-register counter: one rolling column per digit */
    .§odo { display: inline-block; white-space: nowrap; line-height: 1.15em; height: 1.15em; vertical-align: top; }
    .§oc { display: inline-block; height: 1.15em; overflow: hidden; vertical-align: top; }
    .§ocol { display: block; }
    .§ocol span { display: block; height: 1.15em; line-height: 1.15em; text-align: center; }
    .§os { display: inline-block; height: 1.15em; line-height: 1.15em; vertical-align: top; }

    /* the stage: two buyers, the car between them */
    .§floor { position: absolute; left: 40px; top: 1081px; width: 960px; height: 3px;
      background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.14) 20%, rgba(255,255,255,0.14) 80%, rgba(255,255,255,0)); }
    .§person { position: absolute; transform-origin: 50% 100%; }
    .§pl { position: absolute; left: 0; top: 0; width: 100%; height: 100%; overflow: visible; }
    .§pgrey { fill: #2b2b2b; }
    .§pwhite { fill: #f2f2f2; opacity: 0; }
    .§porange { fill: #FB8000; opacity: 0; }
    .§glow { position: absolute; width: 420px; height: 420px; border-radius: 50%; opacity: 0;
      background: radial-gradient(closest-side, rgba(251,128,0,0.55), rgba(251,128,0,0.18) 55%, rgba(251,128,0,0)); }
    .§car { position: absolute; transform-origin: 50% 100%; }
    .§car svg { position: absolute; left: 0; top: 0; width: 100%; height: 100%; overflow: visible; fill: none;
      stroke-linecap: round; stroke-linejoin: round; }

    /* subtitles: the voice word by word in the band y 1260-1440, the key word turns orange */
    .§sub { position: absolute; left: 0; top: 1260px; width: 1080px; height: 180px; pointer-events: none; }
    .§chunk { position: absolute; left: 40px; top: 55px; width: 1000px; text-align: center; white-space: nowrap;
      font: 700 60px/72px "Instrument Sans", sans-serif; color: #ffffff; text-shadow: 0 3px 18px rgba(0,0,0,0.7); }
    .§w { display: inline-block; opacity: 0; }
"""

SHARED_JS = r"""
      var root = document.querySelector('[data-composition-id="' + FID + '"]');
      function $(id) { var e = root.querySelector("#" + P + id); if (!e) throw new Error(FID + ": #" + P + id + " missing"); return e; }
      var tl = gsap.timeline({ paused: true });
      // word cues: at("virement") = local start of that word in this scene, at("même", 2) = its 2nd occurrence
      function at(w, n) { n = n || 1; var k = 0; for (var i = 0; i < W.length; i++) { if (W[i][0] === w && ++k === n) return W[i][1]; } throw new Error(FID + ": cue " + w + " #" + n); }
      function atEnd(w, n) { n = n || 1; var k = 0; for (var i = 0; i < W.length; i++) { if (W[i][0] === w && ++k === n) return W[i][2]; } throw new Error(FID + ": cue " + w + " #" + n); }
      // state-tracked tweens: every tween is a fromTo from the last known value (seek-safe)
      var S = {};
      function cur(id) { return S[id] || (S[id] = { x: 0, y: 0, scale: 1, rotation: 0, opacity: 1 }); }
      function init(id, p) { var c = cur(id); for (var k in p) c[k] = p[k]; }
      function pre(id, p) { init(id, p); tl.set($(id), p, 0); }
      function go(id, p, t, d, ease) {
        var c = cur(id), from = {}, to = { duration: d == null ? 0.3 : d, ease: ease || "power3.out", immediateRender: false };
        for (var k in p) { from[k] = (k in c) ? c[k] : 0; to[k] = p[k]; c[k] = p[k]; }
        tl.fromTo($(id), from, to, Math.max(0, t));
      }
      function slam(id, t, o) {
        o = o || {}; var c = cur(id);
        tl.fromTo($(id), { opacity: 0, scale: o.s || 1.25, filter: "blur(10px)" },
          { opacity: 1, scale: 1, filter: "blur(0px)", duration: o.d || 0.18, ease: "expo.out", immediateRender: false }, Math.max(0, t));
        c.opacity = 1; c.scale = 1;
      }
      function stroke(tid, t) {
        tl.fromTo($(tid + "-s"), { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, Math.max(0, t));
      }
      function draw(id, t, d, ease) {
        var el = $(id), len = 1000;
        try { len = Math.ceil(el.getTotalLength()) + 2; } catch (e) {}
        el.style.strokeDasharray = len; el.style.strokeDashoffset = len;
        tl.fromTo(el, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: d || 0.3, ease: ease || "power3.out", immediateRender: false }, Math.max(0, t));
      }
      function cam(x, y, s, t, d, ease) { go("cran", { x: x, y: y, scale: s }, t, d || 0.45, ease || "power3.inOut"); }
      function shake(id, t, amp) {
        var e = $(id), a = amp || 14, k = [a, -a * 0.8, a * 0.55, -a * 0.3, 0];
        for (var i = 0; i < k.length; i++) tl.fromTo(e, { x: i ? k[i - 1] : 0 }, { x: k[i], duration: 0.045, ease: "sine.inOut", immediateRender: false }, t + i * 0.045);
      }
      function wobble(id, t, deg) {
        var e = $(id), a = deg || 4, k = [a, -a, a * 0.6, -a * 0.4, 0];
        for (var i = 0; i < k.length; i++) tl.fromTo(e, { rotation: i ? k[i - 1] : 0 }, { rotation: k[i], duration: 0.06, ease: "sine.inOut", immediateRender: false }, t + i * 0.06);
      }
      // a buyer's light: grey | white | orange | dim
      function lit(p, m, t, d) {
        d = d || 0.3;
        go(p + "-w", { opacity: m === "white" ? 1 : 0 }, t, d);
        go(p + "-o", { opacity: m === "orange" ? 1 : 0 }, t, d);
        go(p + "-glow", { opacity: m === "orange" ? 1 : 0 }, t, d);
        go(p, { opacity: m === "dim" ? 0.3 : 1 }, t, d);
      }
      // cash-register counter: every digit column rolls to its target, the two last spin twice
      var O = {};
      function odo(id, t, d, o) {
        o = o || {}; var el = $(id);
        var to = (o.to || el.getAttribute("data-to")).replace(/\D/g, "");
        var cols = el.querySelectorAll(".odo-col"), n = cols.length, st = O[id], i;
        if (to.length !== n) throw new Error(FID + ": odo " + id + " digits " + to);
        if (!st) {
          var fr = (o.from || "").replace(/\D/g, ""); while (fr.length < n) fr = "0" + fr;
          st = O[id] = { pos: [], op: [] };
          for (i = 0; i < n; i++) { st.pos[i] = +fr[i]; st.op[i] = 1; tl.set(cols[i], { yPercent: -100 * st.pos[i] / 30 }, 0); }
        }
        var lead = true;
        for (i = 0; i < n; i++) {
          var a = st.pos[i] % 10, b = +to[i], low = n - i <= 2;
          var spin = a !== b || (low && o.spinLow !== false);
          var ib = spin ? b + 10 * (low ? 2 : 1) : a;
          if (b !== 0) lead = false;
          if (ib !== a) tl.fromTo(cols[i], { yPercent: -100 * a / 30 }, { yPercent: -100 * ib / 30,
            duration: d * (0.5 + 0.5 * (i + 1) / n), ease: "power3.out", immediateRender: false }, Math.max(0, t));
          st.pos[i] = ib;
          if (o.dimLead) {
            var op = lead && i < n - 1 ? 0.12 : 1;
            if (op !== st.op[i]) { tl.fromTo(cols[i].parentNode, { opacity: st.op[i] }, { opacity: op, duration: 0.2, immediateRender: false }, op < 1 ? t + d * 0.7 : t); st.op[i] = op; }
          }
        }
      }
      // subtitles: each word 1 frame before its cue, the chunk leaves at data-out
      function subs() {
        Array.prototype.forEach.call($("sub").querySelectorAll(".sub-chunk"), function (ch) {
          Array.prototype.forEach.call(ch.querySelectorAll(".sub-w"), function (w) {
            var t = Math.max(0, parseFloat(w.getAttribute("data-cue")) - 1 / 30);
            tl.fromTo(w, { opacity: 0, y: 14, filter: "blur(6px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.12, ease: "power3.out", immediateRender: false }, t);
            if (w.classList.contains("sub-key")) tl.fromTo(w, { color: "#ffffff" }, { color: "#FB8000", duration: 0.12, ease: "power3.out", immediateRender: false }, t);
          });
          var out = ch.getAttribute("data-out");
          if (out) tl.fromTo(ch, { opacity: 1, filter: "blur(0px)" }, { opacity: 0, filter: "blur(6px)", duration: 0.1, ease: "power3.out", immediateRender: false }, parseFloat(out));
        });
      }
"""

PERSON = '<circle cx="100" cy="62" r="46"/><path d="M14 300 C14 196 52 146 100 146 C148 146 186 196 186 300 Z"/>'
CAR_SIDE = ('<path d="M28 128 L24 100 Q26 84 46 80 L118 70 L168 34 Q178 27 192 27 L276 27 Q294 27 306 40 L340 74 '
            'L366 80 Q384 85 384 102 L382 128 L336 128"/><path d="M64 128 L24 128"/><path d="M126 128 L274 128"/>'
            '<circle cx="95" cy="128" r="30"/><circle cx="305" cy="128" r="30"/><circle cx="95" cy="128" r="7"/>'
            '<circle cx="305" cy="128" r="7"/><path d="M136 70 L174 40 Q180 36 190 36 L234 36 L234 70 Z"/>'
            '<path d="M248 36 L272 36 Q286 36 296 46 L320 70 L248 70 Z"/>')


def odo(id_, text, cls="", style=""):
    parts = []
    for ch in text:
        if ch.isdigit():
            col = "".join(f"<span>{d % 10}</span>" for d in range(30))
            parts.append(f'<span class="§oc"><span class="§ocol odo-col">{col}</span></span>')
        else:
            parts.append(f'<span class="§os">{"&nbsp;" if ch == " " else ch}</span>')
    st = f' style="{style}"' if style else ""
    return f'<span id="§{id_}" class="§odo {cls}" data-to="{text}"{st}>{"".join(parts)}</span>'


def title(tid, lines, top, size=120, extra=""):
    """lines: list of html strings or (html, font-size) pairs; the stroke goes under the last line"""
    out = []
    for i, l in enumerate(lines):
        html, fs = (l if isinstance(l, tuple) else (l, None))
        stk = f'<i class="§stilt"><i class="§stk" id="§{tid}-s"></i></i>' if i == len(lines) - 1 else ""
        st = f' style="font-size:{fs}px"' if fs else ""
        out.append(f'<span class="§tline" id="§{tid}-{i}"{st}>{html}{stk}</span>')
    return f'<div class="§title" id="§{tid}" style="top:{top}px;font-size:{size}px;{extra}">' + "<br>".join(out) + "</div>"


def person(pid, x, y, w=160):
    h = w * 1.5
    return (f'<div id="§{pid}-glow" class="§glow" style="left:{x + w / 2 - 210:.0f}px;top:{y + h / 2 - 230:.0f}px"></div>'
            f'<div id="§{pid}" class="§person" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px">'
            f'<svg viewBox="0 0 200 300" class="§pl §pgrey">{PERSON}</svg>'
            f'<svg viewBox="0 0 200 300" class="§pl §pwhite" id="§{pid}-w">{PERSON}</svg>'
            f'<svg viewBox="0 0 200 300" class="§pl §porange" id="§{pid}-o">{PERSON}</svg></div>')


def car(cid, x, y, w, color="#ffffff", sw=9):
    h = w * 170 / 410
    return (f'<div id="§{cid}" class="§car" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px">'
            f'<svg viewBox="0 0 410 170" style="stroke:{color};stroke-width:{sw}">{CAR_SIDE}</svg></div>')


def stage(car2=False, extra=""):
    s = '<div class="§floor"></div>'
    if car2:
        s += car("car2", 610, 868, 300, "#8a8a8a", 10)
    s += person("pa", 90, 795, 190) + person("pb", 750, 795, 190)
    s += car("car", 300, 898, 440)
    return s + extra


# ---------------------------------------------------------------------------------------------------------------------
# the 8 scenes: (css, stage html [moves with the camera], hud html [titles, cards], js, halo position)



CUR = {}


def cue(w, n=1):
    hits = [x for x in CUR["W"] if x[0] == w]
    if len(hits) < n:
        raise SystemExit(f"build: scene {CUR['id']}: cue {w} #{n} not in the voice")
    return hits[n - 1][1]


def last_end():
    return CUR["W"][-1][2]


_LEN = {}


def clip_len(cid):
    if cid not in _LEN:
        import subprocess
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                              f"assets/clips/{cid}.mp4"], capture_output=True, text=True).stdout.strip()
        _LEN[cid] = float(out) if out else 6.0
    return _LEN[cid]


MEDIA = []   # root-level videos (clip id, film start, duration, scene id): the assembler wants media in index.html


def vids(shots, end=None):
    """shots: [(clip id, local start)]; each clip runs until the next one starts (the last one until `end` or the scene end)"""
    dur = CUR["dur"] if end is None else end
    for i, (cid, t) in enumerate(shots):
        t = max(0.0, t)
        e = shots[i + 1][1] if i + 1 < len(shots) else dur
        d = e - t
        if d > clip_len(cid) - 0.05:
            raise SystemExit(f"build: scene {CUR['id']}: shot {cid} needs {d:.2f} s, clip has {clip_len(cid):.2f} s")
        MEDIA.append((cid, round(CUR["a"] + t, 3), round(d, 3), CUR["id"]))
    return ""


X_CSS = """
    .§ground { background: transparent !important; }
    #§blk { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; background: #0A0A0A; }
    .§full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; opacity: 0; }
    .§full img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(0.1) contrast(1.06); }
    .§card { position: absolute; overflow: hidden; border: 3px solid #FB8000; border-radius: 6px; opacity: 0; box-shadow: 0 24px 60px rgba(0,0,0,0.6); }
    .§card img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(0.1) contrast(1.06); }
    .§shadeT { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; pointer-events: none;
      background: linear-gradient(rgba(10,10,10,0.75) 0%, rgba(10,10,10,0.2) 26%, rgba(10,10,10,0) 40%, rgba(10,10,10,0) 70%, rgba(10,10,10,0.7) 100%); }
    .§title { text-shadow: 0 4px 26px rgba(0,0,0,0.6); }
    .§tline { opacity: 0; }
    .§o { color: #FB8000; }
    .§cap { position: absolute; left: 0; width: 1080px; text-align: center; font: 74px/1.1 "Anton", sans-serif; color: #fff; white-space: nowrap; opacity: 0;
      text-shadow: 0 3px 20px rgba(0,0,0,0.75); }
    .§sub { top: 1580px !important; }
"""

X_JS = """
      // text: fast fade (6 frames), the orange stroke draws left to right in 6 frames
      function fin(id, t) { pre(id, { opacity: 0 }); go(id, { opacity: 1 }, t, 0.2, "none"); }
      function fout(id, t) { go(id, { opacity: 0 }, t, 0.2, "none"); }
      function stroke6(tid, t) { tl.fromTo($(tid + "-s"), { scaleX: 0 }, { scaleX: 1, duration: 0.2, ease: "none", immediateRender: false }, Math.max(0, t)); init(tid + "-s", { scaleX: 1 }); }
      function tin(tid, n, t) { for (var i = 0; i < n; i++) fin(tid + "-" + i, t); stroke6(tid, t + 0.2); }
      function tout(tid, n, t) { for (var i = 0; i < n; i++) fout(tid + "-" + i, t); go(tid + "-s", { scaleX: 0 }, t, 0.2, "none"); }
      // photos: full frame or card, slow Ken Burns 4 %
      function photo(id, t, t2) { pre(id, { opacity: 0, scale: 1 }); go(id, { opacity: 1 }, t, 0.2, "none"); go(id, { scale: 1.04 }, t, Math.max(0.5, (t2 || DUR) - t), "none"); }
"""


def full(fid, src, pos="50% 50%", contain=True):
    """a photo over the whole frame: the photo whole (contain) on a blurred, darkened copy of itself"""
    if not contain:
        return f'<div id="§{fid}" class="§full"><img src="assets/img/{src}" style="object-position:{pos}"></div>'
    return (f'<div id="§{fid}" class="§full"><img src="assets/img/{src}" style="filter:saturate(0.1) blur(28px) brightness(0.45);transform:scale(1.15)">'
            f'<img src="assets/img/{src}" style="object-fit:contain;object-position:50% 50%"></div>')


def card(fid, src, x, y, w, h, pos="50% 50%"):
    return f'<div id="§{fid}" class="§card" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><img src="assets/img/{src}" style="object-position:{pos}"></div>'


def scene_01():
    st = vids([("hook", 0)], end=HOOK) + full("ph1", "p174045.jpg", "55% 50%") + full("ph2", "p174019.jpg", "45% 50%") + '<div class="§shadeT"></div>'
    hud = ('<div id="§c1" class="§cap" style="top:1500px">JE NE CHERCHAIS PAS</div>'
           '<div id="§c2" class="§cap" style="top:1500px">CETTE <span class="§o">VOITURE</span>.</div>'
           + title("t1", ["ON VIENT ME", "LA PROPOSER."], 290, 120)
           + '<div id="§amt" class="§cap" style="top:330px;font-size:230px">' + odo("am", "40 000 €") + '</div>')
    js = X_JS + f"""
      // hook: the raw rush, text at the bottom, no voice
      fin("c1", 0.15); fout("c1", 1.45); fin("c2", 1.5); fout("c2", {HOOK} - 0.15);
      // the opportunity: still photos, slow zoom
      photo("ph1", {HOOK}, at("jamais")); tl.set($("ph1"), {{ opacity: 1 }}, {HOOK});
      photo("ph2", at("jamais") - 0.2);
      tin("t1", 2, at("propose") - 0.1); tout("t1", 2, at("40000euros") - 0.3);
      fin("amt", at("40000euros") - 0.1); odo("am", at("40000euros") - 0.05, 1.2, {{ from: "00 000", dimLead: true }});
      tl.fromTo($("am"), {{ color: "#ffffff" }}, {{ color: "#FB8000", duration: 0.2, immediateRender: false }}, at("40000euros") + 1.15);
    """
    sfx = []
    return X_CSS, st, hud, js, (540, 900), sfx


MOTO = '<path d="M60 170 a45 45 0 1 0 0.1 0 M300 170 a45 45 0 1 0 0.1 0 M60 170 L140 110 L210 110 L250 70 L280 70 M140 110 L180 170 L300 170 M200 110 L230 60 L200 50" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
XBOW = ('<path d="M20 160 L40 120 L120 100 L170 60 L230 60 L260 100 L330 110 L370 130 L380 160 Z" fill="none" stroke="#fff" stroke-width="12" stroke-linejoin="round"/>'
        '<circle cx="90" cy="165" r="36" fill="#0A0A0A" stroke="#fff" stroke-width="12"/><circle cx="310" cy="165" r="36" fill="#0A0A0A" stroke="#fff" stroke-width="12"/>'
        '<path d="M180 62 L200 30 M215 62 L235 30" stroke="#FB8000" stroke-width="10" stroke-linecap="round"/>')


def scene_02():
    t_pas = cue("pas")
    st = ('<div id="§blk"></div>'
          + f'<svg id="§moto" viewBox="0 0 400 240" style="position:absolute;left:190px;top:700px;width:700px;height:420px;opacity:0;overflow:visible">{MOTO}</svg>'
          + f'<svg id="§xb" viewBox="0 0 400 240" style="position:absolute;left:190px;top:700px;width:700px;height:420px;opacity:0;overflow:visible">{XBOW}</svg>'
          + card("k1", "w05.jpg", 90, 640, 900, 600) + card("k2", "p173948.jpg", 90, 640, 900, 600) + card("k3", "p174010.jpg", 90, 640, 900, 600)
          + vids([("cockpit", t_pas - 0.1)]))
    hud = (title("t1", ["KTM FAIT DES MOTOS."], 300, 110) + title("t2", ['790 KG DE <span class="§o">CARBONE</span>.'], 300, 110)
           + title("t3", ["NI TOIT NI PARE-BRISE."], 300, 110))
    js = X_JS + """
      // the motorbike silhouette turns into the X-Bow on the first line
      tin("t1", 1, Math.max(0.05, at("ktm") - 0.1));
      pre("moto", { opacity: 0 }); go("moto", { opacity: 1 }, Math.max(0.05, at("ktm")), 0.2, "none");
      init("moto", { scaleX: 1 }); go("moto", { opacity: 0, scaleX: 0.6 }, at("premièrevoiture") - 0.3, 0.4, "power2.inOut");
      pre("xb", { opacity: 0, scaleX: 0.6 }); go("xb", { opacity: 1, scaleX: 1 }, at("premièrevoiture") - 0.2, 0.4, "power2.inOut");
      tout("t1", 1, at("monocoque") - 0.25);
      // carbon, weight: detail photos in a thin orange frame
      go("xb", { opacity: 0 }, at("monocoque") - 0.25, 0.2, "none");
      tin("t2", 1, at("monocoque") - 0.1);
      photo("k1", at("monocoque") - 0.1, at("790kilos")); photo("k2", at("790kilos") - 0.1, at("pas"));
      // no roof, no windscreen: the open cockpit, rolling
      tout("t2", 1, at("pas") - 0.25); go("k2", { opacity: 0 }, at("pas") - 0.1, 0.2, "none"); go("k1", { opacity: 0 }, at("790kilos"), 0.2, "none");
      tin("t3", 1, at("pas") - 0.1);
      go("blk", { opacity: 0.0 }, at("pas") - 0.1, 0.2, "none");
    """
    sfx = []
    return X_CSS, st, hud, js, (540, 900), sfx


def scene_03():
    a = 0.0
    T = [0.0, cue("presque") - 0.05, cue("le") - 0.05, cue("quand") - 0.05, cue("les") - 0.05, cue("chambord") - 0.05,
         cue("qui") - 0.05, cue("une") - 0.05]
    end_voice = last_end() + 0.3
    ids = ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8"]
    shots = list(zip(ids, T)) + [("breath", end_voice)]
    st = vids(shots) + '<div id="§fb" style="position:absolute;left:0;top:0;width:1080px;height:1920px;background:#0A0A0A;opacity:0"></div>'
    hud = ('<div id="§c1" class="§cap" style="top:300px;font-size:70px">LE BUREAU, PAR BEAU TEMPS.</div>'
           '<div id="§c2" class="§cap" style="top:300px;font-size:70px"><span class="§o">CHAMBORD</span>, LES COPAINS EN MOTO.</div>')
    js = X_JS + """
      fin("c1", at("le") + 0.1); fout("c1", at("les") - 0.15);
      fin("c2", at("chambord") - 0.05); fout("c2", at("une") - 0.15);
      // breathing: engine only, then fade to black
      pre("fb", { opacity: 0 }); go("fb", { opacity: 1 }, DUR - 0.5, 0.5, "none");
    """
    return X_CSS, st, hud, js, (540, 900), []


def scene_04():
    css = X_CSS + """
    .§box { position: absolute; top: 760px; width: 450px; height: 220px; border-radius: 18px; background: #151515; border: 2px solid #2e2e2e; text-align: center; opacity: 0; }
    .§bl { display: block; margin-top: 30px; font: 44px/1 "Anton", sans-serif; color: #b0b0b0; }
    .§bv { display: block; margin-top: 18px; font: 100px/1 "Anton", sans-serif; color: #fff; }
    #§gain { position: absolute; left: 0; top: 740px; width: 1080px; text-align: center; font: 230px/1 "Anton", sans-serif; color: #FB8000; opacity: 0; }
    """
    st = '<div id="§blk"></div>'
    hud = ('<div id="§b1" class="§box" style="left:60px"><span class="§bl">ACHETÉE</span><span class="§bv">' + odo("bi", "40 000 €") + '</span></div>'
           '<div id="§b2" class="§box" style="left:570px;border-color:#FB8000"><span class="§bl">REVENDUE</span><span class="§bv">' + odo("br", "49 000 €") + '</span></div>'
           '<div id="§gain">+ ' + odo("gv", "9 000 €") + '</div>')
    js = X_JS + """
      odo("bi", 0, 0.01, { from: "40 000", spinLow: false });
      fin("b1", Math.max(0.05, at("et") - 0.05));
      fin("b2", at("49000euros") - 0.1); odo("br", at("49000euros") - 0.05, 1.0, { from: "00 000", dimLead: true });
      fout("b1", at("pour") + 0.1); fout("b2", at("pour") + 0.1);
      fin("gain", at("pour") + 0.35); odo("gv", at("pour") + 0.35, 1.1, { from: "0 000", dimLead: true });
    """
    return css, st, hud, js, (540, 900), []


def scene_05():
    css = X_CSS + """
    #§sm { position: absolute; left: 0; top: 590px; width: 1080px; text-align: center; font: 62px/1.1 "Anton", sans-serif; color: #fff; opacity: 0; text-shadow: 0 3px 20px rgba(0,0,0,0.75); }
    #§hn { position: absolute; left: 0; top: 1080px; width: 1080px; text-align: center; font: 70px/1 "Anton", sans-serif; color: #FB8000; opacity: 0; }
    """
    tc = last_end() + 0.35
    st = ('<div id="§blk"></div>' + full("ph", "p174019.jpg", "50% 50%") + full("fz", "freeze-end.jpg", "50% 50%", contain=False)
          + '<div class="§shadeT"></div>')
    hud = (title("t1", ["LES BONNES AFFAIRES", '<span class="§o">NE SE CHERCHENT PAS.</span>'], 300, 96)
           + '<div id="§sm">ENCORE FAUT-IL ÊTRE <span class="§o">IDENTIFIÉ</span>.</div>'
           + title("t2", ["TU SERAIS ALLÉ", "BOSSER AVEC ÇA ?"], 760, 110) + '<div id="§hn">@guillaumeherbin_</div>')
    js = X_JS + f"""
      // the lesson: a still photo, slower
      pre("ph", {{ opacity: 0 }}); go("ph", {{ opacity: 0.5 }}, 0.05, 0.6, "none"); init("ph", {{ scale: 1 }}); go("ph", {{ scale: 1.03 }}, 0, DUR, "none");
      tin("t1", 2, Math.max(0.1, at("cherchée") - 0.1));
      fin("sm", at("mais") - 0.1);
      // CTA: the last rolling frame, frozen and darkened
      tout("t1", 2, {tc} - 0.2); fout("sm", {tc} - 0.2);
      pre("fz", {{ opacity: 0 }}); go("fz", {{ opacity: 0.35 }}, {tc}, 0.2, "none");
      tin("t2", 2, {tc} + 0.1); fin("hn", {tc} + 0.5);
    """
    return css, st, hud, js, (540, 900), []


BUILDERS = [scene_01, scene_02, scene_03, scene_04, scene_05]


# ---------------------------------------------------------------------------------------------------------------------

def subs_html(chunks_words, scene_end):
    """chunks_words: list of lists of (token, local start, local end)"""
    out = []
    for ci, ch in enumerate(chunks_words):
        last_end = ch[-1][2]
        if ci + 1 < len(chunks_words):
            nxt = chunks_words[ci + 1][0][1]
            o = nxt - 0.06 if nxt - last_end < 0.9 else last_end + 0.45
        else:
            o = last_end + 0.5 if scene_end - last_end > 0.9 else None
        spans = []
        for tok, s, e in ch:
            key = " sub-key" if "*" in tok else ""
            spans.append(f'<span class="§w sub-w{key}" data-cue="{s:.3f}">{display(tok)}</span>')
        do = f' data-out="{max(o, ch[-1][1] + 0.2):.3f}"' if o is not None else ""
        out.append(f'<div class="§chunk sub-chunk"{do}>' + " ".join(spans) + "</div>")
    return "\n      ".join(out)


def build():
    d, prov = load_words()
    B, spans = boundaries(d, prov)
    words = d["words"]
    os.makedirs("compositions/frames", exist_ok=True)
    frames, sfx_all = [], []
    for n, (sc, (i, j), mk) in enumerate(zip(SCENES, spans, BUILDERS), 1):
        a, b = B[n - 1], B[n]
        dur = round(b - a, 3)
        P = f"r{n}-"
        toks = scene_tokens(sc)
        W = [[norm(t), round(words[k]["start"] - a, 3), round(words[k]["end"] - a, 3)] for t, k in zip(toks, range(i, j))]
        # chunks with local timings
        cw, k = [], 0
        for ch in sc["chunks"]:
            tt = [t for t in ch.split(" ") if t]
            cw.append([(t, W[k + m][1], W[k + m][2]) for m, t in enumerate(tt)]); k += len(tt)
        CUR.update(W=W, a=a, dur=dur, id=sc['id'])
        css, st, hud, js, halo, sfx = mk()
        # every cue used in the js must exist in this scene's words
        names = [w[0] for w in W]
        for m in re.finditer(r'at(?:End)?\("([^"]+)"(?:,\s*(\d+))?\)', js):
            if names.count(m.group(1)) < int(m.group(2) or 1):
                raise SystemExit(f"build: scene {sc['id']}: cue {m.group(1)} #{m.group(2) or 1} not in the voice")
        for name, w, occ, off, vol in sfx:
            t = off if w is None else [x[1] for x in W if x[0] == w][occ - 1] + off
            sfx_all.append([name, round(a + max(0, t), 3), vol])
        if n > 1:
            sfx_all.append(["whoosh-short", round(max(0, a - 0.03), 3), 0.16])
        html = f"""<template>
  <style>{SHARED_CSS}{css}  </style>

  <div id="root" data-composition-id="{sc['id']}" data-width="1080" data-height="1920" data-duration="{dur}">
    <div id="§ground" class="clip §ground" data-start="0" data-duration="{dur}" data-track-index="0">
      <div class="§grain"></div>
    </div>
    <div id="§push" class="§cam"><div id="§shk" class="§cam"><div id="§cran" class="§cam">
      {st}
    </div></div></div>
    <div id="§hud" class="§cam §hudcam">
      {hud}
    </div>
    <div id="§sub" class="§sub">
      {subs_html(cw, dur)}
    </div>
  </div>

  <script src="assets/vendor/gsap.min.js"></script>
  <script>
    (function () {{
      var FID = "{sc['id']}", P = "§", DUR = {dur};
      // word cues of this scene (local seconds), written by build.py from the voice timings
      var W = {json.dumps(W, ensure_ascii=False)};
{SHARED_JS}
      tl.fromTo($("push"), {{ scale: 1 }}, {{ scale: 1 + Math.min(0.012 * DUR, 0.05), duration: DUR, ease: "none" }}, 0);
      tl.fromTo($("hud"), {{ scale: 1 }}, {{ scale: 1 + 0.005 * DUR, duration: DUR, ease: "none" }}, 0);
{js}
      subs();
      tl.set({{}}, {{}}, DUR);
      window.__timelines = window.__timelines || {{}};
      window.__timelines[FID] = tl;
    }})();
  </script>
</template>
"""
        html = html.replace("§", P)
        src = f"compositions/frames/{sc['id']}.html"
        open(src, "w", encoding="utf-8").write(html)
        frames.append(dict(n=n, id=sc["id"], name=sc["name"], start=a, end=b, dur=dur, src=src,
                           vo=" ".join(display(t) for t in toks)))
    total = round(B[-1], 3)
    json.dump({"provisional": prov, "total": total, "frames": frames}, open("timings.json", "w"), ensure_ascii=False, indent=1)
    json.dump(MEDIA, open("media.json", "w"), indent=0)
    sfx_all.sort(key=lambda x: x[1])
    open("assets/audio/sfx-events.json", "w").write("[" + ",\n ".join(json.dumps(e) for e in sfx_all) + "]\n")
    write_storyboard(frames, total)
    print(("PROVISIONAL timing (brief windows)" if prov else "timing from " + REAL) + f": {len(frames)} frames, {total:.2f} s")
    for f in frames:
        print(f"  {f['n']} {f['id']:<15} {f['start']:6.2f} -> {f['end']:6.2f}  ({f['dur']:.2f} s)")


def write_storyboard(frames, total):
    s = f"""---
format: 1080x1920
duration: "{total}s"
message: "Deux ans à Dubaï : les rassemblements auto n'y ont rien à voir avec la France (nombre, niveau, indifférence, détails) ; même après seize ans dans l'auto, on y redevient spectateur."
arc: Hook → Le nombre → Le niveau → L'indifférence → Les détails → Le regard du pro → CTA
audience: "Personnes qui veulent se lancer dans l'achat-revente automobile"
mode: autonomous
captions: disabled
music: "pre-mixed with voice and SFX in assets/audio/mix.wav (mounted at root by the orchestrator)"
direction: "découpage écrit par Guillaume (SCRIPT.md), reel 9:16"
styleframes: "aucune"
patterns: ../patterns/STORYBOARD-CRAFT.md, ../patterns/PATTERNS.md
---

<!-- generated by build.py: edit build.py, not this file -->

## Video direction

- **One world** : fond #0A0A0A, accent unique #FB8000, texte blanc ; titres Anton en capitales avec le trait orange tracé dessous ; sous-titres de la voix mot par mot, mot-clé en orange.
- **Seams** : coupes franches sur la voix à chaque scène (whoosh court).
- **Timing** : chaque animation est posée sur un mot de la voix (build.py), les durées des scènes suivent la piste voix.
- **Negative list** : rushes de Guillaume uniquement (pas de facecam) ; plaques floutées ; jamais plus de 6 mots par bloc ; carte grise « EN FRANCE » 1 s à chaque fait.

"""
    for f in frames:
        s += f"""## Frame {f['n']}: {f['name']} · {f['start']:.2f} → {f['end']:.2f}

- scene: {f['name']}
- duration: {f['dur']:.2f}s
- transition_in: cut
- status: animated
- src: {f['src']}
- voiceover: "{f['vo']}"
- type: {"hook" if f['n'] == 1 else "cta" if f['n'] == len(frames) else "demo"}
- blueprint: none
- focal: {f['name']}
- rules: kinetic-beat-slam, svg-path-draw, counting-dynamic-scale
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)
- handoff_out: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)

"""
    open("STORYBOARD.md", "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    build()
