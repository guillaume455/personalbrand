"""Configuration centrale du pipeline."""
from __future__ import annotations

import datetime as _dt
import os
from pathlib import Path

# --- Chemins -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("PROSPECT_DATA_DIR", ROOT / "data"))
DB_PATH = DATA_DIR / "prospect.sqlite"
EXPORT_DIR = DATA_DIR / "exports"
CACHE_DIR = DATA_DIR / "cache"

# --- Périmètre métier --------------------------------------------------------
# Codes NAF rév. 2 (= ceux effectivement portés par Sirene jusqu'au 31/12/2026 ;
# la NAF 2025 n'entre en vigueur que le 01/01/2027).
NAF_MARCHAND = {
    "4511Z": "Commerce de voitures et de véhicules automobiles légers",
    "4519Z": "Commerce d'autres véhicules automobiles",
    "4540Z": "Commerce et réparation de motocycles",
}
NAF_REPARATION = {
    "4520A": "Entretien et réparation de véhicules automobiles légers",
    "4520B": "Entretien et réparation d'autres véhicules automobiles",
    "4532Z": "Commerce de détail d'équipements automobiles",
}
NAF_PIECES = {
    "4531Z": "Commerce de gros d'équipements automobiles",
}
NAF_LOCATION = {
    "7711A": "Location de courte durée de voitures et de véhicules automobiles légers",
    "7711B": "Location de longue durée de voitures et de véhicules automobiles légers",
}
# Équivalents NAF 2025 (informatifs aujourd'hui, en vigueur au 01/01/2027).
# Sirene expose déjà la colonne activitePrincipaleNAF25Etablissement depuis déc. 2025.
NAF25_MARCHAND = {
    "4671G": "Commerce de gros de véhicules automobiles légers (< 3,5 t)",
    "4781Y": "Commerce de détail de véhicules automobiles",
    "4792G": "Intermédiation pour le commerce de détail de véhicules automobiles",
    "4618Y": "Intermédiaires spécialisés du commerce de gros d'autres produits",
}

NAF_GROUPS = {
    "marchand": NAF_MARCHAND,
    "reparation": NAF_REPARATION,
    "pieces": NAF_PIECES,
    "location": NAF_LOCATION,
}
DEFAULT_GROUPS = ("marchand",)

DEFAULT_DATE_MIN = "2024-01-01"


def default_date_max() -> str:
    return _dt.date.today().isoformat()


# --- Sources open data -------------------------------------------------------
# Le jeu de données Sirene est résolu dynamiquement via l'API data.gouv.fr :
# les URL directes des fichiers changent à chaque publication mensuelle.
DATAGOUV_DATASET = "base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret"
DATAGOUV_API = "https://www.data.gouv.fr/api/1/datasets/{slug}/"
STOCK_ETABLISSEMENT_HINT = "StockEtablissement_utf8"
STOCK_UNITE_LEGALE_HINT = "StockUniteLegale_utf8"

OVERPASS_ENDPOINTS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
)
# Tags OSM qui décrivent un professionnel de l'auto/moto.
OSM_FILTERS = (
    '["shop"="car"]',
    '["shop"="car_repair"]',
    '["shop"="motorcycle"]',
    '["shop"="truck"]',
    '["shop"="caravan"]',
    '["shop"="motorcycle_repair"]',
)

# --- Politesse réseau --------------------------------------------------------
# Mets une adresse de contact réelle : c'est la règle de courtoisie de base pour
# crawler, et Overpass/data.gouv loguent le User-Agent.
CONTACT_EMAIL = os.environ.get("PROSPECT_CONTACT_EMAIL", "")
USER_AGENT = (
    "prospect-auto-fr/0.1 (pipeline open data ; contact: {contact})".format(
        contact=CONTACT_EMAIL or "non renseigne - definir PROSPECT_CONTACT_EMAIL"
    )
)
HTTP_TIMEOUT = 20
CRAWL_DELAY_PER_DOMAIN = 2.0  # secondes entre 2 requêtes sur un même domaine
CRAWL_WORKERS = 8
MAX_PAGES_PER_SITE = 6
RESPECT_ROBOTS = True

# --- Qualification ----------------------------------------------------------
FREEMAIL_DOMAINS = {
    "gmail.com", "googlemail.com", "hotmail.fr", "hotmail.com", "outlook.fr",
    "outlook.com", "live.fr", "msn.com", "yahoo.fr", "yahoo.com", "orange.fr",
    "wanadoo.fr", "free.fr", "sfr.fr", "laposte.net", "bbox.fr", "numericable.fr",
    "neuf.fr", "aliceadsl.fr", "icloud.com", "me.com", "protonmail.com", "proton.me",
}
ROLE_LOCALPARTS = {
    "contact", "info", "infos", "commercial", "commerciale", "vente", "ventes",
    "sales", "direction", "accueil", "secretariat", "atelier", "sav", "service",
    "administratif", "compta", "comptabilite", "devis", "rdv", "garage", "auto",
}
# Adresses à ne jamais retenir (prestataires, thèmes, trackers, exemples).
EMAIL_BLOCKLIST_DOMAINS = {
    "example.com", "example.org", "domain.com", "email.com", "sentry.io",
    "wixpress.com", "wix.com", "godaddy.com", "squarespace.com", "shopify.com",
    "wordpress.com", "wordpress.org", "jimdo.com", "webself.net", "e-monsite.com",
    "sitew.com", "orson.io", "simplebo.fr", "solocal.com", "pagesjaunes.fr",
    "google.com", "facebook.com", "cloudflare.com", "adobe.com", "w3.org",
    "schema.org", "mysite.com", "votredomaine.fr", "nomdedomaine.fr",
}
EMAIL_BLOCKLIST_LOCALPARTS = {
    "webmaster", "no-reply", "noreply", "nepasrepondre", "postmaster", "abuse",
    "privacy", "dpo", "rgpd", "hostmaster", "sentry", "your", "votre", "nom",
    "email", "adresse", "mail",
}
# Pages qui contiennent l'email dans 90 % des cas.
CONTACT_PATH_HINTS = (
    "contact", "contactez", "nous-contacter", "mentions-legales", "mentions_legales",
    "mentions", "legal", "legales", "infos-legales", "qui-sommes-nous", "a-propos",
    "apropos", "about", "equipe", "notre-equipe", "cgv", "conditions", "devis",
    "horaires", "acces", "plan-acces", "reprise", "rachat",
)
# Mots trop courants pour identifier une entreprise, mais bon signe métier
# quand ils apparaissent dans un nom de domaine.
MOTS_GENERIQUES_AUTO = {
    "auto", "autos", "automobile", "automobiles", "garage", "cars", "car",
    "motors", "moto", "motos", "vo", "vehicules", "vehicule", "occasion",
    "occasions", "carrosserie", "mecanique", "pneus", "sport", "prestige",
}

MIN_SITE_CONFIDENCE = 2  # score minimal pour considérer qu'un domaine est le bon
