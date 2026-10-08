#!/usr/bin/env python3
"""Reel « Marchand ou intermédiaire ? » : one source for the whole film.

Every animation of every scene is placed on a WORD of the voice (at("virement"), at("même", 2)...), never on a fixed
second. The word timings come from one file:
  - assets/audio/voix-montage-mots.json when the real voice is there (align.py writes it), or
  - a provisional timing spread over the brief's windows (0-4, 4-10, 10-26, 26-38, 38-52, 52-62, 62-66 s).
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
   "Tu veux vendre", "des *voitures*.", "OK.", "Mais tu veux porter", "le *stock*, ou pas~?", "Parce que c'est",
   "deux *métiers*", "différents."]),
 dict(id="02-meme-voiture", name="La même voiture", window=(4, 10), chunks=[
   "Prenons la même *voiture*,", "*15~000* euros,", "vendue au même client.", "À gauche, le *marchand*.",
   "À droite, l'*intermédiaire*."]),
 dict(id="03-marchand", name="Le marchand", window=(10, 26), chunks=[
   "Le marchand *achète*", "la voiture 12~000 euros", "avec son argent.", "Il la *stocke*.", "Et pendant qu'elle dort,",
   "elle lui *coûte*~:", "les frais *bancaires*", "sur l'argent immobilisé,", "et la *place*,", "dépôt, parc ou showroom.",
   "Il la *revend* 15~000.", "3~000 de marge", "sur le papier,", "plutôt *2~300* en vrai.", "Et tout le *risque*",
   "est pour lui~:", "la garantie légale,", "les vices cachés,", "et la voiture", "qui peut rester", "immobilisée *plusieurs mois*."]),
 dict(id="04-intermediaire", name="L'intermédiaire", window=(26, 38), chunks=[
   "L'intermédiaire, lui,", "n'achète *rien*.", "Le vendeur lui confie", "un *mandat*.", "Il trouve le *client*,",
   "il organise la vente.", "Les *15~000*", "vont au vendeur.", "Lui prend une *commission*~:", "*1~500* euros", "environ.",
   "Zéro *stock*,", "zéro trésorerie bloquée,", "zéro frais de parc.", "Le vendeur reste *propriétaire*",
   "jusqu'à la vente."]),
 dict(id="05-face-a-face", name="Le face-à-face", window=(38, 52), chunks=[
   "*Résumé*.", "Le marchand sort 12~000,", "garde 2~300,", "porte tout le *risque*.", "L'intermédiaire sort zéro,",
   "garde 1~500,", "porte presque *rien*.", "*800* euros d'écart", "pour 12~000 euros immobilisés", "et tous les risques.",
   "L'un a besoin", "de *trésorerie*.", "L'autre a besoin", "d'un *réseau*", "et de savoir vendre."]),
 dict(id="06-vrai-choix", name="Le vrai choix", window=(52, 62), chunks=[
   "Lequel est le *meilleur*~?", "Mauvaise question.", "Avec *5~000* euros en poche,", "tu ne peux pas être marchand,",
   "mais tu peux être *intermédiaire*", "dès demain.", "Certains passent marchand", "plus tard.", "Mais la plupart",
   "des intermédiaires", "font le choix de le *rester*.", "Parce qu'ils ont compris", "que ne pas avoir de stock,",
   "c'est pas une *étape* nécessaire.", "C'est un *avantage*."]),
 dict(id="07-cta", name="CTA", window=(62, 66), chunks=[
   "*Abonne-toi*", "pour plus de contenu", "comme celui-ci."]),
]
SPOKEN_SYL = {"15000": 3, "12000": 3, "3000": 2, "2300": 5, "1500": 4, "800": 2, "5000": 2, "ok": 2}
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
# the two columns: MARCHAND on the left, INTERMÉDIAIRE on the right
COLS_CSS = """
    .§colh { position: absolute; top: 330px; width: 500px; text-align: center; font: 68px/1.2 "Anton", sans-serif; color: #ffffff; opacity: 0; }
    .§colu { position: absolute; left: 50%; bottom: -8px; width: 70%; height: 10px; margin-left: -35%; border-radius: 5px; background: #FB8000;
      transform: scaleX(0); transform-origin: 0 50%; }
    #§hL { left: 20px; } #§hR { left: 560px; }
    #§divl { position: absolute; left: 539px; top: 330px; width: 3px; height: 900px; background: linear-gradient(180deg, rgba(255,255,255,0), #333 12%, #333 88%, rgba(255,255,255,0));
      transform-origin: 50% 0; transform: scaleY(0); }
    .§flow { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; fill: none; stroke-linecap: round; stroke-linejoin: round; pointer-events: none; }
    .§ar { stroke: #FB8000; stroke-width: 9; }
    .§ah { stroke: #FB8000; stroke-width: 9; opacity: 0; }
    .§lab { position: absolute; padding: 6px 18px; border-radius: 24px; background: #FB8000; color: #0A0A0A; font: 34px/1.2 "Anton", sans-serif; white-space: nowrap; opacity: 0; }
    .§lab.§ghost { background: #151515; color: #ffffff; border: 2px solid #FB8000; }
    .§ptag { position: absolute; padding: 4px 16px; border-radius: 10px; background: #ffffff; color: #0A0A0A; font: 40px/1.2 "Anton", sans-serif; white-space: nowrap; }
    .§who { position: absolute; width: 200px; text-align: center; font: 600 24px/1 "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.1em; opacity: 0; }
"""
COLS_JS = """
      function heads(t, act) {
        go("hL", { opacity: act === "R" ? 0.3 : 1 }, t, 0.3); go("hR", { opacity: act === "L" ? 0.3 : 1 }, t, 0.3);
      }
      function arrow(id, t, d) { draw(id, t, d || 0.45, "power2.inOut"); pre(id + "h", { opacity: 0 }); go(id + "h", { opacity: 1 }, t + (d || 0.45) - 0.05, 0.1); }
"""


def cols(lit=True):
    st = "1" if lit else "0"
    return (f'<div id="§hL" class="§colh" style="opacity:{st}">MARCHAND<i id="§uL" class="§colu"{" style=transform:scaleX(1)" if lit else ""}></i></div>'
            f'<div id="§hR" class="§colh" style="opacity:{st};font-size:60px;top:338px">INTERMÉDIAIRE<i id="§uR" class="§colu"{" style=transform:scaleX(1)" if lit else ""}></i></div>'
            f'<div id="§divl"{" style=transform:scaleY(1)" if lit else ""}></div>')


def head(aid, x, y, ang):
    """arrowhead at (x, y) pointing at angle ang (degrees)"""
    return f'<g transform="translate({x} {y}) rotate({ang})"><path id="§{aid}h" class="§ah" d="M-26 -18 L0 0 L-26 18"/></g>'


def icon_shield(c):
    return f'<svg viewBox="0 0 100 100" style="width:100%;height:100%;fill:none;stroke:{c};stroke-width:8;stroke-linejoin:round;stroke-linecap:round"><path d="M50 8 L86 22 L86 50 Q86 78 50 92 Q14 78 14 50 L14 22 Z"/><path d="M50 32 L50 56 M50 70 L50 72"/></svg>'


def icon_bug(c):
    return f'<svg viewBox="0 0 100 100" style="width:100%;height:100%;fill:none;stroke:{c};stroke-width:8;stroke-linecap:round"><circle cx="42" cy="42" r="28"/><path d="M62 62 L90 90"/><path d="M42 28 L42 46 M42 56 L42 58"/></svg>'


def icon_wait(c):
    return f'<svg viewBox="0 0 100 100" style="width:100%;height:100%;fill:none;stroke:{c};stroke-width:8;stroke-linecap:round;stroke-linejoin:round"><path d="M10 66 L14 52 Q16 44 26 42 L40 30 Q44 26 52 26 L70 26 Q78 26 82 34 L88 46 Q92 48 92 56 L92 66 Z"/><circle cx="28" cy="68" r="9"/><circle cx="74" cy="68" r="9"/><circle cx="74" cy="20" r="0"/></svg>'


RISK_CSS = """
    .§rk { position: absolute; width: 140px; text-align: center; opacity: 0; }
    .§rki { width: 84px; height: 84px; margin: 0 auto; }
    .§rkl { display: block; margin-top: 6px; font: 600 20px/1.15 "Instrument Sans", sans-serif; color: #c9584f; letter-spacing: 0.04em; }
"""


def risks(prefix, x0, y, labels=("GARANTIE", "VICES CACHÉS", "IMMOBILISÉE")):
    fns = [icon_shield, icon_bug, icon_wait]
    return "".join(f'<div id="§{prefix}{k}" class="§rk" style="left:{x0 + k * 155}px;top:{y}px"><div class="§rki">{fns[k](RED)}</div><span class="§rkl">{l}</span></div>'
                   for k, l in enumerate(labels))


def scene_01():
    css = """
    #§t1 { }
    """
    st = stage()
    hud = title("t1", ["TU VEUX VENDRE", "DES VOITURES ?"], 300, 112) + '<div id="§split" style="position:absolute;left:539px;top:600px;width:3px;height:420px;background:#FB8000;transform-origin:50% 0;transform:scaleY(0)"></div>'
    js = """
      ["pa", "pb"].forEach(function (p) { init(p + "-w", { opacity: 0 }); init(p + "-o", { opacity: 0 }); init(p + "-glow", { opacity: 0 }); });
      pre("car", { opacity: 0 }); slam("car", 0.05, { s: 1.3 });
      pre("pa", { opacity: 0, y: 50 }); pre("pb", { opacity: 0, y: 50 });
      go("pa", { opacity: 1, y: 0 }, 0.2, 0.28, "back.out(1.6)"); go("pb", { opacity: 1, y: 0 }, 0.3, 0.28, "back.out(1.6)");
      slam("t1-0", Math.max(0.02, at("vendre") - 0.05)); slam("t1-1", at("voitures") - 0.05); stroke("t1", at("voitures") + 0.15);
      lit("pa", "white", at("stock") - 0.05, 0.25); lit("pb", "white", at("stock") + 0.05, 0.25);
      // two jobs: the scene splits in two
      tl.fromTo($("split"), { scaleY: 0 }, { scaleY: 1, duration: 0.35, ease: "power3.out", immediateRender: false }, at("métiers") - 0.1);
      go("pa", { x: -40 }, at("métiers") - 0.1, 0.4); go("pb", { x: 40 }, at("métiers") - 0.1, 0.4);
      lit("pa", "orange", at("métiers"), 0.3);
      cam(0, -10, 1.04, at("stock"), 0.8);
    """
    sfx = [("pop", None, 0, 0.05, .14), ("pop", "voitures", 1, -.05, .14), ("whoosh-short", "métiers", 1, -.1, .16)]
    return css, st, hud, js, (540, 820), sfx


def scene_02():
    css = PHOTO_CSS + COLS_CSS + """
    #§ph { left: 330px; top: 620px; width: 420px; height: 260px; }
    #§pL { left: 50px; top: 620px; width: 440px; height: 270px; opacity: 0; }
    #§pR { left: 590px; top: 620px; width: 340px; height: 270px; opacity: 0; }
    #§tag { left: 440px; top: 900px; opacity: 0; }
    #§cli { opacity: 0; }
    """
    st = ('<div id="§ph" class="§photo"><img src="assets/img/golf.jpg"></div>'
          '<div id="§pL" class="§photo"><img src="assets/img/golf.jpg"></div><div id="§pR" class="§photo"><img src="assets/img/golf.jpg"></div>'
          '<div id="§tag" class="§ptag">' + odo("pv", "15 000 €") + '</div>' + person("cli", 470, 980, 140))
    hud = cols(False)
    js = COLS_JS + """
      pre("ph", { opacity: 0, scale: 1.1 }); go("ph", { opacity: 1, scale: 1 }, Math.max(0.02, at("voiture") - 0.1), 0.4, "expo.out");
      slam("tag", at("15000") - 0.06, { s: 1.3 }); odo("pv", at("15000") - 0.06, 0.8);
      init("cli-w", { opacity: 1 }); init("cli-o", { opacity: 0 }); init("cli-glow", { opacity: 0 }); tl.set($("cli-w"), { opacity: 1 }, 0);
      pre("cli", { opacity: 0, y: 40 }); go("cli", { opacity: 1, y: 0 }, at("client") - 0.08, 0.3, "back.out(1.6)");
      // the screen splits: same car on both sides
      tl.fromTo($("divl"), { scaleY: 0 }, { scaleY: 1, duration: 0.4, ease: "power3.out", immediateRender: false }, at("gauche") - 0.15);
      go("ph", { opacity: 0 }, at("gauche") - 0.12, 0.15); go("cli", { opacity: 0 }, at("gauche") - 0.12, 0.2); go("tag", { opacity: 0 }, at("gauche") - 0.12, 0.2);
      pre("pL", { opacity: 0, x: 140 }); go("pL", { opacity: 1, x: 0 }, at("gauche") - 0.12, 0.4, "power3.out");
      pre("pR", { opacity: 0, x: -140 }); go("pR", { opacity: 1, x: 0 }, at("droite") - 0.12, 0.4, "power3.out");
      slam("hL", at("marchand") - 0.05); tl.fromTo($("uL"), { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, at("marchand") + 0.15);
      slam("hR", at("l'intermédiaire") - 0.05); tl.fromTo($("uR"), { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, at("l'intermédiaire") + 0.15);
    """
    sfx = [("pop", "voiture", 1, -.1, .14), ("typing", "15000", 1, -.06, .12), ("pop", "client", 1, -.08, .12),
           ("whoosh-short", "gauche", 1, -.15, .16), ("pop", "marchand", 1, -.05, .14), ("pop", "l'intermédiaire", 1, -.05, .14)]
    return css, st, hud, js, (540, 800), sfx


def scene_03():
    css = PHOTO_CSS + COLS_CSS + RISK_CSS + """
    #§car { left: 250px; top: 640px; width: 250px; height: 160px; }
    #§stock { position: absolute; left: 228px; top: 600px; width: 294px; height: 228px; border: 5px dashed #FB8000; border-radius: 14px; opacity: 0; }
    #§stockl { position: absolute; left: 10px; top: -30px; padding: 0 12px; background: #0A0A0A; font: 40px/1.2 "Anton", sans-serif; color: #FB8000; }
    .§cost { position: absolute; top: 860px; width: 225px; height: 120px; border-radius: 18px; background: #151515; border: 2px solid #2e2e2e; opacity: 0; }
    .§costl { position: absolute; left: 0; top: 16px; width: 100%; text-align: center; font: 600 20px/1 "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.06em; }
    .§costv { position: absolute; left: 0; top: 46px; width: 100%; text-align: center; font: 56px/1 "Anton", sans-serif; color: #c9584f; }
    #§mg { position: absolute; left: 40px; top: 1010px; width: 470px; text-align: center; font: 600 28px/1 "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.08em; opacity: 0; }
    #§mgv { display: block; margin-top: 8px; font: 90px/1 "Anton", sans-serif; color: #FB8000; }
    #§mgo { position: absolute; left: 0; top: 0; width: 100%; height: 100%; }
    #§mgx { position: absolute; left: 110px; top: 70px; width: 250px; height: 8px; background: #FB8000; border-radius: 4px; transform: scaleX(0) rotate(-6deg); transform-origin: 0 50%; }
    """
    st = (cols(True) + person("mch", 55, 650, 140)
          + '<div id="§car" class="§photo"><img src="assets/img/golf.jpg"></div>'
          + '<div id="§stock"><span id="§stockl">STOCK</span></div>'
          + '<svg class="§flow" viewBox="0 0 1080 1920"><path id="§a1" class="§ar" d="M180 700 C 200 640, 220 640, 245 680"/>' + head("a1", 245, 680, 60)
          + '<path id="§a2" class="§ar" d="M470 1000 C 420 1060, 220 1060, 140 900"/>' + head("a2", 140, 900, -115) + '</svg>'
          + '<div id="§l1" class="§lab" style="left:40px;top:470px">ACHÈTE ' + odo("buy", "12 000 €") + '</div>'
          + '<div id="§c1" class="§cost" style="left:40px"><div class="§costl">FRAIS BANCAIRES</div><div class="§costv">- ' + odo("cb", "250 €") + '</div></div>'
          + '<div id="§c2" class="§cost" style="left:285px"><div class="§costl">STOCKAGE</div><div class="§costv">- ' + odo("cs", "450 €") + '</div></div>'
          + '<div id="§l2" class="§lab" style="left:250px;top:1040px">VEND ' + odo("sell", "15 000 €") + '</div>'
          + '<div id="§mg">MARGE<span id="§mgv">' + odo("mgn", "3 000 €") + '</span></div>'
          + risks("rk", 45, 1040)
          + '<div id="§rhsph" class="§photo" style="left:590px;top:620px;width:340px;height:270px;opacity:0.3"><img src="assets/img/golf.jpg"></div>')
    hud = ""
    js = COLS_JS + """
      heads(0.05, "L");
      init("mch-w", { opacity: 0 }); init("mch-o", { opacity: 0 }); init("mch-glow", { opacity: 0 });
      pre("mch", { opacity: 0, y: 40 }); go("mch", { opacity: 1, y: 0 }, 0.05, 0.3, "back.out(1.6)"); lit("mch", "orange", 0.1, 0.3);
      pre("car", { opacity: 0, scale: 1.1 }); go("car", { opacity: 1, scale: 1 }, 0.1, 0.35, "expo.out");
      // he buys with his own money
      arrow("a1", at("achète") - 0.05, 0.4);
      pre("l1", { opacity: 0, scale: 0.6 }); go("l1", { opacity: 1, scale: 1 }, at("achète"), 0.25, "back.out(2)"); odo("buy", at("12000") - 0.1, 0.8, { from: "00 000" });
      // into stock
      pre("stock", { opacity: 0, scale: 1.15 }); go("stock", { opacity: 1, scale: 1 }, at("stocke") - 0.05, 0.3, "back.out(1.6)");
      init("car", { opacity: 1, scale: 1 }); go("car", { opacity: 0.6 }, at("dort"), 0.5);
      // while it sleeps, it costs
      pre("c1", { opacity: 0, y: 30 }); go("c1", { opacity: 1, y: 0 }, at("bancaires") - 0.1, 0.3, "back.out(1.6)"); odo("cb", at("bancaires"), 1.4, { from: "000" });
      pre("c2", { opacity: 0, y: 30 }); go("c2", { opacity: 1, y: 0 }, at("place") - 0.1, 0.3, "back.out(1.6)"); odo("cs", at("place"), 1.4, { from: "000" });
      // sold 15 000
      go("car", { opacity: 1 }, at("revend") - 0.1, 0.3);
      arrow("a2", at("revend") - 0.05, 0.5);
      pre("l2", { opacity: 0, scale: 0.6 }); go("l2", { opacity: 1, scale: 1 }, at("revend"), 0.25, "back.out(2)"); odo("sell", at("15000") - 0.1, 0.8, { from: "00 000" });
      // margin 3 000 on paper, 2 300 for real
      ["l1", "l2", "a1", "a1h", "a2", "a2h"].forEach(function (e) { go(e, { opacity: 0 }, at("3000") - 0.15, 0.2); });
      pre("mg", { opacity: 0, y: 30 }); go("mg", { opacity: 1, y: 0 }, at("3000") - 0.1, 0.3, "back.out(1.6)"); odo("mgn", at("3000") - 0.1, 0.8, { from: "0 000" });
      odo("mgn", at("2300") - 0.05, 0.9, { to: "2 300 €" });
      init("c1", { opacity: 1, y: 0, scale: 1 }); init("c2", { opacity: 1, y: 0, scale: 1 });
      go("c1", { scale: 1.08 }, at("2300") - 0.05, 0.15); go("c1", { scale: 1 }, at("2300") + 0.1, 0.25);
      go("c2", { scale: 1.08 }, at("2300") - 0.05, 0.15); go("c2", { scale: 1 }, at("2300") + 0.1, 0.25);
      // and all the risk is his
      ["c1", "c2"].forEach(function (e) { go(e, { opacity: 0 }, at("risque") - 0.15, 0.2); });
      go("mg", { y: -150 }, at("risque") - 0.15, 0.4, "power3.inOut");
      [["rk0", "garantie"], ["rk1", "vices"], ["rk2", "immobilisée"]].forEach(function (r) {
        pre(r[0], { opacity: 0, scale: 0.4 }); go(r[0], { opacity: 1, scale: 1 }, at(r[1]) - 0.08, 0.25, "back.out(2.2)");
      });
      wobble("rk2", at("plusieurs") + 0.25, 6);
      cam(10, -10, 1.04, at("risque"), 0.8);
    """
    sfx = [("pop", None, 0, 0.1, .12), ("whoosh-short", "achète", 1, -.05, .14), ("typing", "12000", 1, -.1, .12),
           ("click-soft", "stocke", 1, -.05, .22), ("typing", "bancaires", 1, 0, .1), ("typing", "place", 1, 0, .1),
           ("whoosh-short", "revend", 1, -.05, .14), ("typing", "15000", 1, -.1, .12), ("pop", "3000", 1, -.1, .14),
           ("typing", "2300", 1, -.05, .12), ("error", "garantie", 1, -.08, .14), ("error", "vices", 1, -.08, .14),
           ("error", "plusieurs", 1, -.08, .14)]
    return css, st, hud, js, (270, 860), sfx


def scene_04():
    css = PHOTO_CSS + COLS_CSS + """
    #§vcar { left: 760px; top: 630px; width: 230px; height: 150px; }
    #§key { position: absolute; left: 790px; top: 600px; padding: 4px 12px; border-radius: 10px; background: #FB8000; color: #0A0A0A; font: 26px/1.2 "Anton", sans-serif; opacity: 0; }
    .§zero { position: absolute; top: 1150px; width: 120px; height: 90px; border-radius: 14px; background: #151515; border: 2px solid #2e2e2e; text-align: center; opacity: 0; }
    .§zv { display: block; margin-top: 6px; font: 44px/1 "Anton", sans-serif; color: #FB8000; }
    .§zl { display: block; margin-top: 4px; font: 600 16px/1 "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.04em; }
    """
    st = (cols(True) + '<div id="§lhsph" class="§photo" style="left:60px;top:640px;width:420px;height:260px;opacity:0.3"><img src="assets/img/golf.jpg"></div>'
          + person("vdr", 590, 640, 120) + '<div id="§whov" class="§who" style="left:550px;top:585px">VENDEUR</div>'
          + '<div id="§vcar" class="§photo"><img src="assets/img/golf.jpg"></div><div id="§key">PROPRIÉTAIRE</div>'
          + person("itm", 600, 930, 120) + '<div id="§whoi" class="§who" style="left:560px;top:1120px">TOI</div>'
          + person("cli", 810, 930, 120) + '<div id="§whoc" class="§who" style="left:770px;top:1120px">CLIENT</div>'
          + '<svg class="§flow" viewBox="0 0 1080 1920">'
          + '<path id="§m1" class="§ar" d="M650 815 L652 915"/>' + head("m1", 652, 915, 88)
          + '<path id="§m2" class="§ar" d="M730 1010 L800 1010" style="stroke:#ffffff;stroke-width:6"/>'
          + '<path id="§m3" class="§ar" d="M895 925 C 905 870, 900 830, 880 795"/>' + head("m3", 880, 795, -115)
          + '<path id="§m4" class="§ar" d="M650 815 L652 915"/>' + head("m4", 652, 915, 88) + '</svg>'
          + '<div id="§lm" class="§lab" style="left:675px;top:845px;font-size:28px">MANDAT</div>'
          + '<div id="§l15" class="§lab §ghost" style="left:830px;top:830px;font-size:28px">' + odo("v15", "15 000 €") + '</div>'
          + '<div id="§lc" class="§lab" style="left:675px;top:845px;font-size:28px">+ ' + odo("com", "1 500 €") + '</div>'
          + "".join(f'<div id="§z{k}" class="§zero" style="left:{575 + k * 128}px"><span class="§zv">0</span><span class="§zl">{l}</span></div>'
                    for k, l in enumerate(["STOCK", "TRÉSO BLOQUÉE", "FRAIS DE PARC"])))
    hud = ""
    js = COLS_JS + """
      heads(0.05, "R");
      [["vdr", "white"], ["itm", "orange"], ["cli", "white"]].forEach(function (p) { init(p[0] + "-w", { opacity: 0 }); init(p[0] + "-o", { opacity: 0 }); init(p[0] + "-glow", { opacity: 0 }); });
      // he buys nothing: the car stays with its owner
      pre("vdr", { opacity: 0, y: 40 }); go("vdr", { opacity: 1, y: 0 }, 0.05, 0.3, "back.out(1.6)"); lit("vdr", "white", 0.1, 0.2);
      pre("vcar", { opacity: 0, scale: 1.1 }); go("vcar", { opacity: 1, scale: 1 }, 0.12, 0.35, "expo.out");
      pre("whov", { opacity: 0 }); go("whov", { opacity: 1 }, 0.2, 0.3);
      pre("itm", { opacity: 0, y: 40 }); go("itm", { opacity: 1, y: 0 }, at("rien") - 0.1, 0.3, "back.out(1.6)"); lit("itm", "orange", at("rien"), 0.3);
      pre("whoi", { opacity: 0 }); go("whoi", { opacity: 1 }, at("rien"), 0.3);
      // the seller gives a mandate
      arrow("m1", at("mandat") - 0.1, 0.35);
      pre("lm", { opacity: 0, scale: 0.6 }); go("lm", { opacity: 1, scale: 1 }, at("mandat") - 0.05, 0.25, "back.out(2)");
      // he finds the client
      pre("cli", { opacity: 0, y: 40 }); go("cli", { opacity: 1, y: 0 }, at("client") - 0.1, 0.3, "back.out(1.6)"); lit("cli", "white", at("client"), 0.2);
      pre("whoc", { opacity: 0 }); go("whoc", { opacity: 1 }, at("client"), 0.3);
      draw("m2", at("organise") - 0.05, 0.4, "power2.inOut");
      // the money goes client -> seller, the commission comes back to him
      go("lm", { opacity: 0 }, at("15000") - 0.2, 0.2); go("m1", { opacity: 0 }, at("commission") - 0.25, 0.15); go("m1h", { opacity: 0 }, at("commission") - 0.25, 0.15);
      arrow("m3", at("15000") - 0.1, 0.4);
      pre("l15", { opacity: 0, scale: 0.6 }); go("l15", { opacity: 1, scale: 1 }, at("15000") - 0.05, 0.25, "back.out(2)"); odo("v15", at("15000"), 0.8, { from: "00 000" });
      arrow("m4", at("commission") - 0.1, 0.45);
      pre("lc", { opacity: 0, scale: 0.6 }); go("lc", { opacity: 1, scale: 1 }, at("1500") - 0.1, 0.25, "back.out(2)"); odo("com", at("1500") - 0.05, 0.8, { from: "0 000" });
      init("itm-glow", { scale: 1 }); go("itm-glow", { scale: 1.3 }, at("1500"), 0.2); go("itm-glow", { scale: 1 }, at("1500") + 0.2, 0.4);
      // zero stock, zero cash tied up, zero yard costs
      [["z0", "stock"], ["z1", "trésorerie"], ["z2", "frais"]].forEach(function (z) {
        pre(z[0], { opacity: 0, y: 30 }); go(z[0], { opacity: 1, y: 0 }, at(z[1]) - 0.1, 0.3, "back.out(2)");
      });
      // the seller stays the owner until the sale
      pre("key", { opacity: 0, scale: 0.5 }); go("key", { opacity: 1, scale: 1 }, at("propriétaire") - 0.1, 0.25, "back.out(2)");
      
    """
    sfx = [("pop", None, 0, 0.05, .12), ("pop", "rien", 1, -.1, .12), ("whoosh-short", "mandat", 1, -.1, .14),
           ("pop", "client", 1, -.1, .12), ("whoosh-short", "15000", 1, -.1, .14), ("typing", "15000", 1, 0, .1),
           ("whoosh-short", "commission", 1, -.1, .14), ("chime", "1500", 1, -.05, .18), ("pop", "stock", 1, -.1, .12),
           ("pop", "trésorerie", 1, -.1, .12), ("pop", "frais", 1, -.1, .12), ("click-soft", "propriétaire", 1, -.1, .22)]
    return css, st, hud, js, (810, 860), sfx


def scene_05():
    css = COLS_CSS + RISK_CSS + """
    .§row { position: absolute; left: 30px; width: 1020px; height: 150px; border-top: 2px solid #232323; }
    .§rl { position: absolute; left: 0; top: 14px; width: 100%; text-align: center; font: 600 24px/1 "Instrument Sans", sans-serif; color: #8a8a8a; letter-spacing: 0.12em; opacity: 0; }
    .§rv { position: absolute; top: 50px; width: 470px; text-align: center; font: 72px/1.1 "Anton", sans-serif; color: #ffffff; opacity: 0; }
    .§rv.§L { left: 0; } .§rv.§R { left: 530px; width: 400px; color: #FB8000; }
    .§rv.§small { font-size: 50px; top: 62px; }
    #§gap { position: absolute; left: 0; top: 1150px; width: 1080px; text-align: center; opacity: 0; }
    #§gapi { display: inline-block; padding: 8px 30px; border-radius: 40px; background: #FB8000; color: #0A0A0A; font: 50px/1.2 "Anton", sans-serif; }
    .§rk { width: 120px; } .§rki { width: 64px; height: 64px; } .§rkl { font-size: 16px; }
    """
    rows = [("r0", 520, "ARGENT À SORTIR", odo("o1", "12 000 €"), odo("o2", "0 €")),
            ("r1", 670, "GAIN NET PAR VOITURE", odo("g1", "2 300 €"), odo("g2", "1 500 €")),
            ("r2", 820, "RISQUE", "", "—"),
            ("r3", 970, "CE QU’IL FAUT", "TRÉSORERIE", "UN RÉSEAU")]
    st = cols(True)
    for rid, y, lab, lv, rv in rows:
        sm = " §small" if rid == "r3" else ""
        st += (f'<div class="§row" style="top:{y}px"><div id="§{rid}l" class="§rl">{lab}</div>'
               f'<div id="§{rid}a" class="§rv §L{sm}">{lv}</div><div id="§{rid}b" class="§rv §R{sm}">{rv}</div></div>')
    st += risks("rk", 70, 875, ("GARANTIE", "VICES", "IMMOBILISÉE"))
    st += '<div id="§gap"><span id="§gapi">' + odo("gp", "800 €") + ' D’ÉCART</span></div>'
    st = st.replace('<div id="§r2a" class="§rv §L"></div>', '')
    hud = ""
    js = COLS_JS + """
      heads(0.02, "both");
      go("hL", { y: -40 }, 0.02, 0.4); go("hR", { y: -40 }, 0.02, 0.4); init("divl", { y: 0 });
      function rowL(r, t) { pre(r + "l", { opacity: 0 }); go(r + "l", { opacity: 1 }, t - 0.1, 0.25); }
      // marchand: out 12 000, keeps 2 300, carries all the risk
      rowL("r0", at("sort")); slam("r0a", at("sort") - 0.04); odo("o1", at("sort"), 0.8, { from: "00 000" });
      rowL("r1", at("garde")); slam("r1a", at("garde") - 0.04); odo("g1", at("garde"), 0.8, { from: "0 000" });
      rowL("r2", at("risque") - 0.1);
      ["rk0", "rk1", "rk2"].forEach(function (r, k) { pre(r, { opacity: 0, scale: 0.4 }); go(r, { opacity: 1, scale: 1 }, at("risque") - 0.05 + k * 0.1, 0.25, "back.out(2.2)"); });
      // intermédiaire: out zero, keeps 1 500, carries almost nothing
      slam("r0b", at("sort", 2) - 0.04);
      slam("r1b", at("garde", 2) - 0.04); odo("g2", at("garde", 2), 0.8, { from: "0 000" });
      slam("r2b", at("rien") - 0.04);
      // 800 apart, for 12 000 tied up and all the risks
      pre("gap", { opacity: 0, scale: 0.6 }); go("gap", { opacity: 1, scale: 1 }, at("800") - 0.06, 0.3, "back.out(2)"); odo("gp", at("800") - 0.06, 0.7, { from: "000" });
      go("gap", { opacity: 0 }, at("l'un") - 0.15, 0.2);
      rowL("r3", at("trésorerie")); slam("r3a", at("trésorerie") - 0.04); slam("r3b", at("réseau") - 0.04);
      cam(0, -10, 1.03, at("800"), 0.8);
    """
    sfx = [("pop", "résumé", 1, 0, .14), ("typing", "sort", 1, 0, .1), ("typing", "garde", 1, 0, .1), ("error", "risque", 1, -.05, .14),
           ("pop", "sort", 2, -.04, .12), ("typing", "garde", 2, 0, .1), ("pop", "rien", 1, -.04, .12), ("chime", "800", 1, -.06, .18),
           ("pop", "trésorerie", 1, -.04, .12), ("pop", "réseau", 1, -.04, .12)]
    return css, st, hud, js, (540, 860), sfx


def scene_06():
    css = COLS_CSS + """
    .§box { position: absolute; top: 560px; width: 440px; height: 520px; border-radius: 30px; background: #151515; border: 2px solid #2e2e2e; }
    #§bL { left: 50px; } #§bR { left: 590px; width: 350px; }
    #§q { position: absolute; left: 0; top: 700px; width: 1080px; text-align: center; font: 220px/1 "Anton", sans-serif; color: #FB8000; opacity: 0; }
    #§qx { position: absolute; left: 400px; top: 800px; width: 280px; height: 14px; border-radius: 7px; background: #ffffff; transform: scaleX(0) rotate(-12deg); transform-origin: 0 50%; }
    #§cashw { position: absolute; left: 0; top: 600px; width: 1080px; text-align: center; opacity: 0; }
    #§cashi { display: inline-block; padding: 8px 30px; border-radius: 40px; background: #ffffff; color: #0A0A0A; font: 54px/1.2 "Anton", sans-serif; }
    #§lock { position: absolute; left: 210px; top: 850px; width: 120px; height: 140px; overflow: visible; opacity: 0; }
    #§go { position: absolute; left: 640px; top: 1000px; width: 250px; text-align: center; font: 50px/1.1 "Anton", sans-serif; color: #FB8000; opacity: 0; }
    """
    st = (cols(True) + '<div id="§bL" class="§box"></div><div id="§bR" class="§box"></div>' + person("pL", 200, 790, 140) + person("pR", 695, 780, 140)
          + '<div id="§q">?</div><div id="§qx"></div>'
          + '<div id="§cashw"><span id="§cashi">' + odo("cash", "5 000 €") + ' EN POCHE</span></div>'
          + f'<svg id="§lock" viewBox="0 0 120 140"><path d="M30 64 L30 40 Q30 12 60 12 Q90 12 90 40 L90 64" fill="none" stroke="{RED}" stroke-width="12"/><rect x="14" y="60" width="92" height="72" rx="12" fill="{RED}"/></svg>'
          + '<div id="§go">DÈS DEMAIN</div>'
          + '<svg class="§flow" viewBox="0 0 1080 1920"><path id="§f1" class="§ar" d="M700 1000 C 640 1160, 440 1160, 300 1000"/>' + head("f1", 300, 1000, -130)
          + '<path id="§f2" class="§ar" d="M765 720 A 90 90 0 1 1 764 721" style="stroke-width:10"/></svg>')
    hud = title("t6", ["PAS UNE ÉTAPE.", "UN AVANTAGE."], 560, 120)
    js = COLS_JS + """
      heads(0.02, "both");
      [["pL", "grey"], ["pR", "orange"]].forEach(function (p) { init(p[0] + "-w", { opacity: 0 }); init(p[0] + "-o", { opacity: 0 }); init(p[0] + "-glow", { opacity: 0 }); lit(p[0], p[1], 0.02, 0.2); });
      // which is best? wrong question
      pre("q", { opacity: 0, scale: 0.4 }); go("q", { opacity: 1, scale: 1 }, Math.max(0.02, at("meilleur") - 0.1), 0.3, "back.out(2)");
      tl.fromTo($("qx"), { scaleX: 0 }, { scaleX: 1, duration: 0.22, ease: "power4.out", immediateRender: false }, at("mauvaise") + 0.05);
      go("q", { opacity: 0 }, at("5000") - 0.2, 0.2); go("qx", { opacity: 0 }, at("5000") - 0.2, 0.2);
      // with 5 000: not a dealer, an intermediary tomorrow
      pre("cashw", { opacity: 0, scale: 0.6 }); go("cashw", { opacity: 1, scale: 1 }, at("5000") - 0.1, 0.3, "back.out(2)"); odo("cash", at("5000") - 0.05, 0.7, { from: "0 000" });
      pre("lock", { opacity: 0, scale: 0.5 }); go("lock", { opacity: 1, scale: 1 }, at("marchand") - 0.05, 0.25, "back.out(2)");
      go("bL", { opacity: 0.4 }, at("marchand"), 0.3); go("pL", { opacity: 0.4 }, at("marchand"), 0.3); go("hL", { opacity: 0.4 }, at("marchand"), 0.3);
      pre("go", { opacity: 0, scale: 0.6 }); go("go", { opacity: 1, scale: 1 }, at("demain") - 0.1, 0.25, "back.out(2)");
      // some move on to dealer later; most stay intermediaries
      go("cashw", { opacity: 0 }, at("certains") - 0.15, 0.2); go("lock", { opacity: 0 }, at("certains") - 0.15, 0.2);
      go("bL", { opacity: 1 }, at("certains") - 0.15, 0.3); go("pL", { opacity: 1 }, at("certains") - 0.15, 0.3); go("hL", { opacity: 1 }, at("certains") - 0.15, 0.3);
      arrow("f1", at("certains") - 0.05, 0.6);
      go("go", { opacity: 0 }, at("certains") - 0.15, 0.2);
      draw("f2", at("rester") - 0.1, 0.7, "power2.inOut");
      tl.fromTo($("f2"), { rotation: 0, svgOrigin: "765 810" }, { rotation: 360, svgOrigin: "765 810", duration: 2, ease: "none", immediateRender: false }, at("rester") + 0.6);
      // not a step: an advantage
      go("f1", { opacity: 0.25 }, at("étape") - 0.2, 0.3); go("f1h", { opacity: 0.25 }, at("étape") - 0.2, 0.3);
      ["bL", "bR", "pL", "pR"].forEach(function (b) { go(b, { opacity: 0.35 }, at("étape") - 0.2, 0.3); });
      slam("t6-0", at("étape") - 0.05); slam("t6-1", at("avantage") - 0.05); stroke("t6", at("avantage") + 0.2);
      cam(0, -10, 1.03, at("étape"), 0.8);
    """
    sfx = [("pop", "meilleur", 1, -.1, .14), ("click", "mauvaise", 1, .05, .25), ("typing", "5000", 1, -.05, .1),
           ("click", "marchand", 1, -.05, .22), ("pop", "demain", 1, -.1, .14), ("whoosh-short", "certains", 1, -.05, .14),
           ("whoosh-short", "rester", 1, -.1, .14), ("pop", "étape", 1, -.05, .14), ("impact-bass-2", "avantage", 1, -.05, .26)]
    return css, st, hud, js, (540, 860), sfx


def scene_07():
    css = """
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
    st = '<div id="§meglow"></div><div id="§me"><img src="assets/img/guillaume.png"></div>'
    hud = (title("t7", ["PAS UNE ÉTAPE.", "UN AVANTAGE."], 560, 120)
           + '<div id="§handle"><span id="§hname">@guillaumeherbin_<i class="§stilt"><i class="§stk" id="§h-s"></i></i></span>'
             '<div id="§pill"><span id="§pilli">S’ABONNER</span></div></div>')
    js = """
      tl.set([$("t7-0"), $("t7-1")], { opacity: 1 }, 0); tl.set($("t7-s"), { scaleX: 1 }, 0);
      init("t7", { y: 0, scale: 1 }); go("t7", { y: -440, scale: 0.68 }, Math.max(0.02, at("abonne-toi") - 0.2), 0.5, "power3.inOut");
      slam("hname", at("abonne-toi") + 0.05, { s: 1.3 }); stroke("h", at("abonne-toi") + 0.25);
      pre("pilli", { opacity: 0, scale: 0.5 }); go("pilli", { opacity: 1, scale: 1 }, at("pour") - 0.04, 0.3, "back.out(2)");
      pre("me", { opacity: 0, y: 60 }); go("me", { opacity: 1, y: 0 }, Math.max(0.08, at("abonne-toi") + 0.1), 0.6, "power3.out");
      pre("meglow", { opacity: 0, scale: 0.6 }); go("meglow", { opacity: 1, scale: 1 }, Math.max(0.15, at("abonne-toi") + 0.2), 0.7, "power2.out");
      init("halo", { scale: 1 }); go("halo", { scale: 1.2 }, 0, DUR, "sine.inOut");
    """
    sfx = [("notification", "abonne-toi", 1, 0, .25), ("pop", "pour", 1, -.04, .14)]
    return css, st, hud, js, (540, 760), sfx


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
message: "Même voiture à 15 000 € : le marchand achète, stocke et porte tout le risque pour environ 2 300 € ; l'intermédiaire, sous mandat, touche 1 500 € sans stock ni trésorerie. Ne pas avoir de stock n'est pas une étape, c'est un avantage."
arc: Hook → Setup → Marchand → Intermédiaire → Face-à-face → Vrai choix → CTA
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
- **Negative list** : aucun billet ni espèce ; jamais plus de 6 mots par bloc de texte ; plaques et logos floutés ; deux colonnes MARCHAND (gauche) / INTERMÉDIAIRE (droite) dès la scène 2 ; risques en rouge sombre.

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
