# prospect-auto-fr

Pipeline open data pour constituer une liste de contacts de **professionnels de
l'automobile en France**, à partir de sources 100 % gratuites et sans clé API.

Le problème : aucune source ne contient à la fois la liste exhaustive des
entreprises **et** leurs emails. Sirene (INSEE) donne la liste complète avec la
date de création, mais aucun email. Les bases qui ont des emails n'ont ni
l'exhaustivité ni le filtre sur la date de création. Ce pipeline fait le pont.

```
Sirene (liste officielle)  ──┐
                             ├─► appariement ─► découverte de site ─► crawl ─► validation ─► CSV
OpenStreetMap (emails/sites)─┘
```

## Démarrage

```bash
python3 -m pip install -r requirements.txt
export PROSPECT_CONTACT_EMAIL="ton@email.fr"   # politesse de crawl, évite des blocages
python3 -m prospect selfcheck                  # data.gouv + Overpass joignables ?
python3 -m prospect run --limite 300           # premier lot de test (~20 min)
python3 -m prospect stats
```

Puis le run complet, une fois que les chiffres du lot de test te conviennent :

```bash
python3 -m prospect run
```

Prévoir **~2 Go de disque** (les deux fichiers stock Sirene) et, pour la France
entière, **plusieurs heures** de crawl : le pipeline ne fait qu'un hit toutes
les 2 secondes par domaine, volontairement.

Tout est reprenable : la base SQLite (`data/prospect.sqlite`) garde l'état, une
commande relancée reprend là où elle s'était arrêtée. `--refaire` force une
reprise complète d'une étape.

## Les 7 étapes

| Commande | Ce qu'elle fait | Source |
|---|---|---|
| `sirene` | télécharge le stock mensuel, garde les NAF auto créés dans la période, récupère les raisons sociales | data.gouv.fr (Licence Ouverte) |
| `osm` | récupère les POI `shop=car`, `car_repair`, `motorcycle`, `truck`… qui ont un email ou un site | Overpass / OSM (ODbL) |
| `match` | rattache chaque POI à un SIRET (ref:FR:SIRET, puis nom+CP, puis nom+commune) | — |
| `resolve` | déduit le domaine depuis la raison sociale, vérifie en DNS puis par le contenu de la page | DNS + HTTP |
| `crawl` | visite l'accueil + les pages contact/mentions légales, extrait les emails | sites des entreprises |
| `validate` | MX du domaine, classement pro/rôle/perso, liste d'opposition | DNS |
| `export` | 3 CSV : contacts pro, contacts perso (prudence), établissements sans email | — |

## Périmètre (à ajuster)

Par défaut : les **marchands** (`4511Z` voitures, `4519Z` autres véhicules,
`4540Z` motocycles), créés depuis le **2024-01-01**, établissements **actifs**
et **diffusibles**.

```bash
# élargir aux garages, aux équipementiers, aux loueurs
python3 -m prospect sirene --groupes marchand,reparation,pieces,location

# une autre période
python3 -m prospect sirene --date-min 2020-01-01 --date-max 2026-09-18

# une seule région pour OSM
python3 -m prospect osm --zones sud-est,corse
```

> **NAF 2025** : la nouvelle nomenclature n'entre en vigueur que le
> **01/01/2027**. Jusque-là, le code APE qui compte est celui de la NAF rév. 2
> (`4511Z`…), et c'est bien ce que filtre le pipeline. Sirene expose déjà la
> colonne `activitePrincipaleNAF25Etablissement` à titre informatif : elle est
> stockée dans la base (colonne `naf25`) pour le jour où il faudra basculer.
> Les codes cibles de la bascule sont déjà notés dans `prospect/config.py`
> (`NAF25_MARCHAND`).

## Rendement : à quoi s'attendre

Chiffres à confirmer par ton propre `stats` — ils dépendent surtout de la part
d'entreprises qui ont un vrai site web, très faible chez les auto-entrepreneurs
récents :

