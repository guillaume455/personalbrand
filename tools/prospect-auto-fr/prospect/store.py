"""Stockage SQLite : le pipeline est reprenable, chaque étape écrit ses résultats."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable, Iterator

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS etablissements (
    siret TEXT PRIMARY KEY,
    siren TEXT NOT NULL,
    raison_sociale TEXT,
    enseigne TEXT,
    naf TEXT,
    naf25 TEXT,
    naf_libelle TEXT,
    date_creation TEXT,
    etat TEXT,
    statut_diffusion TEXT,
    est_siege INTEGER,
    tranche_effectif TEXT,
    categorie_juridique TEXT,
    adresse TEXT,
    code_postal TEXT,
    commune TEXT,
    departement TEXT,
    personne_physique INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_etab_siren ON etablissements(siren);
CREATE INDEX IF NOT EXISTS idx_etab_cp ON etablissements(code_postal);

CREATE TABLE IF NOT EXISTS osm_pois (
    osm_key TEXT PRIMARY KEY,
    nom TEXT,
    commune TEXT,
    code_postal TEXT,
    site_web TEXT,
    email TEXT,
    telephone TEXT,
    siret_ref TEXT,
    shop TEXT,
    lat REAL,
    lon REAL
);
CREATE INDEX IF NOT EXISTS idx_osm_siret ON osm_pois(siret_ref);

CREATE TABLE IF NOT EXISTS sites (
    siret TEXT NOT NULL,
    url TEXT NOT NULL,
    domaine TEXT,
    source TEXT,
    confiance INTEGER DEFAULT 0,
    statut TEXT,
    verifie_le TEXT,
    PRIMARY KEY (siret, url)
);
CREATE INDEX IF NOT EXISTS idx_sites_domaine ON sites(domaine);

CREATE TABLE IF NOT EXISTS emails (
    siret TEXT NOT NULL,
    email TEXT NOT NULL,
    source TEXT,
    url_source TEXT,
    type_email TEXT,
    mx_ok INTEGER,
    score INTEGER DEFAULT 0,
    trouve_le TEXT,
    PRIMARY KEY (siret, email)
);
CREATE INDEX IF NOT EXISTS idx_emails_email ON emails(email);

CREATE TABLE IF NOT EXISTS pages_vues (
    url TEXT PRIMARY KEY,
    statut TEXT,
    vue_le TEXT
);

CREATE TABLE IF NOT EXISTS opposition (
    cle TEXT PRIMARY KEY,   -- email complet ou domaine
    motif TEXT,
    ajoute_le TEXT
);

CREATE TABLE IF NOT EXISTS meta (
    cle TEXT PRIMARY KEY,
    valeur TEXT
);
"""


def connect(path: Path | str | None = None) -> sqlite3.Connection:
    target = Path(path) if path else config.DB_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(SCHEMA)
    return conn


def upsert_many(conn: sqlite3.Connection, table: str, rows: Iterable[dict[str, Any]],
                batch: int = 5000) -> int:
    """INSERT ... ON CONFLICT DO UPDATE générique, par lots."""
    rows = iter(rows)
    total = 0
    pk = {
        "etablissements": ["siret"],
        "osm_pois": ["osm_key"],
        "sites": ["siret", "url"],
        "emails": ["siret", "email"],
        "pages_vues": ["url"],
        "opposition": ["cle"],
        "meta": ["cle"],
    }[table]
    buffer: list[dict[str, Any]] = []
    while True:
        chunk = []
        for row in rows:
            chunk.append(row)
            if len(chunk) >= batch:
                break
        if not chunk:
            break
        cols = list(chunk[0].keys())
        updates = [c for c in cols if c not in pk]
        sql = "INSERT INTO {t} ({cols}) VALUES ({ph})".format(
            t=table, cols=", ".join(cols), ph=", ".join("?" for _ in cols)
        )
        if updates:
            sql += " ON CONFLICT({pk}) DO UPDATE SET {sets}".format(
                pk=", ".join(pk),
                sets=", ".join(f"{c}=excluded.{c}" for c in updates),
            )
        else:
            sql += " ON CONFLICT DO NOTHING"
        conn.executemany(sql, [[r.get(c) for c in cols] for r in chunk])
        conn.commit()
        total += len(chunk)
        buffer = chunk
        if len(chunk) < batch:
            break
    del buffer
    return total


def count(conn: sqlite3.Connection, table: str, where: str = "") -> int:
    sql = f"SELECT COUNT(*) FROM {table}"
    if where:
        sql += f" WHERE {where}"
    return conn.execute(sql).fetchone()[0]


def iter_rows(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> Iterator[sqlite3.Row]:
    cur = conn.execute(sql, params)
    while True:
        rows = cur.fetchmany(1000)
        if not rows:
            return
        yield from rows


def set_meta(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO meta (cle, valeur) VALUES (?, ?) "
        "ON CONFLICT(cle) DO UPDATE SET valeur=excluded.valeur",
        (key, value),
    )
    conn.commit()


def get_meta(conn: sqlite3.Connection, key: str, default: str | None = None) -> str | None:
    row = conn.execute("SELECT valeur FROM meta WHERE cle = ?", (key,)).fetchone()
    return row[0] if row else default
