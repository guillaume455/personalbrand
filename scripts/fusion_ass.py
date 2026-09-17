#!/usr/bin/env python3
"""Concatène des .ass produits segment par segment, chacun décalé de son
point d'entrée dans le montage.

    fusion_ass.py sortie.ass  a.ass 0  b.ass 5.15  c.ass 23.0

Générer les sous-titres par segment plutôt que sur le clip entier borne la
dérive : build_subs.py répartit le texte au prorata des caractères, et sur
une prise débitée sans pause le décalage s'accumule — jusqu'à 2,5 s en fin
de clip sur la première version.
"""
import sys
from pathlib import Path


def s2f(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def f2s(t):
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int((t % 3600) // 60):02d}:{t % 60:05.2f}"


def main(sortie, paires):
    entete, lignes = [], []
    for i in range(0, len(paires), 2):
        src = Path(paires[i]).read_text(encoding="utf-8").splitlines()
        offset = float(paires[i + 1])
        if not entete:                       # en-tête et styles du premier fichier
            entete = [l for l in src if not l.startswith("Dialogue")]
        for l in src:
            if not l.startswith("Dialogue"):
                continue
            p = l.split(",", 9)
            p[1] = f2s(s2f(p[1]) + offset)
            p[2] = f2s(s2f(p[2]) + offset)
            lignes.append(",".join(p))
    Path(sortie).write_text("\n".join(entete + lignes) + "\n", encoding="utf-8")
    print(f"{len(lignes)} sous-titres -> {sortie}")


main(sys.argv[1], sys.argv[2:])
