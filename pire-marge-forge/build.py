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
TAIL = 2.6          # hold after the last word (end card)
FPS = 30

# ---------------------------------------------------------------------------------------------------------------------
# The voice, scene by scene, cut into subtitle chunks (2 to 5 words). *word* = key word (orange). ~ glues two tokens
# into one subtitle word (« 10~000 », « voitures~? »). Numbers are spoken « dix mille », « deux mille vingt-six ».
SCENES = [
 dict(id="01-hook", name="Hook", window=(0, 3.5), chunks=[
   "Ma pire *marge*", "en *16* ans de métier,", "c'est sur une *Ferrari*."]),
 dict(id="02-achat", name="L'achat", window=(3.5, 11), chunks=[
   "Une 360 Modena.", "Achetée *49~000* euros.", "Sur *photos*.", "À quelqu'un", "avec qui je travaillais", "depuis des *années*."]),
 dict(id="03-retour", name="Le retour", window=(11, 18), chunks=[
   "Je la *revends*", "en quelques semaines.", "Le client *revient*~:", "moteur qui *chauffe*.", "Je *rembourse* tout,",
   "carte grise comprise."]),
 dict(id="04-mecanique", name="La mécanique", window=(18, 27), chunks=[
   "Joint de *culasse*.", "*Dépose* moteur.", "Le mécano *abandonne*", "en plein chantier.", "Je repars de *zéro*.",
   "Plus d'un an", "*immobilisée*."]),
 dict(id="05-resultat", name="Revente et résultat", window=(27, 36), chunks=[
   "*15~000* euros", "de mécanique.", "Je finis par la revendre", "*50~000* euros", "à l'*export*.", "Résultat~:",
   "moins *16~800* euros."]),
 dict(id="06-erreurs", name="Les trois erreurs", window=(36, 45), chunks=[
   "Trois *erreurs*.", "J'ai acheté avec le *cœur*,", "sans mes contrôles habituels.", "J'ai confié le moteur", "à quelqu'un",
   "qui n'en était pas *capable*.", "Et j'ai voulu", "gérer *seul*."]),
 dict(id="07-pivot", name="Le pivot", window=(45, 54), chunks=[
   "Mais le vrai problème", "est *ailleurs*.", "C'était mon *argent*", "dans la voiture.", "*49~000* euros *bloqués*",
   "pendant plus de trois ans.", "Chaque erreur,", "c'est *moi* qui l'ai payée."]),
 dict(id="08-comparaison", name="La comparaison", window=(54, 62), chunks=[
   "Quand tu vends la voiture", "de quelqu'un d'autre", "*sans* l'acheter,", "tu ne mets pas", "*un~euro* dedans.",
   "Si ça se passe mal,", "tu perds du *temps*.", "Pas *16~800* euros."]),
 dict(id="09-signature", name="Signature", window=(62, 68), chunks=[
   "C'est le *métier*", "qu'on apprend chez *FORGE*.", "Moi, c'est", "*Guillaume~Herbin*,", "fondateur", "du programme *FORGE*."]),
 dict(id="10-fin", name="Carton de fin", window=(68, 75), chunks=[
   "Si tu veux plus", "de contenus comme celui-ci,", "ou si tu t'intéresses", "aux métiers", "de la vente automobile,",
   "*abonne-toi*."]),
]
SPOKEN_SYL = {"16": 1, "360": 5, "49000": 5, "50000": 3, "15000": 3, "16800": 6, "uneuro": 3, "guillaumeherbin": 4}
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
      font: 700 60px/72px ⟦FU⟧, sans-serif; color: ⟦TEXT⟧; text-shadow: 0 3px 18px rgba(0,0,0,0.7); }
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
            if (w.classList.contains("sub-key")) tl.fromTo(w, { color: "⟦TEXT⟧" }, { color: "⟦KEY⟧", duration: 0.12, ease: "power3.out", immediateRender: false }, t);
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


