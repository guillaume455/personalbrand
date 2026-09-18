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

## 4. Scraper : où est réellement le risque

Le scraping n'est pas illégal en soi en France, et ce projet en fait — il crawle
les sites des entreprises. Trois fondements distincts sont à connaître, parce
qu'ils ne se déclenchent pas dans les mêmes conditions.

**Droit sui generis du producteur de base de données** (art. L341-1 et s. CPI).
C'est le fondement de l'arrêt le plus cité : *Leboncoin c/ Entreparticuliers*,
Cour d'appel de Paris, 18 février 2021, 50 000 € de dommages-intérêts. Ce qui a
été sanctionné : l'extraction **systématique d'une partie substantielle** de la
base d'annonces, **réutilisée dans un service concurrent** — donc aussi du
parasitisme économique et de la concurrence déloyale. Le critère est l'ampleur
et l'usage, pas le fait de scraper. Extraire les coordonnées de quelques
milliers de professionnels pour ta propre prospection, sans republier la base
ni concurrencer la source, est très loin de ces faits — ce n'est pas pour
autant une autorisation, et ça reste une appréciation au cas par cas.

**Conditions d'utilisation.** La plupart des marketplaces interdisent
contractuellement l'extraction automatisée. Le risque est alors contractuel
(blocage, mise en demeure), et c'est le plus probable en pratique.

**Accès et maintien dans un système** (art. 323-1 du code pénal). Contourner une
protection technique — captcha, authentification, blocage d'IP — change la
nature du problème. L'affaire *Bluetouff* (Cass. crim. 2014) a montré qu'un
contenu accessible publiquement ne vaut pas autorisation de le collecter quand
il existait une notion d'accès restreint.

**Et surtout le RGPD**, qui s'applique quelle que soit la licéité de la
collecte : la CNIL considère que des données publiquement accessibles ne peuvent
pas être moissonnées et réutilisées en prospection sans information des
personnes concernées. C'est la section 3 de ce document, et c'est le risque le
plus concret pour un usage comme le tien.

**Conséquence pratique pour ce projet.** Le scraper d'annuaires
(`prospect annuaire`) est générique : tu décris la cible, il moissonne. Aucune
marketplace n'est préconfigurée, pour deux raisons — leurs listings n'exposent
en général pas les emails (contact par formulaire : tu récupères des téléphones
et des sites, pas des adresses), et ce sont précisément les bases où le droit
sui generis a déjà mordu. Si tu choisis d'en cibler une, relis ses CGU, reste
sur une extraction ciblée, ne republie rien, et garde le délai par défaut.

## 5. Ce que le code ne fait pas

- **Pas de contournement d'anti-bot** : ni résolution de captcha, ni rotation de
  proxys ou d'empreintes pour échapper à un blocage. Au-delà du terrain
  juridique (art. 323-1), ça ne tient pas dans le temps : un scraper qui se bat
  contre une protection casse à chaque mise à jour du site.
- **Pas de vérification SMTP** (`RCPT TO`). Techniquement gratuit, mais ça brûle
  la réputation de l'IP et fait plus de faux négatifs que de vrais. Un vérifieur
  payant le fait mieux — voir la section « et ensuite » du README.
- **Pas de contournement d'obfuscation autre que celle de Cloudflare**, qui est
  un simple XOR public documenté, et non une mesure de protection.
