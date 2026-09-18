"""Étape 6 — qualifier et valider les emails.

Gratuit : syntaxe, enregistrement MX du domaine, classement pro/rôle/perso,
dédoublonnage. Pas de test SMTP : envoyer des RCPT TO depuis une IP résidentielle
grille la réputation pour rien — un vérifieur payant le fait mieux, plus tard.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

import dns.exception
import dns.resolver

from . import config, store

_DNS = dns.resolver.Resolver()
_DNS.lifetime = 5.0
_DNS.timeout = 5.0
_CACHE_MX: dict[str, bool] = {}


def mx_ok(domaine: str) -> bool:
    if domaine in _CACHE_MX:
        return _CACHE_MX[domaine]
    resultat = False
    try:
        resultat = bool(_DNS.resolve(domaine, "MX"))
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers, dns.exception.Timeout):
        try:  # certains petits hébergeurs servent le mail sur l'A record
            resultat = bool(_DNS.resolve(domaine, "A"))
        except dns.exception.DNSException:
            resultat = False
    except dns.exception.DNSException:
        resultat = False
    _CACHE_MX[domaine] = resultat
    return resultat


def classer(email: str, domaine_site: str | None = None) -> tuple[str, int]:
    """(type_email, score). Type : pro_nominatif / pro_role / perso / inconnu."""
    local, _, domaine = email.partition("@")
    local_base = local.split("+")[0]
    est_freemail = domaine in config.FREEMAIL_DOMAINS
    est_role = local_base in config.ROLE_LOCALPARTS or any(
        local_base.startswith(r) for r in ("contact", "info", "commercial", "vente")
    )
    meme_domaine = bool(domaine_site) and domaine == domaine_site

    if est_freemail:
        # Donnée personnelle probable : segment à part, jamais dans l'export principal.
        return "perso", 20 if est_role else 10
    score = 50
    if meme_domaine:
        score += 20
    if est_role:
        return "pro_role", score + 15
    if "." in local_base or "-" in local_base:
        return "pro_nominatif", score + 10
    return "pro_role" if len(local_base) <= 4 else "pro_nominatif", score


def run(conn: sqlite3.Connection, *, refaire: bool = False) -> int:
    sql = "SELECT e.siret, e.email, e.source FROM emails e"
    if not refaire:
        sql += " WHERE e.mx_ok IS NULL"
    lignes = list(store.iter_rows(conn, sql))
    if not lignes:
        print("Rien à valider.")
        return 0
    domaines_site = {
        r["siret"]: r["domaine"]
        for r in store.iter_rows(conn, "SELECT siret, domaine FROM sites "
                                       "WHERE statut = 'retenu' GROUP BY siret")
    }
    opposition = charger_opposition(conn)
    print(f"Validation de {len(lignes)} emails (MX + classement)...")
    maj, supprimes = [], 0
    for i, ligne in enumerate(lignes, 1):
        email = ligne["email"]
        domaine = email.partition("@")[2]
        if email in opposition or domaine in opposition:
            conn.execute("DELETE FROM emails WHERE siret = ? AND email = ?",
                         (ligne["siret"], email))
            supprimes += 1
            continue
        type_email, score = classer(email, domaines_site.get(ligne["siret"]))
        ok = mx_ok(domaine)
        if not ok:
            score = max(0, score - 40)
        maj.append((1 if ok else 0, type_email, score, ligne["siret"], email))
        if i % 200 == 0:
            print(f"  {i}/{len(lignes)}", end="\r", flush=True)
    conn.executemany(
        "UPDATE emails SET mx_ok = ?, type_email = ?, score = ? WHERE siret = ? AND email = ?",
        maj,
    )
    conn.commit()
    store.set_meta(conn, "derniere_validation",
                   datetime.now(timezone.utc).isoformat(timespec="seconds"))
    stats = conn.execute(
        "SELECT type_email, COUNT(*) n, SUM(mx_ok) mx FROM emails GROUP BY type_email"
    ).fetchall()
    for s in stats:
        print(f"  {s['type_email'] or 'inconnu':15s} {s['n']:6d} dont MX valide : {s['mx'] or 0}")
    if supprimes:
        print(f"  {supprimes} emails retirés (liste d'opposition)")
    return len(maj)


def charger_opposition(conn: sqlite3.Connection) -> set[str]:
    return {r[0].strip().lower() for r in conn.execute("SELECT cle FROM opposition")}


def ajouter_opposition(conn: sqlite3.Connection, cles: list[str], motif: str) -> int:
    maintenant = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lignes = [{"cle": c.strip().lower(), "motif": motif, "ajoute_le": maintenant}
              for c in cles if c.strip()]
    store.upsert_many(conn, "opposition", lignes)
    # On purge aussi ce qui est déjà en base.
    for ligne in lignes:
        conn.execute("DELETE FROM emails WHERE email = ? OR email LIKE ?",
                     (ligne["cle"], "%@" + ligne["cle"]))
    conn.commit()
    return len(lignes)