def scene_01():
    css = MEDIA_CSS + """
    #§bg { left: 0; top: 0; width: 1080px; height: 1920px; }
    #§bg img { filter: saturate(0.6) brightness(0.38); }
    #§sub1 { position: absolute; left: 0; top: 1060px; width: 1080px; text-align: center; font: 600 56px/1.2 ⟦FU⟧, sans-serif;
      color: ⟦TEXT_SOFT⟧; letter-spacing: 0.08em; opacity: 0; }
    #§sub1 b { color: ⟦KEY⟧; font-weight: 600; }
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
    #§phone { position: absolute; left: 110px; top: 600px; width: 340px; height: 640px; border-radius: 46px; background: #050505; border: 6px solid #3a3a3a;
      box-shadow: 0 30px 80px rgba(0,0,0,0.7); opacity: 0; }
    #§scr { left: 14px; top: 46px; width: 300px; height: 540px; border-radius: 10px; background: #141414; }
    #§notch { position: absolute; left: 120px; top: 16px; width: 88px; height: 14px; border-radius: 7px; background: #222; }
    #§nocheck { position: absolute; left: 650px; top: 640px; width: 260px; height: 260px; overflow: visible; fill: none; stroke: ⟦TEXT⟧; stroke-linecap: round; opacity: 0; }
    """
    phones = ["achat.jpg", "ph-interieur.jpg", "ph-moteur19.jpg", "ph-feux.jpg", "ph-roue19.jpg", "achat.jpg"]
    st = ('<div id="§phone"><div id="§notch"></div><div id="§scr" class="§burst">' + "".join(f'<img src="assets/img/{p}">' for p in phones) + '</div></div>'
          + person("sel", 660, 900, 200) +
          f'<svg id="§nocheck" viewBox="0 0 160 160">{MAG}<path d="M10 150 L150 10" stroke="⟦LINE⟧" stroke-width="16"/></svg>')
    hud = title("t2", ["360 MODENA.", "ACHETÉE SUR PHOTOS."], 360, 96) + total("00 000 €")
    js = TOT_JS + MEDIA_JS + """
      totInit("00 000"); pre("tot", { opacity: 0 });
      slam("t2-0", at("360") - 0.05, { s: 1.3 });
      pre("phone", { opacity: 0, y: 80, rotation: -4 }); go("phone", { opacity: 1, y: 0, rotation: -2 }, 0.05, 0.45, "expo.out");
      // the photos received on the phone, one after the other
      var p0 = at("360") - 0.05, p1 = at("photos"), ps = Math.max(0.25, (p1 - p0) / 5);
      burst("scr", [p0, p0 + ps, p0 + 2 * ps, p0 + 3 * ps, p0 + 4 * ps, p1]);
      slam("tot", at("49000") - 0.1, { s: 1.2 }); odo("totv", at("49000") - 0.05, 0.9, { to: "49 000 €" });
      slam("t2-1", at("photos") - 0.05); stroke("t2", at("photos") + 0.2);
      // a seller he had worked with for years: trusted, nothing checked
      init("sel-w", { opacity: 0 }); init("sel-o", { opacity: 0 }); init("sel-glow", { opacity: 0 });
      pre("sel", { opacity: 0, y: 40 }); go("sel", { opacity: 1, y: 0 }, at("quelqu'un") - 0.05, 0.3, "back.out(1.6)");
      lit("sel", "white", at("travaillais"), 0.3);
      go("sel", { opacity: 0.35 }, at("années") - 0.05, 0.3);
      pre("nocheck", { opacity: 0, scale: 0.4 }); go("nocheck", { opacity: 1, scale: 1 }, at("années") - 0.06, 0.25, "back.out(2)");
      cam(0, -10, 1.04, at("quelqu'un"), 0.8);
    """
    sfx = [("pop", "360", 1, -.05, .14), ("notification", "modena", 1, -.05, .2), ("typing", "49000", 1, -.05, .12),
           ("pop", "photos", 1, -.05, .14), ("pop", "quelqu'un", 1, -.05, .12), ("click", "années", 1, -.06, .25)]
    return css, st, hud, js, (300, 900), sfx


