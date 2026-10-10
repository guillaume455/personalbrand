#!/usr/bin/env python3
"""Reel « L'annonce que personne ne voulait » (Porsche 997, 2014): one source for the whole film.

Every animation of every scene is placed on a WORD of the voice (at("vendeur"), at("mauvaise", 2)...), never on a
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
TAIL = 4.3          # hold after the last word: the CTA, no voice
FPS = 30
HOOK = 4.0          # the hook lasts 4 s whatever the voice (place-voice.py pads it)

# ---------------------------------------------------------------------------------------------------------------------
# The voice, scene by scene, cut into subtitle chunks (2 to 5 words, 42 characters max). *word* = key word (orange).
# ~ glues two tokens into one subtitle word (« 54~000~km »). Numbers are spoken in letters by the voice.
SCENES = [
 dict(id="01-hook", name="Hook", window=(0, 4), speak=(0.3, 3.0), nosubs=True, chunks=[
   "L'*annonce* que personne", "ne voulait."]),
 dict(id="02-warnings", name="Les warnings", window=(4, 18), speak=(4.2, 17.6), chunks=[
   "Leboncoin, 2014.", "Des photos ratées.", "Un *vendeur* pressé,", "qui connaît mal", "sa voiture,", "qu'on n'arrive pas",
   "à avoir au téléphone,", "et qui ne vend", "rien du tout.", "Cinq raisons", "de passer son chemin."]),
 dict(id="03-retournement", name="Le retournement", window=(18, 27), speak=(18.2, 26.6), chunks=[
   "Sauf que ces cinq warnings", "portaient tous", "sur le *vendeur*.", "Sur la voiture,", "il n'y en avait aucun.",
   "Encore fallait-il", "aller *vérifier*."]),
 dict(id="04-verifie", name="Ce que j'ai vérifié", window=(27, 39), speak=(27.2, 38.6), chunks=[
   "Carnet d'entretien à jour,", "dernier passage", "à 54~000~km.", "Contrôle technique vierge.",
   "Rappel constructeur effectué.", "Historique complet.", "Une annonce se juge", "sur ce qu'il y a", "dans le *dossier*,",
   "pas sur la qualité", "des photos."]),
 dict(id="05-voiture", name="La voiture", window=(39, 52), speak=(39.2, 51.6), chunks=[
   "Une 911 type 997", "phase 2 de 2009.", "Flat six 3,6~litres,", "345~chevaux,", "boîte PDK.", "Et surtout",
   "une *phase~2*,", "injection directe,", "et plus d'*arbre~intermédiaire*.", "Le fameux problème", "des phases 1",
   "n'existe plus", "sur celle-là.", "C'est ce détail", "qui fait sa cote", "aujourd'hui."]),
 dict(id="06-prix", name="Le prix", window=(52, 58), speak=(52.2, 57.6), chunks=[
   "2014.", "J'ai *25~ans*.", "C'est ma première Porsche.", "44~000~euros."]),
 dict(id="07-deux-ans", name="Les deux ans", window=(58, 67), speak=(58.2, 66.6), chunks=[
   "Je la garde deux ans.", "1~000~euros", "d'entretien courant,", "450~euros de pneus.", "Je la revends 52~000.",
   "6~550~euros d'écart,", "après avoir roulé avec", "pendant deux ans."]),
 dict(id="08-2026", name="2026", window=(67, 75), speak=(67.2, 74.6), chunks=[
   "Et aujourd'hui,", "plus de dix ans après,", "les mêmes *s'affichent*", "à partir de", "57~000~euros.",
   "Il y a des voitures", "qui décotent,", "et d'autres", "qui font l'inverse."]),
 dict(id="09-lecon", name="La leçon et CTA", window=(75, 89), speak=(75.3, 84.7), chunks=[
   "La vraie leçon", "n'est pas là.", "Une mauvaise *annonce*", "n'est pas", "une mauvaise voiture.", "La plupart des gens",
   "éliminent sur la *présentation*.", "Moi je vérifie", "le *dossier*.", "C'est exactement là", "que se trouvent",
   "les bonnes affaires,", "dans les annonces", "que les autres", "ne prennent pas la peine", "d'ouvrir."]),
]
SPOKEN_SYL = {"2014": 4, "54000km": 9, "911": 4, "997": 6, "2009": 4, "36litres": 4, "345chevaux": 8, "pdk": 3, "2": 1,
              "1": 1, "25ans": 4, "44000euros": 7, "1000euros": 4, "450euros": 6, "52000": 5, "6550euros": 10,
              "57000euros": 7, "leboncoin": 3, "phase2": 2, "d'arbreintermédiaire": 7}


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
      // photos: fade in, slow zoom (k = 1.03 to 1.05) until t2
      function photo(id, t, t2, k, op) { pre(id, { opacity: 0, scale: 1 }); go(id, { opacity: op || 1 }, t, 0.25, "none"); go(id, { scale: k || 1.04 }, t, Math.max(0.5, (t2 || DUR) - t), "none"); }
"""


