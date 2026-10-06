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
TAIL = 1.8          # hold after the last word (end card)
FPS = 30

# ---------------------------------------------------------------------------------------------------------------------
# The voice, scene by scene, cut into subtitle chunks (2 to 5 words). *word* = key word (orange). ~ glues two tokens
# into one subtitle word (« 10~000 », « voitures~? »). Numbers are spoken « dix mille », « deux mille vingt-six ».
SCENES = [
 dict(id="01-hook", name="Hook", window=(0, 3), chunks=[
   "Arrête de *vendre*", "l'extension de garantie."]),
 dict(id="02-probleme", name="Le problème", window=(3, 10), chunks=[
   "Tu expliques la *couverture*,", "les options, le prix.", "Le client n'entend", "qu'une chose~:",
   "un *vendeur* qui veut", "lui vendre", "un truc en plus."]),
 dict(id="03-bascule", name="La bascule", window=(10, 14), chunks=[
   "Alors arrête", "d'*argumenter*.", "Montre-lui", "*trois* choses."]),
 dict(id="04-facture", name="Preuve 1, la facture", window=(14, 24), chunks=[
   "Un~: une vraie *facture*.", "Un client, un *turbo*,", "*2~500* euros", "de réparation.", "Reste à charge~:",
   "*zéro*.", "Il ne t'écoute plus", "décrire une couverture,", "il regarde ce qu'elle", "a déjà *payé*."]),
 dict(id="05-autres", name="Preuve 2, les autres", window=(24, 32), chunks=[
   "Deux~: les *autres*.", "*8* clients sur 10", "la prennent.", "Il n'est plus le *pigeon*", "à qui on refile",
   "une option.", "Il est celui qui *hésite*", "alors que les autres", "ont tranché."]),
 dict(id="06-refus", name="Preuve 3, le refus", window=(32, 42), chunks=[
   "Trois~: celui qui", "a dit *non*.", "*8* mois plus tard,", "la boîte de *vitesses*.", "*6~700* euros",
   "de sa poche.", "Tu ne le racontes pas", "pour faire *peur*.", "Tu le racontes", "parce que c'est *arrivé*."]),
 dict(id="07-closing", name="Le closing", window=(42, 49), chunks=[
   "À ce stade,", "la question n'est plus", "de savoir s'il la prend.", "C'est de savoir", "comment il la *paie*~:",
   "au comptant", "ou tous les mois.", "Tu lui laisses *choisir*,", "c'est tout."]),
 dict(id="08-regle", name="La règle", window=(49, 53), chunks=[
   "Une *facture*,", "un *chiffre*,", "une *histoire*.", "Une *preuve*", "vaut dix arguments."]),
 dict(id="09-cta", name="CTA", window=(53, 57), chunks=[
   "Ne vends pas.", "*Montre*.", "*Abonne-toi*", "pour plus de contenu", "comme celui-ci."]),
]
SPOKEN_SYL = {"2500": 6, "6700": 6, "8": 1, "10": 1}   # « deux mille cinq cents », « six mille sept cents », « huit », « dix »
RED = "#B3261E"   # dark red, only for the gearbox bill of scene 6 (asked in the brief)



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

def eyes(eid, x, y, w):
    h = w * 1.5
    return (f'<svg id="§{eid}" viewBox="0 0 200 300" class="§abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px;overflow:visible">'
            f'<ellipse id="§{eid}-l" cx="82" cy="64" rx="7" ry="11" fill="#0A0A0A"/>'
            f'<ellipse id="§{eid}-r" cx="118" cy="64" rx="7" ry="11" fill="#0A0A0A"/></svg>')


def scene_01():
    css = """
    .§vends { position: relative; display: inline-block; }
    .§strike { position: absolute; left: -0.08em; right: -0.08em; top: 46%; height: 0.13em; background: #FB8000; border-radius: 999px;
      transform: rotate(-5deg) scaleX(0); transform-origin: 0 50%; box-shadow: 0 0 30px rgba(251,128,0,0.5); }
    """
    st = title("t1", ['NE <span class="§vends">VENDS<i id="§strike" class="§strike"></i></span> PAS', "L’EXTENSION",
                      "DE GARANTIE."], 600, 140)
    js = """
      slam("t1-0", Math.max(0.02, at("arrête") - 0.02), { s: 1.35 });
      tl.fromTo($("strike"), { scaleX: 0, rotation: -5 }, { scaleX: 1, rotation: -5, duration: 0.22, ease: "power4.out", immediateRender: false }, at("vendre") + 0.05);
      shake("shk", at("vendre") + 0.2, 12);
      slam("t1-1", at("l'extension") - 0.02); slam("t1-2", at("garantie") - 0.02); stroke("t1", at("garantie") + 0.2);
      cam(0, 0, 1.05, at("vendre"), 0.5, "power2.out");
      init("halo", { scale: 1 }); go("halo", { scale: 1.2 }, at("vendre"), 0.5);
    """
    sfx = [("impact-bass-1", None, 0, 0.02, .28), ("click", "vendre", 1, .05, .3), ("pop", "l'extension", 1, 0, .14),
           ("pop", "garantie", 1, 0, .14)]
    return css, st, "", js, (540, 800), sfx


