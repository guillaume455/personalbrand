---
titre: Passage de la grille de contrôle (STORYBOARD-CRAFT.md, section 5) sur le storyboard v7a
date: 2026-09-29
fichiers: STORYBOARD.md, frame.md, reference/devis-decor.html
---

# Grille de contrôle du storyboard v7a

Verdicts : **tenu**, **tenu après correction** (l'écart a été trouvé par la grille et corrigé dans STORYBOARD.md ou
frame.md), **non tenu** (écart restant, avec sa raison). Temps globaux sauf mention « local ».

## Vérifications mécaniques

- Parseur du pipeline (`scripts/lib/storyboard.mjs`) : 10 séquences, durée totale 43.20 s, 0 avertissement.
- Paquets des sous-agents (`scripts/frame-packets.mjs`, sortie hors projet) : 10 paquets de 24,2 à 42,4 Ko, tous sous
  la limite de 48 Ko ; chaque paquet embarque exactement le blueprint et les règles voulus (aucune règle citée par
  accident dans le texte).
- Blueprints et règles : tous existent dans `hyperframes-animation/` (camera-journey, overwhelm-surround,
  agent-progress-theater, prompt-type-submit-generate, fixed-anchor-cycle, titlecard-reveal, dataviz-countup,
  cta-morph-press ; depth-of-field-blur, coordinate-target-zoom, svg-path-draw, kinetic-beat-slam, card-morph-anchor,
  waterfall-entry, motion-blur-streak, cursor-click-ripple, scale-swap-transition, css-marker-patterns,
  counting-dynamic-scale, stat-bars-and-fills, press-release-spring).
- Passages de relais : un script compare le `handoff_out` de chaque séquence au `handoff_in` de la suivante : les 8
  coutures caméra sont identiques caractère pour caractère ; la coupe 14.02 porte un raccord de position écrit des deux
  côtés (iPhone éteint 594 × 1234 px, centre x 1010, haut y 127).
- Caméra : la fonction de projection `dvProject` a été vérifiée contre le DOM de Chromium (écart de 1 px au plus) ;
  tous les états `cam(...)` du storyboard ont été rendus dans le banc d'essai et cadrent ce qui est annoncé.
- Géométrie du zéro : l'encre du « 0 » de Space Mono dans la case TOTAL a été mesurée (centre (1235, 1812), 37 × 52 u) ;
  ce glyphe a un point central, donc le zéro final est un anneau SVG (écrit dans frame.md et dans la séquence 9).
- Aucun tiret cadratin ni demi-cadratin dans STORYBOARD.md, frame.md et reference/devis-decor.html.

## Les 15 points

**1. En-tête (monde, fonds texturés, couleurs de rôle, signatures datées, registres) : tenu.**
Section « Video direction » : MONDE avec les coordonnées des stations par acte (mot « site » (750, 684), cellule 4
(1240, 1275), ancre des fenêtres (1180, 900), zéro (1235, 1812)), fonds texturés (grain du papier, grain d'image,
graduations de la frise, vagues de la carte de fin), couleurs de rôle ; SIGNATURES avec 6 et 5 occurrences datées ;
trois registres de texte, un mouvement chacun ; rimes.

