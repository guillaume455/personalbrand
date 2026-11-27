#!/usr/bin/env python3
"""Reel « Ma pire marge » (série « Je me suis fait avoir », épisode 3) : one source for the whole film.

Every animation of every scene is placed on a WORD of the voice (at("virement"), at("même", 2)...), never on a fixed
second. The word timings come from one file:
  - assets/audio/voix-montage-mots.json when the real voice is there (align.py writes it), or
  - a provisional timing spread over the brief's windows (0-3, 3-13, 13-22, 22-28, 28-40, 40-48, 48-61, 61-66 s).
So when the final voice arrives (or changes), run: python3 align.py && python3 build.py && bash assemble.sh
and every scene, cut, subtitle and sound effect lands back on the voice.

Usage: python3 build.py [--provisional]
Writes: compositions/frames/*.html, STORYBOARD.md, timings.json, assets/audio/sfx-events.json
"""
import json, os, re, shutil, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "charte"))
import charte   # colours, fonts and logo of the charte chosen by CHARTE (perso by default): charte/<name>.json

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
REAL = "assets/audio/voix-montage-mots.json"
TAIL = 0.9          # hold after the last word (end card), no long silence
FPS = 30

# ---------------------------------------------------------------------------------------------------------------------
# The voice, scene by scene, cut into subtitle chunks (2 to 5 words). *word* = key word (orange). ~ glues two tokens
# into one subtitle word (« 10~000 », « voitures~? »). Numbers are spoken « dix mille », « deux mille vingt-six ».
SCENES = [
 dict(id="01-hook", name="Hook", window=(0, 4), chunks=[
   "Tu savais qu'on peut", "vendre des voitures", "sans jamais les acheter~?", "Reste jusqu'au bout,", "je t'explique comment."]),
 dict(id="02-histoire", name="Mon histoire", window=(4, 8), chunks=[
   "C'est comme ça", "que j'ai *commencé*.", "En *2010*.", "Avec *3~000* euros", "en poche."]),
 dict(id="03-acheter", name="Acheter pour revendre", window=(8, 18), chunks=[
   "La plupart des gens", "achètent pour *revendre*.", "Une voiture", "à *13~000* euros,", "c'est 13~000 euros", "à toi",
   "qui *dorment* dedans.", "Elle tombe en *panne*~?", "C'est pour *toi*.", "Elle ne se vend pas~?", "C'est pour *toi*."]),
 dict(id="04-autre", name="Vendre sans acheter", window=(18, 28), chunks=[
   "L'autre façon~:", "tu vends *sans* acheter.", "La voiture reste", "celle de son *propriétaire*.", "Toi, tu l'*estimes*.",
   "Tu fais l'*annonce*.", "Tu trouves l'*acheteur*.", "Et tu es *payé*", "quand elle se vend."]),
 dict(id="05-face", name="Face à face", window=(28, 32), chunks=[
   "Le premier porte", "le *stock* et le *risque*.", "Toi, tu portes", "la *relation*."]),
 dict(id="06-chute", name="La chute", window=(32, 36), chunks=[
   "C'est un vrai *métier*.", "Et il se démarre", "sans *immobiliser*", "ton argent."]),
 dict(id="07-signature", name="Signature", window=(36, 39), chunks=[
   "Moi, c'est", "*Guillaume~Herbin*,", "fondateur", "du programme *FORGE*."]),
 dict(id="08-fin", name="Carton de fin", window=(39, 42), chunks=[
   "Si tu veux", "en savoir plus", "sur ce *métier*,", "*abonne-toi*."]),
]
SPOKEN_SYL = {"2010": 4, "3000": 3, "13000": 3, "guillaumeherbin": 4}
RED = "⟦ALERT⟧"   # dark red: temperature gauge and cylinder heads only

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
⟦FONT_FACES⟧    #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; color: ⟦TEXT⟧;
      font-family: ⟦FU⟧, sans-serif; -webkit-font-smoothing: antialiased; }
    .§ground { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; background: #0A0A0A; overflow: hidden; }
    .§halo { position: absolute; width: 1200px; height: 1200px; margin: -600px 0 0 -600px; border-radius: 50%;
      background: radial-gradient(closest-side, rgba(⟦HALO_RGB⟧,0.15) 0%, rgba(⟦HALO_RGB⟧,0.09) 38%, rgba(⟦HALO_RGB⟧,0.03) 70%, rgba(⟦HALO_RGB⟧,0) 100%); }
    .§grain { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0.04; mix-blend-mode: screen; pointer-events: none;
      background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='g'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%25' height='100%25' filter='url(%23g)'/></svg>");
      background-size: 240px 240px; }
    .§cam { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 540px 900px; }
    .§hudcam { transform-origin: 540px 600px; }
    .§abs { position: absolute; }

    /* title: Anton caps, white, centred (title zone y 260-640), orange stroke drawn under the last line */
    .§title { position: absolute; left: 60px; width: 960px; text-align: center; font-family: ⟦FT⟧, sans-serif; line-height: 1.2;
      text-transform: uppercase; color: ⟦TEXT⟧; white-space: nowrap; }
    .§tline { position: relative; display: inline-block; opacity: 0; }
    .§stilt { position: absolute; left: -0.078em; right: -0.078em; bottom: -0.02em; height: 0.11em; display: block;
      transform: rotate(-1.5deg); transform-origin: 0 50%; }
    .§stk { position: absolute; left: 0; top: 0; width: 100%; height: 100%; display: block; background: ⟦LINE⟧;
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
    .§pwhite { fill: ⟦TEXT⟧; opacity: 0; }
    .§porange { fill: ⟦LINE⟧; opacity: 0; }
    .§glow { position: absolute; width: 420px; height: 420px; border-radius: 50%; opacity: 0;
      background: radial-gradient(closest-side, rgba(⟦HALO_RGB⟧,0.55), rgba(⟦HALO_RGB⟧,0.18) 55%, rgba(⟦HALO_RGB⟧,0)); }
    .§car { position: absolute; transform-origin: 50% 100%; }
    .§car svg { position: absolute; left: 0; top: 0; width: 100%; height: 100%; overflow: visible; fill: none;
      stroke-linecap: round; stroke-linejoin: round; }

    /* subtitles: the voice word by word in the band y 1260-1440, the key word turns orange */
    .§sub { position: absolute; left: 0; top: 1260px; width: 1080px; height: 180px; pointer-events: none; }
    .§chunk { position: absolute; left: 40px; top: 55px; width: 1000px; text-align: center; white-space: nowrap;
      font: 700 76px/90px ⟦FU⟧, sans-serif; color: ⟦TEXT⟧; text-shadow: 0 3px 18px rgba(0,0,0,0.7); }
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
            if (w.classList.contains("sub-key")) tl.fromTo(w, { color: "⟦TEXT⟧" }, { color: "⟦LINE⟧", duration: 0.12, ease: "power3.out", immediateRender: false }, t);
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


def car(cid, x, y, w, color="⟦TEXT⟧", sw=9):
    h = w * 170 / 410
    return (f'<div id="§{cid}" class="§car" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px">'
            f'<svg viewBox="0 0 410 170" style="stroke:{color};stroke-width:{sw}">{CAR_SIDE}</svg></div>')


def stage(car2=False, extra=""):
    s = '<div class="§floor"></div>'
    if car2:
        s += car("car2", 610, 868, 300, "⟦MUTED⟧", 10)
    s += person("pa", 90, 795, 190) + person("pb", 750, 795, 190)
    s += car("car", 300, 898, 440)
    return s + extra


# ---------------------------------------------------------------------------------------------------------------------
# the 8 scenes: (css, stage html [moves with the camera], hud html [titles, cards], js, halo position)



PHOTO_CSS = """
    .§photo { position: absolute; border: ⟦PHOTO_BORDER⟧ solid ⟦LINE⟧; border-radius: 8px; overflow: hidden; box-shadow: 0 30px 70px rgba(0,0,0,0.6); }
    .§photo img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(0.72) contrast(1.04); }
"""
TOT_CSS = """
    #§tot { position: absolute; right: ⟦TOT_RIGHT⟧; top: ⟦TOT_TOP⟧; text-align: right; transform-origin: 100% 50%; }
    .§totl { font: 600 24px/1 ⟦FU⟧, sans-serif; color: ⟦MUTED⟧; letter-spacing: 0.16em; }
    .§totv { font: ⟦TOT_SIZE⟧ ⟦FT⟧, sans-serif; color: ⟦NUM⟧; margin-top: 4px; border-top: ⟦TOT_RULE⟧; padding-top: ⟦TOT_PAD⟧; }
    .§chip { position: absolute; padding: 6px 24px; border-radius: 30px; background: ⟦CHIP_BG⟧; color: #0A0A0A; border: ⟦CHIP_BORDER⟧; font: 50px/1.2 ⟦FT⟧, sans-serif;
      opacity: 0; white-space: nowrap; }
    .§chips { display: block; font: 600 24px/1 ⟦FU⟧, sans-serif; letter-spacing: 0.04em; text-align: center; margin-top: -2px; padding-bottom: 6px; }
"""
TOT_JS = """
      function totInit(v) { odo("totv", 0, 0.01, { from: v, spinLow: false }); }
      // a cost chip pops, flies into the TOTAL counter, the counter rolls up
      function bump(chip, t, to) {
        var el = $(chip), dx = 900 - (el.offsetLeft + el.offsetWidth / 2), dy = 280 - (el.offsetTop + el.offsetHeight / 2);
        pre(chip, { opacity: 0, scale: 0.5, x: 0, y: 0 });
        go(chip, { opacity: 1, scale: 1 }, t, 0.25, "back.out(2)");
        go(chip, { x: dx, y: dy, opacity: 0, scale: 0.5 }, t + 0.75, 0.42, "power3.in");
        odo("totv", t + 1.1, 0.8, { to: to });
        init("tot", { scale: 1 }); go("tot", { scale: 1.14 }, t + 1.1, 0.12); go("tot", { scale: 1 }, t + 1.22, 0.35);
      }
"""


def total(v):
    return f'<div id="§tot"><div class="§totl">TOTAL</div><div class="§totv">{odo("totv", v)}</div></div>'


def chip(cid, x, y, amount, label=""):
    lab = f'<span class="§chips">{label}</span>' if label else ""
    return f'<div id="§{cid}" class="§chip" style="left:{x}px;top:{y}px">{amount}{lab}</div>'


TRUCK = ('<path d="M440 196 L440 74 Q440 62 452 62 L522 62 L560 112 L588 122 L588 196 Z"/><path d="M456 78 L514 78 L544 114 L456 114 Z"/>'
         '<path d="M30 160 L440 160 L440 182 L30 182 Z"/><circle cx="110" cy="200" r="24"/><circle cx="370" cy="200" r="24"/>'
         '<circle cx="520" cy="200" r="24"/><g transform="translate(60 20) scale(0.86)">' + CAR_SIDE + '</g>')
ENGINE = ('<path class="§eb" d="M160 230 L440 230 L410 380 L190 380 Z"/>'
          '<path class="§eb" d="M168 236 L84 112 L190 62 L280 206 Z"/><path class="§eb" d="M432 236 L516 112 L410 62 L320 206 Z"/>'
          '<path id="§hl" class="§head" d="M84 112 L190 62 L176 32 L66 84 Z"/><path id="§hr" class="§head" d="M516 112 L410 62 L424 32 L534 84 Z"/>'
          '<path class="§eb" d="M262 150 L338 150 L338 214 L262 214 Z"/><path class="§eb" d="M240 280 L360 280 M240 320 L360 320"/>')
DISTRI = ('<g id="§distri" class="§dist"><circle cx="230" cy="330" r="30"/><circle cx="370" cy="330" r="30"/><circle cx="300" cy="402" r="34"/>'
          '<path id="§belt" d="M230 298 L370 298 A32 32 0 0 1 400 340 L328 430 A36 36 0 0 1 272 430 L200 340 A32 32 0 0 1 230 298 Z"/></g>')
MAG = '<circle cx="64" cy="64" r="44" stroke-width="12"/><path d="M98 98 L144 144" stroke-width="18"/>'


MEDIA_CSS = """
    .§burst { position: absolute; overflow: hidden; }
    .§burst img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; filter: saturate(0.72) contrast(1.04); }
    .§sprite { position: absolute; border: ⟦PHOTO_BORDER⟧ solid ⟦LINE⟧; border-radius: 8px; background-repeat: no-repeat; background-size: 600% 600%;
      box-shadow: 0 30px 70px rgba(0,0,0,0.6); filter: saturate(0.72); }
"""
MEDIA_JS = """
      // photo burst: hard cuts from one photo to the next (each shown from times[k])
      function burst(id, times, fade) {
        var imgs = $(id).querySelectorAll("img");
        for (var k = 0; k < imgs.length && k < times.length; k++) {
          tl.set(imgs[k], { opacity: 1 }, Math.max(0, times[k]));
          if (k > 0) tl.set(imgs[k - 1], { opacity: 0 }, Math.max(0, times[k]) + 0.001);
        }
      }
      // video as a sprite sheet (cols x rows frames, 12 fps), played from t for dur seconds, holding its last frame
      function sprite(id, t, dur, n, cols, fps) {
        var el = $(id), rows = Math.ceil(n / cols), step = 1 / (fps || 12), f = 0;
        for (var x = 0; x * step < dur; x++) {
          var k = Math.min(f, n - 1), cx = k % cols, cy = Math.floor(k / cols);
          tl.set(el, { backgroundPosition: (cx * 100 / (cols - 1)) + "% " + (cy * 100 / (rows - 1)) + "%" }, t + x * step);
          f++;
        }
      }
"""
ITEMS = ["POMPE À EAU", "DISTRIBUTION", "EMBRAYAGE", "JOINTS", "VIDANGE HUILE", "CALORSTAT", "DURITES", "SUPPORT MOTEUR"]
DOC = '<svg viewBox="0 0 40 48" class="§idoc"><path d="M6 3 L26 3 L35 12 L35 45 L6 45 Z M26 3 L26 12 L35 12"/></svg>'


TAG = ('<svg id="§tag" viewBox="0 0 220 120" style="position:absolute;left:640px;top:690px;width:220px;height:120px;overflow:visible">'
       '<path d="M10 60 L50 10 L210 10 L210 110 L50 110 Z" fill="#0A0A0A" stroke="⟦LINE⟧" stroke-width="6" stroke-linejoin="round"/>'
       '<circle cx="48" cy="60" r="10" fill="none" stroke="⟦LINE⟧" stroke-width="5"/>'
       '<text x="132" y="84" text-anchor="middle" font-family="Fujecka Titre" font-size="70" fill="⟦TEXT⟧">€</text></svg>')
BIG_CSS = """
    .§big { position: absolute; left: 40px; width: 1000px; text-align: center; font: 150px/1.02 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧;
      text-shadow: 0 6px 30px rgba(0,0,0,0.6); }
    .§strk { position: relative; display: inline-block; }
    .§strk i { position: absolute; left: -4%; right: -4%; top: 46%; height: 0.11em; background: ⟦LINE⟧; border-radius: 999px;
      transform-origin: 0 50%; transform: scaleX(0); display: block; }
"""


STAMP_CSS = """
    .§stamp { position: absolute; padding: 14px 30px; border: 6px solid ⟦LINE⟧; border-radius: 10px; background: rgba(10,10,10,0.88);
      font: 64px/1.05 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; white-space: nowrap; opacity: 0; }
"""

COL_CSS = """
    .§cmp { position: absolute; top: 620px; width: 460px; height: 580px; border-radius: 24px; background: #121212; border: 2px solid #2e2e2e; }
    .§cmp.§right { border: 4px solid ⟦LINE⟧; }
    .§ch { position: absolute; left: 30px; top: 34px; width: 400px; font: 40px/1.1 ⟦FU⟧, sans-serif; color: ⟦MUTED⟧; letter-spacing: 0.04em; }
    .§cr { position: absolute; left: 30px; width: 400px; height: 3px; background: ⟦LINE⟧; top: 140px; }
    .§cv2 { position: absolute; left: 30px; top: 200px; width: 400px; font: 92px/1.05 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
"""


# ---- real images full frame: every scene runs on Guillaume's photos and driving footage, cut every 1 to 2 s
BG_CSS = """
    .§bg { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; opacity: 0; }
    .§bg img, .§bg .§spr { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(0.85) brightness(0.62) contrast(1.06); }
    .§spr { background-repeat: no-repeat; background-size: 800% 600%; }
    .§veil { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; pointer-events: none;
      background: linear-gradient(rgba(10,10,10,0.82) 0%, rgba(10,10,10,0.35) 30%, rgba(10,10,10,0.1) 48%, rgba(10,10,10,0.55) 64%, rgba(10,10,10,0.9) 82%, #0A0A0A 100%); }
"""
BG_JS = """
      // cut to a full-frame photo at t (hard cut), with a slow push-in until the next cut
      var BGS = [];
      function bgcut(id, t, dur, z0, z1, ox) {
        tl.set($(id), { opacity: 1 }, Math.max(0, t));
        BGS.forEach(function (b) { if (b[0] !== id && b[1] < t) tl.set($(b[0]), { opacity: 0 }, Math.max(0, t) + 0.001); });
        BGS.push([id, t]);
        tl.fromTo($(id), { scale: z0 || 1.0, x: 0 }, { scale: z1 || 1.12, x: ox || 0, duration: dur, ease: "none", immediateRender: t <= 0 }, Math.max(0, t));
      }
"""


def bgs(items):
    """items: [(id, image file, object-position)]; a file starting with sp- is a sprite sheet (video)"""
    out = ""
    for i, src, pos in items:
        if src.startswith("sp-"):
            out += f'<div id="§{i}" class="§bg"><div class="§spr" id="§{i}s" style="background-image:url(assets/img/{src})"></div></div>'
        else:
            out += f'<div id="§{i}" class="§bg"><img src="assets/img/{src}" style="object-position:{pos}"></div>'
    return out + '<div class="§veil"></div>'


def scene_01():
    css = BG_CSS + MEDIA_CSS + BIG_CSS + """
    #§h2 { opacity: 0; }
    #§rest { position: absolute; left: 0; top: 1100px; width: 1080px; text-align: center; font: 64px/1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; opacity: 0;
      text-shadow: 0 4px 20px rgba(0,0,0,0.7); }
    #§arrow { position: absolute; left: 500px; top: 1180px; width: 80px; height: 70px; overflow: visible; fill: none; stroke: ⟦LINE⟧;
      stroke-width: 10; stroke-linecap: round; stroke-linejoin: round; opacity: 0; }
    #§tagw { position: absolute; left: 620px; top: 820px; opacity: 0; }
    """
    st = bgs([("b1", "sp-drive.jpg", ""), ("b2", "golf.jpg", "45% 50%"), ("b3", "20140606_174216.jpg", "50% 50%")])
    hud = ('<div id="§h1" class="§big" style="top:290px">VENDRE DES<br>VOITURES</div>'
           '<div id="§h2" class="§big" style="top:290px;font-size:132px">SANS JAMAIS<br>LES <span class="§strk">ACHETER<i id="§sk"></i></span> ?</div>'
           '<div id="§tagw">' + TAG.replace('left:640px;top:690px;', 'left:0;top:0;') + '</div>'
           '<div id="§rest">RESTE JUSQU’AU BOUT</div><svg id="§arrow" viewBox="0 0 80 70"><path d="M40 4 L40 62 M12 36 L40 64 L68 36"/></svg>')
    js = MEDIA_JS + BG_JS + """
      // frame 0: on the road (real footage), the text already there and moving
      var c = at("sans") - 0.04;
      bgcut("b1", 0, c, 1.08, 1.0); sprite("b1s", 0, c, 48, 8, 12);
      tl.fromTo($("h1"), { scale: 1.12 }, { scale: 1, duration: 0.5, ease: "expo.out", immediateRender: true }, 0);
      // hard cut: a car for sale, its price tag; « acheter » struck through
      tl.set($("h1"), { opacity: 0 }, c); tl.set($("h2"), { opacity: 1 }, c);
      tl.fromTo($("h2"), { scale: 1.1 }, { scale: 1, duration: 0.25, ease: "expo.out", immediateRender: false }, c);
      bgcut("b2", c, at("reste") - c, 1.15, 1.0);
      pre("tagw", { opacity: 0, rotation: -20, scale: 0.6 }); go("tagw", { opacity: 1, rotation: 6, scale: 1 }, c + 0.1, 0.3, "back.out(2)");
      tl.fromTo($("sk"), { scaleX: 0 }, { scaleX: 1, duration: 0.25, ease: "power3.out", immediateRender: false }, at("acheter") + 0.25);
      shake("shk", at("acheter") + 0.3, 8);
      // « reste jusqu'au bout »
      go("tagw", { opacity: 0 }, at("reste") - 0.05, 0.1);
      bgcut("b3", at("reste") - 0.05, DUR - at("reste") + 0.1, 1.0, 1.15, -40);
      pre("rest", { opacity: 0, y: 20 }); go("rest", { opacity: 1, y: 0 }, at("reste") - 0.05, 0.2);
      pre("arrow", { opacity: 0, y: -20 }); go("arrow", { opacity: 1, y: 0 }, at("bout"), 0.25, "back.out(2)");
      tl.fromTo($("arrow"), { y: 0 }, { y: 16, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }, at("bout") + 0.3);
    """
    sfx = [("impact-bass-1", None, 0, 0.0, .26), ("pop", "sans", 1, -.06, .2)]
    return css, st, hud, js, (540, 900), sfx


def scene_02():
    css = BG_CSS + """
    #§y { position: absolute; left: 0; top: 640px; width: 1080px; text-align: center; font: 250px/1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; opacity: 0;
      text-shadow: 0 8px 40px rgba(0,0,0,0.7); }
    #§mbox { position: absolute; left: 190px; top: 930px; width: 700px; height: 240px; border: 3px solid ⟦LINE⟧; border-radius: 12px; opacity: 0;
      background: rgba(10,10,10,0.6); }
    #§m { position: absolute; left: 0; top: 40px; width: 100%; text-align: center; font: 170px/1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
    """
    st = bgs([("b1", "20140530_170820.jpg", "40% 50%"), ("b2", "20140606_174140.jpg", "50% 50%")])
    hud = (title("t2", ["J’AI COMMENCÉ"], 340, 110)
           + '<div id="§y">' + odo("yy", "2010") + '</div><div id="§mbox"><div id="§m">' + odo("mm", "3 000 €") + '</div></div>')
    js = BG_JS + """
      bgcut("b1", 0, at("3000") - 0.15, 1.15, 1.0, 30);
      slam("t2-0", 0.02, { s: 1.3 }); stroke("t2", at("commencé"));
      pre("y", { opacity: 0, scale: 1.3 }); go("y", { opacity: 1, scale: 1 }, at("2010") - 0.1, 0.2, "expo.out");
      odo("yy", at("2010") - 0.1, 0.5, { from: "1990" });
      // 3 000 €: the counter stops dead
      bgcut("b2", at("3000") - 0.15, DUR - at("3000") + 0.2, 1.2, 1.05);
      pre("mbox", { opacity: 0, y: 40 }); go("mbox", { opacity: 1, y: 0 }, at("3000") - 0.15, 0.2, "expo.out");
      odo("mm", at("3000") - 0.1, 0.45, { from: "0 000" });
      shake("shk", at("3000") + 0.38, 9);
    """
    return css, st, hud, js, (540, 900), []


def scene_03():
    css = BG_CSS + STAMP_CSS + """
    #§pk { position: absolute; left: 60px; top: 700px; width: 330px; height: 230px; border-radius: 22px; background: rgba(10,10,10,0.78); border: 2px solid ⟦LINE⟧; opacity: 0; }
    .§lab { position: absolute; left: 0; top: 28px; width: 100%; text-align: center; font: 30px/1 ⟦FU⟧, sans-serif; color: ⟦TEXT⟧; letter-spacing: 0.1em; }
    .§val { position: absolute; left: 0; top: 96px; width: 100%; text-align: center; font: 84px/1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
    #§pk0 { opacity: 0; }
    #§cv { position: absolute; left: 470px; top: 700px; width: 550px; height: 230px; border-radius: 22px; background: rgba(10,10,10,0.78); border: 2px solid ⟦LINE⟧; text-align: center; opacity: 0; }
    #§cvl { margin-top: 28px; font: 30px/1 ⟦FU⟧, sans-serif; color: ⟦TEXT⟧; letter-spacing: 0.1em; }
    #§cvv { margin-top: 20px; font: 96px/1.1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
    .§coin { position: absolute; width: 26px; height: 26px; border-radius: 50%; background: ⟦LINE⟧; opacity: 0; }
    """
    coins = "".join(f'<i class="§coin" id="§co{k}" style="left:390px;top:{800 + (k % 3) * 18}px"></i>' for k in range(6))
    st = bgs([("b1", "parc4.jpg", "50% 50%"), ("b2", "parc3.jpg", "60% 50%"), ("b3", "parc2.jpg", "35% 50%"),
              ("b4", "moteur.jpg", "55% 50%"), ("b5", "parc1.jpg", "30% 50%")]) + coins
    hud = (title("t3", [("CE QUE FONT LA PLUPART :", 64), "ACHETER POUR REVENDRE"], 320, 92)
           + '<div id="§pk"><div class="§lab">TA POCHE</div><div class="§val" id="§pk1">13 000 €</div><div class="§val" id="§pk0">0 €</div></div>'
           + '<div id="§cv"><div id="§cvl">DANS LA VOITURE</div><div id="§cvv">' + odo("cvo", "13 000 €") + '</div></div>'
           + '<div id="§s1" class="§stamp" style="left:150px;top:1030px;transform:rotate(-6deg)">PANNE : POUR TOI</div>'
           + '<div id="§s2" class="§stamp" style="left:240px;top:1130px;transform:rotate(4deg)">INVENDUE : POUR TOI</div>')
    js = BG_JS + """
      var t1 = at("voiture") - 0.1, t2 = at("dorment") - 0.1, t3 = at("panne") - 0.1, t4 = at("vend") - 0.15;
      bgcut("b1", 0, t1, 1.0, 1.12, -30);
      slam("t3-0", 0.02); slam("t3-1", at("achètent") - 0.05); stroke("t3", at("revendre"));
      bgcut("b2", t1, t2 - t1, 1.15, 1.0);
      pre("pk", { opacity: 0, x: -60 }); go("pk", { opacity: 1, x: 0 }, at("13000") - 0.1, 0.3, "expo.out");
      // the money goes from your pocket into the car
      var d0 = at("13000", 2) - 0.1, dd = 1.1;
      pre("cv", { opacity: 0 }); go("cv", { opacity: 1 }, d0, 0.2);
      odo("cvo", d0, dd, { from: "00 000" });
      for (var k = 0; k < 6; k++) {
        tl.fromTo($("co" + k), { opacity: 0, x: 0, y: 0 }, { opacity: 1, x: 220, y: 0, duration: 0.4, ease: "power2.in", immediateRender: false }, d0 + k * 0.15);
        tl.set($("co" + k), { opacity: 0 }, d0 + k * 0.15 + 0.41);
      }
      tl.set($("pk1"), { opacity: 0 }, d0 + dd); tl.set($("pk0"), { opacity: 1 }, d0 + dd);
      // it sleeps: the stock, rows of cars
      bgcut("b3", t2, t3 - t2, 1.0, 1.1, 40);
      go("pk", { opacity: 0 }, t3, 0.15); go("cv", { opacity: 0 }, t3, 0.15); go("t3", { opacity: 0 }, t3, 0.15);
      // it breaks down: for you (the engine out, in the garage)
      bgcut("b4", t3, t4 - t3, 1.2, 1.0);
      pre("s1", { opacity: 0, scale: 1.8 }); go("s1", { opacity: 1, scale: 1 }, at("toi", 2) - 0.12, 0.14, "expo.in");
      shake("shk", at("toi", 2) + 0.02, 12);
      // it does not sell: for you
      bgcut("b5", t4, DUR - t4 + 0.1, 1.0, 1.15);
      pre("s2", { opacity: 0, scale: 1.8 }); go("s2", { opacity: 1, scale: 1 }, at("toi", 3) - 0.12, 0.14, "expo.in");
      shake("shk", at("toi", 3) + 0.02, 12);
    """
    sfx = [("impact-bass-2", "toi", 2, 0, .3), ("impact-bass-2", "toi", 3, 0, .3)]
    return css, st, hud, js, (540, 900), sfx


def scene_04():
    css = BG_CSS + """
    #§cv { position: absolute; left: 560px; top: 1010px; width: 440px; height: 190px; border-radius: 22px; background: rgba(10,10,10,0.78); border: 2px solid ⟦LINE⟧; text-align: center; opacity: 0; }
    #§cvl { margin-top: 24px; font: 30px/1 ⟦FU⟧, sans-serif; color: ⟦TEXT⟧; letter-spacing: 0.1em; }
    #§cvv { margin-top: 14px; font: 96px/1.1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
    #§own { position: absolute; left: 80px; top: 1060px; padding: 14px 26px; border: 2px solid ⟦LINE⟧; border-radius: 10px; background: rgba(10,10,10,0.78);
      font: 44px/1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; opacity: 0; }
    .§step { position: absolute; left: 90px; width: 900px; height: 100px; border-radius: 18px; background: rgba(10,10,10,0.82); border: 2px solid #2e2e2e; opacity: 0; }
    .§step.§on { border-color: ⟦LINE⟧; }
    .§sn { position: absolute; left: 24px; top: 16px; width: 68px; height: 68px; border-radius: 50%; background: ⟦CHIP_BG⟧; color: #0A0A0A; font: 48px/68px ⟦FT⟧, sans-serif; text-align: center; }
    .§stx { position: absolute; left: 120px; top: 0; height: 100px; font: 54px/100px ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
    """
    steps = ["ESTIMER", "ANNONCER", "TROUVER L’ACHETEUR", "PAYÉ À LA VENTE"]
    st = bgs([("b1", "x4.jpg", "55% 50%"), ("b2", "fiat.jpg", "50% 50%"), ("b3", "jag-11.jpg", "50% 50%"), ("b4", "jag-01.jpg", "50% 50%"),
              ("b5", "20140606_174128.jpg", "50% 50%"), ("b6", "mustang.jpg", "45% 50%")])
    hud = (title("t4", [("L’AUTRE FAÇON :", 64), "VENDRE SANS ACHETER"], 320, 92)
           + '<div id="§cv"><div id="§cvl">DANS LA VOITURE</div><div id="§cvv">0 €</div></div><div id="§own">SA VOITURE</div>'
           + "".join(f'<div id="§st{k}" class="§step" style="top:{660 + k * 130}px"><div class="§sn">{k + 1}</div><div class="§stx">{t}</div></div>'
                     for k, t in enumerate(steps)))
    js = BG_JS + """
      var cues = [at("l'estimes"), at("l'annonce"), at("l'acheteur"), at("payé")];
      bgcut("b1", 0, at("voiture") - 0.1, 1.0, 1.12, -30);
      slam("t4-0", 0.02); slam("t4-1", at("vends") - 0.05); stroke("t4", at("acheter"));
      // the owner's car, nothing of yours in it
      bgcut("b2", at("voiture") - 0.1, cues[0] - at("voiture"), 1.15, 1.0);
      pre("cv", { opacity: 0, scale: 1.3 }); go("cv", { opacity: 1, scale: 1 }, at("voiture") + 0.3, 0.25, "expo.out");
      pre("own", { opacity: 0, x: -40 }); go("own", { opacity: 1, x: 0 }, at("propriétaire") - 0.15, 0.25, "expo.out");
      go("cv", { opacity: 0 }, cues[0] - 0.2, 0.15); go("own", { opacity: 0 }, cues[0] - 0.2, 0.15); go("t4", { opacity: 0.0 }, cues[0] - 0.2, 0.15);
      // four steps, one photo each
      ["b3", "b4", "b5", "b6"].forEach(function (b, k) {
        var e = k < 3 ? cues[k + 1] - 0.15 : DUR + 0.1;
        bgcut(b, cues[k] - 0.15, e - cues[k] + 0.15, k % 2 ? 1.0 : 1.15, k % 2 ? 1.15 : 1.0);
      });
      [0, 1, 2, 3].forEach(function (k) {
        pre("st" + k, { opacity: 0, x: -60 }); go("st" + k, { opacity: 1, x: 0 }, cues[k] - 0.15, 0.3, "expo.out");
        $("st" + k).classList.add(P + "on");
        if (k > 0) go("st" + (k - 1), { opacity: 0.55 }, cues[k] - 0.15, 0.25);
      });
    """
    return css, st, hud, js, (540, 900), []


def split_bg():
    return ('<div class="§bg" id="§bl" style="width:540px;opacity:1"><img src="assets/img/parc2.jpg" style="object-position:35% 50%"></div>'
            '<div class="§bg" id="§br" style="left:540px;width:540px;opacity:1"><img src="assets/img/golf.jpg" style="object-position:40% 50%"></div>'
            '<div class="§veil"></div>')


COLS = ('<div id="§L" class="§cmp" style="left:50px"><div class="§ch">ACHETER POUR REVENDRE</div><i class="§cr"></i>'
        '<div id="§lv" class="§cv2">STOCK<br>ET RISQUE</div></div>'
        '<div id="§R" class="§cmp §right" style="left:570px"><div class="§ch">VENDRE SANS ACHETER</div><i class="§cr"></i>'
        '<div id="§rv" class="§cv2">RELATION</div></div>')


COL_CSS2 = COL_CSS.replace("background: #121212; border: 2px solid #2e2e2e;", "background: rgba(10,10,10,0.8); border: 2px solid #2e2e2e;")


def scene_05():
    js = """
      tl.fromTo($("bl"), { scale: 1.12 }, { scale: 1.0, duration: DUR, ease: "none", immediateRender: true }, 0);
      tl.fromTo($("br"), { scale: 1.0, opacity: 0.3 }, { scale: 1.12, opacity: 1, duration: DUR, ease: "none", immediateRender: true }, 0);
      pre("L", { opacity: 0, x: -80 }); go("L", { opacity: 1, x: 0 }, 0.0, 0.3, "expo.out");
      pre("lv", { opacity: 0, scale: 1.3 }); go("lv", { opacity: 1, scale: 1 }, at("stock") - 0.1, 0.2, "expo.out");
      pre("R", { opacity: 0, x: 80 }); go("R", { opacity: 1, x: 0 }, at("toi") - 0.1, 0.3, "expo.out");
      pre("rv", { opacity: 0, scale: 1.3 }); go("rv", { opacity: 1, scale: 1 }, at("relation") - 0.1, 0.2, "expo.out");
      go("L", { opacity: 0.4 }, at("relation"), 0.3);
    """
    sfx = [("whoosh-cinematic", None, 0, 0.0, .2)]
    return BG_CSS + COL_CSS2, split_bg() + COLS, "", js, (540, 900), sfx


def scene_06():
    hud = title("t6", ["UN VRAI MÉTIER"], 330, 116) + title("t6b", ["SANS IMMOBILISER", "TON ARGENT"], 300, 104)
    js = """
      tl.set($("L"), { opacity: 0.4 }, 0);
      tl.fromTo($("bl"), { opacity: 0.6 }, { opacity: 0.15, duration: 0.6, immediateRender: true }, 0);
      tl.fromTo($("br"), { scale: 1.12 }, { scale: 1.25, duration: DUR, ease: "none", immediateRender: true }, 0);
      slam("t6-0", at("métier") - 0.25, { s: 1.3 }); stroke("t6", at("métier") + 0.1);
      tl.fromTo($("R"), { scale: 1 }, { scale: 1.05, duration: 0.4, ease: "power2.out", immediateRender: false }, at("démarre") - 0.1);
      go("t6", { opacity: 0, y: -30 }, at("immobiliser") - 0.2, 0.12, "power2.in");
      slam("t6b-0", at("immobiliser") - 0.15); slam("t6b-1", at("argent") - 0.1); stroke("t6b", at("argent") + 0.1);
      go("L", { opacity: 0.15 }, at("argent"), 0.3);
    """
    return BG_CSS + COL_CSS2, split_bg() + COLS, hud, js, (540, 900), []


def scene_07():
    css = """
    #§me { position: absolute; left: 70px; top: 640px; width: 940px; height: 1240px; opacity: 0; }
    #§me img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: contain; object-position: 50% 100%; filter: saturate(0.8) contrast(1.03); }
    #§id { position: absolute; left: 0; top: 330px; width: 1080px; text-align: center; opacity: 0; }
    #§nm { font: 104px/1.05 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
    #§rl { width: 520px; height: 4px; margin: 26px auto 22px; background: ⟦LINE⟧; transform-origin: 50% 50%; }
    #§ro { font: 46px/1.15 ⟦FU⟧, sans-serif; color: ⟦TEXT⟧; letter-spacing: 0.04em; opacity: 0; }
    """
    st = '<div id="§me"><img src="assets/img/guillaume-forge.png"></div>'
    hud = '<div id="§id"><div id="§nm">GUILLAUME HERBIN</div><div id="§rl"></div><div id="§ro">FONDATEUR DU PROGRAMME FORGE</div></div>'
    js = """
      pre("me", { opacity: 0, y: 60 }); go("me", { opacity: 1, y: 0 }, 0.0, 0.4, "expo.out");
      pre("id", { opacity: 0 }); go("id", { opacity: 1 }, at("guillaumeherbin") - 0.1, 0.2);
      tl.fromTo($("rl"), { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, at("guillaumeherbin") + 0.2);
      tl.fromTo($("ro"), { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, at("fondateur") - 0.1);
      init("me", { opacity: 1, y: 0, scale: 1 }); go("me", { scale: 1.05 }, at("fondateur"), 1.2, "none");
    """
    return css, st, hud, js, (540, 700), []


def scene_08():
    shutil.copy(charte.logo_path("logo_dark"), "assets/img/charte-logo.svg")
    css = """
    #§logo { position: absolute; left: 240px; top: 480px; width: 600px; opacity: 0; }
    #§sub { position: absolute; left: 0; top: 820px; width: 1080px; text-align: center; font: 130px/1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; opacity: 0; }
    #§srl { position: absolute; left: 340px; top: 980px; width: 400px; height: 4px; background: ⟦LINE⟧; transform-origin: 50% 50%; transform: scaleX(0); }
    #§kit { position: absolute; left: 0; top: 1020px; width: 1080px; text-align: center; font: 44px/1.2 ⟦FU⟧, sans-serif; color: ⟦TEXT⟧; letter-spacing: 0.04em; opacity: 0; }
    """
    hud = ('<img id="§logo" src="assets/img/charte-logo.svg">'
           '<div id="§sub">ABONNE-TOI</div><i id="§srl"></i><div id="§kit">' + charte.C["end_line"].rstrip(".") + '</div>')
    js = """
      pre("logo", { opacity: 0, scale: 1.1 }); go("logo", { opacity: 1, scale: 1 }, 0.0, 0.35, "expo.out");
      pre("kit", { opacity: 0 }); go("kit", { opacity: 1 }, at("métier") - 0.1, 0.3);
      slam("sub", at("abonne-toi") - 0.05, { s: 1.3 });
      tl.fromTo($("srl"), { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, at("abonne-toi") + 0.15);
    """
    sfx = [("whoosh-cinematic", None, 0, 0.0, .2)]
    return css, "", hud, js, (540, 800), sfx


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
    charte.fonts(HERE)
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
        html = charte.apply(html.replace("§", P).replace("⟦FONT_FACES⟧", charte.font_face_css()))
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
message: "Ma pire marge en 16 ans : une Ferrari 360 achetée sur photos sans contrôle, moteur déposé, plus d'un an immobilisée, revendue avec 16 800 € de perte ; trois erreurs à ne pas refaire."
arc: Hook → Setup → Turn → Diagnosis → Struggle → Payoff → Lessons → CTA
audience: "Marchands et passionnés automobiles"
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
- **Negative list** : aucun billet ni espèce ; jamais plus de 6 mots par bloc de texte ; rouge sombre réservé à la jauge de température et aux culasses ; photos réelles désaturées, cadre orange, plaques floutées.

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
