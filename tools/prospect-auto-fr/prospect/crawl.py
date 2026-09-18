"""Étape 5 — visiter les sites retenus et y récupérer les emails.

Respecte robots.txt, un seul hit toutes les 2 s par domaine, 6 pages max par site :
on cible la page d'accueil puis les pages contact / mentions légales, qui portent
l'email dans la grande majorité des cas.
"""
from __future__ import annotations

import concurrent.futures as futures
import sqlite3
from datetime import datetime, timezone

from . import config, extract, net, store


def crawler_site(url_racine: str, sess) -> tuple[dict[str, tuple[str, str]],
                                                 dict[str, tuple[str, str]], list[dict]]:
    """Renvoie ({email: (méthode, url)}, {téléphone: (méthode, url)}, journal)."""
    vus: dict[str, tuple[str, str]] = {}
    tels: dict[str, tuple[str, str]] = {}
    journal: list[dict] = []
    maintenant = datetime.now(timezone.utc).isoformat(timespec="seconds")
    a_visiter = [url_racine]
    visites: set[str] = set()
    while a_visiter and len(visites) < config.MAX_PAGES_PER_SITE:
        url = a_visiter.pop(0)
        if url in visites:
            continue
        visites.add(url)
        resp = net.get(url, sess)
        if resp is None:
            journal.append({"url": url, "statut": "bloque_ou_erreur", "vue_le": maintenant})
            continue
        journal.append({"url": url, "statut": str(resp.status_code), "vue_le": maintenant})
        if resp.status_code >= 400 or "html" not in resp.headers.get("Content-Type", ""):
            continue
        html_source = resp.text
        for email, methode in extract.extraire(html_source, resp.url).items():
            vus.setdefault(email, (methode, resp.url))
        for tel, methode in extract.extraire_telephones(html_source).items():
            tels.setdefault(tel, (methode, resp.url))
        if len(visites) == 1:  # on ne suit les liens que depuis la racine
            for lien in extract.liens_contact(html_source, resp.url,
                                              config.MAX_PAGES_PER_SITE - 1):
                if lien not in visites:
                    a_visiter.append(lien)
    return vus, tels, journal


def run(conn: sqlite3.Connection, *, limite: int | None = None,
        workers: int | None = None, confiance_min: int | None = None,
        refaire: bool = False) -> int:
    seuil = config.MIN_SITE_CONFIDENCE if confiance_min is None else confiance_min
    sql = (
        "SELECT s.siret, s.url, s.domaine, MAX(s.confiance) AS conf FROM sites s "
        "WHERE s.confiance >= ? "
        + ("" if refaire else "AND s.siret NOT IN (SELECT siret FROM emails) ")
        + "GROUP BY s.siret ORDER BY conf DESC"
    )
    if limite:
        sql += f" LIMIT {int(limite)}"
    cibles = list(store.iter_rows(conn, sql, (seuil,)))
    if not cibles:
        print("Aucun site à crawler (lance `resolve` d'abord, ou --refaire).")
        return 0
    print(f"Crawl de {len(cibles)} sites ({workers or config.CRAWL_WORKERS} threads, "
          f"robots.txt {'respecté' if config.RESPECT_ROBOTS else 'ignoré'})...")
    sess = net.session()
    maintenant = datetime.now(timezone.utc).isoformat(timespec="seconds")
    emails: list[dict] = []
    telephones: list[dict] = []
    pages: list[dict] = []
    sites_avec_email = 0
    with futures.ThreadPoolExecutor(max_workers=workers or config.CRAWL_WORKERS) as pool:
        taches = {pool.submit(crawler_site, c["url"], sess): c for c in cibles}
        for i, tache in enumerate(futures.as_completed(taches), 1):
            cible = taches[tache]
            try:
                trouves, tels_trouves, journal = tache.result()
            except Exception as exc:
                print(f"  {cible['domaine']} : {type(exc).__name__}")
                continue
            pages += journal
            if trouves:
                sites_avec_email += 1
            for tel, (methode, url_source) in tels_trouves.items():
                telephones.append({
                    "siret": cible["siret"], "telephone": tel,
                    "source": f"site:{methode}", "url_source": url_source,
                    "trouve_le": maintenant,
                })
            for email, (methode, url_source) in trouves.items():
                emails.append({
                    "siret": cible["siret"], "email": email,
                    "source": f"site:{methode}", "url_source": url_source,
                    "type_email": None, "mx_ok": None, "score": 0,
                    "trouve_le": maintenant,
                })
            if len(emails) >= 200 or len(pages) >= 500:
                store.upsert_many(conn, "emails", emails)
                store.upsert_many(conn, "telephones", telephones)
                store.upsert_many(conn, "pages_vues", pages)
                emails, telephones, pages = [], [], []
            if i % 25 == 0:
                print(f"  {i}/{len(cibles)} sites, {sites_avec_email} avec email",
                      end="\r", flush=True)
    store.upsert_many(conn, "emails", emails)
    store.upsert_many(conn, "telephones", telephones)
    store.upsert_many(conn, "pages_vues", pages)
    total = store.count(conn, "emails")
    print(f"Crawl terminé : {sites_avec_email}/{len(cibles)} sites ont livré un email. "
          f"{total} emails et {store.count(conn, 'telephones')} téléphones en base."
          + " " * 10)
    return sites_avec_email