def full(fid, src, pos="50% 50%", contain=False):
    """a photo over the whole frame; contain = the photo whole on a blurred, darkened copy of itself"""
    if not contain:
        return f'<div id="§{fid}" class="§full"><img src="assets/img/{src}" style="object-position:{pos}"></div>'
    return (f'<div id="§{fid}" class="§full"><img src="assets/img/{src}" style="filter:saturate(0.1) blur(28px) brightness(0.45);transform:scale(1.15)">'
            f'<img src="assets/img/{src}" style="object-fit:contain;object-position:50% 50%"></div>')


# ---------------------------------------------------------------------------------------------------------------------
# the 9 scenes: (css, stage html, hud html [titles, cards], js, halo, sfx [(name, cue word, occurrence, offset, volume)])

RED = "#E03131"
WARN = ["PHOTOS RATÉES", "VENDEUR PRESSÉ", "CONNAÎT MAL SA VOITURE", "INJOIGNABLE", "AUCUN SENS DU COMMERCE"]
WARN_CSS = f"""
    .§pills {{ position: absolute; left: 160px; top: 1090px; width: 760px; transform-origin: 0 0; }}
    .§pill {{ position: absolute; left: 0; width: 760px; height: 68px; border-radius: 34px; border: 3px solid {RED};
      background: rgba(224,49,49,0.13); opacity: 0; font: 600 40px/62px "Oswald", sans-serif; color: #fff; text-transform: uppercase;
      white-space: nowrap; box-sizing: border-box; padding-left: 86px; }}
    .§pill i {{ position: absolute; left: 10px; top: 7px; width: 48px; height: 48px; border-radius: 50%; background: {RED};
      font: 700 36px/48px "Oswald", sans-serif; font-style: normal; text-align: center; color: #fff; }}
    .§ad {{ position: absolute; left: 140px; top: 300px; width: 800px; height: 700px; border-radius: 26px; background: #161616;
      border: 3px solid #3a3a3a; overflow: hidden; opacity: 0; }}
    .§adph {{ position: absolute; left: 22px; top: 22px; width: 750px; height: 430px; border-radius: 14px; overflow: hidden; background: #222; }}
    .§adph img {{ width: 100%; height: 100%; object-fit: cover; filter: saturate(0.1) blur(9px) brightness(0.85); transform: scale(1.08); }}
    .§bar {{ position: absolute; left: 22px; height: 30px; border-radius: 8px; background: #2c2c2c; }}
    .§wc {{ position: absolute; right: 70px; top: 150px; text-align: right; opacity: 0; font-family: "Oswald", sans-serif; font-weight: 700; }}
    .§wcl {{ display: block; font-size: 40px; letter-spacing: 0.08em; color: #bdbdbd; }}
    .§wcn {{ display: block; font-size: 120px; line-height: 1; color: {RED}; }}
"""


def pills():
    return ('<div id="§pills" class="§pills">' + "".join(
        f'<div id="§p{i}" class="§pill" style="top:{i * 84}px"><i>!</i>{w}</div>' for i, w in enumerate(WARN)) + "</div>")


