#!/usr/bin/env python3
"""Reel « 139 891 km sur une voiture plaisir » (Jaguar F-Type, 2019): one source for the whole film.

Every animation of every scene is placed on a WORD of the voice (at("belge"), at("600euros", 2)...), never on a
fixed second. The word timings come from one file:
  - assets/audio/voix-montage-mots.json when Guillaume's voice is there (align.py writes it), or
  - a provisional timing spread over the brief's windows (scene windows below).
So when the voice arrives (or changes), run: python3 build-voice.py && python3 align.py && python3 place-voice.py
&& python3 build.py && bash assemble.sh, and every scene, subtitle and sound effect lands back on the voice.

Usage: python3 build.py [--provisional]
Writes: compositions/frames/*.html, STORYBOARD.md, timings.json, assets/audio/sfx-events.json
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
REAL = "assets/audio/voix-montage-mots.json"
TAIL = 2.0          # hold after the last word (end card)
FPS = 30
HOOK = 3.0          # the hook: the odometer and its line (place-voice.py pads it if the voice is shorter)

# ---------------------------------------------------------------------------------------------------------------------
# The voice, scene by scene, cut into subtitle chunks (2 to 5 words, 42 characters max). *word* = key word (orange).
# ~ glues two tokens into one subtitle word (« 54~000~km »). Numbers are spoken in letters by the voice.
SCENES = [
 dict(id="01-hook", name="Hook", window=(0, 3.6), speak=(0.15, 3.3), chunks=[
   "139~891~kilomètres.", "Sur une voiture plaisir."]),
 dict(id="02-fuite", name="Pourquoi tout le monde fuit", window=(3.6, 14.5), speak=(3.8, 14.1), chunks=[
   "Une Jaguar F-Type", "cabriolet S,", "V6 3~litres compressé,", "380~chevaux,", "de mai 2014.", "Sur ce genre de voiture,",
   "la valeur tient", "au *kilométrage*,", "parce que ce sont", "des voitures de week-end.", "140~000,", "c'est le double",
   "de ce qu'un acheteur accepte.", "Donc tout le monde", "passe son tour."]),
 dict(id="03-carpass", name="La révélation, le Car-Pass", window=(14.5, 29), speak=(14.7, 25.6), chunks=[
   "Sauf que cette voiture", "était *belge*.", "Et en Belgique,", "il existe un document", "que la plupart des Français",
   "ne connaissent pas,", "le *Car-Pass*.", "À chaque passage", "chez un professionnel,", "le kilométrage est relevé",
   "et enregistré.", "Le vendeur a", "l'*obligation~légale*", "de le remettre à l'acheteur,", "et il se vérifie en ligne."]),
 dict(id="04-nuance", name="La nuance", window=(29, 35), speak=(29.2, 34.6), chunks=[
   "Ce n'est pas *infaillible*.", "Les interventions faites", "hors de Belgique", "n'y figurent pas.",
   "Mais c'est ce qui se fait", "de mieux en Europe", "contre le compteur trafiqué."]),
 dict(id="05-engage", name="Ce que j'ai engagé", window=(35, 43.5), speak=(35.2, 43.1), chunks=[
   "Juillet 2019.", "30~000~euros", "chez un marchand partenaire.", "600~euros de transport", "pour me la faire livrer.",
   "600~euros de révision.", "31~200", "*engagés*."]),
 dict(id="06-revente", name="La revente", window=(43.5, 50.5), speak=(43.7, 50.1), chunks=[
   "90 jours plus tard,", "elle part à 36~200.", "6~200~euros de marge.", "C'est ce que", "tout le monde calcule.",
   "Et c'est *faux*."]),
 dict(id="07-vraie-marge", name="La vraie marge", window=(50.5, 63.5), speak=(50.7, 63.1), chunks=[
   "Moins le transport.", "Moins la révision.", "Et la *TVA*,", "j'ai collecté", "6~033~euros sur la vente,",
   "j'en avais déjà récupéré", "5~200", "sur l'achat et les frais.", "Il m'en reste", "833 à reverser.", "Au final,",
   "4~167~euros.", "Pas 6~200."]),
 dict(id="08-rendement", name="Le chiffre que personne ne regarde", window=(63.5, 71.5), speak=(63.7, 71.1), chunks=[
   "4~167~euros", "sur 31~200 engagés,", "en 90 jours.", "Et surtout,", "aucun retour,", "aucun *service~après-vente*",
   "à gérer."]),
 dict(id="09-lecon", name="La leçon", window=(71.5, 80.5), speak=(71.8, 80.1), chunks=[
   "Le kilométrage", "n'était pas le risque.", "Le risque,", "c'aurait été de ne pas", "pouvoir le *prouver*.",
   "Un compteur élevé", "avec un historique complet", "se vend.", "Un compteur bas", "sans historique, non."]),
 dict(id="10-cta", name="Qui je suis et CTA", window=(80.5, 87), speak=(80.7, 85.2), chunks=[
   "Moi c'est Guillaume~Herbin,", "je suis dans l'automobile", "depuis 2010.", "Suis-moi si tu veux voir",
   "plus de contenus", "comme celui-ci."]),
]
SPOKEN_SYL = {"139891kilomètres": 15, "f-type": 3, "v6": 3, "3litres": 3, "380chevaux": 8, "2014": 4, "140000": 4,
              "car-pass": 2, "2019": 4, "30000euros": 5, "600euros": 4, "31200": 6, "90": 4, "36200": 6, "6200euros": 6,
              "6033euros": 7, "5200": 4, "833": 6, "4167euros": 9, "6200": 4, "obligationlégale": 6,
              "serviceaprès-vente": 6, "2010": 3, "guillaumeherbin": 4, "tva": 3}
PAUSE_AFTER = {"03-carpass": 2.6}   # seconds of silence after the scene's last word (place-voice.py): the text card


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
# shared components (§ = the frame's id prefix, r1- ... r9-)

SHARED_CSS = r"""
    @font-face { font-family: "Oswald"; src: url("assets/fonts/Oswald-var.woff2") format("woff2"); font-weight: 200 700; }
    #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; color: #ffffff; background: #0A0A0A;
      font-family: "Oswald", sans-serif; -webkit-font-smoothing: antialiased; }
    .§ground { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; background: #0A0A0A; overflow: hidden; }
    .§grain { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0.04; mix-blend-mode: screen; pointer-events: none;
      background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='g'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%25' height='100%25' filter='url(%23g)'/></svg>");
      background-size: 240px 240px; }
    .§cam { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 540px 900px; }
    .§hudcam { transform-origin: 540px 700px; }

    /* title: Oswald bold caps, white, centred, orange stroke drawn under the last line (6 frames) */
    .§title { position: absolute; left: 40px; width: 1000px; text-align: center; font-family: "Oswald", sans-serif; font-weight: 700;
      line-height: 1.12; text-transform: uppercase; color: #ffffff; white-space: nowrap; text-shadow: 0 4px 26px rgba(0,0,0,0.55); }
    .§tline { position: relative; display: inline-block; opacity: 0; }
    .§stilt { position: absolute; left: -0.06em; right: -0.06em; bottom: -0.04em; height: 0.09em; display: block;
      transform: rotate(-1.2deg); transform-origin: 0 50%; }
    .§stk { position: absolute; left: 0; top: 0; width: 100%; height: 100%; display: block; background: #FB8000;
      border-radius: 999px; clip-path: polygon(0 0, 100% 32%, 100% 68%, 0 100%); transform-origin: 0 50%; transform: scaleX(0); }

    /* cash-register counter: one rolling column per digit */
    .§odo { display: inline-block; white-space: nowrap; line-height: 1.15em; height: 1.15em; vertical-align: top; }
    .§oc { display: inline-block; height: 1.15em; overflow: hidden; vertical-align: top; }
    .§ocol { display: block; }
    .§ocol span { display: block; height: 1.15em; line-height: 1.15em; text-align: center; }
    .§os { display: inline-block; height: 1.15em; line-height: 1.15em; vertical-align: top; }

    /* subtitles: bottom of the text at 12 % of the height from the bottom (y 1690), white, soft shadow, key word orange */
    .§sub { position: absolute; left: 0; top: 1565px; width: 1080px; height: 140px; pointer-events: none; }
    .§chunk { position: absolute; left: 40px; top: 55px; width: 1000px; text-align: center; white-space: nowrap;
      font: 500 58px/70px "Oswald", sans-serif; color: #ffffff; text-shadow: 0 2px 4px rgba(0,0,0,0.55), 0 4px 22px rgba(0,0,0,0.6); }
    .§w { display: inline-block; opacity: 0; }

    /* photos: full frame, 90 % desaturated, slow zoom 3 to 5 % */
    .§full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; opacity: 0; }
    .§full img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(0.1) contrast(1.06); }
    .§shade { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; pointer-events: none;
      background: linear-gradient(rgba(10,10,10,0.88) 0%, rgba(10,10,10,0.62) 22%, rgba(10,10,10,0.1) 38%, rgba(10,10,10,0) 62%, rgba(10,10,10,0.8) 100%); }
    .§txt { position: absolute; left: 0; width: 1080px; text-align: center; font-family: "Oswald", sans-serif; font-weight: 700;
      text-transform: uppercase; color: #fff; white-space: nowrap; opacity: 0; }
    .§o { color: #FB8000; }
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




CUR = {}


def cue(w, n=1):
    hits = [x for x in CUR["W"] if x[0] == w]
    if len(hits) < n:
        raise SystemExit(f"build: scene {CUR['id']}: cue {w} #{n} not in the voice")
    return hits[n - 1][1]


def last_end():
    return CUR["W"][-1][2]


X_JS = """
      // text: fast fade (6 frames), the orange stroke draws left to right in 6 frames
      function fin(id, t, d) { pre(id, { opacity: 0 }); go(id, { opacity: 1 }, t, d || 0.2, "none"); }
      function fout(id, t, d) { go(id, { opacity: 0 }, t, d || 0.2, "none"); }
      function stroke6(tid, t) { tl.fromTo($(tid + "-s"), { scaleX: 0 }, { scaleX: 1, duration: 0.2, ease: "none", immediateRender: false }, Math.max(0, t)); init(tid + "-s", { scaleX: 1 }); }
      function tin(tid, n, t, d) { for (var i = 0; i < n; i++) fin(tid + "-" + i, t, d); stroke6(tid, t + (d || 0.2)); }
      function tout(tid, n, t) { for (var i = 0; i < n; i++) fout(tid + "-" + i, t); go(tid + "-s", { scaleX: 0 }, t, 0.2, "none"); }
      // punch: a short zoom-out kick of the stage and the texts on a beat (Instagram rhythm)
      function punch(t, k) { k = k || 0.05; ["hp", "shk"].forEach(function (id) { tl.fromTo($(id), { scale: 1 + k }, { scale: 1, duration: 0.32, ease: "expo.out", immediateRender: false }, Math.max(0, t)); }); }
      // photos: fade in, slow zoom (k = 1.03 to 1.05) until t2
      function photo(id, t, t2, k, op) { pre(id, { opacity: 0, scale: 1 }); go(id, { opacity: op || 1 }, t, 0.25, "none"); go(id, { scale: k || 1.04 }, t, Math.max(0.5, (t2 || DUR) - t), "none"); }
"""


def full(fid, src, pos="50% 50%", contain=False):
    """a photo over the whole frame; contain = the photo whole on a blurred, darkened copy of itself"""
    if not contain:
        return f'<div id="§{fid}" class="§full"><img src="assets/img/{src}" style="object-position:{pos}"></div>'
    return (f'<div id="§{fid}" class="§full"><img src="assets/img/{src}" style="filter:saturate(0.1) blur(28px) brightness(0.45);transform:scale(1.15)">'
            f'<img src="assets/img/{src}" style="object-fit:contain;object-position:{pos}"></div>')


# ---------------------------------------------------------------------------------------------------------------------
# the 10 scenes: (css, stage html, hud html [titles, cards], js, halo, sfx [(name, cue word, occurrence, offset, volume)])

RED = "#E03131"
BIG = 'position: absolute; left: 0; width: 1080px; text-align: center; font-family: "Oswald", sans-serif; font-weight: 700; white-space: nowrap; opacity: 0;'


def scene_01():
    css = f"""
    #§km {{ {BIG} top: 640px; font-size: 220px; line-height: 1; color: #fff; opacity: 1; }}
    #§kmu {{ {BIG} top: 880px; font-size: 64px; color: #8c8c8c; letter-spacing: 0.3em; opacity: 1; }}
    """
    hud = ('<div id="§km">' + odo("od", "139 891") + '</div><div id="§kmu">KM</div>'
           + title("t1", ["SUR UNE", "VOITURE PLAISIR."], 1060, 120))
    js = X_JS + """
      // the odometer runs flat out from the first frame, then freezes on 139 891
      odo("od", 0, 1.25, { from: "000 000" });
      tl.fromTo($("km"), { scale: 1.08, filter: "blur(3px)" }, { scale: 1, filter: "blur(0px)", duration: 1.25, ease: "power2.out", immediateRender: false }, 0);
      punch(1.25, 0.05); shake("km", 1.25, 8);
      tin("t1", 2, Math.max(1.35, at("sur") - 0.1)); punch(Math.max(1.35, at("sur") - 0.1), 0.04);
    """
    return css, "", hud, js, None, [("impact-bass-1", None, 1, 1.25, 0.45)]


def scene_02():
    css = f"""
    #§cv {{ position: absolute; left: 90px; top: 520px; width: 900px; height: 700px; opacity: 0; }}
    #§cv svg {{ position: absolute; left: 0; top: 0; width: 900px; height: 700px; overflow: visible; }}
    .§ax {{ font: 600 34px "Oswald", sans-serif; fill: #8c8c8c; }}
    .§lb {{ font: 700 40px "Oswald", sans-serif; }}
    """
    st = (full("ph1", "jag-01.jpg", contain=True) + full("ph2", "jag-04.jpg", contain=True) + full("ph3", "jag-11.jpg", "45% 50%")
          + '<div class="§shade"></div><div id="§blk" style="position:absolute;left:0;top:0;width:1080px;height:1920px;background:#0A0A0A;opacity:0"></div>')
    curve = ('<svg viewBox="0 0 900 700">'
             '<path d="M60 40 L60 600 L880 600" stroke="#4a4a4a" stroke-width="4" fill="none"/>'
             '<text class="§ax" x="0" y="30">VALEUR</text><text class="§ax" x="800" y="650">KM</text>'
             '<path id="§lim" d="M330 600 L330 60" stroke="#8c8c8c" stroke-width="3" stroke-dasharray="12 10" fill="none" opacity="0"/>'
             '<text id="§liml" class="§lb" x="250" y="660" fill="#bdbdbd" opacity="0">70 000</text>'
             '<path id="§crv" d="M60 90 C 220 100, 300 170, 380 300 S 560 540, 860 575" stroke="#FB8000" stroke-width="9" fill="none" stroke-linecap="round"/>'
             f'<path id="§cur" d="M820 600 L820 60" stroke="{RED}" stroke-width="4" stroke-dasharray="12 10" fill="none" opacity="0"/>'
             f'<circle id="§dot" cx="820" cy="572" r="18" fill="{RED}" opacity="0"/>'
             f'<text id="§curl" class="§lb" x="720" y="660" fill="{RED}" opacity="0">140 000</text></svg>')
    hud = (title("t1", ["JAGUAR F-TYPE", "CABRIOLET S"], 300, 110) + title("t2", ["V6 3.0 COMPRESSÉ", "380 CH"], 300, 110)
           + title("t3", ["MAI 2014"], 300, 140) + title("t4", ["LA VALEUR", "SUIT LE KILOMÉTRAGE"], 270, 84)
           + f'<div id="§cv">{curve}</div>' + title("t5", ["× 2"], 1290, 130, "color:#E03131")
           + title("t6", ["TOUT LE MONDE PASSE."], 270, 90))
    js = X_JS + """
      // the car: 3/4 front, 3/4 rear top down, the leather
      tl.set($("ph1"), { opacity: 1 }, 0); photo("ph1", 0, at("v6"), 1.04);
      tin("t1", 2, Math.max(0.05, at("jaguar") - 0.1)); punch(Math.max(0.05, at("jaguar") - 0.1), 0.04);
      tout("t1", 2, at("v6") - 0.25); photo("ph2", at("v6") - 0.15, at("mai"), 1.04); tin("t2", 2, at("v6") - 0.05); punch(at("v6") - 0.15, 0.04);
      tout("t2", 2, at("mai") - 0.25); photo("ph3", at("mai") - 0.15, at("valeur"), 1.05); tin("t3", 1, at("mai") - 0.05); punch(at("mai") - 0.15, 0.04);
      // the value curve falls as the mileage climbs
      tout("t3", 1, at("valeur") - 0.35); go("blk", { opacity: 1 }, at("valeur") - 0.3, 0.25, "none");
      tin("t4", 2, at("valeur") - 0.1); fin("cv", at("valeur") - 0.1); draw("crv", at("valeur"), 1.1, "power2.inOut");
      fin("lim", at("kilométrage")); fin("liml", at("kilométrage"));
      // 140 000: twice what a buyer accepts
      fin("cur", at("140000") - 0.1); fin("curl", at("140000") - 0.1);
      pre("dot", { opacity: 0, scale: 0.2 }); go("dot", { opacity: 1, scale: 1 }, at("140000") - 0.1, 0.3, "back.out(2)"); punch(at("140000") - 0.1, 0.04);
      tin("t5", 1, at("double") - 0.1); punch(at("double") - 0.1, 0.05);
      tout("t4", 2, at("passe") - 0.3); tin("t6", 1, at("passe") - 0.1);
    """
    return css, st, hud, js, None, [("pop", "140000", 1, -0.1, 0.3)]


ROWS_CP = [("03/2015", "24 518"), ("04/2016", "51 207"), ("05/2017", "78 934"), ("06/2018", "104 662"), ("05/2019", "131 045"),
           ("07/2019", "139 891")]


def scene_03():
    css = """
    #§doc { position: absolute; left: 150px; top: 430px; width: 780px; height: 860px; border-radius: 22px; background: #ecebe7; opacity: 0;
      box-shadow: 0 30px 80px rgba(0,0,0,0.6); overflow: hidden; }
    #§dh { position: absolute; left: 50px; top: 44px; font: 700 40px/1 "Oswald", sans-serif; color: #2a2a2a; letter-spacing: 0.04em; }
    #§dl { position: absolute; left: 50px; top: 104px; width: 680px; height: 4px; background: #2a2a2a; }
    .§dc { position: absolute; left: 50px; top: 128px; font: 600 26px/1 "Oswald", sans-serif; color: #7a7a7a; letter-spacing: 0.08em; }
    .§dr { position: absolute; left: 50px; width: 680px; height: 74px; border-bottom: 2px solid #cfcdc7; opacity: 0; }
    .§dr span { position: absolute; top: 16px; font: 600 40px/1 "Oswald", sans-serif; color: #2a2a2a; }
    .§dr svg { position: absolute; right: 6px; top: 14px; width: 44px; height: 44px; overflow: visible; }
    #§qr { position: absolute; left: 560px; top: 680px; width: 150px; height: 150px; opacity: 0; }
    #§stmt { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; background: #0A0A0A; opacity: 0; }
    """
    rows = "".join(f'<div id="§r{i}" class="§dr" style="top:{180 + i * 80}px"><span style="left:0">{d}</span><span style="left:250px">{k} KM</span>'
                   f'<svg viewBox="0 0 44 44"><path id="§k{i}" d="M6 24 L18 36 L38 10" fill="none" stroke="#FB8000" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
                   for i, (d, k) in enumerate(ROWS_CP))
    import random
    rnd = random.Random(7)
    cells = "".join(f'<rect x="{x * 10}" y="{y * 10}" width="10" height="10"/>' for y in range(15) for x in range(15)
                    if (x < 4 and y < 4) or (x > 10 and y < 4) or (x < 4 and y > 10) or (4 <= x <= 10 or 4 <= y <= 10) and rnd.random() < 0.5)
    corners = "".join(f'<rect x="{a}" y="{b}" width="40" height="40" fill="none" stroke="#2a2a2a" stroke-width="6"/><rect x="{a + 12}" y="{b + 12}" width="16" height="16"/>'
                      for a, b in ((0, 0), (110, 0), (0, 110)))
    qr = f'<svg id="§qr" viewBox="0 0 150 150" style="fill:#2a2a2a">{corners}{cells}</svg>'
    doc = ('<div id="§doc"><div id="§dh">HISTORIQUE KILOMÉTRIQUE</div><div id="§dl"></div>'
           '<div class="§dc" style="left:50px">DATE</div><div class="§dc" style="left:300px">KILOMÉTRAGE RELEVÉ</div>' + rows + qr + "</div>")
    hud = (title("t1", ["LE VÉHICULE", "ÉTAIT BELGE."], 560, 140) + doc + title("t2", ["CAR-PASS COMPLET."], 270, 100)
           + '<div id="§stmt"></div>'
           + title("s1", ["JE N'AI PAS ACHETÉ", "UN COMPTEUR."], 560, 104, "color:#FB8000")
           + title("s2", ["J'AI ACHETÉ", "UN HISTORIQUE."], 900, 104, "color:#FB8000"))
    js = X_JS + """
      // the turn: the car was Belgian
      tin("t1", 2, at("belge") - 0.1); punch(at("belge") - 0.1, 0.05);
      // the Car-Pass: a neutral mock-up, fictitious dates and mileages, each line ticked in orange
      tout("t1", 2, at("car-pass") - 0.3);
      pre("doc", { opacity: 0, y: 80, scale: 0.94 }); go("doc", { opacity: 1, y: 0, scale: 1 }, at("car-pass") - 0.15, 0.35, "expo.out"); punch(at("car-pass") - 0.15, 0.04);
      var a = at("chaque") - 0.1, b = atEnd("enregistré"), step = Math.max(0.22, (b - a) / 6);
      for (var i = 0; i < 6; i++) { pre("r" + i, { opacity: 0, x: -30 }); go("r" + i, { opacity: 1, x: 0 }, a + i * step, 0.2); draw("k" + i, a + i * step + 0.12, 0.18, "power2.out"); }
      tin("t2", 1, at("vendeur") - 0.1); punch(at("vendeur") - 0.1, 0.04);
      pre("qr", { opacity: 0, scale: 0.6 }); go("qr", { opacity: 1, scale: 1 }, at("ligne") - 0.15, 0.3, "back.out(2)");
      // in the pause after the voice: what I really bought
      var e = atEnd("ligne") + 0.25;
      go("stmt", { opacity: 1 }, e, 0.25, "none"); tout("t2", 1, e);
      tin("s1", 2, e + 0.15); punch(e + 0.15, 0.04);
      tin("s2", 2, e + 1.15); punch(e + 1.15, 0.05);
    """
    sfx = [("click-soft", "chaque", 1, 0.0, 0.25), ("impact-bass-2", "ligne", 1, 0.7, 0.4)]
    return css, "", hud, js, None, sfx


def scene_04():
    css = """
    #§hb { position: absolute; left: 0; top: 760px; width: 1080px; text-align: center; font: 600 50px/1 "Oswald", sans-serif; color: #8c8c8c; opacity: 0; letter-spacing: 0.02em; }
    """
    hud = (title("t1", ["CE N'EST PAS", "INFAILLIBLE."], 300, 120, "color:#9a9a9a")
           + '<div id="§hb">HORS DE BELGIQUE : NON RELEVÉ</div>'
           + title("t2", ["MAIS C'EST LE MEILLEUR", "GARDE-FOU D'EUROPE."], 960, 100))
    js = X_JS + """
      tin("t1", 2, Math.max(0.05, at("ce") - 0.1)); punch(Math.max(0.05, at("ce") - 0.1), 0.03);
      fin("hb", at("hors") - 0.1);
      tin("t2", 2, at("mais") - 0.1); punch(at("mais") - 0.1, 0.04);
    """
    return css, "", hud, js, None, []


ENG = [("ACHAT", "30 000 €", "30000euros", "00 000"), ("TRANSPORT", "600 €", "600euros", "000"), ("RÉVISION", "600 €", "600euros", "000")]


def scene_05():
    css = """
    .§rw { position: absolute; left: 90px; width: 900px; height: 130px; opacity: 0; border-bottom: 2px solid #2e2e2e; }
    .§rl { position: absolute; left: 0; top: 38px; font: 600 58px/60px "Oswald", sans-serif; color: #cfcfcf; white-space: nowrap; }
    .§rv { position: absolute; right: 0; top: 18px; font: 700 90px/1 "Oswald", sans-serif; color: #fff; white-space: nowrap; }
    #§tot { position: absolute; left: 140px; top: 1010px; width: 800px; height: 300px; border: 5px solid #FB8000; border-radius: 24px; opacity: 0; text-align: center; }
    #§totv { display: block; margin-top: 34px; font: 700 160px/1 "Oswald", sans-serif; color: #fff; }
    #§totl { display: block; margin-top: 16px; font: 700 54px/1 "Oswald", sans-serif; color: #FB8000; letter-spacing: 0.1em; }
    """
    hud = title("t0", ["JUILLET 2019."], 260, 120)
    hud += "".join(f'<div id="§r{i}" class="§rw" style="top:{480 + i * 160}px"><span class="§rl">{l} :</span><span class="§rv">{odo(f"v{i}", v)}</span></div>'
                   for i, (l, v, _, _) in enumerate(ENG))
    hud += '<div id="§tot"><span id="§totv">' + odo("tv", "31 200 €") + '</span><span id="§totl">ENGAGÉS</span></div>'
    js = X_JS + """
      tin("t0", 1, Math.max(0.05, at("juillet") - 0.1));"""
    for i, (_, _, w, fr) in enumerate(ENG):
        n = 2 if i == 2 else 1
        js += f"""
      pre("r{i}", {{ opacity: 0, y: 30 }}); go("r{i}", {{ opacity: 1, y: 0 }}, at("{w}", {n}) - 0.15, 0.25); punch(at("{w}", {n}) - 0.15, 0.03);
      odo("v{i}", at("{w}", {n}) - 0.1, 0.9, {{ from: "{fr}", dimLead: true }});"""
    js += """
      pre("tot", { opacity: 0, scale: 0.9 }); go("tot", { opacity: 1, scale: 1 }, at("31200") - 0.15, 0.3, "back.out(1.6)"); punch(at("31200") - 0.15, 0.05);
      odo("tv", at("31200") - 0.1, 1.0, { from: "00 000", dimLead: true });
    """
    return css, "", hud, js, None, [("pop", "31200", 1, -0.1, 0.3)]


def scene_06():
    css = f"""
    #§cap {{ {BIG} top: 560px; font-size: 46px; font-weight: 600; color: #8c8c8c; letter-spacing: 0.04em; }}
    #§eq {{ {BIG} top: 640px; font-size: 120px; color: #fff; }}
    #§res {{ {BIG} top: 790px; font-size: 200px; color: #fff; }}
    #§rvb {{ {BIG} top: 450px; font-size: 170px; color: #FB8000; }}
    #§x {{ position: absolute; left: 150px; top: 900px; width: 780px; height: 16px; border-radius: 8px; background: {RED}; transform-origin: 0 50%; transform: scaleX(0); }}
    """
    st = full("ph", "jag-03.jpg", "50% 50%") + '<div class="§shade"></div><div id="§blk" style="position:absolute;left:0;top:0;width:1080px;height:1920px;background:#0A0A0A;opacity:0"></div>'
    hud = (title("t1", ["90 JOURS", "DE STOCK."], 300, 130)
           + title("t2", ["REVENDUE"], 300, 120) + '<div id="§rvb">' + odo("rv", "36 200 €") + ' <span style="font-size:0.5em;color:#fff">TTC</span></div>'
           + '<div id="§cap">CE QUE TOUT LE MONDE CALCULE</div><div id="§eq">36 200 − 30 000</div>'
           + '<div id="§res">= ' + odo("rs", "6 200 €") + '</div><div id="§x"></div>')
    js = X_JS + """
      tl.set($("ph"), { opacity: 1 }, 0); photo("ph", 0, DUR, 1.05);
      tin("t1", 2, Math.max(0.05, at("90") - 0.1)); punch(Math.max(0.05, at("90") - 0.1), 0.04);
      tout("t1", 2, at("36200") - 0.25); tin("t2", 1, at("36200") - 0.1); fin("rvb", at("36200") - 0.1); punch(at("36200") - 0.1, 0.04);
      odo("rv", at("36200") - 0.05, 1.0, { from: "00 000", dimLead: true });
      // what everyone works out
      tout("t2", 1, at("6200euros") - 0.25); fout("rvb", at("6200euros") - 0.25); go("blk", { opacity: 1 }, at("6200euros") - 0.25, 0.25, "none");
      fin("cap", at("6200euros") - 0.1); fin("eq", at("6200euros") - 0.05);
      fin("res", at("6200euros") + 0.1); odo("rs", at("6200euros") + 0.1, 0.9, { from: "0 000", dimLead: true }); punch(at("6200euros") + 0.1, 0.04);
      // and it's wrong
      go("x", { scaleX: 1 }, at("faux") - 0.05, 0.2, "power3.out"); shake("res", at("faux") + 0.1, 12); punch(at("faux") - 0.05, 0.05);
    """
    return css, st, hud, js, None, [("glitch-1", "faux", 1, -0.05, 0.25)]


DED = [("TRANSPORT", "600 €", "transport", "5 600"), ("RÉVISION", "600 €", "révision", "5 000"), ("TVA NETTE REVERSÉE", "833 €", "833", "4 167")]


def scene_07():
    css = f"""
    #§top {{ {BIG} top: 790px; font-size: 200px; color: #fff; opacity: 1; transform-origin: 540px 50%; }}
    .§dd {{ position: absolute; left: 90px; width: 900px; height: 110px; opacity: 0; border-bottom: 2px solid #3a1a1a; }}
    .§dl {{ position: absolute; left: 0; top: 30px; font: 600 54px/60px "Oswald", sans-serif; color: {RED}; white-space: nowrap; }}
    .§dv {{ position: absolute; right: 0; top: 16px; font: 700 80px/1 "Oswald", sans-serif; color: {RED}; white-space: nowrap; }}
    #§tvd {{ position: absolute; left: 90px; top: 1000px; width: 900px; text-align: right; font: 600 40px/1 "Oswald", sans-serif; color: #8c8c8c; opacity: 0; }}
    #§rest {{ {BIG} top: 1150px; font-size: 54px; font-weight: 600; color: #8c8c8c; letter-spacing: 0.06em; }}
    """
    hud = '<div id="§top">' + odo("tp", "6 200 €") + '</div>'
    hud += "".join(f'<div id="§d{i}" class="§dd" style="top:{560 + i * 140}px"><span class="§dl">− {l}</span><span class="§dv">{odo(f"dv{i}", v)}</span></div>'
                   for i, (l, v, _, _) in enumerate(DED))
    hud += '<div id="§tvd">6 033 COLLECTÉS − 5 200 RÉCUPÉRÉS</div><div id="§rest">CE QUI RESTE VRAIMENT</div>'
    js = X_JS + """
      // the 6 200 of the previous scene goes up and stays on screen
      odo("tp", 0, 0.01, { from: "6 200", spinLow: false });
      go("top", { y: -520 }, 0.05, 0.45, "power3.inOut");"""
    for i, (_, v, w, after) in enumerate(DED):
        fr = "000" if i < 2 else "000"
        js += f"""
      // deduction {i + 1}, in red; the figure on top drops
      pre("d{i}", {{ opacity: 0, x: 40 }}); go("d{i}", {{ opacity: 1, x: 0 }}, at("{w}") - 0.15, 0.22); punch(at("{w}") - 0.15, 0.03);
      odo("dv{i}", at("{w}") - 0.1, 0.7, {{ from: "{fr}", dimLead: true }});
      odo("tp", at("{w}") + 0.25, 0.8, {{ to: "{after.replace(' ', '')}", spinLow: false }});
      tl.fromTo($("top"), {{ color: "{RED}" }}, {{ color: "#ffffff", duration: 0.6, immediateRender: false }}, at("{w}") + 0.25);"""
    js += """
      fin("tvd", at("collecté") - 0.1);
      // what is really left: 4 167, in orange, the biggest figure of the film
      for (var i = 0; i < 3; i++) go("d" + i, { opacity: 0 }, at("final") - 0.2, 0.3, "none");
      go("tvd", { opacity: 0 }, at("final") - 0.2, 0.3, "none");
      go("top", { y: -120, scale: 1.45 }, at("final") - 0.1, 0.45, "expo.out");
      tl.fromTo($("top"), { color: "#ffffff" }, { color: "#FB8000", duration: 0.3, immediateRender: false }, at("final") - 0.1);
      punch(at("4167euros") - 0.05, 0.06); fin("rest", at("4167euros") + 0.2);
    """
    sfx = [("pop", w, 1, -0.15, 0.3) for _, _, w, _ in DED] + [("impact-bass-1", "4167euros", 1, -0.05, 0.45)]
    return css, "", hud, js, None, sfx


def scene_08():
    css = f"""
    #§pct {{ {BIG} top: 620px; font-size: 250px; color: #FB8000; }}
    #§days {{ {BIG} top: 900px; font-size: 90px; color: #fff; }}
    #§note {{ {BIG} top: 1020px; font-size: 38px; font-weight: 500; color: #8c8c8c; letter-spacing: 0.04em; }}
    """
    hud = (title("t1", ["4 167 € SUR", "31 200 ENGAGÉS."], 280, 96)
           + '<div id="§pct">' + odo("pc", "13,4 %") + '</div><div id="§days">EN 90 JOURS</div>'
           + '<div id="§note">résultat de cette opération, pas une promesse</div>'
           + title("t2", ["ET AUCUN SAV."], 1170, 110))
    js = X_JS + """
      tin("t1", 2, Math.max(0.05, at("4167euros") - 0.1)); punch(Math.max(0.05, at("4167euros") - 0.1), 0.03);
      fin("pct", at("90") - 0.2); odo("pc", at("90") - 0.15, 1.0, { from: "00,0", dimLead: true }); punch(at("90") - 0.15, 0.05);
      fin("days", at("90") - 0.05); fin("note", at("90") + 0.6);
      tin("t2", 1, at("aucun") - 0.1); punch(at("aucun") - 0.1, 0.04);
    """
    return css, "", hud, js, None, []


def scene_09():
    st = full("ph", "jag-04.jpg", contain=True) + '<div class="§shade"></div>'
    hud = (title("t1", ["LE KILOMÉTRAGE", "N'ÉTAIT PAS LE RISQUE."], 290, 96)
           + title("t2", ["LE RISQUE, C'ÉTAIT DE NE PAS", '<span class="§o">POUVOIR LE PROUVER.</span>'], 1320, 64))
    js = X_JS + """
      // the lesson: slower, the photo held long, the music gone
      pre("ph", { opacity: 0, scale: 1 }); go("ph", { opacity: 0.85 }, 0.05, 0.6, "none"); go("ph", { scale: 1.04 }, 0, DUR, "none");
      tin("t1", 2, Math.max(0.1, at("kilométrage") - 0.15), 0.3); punch(Math.max(0.1, at("kilométrage") - 0.15), 0.03);
      tin("t2", 2, at("risque", 2) - 0.1, 0.3); punch(at("risque", 2) - 0.1, 0.03);
    """
    return "", st, hud, js, None, []


def scene_10():
    css = """
    #§me { position: absolute; left: 270px; top: 300px; width: 540px; height: 740px; overflow: hidden; opacity: 0;
      -webkit-mask-image: linear-gradient(#000 74%, transparent 100%); mask-image: linear-gradient(#000 74%, transparent 100%); }
    #§me img { position: absolute; left: 0; top: 0; width: 540px; height: auto; filter: saturate(0.35) contrast(1.04); }
    #§meglow { position: absolute; left: 290px; top: 330px; width: 500px; height: 500px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, rgba(251,128,0,0.5) 0%, rgba(251,128,0,0.16) 45%, rgba(251,128,0,0) 70%); }
    #§since { position: absolute; left: 0; top: 1196px; width: 1080px; text-align: center; font: 600 52px/1 "Oswald", sans-serif; color: #bdbdbd; opacity: 0; letter-spacing: 0.02em; }
    #§hn { position: absolute; left: 0; top: 1290px; width: 1080px; text-align: center; font: 700 66px/1 "Oswald", sans-serif; color: #FB8000; opacity: 0; }
    #§pill { position: absolute; left: 0; top: 1392px; width: 1080px; text-align: center; }
    #§pilli { display: inline-block; padding: 6px 40px; border-radius: 40px; background: #FB8000; color: #0A0A0A; font: 700 46px/1.3 "Oswald", sans-serif;
      opacity: 0; box-shadow: 0 0 40px rgba(251,128,0,0.4); }
    """
    st = '<div id="§meglow"></div><div id="§me"><img src="assets/img/guillaume.png"></div>'
    hud = (title("nm", ["GUILLAUME HERBIN"], 1070, 100) + '<div id="§since">DANS L\'AUTO DEPUIS 2010</div>'
           + '<div id="§hn">@guillaumeherbin_</div><div id="§pill"><span id="§pilli">SUIS-MOI</span></div>')
    js = X_JS + """
      // who I am: the photo, the name, since 2010; then the handle and the button
      pre("me", { opacity: 0, y: 60 }); go("me", { opacity: 1, y: 0 }, 0.05, 0.6, "power3.out");
      pre("meglow", { opacity: 0, scale: 0.6 }); go("meglow", { opacity: 1, scale: 1 }, 0.15, 0.7, "power2.out");
      tin("nm", 1, Math.max(0.2, at("guillaumeherbin") - 0.1)); punch(Math.max(0.2, at("guillaumeherbin") - 0.1), 0.04);
      fin("since", at("depuis") - 0.1);
      fin("hn", at("suis-moi") - 0.1);
      pre("pilli", { opacity: 0, scale: 0.5 }); go("pilli", { opacity: 1, scale: 1 }, at("suis-moi") + 0.1, 0.3, "back.out(2)"); punch(at("suis-moi") + 0.1, 0.04);
    """
    return css, st, hud, js, None, [("notification", "suis-moi", 1, 0.1, 0.25)]


BUILDERS = [scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07, scene_08, scene_09, scene_10]


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
    <div id="§hud" class="§cam §hudcam"><div id="§hp" class="§cam §hudcam">
      {hud}
    </div></div>
    <div id="§sub" class="§sub">
      {"" if sc.get("nosubs") else subs_html(cw, dur)}
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
message: "Une F-Type à 139 891 km que tout le monde refuse, un document que personne ne connaît (le Car-Pass belge), une marge que tout le monde surestime : 4 167 €, pas 6 200 €. Le risque n'était pas le kilométrage, c'était de ne pas pouvoir le prouver."
arc: Hook → Pourquoi tout le monde fuit → Le Car-Pass → La nuance → Ce que j'ai engagé → La revente → La vraie marge → Le chiffre que personne ne regarde → La leçon → Qui je suis et CTA
audience: "Personnes qui veulent se lancer dans l'achat-revente automobile"
mode: autonomous
captions: disabled
music: "pre-mixed with voice and SFX in assets/audio/mix.wav (mounted at root by the orchestrator)"
direction: "brief de Guillaume (SCRIPT.md), reel 9:16, motion design sur fond noir orienté chiffres, ponctué de photos de la F-Type"
styleframes: "aucune"
patterns: ../patterns/STORYBOARD-CRAFT.md, ../patterns/PATTERNS.md
---

<!-- generated by build.py: edit build.py, not this file -->

## Video direction

- **One world** : fond #0A0A0A, accent unique #FB8000, texte blanc, rouge #E03131 pour les seules déductions ; Oswald en capitales, trait orange tracé sous chaque titre en 6 frames ; sous-titres de la voix mot par mot à 12 % du bas, mot-clé en orange.
- **Seams** : coupes franches sur la voix à chaque scène (whoosh court).
- **Timing** : chaque animation est posée sur un mot de la voix (build.py), les durées des scènes suivent la piste voix.
- **Negative list** : les photos de la série K08673 sans filigrane uniquement, pas d'image générée ; ni VIN, ni plaque, ni ville ou nom du marchand belge ; le Car-Pass est une maquette neutre aux dates et kilométrages fictifs, jamais le vrai document ; la nuance « pas infaillible » ne se coupe pas ; 13,4 % = résultat d'une opération, pas une promesse ; pas de billets.

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