def scene_02():
    css = """
    .§bub { position: absolute; padding: 14px 34px; border-radius: 44px; border: 4px solid #ffffff; background: #151515;
      font: 54px/1.15 "Anton", sans-serif; color: #ffffff; opacity: 0; white-space: nowrap; }
    .§tail { position: absolute; left: 34px; bottom: -22px; width: 30px; height: 30px; background: #151515; border-right: 4px solid #fff;
      border-bottom: 4px solid #fff; transform: rotate(45deg); }
    #§zz { position: absolute; left: 870px; top: 760px; font: 70px "Anton", sans-serif; color: #6f6f6f; opacity: 0; }
    """
    st = ('<div class="§floor"></div>' + person("pv", 80, 830, 230) + person("pc", 740, 830, 230) + eyes("ey", 740, 830, 230)
          + '<div id="§b1" class="§bub" style="left:250px;top:610px">COUVERTURE<i class="§tail"></i></div>'
          + '<div id="§b2" class="§bub" style="left:330px;top:720px">OPTION<i class="§tail"></i></div>'
          + '<div id="§b3" class="§bub" style="left:290px;top:830px">SÉRÉNITÉ<i class="§tail"></i></div>'
          + '<div id="§zz">z</div>')
    hud = title("t2", ["IL ENTEND UN", "ARGUMENT DE VENTE"], 280, 110)
    js = """
      ["pv", "pc"].forEach(function (p) { init(p + "-w", { opacity: 0 }); init(p + "-o", { opacity: 0 }); init(p + "-glow", { opacity: 0 }); });
      tl.set($("pc-w"), { opacity: 1 }, 0); init("pc-w", { opacity: 1 });
      lit("pv", "orange", 0.02, 0.3);
      pre("pv", { opacity: 0, y: 60 }); go("pv", { opacity: 1, y: 0 }, 0.02, 0.3, "back.out(1.6)");
      pre("pc", { opacity: 0, y: 60 }); go("pc", { opacity: 1, y: 0 }, 0.12, 0.3, "back.out(1.6)");
      pre("ey", { opacity: 0 }); go("ey", { opacity: 1 }, 0.3, 0.1);
      [["b1", "couverture"], ["b2", "options"], ["b3", "prix"]].forEach(function (b) {
        pre(b[0], { opacity: 0, scale: 0.4 }); go(b[0], { opacity: 1, scale: 1 }, at(b[1]) - 0.04, 0.28, "back.out(2.2)");
      });
      // the client only hears a seller: his eyes close
      var ec = at("chose");
      [["ey-l", 82], ["ey-r", 118]].forEach(function (e) {
        tl.fromTo($(e[0]), { attr: { ry: 11 } }, { attr: { ry: 1.5 }, duration: 0.18, ease: "power2.in", immediateRender: false }, ec);
      });
      pre("zz", { opacity: 0, y: 0 }); go("zz", { opacity: 1, y: -30 }, ec + 0.3, 0.4); go("zz", { opacity: 0, y: -80 }, ec + 1.0, 0.5);
      slam("t2-0", at("vendeur") - 0.05); slam("t2-1", at("vendre", 1) - 0.02); stroke("t2", at("plus") - 0.05);
      ["b1", "b2", "b3"].forEach(function (b, k) { go(b, { opacity: 0.25, scale: 0.92 }, at("truc") + k * 0.05, 0.4); });
      lit("pv", "grey", at("truc"), 0.4);
      cam(0, -10, 1.04, at("n'entend") - 0.1, 0.6);
    """
    sfx = [("pop", "couverture", 1, -.04, .16), ("pop", "options", 1, -.04, .16), ("pop", "prix", 1, -.04, .16),
           ("click-soft", "chose", 1, 0, .25), ("pop", "vendeur", 1, -.05, .14)]
    return css, st, hud, js, (540, 900), sfx


