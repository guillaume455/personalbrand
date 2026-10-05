---
version: 4
name: "Entrepreneurs 2.0 · Launch Frame v8 · La ligne du temps (version finale)"
description: >
  Charte du film v8 (49,52 s, 1920×1080, 30 i/s), sur la voix voix-v8.wav. Direction C « La ligne du temps », choisie
  par Colin, refaite dans un langage épuré à la Reakly (papier clair, beaucoup d'air, interfaces minimalistes aux ombres
  douces, cartes qui volent en profondeur, mot clé dans une boîte d'encre à angles nets, sous-titres centrés en bas),
  avec la charte d'Entrepreneurs 2.0 (papier chaud #f6f1e9, encre #1a1612, terracotta #c25b28 réservé aux moments qui
  comptent, Instrument Sans, Space Mono pour la frise, Big Shoulders pour la marque, carte de fin sombre de la marque).
  Une frise du temps, règle fine aux graduations pendues, porte tout le film : les vraies interfaces sont des stations
  POSÉES sur sa ligne. Le pivot « Il est temps de changer. » se joue sur le sombre de la marque (#0d0b0a).
unit: 1920×1080
principle: "une frise, des stations posées dessus, une idée par image, un geste par transition, chaque couture invisible"
reference: "reference/frise.html (code commun exécutable : kit caméra, frise des jours et des années, stations, barres d'attente, sol, pli, monde B, gabarits devis, montage vidéo, notification, facture, méthode, puce de contact, pastille d'idée, sous-titre, boîte d'encre, trait terracotta ; source UNIQUE) ; reference/v6-*.html (vraies interfaces : Safari et vrai site, iPhone 18 WhatsApp, tuiles d'outils, fenêtre Claude, carte de fin)"

colors:
  paper: "#f6f1e9"             # LE fond du film (monde clair), dégradé très doux vers #efe7dc aux bords
  paper-light: "#fffdf9"       # cartes, colonne AUJOURD'HUI
  ink: "#1a1612"               # encre : traits de la frise, textes, boîte d'encre
  ink-soft: "rgba(26,22,18,.55)"
  canvas: "#0d0b0a"            # sombre de la marque : pivot (séquence 5) et carte de fin (séquence 9)
  ink-on-dark: "#f5efe7"
  accent: "#c25b28"            # terracotta : SEULEMENT les moments qui comptent (voir TEXTE) et la carte de fin
  accent-light: "#d4703f"      # « 2.0 » du mot-symbole
  accent-glow: "#e08a5c"
  claude: "#D97757"            # uniquement DANS la fenêtre Claude (logo, coches, bouton d'envoi)

fonts:
  Instrument Sans: { files: ["assets/fonts/InstrumentSans-400.woff2 (400)", "assets/fonts/InstrumentSans-500.woff2 (500)", "assets/fonts/InstrumentSans-600.woff2 (600)", "assets/fonts/InstrumentSans-700.woff2 (700)"] }
  Space Mono: { files: ["assets/fonts/SpaceMono-400.woff2 (400)", "assets/fonts/SpaceMono-700.woff2 (700)"] }
  Big Shoulders: { files: ["assets/fonts/BigShoulders-800.woff2 (800)"] }

typography:
  subtitle:      { fontFamily: "Instrument Sans", px: 62, weight: 600, lineHeight: 74, tracking: "-0.015em", note: "la phrase de la voix, EN BAS AU CENTRE (classe .fx-sub, haut 896 px, dans la zone réservée y 890 à 980), mot par mot : chaque mot arrive gris (encre à 35 %) puis passe à l'encre en 0,2 s. Ombre claire légère pour se détacher. Sur le sombre : #f5efe7 (.fx-sub.dark). Une seule phrase à la fois ; une phrase coupée par une couture se prolonge avec « … »" }
  type:          { fontFamily: "Instrument Sans", px: 84, weight: 600, lineHeight: 1.12, tracking: "-0.025em", note: "les trois moments typographiques seulement (séquence 3, pivot de la séquence 5, séquence 8) : la phrase EST l'image, centrée ; jamais plus grand que 84 px ; pas de sous-titre en bas pendant ces moments" }
  frise-day:     { fontFamily: "Space Mono", px: 44, weight: 700, tracking: "4px", note: "« LUN 12 » sur la frise (unités u) ; heures « 06:00 » en 20 u 400 ; mois « JUIN 2023 » en 22 u, interlettrage 7 u" }
  frise-year:    { fontFamily: "Space Mono", px: 300, weight: 700, note: "« 2024 » sur la frise des années (u) ; mois en 24 u" }
  micro:         { fontFamily: "Space Mono", px: 16, weight: 400, tracking: "0.2em", upper: true, note: "étiquettes des cartes (« DEVIS », « FACTURE », « LA MÉTHODE », « EN ATTENTE »)" }
  ui:            { fontFamily: "Instrument Sans", px: 22, weight: 500, lineHeight: 1.3, note: "texte des cartes" }
  price:         { fontFamily: "Space Mono", px: 40, weight: 700, note: "« 1 000 € » dans la case du devis ; montants des factures en 34" }
  idea:          { fontFamily: "Instrument Sans", px: 34, weight: 600, note: "pastilles d'idées de la séquence 7" }
  wordmark:      { fontFamily: "Big Shoulders", px: 120, weight: 800, upper: true, note: "« ENTREPRENEURS » en #f5efe7 et « 2.0 » en #d4703f (exception unique)" }
  cta:           { fontFamily: "Big Shoulders", px: 34, weight: 800, upper: true }

components:
  frise:
    summary: "LE composant central : une règle fine, vue de face avec une légère perspective, posée sur un sol de points très pâles. La ligne (Y 600) porte les stations ; les graduations PENDENT dessous (heures, 06:00/12:00/18:00, minuit), l'étiquette du jour « LUN 12 » sous la graduation de minuit, le mois dessous. Trois voies d'attente (hachures) peuvent courir sous les étiquettes. Code : fxDaySVG, fxYearSVG, fxBuildRibbon, fxUpdateRibbon, fxDrawFloor. Section « LA FRISE »."
  camera:
    summary: "Caméra 3D cam(x, y, z, yaw, pitch, roll) + flou + dof(zf, k, max) sur la frise ; caméra 2D cam2(x, y, s) pour le monde B (colonne et tableau), les moments typographiques et la carte de fin. Dérive permanente, crans, whips. Section « CAMÉRA »."
  station:
    summary: "Vraie interface POSÉE sur la ligne de la frise, centrée sur son jour (pied en Y 600), face caméra, avec une ombre de contact douce : fxStand(el, cam, P, base, ax, ay, rot) + fxShadow. Jamais flottante, jamais décentrée dans le plan qui la présente. Positions : section « LA FRISE »."
  wait-bar:
    look: "barre d'attente : hachures d'encre fines à 135°, contour 2 px encre à 26 %, rayon 12, hauteur 70 u, étiquette Space Mono « EN ATTENTE » ; elle se TEND vers la droite par scaleX (origine à gauche) et se RÉTRACTE par scaleX vers aujourd'hui (origine à droite). Classes .fx-wait, .fx-wait-l ; fxMakeWait, fxUpdateWait."
  card:
    look: "toutes les cartes du monde clair : #fffdf9, rayon 16, ombre 0 30px 80px rgba(60,40,20,.14) + 0 2px 6px + filet 1 px encre à 5 % (classe .fx-card). Elles arrivent en volant en profondeur (×1,08 à ×1,2, flou 6 à 10 px → net en 0,14 à 0,2 s expo.out) et ne restent jamais figées (dérive de 2 à 6 px/s)."
  devis:
    look: "gabarit fx-devis (520 × 640) : marque « Studio Cadran » + « Agence web · Nantes », « DEVIS N° 0147 », ligne « Modification sur ton site » / « Changer le titre de la page d’accueil » / « 1 jour », case TOTAL encadrée d'encre avec la cellule du prix « 1 000 € » (Space Mono 700 40) ; trait de rature .fx-dv-strike."
  whatsapp:
    look: "WhatsApp iOS actuel, clair, dans l'iPhone 18 (reference/v6-02-attente.html, station B : .f02-phone à .f02-home) : « Prestataire web », pastilles de date « Lundi », « Vendredi », bulles sortantes #e0fcd6 aux coches BLEUES #3479f3 ; bulle ENTRANTE blanche à queue gauche (.fx-bub-in) et indicateur « en train d'écrire » (.fx-typing) dans reference/frise.html."
  request-bubble:
    look: "la demande de Colin, UNE bulle sortante WhatsApp : « Tu peux modifier le titre de mon site ? » (09:12). Elle naît près du site (séquence 1), s'épingle sur la frise au LUN 12 09:12, et on la retrouve dans le chat de l'iPhone (séquence 2) : même texte, même heure."
  tool-tiles:
    description: "Vrais logos (assets/icons/*.svg : googleforms, gmail, hubspot, stripe ; HubSpot à la place de Make, r5 Colin) dans une tuile blanche de 88 px, rayon 20 px, ombre douce, couleurs de marque (Forms #7248B9, Gmail #EA4335, Make #6D00CC, Stripe #635BFF). Liens entre tuiles en encre (pas en terracotta en v8) ; le maillon qui casse passe en pointillé avec un petit badge « ERREUR » encre. Code : reference/v6-02-attente.html (.f02-node, .f02-tile, .f02-dead, .f02-badge, .f02-links), recolorés en encre."
  video-timeline:
    look: "gabarit fx-video (1000 × 520) : une vraie timeline de montage épurée : barre « Montage » + fichier « video-lancement.mp4 » + état hachuré « EN ATTENTE DU MONTEUR » ; chutier « Rushs · 4 » avec quatre vignettes (recadrages du vrai site) ; règle 00:00 à 00:45 ; pistes V1 (clips .fx-vd-clip, vides au départ), A1 (onde .fx-vd-wave, fxWavePath), T1 ; tête de lecture terracotta .fx-vd-head (seulement quand la vidéo est montée)."
  notification:
    look: "notification iOS CLAIRE (gabarit fx-nt, 520 × 92) : fond #fffdf9 plein à 97 % (pas de backdrop-filter), rayon 24, icône de marque 48 px (Gmail #EA4335, WhatsApp #25D366, Stripe #635BFF), titre, « maintenant », corps."
  bill:
    look: "facture (gabarit fx-bill, 380 × 210) : « FACTURE », numéro, libellé, montant Space Mono 700 34, « À PAYER »."
  real-site:
    files: "assets/img/site-hero.png (avec le bouton) et assets/img/site-hero-sans-bouton.png (bouton masqué), 2850×1620 px = vue 1425×810 à 2x ; bouton « JE PRENDS RENDEZ-VOUS » boîte x 1151, y 1052, l 518, h 94 (pixels image)."
    window: "fenêtre Safari de reference/v6-05-demande.html (#f05-win, #f05-chrome, #f05-view, #f05-ring), 1128 × 692, url « entrepreneurs2-0.com »."
  claude-window:
    look: "fenêtre de l'app Claude (reference/v6-04-aujourdhui.html .f04-cw-*, reference/v6-05-demande.html .f05-cw-*), 1100 × 620 native, posée dans la colonne à l'échelle 0.62 ; tâches à cercle vide qui deviennent un disque #D97757 coché + « Fait » ; champ « Écris ta demande à Claude », bouton d'envoi rond #D97757."
  method-card:
    look: "gabarit fx-method (340 × 230) : « LA MÉTHODE », « 01 Décrire le résultat », « 02 Donner le contexte », « 03 Vérifier, puis lancer »."
  contact-chip:
    look: "gabarit fx-chip : avatar par défaut WhatsApp + « Prestataire web » + « HORS LIGNE » (Space Mono)."
  idea-pill:
    look: "pastille d'idée (.fx-idea) : carte blanche rayon 18, texte seul Instrument Sans 600 34 (« ta vidéo », « ton automatisation », « ton site », « ta landing page », « ta newsletter », « ton offre », « ta formation », « ton podcast »), jamais d'icône ; elles volent en profondeur façon Reakly."
  point:
    look: "le point de lumière : cœur .fx-pt-core 30 px (blanc chaud, bord terracotta doux) + halos .fx-pt-glow 120 et 420 px (closest-side, jamais de disque visible)."
  column:
    summary: "la colonne « AUJOURD’HUI » du monde B (2D, papier) : bande #fffdf9 de x 1540 à 2300 entre deux filets d'encre, sous l'axe de la frise ; en-tête « AUJOURD’HUI » ; rail des minutes à gauche. Section « LE MONDE B »."
  ink-box:
    look: "LA mise en valeur par défaut (boîte terracotta depuis le 2026-09-30, Colin : « des encadrés orange, pas noirs ») : rectangle #c25b28, angles nets (rayon 3 px), qui déborde de 0,14 em de chaque côté ; le texte passe en #f6f1e9. Sur le sombre : boîte #f5efe7, texte #0d0b0a. Classes .fx-ink, .fx-ink-bg, .fx-ink-tx."
    motion: "la boîte se trace de gauche à droite (scaleX 0 → 1, 0,16 s power3.out), 0 à 2 images avant le mot ; le texte change de couleur quand la boîte passe (0,1 s)."
  terracotta-stroke:
    look: "le mot-pic : un trait fin terracotta #c25b28 de 4 px, arrondi, sous le mot (classes .fx-stroke, .fx-stroke-l). Jamais un encadré plein, jamais un mot énorme."
    motion: "se dessine de gauche à droite (scaleX 0 → 1, 0,3 à 0,5 s power2.out) pendant que le mot est dit."
  end-card:
    look: "carte de fin de la marque (reference/v6-09-fin.html) : fond #0d0b0a, 34 vagues terracotta fines dans le tiers haut, halo chaud, mot-symbole « ENTREPRENEURS » + « 2.0 », « Forme-toi » + « pour de bon. » souligné d'un trait fin terracotta (pas de pastille pleine en v8), bouton « JE PRENDS RENDEZ-VOUS → » (Big Shoulders 800 34, fond #f6f1e9, texte #a84d22, halo) qui se remplit de #c25b28 au clic, url « entrepreneurs2-0.com » en Space Mono. Pas de sous-ligne."
  cursor:
    description: "flèche macOS blanche à contour sombre, ombre portée ; elle arrive d'UN seul mouvement en courbe (0,4 à 0,5 s power3.out) et clique directement : pression (échelle 0,85, 0,06 s) + onde terracotta. Jamais d'hésitation."

negative:
  - "Jamais de sous-titre en haut à gauche ; jamais plus de 64 px pour la phrase de la voix ; la zone y 890 à 980 ne porte que la phrase."
  - "Une transition = UN geste lisible en une seconde (un objet qui devient un autre, un whip, une poussée). Jamais plusieurs objets qui bougent chacun de leur côté pendant une couture."
  - "Mots clés des sous-titres : petite boîte terracotta à angles nets, texte papier (Colin, 2026-09-30). Mots-pics (géants) : élégants, trait fin terracotta ; jamais un gros encadré orange ni un mot énorme."
  - "Une demande de modif sur le site se montre comme une annotation reliée au titre sélectionné (pastille, trait de rappel, carte de message propre dans l'espace libre), jamais une bulle qui flotte ou mord sur le site (Colin, 2026-09-30)."
  - "Chaque image illustre littéralement sa phrase ; aucun symbole abstrait (pas de compteur, pas d'orbe, pas de diagramme inventé) ; aucune seconde immobile."
  - "Terracotta seulement : le trait sous « 1 000 € », le trait sous « changer. », le trait sous « correctement » (coup de pinceau terracotta effilé, r4), le point de lumière, la tête de lecture de la vidéo montée, la carte de fin. Partout ailleurs : encre et papier (et les couleurs de marque DANS les vraies interfaces)."
  - "Pas d'Inter, Space Grotesk, Geist, system-ui (sauf la police système d'iOS dans l'iPhone). Pas d'emoji. Pas d'icône dans une pastille ronde."
  - "Pas d'easing élastique ni back.out ; pas de boucle de respiration ; pas d'hésitation du curseur."
  - "Aucun texte visible hors des lignes Scene, de la frise (dates, heures, mois, années, libellés des voies écrits ici) et des vraies interfaces."
  - "Pas de maquette générique (barres grises sans contenu), pas de chat anonyme, pas de personnage clip-art, pas de dégradé violet, pas de glassmorphism."
  - "Pas de dédoublement : un même objet n'est jamais deux fois à l'écran (sauf les copies d'une traînée de mouvement)."
  - "Jamais de tiret cadratin ni demi-cadratin dans un texte visible. Typographie française : espace insécable avant « : », espace fine insécable avant « ? » et « ! », apostrophe ’, espace fine insécable dans « 1 000 »."

fabrication:
  - "BLOQUANT. Tout <template id> interne est placé À L'INTÉRIEUR de <div id=\"root\">, et son id porte le préfixe de la séquence (ex. « p04-fx-video »)."
  - "BLOQUANT. Jamais style.visibility = \"visible\" : toujours \"inherit\"."
  - "BLOQUANT. Tout élément part de opacity: 0 en CSS avant son entrée (sauf ce qui est à l'écran dès la première image de la séquence et qui doit alors correspondre au handoff_in)."
  - "BLOQUANT. immediateRender: false sur tout fromTo placé après t = 0."
  - "BLOQUANT. Transforms seulement : jamais de tween sur letterSpacing, top, left, width, height (une largeur qui change = scaleX d'un fond séparé)."
  - "BLOQUANT. Pas de backdrop-filter (couleurs pleines) ; pas de clip-path polygon interpolé (circle, ellipse et inset autorisés)."
  - "BLOQUANT. Tous les ids commencent par une lettre et portent le préfixe de la séquence (p01- à p09-)."
  - "BLOQUANT. Pas de calque 3D géant flouté : le sol est un canvas (fxDrawFloor) ; fxPlace masque tout quad dont un coin est à moins de minZ de la caméra ou dont la projection dépasse maxPx ; aucun objet flouté de plus de 1800 px de côté ; une poussée à travers un objet (zoom-through) passe le relais à une copie écran 2D avant de dépasser ×4."
  - "BLOQUANT. La zone y 890 à 980 est réservée à la phrase : aucun élément important n'y entre (les cadrages du storyboard le respectent)."
  - "BLOQUANT. Paquet de séquence sous 48 Ko : au plus 2 règles dans « rules: » ; ne jamais écrire le nom d'une autre règle dans le bloc."
  - "Une seule timeline GSAP en pause, sans transition CSS. La caméra est un objet proxy écrit par UN seul onUpdate (render) qui appelle le kit (fxUpdateRibbon, fxDrawFloor, fxStand, fxShadow, fxUpdateWait, fxApplyCam2). Jamais de getBoundingClientRect dans onUpdate ; les largeurs se mesurent une fois à l'initialisation."
  - "Une séquence n'est jamais masquée avant son début ; chaque séquence peint son propre fond sur un calque class=\"clip\" de toute sa durée, jamais sur #root. L'orchestrateur pose un sol commun #f6f1e9 sous les séquences claires (0 à 22,60 et 25,12 à 42,30)."
  - "Chemins relatifs à la racine du projet : assets/fonts/..., assets/img/..., assets/icons/... (dans la référence : ../assets/...)."
---

# Entrepreneurs 2.0 · charte v8 « La ligne du temps »

Le texte raconte une semaine, puis des années d'attente, puis un seul jour où tout se fait. Le film est une frise :
une règle fine sur un papier chaud, vue de face avec une légère perspective, que la caméra longe. Les vraies
interfaces y sont posées comme des objets sur une étagère, chacune à son jour : le vrai site le lundi, le devis le
mercredi, l'iPhone le vendredi. Tout est épuré, aéré, à la Reakly : cartes blanches aux ombres douces qui arrivent en
volant, sous-titre centré en bas, un mot clé par phrase dans une boîte d'encre. Le terracotta ne sert qu'aux moments qui
comptent. Au pivot, le noir de la marque : « Il est temps de changer. », et la frise se replie en un point de lumière.
Ce point s'ouvre sur la colonne « AUJOURD’HUI » où Claude fait tout, avec les bons outils et une méthode. Les devis
s'envolent, les attentes se rétractent, les idées volent et atterrissent le jour même ; la frise n'est plus qu'une
ligne sur laquelle s'écrit la promesse, et cette ligne devient les vagues de la carte de fin.

Toutes les durées et tous les temps sont en secondes avec un point décimal dans le storyboard (ex. 5.82) ; ce texte
utilise la virgule en prose.

## LA FRISE (au u près)

**Source unique du code** : `reference/frise.html`, entre « LIGNE v8 : début du bloc CSS à copier » et « fin du bloc
CSS », les `<template>` (fx-devis, fx-video, fx-nt, fx-bill, fx-method, fx-chip) et le « kit ligne v8 ». Chaque
séquence copie ces blocs MOT POUR MOT (seuls changements : `../assets/` devient `assets/`, et l'id du gabarit reçoit le
préfixe de la séquence). Ouvrir le fichier et appeler `demo("1@0.00")`, `demo("1@4.90")`, `demo("2@2.90")`,
`demo("4@0.00")`, `demo("4@1.46")`, `demo("4@3.14")`, `demo("4@4.56")`, `demo("4@6.00")`, `demo("5@1.20")`,
`demo("5@pivot")`, `demo("B:claude")`, `demo("B:colonne")`, `demo("B:large")`, `demo("B:devis")`, `demo("cards")`,
`demo("type")` pour voir les états de référence. Utilitaires du kit : `FX_ICON` et `fxIconSVG(nom, couleur)` (logos de
marque sans chargement), `fxWavePath()` (onde de la piste audio), `.fx-sp` (espace étroite des montants en Space Mono :
« 1 000 € » s'écrit `1<i class="fx-sp"></i>000<i class="fx-sp"></i>€`, sinon chaque espace est aussi large qu'un chiffre).

### Repère du monde A (frise des jours)

- X vers la droite = le temps ; Y vers le haut ; Z vers le fond. Unité u. Sol (points) : plan Y = 0.
- **Frise des jours** : plan Z = 0 ; LA LIGNE en Y 600 ; un jour = 1300 u ; `fxX(t) = -1400 + 1300 t`, t en jours
  depuis le DIM 11 juin 2023 à 00:00. LUN 12 de X -100 à 1200 (midi en 550), MAR 13 de 1200 à 2500, MER 14 de 2500 à
  3800 (midi 3150), JEU 15, VEN 16 de 5100 à 6400 (midi 5750), SAM 17, DIM 18, LUN 19 de 9000 à 10300 (midi 9650),
  MAR 20 (midi 10950), MER 21 (midi 12250), JEU 22, VEN 23 de 14200 à 15500.
- Un jour (`fxDaySVG`, quad 1300 × 620 u de Y 620 à Y 0) : la ligne (3 u, encre 78 %) ; graduations PENDUES sous la
  ligne : heures 22 u, 06:00, 12:00, 18:00 en 48 u avec leur heure (Space Mono 20 u), minuit en 170 u ; « LUN 12 »
  (Space Mono 700 44 u) sous la graduation de minuit ; mois (« JUIN 2023 ») dessous au premier jour montré. Voies
  d'attente (si `lanes`) : trois rails de 70 u en Y 290, 200, 110 (haut de la voie).

| Station | Pied (monde) | Base, ancre | Jour |
|---|---|---|---|
| Vrai site dans Safari | (550, 600, -4) | 0.85, (564, 692) | LUN 12 |
| Bulle de la demande | épinglée sur la ligne en (fxX(1.385) = 400, 600, -4) après son envoi | 0.9, pied de la bulle | LUN 12 09:12 |
| Devis | (3150, 600, -4), rotation -3° | 1.0, (260, 640) | MER 14 |
| iPhone 18 WhatsApp | (5750, 600, -4) | 0.72, (202, 840) | VEN 16 |
| Vrai site (la modif en attente) | (9650, 600, -4) | 0.55, (564, 692) | LUN 19 |
| Quatre tuiles | pieds en (10605 + 230 i, 600, -4), i = 0 à 3 | 1.8, (44, 88) | MAR 20 |
| Timeline de montage | (12250, 600, -4) | 0.65, (500, 520) | MER 21 |
| Puce « Prestataire web » | (14700, 600, -4) | 1.2, pied de la puce | VEN 23 |
| Barres d'attente | voie 0 de t 8.5, voie 1 de t 9.5, voie 2 de t 10.5, jusqu'à t 12.0 au plus | hauteur 70 u | sous les stations |

Chaque station a son ombre de contact (fxShadow, largeur = 90 % de sa largeur) : elle est POSÉE, pas flottante.

### Frise des années (séquence 5)

- Plan Z = 400, LA LIGNE en Y 600 (bug de la v7 corrigé : `fxUpdateRibbon` pose le haut du quad en Y 600 + 420).
  Une année = 1200 u, de juin à juin : l'année y commence en X = -1500 + (y - 2023) × 1200. L'année « 2024 » (Space
  Mono 700 300 u) est posée au-dessus de la ligne, les mois pendent dessous.

## CAMÉRA

- **3D** (monde A et années) : `cam(x, y, z, yaw, pitch, roll)` en u et degrés ; yaw > 0 regarde vers le futur (+X),
  pitch > 0 vers le haut, roll > 0 tourne l'image dans le sens horaire. Focale 1000 px au centre (960, 540). Plus
  `flou` (px) et `dof(zf, k, max)` : flou d'un objet à la profondeur z = min(max, k × |z - zf| / z). Code :
  `fxProject`, `fxPlace`, `fxStand`, `fxShadow`, `fxCoc`. Roulis faible (0 à -1°) : la v8 est calme et nette.
- **2D** (monde B, moments typographiques, carte de fin) : `cam2(x, y, s)` : le point (x, y) du monde est au centre
  du cadre à l'échelle s (`fxApplyCam2`).
- **Dérive** permanente (jamais d'arrêt), écrite en u/s, px/s ou %/s ; elle repart de 0 au sommet du flou d'un cran.
- **Cran** : 0,2 à 0,4 s `expo.inOut`, flou 0 → 8 px → 0. **Whip** : `power2.in` jusqu'au pic de flou (12 à 16 px),
  puis `expo.out` ; pendant un whip le long de la frise, flou directionnel horizontal sur les rubans (fxMbDefs).
- **Passage de relais (règle absolue)** : chaque séquence commence EXACTEMENT dans l'état où la précédente s'arrête
  (caméra, flou, objets, texte) ; ces valeurs sont écrites deux fois à l'identique (`handoff_out` de N, `handoff_in` de
  N+1). La couture tombe au sommet du flou d'un mouvement, dérive 0, et aucun élément ne naît ni ne meurt dans les
  2 images autour. Une seule coupe franche : 22.60 (noir du pivot, sur « Il » ; la musique continue sous le noir jusqu'à l'impact de 23.40).

## LE MONDE B v2 (colonne et tableau, 2D, papier ; séquences 6 et 7 ; r4 Colin 2026-09-30)

Règle de Colin : dans la colonne du jour, les TÂCHES à gauche et l'IA à droite, côte à côte (jamais l'IA en haut et les
tâches dessous) ; les voies hachurées du passé n'apparaissent jamais dans les plans de la séquence 6 (décor sans sens),
elles ne vivent que dans le tableau de la séquence 7 où elles portent « Terminé, l'attente ».

