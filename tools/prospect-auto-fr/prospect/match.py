"""Étape 3 — appariement Sirene <-> OSM.

Trois passes, de la plus sûre à la plus permissive :
  1. le tag ref:FR:SIRET de l'objet OSM,
  2. nom normalisé + code postal,
  3. nom normalisé + commune normalisée.
"""
from __future__ import annotations

import re
import sqlite3
import unicodedata

from . import store

FORMES_JURIDIQUES = {
    "sarl", "sas", "sasu", "eurl", "sa", "sci", "snc", "scop", "selarl", "sc",
    "ets", "etablissements", "ste", "societe", "sarlu", "eirl", "ei", "scm",
    "groupe", "group", "co", "cie", "compagnie", "entreprise", "holding",
}


def normaliser(texte: str | None) -> str:
    if not texte:
        return ""
    sans_accents = "".join(
        c for c in unicodedata.normalize("NFKD", texte) if not unicodedata.combining(c)
    )
    mots = [m for m in re.split(r"[^a-z0-9]+", sans_accents.lower()) if m]
    gardes = [m for m in mots if m not in FORMES_JURIDIQUES]
    # « S.A.S. AUTO-PRESTIGE » -> ['s','a','s','auto','prestige'] : les lettres
    # isolées viennent des sigles ponctués et faussent l'appariement.
    substantiels = [m for m in gardes if len(m) > 1]
    if len(substantiels) >= 2:
        gardes = substantiels
    return " ".join(gardes) or " ".join(mots)


def cles(nom: str | None, code_postal: str | None, commune: str | None) -> list[str]:
    base = normaliser(nom)
    if not base:
        return []
    out = []
    if code_postal:
        out.append(f"cp:{base}|{code_postal.strip()}")
    if commune:
        out.append(f"co:{base}|{normaliser(commune)}")
    return out


def run(conn: sqlite3.Connection) -> int:
    """Crée les sites candidats et les emails issus d'OSM. Renvoie le nb d'appariements."""
    index: dict[str, str] = {}
    for row in store.iter_rows(conn, "SELECT siret, raison_sociale, enseigne, "
                                     "code_postal, commune FROM etablissements"):
        for nom in (row["enseigne"], row["raison_sociale"]):
            for cle in cles(nom, row["code_postal"], row["commune"]):
                index.setdefault(cle, row["siret"])

    sirets = {r[0] for r in conn.execute("SELECT siret FROM etablissements")}
    sites, emails = [], []
    apparies = 0
    for poi in store.iter_rows(conn, "SELECT * FROM osm_pois"):
        siret = None
        source = None
        ref = (poi["siret_ref"] or "").replace(" ", "")
        if len(ref) == 14 and ref in sirets:
            siret, source = ref, "osm:ref_siret"
        else:
            for cle in cles(poi["nom"], poi["code_postal"], poi["commune"]):
                if cle in index:
                    siret = index[cle]
                    source = "osm:nom_cp" if cle.startswith("cp:") else "osm:nom_commune"
                    break
        if not siret:
            continue
        apparies += 1
        if poi["site_web"]:
            sites.append({
                "siret": siret, "url": poi["site_web"],
                "domaine": _domaine(poi["site_web"]), "source": source,
                "confiance": 5 if source == "osm:ref_siret" else 4,
                "statut": None, "verifie_le": None,
            })
        if poi["email"]:
            emails.append({
                "siret": siret, "email": poi["email"].lower(),
                "source": source, "url_source": f"https://www.openstreetmap.org/{poi['osm_key']}",
                "type_email": None, "mx_ok": None, "score": 0, "trouve_le": None,
            })
    store.upsert_many(conn, "sites", sites)
    store.upsert_many(conn, "emails", emails)
    print(f"Appariement : {apparies} POI OSM rattachés à un SIRET "
          f"({len(sites)} sites, {len(emails)} emails directs).")
    return apparies


def _domaine(url: str) -> str | None:
    from urllib.parse import urlparse
    if not url:
        return None
    if "://" not in url:
        url = "http://" + url
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host or None