def scene_03():
    css = PHOTO_CSS + MEDIA_CSS + TOT_CSS + f"""
    #§ph {{ left: 90px; top: 620px; width: 900px; height: 470px; }}
    #§hand {{ position: absolute; left: 330px; top: 1000px; width: 420px; height: 224px; overflow: visible; fill: none; stroke: ⟦TEXT⟧; stroke-width: 12;
      stroke-linecap: round; stroke-linejoin: round; opacity: 0; }}
    #§handbg {{ position: absolute; left: 300px; top: 980px; width: 480px; height: 260px; border-radius: 30px; background: rgba(10,10,10,0.9); opacity: 0; }}
    #§dash {{ left: 100px; top: 600px; width: 330px; height: 660px; opacity: 0; }}
    #§ring {{ position: absolute; left: 600px; top: 590px; width: 240px; height: 352px; overflow: visible; fill: none; stroke: ⟦TEXT⟧; stroke-width: 10;
      stroke-linecap: round; stroke-linejoin: round; opacity: 0; }}
    .§wave {{ stroke: ⟦LINE⟧; }}
    #§gauge {{ position: absolute; left: 500px; top: 940px; width: 450px; height: 300px; overflow: visible; fill: none; stroke-linecap: round; opacity: 0; }}
    #§glab {{ position: absolute; left: 500px; top: 1190px; width: 450px; text-align: center; font: 600 28px ⟦FU⟧, sans-serif; color: ⟦MUTED⟧; letter-spacing: 0.1em; opacity: 0; }}
    """
    st = ('<div id="§ph" class="§photo"><img src="assets/img/ph-profil.jpg"></div>'
          '<div id="§handbg"></div><svg id="§hand" viewBox="0 0 300 160">'
          '<path d="M0 50 L26 50 L26 126 L0 126"/><path d="M300 50 L274 50 L274 126 L300 126"/>'
          '<path d="M26 64 L92 64 Q112 64 128 76 L176 108 Q188 117 180 127 Q172 135 160 128 L132 110"/>'
          '<path d="M274 64 L208 64 Q188 64 172 76 L124 110 Q112 119 120 129 Q128 137 140 130 L170 112"/>'
          '<path d="M120 96 L150 118 M106 106 L136 128" stroke="⟦LINE⟧"/></svg>'
          '<div id="§dash" class="§sprite" style="background-image:url(assets/img/sp-dash.jpg)"></div>'
          '<svg id="§ring" viewBox="0 0 300 440"><g id="§ringph"><rect x="70" y="80" width="160" height="300" rx="28"/><path d="M128 110 L172 110"/>'
          '<path d="M130 350 L170 350"/></g><path class="§wave" d="M260 140 Q290 180 260 220"/><path class="§wave" d="M40 140 Q10 180 40 220"/>'
          '<path class="§wave" d="M280 110 Q330 180 280 250"/><path class="§wave" d="M20 110 Q-30 180 20 250"/></svg>'
          f'<svg id="§gauge" viewBox="0 0 300 200"><path d="M40 170 A110 110 0 0 1 260 170" stroke="#3a3a3a" stroke-width="20"/>'
          f'<path d="M226 92 A110 110 0 0 1 260 170" stroke="{RED}" stroke-width="20"/>'
          '<line id="§needle" x1="150" y1="170" x2="150" y2="80" stroke="⟦TEXT⟧" stroke-width="9"/><circle cx="150" cy="170" r="14" fill="⟦TEXT⟧"/></svg>'
          '<div id="§glab">TEMPÉRATURE MOTEUR</div>')
    hud = (title("t3", ["TOUT REMBOURSÉ."], 380, 110) + total("49 000 €")
           + chip("c1", 260, 640, "+2 000 €", "CARTE GRISE") + chip("c2", 600, 640, "+800 €", "TRANSPORT"))
    js = TOT_JS + MEDIA_JS + """
      totInit("49 000");
      // sold in a few weeks
      pre("ph", { opacity: 0, scale: 1.08 }); go("ph", { opacity: 1, scale: 1 }, at("revends") - 0.08, 0.4, "expo.out");
      init("ph", { opacity: 1, scale: 1, x: 0 }); go("ph", { x: -30 }, at("revends"), 1.6, "none");
      pre("handbg", { opacity: 0 }); go("handbg", { opacity: 1 }, at("semaines") - 0.1, 0.2);
      pre("hand", { opacity: 0, scale: 0.6 }); go("hand", { opacity: 1, scale: 1 }, at("semaines") - 0.06, 0.35, "back.out(1.8)");
      go("ph", { opacity: 0 }, at("client") - 0.12, 0.2); go("hand", { opacity: 0 }, at("client") - 0.12, 0.2); go("handbg", { opacity: 0 }, at("client") - 0.12, 0.2);
      // the buyer comes back: the engine overheats (the real dashboard)
      pre("ring", { opacity: 0, scale: 0.7 }); go("ring", { opacity: 1, scale: 1 }, at("client") - 0.1, 0.3, "back.out(2)");
      wobble("ringph", at("revient"), 7); wobble("ringph", at("revient") + 0.35, 6);
      pre("dash", { opacity: 0, x: -60 }); go("dash", { opacity: 1, x: 0 }, at("moteur") - 0.15, 0.35, "expo.out");
      sprite("dash", at("moteur") - 0.15, Math.max(1.2, at("rembourse") - at("moteur") + 0.3), 36, 6, 12);
      go("ring", { opacity: 0, scale: 0.8 }, at("moteur") + 0.1, 0.25);
      pre("gauge", { opacity: 0, y: 30 }); go("gauge", { opacity: 1, y: 0 }, at("moteur") - 0.05, 0.3); pre("glab", { opacity: 0 }); go("glab", { opacity: 1 }, at("moteur"), 0.3);
      tl.set($("needle"), { svgOrigin: "150 170", rotation: -70 }, 0);
      tl.fromTo($("needle"), { rotation: -70 }, { rotation: 62, duration: 0.7, ease: "power2.in", immediateRender: false }, at("chauffe") - 0.25);
      // full refund: the costs go into the TOTAL
      go("dash", { opacity: 0, x: -60 }, at("rembourse") - 0.15, 0.3); go("gauge", { opacity: 0 }, at("rembourse") - 0.15, 0.3); go("glab", { opacity: 0 }, at("rembourse") - 0.15, 0.3);
      slam("t3-0", at("rembourse") - 0.04); stroke("t3", at("tout") + 0.1);
      bump("c1", at("carte") - 0.15, "51 000 €");
      bump("c2", at("comprise") + 0.05, "51 800 €");
    """
    sfx = [("pop", "revends", 1, -.08, .14), ("pop", "semaines", 1, -.06, .14), ("notification", "client", 1, -.1, .25),
           ("whoosh-short", "moteur", 1, -.15, .12), ("error", "chauffe", 1, .3, .18), ("pop", "rembourse", 1, -.05, .14),
           ("pop", "carte", 1, -.15, .14), ("typing", "carte", 1, .95, .12), ("pop", "comprise", 1, .05, .14)]
    return css, st, hud, js, (540, 880), sfx


def engine_css():
    return f"""
    #§eng {{ position: absolute; left: 140px; top: 640px; width: 800px; height: 560px; overflow: visible; fill: none; stroke-linejoin: round; stroke-linecap: round; }}
    .§eb {{ stroke: ⟦TEXT⟧; stroke-width: 7; fill: #141414; }}
    .§head {{ stroke: ⟦TEXT⟧; stroke-width: 7; fill: #141414; }}
    .§dist circle, .§dist path {{ stroke: ⟦LINE⟧; stroke-width: 7; fill: none; }}
    #§hoist {{ stroke: ⟦MUTED⟧; stroke-width: 6; stroke-dasharray: 10 10; }}
    """


