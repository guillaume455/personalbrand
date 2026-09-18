"""Étape 1 — la liste officielle des établissements, depuis le stock Sirene open data.

Le stock mensuel (data.gouv.fr, Licence Ouverte) est la seule source exhaustive
qui porte la date de création. Il ne contient aucun email : c'est le squelette
que les étapes suivantes viennent enrichir.
"""
from __future__ import annotations

import csv
import io
import sqlite3
import sys
import zipfile
from pathlib import Path
from typing import Iterator

from . import config, net, store

csv.field_size_limit(1 << 24)

# Colonnes du fichier StockEtablissement. Plusieurs alias par champ : le schéma
# INSEE bouge (ajout de activitePrincipaleNAF25Etablissement en déc. 2025), on
# ne veut pas casser sur un renommage.
ETAB_COLS = {
    "siret": ("siret",),
    "siren": ("siren",),
    "naf": ("activitePrincipaleEtablissement",),
    "naf25": ("activitePrincipaleNAF25Etablissement",),
    "date_creation": ("dateCreationEtablissement",),
    "etat": ("etatAdministratifEtablissement",),
    "statut_diffusion": ("statutDiffusionEtablissement",),
    "est_siege": ("etablissementSiege",),
    "tranche_effectif": ("trancheEffectifsEtablissement",),
    "enseigne": ("enseigne1Etablissement", "denominationUsuelleEtablissement"),
    "code_postal": ("codePostalEtablissement",),
    "commune": ("libelleCommuneEtablissement",),
    "num_voie": ("numeroVoieEtablissement",),
    "type_voie": ("typeVoieEtablissement",),
    "libelle_voie": ("libelleVoieEtablissement",),
    "complement": ("complementAdresseEtablissement",),
}
UL_COLS = {
    "siren": ("siren",),
    "denomination": ("denominationUniteLegale",),
    "nom": ("nomUniteLegale",),
    "prenom": ("prenom1UniteLegale", "prenomUsuelUniteLegale"),
    "categorie_juridique": ("categorieJuridiqueUniteLegale",),
    "statut_diffusion": ("statutDiffusionUniteLegale",),
}


def _pick(row: dict, aliases: tuple[str, ...]) -> str:
    for name in aliases:
        value = row.get(name)
        if value:
            return value.strip()
    return ""


def resolve_stock_urls() -> dict[str, str]:
    """Trouve les URL des fichiers stock du mois via l'API data.gouv.fr."""
    sess = net.session()
    url = config.DATAGOUV_API.format(slug=config.DATAGOUV_DATASET)
    resp = sess.get(url, timeout=60)
    resp.raise_for_status()
    found: dict[str, str] = {}
    for res in resp.json().get("resources", []):
        title = (res.get("title") or "") + " " + (res.get("url") or "")
        if config.STOCK_ETABLISSEMENT_HINT in title and "etablissement" not in found:
            if "Historique" not in title:
                found["etablissement"] = res["url"]
        if config.STOCK_UNITE_LEGALE_HINT in title and "unite_legale" not in found:
            if "Historique" not in title:
                found["unite_legale"] = res["url"]
    missing = {"etablissement", "unite_legale"} - set(found)
    if missing:
        raise RuntimeError(
            "Fichiers stock introuvables sur data.gouv.fr ({}). "
            "Passe les URL à la main avec --url-etablissement / --url-unite-legale "
            "(page du jeu de données : https://www.data.gouv.fr/datasets/{})".format(
                ", ".join(sorted(missing)), config.DATAGOUV_DATASET
            )
        )
    return found


def _open_csv(zip_path: Path) -> tuple[zipfile.ZipFile, csv.DictReader]:
    """Ouvre le CSV contenu dans le zip en flux (pas d'extraction sur disque)."""
    zf = zipfile.ZipFile(zip_path)
    names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
    if not names:
        raise RuntimeError(f"aucun CSV dans {zip_path}")
    stream = io.TextIOWrapper(zf.open(names[0]), encoding="utf-8", newline="")
    return zf, csv.DictReader(stream)


def inspect_header(zip_path: Path) -> list[str]:
    zf, reader = _open_csv(zip_path)
    try:
        return list(reader.fieldnames or [])
    finally:
        zf.close()


