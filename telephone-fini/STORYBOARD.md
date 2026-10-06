---
format: 1080x1920
duration: "58.23s"
message: "Depuis le 11 août, démarcher pour un mandat au téléphone sans accord est interdit ; le téléphone mourait déjà ; ce qui dure, ce sont les canaux que tu possèdes : contenu, réputation, point de vente."
arc: Hook → Problem → Pivot → Turn → Demo → Payoff → Reassurance → CTA
audience: "Marchands et intermédiaires automobiles (mandats, dépôt-vente) qui trouvent leurs clients au téléphone"
mode: autonomous
captions: disabled
music: "pre-mixed with voice and SFX in assets/audio/mix.wav (mounted at root by the orchestrator)"
direction: "découpage écrit par Guillaume (SCRIPT.md), reel 9:16"
styleframes: "aucune (look validé sur la frame pilote)"
patterns: ../patterns/STORYBOARD-CRAFT.md, ../patterns/PATTERNS.md
---

## Video direction

- **One world** (frame.md) : un fond noir #0A0A0A, un accent orange #FB8000, du texte blanc. Chaque scène s'ouvre sur son titre en capitales grasses avec le trait orange tracé dessous, puis le visuel joue la phrase de la voix. Format vertical 1080×1920 : zones de sécurité des applis respectées (rien d'important en haut sur 220 px, en bas sur 360 px, ni à droite sous y 900).
- **Seams** : coupes franches voulues aux changements de scène (rythme reel, sur la voix, avec un whoosh) ; à l'intérieur d'une scène découpée en deux frames (3-4, 6-7, 8-9, 12-13), le handoff_out de N est copié mot pour mot dans le handoff_in de N+1.
- **Text** : la voix en sous-titres courts (2 à 6 mots par morceau) dans la bande y 1260 à 1440, mot par mot sur les temps donnés, le mot-clé de chaque phrase en orange ([orange : …]). Jamais plus de 6 mots dans un même bloc de texte.
- **Titres** : capitales grasses, trait orange tracé dessous, 6 mots au plus.
- **Motion grammar** : entrées qui claquent (×1,25 et flou → net en 0,18 s), traits qui se tracent, chiffres qui roulent, caméra qui ne s'arrête jamais (dérive lente + crans), pas d'image figée.
- **Negative list** : texte de plus de 6 mots, faux avis rédigés, vrais numéros de téléphone, nom de marque inventé sur la vitrine, deuxième couleur d'accent.

**MONDE** : une scène noire ; zones : titre y 260 à 640, visuel y 560 à 1220, sous-titres y 1260 à 1440.

**SIGNATURES**
- Mécanisme 1 « le trait orange » : sous chaque titre (0.4, 3.5, 8.3, 15.8, 21.6, 30.0, 37.6, 43.5, 50.0, 54.0).
- Mécanisme 2 « le chiffre qui roule » : 11 AOÛT 2026 (0.0), 9 → 3 (12–15), VUES (24–29), JOUR 1 → 214 (50–54).
- Rime : le téléphone barré de l'accroche revient en petit dans le titre de la fin (49.9).

**PARTITION CAMÉRA** : poussée lente continue (+1 à +2 %/s) dans chaque scène, crans de 0,3 s sur chaque nouvelle idée.

**VOIX** : montage resserré (pauses ramenées à 0,34 s, voix ×1,08) ; seule respiration gardée : après « trois. » (15.1 à 15.6).

**COUPES** (voulues, reel) : 3.26 « La » · 8.25 « Mais » · 15.63 « Le » · 21.46 « Un » · 29.90 « Deux » · 37.48 « Trois » · 43.36 « Ça » · 49.91 « Le ».

**RYTHME** : un événement toutes les 0,3 à 0,6 s partout.

**SON** : whoosh-short sur chaque coupe ; pop sur chaque titre ; key-press sur les chiffres qui roulent ; click sur le trait du téléphone barré ; notification sur l'abonnement.

## Frame 1: 11 août 2026 · 0.00 → 3.26

- scene: Les chiffres « 11 AOÛT 2026 » claquent un par un en très gros, puis un téléphone apparaît et se fait barrer d'un trait orange
- duration: 3.26s
- transition_in: cut
- status: outline
- src: compositions/frames/01-date.html
- voiceover: "Si tu trouves tes mandats au téléphone, t'as un problème depuis le onze août."
- type: hook
- blueprint: titlecard-reveal (Adapt)
- focal: 11 août 2026
- rules: kinetic-beat-slam, svg-path-draw
- world: dark
- handoff_in: aucun (ouverture du film) ; première image = « 11 » en Big Shoulders 900 300 px, blanc, arrivant ×1,4 et flou 10 px au centre du cadre, sur le fond noir avec son halo orange
- handoff_out: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)

