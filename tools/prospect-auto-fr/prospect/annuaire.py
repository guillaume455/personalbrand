"""Scraper générique d'annuaires et de listings — tu décris la cible, il moissonne.

Aucun site n'est codé en dur : une cible = un fichier JSON décrivant les pages
de liste, le lien vers la fiche et les sélecteurs CSS des champs. Tout passe par
la couche réseau polie du projet (un hit toutes les N secondes par domaine).

    python -m prospect annuaire --config sources/mon-annuaire.json
    python -m prospect annuaire-match

Avant de pointer une cible : lis ses conditions d'utilisation et LEGAL.md. Le
risque juridique en France n'est pas le scraping en soi, c'est l'extraction
d'une partie substantielle d'une base protégée et sa réutilisation dans un
service concurrent (arrêt LeBonCoin, CA Paris 18/02/2021).
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from . import extract, match, net, store

GABARIT = {
    "nom": "exemple-annuaire",
    "pages": ["https://exemple.fr/annuaire/garages?page={page}"],
    "pagination": {"debut": 1, "fin": 10, "pas": 1},
    "cartes": None,
    "lien_fiche": "a.fiche-link",
    "selecteurs": {
        "nom": "h1.titre",
        "commune": ".adresse .ville",
        "code_postal": ".adresse .cp",
        "telephone": "a[href^='tel:']",
        "site_web": "a.site-web",
        "email": "a[href^='mailto:']",
    },
    "delai": 3.0,
    "respecter_robots": True,
    "max_fiches": 2000,
}


def charger_config(chemin: Path) -> dict:
    cfg = json.loads(Path(chemin).read_text(encoding="utf-8"))
    for obligatoire in ("nom", "pages"):
        if obligatoire not in cfg:
            raise SystemExit(f"config incomplète : champ « {obligatoire} » manquant")
    cfg.setdefault("selecteurs", {})
    cfg.setdefault("delai", 3.0)
    cfg.setdefault("respecter_robots", True)
    cfg.setdefault("max_fiches", 2000)
    cfg.setdefault("pagination", {"debut": 1, "fin": 1, "pas": 1})
    return cfg


def urls_de_liste(cfg: dict) -> list[str]:
    pagination = cfg["pagination"]
    urls = []
    for gabarit in cfg["pages"]:
        if "{page}" not in gabarit:
            urls.append(gabarit)
            continue
        for n in range(pagination.get("debut", 1), pagination.get("fin", 1) + 1,
                       pagination.get("pas", 1)):
            urls.append(gabarit.format(page=n))
    return urls


def _valeur(noeud, selecteur: str | None) -> str | None:
    """Texte ou href (mailto/tel/site) du premier élément qui matche."""
    if not selecteur or noeud is None:
        return None
    cible = noeud.select_one(selecteur)
    if cible is None:
        return None
    href = (cible.get("href") or "").strip() if cible.name == "a" else ""
    if href.lower().startswith("mailto:"):
        return href[7:].split("?")[0]
    if href.lower().startswith("tel:"):
        return href[4:]
    if href and not href.startswith(("#", "javascript:")):
        return href
    return cible.get_text(" ", strip=True) or None


def extraire_fiche(html_source: str, url: str, cfg: dict, noeud=None) -> dict | None:
    """Une fiche = un pro. Les sélecteurs d'abord, l'extraction générique en secours."""
    sel = cfg["selecteurs"]
    racine = noeud if noeud is not None else BeautifulSoup(html_source, "html.parser")
    nom = _valeur(racine, sel.get("nom"))
    email = _valeur(racine, sel.get("email"))
    tel = _valeur(racine, sel.get("telephone"))
    site = _valeur(racine, sel.get("site_web"))
    fragment = str(racine) if noeud is not None else html_source
    if not email:
        emails = extract.extraire(fragment, url)
        email = next(iter(emails), None)
    if not tel:
        tels = extract.extraire_telephones(fragment)
        tel = next(iter(tels), None)
    if email:
        email = extract.nettoyer(email)
    if tel:
        tel = extract.normaliser_tel(tel)
    if site:
        site = urljoin(url, site)
        hote = urlparse(site).netloc.lower()
        if hote and hote in url:
            site = None  # lien interne à l'annuaire, pas le site du pro
    if not (nom and (email or tel or site)):
        return None
    return {
        "cle": f"{cfg['nom']}|{nom.lower()}|{_valeur(racine, sel.get('code_postal')) or ''}",
        "source": cfg["nom"],
        "nom": nom,
        "commune": _valeur(racine, sel.get("commune")),
        "code_postal": _valeur(racine, sel.get("code_postal")),
        "telephone": tel,
        "site_web": site,
        "email": email,
        "url_source": url,
        "vu_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def run(conn: sqlite3.Connection, chemin_config: Path) -> int:
    cfg = charger_config(chemin_config)
    sess = net.session()
    robots = cfg["respecter_robots"]
    if not robots:
        print("! robots.txt ignoré pour cette source (choix de la config).")
    fiches: list[dict] = []
    liste = urls_de_liste(cfg)
    print(f"Source « {cfg['nom']} » : {len(liste)} pages de liste, "
          f"{cfg['delai']} s entre deux requêtes.")
    for i, url_liste in enumerate(liste, 1):
        resp = net.get(url_liste, sess, check_robots=robots, delay=cfg["delai"])
        if resp is None or resp.status_code >= 400:
            code = "bloqué/erreur" if resp is None else resp.status_code
            print(f"  page {i}/{len(liste)} : {code} — on continue")
            continue
        soup = BeautifulSoup(resp.text, "html.parser")

        if cfg.get("cartes"):  # tout est dans la page de liste
            for carte in soup.select(cfg["cartes"]):
                fiche = extraire_fiche("", resp.url, cfg, noeud=carte)
                if fiche:
                    fiches.append(fiche)
        elif cfg.get("lien_fiche"):
            liens = []
            for a in soup.select(cfg["lien_fiche"]):
                href = a.get("href")
                if href:
                    liens.append(urljoin(resp.url, href))
            for lien in dict.fromkeys(liens):
                if len(fiches) >= cfg["max_fiches"]:
                    break
                page = net.get(lien, sess, check_robots=robots, delay=cfg["delai"])
                if page is None or page.status_code >= 400:
                    continue
                fiche = extraire_fiche(page.text, page.url, cfg)
                if fiche:
                    fiches.append(fiche)
        else:
            fiche = extraire_fiche(resp.text, resp.url, cfg)
            if fiche:
                fiches.append(fiche)

        if len(fiches) >= 200:
            store.upsert_many(conn, "annuaire_fiches", fiches)
            fiches = []
        print(f"  page {i}/{len(liste)}, {store.count(conn, 'annuaire_fiches')} fiches",
              end="\r", flush=True)
        if store.count(conn, "annuaire_fiches") >= cfg["max_fiches"]:
            print("\n  plafond max_fiches atteint, arrêt propre.")
            break
    store.upsert_many(conn, "annuaire_fiches", fiches)
    total = store.count(conn, "annuaire_fiches", f"source = '{cfg['nom']}'")
    print(f"Source « {cfg['nom']} » : {total} fiches en base." + " " * 15)
    return total


def apparier(conn: sqlite3.Connection) -> int:
    """Rattache les fiches d'annuaire aux SIRET, et en tire sites/emails/téléphones."""
    index = match.index_etablissements(conn)
    maintenant = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sites, emails, tels = [], [], []
    apparies = 0
    for fiche in store.iter_rows(conn, "SELECT * FROM annuaire_fiches"):
        siret, methode = match.trouver_siret(index, fiche["nom"], fiche["code_postal"],
                                             fiche["commune"])
        if not siret:
            continue
        apparies += 1
        origine = f"annuaire:{fiche['source']}:{methode}"
        if fiche["site_web"]:
            sites.append({"siret": siret, "url": fiche["site_web"],
                          "domaine": match._domaine(fiche["site_web"]),
                          "source": origine, "confiance": 4, "statut": "retenu",
                          "verifie_le": maintenant})
        if fiche["email"]:
            emails.append({"siret": siret, "email": fiche["email"], "source": origine,
                           "url_source": fiche["url_source"], "type_email": None,
                           "mx_ok": None, "score": 0, "trouve_le": maintenant})
        if fiche["telephone"]:
            tels.append({"siret": siret, "telephone": fiche["telephone"],
                         "source": origine, "url_source": fiche["url_source"],
                         "trouve_le": maintenant})
    store.upsert_many(conn, "sites", sites)
    store.upsert_many(conn, "emails", emails)
    store.upsert_many(conn, "telephones", tels)
    print(f"Annuaires : {apparies} fiches rattachées à un SIRET "
          f"({len(sites)} sites, {len(emails)} emails, {len(tels)} téléphones).")
    return apparies


def ecrire_gabarit(chemin: Path) -> Path:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(GABARIT, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    return chemin
