"""Étape 4 — trouver le site web de chaque établissement, sans moteur payant.

Deux leviers gratuits :
  1. déduction de domaine depuis la raison sociale / l'enseigne, vérifiée par DNS
     puis par le contenu de la page (le nom, la ville ou le SIREN doivent y être) ;
  2. en option, une instance SearXNG (--searx) pour les cas non déduits.
"""
from __future__ import annotations

import concurrent.futures as futures
import re
import sqlite3
import unicodedata
from datetime import datetime, timezone

import dns.exception
import dns.resolver
from bs4 import BeautifulSoup

from . import config, net, store
from .match import FORMES_JURIDIQUES, normaliser

TLDS = (".fr", ".com")
# Mots de liaison : « garage dupré et fils » s'écrit aussi bien garagedupre-fils.fr
MOTS_LIAISON = {"et", "and", "de", "du", "des", "la", "le", "les", "d", "l", "aux", "au"}
MOTS_GENERIQUES = config.MOTS_GENERIQUES_AUTO
SIGNES_PARKING = (
    "ce domaine est à vendre", "this domain is for sale", "domain for sale",
    "parked domain", "sedoparking", "afterhostingpage", "site en construction",
    "bienvenue sur votre nouveau site", "default web page", "index of /",
)
_DNS = dns.resolver.Resolver()
_DNS.lifetime = 5.0
_DNS.timeout = 5.0


def _slug(texte: str) -> str:
    sans = "".join(c for c in unicodedata.normalize("NFKD", texte)
                   if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", sans.lower()).strip()


def candidats_domaines(noms: list[str], max_candidats: int = 8) -> list[str]:
    """Génère les domaines plausibles pour une entreprise."""
    bases: list[str] = []
    for nom in noms:
        if not nom:
            continue
        mots = [m for m in _slug(nom).split() if m and m not in FORMES_JURIDIQUES]
        if not mots:
            continue
        sans_liaison = [m for m in mots if m not in MOTS_LIAISON] or mots
        significatifs = [m for m in sans_liaison if m not in MOTS_GENERIQUES] or sans_liaison
        variantes = []
        for jeu in (mots, sans_liaison, [m for m in sans_liaison if not m.isdigit()],
                    significatifs):
            if jeu:
                variantes += ["".join(jeu), "-".join(jeu)]
        for v in variantes:
            v = v.strip("-")
            if 3 <= len(v) <= 40 and not v.isdigit() and v not in bases:
                bases.append(v)
    out = []
    for base in bases:
        for tld in TLDS:
            domaine = base + tld
            if domaine not in out:
                out.append(domaine)
    return out[:max_candidats]


def domaine_existe(domaine: str) -> bool:
    for enregistrement in ("A", "MX"):
        try:
            if _DNS.resolve(domaine, enregistrement):
                return True
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
                dns.resolver.NoNameservers, dns.exception.Timeout):
            continue
        except dns.exception.DNSException:
            continue
    return False


def score_page(html_source: str, etab: sqlite3.Row) -> int:
    """Le domaine trouvé appartient-il vraiment à cette entreprise ?"""
    soup = BeautifulSoup(html_source, "html.parser")
    texte = normaliser(soup.get_text(" ", strip=True))
    brut = re.sub(r"\D", "", html_source)
    score = 0
    if any(signe in texte for signe in (normaliser(s) for s in SIGNES_PARKING)):
        return -10
    for nom in (etab["raison_sociale"], etab["enseigne"]):
        cible = normaliser(nom)
        if cible and len(cible) > 4 and cible in texte:
            score += 2
            break
    if etab["commune"] and normaliser(etab["commune"]) in texte:
        score += 2
    if etab["code_postal"] and etab["code_postal"] in html_source:
        score += 1
    if etab["siren"] and etab["siren"] in brut:
        score += 3
    return score


def _tester_domaine(domaine: str, etab: sqlite3.Row, sess) -> tuple[str, int, str] | None:
    if not domaine_existe(domaine):
        return None
    for prefixe in ("https://www.", "https://", "http://www.", "http://"):
        url = prefixe + domaine
        resp = net.get(url, sess, delay=1.0)
        if resp is None or resp.status_code >= 400 or not resp.text:
            continue
        return (resp.url, score_page(resp.text, etab), "devine")
    return None


def _resoudre_un(etab: sqlite3.Row, sess, searx: str | None,
                 depuis_index: list[tuple[str, int]] | None = None) -> list[dict]:
    noms = [etab["enseigne"], etab["raison_sociale"]]
    resultats = []
    # Les domaines issus de l'index existent pour de vrai : on les teste d'abord.
    for domaine, indice in (depuis_index or []):
        essai = _tester_domaine(domaine, etab, sess)
        if essai:
            url, score, _ = essai
            resultats.append({"url": url, "confiance": score + (1 if indice >= 6 else 0),
                              "source": "index"})
            if resultats[-1]["confiance"] >= config.MIN_SITE_CONFIDENCE:
                return resultats
    for domaine in candidats_domaines([n for n in noms if n]):
        essai = _tester_domaine(domaine, etab, sess)
        if essai:
            url, score, source = essai
            resultats.append({"url": url, "confiance": score, "source": source})
            if score >= config.MIN_SITE_CONFIDENCE:
                return resultats
    if searx and not any(r["confiance"] >= config.MIN_SITE_CONFIDENCE for r in resultats):
        for url in _searx(searx, noms, etab["commune"], sess):
            resp = net.get(url, sess, delay=1.0)
            if resp is None or resp.status_code >= 400:
                continue
            resultats.append({"url": resp.url, "confiance": score_page(resp.text, etab),
                              "source": "searx"})
            if resultats[-1]["confiance"] >= config.MIN_SITE_CONFIDENCE:
                break
    return resultats