Word cues: Si@0.05 tu@0.18 trouves@0.31 tes@0.43 mandats@0.56 au@0.82 téléphone@0.95 t'as@1.66 un@1.82 problème@1.98 depuis@2.30 le@2.63 onze@2.79 août@2.95

Scene 1 (0.00 à 1.60 s) : P1, la date
  TEXTE ÉCRAN : « 11 AOÛT 2026 » (jumbo, sur deux lignes : « 11 AOÛT » / « 2026 ») ; sous-titres « Si tu trouves tes [orange : mandats] » (0.05 à 0.75) puis « au téléphone, » (0.82 à 1.60).
  ÉTAPES : 0.00 « 11 » claque (×1,4 flou 10 → net 0,15 s) ; 0.30 « AOÛT » claque ; 0.60 « 2026 » claque dessous, ses chiffres roulent de 2020 à 2026 (0,25 s) ; 0.95 le trait orange se trace sous « 2026 ».
  PISTE CAMÉRA : poussée +2 %/s ; cran à 0.60 (recadrage pour les deux lignes).
  COUCHES ET PROFONDEUR : halo orange derrière la date ; grain.
  SON : pop 0.00, 0.30, 0.60.
  IMAGE CLÉ : 1.20 : « 11 AOÛT 2026 » énorme, trait orange sous 2026, « au téléphone, » en bas.

Scene 2 (1.60 à 3.26 s) : P2, le téléphone barré
  TEXTE ÉCRAN : sous-titre « t'as un [orange : problème] » (1.66 à 2.25) puis « depuis le onze août. » (2.30 à 3.26) ; la date reste au-dessus, réduite.
  ÉTAPES : 1.60 la date monte et rétrécit dans la zone titre (0,3 s power3.out) ; 1.75 le téléphone (composant phone) arrive dans la zone visuelle (×1,3 flou → net 0,18 s) ; 1.98 sur « problème », le trait orange le barre en diagonale (0,25 s) ; 2.30 le téléphone tremble deux fois (rotation ±3°, 0,08 s) puis se grise ; 2.80 à 3.26 poussée.
  PISTE CAMÉRA : poussée +2 %/s, cran à 1.60.
  SON : click 1.98.
  IMAGE CLÉ : 2.60 : la date en haut, le téléphone barré d'orange au centre, « depuis le onze août. » en bas.

## Frame 2: Démarchage sans accord · 3.26 → 8.25

- scene: « DÉMARCHAGE SANS ACCORD = INTERDIT » en titre, une liste de numéros masqués qui se grisent un par un
- duration: 4.99s
- transition_in: cut
- status: outline
- src: compositions/frames/02-loi.html
- voiceover: "La loi est passée : tu n'as plus le droit d'appeler un particulier pour lui proposer un mandat, sans son accord."
- type: context
- blueprint: typewriter-reveal (Adapt)
- focal: Démarchage sans accord
- rules: svg-path-draw, waterfall-entry
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)
- handoff_out: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)

Word cues: La@0.16 loi@0.30 est@0.44 passée@0.57 tu@0.85 n'as@1.12 plus@1.24 le@1.47 droit@1.61 d'appeler@1.75 un@2.18 particulier@2.32 pour@2.89 lui@3.03 proposer@3.30 un@3.61 mandat@3.71 sans@4.14 son@4.32 accord@4.50

Scene 1 (0.00 à 4.99 s) : P3, la loi
  TEXTE ÉCRAN : titre « DÉMARCHAGE SANS ACCORD = INTERDIT » (3 lignes : « DÉMARCHAGE » / « SANS ACCORD » / « = INTERDIT », « INTERDIT » en accent) ; liste de 7 numéros masqués (composant number-list) ; sous-titres « La loi est [orange : passée] » (0.16 à 0.80), « tu n'as plus le droit » (0.85 à 1.70), « d'appeler un particulier » (1.75 à 2.85), « pour lui proposer un [orange : mandat], » (2.89 à 4.05), « sans son accord. » (4.14 à 4.99).
  ÉTAPES : 0.00 « DÉMARCHAGE » claque ; 0.20 « SANS ACCORD » ; 0.40 « = INTERDIT » ; 0.60 le trait orange se trace ; 1.00 à 1.80 la liste de numéros tombe en cascade dans la zone visuelle (0,1 s d'écart) ; 2.20 à 4.60 les numéros se grisent et se barrent un par un (0,35 s d'écart) ; 4.50 le dernier se barre en accent.
  PISTE CAMÉRA : poussée +1,5 %/s ; cran à 1.00 vers la liste.
  SON : pop 0.00 ; key-press léger sur chaque numéro barré.
  IMAGE CLÉ : 4.60 : le titre, la liste entièrement grisée et barrée, « sans son accord. » en bas.

## Frame 3: Le téléphone mourait déjà · 8.25 → 11.75

