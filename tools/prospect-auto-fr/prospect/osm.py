"""Étape 2 — OpenStreetMap (Overpass) : la seule source gratuite qui donne
directement des emails et des sites web de pros de l'auto, sans clé API.

Données sous licence ODbL : réutilisables, à condition de citer OpenStreetMap
et de garder la trace de la provenance (colonne `source` de l'export).
"""
from __future__ import annotations

import json
import sqlite3
import time

from . import config, net, store

# Découpage en boîtes pour ne pas faire tomber Overpass en timeout.
BOITES = {
    "nord-ouest": (47.0, -5.3, 51.3, 1.0),
    "nord-est": (47.0, 1.0, 51.3, 8.3),
    "centre-ouest": (44.0, -2.5, 47.0, 1.0),
    "centre-est": (44.0, 1.0, 47.0, 7.8),
    "sud-ouest": (41.3, -2.5, 44.0, 1.5),
    "sud-est": (41.3, 1.5, 44.0, 9.7),
    "corse": (41.2, 8.4, 43.1, 9.7),
    "guadeloupe": (15.8, -61.9, 16.6, -60.9),
    "martinique": (14.3, -61.3, 14.9, -60.7),
    "guyane": (2.0, -54.7, 5.9, -51.5),
    "reunion": (-21.5, 55.1, -20.8, 55.9),
    "mayotte": (-13.1, 44.9, -12.6, 45.4),
}


def requete(bbox: tuple[float, float, float, float]) -> str:
    s, w, n, e = bbox
    clauses = []
    for filtre in config.OSM_FILTERS:
        clauses.append(f"  node{filtre}({s},{w},{n},{e});")
        clauses.append(f"  way{filtre}({s},{w},{n},{e});")
    corps = "\n".join(clauses)
    return f"[out:json][timeout:300];\n(\n{corps}\n);\nout center tags;"


def _tag(tags: dict, *noms: str) -> str | None:
    for nom in noms:
        val = tags.get(nom)
        if val:
            return val.strip()
    return None


def parser_reponse(payload: dict) -> list[dict]:
    lignes = []
    for el in payload.get("elements", []):
        tags = el.get("tags") or {}
        email = _tag(tags, "contact:email", "email")
        site = _tag(tags, "contact:website", "website", "url")
        if not (email or site):
            continue  # un POI sans contact ni site ne sert à rien ici
        centre = el.get("center") or {}
        lignes.append({
            "osm_key": f"{el.get('type')}/{el.get('id')}",
            "nom": _tag(tags, "name", "operator", "brand"),
            "commune": _tag(tags, "addr:city"),
            "code_postal": _tag(tags, "addr:postcode"),
            "site_web": site,
            "email": email.lower() if email else None,
            "telephone": _tag(tags, "contact:phone", "phone"),
            "siret_ref": _tag(tags, "ref:FR:SIRET", "ref:FR:SIREN"),
            "shop": _tag(tags, "shop", "amenity"),
            "lat": el.get("lat") or centre.get("lat"),
            "lon": el.get("lon") or centre.get("lon"),
        })
    return lignes


def run(conn: sqlite3.Connection, *, boites: tuple[str, ...] | None = None) -> int:
    sess = net.session()
    cibles = boites or tuple(BOITES)
    total = 0
    for nom in cibles:
        if nom not in BOITES:
            raise SystemExit(f"zone inconnue : {nom} (dispo : {', '.join(BOITES)})")
        query = requete(BOITES[nom])
        payload = None
        for endpoint in config.OVERPASS_ENDPOINTS:
            for essai in range(3):
                try:
                    net.throttle(endpoint, 5.0)
                    resp = sess.post(endpoint, data={"data": query}, timeout=360)
                    if resp.status_code == 200:
                        payload = resp.json()
                        break
                    print(f"  {nom} : {endpoint} a répondu {resp.status_code}")
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    print(f"  {nom} : {type(exc).__name__} sur {endpoint}")
                time.sleep(5 * (essai + 1))
            if payload is not None:
                break
        if payload is None:
            print(f"  {nom} : abandon (Overpass indisponible), on continue")
            continue
        lignes = parser_reponse(payload)
        store.upsert_many(conn, "osm_pois", lignes)
        total += len(lignes)
        avec_email = sum(1 for l in lignes if l["email"])
        print(f"  {nom} : {len(lignes)} POI avec contact ({avec_email} emails directs)")
    print(f"OSM : {store.count(conn, 'osm_pois')} POI en base, "
          f"{store.count(conn, 'osm_pois', 'email IS NOT NULL')} avec email.")
    return total