def ad():
    return ('<div id="§ad" class="§ad"><div class="§adph"><img src="assets/img/20140606_174216.jpg"></div>'
            '<div class="§bar" style="top:482px;width:520px"></div><div class="§bar" style="top:532px;width:360px;background:#242424"></div>'
            '<div class="§bar" style="top:604px;width:230px;height:46px;background:#333"></div>'
            '<div class="§bar" style="top:614px;left:560px;width:200px;height:26px;background:#242424"></div></div>')


def scene_01():
    hud = title("t1", ["L'ANNONCE", "QUE PERSONNE", "NE VOULAIT."], 590, 168)
    js = X_JS + """
      // brutal: the three lines slam in on the voice, the first one from the first frames (works without sound)
      slam("t1-0", 0.0, { s: 1.35, d: 0.16 }); shake("hud", 0.05, 10);
      slam("t1-1", Math.max(0.35, at("personne") - 0.05), { s: 1.35, d: 0.16 });
      slam("t1-2", Math.max(0.7, at("ne") - 0.05), { s: 1.35, d: 0.16 }); shake("hud", Math.max(0.7, at("ne") - 0.05), 12);
      stroke6("t1", Math.max(0.9, at("ne") + 0.15));
    """
    return "", "", hud, js, None, [("impact-bass-1", None, 1, 0.0, 0.5)]


def scene_02():
    css = WARN_CSS
    st = ad()
    hud = ('<div id="§wc" class="§wc"><span class="§wcl">WARNINGS</span><span class="§wcn">' + odo("wn", "0") + '</span></div>' + pills())
    cues = [("photos", 1), ("vendeur", 1), ("connaît", 1), ("téléphone", 1), ("vend", 1)]
    js = X_JS + """
      // a neutral ad mock-up: grey frame, blurred photo, no logo, no brand
      pre("ad", { opacity: 0, scale: 0.96 }); go("ad", { opacity: 1, scale: 1 }, 0.05, 0.35);
      fin("wc", at("photos") - 0.1);
    """
    for i, (w, n) in enumerate(cues):
        js += f"""
      // warning {i + 1}: the red pill pops in, the counter climbs
      pre("p{i}", {{ opacity: 0, x: -50, scale: 1 }}); go("p{i}", {{ opacity: 1, x: 0 }}, at("{w}") - 0.05, 0.22);
      tl.fromTo($("p{i}"), {{ scale: 1.12 }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }}, at("{w}") - 0.05);
      odo("wn", at("{w}") - 0.05, 0.25, {{ to: "{i + 1}", spinLow: false }});
      tl.fromTo($("wc"), {{ scale: 1.25 }}, {{ scale: 1, duration: 0.3, ease: "power3.out", immediateRender: false }}, at("{w}") - 0.05);"""
    js += """
      // five reasons to walk away: the ad goes dark
      go("ad", { opacity: 0.35 }, at("cinq") - 0.1, 0.4, "none");
    """
    sfx = [("pop", w, n, -0.05, 0.35) for w, n in cues]
    return css, st, hud, js, None, sfx


