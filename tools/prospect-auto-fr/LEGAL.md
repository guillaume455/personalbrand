# Cadre juridique — à lire avant le premier envoi

Rien ici ne remplace un avis d'avocat. C'est le résumé des règles que le pipeline
applique par construction, et de celles qui restent à ta charge.

## 1. Les sources sont réutilisables

| Source | Licence | Obligation |
|---|---|---|
| Base Sirene (INSEE, via data.gouv.fr) | Licence Ouverte v2.0 | citer la source et la date de la version |
| OpenStreetMap (Overpass) | ODbL | citer « © les contributeurs OpenStreetMap » |
| Sites web des entreprises | pas de licence : données publiées par l'entreprise | robots.txt respecté, pas de contournement de protection |

Le pipeline conserve dans chaque ligne exportée la colonne `url_source` : c'est
elle qui prouve d'où vient une adresse le jour où quelqu'un le demande.

## 2. Ce que le code exclut tout seul

- **Établissements non diffusibles** (`statutDiffusionEtablissement` ≠ `O`) :
  jamais extraits. Même règle appliquée au niveau de l'unité légale — si l'unité
  légale est non diffusible, l'établissement est supprimé de la base.
- **Emails en freemail** (gmail, orange, free…) : classés `perso` et exportés
  dans un fichier séparé, jamais dans `contacts_pro_*.csv`. Ce sont des données
  personnelles au sens plein, pas des adresses d'entreprise.
- **Adresses de rôle non commerciales** : `dpo@`, `rgpd@`, `privacy@`,
  `abuse@`, `postmaster@`, `no-reply@` sont écartées à l'extraction.
- **Liste d'opposition** : `python -m prospect opposition <email|domaine>` purge
  la base et bloque toute réapparition aux runs suivants.

## 3. Ce qui reste à ta charge

**Base légale.** En B2B, la prospection par email vers une adresse
professionnelle, sur un sujet en lien avec le métier de la personne, repose sur
l'intérêt légitime (RGPD art. 6.1.f) — pas de consentement préalable requis
(position constante de la CNIL). La condition « en lien avec le métier » n'est
pas cosmétique : un message hors sujet fait tomber la base légale.

**Dans chaque message.** Ton identité, l'objet, un moyen de refus simple et
gratuit (lien ou « répondez STOP »), et l'origine des données si on te la
demande. Traite les refus immédiatement : c'est à ça que sert la commande
`opposition`.

**Information des personnes.** Tu collectes des données sans contact préalable :
l'information doit être fournie au plus tard au premier message (RGPD art. 14),
en pratique via une page « politique de confidentialité » liée dans l'email.

**Registre des traitements.** Obligatoire dès que tu traites des données
personnelles de façon non occasionnelle. Une page suffit : finalité
(prospection B2B), catégories de données, sources (Sirene, OSM, sites web),
durée de conservation (3 ans sans réponse est la référence CNIL), destinataires.

**Cas particulier des entrepreneurs individuels.** Une partie importante des
marchands auto créés récemment sont des personnes physiques : leur raison
sociale *est* leur nom, leur email est souvent personnel. La colonne
`personne_physique` les signale. Traite-les avec prudence, ou exclus-les.

**Bloctel** ne concerne que le téléphone, pas l'email.

## 4. Ce que le code ne fait pas, volontairement

- **Pas de scraping des marketplaces** (LaCentrale, LeBonCoin, AutoScout24…).
  Leurs CGU l'interdisent et leurs annonces ne sont pas de l'open data. C'est le
  gisement le plus dense de marchands actifs, mais il se travaille autrement :
  compte pro, partenariat, ou récupération manuelle.
- **Pas de vérification SMTP** (`RCPT TO`). Techniquement gratuit, mais ça brûle
  la réputation de l'IP et fait plus de faux négatifs que de vrais. Un vérifieur
  payant le fait mieux — voir la section « et ensuite » du README.
- **Pas de contournement d'obfuscation autre que celle de Cloudflare**, qui est
  un simple XOR public et non une mesure de protection.