def scene_04():
    css = PHOTO_CSS + MEDIA_CSS + TOT_CSS + engine_css() + """
    #§ph { left: 90px; top: 600px; width: 900px; height: 420px; opacity: 0; }
    #§ph2 { left: 140px; top: 620px; width: 800px; height: 560px; opacity: 0; }
    #§gar { left: 375px; top: 590px; width: 330px; height: 620px; opacity: 0; }
    #§mech { opacity: 0; }
    #§wrench { position: absolute; left: 840px; top: 900px; width: 110px; height: 110px; overflow: visible; fill: none; stroke: ⟦TEXT⟧; stroke-width: 10;
      stroke-linecap: round; opacity: 0; }
    #§cal { position: absolute; left: 370px; top: 860px; width: 340px; height: 300px; border-radius: 26px; background: #151515; border: 3px solid #2e2e2e; opacity: 0; overflow: hidden; }
    #§calh { position: absolute; left: 0; top: 0; width: 100%; height: 64px; background: #2a2a2a; }
    #§calv { position: absolute; left: 0; top: 76px; width: 100%; text-align: center; font: 140px/1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
    #§calm { position: absolute; left: 0; top: 236px; width: 100%; text-align: center; font: 600 32px ⟦FU⟧, sans-serif; color: ⟦MUTED⟧; letter-spacing: 0.1em; }
    """
    st = (f'<svg id="§eng" viewBox="0 0 600 420"><path id="§hoist" d="M300 12 L300 30 M300 30 L180 70 M300 30 L420 70"/>'
          f'<g id="§motor">{ENGINE}{DISTRI}</g></svg>'
          '<div id="§ph" class="§photo"><img src="assets/img/moteur.jpg"></div>'
          '<div id="§ph2" class="§photo"><img src="assets/img/ph-moteur22.jpg"></div>'
          '<div id="§gar" class="§sprite" style="background-image:url(assets/img/sp-garage.jpg);background-size:900% 300%"></div>'
          + person("mech", 760, 830, 170)
          + '<svg id="§wrench" viewBox="0 0 110 110"><path d="M20 90 L64 46"/><circle cx="76" cy="34" r="20"/></svg>'
          + '<div id="§cal"><div id="§calh"></div><div id="§calv">' + odo("mo", "14") + '</div><div id="§calm">MOIS</div></div>')
    hud = (title("t4", ["JOINT DE CULASSE.", "DÉPOSE MOTEUR."], 360, 104) + title("t5", ["REPARTIR DE ZÉRO."], 380, 110)
           + title("t5b", ["PLUS D’UN AN", "IMMOBILISÉE."], 350, 100) + total("51 800 €"))
    js = TOT_JS + MEDIA_JS + f"""
      totInit("51 800");
      pre("eng", {{ opacity: 0, scale: 0.9 }}); go("eng", {{ opacity: 1, scale: 1 }}, 0.02, 0.4, "expo.out");
      tl.set($("distri"), {{ opacity: 0 }}, 0);
      slam("t4-0", at("culasse") - 0.15);
      ["hl", "hr"].forEach(function (h, k) {{
        tl.fromTo($(h), {{ fill: "#141414", stroke: "⟦TEXT⟧" }}, {{ fill: "{RED}", stroke: "{RED}", duration: 0.25, immediateRender: false }}, at("culasse") + k * 0.08);
      }});
      // a Ferrari: the engine comes out
      $("hoist").style.opacity = 0; pre("hoist", {{ opacity: 0 }}); go("hoist", {{ opacity: 1 }}, at("dépose") - 0.15, 0.2);
      go("motor", {{ y: -70 }}, at("dépose"), 0.7, "power2.inOut");
      slam("t4-1", at("dépose") - 0.04); stroke("t4", at("moteur") + 0.1);
      // the mechanic gives up halfway
      go("eng", {{ opacity: 0, y: -40 }}, at("mécano") - 0.2, 0.25, "power2.in"); go("t4", {{ opacity: 0, y: -30 }}, at("mécano") - 0.2, 0.15, "power2.in");
      pre("ph", {{ opacity: 0, scale: 1.08 }}); go("ph", {{ opacity: 1, scale: 1 }}, at("mécano") - 0.15, 0.4, "expo.out");
      init("mech-w", {{ opacity: 0 }}); init("mech-o", {{ opacity: 0 }}); init("mech-glow", {{ opacity: 0 }});
      pre("mech", {{ opacity: 0, y: 40 }}); go("mech", {{ opacity: 1, y: 0 }}, at("mécano") - 0.05, 0.3, "back.out(1.6)"); lit("mech", "white", at("mécano"), 0.25);
      pre("wrench", {{ opacity: 0, rotation: -30 }}); go("wrench", {{ opacity: 1, rotation: 0 }}, at("mécano") + 0.2, 0.3, "back.out(2)");
      go("mech", {{ opacity: 0, y: -30 }}, at("abandonne"), 0.6, "power2.in"); go("wrench", {{ opacity: 0, y: 40, rotation: 40 }}, at("abandonne") + 0.1, 0.5, "power2.in");
      go("ph", {{ opacity: 0 }}, at("chantier") - 0.1, 0.2); pre("ph2", {{ opacity: 0, scale: 1.1 }}); go("ph2", {{ opacity: 1, scale: 1 }}, at("chantier") - 0.1, 0.4, "expo.out");
      // starting over, in the garage
      slam("t5-0", at("repars") - 0.05); stroke("t5", at("zéro") + 0.1);
      go("ph2", {{ opacity: 0 }}, at("repars") - 0.1, 0.2);
      pre("gar", {{ opacity: 0, scale: 0.92 }}); go("gar", {{ opacity: 1, scale: 1 }}, at("repars") - 0.1, 0.35, "expo.out");
      sprite("gar", at("repars") - 0.1, Math.max(1.2, at("plus") - at("repars") + 0.3), 27, 9, 12);
      // more than a year off the road
      go("gar", {{ opacity: 0, x: -200 }}, at("plus") - 0.1, 0.3, "power2.in");
      go("t5", {{ opacity: 0, y: -30 }}, at("plus") - 0.12, 0.14, "power2.in");
      pre("cal", {{ opacity: 0, y: 60 }}); go("cal", {{ opacity: 1, y: 0 }}, at("plus") - 0.1, 0.3, "back.out(1.5)");
      odo("mo", at("plus"), Math.max(1.0, at("immobilisée") + 0.3 - at("plus")), {{ from: "00" }});
      slam("t5b-0", at("an") - 0.05); slam("t5b-1", at("immobilisée") - 0.04); stroke("t5b", at("immobilisée") + 0.2);
      cam(0, -10, 1.04, at("mécano"), 0.8);
    """
    sfx = [("pop", None, 0, 0.02, .12), ("error", "culasse", 1, 0, .18), ("whoosh-short", "dépose", 1, 0, .14),
           ("pop", "mécano", 1, -.05, .14), ("whoosh-short", "abandonne", 1, 0, .12), ("pop", "repars", 1, -.05, .14),
           ("typing", "plus", 1, 0, .12), ("impact-bass-2", "immobilisée", 1, -.04, .26)]
    return css, st, hud, js, (540, 820), sfx