**2. Piste caméra dans chaque plan (dérive chiffrée, événements datés avec cible, jamais d'arrêt de plus de 0,5 s) : tenu.**
Chaque Scene a une ligne PISTE CAMÉRA avec la dérive en u/s et %/s et chaque cran avec son état cible `cam(...)`.
La partition globale est récapitulée en tête.

**3. Aucun trou de plus de 1 s entre deux étapes (0,3 s dans les 3 premières secondes) : tenu après correction.**
- La grille a trouvé un trou de 1,04 s dans la carte de fin (local 0.60 à 1.64) : ajout du resserrement des vagues à
  1.10 et du resserrement des lettres à 1.40.
- Elle a aussi trouvé un trou de 1,3 s dans la tenue finale : ajout du curseur qui s'écarte (5.20) et du reflet sur
  les vagues (5.30).
- Dans l'accroche, l'écart maximal entre deux étapes est de 0,26 s (0.78 à 1.04).

**4. Apparitions de 0,2 s au plus ; dérives d'au moins 1 s ; zone 0,3 à 0,9 s réservée à la caméra et au curseur, en expo, power3 ou power4 : tenu après correction, avec deux exceptions.**
Corrigé dans frame.md :
- mot à mot 0,3 → 0,2 s ;
- tracé de pastille 0,28 → 0,2 s, avec la rotation dans le même temps ;
- pastille géante 0,36 → 0,2 s ;
- convergence de l'écho 0,4 → 0,2 s ;
- prix qui tombe 0,26 → 0,2 s ;
- barre de « TOI. » 0,26 → 0,2 s.

Corrigé dans le storyboard :
- cadre de sélection 0,3 → 0,2 s ;
- cadre de la ligne 5 0,3 → 0,2 s ;
- portail qui se referme 0,3 → 0,2 s ;
- traînée de la ligne 5 0,46 s → trait de 0,18 s puis extinction linéaire ;
- remplissage du zéro 0,3 → 0,2 s ;
- flash 0,42 → 0,2 s ;
- pose du devis clair 0,3 s → 0,12 s puis recul lent ;
- ombre du devis en vol 0,5 s → traversée linéaire de 0,98 s ;
- point lumineux des tuiles 0,4 s → trois bonds de 0,12 s ;
- aplatissement sur le zéro et iris final, de power2 vers power3.

Exceptions assumées :
- (a) Dans l'accroche, le plan « dans le vrai site » dure 0,78 s : sa dérive ne peut pas atteindre 1 s. Les plans de
  l'accroche gardent le même vecteur de dérive d'un plan à l'autre.
- (b) « Stop. » (0,3 s) n'a pas de dérive mais un coup d'appareil, puis les échos qui dérivent.

**5. Chaque tenue de plus de 0,5 s nomme sa couche vivante, aucune image figée, fin comprise : tenu.**
Chaque tenue est nommée :
- tenue de la ligne 2 (5.40) : dérive et grain ;
- attente WhatsApp : bulles et poussée ;
- écran verrouillé plein (13.45 à 14.02) : pile qui glisse et poussée ;
- silence de la ligne 5 : dérive, extinction de la traînée ;
- « libre. » : dérive de la pastille, ombre qui passe ;
- fin : vagues, halo, reflet, puis iris.

**6. Chaque jonction nomme son objet-pont ou son vecteur, zéro dédoublement : tenu.**
Chaque Scene a sa ligne OBJET-PONT ET VECTEUR ; entre séquences, le vecteur est porté par le handoff (état + vitesse).

Les objets-ponts :
- portail → site ;
- cellule 4 → iPhone ;
- iPhone WhatsApp → écran verrouillé → iPhone éteint derrière « Stop. » ;
- devis → notification Gmail ;
- point de « Stop. » → lumière ;
- bulle → texte du champ de Claude ;
- « TOI. » → pastille « toi » ;
- zéro → portail vers la carte de fin.

Aucun objet n'est à l'écran deux fois : le prix en vol disparaît dans l'image où celui de la cellule apparaît, et la
bulle devient le texte du champ. Les trois couches du devis et les copies de traînée sont déclarées comme un seul
objet (frame.md, négatifs).

**7. Deux transitions « effet » au plus : tenu.**
Une seule : le flash de lumière de 14.40, qui part du point de « Stop. ». Les relais sous le flou de la plongée
(1.62 et 2.54) font partie de la signature 2 (même objet, autre échelle) ; toutes les autres jonctions sont des
mouvements de caméra.

**8. Coupes franches au quota de la voix, avec leur ligne « t, premier mot, raison » : tenu.**
Voix narrative, une seule coupe : 14.02, dans le silence après « technique », changement d'acte (douleur vers
solution, monde sombre vers monde clair), musique coupée dans le mix. La sortie du zéro (36.68) se fait sur un noir
uni : invisible, ce n'est pas une coupe.

**9. Chaque entrée d'élément principal a un état de départ écrit (×1,1 à ×6 + flou, ou un point), aucun fondu à taille finale : tenu après correction.**
États de départ ajoutés :
- la lumière d'ouverture naît d'un point ;
- « 02 », sous-lignes et quantités, badge « ERREUR » ;
- puces et bulles WhatsApp, notifications ;
- bulle et tâches de Claude, fenêtre Safari, étiquette « AJOUTÉ À L’INSTANT » ;
- « maintenant », « 05 » ;
- lettres du mot-symbole, « 2.0 », url, bouton.

**10. Écart de chaque mot-image, changement de composition sur le premier mot de l'idée ou dans un silence, chaque silence de plus de 0,4 s écrit comme un plan : tenu après correction.**

Avances ajoutées :

| Mot-image | Image | Avance |
|---|---|---|
| « site » | le portail s'ouvre | 0,12 s |
| « journée » | la sélection, puis l'étiquette « 1 JOUR DE TRAVAIL » | 0,18 s et 0,1 s |
| « mille euros » | l'ombre du prix | 0,16 s |
| « années » | la frise | 0,1 s |
| « une ligne » | le cadre de la ligne 5 | 0,18 s |

Avances qui étaient déjà là :

| Mot-image | Image | Avance |
|---|---|---|
| « six cents euros » | ombre | 0,28 s |
| « Délai » | la cellule s'ouvre | 0,28 s |
| « l'IA » | fenêtre Claude | 0,44 s |
| « expliques » | bulle | 0,22 s |
| « fait » | bouton | 0,38 s |
| « libre » | envol du devis | 0,26 s |
| « zéro » | le total roule | 0,18 s |

