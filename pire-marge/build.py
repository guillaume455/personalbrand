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
   "Ma pire *marge*", "en *16* ans de métier,", "c'est sur une *Ferrari*."]),
 dict(id="02-achat", name="L'achat", window=(3, 13), chunks=[
   "Septembre *2019*.", "J'ai 30 ans.", "Ma première *Ferrari*,", "une 360 Modena,", "*49~000* euros.",
   "Je l'achète sur *photos*.", "Les factures d'entretien~?", "Sur photos *aussi*.", "Je me la fais *livrer*",
   "sans l'avoir vue.", "Le vendeur, je bosse", "avec lui depuis des années.", "Alors je ne vérifie *rien*."]),
 dict(id="03-retour", name="Le retour", window=(13, 22), chunks=[
   "Je la *revends*", "à un particulier", "en quelques semaines.", "Puis il m'*appelle*", "pour un problème", "de moteur qui *chauffe*.",
   "Je ne discute pas,", "je le *rembourse*", "intégralement,", "carte grise comprise,", "et je *rapatrie*",
   "la voiture", "dans mon garage."]),
 dict(id="04-diagnostic", name="Le diagnostic", window=(22, 28), chunks=[
   "*Diagnostic*~:", "joint de *culasse*.", "Sur une Ferrari,", "ça veut dire", "*déposer* le moteur.",
   "Et tant qu'on y est,", "la *distribution*."]),
 dict(id="05-mecano", name="Le mécano", window=(28, 40), chunks=[
   "Je confie le chantier", "à un *mécano*.", "Il commence.", "Puis il *abandonne*,", "moteur ouvert.",
   "Je dois tout reprendre", "à *zéro*~:", "trouver quelqu'un", "capable d'intervenir", "sur place,",
   "dans mon *garage*,", "parce que la voiture", "ne bouge plus.", "Elle reste plus d'un an", "*immobilisée*."]),
 dict(id="06-revente", name="La revente", window=(40, 48), chunks=[
   "Le mécano qui reprend", "le chantier me fait commander", "l'*embrayage* en plus,", "pour anticiper.",
   "Cette fois, j'*écoute*.", "Avril *2023*,", "je la revends", "*50~000* euros", "à l'*export*.",
   "Trois ans et demi", "plus tard.", "Moins *17~000* euros,", "sans compter l'argent", "bloqué pendant",
   "tout ce temps."]),
 dict(id="07-erreurs", name="Mes erreurs", window=(48, 61), chunks=[
   "Mes trois *erreurs*.", "Un~: j'ai acheté", "avec le *cœur*.", "Pas d'essai,", "pas de contrôle,",
   "aucune des vérifications", "que je fais", "sur n'importe quelle occasion.", "La *confiance*,",
   "même après des années,", "ne remplace pas", "un *contrôle*.", "Deux~: j'ai confié", "ce moteur à quelqu'un",
   "qui pensait en être capable.", "Ce type de mécanique", "ne se confie pas", "à tout le *monde*.",
   "Trois~: j'ai cru", "pouvoir gérer ça *seul*,", "sans demander à ceux", "qui savaient *vraiment*."]),
 dict(id="08-cta", name="CTA", window=(61, 66), chunks=[
   "J'ai perdu", "*17~000* euros.", "J'ai gardé les *leçons*.", "*Abonne-toi*", "pour plus de contenu", "comme celui-ci."]),
]
SPOKEN_SYL = {"16": 1, "2019": 5, "30": 2, "360": 5, "49000": 5, "2023": 5, "50000": 3, "17000": 3}
RED = "#B3261E"   # dark red: temperature gauge and cylinder heads only

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
    .§photo { position: absolute; border: 4px solid #FB8000; border-radius: 8px; overflow: hidden; box-shadow: 0 30px 70px rgba(0,0,0,0.6); }
    .§photo img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(0.72) contrast(1.04); }
