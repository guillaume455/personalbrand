"""Index local de tous les domaines existants — le levier décisif de l'étape 4.

Deviner « garage-dupre.fr » puis tester en DNS coûte des milliers de requêtes
pour un taux de succès médiocre. Ici on fait l'inverse : on charge la liste
réelle des domaines déposés et on y cherche l'entreprise. Deux sources, les
deux gratuites et réutilisables :

  * AFNIC open data — la liste exhaustive des ~4 M de domaines .fr (recommandé).
    https://opendata.afnic.fr/  /  https://www.data.gouv.fr/datasets/open-data-du-fr-1
  * Common Crawl host graph — tous TLD, plus gros, moins précis.
    https://commoncrawl.org/web-graphs

Le format des fichiers change à chaque publication : le parseur détecte seul
ce qu'il lit (CSV AFNIC, texte brut, .gz, ou hosts inversés Common Crawl).
"""
from __future__ import annotations

import csv
import gzip
import io
import re
import sqlite3
import zipfile
from pathlib import Path
from typing import Iterator

from . import store
from .match import normaliser
from .resolve import MOTS_GENERIQUES

DOMAINE_RE = re.compile(r"^[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?(?:\.[a-z0-9\-]{2,63})+$")
TLDS_CONNUS = {"fr", "com", "net", "org", "eu", "re", "pm", "yt", "wf", "tf",
               "gp", "mq", "gf", "nc", "auto", "paris", "bzh", "alsace", "corsica"}
# Suffixes à deux niveaux : chez eux le domaine utile a trois labels.
SUFFIXES_DOUBLES = {"gouv.fr", "asso.fr", "com.fr", "tm.fr", "nom.fr", "prd.fr",
                    "presse.fr", "avoues.fr", "avocat.fr", "notaires.fr",
                    "veterinaire.fr", "pharmacien.fr", "chirurgiens-dentistes.fr",
                    "medecin.fr", "experts-comptables.fr", "greta.fr", "port.fr",
                    "aeroport.fr", "co.uk", "com.br"}


def _ouvrir(path: Path):
    """Ouvre un .zip, .gz ou fichier texte et renvoie un flux de lignes."""
    nom = path.name.lower()
    if nom.endswith(".zip"):
        zf = zipfile.ZipFile(path)
        interne = next((n for n in zf.namelist()
                        if n.lower().endswith((".csv", ".txt", ".tsv"))), None)
        if interne is None:
            raise RuntimeError(f"aucun csv/txt dans {path.name}")
        return io.TextIOWrapper(zf.open(interne), encoding="utf-8", errors="replace")
    if nom.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, "r", encoding="utf-8", errors="replace")


def _depuis_host_inverse(valeur: str) -> str | None:
    """« fr.exemple.www » (Common Crawl) -> « exemple.fr »."""
    labels = valeur.split(".")
    if len(labels) < 2 or labels[0] not in TLDS_CONNUS:
        return None
    if len(labels) >= 3 and f"{labels[1]}.{labels[0]}" in SUFFIXES_DOUBLES:
        return f"{labels[2]}.{labels[1]}.{labels[0]}"
    return f"{labels[1]}.{labels[0]}"


def domaine_enregistrable(valeur: str) -> str | None:
    """Ramène n'importe quelle écriture d'hôte au domaine de second niveau."""
    valeur = valeur.strip().strip('"').lower()
    if not valeur or " " in valeur:
        return None
    valeur = valeur.removeprefix("http://").removeprefix("https://").split("/")[0]
    valeur = valeur.split("@")[-1].removeprefix("www.").rstrip(".")
    if not DOMAINE_RE.match(valeur):
        return None
    labels = valeur.split(".")
    # Common Crawl écrit les hôtes à l'envers : on le détecte au premier label.
    if labels[0] in TLDS_CONNUS and labels[-1] not in TLDS_CONNUS:
        return _depuis_host_inverse(valeur)
    deux = ".".join(labels[-2:])
    if deux in SUFFIXES_DOUBLES and len(labels) >= 3:
        return ".".join(labels[-3:])
    return deux