- Monde en px, caméra cam2. **Axe de la frise** en haut : ligne en y 70 de x 40 à 3520 (fxAxisSVG(40, 3520, 1540)),
  graduations de mois pendues jusqu'à x 1540, « JUIN 2023 » (x 60), « JUIN 2024 » (x 520), « JUIN 2025 » (x 980).
- **Colonne « AUJOURD’HUI »** : bande #fffdf9 de x 1540 à 3480 (1940 px) sous l'axe (à partir de y 110), filets d'encre
  à 50 % en x 1539 et 3479 ; en-tête « AUJOURD’HUI » en (1640, 80) ; rail des minutes à gauche de la bande (Space Mono
  20, aligné à droite sur x 1510) : « 09:41 » en y 200, « 09:42 » en y 420, « 09:43 » en y 690 (hors champ en séquence 6).
- **Trois lignes du jour, À GAUCHE** : cartes #fffdf9 de 700 × 90 en x 1640, y 267, 387, 507 (bloc de 267 à 597, centre
  432) ; miniature, libellé, état « EN ATTENTE » puis disque #D97757 coché et « Fait » à droite de la carte.
- **Fenêtre Claude, À DROITE** : native 1100 × 620, posée en (2420, 215) à l'échelle 0.7 (770 × 434, centre y 432) ; son
  champ de saisie (native 152, 262, 860 × 144) tombe en (2526, 398) à (3128, 499) du monde, centre (2827, 449).
