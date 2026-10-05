---
format: 1920x1080
duration: "56.80s"
message: "Se lancer pour essayer coûte des mois, ta marge et ton épargne ; se lancer avec un plan fait par quelqu’un qui connaît le métier limite la casse."
arc: Hook → Problem → Pivot → Turn → Demo → Payoff → Reassurance → CTA
audience: "Passionnés d’automobile, souvent salariés, qui veulent en vivre (achat-revente, dépôt-vente, courtage, intermédiation) et hésitent à se lancer"
mode: autonomous
captions: disabled
music: "pre-mixed with voice and SFX in assets/audio/mix.wav (mounted at root by the orchestrator)"
direction: "mélange A « L’annonce » + B « Le tableau de bord » + C « Le brouillon et la preuve » (DIRECTIONS.md, Choix)"
styleframes: "styleframes/png/A1.png (8.1 s), A2.png (11.5 s), C1.png (16 s), C2.png (33 s, sans Kbis), B3.png (42.8 s), A3.png (45.7 s), C3.png (52.2 s)"
patterns: ../patterns/STORYBOARD-CRAFT.md, ../patterns/PATTERNS.md
---

## Video direction

- **One world** (frame.md) : une seule scène sombre, éclairée comme le bandeau de Guillaume (halo orange, contre-jour bleu), sur laquelle on pose des objets réels : l'annonce leboncoin, le solde, le brouillon, l'écran GPS, le portrait, la frise des années, le plan de lancement. Frames 1-5 = PROBLÈME ; frame 6 = BASCULE sur noir ; frames 7-11 = SOLUTION ; frame 12 = FIN. Chaque frame peint son propre fond plein cadre comme couche `class="clip"`.
- **Invisible seams** : chaque frame entre en `cut` ; chaque jonction tombe au sommet du flou d'un mouvement de caméra, et le `handoff_out` de la frame N est copié mot pour mot dans le `handoff_in` de la frame N+1. Exceptions voulues : 22.90 (la feuille s'éteint jusqu'au noir, fondu 1 sur 2) et 56.80 (fin au noir, fondu 2 sur 2). Aucune coupe franche.
- **Text** : chaque phrase de la voix est un `subtitle` en bas au centre (bande y 890 à 980, rien d'autre dedans), MOT PAR MOT sur les temps donnés (`mot@secondes`, locaux à la frame). Exactement UN mot ou groupe par phrase dans la `key-word-box` ([boîte : …]). Moments typographiques (la phrase EST l'image, centrée, 84 px au plus) : « C'est de te lancer sans plan. » (frame 4) et « Et si tu essayais… avec un plan ? » (frame 6).
- **Peaks** : les 3 pics [trait : …] : « sans plan » (17.5), « métier » (29.2), « moins de casse » (47.0).
- **One thing to look at** : dans chaque plan, la caméra isole le sujet de la phrase ; un zoom franc dans un sens, jamais d'aller-retour ; pas de décor sans sens.
- **Real interfaces** (frame.md) : l'annonce leboncoin Audi RS Q8 et Ford Ranger (floutées), la page d'accueil La Centrale, la barre de recherche leboncoin, le portrait de Guillaume, l'aperçu réel du plan de lancement.
- **Motion grammar** : deux vitesses, gestes de 1 à 6 images (expo.out) et dérives linéaires qui ne s'arrêtent pas ; la zone 0,3 à 0,9 s est réservée à la caméra et au curseur (expo, power3, power4) ; les éléments arrivent trop grands et flous puis se posent ; jamais d'image figée.
- **Visible copy** : exactement le texte cité dans les lignes Scene, rien d'autre.
- **Negative list** : diaporama, économiseur d'écran, objet dédoublé, texte coloré au lieu de la boîte, grosse phrase, mot géant, symbole abstrait, curseur qui hésite (hors gag de la frame 3), plusieurs objets en mouvement sur une jonction, autre teinte que l'accent hors interfaces réelles, chiffre d'affaires ou promesse de revenu.

**MONDE**
- Acte 1 (0.00 à 14.00) : l'annonce. La barre de recherche, puis la page leboncoin posée sur la scène comme une feuille blanche ; stations : résultats (960, 600), annonce Audi (photos en haut, prix en bas à gauche), onglets (barre en haut), carte vendeur de la Ford (à droite) ; fond sombre, halo orange derrière la page.
- Acte 2 (14.00 à 22.90) : le brouillon. Feuille crème lignée sur la scène sombre, éclairée par un halo orange ; stations : calculs (haut), marge (milieu), trois questions (bas).
- Bascule (22.90 à 27.30) : noir pur, puis l'écran GPS qui s'allume.
- Acte 3 (27.30 à 48.85) : la preuve et la route. Écran GPS (route de (330, 700) à (1590, 200)), portrait (500, 440), frise des années 2010 → 2026 (horizontale y 470), la route du GPS, la page du plan, les cadrans du tableau de bord.
- Fin (48.85 à 56.80) : la barre de recherche du début devient le bouton.
- Couleurs de rôle : accent = ce qui compte (boîtes, traits, route, bouton, chiffres qui roulent) ; vert leboncoin = le prix ; rouge stylo = la perte sur le brouillon ; bleu = contre-jour et point de départ du GPS uniquement.

**SIGNATURES**
- Mécanisme 1 « le chiffre qui roule » : 5.4 (la date vieillit), 8.1 (le prix baisse), 10.5 (le solde descend), 32.5 (21 ans), 33.6 (3 000 €), 38.6 (2010 → 2026), 47.9 (le compteur de mois revient à 00).
- Mécanisme 2 « la rature accent » : 7.7 (prix barré), 19.0 à 22.0 (les trois questions), 37.3 à 38.9 (les erreurs de la frise), 43.9 (les modèles tranchés).
- Registres de texte : sous-titre mot par mot (fromTo opacité + y + flou, 0,14 s) ; boîte (scaleX depuis la gauche, 0,16 s) ; trait (scaleX, 0,35 s) ; moment typographique (lettres qui convergent, 0,5 s expo.out).
- Rimes : la barre de recherche de l'accroche (0.00 à 3.80) revient à la fin (48.85) et devient le bouton ; le curseur qui clique « Rechercher » à 2.90 clique le bouton à 53.70, sans hésiter cette fois.

**PARTITION CAMÉRA** (temps globaux) : 0.00 arrivée de la barre (×2,2 → ×1) · 0.30 à 3.30 dérive z +1,5 %/s · 3.35 plongée dans la carte (power3.in) · 3.80 atterrissage sur l'annonce (expo.out) · 4.80 descente vers la date · 6.40 montée vers le prix (expo.inOut) · 8.55 panoramique vers les onglets · 11.15 poussée vers la carte vendeur · 13.15 suivi de la page qui se referme · 14.00 dérive vers le bas le long des calculs · 17.40 recul (power3.out) · 18.00 trois crans vers le bas (un par question) · 22.20 extinction · 25.90 poussée lente sur l'écran GPS · 29.30 plongée dans le point bleu · 30.00 dérive droite · 36.70 whip droite · 37.00 travelling le long de la frise · 39.70 arrêt sur 2026 puis montée avec la route · 41.75 poussée vers le départ · 43.55 travelling vers le 2e point · 44.80 arrivée au 3e point, plongée dans l'anneau · 46.60 recul sur les cadrans · 48.40 poussée vers le point d'arrivée · 48.85 atterrissage sur la barre · 50.90 poussée sur le bouton · 53.60 dérive lente de tenue · 56.25 sortie au noir.

**VOIX** : temps dans onsets.json ; silences de plus de 0,4 s, chacun avec son action : 1.40 à 1.75 (la requête finit de se taper) · 2.51 à 2.90 (le curseur arrive sur Rechercher) · 3.42 à 3.95 (plongée dans l'annonce) · 5.82 à 6.37 (la date finit de rouler, la caméra monte vers le prix) · 8.45 à 9.00 (l'étiquette du prix part) · 11.13 à 14.15 (LE GAG MUET : le curseur hésite trois fois sur « Envoyer un message », puis ferme l'onglet) · 17.71 à 18.10 (recul sur la feuille) · 19.86 à 20.29 et 21.03 à 21.38 (les questions s'écrivent) · 22.23 à 23.52 (la feuille s'éteint, noir) · 25.84 à 27.57 (le GPS s'allume) · 29.48 à 30.38 (plongée dans le point bleu, le portrait apparaît) · 38.99 à 39.70 (arrivée sur 2026, la ligne continue) · 41.54 à 42.06 (poussée vers le départ du GPS) · 46.12 à 46.68 (recul vers les cadrans) · 48.39 à 49.26 (la route mène à la barre de recherche) · 52.58 à 56.80 (clic sur le bouton, tenue, noir).