def iter_domaines(path: Path, tlds: tuple[str, ...] = ("fr",)) -> Iterator[str]:
    """Extrait les domaines de n'importe lequel des formats supportés."""
    flux = _ouvrir(path)
    suffixes = tuple("." + t.lstrip(".") for t in tlds)
    vus: set[str] = set()
    try:
        premiere = flux.readline()
        delimiteur = ";" if premiere.count(";") > premiere.count("\t") else "\t"
        colonne = None
        entetes = [c.strip().strip('"').lower() for c in premiere.split(delimiteur)]
        if len(entetes) > 1 and not any(domaine_enregistrable(e) for e in entetes):
            # ligne d'en-tête : on repère la colonne qui porte le nom de domaine
            for i, entete in enumerate(entetes):
                if "domaine" in entete or "domain" in entete or entete == "host":
                    colonne = i
                    break
            if colonne is None:
                colonne = 0
        else:
            flux = io.StringIO(premiere + flux.read())  # pas d'en-tête : tout relire
        lecteur = csv.reader(flux, delimiter=delimiteur)
        for ligne in lecteur:
            if not ligne:
                continue
            brut = ligne[colonne] if colonne is not None and len(ligne) > colonne else ligne[0]
            # Common Crawl : « 12345<TAB>fr.exemple.www »
            if colonne is None and len(ligne) == 2 and ligne[0].strip().isdigit():
                brut = ligne[1]
            domaine = domaine_enregistrable(brut)
            if domaine and domaine.endswith(suffixes) and domaine not in vus:
                vus.add(domaine)
                yield domaine
    finally:
        if hasattr(flux, "close"):
            flux.close()


def _tokens_domaine(sld: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9]+", sld) if len(t) > 1]


def construire(conn: sqlite3.Connection, path: Path,
               tlds: tuple[str, ...] = ("fr",)) -> int:
    """Charge le fichier dans les tables `domaines` et `domaine_token`."""
    lots_domaines, lots_tokens = [], []
    total = 0
    for domaine in iter_domaines(path, tlds):
        sld = domaine.split(".")[0]
        lots_domaines.append({"domaine": domaine, "sld": sld,
                              "cle_plate": sld.replace("-", "")})
        for token in _tokens_domaine(sld):
            lots_tokens.append({"token": token, "domaine": domaine})
        total += 1
        if len(lots_domaines) >= 20000:
            store.upsert_many(conn, "domaines", lots_domaines)
            store.upsert_many(conn, "domaine_token", lots_tokens)
            lots_domaines, lots_tokens = [], []
            print(f"  {total} domaines indexés", end="\r", flush=True)
    store.upsert_many(conn, "domaines", lots_domaines)
    store.upsert_many(conn, "domaine_token", lots_tokens)
    store.set_meta(conn, "index_domaines_source", path.name)
    store.set_meta(conn, "index_domaines_total", str(total))
    print(f"  {total} domaines indexés depuis {path.name}" + " " * 20)
    return total


def index_disponible(conn: sqlite3.Connection) -> bool:
    return store.count(conn, "domaines") > 0


def candidats(conn: sqlite3.Connection, noms: list[str], commune: str | None = None,
              max_candidats: int = 6, max_postings: int = 300) -> list[tuple[str, int]]:
    """Cherche les domaines plausibles pour une entreprise. [(domaine, indice)]."""
    resultats: dict[str, int] = {}
    for nom in [n for n in noms if n]:
        tokens = [t for t in normaliser(nom).split() if len(t) > 1]
        if not tokens:
            continue
        distinctifs = [t for t in tokens if t not in MOTS_GENERIQUES] or tokens

        # 1. correspondance exacte du jeu de tokens (insensible aux tirets)
        for jeu in (tokens, distinctifs, [t for t in tokens if not t.isdigit()]):
            if not jeu:
                continue
            plate = "".join(jeu)
            for (domaine,) in conn.execute(
                    "SELECT domaine FROM domaines WHERE cle_plate = ?", (plate,)):
                resultats[domaine] = max(resultats.get(domaine, 0), 6)

        # 2. correspondance par token distinctif, si le token est assez rare
        for token in distinctifs:
            nb = conn.execute("SELECT COUNT(*) FROM domaine_token WHERE token = ?",
                              (token,)).fetchone()[0]
            if not nb or nb > max_postings:
                continue
            for (domaine,) in conn.execute(
                    "SELECT domaine FROM domaine_token WHERE token = ? LIMIT ?",
                    (token, max_postings)):
                if domaine in resultats:
                    continue
                tokens_dom = set(_tokens_domaine(domaine.split(".")[0]))
                communs = tokens_dom & set(tokens)
                if not communs:
                    continue
                indice = 2 + len(communs)
                if commune and normaliser(commune).replace(" ", "") in domaine:
                    indice += 2
                if tokens_dom & set(MOTS_GENERIQUES):
                    indice += 1  # « ...-automobiles.fr » : bon signe métier
                resultats[domaine] = max(resultats.get(domaine, 0), indice)

    return sorted(resultats.items(), key=lambda kv: -kv[1])[:max_candidats]
