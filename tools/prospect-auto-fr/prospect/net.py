"""Couche réseau : User-Agent, politesse par domaine, robots.txt, téléchargements."""
from __future__ import annotations

import threading
import time
import urllib.robotparser as robotparser
from pathlib import Path
from urllib.parse import urlparse

import requests

from . import config

_LOCK = threading.Lock()
_LAST_HIT: dict[str, float] = {}
_ROBOTS: dict[str, robotparser.RobotFileParser | None] = {}


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": config.USER_AGENT,
        "Accept-Language": "fr-FR,fr;q=0.9",
    })
    return s


def throttle(url: str, delay: float | None = None) -> None:
    """Un seul hit par domaine toutes les `delay` secondes, tous threads confondus."""
    host = urlparse(url).netloc.lower()
    wait_for = delay if delay is not None else config.CRAWL_DELAY_PER_DOMAIN
    while True:
        with _LOCK:
            now = time.monotonic()
            last = _LAST_HIT.get(host, 0.0)
            if now - last >= wait_for:
                _LAST_HIT[host] = now
                return
            sleep_for = wait_for - (now - last)
        time.sleep(min(sleep_for, wait_for))


def robots_allows(url: str, sess: requests.Session | None = None) -> bool:
    """False si le robots.txt du site interdit l'URL à notre User-Agent."""
    if not config.RESPECT_ROBOTS:
        return True
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    with _LOCK:
        cached = _ROBOTS.get(origin, "missing")
    if cached == "missing":
        parser: robotparser.RobotFileParser | None = robotparser.RobotFileParser()
        parser.set_url(origin + "/robots.txt")
        try:
            sess = sess or session()
            throttle(origin, 1.0)
            resp = sess.get(origin + "/robots.txt", timeout=config.HTTP_TIMEOUT)
            if resp.status_code >= 400:
                parser = None  # pas de robots.txt = tout est autorisé
            else:
                parser.parse(resp.text.splitlines())
        except requests.RequestException:
            parser = None
        with _LOCK:
            _ROBOTS[origin] = parser
        cached = parser
    if cached is None:
        return True
    return cached.can_fetch(config.USER_AGENT, url)


def get(url: str, sess: requests.Session | None = None, *, check_robots: bool = True,
        timeout: int | None = None, delay: float | None = None) -> requests.Response | None:
    """GET poli. Renvoie None si interdit par robots.txt ou en cas d'erreur réseau."""
    sess = sess or session()
    if check_robots and not robots_allows(url, sess):
        return None
    throttle(url, delay)
    try:
        return sess.get(url, timeout=timeout or config.HTTP_TIMEOUT, allow_redirects=True)
    except requests.RequestException:
        return None


def download(url: str, dest: Path, *, sess: requests.Session | None = None,
             chunk: int = 1 << 20, resume: bool = True) -> Path:
    """Télécharge un gros fichier avec reprise (Range) et affichage de progression."""
    sess = sess or session()
    dest.parent.mkdir(parents=True, exist_ok=True)
    existing = dest.stat().st_size if dest.exists() else 0
    headers = {}
    mode = "wb"
    if resume and existing:
        head = sess.head(url, timeout=config.HTTP_TIMEOUT, allow_redirects=True)
        total = int(head.headers.get("Content-Length", 0))
        if total and existing >= total:
            print(f"  déjà téléchargé : {dest.name} ({existing/1e9:.2f} Go)")
            return dest
        headers["Range"] = f"bytes={existing}-"
        mode = "ab"
    with sess.get(url, stream=True, timeout=120, headers=headers) as resp:
        resp.raise_for_status()
        if resp.status_code == 200:
            mode, existing = "wb", 0  # le serveur ignore Range : on repart de zéro
        total = int(resp.headers.get("Content-Length", 0)) + existing
        done = existing
        last_print = 0.0
        with open(dest, mode) as fh:
            for block in resp.iter_content(chunk_size=chunk):
                fh.write(block)
                done += len(block)
                if time.monotonic() - last_print > 2:
                    pct = f"{done/total*100:.1f}%" if total else "?"
                    print(f"  {dest.name} : {done/1e9:.2f} Go ({pct})", end="\r", flush=True)
                    last_print = time.monotonic()
    print(f"  {dest.name} : {done/1e9:.2f} Go — terminé")
    return dest
