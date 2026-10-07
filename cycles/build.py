#!/usr/bin/env python3
"""Reel « 3 voitures, 3 cycles de vente » : one source for the whole film.

Every animation of every scene is placed on a WORD of the voice (at("virement"), at("même", 2)...), never on a fixed
second. The word timings come from one file:
  - assets/audio/voix-montage-mots.json when the real voice is there (align.py writes it), or
  - a provisional timing spread over the brief's windows (0-4, 4-16, 16-28, 28-40, 40-49, 49-62, 62-70 s).
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
 dict(id="01-hook", name="Hook", window=(0, 4), chunks=[
   "Tu as *30~000* euros", "pour démarrer", "et *douze* mois devant toi.", "Trois façons", "de les *placer*.", "Une seule sort", "vraiment du *lot*,", "je t'explique."]),
 dict(id="02-sportive", name="Option 1, la sportive", window=(4, 16), chunks=[
   "Option un~:", "une *sportive*.", "Achetée 30~000,", "revendue 35~000.", "*5~000* euros de marge,", "c'est beau.",
   "Mais son délai", "de *rotation* de stock,", "c'est quatre mois.", "*Trois* cycles de vente", "sur douze *mois*.",
   "*15~000* euros."]),
 dict(id="03-suv-citadine", name="Option 2, SUV + citadine", window=(16, 28), chunks=[
   "Option deux~:", "un *SUV* à 20~000", "et une *citadine* à 10~000.", "Le SUV fait 3~000 de marge",
   "et tourne en 30 jours~:", "*douze* cycles de vente,", "36~000 euros.", "La citadine fait 1~500",
   "et tourne en 15 jours~:", "*vingt-quatre* cycles,", "36~000 aussi.", "Total~:", "*72~000* euros."]),
 dict(id="04-citadines", name="Option 3, trois citadines", window=(28, 40), chunks=[
   "Option trois~:", "trois *citadines*.", "1~500 euros de marge", "chacune,", "15 jours de rotation.",
   "Sur le papier,", "*108~000* euros", "dans l'année.", "Soyons honnêtes~:", "enchaîner *72* cycles", "de vente,",
   "c'est un vrai *métier*.", "Divise par *deux*.", "Tu es encore", "à *54~000*."]),
 dict(id="05-verdict", name="Le verdict", window=(40, 49), chunks=[
   "Même *budget* de départ.", "La voiture à la plus", "grosse *marge*", "est celle qui te rapporte", "le *moins*.",
   "Ce qui compte,", "c'est pas la marge", "d'une vente.", "C'est la *rotation*", "de ta trésorerie~:", "combien de fois",
   "ton argent *revient*", "dans l'année."]),
 dict(id="06-risque", name="Le risque", window=(49, 62), chunks=[
   "Et je n'ai pas encore", "parlé du *risque*.", "En tant que pro,", "tu es tenu par", "la *garantie* légale",
   "de conformité", "et par les *vices* cachés.", "Une *panne* sur une sportive,", "ça se paie", "au prix d'une sportive.",
   "La même panne", "sur une citadine,", "c'est *cinq* fois moins.", "La voiture la plus chère,", "c'est aussi celle",
   "qui te coûte le plus *cher*", "quand ça casse."]),
 dict(id="07-regle", name="La règle et CTA", window=(62, 70), chunks=[
   "Ce que tu *gagnes*,", "c'est ta *marge*", "fois ton nombre", "de *cycles* de vente.", "Au début, prends",
   "les voitures qui tournent *vite*", "et qui cassent pas *cher*.", "*Abonne-toi*", "pour plus de contenu", "comme celui-ci."]),
]
SPOKEN_SYL = {"30000": 3, "35000": 4, "5000": 2, "15000": 3, "20000": 3, "10000": 2, "3000": 2, "30": 2, "36000": 4,
              "1500": 4, "15": 2, "72000": 4, "108000": 3, "72": 3, "54000": 5, "suv": 3}
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
    .§ground { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; background: #0A0A0A; overflow: hidden; }
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



PHOTO_CSS = """
    .§photo { position: absolute; border: 4px solid #FB8000; border-radius: 10px; overflow: hidden; box-shadow: 0 30px 70px rgba(0,0,0,0.6); }
    .§photo img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(0.8) contrast(1.04); }