Impacts à ± 0,1 s (règle des verbes d'impact) : « planté », « sur devis », « Toi » ×3, la tâche cochée sur « faire ».

Changements de composition recalés :
- cran latéral déplacé de 0.62 à 0.68 (posé sur « sur ») ;
- gros plan sur l'iPhone déplacé de 10.04 à 9.62 (posé sur « quand ») ;
- vol de la bulle requalifié en suivi du même sujet (pas de nouveau plan) ;
- permutation Claude vers Safari placée dans le silence avant « Elle » ;
- aplatissement sur le zéro placé dans le silence après « zéro ».

Les 8 silences de plus de 0,4 s sont listés en tête avec leur action.

**11. Au moins 3 verbes joués physiquement, contact à ± 0,1 s : tenu.**

| Verbe | Action physique | Contact | Mot |
|---|---|---|---|
| « planté » | la tuile Make tremble et casse | 7.26 | 7.28 |
| « sur devis » | le tampon s'écrase | 7.80 | 7.78 |
| « faire » | la deuxième tâche se coche | 16.36 | 16.36 |
| « expliques » | la bulle se tape | à partir de 17.52 | 17.68 |
| « partent de zéro » | les totaux roulent | 34.46 à 35.02 | |

**12. La moitié des plans à 3 niveaux, une parallaxe par acte, chaque géant devant ou derrière un objet : tenu après correction.**
- **3 niveaux** : 25 plans sur 27 ont avant-plan flou, sujet net et fond. Pour le devis, les trois couches de
  profondeur de champ le donnent partout. Les deux plans qui ne l'ont pas sont « Stop. » et le montage de la carte de fin.
- **Parallaxe** :
  - acte 1 : panoramique des années en 3 vitesses (3, 1 et 0,35) ;
  - acte 2 : survol incliné de 44° à 28° ;
  - acte 3 : vagues à 0,5.
- **Géants** :
  - « aujourd’hui, » derrière la fenêtre Claude ;
  - « TOI. » devant le devis, sur la ligne qu'il barre ;
  - « libre. » sous l'ombre du devis qui vole.
- **Correction** : la grille a trouvé « Stop. » seul sur du noir. Il se pose maintenant DEVANT l'iPhone à l'écran
  éteint, à la place exacte où la séquence 3 le laisse. Ça renforce aussi l'idée : tout s'est arrêté.

**13. Couches animées : régime au moins 2, pic 3 à 4, un seul élément actif : tenu.**
Le régime courant est la dérive de caméra plus un élément actif ; les pics à 3 sont nommés dans les lignes COUCHES
(ombre + prix + caméra à 4.72, tuile + badge + caméra à 7.26, cascade + secousse + caméra à 12.6, curseur + bouton
+ onde à 41.35).

**14. Rime : le mécanisme de l'accroche rejoué à l'identique avant la fin : tenu.**
La plongée dans le zéro (35.90) rejoue la plongée dans le mot « site » (1.30) : même aplatissement, même courbe
power3.in, même relais par un calque écran. L'anneau du bouton du site (19.70) est rejoué sur le bouton de fin
(39.63). Le total gonflé à l'aller retombe à zéro.

**15. Fin : geste qui rassemble le film, curseur qui hésite au moins 0,8 s puis clique (3 couleurs, onde), 2 à 3 s de tenue vivante, sortie en iris ou au noir : non tenu sur un seul sous-point.**
- **Tenu** :
  - le tunnel des interfaces du film dans le trou du zéro (36.00 à 36.60) rassemble le film ;
  - le curseur entre en courbe, touche, recule, s'arrête, revient : 0,82 s d'hésitation ;
  - le clic se fait en 3 couleurs (#e08a5c, #fffdf9, #c25b28), avec l'onde, et le bouton se remplit de terracotta ;
  - la sortie se fait en iris noir sur le bouton.
- **Non tenu** : la tenue vivante après le clic dure 1,49 s (plus 0,3 s d'iris), pas 2 à 3 s. Le clic est verrouillé
  à 41.35 dans le mix M1, déjà bruité, et le film finit à 43.20 : il reste au plus 1,85 s. Pour tenir le point, il
  faudrait remixer en avançant le bruitage du clic vers 40.6 (et donc l'hésitation). À décider par Colin : « mêmes
  bruitages que la v6 » l'interdit aujourd'hui.

## Limites connues

- Les fins de mots (donc les bornes des silences) sont estimées depuis le minutage des débuts de mots de
  DIRECTIONS.md ; une transcription horodatée mot par mot (Whisper) les fixerait au centième.
- Les bruitages du mix M1 ont été posés pour la v6 : l'image v7a se cale dessus (liste en tête du storyboard). Deux
  gestes n'ont pas de bruitage propre : le vol de la bulle (19.00) et le survol du devis (32.10 à 33.44).
- Coût de rendu : trois copies floutées de la feuille sous une caméra 3D à chaque image, plus les plongées à fort
  grossissement (s = 18 dans la séquence 1). Le relais par calque écran au sommet du flou évite de rastériser la
  feuille à l'échelle de la plongée ; à surveiller au premier rendu.