def scene_03():
    css = WARN_CSS + f"""
    #§zero {{ position: absolute; left: 540px; top: 590px; width: 540px; text-align: center; font: 700 440px/1 "Oswald", sans-serif; color: #FB8000; opacity: 0; }}
    #§div {{ position: absolute; left: 539px; top: 460px; width: 3px; height: 560px; background: #3a3a3a; transform-origin: 50% 0; }}
    """
    st = ad()
    hud = ('<div id="§wc" class="§wc"><span class="§wcl">WARNINGS</span><span class="§wcn">5</span></div>' + pills()
           + '<div id="§div"></div>'
           + title("tl", ["SUR LE VENDEUR"], 470, 60, "left:0;width:540px") + title("tr", ["SUR LA VOITURE"], 470, 60, "left:540px;width:540px")
           + '<div id="§zero">0</div>')
    js = X_JS + """
      // where scene 2 ended: the dark ad, five pills, the counter at 5
      pre("ad", { opacity: 0.35 }); pre("wc", { opacity: 1 });
      for (var i = 0; i < 5; i++) pre("p" + i, { opacity: 1 });
      // the pills gather in the centre, the ad and the counter go
      go("ad", { opacity: 0 }, 0.1, 0.3, "none"); go("wc", { opacity: 0 }, 0.1, 0.3, "none");
      pre("pills", { x: 0, y: 0, scale: 1 }); go("pills", { y: -380 }, 0.15, 0.55, "power3.inOut");
      // then slide as one block to the left, under « sur le vendeur »
      var tv = Math.max(1.0, at("vendeur") - 0.35);
      go("pills", { x: -118, y: -430, scale: 0.6 }, tv, 0.55, "power3.inOut");
      tin("tl", 1, tv + 0.25);
      pre("div", { scaleY: 0 }); go("div", { scaleY: 1 }, tv + 0.25, 0.4);
      // the right side stays empty under « sur la voiture », then a big orange 0
      tin("tr", 1, at("voiture") - 0.1);
      slam("zero", at("aucun") - 0.05, { s: 1.5, d: 0.2 });
      tl.fromTo($("zero"), { textShadow: "0 0 0px rgba(251,128,0,0)" }, { textShadow: "0 0 60px rgba(251,128,0,0.55)", duration: 0.5, immediateRender: false }, at("vérifier") - 0.1);
    """
    return css, st, hud, js, None, [("impact-bass-2", "aucun", 1, -0.05, 0.45)]


CHECK = [("CARNET À JOUR", "DERNIER ENTRETIEN À 54 000 KM", "carnet"), ("CONTRÔLE TECHNIQUE VIERGE", "", "contrôle"),
         ("RAPPEL CONSTRUCTEUR : FAIT", "", "rappel"), ("HISTORIQUE COMPLET", "", "historique")]


def scene_04():
    css = """
    .§row { position: absolute; left: 90px; width: 940px; height: 150px; }
    .§row svg { position: absolute; left: 0; top: 6px; width: 84px; height: 84px; overflow: visible; }
    .§rt { position: absolute; left: 116px; top: 0; font: 700 66px/96px "Oswald", sans-serif; color: #fff; white-space: nowrap; opacity: 0; }
    .§rs { position: absolute; left: 118px; top: 92px; font: 500 38px/44px "Oswald", sans-serif; color: #9a9a9a; white-space: nowrap; opacity: 0; letter-spacing: 0.02em; }
    """
    hud = ""
    js = X_JS
    for i, (txt, sub, w) in enumerate(CHECK):
        y = 470 + i * 205
        hud += (f'<div class="§row" style="top:{y}px"><svg viewBox="0 0 84 84">'
                f'<rect id="§bx{i}" x="3" y="3" width="78" height="78" rx="12" fill="none" stroke="#FB8000" stroke-width="6"/>'
                f'<path id="§ck{i}" d="M20 44 L36 60 L64 26" fill="none" stroke="#FB8000" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
                f'<div id="§rt{i}" class="§rt">{txt}</div>' + (f'<div id="§rs{i}" class="§rs">{sub}</div>' if sub else "") + "</div>")
        js += f"""
      // line {i + 1}: the box draws, the line comes in, the orange tick
      draw("bx{i}", at("{w}") - 0.1, 0.25, "none"); fin("rt{i}", at("{w}") - 0.05); draw("ck{i}", at("{w}") + 0.2, 0.2, "power2.out");"""
    js += """
      fin("rs0", at("54000km") - 0.1);
      // a listing is judged on the file: the four ticks pulse
      for (var i = 0; i < 4; i++) tl.fromTo($("ck" + i), { scale: 1 }, { scale: 1.25, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "50% 50%", immediateRender: false }, at("dossier") - 0.1 + i * 0.06);
    """
    sfx = [("click-soft", w, 1, 0.2, 0.35) for _, _, w in CHECK]
    return css, "", hud, js, None, sfx