- scene: Titre « LE TÉLÉPHONE MOURAIT DÉJÀ », la courbe démarre en haut avec « 2010 : 9 RDV SUR 10 APPELS »
- duration: 3.50s
- transition_in: cut
- status: outline
- src: compositions/frames/03-courbe.html
- voiceover: "Mais soyons honnêtes : le téléphone mourait déjà. Quand j'ai commencé,"
- type: pain_point
- blueprint: dataviz-countup (Adapt)
- focal: Le téléphone mourait déjà
- rules: svg-path-draw, counting-dynamic-scale
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)
- handoff_out: à 3.50 : la courbe (composant curve) cadrée plein écran, ligne blanche tracée de 2010 jusqu'à 2016 environ et qui commence à chuter, étiquette « 2010 : 9 RDV SUR 10 APPELS » posée en haut à gauche, caméra en travelling lent vers la droite (+40 px/s) ; titre « LE TÉLÉPHONE MOURAIT DÉJÀ » en haut avec son trait ; aucun sous-titre ; halo orange à gauche ; grain 4 %

Word cues: Mais@0.15 soyons@0.31 honnêtes@0.46 le@1.08 téléphone@1.23 mourait@1.70 déjà@2.00 Quand@2.61 j'ai@2.77 commencé@2.92

Scene 1 (0.00 à 3.50 s) : P4, la courbe commence haut
  TEXTE ÉCRAN : titre « LE TÉLÉPHONE MOURAIT DÉJÀ » (2 lignes) ; sous-titres « Mais soyons honnêtes : » (0.15 à 0.95), « le téléphone [orange : mourait] déjà. » (1.08 à 2.50), « Quand j'ai commencé, » (2.61 à 3.50) ; sur la courbe : axe « 2010 » … « 2026 », étiquette « 2010 : 9 RDV SUR 10 APPELS ».
  ÉTAPES : 0.00 le titre claque ; 0.30 le trait ; 0.60 les axes se tracent ; 1.00 la ligne blanche démarre en haut à gauche (point de départ net) ; 1.70 sur « mourait » la ligne se met à descendre ; 2.61 l'étiquette « 2010 : 9 RDV SUR 10 APPELS » se pose près du départ (le 9 roule de 0 à 9) ; 3.00 à 3.50 la ligne continue jusqu'à 2016 environ.
  PISTE CAMÉRA : travelling lent vers la droite (+40 px/s) qui suit la pointe de la ligne.
  SON : pop 0.00 ; key-press 2.61.
  IMAGE CLÉ : 3.00 : la courbe qui commence à chuter, « 2010 : 9 RDV SUR 10 APPELS », « Quand j'ai commencé, ».

## Frame 4: Aujourd'hui, trois · 11.75 → 15.63

- scene: La courbe chute jusqu'en 2026, « 2026 : 3 » se pose, le 3 en orange
- duration: 3.88s
- transition_in: cut
- status: outline
- src: compositions/frames/04-trois.html
- voiceover: "sur dix appels, je décrochais neuf rendez-vous. Aujourd'hui, trois."
- type: pain_point
- blueprint: dataviz-countup (Adapt)
- focal: Aujourd'hui, trois
- rules: svg-path-draw, counting-dynamic-scale
- world: dark
- handoff_in: à 0.00 : la courbe (composant curve) cadrée plein écran, ligne blanche tracée de 2010 jusqu'à 2016 environ et qui commence à chuter, étiquette « 2010 : 9 RDV SUR 10 APPELS » posée en haut à gauche, caméra en travelling lent vers la droite (+40 px/s) ; titre « LE TÉLÉPHONE MOURAIT DÉJÀ » en haut avec son trait ; aucun sous-titre ; halo orange à gauche ; grain 4 %
- handoff_out: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)

Word cues: sur@0.11 dix@0.29 appels@0.47 je@0.83 décrochais@1.01 neuf@1.55 rendez-vous@1.73 Aujourd'hui@2.57 trois@3.35

Scene 1 (0.00 à 3.88 s) : P5, 9 sur 10, puis 3
  TEXTE ÉCRAN : sous-titres « sur [orange : dix] appels, » (0.11 à 0.80), « je décrochais [orange : neuf] rendez-vous. » (0.83 à 2.45), « Aujourd'hui, [orange : trois]. » (2.57 à 3.88) ; étiquette de fin « 2026 : 3 » (le 3 en accent, jumbo 220 px).
  ÉTAPES : 0.11 à 1.80 l'étiquette 2010 pulse une fois sur « neuf » (×1,1) ; 1.90 à 2.80 la ligne plonge jusqu'en 2026 (power2.in) ; 2.57 le travelling accélère ; 3.00 le point d'arrivée accent se pose ; 3.35 sur « trois » : « 2026 : 3 » claque, le 3 en accent roule de 9 à 3 ; 3.40 à 3.88 respiration : le 3 respire une fois (×1,05) et la ligne fait une ombre orange.
  PISTE CAMÉRA : travelling +40 px/s, accélération à 2.57, cran vers l'étiquette finale à 3.20.
  SON : key-press 3.35 ; pop 3.35.
  IMAGE CLÉ : 3.60 : la courbe effondrée, « 2026 : 3 » avec le 3 orange, « Aujourd'hui, trois. ».

