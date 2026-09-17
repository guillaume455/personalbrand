#!/usr/bin/env python3
"""
Génère des sous-titres ASS incrustables, phrase par phrase, sans modèle ASR.

Principe : ffmpeg `silencedetect` repère les pauses réelles de la parole dans la
fenêtre du clip. Le texte (corrigé à la main) est découpé en unités de sous-titre,
puis réparti sur les segments de parole proportionnellement à sa longueur, les
silences étant sautés. La coupure tombe donc sur les respirations, pas au hasard.

Usage:
  build_subs.py --src RUSH.mp4 --start 4.2 --end 38.0 \
                --text texte.txt --out subs.ass [--noise -30dB] [--min-sil 0.28]
"""
import argparse
import os
import re
import subprocess
import sys

# Repris de scripts/lib.sh — gardés synchronisés à la main.
FONT = os.environ.get("SUB_FONT", "DejaVu Sans")
FONTSIZE = int(os.environ.get("SUB_FONTSIZE", 62))
OUTLINE = int(os.environ.get("SUB_OUTLINE", 3))
SHADOW = int(os.environ.get("SUB_SHADOW", 0))
MARGIN_V = int(os.environ.get("SUB_MARGIN_V", 300))
MAX_CHARS = int(os.environ.get("SUB_MAX_CHARS", 42))
OUT_W = int(os.environ.get("OUT_W", 1080))
OUT_H = int(os.environ.get("OUT_H", 1920))

MIN_CUE = 0.85   # durée plancher d'un sous-titre, en secondes
MAX_CUE = 4.5    # durée plafond


def speech_segments(src, start, end, noise, min_sil):
    """Retourne les intervalles de parole (relatifs au début du clip)."""
    dur = end - start
    cmd = [
        "ffmpeg", "-hide_banner", "-nostats",
        "-ss", f"{start}", "-t", f"{dur}", "-i", src,
        "-map", "0:a:0",
        "-af", f"silencedetect=noise={noise}:d={min_sil}",
        "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    log = proc.stderr

    silences = []
    cur = None
    for m in re.finditer(r"silence_(start|end):\s*(-?[\d.]+)", log):
        kind, val = m.group(1), float(m.group(2))
        if kind == "start":
            cur = val
        elif cur is not None:
            silences.append((max(0.0, cur), min(dur, val)))
            cur = None
    if cur is not None:
        silences.append((max(0.0, cur), dur))

    # Complément des silences = parole.
    segs, pos = [], 0.0
    for s0, s1 in sorted(silences):
        if s0 > pos:
            segs.append((pos, min(s0, dur)))
        pos = max(pos, s1)
    if pos < dur:
        segs.append((pos, dur))

    segs = [(a, b) for a, b in segs if b - a > 0.12]
    return segs if segs else [(0.0, dur)]


def split_text(text):
    """Découpe le texte en unités de sous-titre lisibles."""
    text = " ".join(text.split())
    # Coupe après . ! ? … et aussi sur , ; : quand la phrase est longue.
    parts = re.split(r"(?<=[.!?…])\s+", text)
    units = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if len(p) <= MAX_CHARS * 2:
            units.append(p)
            continue
        # Phrase longue : on la recoupe sur la ponctuation faible, sinon sur les mots.
        chunks = re.split(r"(?<=[,;:])\s+", p)
        buf = ""
        for c in chunks:
            if not buf:
                buf = c
            elif len(buf) + 1 + len(c) <= MAX_CHARS * 2:
                buf += " " + c
            else:
                units.append(buf)
                buf = c
        if buf:
            units.append(buf)

    # Dernier filet : rien ne dépasse 2 lignes pleines.
    final = []
    for u in units:
        final.extend(split_balanced(u, MAX_CHARS * 2))

    # Un fragment de deux mots seul à l'écran se lit mal et, en fin de clip,
    # n'a même plus de parole pour durer. On le rattache au précédent.
    fusion = []
    for u in final:
        if fusion and len(u) < 12 and len(fusion[-1]) + 1 + len(u) <= MAX_CHARS * 2:
            fusion[-1] += " " + u
        else:
            fusion.append(u)
    return fusion


def split_balanced(u, limit):
    """Découpe en parts de longueurs voisines plutôt qu'en remplissant chaque
    ligne au maximum : une coupe gloutonne laisse le reliquat en fin d'unité,
    d'où les sous-titres d'un seul mot."""
    if len(u) <= limit:
        return [u]
    n = -(-len(u) // limit)
    cible = len(u) / n
    parts, buf = [], ""
    for mot in u.split():
        essai = f"{buf} {mot}".strip()
        if buf and (len(essai) > limit
                    or (len(buf) >= cible and len(parts) < n - 1)):
            parts.append(buf)
            buf = mot
        else:
            buf = essai
    if buf:
        parts.append(buf)
    return parts


def wrap(s):
    """Retour à la ligne ASS (\\N) pour tenir en 2 lignes centrées."""
    if len(s) <= MAX_CHARS:
        return s
    cut = s.rfind(" ", 0, MAX_CHARS)
    if cut <= 0:
        return s
    return s[:cut] + "\\N" + s[cut + 1:]


def allocate(units, segs):
    """Répartit les unités sur les segments de parole, au prorata des caractères."""
    total_speech = sum(b - a for a, b in segs)
    total_chars = sum(max(1, len(u)) for u in units)
    per_char = total_speech / total_chars if total_chars else 0.0

    cues, si = [], 0
    cursor = segs[0][0]
    for u in units:
        want = max(MIN_CUE, min(MAX_CUE, len(u) * per_char))
        start = cursor
        remaining = want
        end = cursor
        # Consomme la durée demandée en traversant les segments de parole.
        while remaining > 0 and si < len(segs):
            seg_a, seg_b = segs[si]
            if cursor < seg_a:
                cursor = seg_a
                if not cues and start < seg_a:
                    start = seg_a
            avail = seg_b - cursor
            if avail <= 0:
                si += 1
                if si < len(segs):
                    cursor = segs[si][0]
                continue
            take = min(avail, remaining)
            cursor += take
            remaining -= take
            end = cursor
            if remaining > 0:
                si += 1
                if si < len(segs):
                    cursor = segs[si][0]
        if end <= start:
            end = start + MIN_CUE
        cues.append((start, end, u))
    return cues


def ts(t):
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--start", type=float, required=True)
    ap.add_argument("--end", type=float, required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--noise", default="-30dB")
    ap.add_argument("--min-sil", type=float, default=0.28)
    ap.add_argument("--offset", type=float, default=0.0,
                    help="décalage global des sous-titres, en secondes")
    a = ap.parse_args()

    with open(a.text, encoding="utf-8") as f:
        text = f.read()

    segs = speech_segments(a.src, a.start, a.end, a.noise, a.min_sil)
    units = split_text(text)
    if not units:
        sys.exit("Texte de sous-titres vide.")
    cues = allocate(units, segs)

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {OUT_W}
PlayResY: {OUT_H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Clip,{FONT},{FONTSIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,{OUTLINE},{SHADOW},2,80,80,{MARGIN_V},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for st, en, txt in cues:
        st += a.offset
        en += a.offset
        lines.append(
            f"Dialogue: 0,{ts(st)},{ts(en)},Clip,,0,0,0,,{wrap(txt)}\n"
        )

    with open(a.out, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"{len(cues)} sous-titres -> {a.out}")
    print(f"segments de parole détectés : {len(segs)}")
    for st, en, txt in cues:
        print(f"  {ts(st)} -> {ts(en)}  {txt[:58]}")


if __name__ == "__main__":
    main()