def scene_05():
    css = """
    #§box { position: absolute; left: 70px; top: 760px; width: 940px; height: 270px; opacity: 1; }
    #§box svg { position: absolute; left: 0; top: 0; width: 940px; height: 270px; overflow: visible; }
    #§bg { position: absolute; left: 0; top: 0; width: 940px; height: 270px; border-radius: 24px; background: rgba(10,10,10,0.72); opacity: 0; }
    .§bl { position: absolute; left: 0; width: 940px; text-align: center; font: 700 64px/1 "Oswald", sans-serif; color: #fff; white-space: nowrap; opacity: 0; }
    """
    st = (full("ph1", "20140606_174128.jpg", contain=True) + full("ph2", "20140606_174216.jpg", "22% 50%")
          + full("ph3", "20140606_174140.jpg", "62% 50%") + '<div class="§shade"></div>')
    hud = (title("t1", ["911 TYPE 997", "PHASE 2 — 2009"], 290, 104) + title("t2", ["FLAT 6 3.6", "345 CH"], 290, 104)
           + title("t3", ["PDK", "7 RAPPORTS"], 290, 104)
           + '<div id="§box"><div id="§bg"></div><svg viewBox="0 0 940 270"><rect id="§bx" x="2" y="2" width="936" height="266" rx="24" fill="none" stroke="#FB8000" stroke-width="4"/></svg>'
           + '<div id="§b1" class="§bl" style="top:58px">PHASE 2 = <span class="§o">INJECTION DIRECTE</span></div>'
           + '<div id="§b2" class="§bl" style="top:150px">PLUS D\'<span class="§o">ARBRE INTERMÉDIAIRE</span></div></div>')
    js = X_JS + """
      // the first photo full frame, then the side, then the cockpit (the PDK lever)
      tl.set($("ph1"), { opacity: 1 }, 0); photo("ph1", 0, at("flat"), 1.04);
      tin("t1", 2, Math.max(0.1, at("911") - 0.1));
      tout("t1", 2, at("flat") - 0.25); photo("ph2", at("flat") - 0.15, at("boîte"), 1.04); tin("t2", 2, at("flat") - 0.05);
      tout("t2", 2, at("boîte") - 0.25); photo("ph3", at("boîte") - 0.15, DUR, 1.05); tin("t3", 2, at("boîte") - 0.05);
      // the detached box, traced by the orange line: what makes a phase 2
      tout("t3", 2, at("surtout") - 0.2);
      go("ph3", { opacity: 0.4 }, at("surtout") - 0.1, 0.4, "none");
      fin("bg", at("surtout")); draw("bx", at("surtout"), 0.45, "power2.inOut");
      fin("b1", at("injection") - 0.1); fin("b2", at("d'arbreintermédiaire") - 0.1);
    """
    return css, st, hud, js, None, [("whoosh-short", "surtout", 1, 0.0, 0.18)]


def scene_06():
    st = full("ph", "20140606_174224.jpg", "38% 50%") + '<div class="§shade"></div>'
    hud = (title("y", ["2014."], 330, 230) + title("a", ["25 ANS."], 330, 230) + title("p", ["MA PREMIÈRE", "PORSCHE."], 330, 140)
           + '<div id="§amt" class="§txt" style="top:360px;font-size:220px">' + odo("am", "44 000 €") + '</div>')
    js = X_JS + """
      photo("ph", 0, DUR, 1.04); tl.set($("ph"), { opacity: 1 }, 0);
      tin("y", 1, Math.max(0.05, at("2014") - 0.1));
      tout("y", 1, at("25ans") - 0.25); tin("a", 1, at("25ans") - 0.1);
      tout("a", 1, at("première") - 0.25); tin("p", 2, at("première") - 0.1);
      tout("p", 2, at("44000euros") - 0.25);
      fin("amt", at("44000euros") - 0.1); odo("am", at("44000euros") - 0.05, 1.1, { from: "00 000", dimLead: true });
      tl.fromTo($("am"), { color: "#ffffff" }, { color: "#FB8000", duration: 0.2, immediateRender: false }, at("44000euros") + 1.05);
    """
    return "", st, hud, js, None, []


ROWS = [("ENTRETIEN COURANT", "1 000 €", "1000euros", "0 000"), ("2 PNEUMATIQUES", "450 €", "450euros", "000"),
        ("REVENDUE 2 ANS PLUS TARD", "52 000 €", "52000", "00 000")]