## Frame 5: Tout le monde pêche au même endroit · 15.63 → 21.46

- scene: Une mosaïque d'annonces auto identiques qui se multiplient jusqu'à remplir l'écran, puis « TOUT LE MONDE PÊCHE AU MÊME ENDROIT »
- duration: 5.83s
- transition_in: cut
- status: outline
- src: compositions/frames/05-mosaique.html
- voiceover: "Le vrai problème, c'est pas la loi. Si tu pêches là où pêchent tous tes concurrents, c'est normal d'avoir de la concurrence."
- type: pain_point
- blueprint: overwhelm-surround (Adapt)
- focal: Tout le monde pêche au même endroit
- rules: waterfall-entry, kinetic-beat-slam
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)
- handoff_out: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)

Word cues: Le@0.27 vrai@0.44 problème@0.60 c'est@1.10 pas@1.26 la@1.43 loi@1.59 Si@2.06 tu@2.22 pêches@2.38 là@2.54 où@2.70 pêchent@2.86 tous@3.17 tes@3.33 concurrents@3.49 c'est@4.16 normal@4.30 d'avoir@4.57 de@4.85 la@4.99 concurrence@5.13

Scene 1 (0.00 à 2.00 s) : P6, le vrai problème
  TEXTE ÉCRAN : sous-titres « Le vrai [orange : problème], » (0.27 à 1.05), « c'est pas la loi. » (1.10 à 2.00) ; une annonce (composant listing-tile) au centre.
  ÉTAPES : 0.10 une annonce se pose au centre ; 0.60 elle se duplique en 2, 1.00 en 4, 1.40 en 9, 1.80 en 16 (grille qui se densifie, copies identiques, chacune ×1,2 flou → net).
  PISTE CAMÉRA : recul continu (échelle 1,3 → 0,8) pour découvrir la mosaïque.
  SON : pop léger sur chaque multiplication.
  IMAGE CLÉ : 1.60 : une grille de 9 annonces identiques, « c'est pas la loi. ».

Scene 2 (2.00 à 5.83 s) : P7, la même mare
  TEXTE ÉCRAN : titre « TOUT LE MONDE PÊCHE AU MÊME ENDROIT » (3 lignes : « TOUT LE MONDE PÊCHE » / « AU MÊME » / « ENDROIT ») sur un bandeau sombre par-dessus la mosaïque ; sous-titres « Si tu [orange : pêches] là où » (2.06 à 2.85), « pêchent tous tes concurrents, » (2.86 à 4.05), « c'est normal d'avoir » (4.16 à 4.95), « de la [orange : concurrence]. » (4.99 à 5.83).
  ÉTAPES : 2.06 la mosaïque se densifie encore (36 tuiles) et s'assombrit à 35 % ; 2.38 sur « pêches » le titre claque ligne par ligne (0,15 s d'écart) ; 2.90 le trait ; 3.49 sur « concurrents » les tuiles clignotent toutes en même temps une fois ; 5.13 sur « concurrence » la mosaïque se resserre d'un cran.
  PISTE CAMÉRA : dérive lente vers le haut (−20 px/s) sur la mosaïque, poussée +1 %/s.
  SON : pop 2.38.
  IMAGE CLÉ : 3.60 : la mosaïque d'annonces identiques assombrie, le titre par-dessus avec son trait.

## Frame 6: 1 · Montre ton travail · 21.46 → 26.26

- scene: La carte 1 monte du bas : « MONTRE TON TRAVAIL », un feed qui défile (remise de clés, voiture préparée), le compteur de vues grimpe
- duration: 4.80s
- transition_in: cut
- status: outline
- src: compositions/frames/06-carte1.html
- voiceover: "Un : montre ton travail. Chaque voiture vendue, chaque client livré, c'est un contenu."
- type: solution
- blueprint: fixed-anchor-cycle (Adapt)
- focal: 1 · Montre ton travail
- rules: card-morph-anchor, counting-dynamic-scale
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)
- handoff_out: à 4.80 : la carte 1 « MONTRE TON TRAVAIL » (composant card, badge « 1 ») centrée, son feed défile vers le haut (60 px/s), compteur « VUES » à 9 800 qui monte ; aucun sous-titre ; grain 4 %

Word cues: Un@0.15 montre@0.65 ton@0.87 travail@1.09 Chaque@1.83 voiture@2.18 vendue@2.53 chaque@2.88 client@3.24 livré@3.41 c'est@3.76 un@3.94 contenu@4.11