def _adresse(row: dict) -> str:
    parts = [
        _pick(row, ETAB_COLS["num_voie"]),
        _pick(row, ETAB_COLS["type_voie"]),
        _pick(row, ETAB_COLS["libelle_voie"]),
    ]
    base = " ".join(p for p in parts if p)
    comp = _pick(row, ETAB_COLS["complement"])
    return f"{base} {comp}".strip() if comp else base


def filtrer_etablissements(zip_path: Path, naf_codes: set[str], date_min: str,
                           date_max: str, *, inclure_fermes: bool = False,
                           progress_every: int = 2_000_000) -> Iterator[dict]:
    """Balaie les ~40 M de lignes du stock et ne garde que la cible."""
    zf, reader = _open_csv(zip_path)
    fields = set(reader.fieldnames or [])
    if "siret" not in fields:
        raise RuntimeError(
            "En-tête inattendu dans {} (colonnes : {}...). Lance "
            "`python -m prospect inspect-header` et compare avec prospect/sirene.py".format(
                zip_path.name, ", ".join(sorted(fields)[:6])
            )
        )
    has_naf25 = any(c in fields for c in ETAB_COLS["naf25"])
    seen = kept = 0
    try:
        for row in reader:
            seen += 1
            if progress_every and seen % progress_every == 0:
                print(f"  {seen/1e6:.0f} M lignes lues, {kept} retenues", end="\r", flush=True)
            naf = _pick(row, ETAB_COLS["naf"]).replace(".", "").upper()
            if naf not in naf_codes:
                continue
            date_creation = _pick(row, ETAB_COLS["date_creation"])
            if not date_creation or not (date_min <= date_creation <= date_max):
                continue
            if not inclure_fermes and _pick(row, ETAB_COLS["etat"]) != "A":
                continue
            # RGPD : on n'exploite jamais les établissements non diffusibles.
            if _pick(row, ETAB_COLS["statut_diffusion"]) not in ("O", ""):
                continue
            cp = _pick(row, ETAB_COLS["code_postal"])
            kept += 1
            yield {
                "siret": _pick(row, ETAB_COLS["siret"]),
                "siren": _pick(row, ETAB_COLS["siren"]),
                "raison_sociale": None,
                "enseigne": _pick(row, ETAB_COLS["enseigne"]) or None,
                "naf": naf,
                "naf25": (_pick(row, ETAB_COLS["naf25"]) or None) if has_naf25 else None,
                "naf_libelle": libelle_naf(naf),
                "date_creation": date_creation,
                "etat": _pick(row, ETAB_COLS["etat"]),
                "statut_diffusion": _pick(row, ETAB_COLS["statut_diffusion"]),
                "est_siege": 1 if _pick(row, ETAB_COLS["est_siege"]).lower() == "true" else 0,
                "tranche_effectif": _pick(row, ETAB_COLS["tranche_effectif"]) or None,
                "categorie_juridique": None,
                "adresse": _adresse(row) or None,
                "code_postal": cp or None,
                "commune": _pick(row, ETAB_COLS["commune"]) or None,
                "departement": departement(cp),
                "personne_physique": 0,
            }
        print(f"  {seen} lignes lues, {kept} retenues" + " " * 20)
    finally:
        zf.close()