def scene_07():
    css = """
    .§rw { position: absolute; left: 80px; width: 920px; height: 120px; opacity: 0; border-bottom: 2px solid #2e2e2e; }
    .§rl { position: absolute; left: 0; top: 30px; font: 600 50px/60px "Oswald", sans-serif; color: #cfcfcf; white-space: nowrap; }
    .§rv { position: absolute; right: 0; top: 14px; font: 700 80px/1 "Oswald", sans-serif; color: #fff; white-space: nowrap; }
    #§gain { position: absolute; left: 0; top: 1040px; width: 1080px; text-align: center; font: 700 210px/1 "Oswald", sans-serif; color: #FB8000; opacity: 0; }
    """
    hud = "".join(f'<div id="§r{i}" class="§rw" style="top:{470 + i * 150}px"><span class="§rl">{l} :</span><span class="§rv">{odo(f"v{i}", v)}</span></div>'
                  for i, (l, v, _, _) in enumerate(ROWS))
    hud += '<div id="§gain">+ ' + odo("gv", "6 550 €") + '</div>'
    js = X_JS
    for i, (_, _, w, fr) in enumerate(ROWS):
        js += f"""
      pre("r{i}", {{ opacity: 0, y: 30 }}); go("r{i}", {{ opacity: 1, y: 0 }}, at("{w}") - 0.15, 0.3); odo("v{i}", at("{w}") - 0.1, 0.9, {{ from: "{fr}", dimLead: true }});"""
    js += """
      // the gap, big and orange
      pre("gain", { opacity: 0, scale: 0.85 }); go("gain", { opacity: 1, scale: 1 }, at("6550euros") - 0.15, 0.3, "back.out(1.6)");
      odo("gv", at("6550euros") - 0.1, 1.2, { from: "0 000", dimLead: true });
    """
    return css, "", hud, js, None, [("pop", "6550euros", 1, -0.1, 0.3)]


def scene_08():
    css = """
    #§tlw { position: absolute; left: 100px; top: 360px; width: 880px; height: 160px; }
    #§tlw svg { position: absolute; left: 0; top: 0; width: 880px; height: 120px; overflow: visible; }
    .§yr { position: absolute; top: 84px; font: 700 64px/1 "Oswald", sans-serif; color: #9a9a9a; opacity: 0; }
    #§since { position: absolute; left: 0; top: 1020px; width: 1080px; text-align: center; font: 700 76px/1 "Oswald", sans-serif; color: #fff; opacity: 0; }
    #§big { position: absolute; left: 0; top: 1110px; width: 1080px; text-align: center; font: 700 230px/1 "Oswald", sans-serif; color: #FB8000; opacity: 0; }
    #§note { position: absolute; left: 0; top: 1395px; width: 1080px; text-align: center; font: 500 36px/1 "Oswald", sans-serif; color: #8c8c8c; opacity: 0; letter-spacing: 0.02em; }
    """
    ticks = "".join(f'<path id="§tk{k}" d="M{20 + k * 70} 14 L{20 + k * 70} 58" stroke="#FB8000" stroke-width="{8 if k in (0, 12) else 4}" opacity="0"/>' for k in range(13))
    hud = (f'<div id="§tlw"><svg viewBox="0 0 880 120"><path id="§ln" d="M20 36 L860 36" stroke="#FB8000" stroke-width="8" stroke-linecap="round" fill="none"/>{ticks}</svg>'
           '<div id="§y0" class="§yr" style="left:-20px">2014</div><div id="§y1" class="§yr" style="right:-20px;color:#FB8000">2026</div></div>'
           + title("t1", ["AUJOURD'HUI,", "LES MÊMES S'AFFICHENT"], 620, 92)
           + '<div id="§since">À PARTIR DE</div><div id="§big">' + odo("bg", "57 000 €") + '</div>'
           + '<div id="§note">prix demandés, France, octobre 2026</div>')
    js = X_JS + """
      // a timeline from 2014 to 2026 draws in orange, one tick per year
      fin("y0", 0.05); draw("ln", 0.1, 1.3, "power1.inOut");
      for (var k = 0; k < 13; k++) { pre("tk" + k, { opacity: 0 }); go("tk" + k, { opacity: 1 }, 0.1 + k * 0.1, 0.12, "none"); }
      fin("y1", 1.35);
      tin("t1", 2, at("aujourd'hui") - 0.1);
      fin("since", at("partir") - 0.15);
      fin("big", at("57000euros") - 0.15); odo("bg", at("57000euros") - 0.1, 1.2, { from: "00 000", dimLead: true });
      fin("note", at("57000euros") + 0.3);
    """
    return css, "", hud, js, None, []