def scene_05():
    css = PHOTO_CSS + MEDIA_CSS + TOT_CSS + """
    #§ph { left: 120px; top: 640px; width: 840px; height: 565px; border: ⟦PHOTO_BORDER⟧ solid ⟦LINE⟧; border-radius: 8px; box-shadow: 0 30px 70px rgba(0,0,0,0.6); opacity: 0; }
    #§mot { left: 120px; top: 600px; width: 840px; height: 420px; opacity: 0; }
    #§face { position: absolute; left: 80px; top: 620px; width: 920px; height: 600px; opacity: 0; }
    .§col { position: absolute; top: 0; width: 430px; height: 300px; border-radius: 28px; background: #151515; border: 2px solid #2e2e2e; }
    .§coll { position: absolute; left: 0; top: 40px; width: 100%; text-align: center; font: 600 32px ⟦FU⟧, sans-serif; color: ⟦MUTED⟧; letter-spacing: 0.1em; }
    .§colv { position: absolute; left: 0; top: 110px; width: 100%; text-align: center; font: 96px ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
    #§res { position: absolute; left: 0; top: 350px; width: 920px; text-align: center; font: 190px ⟦FT⟧, sans-serif; color: ⟦NUM⟧; opacity: 0; }
    .§minus { display: inline-block; width: 0.42em; height: 0.11em; margin-right: 0.12em; background: ⟦NUM⟧; vertical-align: 0.5em; border-radius: 0.05em; }
    """
    st = ('<div id="§mot" class="§photo"><img src="assets/img/ph-moteur22.jpg"></div>'
          '<div id="§ph" class="§burst">' + "".join(f'<img src="assets/img/{p}">' for p in ["ph-retro.jpg", "ph-jante.jpg", "ph-interieur22.jpg", "export.jpg"]) + '</div>'
          '<div id="§face"><div class="§col" style="left:0"><div class="§coll">DÉPENSÉ</div><div class="§colv">' + odo("dep", "66 800 €") + '</div></div>'
          '<div class="§col" style="left:490px"><div class="§coll">ENCAISSÉ</div><div class="§colv">' + odo("enc", "50 000 €") + '</div></div>'
          '<div id="§res"><i class="§minus"></i>' + odo("rv", "16 800 €") + '</div></div>')
    hud = (title("t6", ["50 000 €. EXPORT."], 380, 104) + total("51 800 €")
           + chip("c3", 330, 1060, "+15 000 €", "MÉCANIQUE"))
    js = TOT_JS + MEDIA_JS + """
      totInit("51 800");
      // the mechanics: 15 000 € into the TOTAL
      pre("mot", { opacity: 0, scale: 1.06 }); go("mot", { opacity: 1, scale: 1 }, 0.02, 0.4, "expo.out");
      bump("c3", at("15000") - 0.05, "66 800 €");
      // sold for export
      go("mot", { opacity: 0 }, at("finis") - 0.15, 0.2);
      var a0 = at("finis") - 0.1, a1 = at("50000") - 0.05, as = Math.max(0.22, (a1 - a0) / 3);
      pre("ph", { opacity: 0, scale: 1.06 }); go("ph", { opacity: 1, scale: 1 }, a0, 0.3, "expo.out");
      burst("ph", [a0, a0 + as, a0 + 2 * as, a1]);
      slam("t6-0", at("50000") - 0.05); stroke("t6", at("l'export"));
      // spent vs cashed in
      go("t6", { opacity: 0, y: -30 }, at("résultat") - 0.12, 0.14, "power2.in");
      go("ph", { opacity: 0, scale: 0.9 }, at("résultat") - 0.1, 0.3, "power2.in");
      pre("face", { opacity: 0, y: 60 }); go("face", { opacity: 1, y: 0 }, at("résultat"), 0.35, "back.out(1.4)");
      odo("dep", at("résultat") + 0.1, 0.7, { from: "00 000" }); odo("enc", at("résultat") + 0.25, 0.7, { from: "00 000" });
      pre("res", { opacity: 0, scale: 1.4 }); go("res", { opacity: 1, scale: 1 }, at("moins") - 0.06, 0.2, "expo.out");
      odo("rv", at("moins") - 0.06, 0.9, { from: "00 000" });
      shake("shk", at("16800") + 0.3, 10);
      cam(0, -10, 1.04, at("résultat"), 0.8);
    """
    sfx = [("pop", "15000", 1, -.05, .14), ("typing", "15000", 1, 1.0, .12), ("whoosh-short", "finis", 1, -.1, .14),
           ("pop", "50000", 1, -.05, .14), ("typing", "résultat", 1, .1, .12), ("impact-bass-1", "moins", 1, -.06, .3)]
    return css, st, hud, js, (540, 900), sfx


