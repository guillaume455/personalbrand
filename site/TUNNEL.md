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
prenom · nom · email · telephone · zone · consentement · marketing
statut_lead · statut_suggere
utm_source · utm_medium · utm_campaign · utm_content · page
```

`tunnel` vaut `lancement` et existe dès la première candidature : le second
tunnel « marchands » n'imposera pas de migration.

`statut_lead` suit le cycle de vie imposé par le §33 du cahier V2 :
`started`, `completed`, `approved`, `rejected`, `checkout_started`, `paid`,
`booked`, `diagnostic_completed`, plus éventuellement `no_show`, `refunded`
et `nurture`. La page n'écrit que `completed` ; tous les autres sont posés
par le backend.

`statut_suggere` vaut `qualifie` ou `a_revoir`. C'est une **aide au tri**,
pas une décision. « Non qualifié » n'est jamais calculé.

`marketing` est le consentement facultatif du §50, distinct de celui qui
autorise le traitement de la candidature. Ne jamais confondre les deux :
remplir le questionnaire n'autorise pas la prospection.

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

### Ordre imposé : validation, puis paiement, puis agenda

Le §34 du cahier V2 impose cet ordre, et le §37 interdit d'exposer l'agenda
depuis la landing. Trois pages, trois rôles :

- `/accompagnement/merci/` annonce la réception de la candidature ;
- `/accompagnement/reservation/` porte la case de renoncement et le
  **paiement Stripe**, rien d'autre ;
- `/accompagnement/confirmation/` porte le **calendrier**, et n'est atteinte
  que par la redirection de succès de Stripe.

D'où deux champs distincts dans `config.js` : `reservation.checkoutStripe`
pour le lien de paiement, `reservation.url` pour le calendrier. Ne jamais
mettre le calendrier ailleurs que sur la page de confirmation.

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

Événements émis, conformes au §40 : `landing_view`, `page_view`,
`cta_click` (avec la position du bouton), `application_start`,
`contact_submitted`, `question_1_completed` à `question_5_completed`,
`application_complete`, `checkout_start`, `purchase` (490 EUR),
`booking_page_view`, `lead_magnet_signup`.

`lead_approved` et `lead_rejected` relèvent de ta décision manuelle : ils
sont posés par le backend, pas par la page.

Les UTM de la première page vue sont conservés pour la session et joints à la
candidature.

## Référencement : le tunnel est hors des moteurs

Jusqu'au lancement, **aucune page du tunnel n'est référençable** :
`/accompagnement` et ses étapes, `/calcul-marge` et sa page de remerciement,
`/cgv` et `/temoignages`. Seule `/confidentialite` reste indexable : elle
couvre aussi le formulaire de contact du site vitrine et son pied de page y
renvoie.

Trois couches, plus une absence volontaire :

1. **`<meta name="robots" content="noindex, nofollow">`** sur chaque page.
2. **En-tête `X-Robots-Tag: noindex, nofollow`**, posé par un `.htaccess` dans
   `accompagnement/`, `calcul-marge/`, `cgv/` et `temoignages/`. Les en-têtes
   sont hérités par les sous-dossiers.
3. **Sitemap** : aucune de ces pages n'y figure, et aucune page indexée ne
   renvoie vers `/accompagnement` (le lien qui existait dans les mentions
   légales a été retiré, le texte est resté).
4. **Aucun `Disallow` dans `robots.txt`**, et c'est délibéré.

### Pourquoi surtout pas de `Disallow`

C'est contre-intuitif, donc autant l'écrire noir sur blanc.

Un `Disallow` empêche le robot de **charger** la page. Il ne peut donc pas y
lire la balise `noindex`. Si quelqu'un poste l'adresse quelque part, Google
indexe alors l'URL seule, sans titre ni description, avec la mention « aucune
information disponible » — exactement l'inverse du but recherché. Pour qu'une
page soit réellement exclue, le robot doit pouvoir la charger et y voir le
`noindex`. C'est la recommandation de Google elle-même.

Seconde raison, plus concrète : **le robot de Meta respecte `robots.txt`**. Un
`Disallow` supprimerait l'aperçu des liens partagés en story, en DM ou sur
WhatsApp. Or c'est précisément par là que doit arriver tout le trafic.

### Vérifier une fois en ligne

```
curl -sI  https://guillaumeherbin.fr/accompagnement/ | grep -i x-robots-tag
curl -s   https://guillaumeherbin.fr/accompagnement/ | grep -i 'name="robots"'
```

La première commande doit renvoyer `X-Robots-Tag: noindex, nofollow`. Si elle
ne renvoie rien, c'est que `mod_headers` n'est pas actif sur l'hébergement :
la balise HTML suffit alors, mais on perd la seconde couche.

Dans la Search Console, ne **pas** soumettre ces URL à l'indexation, et ne pas
s'inquiéter de les voir signalées « Exclue par la balise noindex » : c'est le
résultat attendu.

### Activer le référencement au lancement

1. retirer `noindex=True` des pages concernées et régénérer, ou remplacer la
   balise par `index, follow` à la main
2. supprimer les fichiers `.htaccess` des dossiers concernés
3. ajouter les URL au `sitemap.xml`
4. rétablir les liens internes voulus
5. demander l'indexation dans la Search Console

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
- **Aperçu du dossier « Plan de lancement »** — brief complet prêt à
  transmettre dans [`BRIEF-APERCU-DOSSIER.md`](BRIEF-APERCU-DOSSIER.md).
  À remplacer par un vrai dossier anonymisé dès le premier diagnostic test
- **PDF du calcul de marge** — à décliner depuis le carrousel existant
- **Années d'accompagnement** d'Aurélien, Pierre et Thomas
- **Accords écrits** des quatre témoins
- **Textes des e-mails E1 à E6** — à écrire à la main, pas à générer
- **Médiateur de la consommation** : nom et coordonnées, obligatoires dans les
  CGV pour tout professionnel vendant à des particuliers
- **Relecture juridique** des CGV et de la politique de confidentialité

Les emplacements manquants apparaissent en encadré orange sur les pages : ils
sont impossibles à rater, et ils disparaîtront quand `preprod` passera à `false`.

## Intégrer un visuel reçu

Déposer le fichier dans `assets/img/tunnel/`, puis remplacer le bloc
`<div class="a-fournir">` correspondant par :

```html
<div class="media" style="margin-top:26px">
  <picture>
    <source srcset="../assets/img/tunnel/NOM.webp" type="image/webp">
    <img src="../assets/img/tunnel/NOM.jpg" width="1600" height="1067"
         alt="DESCRIPTION" loading="lazy" decoding="async">
  </picture>
</div>
```

Les attributs `width` et `height` sont obligatoires : sans eux la page saute
pendant le chargement et le score de stabilité visuelle tombe. Le chemin est
en `../` depuis `/accompagnement/`, en `../../` depuis une sous-page.

`.media img` impose un rapport 4/5 : pour un visuel paysage, ajouter
`style="aspect-ratio:3/2"` sur la balise `img`.

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