def scene_03():
    css = """
    #§arg { position: absolute; left: 140px; top: 760px; width: 800px; text-align: center; }
    #§argb { display: inline-block; padding: 26px 60px; border-radius: 70px; border: 6px solid #ffffff; background: #151515;
      font: 120px/1.1 "Anton", sans-serif; color: #ffffff; }
    .§shard { position: absolute; left: 530px; top: 840px; width: 26px; height: 26px; background: #FB8000; opacity: 0; border-radius: 4px; }
    .§slot { position: absolute; top: 700px; width: 240px; height: 320px; border-radius: 28px; border: 5px dashed #4a4a4a; opacity: 0; }
    .§slotn { position: absolute; left: -22px; top: -22px; width: 64px; height: 64px; border-radius: 50%; background: #FB8000; color: #0A0A0A;
      font: 44px/64px "Anton", sans-serif; text-align: center; opacity: 0; }
    .§ico { position: absolute; left: 30px; top: 50px; width: 180px; height: 220px; overflow: visible; opacity: 0; fill: none; stroke: #ffffff;
      stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; }
    """
    ICONS = [
      # the bill
      '<path d="M40 20 L120 20 L150 50 L150 200 L40 200 Z"/><path d="M120 20 L120 50 L150 50"/>'
      '<path d="M62 86 L128 86 M62 116 L128 116 M62 146 L100 146"/><path d="M62 176 L128 176" stroke="#FB8000"/>',
      # the others: three customers
      '<g fill="#ffffff" stroke="none"><circle cx="50" cy="96" r="20"/><path d="M18 196 C18 150 34 128 50 128 C66 128 82 150 82 196 Z"/>'
      '<circle cx="130" cy="96" r="20"/><path d="M98 196 C98 150 114 128 130 128 C146 128 162 150 162 196 Z"/>'
      '<circle cx="90" cy="66" r="24" fill="#FB8000"/><path d="M52 196 C52 140 70 106 90 106 C110 106 128 140 128 196 Z" fill="#FB8000"/></g>',
      # the one who said no
      '<g fill="#6f6f6f" stroke="none"><circle cx="78" cy="78" r="30"/><path d="M28 200 C28 140 50 116 78 116 C106 116 128 140 128 200 Z"/></g>'
      '<path d="M120 40 L168 88 M168 40 L120 88" stroke="#FB8000" stroke-width="12"/>',
    ]
    shards = "".join(f'<div id="§sh{i}" class="§shard"></div>' for i in range(10))
    slots = "".join(f'<div id="§s{i}" class="§slot" style="left:{140 + i * 280}px"><svg id="§ic{i}" class="§ico" viewBox="0 0 180 220">{ICONS[i]}</svg>'
                    f'<span id="§n{i}" class="§slotn">{i + 1}</span></div>' for i in range(3))
    st = '<div id="§arg"><span id="§argb">ARGUMENT</span></div>' + shards + slots
    hud = title("t3", ["MONTRE-LUI", "TROIS CHOSES"], 290, 116)
    js = """
      slam("arg", 0.02, { s: 1.3 });
      go("arg", { scale: 1.12 }, at("d'argumenter") - 0.2, 0.2, "power2.in");
      go("arg", { opacity: 0, scale: 1.5 }, at("d'argumenter"), 0.12, "power2.out");
      for (var i = 0; i < 10; i++) {
        var a = (i / 10) * Math.PI * 2;
        pre("sh" + i, { opacity: 0, x: 0, y: 0, rotation: 0 });
        go("sh" + i, { opacity: 1, x: Math.cos(a) * 60, y: Math.sin(a) * 40 }, at("d'argumenter"), 0.05);
        go("sh" + i, { opacity: 0, x: Math.cos(a) * (380 + (i % 3) * 80), y: Math.sin(a) * (260 + (i % 2) * 90), rotation: 200 }, at("d'argumenter") + 0.05, 0.6, "power3.out");
      }
      shake("shk", at("d'argumenter") + 0.02, 14);
      slam("t3-0", at("montre-lui") - 0.03); slam("t3-1", at("trois")); stroke("t3", at("choses"));
      for (var k = 0; k < 3; k++) {
        pre("s" + k, { opacity: 0, y: 50, borderColor: "#4a4a4a" }); go("s" + k, { opacity: 1, y: 0 }, at("montre-lui") + 0.08 + k * 0.08, 0.3, "back.out(1.6)");
        slam("ic" + k, at("trois") + k * 0.16, { s: 1.4 });
        pre("n" + k, { opacity: 0, scale: 0.3 }); go("n" + k, { opacity: 1, scale: 1 }, at("trois") + k * 0.16 + 0.08, 0.22, "back.out(2.4)");
        go("s" + k, { borderColor: "#FB8000" }, at("trois") + k * 0.16, 0.2);
      }
      cam(0, -10, 1.04, at("montre-lui"), 0.6);
    """
    sfx = [("pop", None, 0, 0.02, .16), ("impact-bass-2", "d'argumenter", 1, 0, .3), ("whoosh-short", "montre-lui", 1, 0, .14),
           ("pop", "trois", 1, 0, .14), ("pop", "trois", 1, .14, .14), ("pop", "trois", 1, .28, .14)]
    return css, st, hud, js, (540, 860), sfx