def scene_09():
    css = """
    #§hn { position: absolute; left: 0; top: 1130px; width: 1080px; text-align: center; font: 700 72px/1 "Oswald", sans-serif; color: #FB8000; opacity: 0; }
    """
    tc = last_end() + 0.35
    st = full("ph", "20140607_183242.jpg", "22% 50%") + '<div class="§shade"></div><div id="§dk" style="position:absolute;left:0;top:0;width:1080px;height:1920px;background:#0A0A0A;opacity:0"></div>'
    hud = (title("t1", ["UNE MAUVAISE ANNONCE", "N'EST PAS UNE", "MAUVAISE VOITURE."], 760, 100)
           + title("t2", ["TU SERAIS ALLÉ VOIR", "CETTE ANNONCE, TOI ?"], 780, 104) + '<div id="§hn">@guillaumeherbin_</div>')
    js = X_JS + f"""
      // the lesson: slower, the last photo held long, the music gone
      pre("ph", {{ opacity: 0, scale: 1 }}); go("ph", {{ opacity: 0.75 }}, 0.05, 0.8, "none"); go("ph", {{ scale: 1.03 }}, 0, DUR, "none");
      tin("t1", 3, Math.max(0.2, at("mauvaise") - 0.15), 0.45);
      // CTA, no voice
      tout("t1", 3, {tc} - 0.25);
      go("dk", {{ opacity: 0.6 }}, {tc} - 0.25, 0.4, "none");
      tin("t2", 2, {tc} + 0.1); fin("hn", {tc} + 0.6);
    """
    return css, st, hud, js, None, []


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
    <div id="§hud" class="§cam §hudcam">
      {hud}
    </div>
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
message: "Une annonce qui fait fuir tout le monde, un acheteur qui vérifie au lieu de juger : les cinq warnings portaient sur le vendeur, aucun sur la voiture. Une mauvaise annonce n'est pas une mauvaise voiture."
arc: Hook → Les warnings → Le retournement → Ce que j'ai vérifié → La voiture → Le prix → Les deux ans → 2026 → La leçon et CTA
audience: "Personnes qui veulent se lancer dans l'achat-revente automobile"
mode: autonomous
captions: disabled
music: "pre-mixed with voice and SFX in assets/audio/mix.wav (mounted at root by the orchestrator)"
direction: "brief de Guillaume (SCRIPT.md), reel 9:16, motion design sur fond noir et photos de 2014"
styleframes: "aucune"
patterns: ../patterns/STORYBOARD-CRAFT.md, ../patterns/PATTERNS.md
---

<!-- generated by build.py: edit build.py, not this file -->

## Video direction

- **One world** : fond #0A0A0A, accent unique #FB8000, texte blanc, rouge #E03131 pour les seules pastilles de warning ; Oswald en capitales, trait orange tracé sous chaque titre en 6 frames ; sous-titres de la voix mot par mot à 12 % du bas, mot-clé en orange.
- **Seams** : coupes franches sur la voix à chaque scène (whoosh court).
- **Timing** : chaque animation est posée sur un mot de la voix (build.py), les durées des scènes suivent la piste voix.
- **Negative list** : les 5 photos de juin 2014 uniquement, pas d'image générée ; plaques et enseigne du garage floutées ; aucun logo ni capture de site d'annonces ; jamais « vaut 57 000 € » ; pas de billets.

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