def scene_06():
    css = TOT_CSS + """
    .§err { position: absolute; left: 80px; width: 920px; height: 180px; border-radius: 28px; background: #151515; border: 2px solid #2e2e2e; opacity: 0; }
    .§errn { position: absolute; left: 28px; top: 50px; width: 80px; height: 80px; border-radius: 50%; background: ⟦CHIP_BG⟧; color: #0A0A0A;
      font: 56px/80px ⟦FT⟧, sans-serif; text-align: center; }
    .§errt { position: absolute; left: 136px; top: 0; width: 760px; height: 180px; display: flex; align-items: center;
      font: 50px/1.15 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
    .§k { color: ⟦TEXT⟧; }
    """
    lines = [("e1", 600, "ACHETÉE AVEC LE CŒUR, SANS MES CONTRÔLES."),
             ("e2", 810, "CONFIÉE À QUELQU’UN QUI N’EN ÉTAIT PAS CAPABLE."),
             ("e3", 1020, "J’AI VOULU GÉRER SEUL.")]
    st = "".join(f'<div id="§{i}" class="§err" style="top:{y}px"><div class="§errn">{k + 1}</div><div class="§errt"><div>{t}</div></div></div>'
                 for k, (i, y, t) in enumerate(lines))
    hud = title("t7", ["TROIS ERREURS"], 380, 116) + total("66 800 €")
    js = TOT_JS + """
      totInit("66 800");
      slam("t7-0", Math.max(0.02, at("trois") - 0.02)); stroke("t7", at("erreurs"));
      var cues = [at("acheté"), at("confié"), at("voulu")];
      ["e1", "e2", "e3"].forEach(function (e, k) {
        pre(e, { opacity: 0, x: -80 }); go(e, { opacity: 1, x: 0 }, cues[k] - 0.1, 0.35, "expo.out");
        if (k > 0) go(["e1", "e2"][k - 1], { opacity: 0.4 }, cues[k] - 0.1, 0.3);
      });
      init("e3", { opacity: 1 }); go("e1", { opacity: 1 }, at("seul") + 0.3, 0.4); go("e2", { opacity: 1 }, at("seul") + 0.3, 0.4);
      cam(0, -10, 1.04, at("confié"), 1.0);
    """
    sfx = [("pop", "trois", 1, 0, .14), ("whoosh-short", "acheté", 1, -.1, .14), ("whoosh-short", "confié", 1, -.1, .14),
           ("whoosh-short", "voulu", 1, -.1, .14), ("click-soft", "seul", 1, -.04, .22)]
    return css, st, hud, js, (540, 900), sfx