Scene 1 (0.00 à 4.80 s) : P8, la carte 1
  TEXTE ÉCRAN : carte 1 (composant card, badge « 1 ») titre « MONTRE TON TRAVAIL » ; feed (composant feed) avec 3 légendes courtes dans les posts : « CLÉS REMISES », « PRÊTE À PARTIR », « CLIENT LIVRÉ » (Space Mono 26) ; compteur « VUES » ; sous-titres « Un : [orange : montre] ton travail. » (0.15 à 1.70), « Chaque voiture vendue, » (1.83 à 2.80), « chaque client livré, » (2.88 à 3.70), « c'est un [orange : contenu]. » (3.76 à 4.80).
  ÉTAPES : 0.00 la carte monte du bas (y +900 → 0, 0,35 s expo.out) ; 0.15 le badge « 1 » claque ; 0.65 le titre de la carte claque, 0.90 son trait ; 1.83 le feed commence à défiler ; 2.18 post « PRÊTE À PARTIR » ; 2.88 post « CLÉS REMISES » ; 3.41 post « CLIENT LIVRÉ » ; 3.76 le compteur « VUES » roule de 1 240 à 9 800.
  PISTE CAMÉRA : poussée +1 %/s, cran à 1.80 vers le feed.
  SON : whoosh-short 0.00 ; pop 0.15 ; key-press 3.76.
  IMAGE CLÉ : 4.20 : la carte 1, le feed qui défile, « VUES 9 800 », « c'est un contenu. ».

## Frame 7: Organique, pas pub · 26.26 → 29.90

- scene: Sur la carte 1, une étiquette « PUB » se barre, « ORGANIQUE » s'allume, le compteur de vues continue de grimper
- duration: 3.64s
- transition_in: cut
- status: outline
- src: compositions/frames/07-organique.html
- voiceover: "En organique, pas en pub. On achète à quelqu'un qu'on a déjà vu bosser."
- type: solution
- blueprint: fixed-anchor-cycle (Adapt)
- focal: Organique, pas pub
- rules: counting-dynamic-scale, svg-path-draw
- world: dark
- handoff_in: à 0.00 : la carte 1 « MONTRE TON TRAVAIL » (composant card, badge « 1 ») centrée, son feed défile vers le haut (60 px/s), compteur « VUES » à 9 800 qui monte ; aucun sous-titre ; grain 4 %
- handoff_out: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)

Word cues: En@0.15 organique@0.27 pas@0.93 en@1.07 pub@1.22 On@1.67 achète@1.79 à@2.03 quelqu'un@2.16 qu'on@2.52 a@2.76 déjà@2.88 vu@3.13 bosser@3.25

Scene 1 (0.00 à 3.64 s) : P9, organique
  TEXTE ÉCRAN : deux pastilles sur la carte : « ORGANIQUE » (accent) et « PUB » (barrée) ; sous-titres « En [orange : organique], » (0.15 à 0.90), « pas en pub. » (0.93 à 1.60), « On achète à quelqu'un » (1.67 à 2.50), « qu'on a déjà vu [orange : bosser]. » (2.52 à 3.64).
  ÉTAPES : 0.27 la pastille « ORGANIQUE » s'allume en accent ; 0.93 la pastille « PUB » apparaît et 1.22 se fait barrer ; 1.67 le feed accélère ; 2.16 le compteur « VUES » repart de 9 800 à 18 600 ; 3.25 sur « bosser » un post « CLIENT LIVRÉ » se fige au centre avec un cœur accent.
  PISTE CAMÉRA : poussée +1 %/s.
  SON : click 1.22 ; key-press 2.16.
  IMAGE CLÉ : 3.30 : la carte 1, « ORGANIQUE » allumé, « PUB » barré, « VUES 18 600 ».

## Frame 8: 2 · Ta réputation · 29.90 → 33.34

- scene: La carte 2 monte et recouvre la carte 1 : « TA RÉPUTATION », cinq étoiles se remplissent, les avis s'empilent
- duration: 3.44s
- transition_in: cut
- status: outline
- src: compositions/frames/08-carte2.html
- voiceover: "Deux : ta réputation. Les avis, les clients qui reviennent,"
- type: solution
- blueprint: fixed-anchor-cycle (Adapt)
- focal: 2 · Ta réputation
- rules: card-morph-anchor, waterfall-entry
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)
- handoff_out: à 3.44 : la carte 2 « TA RÉPUTATION » (badge « 2 ») centrée au-dessus de la carte 1 réduite à 0,94 et assombrie, cinq étoiles pleines en accent, deux bulles d'avis empilées, une troisième qui arrive ; aucun sous-titre ; grain 4 %

Word cues: Deux@0.15 ta@0.31 réputation@0.77 Les@1.70 avis@1.87 les@2.37 clients@2.53 qui@2.68 reviennent@2.84