def scene_04():
    css = """
    #§paper { position: absolute; left: 100px; top: 300px; width: 880px; height: 920px; border-radius: 10px; background: #f7f5f1;
      box-shadow: 0 40px 90px rgba(0,0,0,0.7); transform: rotate(-1.5deg); color: #141414; font-family: "Instrument Sans", sans-serif; overflow: hidden; }
    .§pa { position: absolute; }
    .§blur { position: absolute; height: 26px; border-radius: 6px; background: #b8b4ad; filter: blur(5px); }
    .§lab { font: 600 26px/1 "Instrument Sans", sans-serif; color: #8a857c; text-transform: uppercase; letter-spacing: 0.05em; }
    .§row { position: absolute; left: 50px; width: 780px; height: 64px; }
    .§rowt { position: absolute; left: 16px; top: 0; font: 600 34px/64px "Instrument Sans", sans-serif; }
    .§rowv { position: absolute; right: 16px; top: 0; font: 40px/64px "Anton", sans-serif; }
    .§hl { position: absolute; left: 0; top: 0; width: 100%; height: 100%; border-radius: 10px; background: rgba(251,128,0,0.22);
      border-left: 8px solid #FB8000; transform-origin: 0 50%; transform: scaleX(0); }
    #§stamp { position: absolute; left: 520px; top: 740px; padding: 6px 30px; border: 8px solid #FB8000; border-radius: 16px;
      font: 92px/1.1 "Anton", sans-serif; color: #FB8000; transform: rotate(-10deg); opacity: 0; }
    #§badge { position: absolute; left: 60px; top: 236px; width: 110px; height: 110px; border-radius: 50%; background: #FB8000; color: #0A0A0A;
      font: 76px/110px "Anton", sans-serif; text-align: center; opacity: 0; box-shadow: 0 0 40px rgba(251,128,0,0.5); }
    """
    rows = [("r1", 330, "Turbo (remplacement)", "1 980,00 €", ""), ("r2", 400, "Main-d’œuvre", "520,00 €", ""),
            ("r3", 480, "TOTAL TTC", None, "font-weight:700"), ("r4", 556, "Garantie mécanique", "− 2 500,00 €", ""),
            ("r5", 650, "RESTE À CHARGE", None, "")]
    rh = ""
    for rid, y, t, v, sty in rows:
        big = rid == "r5"
        val = (odo("tot", "2 500,00 €") if rid == "r3" else odo("rac", "0,00 €") if big else v)
        fs = ' style="font-size:46px"' if big else ""
        rh += (f'<div class="§row" style="top:{y}px{";height:80px" if big else ""}"><div id="§{rid}-hl" class="§hl"></div>'
               f'<div class="§rowt" style="{sty}{";font:52px/80px Anton,sans-serif" if big else ""}">{t}</div>'
               f'<div class="§rowv"{fs if not big else " style=font-size:60px;line-height:80px"}>{val}</div></div>')
    st = ('<div id="§paper">'
          '<div class="§pa" style="left:50px;top:40px;font:72px/1 Anton,sans-serif">FACTURE</div>'
          '<div class="§pa §lab" style="left:560px;top:52px">N°</div><div class="§blur" style="left:610px;top:48px;width:200px"></div>'
          '<div class="§blur" style="left:50px;top:140px;width:300px"></div><div class="§blur" style="left:50px;top:182px;width:220px"></div>'
          '<div class="§pa §lab" style="left:480px;top:140px">Client</div><div class="§blur" style="left:600px;top:136px;width:220px"></div>'
          '<div class="§pa §lab" style="left:480px;top:186px">Immat.</div><div class="§blur" style="left:600px;top:182px;width:170px"></div>'
          '<div class="§pa" style="left:50px;top:250px;width:780px;height:2px;background:#d8d3ca"></div>'
          '<div class="§pa §lab" style="left:66px;top:282px">Désignation</div><div class="§pa §lab" style="right:66px;top:282px">Montant</div>'
          + rh + '<div id="§stamp">PAYÉ</div></div><div id="§badge">1</div>')
    js = """
      pre("paper", { opacity: 0, y: 160, rotation: -5 }); go("paper", { opacity: 1, y: 0, rotation: -1.5 }, 0.02, 0.45, "expo.out");
      pre("badge", { opacity: 0, scale: 0.3 }); go("badge", { opacity: 1, scale: 1 }, at("facture") - 0.05, 0.28, "back.out(2.2)");
      odo("tot", 0, 0.01, { from: "0 000,00", spinLow: false });
      tl.fromTo($("r1-hl"), { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, at("turbo") - 0.04);
      tl.fromTo($("r3-hl"), { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, at("2500") - 0.06);
      odo("tot", at("2500") - 0.06, 0.9);
      cam(0, -60, 1.12, at("reste") - 0.1, 0.6);
      tl.fromTo($("r5-hl"), { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, at("charge") - 0.05);
      pre("rac", { opacity: 0 }); slam("rac", at("zéro") - 0.06, { s: 1.4 }); odo("rac", at("zéro") - 0.06, 0.5, { from: "0,00" });
      init("halo", { y: 0 }); go("halo", { y: 220 }, at("reste"), 0.6);
      cam(0, -10, 1.04, at("t'écoute") - 0.1, 0.7, "power2.inOut");
      pre("stamp", { opacity: 0, scale: 2.4, rotation: -10 }); go("stamp", { opacity: 1, scale: 1, rotation: -10 }, at("payé") - 0.08, 0.16, "expo.in");
      shake("shk", at("payé") + 0.08, 8);
      cam(0, -40, 1.08, at("payé") + 0.1, 0.8, "power2.out");
    """
    sfx = [("whoosh-short", None, 0, 0.02, .16), ("pop", "facture", 1, -.05, .16), ("click-soft", "turbo", 1, -.04, .25),
           ("typing", "2500", 1, -.06, .12), ("click-soft", "charge", 1, -.05, .25), ("typing", "zéro", 1, -.25, .1),
           ("chime", "zéro", 1, .1, .18), ("impact-bass-2", "payé", 1, -.04, .28)]
    return css, st, "", js, (540, 900), sfx