**COUPES** (quota de la voix) : aucune coupe franche ; deux fondus voulus : 22.23 à 22.90 (« Et », la feuille s'éteint avant la bascule) et 56.25 à 56.80 (fin).

**RYTHME** : douleur (0 à 22.9) : 9 plans, environ 4 par 10 s, un événement toutes les 0,3 à 0,6 s ; solution (27.3 à 48.85) : 10 plans, environ 4,6 par 10 s.

**SON** (temps globaux, sur les gestes) : key-press 0.10 à 1.40 (frappe de la requête) · click 2.90 · whoosh-short 3.60 · pop 4.00 (étiquette modèle) · key-press 5.30 à 5.65 (la date roule) · pop 8.13 (nouveau prix) · whoosh-short 8.60 · pop 9.15 et 9.55 (onglets) · key-press 10.45 à 10.75 (le solde roule) · click 13.45 (fermeture de l'onglet) · whoosh-short 13.55 · key-press 14.20 à 15.60 (le stylo écrit) · pop 16.65 (− 650 €) · whoosh 22.30 (extinction) · NOTIFICATION À DEUX TONS 26.30 (« Itinéraire calculé », la signature) · whoosh-short 29.35 · pop 32.52 et 33.52 (chiffres) · whoosh 36.70 · pop 37.70, 38.30, 38.85 (ratures) · pop 42.76 · pop 43.83 · pop 45.72 · ping 46.68 · whoosh-short 48.40 · key-press 49.70 à 50.40 (effacement de la requête) · pop 51.20 (le bouton se forme) · click 53.70.

## Frame 1: J'essaie · 0.00 → 3.80

- scene: Sur la scène sombre, la barre de recherche leboncoin arrive trop grande et floue et se pose ; la requête « voiture occasion » se tape ; le curseur arrive et clique Rechercher sur « j'essaie » ; trois résultats tombent ; la caméra plonge dans le premier
- duration: 3.80s
- transition_in: cut
- status: outline
- src: compositions/frames/01-recherche.html
- voiceover: "Tu veux vivre de l’automobile. Alors tu te dis : j’essaie."
- type: hook
- blueprint: prompt-type-submit-generate (Adapt)
- focal: la barre de recherche, puis la 1re annonce
- rules: cursor-click-ripple, waterfall-entry
- world: dark
- handoff_in: aucun (ouverture du film) ; première image = la barre de recherche leboncoin (composant search) au centre à ×2,2, flou 14 px, champ vide, caret accent, sur la scène sombre avec son halo orange
- handoff_out: à 3.80 : poussée power3.in en cours vers la 1re carte de résultat (vignette de l'Audi grise + « 86 900 € »), la carte couvre 120 % du cadre, flou 12 px ; scène sombre derrière ; aucun sous-titre ; grain 5 %

Word cues: Tu@0.06 veux@0.21 vivre@0.36 de@0.51 l'automobile@0.66 Alors@1.75 tu@2.05 te@2.21 dis@2.36 j'essaie@2.90

Scene 1 (0.00 à 1.70 s) : P1, la recherche
  TEXTE ÉCRAN : sous-titre « Tu veux vivre de [boîte : l’automobile.] » mot par mot (Tu 0.06 … boîte tracée 0.64, l’automobile. 0.66) ; dans le champ, la requête « voiture occasion » ; écart : avance de 0,1 s (la frappe commence avant « vivre »).
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 à 0.30 la barre se pose (×2,2 flou 14 → ×1 net, expo.out) ; 0.10 le logo leboncoin (crop réel) s'allume à gauche de la barre ; 0.18 premier caractère, puis un caractère toutes les 0,07 s jusqu'à 1.30 (« voiture occasion ») ; 0.66 la boîte de « l’automobile » ; 1.30 à 1.70 le caret clignote (2 pas finis).
  PISTE CAMÉRA : 0.00 à 0.30 arrivée (échelle 2,2 → 1, expo.out) ; dérive z +1,5 %/s de 0.30 à 3.30.
  COUCHES ET PROFONDEUR : avant-plan : reflet orange flou coupé par le bord bas droit ; sujet : la barre ; fond : scène sombre, halo orange, arc bleu en haut.
  OBJET-PONT ET VECTEUR : la barre de recherche (elle reviendra à la fin et deviendra le bouton : la rime).
  SON : key-press 0.10 à 1.40.
  IMAGE CLÉ : 1.20 : la barre leboncoin au centre, « voiture occas|ion » qui se tape, « Tu veux vivre de [l’automobile.] » en bas.

Scene 2 (1.70 à 3.80 s) : P2, le clic et la plongée
  TEXTE ÉCRAN : sous-titre « Alors tu te dis : [boîte : j’essaie.] » (Alors 1.75, tu 2.05, te 2.21, dis 2.36, boîte 2.88, j’essaie. 2.90) ; trois cartes de résultat : vignette de l'Audi grise « 86 900 € », vignette du Ford Ranger « 55 809 € », une troisième carte floue.
  IMAGE DE DÉPART : la barre posée, requête écrite.
  ÉTAPES : 2.40 le curseur arrive d'en bas à droite en une courbe (0,45 s power3.out) sur le bouton orange de recherche ; 2.90 clic (pression ×0,85 0,06 s, onde accent) sur « j’essaie » ; 3.00, 3.10, 3.20 les trois cartes tombent sous la barre en cascade (×1,15 flou 8 → net en 0,16 s chacune) ; 3.35 à 3.80 la caméra plonge dans la 1re carte (Audi).
  PISTE CAMÉRA : dérive z continue ; 3.35 à 3.80 poussée power3.in vers la 1re carte (échelle 1 → 4), flou 0 → 12 px.
  COUCHES ET PROFONDEUR : barre (haut, nette puis floue), cartes (sujet), scène sombre ; le curseur au-dessus de tout.
  OBJET-PONT ET VECTEUR : la 1re carte devient la page de l'annonce (frame 2), vecteur : poussée vers l'avant.
  SON : click 2.90 ; pop léger 3.00 ; whoosh-short 3.60.
  IMAGE CLÉ : 3.25 : la barre, le curseur juste après le clic, trois résultats en cascade, « Alors tu te dis : [j’essaie.] ».

## Frame 2: Ça coûte des mois, ta marge · 3.80 → 8.85

- scene: La vraie annonce Audi : une étiquette « Modèle : achat-revente » se tamponne ; la date « avant-hier » roule jusqu'à « il y a 3 mois » ; la caméra monte au prix : il est barré, le nouveau prix arrive trop grand et flou, « Baisse de prix » ; l'étiquette du prix se détache
- duration: 5.05s
- transition_in: cut
- status: outline
- src: compositions/frames/02-annonce.html
- voiceover: "Essayer un modèle… ça coûte des mois. Essayer une voiture… ça coûte ta marge."
- type: pain_point
- blueprint: device-surface-showcase (Adapt)
- focal: la date de l'annonce, puis le prix
- rules: coordinate-target-zoom, counting-dynamic-scale, motion-blur-streak
- world: dark
- handoff_in: à 0.00 : poussée power3.in en cours vers la 1re carte de résultat (vignette de l'Audi grise + « 86 900 € »), la carte couvre 120 % du cadre, flou 12 px ; scène sombre derrière ; aucun sous-titre ; grain 5 %
- handoff_out: à 5.05 : cadrage A1 sur l'annonce Audi (listing à l'échelle 2, le prix barré « 86 900 € » au centre-gauche), l'étiquette verte « 84 400 € » détachée de la page file vers le haut à droite (1800 px/s, flou de mouvement 10 px), panoramique caméra vers le haut-droite en cours (expo.in), aucun sous-titre ; grain 5 %

Word cues: Essayer@0.15 un@0.43 modèle@0.58 ça@1.34 coûte@1.51 des@1.68 mois@1.85 Essayer@2.57 une@2.87 voiture@3.02 ça@3.84 coûte@4.00 ta@4.16 marge@4.33

Scene 1 (0.00 à 2.55 s) : P3, le modèle et les mois
  TEXTE ÉCRAN : sous-titre « Essayer un modèle… ça coûte des [boîte : mois.] » (Essayer 0.15, un 0.43, modèle… 0.58, ça 1.34, coûte 1.51, des 1.68, boîte 1.83, mois. 1.85) ; sur la page : l'étiquette « Modèle : achat-revente » (Space Mono 24, contour accent, fond blanc) ; la date qui roule : « avant-hier à 12:11 » → « il y a 2 semaines » → « il y a 1 mois » → « il y a 3 mois ».
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 à 0.30 atterrissage sur l'annonce (composant listing, cadrage photos + titre, échelle 1,15, flou 12 → 0) ; 0.20 l'étiquette « Modèle : achat-revente » se tamponne à côté du titre (×1,4 flou 6 → net en 0,16 s, rotation -3°) ; 0.80 à 1.20 la caméra descend vers la ligne de date ; 1.30 la date commence à rouler (chaque libellé glisse vers le haut en 0,12 s, flou vertical 4 px) ; 1.85 « il y a 3 mois » se pose sur « mois » ; 2.00 à 2.55 tenue vivante (dérive).
  PISTE CAMÉRA : 0.00 à 0.30 expo.out ; 0.30 à 0.80 dérive x +12 px/s ; 0.80 à 1.20 descente expo.inOut jusqu'au cadrage de la date (échelle 1,6) ; dérive z +1 %/s ensuite.
  COUCHES ET PROFONDEUR : avant-plan : le bord flou de la photo de l'Audi en haut ; sujet : la ligne de date ; fond : la page blanche, la scène sombre aux bords.
  OBJET-PONT ET VECTEUR : la ligne de date mène au prix juste au-dessus (même page, un geste de caméra).
  SON : pop 0.20 (étiquette) ; key-press 1.30 à 1.85 (la date roule).
  IMAGE CLÉ : 1.95 : « il y a 3 mois » à la place de « avant-hier », l'étiquette « Modèle : achat-revente » floue au-dessus, « Essayer un modèle… ça coûte des [mois.] ».

Scene 2 (2.55 à 5.05 s) : P4, la voiture et la marge
  TEXTE ÉCRAN : sous-titre « Essayer une voiture… ça coûte ta [boîte : marge.] » (Essayer 2.57, une 2.87, voiture… 3.02, ça 3.84, coûte 4.00, ta 4.16, boîte 4.31, marge. 4.33) ; sur la page : le prix barré « 86 900 € », le nouveau prix « 84 400 € », la pastille « ↘ Baisse de prix · −2 500 € ».
  IMAGE DE DÉPART : la ligne de date au centre.
  ÉTAPES : 2.55 à 3.05 la caméra monte vers le prix (cadrage A1) ; 3.02 la photo de l'Audi glisse d'un cran (vignette suivante, 0,2 s) sur « voiture » ; 3.84 un trait accent barre « 86 900 € » (0,18 s) ; 4.05 le nouveau prix « 84 400 € » arrive trop grand et flou de la caméra (×1,6 flou 9 → ×1 net en 0,28 s, expo.out) et se pose à droite de l'ancien ; 4.33 pastille « Baisse de prix » (×1,2 flou 4 → net 0,14 s) ; 4.70 à 5.05 l'étiquette verte du nouveau prix se détache de la page et file vers le haut à droite (power3.in).
  PISTE CAMÉRA : 2.55 à 3.05 montée expo.inOut (échelle 1,6 → 2) ; dérive x +10 px/s ; 4.70 à 5.05 panoramique expo.in vers le haut-droite, flou 0 → 10 px.
  COUCHES ET PROFONDEUR : avant-plan : le nouveau prix flou en arrivée ; sujet : le prix barré ; fond : le titre de l'annonce, la page, la scène.
  OBJET-PONT ET VECTEUR : l'étiquette « 84 400 € » part vers le haut à droite : elle devient le solde de la frame 3.
  SON : pop 4.33 (nouveau prix) ; whoosh-short 4.75.
  IMAGE CLÉ : 4.40 : le prix barré d'orange, « 84 400 € » qui se pose, « Baisse de prix », « Essayer une voiture… ça coûte ta [marge.] » (styleframe A1).

## Frame 3: Ton épargne, et le gag · 8.85 → 14.00

- scene: Les annonces s'empilent en onglets (Ford Ranger, La Centrale) ; l'étiquette du prix tombe dans une carte « SOLDE ÉPARGNE » qui roule de 12 400 € à 4 150 € ; puis, en silence, le curseur hésite trois fois sur « Envoyer un message » de la Ford et ferme l'onglet ; la page se replie en une feuille
- duration: 5.15s
- transition_in: cut
- status: outline
- src: compositions/frames/03-onglets.html
- voiceover: "Essayer encore… ça coûte ton épargne."
- type: pain_point
- blueprint: overwhelm-surround (Adapt)
- focal: le solde, puis le curseur sur « Envoyer un message »
- rules: counting-dynamic-scale, cursor-click-ripple, card-morph-anchor
- world: dark
- handoff_in: à 0.00 : cadrage A1 sur l'annonce Audi (listing à l'échelle 2, le prix barré « 86 900 € » au centre-gauche), l'étiquette verte « 84 400 € » détachée de la page file vers le haut à droite (1800 px/s, flou de mouvement 10 px), panoramique caméra vers le haut-droite en cours (expo.in), aucun sous-titre ; grain 5 %
- handoff_out: à 5.15 : au centre, une feuille crème 760 × 980 (la page refermée), rotation -4°, flou 6 px, qui se pose en descendant (300 px/s, décélère) ; scène sombre, halo orange doux derrière ; aucun sous-titre ; grain 5 %

Word cues: Essayer@0.15 encore@0.45 ça@1.35 coûte@1.51 ton@1.66 épargne@1.82 (silence de 2.28 à 5.15 : le gag muet)

Scene 1 (0.00 à 2.30 s) : P5, encore, et l'épargne
  TEXTE ÉCRAN : sous-titre « Essayer encore… ça coûte ton [boîte : épargne.] » (Essayer 0.15, encore… 0.45, ça 1.35, coûte 1.51, ton 1.66, boîte 1.80, épargne. 1.82) ; barre d'onglets : « Audi RS Q8 4.0 V8… », « Ford Ranger WILDTRAK… », « La Centrale » ; carte « SOLDE ÉPARGNE » avec « 12 400 € » → « 4 150 € ».
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 à 0.25 fin du panoramique : la caméra recule (échelle 2 → 0,9), on voit la page entière de l'annonce Audi et une barre d'onglets au-dessus ; 0.30 la page Ford (réelle) glisse par-dessus en nouvel onglet (×1,15 flou 8 → net en 0,18 s) ; 0.70 la page d'accueil La Centrale glisse à son tour, puis la Ford repasse devant (0.95) ; 0.30 à 0.60 l'étiquette verte « 84 400 € » (de la frame 2) tombe en haut à droite dans la carte « SOLDE ÉPARGNE » (verre sombre) et s'y fond ; 1.35 à 1.82 le solde roule de « 12 400 € » à « 4 150 € » (chiffres tabulaires, léger rétrécissement) ; 1.82 boîte.
  PISTE CAMÉRA : 0.00 à 0.25 recul expo.out ; dérive x −15 px/s ; 1.30 à 1.60 léger cran vers la carte du solde (expo.out).
  COUCHES ET PROFONDEUR : avant-plan : la carte du solde (nette) en haut à droite ; sujet : la pile d'onglets ; fond : scène sombre.
  OBJET-PONT ET VECTEUR : l'étiquette du prix devient le solde.
  SON : pop 0.30 et 0.70 (onglets) ; key-press 1.60 à 1.90 (le solde roule).
  IMAGE CLÉ : 1.90 : trois onglets d'annonces, le solde tombé à « 4 150 € », « Essayer encore… ça coûte ton [épargne.] ».

Scene 2 (2.30 à 5.15 s) : P6, le gag muet, puis la page se referme
  TEXTE ÉCRAN : aucun sous-titre (silence) ; seuls les textes réels de la page Ford (carte vendeur floutée, « Envoyer un message », « Voir le numéro »).
  IMAGE DE DÉPART : la pile d'onglets, la Ford devant.
  ÉTAPES : 2.30 à 2.70 la caméra pousse sur la carte vendeur de la Ford (cadrage A2) ; 2.60 le curseur arrive en courbe sur « Envoyer un message » et s'arrête ; 3.00 il glisse de 60 px à gauche et s'arrête ; 3.40 il revient de 90 px à droite et s'arrête (les trois arrêts : c'est le gag, 0,4 s chacun, le bouton s'éclaire au survol puis s'éteint) ; 3.85 à 4.25 il part d'un geste vers le haut, vers la croix de l'onglet Ford (power3.out) ; 4.30 clic sur la croix (onde accent) ; 4.35 à 5.15 les trois onglets se ferment en cascade (0,1 s d'écart), la dernière page blanche se replie vers le centre en une feuille 760 × 980, son blanc tourne au crème, rotation -4°.
  PISTE CAMÉRA : 2.30 à 2.70 poussée expo.out (échelle 0,9 → 1,6) ; dérive z +1 %/s pendant les hésitations ; 3.85 à 4.25 recadrage vers le haut ; 4.35 à 5.15 la caméra suit la feuille qui descend vers le centre (power2.inOut).
  COUCHES ET PROFONDEUR : avant-plan : le curseur ; sujet : le bouton « Envoyer un message » ; fond : les photos floues de la Ford à gauche.
  OBJET-PONT ET VECTEUR : la page refermée devient la feuille du brouillon (frame 4).
  SON : aucun bruitage pendant les hésitations (silence voulu) ; click 4.30 ; whoosh-short 4.40.
  IMAGE CLÉ : 3.40 : le curseur arrêté sur « Envoyer un message », les traces de ses deux arrêts précédents, aucune voix (styleframe A2).

## Frame 4: Sans plan · 14.00 → 18.00

- scene: La feuille se pose : le brouillon de celui qui se lance seul s'écrit à la main (achat, contrôle, carte grise, baisse de prix), le total tombe, « Marge : − 650 € » en rouge, entouré ; « C'est de te lancer sans plan. » s'inscrit au centre
- duration: 4.00s
- transition_in: cut
- status: outline
- src: compositions/frames/04-brouillon.html
- voiceover: "Le problème, ce n’est pas de te lancer. C’est de te lancer sans plan."
- type: pain_point
- blueprint: typewriter-reveal (Adapt)
- focal: le brouillon, puis « − 650 € »
- rules: svg-path-draw, depth-of-field-blur
- world: dark
- handoff_in: à 0.00 : au centre, une feuille crème 760 × 980 (la page refermée), rotation -4°, flou 6 px, qui se pose en descendant (300 px/s, décélère) ; scène sombre, halo orange doux derrière ; aucun sous-titre ; grain 5 %
- handoff_out: à 4.00 : le brouillon entier au centre (échelle 0,85, rotation -4°), lignes de calcul et « − 650 € » entouré en rouge, bas de la feuille encore vide, recul caméra power3.out qui s'achève (dérive résiduelle z −1 %/s) ; stylo flou sorti par la droite ; aucun sous-titre ; halo orange derrière ; grain 5 %

Word cues: Le@0.15 problème@0.31 ce@0.80 n'est@0.96 pas@1.12 de@1.28 te@1.44 lancer@1.61 C'est@2.35 de@2.54 te@2.74 lancer@2.93 sans@3.32 plan@3.52

Scene 1 (0.00 à 2.00 s) : P7, le brouillon s'écrit
  TEXTE ÉCRAN : sous-titre « Le problème, ce n’est pas de te [boîte : lancer.] » (Le 0.15, problème, 0.31, ce 0.80, n’est 0.96, pas 1.12, de 1.28, te 1.44, boîte 1.59, lancer. 1.61) ; sur la feuille (Caveat) : « Essai n°2 — la voiture », « Achat ……… 11 800 », « Contrôle + pneus … 640 », « Carte grise, annonce … 310 », « Baisse de prix …… 900 ».
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 à 0.20 la feuille se pose (flou 6 → 0) ; 0.20 l'en-tête s'écrit (0,25 s, clip depuis la gauche, le stylo flou suit la pointe) ; 0.55 « Achat » ; 0.85 « Contrôle + pneus » ; 1.15 « Carte grise, annonce » ; 1.45 « Baisse de prix » ; 1.75 le trait de total se tire (0,2 s).
  PISTE CAMÉRA : dérive y −40 px/s (la caméra descend avec l'écriture), échelle 1,3.
  COUCHES ET PROFONDEUR : avant-plan : le stylo noir flou (composant pen) ; sujet : la ligne qui s'écrit ; fond : la feuille, la scène sombre et son halo orange.
  OBJET-PONT ET VECTEUR : le stylo, qui écrira aussi les questions de la frame 5.
  SON : key-press 0.20 à 1.60 (le stylo écrit, volume bas).
  IMAGE CLÉ : 1.60 : le brouillon à moitié écrit, le stylo flou, « Le problème, ce n’est pas de te [lancer.] ».

Scene 2 (2.00 à 4.00 s) : P8, la marge négative, et la phrase
  TEXTE ÉCRAN : moment typographique (84 px, centré dans le tiers bas de la feuille, sur un bandeau sombre) : « C’est de te lancer [boîte : sans plan.] » mot par mot (C’est 2.35, de 2.54, te 2.74, lancer 2.93, boîte 3.30, sans 3.32, plan. 3.52) avec [trait : sans plan] tiré de 3.32 à 3.67 ; aucun sous-titre en bas pendant ce temps ; sur la feuille : « Marge : » puis « − 650 € » en rouge stylo, entouré.
  IMAGE DE DÉPART : la feuille, total tiré.
  ÉTAPES : 2.00 « Marge : » s'écrit ; 2.30 « − 650 € » s'écrit en rouge (0,3 s) ; 2.65 un cercle rouge l'entoure (svg-path-draw 0,3 s) ; 2.35 à 3.52 la phrase arrive mot par mot (lettres qui convergent, 0,3 s) ; 3.40 à 4.00 recul de la caméra : la feuille entière.
  PISTE CAMÉRA : 2.00 à 3.40 dérive z +1 %/s sur la marge ; 3.40 à 4.00 recul power3.out (échelle 1,3 → 0,85).
  COUCHES ET PROFONDEUR : avant-plan : la phrase sur son bandeau ; sujet : « − 650 € » entouré ; fond : la feuille.
  OBJET-PONT ET VECTEUR : le bas vide de la feuille accueillera les trois questions.
  SON : pop 2.65 (le cercle) ; aucun autre.
  IMAGE CLÉ : 3.60 : la feuille, « − 650 € » entouré de rouge, « C’est de te lancer [sans plan.] » au centre avec son trait (styleframe C1).

## Frame 5: Les trois questions · 18.00 → 22.90

- scene: Au bas du brouillon, le stylo écrit trois questions sans réponse, chacune sur son mot : « Quel modèle ? », « Combien il me faut ? », « Combien je dois vendre ? » ; chaque point d'interrogation est repris en rouge ; puis la lumière s'éteint sur la feuille jusqu'au noir
- duration: 4.90s
- transition_in: cut
- status: outline
- src: compositions/frames/05-questions.html
- voiceover: "Sans savoir quel modèle te correspond. Combien il te faut. Combien tu dois vendre."
- type: pain_point
- blueprint: fixed-anchor-cycle (Adapt)
- focal: la question en cours
- rules: svg-path-draw, depth-of-field-blur
- world: dark
- handoff_in: à 0.00 : le brouillon entier au centre (échelle 0,85, rotation -4°), lignes de calcul et « − 650 € » entouré en rouge, bas de la feuille encore vide, recul caméra power3.out qui s'achève (dérive résiduelle z −1 %/s) ; stylo flou sorti par la droite ; aucun sous-titre ; halo orange derrière ; grain 5 %
- handoff_out: à 4.90 : noir total #000 et grain 5 % ; seuls les trois « ? » rouges (Caveat 600, 72 px, #d33a2c, halo rouge) aux points (880, 520), (960, 500), (1040, 520), qui convergent vers (960, 520) à 60 px/s ; aucun sous-titre

Word cues: Sans@0.10 savoir@0.28 quel@0.63 modèle@0.80 te@1.16 correspond@1.33 Combien@2.29 il@2.59 te@2.73 faut@2.88 Combien@3.38 tu@3.66 dois@3.80 vendre@3.95

Scene 1 (0.00 à 4.25 s) : P9 à P11, trois questions, trois crans
  TEXTE ÉCRAN : sous-titres successifs : « Sans savoir quel [boîte : modèle] te correspond. » (Sans 0.10, savoir 0.28, quel 0.63, boîte 0.78, modèle 0.80, te 1.16, correspond. 1.33) ; « Combien [boîte : il te faut.] » (Combien 2.29, boîte 2.57, il 2.59, te 2.73, faut. 2.88) ; « Combien tu dois [boîte : vendre.] » (Combien 3.38, tu 3.66, dois 3.80, boîte 3.93, vendre. 3.95) ; sur la feuille (Caveat) : « Quel modèle ? », « Combien il me faut ? », « Combien je dois vendre ? ».
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.30 « Quel modèle » s'écrit (0,4 s) ; 0.80 son « ? » en rouge ; 1.40 quatre mots griffonnés en petit autour (« achat-revente ? dépôt-vente ? courtage ? intermédiation ? »), puis raturés d'un trait rouge à 1.90 ; 2.29 « Combien il me faut » s'écrit ; 2.88 « ? » rouge ; 3.38 « Combien je dois vendre » s'écrit ; 3.95 « ? » rouge ; 4.10 trois « ? » rouges pulsent une fois (×1,1, 0,12 s).
  PISTE CAMÉRA : trois crans vers le bas (0.20, 2.15, 3.25 : 0,35 s expo.inOut chacun, la question en cours au centre), dérive z +1 %/s entre les crans.
  COUCHES ET PROFONDEUR : avant-plan : le stylo flou ; sujet : la question en cours ; fond : les calculs flous au-dessus (profondeur de champ).
  OBJET-PONT ET VECTEUR : la feuille, qui va s'éteindre.
  SON : key-press doux pendant l'écriture ; pop 0.80, 2.88, 3.95 (les « ? »).
  IMAGE CLÉ : 3.98 : trois questions sans réponse au bas du brouillon, trois « ? » rouges, « Combien tu dois [vendre.] ».

Scene 2 (4.25 à 4.90 s) : P12, la lumière s'éteint
  TEXTE ÉCRAN : le sous-titre sort à 4.25 ; rien d'autre.
  IMAGE DE DÉPART : la feuille et ses questions.
  ÉTAPES : 4.30 la lumière s'éteint d'un coup (0,12 s) : la feuille, le stylo et le halo passent au noir, SAUF les trois « ? » rouges qui restent allumés avec un halo ; 4.42 à 4.90 ils se détachent de la feuille et glissent vers le centre (72 px, droits).
  PISTE CAMÉRA : dérive z +2 %/s jusqu'au noir.
  COUCHES ET PROFONDEUR : la feuille seule, puis rien.
  OBJET-PONT ET VECTEUR : les trois « ? » rouges, qui fusionnent au centre au début de la frame 6.
  SON : whoosh 4.30 (extinction, volume bas).
  IMAGE CLÉ : 4.60 : la feuille à moitié avalée par l'ombre, les trois « ? » encore visibles.

## Frame 6: La bascule · 22.90 → 27.30

- scene: Noir. « Et si tu essayais… avec un plan ? » s'écrit seul au centre. Dans le silence, un point bleu s'allume, l'écran du GPS se dessine autour, « Itinéraire calculé · ton plan »
- duration: 4.40s
- transition_in: cut
- status: outline
- src: compositions/frames/06-bascule.html
- voiceover: "Et si tu essayais… avec un plan ?"
- type: pivot
- blueprint: titlecard-reveal (Adapt)
- focal: la question, puis le point bleu du GPS
- rules: kinetic-beat-slam, svg-path-draw
- world: dark
- handoff_in: à 0.00 : noir total #000 et grain 5 % ; seuls les trois « ? » rouges (Caveat 600, 72 px, #d33a2c, halo rouge) aux points (880, 520), (960, 500), (1040, 520), qui convergent vers (960, 520) à 60 px/s ; aucun sous-titre
- handoff_out: à 4.40 : écran GPS (composant gps) à l'échelle 0,92, centré, cartes et routes visibles, bandeau « Itinéraire calculé · ton plan » écrit, point de départ bleu à (330, 700) net, aucun itinéraire tracé, poussée caméra lente (+2 %/s) ; aucun sous-titre ; arc bleu en haut du cadre ; grain 5 %

Word cues: Et@0.62 si@0.76 tu@1.04 essayais@1.34 avec@2.36 un@2.65 plan@2.80 (silence de 2.94 à 4.40 : le GPS s'allume)

Scene 1 (0.00 à 3.10 s) : P13, la question sur noir
  TEXTE ÉCRAN : moment typographique (84 px, centré, y 500) : « Et si tu essayais… avec un [boîte : plan] ? » mot par mot (Et 0.62, si 0.76, tu 1.04, essayais… 1.34, avec 2.36, un 2.65, boîte 2.78, plan 2.80, ? 2.94) ; aucun sous-titre en bas.
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 à 0.50 les trois « ? » rouges convergent et fusionnent en un point rouge qui s'éteint à 0.60 ; chaque mot arrive par convergence de ses lettres (0,3 s expo.out) ; 1.80 à 2.30 « Et si tu essayais… » glisse de 40 px vers le haut pour faire place à la suite (0,4 s) ; 2.36 à 2.94 « avec un plan ? » ; la boîte de « plan » est la seule couleur de l'écran.
  PISTE CAMÉRA : dérive z +1 %/s (texture du grain qui bouge).
  COUCHES ET PROFONDEUR : la phrase seule sur noir.
  OBJET-PONT ET VECTEUR : la boîte orange de « plan » rétrécit en un point (0,2 s) qui tourne au bleu : le point de départ du GPS.
  SON : aucun (la voix seule).
  IMAGE CLÉ : 2.95 : noir, « Et si tu essayais… avec un [plan] ? » au centre.

Scene 2 (3.10 à 4.40 s) : P14, le GPS s'allume
  TEXTE ÉCRAN : bandeau du GPS « Itinéraire calculé · ton plan » (Instrument Sans 30, « ton plan » en accent est la seule exception : il est dans l'interface).
  IMAGE DE DÉPART : la phrase, et la boîte de « plan ».
  ÉTAPES : 3.10 la phrase sort (opacité 1 → 0, flou 0 → 6 px, 0,14 s) sauf la boîte qui se contracte en point (3.10 à 3.30) et devient le point bleu à anneau blanc (330, 700 dans l'écran) ; 3.40 à 3.90 le cadre de l'écran GPS se trace autour (svg-path-draw) ; 3.60 les routes apparaissent en dégradé depuis le point ; 3.90 le bandeau arrive (×1,1 flou 4 → net 0,14 s) ; 4.00 à 4.40 tenue vivante.
  PISTE CAMÉRA : 3.10 à 3.90 recul expo.out pour découvrir l'écran (échelle 1,6 → 0,92) ; dérive z +2 %/s ensuite.
  COUCHES ET PROFONDEUR : avant-plan : le reflet en biais sur la vitre ; sujet : le point bleu ; fond : la carte sombre, arc bleu en haut du cadre.
  OBJET-PONT ET VECTEUR : l'écran GPS continue en frame 7.
  SON : NOTIFICATION À DEUX TONS 3.40 (l'écran s'allume : la signature du film).
  IMAGE CLÉ : 4.10 : l'écran GPS dans la nuit, le point bleu, « Itinéraire calculé · ton plan ».

## Frame 7: Quelqu'un qui connaît le métier · 27.30 → 31.40

- scene: L'itinéraire orange se trace sur le GPS, d'un seul geste sûr ; la caméra plonge dans le point bleu, qui devient le halo du vrai portrait de Guillaume ; « Guillaume Herbin » se pose à côté
- duration: 4.10s
- transition_in: cut
- status: outline
- src: compositions/frames/07-metier.html
- voiceover: "Un plan fait par quelqu’un qui connaît le métier. Je m’appelle Guillaume Herbin."
- type: solution
- blueprint: spatial-pan-stations (Adapt)
- focal: la route, puis le portrait
- rules: svg-path-draw, scale-swap-transition
- world: dark
- handoff_in: à 0.00 : écran GPS (composant gps) à l'échelle 0,92, centré, cartes et routes visibles, bandeau « Itinéraire calculé · ton plan » écrit, point de départ bleu à (330, 700) net, aucun itinéraire tracé, poussée caméra lente (+2 %/s) ; aucun sous-titre ; arc bleu en haut du cadre ; grain 5 %
- handoff_out: à 4.10 : portrait réel à gauche (centre x 500, y 440, 660 px) avec son halo orange et bleu, nom « Guillaume Herbin » à droite (x 880, y 600, Montserrat 800 54 px), dérive caméra lente vers la droite (+20 px/s) ; sous-titre sorti ; fond sombre, arc bleu en haut ; grain 5 %

Word cues: Un@0.27 plan@0.42 fait@0.56 par@0.71 quelqu'un@0.85 qui@1.29 connaît@1.59 le@1.83 métier@1.94 Je@3.08 m'appelle@3.22 Guillaume@3.50 Herbin@3.77

Scene 1 (0.00 à 2.00 s) : P15, la route se trace
  TEXTE ÉCRAN : sous-titre « Un plan fait par quelqu’un » puis « qui connaît le [boîte : métier.] » (Un 0.27, plan 0.42, fait 0.56, par 0.71, quelqu’un 0.85 ; qui 1.29, connaît 1.59, le 1.83, boîte 1.92, métier. 1.94) avec [trait : métier] de 1.94 à 2.29 ; sur l'écran : bandeau, routes.
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.30 à 1.90 l'itinéraire orange se trace du point bleu (330, 700) vers le point d'arrivée (1590, 200) d'un seul geste (svg-path-draw, power2.inOut), lueur qui suit la pointe ; 0.90 et 1.40 les points intermédiaires s'allument au passage (anneaux accent, ×1,4 → ×1, 0,14 s) ; 1.90 le point d'arrivée s'allume.
  PISTE CAMÉRA : dérive x +25 px/s qui suit la pointe ; échelle 0,92 → 0,98.
  COUCHES ET PROFONDEUR : avant-plan : reflet de vitre ; sujet : la pointe de la route ; fond : la carte.
  OBJET-PONT ET VECTEUR : le point bleu de départ, dans lequel on plonge.
  SON : aucun (la voix).
  IMAGE CLÉ : 1.95 : la route orange tracée en entier sur le GPS, « qui connaît le [métier.] » souligné.

Scene 2 (2.00 à 4.10 s) : P16, Guillaume
  TEXTE ÉCRAN : sous-titre « Je m’appelle [boîte : Guillaume Herbin.] » (Je 3.08, m’appelle 3.22, boîte 3.48, Guillaume 3.50, Herbin. 3.77) ; nom « Guillaume Herbin » (Montserrat 800 54 px, « Herbin » en accent comme sur le bandeau).
  IMAGE DE DÉPART : la route tracée.
  ÉTAPES : 2.00 à 2.60 la caméra recule d'un cran puis plonge vers le point bleu (power3.in) ; 2.60 le point bleu à anneau blanc couvre le cadre et se change en l'anneau orange et bleu du portrait (scale-swap, 0,2 s) ; 2.80 le vrai portrait se pose dans l'anneau (×1,2 flou 8 → net 0,2 s), centre (500, 440), 660 px ; 3.50 « Guillaume » arrive (lettres qui convergent), 3.77 « Herbin » ; 3.80 à 4.10 tenue vivante.
  PISTE CAMÉRA : 2.00 à 2.60 plongée power3.in ; 2.60 à 2.90 atterrissage expo.out ; dérive x +20 px/s.
  COUCHES ET PROFONDEUR : avant-plan : particules orange floues coupées par le bord gauche ; sujet : le portrait ; fond : halo orange et bleu, arc bleu.
  OBJET-PONT ET VECTEUR : l'anneau du point GPS devient le halo du portrait.
  SON : whoosh-short 2.05.
  IMAGE CLÉ : 3.85 : le portrait de Guillaume dans son halo, « Guillaume Herbin » à droite, « Je m’appelle [Guillaume Herbin.] ».

## Frame 8: 21 ans, 3 000 € · 31.40 → 37.00

- scene: À côté du portrait, « 21 ANS » roule, puis « 3 000 € » ; « 2010 » en filigrane ; « Pas de formation. Pas d'expérience. » se posent en deux lignes ; whip vers la droite sur 2010
- duration: 5.60s
- transition_in: cut
- status: outline
- src: compositions/frames/08-preuve.html
- voiceover: "Je me suis lancé à vingt et un ans, avec trois mille euros en poche. Pas de formation. Pas d’expérience."
- type: proof
- blueprint: dataviz-countup (Adapt)
- focal: « 21 ANS », puis « 3 000 € »
- rules: counting-dynamic-scale, kinetic-beat-slam, motion-blur-streak
- world: dark
- handoff_in: à 0.00 : portrait réel à gauche (centre x 500, y 440, 660 px) avec son halo orange et bleu, nom « Guillaume Herbin » à droite (x 880, y 600, Montserrat 800 54 px), dérive caméra lente vers la droite (+20 px/s) ; sous-titre sorti ; fond sombre, arc bleu en haut ; grain 5 %
- handoff_out: à 5.60 : whip caméra vers la droite (3000 px/s, flou de mouvement horizontal 14 px), « 2010 » en Big Shoulders 800 blanc à x 960 y 470 qui entre dans le cadre ; portrait et chiffres sortis par la gauche ; aucun sous-titre ; grain 5 %

Word cues: Je@0.33 me@0.46 suis@0.59 lancé@0.73 à@0.99 vingt@1.12 et@1.25 un@1.39 ans@1.52 avec@1.84 trois@2.12 mille@2.26 euros@2.40 en@2.69 poche@2.83 Pas@3.52 de@3.67 formation@3.81 Pas@4.58 d'expérience@4.73

Scene 1 (0.00 à 3.40 s) : P17, les chiffres du départ
  TEXTE ÉCRAN : sous-titres : « Je me suis lancé à 21 ans, » (Je 0.33, me 0.46, suis 0.59, lancé 0.73, à 0.99, 21 1.12, ans, 1.52) puis « avec [boîte : 3 000 €] en poche. » (avec 1.84, boîte 2.10, 3 000 € 2.12, en 2.69, poche. 2.83) ; à l'écran : « 2010 » en filigrane (Big Shoulders 900, blanc 6 %), « 21 ANS » (blanc) et « 3 000 € » (accent), Big Shoulders 900, 170 px, empilés à droite du portrait (x 880).
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.30 le nom glisse vers le bas (y 600 → 640, 0,3 s) pour faire place ; 0.40 « 2010 » paraît en filigrane derrière ; 1.00 « 21 ANS » roule de 00 à 21 (0,25 s, arrive trop grand ×1,3 flou 6 → net) ; 2.05 « 3 000 € » roule de 0 à 3 000 (0,35 s) ; 2.83 tenue vivante.
  PISTE CAMÉRA : dérive x +20 px/s et z +1 %/s.
  COUCHES ET PROFONDEUR : avant-plan : particules floues ; sujet : les chiffres ; fond : le portrait (net, plus loin), le filigrane 2010.
  OBJET-PONT ET VECTEUR : le filigrane « 2010 » deviendra la 1re année de la frise.
  SON : pop 1.12 et 2.12 (les chiffres se posent).
  IMAGE CLÉ : 2.95 : le portrait, « 21 ANS » et « 3 000 € » empilés, « avec [3 000 €] en poche. » (styleframe C2 sans Kbis).

Scene 2 (3.40 à 5.60 s) : P18, ni formation, ni expérience
  TEXTE ÉCRAN : sous-titres « Pas de [boîte : formation.] » (Pas 3.52, de 3.67, boîte 3.79, formation. 3.81) puis « Pas [boîte : d’expérience.] » (Pas 4.58, boîte 4.71, d’expérience. 4.73) ; à l'écran sous les chiffres, deux lignes Space Mono 28 : « FORMATION : AUCUNE », « EXPÉRIENCE : AUCUNE ».
  IMAGE DE DÉPART : les chiffres posés.
  ÉTAPES : 3.52 « FORMATION : AUCUNE » se tape (0,25 s) ; 4.58 « EXPÉRIENCE : AUCUNE » se tape ; 5.00 tenue ; 5.30 à 5.60 whip vers la droite : le filigrane « 2010 » prend la lumière (blanc 100 %) et file vers le centre.
  PISTE CAMÉRA : dérive x +20 px/s ; 5.30 à 5.60 whip expo.in vers la droite, flou horizontal 0 → 14 px.
  COUCHES ET PROFONDEUR : sujet : les deux lignes ; fond : portrait, chiffres.
  OBJET-PONT ET VECTEUR : « 2010 » devient la 1re année de la frise (frame 9).
  SON : key-press 3.52 et 4.58 ; whoosh 5.30.
  IMAGE CLÉ : 4.90 : « 21 ANS · 3 000 € », « FORMATION : AUCUNE », « EXPÉRIENCE : AUCUNE », le portrait à gauche.

## Frame 9: Seize ans d'erreurs corrigées · 37.00 → 41.75

- scene: La frise 2010 → 2026 défile ; entre les années, des erreurs écrites à la main sont raturées d'un trait orange ; arrivée sur 2026 : la ligne continue, tourne à l'orange et devient l'itinéraire du GPS, pour « toi »
- duration: 4.75s
- transition_in: cut
- status: outline
- src: compositions/frames/09-frise.html
- voiceover: "J’ai appris en me trompant, pendant seize ans. Toi, tu peux commencer avec un plan."
- type: proof
- blueprint: camera-journey (Adapt)
- focal: l'erreur raturée en cours, puis la route
- rules: motion-blur-streak, svg-path-draw
- world: dark
- handoff_in: à 0.00 : whip caméra vers la droite (3000 px/s, flou de mouvement horizontal 14 px), « 2010 » en Big Shoulders 800 blanc à x 960 y 470 qui entre dans le cadre ; portrait et chiffres sortis par la gauche ; aucun sous-titre ; grain 5 %
- handoff_out: à 4.75 : écran GPS cadré à l'échelle 1, l'itinéraire orange tracé du point de départ bleu (330, 700) au point d'arrivée (1590, 200), aucune épingle allumée, poussée caméra lente vers le point de départ (+2 %/s) ; aucun sous-titre ; grain 5 %

Word cues: J'ai@0.14 appris@0.31 en@0.64 me@0.81 trompant@0.98 pendant@1.32 seize@1.65 ans@1.82 Toi@2.70 tu@3.26 peux@3.40 commencer@3.54 avec@3.97 un@4.26 plan@4.40

Scene 1 (0.00 à 2.70 s) : P19, la frise des erreurs
  TEXTE ÉCRAN : sous-titres « J’ai appris en me trompant, » (J’ai 0.14, appris 0.31, en 0.64, me 0.81, trompant, 0.98) puis « pendant [boîte : seize ans.] » (pendant 1.32, boîte 1.63, seize 1.65, ans. 1.82) ; frise : années 2010, 2012, 2014 … 2026 (Big Shoulders 800) ; erreurs (Caveat, encre douce) : « mauvais achat », « marge mal calculée », « charges oubliées ».
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 à 0.25 fin du whip, « 2010 » se pose (net) ; 0.30 « mauvais achat » s'écrit sous 2011 ; 0.98 il est raturé d'un trait accent (0,15 s) ; 1.05 « marge mal calculée » ; 1.30 rature ; 1.55 « charges oubliées » ; 1.80 rature ; 1.65 à 2.10 le compteur d'années au-dessus de la frise roule de 2010 à 2026 ; 2.10 à 2.70 la caméra ralentit et s'arrête sur 2026 (blanc).
  PISTE CAMÉRA : travelling x +900 px/s qui décélère (power2.out) de 0.25 à 2.70.
  COUCHES ET PROFONDEUR : avant-plan : années floues qui défilent plus vite (parallaxe) ; sujet : l'erreur en cours ; fond : la ligne de la frise, scène sombre.
  OBJET-PONT ET VECTEUR : la ligne de la frise devient la route.
  SON : pop 0.98, 1.30, 1.80 (ratures) ; whoosh-short 0.05.
  IMAGE CLÉ : 1.85 : trois erreurs raturées sur la frise, le compteur à 2026, « pendant [seize ans.] ».

Scene 2 (2.70 à 4.75 s) : P20, toi, avec un plan
  TEXTE ÉCRAN : sous-titres « Toi, » (2.70) puis « tu peux commencer [boîte : avec un plan.] » (tu 3.26, peux 3.40, commencer 3.54, boîte 3.95, avec 3.97, un 4.26, plan. 4.40).
  IMAGE DE DÉPART : arrêt sur 2026.
  ÉTAPES : 2.70 au bout de la frise, un point bleu à anneau blanc se pose après 2026 (×1,4 → ×1, 0,14 s) : « toi » ; 3.26 à 4.40 la ligne de la frise repart de ce point, tourne à l'orange et monte en courbe (svg-path-draw) ; 3.80 les routes du GPS apparaissent autour (dégradé) ; 4.40 le cadre de l'écran GPS est complet, la frise a disparu.
  PISTE CAMÉRA : 2.70 à 3.20 arrêt et léger recul ; 3.20 à 4.75 la caméra suit la route qui monte (power2.inOut) puis recule jusqu'au cadrage de l'écran entier (échelle 1).
  COUCHES ET PROFONDEUR : sujet : la pointe de la route ; fond : frise qui s'éteint, carte qui s'allume.
  OBJET-PONT ET VECTEUR : la route, qui porte les étapes de la frame 10.
  SON : pop 2.70 (le point « toi »).
  IMAGE CLÉ : 4.45 : l'écran GPS, l'itinéraire orange complet né de la frise, le point bleu de départ, « tu peux commencer [avec un plan.] ».

## Frame 10: Ta situation, ton modèle · 41.75 → 44.80

- scene: Sur le GPS, l'épingle « Ta situation » s'allume au départ ; travelling le long de la route jusqu'au 2e point : quatre modèles se déploient, trois sont tranchés d'un trait, « Ton modèle » s'allume
- duration: 3.05s
- transition_in: cut
- status: outline
- src: compositions/frames/10-situation.html
- voiceover: "On part de ta situation. On tranche le modèle."
- type: demo
- blueprint: spatial-pan-stations (Adapt)
- focal: l'épingle en cours
- rules: coordinate-target-zoom, motion-blur-streak
- world: dark
- handoff_in: à 0.00 : écran GPS cadré à l'échelle 1, l'itinéraire orange tracé du point de départ bleu (330, 700) au point d'arrivée (1590, 200), aucune épingle allumée, poussée caméra lente vers le point de départ (+2 %/s) ; aucun sous-titre ; grain 5 %
- handoff_out: à 3.05 : caméra en travelling le long de l'itinéraire vers le 3e point « Tes chiffres » (1230, 330), mi-course, flou de mouvement 8 px, épingles « Ta situation » et « Ton modèle » allumées en accent derrière ; aucun sous-titre ; grain 5 %

Word cues: On@0.31 part@0.49 de@0.66 ta@0.84 situation@1.01 On@1.93 tranche@2.08 le@2.23 modèle@2.38

Scene 1 (0.00 à 1.75 s) : P21, ta situation
  TEXTE ÉCRAN : sous-titre « On part de ta [boîte : situation.] » (On 0.31, part 0.49, de 0.66, ta 0.84, boîte 0.99, situation. 1.01) ; épingle « Ta situation ».
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.31 la caméra est au départ ; 0.60 l'épingle « Ta situation » arrive (×1,3 flou 4 → net 0,14 s) ; 1.01 elle se remplit d'accent (glow) ; 1.20 à 1.75 tenue vivante (la lueur du point bleu tourne une fois).
  PISTE CAMÉRA : 0.00 à 0.35 fin de la poussée (échelle 1 → 1,6 sur le départ, expo.out) ; dérive x +15 px/s.
  COUCHES ET PROFONDEUR : avant-plan : reflet ; sujet : l'épingle ; fond : la route floue qui part.
  OBJET-PONT ET VECTEUR : la route, que la caméra suit.
  SON : pop 1.01.
  IMAGE CLÉ : 1.40 : l'épingle « Ta situation » allumée au départ de la route (styleframe B3).

Scene 2 (1.75 à 3.05 s) : P22, on tranche le modèle
  TEXTE ÉCRAN : sous-titre « On tranche le [boîte : modèle.] » (On 1.93, tranche 2.08, le 2.23, boîte 2.36, modèle. 2.38) ; quatre étiquettes autour du 2e point : « Achat-revente », « Dépôt-vente », « Courtage », « Intermédiation » ; épingle « Ton modèle ».
  IMAGE DE DÉPART : l'épingle « Ta situation » allumée.
  ÉTAPES : 1.75 à 2.05 travelling vers le 2e point ; 1.95 les quatre étiquettes se déploient en éventail autour du point (0,05 s d'écart, ×1,2 flou → net) ; 2.08 sur « tranche », trois sont tranchées d'un trait accent et s'éteignent (0,05 s d'écart), une seule reste, sans nom lisible (floue) ; 2.38 l'étiquette restante se change en l'épingle « Ton modèle » allumée ; 2.60 à 3.05 la caméra repart le long de la route vers le 3e point.
  PISTE CAMÉRA : 1.75 à 2.05 travelling expo.inOut ; 2.60 à 3.05 travelling expo.in, flou 0 → 8 px.
  COUCHES ET PROFONDEUR : sujet : les étiquettes ; fond : la route et l'épingle 1 floue.
  OBJET-PONT ET VECTEUR : le travelling continue en frame 11.
  SON : pop 2.08 ; whoosh-short 2.70.
  IMAGE CLÉ : 2.45 : trois modèles tranchés, l'épingle « Ton modèle » allumée sur la route.

## Frame 11: Les vrais chiffres, moins de casse · 44.80 → 48.85

- scene: Au 3e point, la caméra plonge dans l'anneau et arrive sur la vraie page « Ton point d'équilibre » du plan : la ligne « Ventes nécessaires » est cerclée d'orange ; puis les cadrans du tableau de bord : la jauge épargne remonte de la réserve, le compteur de mois perdus revient à 00
- duration: 4.05s
- transition_in: cut
- status: outline
- src: compositions/frames/11-chiffres.html
- voiceover: "On pose les vrais chiffres. Moins de casse. Moins de temps perdu."
- type: demo
- blueprint: device-surface-showcase (Adapt)
- focal: la ligne « Ventes nécessaires », puis la jauge
- rules: coordinate-target-zoom, counting-dynamic-scale, svg-path-draw
- world: dark
- handoff_in: à 0.00 : caméra en travelling le long de l'itinéraire vers le 3e point « Tes chiffres » (1230, 330), mi-course, flou de mouvement 8 px, épingles « Ta situation » et « Ton modèle » allumées en accent derrière ; aucun sous-titre ; grain 5 %
- handoff_out: à 4.05 : le point d'arrivée de l'itinéraire (disque accent 44 px) au centre, poussée caméra power3.in en cours vers lui (il couvre 30 % du cadre), flou 6 px, route orange floue derrière ; aucun sous-titre ; grain 5 %

Word cues: On@0.11 pose@0.31 les@0.51 vrais@0.72 chiffres@0.92 Moins@1.88 de@2.05 casse@2.22 Moins@2.81 de@2.97 temps@3.12 perdu@3.28

Scene 1 (0.00 à 1.75 s) : P23, les vrais chiffres
  TEXTE ÉCRAN : sous-titre « On pose les vrais [boîte : chiffres.] » (On 0.11, pose 0.31, les 0.51, vrais 0.72, boîte 0.90, chiffres. 0.92) ; la vraie page du plan (composant plan).
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 à 0.25 arrivée sur le 3e point ; 0.25 à 0.55 la caméra traverse l'anneau, qui s'agrandit et cadre la page « Ton point d'équilibre » (×3 flou 10 → net) ; 0.92 l'anneau accent se trace autour de « Ventes nécessaires par mois … 2 » (0,3 s) ; 1.20 à 1.75 dérive lente sur la ligne.
  PISTE CAMÉRA : 0.25 à 0.55 plongée power3.in puis atterrissage expo.out ; dérive z +1 %/s.
  COUCHES ET PROFONDEUR : avant-plan : une étiquette verte « 84 400 € » floue qui traverse (rappel de l'acte 1) ; sujet : la ligne cerclée ; fond : couverture et 3e page floues.
  OBJET-PONT ET VECTEUR : vecteur recul vers les cadrans.
  SON : pop 0.92.
  IMAGE CLÉ : 1.30 : la page du plan, « Ventes nécessaires par mois … 2 » cerclée d'orange, « On pose les vrais [chiffres.] » (styleframe A3).

Scene 2 (1.75 à 4.05 s) : P24, moins de casse, moins de temps perdu
  TEXTE ÉCRAN : sous-titres « [boîte : Moins de casse.] » (boîte 1.86, Moins 1.88, de 2.05, casse. 2.22) avec [trait : moins de casse] de 1.88 à 2.23, puis « Moins de [boîte : temps perdu.] » (Moins 2.81, de 2.97, boîte 3.10, temps 3.12, perdu. 3.28) ; cadrans : jauge « ÉPARGNE », compteur « 00 mois perdus ».
  IMAGE DE DÉPART : la page du plan.
  ÉTAPES : 1.75 à 2.00 la page s'éloigne et les cadrans du tableau de bord (composant dashboard, de nuit) entrent du bas ; 2.05 l'aiguille de la jauge « ÉPARGNE » quitte la réserve et remonte au milieu (0,4 s power3.out), le voyant € s'éteint ; 2.81 le compteur « 03 » roule à l'envers jusqu'à « 00 » (0,3 s) sur « temps perdu » ; 3.40 à 3.60 tenue ; 3.60 à 4.05 la caméra recule : l'écran GPS reprend le cadre, la caméra pousse vers le point d'arrivée de la route.
  PISTE CAMÉRA : 1.75 à 2.00 recul expo.out ; dérive x +15 px/s ; 3.60 à 4.05 poussée power3.in vers le point d'arrivée.
  COUCHES ET PROFONDEUR : avant-plan : cadran gauche flou ; sujet : l'aiguille, puis le compteur ; fond : arc bleu.
  OBJET-PONT ET VECTEUR : le point d'arrivée de la route devient la barre de recherche (frame 12).
  SON : ping 1.88 ; key-press 2.81 à 3.10 (le compteur roule) ; whoosh-short 3.60.
  IMAGE CLÉ : 3.35 : la jauge épargne remontée, le compteur à « 00 mois perdus », « Moins de [temps perdu.] ».

## Frame 12: Ta prochaine étape · 48.85 → 56.80

- scene: Le point d'arrivée s'étire et redevient la barre de recherche du début ; la requête « voiture occasion » s'efface ; la barre se change en bouton « Voir si mon profil correspond » ; un curseur arrive et clique directement ; tenue vivante ; noir
- duration: 7.95s
- transition_in: cut
- status: outline
- src: compositions/frames/12-fin.html
- voiceover: "Tu n’as pas besoin de tout savoir. Juste ta prochaine étape."
- type: cta
- blueprint: cta-morph-press (Adapt)
- focal: la barre, puis le bouton
- rules: cursor-click-ripple, card-morph-anchor, press-release-spring
- world: dark
- handoff_in: à 0.00 : le point d'arrivée de l'itinéraire (disque accent 44 px) au centre, poussée caméra power3.in en cours vers lui (il couvre 30 % du cadre), flou 6 px, route orange floue derrière ; aucun sous-titre ; grain 5 %
- handoff_out: aucun (fin du film, noir à 7.95)

Word cues: Tu@0.41 n'as@0.58 pas@0.74 besoin@0.91 de@1.24 tout@1.40 savoir@1.57 Juste@2.26 ta@2.93 prochaine@3.06 étape@3.33 (tenue jusqu'à 7.95)

Scene 1 (0.00 à 2.10 s) : P25, la barre revient
  TEXTE ÉCRAN : sous-titre « Tu n’as pas besoin de [boîte : tout savoir.] » (Tu 0.41, n’as 0.58, pas 0.74, besoin 0.91, de 1.24, boîte 1.38, tout 1.40, savoir. 1.57) ; la barre de recherche avec « voiture occasion » qui s'efface.
  IMAGE DE DÉPART : handoff_in.
  ÉTAPES : 0.00 à 0.30 le disque accent s'étire en pilule et devient la barre de recherche du début (card-morph, 0,3 s expo.out), avec la même requête « voiture occasion » ; 0.85 à 1.55 la requête s'efface caractère par caractère (0,04 s par caractère), caret accent ; 1.60 à 2.10 champ vide, le caret clignote (2 pas).
  PISTE CAMÉRA : 0.00 à 0.30 atterrissage expo.out ; dérive z +1,5 %/s.
  COUCHES ET PROFONDEUR : avant-plan : arcs orange et bleu du bandeau qui traversent en bas ; sujet : la barre ; fond : le plan de lancement très flou.
  OBJET-PONT ET VECTEUR : la barre devient le bouton.
  SON : key-press 0.85 à 1.55.
  IMAGE CLÉ : 1.30 : la barre du début à moitié effacée, « Tu n’as pas besoin de [tout savoir.] ».

Scene 2 (2.10 à 4.20 s) : P26, le bouton
  TEXTE ÉCRAN : sous-titre « Juste ta prochaine [boîte : étape.] » (Juste 2.26, ta 2.93, prochaine 3.06, boîte 3.31, étape. 3.33) ; au-dessus du bouton, micro « TA PROCHAINE ÉTAPE » ; le bouton « Voir si mon profil correspond » ; dessous, « 5 questions · 2 minutes · aucun paiement à ce stade » et « guillaumeherbin.fr/accompagnement ».
  IMAGE DE DÉPART : la barre vide.
  ÉTAPES : 2.26 la barre se remplit d'accent et se change en bouton (card-morph, 0,3 s) ; 2.60 le libellé « Voir si mon profil correspond » arrive (×1,1 flou 4 → net) ; 3.06 « TA PROCHAINE ÉTAPE » se tape au-dessus ; 3.40 la ligne « 5 questions · 2 minutes · aucun paiement à ce stade » arrive ; 3.70 l'URL se tape.
  PISTE CAMÉRA : dérive z +1 %/s ; 2.20 à 2.60 léger recul expo.out pour faire place aux lignes.
  COUCHES ET PROFONDEUR : sujet : le bouton ; fond : plan flou, arcs.
  OBJET-PONT ET VECTEUR : le curseur de l'accroche revient.
  SON : pop 2.35.
  IMAGE CLÉ : 3.90 : le bouton « Voir si mon profil correspond » et ses deux lignes, « Juste ta prochaine [étape.] » (styleframe C3).

Scene 3 (4.20 à 7.95 s) : P27, le clic et la tenue
  TEXTE ÉCRAN : le sous-titre sort à 4.20 ; le bouton, ses lignes.
  IMAGE DE DÉPART : le bouton posé.
  ÉTAPES : 4.40 le curseur arrive d'en bas à droite en UNE courbe (0,45 s power3.out) et clique directement à 4.85 (pression ×0,85 0,06 s, onde accent, état pressé en 3 couleurs : accent → accent-deep → accent) ; 5.00 à 7.40 tenue vivante : les arcs orange et bleu glissent lentement, le plan flou derrière dérive, la lueur du bouton se déplace d'un bord à l'autre une fois ; 7.40 à 7.95 sortie au noir (fondu voulu 2 sur 2).
  PISTE CAMÉRA : dérive z +0,8 %/s jusqu'au noir.
  COUCHES ET PROFONDEUR : avant-plan : le curseur ; sujet : le bouton ; fond : plan flou, arcs.
  OBJET-PONT ET VECTEUR : aucun (fin).
  SON : click 4.85.
  IMAGE CLÉ : 5.20 : le bouton pressé, l'onde accent, le curseur dessus.