- **Carte « LA MÉTHODE »** : (2960, 540), rotation 3°, échelle 1, à cheval sur le coin bas droit de la fenêtre.
- **Voies d'attente du passé** : trois barres .fx-wait de x 80 à 1520, hauteur 70, en y 590, 700, 810, libellés
  « MODIF DU SITE », « AUTOMATISATION », « VIDÉO À MONTER » (séquence 7 seulement à l'écran).
- **Devis** (gabarit fx-devis) : posé dans le passé en (260, 170), échelle 0.42, rotation -4°.
- **Code** : `fxBuildWorldB(host, idGabaritDevis)`, identique dans les séquences 6 et 7 (la couture de 32.20 tombe au pixel).
- **Cadrages de référence** : colonne du jour (tâches + IA) cam2(2398 → 2454, 465, 0.95), marges gauche et droite égales à ±40 px
  (le filet gauche de la bande en bord net, à 90 px au moins du cadre ; rail et voies cachés jusqu'au recul final) ; champ de Claude en gros plan cam2(2856, 468, 1.9) (la fenêtre tient entre y 59 et 884) ; couture 6 → 7
  cam2(1600, 480, 0.80) flou 10 px ; tableau entier cam2(1100, 480, 0.74) (la fenêtre Claude et la carte méthode s'effacent
  quand il en reste moins de 100 px dans le champ, jamais un liseré) ; devis cam2(380, 330, 1.4) ; axe seul cam2(1200, 60, 2.0) (la ligne en y 560 px).
  Tout tient au-dessus de y 880 à l'écran.

## TEXTE

- **Sous-titre** (la voix) : en bas au centre, 62 px, 45 signes au plus par morceau (une phrase plus longue se découpe en
  morceaux qui se remplacent, avec « … »), un morceau à la fois, mot par mot sur ses horodatages (temps
  LOCAUX de chaque séquence) : chaque mot arrive gris (encre 35 %, y +8, flou 6 → 0 en 0,14 s) puis passe à l'encre en
  0,2 s. Sortie avant une couture : opacité 1 → 0 et flou 0 → 6 en 0,14 s.
- **Une mise en valeur par phrase**, nommée dans le storyboard : [boîte : …] (boîte d'encre, par défaut) ou
  [trait : …] (trait fin terracotta, seulement « 1 000 € », « changer. », « correctement » (coup de pinceau terracotta effilé, r4),
  « pour de bon. ») ou une action dans le monde (rature du devis, barres qui se rétractent).
- **Règle de Colin (r4)** : jamais un filet de frise qui traverse ou coupe un moment typographique ; la ligne du raccord
  se replie dès l'arrivée et la phrase vit sur papier nu. Mise en valeur d'un pic : un coup de pinceau terracotta
  effilé (attaque arrondie, sortie fine, légère courbe montante) sous LE mot clé, pas sous toute la phrase.
- **Moments typographiques** (séquence 3, pivot de la séquence 5, séquence 8) : la phrase est l'image, centrée, 84 px,
  mot par mot ; pas de sous-titre en bas pendant ces moments.

## SON (le mix se fera sur l'image)

Le mix est VERROUILLÉ par l'orchestrateur (build-audio-v8.py) : l'image se cale sur lui, jamais l'inverse. À la Reakly :
une musique de tension de 0 à 23,40, avec une montée (riser) de 20,20 à 23,40, qui continue sous le noir du pivot et
se coupe net sur « changer. » par un impact grave (23,40), puis silence ; la musique d'élan attaque sur « Aujourd’hui »
(25,12) et s'éteint en fondu sur la carte de fin. Un micro-bruitage sur les événements d'interface (clic, pop, whoosh,
frappe) ; UNE notification à deux tons, la signature, sur la réponse du prestataire (8,80). Chaque séquence liste les
bruitages verrouillés qui tombent chez elle, en temps locaux : l'événement visuel correspondant tombe sur la même image.