Scene 1 (0.00 à 3.44 s) : P10, la carte 2
  TEXTE ÉCRAN : carte 2 (badge « 2 ») titre « TA RÉPUTATION » ; cinq étoiles (composant stars) ; bulles d'avis sans texte lisible ; sous-titres « Deux : ta [orange : réputation]. » (0.15 à 1.60), « Les [orange : avis], » (1.70 à 2.30), « les clients qui reviennent, » (2.37 à 3.44).
  ÉTAPES : 0.00 la carte 1 réduite (0,94, assombrie) est en place derrière ; la carte 2 monte du bas (0,35 s expo.out) ; 0.15 badge « 2 » ; 0.77 le titre claque, 1.00 son trait ; 1.70 à 2.30 les cinq étoiles se remplissent une à une ; 2.37 une première bulle d'avis se pose ; 2.84 une deuxième ; 3.20 une troisième arrive.
  PISTE CAMÉRA : poussée +1 %/s.
  SON : whoosh-short 0.00 ; pop sur chaque étoile.
  IMAGE CLÉ : 2.60 : la carte 2 sur la carte 1, cinq étoiles orange, une bulle d'avis.

## Frame 9: Aucun concurrent ne peut te le prendre · 33.34 → 37.48

- scene: Sur la carte 2, une flèche de recommandation relie deux bulles (« le beau-frère »), puis un cadenas orange se ferme sur les étoiles
- duration: 4.14s
- transition_in: cut
- status: outline
- src: compositions/frames/09-cadenas.html
- voiceover: "ceux qui t'envoient leur beau-frère. Ça, aucun concurrent ne peut te le prendre."
- type: solution
- blueprint: fixed-anchor-cycle (Adapt)
- focal: Aucun concurrent ne peut te le prendre
- rules: svg-path-draw, kinetic-beat-slam
- world: dark
- handoff_in: à 0.00 : la carte 2 « TA RÉPUTATION » (badge « 2 ») centrée au-dessus de la carte 1 réduite à 0,94 et assombrie, cinq étoiles pleines en accent, deux bulles d'avis empilées, une troisième qui arrive ; aucun sous-titre ; grain 4 %
- handoff_out: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)

Word cues: ceux@0.12 qui@0.25 t'envoient@0.38 leur@0.64 beau-frère@0.77 Ça@1.47 aucun@2.04 concurrent@2.31 ne@2.72 peut@2.86 te@2.99 le@3.27 prendre@3.69

Scene 1 (0.00 à 4.14 s) : P11, le beau-frère et le cadenas
  TEXTE ÉCRAN : sous-titres « ceux qui t'envoient » (0.12 à 0.70), « leur [orange : beau-frère]. » (0.64 à 1.40), « Ça, » (1.47 à 2.00), « aucun concurrent ne peut » (2.04 à 2.95), « te le [orange : prendre]. » (2.99 à 4.14).
  ÉTAPES : 0.38 une petite silhouette (cercle + épaules, ligne blanche) apparaît à côté d'une bulle d'avis ; 0.64 une flèche accent courbe part d'elle vers une deuxième silhouette (svg path draw 0,3 s) ; 1.47 les étoiles brillent une fois ; 2.31 sur « concurrent » des silhouettes grises tentent d'entrer par les bords et s'arrêtent ; 3.27 un cadenas orange se ferme sur les étoiles (×1,3 → 1, 0,18 s) ; 3.69 sur « prendre » le cadenas claque.
  PISTE CAMÉRA : poussée +1 %/s, cran à 3.20 sur le cadenas.
  SON : click 3.69.
  IMAGE CLÉ : 3.80 : la carte 2, cinq étoiles, le cadenas orange fermé dessus.

## Frame 10: 3 · Sois installé · 37.48 → 43.36

- scene: La carte 3 monte : « SOIS INSTALLÉ », une vitrine s'allume, une adresse apparaît sur une carte avec un repère orange
- duration: 5.88s
- transition_in: cut
- status: outline
- src: compositions/frames/10-carte3.html
- voiceover: "Trois : sois installé. Un point de vente, une adresse, une vitrine. Face à un inconnu sur Leboncoin, c'est ce qui rassure."
- type: solution
- blueprint: fixed-anchor-cycle (Adapt)
- focal: 3 · Sois installé
- rules: card-morph-anchor, coordinate-target-zoom
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)
- handoff_out: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)

Word cues: Trois@0.12 sois@0.30 installé@0.48 Un@1.30 point@1.45 de@1.60 vente@1.75 une@2.05 adresse@2.20 une@2.66 vitrine@2.81 Face@3.58 à@3.71 un@3.85 inconnu@3.98 sur@4.38 Leboncoin@4.52 c'est@4.92 ce@5.05 qui@5.18 rassure@5.32