def scene_05():
    css = """
    #§q { position: absolute; left: 745px; top: 905px; width: 80px; text-align: center; font: 84px/1 "Anton", sans-serif; color: #ffffff; opacity: 0; }
    #§ring5 { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; fill: none; stroke: #ffffff; stroke-width: 7; }
    """
    ppl = ""
    for k in range(10):
        r, c = divmod(k, 5)
        ppl += person(f"p{k}", 115 + c * 170, 690 + r * 260, 140)
    st = ('<div class="§floor" style="top:901px"></div><div class="§floor" style="top:1161px"></div>' + ppl
          + '<svg id="§ring5" viewBox="0 0 1080 1920"><circle id="§rc" cx="865" cy="1056" r="120" transform="rotate(-90 865 1056)"/></svg>'
          + '<div id="§q">?</div>')
    hud = title("t5", [odo("n8", "8") + " CLIENTS SUR 10"], 330, 124)
    js = """
      for (var k = 0; k < 10; k++) {
        var p = "p" + k; init(p + "-w", { opacity: 0 }); init(p + "-o", { opacity: 0 }); init(p + "-glow", { opacity: 0 });
        pre(p, { opacity: 0, y: 40 }); go(p, { opacity: 1, y: 0 }, 0.02 + k * 0.05, 0.25, "back.out(1.6)");
      }
      slam("t5-0", at("8") - 0.05, { s: 1.2 }); stroke("t5", at("10") + 0.1);
      var t0 = at("8"), span = Math.max(0.9, at("prennent") + 0.35 - t0);
      odo("n8", t0, span);
      for (var j = 0; j < 8; j++) lit("p" + j, "orange", t0 + j * span / 8, 0.18);
      ["p8", "p9"].forEach(function (p) { lit(p, "white", t0 + span, 0.2); });
      // the one who hesitates while the others have decided
      $("rc").style.opacity = 1; draw("rc", at("pigeon") - 0.05, 0.4, "power2.inOut");
      lit("p8", "dim", at("pigeon"), 0.3);
      pre("q", { opacity: 0, scale: 0.4 }); go("q", { opacity: 1, scale: 1 }, at("hésite") - 0.04, 0.25, "back.out(2.2)");
      wobble("p9", at("hésite") + 0.1, 6);
      for (var m = 0; m < 8; m++) { init("p" + m + "-glow", { scale: 1 }); go("p" + m + "-glow", { scale: 1.25 }, at("tranché") - 0.05 + m * 0.03, 0.2); go("p" + m + "-glow", { scale: 1 }, at("tranché") + 0.2 + m * 0.03, 0.35); }
      cam(-80, -40, 1.1, at("pigeon") - 0.1, 0.7);
    """
    sfx = [("pop", None, 0, 0.02, .12), ("typing", "8", 1, 0, .12)] + [("pop", "8", 1, k * 0.12, .08) for k in range(8)] + [
           ("click", "pigeon", 1, -.05, .25), ("pop", "hésite", 1, -.04, .14), ("sparkle", "tranché", 1, -.05, .2)]
    return css, st, hud, js, (540, 900), sfx