- **Sirene** → la liste est exhaustive par construction.
- **OSM** → quelques milliers de pros de l'auto avec email ou site en France,
  dont une fraction seulement est appariable à une création récente. C'est du
  bonus de haute qualité, pas le gros du volume.
- **Déduction de domaine** → là où se joue le volume. Un nom distinctif
  (« AUTO PRESTIGE 77 ») se déduit bien ; « JEAN DUPRE » ne se déduit pas.
- **Crawl** → quand le site est trouvé, l'email sort dans la grande majorité des
  cas (mentions légales obligatoires en France).

Le fichier `sans_email_*.csv` n'est pas un déchet : c'est la liste exacte à
donner à un enrichisseur payant, avec SIRET et adresse, donc au meilleur taux
de match possible.

## Régler le compromis volume / qualité

Dans `prospect/config.py` :

- `MIN_SITE_CONFIDENCE` (défaut `2`) : baisser à `1` augmente le volume et les
  faux rattachements ; monter à `3` ne garde que les sites où le nom **et** la
  ville (ou le SIREN) apparaissent.
- `CRAWL_DELAY_PER_DOMAIN` (défaut `2.0` s) et `CRAWL_WORKERS` (défaut `8`) :
  ne descends pas le délai, monte plutôt le nombre de workers — ils travaillent
  sur des domaines différents.
- `MAX_PAGES_PER_SITE` (défaut `6`) : 8-10 gagne quelques emails sur les gros
  sites de concessions.
- `TLDS` dans `prospect/resolve.py` : ajouter `.eu`, `.net`, `.auto` élargit un
  peu, au prix de 1,5× plus de requêtes DNS.

Une instance SearXNG améliore nettement la découverte de sites, toujours sans
clé : `python3 -m prospect resolve --searx https://mon-instance-searx.fr`
(beaucoup d'instances publiques limitent le débit ou bloquent l'API JSON ;
la plus fiable est celle que tu héberges toi-même).

## Et ensuite, si le volume ne suffit pas

Dans l'ordre du rapport résultat/coût, en repartant de `sans_email_*.csv` :

1. **Un moteur de recherche avec API** (Brave Search, Bing, Google CSE) pour
   remplacer la déduction de domaine : c'est le seul vrai plafond du pipeline
   gratuit. Quelques euros pour quelques milliers de requêtes.
2. **Dropcontact** (français, conçu pour le RGPD) : enrichissement à partir du
   nom + SIRET, bon sur les TPE françaises.
3. **Un vérifieur d'emails** (Bouncer, NeverBounce) avant le premier envoi.
   Indispensable : un fichier non vérifié brûle un domaine d'envoi en une
   campagne.
4. **Pappers API** pour les dirigeants et quelques contacts, en complément.

Les branchements se font tous au même endroit : `resolve.py` (découverte) et
`validate.py` (vérification).

## Avant d'envoyer quoi que ce soit

Lis [`LEGAL.md`](LEGAL.md). En résumé : la prospection B2B par email est
licite sans consentement préalable (intérêt légitime), à condition que le
message concerne le métier de la personne, que ton identité soit claire et que
le refus soit possible en un clic. Le pipeline exclut d'office les
non-diffusibles, isole les emails personnels et gère une liste d'opposition —
le reste (mentions dans l'email, information des personnes, registre) est à ta
charge.

Sources à citer dans tes mentions : Sirene / INSEE (Licence Ouverte v2.0) et
© les contributeurs OpenStreetMap (ODbL).

## Développement

```bash
python3 -m unittest discover -s tests -v   # 18 tests, 100 % hors ligne
python3 -m prospect inspect-header data/cache/StockEtablissement.zip
```

Le schéma du stock Sirene bouge (une colonne a été ajoutée en décembre 2025) :
si le filtrage ne retient plus rien, `inspect-header` affiche les colonnes
réelles du fichier, à comparer avec les alias de `prospect/sirene.py`.