Scene 1 (0.00 à 5.88 s) : P12, la carte 3
  TEXTE ÉCRAN : carte 3 (badge « 3 ») titre « SOIS INSTALLÉ » ; vitrine et carte de quartier (composant shopfront) ; à la fin, une tuile d'annonce floue étiquetée « INCONNU ? » ; sous-titres « Trois : sois [orange : installé]. » (0.12 à 1.20), « Un point de vente, » (1.30 à 2.00), « une adresse, » (2.05 à 2.60), « une vitrine. » (2.66 à 3.50), « Face à un inconnu » (3.58 à 4.35), « sur Leboncoin, » (4.38 à 4.90), « c'est ce qui [orange : rassure]. » (4.92 à 5.88).
  ÉTAPES : 0.00 les cartes 1 et 2 réduites derrière, la carte 3 monte du bas ; 0.12 badge « 3 » ; 0.48 titre, 0.70 trait ; 1.45 la façade se dessine ; 2.20 sur « adresse » la carte de quartier se pose et le repère accent tombe sur son point ; 2.81 sur « vitrine » la vitrine s'allume (lueur accent) ; 3.58 une tuile d'annonce grise et floue « INCONNU ? » apparaît à gauche, petite ; 5.32 sur « rassure » la vitrine éclaire plus fort et l'annonce floue s'éteint.
  PISTE CAMÉRA : poussée +1 %/s, crans à 2.20 et 3.58.
  SON : whoosh-short 0.00 ; pop 2.20 ; pop 2.81.
  IMAGE CLÉ : 3.20 : la carte 3, la vitrine allumée et le repère orange sur la carte.

## Frame 11: Le mur · 43.36 → 49.91

- scene: Un mur se construit brique par brique du bas vers le haut, la dernière brique en orange ; « Le marché tranchera pour toi »
- duration: 6.55s
- transition_in: cut
- status: outline
- src: compositions/frames/11-mur.html
- voiceover: "Ça prend du temps et de la régularité. Mais une fois en place, personne ne te le prend. Pas le temps d'être régulier ? Le marché tranchera pour toi."
- type: punchline
- blueprint: fixed-anchor-cycle (Adapt)
- focal: Le mur
- rules: waterfall-entry, kinetic-beat-slam
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)
- handoff_out: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)

Word cues: Ça@0.16 prend@0.28 du@0.39 temps@0.51 et@0.62 de@0.74 la@0.98 régularité@1.12 Mais@2.10 une@2.25 fois@2.40 en@2.55 place@2.71 personne@3.23 ne@3.45 te@3.56 le@3.66 prend@3.77 Pas@4.37 le@4.48 temps@4.59 d'être@4.70 régulier@4.82 Le@5.45 marché@5.57 tranchera@5.81 pour@6.17 toi@6.29

Scene 1 (0.00 à 6.55 s) : P13, brique par brique
  TEXTE ÉCRAN : titre « BRIQUE PAR BRIQUE » ; mur (composant wall) ; sous-titres « Ça prend du [orange : temps] » (0.16 à 0.90), « et de la régularité. » (0.62 à 2.00), « Mais une fois en place, » (2.10 à 3.15), « personne ne te le [orange : prend]. » (3.23 à 4.25), « Pas le temps d'être régulier ? » (4.37 à 5.35), « Le marché [orange : tranchera] pour toi. » (5.45 à 6.55).
  ÉTAPES : 0.00 le titre claque, 0.30 son trait ; 0.40 à 3.70 les briques se posent du bas vers le haut au rythme de la voix (une brique toutes les 0,12 s, rangée après rangée) ; 3.77 sur « prend » la dernière brique, orange, claque au sommet ; 4.37 à 5.40 le mur reste, une lueur orange le parcourt ; 5.81 sur « tranchera » un trait orange tranche l'écran en diagonale et le mur s'éclaire.
  PISTE CAMÉRA : montée lente avec le mur (−30 px/s), cran à 3.70.
  SON : pop doux sur les rangées ; click 3.77 ; whoosh 5.81.
  IMAGE CLÉ : 4.00 : le mur complet, la brique orange au sommet, « personne ne te le prend. ».

## Frame 12: Tu loues tes clients · 49.91 → 53.83

- scene: « LE TÉLÉPHONE : TU LOUES TES CLIENTS. » avec un compteur de jours qui défile dessous
- duration: 3.92s
- transition_in: cut
- status: outline
- src: compositions/frames/12-louer.html
- voiceover: "Le téléphone, c'est louer tes clients, et chercher de nouvelles locations tous les jours."
- type: cta
- blueprint: titlecard-reveal (Adapt)
- focal: Tu loues tes clients
- rules: counting-dynamic-scale, kinetic-beat-slam
- world: dark
- handoff_in: aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)
- handoff_out: à 3.92 : fond #0A0A0A, titre « LE TÉLÉPHONE : TU LOUES TES CLIENTS. » en haut avec son trait, compteur « JOUR 214 » qui défile dessous (accent), caméra en poussée lente (+1 %/s) ; aucun sous-titre ; grain 4 %

