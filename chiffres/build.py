#!/usr/bin/env python3
"""Reel « Le marché VO en 5 chiffres » : one source for the whole film.

Every animation of every scene is placed on a WORD of the voice (at("virement"), at("même", 2)...), never on a fixed
second. The word timings come from one file:
  - assets/audio/voix-montage-mots.json when the real voice is there (align.py writes it), or
  - a provisional timing spread over the brief's windows (0-5, 5-15, 15-26, 26-36, 36-45, 45-56, 56-60 s).
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
   "*Cinq* chiffres", "sur le marché", "de l'*occasion* en France.", "Si t'es", "dans l'*auto*,", "tu dois les *connaître*."]),
 dict(id="02-volume", name="Chiffre 1 · le volume", window=(5, 15), chunks=[
   "Un~:", "*5,5~millions*", "de voitures d'occasion", "vendues l'an dernier.", "Plus de *trois* occasions", "pour une neuve.",
   "Ce que ça *change*~:", "le marché est là,", "il est *énorme*,", "et il ne dépend pas", "des *concessions*."]),
 dict(id="03-qui-vend", name="Chiffre 2 · qui vend", window=(15, 26), chunks=[
   "Deux~:", "*47~%* des ventes", "se font entre *particuliers*.", "Les pros", "n'en font que *44*.", "Ce que ça *change*~:",
   "près d'une voiture sur deux", "se vend *sans* passer", "par un professionnel.", "C'est un marché", "à *prendre*,",
   "pas un marché saturé."]),
 dict(id="04-age", name="Chiffre 3 · l'âge", window=(26, 36), chunks=[
   "Trois~:", "*11~ans* d'âge moyen,", "et ça *vieillit*", "chaque année.", "Près d'une voiture vendue", "sur *trois*",
   "a plus de 15~ans.", "Ce que ça *change*~:", "le vrai volume", "est sur les voitures", "*pas~chères*.",
   "Pas sur les récentes."]),
 dict(id="05-prix", name="Chiffre 4 · le prix", window=(36, 45), chunks=[
   "Quatre~:", "*20~200~euros*", "de prix moyen,", "en *baisse*", "de près de 4~%", "sur un an.", "Ce que ça *change*~:",
   "les prix *descendent*.", "Si tu achètes", "au prix d'hier,", "tu revends à *perte*", "demain."]),
 dict(id="06-delai", name="Chiffre 5 · le délai", window=(45, 56), chunks=[
   "Cinq~:", "*147~jours*.", "C'est le temps moyen", "qu'une voiture thermique", "reste chez un marchand", "avant d'être vendue.",
   "Cinq *mois*.", "Ce que ça *change*~:", "si tu tournes", "en *30~jours*,", "tu es cinq fois", "plus *rapide* que le marché.",
   "C'est là", "que se fait l'*écart*."]),
 dict(id="07-cta", name="Récap et CTA", window=(56, 60), chunks=[
   "*Abonne-toi*", "pour plus de contenu", "comme celui-ci."]),
]
SPOKEN_SYL = {"55millions": 6, "47": 5, "44": 4, "11ans": 2, "15ans": 2, "paschères": 2, "20200euros": 6, "4": 3,
              "147jours": 6, "30jours": 3}
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



NUM_CSS = """
    @font-face { font-family: "Space Mono"; src: url("assets/fonts/SpaceMono-700.woff2") format("woff2"); font-weight: 700; }
    #§main { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 540px 280px; }
    #§kick { position: absolute; left: 0; top: 280px; width: 1080px; text-align: center; font: 700 36px/1 "Space Mono", monospace; color: #FB8000; letter-spacing: 0.1em; opacity: 0; }
    #§bigw { position: absolute; left: 0; top: 330px; width: 1080px; text-align: center; font: 230px/1.15 "Anton", sans-serif; color: #ffffff; white-space: nowrap; opacity: 0; }
    #§src { position: absolute; left: 0; top: 612px; width: 1080px; text-align: center; font: 600 26px/1 "Instrument Sans", sans-serif; color: #8a8a8a; letter-spacing: 0.14em; opacity: 0; }
    #§chg { position: absolute; left: 90px; top: 650px; width: 900px; height: 40px; }
    #§chgl, #§chgr { position: absolute; top: 18px; height: 5px; width: 200px; background: #FB8000; border-radius: 3px; transform: scaleX(0); }
    #§chgl { left: 0; transform-origin: 100% 50%; } #§chgr { right: 0; transform-origin: 0 50%; }
    #§chgt { position: absolute; left: 0; top: 0; width: 900px; text-align: center; font: 700 36px/40px "Instrument Sans", sans-serif; color: #FB8000; letter-spacing: 0.12em; opacity: 0; }
    .§minus { display: inline-block; width: 0.34em; height: 0.085em; background: currentColor; vertical-align: 0.3em; margin-right: 0.05em; border-radius: 0.04em; }
    .§or { color: #FB8000; }
    .§lab { position: absolute; font: 700 30px/1 "Instrument Sans", sans-serif; letter-spacing: 0.1em; }
"""

NUM_JS = """
      // the figure: kicker, counter rolling 0 -> value in 1 s, source
      function figure(t, oid, from, dim) {
        pre("kick", { opacity: 0, y: 20 }); go("kick", { opacity: 1, y: 0 }, Math.max(0.02, t - 0.35), 0.3);
        if (oid) { pre("bigw", { opacity: 0, scale: 0.7 }); go("bigw", { opacity: 1, scale: 1 }, t - 0.08, 0.35, "back.out(1.6)");
          odo(oid, t - 0.05, 1.0, { from: from, dimLead: !!dim }); }
        pre("src", { opacity: 0 }); go("src", { opacity: 1 }, t + 0.9, 0.4);
      }
      // title line by line (slam), stroke under the last line
      function tshow(tid, n, cues) { for (var i = 0; i < n; i++) slam(tid + "-" + i, cues[i] - 0.05); stroke(tid, cues[n - 1] + 0.18); init(tid + "-s", { scaleX: 1 }); }
      function thide(tid, n, t) { for (var i = 0; i < n; i++) go(tid + "-" + i, { opacity: 0 }, t, 0.2); go(tid + "-s", { scaleX: 0 }, t, 0.2); }
      // « ce que ça change »: the figure shrinks up, the orange line opens under it
      function change(t, gone) {
        gone.forEach(function (id) { go(id, { opacity: 0 }, t - 0.2, 0.2); });
        init("main", { scale: 1, y: 0 }); go("main", { scale: 0.72, y: -10 }, t - 0.15, 0.5, "power3.inOut");
        tl.fromTo($("chgl"), { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power3.out", immediateRender: false }, t + 0.1);
        tl.fromTo($("chgr"), { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power3.out", immediateRender: false }, t + 0.1);
        pre("chgt", { opacity: 0, y: 10 }); go("chgt", { opacity: 1, y: 0 }, t + 0.05, 0.3);
      }
"""


def numframe(k, big, source):
    """main group (shrinks on « change »): kicker, big counter, source"""
    return (f'<div id="§kick">{k} / 5</div>'
            + (f'<div id="§bigw">{big}</div>' if big else "")
            + f'<div id="§src">SOURCE · {source}</div>')


def main(html):
    return f'<div id="§main">{html}</div>'


CHG = '<div id="§chg"><i id="§chgl"></i><i id="§chgr"></i><div id="§chgt">CE QUE ÇA CHANGE</div></div>'


def scene_01():
    css = NUM_CSS + """
    .§tile { position: absolute; top: 900px; width: 150px; height: 180px; border-radius: 22px; background: #151515; border: 3px solid #2e2e2e;
      text-align: center; font: 110px/180px "Anton", sans-serif; color: #3a3a3a; opacity: 0; }
    """
    st = "".join(f'<div id="§tl{i}" class="§tile" style="left:{75 + i * 190}px">{i + 1}</div>' for i in range(5))
    hud = (title("t1", ["5 CHIFFRES."], 520, 230)
           + title("t2", ["SI T'ES DANS L'AUTO,"], 560, 100) + title("t3", ["TU DOIS LES", "CONNAÎTRE."], 500, 120))
    js = NUM_JS + """
      slam("t1-0", Math.max(0.02, at("cinq") - 0.05), { s: 1.4 }); stroke("t1", at("chiffres") + 0.1);
      for (var i = 0; i < 5; i++) { pre("tl" + i, { opacity: 0, y: 40 }); go("tl" + i, { opacity: 1, y: 0 }, at("marché") - 0.1 + i * 0.07, 0.3, "back.out(1.8)"); }
      // the hook: you must know them
      thide("t1", 1, at("si") - 0.15);
      slam("t2-0", at("l'auto") - 0.25); stroke("t2", at("l'auto") + 0.1);
      thide("t2", 1, at("tu") - 0.12);
      tshow("t3", 2, [at("tu"), at("connaître")]);
      for (var j = 0; j < 5; j++) {
        tl.fromTo($("tl" + j), { color: "#3a3a3a", borderColor: "#2e2e2e" }, { color: "#FB8000", borderColor: "#FB8000", duration: 0.15, immediateRender: false }, at("connaître") + j * 0.08);
      }
      cam(0, -10, 1.03, at("l'auto"), 0.8);
    """
    sfx = [("impact-bass-2", "cinq", 1, -.05, .22), ("pop", "marché", 1, -.1, .12), ("whoosh-short", "l'auto", 1, -.25, .14),
           ("pop", "connaître", 1, 0, .14)]
    return css, st, hud, js, (540, 760), sfx


def scene_02():
    css = NUM_CSS + """
    #§beam { position: absolute; left: 180px; top: 1080px; width: 720px; height: 12px; border-radius: 6px; background: #ffffff; transform-origin: 50% 50%; opacity: 0; }
    #§post { position: absolute; left: 532px; top: 1086px; width: 16px; height: 110px; background: #ffffff; opacity: 0; }
    #§base { position: absolute; left: 470px; top: 1190px; width: 140px; height: 10px; border-radius: 5px; background: #ffffff; opacity: 0; }
    .§pan { position: absolute; top: 940px; width: 280px; height: 140px; }
    .§pan .§car { opacity: 0; }
    #§pL { left: 60px; } #§pR { left: 740px; }
    """
    st = main(numframe(1, odo("vol", "5 500 000"), "SDES, 2025")
          + title("c1", ["VOITURES D'OCCASION", "VENDUES EN 2025"], 690, 64)
          + title("c2", ['<span class="§or">3 OCCASIONS</span> POUR 1 NEUVE'], 700, 72)
          + '<div id="§beam"></div><div id="§post"></div><div id="§base"></div>'
          + '<div id="§pL" class="§pan">' + car("u1", 0, 80, 140, "#FB8000", 13) + car("u2", 140, 80, 140, "#FB8000", 13)
          + car("u3", 70, 18, 140, "#FB8000", 13) + '</div>'
          + '<div id="§pR" class="§pan">' + car("n1", 55, 68, 170, "#8a8a8a", 12) + '</div>'
          + '<div id="§lo" class="§lab" style="left:130px;top:1112px;color:#FB8000;opacity:0">OCCASION</div>'
          + '<div id="§ln" class="§lab" style="left:832px;top:1112px;color:#8a8a8a;opacity:0">NEUVE</div>')
    hud = CHG + title("k1", ["LE MARCHÉ EST <span class=\"§or\">ÉNORME</span>.", "SANS LES CONCESSIONS."], 740, 84)
    js = NUM_JS + """
      figure(at("55millions"), "vol", "0 000 000", true);
      tshow("c1", 2, [at("voitures"), at("vendues")]);
      // the scale: 3 used cars outweigh 1 new
      thide("c1", 2, at("trois") - 0.25);
      slam("c2-0", at("trois") - 0.05);
      ["beam", "post", "base"].forEach(function (b) { pre(b, { opacity: 0 }); go(b, { opacity: 1 }, at("plus") - 0.1, 0.3); });
      ["u1", "u2", "u3"].forEach(function (c, i) { pre(c, { opacity: 0, y: -60 }); go(c, { opacity: 1, y: 0 }, at("trois") + i * 0.1, 0.3, "back.out(1.6)"); });
      pre("lo", { opacity: 0 }); go("lo", { opacity: 1 }, at("trois") + 0.2, 0.3);
      pre("n1", { opacity: 0, y: -60 }); go("n1", { opacity: 1, y: 0 }, at("neuve") - 0.1, 0.3, "back.out(1.6)");
      pre("ln", { opacity: 0 }); go("ln", { opacity: 1 }, at("neuve"), 0.3);
      init("beam", { rotation: 0 }); go("beam", { rotation: -9 }, atEnd("neuve") - 0.1, 0.6, "back.out(1.4)");
      init("pL", { y: 0 }); go("pL", { y: 50 }, atEnd("neuve") - 0.1, 0.6, "back.out(1.4)");
      init("pR", { y: 0 }); go("pR", { y: -50 }, atEnd("neuve") - 0.1, 0.6, "back.out(1.4)");
      init("lo", { y: 0 }); go("lo", { y: 50 }, atEnd("neuve") - 0.1, 0.6, "back.out(1.4)");
      init("ln", { y: 0 }); go("ln", { y: -50 }, atEnd("neuve") - 0.1, 0.6, "back.out(1.4)");
      // what it changes
      change(at("change"), ["c2-0", "c2-s", "beam", "post", "base", "pL", "pR", "lo", "ln"]);
      tshow("k1", 2, [at("énorme"), at("concessions")]);
    """
    sfx = [("typing", "55millions", 1, -.05, .1), ("pop", "trois", 1, 0, .12), ("pop", "neuve", 1, -.1, .12),
           ("click-soft", "neuve", 1, .3, .2), ("whoosh-short", "change", 1, -.15, .14), ("impact-bass-2", "énorme", 1, -.05, .2)]
    return css, st, hud, js, (540, 700), sfx


def scene_03():
    css = NUM_CSS + """
    .§bar { position: absolute; bottom: 800px; width: 220px; border-radius: 16px 16px 4px 4px; transform-origin: 50% 100%; transform: scaleY(0); }
    #§bP { left: 230px; height: 490px; background: #5a5a5a; } #§bR { left: 630px; height: 458px; background: #FB8000; }
    .§pct { position: absolute; width: 360px; text-align: center; font: 120px/1 "Anton", sans-serif; opacity: 0; }
    #§vP { left: 160px; top: 480px; color: #ffffff; } #§vR { left: 560px; top: 512px; color: #FB8000; }
    .§bl { position: absolute; top: 1140px; width: 360px; text-align: center; font: 50px/1 "Anton", sans-serif; opacity: 0; }
    #§lP { left: 160px; color: #9a9a9a; } #§lR { left: 560px; color: #FB8000; }
    #§src { top: 1215px; }
    """
    st = main(numframe(2, None, "NGC-DATA, 2025")
          + '<div id="§bP" class="§bar"></div><div id="§bR" class="§bar"></div>'
          + '<div id="§vP" class="§pct">' + odo("oP", "47 %") + '</div><div id="§vR" class="§pct">' + odo("oR", "44 %") + '</div>'
          + '<div id="§lP" class="§bl">PARTICULIERS</div><div id="§lR" class="§bl">PROS</div>')
    hud = (CHG + title("k1", ["PRÈS D'1 SUR 2", "<span class=\"§or\">SANS</span> PRO."], 740, 100)
           + title("k2", ["UN MARCHÉ <span class=\"§or\">À PRENDRE</span>.", "PAS SATURÉ."], 740, 92))
    js = NUM_JS + """
      figure(at("47"), null);
      // two bars: individuals 47 %, pros 44 %
      tl.fromTo($("bP"), { scaleY: 0 }, { scaleY: 1, duration: 1.0, ease: "power3.out", immediateRender: false }, at("47") - 0.05);
      pre("vP", { opacity: 0, y: 30 }); go("vP", { opacity: 1, y: 0 }, at("47") - 0.08, 0.3); odo("oP", at("47") - 0.05, 1.0);
      pre("lP", { opacity: 0 }); go("lP", { opacity: 1 }, at("particuliers") - 0.1, 0.3);
      tl.fromTo($("bR"), { scaleY: 0 }, { scaleY: 1, duration: 1.0, ease: "power3.out", immediateRender: false }, at("pros") - 0.05);
      pre("lR", { opacity: 0 }); go("lR", { opacity: 1 }, at("pros") - 0.05, 0.3);
      pre("vR", { opacity: 0, y: 30 }); go("vR", { opacity: 1, y: 0 }, at("44") - 0.08, 0.3); odo("oR", at("44") - 0.05, 1.0);
      // what it changes
      change(at("change"), ["bP", "bR", "vP", "vR", "lP", "lR"]);
      init("src", { y: 0 }); go("src", { y: -600 }, at("change") - 0.15, 0.5, "power3.inOut");
      tshow("k1", 2, [at("près"), at("sans")]);
      thide("k1", 2, at("c'est") - 0.15);
      tshow("k2", 2, [at("prendre"), at("saturé")]);
    """
    sfx = [("typing", "47", 1, -.05, .1), ("pop", "particuliers", 1, -.1, .12), ("typing", "44", 1, -.05, .1),
           ("whoosh-short", "change", 1, -.15, .14), ("pop", "sans", 1, -.05, .14), ("impact-bass-2", "prendre", 1, -.05, .2)]
    return css, st, hud, js, (540, 760), sfx


def scene_04():
    css = NUM_CSS + """
    #§pie { position: absolute; left: 150px; top: 880px; width: 300px; height: 300px; overflow: visible; opacity: 0; }
    #§pv { position: absolute; left: 500px; top: 870px; font: 140px/1 "Anton", sans-serif; color: #FB8000; opacity: 0; }
    #§pl { position: absolute; left: 504px; top: 1050px; font: 54px/1.15 "Anton", sans-serif; color: #ffffff; opacity: 0; }
    #§up { position: absolute; left: 720px; top: 680px; width: 90px; height: 90px; overflow: visible; opacity: 0; }
    """
    st = main(numframe(3, odo("age", "11,1") + " ANS", "SDES, 2025") + title("c1", ["ÂGE MOYEN"], 690, 72)
          + '<svg id="§up" viewBox="0 0 120 120"><path d="M10 100 L60 50 L80 70 L110 30" fill="none" stroke="#FB8000" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><path d="M84 28 L112 26 L110 54" fill="none" stroke="#FB8000" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>'
          + '<svg id="§pie" viewBox="0 0 300 300"><circle cx="150" cy="150" r="150" fill="#2a2a2a"/>'
            '<circle id="§sl" cx="150" cy="150" r="75" fill="none" stroke="#FB8000" stroke-width="150" stroke-dasharray="0 471.24" transform="rotate(-90 150 150)"/></svg>'
          + '<div id="§pv">' + odo("p30", "30 %") + '</div><div id="§pl">ONT PLUS<br>DE 15 ANS</div>')
    hud = CHG + title("k1", ["LE VRAI VOLUME :", "LES <span class=\"§or\">PAS CHÈRES</span>."], 740, 96)
    js = NUM_JS + """
      figure(at("11ans"), "age", "00,0");
      slam("c1-0", at("moyen") - 0.05); stroke("c1", at("moyen") + 0.15);
      // it gets older every year
      pre("up", { opacity: 0, scale: 0.4 }); go("up", { opacity: 1, scale: 1 }, at("vieillit") - 0.05, 0.3, "back.out(2)");
      // the pie: 30 % are over 15
      thide("c1", 1, at("près") - 0.15);
      pre("pie", { opacity: 0, scale: 0.6 }); go("pie", { opacity: 1, scale: 1 }, at("près") - 0.1, 0.35, "back.out(1.6)");
      tl.fromTo($("sl"), { attr: { "stroke-dasharray": "0 471.24" } }, { attr: { "stroke-dasharray": "141.37 471.24" }, duration: 0.8, ease: "power3.out", immediateRender: false }, at("trois", 2) - 0.05);
      pre("pv", { opacity: 0, x: 30 }); go("pv", { opacity: 1, x: 0 }, at("trois", 2) - 0.08, 0.3); odo("p30", at("trois", 2) - 0.05, 0.8);
      pre("pl", { opacity: 0, x: 30 }); go("pl", { opacity: 1, x: 0 }, at("15ans") - 0.1, 0.3);
      // what it changes
      change(at("change"), ["pie", "pv", "pl", "up"]);
      tshow("k1", 2, [at("volume"), at("paschères")]);
    """
    sfx = [("typing", "11ans", 1, -.05, .1), ("pop", "vieillit", 1, -.05, .12), ("pop", "trois", 1, -.05, .12),
           ("whoosh-short", "change", 1, -.15, .14), ("impact-bass-2", "paschères", 1, -.05, .2)]
    return css, st, hud, js, (540, 700), sfx


def scene_05():
    css = NUM_CSS + """
    #§bigw { font-size: 220px; }
    #§chart { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; pointer-events: none; }
    #§dot { opacity: 0; }
    """
    st = main(numframe(4, odo("px", "20 200") + " €", "LA CENTRALE, 2025") + title("c1", ["PRIX MOYEN"], 690, 72)
          + title("c2", ['<span class="§or"><i class="§minus"></i>3,7 %</span> EN UN AN'], 690, 80)
          + '<svg id="§chart" viewBox="0 0 1080 1920"><path id="§ln" d="M150 900 L290 925 L410 905 L530 975 L650 990 L770 1070 L890 1130" fill="none" stroke="#FB8000" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
            '<g transform="translate(890 1130) rotate(26)"><path id="§lnh" d="M-34 -24 L0 0 L-34 24" fill="none" stroke="#FB8000" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" opacity="0"/></g>'
            '<path id="§base" d="M150 1180 L930 1180" stroke="#2e2e2e" stroke-width="4"/></svg>')
    hud = (CHG + title("k1", ["LES PRIX", "<span class=\"§or\">DESCENDENT</span>."], 740, 110)
           + title("k2", ["ACHAT D'HIER,", "<span class=\"§or\">PERTE</span> DEMAIN."], 740, 110))
    js = NUM_JS + """
      figure(at("20200euros"), "px", "00 000", true);
      slam("c1-0", at("moyen") - 0.05); stroke("c1", at("moyen") + 0.15);
      // down 3.7 % in a year
      thide("c1", 1, at("baisse") - 0.2);
      slam("c2-0", at("baisse") - 0.05); stroke("c2", at("4") + 0.1);
      draw("ln", at("baisse") - 0.05, 1.2, "power2.inOut");
      pre("lnh", { opacity: 0 }); go("lnh", { opacity: 1 }, at("baisse") + 1.1, 0.1);
      // what it changes
      change(at("change"), ["c2-0", "c2-s", "chart"]);
      tshow("k1", 2, [at("prix", 2), at("descendent")]);
      thide("k1", 2, at("si") - 0.15);
      tshow("k2", 2, [at("d'hier"), at("perte")]);
    """
    sfx = [("typing", "20200euros", 1, -.05, .1), ("whoosh-short", "baisse", 1, -.05, .14), ("whoosh-short", "change", 1, -.15, .14),
           ("pop", "descendent", 1, -.05, .14), ("impact-bass-2", "perte", 1, -.05, .2)]
    return css, st, hud, js, (540, 700), sfx


MONTHS = ["JANVIER", "FÉVRIER", "MARS", "AVRIL", "MAI"]


def scene_06():
    css = NUM_CSS + """
    #§cal { position: absolute; left: 370px; top: 870px; width: 340px; height: 320px; border-radius: 24px; background: #151515; border: 3px solid #2e2e2e; overflow: hidden; opacity: 0; }
    #§calh { position: absolute; left: 0; top: 0; width: 100%; height: 84px; background: #FB8000; }
    .§mo { position: absolute; left: 0; top: 0; width: 100%; text-align: center; font: 52px/84px "Anton", sans-serif; color: #0A0A0A; opacity: 0; }
    #§cald { position: absolute; left: 0; top: 112px; width: 100%; text-align: center; font: 150px/1.15 "Anton", sans-serif; color: #ffffff; }
    .§rail { position: absolute; left: 260px; height: 64px; border-radius: 10px; transform-origin: 0 50%; transform: scaleX(0); }
    #§rM { top: 760px; width: 600px; background: #5a5a5a; } #§rT { top: 860px; width: 122px; background: #FB8000; }
    .§rl { position: absolute; left: 60px; width: 180px; text-align: right; font: 46px/64px "Anton", sans-serif; opacity: 0; }
    .§rv { position: absolute; font: 50px/64px "Anton", sans-serif; opacity: 0; }
    """
    st = main(numframe(5, odo("days", "147") + " JOURS", "MOBILIANS / AAA DATA, 2026") + title("c1", ["DÉLAI MOYEN CHEZ UN PRO"], 690, 66)
          + '<div id="§cal"><div id="§calh">' + "".join(f'<div id="§m{i}" class="§mo">{m}</div>' for i, m in enumerate(MONTHS))
          + '<div id="§m5" class="§mo">5 MOIS</div></div><div id="§cald">' + odo("cd", "147") + '</div></div>')
    hud = (CHG + '<div id="§lM" class="§rl" style="top:760px;color:#9a9a9a">MARCHÉ</div><div id="§lT" class="§rl" style="top:860px;color:#FB8000">TOI</div>'
           + '<div id="§rM" class="§rail"></div><div id="§rT" class="§rail"></div>'
           + '<div id="§vM" class="§rv" style="left:880px;top:760px;color:#9a9a9a">147 J</div><div id="§vT" class="§rv" style="left:402px;top:860px;color:#FB8000">30 J</div>'
           + title("k1", ["5 FOIS PLUS <span class=\"§or\">RAPIDE</span>."], 990, 100))
    js = NUM_JS + """
      figure(at("147jours"), "days", "000");
      slam("c1-0", at("moyen") - 0.05); stroke("c1", at("moyen") + 0.15);
      // a calendar runs almost five months
      thide("c1", 1, at("thermique") - 0.2);
      pre("cal", { opacity: 0, scale: 0.7 }); go("cal", { opacity: 1, scale: 1 }, at("thermique") - 0.15, 0.35, "back.out(1.6)");
      var t0 = at("thermique") + 0.1, t1 = at("mois") - 0.1, step = (t1 - t0) / 5;
      for (var i = 0; i < 5; i++) { pre("m" + i, { opacity: 0 }); go("m" + i, { opacity: 1 }, t0 + i * step, 0.05); if (i < 4) go("m" + i, { opacity: 0 }, t0 + (i + 1) * step, 0.05); }
      odo("cd", t0, t1 - t0, { from: "000" });
      go("m4", { opacity: 0 }, at("mois") - 0.05, 0.1); pre("m5", { opacity: 0 }); go("m5", { opacity: 1 }, at("mois") - 0.05, 0.15);
      init("cal", { scale: 1 }); go("cal", { scale: 1.08 }, at("mois") - 0.05, 0.12); go("cal", { scale: 1 }, at("mois") + 0.07, 0.3);
      // what it changes: 30 days against 147
      change(at("change"), ["cal"]);
      ["lM", "vM"].forEach(function (e) { pre(e, { opacity: 0 }); go(e, { opacity: 1 }, at("tournes") - 0.1, 0.3); });
      tl.fromTo($("rM"), { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.out", immediateRender: false }, at("tournes") - 0.1);
      ["lT", "vT"].forEach(function (e) { pre(e, { opacity: 0 }); go(e, { opacity: 1 }, at("30jours") - 0.05, 0.3); });
      tl.fromTo($("rT"), { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power3.out", immediateRender: false }, at("30jours") - 0.05);
      tshow("k1", 1, [at("cinq", 3)]);
      init("k1", { scale: 1 }); go("k1", { scale: 1.08 }, at("l'écart") - 0.05, 0.15); go("k1", { scale: 1 }, at("l'écart") + 0.1, 0.3);
    """
    sfx = [("typing", "147jours", 1, -.05, .1), ("pop", "thermique", 1, -.15, .12), ("typing", "thermique", 1, .1, .08),
           ("click-soft", "mois", 1, -.05, .2), ("whoosh-short", "change", 1, -.15, .14), ("pop", "30jours", 1, -.05, .14),
           ("impact-bass-2", "rapide", 1, -.05, .2)]
    return css, st, hud, js, (540, 700), sfx


RECAP = ["5,5 M", "47 %", "11 ANS", "20 200 €", "147 J"]


def scene_07():
    css = """
    .§rc { position: absolute; left: 0; width: 1080px; text-align: center; font: 120px/1.15 "Anton", sans-serif; color: #ffffff; opacity: 0; }
    #§rline { position: absolute; left: 0; top: 250px; width: 1080px; text-align: center; font: 50px/1.2 "Anton", sans-serif; color: #ffffff; white-space: nowrap; opacity: 0; }
    #§rline b { font-weight: 400; color: #FB8000; }
    #§handle { position: absolute; left: 60px; top: 1040px; width: 960px; text-align: center; white-space: nowrap; }
    #§hname { position: relative; display: inline-block; font: 96px/1.2 "Anton", sans-serif; color: #ffffff; opacity: 0; }
    #§pill { position: absolute; left: 50%; top: 175px; transform: translateX(-50%); }
    #§pilli { display: inline-block; padding: 8px 40px; border-radius: 40px; background: #FB8000; color: #0A0A0A; font: 52px/1.25 "Anton", sans-serif; opacity: 0;
      box-shadow: 0 0 46px rgba(251,128,0,0.45); }
    #§me { position: absolute; left: 240px; top: 360px; width: 600px; height: 740px; overflow: hidden; opacity: 0;
      -webkit-mask-image: linear-gradient(#000 72%, transparent 100%); mask-image: linear-gradient(#000 72%, transparent 100%); }
    #§me img { position: absolute; left: 0; top: 0; width: 600px; height: auto; }
    #§meglow { position: absolute; left: 290px; top: 340px; width: 500px; height: 500px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, rgba(251,128,0,0.55) 0%, rgba(251,128,0,0.18) 45%, rgba(251,128,0,0) 70%); }
    """
    st = '<div id="§meglow"></div><div id="§me"><img src="assets/img/guillaume.png"></div>'
    hud = ("".join(f'<div id="§r{i}" class="§rc" style="top:{300 + i * 150}px{";color:#FB8000" if i == 4 else ""}">{v}</div>'
                   for i, v in enumerate(RECAP))
           + '<div id="§rline">' + ' <b>·</b> '.join(RECAP[:4]) + ' <b>·</b> <b>147 J</b></div>'
           + '<div id="§handle"><span id="§hname">@guillaumeherbin_<i class="§stilt"><i class="§stk" id="§h-s"></i></i></span>'
             '<div id="§pill"><span id="§pilli">S’ABONNER</span></div></div>')
    js = """
      // the five figures line up in a column, then fold into one line on top
      for (var i = 0; i < 5; i++) { pre("r" + i, { opacity: 0, scale: 1.6 }); go("r" + i, { opacity: 1, scale: 1 }, 0.02 + i * 0.07, 0.25, "expo.out"); }
      var tc = Math.max(0.9, at("pour") - 0.1);
      for (var j = 0; j < 5; j++) go("r" + j, { opacity: 0, scale: 0.4, y: 250 - (300 + j * 150) }, tc, 0.35, "power3.in");
      pre("rline", { opacity: 0, scale: 0.8 }); go("rline", { opacity: 1, scale: 1 }, tc + 0.25, 0.3, "back.out(1.6)");
      // subscribe: the photo, the handle, the button
      pre("me", { opacity: 0, y: 60 }); go("me", { opacity: 1, y: 0 }, tc + 0.2, 0.6, "power3.out");
      pre("meglow", { opacity: 0, scale: 0.6 }); go("meglow", { opacity: 1, scale: 1 }, tc + 0.3, 0.7, "power2.out");
      slam("hname", tc + 0.3, { s: 1.3 }); stroke("h", tc + 0.5);
      pre("pilli", { opacity: 0, scale: 0.5 }); go("pilli", { opacity: 1, scale: 1 }, tc + 0.6, 0.3, "back.out(2)");
      init("halo", { scale: 1 }); go("halo", { scale: 1.2 }, 0, DUR, "sine.inOut");
    """
    sfx = [("pop", None, 0, 0.02, .12), ("whoosh-short", "pour", 1, -.1, .14), ("notification", "pour", 1, .3, .25)]
    return css, st, hud, js, (540, 700), sfx


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
message: "Cinq chiffres du marché VO en France (volume, qui vend, âge, prix, délai) et ce que chacun change pour quelqu'un qui se lance ; retiens surtout le dernier : 147 jours de délai moyen chez un pro."
arc: Hook → Volume → Qui vend → Âge → Prix → Délai → Récap + CTA
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
- **Negative list** : aucun billet ni espèce ; jamais plus de 6 mots par bloc de texte ; aucune photo d'illustration (tout est dessiné) ; chaque chiffre porte sa source en gris ; « CE QUE ÇA CHANGE » en ligne orange.

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