def scene_06():
    css = f"""
    #§say {{ position: absolute; left: 330px; top: 640px; padding: 12px 34px; border-radius: 40px; background: #ffffff; color: #0A0A0A;
      font: 60px/1.15 "Anton", sans-serif; opacity: 0; white-space: nowrap; }}
    #§say i {{ position: absolute; left: 30px; bottom: -16px; width: 30px; height: 30px; background: #fff; transform: rotate(45deg); }}
    #§cal {{ position: absolute; left: 560px; top: 760px; width: 360px; height: 330px; border-radius: 28px; background: #151515; border: 3px solid #2e2e2e; opacity: 0; overflow: hidden; }}
    #§calh {{ position: absolute; left: 0; top: 0; width: 100%; height: 70px; background: #2a2a2a; }}
    .§ring {{ position: absolute; top: -18px; width: 22px; height: 46px; border-radius: 11px; background: #6f6f6f; }}
    #§calv {{ position: absolute; left: 0; top: 86px; width: 100%; text-align: center; font: 150px/1 "Anton", sans-serif; color: #ffffff; }}
    #§calm {{ position: absolute; left: 0; top: 256px; width: 100%; text-align: center; font: 600 34px "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.1em; }}
    #§bill {{ position: absolute; left: 0; top: 520px; width: 1080px; text-align: center; opacity: 0; }}
    #§billt {{ display: inline-block; padding: 6px 22px; border: 6px solid {RED}; border-radius: 12px; font: 54px/1.15 "Anton", sans-serif; color: {RED};
      background: rgba(10,10,10,0.85); transform: rotate(-6deg); }}
    #§billv {{ display: block; margin-top: 18px; font: 130px "Anton", sans-serif; color: {RED}; text-shadow: 0 0 40px rgba(179,38,30,0.45); }}
    #§pr-red {{ position: absolute; left: 160px; top: 770px; width: 240px; height: 360px; opacity: 0; fill: {RED}; }}
    """
    st = ('<div class="§floor"></div>' + person("pr", 160, 770, 240)
          + f'<svg id="§pr-red" viewBox="0 0 200 300">{PERSON}</svg>'
          + '<div id="§say">NON MERCI<i></i></div>'
          + '<div id="§cal"><div id="§calh"></div><i class="§ring" style="left:90px"></i><i class="§ring" style="left:248px"></i>'
            '<div id="§calv">+' + odo("mo", "8") + '</div><div id="§calm">MOIS</div></div>'
          + '<div id="§bill"><span id="§billt">BOÎTE DE VITESSES</span>' + odo("bv", "6 700 €", style="display:block;margin:18px auto 0;width:max-content") + '</div>')
    st = st.replace('style="display:block;margin:18px auto 0;width:max-content"', 'style="display:block;margin:18px auto 0;width:max-content;font:130px Anton,sans-serif;color:' + RED + ';line-height:1.15em;height:1.15em"')
    hud = title("t6", ["IL A DIT NON."], 330, 130) + title("t6b", ["C’EST ARRIVÉ."], 330, 130)
    js = """
      init("pr-o", { opacity: 0 }); init("pr-glow", { opacity: 0 }); pre("pr-w", { opacity: 0.4 });
      pre("pr", { opacity: 0, y: 50 }); go("pr", { opacity: 1, y: 0 }, 0.02, 0.3, "back.out(1.6)");
      pre("say", { opacity: 0, scale: 0.4 }); go("say", { opacity: 1, scale: 1 }, at("non") - 0.06, 0.26, "back.out(2.2)");
      slam("t6-0", at("non")); stroke("t6", at("non") + 0.2);
      // eight months later
      go("say", { opacity: 0, scale: 0.8 }, at("8") - 0.15, 0.2);
      pre("cal", { opacity: 0, y: 60 }); go("cal", { opacity: 1, y: 0 }, at("8") - 0.12, 0.3, "back.out(1.5)");
      odo("mo", at("8") - 0.05, Math.max(0.6, at("tard") + 0.2 - at("8")), { from: "0" });
      wobble("cal", at("tard"), 3);
      // the gearbox: the bill lands on him
      go("pr-red", { opacity: 0.85 }, at("vitesses") - 0.1, 0.4); go("pr-w", { opacity: 0 }, at("vitesses") - 0.1, 0.4);
      pre("bill", { opacity: 0 }); slam("bill", at("boîte") - 0.04, { s: 1.4 });
      odo("bv", 0, 0.01, { from: "0 000", spinLow: false }); odo("bv", at("6700") - 0.06, 0.9);
      shake("shk", at("6700") + 0.6, 10);
      go("cal", { opacity: 0.35 }, at("vitesses"), 0.4);
      cam(0, 10, 1.04, at("vitesses") - 0.1, 0.6);
      // not to scare: because it happened
      go("t6", { opacity: 0, y: -30 }, at("arrivé") - 0.16, 0.14, "power2.in");
      slam("t6b-0", at("arrivé") - 0.02); stroke("t6b", at("arrivé") + 0.2);
      cam(0, 0, 1.02, at("racontes") - 0.1, 0.8, "power2.inOut");
    """
    sfx = [("pop", None, 0, 0.02, .12), ("pop", "non", 1, -.06, .18), ("whoosh-short", "8", 1, -.12, .14),
           ("typing", "8", 1, -.05, .12), ("impact-bass-1", "vitesses", 1, -.1, .3), ("typing", "6700", 1, -.06, .12),
           ("click", "arrivé", 1, -.02, .25)]
    return css, st, hud, js, (300, 940), sfx