def scene_07():
    # the pivot: the car stands still, 49 000 € locked in it, a timeline that stretches over more than three years
    css = PHOTO_CSS + """
    #§ph { left: 90px; top: 540px; width: 900px; height: 340px; opacity: 0; }
    #§ph img { filter: saturate(0.35) brightness(0.75) contrast(1.05); }
    #§big { position: absolute; left: 0; top: 895px; width: 1080px; text-align: center; opacity: 0; }
    #§bigv { font: 132px/1.05 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
    #§bigl { font: 56px/1.1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; letter-spacing: 0.06em; }
    #§frise { position: absolute; left: 90px; top: 1140px; width: 900px; height: 70px; opacity: 0; }
    #§fbar { position: absolute; left: 0; top: 30px; width: 900px; height: 6px; background: ⟦LINE⟧; transform-origin: 0 50%; transform: scaleX(0); }
    .§tk { position: absolute; top: 18px; width: 3px; height: 30px; background: ⟦LINE⟧; opacity: 0; }
    .§tkl { position: absolute; top: 50px; width: 160px; margin-left: -80px; text-align: center; font: 600 26px ⟦FU⟧, sans-serif; color: ⟦MUTED⟧; letter-spacing: 0.08em; opacity: 0; }
    """
    ticks = "".join(f'<i class="§tk" id="§tk{k}" style="left:{x}px"></i><span class="§tkl" id="§tl{k}" style="left:{x}px">{lab}</span>'
                    for k, (x, lab) in enumerate([(0, "ACHAT"), (250, "1 AN"), (500, "2 ANS"), (750, "3 ANS")]))
    st = ('<div id="§ph" class="§photo"><img src="assets/img/cta.jpg"></div>'
          '<div id="§big"><div id="§bigv">' + odo("bv", "49 000 €") + '</div><div id="§bigl">BLOQUÉS</div></div>'
          f'<div id="§frise"><i id="§fbar"></i>{ticks}</div>')
    hud = title("t8", ["LE VRAI PROBLÈME."], 380, 110) + title("t8b", ["PAYÉ DE MA POCHE."], 380, 110)
    js = """
      slam("t8-0", at("problème") - 0.05); stroke("t8", at("ailleurs"));
      // my money, in a car that does not move
      pre("ph", { opacity: 0, scale: 1.05 }); go("ph", { opacity: 1, scale: 1 }, at("argent") - 0.1, 0.5, "expo.out");
      pre("big", { opacity: 0, y: 40 }); go("big", { opacity: 1, y: 0 }, at("49000") - 0.08, 0.3, "expo.out");
      odo("bv", at("49000") - 0.05, 0.8, { from: "00 000" });
      // the timeline stretches over more than three years
      pre("frise", { opacity: 0 }); go("frise", { opacity: 1 }, at("pendant") - 0.1, 0.2);
      var f0 = at("pendant") - 0.05, f1 = at("ans") + 0.4;
      tl.fromTo($("fbar"), { scaleX: 0 }, { scaleX: 1, duration: f1 - f0, ease: "none", immediateRender: false }, f0);
      [0, 1, 2, 3].forEach(function (k) {
        var t = f0 + (f1 - f0) * (k / 3.6);
        tl.fromTo($("tk" + k), { opacity: 0 }, { opacity: 1, duration: 0.12, immediateRender: false }, t);
        tl.fromTo($("tl" + k), { opacity: 0 }, { opacity: 1, duration: 0.12, immediateRender: false }, t);
      });
      // every mistake, paid by me
      go("t8", { opacity: 0, y: -30 }, at("chaque") - 0.12, 0.14, "power2.in");
      slam("t8b-0", at("payée") - 0.3); stroke("t8b", at("payée") + 0.1);
      go("ph", { opacity: 0.35 }, at("chaque"), 0.4);
      cam(0, -10, 1.04, at("49000"), 1.0);
    """
    sfx = [("pop", "problème", 1, -.05, .14), ("whoosh-short", "argent", 1, -.1, .12), ("impact-bass-2", "49000", 1, -.06, .26),
           ("typing", "pendant", 1, 0, .1), ("pop", "payée", 1, -.3, .14)]
    return css, st, hud, js, (540, 900), sfx


def scene_08():
    # two columns: buying to resell / selling without buying
    css = """
    .§cmp { position: absolute; top: 560px; width: 460px; height: 640px; border-radius: 24px; background: #121212; border: 2px solid #2e2e2e; opacity: 0; }
    .§cmp.§right { border-color: ⟦LINE⟧; }
    .§ch { position: absolute; left: 30px; top: 34px; width: 400px; font: 44px/1.1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
    .§cr { position: absolute; left: 30px; width: 400px; height: 3px; background: ⟦LINE⟧; top: 150px; }
    .§row { position: absolute; left: 30px; width: 400px; font: 38px/1.15 ⟦FU⟧, sans-serif; color: ⟦TEXT⟧; opacity: 0; }
    .§cv { position: absolute; left: 0; bottom: 34px; width: 100%; text-align: center; font: 68px/1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; opacity: 0; }
    """
    st = ('<div id="§L" class="§cmp" style="left:50px"><div class="§ch">ACHETER POUR REVENDRE</div><i class="§cr"></i>'
          '<div id="§l1" class="§row" style="top:190px">TON ARGENT DANS LA VOITURE</div>'
          '<div id="§l2" class="§row" style="top:330px">CHAQUE ERREUR À TES FRAIS</div>'
          '<div id="§lv" class="§cv">−16 800 €</div></div>'
          '<div id="§R" class="§cmp §right" style="left:570px"><div class="§ch">VENDRE SANS ACHETER</div><i class="§cr"></i>'
          '<div id="§r1" class="§row" style="top:190px">0 € DANS LA VOITURE</div>'
          '<div id="§r2" class="§row" style="top:330px">SI ÇA RATE, TU PERDS DU TEMPS</div>'
          '<div id="§rv" class="§cv">DU TEMPS</div></div>')
    hud = ""
    js = """
      pre("L", { opacity: 0, x: -60 }); go("L", { opacity: 1, x: 0 }, 0.02, 0.35, "expo.out");
      pre("l1", { opacity: 0 }); go("l1", { opacity: 1 }, 0.25, 0.25); pre("l2", { opacity: 0 }); go("l2", { opacity: 1 }, 0.5, 0.25);
      pre("R", { opacity: 0, x: 60 }); go("R", { opacity: 1, x: 0 }, at("sans") - 0.1, 0.35, "expo.out");
      pre("r1", { opacity: 0, y: 20 }); go("r1", { opacity: 1, y: 0 }, at("uneuro") - 0.1, 0.25);
      pre("r2", { opacity: 0, y: 20 }); go("r2", { opacity: 1, y: 0 }, at("temps") - 0.15, 0.25);
      go("L", { opacity: 0.45 }, at("temps") - 0.1, 0.4);
      pre("rv", { opacity: 0 }); go("rv", { opacity: 1 }, at("temps") + 0.1, 0.3);
      pre("lv", { opacity: 0, scale: 1.3 }); go("lv", { opacity: 1, scale: 1 }, at("pas") - 0.05, 0.2, "expo.out");
    """
    sfx = [("whoosh-short", None, 0, 0.02, .12), ("whoosh-short", "sans", 1, -.1, .12), ("pop", "uneuro", 1, -.1, .14),
           ("pop", "temps", 1, -.15, .14), ("impact-bass-1", "pas", 1, -.05, .22)]
    return css, st, hud, js, (540, 900), sfx


