#!/usr/bin/env python3
"""Reel « 2 000 €, elle ne roulait pas » : one source for the whole film.

Every animation of every scene is placed on a WORD of the voice (at("virement"), at("même", 2)...), never on a fixed
second. The word timings come from one file:
  - assets/audio/voix-montage-mots.json when the real voice is there (align.py writes it), or
  - a provisional timing spread over the brief's windows (0-4, 4-14, 14-26, 26-36, 36-46, 46-56, 56-64, 64-78, 78-90, 90-95 s).
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
   "*2~000~euros*.", "Pour une voiture", "qui ne *roulait* pas."]),
 dict(id="02-trouvaille", name="La trouvaille", window=(4, 14), chunks=[
   "On remonte en *2015*.", "Une Mini British Open *1300*,", "démontée dans un garage.", "Le propriétaire", "avait lancé la restauration,",
   "et il avait *abandonné*", "en cours de route.", "C'est ce qui m'a permis", "de l'acheter à ce *prix*.", "Une voiture *immobile*",
   "fait fuir presque tout le monde."]),
 dict(id="03-voiture", name="La voiture", window=(14, 26), chunks=[
   "Une *série~limitée*", "de juin *1992*.", "British Racing Green,", "sellerie *tweed*,", "et un *toit* en toile électrique",
   "sur toute la longueur.", "Pas un toit ouvrant,", "un vrai toit qui *s'escamote*.", "*Mille* exemplaires",
   "pour le marché anglais."]),
 dict(id="04-detail", name="Le détail", window=(26, 36), chunks=[
   "*1275* centimètres cubes", "avec un *carburateur*.", "Quelques mois plus tard,", "la Mini passe", "à l'*injection* monopoint.",
   "Celle-ci est née", "du *bon~côté* de la bascule.", "C'est le genre de détail", "qui sépare deux voitures",
   "identiques sur une *photo*."]),
 dict(id="05-chantier", name="Le chantier", window=(36, 46), chunks=[
   "*Six~mois* de chantier.", "Carrosserie, peinture,", "remontage complet.", "Six mois à *démonter*,", "à *comprendre*,",
   "et à *remonter*."]),
 dict(id="06-couts", name="Les coûts", window=(46, 56), chunks=[
   "*1~500~euros* de carrosserie,", "peinture et remontage.", "*500~euros*", "de pièces neuves.", "*300~euros*",
   "de remise en route.", "*60~euros*", "de contrôle technique.", "*Total*~:", "*4~360~euros*."]),
 dict(id="07-revente", name="La revente", window=(56, 64), chunks=[
   "Je l'ai gardée *quatre~ans*.", "Revendue *8~500~euros*.", "*4~140~euros* d'écart."]),
 dict(id="08-retournement", name="Le retournement", window=(64, 78), chunks=[
   "Sauf que je ne l'ai pas", "achetée pour *ça*.", "Je l'ai achetée pour *apprendre*", "à faire des choses",
   "que je ne savais pas faire.", "Et puis j'ai pris *goût*", "à la posséder,", "et à rouler avec.", "L'argent est arrivé *après*.",
   "Il n'était pas la *raison*."]),
 dict(id="09-lecon", name="La leçon", window=(78, 90), chunks=[
   "La marge s'est faite", "à l'*achat*.", "Le jour où j'ai accepté", "d'acheter un tas de *pièces*.", "Et la valeur est venue",
   "du *modèle*,", "pas du chantier~:", "une restauration", "ne crée pas de valeur", "sur une voiture *banale*,", "elle la *révèle*",
   "sur une voiture *recherchée*."]),
 dict(id="10-cta", name="CTA", window=(90, 95), chunks=[
   "Toi, tu aurais vu", "l'*opportunité*", "et tu te serais lancé", "dans ce chantier", "de *restauration*~?"]),
]
SPOKEN_SYL = {"2000euros": 4, "2015": 3, "1300": 2, "1992": 7, "sérielimitée": 5, "1275": 6, "sixmois": 2, "1500euros": 5,
              "500euros": 4, "300euros": 4, "60euros": 4, "4360euros": 8, "quatreans": 3, "8500euros": 6, "4140euros": 7,
              "boncôté": 2, "mille": 1}
GOLD = "#C9A84C"


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
      background: radial-gradient(closest-side, rgba(201,168,76,0.15) 0%, rgba(201,168,76,0.09) 38%, rgba(201,168,76,0.03) 70%, rgba(201,168,76,0) 100%); }
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
    .§stk { position: absolute; left: 0; top: 0; width: 100%; height: 100%; display: block; background: #C9A84C;
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
    .§porange { fill: #C9A84C; opacity: 0; }
    .§glow { position: absolute; width: 420px; height: 420px; border-radius: 50%; opacity: 0;
      background: radial-gradient(closest-side, rgba(201,168,76,0.55), rgba(201,168,76,0.18) 55%, rgba(201,168,76,0)); }
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
            if (w.classList.contains("sub-key")) tl.fromTo(w, { color: "#ffffff" }, { color: "#C9A84C", duration: 0.12, ease: "power3.out", immediateRender: false }, t);
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



PH_CSS = """
    @font-face { font-family: "Space Mono"; src: url("assets/fonts/SpaceMono-700.woff2") format("woff2"); font-weight: 700; }
    .§ph { position: absolute; overflow: hidden; border: 3px solid #C9A84C; border-radius: 6px; box-shadow: 0 24px 60px rgba(0,0,0,0.6); background: #151515; }
    .§ph img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(0.78) contrast(1.04); }
    .§full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
    .§full img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(0.78) contrast(1.04); }
    .§g { color: #C9A84C; }
    .§lab { position: absolute; left: 0; width: 1080px; text-align: center; font: 96px/1.1 "Anton", sans-serif; color: #fff; white-space: nowrap; opacity: 0;
      text-shadow: 0 4px 24px rgba(0,0,0,0.6); }
    .§title { text-shadow: 0 4px 24px rgba(0,0,0,0.5); }
    #§tot { position: absolute; right: 40px; top: 130px; text-align: right; opacity: 0; }
    #§totl { display: block; font: 700 22px/1 "Space Mono", monospace; color: #9a9a9a; letter-spacing: 0.12em; }
    #§totv { display: block; margin-top: 6px; font: 60px/1 "Anton", sans-serif; color: #C9A84C; }
"""

PH_JS = """
      function label(id, t, out) { pre(id, { opacity: 0 }); slam(id, t); if (out != null) go(id, { opacity: 0 }, out, 0.15); }
      function tshow(tid, n, cues) { for (var i = 0; i < n; i++) slam(tid + "-" + i, cues[i] - 0.05); stroke(tid, cues[n - 1] + 0.15); init(tid + "-s", { scaleX: 1 }); }
      function thide(tid, n, t) { for (var i = 0; i < n; i++) go(tid + "-" + i, { opacity: 0 }, t, 0.15); go(tid + "-s", { scaleX: 0 }, t, 0.15); }
      function photo(id, t, o) { o = o || {}; pre(id, { opacity: 0, scale: o.s || 1.08, rotation: o.r || 0 }); go(id, { opacity: 1, scale: 1 }, t, o.d || 0.45, o.ease || "power3.out"); }
"""


def ph(pid, src, x, y, w, h, pos="50% 50%", rot=0):
    return (f'<div id="§{pid}" class="§ph" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)">'
            f'<img src="assets/img/{src}" style="object-position:{pos}"></div>')


def tot(text):
    """the TOTAL INVESTI counter, top right, from scene 2 on"""
    return f'<div id="§tot"><span id="§totl">TOTAL INVESTI</span><span id="§totv">{odo("tv", text)}</span></div>'


TOT_ON = 'tl.set($("tot"), { opacity: 1 }, 0); init("tot", { opacity: 1 }); odo("tv", 0, 0.01, { from: $("tv").getAttribute("data-to"), spinLow: false });'


def scene_01():
    st = ph("p1", "austin1.jpg", 60, 560, 960, 540, "50% 55%", -1.5)
    hud = (title("t1", [odo("big", "2 000 €") + "."], 230, 230)
           + '<div id="§l1" class="§lab" style="top:1130px;font-size:84px">ELLE NE <span class="§g">ROULAIT</span> PAS.</div>')
    js = PH_JS + """
      slam("t1-0", 0.02, { s: 1.4 }); odo("big", 0.02, 0.9, { from: "0 000", dimLead: true }); stroke("t1", 0.9);
      // the stripped car slams in
      pre("p1", { opacity: 0, scale: 1.25, rotation: -1.5 }); go("p1", { opacity: 1, scale: 1 }, Math.max(0.05, at("pour") - 0.1), 0.18, "expo.out");
      shake("p1", at("pour") + 0.05, 16);
      label("l1", at("roulait") - 0.05);
    """
    sfx = [("impact-bass-2", None, 0, 0.02, .24), ("typing", None, 0, 0.05, .1), ("whoosh-short", "pour", 1, -.12, .16), ("pop", "roulait", 1, -.05, .14)]
    return PH_CSS, st, hud, js, (540, 800), sfx


PARTS = [("echappement", 40, 500, -6), ("siege", 880, 500, 5), ("roue", 30, 1000, 4), ("calandre", 890, 1010, -5), ("volant", 470, 1090, 3)]


def scene_02():
    st = ph("p1", "austin2.jpg", 120, 560, 840, 470, "50% 50%", 1) + "".join(
        f'<div id="§q{i}" class="§ph" style="left:{x}px;top:{y}px;width:160px;height:160px;transform:rotate({r}deg)"><img src="assets/img/part-{n}.jpg"></div>'
        for i, (n, x, y, r) in enumerate(PARTS))
    hud = (title("t1", ["2015."], 240, 170) + title("t2", ["PROJET", '<span class="§g">ABANDONNÉ</span>.'], 230, 120) + tot("2 000 €"))
    js = PH_JS + "".join(f"""
      pre("q{i}", {{ opacity: 0, x: {540 - 80 - x}, y: {795 - 80 - y}, scale: 0.3 }});
      go("q{i}", {{ opacity: 1, x: 0, y: 0, scale: 1 }}, at("démontée") + {i * 0.08:.2f}, 0.55, "back.out(1.4)");""" for i, (n, x, y, r) in enumerate(PARTS)) + """
      tshow("t1", 1, [Math.max(0.05, at("2015"))]);
      photo("p1", Math.max(0.05, at("2015") + 0.1));
      thide("t1", 1, at("abandonné") - 0.2);
      tshow("t2", 2, [at("abandonné") - 0.1, at("abandonné") + 0.25]);
      // what made the price: the counter starts
      pre("tot", { opacity: 0, x: 30 }); go("tot", { opacity: 1, x: 0 }, at("prix") - 0.1, 0.3); odo("tv", at("prix"), 0.9, { from: "0 000", dimLead: true });
      init("p1", { scale: 1 }); go("p1", { scale: 1.04 }, at("immobile"), 2.5, "sine.inOut");
    """
    sfx = [("pop", "2015", 1, -.05, .14), ("whoosh-short", "démontée", 1, 0, .16), ("pop", "abandonné", 1, -.1, .14),
           ("typing", "prix", 1, 0, .1), ("click-soft", "prix", 1, .5, .2)]
    return PH_CSS, st, hud, js, (540, 800), sfx


ROOF = """<svg id="§roof" viewBox="0 0 400 700" style="position:absolute;left:340px;top:420px;width:400px;height:700px;opacity:0;overflow:visible">
  <rect x="40" y="20" width="320" height="660" rx="90" fill="#1f3b2e" stroke="#C9A84C" stroke-width="6"/>
  <rect x="70" y="150" width="260" height="70" rx="20" fill="#0d1a14" stroke="#C9A84C" stroke-width="3"/>
  <rect x="80" y="560" width="240" height="44" rx="14" fill="#0d1a14" stroke="#C9A84C" stroke-width="3"/>
  <rect x="70" y="230" width="260" height="320" rx="16" fill="#d9cfb7" opacity="0.35"/>
  <g id="§canvas"><rect x="70" y="230" width="260" height="320" rx="16" fill="#151515" stroke="#C9A84C" stroke-width="3"/>
  <path d="M90 290 H310 M90 350 H310 M90 410 H310 M90 470 H310" stroke="#3a3a3a" stroke-width="4"/></g>
  <text x="200" y="12" text-anchor="middle" font-family="Space Mono" font-size="20" fill="#9a9a9a">AVANT</text>
</svg>"""


def scene_03():
    st = ph("p1", "20190228_165907.jpg", 60, 450, 960, 467, "50% 50%") + ROOF
    hud = (title("t1", ["BRITISH OPEN CLASSIC", '<span class="§g">JUIN 1992</span>'], 250, 84) + tot("2 000 €")
           + '<div id="§l1" class="§lab" style="top:960px">SÉRIE <span class="§g">LIMITÉE</span></div>'
           + '<div id="§l2" class="§lab" style="top:1150px;font-size:80px">TOIT TOILE <span class="§g">ÉLECTRIQUE</span></div>'
           + '<div id="§l3" class="§lab" style="top:960px"><span class="§g">1 000</span> EXEMPLAIRES UK</div>')
    js = PH_JS + TOT_ON + """
      photo("p1", 0.05);
      tshow("t1", 2, [Math.max(0.05, at("une")), at("1992")]);
      label("l1", at("sérielimitée") - 0.05, at("toit") - 0.15);
      // the canvas roof: the whole length folds back
      go("p1", { opacity: 0 }, at("toit") - 0.15, 0.3);
      pre("roof", { opacity: 0, scale: 0.85 }); go("roof", { opacity: 1, scale: 1 }, at("toit") - 0.1, 0.4, "back.out(1.4)");
      label("l2", at("toit"), at("mille") - 0.15);
      tl.fromTo($("canvas"), { scaleY: 1, svgOrigin: "200 550" }, { scaleY: 0.16, svgOrigin: "200 550", duration: 1.4, ease: "power2.inOut", immediateRender: false }, at("s'escamote") - 0.3);
      go("roof", { opacity: 0 }, at("mille") - 0.2, 0.25); go("p1", { opacity: 1 }, at("mille") - 0.2, 0.3);
      label("l3", at("mille") - 0.05);
    """
    sfx = [("pop", "sérielimitée", 1, -.05, .14), ("whoosh-short", "toit", 1, -.1, .14), ("whoosh-short", "s'escamote", 1, -.3, .12),
           ("pop", "mille", 1, -.05, .14)]
    return PH_CSS, st, hud, js, (540, 800), sfx


def scene_04():
    css = PH_CSS + """
    #§sw { position: absolute; left: 90px; top: 960px; width: 900px; height: 250px; opacity: 0; }
    #§track { position: absolute; left: 150px; top: 110px; width: 600px; height: 6px; background: #3a3a3a; border-radius: 3px; }
    #§knob { position: absolute; left: 126px; top: 89px; width: 48px; height: 48px; border-radius: 50%; background: #C9A84C; box-shadow: 0 0 30px rgba(201,168,76,0.6); }
    .§swl { position: absolute; top: 0; width: 300px; text-align: center; font: 58px/1 "Anton", sans-serif; color: #ffffff; }
    .§swd { position: absolute; top: 160px; width: 300px; text-align: center; font: 700 22px/1.3 "Space Mono", monospace; color: #9a9a9a; letter-spacing: 0.08em; }
    #§here { position: absolute; left: 30px; top: -60px; width: 180px; text-align: center; font: 34px/1 "Anton", sans-serif; color: #0A0A0A; background: #C9A84C; border-radius: 30px; padding: 6px 0; opacity: 0; }
    """
    st = ph("p1", "20190228_165935.jpg", 60, 510, 960, 400, "50% 40%")
    hud = (title("t1", ["1275 CM3", '<span class="§g">CARBURATEUR</span>'], 250, 100) + tot("2 000 €")
           + '<div id="§sw"><div id="§track"></div><div id="§knob"></div>'
             '<div id="§sl" class="§swl" style="left:0">CARBU</div><div id="§sr" class="§swl" style="left:600px">INJECTION</div>'
             '<div class="§swd" style="left:0">JUIN 1992</div><div class="§swd" style="left:600px">QUELQUES MOIS<br>PLUS TARD</div>'
             '<div id="§here">CELLE-CI</div></div>')
    js = PH_JS + TOT_ON + """
      photo("p1", 0.05);
      tshow("t1", 2, [Math.max(0.05, at("1275")), at("carburateur")]);
      // the switch: carburettor, then single-point injection a few months later
      pre("sw", { opacity: 0, y: 30 }); go("sw", { opacity: 1, y: 0 }, at("quelques") - 0.1, 0.35);
      go("p1", { opacity: 0.35 }, at("quelques") - 0.1, 0.4);
      init("knob", { x: 0 }); go("knob", { x: 600 }, at("l'injection") - 0.1, 0.6, "power3.inOut");
      tl.fromTo($("sr"), { color: "#ffffff" }, { color: "#C9A84C", duration: 0.2, immediateRender: false }, at("l'injection") + 0.3);
      go("knob", { x: 0 }, at("boncôté") - 0.2, 0.6, "power3.inOut");
      tl.fromTo($("sr"), { color: "#C9A84C" }, { color: "#ffffff", duration: 0.2, immediateRender: false }, at("boncôté") - 0.2);
      tl.fromTo($("sl"), { color: "#ffffff" }, { color: "#C9A84C", duration: 0.2, immediateRender: false }, at("boncôté") + 0.3);
      label("here", at("boncôté") + 0.3);
      thide("t1", 2, at("c'est") - 0.1);
      go("p1", { opacity: 1 }, at("photo") - 0.4, 0.4); go("sw", { opacity: 0 }, at("photo") - 0.4, 0.3);
    """
    sfx = [("typing", "1275", 1, 0, .1), ("pop", "carburateur", 1, -.05, .14), ("whoosh-short", "l'injection", 1, -.1, .14),
           ("whoosh-short", "boncôté", 1, -.2, .14), ("click-soft", "boncôté", 1, .35, .2)]
    return css, st, hud, js, (540, 800), sfx


def scene_05():
    css = PH_CSS + """
    #§cal { position: absolute; left: 790px; top: 500px; width: 190px; height: 190px; border-radius: 18px; background: #151515; border: 3px solid #C9A84C; overflow: hidden; opacity: 0; }
    #§calh { position: absolute; left: 0; top: 0; width: 100%; height: 48px; background: #C9A84C; text-align: center; font: 700 22px/48px "Space Mono", monospace; color: #0A0A0A; letter-spacing: 0.1em; }
    #§cald { position: absolute; left: 0; top: 56px; width: 100%; text-align: center; font: 110px/1.15 "Anton", sans-serif; color: #fff; }
    """
    st = (ph("p1", "20170225_154834.jpg", 60, 560, 960, 540, "50% 50%") + ph("p2", "20170408_135132.jpg", 60, 560, 960, 540, "50% 50%")
          + '<div id="§cal"><div id="§calh">MOIS</div><div id="§cald">' + odo("md", "6") + '</div></div>')
    hud = (title("t1", [odo("six", "6") + ' <span class="§g">MOIS</span>'], 230, 220) + tot("2 000 €")
           + '<div id="§l1" class="§lab" style="top:1140px;font-size:64px">DÉMONTER.</div>'
           + '<div id="§l2" class="§lab" style="top:1140px;font-size:64px">DÉMONTER. COMPRENDRE.</div>'
           + '<div id="§l3" class="§lab" style="top:1140px;font-size:64px">DÉMONTER. COMPRENDRE. <span class="§g">REMONTER.</span></div>')
    js = PH_JS + TOT_ON + """
      tshow("t1", 1, [Math.max(0.05, at("sixmois"))]); odo("six", Math.max(0.05, at("sixmois")), 0.8, { from: "0" });
      photo("p1", 0.05);
      pre("p2", { opacity: 0 }); go("p2", { opacity: 1 }, at("remontage") - 0.2, 1.2, "sine.inOut");
      // a calendar runs six months
      pre("cal", { opacity: 0, scale: 0.7 }); go("cal", { opacity: 1, scale: 1 }, Math.max(0.1, at("sixmois") + 0.2), 0.3, "back.out(1.6)");
      odo("md", at("sixmois") + 0.3, at("démonter") - at("sixmois") - 0.4, { from: "1", spinLow: false });
      label("l1", at("démonter") - 0.05, at("comprendre") - 0.02);
      label("l2", at("comprendre") - 0.05, at("remonter") - 0.02);
      label("l3", at("remonter") - 0.05);
    """
    sfx = [("impact-bass-2", "sixmois", 1, -.05, .2), ("pop", "démonter", 1, -.05, .12), ("pop", "comprendre", 1, -.05, .12),
           ("pop", "remonter", 1, -.05, .14)]
    return css, st, hud, js, (540, 800), sfx


COSTS = [("CARROSSERIE, PEINTURE, REMONTAGE", "1 500 €", "1500euros", "3 500 €"), ("PIÈCES NEUVES", "500 €", "500euros", "4 000 €"),
         ("REMISE EN ROUTE", "300 €", "300euros", "4 300 €"), ("CONTRÔLE TECHNIQUE", "60 €", "60euros", "4 360 €")]


def scene_06():
    css = PH_CSS + """
    .§row { position: absolute; left: 70px; width: 940px; height: 120px; border-bottom: 2px solid #2a2a2a; opacity: 0; }
    .§rl { position: absolute; left: 0; top: 44px; font: 700 28px/1 "Instrument Sans", sans-serif; color: #b0b0b0; letter-spacing: 0.06em; }
    .§rv { position: absolute; right: 0; top: 18px; font: 76px/1 "Anton", sans-serif; color: #ffffff; }
    #§big { position: absolute; left: 0; top: 960px; width: 1080px; text-align: center; opacity: 0; }
    #§bigl { display: block; font: 700 30px/1 "Space Mono", monospace; color: #9a9a9a; letter-spacing: 0.16em; }
    #§bigv { display: block; margin-top: 14px; font: 190px/1 "Anton", sans-serif; color: #C9A84C; }
    """
    hud = (tot("2 000 €") + "".join(
        f'<div id="§r{i}" class="§row" style="top:{360 + i * 140}px"><span class="§rl">{l}</span><span class="§rv">{odo(f"v{i}", v)}</span></div>'
        for i, (l, v, c, t) in enumerate(COSTS))
        + '<div id="§big"><span id="§bigl">TOTAL INVESTI</span><span id="§bigv">' + odo("bv", "4 360 €") + '</span></div>')
    js = PH_JS + TOT_ON + "".join(f"""
      pre("r{i}", {{ opacity: 0, x: -40 }}); go("r{i}", {{ opacity: 1, x: 0 }}, at("{c}") - 0.1, 0.3);
      odo("v{i}", at("{c}") - 0.05, 0.8, {{ from: "{''.join('0' if ch.isdigit() else ch for ch in v)}", dimLead: true }});
      odo("tv", at("{c}") + 0.25, 0.8, {{ to: "{t}" }});""" for i, (l, v, c, t) in enumerate(COSTS)) + """
      // the total freezes, big, in the centre
      ["r0", "r1", "r2", "r3"].forEach(function (r) { go(r, { opacity: 0.35 }, at("total") - 0.1, 0.3); });
      pre("big", { opacity: 0, scale: 0.8 }); go("big", { opacity: 1, scale: 1 }, at("total") - 0.05, 0.35, "back.out(1.6)");
      odo("bv", at("4360euros") - 0.3, 1.0, { from: "0 000", dimLead: true });
      init("bigv", { scale: 1 }); go("bigv", { scale: 1.08 }, at("4360euros") + 0.75, 0.12); go("bigv", { scale: 1 }, at("4360euros") + 0.87, 0.3);
    """
    sfx = [("typing", "1500euros", 1, 0, .1), ("typing", "500euros", 1, 0, .1), ("typing", "300euros", 1, 0, .1),
           ("typing", "60euros", 1, 0, .1), ("impact-bass-2", "4360euros", 1, .7, .24)]
    return css, "", hud, js, (540, 900), sfx


def scene_07():
    css = PH_CSS + """
    .§box { position: absolute; top: 940px; width: 440px; height: 190px; border-radius: 18px; background: #151515; border: 2px solid #2e2e2e; text-align: center; opacity: 0; }
    .§bl { display: block; margin-top: 26px; font: 700 26px/1 "Space Mono", monospace; color: #9a9a9a; letter-spacing: 0.14em; }
    .§bv { display: block; margin-top: 16px; font: 92px/1 "Anton", sans-serif; color: #fff; }
    #§gain { position: absolute; left: 0; top: 560px; width: 1080px; text-align: center; font: 170px/1 "Anton", sans-serif; color: #C9A84C; opacity: 0;
      text-shadow: 0 8px 40px rgba(0,0,0,0.75); }
    """
    st = ph("p1", "2.jpg", 60, 520, 960, 380, "50% 55%")
    hud = (title("t1", ["4 ANS", '<span class="§g">PLUS TARD.</span>'], 230, 110) + tot("4 360 €")
           + '<div id="§b1" class="§box" style="left:70px"><span class="§bl">INVESTI</span><span class="§bv">' + odo("bi", "4 360 €") + '</span></div>'
           + '<div id="§b2" class="§box" style="left:570px;border-color:#C9A84C"><span class="§bl">REVENDUE</span><span class="§bv">' + odo("br", "8 500 €") + '</span></div>'
           + '<div id="§gain">+ ' + odo("gv", "4 140 €") + '</div>')
    js = PH_JS + TOT_ON + """
      tshow("t1", 2, [Math.max(0.05, at("quatreans") - 0.1), at("quatreans") + 0.2]);
      photo("p1", 0.05);
      thide("t1", 2, at("revendue") - 0.2);
      odo("bi", 0, 0.01, { from: "4 360", spinLow: false }); pre("b1", { opacity: 0, y: 30 }); go("b1", { opacity: 1, y: 0 }, at("revendue") - 0.15, 0.3);
      pre("b2", { opacity: 0, y: 30 }); go("b2", { opacity: 1, y: 0 }, at("8500euros") - 0.1, 0.3); odo("br", at("8500euros") - 0.05, 0.9, { from: "0 000", dimLead: true });
      go("p1", { opacity: 0.4 }, at("4140euros") - 0.2, 0.3);
      pre("gain", { opacity: 0, scale: 0.6 }); go("gain", { opacity: 1, scale: 1 }, at("4140euros") - 0.1, 0.35, "back.out(1.8)");
      odo("gv", at("4140euros") - 0.05, 1.0, { from: "0 000", dimLead: true });
    """
    sfx = [("whoosh-short", "quatreans", 1, -.1, .14), ("typing", "8500euros", 1, 0, .1), ("impact-bass-2", "4140euros", 1, .8, .24)]
    return css, st, hud, js, (540, 800), sfx


def scene_08():
    css = PH_CSS + """
    #§shade { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px;
      background: linear-gradient(rgba(10,10,10,0.7) 0%, rgba(10,10,10,0.15) 26%, rgba(10,10,10,0) 40%, rgba(10,10,10,0.35) 60%, rgba(10,10,10,0.85) 100%); }
    #§gain { position: absolute; left: 0; top: 300px; width: 1080px; text-align: center; font: 170px/1 "Anton", sans-serif; color: #C9A84C; }
    """
    st = '<div id="§fp" class="§full"><img src="assets/img/1.jpg" style="object-position:28% 50%"></div><div id="§shade"></div>'
    hud = ('<div id="§gain">+ 4 140 €</div>' + title("t1", ["CE N'ÉTAIT PAS", '<span class="§g">LE BUT</span>.'], 280, 120))
    js = PH_JS + """
      init("fp", { scale: 1 }); go("fp", { scale: 1.1 }, 0, DUR, "none");
      // slow: the gain fades away, the point appears
      init("gain", { opacity: 1 }); go("gain", { opacity: 0, y: -20 }, at("ça"), 2.2, "sine.inOut");
      tshow("t1", 2, [at("apprendre") - 0.2, at("apprendre") + 0.4]);
    """
    sfx = [("click-soft", "apprendre", 1, -.2, .18)]
    return css, st, hud, js, (540, 800), sfx


def scene_09():
    css = PH_CSS + """
    #§bg { opacity: 0.22; }
    #§kick { position: absolute; left: 0; top: 270px; width: 1080px; text-align: center; font: 700 34px/1 "Space Mono", monospace; color: #C9A84C; letter-spacing: 0.14em; opacity: 0; }
    .§rule { position: absolute; left: 80px; width: 920px; font: 76px/1.12 "Anton", sans-serif; color: #fff; opacity: 0; }
    .§rule b { font-weight: 400; color: #C9A84C; }
    """
    st = '<div id="§bg" class="§full"><img src="assets/img/4.jpg" style="object-position:50% 50%"></div>'
    hud = ('<div id="§kick">CE QUE J\'EN RETIENS</div>'
           + '<div id="§a1" class="§rule" style="top:400px">1. LA MARGE SE FAIT<br>À L\'<b>ACHAT</b>.</div>'
           + '<div id="§a2" class="§rule" style="top:700px">2. LA VALEUR VIENT<br>DU <b>MODÈLE</b>,<br>PAS DU CHANTIER.</div>')
    js = PH_JS + """
      pre("kick", { opacity: 0, y: 14 }); go("kick", { opacity: 1, y: 0 }, 0.05, 0.3);
      pre("a1", { opacity: 0, x: -30 }); go("a1", { opacity: 1, x: 0 }, at("l'achat") - 0.2, 0.35);
      pre("a2", { opacity: 0, x: -30 }); go("a2", { opacity: 1, x: 0 }, at("modèle") - 0.2, 0.35);
      go("a1", { opacity: 0.35 }, at("modèle") - 0.2, 0.3);
      
    """
    sfx = [("pop", "l'achat", 1, -.2, .14), ("pop", "modèle", 1, -.2, .14)]
    return css, st, hud, js, (540, 800), sfx


def scene_10():
    css = PH_CSS + """
    #§handle { position: absolute; left: 60px; top: 1080px; width: 960px; text-align: center; white-space: nowrap; }
    #§hname { position: relative; display: inline-block; font: 84px/1.2 "Anton", sans-serif; color: #ffffff; opacity: 0; }
    """
    st = ph("p1", "avant-plq.jpg", 300, 250, 480, 560, "50% 50%")
    hud = (title("t1", ["TU TE SERAIS", '<span class="§g">LANCÉ</span>, TOI ?'], 860, 96)
           + '<div id="§handle"><span id="§hname">@guillaumeherbin_<i class="§stilt"><i class="§stk" id="§h-s"></i></i></span></div>')
    js = PH_JS + """
      photo("p1", 0.02, { s: 0.85, ease: "back.out(1.4)" });
      tshow("t1", 2, [at("lancé"), at("restauration")]);
      slam("hname", at("restauration") + 0.5, { s: 1.3 }); stroke("h", at("restauration") + 0.7);
    """
    sfx = [("pop", "lancé", 1, -.05, .14), ("notification", "restauration", 1, .5, .24)]
    return css, st, hud, js, (540, 800), sfx


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
message: "Une Mini British Open 1992 achetée 2 000 € démontée, restaurée en six mois pour 4 360 € au total, revendue 8 500 € quatre ans plus tard ; mais l'argent n'était pas le but : la marge se fait à l'achat, et la valeur vient du modèle, pas du chantier."
arc: Hook → Trouvaille → La voiture → Le détail → Chantier → Coûts → Revente → Retournement → Leçon → CTA
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

- **One world** : fond #0A0A0A, accent unique #C9A84C, texte blanc ; titres Anton en capitales avec le trait orange tracé dessous ; sous-titres de la voix mot par mot, mot-clé en orange.
- **Seams** : coupes franches sur la voix à chaque scène (whoosh court).
- **Timing** : chaque animation est posée sur un mot de la voix (build.py), les durées des scènes suivent la piste voix.
- **Negative list** : aucun billet ni espèce ; jamais plus de 6 mots à l'écran (sauf les lignes de coûts et la leçon, voulues par le brief) ; photos de Guillaume désaturées en cadre or, plaques floutées ; compteur TOTAL INVESTI en haut à droite des scènes 2 à 7.

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