def scene_07():
    css = """
    #§chip { position: absolute; left: 0; top: 760px; width: 1080px; text-align: center; opacity: 0; }
    #§chipi { position: relative; display: inline-block; padding: 14px 40px; border-radius: 50px; border: 4px solid #6f6f6f; color: #bdbdbd;
      font: 70px/1.15 "Anton", sans-serif; }
    #§chipx { position: absolute; left: -10px; right: -10px; top: 48%; height: 12px; border-radius: 6px; background: #FB8000; transform: scaleX(0); transform-origin: 0 50%; }
    .§btn { position: absolute; top: 840px; height: 150px; border-radius: 75px; border: 5px solid #ffffff; background: #151515;
      font: 66px/140px "Anton", sans-serif; color: #ffffff; text-align: center; opacity: 0; }
    .§btnhl { position: absolute; left: -5px; top: -5px; right: -5px; bottom: -5px; border-radius: 75px; background: #FB8000; opacity: 0; }
    .§btnt { position: relative; }
    #§ba { left: 70px; width: 440px; } #§bb { left: 560px; width: 380px; }
    #§cur { position: absolute; left: 520px; top: 1080px; width: 70px; height: 90px; overflow: visible; opacity: 0; }
    """
    st = ('<div id="§chip"><span id="§chipi">OUI OU NON ?<i id="§chipx"></i></span></div>'
          '<div id="§ba" class="§btn"><div id="§bahl" class="§btnhl"></div><span class="§btnt">AU COMPTANT</span></div>'
          '<div id="§bb" class="§btn"><div id="§bbhl" class="§btnhl"></div><span class="§btnt">PAR MOIS</span></div>'
          '<svg id="§cur" viewBox="0 0 70 90"><path d="M6 4 L6 70 L22 56 L34 84 L46 78 L34 52 L56 52 Z" fill="#ffffff" stroke="#0A0A0A" stroke-width="5" stroke-linejoin="round"/></svg>')
    hud = title("t7", ["LA SEULE QUESTION", "QUI RESTE"], 290, 116)
    js = """
      pre("chip", { opacity: 0, scale: 0.6 }); go("chip", { opacity: 1, scale: 1 }, at("question") - 0.05, 0.28, "back.out(2)");
      tl.fromTo($("chipx"), { scaleX: 0 }, { scaleX: 1, duration: 0.22, ease: "power4.out", immediateRender: false }, at("prend") + 0.05);
      go("chip", { opacity: 0, y: -40 }, at("c'est") - 0.12, 0.18, "power2.in");
      slam("t7-0", at("c'est")); slam("t7-1", at("comment")); stroke("t7", at("paie"));
      pre("ba", { opacity: 0, y: 60 }); pre("bb", { opacity: 0, y: 60 });
      go("ba", { opacity: 1, y: 0 }, at("paie") - 0.1, 0.3, "back.out(1.6)"); go("bb", { opacity: 1, y: 0 }, at("paie"), 0.3, "back.out(1.6)");
      // the cursor hesitates between the two
      pre("cur", { opacity: 0, x: 0, y: 0 }); go("cur", { opacity: 1 }, at("paie") + 0.2, 0.2);
      init("bahl", { opacity: 0 }); init("bbhl", { opacity: 0 });
      go("cur", { x: -260, y: -130 }, at("comptant") - 0.15, 0.4, "power2.inOut"); go("bahl", { opacity: 0.9 }, at("comptant"), 0.15);
      go("bahl", { opacity: 0 }, at("ou") - 0.05, 0.15);
      go("cur", { x: 210, y: -130 }, at("ou") - 0.05, 0.45, "power2.inOut"); go("bbhl", { opacity: 0.9 }, at("mois"), 0.15);
      go("bbhl", { opacity: 0 }, at("tu") - 0.05, 0.15);
      go("cur", { x: -10, y: -60 }, at("tu") - 0.05, 0.5, "power2.inOut");
      // « tu lui laisses choisir » : both answers are good ones
      go("bahl", { opacity: 0.9 }, at("choisir") - 0.03, 0.2); go("bbhl", { opacity: 0.9 }, at("choisir") + 0.12, 0.2);
      go("cur", { opacity: 0, y: 40 }, at("tout"), 0.3);
      cam(0, -20, 1.05, at("paie"), 0.8);
    """
    sfx = [("pop", "question", 1, -.05, .14), ("click", "prend", 1, .05, .25), ("pop", "c'est", 1, 0, .14),
           ("pop", "paie", 1, -.1, .12), ("click-soft", "comptant", 1, 0, .25), ("click-soft", "mois", 1, 0, .25),
           ("chime", "choisir", 1, 0, .18)]
    return css, st, hud, js, (540, 900), sfx


