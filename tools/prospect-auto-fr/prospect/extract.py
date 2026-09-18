"""Extraction d'emails dans une page HTML — le cœur du rendement.

Couvre les cas réels des sites de garages : mailto, texte brut, entités HTML,
obfuscation Cloudflare (data-cfemail), « nom (at) domaine.fr », JSON-LD.
"""
from __future__ import annotations

import html as _html
import re
from urllib.parse import unquote, urljoin, urlparse

from bs4 import BeautifulSoup

from . import config

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]{1,64}@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,24}")
# « contact (at) garage-dupre (dot) fr », « contact arobase garage.fr », « a@b .fr »
OBFUSC_RE = re.compile(
    r"([A-Za-z0-9._%+\-]{1,64})\s*(?:\(|\[|\{)?\s*(?:@|at|arobase|chez)\s*(?:\)|\]|\})?\s*"
    r"([A-Za-z0-9\-]{2,}(?:\s*(?:\(|\[)?\s*(?:\.|dot|point)\s*(?:\)|\])?\s*[A-Za-z0-9\-]{2,}){1,3})",
    re.IGNORECASE,
)
EXT_INTERDITES = (
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".css", ".js", ".php",
    ".html", ".htm", ".json", ".xml", ".woff", ".woff2", ".ttf", ".ico", ".pdf",
)


def decoder_cfemail(encode: str) -> str | None:
    """Décode l'obfuscation Cloudflare Email Protection (data-cfemail)."""
    try:
        cle = int(encode[:2], 16)
        return "".join(
            chr(int(encode[i:i + 2], 16) ^ cle) for i in range(2, len(encode), 2)
        )
    except (ValueError, IndexError):
        return None


def nettoyer(email: str) -> str | None:
    email = email.strip().strip(".,;:()[]<>\"'").lower()
    email = unquote(email)
    if email.count("@") != 1:
        return None
    local, _, domaine = email.partition("@")
    if not local or not domaine or "." not in domaine:
        return None
    if len(email) > 100 or len(local) > 64:
        return None
    if email.endswith(EXT_INTERDITES) or domaine.endswith(EXT_INTERDITES):
        return None
    if domaine in config.EMAIL_BLOCKLIST_DOMAINS or any(
        domaine.endswith("." + bloque) for bloque in config.EMAIL_BLOCKLIST_DOMAINS
    ):
        return None
    if local in config.EMAIL_BLOCKLIST_LOCALPARTS:
        return None
    if re.fullmatch(r"[0-9a-f]{16,}", local):  # clés Sentry & co
        return None
    if not re.fullmatch(r"[a-z0-9._%+\-]+", local):
        return None
    if not re.fullmatch(r"[a-z0-9.\-]+\.[a-z]{2,24}", domaine):
        return None
    if domaine.split(".")[-1] in {"png", "jpg", "js", "css"}:
        return None
    return email


def extraire(html_source: str, base_url: str = "") -> dict[str, str]:
    """Renvoie {email: méthode de découverte}."""
    trouves: dict[str, str] = {}

    def ajouter(brut: str, methode: str) -> None:
        propre = nettoyer(brut)
        if propre:
            trouves.setdefault(propre, methode)

    soup = BeautifulSoup(html_source, "html.parser")

    # 1. Cloudflare : <a class="__cf_email__" data-cfemail="...">
    for node in soup.select("[data-cfemail]"):
        decode = decoder_cfemail(node.get("data-cfemail", ""))
        if decode:
            ajouter(decode, "cfemail")

    # 2. mailto:
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.lower().startswith("mailto:"):
            cible = href[7:].split("?")[0]
            for part in cible.split(","):
                ajouter(part, "mailto")

    # 3. texte visible + entités HTML décodées
    texte = _html.unescape(soup.get_text(" ", strip=True))
    for m in EMAIL_RE.finditer(texte):
        ajouter(m.group(0), "texte")

    # 4. source brute (emails dans le JS, JSON-LD, attributs data-*)
    brut = _html.unescape(html_source)
    for m in EMAIL_RE.finditer(brut):
        ajouter(m.group(0), "source")

    # 5. obfuscations « (at) » / « arobase » / « vente &#64;domaine.fr »
    for m in OBFUSC_RE.finditer(texte):
        local, domaine = m.group(1), m.group(2)
        domaine = re.sub(r"\s*(?:\(|\[)?\s*(?:dot|point)\s*(?:\)|\])?\s*", ".",
                         domaine, flags=re.IGNORECASE)
        domaine = re.sub(r"\s+", "", domaine).lower()
        if len(local) >= 2 and re.fullmatch(r"[a-z0-9.\-]+\.[a-z]{2,6}", domaine):
            ajouter(f"{local}@{domaine}", "obfusque")

    return trouves


def liens_contact(html_source: str, base_url: str, max_liens: int = 6) -> list[str]:
    """Liens internes qui sentent la page contact / mentions légales."""
    soup = BeautifulSoup(html_source, "html.parser")
    origine = urlparse(base_url).netloc.lower().removeprefix("www.")
    scores: dict[str, int] = {}
    for a in soup.find_all("a", href=True):
        url = urljoin(base_url, a["href"].split("#")[0])
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            continue
        if parsed.netloc.lower().removeprefix("www.") != origine:
            continue
        cible = (parsed.path + " " + (a.get_text(" ", strip=True) or "")).lower()
        score = sum(1 for hint in config.CONTACT_PATH_HINTS if hint in cible)
        if score:
            scores[url] = max(scores.get(url, 0), score)
    return [u for u, _ in sorted(scores.items(), key=lambda kv: -kv[1])[:max_liens]]