def _searx(instance: str, noms: list[str], commune: str | None, sess) -> list[str]:
    """Recherche via une instance SearXNG (JSON). Beaucoup limitent le débit : sois poli."""
    requete = " ".join(filter(None, [next((n for n in noms if n), ""), commune or ""]))
    if not requete.strip():
        return []
    try:
        net.throttle(instance, 4.0)
        resp = sess.get(instance.rstrip("/") + "/search",
                        params={"q": requete, "format": "json", "language": "fr"},
                        timeout=config.HTTP_TIMEOUT)
        if resp.status_code != 200:
            return []
        données = resp.json()
    except Exception:
        return []
    urls = []
    for res in données.get("results", [])[:5]:
        url = res.get("url")
        if url and not any(x in url for x in ("facebook.", "pagesjaunes.", "linkedin.",
                                              "societe.com", "pappers.", "leboncoin.",
                                              "lacentrale.", "verif.com", "annuaire")):
            urls.append(url)
    return urls


def run(conn: sqlite3.Connection, *, limite: int | None = None, workers: int | None = None,
        searx: str | None = None, refaire: bool = False) -> int:
    """Cherche un site pour les établissements qui n'en ont pas encore."""
    filtre = "" if refaire else (
        " WHERE e.siret NOT IN (SELECT siret FROM sites)"
    )
    sql = f"SELECT e.* FROM etablissements e{filtre} ORDER BY e.date_creation DESC"
    if limite:
        sql += f" LIMIT {int(limite)}"
    etabs = list(store.iter_rows(conn, sql))
    if not etabs:
        print("Rien à résoudre (utilise --refaire pour tout reprendre).")
        return 0
    # L'index de domaines (AFNIC / Common Crawl) est interrogé dans le thread
    # principal : une connexion SQLite ne se partage pas entre threads.
    from . import domaines as _domaines
    index_candidats: dict[str, list[tuple[str, int]]] = {}
    if _domaines.index_disponible(conn):
        print(f"Index de domaines : {store.count(conn, 'domaines')} domaines connus, "
              "interrogation locale avant toute requête réseau...")
        for etab in etabs:
            index_candidats[etab["siret"]] = _domaines.candidats(
                conn, [etab["enseigne"], etab["raison_sociale"]], etab["commune"])
        avec = sum(1 for v in index_candidats.values() if v)
        print(f"  {avec}/{len(etabs)} établissements ont au moins un domaine candidat.")
    else:
        print("Pas d'index de domaines (`python -m prospect domaines --fichier ...`) : "
              "on se rabat sur la déduction + DNS, moins efficace.")
    print(f"Résolution de site web pour {len(etabs)} établissements "
          f"({workers or config.CRAWL_WORKERS} threads)...")
    sess = net.session()
    maintenant = datetime.now(timezone.utc).isoformat(timespec="seconds")
    trouves = 0
    lignes: list[dict] = []
    with futures.ThreadPoolExecutor(max_workers=workers or config.CRAWL_WORKERS) as pool:
        taches = {pool.submit(_resoudre_un, e, sess, searx,
                              index_candidats.get(e["siret"])): e for e in etabs}
        for i, tache in enumerate(futures.as_completed(taches), 1):
            etab = taches[tache]
            try:
                resultats = tache.result()
            except Exception as exc:  # un site cassé ne doit jamais tuer le run
                print(f"  {etab['siret']} : {type(exc).__name__}")
                resultats = []
            retenu = False
            for res in resultats:
                lignes.append({
                    "siret": etab["siret"], "url": res["url"],
                    "domaine": _domaine(res["url"]), "source": res["source"],
                    "confiance": res["confiance"],
                    "statut": "retenu" if res["confiance"] >= config.MIN_SITE_CONFIDENCE
                              else "doute",
                    "verifie_le": maintenant,
                })
                retenu = retenu or res["confiance"] >= config.MIN_SITE_CONFIDENCE
            trouves += 1 if retenu else 0
            if len(lignes) >= 200:
                store.upsert_many(conn, "sites", lignes)
                lignes = []
            if i % 50 == 0:
                print(f"  {i}/{len(etabs)} traités, {trouves} sites retenus",
                      end="\r", flush=True)
    store.upsert_many(conn, "sites", lignes)
    print(f"Sites retenus : {trouves}/{len(etabs)} "
          f"({trouves/max(len(etabs),1)*100:.1f} %)" + " " * 20)
    return trouves


def _domaine(url: str) -> str | None:
    from urllib.parse import urlparse
    host = urlparse(url).netloc.lower()
    return host.removeprefix("www.") or None