def scene_09():
    # the signature: the real photo (background cut out) on black, name and role in cream, bronze rule
    css = """
    #§me { position: absolute; left: 70px; top: 700px; width: 940px; height: 1180px; opacity: 0; }
    #§me img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: contain; object-position: 50% 100%; filter: saturate(0.8) contrast(1.03); }
    #§id { position: absolute; left: 0; top: 380px; width: 1080px; text-align: center; opacity: 0; }
    #§nm { font: 104px/1.05 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; }
    #§rl { width: 520px; height: 4px; margin: 26px auto 22px; background: ⟦LINE⟧; transform-origin: 50% 50%; }
    #§ro { font: 46px/1.15 ⟦FU⟧, sans-serif; color: ⟦TEXT⟧; letter-spacing: 0.04em; }
    """
    st = '<div id="§me"><img src="assets/img/guillaume-forge.png"></div>'
    hud = (title("t9", ["VENDRE DES VOITURES", "SANS LES ACHETER."], 380, 96)
           + '<div id="§id"><div id="§nm">GUILLAUME HERBIN</div><div id="§rl"></div><div id="§ro">FONDATEUR DU PROGRAMME FORGE</div></div>')
    js = """
      slam("t9-0", at("métier") - 0.1); slam("t9-1", at("forge") - 0.2); stroke("t9", at("forge"));
      go("t9", { opacity: 0, y: -30 }, at("moi") - 0.12, 0.14, "power2.in");
      pre("me", { opacity: 0, y: 60 }); go("me", { opacity: 1, y: 0 }, at("moi") - 0.1, 0.5, "expo.out");
      pre("id", { opacity: 0 }); go("id", { opacity: 1 }, at("guillaumeherbin") - 0.1, 0.25);
      tl.fromTo($("rl"), { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power3.out", immediateRender: false }, at("guillaumeherbin") + 0.2);
      tl.fromTo($("ro"), { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, at("fondateur") - 0.1);
    """
    sfx = [("pop", "métier", 1, -.1, .12), ("whoosh-short", "moi", 1, -.1, .12), ("pop", "guillaumeherbin", 1, -.1, .12)]
    return css, st, hud, js, (540, 700), sfx


def scene_10():
    # end card: FORGE logo, « ABONNE-TOI » in cream, the kit line smaller
    shutil.copy(charte.logo_path("logo_dark"), "assets/img/charte-logo.svg")
    css = """
    #§logo { position: absolute; left: 240px; top: 520px; width: 600px; opacity: 0; }
    #§sub { position: absolute; left: 0; top: 860px; width: 1080px; text-align: center; font: 120px/1 ⟦FT⟧, sans-serif; color: ⟦TEXT⟧; opacity: 0; }
    #§srl { position: absolute; left: 340px; top: 1010px; width: 400px; height: 4px; background: ⟦LINE⟧; transform-origin: 50% 50%; transform: scaleX(0); }
    #§kit { position: absolute; left: 0; top: 1050px; width: 1080px; text-align: center; font: 44px/1.2 ⟦FU⟧, sans-serif; color: ⟦TEXT⟧; letter-spacing: 0.04em; opacity: 0; }
    """
    st = ""
    hud = ('<img id="§logo" src="assets/img/charte-logo.svg">'
           '<div id="§sub">ABONNE-TOI</div><i id="§srl"></i><div id="§kit">' + charte.C["end_line"].rstrip(".") + '</div>')
    js = """
      pre("logo", { opacity: 0, y: 30 }); go("logo", { opacity: 1, y: 0 }, 0.05, 0.5, "expo.out");
      pre("kit", { opacity: 0 }); go("kit", { opacity: 1 }, at("métiers") - 0.1, 0.4);
      slam("sub", at("abonne-toi") - 0.05, { s: 1.3 });
      tl.fromTo($("srl"), { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power3.out", immediateRender: false }, at("abonne-toi") + 0.15);
    """
    sfx = [("whoosh-cinematic", None, 0, 0.02, .2), ("pop", "abonne-toi", 1, -.05, .16)]
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
