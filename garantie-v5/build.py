#!/usr/bin/env python3
"""Reel « Ne vends pas. Montre. » : one source for the whole film.

Every animation of every scene is placed on a WORD of the voice (at("virement"), at("même", 2)...), never on a fixed
second. The word timings come from one file:
  - assets/audio/voix-montage-mots.json when the real voice is there (align.py writes it), or
  - a provisional timing spread over the brief's windows (0-3, 3-10, 10-14, 14-24, 24-32, 32-42, 42-49, 49-53, 53-57 s).
So when the final voice arrives (or changes), run: python3 align.py && python3 build.py && bash assemble.sh
and every scene, cut, subtitle and sound effect lands back on the voice.

Usage: python3 build.py [--provisional]
Writes: compositions/frames/*.html, STORYBOARD.md, timings.json, assets/audio/sfx-events.json
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
REAL = "assets/audio/voix-montage-mots.json"
TAIL = 1.0          # hold after the last word: a clean end on « tu as ta réponse »
FPS = 30

# ---------------------------------------------------------------------------------------------------------------------
# The voice, scene by scene, cut into subtitle chunks (2 to 5 words). *word* = key word (orange). ~ glues two tokens
# into one subtitle word (« 10~000 », « voitures~? »). Numbers are spoken « dix mille », « deux mille vingt-six ».
SCENES = [
 dict(id="01-hook", name="Hook (la cover dès l'image 0)", window=(0, 6), chunks=[
   "∅L'extension de garantie~:", "∅arnaque,", "∅ou vrai bon plan~?", "J'en vends", "depuis *seize~ans*.", "Réponse avec",
   "*deux~clients*."]),
 dict(id="02-principe", name="C'est quoi", window=(6, 14), chunks=[
   "Le *principe*~:", "quand tu achètes", "une voiture d'occasion,", "tu peux payer", "un *supplément*",
   "pour que les grosses *pannes*", "ne soient plus pour toi."]),
 dict(id="03-non", name="Celui qui a dit non", window=(14, 25), chunks=[
   "Le premier", "me dit *non~merci*.", "*Huit~mois* plus tard,", "sa boîte de vitesses *lâche*.", "Il a dit non",
   "pour *49~euros* par mois.", "Il a payé", "*6~700~euros*."]),
 dict(id="04-oui", name="Celui qui a dit oui", window=(25, 34), chunks=[
   "Le deuxième", "dit *oui*.", "Un jour,", "son *turbo* casse~:", "*2~500~euros*.", "Lui, il a payé", "*zéro*.",
   "La garantie", "a réglé le garage."]),
 dict(id="05-face", name="Le face à face", window=(34, 39), chunks=[
   "Donc toujours", "un bon plan~?", "*Non*.", "Tout dépend", "de *quatre~lignes*", "du contrat."]),
 dict(id="06-lignes", name="Les 4 lignes", window=(39, 57), chunks=[
   "Un~: le *plafond*.", "Le maximum", "que la garantie paie", "par panne.", "Deux~: la *vétusté*.", "Plus ta voiture",
   "a de kilomètres,", "moins la pièce", "est remboursée.", "Trois~:", "le *remboursement*.", "La garantie paie le garage,",
   "ou c'est toi", "qui avances l'argent~?", "Quatre~:", "les *exclusions*.", "Tout ce qui", "n'est pas couvert."]),
 dict(id="07-chute", name="La chute", window=(57, 66), chunks=[
   "Demande au vendeur", "de te montrer", "ces *quatre~lignes*.", "S'il te les *montre*,", "tu sais", "ce que tu achètes.",
   "S'il *bafouille*,", "tu as ta *réponse*."]),
]
SPOKEN_SYL = {"seizeans": 3, "deuxclients": 3, "nonmerci": 3, "huitmois": 2, "49euros": 5, "6700euros": 7, "2500euros": 7,
              "quatrelignes": 3, "zéro": 2}
HIDE = "∅"         # a chunk starting with ∅ is not shown as a subtitle (the cover already says it on the first frames)
RED = "#B3261E"   # dark red of the project: the gearbox crack only



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
# the 7 scenes: (css, stage html [moves with the camera], hud html [titles, cards], js, halo position, sfx)

def band():
    """the « EXTENSION DE GARANTIE » band: same place as on the cover, on screen for the whole video"""
    return '<div id="§band" class="§band"><span>EXTENSION DE GARANTIE</span></div>'


BAND_CSS = """
    .§band { position: absolute; left: 0; top: 262px; width: 1080px; text-align: center; }
    .§band span { display: inline-block; padding: 8px 34px; border-radius: 40px; background: #FB8000; color: #0A0A0A;
      font: 54px/1.2 "Anton", sans-serif; letter-spacing: 0.02em; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
"""

# the two columns of scenes 3 to 5: « il a dit non » on the left (grey), « il a dit oui » on the right (orange)
COL_CSS = BAND_CSS + """
    .§col { position: absolute; top: 380px; width: 480px; height: 870px; border-radius: 28px; background: #121212; border: 3px solid #262626; }
    .§colh { position: absolute; top: 410px; width: 480px; text-align: center; font: 64px/1 "Anton", sans-serif; }
    .§cnl { position: absolute; top: 1066px; width: 480px; text-align: center; font: 600 28px/1 "Instrument Sans", sans-serif; color: #8c8c8c; letter-spacing: 0.08em; }
    .§cnv { position: absolute; top: 1108px; width: 480px; text-align: center; font: 112px/1.15 "Anton", sans-serif; color: #ffffff; transform-origin: 50% 50%; }
"""


def columns(left_val="0 000 €", right_html="? €"):
    return (f'<div id="§cl" class="§col" style="left:40px"></div><div id="§cr" class="§col" style="left:560px"></div>'
            f'<div id="§hl" class="§colh" style="left:40px;color:#bdbdbd">IL A DIT NON</div>'
            f'<div id="§hr" class="§colh" style="left:560px;color:#FB8000">IL A DIT OUI</div>'
            + person("pn", 195, 490, 170) + person("py", 715, 490, 170)
            + '<div id="§nl" class="§cnl" style="left:40px">CE QU’IL A PAYÉ</div><div id="§nr" class="§cnl" style="left:560px">CE QU’IL A PAYÉ</div>'
            f'<div id="§vl" class="§cnv" style="left:40px;color:#FB8000">{odo("ln", "6 700 €")}</div>'
            f'<div id="§vr" class="§cnv" style="left:560px">{right_html}</div>')


COL_JS = """
      // the two clients: the grey one said no, the orange one said yes
      init("pn-w", { opacity: 0 }); init("pn-o", { opacity: 0 }); init("pn-glow", { opacity: 0 });
      init("py-w", { opacity: 0 }); init("py-o", { opacity: 0 }); init("py-glow", { opacity: 0 });
      tl.set($("py-o"), { opacity: 1 }, 0); init("py-o", { opacity: 1 });
      function side(s, t) {     // light one column, dim the other
        var L = s === "l", d = 0.35;
        go("cl", { opacity: L ? 1 : 0.35 }, t, d); go("hl", { opacity: L ? 1 : 0.35 }, t, d); go("pn", { opacity: L ? 1 : 0.3 }, t, d);
        go("cr", { opacity: L ? 0.35 : 1 }, t, d); go("hr", { opacity: L ? 0.35 : 1 }, t, d); go("py", { opacity: L ? 0.3 : 1 }, t, d);
        tl.to($(L ? "cl" : "cr"), { borderColor: L ? "#9a9a9a" : "#FB8000", duration: d }, t);
        tl.to($(L ? "cr" : "cl"), { borderColor: "#262626", duration: d }, t);
      }
"""


def scene_01():
    css = BAND_CSS + """
    #§cov { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 540px 700px; }
    #§cov img { width: 1080px; height: 1920px; display: block; }
    #§twins { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    """
    # the cover, exactly: frame 0 of the film is this image
    st = '<div id="§cov"><img src="assets/img/cover.png"></div>'
    hud = (band() + title("t1", ["J’EN VENDS", '<span style="color:#FB8000">DEPUIS 16 ANS.</span>'], 560, 150)
           + title("t2", ["RÉPONSE AVEC", '<span style="color:#FB8000">2 CLIENTS.</span>'], 560, 150))
    js = """
      // frame 0 = the cover (text already there, no fade); then a slow push-in
      tl.set($("cov"), { opacity: 1, scale: 1 }, 0); init("cov", { opacity: 1, scale: 1 });
      go("cov", { scale: 1.04 }, 0.05, Math.max(0.6, at("j'en") - 0.2), "none");
      pre("band", { opacity: 0 });
      // « 16 years »: the cover steps back, the band stays
      go("band", { opacity: 1 }, at("j'en") - 0.12, 0.01, "none");
      go("cov", { opacity: 0, scale: 1.08 }, at("j'en") - 0.12, 0.3, "power2.out");
      slam("t1-0", at("j'en") - 0.05); slam("t1-1", at("seizeans") - 0.05); stroke("t1", at("seizeans") + 0.15);
      go("t1", { opacity: 0, y: -30 }, at("réponse") - 0.15, 0.14, "power2.in");
      slam("t2-0", at("réponse") - 0.03); slam("t2-1", at("deuxclients") - 0.05); stroke("t2", at("deuxclients") + 0.15);
    """
    sfx = [("pop", "j'en", 1, -.05, .14), ("pop", "réponse", 1, -.04, .14)]
    return css, st, hud, js, (540, 900), sfx


def scene_02():
    css = BAND_CSS + """
    #§tag { position: absolute; left: 600px; top: 650px; transform-origin: 30px 0; opacity: 0; }
    #§tag b { display: block; margin-top: 70px; padding: 10px 26px; border-radius: 14px; background: #FB8000; color: #0A0A0A;
      font: 56px/1.15 "Anton", sans-serif; font-weight: 400; box-shadow: 0 12px 30px rgba(0,0,0,0.5); white-space: nowrap; }
    #§tag i { position: absolute; left: 30px; top: 0; width: 4px; height: 74px; background: #bdbdbd; }
    #§warn { position: absolute; left: 470px; top: 610px; width: 140px; height: 124px; opacity: 0; }
    .§btn { position: absolute; top: 1080px; width: 360px; height: 140px; border-radius: 70px; text-align: center; font: 90px/140px "Anton", sans-serif; opacity: 0; }
    """
    st = car("car", 220, 760, 640, "#ffffff", 9) + ('<svg id="§warn" viewBox="0 0 140 124"><path d="M70 6 L134 118 L6 118 Z" fill="#FB8000"/>'
                                                    '<path d="M70 44 L70 82 M70 98 L70 102" stroke="#0A0A0A" stroke-width="12" stroke-linecap="round"/></svg>')
    hud = (band() + title("t1", ["LE PRINCIPE"], 420, 130)
           + '<div id="§tag"><i></i><b>EN OPTION</b></div>'
           + '<div id="§by" class="§btn" style="left:150px;background:#FB8000;color:#0A0A0A">OUI</div>'
           + '<div id="§bn" class="§btn" style="left:570px;background:#1c1c1c;color:#bdbdbd;border:4px solid #3a3a3a">NON</div>')
    js = """
      tin = null;
      slam("t1-0", Math.max(0.02, at("principe") - 0.08)); stroke("t1", Math.max(0.2, at("principe") + 0.15));
      // a used car rolls in
      pre("car", { x: -900, opacity: 1 }); go("car", { x: 0 }, Math.max(0.1, at("achètes") - 0.2), 0.7, "power3.out");
      // the option hooks onto it
      pre("tag", { opacity: 0, rotation: -40, y: -120 }); go("tag", { opacity: 1, y: 0, rotation: 10 }, at("supplément") - 0.1, 0.35, "back.out(1.6)");
      go("tag", { rotation: -4 }, at("supplément") + 0.25, 0.4, "sine.inOut"); go("tag", { rotation: 0 }, at("supplément") + 0.65, 0.4, "sine.inOut");
      // the big breakdowns are not for you any more
      pre("warn", { opacity: 0, scale: 0.3 }); go("warn", { opacity: 1, scale: 1 }, at("pannes") - 0.1, 0.25, "back.out(2)"); shake("car", at("pannes"), 10);
      go("warn", { opacity: 0, scale: 0.6 }, at("toi") - 0.15, 0.2);
      // yes or no
      pre("by", { opacity: 0, y: 40 }); go("by", { opacity: 1, y: 0 }, at("toi") - 0.1, 0.25, "back.out(1.8)");
      pre("bn", { opacity: 0, y: 40 }); go("bn", { opacity: 1, y: 0 }, at("toi") + 0.05, 0.25, "back.out(1.8)");
    """.replace("tin = null;\n", "")
    sfx = [("whoosh-short", "achètes", 1, -.2, .14), ("pop", "supplément", 1, -.1, .16), ("click", "pannes", 1, -.1, .22),
           ("pop", "toi", 1, -.1, .14)]
    return css, st, hud, js, (540, 900), sfx


def scene_03():
    css = COL_CSS + f"""
    .§prop {{ position: absolute; opacity: 0; }}
    #§price {{ left: 95px; top: 820px; width: 370px; height: 150px; border-radius: 20px; background: #f2f2f2; color: #0A0A0A; text-align: center;
      font: 74px/150px "Anton", sans-serif; }}
    #§pstrike {{ position: absolute; left: 20px; top: 70px; width: 330px; height: 12px; border-radius: 6px; background: #FB8000; transform: scaleX(0); transform-origin: 0 50%; }}
    #§nm {{ left: 60px; top: 990px; width: 440px; text-align: center; font: 48px/1 "Anton", sans-serif; color: #8c8c8c; }}
    #§cal {{ left: 150px; top: 790px; width: 260px; height: 240px; border-radius: 24px; background: #1a1a1a; border: 3px solid #3a3a3a; overflow: hidden; }}
    #§calh {{ position: absolute; left: 0; top: 0; width: 100%; height: 50px; background: #2a2a2a; }}
    #§calv {{ position: absolute; left: 0; top: 64px; width: 100%; text-align: center; font: 110px/1 "Anton", sans-serif; color: #fff; }}
    #§calm {{ position: absolute; left: 0; top: 184px; width: 100%; text-align: center; font: 600 28px "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.1em; }}
    #§gear {{ left: 150px; top: 780px; width: 260px; height: 260px; }}
    #§over {{ position: absolute; left: 40px; top: 380px; width: 1000px; height: 660px; border-radius: 28px; background: rgba(10,10,10,0.94); opacity: 0; }}
    #§bigp {{ position: absolute; left: 0; top: 470px; width: 1080px; text-align: center; font: 120px/1 "Anton", sans-serif; color: #7a7a7a; opacity: 0; }}
    #§bigs {{ position: absolute; left: 140px; top: 530px; width: 800px; height: 16px; border-radius: 8px; background: #7a7a7a; transform: scaleX(0); transform-origin: 0 50%; }}
    #§bigv {{ position: absolute; left: 0; top: 660px; width: 1080px; text-align: center; font: 250px/1.15 "Anton", sans-serif; color: #FB8000; opacity: 0;
      text-shadow: 0 0 60px rgba(251,128,0,0.35); }}
    """
    teeth = "".join(f'<rect x="118" y="6" width="24" height="40" rx="5" transform="rotate({k * 45} 130 130)"/>' for k in range(8))
    gear = (f'<svg id="§gear" class="§prop" viewBox="0 0 260 260"><g fill="#6f6f6f">{teeth}<circle cx="130" cy="130" r="92"/></g>'
            f'<circle cx="130" cy="130" r="34" fill="#121212"/>'
            f'<path id="§crack" d="M150 46 L128 98 L152 120 L118 170 L140 196 L116 226" fill="none" stroke="{RED}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    st = columns()
    hud = (band() + '<div id="§price" class="§prop">49 € / MOIS<i id="§pstrike"></i></div><div id="§nm" class="§prop">NON MERCI</div>'
           + '<div id="§cal" class="§prop"><div id="§calh"></div><div id="§calv">+' + odo("mo", "8") + '</div><div id="§calm">MOIS</div></div>'
           + gear + '<div id="§over"></div><div id="§bigp">49 € PAR MOIS</div><div id="§bigs"></div>'
           + '<div id="§bigv">' + odo("bv", "6 700 €") + '</div>')
    js = COL_JS + """
      // the columns appear, the left one lights up
      ["cl", "cr", "hl", "hr", "pn", "py", "nl", "nr", "vl", "vr"].forEach(function (id, k) { pre(id, { opacity: 0, y: 30 }); go(id, { opacity: 1, y: 0 }, 0.02 + k * 0.03, 0.3); });
      side("l", Math.max(0.3, at("premier") - 0.05));
      odo("ln", 0, 0.01, { from: "0 000", to: "0000", spinLow: false, dimLead: true });
      // 49 € a month: no thanks
      pre("price", { opacity: 0, scale: 0.6 }); go("price", { opacity: 1, scale: 1 }, at("nonmerci") - 0.15, 0.25, "back.out(2)");
      tl.fromTo($("pstrike"), { scaleX: 0 }, { scaleX: 1, duration: 0.2, ease: "power3.out", immediateRender: false }, at("nonmerci") + 0.15);
      pre("nm", { opacity: 0 }); slam("nm", at("nonmerci") + 0.2, { s: 1.3 });
      // eight months later
      go("price", { opacity: 0 }, at("huitmois") - 0.15, 0.15); go("nm", { opacity: 0 }, at("huitmois") - 0.15, 0.15);
      pre("cal", { opacity: 0, y: 40 }); go("cal", { opacity: 1, y: 0 }, at("huitmois") - 0.12, 0.25, "back.out(1.5)");
      odo("mo", at("huitmois") - 0.05, Math.max(0.6, at("lâche") - 0.2 - at("huitmois")), { from: "0" });
      // the gearbox gives up
      go("cal", { opacity: 0 }, at("lâche") - 0.35, 0.15);
      pre("gear", { opacity: 0, scale: 0.7 }); go("gear", { opacity: 1, scale: 1 }, at("lâche") - 0.3, 0.2, "back.out(1.8)");
      draw("crack", at("lâche") - 0.05, 0.25, "power2.in"); shake("gear", at("lâche") + 0.2, 12);
      // the last picture: 49 € a month, crossed out, over 6 700 €
      go("over", { opacity: 1 }, at("49euros") - 0.25, 0.25, "none");
      pre("bigp", { opacity: 0 }); slam("bigp", at("49euros") - 0.1, { s: 1.2 });
      tl.fromTo($("bigs"), { scaleX: 0 }, { scaleX: 1, duration: 0.25, ease: "power3.out", immediateRender: false }, atEnd("mois") + 0.05);
      pre("bigv", { opacity: 0 }); slam("bigv", at("6700euros") - 0.08, { s: 1.4 });
      odo("bv", 0, 0.01, { from: "0 000", to: "0000", spinLow: false }); odo("bv", at("6700euros") - 0.05, 0.9);
      odo("ln", at("6700euros") - 0.05, 0.9);
      shake("bigv", at("6700euros") + 0.9, 10);
    """
    sfx = [("pop", "nonmerci", 1, -.15, .16), ("click", "nonmerci", 1, .15, .2), ("whoosh-short", "huitmois", 1, -.15, .14),
           ("impact-bass-1", "lâche", 1, -.05, .3), ("typing", "6700euros", 1, -.05, .12)]
    return css, st, hud, js, (300, 900), sfx


def scene_04():
    css = COL_CSS + """
    #§paper { position: absolute; left: 100px; top: 300px; width: 880px; height: 920px; border-radius: 10px; background: #f7f5f1;
      box-shadow: 0 40px 90px rgba(0,0,0,0.7); color: #141414; font-family: "Instrument Sans", sans-serif; overflow: hidden; transform-origin: 440px 0; }
    .§pa { position: absolute; }
    .§blur { position: absolute; height: 26px; border-radius: 6px; background: #b8b4ad; filter: blur(5px); }
    .§lab { font: 600 26px/1 "Instrument Sans", sans-serif; color: #8a857c; text-transform: uppercase; letter-spacing: 0.05em; }
    .§row { position: absolute; left: 50px; width: 780px; height: 64px; }
    .§rowt { position: absolute; left: 16px; top: 0; font: 600 34px/64px "Instrument Sans", sans-serif; }
    .§rowv { position: absolute; right: 16px; top: 0; font: 40px/64px "Anton", sans-serif; }
    .§hlr { position: absolute; left: 0; top: 0; width: 100%; height: 100%; border-radius: 10px; background: rgba(251,128,0,0.22);
      border-left: 8px solid #FB8000; transform-origin: 0 50%; transform: scaleX(0); }
    #§x25 { position: absolute; left: 470px; top: 512px; width: 330px; height: 9px; border-radius: 5px; background: #141414; transform: scaleX(0); transform-origin: 0 50%; }
    #§stamp { position: absolute; left: 470px; top: 760px; padding: 6px 30px; border: 8px solid #FB8000; border-radius: 16px;
      font: 84px/1.1 "Anton", sans-serif; color: #FB8000; transform: rotate(-10deg); opacity: 0; }
    """
    rows = [("r1", 330, "Turbo (remplacement)", "1 980,00 €", ""), ("r2", 400, "Main-d’œuvre", "520,00 €", ""),
            ("r3", 480, "TOTAL TTC", None, "font-weight:700"), ("r4", 556, "Garantie mécanique", "− 2 500,00 €", ""),
            ("r5", 650, "RESTE À CHARGE", None, "")]
    rh = ""
    for rid, y, t, v, sty in rows:
        big = rid == "r5"
        val = (odo("tot", "2 500,00 €") if rid == "r3" else odo("rac", "0,00 €") if big else v)
        fs = ' style="font-size:46px"' if big else ""
        rh += (f'<div class="§row" style="top:{y}px{";height:80px" if big else ""}"><div id="§{rid}-hl" class="§hlr"></div>'
               f'<div class="§rowt" style="{sty}{";font:52px/80px Anton,sans-serif" if big else ""}">{t}</div>'
               f'<div class="§rowv"{fs if not big else " style=font-size:60px;line-height:80px"}>{val}</div></div>')
    paper = ('<div id="§paper">'
             '<div class="§pa" style="left:50px;top:40px;font:72px/1 Anton,sans-serif">FACTURE</div>'
             '<div class="§pa §lab" style="left:560px;top:52px">N°</div><div class="§blur" style="left:610px;top:48px;width:200px"></div>'
             '<div class="§blur" style="left:50px;top:140px;width:300px"></div><div class="§blur" style="left:50px;top:182px;width:220px"></div>'
             '<div class="§pa §lab" style="left:480px;top:140px">Client</div><div class="§blur" style="left:600px;top:136px;width:220px"></div>'
             '<div class="§pa §lab" style="left:480px;top:186px">Immat.</div><div class="§blur" style="left:600px;top:182px;width:170px"></div>'
             '<div class="§pa" style="left:50px;top:250px;width:780px;height:2px;background:#d8d3ca"></div>'
             '<div class="§pa §lab" style="left:66px;top:282px">Désignation</div><div class="§pa §lab" style="right:66px;top:282px">Montant</div>'
             + rh + '<div id="§x25"></div><div id="§stamp">RÉGLÉ</div></div>')
    st = columns(right_html=odo("rn", "0 €"))
    hud = band() + paper
    js = COL_JS + """
      // where scene 3 left them: the left counter shows 6 700 €
      odo("ln", 0, 0.01, { from: "6 700", spinLow: false });
      odo("rn", 0, 0.01, { from: "0", spinLow: false }); pre("vr", { opacity: 0.25 });
      side("l", 0); side("r", Math.max(0.05, at("deuxième") - 0.1));
      go("py-glow", { opacity: 1 }, at("oui") - 0.05, 0.3); shake("py", at("oui"), 8);
      // the real invoice (blurred): the turbo, 2 500 €, then nothing left to pay
      pre("paper", { opacity: 0, y: 120, scale: 0.62, rotation: -4 });
      go("paper", { opacity: 1, y: 140, scale: 0.62, rotation: -1.5 }, at("turbo") - 0.2, 0.4, "expo.out");
      odo("tot", 0, 0.01, { from: "0 000,00", to: "000000", spinLow: false });
      tl.fromTo($("r1-hl"), { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, at("turbo") + 0.1);
      tl.fromTo($("r3-hl"), { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, at("2500euros") - 0.06);
      odo("tot", at("2500euros") - 0.06, 0.9);
      tl.fromTo($("x25"), { scaleX: 0 }, { scaleX: 1, duration: 0.25, ease: "power3.out", immediateRender: false }, at("2500euros") + 0.9);
      tl.fromTo($("r5-hl"), { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, at("lui") - 0.05);
      pre("rac", { opacity: 0 }); slam("rac", at("zéro") - 0.06, { s: 1.4 }); odo("rac", at("zéro") - 0.06, 0.5, { from: "0,00" });
      // his counter: 0 €
      go("vr", { opacity: 1 }, at("zéro") - 0.06, 0.2); tl.fromTo($("vr"), { color: "#ffffff", scale: 1.3 }, { color: "#FB8000", scale: 1, duration: 0.4, immediateRender: false }, at("zéro") - 0.06);
      pre("stamp", { opacity: 0, scale: 2.4, rotation: -10 }); go("stamp", { opacity: 1, scale: 1, rotation: -10 }, at("réglé") - 0.08, 0.16, "expo.in");
      shake("paper", at("réglé") + 0.08, 6);
    """
    sfx = [("pop", "oui", 1, -.05, .16), ("whoosh-short", "turbo", 1, -.2, .14), ("typing", "2500euros", 1, -.06, .12),
           ("chime", "zéro", 1, .05, .18), ("impact-bass-2", "réglé", 1, -.04, .28)]
    return css, st, hud, js, (780, 900), sfx


def scene_05():
    css = COL_CSS
    st = columns(right_html=odo("rn", "0 €"))
    hud = (band() + title("t1", ["TOUJOURS UN", "BON PLAN ?"], 370, 110) + title("t2", ['<span style="color:#FB8000">NON.</span>'], 430, 220)
           + title("t3", ["ÇA DÉPEND", "DU CONTRAT."], 1000, 110))
    js = COL_JS + """
      odo("ln", 0, 0.01, { from: "6 700", spinLow: false }); odo("rn", 0, 0.01, { from: "0", spinLow: false });
      tl.set($("vr"), { color: "#FB8000" }, 0);
      // face to face: only the two counters, very big
      ["cl", "cr", "hl", "hr", "pn", "py", "nl", "nr"].forEach(function (id) { go(id, { opacity: 0 }, 0.05, 0.3); });
      go("vl", { y: -300, scale: 1.55 }, 0.1, 0.5, "power3.inOut"); go("vr", { y: -300, scale: 1.55 }, 0.1, 0.5, "power3.inOut");
      slam("t1-0", Math.max(0.3, at("toujours") - 0.1)); slam("t1-1", at("plan") - 0.05); stroke("t1", at("plan") + 0.15);
      go("t1", { opacity: 0 }, at("non") - 0.12, 0.1);
      slam("t2-0", at("non") - 0.05, { s: 1.5 }); shake("t2", at("non") + 0.15, 14);
      go("t2", { opacity: 0 }, at("dépend") - 0.15, 0.12);
      slam("t3-0", at("dépend") - 0.05); slam("t3-1", at("contrat") - 0.05); stroke("t3", at("contrat") + 0.15);
    """
    sfx = [("impact-bass-1", "non", 1, -.05, .3), ("pop", "dépend", 1, -.05, .14)]
    return css, st, hud, js, (540, 900), sfx


LIGNES = [("1.", "LE PLAFOND", "le maximum payé par panne", "un", "Plafond de prise en charge par panne"),
          ("2.", "LA VÉTUSTÉ", "plus de kilomètres, moins de remboursement", "deux", "Vétusté selon le kilométrage"),
          ("3.", "LE REMBOURSEMENT", "qui avance l’argent ?", "trois", "Modalités de remboursement"),
          ("4.", "LES EXCLUSIONS", "ce qui n’est pas couvert", "quatre", "Exclusions de garantie")]


def scene_06():
    css = BAND_CSS + """
    #§doc { position: absolute; left: 90px; top: 370px; width: 900px; height: 560px; border-radius: 10px; background: #f7f5f1;
      box-shadow: 0 40px 90px rgba(0,0,0,0.7); color: #141414; overflow: hidden; }
    .§pa { position: absolute; }
    .§blur { position: absolute; height: 22px; border-radius: 6px; background: #b8b4ad; filter: blur(5px); }
    .§fill { position: absolute; left: 50px; height: 14px; border-radius: 7px; background: #dcd8d0; }
    .§ln { position: absolute; left: 40px; width: 820px; height: 62px; border-radius: 10px; }
    .§lnh { position: absolute; left: 0; top: 0; width: 100%; height: 100%; border-radius: 10px; background: rgba(251,128,0,0.25);
      border-left: 8px solid #FB8000; transform-origin: 0 50%; transform: scaleX(0); }
    .§lnt { position: absolute; left: 22px; top: 0; font: 600 32px/62px "Instrument Sans", sans-serif; color: #2a2a2a; }
    .§kw { position: absolute; left: 0; top: 980px; width: 1080px; text-align: center; opacity: 0; }
    .§kwt { display: block; font: 100px/1.1 "Anton", sans-serif; color: #fff; white-space: nowrap; }
    .§kwt b { color: #FB8000; font-weight: 400; }
    .§kws { display: block; margin-top: 10px; font: 600 44px/1.2 "Instrument Sans", sans-serif; color: #9a9a9a; }
    """
    lines = ""
    for k, (n, kw, sub, cue, txt) in enumerate(LIGNES):
        y = 150 + k * 96
        lines += (f'<div class="§ln" style="top:{y}px"><div id="§h{k}" class="§lnh"></div><div class="§lnt">{n} {txt}</div></div>'
                  f'<div class="§fill" style="top:{y + 72}px;width:{560 - k * 60}px"></div>')
    doc = ('<div id="§doc"><div class="§pa" style="left:50px;top:40px;font:64px/1 Anton,sans-serif">CONTRAT DE GARANTIE</div>'
           '<div class="§blur" style="left:620px;top:52px;width:220px"></div>' + lines + '</div>')
    hud = band() + doc + "".join(f'<div id="§k{k}" class="§kw"><span class="§kwt"><b>{n}</b> {kw}</span><span class="§kws">{sub}</span></div>'
                                 for k, (n, kw, sub, cue, txt) in enumerate(LIGNES))
    js = """
      pre("doc", { opacity: 0, y: 100, rotation: -3 }); go("doc", { opacity: 1, y: 0, rotation: -1 }, 0.0, 0.35, "expo.out");"""
    for k, (n, kw, sub, cue, txt) in enumerate(LIGNES):
        js += f"""
      // line {k + 1}
      tl.fromTo($("h{k}"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out", immediateRender: false }}, at("{cue}") - 0.05);
      pre("k{k}", {{ opacity: 0, y: 30 }}); go("k{k}", {{ opacity: 1, y: 0 }}, at("{cue}") - 0.05, 0.25, "back.out(1.6)");"""
        if k < 3:
            js += f"""
      go("k{k}", {{ opacity: 0, y: -20 }}, at("{LIGNES[k + 1][3]}") - 0.2, 0.15);"""
    sfx = [("click-soft", c, 1, -.05, .25) for _, _, _, c, _ in LIGNES]
    return css, "", hud, js, (540, 1000), sfx


def scene_07():
    css = BAND_CSS + """
    .§pl4 { position: absolute; top: 0; padding: 6px 22px; border-radius: 30px; border: 3px solid #FB8000; color: #FB8000;
      font: 46px/1.2 "Anton", sans-serif; white-space: nowrap; opacity: 0; }
    #§pills { position: absolute; left: 0; top: 400px; width: 1080px; height: 140px; }
    .§out { position: absolute; left: 0; width: 1080px; text-align: center; font: 96px/1.1 "Anton", sans-serif; opacity: 0; white-space: nowrap; }
    #§hn { position: absolute; left: 0; top: 1205px; width: 1080px; text-align: center; font: 600 48px/1 "Instrument Sans", sans-serif; color: #FB8000; opacity: 0; }
    """
    pills = [("PLAFOND", 120, 0), ("VÉTUSTÉ", 560, 0), ("REMBOURSEMENT", 120, 80), ("EXCLUSIONS", 560, 80)]
    hud = (band() + '<div id="§pills">' + "".join(f'<span id="§q{k}" class="§pl4" style="left:{x}px;top:{y}px">{t}</span>' for k, (t, x, y) in enumerate(pills))
           + '</div>' + title("t1", ["DEMANDE-LES."], 600, 120)
           + '<div id="§o1" class="§out" style="top:620px;color:#FB8000">✓ IL TE LES MONTRE</div>'
           + '<div id="§o2" class="§out" style="top:780px;color:#7a7a7a">… IL BAFOUILLE</div>'
           + title("t2", ["TU AS TA", "RÉPONSE."], 850, 140) + '<div id="§hn">@guillaumeherbin_</div>')
    js = """
      for (var k = 0; k < 4; k++) { pre("q" + k, { opacity: 0, y: 20 }); go("q" + k, { opacity: 1, y: 0 }, 0.02 + k * 0.08, 0.25, "back.out(1.6)"); }
      slam("t1-0", Math.max(0.3, at("montrer") - 0.1)); stroke("t1", at("quatrelignes") + 0.1);
      go("t1", { opacity: 0 }, at("montre") - 0.25, 0.12);
      pre("o1", { opacity: 0, x: -60 }); go("o1", { opacity: 1, x: 0 }, at("montre") - 0.1, 0.25, "back.out(1.6)");
      pre("o2", { opacity: 0, x: 60 }); go("o2", { opacity: 1, x: 0 }, at("bafouille") - 0.1, 0.25, "back.out(1.6)"); wobble("o2", at("bafouille") + 0.2, 3);
      // the answer, and that's it
      go("o1", { opacity: 0.3 }, at("réponse") - 0.3, 0.2); go("o2", { opacity: 0.3 }, at("réponse") - 0.3, 0.2);
      slam("t2-0", at("tu", 2) - 0.05); slam("t2-1", at("réponse") - 0.05); stroke("t2", at("réponse") + 0.15);
      fin = null;
      go("hn", { opacity: 1 }, at("réponse") + 0.2, 0.25);
    """.replace("      fin = null;\n", "")
    sfx = [("pop", "montre", 1, -.1, .16), ("pop", "bafouille", 1, -.1, .12), ("impact-bass-2", "réponse", 1, -.05, .25)]
    return css, "", hud, js, (540, 1000), sfx


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
            if not ch.startswith(HIDE):
                cw.append([(t, W[k + m][1], W[k + m][2]) for m, t in enumerate(tt)])
            k += len(tt)
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
message: "Ne vends pas l'extension de garantie : montre trois preuves (une facture, un chiffre, une histoire), puis laisse le client choisir comment il la paie."
arc: Hook → Problem → Turn → Proof → Proof → Proof → Close → Rule → CTA
audience: "Vendeurs automobiles qui proposent l'extension de garantie"
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
- **Negative list** : aucun billet ni espèce ; jamais plus de 6 mots par bloc de texte ; rouge sombre réservé à la facture de la boîte de vitesses (scène 6).

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