def scene_08():
    css = f"""
    .§mini {{ position: absolute; top: 720px; width: 250px; height: 300px; border-radius: 26px; background: #151515; border: 3px solid #2e2e2e; opacity: 0; }}
    .§minit {{ position: absolute; left: 0; top: 196px; width: 100%; text-align: center; font: 600 28px "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.06em; }}
    .§miniv {{ position: absolute; left: 0; top: 70px; width: 100%; text-align: center; font: 96px/1.1 "Anton", sans-serif; color: #FB8000; }}
    """
    st = ('<div id="§m0" class="§mini" style="left:110px"><div class="§miniv">0 €</div><div class="§minit">FACTURE</div></div>'
          '<div id="§m1" class="§mini" style="left:400px"><div class="§miniv">8/10</div><div class="§minit">CHIFFRE</div></div>'
          f'<div id="§m2" class="§mini" style="left:690px"><div class="§miniv" style="color:{RED}">6 700 €</div><div class="§minit">HISTOIRE</div></div>')
    st = st.replace('<div class="§miniv" style="color:' + RED + '">6 700 €</div>', '<div class="§miniv" style="color:' + RED + ';font-size:72px;top:84px">6 700 €</div>')
    hud = title("t8", ["UNE PREUVE VAUT", "DIX ARGUMENTS."], 290, 116)
    js = """
      [["m0", "facture"], ["m1", "chiffre"], ["m2", "histoire"]].forEach(function (m) {
        pre(m[0], { opacity: 0, y: 60, scale: 0.9 }); go(m[0], { opacity: 1, y: 0, scale: 1 }, at(m[1]) - 0.06, 0.3, "back.out(1.6)");
      });
      ["m0", "m1", "m2"].forEach(function (m, k) { go(m, { y: 120, scale: 0.86 }, at("preuve") - 0.1 + k * 0.04, 0.4, "power3.inOut"); });
      slam("t8-0", at("preuve") - 0.02); slam("t8-1", at("dix") - 0.02); stroke("t8", at("arguments"));
      cam(0, -10, 1.04, at("preuve"), 0.6);
    """
    sfx = [("pop", "facture", 1, -.06, .14), ("pop", "chiffre", 1, -.06, .14), ("pop", "histoire", 1, -.06, .14),
           ("whoosh-short", "preuve", 1, -.1, .14), ("pop", "dix", 1, 0, .16)]
    return css, st, hud, js, (540, 870), sfx


def scene_09():
    css = """
    .§vends { position: relative; display: inline-block; }
    .§strike { position: absolute; left: -0.08em; right: -0.08em; top: 46%; height: 0.13em; background: #FB8000; border-radius: 999px;
      transform: rotate(-5deg) scaleX(0); transform-origin: 0 50%; }
    #§t9 { transform-origin: 540px 0; }
    #§handle { position: absolute; left: 60px; top: 860px; width: 960px; text-align: center; white-space: nowrap; }
    #§hname { position: relative; display: inline-block; font: 96px/1.2 "Anton", sans-serif; color: #ffffff; opacity: 0; }
    #§pill { position: absolute; left: 50%; top: 175px; transform: translateX(-50%); }
    #§pilli { display: inline-block; padding: 8px 40px; border-radius: 40px; background: #FB8000; color: #0A0A0A; font: 52px/1.25 "Anton", sans-serif; opacity: 0;
      box-shadow: 0 0 46px rgba(251,128,0,0.45); }
    """
    hud = (title("t9", ['NE <span class="§vends">VENDS<i id="§strike" class="§strike"></i></span> PAS.', '<span style="color:#FB8000">MONTRE.</span>'], 600, 170)
           + '<div id="§handle"><span id="§hname">@guillaumeherbin_<i class="§stilt"><i class="§stk" id="§h-s"></i></i></span>'
             '<div id="§pill"><span id="§pilli">S’ABONNER</span></div></div>')
    js = """
      slam("t9-0", Math.max(0.02, at("ne") - 0.02), { s: 1.3 });
      tl.fromTo($("strike"), { scaleX: 0, rotation: -5 }, { scaleX: 1, rotation: -5, duration: 0.2, ease: "power4.out", immediateRender: false }, at("vends") + 0.08);
      slam("t9-1", at("montre") - 0.02, { s: 1.5 }); stroke("t9", at("montre") + 0.2);
      shake("shk", at("montre") + 0.05, 10);
      go("t9", { y: -320, scale: 0.62 }, at("abonne-toi") - 0.15, 0.5, "power3.inOut");
      slam("hname", at("abonne-toi") + 0.1, { s: 1.3 }); stroke("h", at("abonne-toi") + 0.3);
      pre("pilli", { opacity: 0, scale: 0.5 }); go("pilli", { opacity: 1, scale: 1 }, at("pour") - 0.04, 0.3, "back.out(2)");
      init("pilli", { opacity: 1, scale: 1 }); go("pilli", { scale: 1.08 }, at("comme"), 0.15); go("pilli", { scale: 1 }, at("comme") + 0.15, 0.3);
      init("halo", { scale: 1 }); go("halo", { scale: 1.2 }, at("abonne-toi"), 1.2, "sine.inOut");
    """
    sfx = [("pop", "ne", 1, 0, .14), ("click", "vends", 1, .08, .25), ("impact-bass-2", "montre", 1, 0, .28),
           ("notification", "abonne-toi", 1, .05, .25), ("pop", "pour", 1, -.04, .14)]
    return css, "", hud, js, (540, 800), sfx


BUILDERS = [scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07, scene_08, scene_09]


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
