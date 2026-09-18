"""Étape 7 — exports CSV prêts à l'emploi, avec la provenance de chaque email."""
from __future__ import annotations

import csv
import sqlite3
from datetime import date

from . import config, store

COLONNES = [
    "siret", "siren", "raison_sociale", "enseigne", "naf", "activite",
    "date_creation", "adresse", "code_postal", "commune", "departement",
    "site_web", "email", "type_email", "score", "mx_ok", "telephone",
    "source_email", "url_source", "personne_physique",
]

SQL_BASE = """
SELECT e.siret, e.siren, e.raison_sociale, e.enseigne, e.naf,
       e.naf_libelle AS activite, e.date_creation, e.adresse, e.code_postal,
       e.commune, e.departement, e.personne_physique,
       (SELECT url FROM sites s WHERE s.siret = e.siret
          ORDER BY s.confiance DESC LIMIT 1) AS site_web,
       (SELECT telephone FROM telephones t WHERE t.siret = e.siret
          LIMIT 1) AS telephone,
       m.email, m.type_email, m.score, m.mx_ok, m.source AS source_email, m.url_source
FROM etablissements e
JOIN emails m ON m.siret = e.siret
"""


def _ecrire(chemin, lignes) -> int:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    # utf-8-sig : Excel FR ouvre le fichier sans casser les accents.
    with open(chemin, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLONNES, delimiter=";",
                                extrasaction="ignore")
        writer.writeheader()
        for ligne in lignes:
            writer.writerow({c: ligne[c] for c in COLONNES})
            n += 1
    return n


def run(conn: sqlite3.Connection, *, prefixe: str | None = None,
        mx_obligatoire: bool = True) -> dict[str, int]:
    suffixe = prefixe or date.today().isoformat()
    dossier = config.EXPORT_DIR
    filtre_mx = "AND m.mx_ok = 1" if mx_obligatoire else ""
    resultats = {}

    pro = dossier / f"contacts_pro_{suffixe}.csv"
    resultats[pro.name] = _ecrire(pro, store.iter_rows(
        conn, SQL_BASE + f"WHERE m.type_email IN ('pro_role','pro_nominatif') {filtre_mx} "
                         "ORDER BY m.score DESC, e.date_creation DESC"))

    perso = dossier / f"contacts_perso_prudence_{suffixe}.csv"
    resultats[perso.name] = _ecrire(perso, store.iter_rows(
        conn, SQL_BASE + f"WHERE m.type_email = 'perso' {filtre_mx} "
                         "ORDER BY e.date_creation DESC"))

    sans = dossier / f"sans_email_{suffixe}.csv"
    resultats[sans.name] = _ecrire(sans, store.iter_rows(conn, """
        SELECT e.*, (SELECT url FROM sites s WHERE s.siret = e.siret
                       ORDER BY s.confiance DESC LIMIT 1) AS site_web,
               (SELECT telephone FROM telephones t WHERE t.siret = e.siret
                  LIMIT 1) AS telephone,
               NULL AS email, NULL AS type_email, NULL AS score, NULL AS mx_ok,
               NULL AS source_email, NULL AS url_source, e.naf_libelle AS activite
        FROM etablissements e
        WHERE e.siret NOT IN (SELECT siret FROM emails)
        ORDER BY e.date_creation DESC"""))

    print("Exports écrits :")
    for nom, n in resultats.items():
        print(f"  {dossier / nom}  ({n} lignes)")
    print("\nRappel : citer les sources — Sirene/INSEE (Licence Ouverte) et "
          "OpenStreetMap (ODbL) — et conserver la colonne url_source, c'est elle "
          "qui justifie la provenance en cas de demande RGPD.")
    return resultats


def stats(conn: sqlite3.Connection) -> None:
    etabs = store.count(conn, "etablissements")
    sites = conn.execute("SELECT COUNT(DISTINCT siret) FROM sites "
                         "WHERE statut = 'retenu' OR confiance >= ?",
                         (config.MIN_SITE_CONFIDENCE,)).fetchone()[0]
    avec_email = conn.execute("SELECT COUNT(DISTINCT siret) FROM emails").fetchone()[0]
    print(f"Établissements ciblés           : {etabs}")
    print(f"  dont site web identifié       : {sites}"
          f" ({sites/max(etabs,1)*100:.1f} %)")
    print(f"  dont au moins un email        : {avec_email}"
          f" ({avec_email/max(etabs,1)*100:.1f} %)")
    avec_tel = conn.execute("SELECT COUNT(DISTINCT siret) FROM telephones").fetchone()[0]
    print(f"  dont au moins un téléphone    : {avec_tel}"
          f" ({avec_tel/max(etabs,1)*100:.1f} %)")
    print(f"POI OpenStreetMap appariés      : {store.count(conn, 'osm_pois')}")
    print(f"Fiches d'annuaires scrapées     : {store.count(conn, 'annuaire_fiches')}")
    print(f"Emails en base                  : {store.count(conn, 'emails')}")
    print(f"Téléphones en base              : {store.count(conn, 'telephones')}")
    for r in conn.execute("SELECT type_email, COUNT(*) n FROM emails "
                          "GROUP BY type_email ORDER BY n DESC"):
        print(f"  {r['type_email'] or 'non classé':16s}            : {r['n']}")
    for r in conn.execute("SELECT source, COUNT(*) n FROM emails "
                          "GROUP BY source ORDER BY n DESC"):
        print(f"  source {r['source']:24s} : {r['n']}")
    periode = (store.get_meta(conn, "sirene_date_min"), store.get_meta(conn, "sirene_date_max"))
    if periode[0]:
        print(f"Période de création retenue     : {periode[0]} → {periode[1]}")