def enrichir_unites_legales(zip_path: Path, conn: sqlite3.Connection,
                            progress_every: int = 2_000_000) -> int:
    """Deuxième passe : le nom de l'entreprise vit dans StockUniteLegale."""
    sirens = {r[0] for r in conn.execute("SELECT DISTINCT siren FROM etablissements")}
    if not sirens:
        print("  aucun établissement en base : lance d'abord l'étape `sirene`.")
        return 0
    zf, reader = _open_csv(zip_path)
    updates: list[tuple] = []
    seen = matched = 0
    try:
        for row in reader:
            seen += 1
            if progress_every and seen % progress_every == 0:
                print(f"  {seen/1e6:.0f} M unités légales lues, {matched} appariées",
                      end="\r", flush=True)
            siren = _pick(row, UL_COLS["siren"])
            if siren not in sirens:
                continue
            denom = _pick(row, UL_COLS["denomination"])
            nom = _pick(row, UL_COLS["nom"])
            prenom = _pick(row, UL_COLS["prenom"])
            personne_physique = 0
            if not denom and (nom or prenom):
                denom = " ".join(p for p in (prenom, nom) if p)
                personne_physique = 1
            diffusion_ul = _pick(row, UL_COLS["statut_diffusion"])
            matched += 1
            updates.append((
                denom or None,
                _pick(row, UL_COLS["categorie_juridique"]) or None,
                personne_physique,
                diffusion_ul,
                siren,
            ))
            if len(updates) >= 5000:
                _flush_ul(conn, updates)
        _flush_ul(conn, updates)
        print(f"  {seen} unités légales lues, {matched} appariées" + " " * 20)
    finally:
        zf.close()
    # Les unités légales non diffusibles sont retirées, même si l'établissement l'était.
    removed = conn.execute(
        "DELETE FROM etablissements WHERE statut_diffusion NOT IN ('O','')"
    ).rowcount
    conn.commit()
    if removed:
        print(f"  {removed} établissements retirés (unité légale non diffusible)")
    return matched


def _flush_ul(conn: sqlite3.Connection, updates: list[tuple]) -> None:
    if not updates:
        return
    conn.executemany(
        "UPDATE etablissements SET raison_sociale = ?, categorie_juridique = ?, "
        "personne_physique = ?, statut_diffusion = CASE WHEN ? IN ('O','') "
        "THEN statut_diffusion ELSE ? END WHERE siren = ?",
        [(d, c, p, s, s, siren) for d, c, p, s, siren in updates],
    )
    conn.commit()
    updates.clear()


def libelle_naf(code: str) -> str | None:
    for group in config.NAF_GROUPS.values():
        if code in group:
            return group[code]
    return config.NAF25_MARCHAND.get(code)


def departement(code_postal: str | None) -> str | None:
    if not code_postal or len(code_postal) < 2:
        return None
    if code_postal.startswith("97") or code_postal.startswith("98"):
        return code_postal[:3]
    return code_postal[:2]


def codes_naf(groupes: tuple[str, ...]) -> set[str]:
    codes: set[str] = set()
    for nom in groupes:
        if nom not in config.NAF_GROUPS:
            raise SystemExit(
                f"groupe NAF inconnu : {nom} (dispo : {', '.join(config.NAF_GROUPS)})"
            )
        codes |= set(config.NAF_GROUPS[nom])
    return codes


def run(conn: sqlite3.Connection, *, groupes: tuple[str, ...], date_min: str,
        date_max: str, url_etab: str | None = None, url_ul: str | None = None,
        garder_zips: bool = True, inclure_fermes: bool = False) -> int:
    codes = codes_naf(groupes)
    print(f"Codes NAF ciblés : {', '.join(sorted(codes))}")
    print(f"Créations du {date_min} au {date_max}")
    if not (url_etab and url_ul):
        print("Résolution des fichiers stock sur data.gouv.fr...")
        urls = resolve_stock_urls()
        url_etab = url_etab or urls["etablissement"]
        url_ul = url_ul or urls["unite_legale"]
    config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    etab_zip = config.CACHE_DIR / "StockEtablissement.zip"
    ul_zip = config.CACHE_DIR / "StockUniteLegale.zip"

    print(f"Téléchargement du stock établissements ({url_etab})")
    net.download(url_etab, etab_zip)
    print("Filtrage (quelques minutes : ~40 M de lignes)...")
    n = store.upsert_many(
        conn, "etablissements",
        filtrer_etablissements(etab_zip, codes, date_min, date_max,
                               inclure_fermes=inclure_fermes),
    )
    print(f"{n} établissements retenus.")

    print(f"Téléchargement du stock unités légales ({url_ul})")
    net.download(url_ul, ul_zip)
    print("Récupération des raisons sociales...")
    enrichir_unites_legales(ul_zip, conn)

    store.set_meta(conn, "sirene_date_min", date_min)
    store.set_meta(conn, "sirene_date_max", date_max)
    store.set_meta(conn, "sirene_groupes", ",".join(groupes))
    if not garder_zips:
        for p in (etab_zip, ul_zip):
            p.unlink(missing_ok=True)
    total = store.count(conn, "etablissements")
    print(f"Base : {total} établissements.")
    return total