"""
TOT_CSS = """
    #§tot { position: absolute; right: 50px; top: 226px; text-align: right; transform-origin: 100% 50%; }
    .§totl { font: 600 24px/1 "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.16em; }
    .§totv { font: 70px "Anton", sans-serif; color: #FB8000; margin-top: 4px; }
    .§chip { position: absolute; padding: 6px 24px; border-radius: 30px; background: #FB8000; color: #0A0A0A; font: 50px/1.2 "Anton", sans-serif;
      opacity: 0; white-space: nowrap; }
    .§chips { display: block; font: 600 24px/1 "Instrument Sans", sans-serif; letter-spacing: 0.04em; text-align: center; margin-top: -2px; padding-bottom: 6px; }
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
    .§sprite { position: absolute; border: 4px solid #FB8000; border-radius: 8px; background-repeat: no-repeat; background-size: 600% 600%;
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


def scene_01():
    css = MEDIA_CSS + """
    #§bg { left: 0; top: 0; width: 1080px; height: 1920px; }
    #§bg img { filter: saturate(0.6) brightness(0.38); }
    #§sub1 { position: absolute; left: 0; top: 1060px; width: 1080px; text-align: center; font: 600 56px/1.2 "Instrument Sans", sans-serif;
      color: #d0d0d0; letter-spacing: 0.08em; opacity: 0; }
    #§sub1 b { color: #FB8000; font-weight: 600; }
    """
    st = '<div id="§bg" class="§burst">' + "".join(f'<img src="assets/img/{p}">' for p in ["ph-feux.jpg", "ph-badge.jpg", "ph-profil.jpg", "ph-interieur.jpg"]) + '</div>'
    hud = (title("t1", ["MA PIRE", "MARGE."], 480, 200)
           + '<div id="§sub1"><b>' + odo("y16", "16") + '</b> ANS DE MÉTIER</div>')
    js = MEDIA_JS + """
      var e = at("ferrari"), n = 4, step = Math.max(0.35, (DUR - 0.05) / n);
      burst("bg", [0, step, 2 * step, 3 * step]);
      init("bg", { scale: 1 }); go("bg", { scale: 1.12 }, 0, DUR, "none");
      slam("t1-0", Math.max(0.02, at("ma") - 0.02), { s: 1.4 }); slam("t1-1", at("marge") - 0.04, { s: 1.4 }); stroke("t1", at("marge") + 0.2);
      shake("shk", at("marge") + 0.05, 10);
      pre("sub1", { opacity: 0, y: 30 }); go("sub1", { opacity: 1, y: 0 }, at("16") - 0.06, 0.3); odo("y16", at("16") - 0.06, 0.7);
      go("t1", { scale: 1.06 }, e - 0.05, 0.6, "power2.out");
    """
    sfx = [("impact-bass-1", None, 0, 0.02, .28), ("pop", "marge", 1, -.04, .16), ("typing", "16", 1, -.06, .12),
           ("whoosh-short", "ferrari", 1, -.05, .14)]
    return css, st, hud, js, (540, 760), sfx


def scene_02():
    css = MEDIA_CSS + TOT_CSS + """
    #§phone { position: absolute; left: 110px; top: 610px; width: 340px; height: 640px; border-radius: 46px; background: #050505; border: 6px solid #3a3a3a;
      box-shadow: 0 30px 80px rgba(0,0,0,0.7); opacity: 0; }
    #§scr { left: 14px; top: 46px; width: 300px; height: 540px; border-radius: 10px; background: #141414; }
    #§notch { position: absolute; left: 120px; top: 16px; width: 88px; height: 14px; border-radius: 7px; background: #222; }
    #§carnet { left: 470px; top: 700px; width: 500px; height: 380px; border-radius: 8px; border: 4px solid #FB8000; opacity: 0; background: #1a1a1a; }
    #§carnet img { object-fit: contain; filter: none; }
    #§list { position: absolute; left: 500px; top: 600px; width: 440px; height: 620px; overflow: hidden; opacity: 0;
      -webkit-mask-image: linear-gradient(180deg, transparent 0, #000 14%, #000 86%, transparent 100%); }
    #§lcol { position: absolute; left: 0; top: 0; width: 440px; }
    .§it { position: relative; height: 92px; margin-bottom: 18px; border-radius: 20px; background: #151515; border: 2px solid #2e2e2e;
      font: 40px/92px "Anton", sans-serif; color: #ffffff; padding-left: 78px; white-space: nowrap; }
    .§idoc { position: absolute; left: 22px; top: 22px; width: 40px; height: 48px; fill: none; stroke: #9a9a9a; stroke-width: 3.5; stroke-linejoin: round; }
    .§tick { position: absolute; right: 22px; top: 22px; width: 48px; height: 48px; border-radius: 50%; background: #FB8000; }
    .§tick svg { position: absolute; left: 0; top: 0; width: 48px; height: 48px; fill: none; stroke: #0A0A0A; stroke-width: 7; stroke-linecap: round; stroke-linejoin: round; }
    #§truck { position: absolute; left: 240px; top: 860px; width: 600px; height: 230px; overflow: visible; fill: none; stroke: #ffffff;
      stroke-width: 8; stroke-linejoin: round; stroke-linecap: round; opacity: 0; transform: scaleX(-1); }
    #§nocheck { position: absolute; left: 700px; top: 620px; width: 220px; height: 220px; overflow: visible; fill: none; stroke: #ffffff; stroke-linecap: round; opacity: 0; }
    """
    phones = ["achat.jpg", "ph-interieur.jpg", "ph-moteur19.jpg", "ph-feux.jpg", "ph-roue19.jpg", "achat.jpg"]
    items = "".join(f'<div class="§it">{DOC}{t}<i class="§tick"><svg viewBox="0 0 48 48"><path d="M13 25 L21 33 L36 16"/></svg></i></div>'
                    for t in ITEMS)
    st = ('<div id="§phone"><div id="§notch"></div><div id="§scr" class="§burst">' + "".join(f'<img src="assets/img/{p}">' for p in phones) + '</div></div>'
          '<div id="§carnet" class="§burst">' + "".join(f'<img src="assets/img/carnet{k}.jpg">' for k in [1, 2, 3, 4, 5, 6]) + '</div>'
          f'<div id="§list"><div id="§lcol">{items}</div></div>'
          f'<svg id="§truck" viewBox="0 0 600 230">{TRUCK}</svg>'
          + person("sel", 50, 870, 170) +
          f'<svg id="§nocheck" viewBox="0 0 160 160">{MAG}<path d="M10 150 L150 10" stroke="#FB8000" stroke-width="16"/></svg>')
    hud = title("t2", ["2019. 30 ANS.", "ACHETÉE SUR PHOTOS."], 360, 96) + total("00 000 €")
    js = TOT_JS + MEDIA_JS + """
      totInit("00 000"); pre("tot", { opacity: 0 });
      slam("t2-0", at("2019") - 0.05, { s: 1.3 });
      pre("phone", { opacity: 0, y: 80, rotation: -4 }); go("phone", { opacity: 1, y: 0, rotation: -2 }, 0.1, 0.45, "expo.out");
      // the photos received on the phone, one after the other
      var p0 = at("ferrari") - 0.05, p1 = at("photos", 1), ps = Math.max(0.28, (p1 - p0) / 5);
      burst("scr", [p0, p0 + ps, p0 + 2 * ps, p0 + 3 * ps, p0 + 4 * ps, p1]);
      slam("tot", at("49000") - 0.1, { s: 1.2 }); odo("totv", at("49000") - 0.05, 0.9, { to: "49 000 €" });
      slam("t2-1", at("photos") - 0.05); stroke("t2", at("photos") + 0.2);
      // the service book, straightened, very fast
      var c0 = at("factures") - 0.1, c1 = at("aussi") - 0.05, cs = Math.max(0.16, (c1 - c0) / 6);
      pre("carnet", { opacity: 0, scale: 0.9 }); go("carnet", { opacity: 1, scale: 1 }, c0, 0.15);
      burst("carnet", [c0, c0 + cs, c0 + 2 * cs, c0 + 3 * cs, c0 + 4 * cs, c0 + 5 * cs]);
      go("carnet", { opacity: 0, x: 60 }, c0 + 6 * cs, 0.12);
      // then the maintenance bills, one after the other
      var l0 = c0 + 6 * cs, l1 = at("livrer") - 0.12, lh = 110;
      pre("list", { opacity: 0 }); go("list", { opacity: 1 }, l0, 0.12);
      tl.fromTo($("lcol"), { y: 560 }, { y: -(8 * lh) + 380, duration: Math.max(0.9, l1 - l0), ease: "none", immediateRender: false }, l0);
      // delivered without being seen
      go("phone", { opacity: 0, x: -500 }, at("livrer") - 0.1, 0.4, "power3.in"); go("list", { opacity: 0, x: 400 }, at("livrer") - 0.1, 0.4, "power3.in");
      pre("truck", { opacity: 0, x: 900 }); go("truck", { opacity: 1, x: 0 }, at("livrer"), 0.9, "power3.out");
      init("sel-w", { opacity: 0 }); init("sel-o", { opacity: 0 }); init("sel-glow", { opacity: 0 });
      pre("sel", { opacity: 0, y: 40 }); go("sel", { opacity: 1, y: 0 }, at("vendeur") - 0.05, 0.3, "back.out(1.6)");
      lit("sel", "white", at("bosse"), 0.3);
      pre("nocheck", { opacity: 0, scale: 0.4 }); go("nocheck", { opacity: 1, scale: 1 }, at("rien") - 0.06, 0.25, "back.out(2)");
      cam(0, -10, 1.04, at("livrer"), 0.8);
    """
    sfx = [("pop", "2019", 1, -.05, .14), ("whoosh-short", None, 0, 0.1, .12), ("notification", "ferrari", 1, -.05, .22),
           ("typing", "49000", 1, -.05, .12), ("pop", "photos", 1, -.05, .14), ("whoosh-short", "factures", 1, -.1, .12),
           ("typing", "aussi", 1, -.05, .12), ("whoosh-cinematic", "livrer", 1, 0, .22), ("pop", "vendeur", 1, -.05, .12),
           ("click", "rien", 1, -.06, .25)]
    return css, st, hud, js, (300, 900), sfx


def scene_03():
    css = PHOTO_CSS + MEDIA_CSS + TOT_CSS + f"""
    #§ph {{ left: 90px; top: 620px; width: 900px; height: 470px; }}
    #§hand {{ position: absolute; left: 330px; top: 1000px; width: 420px; height: 224px; overflow: visible; fill: none; stroke: #ffffff; stroke-width: 12;
      stroke-linecap: round; stroke-linejoin: round; opacity: 0; }}
    #§handbg {{ position: absolute; left: 300px; top: 980px; width: 480px; height: 260px; border-radius: 30px; background: rgba(10,10,10,0.9); opacity: 0; }}
    #§dash {{ left: 100px; top: 600px; width: 330px; height: 660px; opacity: 0; }}
    #§ring {{ position: absolute; left: 600px; top: 590px; width: 240px; height: 352px; overflow: visible; fill: none; stroke: #ffffff; stroke-width: 10;
      stroke-linecap: round; stroke-linejoin: round; opacity: 0; }}
    .§wave {{ stroke: #FB8000; }}
    #§gauge {{ position: absolute; left: 500px; top: 940px; width: 450px; height: 300px; overflow: visible; fill: none; stroke-linecap: round; opacity: 0; }}
    #§glab {{ position: absolute; left: 500px; top: 1190px; width: 450px; text-align: center; font: 600 28px "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.1em; opacity: 0; }}
    #§truck {{ position: absolute; left: 240px; top: 880px; width: 600px; height: 230px; overflow: visible; fill: none; stroke: #ffffff;
      stroke-width: 8; stroke-linejoin: round; stroke-linecap: round; opacity: 0; }}
    """
    st = ('<div id="§ph" class="§photo"><img src="assets/img/ph-profil.jpg"></div>'
          '<div id="§handbg"></div><svg id="§hand" viewBox="0 0 300 160">'
          '<path d="M0 50 L26 50 L26 126 L0 126"/><path d="M300 50 L274 50 L274 126 L300 126"/>'
          '<path d="M26 64 L92 64 Q112 64 128 76 L176 108 Q188 117 180 127 Q172 135 160 128 L132 110"/>'
          '<path d="M274 64 L208 64 Q188 64 172 76 L124 110 Q112 119 120 129 Q128 137 140 130 L170 112"/>'
          '<path d="M120 96 L150 118 M106 106 L136 128" stroke="#FB8000"/></svg>'
          '<div id="§dash" class="§sprite" style="background-image:url(assets/img/sp-dash.jpg)"></div>'
          '<svg id="§ring" viewBox="0 0 300 440"><g id="§ringph"><rect x="70" y="80" width="160" height="300" rx="28"/><path d="M128 110 L172 110"/>'
          '<path d="M130 350 L170 350"/></g><path class="§wave" d="M260 140 Q290 180 260 220"/><path class="§wave" d="M40 140 Q10 180 40 220"/>'
          '<path class="§wave" d="M280 110 Q330 180 280 250"/><path class="§wave" d="M20 110 Q-30 180 20 250"/></svg>'
          f'<svg id="§gauge" viewBox="0 0 300 200"><path d="M40 170 A110 110 0 0 1 260 170" stroke="#3a3a3a" stroke-width="20"/>'
          f'<path d="M226 92 A110 110 0 0 1 260 170" stroke="{RED}" stroke-width="20"/>'
          '<line id="§needle" x1="150" y1="170" x2="150" y2="80" stroke="#ffffff" stroke-width="9"/><circle cx="150" cy="170" r="14" fill="#ffffff"/></svg>'
          '<div id="§glab">TEMPÉRATURE MOTEUR</div>'
          f'<svg id="§truck" viewBox="0 0 600 230">{TRUCK}</svg>')
    hud = (title("t3", ["ELLE REVIENT."], 380, 120) + total("49 000 €")
           + chip("c1", 380, 620, "+2 000 €", "CARTE GRISE") + chip("c2", 420, 620, "+800 €", "TRANSPORT"))
    js = TOT_JS + MEDIA_JS + """
      totInit("49 000");
      // sold to a private buyer
      pre("ph", { opacity: 0, scale: 1.08 }); go("ph", { opacity: 1, scale: 1 }, at("revends") - 0.08, 0.4, "expo.out");
      init("ph", { opacity: 1, scale: 1, x: 0 }); go("ph", { x: -30 }, at("revends"), 1.6, "none");
      pre("handbg", { opacity: 0 }); go("handbg", { opacity: 1 }, at("particulier") - 0.1, 0.2);
      pre("hand", { opacity: 0, scale: 0.6 }); go("hand", { opacity: 1, scale: 1 }, at("particulier") - 0.06, 0.35, "back.out(1.8)");
      go("ph", { opacity: 0 }, at("puis") - 0.12, 0.2); go("hand", { opacity: 0 }, at("puis") - 0.12, 0.2); go("handbg", { opacity: 0 }, at("puis") - 0.12, 0.2);
      // he calls: the engine overheats (the real dashboard)
      pre("ring", { opacity: 0, scale: 0.7 }); go("ring", { opacity: 1, scale: 1 }, at("m'appelle") - 0.1, 0.3, "back.out(2)");
      wobble("ringph", at("m'appelle"), 7); wobble("ringph", at("m'appelle") + 0.35, 6);
      pre("dash", { opacity: 0, x: -60 }); go("dash", { opacity: 1, x: 0 }, at("moteur") - 0.15, 0.35, "expo.out");
      sprite("dash", at("moteur") - 0.15, Math.max(1.5, at("rembourse") - at("moteur") + 0.3), 36, 6, 12);
      go("ring", { opacity: 0, scale: 0.8 }, at("moteur") + 0.1, 0.25);
      pre("gauge", { opacity: 0, y: 30 }); go("gauge", { opacity: 1, y: 0 }, at("moteur") - 0.05, 0.3); pre("glab", { opacity: 0 }); go("glab", { opacity: 1 }, at("moteur"), 0.3);
      tl.set($("needle"), { svgOrigin: "150 170", rotation: -70 }, 0);
      tl.fromTo($("needle"), { rotation: -70 }, { rotation: 62, duration: 0.9, ease: "power2.in", immediateRender: false }, at("chauffe") - 0.2);
      wobble("gauge", at("chauffe") + 0.7, 2);
      // full refund: the costs go into the TOTAL
      go("dash", { opacity: 0, x: -60 }, at("rembourse") - 0.15, 0.3); go("gauge", { opacity: 0 }, at("rembourse") - 0.15, 0.3); go("glab", { opacity: 0 }, at("rembourse") - 0.15, 0.3);
      bump("c1", at("carte") - 0.1, "51 000 €");
      // the car comes back on a truck
      pre("truck", { opacity: 0, x: 900 }); go("truck", { opacity: 1, x: 0 }, at("rapatrie") - 0.1, 0.9, "power3.out");
      slam("t3-0", at("rapatrie") - 0.04); stroke("t3", at("rapatrie") + 0.2);
      bump("c2", Math.max(at("rapatrie") + 0.2, at("carte") + 1.6), "51 800 €");
      cam(0, -10, 1.04, at("rapatrie"), 0.8);
    """
    sfx = [("pop", "revends", 1, -.08, .14), ("pop", "particulier", 1, -.06, .14), ("notification", "m'appelle", 1, -.1, .25),
           ("whoosh-short", "moteur", 1, -.15, .12), ("error", "chauffe", 1, .6, .18), ("pop", "carte", 1, -.1, .14),
           ("typing", "carte", 1, 1.0, .12), ("whoosh-cinematic", "rapatrie", 1, -.1, .2), ("pop", "rapatrie", 1, .2, .14)]
    return css, st, hud, js, (540, 880), sfx


def engine_css():
    return f"""
    #§eng {{ position: absolute; left: 140px; top: 640px; width: 800px; height: 560px; overflow: visible; fill: none; stroke-linejoin: round; stroke-linecap: round; }}
    .§eb {{ stroke: #ffffff; stroke-width: 7; fill: #141414; }}
    .§head {{ stroke: #ffffff; stroke-width: 7; fill: #141414; }}
    .§dist circle, .§dist path {{ stroke: #FB8000; stroke-width: 7; fill: none; }}
    #§hoist {{ stroke: #9a9a9a; stroke-width: 6; stroke-dasharray: 10 10; }}
    """



def scene_04():
    css = TOT_CSS + engine_css()
    st = (f'<svg id="§eng" viewBox="0 0 600 420"><path id="§hoist" d="M300 -260 L300 30 M300 30 L180 70 M300 30 L420 70"/>'
          f'<g id="§motor">{ENGINE}{DISTRI}</g></svg>')
    hud = title("t4", ["JOINT DE CULASSE.", "DÉPOSE MOTEUR."], 360, 104) + total("51 800 €")
    js = TOT_JS + f"""
      totInit("51 800");
      pre("eng", {{ opacity: 0, scale: 0.9 }}); go("eng", {{ opacity: 1, scale: 1 }}, 0.02, 0.4, "expo.out");
      slam("t4-0", at("culasse") - 0.05);
      ["hl", "hr"].forEach(function (h, k) {{
        tl.fromTo($(h), {{ fill: "#141414", stroke: "#ffffff" }}, {{ fill: "{RED}", stroke: "{RED}", duration: 0.25, immediateRender: false }}, at("culasse") + k * 0.08);
        tl.fromTo($(h), {{ opacity: 1 }}, {{ opacity: 0.55, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }}, at("culasse") + 0.4);
      }});
      // a Ferrari: the engine comes out
      $("hoist").style.opacity = 0; pre("hoist", {{ opacity: 0 }}); go("hoist", {{ opacity: 1 }}, at("déposer") - 0.15, 0.2);
      go("motor", {{ y: -70 }}, at("déposer"), 0.8, "power2.inOut");
      slam("t4-1", at("déposer") - 0.04); stroke("t4", at("moteur") + 0.1);
      pre("distri", {{ opacity: 0 }}); go("distri", {{ opacity: 1 }}, at("distribution") - 0.15, 0.1);
      draw("belt", at("distribution") - 0.1, 0.5, "power2.inOut");
      cam(0, -20, 1.05, at("déposer"), 0.8);
    """
    sfx = [("pop", None, 0, 0.02, .12), ("error", "culasse", 1, 0, .18), ("pop", "culasse", 1, -.05, .14),
           ("whoosh-short", "déposer", 1, 0, .14), ("click", "distribution", 1, -.1, .25)]
    return css, st, hud, js, (540, 900), sfx




def scene_05():
    css = PHOTO_CSS + MEDIA_CSS + TOT_CSS + """
    #§ph { left: 90px; top: 600px; width: 900px; height: 420px; }
    #§ph2 { left: 140px; top: 620px; width: 800px; height: 560px; opacity: 0; }
    #§gar { left: 320px; top: 590px; width: 330px; height: 660px; opacity: 0; }
    #§mech { opacity: 0; }
    #§wrench { position: absolute; left: 840px; top: 900px; width: 110px; height: 110px; overflow: visible; fill: none; stroke: #ffffff; stroke-width: 10;
      stroke-linecap: round; opacity: 0; }
    #§mag { position: absolute; left: 200px; top: 720px; width: 170px; height: 170px; overflow: visible; fill: none; stroke: #ffffff; stroke-linecap: round; opacity: 0; }
    #§cal { position: absolute; left: 600px; top: 900px; width: 340px; height: 300px; border-radius: 26px; background: #151515; border: 3px solid #2e2e2e; opacity: 0; overflow: hidden; }
    #§calh { position: absolute; left: 0; top: 0; width: 100%; height: 64px; background: #2a2a2a; }
    #§calv { position: absolute; left: 0; top: 76px; width: 100%; text-align: center; font: 140px/1 "Anton", sans-serif; color: #ffffff; }
    #§calm { position: absolute; left: 0; top: 236px; width: 100%; text-align: center; font: 600 32px "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.1em; }
    """
    st = ('<div id="§ph" class="§photo"><img src="assets/img/moteur.jpg"></div>'
          '<div id="§ph2" class="§photo"><img src="assets/img/ph-moteur22.jpg"></div>'
          '<div id="§gar" class="§sprite" style="background-image:url(assets/img/sp-garage.jpg);background-size:900% 300%"></div>'
          + person("mech", 760, 830, 170)
          + '<svg id="§wrench" viewBox="0 0 110 110"><path d="M20 90 L64 46"/><circle cx="76" cy="34" r="20"/></svg>'
          + f'<svg id="§mag" viewBox="0 0 160 160">{MAG}</svg>'
          + '<div id="§cal"><div id="§calh"></div><div id="§calv">' + odo("mo", "14") + '</div><div id="§calm">MOIS</div></div>')
    hud = (title("t5", ["REPRENDRE À ZÉRO."], 380, 110) + title("t5b", ["PLUS D’UN AN", "IMMOBILISÉE."], 350, 100) + total("51 800 €")
           + chip("c3", 330, 1080, "+15 000 €", "MÉCANIQUE"))
    js = TOT_JS + MEDIA_JS + """
      totInit("51 800");
      pre("ph", { opacity: 0, scale: 1.08 }); go("ph", { opacity: 1, scale: 1 }, 0.02, 0.5, "expo.out");
      init("mech-w", { opacity: 0 }); init("mech-o", { opacity: 0 }); init("mech-glow", { opacity: 0 });
      pre("mech", { opacity: 0, y: 40 }); go("mech", { opacity: 1, y: 0 }, at("mécano") - 0.05, 0.3, "back.out(1.6)"); lit("mech", "white", at("mécano"), 0.25);
      pre("wrench", { opacity: 0, rotation: -30 }); go("wrench", { opacity: 1, rotation: 0 }, at("commence") - 0.05, 0.3, "back.out(2)");
      wobble("wrench", at("commence") + 0.3, 12);
      // he gives up, engine open: he fades away; the engine bay, open
      go("mech", { opacity: 0, y: -30 }, at("abandonne"), 0.7, "power2.in"); go("wrench", { opacity: 0, y: 40, rotation: 40 }, at("abandonne") + 0.1, 0.5, "power2.in");
      go("ph", { opacity: 0 }, at("ouvert") - 0.1, 0.2); pre("ph2", { opacity: 0, scale: 1.1 }); go("ph2", { opacity: 1, scale: 1 }, at("ouvert") - 0.1, 0.4, "expo.out");
      slam("t5-0", at("zéro") - 0.05); stroke("t5", at("zéro") + 0.15);
      bump("c3", at("zéro") + 0.2, "66 800 €");
      // looking for someone able to work on site, in my garage
      pre("mag", { opacity: 0, scale: 0.6, x: 0 }); go("mag", { opacity: 1, scale: 1 }, at("trouver") - 0.05, 0.25, "back.out(2)");
      go("mag", { x: 380 }, at("trouver") + 0.2, 0.7, "sine.inOut"); go("mag", { x: 60 }, at("trouver") + 0.95, 0.7, "sine.inOut");
      go("mag", { opacity: 0 }, at("garage") - 0.15, 0.2); go("ph2", { opacity: 0 }, at("garage") - 0.15, 0.25);
      pre("gar", { opacity: 0, scale: 0.92 }); go("gar", { opacity: 1, scale: 1 }, at("garage") - 0.15, 0.35, "expo.out");
      sprite("gar", at("garage") - 0.15, Math.max(1.5, at("elle") - at("garage") + 0.4), 27, 9, 12);
      // more than a year off the road
      go("gar", { opacity: 0, x: -200 }, at("elle") - 0.1, 0.35, "power2.in");
      go("ph2", { opacity: 0.55 }, at("elle") - 0.1, 0.4);
      go("t5", { opacity: 0, y: -30 }, at("elle") - 0.12, 0.14, "power2.in");
      pre("cal", { opacity: 0, y: 60 }); go("cal", { opacity: 1, y: 0 }, at("elle") - 0.1, 0.3, "back.out(1.5)");
      odo("mo", at("elle"), Math.max(1.0, at("immobilisée") + 0.3 - at("elle")), { from: "00" });
      slam("t5b-0", at("an") - 0.05); slam("t5b-1", at("immobilisée") - 0.04); stroke("t5b", at("immobilisée") + 0.2);
      tl.fromTo($("ph2").querySelector("img"), { filter: "saturate(0.72) brightness(1)" }, { filter: "saturate(0.2) brightness(0.6)", duration: 0.8, immediateRender: false }, at("immobilisée") - 0.1);
      cam(0, -10, 1.04, at("trouver"), 0.8);
    """
    sfx = [("whoosh-short", None, 0, 0.02, .12), ("pop", "mécano", 1, -.05, .14), ("click-soft", "commence", 1, 0, .25),
           ("whoosh-short", "abandonne", 1, 0, .12), ("whoosh-short", "ouvert", 1, -.1, .12), ("pop", "zéro", 1, -.05, .14),
           ("typing", "zéro", 1, 1.3, .12), ("whoosh-short", "trouver", 1, .2, .12), ("whoosh-short", "garage", 1, -.15, .12),
           ("typing", "elle", 1, 0, .12), ("impact-bass-2", "immobilisée", 1, -.04, .26)]
    return css, st, hud, js, (540, 820), sfx


def scene_06():
    css = PHOTO_CSS + MEDIA_CSS + TOT_CSS + engine_css() + """
    #§eng { left: 240px; top: 640px; width: 600px; height: 420px; }
    #§clutch { stroke: #FB8000; stroke-width: 7; fill: none; }
    #§ok { position: absolute; left: 860px; top: 660px; width: 90px; height: 90px; border-radius: 50%; background: #FB8000; opacity: 0; }
    #§ok svg { position: absolute; left: 0; top: 0; width: 90px; height: 90px; fill: none; stroke: #0A0A0A; stroke-width: 11; stroke-linecap: round; stroke-linejoin: round; }
    #§ph { left: 120px; top: 640px; width: 840px; height: 565px; border: 4px solid #FB8000; border-radius: 8px; box-shadow: 0 30px 70px rgba(0,0,0,0.6); opacity: 0; }
    #§face { position: absolute; left: 80px; top: 620px; width: 920px; height: 600px; opacity: 0; }
    .§col { position: absolute; top: 0; width: 430px; height: 300px; border-radius: 28px; background: #151515; border: 2px solid #2e2e2e; }
    .§coll { position: absolute; left: 0; top: 40px; width: 100%; text-align: center; font: 600 32px "Instrument Sans", sans-serif; color: #9a9a9a; letter-spacing: 0.1em; }
    .§colv { position: absolute; left: 0; top: 110px; width: 100%; text-align: center; font: 96px "Anton", sans-serif; color: #ffffff; }
    #§res { position: absolute; left: 0; top: 350px; width: 920px; text-align: center; font: 190px "Anton", sans-serif; color: #FB8000; opacity: 0; }
    .§minus { display: inline-block; width: 0.42em; height: 0.11em; margin-right: 0.12em; background: #FB8000; vertical-align: 0.5em; border-radius: 0.05em; }
    """
    st = (f'<svg id="§eng" viewBox="0 0 600 420"><g id="§motor">{ENGINE}{DISTRI}</g>'
          '<g id="§clg"><circle id="§clutch" cx="520" cy="320" r="62"/><circle cx="520" cy="320" r="22" stroke="#FB8000" stroke-width="7" fill="none"/>'
          '<path d="M520 258 L520 298 M520 342 L520 382 M458 320 L498 320 M542 320 L582 320" stroke="#FB8000" stroke-width="7"/></g></svg>'
          '<div id="§ok"><svg viewBox="0 0 90 90"><path d="M24 46 L39 61 L66 32"/></svg></div>'
          '<div id="§ph" class="§burst">' + "".join(f'<img src="assets/img/{p}">' for p in ["ph-retro.jpg", "ph-jante.jpg", "ph-interieur22.jpg", "export.jpg"]) + '</div>'
          '<div id="§face"><div class="§col" style="left:0"><div class="§coll">DÉPENSÉ</div><div class="§colv">' + odo("dep", "66 800 €") + '</div></div>'
          '<div class="§col" style="left:490px"><div class="§coll">ENCAISSÉ</div><div class="§colv">' + odo("enc", "50 000 €") + '</div></div>'
          '<div id="§res"><i class="§minus"></i>' + odo("rv", "16 800 €") + '</div></div>')
    hud = title("t6", ["AVRIL 2023.", "50 000 €. EXPORT."], 360, 104) + total("66 800 €")
    js = TOT_JS + MEDIA_JS + """
      totInit("66 800");
      tl.set($("distri"), { opacity: 1 }, 0);
      pre("eng", { opacity: 0, scale: 0.9 }); go("eng", { opacity: 1, scale: 1 }, 0.02, 0.4, "expo.out");
      pre("clg", { opacity: 0 }); go("clg", { opacity: 1 }, at("l'embrayage") - 0.12, 0.1);
      draw("clutch", at("l'embrayage") - 0.1, 0.5, "power2.inOut");
      tl.fromTo($("clg"), { rotation: 0, svgOrigin: "520 320" }, { rotation: 180, svgOrigin: "520 320", duration: 1.6, ease: "power2.out", immediateRender: false }, at("l'embrayage") + 0.3);
      pre("ok", { opacity: 0, scale: 2.2 }); go("ok", { opacity: 1, scale: 1 }, at("j'écoute") - 0.05, 0.16, "expo.in");
      // April 2023: one last look at the car, sold for export
      go("eng", { opacity: 0, y: -40 }, at("avril") - 0.2, 0.25, "power2.in"); go("ok", { opacity: 0 }, at("avril") - 0.2, 0.2);
      var a0 = at("avril") - 0.1, a1 = at("50000") - 0.05, as = Math.max(0.22, (a1 - a0) / 3);
      pre("ph", { opacity: 0, scale: 1.06 }); go("ph", { opacity: 1, scale: 1 }, a0, 0.3, "expo.out");
      burst("ph", [a0, a0 + as, a0 + 2 * as, a1]);
      slam("t6-0", at("avril") - 0.04); slam("t6-1", at("50000") - 0.05); stroke("t6", at("l'export"));
      // spent vs cashed in
      go("t6", { opacity: 0, y: -30 }, at("trois") - 0.12, 0.14, "power2.in");
      go("ph", { opacity: 0, scale: 0.9 }, at("trois") - 0.1, 0.3, "power2.in");
      pre("face", { opacity: 0, y: 60 }); go("face", { opacity: 1, y: 0 }, at("trois"), 0.35, "back.out(1.4)");
      odo("dep", at("trois") + 0.1, 0.8, { from: "00 000" }); odo("enc", at("trois") + 0.25, 0.8, { from: "00 000" });
      pre("res", { opacity: 0, scale: 1.4 }); go("res", { opacity: 1, scale: 1 }, at("moins") - 0.06, 0.2, "expo.out");
      odo("rv", at("moins") - 0.06, 0.9, { from: "00 000" });
      shake("shk", at("17000") + 0.3, 10);
      cam(0, -10, 1.04, at("trois"), 0.8);
    """
    sfx = [("pop", None, 0, 0.02, .12), ("click-soft", "l'embrayage", 1, -.1, .25), ("pop", "j'écoute", 1, -.05, .16),
           ("whoosh-short", "avril", 1, -.1, .14), ("pop", "50000", 1, -.05, .14), ("typing", "trois", 1, .1, .12),
           ("impact-bass-1", "moins", 1, -.06, .3)]
    return css, st, hud, js, (540, 900), sfx


def scene_07():
    css = TOT_CSS + """
    .§err { position: absolute; left: 80px; width: 920px; height: 180px; border-radius: 28px; background: #151515; border: 2px solid #2e2e2e; opacity: 0; }
    .§errn { position: absolute; left: 28px; top: 50px; width: 80px; height: 80px; border-radius: 50%; background: #FB8000; color: #0A0A0A;
      font: 56px/80px "Anton", sans-serif; text-align: center; }
    .§errt { position: absolute; left: 136px; top: 0; width: 760px; height: 180px; display: flex; align-items: center;
      font: 54px/1.15 "Anton", sans-serif; color: #ffffff; }
    .§k { color: #ffffff; }
    """
    lines = [("e1", 600, "ACHETÉE AVEC LE <span id='§k1' class='§k'>CŒUR</span>, <span id='§k1b' class='§k'>SANS CONTRÔLE</span>."),
             ("e2", 810, "PAS À <span id='§k2' class='§k'>N’IMPORTE QUEL MÉCANO</span>."),
             ("e3", 1020, "J’AI VOULU GÉRER <span id='§k3' class='§k'>SEUL</span>.")]
    st = "".join(f'<div id="§{i}" class="§err" style="top:{y}px"><div class="§errn">{k + 1}</div><div class="§errt"><div>{t}</div></div></div>'
                 for k, (i, y, t) in enumerate(lines))
    hud = title("t7", ["MES TROIS ERREURS"], 380, 116) + total("66 800 €")
    js = TOT_JS + """
      totInit("66 800");
      slam("t7-0", Math.max(0.02, at("mes") - 0.02)); stroke("t7", at("erreurs"));
      var cues = [at("un"), at("deux"), at("trois", 2)];
      ["e1", "e2", "e3"].forEach(function (e, k) {
        pre(e, { opacity: 0, x: -80 }); go(e, { opacity: 1, x: 0 }, cues[k] - 0.06, 0.35, "expo.out");
        if (k > 0) go(["e1", "e2"][k - 1], { opacity: 0.4 }, cues[k] - 0.06, 0.3);
      });
      var keys = [["k1", at("cœur")], ["k1b", at("contrôle")], ["k2", at("monde")], ["k3", at("seul")]];
      keys.forEach(function (kk) { tl.fromTo($(kk[0]), { color: "#ffffff" }, { color: "#FB8000", duration: 0.2, immediateRender: false }, kk[1] - 0.04); });
      init("e3", { opacity: 1 }); go("e1", { opacity: 1 }, at("vraiment") + 0.3, 0.4); go("e2", { opacity: 1 }, at("vraiment") + 0.3, 0.4);
      cam(0, -10, 1.04, at("deux"), 1.0);
    """
    sfx = [("pop", "mes", 1, 0, .14), ("whoosh-short", "un", 1, -.06, .14), ("whoosh-short", "deux", 1, -.06, .14),
           ("whoosh-short", "trois", 2, -.06, .14), ("click-soft", "contrôle", 2, -.04, .22), ("click-soft", "monde", 1, -.04, .22),
           ("click-soft", "seul", 1, -.04, .22)]
    return css, st, hud, js, (540, 900), sfx




def scene_08():
    css = MEDIA_CSS + """
    #§hap { left: 0; top: 0; width: 1080px; height: 1920px; border: none; border-radius: 0; box-shadow: none; background-size: 1000% 600%; filter: saturate(0.85); }
    #§shade { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px;
      background: linear-gradient(180deg, rgba(10,10,10,0.75) 0%, rgba(10,10,10,0.25) 30%, rgba(10,10,10,0) 50%, rgba(10,10,10,0.35) 62%, rgba(10,10,10,0.9) 80%, rgba(10,10,10,0.95) 100%); }
    #§handle { position: absolute; left: 60px; top: 380px; width: 960px; text-align: center; white-space: nowrap; }
    #§hname { position: relative; display: inline-block; font: 96px/1.2 "Anton", sans-serif; color: #ffffff; opacity: 0; text-shadow: 0 4px 30px rgba(0,0,0,0.6); }
    #§pill { position: absolute; left: 50%; top: 175px; transform: translateX(-50%); }
    #§pilli { display: inline-block; padding: 8px 40px; border-radius: 40px; background: #FB8000; color: #0A0A0A; font: 52px/1.25 "Anton", sans-serif; opacity: 0;
      box-shadow: 0 0 46px rgba(251,128,0,0.45); }
    .§title { text-shadow: 0 4px 30px rgba(0,0,0,0.6); }
    """
    st = '<div id="§hap" class="§sprite" style="background-image:url(assets/img/sp-happy.jpg)"></div><div id="§shade"></div>'
    hud = (title("t8", ["JE ME SUIS", "FAIT AVOIR."], 330, 130)
           + '<div id="§handle"><span id="§hname">@guillaumeherbin_<i class="§stilt"><i class="§stk" id="§h-s"></i></i></span>'
             '<div id="§pill"><span id="§pilli">S’ABONNER</span></div></div>')
    js = MEDIA_JS + """
      // happy end: the car on the road, on the day it was sold (plate blurred)
      tl.set($("hap"), { backgroundPosition: "0% 0%" }, 0);
      sprite("hap", 0, DUR, 60, 10, Math.max(12, Math.min(15, 60 / DUR)));
      slam("t8-0", at("gardé") - 0.05); slam("t8-1", at("leçons") - 0.05); stroke("t8", at("leçons") + 0.2);
      go("t8", { opacity: 0, y: -40 }, at("abonne-toi") - 0.14, 0.15, "power2.in");
      slam("hname", at("abonne-toi"), { s: 1.3 }); stroke("h", at("abonne-toi") + 0.2);
      pre("pilli", { opacity: 0, scale: 0.5 }); go("pilli", { opacity: 1, scale: 1 }, at("pour") - 0.06, 0.3, "back.out(2)");
    """
    sfx = [("whoosh-cinematic", None, 0, 0.02, .2), ("pop", "gardé", 1, -.05, .14), ("pop", "leçons", 1, -.05, .14),
           ("notification", "abonne-toi", 1, 0, .25), ("pop", "pour", 1, -.06, .14)]
    return css, st, hud, js, (540, 700), sfx


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
