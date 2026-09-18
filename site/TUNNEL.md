# Tunnel /accompagnement

Onze pages statiques, sans étape de build, alignées sur la stack du site
(HTML/CSS/JS servis par OVH). Ce document dit ce qui est fait, ce qui reste à
brancher, et où.

## État du lot

| Élément | État |
|---|---|
| Les 11 pages, contenus définitifs du cahier des charges mis en forme | fait |
| Table de qualification §3, vérifiée sur les 20 combinaisons | fait |
| Formulaire 5 questions, pas à pas, reprise du brouillon, anti-robot | fait |
| Bandeau de consentement, refus aussi accessible que l'acceptation | fait |
| Événements de mesure, mis en file tant que le consentement manque | fait |
| Case de renoncement au droit de rétractation, bloquante | fait |
| `/temoignages` en `noindex`, hors sitemap, sans lien entrant | fait |
| CGV et politique de confidentialité | rédigées, **à faire relire** |
| Comptes externes (backend, Cal.com, Stripe, Brevo, GA4, pixel) | **à brancher** |
| Vidéo 60 s, photo d'archive, aperçu du dossier, PDF du calcul de marge | **à fournir** |
| Textes des e-mails E1 à E6 | **à rédiger** |

Tant que les comptes ne sont pas branchés, le tunnel tourne en **mode démo** :
il se parcourt de bout en bout, les envois sont journalisés dans la console du
navigateur au lieu de partir, et un avertissement s'affiche dans cette même
console. Rien ne casse, rien ne part.

## Regarder les pages en local

Les chemins sont **relatifs**, pas absolus : il suffit de double-cliquer
n'importe quel `index.html` pour voir la page complète, mise en forme comprise.
Le parcours entier se déroule ainsi, formulaire compris.

Deux détails propres à l'ouverture directe, sans effet une fois en ligne :

- la console signale que `archivo-latin.woff2` n'a pas pu être préchargé. Le
  préchargement exige `crossorigin`, que `file://` refuse par principe. La
  police se charge quand même, par la feuille de style ;
- les liens vers un dossier sont complétés en `…/index.html` par le script,
  parce qu'un navigateur ouvrant un fichier local affiche le contenu du dossier
  au lieu d'y chercher l'index. Une fois le site servi par OVH, la condition est
  fausse et les adresses restent propres.

## Ce qu'il faut renseigner

Tout tient dans **`/assets/js/config.js`**. Aucune clé n'est écrite ailleurs.

Ce fichier est servi au navigateur, donc public. N'y mettre que des clés
publiques : clé anonyme Supabase, identifiant de mesure, clé publiable Stripe.
**Jamais** de clé secrète, et surtout pas la clé d'API Brevo — d'où le fait que
les e-mails partent du backend et non de la page.

Une fois tout branché, passer `preprod` à `false` : cela masque les encarts
orange « à fournir » et les avertissements de console.

## Backend du formulaire

L'hébergement OVH est statique : rien ne s'exécute côté serveur. Les
candidatures partent en `fetch` vers un service externe, au choix Supabase ou
un webhook (Airtable + Make, n8n…).

Table `candidatures`, une colonne par champ :

```
horodatage · tunnel · avancement · capital · temps · delai · question
prenom · nom · email · telephone · zone · consentement
statut · statut_reservation
utm_source · utm_medium · utm_campaign · utm_content · page
```

`tunnel` vaut `lancement` et existe dès la première candidature : le second
tunnel « marchands » (§13) n'imposera pas de migration.

`statut` vaut `qualifie` ou `a_revoir`, jamais autre chose. **« Non qualifié »
n'est jamais calculé** : il résulte de ta seule lecture de la question libre.

Table `inscriptions` pour le calcul de marge : `horodatage · email ·
consentement · source · tunnel · page · utm`.

Le backend doit déclencher les e-mails **E1** (profil qualifié, avec le lien de
réservation), **E2** (profil à revoir, réponse sous 48 h) et **E3** (fiche
complète pour toi). **E5** (relance à 48 h sans réservation) suppose une tâche
planifiée. **E4** vient de l'outil de rendez-vous, **E6** de Brevo.

### Le statut est calculé dans le navigateur

Conséquence à connaître : quelqu'un d'un peu curieux peut ouvrir la console et
se déclarer qualifié pour atteindre la page de réservation. Il devra quand même
payer 490 € pour bloquer un créneau, donc le risque réel est faible. Si tu veux
fermer complètement la porte, il faut recalculer le statut côté backend et ne
transmettre le lien de réservation que par e-mail — c'est une évolution, pas un
correctif.

## Réservation

Cal.com de préférence, Calendly en repli. Réglages imposés par le §6 :

- « Diagnostic individuel », **90 minutes**, visio **Google Meet**
- fuseau **Europe/Paris** (tu es à Marrakech : vérifier le décalage)
- **8 réservations par semaine au maximum**. Recommandé : n'en ouvrir que 4 les
  deux premières semaines, puis monter selon la charge réelle
