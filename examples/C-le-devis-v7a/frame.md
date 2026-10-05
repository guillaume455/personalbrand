---
version: 3
name: "Entrepreneurs 2.0 · Launch Frame v7a · Le devis est le décor"
description: >
  Charte du film v7a (43,2 s, 1920×1080, 30 i/s). Un seul lieu : un vrai devis d'agence web, posé sur la scène
  sombre et éclairé par une flaque de lumière chaude pendant la douleur (aller), le même devis en plein jour pendant
  la solution (retour). Une caméra 3D le parcourt de très près, avec un flou de profondeur à trois couches. Les vraies
  interfaces de la v6 (iPhone 18 et WhatsApp iOS 2026, écran verrouillé, fenêtre Claude, vrai site dans Safari,
  tuiles d'outils) sortent du devis comme des objets debout. Un seul accent, le terracotta. Images de style de
  référence : styleframes/A1.png (2,9 s), A2.png (9,8 s), A3.png (25,4 s).
unit: 1920×1080
principle: "un lieu, une caméra qui s'y déplace, un événement toutes les 0,5 s, chaque couture invisible"
reference: "reference/devis-decor.html (code exécutable du devis-décor et du kit caméra, source unique du code) ; reference/v6-*.html (vraies interfaces de la v6)"

colors:
  canvas: "#0d0b0a"            # scène sombre (aller, carte de fin)
  canvas-2: "#141010"
  paper: "#f6f1e9"             # papier de la v6 (flash de lumière, bouton de fin)
  ground-day: "#efe7dc"        # sol du monde clair (retour), sous la feuille
  sheet-dark: "#f6f1e8"        # la feuille du devis à l'aller (papier éclairé)
  sheet-day: "#fffdf9"         # la même feuille au retour (plein jour)
  ink: "#f5efe7"               # texte sur fond sombre
  ink-soft: "#cdbfb2"
  ink-mute: "#9b9289"
  ink-dark: "#1a1612"          # encre du devis, texte sur fond clair
  ink-dark-soft: "#5a5348"
  sheet-grey: "#7a7064"        # sous-lignes et micro-libellés du devis
  sheet-num: "#8a8074"         # numéros de ligne
  sheet-rule: "#d9cfc1"        # filets entre lignes
  hairline-light: "#e2d9cc"
  accent: "#c25b28"            # LE seul accent : pastilles, barres, tampon, cadre de la ligne 5, anneau du zéro
  accent-light: "#d4703f"
  accent-deep: "#a84d22"
  accent-glow: "#e08a5c"

fonts:
  Instrument Sans: { files: ["assets/fonts/InstrumentSans-400.woff2 (400)", "assets/fonts/InstrumentSans-500.woff2 (500)", "assets/fonts/InstrumentSans-600.woff2 (600)", "assets/fonts/InstrumentSans-700.woff2 (700)"] }
  Space Mono: { files: ["assets/fonts/SpaceMono-400.woff2 (400)", "assets/fonts/SpaceMono-700.woff2 (700)"] }
  Big Shoulders: { files: ["assets/fonts/BigShoulders-800.woff2 (800)"] }

typography:
  phrase:        { fontFamily: "Instrument Sans", px: 54, weight: 600, lineHeight: 1.18, tracking: "-0.02em", note: "la phrase de la voix, petite, mot par mot ; aller : #f5efe7 en haut à gauche (x 118, y 92) ; retour : #1a1612 en bas à gauche (x 118, y 928)" }
  giant:         { fontFamily: "Instrument Sans", px: 260, weight: 700, lineHeight: 0.9, tracking: "-0.05em", note: "seulement « Stop. », « aujourd’hui, », « TOI. » ; arrive de la caméra, passe devant ou derrière un objet" }
  giant-pill:    { fontFamily: "Instrument Sans", px: 260, weight: 700, note: "une seule fois : « libre. »" }
  dv-title:      { fontFamily: "Instrument Sans", px: 150, weight: 700, lineHeight: 0.9, tracking: "-0.045em", note: "« Devis » dans la feuille (unités u)" }
  dv-label:      { fontFamily: "Instrument Sans", px: 52, weight: 600, lineHeight: 1.15, tracking: "-0.02em", note: "désignation d'une ligne (u)" }
  dv-sub:        { fontFamily: "Instrument Sans", px: 25, weight: 400, lineHeight: 1.2, color: "#7a7064" }
  dv-price:      { fontFamily: "Space Mono", px: 46, weight: 700, note: "prix dans la cellule (u) ; « quand il aura le temps » et « maintenant » en 34" }
  dv-qty:        { fontFamily: "Space Mono", px: 30, weight: 400, color: "#3a332b" }
  dv-micro:      { fontFamily: "Space Mono", px: 19, weight: 400, tracking: "0.16em", upper: true, color: "#5a5348" }
  dv-total:      { fontFamily: "Space Mono", px: 72, weight: 700, note: "valeur de la case TOTAL (u)" }
  ui:            { fontFamily: "Instrument Sans", px: 28, weight: 500, lineHeight: 1.3 }
  micro:         { fontFamily: "Space Mono", px: 18, weight: 400, tracking: "0.2em", upper: true }
  wordmark:      { fontFamily: "Big Shoulders", px: 120, weight: 800, upper: true, note: "« ENTREPRENEURS » en #f5efe7 et « 2.0 » en #d4703f (couleur de marque, exception unique)" }
  cta:           { fontFamily: "Big Shoulders", px: 34, weight: 800, upper: true }

components:
  devis-decor:
    summary: "LE composant central. Une feuille A4 de 1500 × 2120 u (1 u = 1 px CSS de la feuille à l'échelle 1), rendue en 3D sous la caméra, en trois copies identiques pour le flou de profondeur. Coordonnées, états et code : section « LE DEVIS-DÉCOR » plus bas, code source unique dans reference/devis-decor.html."
  camera:
    summary: "État cam(x, y, s, rx, rz) + flou + dof(f, b1, b2). Dérive permanente, crans datés, plongées. Chaque séquence commence exactement dans l'état où la précédente s'arrête. Section « CAMÉRA »."
  billboard:
    summary: "Objet debout (iPhone, tuiles, fenêtre Claude, fenêtre Safari) ancré à un point (u, v) de la feuille : il suit la projection de ce point et son échelle apparente, mais reste face caméra. Fonction dvBillboard."
  ground-dark:
    look: "#0d0b0a plein cadre + halo terracotta en haut à droite (classe .dv-ground-dark) ; grain 6 % au-dessus de tout"
  ground-light:
    look: "#efe7dc plein cadre (classe .dv-ground-day) ; la feuille en #fffdf9 ; vignette claire .lt-day ; grain 3 %"
  lighting-dark:
    look: "trois calques écran au-dessus de la scène : .lt-pool (flaque de lumière chaude centrée (960, 640), bords en brun presque noir), .lt-corner (coin sombre en haut à gauche, sous la phrase), .lt-warm (voile terracotta en lumière douce). Aucun gris boueux : les chutes vont vers rgba(14,8,5,.93)."
  lighting-day:
    look: ".lt-day (vignette crème + halo terracotta 10 %) ; .lt-fgsheet (coin de feuille flou au premier plan en bas à gauche, sous la phrase du retour)"
  word-by-word:
    rule: "Chaque mot apparaît SUR son horodatage : fromTo {opacity:0, y:10, filter:blur(8px)} vers {opacity:1, y:0, blur(0)} en 0,2 s power3.out (toute apparition dure 0,2 s au plus). Jamais la phrase entière d'un coup. Avant une couture, la phrase sort : flou 0 à 8 px + opacité 1 à 0 en 0,14 s power2.in."
  accent-pill:
    look: "rectangle plein #c25b28, rayon 12 px, padding 0.06em 0.32em, texte blanc"
    motion: "la pastille se trace d'abord (scaleX 0 à 1 depuis la gauche en 0,2 s power3.out, rotation -8° à 0 dans le même temps), puis les lettres s'écrivent dedans (x -8 à 0, opacité, 0,12 s par lettre, décalage 0,02 s). Départ 0 à 2 images avant le mot."
    rule: "UNE pastille par phrase, sur le mot nommé par le storyboard. Au retour, la pastille de « Toi » vit dans la cellule prix (pastille « toi » du devis)."
  giant-pill:
    look: "la pastille à taille géante : rayon 28 px, padding 0.04em 0.26em, texte 260 px 700 blanc #fffdf9"
    motion: "trace depuis la gauche (scaleX 0 à 1, 0,2 s power3.out) avec rotation -6° à 0, puis lettres qui se posent avec le resserrement par lettre (0,2 s)"
  giant-word:
    motion: "arrive de la caméra (×2 à ×2,4, flou 12 à 20 px, traînée de 6 copies à 3 à 16 % d'opacité le long du trajet), se pose en 0,1 à 0,2 s expo.out, puis continue de reculer (×1 à ×0,97 sur la tenue). Resserrement : lettres en inline-block, x de chaque lettre de (i - (n-1)/2) × 0.4em à 0. JAMAIS de tween sur letterSpacing."
  echo-stack:
    look: "le mot net au centre + 4 copies au-dessus et en dessous à 60/35/20/10 % d'opacité, légèrement floues"
    motion: "les copies partent à ±180 px et convergent à ±70 px en 0,2 s power3.out pendant que le mot central se pose, puis dérivent de ±70 à ±62 px sur la tenue"
  price-drop (signature 1):
    summary: "Un prix (ou le tampon, ou « TOI. ») arrive de la caméra trop grand et flou, avec traînée, et se pose dans sa cellule de prix. Recette chiffrée : section « SIGNATURES »."
  cell-portal (signature 2):
    summary: "Un mot ou une cellule du devis s'ouvre sur son monde : soit la caméra plonge dedans (site, ligne 5, zéro), soit le monde en sort debout (tuiles, iPhone). Recette : section « SIGNATURES »."
  stamp:
    look: "vrai tampon encreur sur le papier : « SUR DEVIS », Big Shoulders 800 84 u, #c25b28, bordure 6 u, rayon 14 u, rotation -8°, mix-blend-mode multiply, masque de grain (encre irrégulière). Centre (960, 1085) u, dans la ligne 3, à cheval entre la fin du libellé et la colonne prix."
  tool-tiles:
    description: "Vrais logos (assets/icons/*.svg, Simple Icons CC0 : googleforms, gmail, make, stripe) dans une tuile blanche de 88 px, rayon 20 px, ombre douce, remplis de leur couleur de marque : Google Forms #7248B9, Gmail #EA4335, Make #6D00CC, Stripe #635BFF. Couleurs de marque autorisées uniquement dans les tuiles et les interfaces. Code : reference/v6-02-attente.html (classes .f02-node, .f02-tile, .f02-dead, .f02-badge, .f02-links)."
  real-site:
    files: "assets/img/site-hero.png (avec le bouton) et assets/img/site-hero-sans-bouton.png (même capture, bouton masqué), 2850×1620 px = vue 1425×810 à 2x. En pixels image : titre « ARRÊTE DE PRENDRE DU RETARD AVEC L'IA. » boîte x 402, y 538, l 2048, h 320 ; bouton « JE PRENDS RENDEZ-VOUS » boîte x 1151, y 1052, l 518, h 94."
    window: "vraie fenêtre de navigateur : chrome sombre #1f1d1b, 3 pastilles (#ff5f57, #febc2e, #28c840), champ d'adresse #2c2a28 avec l'url « entrepreneurs2-0.com » en Space Mono et un petit cadenas SVG, rayon 14 px, ombre 0 40px 120px rgba(0,0,0,.6). Code : reference/v6-05-demande.html (#f05-site, #f05-win, #f05-chrome, #f05-view, #f05-ring, #f05-tag)."
  whatsapp-chat:
    look: "WhatsApp iOS actuel (refonte 2026, mode clair), épuré : fond #f4f1ec, pas de barre d'en-tête, capsules de verre #fdfcf7, « Prestataire web » + « vu aujourd’hui à 09:12 », pastilles de date blanches, bulles sortantes #e0fcd6 rayon 20 px, doubles coches grises puis BLEUES #3479f3, champ de saisie en capsule. L'ancien WhatsApp sombre est INTERDIT. Code : reference/v6-02-attente.html (station B, classes .f02-phone à .f02-home)."
  iphone-18:
    look: "iPhone 18 Pro de face, cadre titane à bords plats (dégradé 150°), bordure noire très fine, Dynamic Island petite, boutons latéraux ; appareil entier visible. 404×840 px à l'échelle 1. Code : reference/v6-02-attente.html."
  ios-lockscreen:
    look: "le même iPhone ; fond d'écran brun chaud avec lueur terracotta floue ; ligne de date « lundi 12 juin 2023 » (blanc 70 %, 30 px 600) au-dessus de l'heure « 09:41 » (blanc 92 %, 150 px) ; notifications iOS : carte rgba(60,52,48,.82) PLEINE (pas de backdrop-filter), rayon 26 px, icône 44 px (Gmail #EA4335, WhatsApp #25D366, Stripe #635BFF, Calendrier #4285F4, logo blanc depuis assets/icons), nom de l'app, « maintenant », titre et corps. Les nouvelles arrivent en haut, les anciennes se tassent en pile. Code : reference/v6-03-prix.html (classes .f03-phone à .f03-nt-b)."
  claude-window:
    look: "fenêtre de l'app Claude, claire : fond #faf9f5, bordure 1 px #e8e4da, rayon 16 px, ombre 0 30px 80px rgba(60,40,20,.18) ; barre avec le logo Claude (assets/icons/claude.svg, #D97757) et « Claude » ; conversation ; carte de saisie blanche « Écris ta demande à Claude » avec bouton d'envoi rond #D97757. Tâche : cercle vide qui devient un disque #D97757 coché, libellé 30 px, étiquette « Fait ». Taille native 1040×600. Code : reference/v6-04-aujourdhui.html et reference/v6-05-demande.html (classes .f04-cw-*, .f05-cw-*)."
  request-bubble:
    look: "la demande de l'utilisateur, UNE seule bulle : carte #fffdf9, rayon 22 px, ombre 0 24px 60px rgba(60,40,20,.18), largeur 720 px, texte Instrument Sans 500 34 px #1a1612, curseur de frappe #D97757. Texte : « Ajoute un bouton « Je prends rendez-vous » sous mon titre. »"
  years-frieze:
    look: "frise du temps sur la scène sombre (emprunt à la direction C) : un filet horizontal 2 px rgba(245,239,231,.28) à y 820, des graduations fines tous les 60 px et une haute à chaque année, les années « 2023 », « 2024 », « 2025 » en Instrument Sans 700 360 px, #f5efe7 à 12 %, espacées de 1400 px. Pendant le panoramique filé : flou directionnel horizontal (filtre SVG feGaussianBlur stdDeviation « 28 0 », animé par attribut)."
  cursor:
    description: "flèche macOS blanche, contour sombre, ombre portée ; clic = pression (échelle 0,85) + onde terracotta qui s'étend et s'efface"
  zero-portal:
    look: "le zéro de la case TOTAL est un anneau SVG, jamais le glyphe (le « 0 » de Space Mono a un point central) : ellipse extérieure rx 18,6 ry 26,2, trou rx 10 ry 17,5, centrées EXACTEMENT en (1235, 1812) u (fill-rule evenodd, classe .dv-zero-ring). Pour la plongée, un SVG écran de 1920×1080 reprend la même géométrie projetée (section SIGNATURES)."
  end-card:
    look: "scène sombre #0d0b0a, texture de 34 vagues terracotta fines sur le tiers haut, halo chaud ; mot-symbole « ENTREPRENEURS » + « 2.0 » ; « Forme-toi » + pastille « pour de bon. » ; sous-ligne « Pensé pour ceux qui ne sont pas techniques. » (#cdbfb2) ; bouton « JE PRENDS RENDEZ-VOUS → » (Big Shoulders 800 34 px, fond #f6f1e9, texte #a84d22, halo terracotta) qui se remplit de #c25b28 au clic ; url « entrepreneurs2-0.com » en Space Mono. Code : reference/v6-09-fin.html (fond, vagues, mot-symbole, bouton, curseur)."

negative:
  - "Pas de deuxième mécanisme de mise en valeur : la pastille terracotta est la SEULE façon de souligner un mot (pas de texte coloré, pas de texte lumineux)."
  - "Pas de grande phrase : les phrases sont à la taille « phrase » ; seuls les pics nommés passent en « giant »."
  - "Aucune teinte hors terracotta, sauf les couleurs de marque DANS les interfaces réelles et les tuiles, et le « 2.0 » du mot-symbole."
  - "Pas d'Inter, Space Grotesk, Geist, system-ui (sauf la police système d'iOS DANS l'écran de l'iPhone). Pas d'emoji. Pas d'icône dans une pastille ronde."
  - "Pas d'easing élastique ni back.out ; pas de boucle de respiration ; pas d'image figée : chaque tenue a une couche vivante nommée."
  - "Aucun texte visible qui ne soit pas dans les lignes Scene du storyboard (le texte des interfaces réelles, de la capture du site et du devis est autorisé)."
  - "Pas de maquette générique (barres grises), pas de chat anonyme, pas de personnage clip-art, pas d'orbe 3D brillante."
  - "Pas de dédoublement : un même objet n'est jamais deux fois à l'écran (sauf les trois couches du devis, qui sont UNE feuille, et les copies de traînée, qui sont un seul objet en mouvement)."
  - "Jamais de tiret cadratin ni demi-cadratin dans un texte visible. Typographie française : espace insécable avant « : », espace fine insécable avant « ? » et « ! », apostrophe ’."

fabrication:
  - "Tout élément part de opacity: 0 en CSS avant son entrée (sauf ce qui est à l'écran dès la première image de la séquence, et qui doit alors correspondre au handoff_in)."
  - "immediateRender: false sur tout fromTo placé après t = 0."
  - "Jamais d'animation de letterSpacing ; jamais de clip-path polygon interpolé (clip-path circle et ellipse autorisés) ; pas de backdrop-filter (couleurs pleines à la place)."
  - "Une séquence n'est jamais masquée avant son début ; chaque séquence peint son propre fond sur un calque class=\"clip\" de toute sa durée, jamais sur #root. L'orchestrateur pose en plus un sol commun #efe7dc sous les séquences claires (14,40 à 36,68)."
  - "Une seule timeline GSAP en pause, sans transition CSS. La caméra est un objet proxy écrit par UN seul onUpdate (dvApplyCam, dvApplyDof, dvBillboard). Jamais de getBoundingClientRect dans onUpdate : la projection se calcule avec dvProject (mathématique pure)."
  - "Dans la feuille, aucun id : tout se vise par classe (les trois copies bougent ensemble)."
  - "Chemins relatifs à la racine du projet : assets/fonts/..., assets/img/..., assets/icons/..."
---

# Entrepreneurs 2.0 · charte v7a « Le devis est le décor »

Le film ne change pas d'écran : il parcourt un lieu. Ce lieu est un vrai devis d'agence web, n° 0147, émis par un
prestataire fictif, Studio Cadran. Pendant la douleur (0 à 14,02 s), la feuille est posée sur la scène sombre et
éclairée par une flaque de lumière chaude : la caméra la descend ligne par ligne et chaque ligne s'ouvre sur son monde
(le vrai site, les tuiles qui cassent, le WhatsApp sans réponse). « Pendant des années » l'aspire en notification sur
un écran verrouillé. « Stop. » coupe tout. Au retour (14,30 à 36,68 s), c'est le même devis en plein jour : Claude
coche les tâches, la demande traverse l'écran, puis chaque « TOI. » tombe dans une cellule prix et barre sa ligne. Il
ne reste qu'une ligne ; le devis s'envole ; le total tombe à zéro et l'on plonge par le trou de ce zéro jusqu'à la
carte de fin, sur la scène sombre.

Toutes les durées et tous les temps sont en secondes avec un point décimal dans le storyboard (ex. 5.82) ; ce texte
utilise la virgule quand il parle en prose.

## LE DEVIS-DÉCOR (au pixel)

**Source unique du code** : `reference/devis-decor.html`, entre les marqueurs « DEVIS-DÉCOR v7a : début du bloc à
copier » et « fin du bloc CSS » (le CSS), le `<template id="dv-sheet">` (le gabarit) et le « kit caméra v7a » (le JS).
Chaque séquence qui montre le devis copie ces trois blocs MOT POUR MOT (seul changement autorisé : `../assets/` devient
`assets/`). Ouvrir le fichier et appeler `demo({...})` dans la console pour voir n'importe quel état.

### La feuille

Feuille A4 de **1500 × 2120 u**, origine en haut à gauche, x vers la droite, y vers le bas. Marges 120 u. Papier
`#f6f1e8` à l'aller (ombre portée sombre), `#fffdf9` au retour (classe `day` sur `.dv`), grain de papier en
multiplication.

| Élément | Boîte en u (x1 à x2, y1 à y2) | Contenu |
|---|---|---|
| Marque | 120 à 482, 136 à 206 | carré 70 u + « Studio Cadran » (700 40) + « AGENCE WEB · NANTES » (mono 19) |
| Titre | 1021 à 1380, 104 à 239 | « Devis » 150 u 700, puis « N° 0147 » mono 30 700 dessous |
| Méta | 120 à 1380, 372 à 452 | « Émis le · 12 juin 2023 », « Valable jusqu’au · 12 juillet 2023 », « Client · Ton entreprise » |
| En-tête du tableau | 120 à 1380, 540 à 610 | « N° », « DÉSIGNATION », « QTÉ », « PRIX HT » ; filet noir 3 u en bas |
| Colonnes | N° 120 à 230 ; désignation 230 à 910 ; qté 910 à 1100 (alignée à droite) ; prix 1100 à 1380 (alignée à droite) | |
| Ligne n (n = 1 à 5) | 120 à 1380, T(n) à T(n) + 190, avec T = 610, 800, 990, 1180, 1370 | filet 1,5 u `#d9cfc1` en bas (pas pour la ligne 5) |
| Libellé de la ligne n | x 230, y T + 44 à T + 104 (52 u, 600) | ligne 1 : 230 à 793 ; 2 : 230 à 563 ; 3 : 230 à 803 ; 4 : 230 à 623 ; 5 : 230 à 760 |
| Sous-ligne | x 230, y T + 116 à T + 146 (25 u, `#7a7064`) | |
| Numéro | x 120, haut T + 58 (mono 24) | « 01 » à « 05 » |
| Quantité | droite 1100, centre y T + 95 (mono 30) | ligne 1 : « 1 jour » (990 à 1100) ; ligne 2 : « 1 » ; lignes 3 à 5 : vide |
| **Cellule prix n** | **1100 à 1380, T + 55 à T + 135 ; centre (1240, T + 95)** | ligne 1 (1240, 705) ; 2 (1240, 895) ; 3 (1240, 1085) ; 4 (1240, 1275) |
| Mot « site » (ligne 1) | 708 à 793, 652 à 715 ; centre (750, 684) | portail : fenêtre 212 × 132 u en (700, 618) |
| Tampon « SUR DEVIS » | centre (960, 1085), environ 430 × 110 u, rotation -8° | ligne 3 |
| **Ligne vide finale (ligne 5)** | cadre terracotta 3 u, rayon 14 : 106 à 1394, 1384 à 1546 ; libellé « Apprendre à t’en servir » 230 à 760, 1414 à 1474 | sous-ligne « La seule ligne qui reste » |
| Signature | 120 à 640, 1600 à 1840 | « BON POUR ACCORD / DATE ET SIGNATURE » |
| Totaux | 740 à 1380, 1600 à 1716 | « Total HT · 1 600 € », « TVA 20 % · 320 € » (mono 26) |
| **Case TOTAL** | **740 à 1380, 1740 à 1880, bordure 3 u `#1a1612`, rayon 10 u** | « TOTAL TTC » (mono 22) à gauche ; valeur « 1 920 € » (mono 700 72, alignée à droite sur 1345, 44 u par caractère : « 0 » final de 1213 à 1257) |
| Zéro-portail | anneau centré (1235, 1812) : extérieur rx 18,6 ry 26,2 ; trou rx 10 ry 17,5 | remplace le « 0 » final |
| Pied | 120 à 1380, 1990 à 2040 | « Studio Cadran · 4 quai de la Fosse, 44000 Nantes » et « Page 1/1 » |

Toutes les sommes utilisent une espace insécable entre milliers et avant « € » (`1&nbsp;000&nbsp;€`), la case TOTAL
aussi (chasse fixe, donc le « 0 » final reste exactement à la place du « 0 » de « 920 »).

### Les états du devis

Chaque séquence déclare l'état du devis à son début et à sa fin. Un état dit ce qui est visible (opacité 1) ; tout
le reste de la feuille est toujours visible, sauf la ligne 5 et les éléments listés.

| État | Monde | Visible en plus de la feuille de base |
|---|---|---|
| D0 | aller | cellules prix vides, pas de tampon, cellule 4 vide, ligne 5 absente, portail fermé |
| D1 | aller | + « 1 000 € » dans la cellule 1 |
| D2 | aller | + « 600 € » dans la cellule 2 |
| D3 | aller | + tampon « SUR DEVIS » sur la ligne 3 |
| D4 | aller | cellule 4 vide : elle est devenue l'iPhone (objet debout ancré au centre de la cellule 4) |
| J0 | retour | « 1 000 € », « 600 € », tampon, « quand il aura le temps » dans la cellule 4 |
| J1, J2, J3 | retour | ligne 1 (puis 2, puis 3) barrée : barre terracotta pleine, libellé, sous-ligne et quantité à 42 %, prix remplacé par la pastille « toi » ; en J3 le tampon a disparu |
| J4 | retour | + « maintenant » à la place de « quand il aura le temps » |
| J5 | retour | + cadre terracotta de la ligne 5 et numéro « 05 » (libellé encore invisible) |
| J6 | retour | + « Apprendre à t’en servir » écrit, avec la pastille sur « t’en servir » |
| J7 | retour | totaux HT et TVA à « 0 € » ; case TOTAL : « TOTAL TTC » et « € » effacés, zéro-portail en anneau terracotta |

### Les trois couches (flou de profondeur)

La feuille existe en trois copies identiques dans `.dv-rig` (fonction `dvBuild`) : **lointaine** (flou b2, sans
masque), **moyenne** (flou b1, masquée sur f ± 250 u avec fondu jusqu'à ± 420 u) et **nette** (sans flou, masquée sur
f ± 85 u avec fondu jusqu'à ± 160 u), f étant l'ordonnée (en u) de la ligne nette. Les masques sont en coordonnées de
la feuille : l'inclinaison de la caméra transforme cette bande en profondeur de champ réelle (le haut de la feuille,
lointain, et le bas, proche, sont flous). Aller : `dof(f, 5.5, 15)` ; retour : `dof(f, 3.2, 14)` ; plans larges :
`dof(f, 1.5, 5)`. Un changement de ligne nette (bascule de netteté) est un tween de f sur la même fenêtre que le cran.

Tout ce qui s'anime DANS la feuille s'anime sur les trois copies à la fois (sélecteur de classe).

### L'éclairage

- **Aller (dans le noir)** : sol `.dv-ground-dark`, feuille `#f6f1e8`, puis au-dessus de la scène trois calques écran :
  `.lt-pool` (flaque de lumière centrée (960, 640), 1250 × 620), `.lt-corner` (coin sombre en haut à gauche qui porte
  la phrase), `.lt-warm` (voile terracotta). Grain 6 %. Référence : styleframes/A1.png et A2.png.
- **Retour (plein jour)** : sol `.dv-ground-day`, feuille `#fffdf9`, `.lt-day` (vignette crème), `.lt-fgsheet` (coin
  de feuille flou au premier plan en bas à gauche, sous la phrase). Grain 3 %. Référence : styleframes/A3.png.

### Ordre des calques d'une séquence

```
#root
  .clip  sol (.dv-ground-dark ou .dv-ground-day), toute la durée
  .clip  monde : .dv-blur > [ .dv-stage > .dv-flight > .dv-rig > .dv-layer ×3 ] + objets debout (billboards)
  .clip  lumière (.lt-*) puis objets écran (prix en vol, géants, phrase)
  .clip  grain
```
Le flou de caméra s'applique à `.dv-blur` (feuille ET objets debout) ; la phrase et les géants ont leur propre flou.

## CAMÉRA

### Repère et état

- **Repère du monde** : les unités u de la feuille (section précédente). La scène fait 1920 × 1080 px ; perspective
  2300 px, origine au centre du cadre (960, 540).
- **État caméra** : `cam(x, y, s, rx, rz)` : le point (x, y) de la feuille est au centre du cadre ; s = échelle ;
  rx = inclinaison en degrés (bord haut de la feuille qui s'éloigne) ; rz = roulis en degrés (négatif à l'aller,
  positif au retour : le retour est le miroir de l'aller). Plus `flou` (px, flou de caméra sur `.dv-blur`) et
  `dof(f, b1, b2)`.
- **Écriture dans le storyboard** : « cam(800, 590, 1.48, 30, -4) flou 0 dof(705, 5.5, 15) ». Un point de la feuille
  s'écrit (u, v). Une position écran s'écrit en px.
- **Code** (identique dans reference/devis-decor.html) :

```js
var DV_P = 2300;
function dvMatrix(c) { return new DOMMatrix().translate(960, 540).rotateAxisAngle(0, 0, 1, c.rz).rotateAxisAngle(1, 0, 0, c.rx).scale(c.s, c.s, 1).translate(-c.x, -c.y); }
function dvProject(c, u, v) { var p = dvMatrix(c).transformPoint(new DOMPoint(u, v, 0, 1)); var k = DV_P / (DV_P - p.z); return { x: 960 + (p.x - 960) * k, y: 540 + (p.y - 540) * k, k: k * c.s }; }
function dvApplyCam(rig, blurEl, c) {
  rig.style.transformOrigin = c.x + "px " + c.y + "px";
  rig.style.transform = "translate(" + (960 - c.x) + "px," + (540 - c.y) + "px) rotateZ(" + c.rz + "deg) rotateX(" + c.rx + "deg) scale(" + c.s + ")";
  blurEl.style.filter = c.blur > 0.05 ? "blur(" + c.blur.toFixed(2) + "px)" : "none";
}
// dvApplyDof(layers, {f, b1, b2}), dvBillboard(el, cam, u, v, base, ax, ay), dvBuild(rig, day) : voir reference/devis-decor.html
```

La projection a été vérifiée contre le DOM : écart de 1 px au plus.

### Dérive, crans, plongées

- **Dérive** (jamais d'arrêt) : chaque plan déclare une dérive linéaire additive, en u/s pour x et y et en %/s pour s
  (ex. « dérive x +20 u/s, s +2 %/s »), d'au moins 1 s. Elle s'additionne à l'état visé par les crans (`CAM_DRIFT`) et
  repart de 0 au sommet du flou d'un cran qui change de ligne ou de sujet (le saut est masqué par le flou) ; un cran
  latéral ou une poussée sur le même sujet s'ajoute à la dérive sans la remettre à zéro.
- **Cran** : tween de l'état vers un nouvel état absolu, 0,10 à 0,36 s, `expo.inOut` (dans la zone 0,3 à 0,9 s, seules les
  courbes expo, power3 et power4 sont permises), avec une enveloppe de flou
  0 → pic → 0 (pic de 8 à 12 px au milieu du trajet). La ligne nette f suit dans la même fenêtre.
- **Plongée** (signature 2) : tween `power3.in` vers un état très serré, à plat (rx 0, rz 0), flou 0 → 14 px ; au
  sommet du flou, un calque écran prend le relais (fondu 0,06 s) et se pose en `expo.out` 0,18 s depuis ×1,12 flou
  14 px. Sortie de plongée : l'inverse.
- **Objets debout** : `dvBillboard(el, cam, u, v, base, ax, ay)` place l'objet pour que son point d'ancrage (ax, ay)
  tombe sur la projection de (u, v), avec l'échelle `base × k`. Bases : iPhone 0.57 (ancre = centre de la cellule 4,
  point d'ancrage = centre de l'appareil 202, 420) ; tuiles 0.93 (ancre = pied de la tuile) ; fenêtre Claude 1.61
  (ancre (1180, 900), point d'ancrage = centre 520, 300) ; fenêtre Safari même ancre, base 1.50.

### Passage de relais (règle absolue)

1. **Chaque séquence commence EXACTEMENT dans l'état où la précédente s'arrête** : même `cam(...)`, même flou, même
   `dof(...)`, même état du devis, mêmes objets debout (ancre, base, contenu), même éclairage, même phrase visible (en
   pratique : aucune). Ces valeurs sont écrites deux fois dans le storyboard, en `handoff_out` de la séquence N et en
   `handoff_in` de la séquence N+1, à l'identique.
2. **La couture tombe au sommet du flou d'un mouvement de caméra** (cran, recul, whip) : la séquence N accélère vers
   l'état de couture (`power2.in`, flou qui monte), la séquence N+1 repart de cet état exact et décélère (`expo.out`,
   flou qui descend). Même direction, même vitesse au point de couture : la coupe est invisible.
3. **La dérive vaut 0 à la couture**, et aucun élément ne naît ni ne meurt dans les 2 images qui entourent la couture.
4. Exceptions écrites : 14.02 (coupe franche « Stop. », voulue) et 36.68 (sortie du zéro sur un cadre noir uni).

## SIGNATURES

### Signature 1 : le prix qui tombe dans sa case

- Un objet écran (le texte exact qui va se poser) part de la caméra : échelle ×4,4 de sa taille finale à l'écran
  (taille finale = taille dans la feuille × k de la cellule), flou 22 px, décalé de (-370, -300) px par rapport au
  point de contact (vers un bord du cadre), avec 7 copies de traînée le long du trajet (échelles décroissantes,
  opacité 3 à 18 %, flou 3 à 17 px). Il se pose en 0,2 s `expo.out` sur la projection du centre de la cellule. Son image devance le mot : l'ombre paraît dans la cellule 0,15 à 0,3 s avant.
- Pendant l'approche, l'ombre du prix grandit dans la cellule (copie floue 9 px, opacité 0 à 0,3).
- **Contact** : dans la même image, l'objet écran disparaît et le texte de la cellule (trois copies) apparaît ;
  petit coup de caméra (s ×1,01 aller-retour en 0,06 s). Bruitage calé sur l'arrivée.
- Variante « TOI. » (retour) : le géant « TOI. » (260 px) arrive du coin bas droit (×2, flou 20 px, 6 copies), touche
  la cellule en 0,2 s, reste GÉANT 0,28 s pendant que la barre trace la ligne (0,2 s `power3.out`), puis se comprime en 0,12 s
  (`power2.in`) dans la pastille « toi » de la cellule (la pastille se trace sous lui, les lettres passent de
  « TOI. » à « toi » par fondu croisé).
- Variante tampon : « SUR DEVIS » arrive à ×2,3 flou 16 px et s'écrase en 0,12 s `power4.out`, secousse de caméra
  décroissante 0,26 s (12 px, 7 px).

### Signature 2 : la case qui s'ouvre sur son monde

- Ouverture : la cellule (ou le mot) fait apparaître son monde dans sa propre boîte (échelle 0,4 à 1 en 0,12 s
  `expo.out`, halo terracotta 0 70px 6px rgba(194,91,40,.35)).
- Puis soit la **caméra plonge** (mot « site », ligne 5, zéro), soit **le monde sort debout** (tuiles de la ligne 3,
  iPhone de la cellule 4) : morph en deux temps, contraction rapide (0,05 s `power2.in`) puis expansion lente
  (0,2 s `expo.out`).
- Zéro-portail (fin) : quand la caméra est à plat sur le zéro, cam(1235, 1812, 12, 0, 0), un SVG écran de
  1920 × 1080 prend le relais dans la même image : papier #fffdf9 partout sauf l'anneau (extérieur rx 223,2 ry 314,4
  px, trou rx 120 ry 210 px, centre (960, 540)) et le trou transparent, qui laisse voir le sol de la carte de fin
  (#0d0b0a). On anime ensuite les rayons de ces ellipses (×10, 0,6 s `power3.in`) au lieu de grossir la feuille.

## TEXTE

- Phrase : aller en haut à gauche (x 118, y 92, #f5efe7, sur `.lt-corner`) ; retour en bas à gauche (x 118, y 928,
  #1a1612, sur `.lt-fgsheet`). Une phrase sort avant chaque couture.
- Géants : « Stop. » (écho), « aujourd’hui, » (derrière la fenêtre Claude), « TOI. » (devant le devis, sur la ligne
  qu'il barre). Pastille géante : « libre. » une seule fois.
- Registres : un mouvement chacun. Petit mot à mot : flou vers net. Géant : arrive de la caméra et se pose. Pastille :
  se trace puis s'écrit.
