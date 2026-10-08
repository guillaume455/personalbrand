#!/usr/bin/env python3
"""Reel « Les rassemblements auto à Dubaï » : one source for the whole film.

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
TAIL = 1.8          # hold after the last word (end card)
FPS = 30

# ---------------------------------------------------------------------------------------------------------------------
# The voice, scene by scene, cut into subtitle chunks (2 to 5 words). *word* = key word (orange). ~ glues two tokens
# into one subtitle word (« 10~000 », « voitures~? »). Numbers are spoken « dix mille », « deux mille vingt-six ».
SCENES = [
 dict(id="01-hook", name="Hook", window=(0, 5), chunks=[
   "J'ai vécu deux ans", "à *Dubaï*.", "Les rassemblements de voitures", "là-bas,", "c'est pas le même *délire*",
   "qu'en France."]),
 dict(id="02-nombre", name="Le nombre", window=(5, 18), chunks=[
   "Premier *choc*~:", "le nombre.", "*Plusieurs~centaines* de voitures,", "un dimanche comme un autre", "dans des lieux",
   "prévus pour *recevoir*~:", "*animations*,", "*restauration*,", "programme avec des *shows*...", "En France,",
   "un bon rassemblement,", "c'est *cinquante* voitures", "sur le parking", "d'un centre commercial."]),
 dict(id="03-niveau", name="Le niveau", window=(18, 28), chunks=[
   "Deuxième *choc*~:", "le niveau.", "*Bugatti*,", "*Rolls*,", "*Bentley*,", "des préparations", "à *six* chiffres.",
   "Là-bas,", "c'est le parc *normal*.", "En France, une *Porsche*", "arrive et tout le monde", "se retourne."]),
 dict(id="04-indifference", name="L'indifférence", window=(28, 36), chunks=[
   "Troisième *choc*~:", "personne ne *regarde*.", "Une voiture", "à un *million* passe,", "les gens continuent",
   "leur café.", "C'est ça", "qui m'a le plus marqué~:", "là-bas,", "l'exceptionnel est *banal*."]),
 dict(id="05-details", name="Les détails", window=(36, 44), chunks=[
   "Et puis les *détails*.", "Personne ne vient", "avec une voiture d'origine.", "*Couleur* sur mesure,",
   "*intérieur* refait,", "*jantes* forgées.", "Et toutes", "en *état~concours*,", "comme si elles", "sortaient d'usine."]),
 dict(id="06-regard", name="Le regard du pro", window=(44, 52), chunks=[
   "*Seize* ans", "que je vends des voitures.", "J'en ai vu passer", "des *milliers*.", "Et là-bas,", "j'ai regardé",
   "comme un *gamin*.", "Ça fait du bien", "de redevenir *spectateur*."]),
 dict(id="07-cta", name="CTA", window=(52, 56), chunks=[
   "Deux ans aux *Émirats*,", "j'en ai ramené", "des souvenirs.", "Si tu veux les suivantes,", "*abonne-toi*."]),
]
SPOKEN_SYL = {"plusieurscentaines": 4, "étatconcours": 4, "shows": 1, "bugatti": 3, "rolls": 1, "bentley": 2, "porsche": 2}
RED = "#B3261E"


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
        a, b = sc["window"]
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



#  the footage: every scene plays clips cut by cut-clips.py (shots.py); cuts land on words, and in scene 3 on the beat
BEAT0, BEAT = 17.75, 0.4644      # film time of the music drop (MUS_START 58.10 in build-mix.sh) and the beat period
CUR = {}                          # the scene being built: words (local), start, duration


def cue(w, n=1):
    hits = [x for x in CUR["W"] if x[0] == w]
    if len(hits) < n:
        raise SystemExit(f"build: scene {CUR['id']}: cue {w} #{n} not in the voice")
    return hits[n - 1][1]


def beat(k):
    return BEAT0 + k * BEAT - CUR["a"]


_LEN = {}
MEDIA = []   # root-level videos (clip id, film start, duration): the assembler wants media in index.html


def clip_len(cid):
    if cid not in _LEN:
        import subprocess
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                              f"assets/clips/{cid}.mp4"], capture_output=True, text=True).stdout.strip()
        _LEN[cid] = float(out) if out else 6.0
    return _LEN[cid]


def vids(shots):
    """shots: [(clip id, local start[, play length])]; each clip runs until the next one starts (or for its play length)"""
    out, dur = [], CUR["dur"]
    for i, s in enumerate(shots):
        cid, t = s[0], max(0.0, s[1])
        end = shots[i + 1][1] if i + 1 < len(shots) else dur
        d = s[2] if len(s) > 2 else end - t
        if d > clip_len(cid) - 0.05:
            raise SystemExit(f"build: scene {CUR['id']}: shot {cid} needs {d:.2f} s, clip has {clip_len(cid):.2f} s")
        MEDIA.append((cid, round(CUR["a"] + t, 3), round(d, 3)))
    return ""


VID_CSS = """
    @font-face { font-family: "Space Mono"; src: url("assets/fonts/SpaceMono-700.woff2") format("woff2"); font-weight: 700; }
    .§vid { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
    .§still { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; opacity: 0; }
    .§shade { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; pointer-events: none;
      background: linear-gradient(rgba(0,0,0,0.62) 0%, rgba(0,0,0,0.25) 22%, rgba(0,0,0,0) 34%, rgba(0,0,0,0) 54%, rgba(0,0,0,0.55) 68%, rgba(0,0,0,0.78) 100%); }
    .§title { text-shadow: 0 4px 26px rgba(0,0,0,0.65); }
    .§or { color: #FB8000; }
    #§kick { position: absolute; left: 0; top: 250px; width: 1080px; text-align: center; font: 700 36px/1 "Space Mono", monospace; color: #FB8000;
      letter-spacing: 0.12em; text-shadow: 0 2px 14px rgba(0,0,0,0.7); opacity: 0; }
    .§lab { position: absolute; left: 0; top: 330px; width: 1080px; text-align: center; font: 118px/1.1 "Anton", sans-serif; color: #ffffff;
      text-shadow: 0 4px 26px rgba(0,0,0,0.7); white-space: nowrap; opacity: 0; }
    .§fr { position: absolute; left: 50px; top: 1100px; padding: 14px 24px 16px; border-radius: 12px; background: rgba(26,26,26,0.92);
      border-left: 6px solid #8a8a8a; opacity: 0; }
    .§frk { display: block; font: 700 22px/1 "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.16em; }
    .§frt { display: block; margin-top: 8px; font: 46px/1.1 "Anton", sans-serif; color: #d6d6d6; white-space: nowrap; }
    .§frame { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; pointer-events: none; }
    .§frame rect { fill: none; stroke: #FB8000; stroke-width: 7; }
"""

VID_JS = """
      // a word label (model name, fact): slams in at t, leaves at out
      function label(id, t, out) { pre(id, { opacity: 0 }); slam(id, t); if (out != null) go(id, { opacity: 0 }, out, 0.12); }
      // « EN FRANCE » card: slides in bottom left, stays one second
      function card(id, t, hold) { pre(id, { opacity: 0, x: -40 }); go(id, { opacity: 1, x: 0 }, t, 0.25); go(id, { opacity: 0, x: -20 }, t + (hold || 1.1), 0.25, "power2.in"); }
      function tshow(tid, n, cues) { for (var i = 0; i < n; i++) slam(tid + "-" + i, cues[i] - 0.05); stroke(tid, cues[n - 1] + 0.15); init(tid + "-s", { scaleX: 1 }); }
      function thide(tid, n, t) { for (var i = 0; i < n; i++) go(tid + "-" + i, { opacity: 0 }, t, 0.15); go(tid + "-s", { scaleX: 0 }, t, 0.15); }
      function kick(t, out) { pre("kick", { opacity: 0, y: 14 }); go("kick", { opacity: 1, y: 0 }, t, 0.25); if (out != null) go("kick", { opacity: 0 }, out, 0.15); }
"""


def frcard(fid, text):
    return f'<div id="§{fid}" class="§fr"><span class="§frk">EN FRANCE</span><span class="§frt">{text}</span></div>'


def frame_rect(fid, x, y, w, h):
    return (f'<svg class="§frame" viewBox="0 0 1080 1920"><rect id="§{fid}" x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/></svg>')


SHADE = '<div class="§shade"></div>'


def scene_01():
    shots = [("chiron", 0), ("rollsrow", cue("voitures") - 0.05)]
    hud = (SHADE + '<div id="§kick">DUBAÏ · 2024-2026</div>' + title("t1", ["EN FRANCE,", "ÇA N'<span class=\"§or\">EXISTE</span> PAS."], 300, 112))
    js = VID_JS + """
      kick(at("dubaï") - 0.05);
      go("kick", { opacity: 0 }, at("même") - 0.2, 0.15);
      tshow("t1", 2, [at("même"), at("france")]);
    """
    sfx = [("impact-bass-2", None, 0, 0.0, .2), ("whoosh-short", "voitures", 1, -.1, .14), ("pop", "même", 1, -.05, .14),
           ("impact-bass-2", "france", 1, -.05, .22)]
    return VID_CSS, vids(shots), hud, js, (540, 900), sfx


def scene_02():
    shots = [("wide1", 0), ("lot", cue("plusieurscentaines") - 0.1), ("crowd", cue("un") - 0.05),
             ("anim", cue("animations") - 0.05), ("resto", cue("restauration") - 0.05), ("drift", cue("programme") - 0.05),
             ("wide2", cue("en") - 0.05)]
    hud = (SHADE + '<div id="§kick">CHOC N°1</div>' + title("t1", ["LE NOMBRE."], 320, 130)
           + title("t2", ['<span class="§or">PLUSIEURS</span>', '<span class="§or">CENTAINES</span>', "DE VOITURES."], 300, 112)
           + '<div id="§l1" class="§lab">ANIMATIONS</div><div id="§l2" class="§lab">RESTAURATION</div><div id="§l3" class="§lab">SHOWS</div>'
           + frcard("fr", "50 VOITURES SUR UN PARKING"))
    js = VID_JS + """
      kick(Math.max(0.02, at("premier") - 0.05), at("plusieurscentaines") - 0.15);
      tshow("t1", 1, [at("nombre")]); thide("t1", 1, at("plusieurscentaines") - 0.15);
      tshow("t2", 3, [at("plusieurscentaines"), at("plusieurscentaines") + 0.35, at("voitures")]);
      thide("t2", 3, at("animations") - 0.12);
      label("l1", at("animations") - 0.05, at("restauration") - 0.08);
      label("l2", at("restauration") - 0.05, at("programme") - 0.08);
      label("l3", at("shows") - 0.08, at("en") - 0.1);
      card("fr", at("france"), 1.3);
    """
    sfx = [("whoosh-short", "plusieurscentaines", 1, -.12, .14), ("impact-bass-2", "plusieurscentaines", 1, 0, .22),
           ("pop", "animations", 1, -.05, .12), ("pop", "restauration", 1, -.05, .12), ("pop", "shows", 1, -.08, .12),
           ("click-soft", "france", 1, 0, .2)]
    return VID_CSS, vids(shots), hud, js, (540, 900), sfx


def scene_03():
    shots = [("brabus", 0), ("bugatti", beat(4)), ("rolls", beat(5)), ("bentley", beat(6)), ("urus", beat(8)),
             ("sixsix", beat(10)), ("parc", beat(12)), ("sf90", beat(15))]
    labs = [("bugatti", "BUGATTI", 4, 5), ("rolls", "ROLLS-ROYCE", 5, 6), ("bentley", "BENTLEY", 6, 8), ("urus", "MANSORY", 8, 10),
            ("sixsix", "BRABUS 6X6", 10, 12)]
    hud = (SHADE + '<div id="§kick">CHOC N°2</div>' + title("t1", ["LE NIVEAU."], 320, 130)
           + "".join(f'<div id="§l{k}" class="§lab">{txt}</div>' for k, txt, a, b in labs)
           + title("t2", ["LE PARC", '<span class="§or">NORMAL</span>.'], 300, 120)
           + frcard("fr", "1 PORSCHE : TOUS SE RETOURNENT"))
    js = VID_JS + "\n".join(f'      label("l{k}", {beat(a):.3f} - 0.02, {beat(b):.3f} - 0.06);' for k, txt, a, b in labs) + """
      kick(Math.max(0.02, at("deuxième") - 0.05), at("bugatti") - 0.2);
      tshow("t1", 1, [at("niveau")]); thide("t1", 1, at("bugatti") - 0.15);
      tshow("t2", 2, [at("parc"), at("normal")]); thide("t2", 2, at("en") - 0.1);
      card("fr", at("france"), 1.4);
    """
    sfx = [("whoosh-short", "bugatti", 1, -.05, .12), ("pop", "rolls", 1, -.2, .12), ("pop", "bentley", 1, -.02, .12),
           ("pop", "six", 1, -.02, .12), ("impact-bass-2", "normal", 1, -.05, .2), ("click-soft", "france", 1, 0, .2)]
    return VID_CSS, vids(shots), hud, js, (540, 900), sfx


FERRARI_FREEZE = 0.83


def scene_04():
    tf = cue("une") - 0.05
    shots = [("walk", 0), ("ferrari", tf, FERRARI_FREEZE), ("sunset", cue("c'est") - 0.05)]
    st = (vids(shots) + '<img id="§fz" class="§still" src="assets/img/freeze-ferrari.jpg">' + frame_rect("fq", 290, 540, 780, 820))
    hud = (SHADE + '<div id="§kick">CHOC N°3</div>' + title("t1", ["PERSONNE NE", '<span class="§or">REGARDE</span>.'], 300, 120)
           + title("t2", ["L'EXCEPTIONNEL", 'EST <span class="§or">BANAL</span>.'], 300, 120)
           + frcard("fr", "UNE BELLE VOITURE = UN ATTROUPEMENT"))
    js = VID_JS + f"""
      kick(Math.max(0.02, at("troisième") - 0.05), at("personne") - 0.15);
      tshow("t1", 2, [at("personne"), at("regarde")]);
      // the million car: the picture freezes, an orange frame draws round it, nobody turns
      pre("fz", {{ opacity: 0 }}); go("fz", {{ opacity: 1 }}, {tf + FERRARI_FREEZE:.3f}, 0.01);
      init("fz", {{ scale: 1 }}); go("fz", {{ scale: 1.05 }}, {tf + FERRARI_FREEZE:.3f}, 2.0, "sine.out");
      draw("fq", {tf + FERRARI_FREEZE:.3f} + 0.05, 0.5, "power2.inOut");
      go("fz", {{ opacity: 0 }}, at("c'est") - 0.05, 0.01); go("fq", {{ opacity: 0 }}, at("c'est") - 0.05, 0.01);
      thide("t1", 2, at("c'est") - 0.1);
      tshow("t2", 2, [at("l'exceptionnel"), at("banal")]);
      card("fr", at("banal") + 0.1, 1.2);
    """
    sfx = [("click-soft", "million", 1, -.02, .25), ("whoosh-short", "c'est", 1, -.1, .14), ("impact-bass-2", "banal", 1, -.05, .22)]
    return VID_CSS, st, hud, js, (540, 900), sfx


def scene_05():
    shots = [("lowrider", 0), ("gt", cue("couleur") - 0.05), ("orange", cue("intérieur") - 0.05), ("jantes", cue("jantes") - 0.05),
             ("concours", cue("et", 2) - 0.05)]
    hud = (SHADE + title("t1", ["LES", '<span class="§or">DÉTAILS</span>.'], 300, 130)
           + title("t2", ["0 VOITURE", "D'ORIGINE."], 300, 120)
           + '<div id="§l1" class="§lab">COULEUR<br><span class="§or">SUR MESURE</span></div>'
           + '<div id="§l2" class="§lab">INTÉRIEUR<br><span class="§or">REFAIT</span></div>'
           + '<div id="§l3" class="§lab">JANTES<br><span class="§or">FORGÉES</span></div>'
           + '<div id="§l4" class="§lab">ÉTAT<br><span class="§or">CONCOURS</span></div>'
           + frcard("fr", "100 % D'ORIGINE, RAYURES COMPRISES"))
    js = VID_JS + """
      tshow("t1", 2, [Math.max(0.05, at("les")), at("détails")]); thide("t1", 2, at("personne") - 0.12);
      tshow("t2", 2, [at("personne"), at("d'origine")]); thide("t2", 2, at("couleur") - 0.12);
      label("l1", at("couleur") - 0.05, at("intérieur") - 0.08);
      label("l2", at("intérieur") - 0.05, at("jantes") - 0.08);
      label("l3", at("jantes") - 0.05, at("et", 2) - 0.08);
      label("l4", at("étatconcours") - 0.05);
      card("fr", at("d'usine") - 0.1, 1.1);
    """
    sfx = [("pop", "détails", 1, -.05, .14), ("pop", "couleur", 1, -.05, .14), ("pop", "intérieur", 1, -.05, .14),
           ("pop", "jantes", 1, -.05, .14), ("impact-bass-2", "étatconcours", 1, -.05, .2), ("click-soft", "d'usine", 1, -.1, .2)]
    return VID_CSS, vids(shots), hud, js, (540, 900), sfx


ENZO_FREEZE = 1.5


def scene_06():
    shots = [("enzo", 0, ENZO_FREEZE), ("phantom", cue("et") - 0.05)]
    st = vids(shots) + '<img id="§fz" class="§still" src="assets/img/freeze-enzo.jpg">' + frame_rect("fq", 296, 806, 734, 534)
    hud = (SHADE + title("t1", ['<span class="§or">16 ANS</span>', "DANS L'AUTO."], 300, 130)
           + title("t2", ["COMME", 'UN <span class="§or">GAMIN</span>.'], 300, 130)
           + title("t3", ["REDEVENIR", '<span class="§or">SPECTATEUR</span>.'], 300, 120))
    js = VID_JS + f"""
      tshow("t1", 2, [Math.max(0.05, at("seize")), at("voitures")]);
      // a calm shot: the Enzo freezes inside an orange frame
      pre("fz", {{ opacity: 0 }}); go("fz", {{ opacity: 1 }}, {ENZO_FREEZE}, 0.01);
      init("fz", {{ scale: 1 }}); go("fz", {{ scale: 1.04 }}, {ENZO_FREEZE}, 2.5, "sine.out");
      draw("fq", {ENZO_FREEZE} + 0.05, 0.6, "power2.inOut");
      go("fz", {{ opacity: 0 }}, at("et") - 0.05, 0.01); go("fq", {{ opacity: 0 }}, at("et") - 0.05, 0.01);
      thide("t1", 2, at("et") - 0.1);
      tshow("t2", 2, [at("comme"), at("gamin")]); thide("t2", 2, at("ça") - 0.1);
      tshow("t3", 2, [at("redevenir"), at("spectateur")]);
    """
    sfx = [("click-soft", None, 0, ENZO_FREEZE, .22), ("whoosh-short", "et", 1, -.1, .12), ("pop", "gamin", 1, -.05, .14),
           ("impact-bass-2", "spectateur", 1, -.05, .2)]
    return VID_CSS, st, hud, js, (540, 900), sfx


def scene_07():
    css = VID_CSS + """
    #§dim { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; background: #0A0A0A; opacity: 0; }
    #§handle { position: absolute; left: 60px; top: 1040px; width: 960px; text-align: center; white-space: nowrap; }
    #§hname { position: relative; display: inline-block; font: 96px/1.2 "Anton", sans-serif; color: #ffffff; opacity: 0; }
    #§pill { position: absolute; left: 50%; top: 175px; transform: translateX(-50%); }
    #§pilli { display: inline-block; padding: 8px 40px; border-radius: 40px; background: #FB8000; color: #0A0A0A; font: 52px/1.25 "Anton", sans-serif; opacity: 0;
      box-shadow: 0 0 46px rgba(251,128,0,0.45); }
    #§me { position: absolute; left: 240px; top: 410px; width: 600px; height: 700px; overflow: hidden; opacity: 0;
      -webkit-mask-image: linear-gradient(#000 72%, transparent 100%); mask-image: linear-gradient(#000 72%, transparent 100%); }
    #§me img { position: absolute; left: 0; top: 0; width: 600px; height: auto; }
    #§meglow { position: absolute; left: 290px; top: 380px; width: 500px; height: 500px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, rgba(251,128,0,0.55) 0%, rgba(251,128,0,0.18) 45%, rgba(251,128,0,0) 70%); }
    """
    st = vids([("fin", 0)]) + '<div id="§dim"></div><div id="§meglow"></div><div id="§me"><img src="assets/img/guillaume.png"></div>'
    hud = (SHADE + title("t7", ['2 ANS AUX <span class="§or">ÉMIRATS</span>.', "DES SOUVENIRS."], 560, 100)
           + '<div id="§handle"><span id="§hname">@guillaumeherbin_<i class="§stilt"><i class="§stk" id="§h-s"></i></i></span>'
             '<div id="§pill"><span id="§pilli">S’ABONNER</span></div></div>')
    js = VID_JS + """
      tshow("t7", 2, [Math.max(0.05, at("deux")), at("souvenirs")]);
      // subscribe: the shot darkens, the title goes up, the photo, the handle, the button
      var tc = at("si") - 0.1;
      pre("dim", { opacity: 0 }); go("dim", { opacity: 0.82 }, tc, 0.4);
      init("t7", { y: 0, scale: 1 }); go("t7", { y: -440, scale: 0.68 }, tc, 0.5, "power3.inOut");
      pre("me", { opacity: 0, y: 60 }); go("me", { opacity: 1, y: 0 }, tc + 0.15, 0.6, "power3.out");
      pre("meglow", { opacity: 0, scale: 0.6 }); go("meglow", { opacity: 1, scale: 1 }, tc + 0.25, 0.7, "power2.out");
      slam("hname", at("abonne-toi") - 0.05, { s: 1.3 }); stroke("h", at("abonne-toi") + 0.15);
      pre("pilli", { opacity: 0, scale: 0.5 }); go("pilli", { opacity: 1, scale: 1 }, at("abonne-toi") + 0.25, 0.3, "back.out(2)");
    """
    sfx = [("pop", "émirats", 1, -.05, .14), ("whoosh-short", "si", 1, -.1, .14), ("notification", "abonne-toi", 1, 0, .25)]
    return css, st, hud, js, (540, 900), sfx


BUILDERS = [scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07]


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