- **48 heures** de préavis minimum, tampons de **30 minutes** avant et après
- paiement Stripe de **490 € TTC** obligatoire, aucune réservation sans paiement
- report possible jusqu'à **24 heures** avant
- rappels automatiques à 24 h et 1 h
- redirection après paiement vers `/accompagnement/confirmation/`

### La case de renoncement

Le §6 demandait de vérifier en semaine 1 si Cal.com peut rendre obligatoire la
case de renoncement au droit de rétractation. **Le repli est déjà en place** :
la case est posée sur `/accompagnement/reservation/` et le module de réservation
ne s'affiche pas tant qu'elle n'est pas cochée. Si Cal.com sait porter la case
nativement, tant mieux, ce sera une ceinture de plus. Sinon, la page suffit.

Sans cette case, **toute séance tenue dans les 14 jours suivant la réservation
reste intégralement remboursable**, même après avoir eu lieu.

## Mesure

GA4 et pixel Meta. Rien ne se charge avant acceptation : aucun script, aucun
cookie, aucun appel réseau — c'est vérifié par les tests. Les événements
déclenchés avant la décision sont mis en attente et rejoués si le visiteur
accepte, jetés s'il refuse.

Événements émis : `page_view`, `cta_click` (avec la position du bouton),
`form_start`, `form_submit` (avec le statut), `booking_page_view`,
`purchase` (490 EUR), `lead_magnet_submit`.

Les UTM de la première page vue sont conservés pour la session et joints à la
candidature.

## Activer `/temoignages`

La page est en ligne mais volontairement invisible : `noindex, nofollow`,
absente du sitemap, bloquée dans `robots.txt`, et aucune page du site ne pointe
vers elle. Pour l'activer le jour où tu le décides :

1. `temoignages/index.html` : passer `robots` à `index, follow`
2. `robots.txt` : retirer la ligne `Disallow: /temoignages/`
3. `sitemap.xml` : ajouter l'URL
4. ajouter les liens voulus, notamment sous les extraits du tunnel

Avant d'activer, obtenir les **accords écrits de publication** des quatre
témoins (§11), et remplacer les mentions « année à préciser ».

## Ce qui reste à toi

- **Vidéo de 60 s** présentant le diagnostic — obligatoire pour le lancement
- **Photo d'archive 2010 ou Kbis flouté** — Drive « 02 Origine »
- **Aperçu du dossier « Plan de lancement »** — remplacer par un vrai dossier
  anonymisé dès le premier diagnostic test
- **PDF du calcul de marge** — à décliner depuis le carrousel existant
- **Années d'accompagnement** d'Aurélien, Pierre et Thomas
- **Accords écrits** des quatre témoins
- **Textes des e-mails E1 à E6** — à écrire à la main, pas à générer
- **Médiateur de la consommation** : nom et coordonnées, obligatoires dans les
  CGV pour tout professionnel vendant à des particuliers
- **Relecture juridique** des CGV et de la politique de confidentialité

Les emplacements manquants apparaissent en encadré orange sur les pages : ils
sont impossibles à rater, et ils disparaîtront quand `preprod` passera à `false`.

## Recette (annexe B)

Vérifié automatiquement, et rejouable :

- table de qualification conforme sur les **20 combinaisons** capital × délai
- parcours complet, branche qualifiée et branche à revoir
- aucun appel tiers ni cookie avant consentement, refus mémorisé
- refuser et accepter ont la même taille et la même graisse
- case de renoncement obligatoire avant l'affichage du module
- `/temoignages` en noindex, hors sitemap, sans lien entrant
- aucune donnée personnelle ni statut dans les URL
- le CTA apparaît 6 fois, aux 4 positions imposées
- colonnes « pour / pas pour » strictement identiques en traitement
- axe-core : **aucune violation** sur les 11 vues, en mobile et en desktop
- Lighthouse mobile : **performance 99-100, accessibilité 100**, LCP 1,65 à
  2,10 s en 4G simulée, CLS 0
- navigateur Instagram émulé (iOS et Android) : pas de débordement, champs à
  16 px donc pas de zoom automatique iOS
- parcours complet en ouverture directe des fichiers, sans serveur
- le pied de page et ses liens légaux restent atteignables bandeau affiché

À vérifier par toi, parce que ça ne se simule pas :

- **un vrai paiement de 490 € encaissé puis remboursé**
- **le parcours sur un vrai téléphone, dans la vraie application Instagram** —
  l'émulation reproduit la fenêtre et l'identifiant du navigateur, pas son moteur
- **les e-mails arrivant en boîte de réception et non en spam** (SPF, DKIM et
  DMARC sont déjà actifs via Google Workspace : vérifier la cohabitation avec
  Brevo sans casser l'existant)
- **les événements remontant réellement** dans GA4 et dans le gestionnaire Meta