Word cues: Le@0.14 téléphone@0.32 c'est@1.02 louer@1.20 tes@1.38 clients@1.55 et@2.00 chercher@2.15 de@2.44 nouvelles@2.59 locations@2.88 tous@3.32 les@3.47 jours@3.61

Scene 1 (0.00 à 3.92 s) : P14, louer
  TEXTE ÉCRAN : titre « LE TÉLÉPHONE : » / « TU LOUES TES CLIENTS. » (2 blocs, 5 mots max chacun, un petit téléphone barré à gauche de « LE TÉLÉPHONE », rime de l'accroche) ; compteur (composant day-counter) « JOUR 1 » → « JOUR 214 » ; sous-titres « Le téléphone, » (0.14 à 0.95), « c'est [orange : louer] tes clients, » (1.02 à 1.95), « et chercher de nouvelles locations » (2.00 à 3.25), « tous les [orange : jours]. » (3.32 à 3.92).
  ÉTAPES : 0.14 « LE TÉLÉPHONE : » claque avec le petit téléphone barré ; 1.20 sur « louer » « TU LOUES TES CLIENTS. » claque, 1.40 le trait ; 2.00 le compteur apparaît « JOUR 1 » et défile de plus en plus vite jusqu'à « JOUR 214 » à 3.90.
  PISTE CAMÉRA : poussée +1 %/s.
  SON : pop 0.14 ; pop 1.20 ; key-press 2.00 à 3.90.
  IMAGE CLÉ : 3.50 : le titre en deux blocs, le compteur « JOUR 197 » qui défile.

## Frame 13: Tu les possèdes · 53.83 → 58.23

- scene: « CES CANAUX : TU LES POSSÈDES. », puis « @guillaumeherbin_ » avec un bouton S'abonner
- duration: 4.40s
- transition_in: cut
- status: outline
- src: compositions/frames/13-posseder.html
- voiceover: "Ces canaux-là, tu les possèdes. Abonne-toi pour la suite."
- type: cta
- blueprint: cta-morph-press (Adapt)
- focal: Tu les possèdes
- rules: kinetic-beat-slam, cursor-click-ripple
- world: dark
- handoff_in: à 0.00 : fond #0A0A0A, titre « LE TÉLÉPHONE : TU LOUES TES CLIENTS. » en haut avec son trait, compteur « JOUR 214 » qui défile dessous (accent), caméra en poussée lente (+1 %/s) ; aucun sous-titre ; grain 4 %
- handoff_out: aucun (fin du film, tenue jusqu'à 4.40)

Word cues: Ces@0.15 canaux-là@0.29 tu@0.91 les@1.04 possèdes@1.16 Abonne-toi@1.85 pour@2.26 la@2.36 suite@2.47

Scene 1 (0.00 à 1.80 s) : P15, posséder
  TEXTE ÉCRAN : titre « CES CANAUX : » / « TU LES POSSÈDES. » (les trois icônes des cartes en petit au-dessus : feed, étoile, vitrine) ; sous-titres « Ces canaux-là, » (0.15 à 0.85), « tu les [orange : possèdes]. » (0.91 à 1.80).
  ÉTAPES : 0.00 le titre « LE TÉLÉPHONE… » et le compteur sortent vers le haut (0,2 s) ; 0.15 « CES CANAUX : » claque, les trois petites icônes se posent au-dessus (0,08 s d'écart) ; 1.16 sur « possèdes » « TU LES POSSÈDES. » claque, 1.30 le trait.
  PISTE CAMÉRA : poussée +1 %/s.
  SON : pop 0.15, 1.16.
  IMAGE CLÉ : 1.60 : « CES CANAUX : TU LES POSSÈDES. » avec les trois icônes.

Scene 2 (1.80 à 4.40 s) : P16, l'abonnement
  TEXTE ÉCRAN : « @guillaumeherbin_ » (handle) ; un bouton « S'ABONNER » (accent, texte noir) ; sous-titre « [orange : Abonne-toi] pour la suite. » (1.85 à 3.20).
  ÉTAPES : 1.85 le handle arrive (×1,2 flou → net) ; 2.10 le bouton « S'ABONNER » se pose dessous ; 2.60 un curseur (doigt ou flèche) arrive en une courbe et tape le bouton à 3.00, qui passe à « ABONNÉ ✓ » ; 3.20 à 4.40 tenue vivante (halo qui glisse, poussée lente).
  PISTE CAMÉRA : poussée +1 %/s.
  SON : notification 3.00.
  IMAGE CLÉ : 3.40 : « @guillaumeherbin_ », le bouton « ABONNÉ ✓ », la lueur orange.