"""
# the 12-month timeline: lanes of sale cycles, the car token advances one cycle at a time, a counter per lane at the right
FR_X, FR_W, FR_TOP = 150, 520, 985
FRISE_CSS = """
    #§fr { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
    .§mo { position: absolute; top: %dpx; width: %.2fpx; text-align: center; font: 700 28px/1 "Instrument Sans", sans-serif; color: #8a8a8a; }
    .§lane { position: absolute; left: %dpx; width: %dpx; height: 54px; border-radius: 27px; background: #181818; border: 2px solid #262626; overflow: hidden; }
    .§seg { position: absolute; top: 0; height: 100%%; background: #FB8000; transform-origin: 0 50%%; transform: scaleX(0); border-right: 3px solid #0A0A0A; }
    .§seg.§alt { background: #d96c00; }
    .§tok { position: absolute; width: 76px; height: 76px; border-radius: 50%%; border: 3px solid #ffffff; overflow: hidden; box-shadow: 0 6px 20px rgba(0,0,0,0.6); }
    .§tok img { width: 100%%; height: 100%%; object-fit: cover; }
    .§lc { position: absolute; left: 725px; width: 220px; text-align: right; font: 52px/1 "Anton", sans-serif; color: #FB8000; }
    .§lcl { display: block; font: 600 18px/1 "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.12em; margin-bottom: 4px; }
""" % (FR_TOP, FR_W / 12, FR_X, FR_W)
FRISE_JS = """
      // a lane: n cycles over the year, from t0 for dur seconds; the token rides the head of the fill
      function lane(L, n, t0, dur, cnt, to) {
        var segW = %(w)f / n, step = dur / n, el = $(L + "-tok");
        for (var k = 0; k < n; k++) {
          var s = root.querySelector("#" + P + L + "-s" + k);
          tl.fromTo(s, { scaleX: 0 }, { scaleX: 1, duration: step * 0.92, ease: n > 6 ? "none" : "power1.inOut", immediateRender: false }, t0 + k * step);
          go(L + "-tok", { x: (k + 1) * segW }, t0 + k * step, step * 0.92, n > 6 ? "none" : "power1.inOut");
        }
        if (cnt) odo(cnt, t0, dur, { to: to, spinLow: true });
      }
""" % {"w": FR_W}


def frise(lanes):
    """lanes: list of (id, n cycles, photo, counter id, counter final text, label)"""
    h = '<div id="§fr">'
    for m, lab in enumerate("JFMAMJJASOND"):
        h += f'<div class="§mo" style="left:{FR_X + m * FR_W / 12:.1f}px">{lab}</div>'
    for i, (lid, n, photo, cid, final, label) in enumerate(lanes):
        y = FR_TOP + 46 + i * 80
        segs = "".join(f'<i id="§{lid}-s{k}" class="§seg{" §alt" if k % 2 else ""}" style="left:{k * FR_W / n:.2f}px;width:{FR_W / n:.2f}px"></i>' for k in range(n))
        h += f'<div class="§lane" style="top:{y}px">{segs}</div>'
        h += f'<div id="§{lid}-tok" class="§tok" style="left:{FR_X - 38}px;top:{y - 11}px"><img src="assets/img/{photo}"></div>'
        if cid:
            zero = "".join("0" if ch.isdigit() else ch for ch in final)
            h += f'<div class="§lc" style="top:{y - 18}px"><span class="§lcl">{label}</span>{odo(cid, final)}</div>'
    return h + "</div>"


def zero(txt):
    return "".join("0" if ch.isdigit() else ch for ch in txt)


def scene_01():
    css = PHOTO_CSS + """
    .§cfg { position: absolute; top: 770px; width: 290px; height: 300px; opacity: 0; }
    .§cfgn { position: absolute; left: 50%; top: -34px; margin-left: -30px; width: 60px; height: 60px; border-radius: 50%; background: #FB8000; color: #0A0A0A;
      font: 40px/60px "Anton", sans-serif; text-align: center; z-index: 2; }
    """
    def cfg(i, x, photos):
        n = len(photos); w = 290
        inner = "".join(f'<div class="§photo" style="left:{0}px;top:{k * (300 / n) + (6 if k else 0)}px;width:{w}px;height:{300 / n - (6 if n > 1 else 0):.0f}px"><img src="assets/img/{p}"></div>'
                        for k, p in enumerate(photos))
        return f'<div id="§c{i}" class="§cfg" style="left:{x}px">{inner}<div class="§cfgn">{i + 1}</div></div>'
    st = cfg(0, 70, ["mustang.jpg"]) + cfg(1, 395, ["x4.jpg", "mini.jpg"]) + cfg(2, 720, ["golf.jpg", "fiat.jpg", "mini.jpg"])
    hud = title("t1", [(odo("bud", "30 000 €"), 230), ("<span style='color:#ffffff'>SUR 12 MOIS</span>", 70)], 300, 120, "color:#FB8000")
    js = """
      slam("t1-0", Math.max(0.02, at("30000") - 0.05), { s: 1.3 }); odo("bud", Math.max(0.02, at("30000") - 0.05), 0.9);
      stroke("t1", at("douze") + 0.3); slam("t1-1", at("douze") - 0.05, { s: 1.3 });
      ["c0", "c1", "c2"].forEach(function (c, k) { pre(c, { opacity: 0, y: 80 }); go(c, { opacity: 1, y: 0 }, at("façons") - 0.1 + k * 0.14, 0.35, "back.out(1.5)"); });
      // only one makes you a living: which one?
      ["c0", "c1", "c2"].forEach(function (c, k) { wobble(c, at("lot") - 0.1 + k * 0.08, 3); });
      cam(0, -10, 1.04, at("seule"), 0.8);
    """
    sfx = [("typing", "30000", 1, -.05, .12), ("pop", "démarrer", 1, 0, .14), ("pop", "façons", 1, -.1, .12),
           ("pop", "façons", 1, .04, .12), ("pop", "façons", 1, .18, .12), ("whoosh-short", "lot", 1, -.1, .12), ("pop", "douze", 1, -.05, .14)]
    return css, st, hud, js, (540, 760), sfx


def stat_rows(rows, top):
    h = ""
    for i, (rid, lab, val, orange) in enumerate(rows):
        col = "#FB8000" if orange else "#ffffff"
        h += (f'<div id="§{rid}" class="§srow" style="top:{top + i * 96}px"><span class="§sl">{lab}</span>'
              f'<span class="§sv" style="color:{col}">{odo(rid + "v", val)}</span></div>')
    return h


STAT_CSS = """
    .§srow { position: absolute; left: 120px; width: 840px; height: 86px; opacity: 0; border-bottom: 2px solid #222; }
    .§sl { position: absolute; left: 0; top: 22px; font: 600 34px/1 "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.08em; }
    .§sv { position: absolute; right: 0; top: 4px; font: 70px/1 "Anton", sans-serif; }
"""


def scene_02():
    css = PHOTO_CSS + FRISE_CSS + STAT_CSS + """
    #§ph { left: 120px; top: 600px; width: 840px; height: 360px; }
    """
    st = ('<div id="§ph" class="§photo"><img src="assets/img/mustang.jpg"></div>'
          + frise([("l1", 3, "mustang.jpg", "c1", "15 000 €", "PAR AN")]))
    hud = (title("t2", ["OPTION 1", "LA SPORTIVE"], 290, 110)
           + stat_rows([("r1", "ACHETÉE", "30 000 €", False), ("r2", "REVENDUE", "35 000 €", False), ("r3", "MARGE", "5 000 €", True)], 270)
           + title("t2b", ["ROTATION : 4 MOIS"], 330, 110))
    js = FRISE_JS + """
      slam("t2-0", Math.max(0.02, at("un") - 0.05)); slam("t2-1", at("sportive") - 0.05); stroke("t2", at("sportive") + 0.15);
      pre("ph", { opacity: 0, scale: 1.08 }); go("ph", { opacity: 1, scale: 1 }, at("sportive") - 0.1, 0.45, "expo.out");
      init("ph", { opacity: 1, scale: 1 }); go("ph", { scale: 1.05 }, at("sportive"), 3, "none");
      go("t2", { opacity: 0, y: -30 }, at("achetée") - 0.32, 0.16, "power2.in");
      [["r1", "achetée"], ["r2", "revendue"], ["r3", "5000"]].forEach(function (r) {
        pre(r[0], { opacity: 0, x: -60 }); go(r[0], { opacity: 1, x: 0 }, at(r[1]) - 0.06, 0.3, "expo.out");
        odo(r[0] + "v", at(r[1]) - 0.02, 0.8, { from: "0" });
      });
      init("r3", { scale: 1 }); go("r3", { scale: 1.04 }, at("beau") - 0.05, 0.15); go("r3", { scale: 1 }, at("beau") + 0.1, 0.3);
      // but the rotation is 4 months: three sale cycles in the year
      ["r1", "r2", "r3"].forEach(function (r, k) { go(r, { opacity: 0, x: 40 }, at("délai") - 0.1 + k * 0.04, 0.2, "power2.in"); });
      slam("t2b-0", at("rotation") - 0.05); stroke("t2b", at("mois") + 0.05);
      pre("fr", { opacity: 0, y: 40 }); go("fr", { opacity: 1, y: 0 }, at("rotation") - 0.1, 0.4, "expo.out");
      odo("c1", 0, 0.01, { from: "00 000", spinLow: false });
      var t0 = at("quatre") - 0.05, t1 = at("15000") + 0.25, st = (t1 - t0) / 3;
      lane("l1", 3, t0, t1 - t0);
      ["05 000 €", "10 000 €", "15 000 €"].forEach(function (v, k) { odo("c1", t0 + (k + 1) * st - 0.2, 0.5, { to: v, dimLead: true }); });
      cam(0, -10, 1.04, at("trois"), 1.0);
    """
    sfx = [("pop", "un", 1, -.05, .12), ("pop", "sportive", 1, -.05, .14), ("typing", "achetée", 1, 0, .1),
           ("typing", "revendue", 1, 0, .1), ("typing", "5000", 1, 0, .1), ("pop", "rotation", 1, -.05, .14),
           ("click-soft", "quatre", 1, .3, .2), ("click-soft", "sur", 1, 0, .2), ("chime", "15000", 1, .1, .18)]
    return css, st, hud, js, (540, 800), sfx


def scene_03():
    css = PHOTO_CSS + FRISE_CSS + """
    .§cardp { position: absolute; top: 590px; width: 420px; height: 280px; opacity: 0; }
    .§cap { position: absolute; left: 0; top: 292px; width: 420px; text-align: center; font: 40px/1.15 "Anton", sans-serif; color: #ffffff; }
    .§cap b { color: #FB8000; font-weight: 400; }
    .§caps { display: block; font: 600 26px/1.2 "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.06em; }
    """
    def card(i, x, photo, a, b, m, days):
        return (f'<div id="§k{i}" class="§cardp" style="left:{x}px"><div class="§photo" style="left:0;top:0;width:420px;height:280px"><img src="assets/img/{photo}"></div>'
                f'<div class="§cap">{a} → {b}<span class="§caps"><b>+{m}</b> · ROTATION {days}</span></div></div>')
    st = (card(0, 90, "x4.jpg", "20 000", "23 000", "3 000 €", "30 J") + card(1, 570, "mini.jpg", "10 000", "11 500", "1 500 €", "15 J")
          + frise([("l1", 12, "x4.jpg", "c1", "36 000 €", "SUV"), ("l2", 24, "mini.jpg", "c2", "36 000 €", "CITADINE")]))
    st = st.replace('<span class="§caps"><b>', '<span class="§caps"><b style="color:#FB8000">')
    hud = title("t3", ["OPTION 2", "SUV + CITADINE"], 290, 110) + title("t3b", ["TOTAL", (odo("tot", "72 000 €"), 150)], 270, 70)
    js = FRISE_JS + """
      slam("t3-0", Math.max(0.02, at("deux") - 0.05)); slam("t3-1", at("suv") - 0.05); stroke("t3", at("citadine") + 0.1);
      pre("k0", { opacity: 0, y: 60 }); go("k0", { opacity: 1, y: 0 }, at("suv") - 0.05, 0.35, "back.out(1.5)");
      pre("k1", { opacity: 0, y: 60 }); go("k1", { opacity: 1, y: 0 }, at("citadine") - 0.05, 0.35, "back.out(1.5)");
      pre("fr", { opacity: 0, y: 40 }); go("fr", { opacity: 1, y: 0 }, at("tourne") - 0.2, 0.4, "expo.out");
      odo("c1", 0, 0.01, { from: "00 000", spinLow: false }); odo("c2", 0, 0.01, { from: "00 000", spinLow: false });
      var a0 = at("douze") - 0.1, a1 = at("36000", 1) + 0.6;
      lane("l1", 12, a0, a1 - a0, "c1");
      init("k0", { opacity: 1, scale: 1, y: 0 }); go("k0", { scale: 1.04 }, a0, 0.2); go("k0", { scale: 1 }, a1, 0.3);
      var b0 = at("vingt-quatre") - 0.1, b1 = at("36000", 2) + 0.6;
      lane("l2", 24, b0, b1 - b0, "c2");
      init("k1", { opacity: 1, scale: 1, y: 0 }); go("k1", { scale: 1.04 }, b0, 0.2); go("k1", { scale: 1 }, b1, 0.3);
      // total
      go("t3", { opacity: 0, y: -30 }, at("total") - 0.15, 0.14, "power2.in");
      slam("t3b-0", at("total") - 0.03); slam("t3b-1", at("72000") - 0.05); odo("tot", at("72000") - 0.05, 0.9, { from: "00 000" }); stroke("t3b", at("72000") + 0.4);
      cam(0, -10, 1.04, at("total"), 0.8);
    """
    sfx = [("pop", "deux", 1, -.05, .12), ("pop", "suv", 1, -.05, .14), ("pop", "citadine", 1, -.05, .14),
           ("typing", "douze", 1, -.1, .12), ("typing", "vingt-quatre", 1, -.1, .12), ("pop", "total", 1, 0, .14),
           ("chime", "72000", 1, .2, .2)]
    return css, st, hud, js, (540, 800), sfx


def scene_04():
    css = PHOTO_CSS + FRISE_CSS + """
    .§c3 { position: absolute; top: 600px; width: 290px; height: 220px; opacity: 0; }
    #§cy { position: absolute; left: 0; top: 860px; width: 1080px; text-align: center; opacity: 0; }
    #§cyi { display: inline-block; padding: 8px 30px; border-radius: 40px; background: #FB8000; color: #0A0A0A; font: 48px/1.2 "Anton", sans-serif; }
    """
    cards = "".join(f'<div id="§k{i}" class="§c3 §photo" style="left:{70 + i * 325}px"><img src="assets/img/{p}"></div>'
                    for i, p in enumerate(["golf.jpg", "fiat.jpg", "mini.jpg"]))
    st = (cards + '<div id="§cy"><span id="§cyi">72 CYCLES DE VENTE</span></div>'
          + frise([("l1", 24, "golf.jpg", "c1", "36 000 €", ""), ("l2", 24, "fiat.jpg", "c2", "36 000 €", ""), ("l3", 24, "mini.jpg", "c3", "36 000 €", "")]))
    hud = (title("t4", ["OPTION 3", "3 CITADINES"], 290, 110) + title("t4b", [(odo("tot", "108 000 €"), 170)], 300, 110)
           + title("t4c", ["MÊME DIVISÉ PAR 2", (odo("half", "54 000 €"), 150)], 250, 84))
    js = FRISE_JS + """
      slam("t4-0", Math.max(0.02, at("trois") - 0.05)); slam("t4-1", at("citadines") - 0.05); stroke("t4", at("citadines") + 0.2);
      ["k0", "k1", "k2"].forEach(function (k, i) { pre(k, { opacity: 0, y: 60 }); go(k, { opacity: 1, y: 0 }, at("citadines") - 0.05 + i * 0.1, 0.35, "back.out(1.5)"); });
      pre("fr", { opacity: 0, y: 40 }); go("fr", { opacity: 1, y: 0 }, at("1500") - 0.1, 0.4, "expo.out");
      ["c1", "c2", "c3"].forEach(function (c) { odo(c, 0, 0.01, { from: "00 000", spinLow: false }); });
      var t0 = at("15") - 0.1, t1 = at("108000") + 0.5;
      lane("l1", 24, t0, t1 - t0, "c1"); lane("l2", 24, t0 + 0.05, t1 - t0, "c2"); lane("l3", 24, t0 + 0.1, t1 - t0, "c3");
      go("t4", { opacity: 0, y: -30 }, at("papier") - 0.12, 0.14, "power2.in");
      slam("t4b-0", at("108000") - 0.1, { s: 1.3 }); odo("tot", at("108000") - 0.1, 0.9, { from: "000 000" }); stroke("t4b", at("108000") + 0.5);
      // to be honest: 72 cycles is a real job; divide by two
      pre("cy", { opacity: 0, scale: 0.6 }); go("cy", { opacity: 1, scale: 1 }, at("72") - 0.05, 0.3, "back.out(2)");
      go("cy", { opacity: 0 }, at("divise") - 0.15, 0.2);
      go("t4b", { opacity: 0, scale: 0.7, y: -40 }, at("divise") - 0.1, 0.3, "power2.in");
      slam("t4c-0", at("divise") - 0.02); slam("t4c-1", at("54000") - 0.1, { s: 1.3 }); odo("half", at("54000") - 0.1, 0.8, { from: "00 000" }); stroke("t4c", at("54000") + 0.4);
      cam(0, -10, 1.04, at("papier"), 0.8);
    """
    sfx = [("pop", "trois", 1, -.05, .12), ("pop", "citadines", 1, -.05, .14), ("typing", "15", 1, -.1, .12),
           ("pop", "108000", 1, -.1, .16), ("pop", "72", 1, -.05, .14), ("whoosh-short", "divise", 1, -.1, .14),
           ("chime", "54000", 1, 0, .18)]
    return css, st, hud, js, (540, 800), sfx


def scene_05():
    css = PHOTO_CSS + """
    .§bar { position: absolute; left: 80px; width: 860px; height: 150px; opacity: 0; }
    .§bth { position: absolute; left: 0; top: 0; width: 150px; height: 150px; border-radius: 16px; overflow: hidden; border: 3px solid #2e2e2e; }
    .§bth img { width: 100%; height: 100%; object-fit: cover; }
    .§btr { position: absolute; left: 170px; top: 86px; width: 650px; height: 40px; border-radius: 20px; background: #181818; }
    .§bfill { position: absolute; left: 0; top: 0; height: 100%; border-radius: 20px; background: #FB8000; transform-origin: 0 50%; transform: scaleX(0); }
    .§bext { position: absolute; top: 0; height: 100%; border-radius: 0 20px 20px 0; background: repeating-linear-gradient(45deg, #FB8000 0 10px, #7a3e00 10px 20px); transform-origin: 0 50%; transform: scaleX(0); }
    .§bv { position: absolute; left: 170px; top: 6px; font: 66px/1 "Anton", sans-serif; color: #ffffff; }
    #§loop { position: absolute; left: 430px; top: 1115px; width: 220px; height: 140px; overflow: visible; fill: none; stroke: #FB8000; stroke-width: 12; stroke-linecap: round; opacity: 0; }
    """
    def bar(i, y, photos, amount, frac, ext=None):
        th = "".join(f'<img src="assets/img/{p}" style="width:{100 / len(photos):.2f}%;float:left">' for p in photos)
        e = f'<i id="§be{i}" class="§bext" style="left:{frac * 650:.0f}px;width:{(ext - frac) * 650:.0f}px"></i>' if ext else ""
        return (f'<div id="§b{i}" class="§bar" style="top:{y}px"><div class="§bth">{th}</div><div class="§btr"><i id="§bf{i}" class="§bfill" style="width:{frac * 650:.0f}px"></i>{e}</div>'
                f'<div class="§bv" id="§bv{i}">{amount}</div></div>')
    st = (bar(0, 590, ["mustang.jpg"], odo("v0", "15 000 €"), 15 / 108) + bar(1, 770, ["x4.jpg", "mini.jpg"], odo("v1", "72 000 €"), 72 / 108)
          + bar(2, 950, ["golf.jpg", "fiat.jpg", "mini.jpg"], odo("v2", "54 000 €") + " <span style='font-size:44px;color:#9a9a9a'>À 108 000 €</span>", 54 / 108, 1.0)
          + '<svg id="§loop" viewBox="0 0 300 190"><path id="§lp" d="M70 150 A80 70 0 1 1 230 150"/><path d="M200 120 L232 152 L262 116"/></svg>')
    hud = title("t5", ["MÊME BUDGET.", "JUSQU’À 7 FOIS PLUS."], 280, 104) + title("t5b", ["ROTATION", "DE TRÉSORERIE"], 290, 110)
    js = """
      slam("t5-0", Math.max(0.02, at("budget") - 0.05));
      [0, 1, 2].forEach(function (i) {
        pre("b" + i, { opacity: 0, x: -60 }); go("b" + i, { opacity: 1, x: 0 }, 0.1 + i * 0.15, 0.35, "expo.out");
        tl.fromTo($("bf" + i), { scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: "power3.out", immediateRender: false }, 0.3 + i * 0.15);
        odo("v" + i, 0.3 + i * 0.15, 0.9, { from: "00 000" });
      });
      tl.fromTo($("be2"), { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.out", immediateRender: false }, 1.0);
      // the biggest margin earns the least
      go("b0", { opacity: 0.35 }, at("moins") - 0.05, 0.4); tl.fromTo($("bf0"), { background: "#FB8000" }, { background: "#5a5a5a", duration: 0.4, immediateRender: false }, at("moins") - 0.05);
      slam("t5-1", at("moins") - 0.02); stroke("t5", at("moins") + 0.2);
      // it's the rotation of your cash
      go("t5", { opacity: 0, y: -30 }, at("rotation") - 0.15, 0.14, "power2.in");
      slam("t5b-0", at("rotation") - 0.02); slam("t5b-1", at("trésorerie") - 0.04); stroke("t5b", at("trésorerie") + 0.2);
      pre("loop", { opacity: 0, scale: 0.6 }); go("loop", { opacity: 1, scale: 1 }, at("combien") - 0.1, 0.3, "back.out(2)");
      tl.fromTo($("loop"), { rotation: 0 }, { rotation: 360, duration: 1.4, ease: "power2.inOut", immediateRender: false }, at("revient") - 0.2);
      cam(0, -10, 1.04, at("rotation"), 0.8);
    """
    sfx = [("pop", "budget", 1, -.05, .14), ("typing", None, 0, 0.3, .12), ("click", "moins", 1, -.05, .25),
           ("pop", "rotation", 1, -.02, .14), ("whoosh-short", "revient", 1, -.2, .14)]
    return css, st, hud, js, (540, 820), sfx


def scene_06():
    css = PHOTO_CSS + """
    #§ph { left: 120px; top: 590px; width: 840px; height: 420px; }
    #§doc { position: absolute; left: 560px; top: 620px; width: 380px; height: 480px; border-radius: 10px; background: #f7f5f1; color: #141414; opacity: 0;
      transform: rotate(4deg); box-shadow: 0 30px 70px rgba(0,0,0,0.7); font-family: "Instrument Sans", sans-serif; }
    #§doch { position: absolute; left: 0; top: 0; width: 100%; height: 86px; background: #141414; color: #ffffff; text-align: center; font: 50px/86px "Anton", sans-serif; border-radius: 10px 10px 0 0; }
    .§dl { position: absolute; left: 30px; font: 600 22px/1.2 "Instrument Sans", sans-serif; color: #141414; }
    .§dln { position: absolute; left: 30px; height: 10px; border-radius: 5px; background: #d8d3ca; }
    #§dst { position: absolute; left: 190px; top: 380px; padding: 4px 16px; border: 5px solid #FB8000; color: #FB8000; font: 34px/1.1 "Anton", sans-serif; transform: rotate(-10deg); }
    #§wr { position: absolute; left: 160px; top: 650px; width: 170px; height: 170px; overflow: visible; fill: none; stroke: #ffffff; stroke-width: 14; stroke-linecap: round; opacity: 0; }
    .§rep { position: absolute; top: 640px; width: 420px; height: 420px; border-radius: 28px; background: #151515; border: 2px solid #2e2e2e; opacity: 0; overflow: hidden; }
    .§repph { position: absolute; left: 0; top: 0; width: 100%; height: 200px; }
    .§repph img { width: 100%; height: 100%; object-fit: cover; filter: saturate(0.8); }
    .§repl { position: absolute; left: 0; top: 220px; width: 100%; text-align: center; font: 600 28px "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.1em; }
    .§repv { position: absolute; left: 0; top: 270px; width: 100%; text-align: center; font: 100px/1.1 "Anton", sans-serif; color: #ffffff; }
    #§div5 { position: absolute; left: 470px; top: 790px; width: 140px; height: 140px; border-radius: 50%; background: #FB8000; color: #0A0A0A; font: 64px/140px "Anton", sans-serif;
      text-align: center; opacity: 0; box-shadow: 0 0 40px rgba(251,128,0,0.5); z-index: 3; }
    """
    lines = ('<div class="§dl" style="top:116px">GARANTIE LÉGALE DE CONFORMITÉ</div><div class="§dln" style="top:150px;width:300px"></div>'
             '<div class="§dln" style="top:172px;width:250px"></div><div class="§dl" style="top:210px">VICES CACHÉS</div>'
             '<div class="§dln" style="top:244px;width:310px"></div><div class="§dln" style="top:266px;width:220px"></div>'
             '<div class="§dln" style="top:288px;width:280px"></div><div id="§dst">VENDEUR PRO</div>')
    st = ('<div id="§ph" class="§photo"><img src="assets/img/mustang.jpg"></div>'
          f'<div id="§doc"><div id="§doch">GARANTIE</div>{lines}</div>'
          '<svg id="§wr" viewBox="0 0 170 170"><path d="M30 140 L100 70"/><circle cx="118" cy="52" r="30"/><path d="M118 22 L118 52 L148 52" stroke="#0A0A0A" stroke-width="16"/></svg>'
          '<div id="§r1" class="§rep" style="left:90px"><div class="§repph"><img src="assets/img/mustang.jpg"></div><div class="§repl">SPORTIVE</div><div class="§repv">' + odo("rv1", "6 000 €") + '</div></div>'
          '<div id="§r2" class="§rep" style="left:570px"><div class="§repph"><img src="assets/img/golf.jpg"></div><div class="§repl">CITADINE</div><div class="§repv">' + odo("rv2", "1 200 €") + '</div></div>'
          '<div id="§div5">÷ 5</div>')
    hud = title("t6", ["LE RISQUE"], 330, 130) + title("t6b", ["LA MÊME PANNE"], 330, 110)
    js = """
      slam("t6-0", at("risque") - 0.05); stroke("t6", at("risque") + 0.2);
      pre("ph", { opacity: 0, scale: 1.08 }); go("ph", { opacity: 1, scale: 1 }, at("risque") - 0.1, 0.45, "expo.out");
      pre("wr", { opacity: 0, rotation: -40, scale: 0.6 }); go("wr", { opacity: 1, rotation: 0, scale: 1 }, at("pro") - 0.1, 0.35, "back.out(2)");
      pre("doc", { opacity: 0, y: 80, rotation: 10 }); go("doc", { opacity: 1, y: 0, rotation: 4 }, at("garantie") - 0.1, 0.4, "back.out(1.4)");
      init("dst", { opacity: 1 }); tl.fromTo($("dst"), { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.16, ease: "expo.in", immediateRender: false }, at("vices") - 0.05);
      // same breakdown, sportive vs city car
      ["ph", "doc", "wr"].forEach(function (e) { go(e, { opacity: 0, y: -40 }, at("panne") - 0.15, 0.25, "power2.in"); });
      go("t6", { opacity: 0, y: -30 }, at("panne") - 0.15, 0.14, "power2.in"); slam("t6b-0", at("panne") - 0.02); stroke("t6b", at("panne") + 0.2);
      pre("r1", { opacity: 0, y: 60 }); go("r1", { opacity: 1, y: 0 }, at("panne"), 0.35, "back.out(1.5)"); odo("rv1", at("prix") - 0.1, 0.8, { from: "0 000" });
      pre("r2", { opacity: 0, y: 60 }); go("r2", { opacity: 1, y: 0 }, at("citadine") - 0.1, 0.35, "back.out(1.5)"); odo("rv2", at("citadine"), 0.8, { from: "0 000" });
      pre("div5", { opacity: 0, scale: 2.2 }); go("div5", { opacity: 1, scale: 1 }, at("cinq") - 0.05, 0.18, "expo.in");
      // the most expensive car is also the one that costs the most when it breaks
      go("r2", { opacity: 0, x: 120 }, at("chère") - 0.1, 0.3); go("div5", { opacity: 0 }, at("chère") - 0.1, 0.2);
      init("r1", { opacity: 1, y: 0, scale: 1 }); go("r1", { x: 240, scale: 1.08 }, at("chère") - 0.1, 0.5, "power3.inOut");
      tl.fromTo($("rv1"), { color: "#ffffff" }, { color: "#FB8000", duration: 0.3, immediateRender: false }, at("cher") - 0.05);
      wobble("r1", at("casse") - 0.05, 3);
      cam(0, -10, 1.04, at("panne"), 0.8);
    """
    sfx = [("pop", "risque", 1, -.05, .16), ("click-soft", "pro", 1, -.1, .22), ("whoosh-short", "garantie", 1, -.1, .12),
           ("pop", "vices", 1, -.05, .14), ("whoosh-short", "panne", 1, -.15, .12), ("typing", "prix", 1, -.1, .12),
           ("typing", "citadine", 1, 0, .12), ("impact-bass-2", "cinq", 1, -.05, .26), ("error", "casse", 1, -.05, .16)]
    return css, st, hud, js, (540, 820), sfx


def scene_07():
    css = """
    .§tip { position: absolute; left: 0; width: 1080px; text-align: center; opacity: 0; }
    .§tipi { display: inline-block; padding: 10px 34px; border-radius: 40px; border: 4px solid #FB8000; color: #ffffff; font: 54px/1.2 "Anton", sans-serif; }
    #§handle { position: absolute; left: 60px; top: 820px; width: 960px; text-align: center; white-space: nowrap; }
    #§hname { position: relative; display: inline-block; font: 96px/1.2 "Anton", sans-serif; color: #ffffff; opacity: 0; }
    #§pill { position: absolute; left: 50%; top: 175px; transform: translateX(-50%); }
    #§pilli { display: inline-block; padding: 8px 40px; border-radius: 40px; background: #FB8000; color: #0A0A0A; font: 52px/1.25 "Anton", sans-serif; opacity: 0;
      box-shadow: 0 0 46px rgba(251,128,0,0.45); }
    """
    hud = (title("t7", ["CE QUE TU GAGNES =", '<span id="§fm">MARGE</span> <span id="§fx">×</span> <span id="§fc">CYCLES</span>'], 520, 116)
           + '<div id="§tp1" class="§tip" style="top:620px"><span class="§tipi">ROTATION RAPIDE</span></div>'
             '<div id="§tp2" class="§tip" style="top:760px"><span class="§tipi">PANNES PAS CHÈRES</span></div>'
           + '<div id="§handle"><span id="§hname">@guillaumeherbin_<i class="§stilt"><i class="§stk" id="§h-s"></i></i></span>'
             '<div id="§pill"><span id="§pilli">S’ABONNER</span></div></div>')
    css += "#§fm, #§fx, #§fc { display: inline-block; opacity: 0; } #§fx { color: #FB8000; }"
    js = """
      slam("t7-0", Math.max(0.02, at("gagnes") - 0.05));
      tl.set($("t7-1"), { opacity: 1 }, 0);
      slam("fm", at("marge") - 0.04, { s: 1.4 }); slam("fx", at("fois") - 0.04, { s: 1.6 }); slam("fc", at("cycles") - 0.04, { s: 1.4 }); stroke("t7", at("vente") + 0.1);
      init("t7", { opacity: 1, y: 0, scale: 1 }); go("t7", { y: -220, scale: 0.8 }, at("début") - 0.2, 0.5, "power3.inOut");
      pre("tp1", { opacity: 0, y: 40 }); go("tp1", { opacity: 1, y: 0 }, at("vite") - 0.1, 0.3, "back.out(1.6)");
      pre("tp2", { opacity: 0, y: 40 }); go("tp2", { opacity: 1, y: 0 }, at("cher") - 0.1, 0.3, "back.out(1.6)");
      ["t7", "tp1", "tp2"].forEach(function (e) { go(e, { opacity: 0 }, at("abonne-toi") - 0.15, 0.2); });
      slam("hname", at("abonne-toi"), { s: 1.3 }); stroke("h", at("abonne-toi") + 0.2);
      pre("pilli", { opacity: 0, scale: 0.5 }); go("pilli", { opacity: 1, scale: 1 }, at("pour") - 0.04, 0.3, "back.out(2)");
      init("halo", { scale: 1 }); go("halo", { scale: 1.2 }, at("abonne-toi"), 1.2, "sine.inOut");
    """
    sfx = [("pop", "gagnes", 1, -.05, .14), ("pop", "marge", 1, -.04, .14), ("pop", "cycles", 1, -.04, .14),
           ("click-soft", "vite", 1, -.1, .22), ("click-soft", "cher", 1, -.1, .22), ("notification", "abonne-toi", 1, 0, .25),
           ("pop", "pour", 1, -.04, .14)]
    return css, "", hud, js, (540, 760), sfx


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
      <div id="§halo" class="§halo" style="left:{halo[0]}px;top:{halo[1]}px"></div>
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
message: "Même budget de 30 000 € : la sportive à grosse marge rapporte le moins ; ce qui compte, c'est la rotation de la trésorerie (marge × cycles de vente), et les voitures qui cassent pas cher."
arc: Hook → Option 1 → Option 2 → Option 3 → Verdict → Risk → Rule + CTA
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
- **Negative list** : aucun billet ni espèce ; jamais plus de 6 mots par bloc de texte ; photos réelles de Guillaume, plaques floutées ; frise de 12 mois en bas d'écran, compteur annuel à droite.

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
