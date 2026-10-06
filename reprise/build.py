#!/usr/bin/env python3
"""Reel « Prends l'acheteur avec reprise » : one source for the whole film.

Every animation of every scene is placed on a WORD of the voice (at("virement"), at("même", 2)...), never on a fixed
second. The word timings come from one file:
  - assets/audio/voix-montage-mots.json when the real voice is there (align.py writes it), or
  - a provisional timing spread over the brief's windows (0-5, 5-11, 11-17, 17-29, 29-40, 40-49, 49-54, 54-60 s).
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
   "Tu achètes et tu revends", "des *voitures*~?", "OK.", "Prenons le cas", "de deux *acheteurs*.", "Même voiture",
   "et même *prix*."]),
 dict(id="02-acheteur1", name="Acheteur 1", window=(5, 11), chunks=[
   "Le premier te l'achète", "*10~000* euros comptant,", "sans *discuter*,", "*virement* le jour même.", "Le *rêve*."]),
 dict(id="03-acheteur2", name="Acheteur 2", window=(11, 17), chunks=[
   "Le second te l'achète", "aussi *10~000* euros,", "mais il a une voiture", "à *reprendre*.",
   "La plupart des vendeurs", "choisissent le *premier*.", "*Erreur*."]),
 dict(id="04-calcul", name="Le calcul", window=(17, 29), chunks=[
   "Avec lui, tu fais", "une deuxième *vente*.", "Tu *reprends* sa voiture", "au juste prix,",
   "tu la *revends* derrière.", "Même *client*,", "deux *marges*."]),
 dict(id="05-tresorerie", name="La trésorerie", window=(29, 40), chunks=[
   "La voiture que tu vends", "est à *toi*,", "donc cette *reprise*,", "tu la paies avec", "l'argent de la *vente*.",
   "Pas de *crédit*,", "pas d'*intérêts*.", "L'argent emprunté", "coûte *cher*~:", "chaque voiture que tu",
   "ne finances pas", "à la *banque*,", "c'est de la *marge*", "que tu gardes."]),
 dict(id="06-piege", name="Le piège", window=(40, 49), chunks=[
   "Mais attention", "au *piège*~:", "*surpayer* la reprise", "pour signer la vente.", "Une reprise trop *chère*",
   "*mange* la marge", "que tu viens de faire.", "Elle s'estime", "comme un *achat*,", "au *centime* près."]),
 dict(id="07-bonus", name="Le bonus", window=(49, 54), chunks=[
   "Et en *2026*,", "trouver des voitures,", "c'est le plus *dur*.", "La *reprise*,", "c'est une voiture",
   "qui vient à *toi*."]),
 dict(id="08-cta", name="CTA", window=(54, 60), chunks=[
   "Entre deux clients", "au même *prix*,", "prends celui qui a", "une *reprise*.", "*Abonne-toi*",
   "pour plus de contenu", "comme celui-ci."]),
]
SPOKEN_SYL = {"10000": 3, "2026": 5}   # « dix mille », « deux mille vingt-six »


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

def scene_01():
    css = """
    #§banner { position: absolute; left: 0; top: 250px; width: 1080px; height: 150px; background: #FB8000;
      font: 86px/150px "Anton", sans-serif; color: #0A0A0A; text-align: center; white-space: nowrap; }
    .§bw { display: inline-block; opacity: 0; margin: 0 10px; }
    .§q { position: absolute; width: 190px; text-align: center; font: 100px/1 "Anton", sans-serif; color: #FB8000; opacity: 0; }
    """
    st = stage(extra='<div id="§qa" class="§q" style="left:90px;top:680px">?</div>'
                     '<div id="§qb" class="§q" style="left:750px;top:680px">?</div>')
    hud = ('<div id="§banner">' + "".join(f'<span class="§bw" id="§bw{i}">{w}</span>' for i, w in
                                         enumerate(["TU", "ACHÈTES", "TES", "VOITURES ?"])) + '</div>'
           + title("t1", ["MÊME VOITURE.", "MÊME PRIX."], 285, 120))
    js = """
      pre("banner", { y: -420 }); go("banner", { y: 0 }, 0, 0.32, "expo.out");
      var bw = ["tu", "achètes", "des", "voitures"];
      for (var i = 0; i < 4; i++) slam("bw" + i, Math.max(0.03, at(bw[i]) - 0.03), { s: 1.4, d: 0.15 });
      pre("car", { opacity: 0 }); slam("car", at("voitures") - 0.03, { s: 1.3, d: 0.2 });
      init("halo", { scale: 1, opacity: 1 }); go("halo", { scale: 1.15 }, at("voitures"), 0.4);
      ["pa", "pb"].forEach(function (p) { init(p + "-w", { opacity: 0 }); init(p + "-o", { opacity: 0 }); init(p + "-glow", { opacity: 0 }); });
      pre("pa", { opacity: 0, y: 60 }); pre("pb", { opacity: 0, y: 60 });
      go("pa", { opacity: 1, y: 0 }, at("deux") - 0.03, 0.28, "back.out(1.6)");
      go("pb", { opacity: 1, y: 0 }, at("deux") + 0.07, 0.28, "back.out(1.6)");
      go("pa-w", { opacity: 1 }, at("acheteurs"), 0.2); go("pb-w", { opacity: 1 }, at("acheteurs") + 0.06, 0.2);
      // the banner leaves, the title takes its place
      go("banner", { y: -170, opacity: 0 }, at("même") - 0.14, 0.2, "power3.in");
      slam("t1-0", at("même")); slam("t1-1", at("même", 2)); stroke("t1", at("prix") + 0.05);
      cam(0, -10, 1.04, at("même") - 0.05, 0.45);
      // same car, same price: which one ? the light hesitates between the two buyers
      var q = atEnd("prix") + 0.05;
      pre("qa", { opacity: 0, scale: 0.4 }); pre("qb", { opacity: 0, scale: 0.4 });
      go("qa", { opacity: 1, scale: 1 }, q, 0.25, "back.out(2)");
      go("qb", { opacity: 1, scale: 1 }, q + 0.08, 0.25, "back.out(2)");
      var step = Math.max(0.16, Math.min(0.3, (DUR - q - 0.15) / 4));
      ["pa", "pb", "pa", "pb"].forEach(function (p, k) {
        go(p + "-o", { opacity: 0.95 }, q + 0.1 + k * step, 0.07, "power2.out");
        go(p + "-o", { opacity: 0 }, q + 0.1 + k * step + step * 0.6, 0.1, "power2.in");
      });
      cam(0, -14, 1.07, q, 0.6, "power2.out");
    """
    sfx = [("pop", "tu", 1, 0, .14), ("pop", "voitures", 1, 0, .18), ("pop", "deux", 1, 0, .12), ("whoosh-short", "même", 1, -.12, .16),
           ("pop", "même", 1, 0, .16), ("pop", "même", 2, 0, .16), ("pop", "prix", 1, .45, .14)]
    return css, st, hud, js, (540, 840), sfx


def scene_02():
    css = """
    #§notif { position: absolute; left: 100px; top: 1078px; width: 820px; height: 156px; border-radius: 34px;
      background: rgba(30,30,30,0.96); border: 2px solid #2e2e2e; box-shadow: 0 24px 60px rgba(0,0,0,0.6); }
    #§nicon { position: absolute; left: 30px; top: 34px; width: 88px; height: 88px; border-radius: 24px; background: #FB8000; }
    #§nicon svg { position: absolute; left: 0; top: 0; width: 88px; height: 88px; fill: none; stroke: #0A0A0A; stroke-width: 7; stroke-linecap: round; stroke-linejoin: round; }
    #§nlab { position: absolute; left: 146px; top: 26px; font: 600 38px/1.2 "Instrument Sans", sans-serif; color: #bdbdbd; }
    #§nval { position: absolute; left: 146px; top: 70px; font: 64px "Anton", sans-serif; color: #ffffff; }
    .§spark { position: absolute; width: 18px; height: 18px; border-radius: 50%; background: #FB8000; opacity: 0; }
    """
    st = stage()
    sparks = "".join(f'<div id="§sp{i}" class="§spark" style="left:{165 + 0}px;top:{1138}px"></div>' for i in range(6))
    hud = (title("t2", [(odo("amt", "10 000 €"), 150), ("COMPTANT", 110)], 270, 120)
           + '<div id="§notif"><div id="§nicon"><svg viewBox="0 0 88 88"><path d="M44 18 L44 54 M28 40 L44 56 L60 40"/>'
             '<path d="M24 66 L64 66"/></svg></div><div id="§nlab">Virement reçu</div>'
           + f'<div id="§nval">{odo("nv", "+10 000,00 €")}</div></div>' + sparks)
    js = """
      ["pa", "pb"].forEach(function (p) { init(p + "-w", { opacity: 1 }); init(p + "-o", { opacity: 0 }); init(p + "-glow", { opacity: 0 }); });
      tl.set([$("pa-w"), $("pb-w")], { opacity: 1 }, 0);
      lit("pa", "orange", 0.05, 0.35); lit("pb", "dim", 0.05, 0.35); go("car", { opacity: 0.45 }, 0.05, 0.35);
      cam(240, -70, 1.1, 0, 0.7);
      slam("t2-0", at("10000") - 0.05, { s: 1.2 }); odo("amt", at("10000") - 0.05, 0.9);
      slam("t2-1", at("comptant")); stroke("t2", at("comptant") + 0.15);
      init("pa-glow", { scale: 1 });
      go("pa-glow", { scale: 1.3 }, at("discuter"), 0.18, "power2.out"); go("pa-glow", { scale: 1 }, at("discuter") + 0.18, 0.35, "power2.inOut");
      pre("notif", { opacity: 0, y: 110 }); go("notif", { opacity: 1, y: 0 }, at("virement") - 0.1, 0.38, "back.out(1.5)");
      odo("nv", at("virement") + 0.12, 0.85);
      // « le rêve » : sparks out of the notification, the halo blooms
      for (var i = 0; i < 6; i++) {
        var a = (i / 6) * Math.PI * 2 - 0.4;
        pre("sp" + i, { opacity: 0, scale: 0.3, x: 0, y: 0 });
        go("sp" + i, { opacity: 1, scale: 1, x: Math.cos(a) * 110, y: Math.sin(a) * 90 }, at("rêve") - 0.04 + i * 0.02, 0.3, "power3.out");
        go("sp" + i, { opacity: 0, scale: 0.4 }, at("rêve") + 0.36 + i * 0.02, 0.3, "power2.in");
      }
      init("halo", { scale: 1, opacity: 1 }); go("halo", { scale: 1.3 }, at("rêve") - 0.05, 0.5);
      cam(270, -90, 1.15, at("rêve") - 0.05, 0.7, "power2.out");
    """
    sfx = [("typing", "10000", 1, -.05, .12), ("pop", "comptant", 1, 0, .14), ("notification", "virement", 1, -.1, .3),
           ("typing", "virement", 1, .12, .1), ("sparkle", "rêve", 1, -.04, .25)]
    return css, st, hud, js, (240, 830), sfx


def scene_03():
    css = """
    #§ring { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; fill: none; stroke-linecap: round; }
    #§ringc { stroke: #ffffff; stroke-width: 8; }
    .§xl { stroke: #FB8000; stroke-width: 24; }
    """
    st = stage(car2=True, extra='<svg id="§ring" viewBox="0 0 1080 1920"><circle id="§ringc" cx="185" cy="935" r="172"'
                                ' transform="rotate(-90 185 935)"/>'
                                '<path id="§x1" class="§xl" d="M75 825 L295 1045"/><path id="§x2" class="§xl" d="M295 825 L75 1045"/></svg>')
    hud = (title("t3", [(odo("amt", "10 000 €"), 150), ("+ REPRISE", 110)], 270, 120)
           + title("t3e", ["ERREUR."], 330, 190))
    js = """
      ["pa", "pb"].forEach(function (p) { init(p + "-w", { opacity: 1 }); init(p + "-o", { opacity: 0 }); init(p + "-glow", { opacity: 0 }); });
      tl.set([$("pa-w"), $("pb-w")], { opacity: 1 }, 0);
      lit("pb", "orange", 0.05, 0.35); lit("pa", "dim", 0.05, 0.35); go("car", { opacity: 0.25 }, 0.05, 0.35);
      cam(-240, 10, 1.1, 0, 0.7);
      slam("t3-0", at("10000") - 0.05, { s: 1.2 }); odo("amt", at("10000") - 0.05, 0.9);
      // the car to take back appears behind him
      pre("car2", { opacity: 0, x: 160 }); go("car2", { opacity: 1, x: 0 }, at("voiture") - 0.06, 0.45, "power3.out");
      slam("t3-1", at("reprendre")); stroke("t3", at("reprendre") + 0.15);
      // « la plupart choisissent le premier » : pull back, the ring circles the first buyer
      cam(0, 0, 1, at("plupart") - 0.12, 0.55);
      go("car", { opacity: 1 }, at("plupart"), 0.3);
      lit("pb", "white", at("plupart"), 0.3); lit("pa", "white", at("vendeurs"), 0.3);
      $("ringc").style.opacity = 1; draw("ringc", at("choisissent"), 0.45, "power2.inOut");
      init("ringc", { scale: 1 }); tl.set($("ringc"), { transformOrigin: "50% 50%" }, 0);
      // « erreur » : the ring goes, a big orange cross, the first buyer dims, the second lights up
      pre("x1", {}); pre("x2", {});
      go("ringc", { opacity: 0 }, at("erreur") - 0.06, 0.1, "power2.in");
      draw("x1", at("erreur") - 0.04, 0.13, "power4.out"); draw("x2", at("erreur") + 0.06, 0.13, "power4.out");
      shake("shk", at("erreur") + 0.04, 16);
      lit("pa", "dim", at("erreur") + 0.12, 0.25); lit("pb", "orange", at("erreur") + 0.16, 0.3);
      go("t3", { opacity: 0, y: -30 }, at("erreur") - 0.12, 0.12, "power2.in");
      slam("t3e-0", at("erreur"), { s: 1.4 }); stroke("t3e", at("erreur") + 0.14);
      cam(-60, -6, 1.05, at("erreur") + 0.2, 0.6, "power2.out");
    """
    sfx = [("typing", "10000", 1, -.05, .12), ("whoosh-short", "voiture", 1, -.06, .18), ("pop", "reprendre", 1, 0, .14),
           ("click", "choisissent", 1, 0, .3), ("error", "erreur", 1, -.03, .3), ("impact-bass-1", "erreur", 1, -.03, .3)]
    return css, st, hud, js, (860, 830), sfx


def card_rows(cid, header, rows, summary, accent):
    h = f'<div id="§{cid}" class="§card{" §cardb" if accent else ""}"><div id="§{cid}-hl" class="§cardhl"></div>'
    h += f'<div class="§chead{" §or" if accent else ""}">{header}</div><div class="§cdiv"></div>'
    for i, (lab, val) in enumerate(rows):
        h += (f'<div id="§{cid}-r{i}" class="§row" style="top:{130 + i * 116}px"><div class="§rlab">{lab}</div>'
              f'<div class="§rval">{odo(f"{cid}-v{i}", val)}</div></div>')
    h += f'<div id="§{cid}-sum" class="§sum{" §or" if accent else ""}">'
    h += "".join(f'<span id="§{cid}-s{i}" class="§sline">{s}</span><br>' for i, s in enumerate(summary)) + "</div></div>"
    return h


def scene_04():
    css = """
    .§card { position: absolute; top: 592px; width: 420px; height: 630px; border-radius: 30px; background: #151515; border: 2px solid #262626; }
    .§cardhl { position: absolute; left: -2px; top: -2px; right: -2px; bottom: -2px; border-radius: 30px; border: 4px solid #FB8000; opacity: 0;
      box-shadow: 0 0 40px rgba(251,128,0,0.35); }
    #§ca { left: 80px; } #§cb { left: 520px; }
    .§chead { position: absolute; left: 0; top: 30px; width: 100%; text-align: center; font: 56px/1.15 "Anton", sans-serif; color: #ffffff; }
    .§or { color: #FB8000; }
    .§cdiv { position: absolute; left: 34px; right: 34px; top: 118px; height: 2px; background: #2a2a2a; }
    .§row { position: absolute; left: 34px; width: 352px; }
    .§rlab { font: 600 30px/36px "Instrument Sans", sans-serif; color: #9a9a9a; text-transform: uppercase; letter-spacing: 0.02em; }
    .§rval { font: 64px "Anton", sans-serif; color: #ffffff; margin-top: 4px; }
    .§sum { position: absolute; left: 0; top: 512px; width: 100%; text-align: center; font: 50px/1.12 "Anton", sans-serif; color: #8a8a8a; }
    .§sline { display: inline-block; opacity: 0; }
    """
    st = (card_rows("ca", "ACHETEUR 1", [("Vente", "10 000 €")], ["1 VENTE", "1 MARGE"], False)
          + card_rows("cb", "ACHETEUR 2", [("Vente", "10 000 €"), ("Reprise estimée", "6 500 €"), ("Revendue", "8 000 €")],
                      ["2 VENTES", "2 MARGES"], True))
    hud = title("t4", ["LE CALCUL"], 300, 124)
    js = """
      slam("t4-0", 0.02); stroke("t4", 0.25);
      pre("ca", { opacity: 0, y: 90 }); pre("cb", { opacity: 0, y: 90 });
      go("ca", { opacity: 1, y: 0 }, 0.1, 0.42, "expo.out"); go("cb", { opacity: 1, y: 0 }, 0.2, 0.42, "expo.out");
      odo("ca-v0", 0.3, 0.8); odo("cb-v0", 0.4, 0.8);
      pre("cb-r1", { opacity: 0 }); pre("cb-r2", { opacity: 0 });
      slam("ca-s0", at("fais") - 0.05, { s: 1.2 }); slam("ca-s1", at("fais") + 0.1, { s: 1.2 });
      slam("cb-s0", at("vente") - 0.03, { s: 1.4 });
      cam(-40, 0, 1.04, at("reprends") - 0.1, 0.5);
      slam("cb-r1", at("reprends") - 0.05, { s: 1.15 }); odo("cb-v1", at("prix") - 0.1, 0.8);
      slam("cb-r2", at("revends") - 0.05, { s: 1.15 }); odo("cb-v2", at("revends") + 0.05, 0.8);
      pre("cb-hl", { opacity: 0 }); go("cb-hl", { opacity: 1 }, at("client") - 0.05, 0.3);
      go("ca", { opacity: 0.45 }, at("client"), 0.4);
      slam("cb-s1", at("marges") - 0.03, { s: 1.4 });
      cam(-20, -6, 1.04, at("marges") - 0.05, 0.6, "power2.out");
    """
    sfx = [("pop", None, 0, 0.02, .14), ("typing", None, 0, 0.3, .12), ("pop", "fais", 1, -.05, .12), ("pop", "vente", 1, -.03, .16),
           ("pop", "reprends", 1, -.05, .12), ("typing", "prix", 1, -.1, .12), ("pop", "revends", 1, -.05, .12),
           ("typing", "revends", 1, .05, .12), ("click-soft", "client", 1, -.05, .3), ("pop", "marges", 1, -.03, .2)]
    return css, st, hud, js, (730, 900), sfx


def scene_05():
    css = """
    .§node { position: absolute; width: 400px; height: 180px; border-radius: 30px; background: #151515; border: 2px solid #2a2a2a; opacity: 0; }
    #§n1 { left: 80px; top: 660px; } #§n2 { left: 520px; top: 990px; width: 400px; border-color: #FB8000; }
    .§nlab { position: absolute; left: 34px; top: 24px; font: 600 30px/36px "Instrument Sans", sans-serif; color: #9a9a9a; text-transform: uppercase; }
    .§nval { position: absolute; left: 34px; top: 64px; font: 84px "Anton", sans-serif; color: #ffffff; }
    #§toi { position: absolute; left: 390px; top: 632px; padding: 6px 22px; border-radius: 14px; background: #FB8000; color: #0A0A0A;
      font: 44px/1.2 "Anton", sans-serif; transform: rotate(-6deg); opacity: 0; }
    #§flowsvg { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; fill: none; stroke-linecap: round; stroke-linejoin: round; }
    #§arrow { stroke: #FB8000; stroke-width: 12; }
    #§flow { stroke: #ffd0a0; stroke-width: 14; stroke-dasharray: 2 34; opacity: 0; }
    #§head { stroke: #FB8000; stroke-width: 12; opacity: 0; }
    #§bline { stroke: #4a4a4a; stroke-width: 6; stroke-dasharray: 16 14; opacity: 0; }
    .§bx { stroke: #FB8000; stroke-width: 14; }
    #§bank { position: absolute; left: 100px; top: 1000px; width: 240px; height: 250px; opacity: 0; }
    #§bank svg { position: absolute; left: 10px; top: 0; width: 220px; height: 200px; fill: none; stroke: #5a5a5a; stroke-width: 9; stroke-linejoin: round; }
    #§banklab { position: absolute; left: 0; top: 206px; width: 240px; text-align: center; font: 600 30px "Instrument Sans", sans-serif; color: #6f6f6f; letter-spacing: 0.06em; }
    #§pct { position: absolute; left: 196px; top: -26px; width: 84px; height: 84px; border-radius: 50%; background: #FB8000; color: #0A0A0A;
      font: 52px/84px "Anton", sans-serif; text-align: center; opacity: 0; }
    #§chip { position: absolute; left: 600px; top: 1186px; height: 64px; padding: 0 28px 0 76px; border-radius: 32px; background: #FB8000;
      color: #0A0A0A; font: 46px/64px "Anton", sans-serif; opacity: 0; box-shadow: 0 0 40px rgba(251,128,0,0.45); }
    #§lock { position: absolute; left: 22px; top: 4px; width: 44px; height: 56px; overflow: visible; }
    #§shackle { fill: none; stroke: #0A0A0A; stroke-width: 7; stroke-linecap: round; }
    """
    st = ('<svg id="§flowsvg" viewBox="0 0 1080 1920">'
          '<path id="§bline" d="M340 1100 L516 1088"/>'
          '<path id="§bx1" class="§bx" d="M404 1070 L452 1118"/><path id="§bx2" class="§bx" d="M452 1070 L404 1118"/>'
          '<path id="§arrow" d="M300 846 C 300 930, 660 900, 700 980"/>'
          '<path id="§flow" d="M300 846 C 300 930, 660 900, 700 980"/>'
          '<g transform="translate(702 984) rotate(67)"><path id="§head" d="M-34 -22 L0 0 L-34 22"/></g></svg>'
          '<div id="§n1" class="§node"><div class="§nlab">Vente</div><div class="§nval">' + odo("n1v", "10 000 €") + '</div></div>'
          '<div id="§toi">À TOI</div>'
          '<div id="§n2" class="§node"><div class="§nlab">Reprise</div><div class="§nval">' + odo("n2v", "6 500 €") + '</div></div>'
          '<div id="§bank"><div id="§bankshk" class="§abs" style="left:0;top:0;width:240px;height:250px">'
          '<svg viewBox="0 0 240 220"><path d="M20 72 L120 14 L220 72 Z"/><path d="M56 88 L56 176 M98 88 L98 176 M142 88 L142 176 M184 88 L184 176"/>'
          '<path d="M30 184 L210 184 M18 204 L222 204"/></svg><div id="§banklab">BANQUE</div><div id="§pct">%</div></div></div>'
          '<div id="§chip"><svg id="§lock" viewBox="0 0 44 56"><path id="§shackle" d="M11 26 L11 17 Q11 5 22 5 Q33 5 33 17 L33 26"/>'
          '<rect x="3" y="24" width="38" height="30" rx="6" fill="#0A0A0A"/></svg>MARGE</div>')
    hud = title("t5a", ["PAYÉE PAR", "LA VENTE"], 280, 116) + title("t5b", ["PAS PAR", "LA BANQUE"], 280, 116)
    js = """
      slam("n1", 0.02, { s: 1.2 }); odo("n1v", 0.08, 0.8);
      pre("toi", { opacity: 0, scale: 2.4, rotation: -6 }); go("toi", { opacity: 1, scale: 1, rotation: -6 }, at("toi") - 0.06, 0.16, "expo.in");
      slam("n2", at("reprise") - 0.05, { s: 1.2 }); odo("n2v", at("reprise"), 0.8);
      // the sale pays the trade-in: the arrow draws, the money flows
      draw("arrow", at("paies") - 0.05, 0.5, "power2.inOut");
      pre("head", { opacity: 0 }); go("head", { opacity: 1 }, at("paies") + 0.4, 0.1);
      pre("flow", { opacity: 0 }); go("flow", { opacity: 1 }, at("paies") + 0.45, 0.25);
      var f0 = at("paies") + 0.45; tl.fromTo($("flow"), { strokeDashoffset: 0 }, { strokeDashoffset: -36 * Math.round((DUR - f0) * 2.2), duration: DUR - f0, ease: "none", immediateRender: false }, f0);
      slam("t5a-0", at("l'argent")); slam("t5a-1", at("vente")); stroke("t5a", at("vente") + 0.12);
      init("halo", { x: 0, y: 0, scale: 1 }); go("halo", { x: 220, y: 200 }, at("vente"), 0.8, "power2.inOut");
      // not the bank
      pre("bank", { opacity: 0, y: 40 }); go("bank", { opacity: 1, y: 0 }, at("crédit") - 0.2, 0.3);
      pre("bline", { opacity: 0 }); go("bline", { opacity: 1 }, at("crédit") - 0.05, 0.2);
      go("t5a", { opacity: 0, y: -30 }, at("pas") - 0.14, 0.13, "power2.in");
      slam("t5b-0", at("pas")); slam("t5b-1", at("d'intérêts")); stroke("t5b", at("d'intérêts") + 0.12);
      draw("bx1", at("crédit") + 0.08, 0.12, "power4.out"); draw("bx2", at("crédit") + 0.18, 0.12, "power4.out");
      pre("pct", { opacity: 0, scale: 0 }); go("pct", { opacity: 1, scale: 1 }, at("emprunté") - 0.05, 0.25, "back.out(2.2)");
      wobble("bankshk", at("cher") - 0.02, 5);
      go("bank", { opacity: 0.28, x: -24 }, at("banque") - 0.05, 0.45); go("bline", { opacity: 0.25 }, at("banque") - 0.05, 0.45);
      // the margin you keep
      pre("chip", { opacity: 0, scale: 0.6 }); go("chip", { opacity: 1, scale: 1 }, at("marge") - 0.04, 0.26, "back.out(2)");
      pre("shackle", { y: -9 }); go("shackle", { y: 0 }, at("gardes") + 0.05, 0.14, "power4.in");
      init("chip", { opacity: 1, scale: 1 }); go("chip", { scale: 1.08 }, at("gardes") + 0.19, 0.12, "power2.out"); go("chip", { scale: 1 }, at("gardes") + 0.31, 0.3, "power2.inOut");
      cam(10, -10, 1.03, at("crédit") - 0.1, 0.6); cam(-10, -14, 1.04, at("marge") - 0.1, 0.7, "power2.out");
    """
    sfx = [("typing", None, 0, 0.08, .12), ("pop", "toi", 1, -.06, .18), ("typing", "reprise", 1, 0, .12),
           ("whoosh-short", "paies", 1, -.05, .18), ("pop", "l'argent", 1, 0, .12), ("pop", "pas", 1, 0, .14),
           ("glitch-1", "crédit", 1, .08, .14), ("pop", "emprunté", 1, -.05, .14), ("click", "cher", 1, 0, .25),
           ("chime", "marge", 1, -.04, .2), ("click", "gardes", 1, .05, .35)]
    return css, st, hud, js, (300, 760), sfx


def scene_06():
    css = """
    #§warn { position: absolute; left: 190px; top: 640px; width: 700px; height: 520px; opacity: 0; }
    #§wtri { position: absolute; left: 200px; top: 0; width: 300px; height: 270px; overflow: visible; }
    #§wlab { position: absolute; left: 0; top: 300px; width: 700px; text-align: center; font: 140px/1.15 "Anton", sans-serif; color: #FB8000; }
    #§card { position: absolute; left: 140px; top: 640px; width: 800px; height: 580px; border-radius: 30px; background: #151515; border: 2px solid #2a2a2a; opacity: 0; }
    .§clab { position: absolute; left: 44px; font: 600 32px/38px "Instrument Sans", sans-serif; color: #9a9a9a; text-transform: uppercase; }
    #§repv { position: absolute; left: 44px; top: 112px; font: 112px "Anton", sans-serif; color: #ffffff; }
    #§marv { position: absolute; left: 44px; top: 352px; font: 76px "Anton", sans-serif; color: #FB8000; }
    #§bar { position: absolute; left: 44px; top: 462px; width: 712px; height: 30px; border-radius: 15px; background: #FB8000; transform-origin: 0 50%; }
    #§bartrack { position: absolute; left: 44px; top: 462px; width: 712px; height: 30px; border-radius: 15px; background: #242424; }
    .§drop { position: absolute; width: 16px; height: 24px; border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%; background: #FB8000; opacity: 0; }
    #§sig { position: absolute; left: 0; top: 0; width: 800px; height: 580px; overflow: visible; fill: none; stroke: #ffffff; stroke-width: 5; stroke-linecap: round; stroke-linejoin: round; }
    #§chk { position: absolute; left: 640px; top: 120px; width: 112px; height: 112px; border-radius: 50%; background: #FB8000; opacity: 0; }
    #§chk svg { position: absolute; left: 0; top: 0; width: 112px; height: 112px; fill: none; stroke: #0A0A0A; stroke-width: 12; stroke-linecap: round; stroke-linejoin: round; }
    """
    drops = "".join(f'<div id="§dr{i}" class="§drop" style="left:{140 + i * 230}px;top:486px"></div>' for i in range(3))
    st = ('<div id="§warn"><svg id="§wtri" viewBox="0 0 300 270"><path d="M150 22 L282 250 L18 250 Z" fill="#FB8000" stroke="#FB8000" '
          'stroke-width="26" stroke-linejoin="round"/><rect x="137" y="88" width="26" height="104" rx="13" fill="#0A0A0A"/>'
          '<circle cx="150" cy="222" r="16" fill="#0A0A0A"/></svg><div id="§wlab">ATTENTION</div></div>'
          '<div id="§card"><div class="§clab" style="top:66px">Reprise</div><div id="§repv">' + odo("rv", "6 500,00 €") + '</div>'
          '<div class="§clab" style="top:306px">Marge</div><div id="§marv">' + odo("mv", "1 500 €") + '</div>'
          '<div id="§bartrack"></div><div id="§bar"></div>' + drops +
          '<svg id="§sig" viewBox="0 0 800 580"><path id="§sigp" d="M430 548 C 452 506, 470 568, 494 530 S 528 498, 546 534 S 590 560, 612 526 '
          'S 650 504, 676 536 L 744 528"/></svg>'
          '<div id="§chk"><svg viewBox="0 0 112 112"><path d="M30 58 L48 76 L84 38"/></svg></div></div>')
    hud = title("t6a", ["REPRISE SURPAYÉE", "= MARGE PERDUE"], 280, 108) + title("t6b", ["COMME UN ACHAT"], 360, 116)
    js = """
      slam("warn", 0.02, { s: 1.5, d: 0.22 }); wobble("wtri", at("piège") - 0.03, 6);
      init("halo", { scale: 1, opacity: 1 }); go("halo", { scale: 1.25 }, 0.02, 0.4);
      go("warn", { opacity: 0, scale: 0.4, y: -380 }, at("surpayer") - 0.24, 0.26, "power3.in");
      pre("card", { opacity: 0, y: 90 }); go("card", { opacity: 1, y: 0 }, at("surpayer") - 0.06, 0.38, "expo.out");
      odo("rv", 0, 0.01, { from: "6 500,00", spinLow: false }); odo("mv", 0, 0.01, { from: "1 500", spinLow: false });
      // overpaying the trade-in to sign the sale
      init("repv", { color: "#ffffff" });
      odo("rv", at("reprise") - 0.05, 0.9, { to: "8 000,00 €" }); go("repv", { color: "#FB8000" }, at("reprise"), 0.3);
      $("sigp").style.opacity = 1; draw("sigp", at("signer") - 0.04, 0.55, "power1.inOut");
      slam("t6a-0", at("reprise", 2)); slam("t6a-1", at("mange")); stroke("t6a", at("mange") + 0.12);
      // the margin melts
      init("bar", { scaleX: 1 }); go("bar", { scaleX: 0.02 }, at("mange"), 1.1, "power2.in");
      odo("mv", at("mange"), 1.0, { to: "0 000 €", dimLead: true });
      for (var i = 0; i < 3; i++) {
        pre("dr" + i, { opacity: 0, y: 0 });
        go("dr" + i, { opacity: 1 }, at("mange") + 0.15 + i * 0.2, 0.1);
        go("dr" + i, { y: 70, opacity: 0 }, at("mange") + 0.25 + i * 0.2, 0.45, "power2.in");
      }
      wobble("card", at("faire") - 0.05, 1.5);
      // estimated like a purchase, to the cent
      go("t6a", { opacity: 0, y: -30 }, at("s'estime") - 0.12, 0.14, "power2.in");
      odo("rv", at("s'estime"), 0.9, { to: "6 500,00 €" }); go("repv", { color: "#ffffff" }, at("s'estime"), 0.3);
      go("sigp", { opacity: 0 }, at("s'estime"), 0.2);
      go("bar", { scaleX: 1 }, at("s'estime") + 0.2, 0.8, "power3.out");
      odo("mv", at("s'estime") + 0.2, 0.8, { to: "1 500 €", dimLead: true });
      slam("t6b-0", at("achat")); stroke("t6b", at("achat") + 0.12);
      odo("rv", at("centime") - 0.03, 0.7, { to: "6 500,00 €" });
      pre("chk", { opacity: 0, scale: 2.2 }); go("chk", { opacity: 1, scale: 1 }, at("centime") + 0.45, 0.16, "expo.in");
      cam(0, -10, 1.04, at("surpayer"), 0.6); cam(0, -20, 1.08, at("centime") - 0.1, 0.8, "power2.out");
    """
    sfx = [("impact-bass-1", None, 0, 0.02, .3), ("error", "piège", 1, -.03, .22), ("typing", "reprise", 1, -.05, .12),
           ("click-soft", "signer", 1, -.04, .25), ("pop", "reprise", 2, 0, .14), ("glitch-2", "mange", 1, 0, .14),
           ("typing", "s'estime", 1, 0, .12), ("pop", "achat", 1, 0, .14), ("typing", "centime", 1, -.03, .1),
           ("chime", "centime", 1, .45, .22)]
    return css, st, hud, js, (540, 880), sfx


def scene_07():
    css = """
    #§road { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; fill: none; stroke-linecap: round; }
    .§edge { stroke: #3a3a3a; stroke-width: 6; }
    #§mid { stroke: #6a6a6a; stroke-width: 10; stroke-dasharray: 40 46; }
    #§vp { position: absolute; left: 340px; top: 470px; width: 400px; height: 400px; border-radius: 50%;
      background: radial-gradient(closest-side, rgba(251,128,0,0.4), rgba(251,128,0,0)); }
    #§mag { position: absolute; left: 460px; top: 760px; width: 160px; height: 160px; overflow: visible; fill: none; stroke: #ffffff; stroke-linecap: round; opacity: 0; }
    #§carf { position: absolute; left: 240px; top: 770px; width: 600px; height: 450px; transform-origin: 50% 100%; opacity: 0; }
    #§carf svg { position: absolute; left: 0; top: 0; width: 600px; height: 450px; overflow: visible; fill: none; stroke: #ffffff; stroke-width: 9; stroke-linejoin: round; stroke-linecap: round; }
    .§hl { fill: #2a2a2a; }
    .§hlon { fill: #fff3e0; opacity: 0; }
    #§flare { position: absolute; left: 140px; top: 760px; width: 800px; height: 400px; opacity: 0; mix-blend-mode: screen;
      background: radial-gradient(ellipse at 28% 50%, rgba(255,235,210,0.95) 0%, rgba(251,128,0,0.35) 18%, rgba(251,128,0,0) 34%),
                  radial-gradient(ellipse at 72% 50%, rgba(255,235,210,0.95) 0%, rgba(251,128,0,0.35) 18%, rgba(251,128,0,0) 34%); }
    """
    st = ('<div id="§vp"></div><svg id="§road" viewBox="0 0 1080 1920">'
          '<path class="§edge" d="M500 660 L60 1230"/><path class="§edge" d="M580 660 L1020 1230"/>'
          '<path id="§mid" d="M540 660 L540 1230"/></svg>'
          '<svg id="§mag" viewBox="0 0 160 160"><circle cx="64" cy="64" r="44" stroke-width="12"/><path d="M98 98 L144 144" stroke-width="18"/></svg>'
          '<div id="§carf"><svg viewBox="0 0 400 300"><path d="M92 120 L122 44 Q128 30 144 30 L256 30 Q272 30 278 44 L308 120"/>'
          '<path d="M40 150 Q40 122 72 120 L328 120 Q360 122 360 150 L360 232 Q360 246 346 246 L54 246 Q40 246 40 232 Z"/>'
          '<rect x="58" y="246" width="54" height="40" rx="10"/><rect x="288" y="246" width="54" height="40" rx="10"/>'
          '<rect x="150" y="166" width="100" height="46" rx="10"/><path d="M60 118 L34 106 M340 118 L366 106"/>'
          '<ellipse class="§hl" cx="98" cy="172" rx="34" ry="18"/><ellipse class="§hl" cx="302" cy="172" rx="34" ry="18"/>'
          '<ellipse id="§hl1" class="§hlon" cx="98" cy="172" rx="34" ry="18" stroke="none"/>'
          '<ellipse id="§hl2" class="§hlon" cx="302" cy="172" rx="34" ry="18" stroke="none"/></svg></div>'
          '<div id="§flare"></div>')
    hud = (title("t7y", [(odo("yr", "2026"), 230)], 290, 120, "color:#FB8000")
           + title("t7", ["LA VOITURE", "VIENT À TOI"], 280, 124))
    js = """
      tl.fromTo($("mid"), { strokeDashoffset: 0 }, { strokeDashoffset: -86 * Math.round(DUR * 2.5), duration: DUR, ease: "none" }, 0);
      slam("t7y-0", at("2026") - 0.04, { s: 1.3 }); odo("yr", at("2026") - 0.04, 0.8, { from: "2010" });
      // finding cars: the search finds nothing
      pre("mag", { opacity: 0, scale: 0.6 }); go("mag", { opacity: 1, scale: 1 }, at("trouver") - 0.06, 0.25, "back.out(2)");
      go("mag", { x: -200 }, at("trouver") + 0.12, 0.42, "sine.inOut"); go("mag", { x: 190 }, at("trouver") + 0.56, 0.5, "sine.inOut");
      go("mag", { x: 0, y: 30, rotation: -14, opacity: 0.35 }, at("dur") - 0.04, 0.3, "power2.out"); shake("shk", at("dur"), 10);
      // the trade-in: a car that drives to you
      go("t7y", { opacity: 0, y: -30 }, at("la") - 0.12, 0.13, "power2.in"); go("mag", { opacity: 0 }, at("la") - 0.1, 0.2);
      slam("t7-0", at("la")); slam("t7-1", at("vient")); stroke("t7", at("toi") - 0.05);
      pre("carf", { opacity: 0, scale: 0.06, y: -560 }); go("carf", { opacity: 1 }, at("reprise") - 0.08, 0.2);
      go("carf", { scale: 1, y: 0 }, at("reprise") - 0.08, at("toi") + 0.1 - (at("reprise") - 0.08), "power2.in");
      pre("hl1", { opacity: 0 }); pre("hl2", { opacity: 0 });
      go("hl1", { opacity: 1 }, at("voiture") - 0.05, 0.25); go("hl2", { opacity: 1 }, at("voiture") - 0.05, 0.25);
      pre("flare", { opacity: 0, scale: 0.6 }); go("flare", { opacity: 1, scale: 1.35 }, at("toi") + 0.05, 0.14, "power2.out");
      go("flare", { opacity: 0.55, scale: 1.1 }, at("toi") + 0.19, 0.6, "power2.inOut");
      init("carf", { opacity: 1, scale: 1, y: 0 }); go("carf", { scale: 1.06 }, at("toi") + 0.1, 0.5, "power2.out");
      shake("shk", at("toi") + 0.08, 8);
      init("vp", { opacity: 1 }); go("vp", { opacity: 0.3 }, at("toi"), 0.6);
    """
    sfx = [("typing", "2026", 1, -.04, .12), ("whoosh-short", "trouver", 1, .1, .14), ("whoosh-short", "trouver", 1, .55, .14),
           ("click", "dur", 1, 0, .25), ("pop", "la", 1, 0, .14), ("whoosh-cinematic", "reprise", 1, 0, .3),
           ("impact-bass-2", "toi", 1, .08, .3)]
    return css, st, hud, js, (540, 700), sfx


def scene_08():
    css = """
    #§handle { position: absolute; left: 60px; top: 330px; width: 960px; text-align: center; white-space: nowrap; }
    #§hname { position: relative; display: inline-block; font: 96px/1.2 "Anton", sans-serif; color: #ffffff; opacity: 0; }
    #§pill { position: absolute; left: 50%; top: 175px; transform: translateX(-50%); }
    #§pilli { display: inline-block; padding: 8px 40px; border-radius: 40px; background: #FB8000; color: #0A0A0A; font: 52px/1.25 "Anton", sans-serif; opacity: 0;
      box-shadow: 0 0 46px rgba(251,128,0,0.45); }
    """
    st = stage(car2=True)
    hud = (title("t8", ["PRENDS CELUI QUI", "A UNE REPRISE."], 285, 108)
           + '<div id="§handle"><span id="§hname">@guillaumeherbin_<i class="§stilt"><i class="§stk" id="§h-s"></i></i></span>'
             '<div id="§pill"><span id="§pilli">S’ABONNER</span></div></div>')
    js = """
      ["pa", "pb"].forEach(function (p) { init(p + "-w", { opacity: 1 }); init(p + "-o", { opacity: 0 }); init(p + "-glow", { opacity: 0 }); });
      tl.set([$("pa-w"), $("pb-w")], { opacity: 1 }, 0);
      pre("car", { opacity: 0 }); slam("car", 0.02, { s: 1.25 });
      pre("pa", { opacity: 0, y: 50 }); pre("pb", { opacity: 0, y: 50 });
      go("pa", { opacity: 1, y: 0 }, at("deux") - 0.06, 0.26, "back.out(1.6)"); go("pb", { opacity: 1, y: 0 }, at("deux") + 0.04, 0.26, "back.out(1.6)");
      cam(0, -10, 1.03, 0, 0.6, "power2.out");
      // the one with a trade-in lights up
      lit("pb", "orange", at("prends") - 0.05, 0.35); lit("pa", "dim", at("prends") - 0.05, 0.35);
      pre("car2", { opacity: 0, x: 160 }); go("car2", { opacity: 1, x: 0 }, at("une") - 0.06, 0.4, "power3.out");
      slam("t8-0", at("prends")); slam("t8-1", at("une")); stroke("t8", at("reprise") + 0.05);
      cam(-120, -10, 1.08, at("prends") - 0.05, 0.6);
      init("pb-glow", { scale: 1 }); go("pb-glow", { scale: 1.25 }, at("reprise"), 0.25, "power2.out"); go("pb-glow", { scale: 1 }, at("reprise") + 0.25, 0.4);
      // subscribe
      go("t8", { opacity: 0, y: -40 }, at("abonne-toi") - 0.14, 0.15, "power2.in");
      slam("hname", at("abonne-toi"), { s: 1.3 }); stroke("h", at("abonne-toi") + 0.18);
      pre("pilli", { opacity: 0, scale: 0.5 }); go("pilli", { opacity: 1, scale: 1 }, at("pour") - 0.04, 0.3, "back.out(2)");
      init("pilli", { opacity: 1, scale: 1 }); go("pilli", { scale: 1.08 }, at("comme"), 0.15); go("pilli", { scale: 1 }, at("comme") + 0.15, 0.3);
      cam(-60, 10, 1.03, at("abonne-toi") - 0.1, 0.8);
      init("halo", { scale: 1 }); go("halo", { scale: 1.2 }, at("abonne-toi"), 1.2, "sine.inOut");
    """
    sfx = [("pop", None, 0, 0.02, .14), ("pop", "deux", 1, -.06, .12), ("sparkle", "prends", 1, -.05, .22),
           ("whoosh-short", "une", 1, -.06, .14), ("pop", "reprise", 1, .05, .14), ("notification", "abonne-toi", 1, 0, .25),
           ("pop", "pour", 1, -.04, .14)]
    return css, st, hud, js, (860, 820), sfx


BUILDERS = [scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07, scene_08]


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
message: "Entre deux acheteurs au même prix, prends celui qui a une reprise : deux ventes, deux marges, une reprise payée par la vente et pas par la banque, à condition de l'estimer comme un achat."
arc: Hook → Problem → Turn → Demo → Payoff → Warning → Bonus → CTA
audience: "Marchands automobiles qui achètent et revendent des véhicules d'occasion"
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
- **Negative list** : aucun billet, aucune liasse, aucune espèce ; jamais plus de 6 mots par bloc de texte.

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
