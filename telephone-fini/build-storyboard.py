#!/usr/bin/env python3
import json,re
d=json.load(open("onsets.json"))
B=[0,3.26,8.25,11.75,15.63,21.46,26.26,29.90,33.34,37.48,43.36,49.91,53.83,58.23]
def cues(i,extra=""):
    a,b=B[i-1],B[i]
    return "Word cues: "+" ".join(f"{re.sub(r'[.,:;?!]+$','',w['w'])}@{w['s']-a:.2f}" for w in d['words'] if a<=w['s']<b)+(" "+extra if extra else "")
CUT="aucun raccord de caméra (coupe franche voulue, changement de scène sur la voix)"
# handoff_out of frame n (None = hard cut to next)
H={3:"à 3.50 : la courbe (composant curve) cadrée plein écran, ligne blanche tracée de 2010 jusqu'à 2016 environ et qui commence à chuter, étiquette « 2010 : 9 RDV SUR 10 APPELS » posée en haut à gauche, caméra en travelling lent vers la droite (+40 px/s) ; titre « LE TÉLÉPHONE MOURAIT DÉJÀ » en haut avec son trait ; aucun sous-titre ; halo orange à gauche ; grain 4 %",
   6:"à 4.80 : la carte 1 « MONTRE TON TRAVAIL » (composant card, badge « 1 ») centrée, son feed défile vers le haut (60 px/s), compteur « VUES » à 9 800 qui monte ; aucun sous-titre ; grain 4 %",
   8:"à 3.44 : la carte 2 « TA RÉPUTATION » (badge « 2 ») centrée au-dessus de la carte 1 réduite à 0,94 et assombrie, cinq étoiles pleines en accent, deux bulles d'avis empilées, une troisième qui arrive ; aucun sous-titre ; grain 4 %",
   12:"à 3.92 : fond #0A0A0A, titre « LE TÉLÉPHONE : TU LOUES TES CLIENTS. » en haut avec son trait, compteur « JOUR 214 » qui défile dessous (accent), caméra en poussée lente (+1 %/s) ; aucun sous-titre ; grain 4 %"}
head=open("../.claude/skills/motion-design/templates/STORYBOARD.md").read().split("<!--")[0]
head=head.replace('"{{TOTAL}}s"','"58.23s"').replace('"{{ONE_LINE_THESIS}}"','"Depuis le 11 août, démarcher pour un mandat au téléphone sans accord est interdit ; le téléphone mourait déjà ; ce qui dure, ce sont les canaux que tu possèdes : contenu, réputation, point de vente."')
head=head.replace('"{{AUDIENCE}}"','"Marchands et intermédiaires automobiles (mandats, dépôt-vente) qui trouvent leurs clients au téléphone"')
head=head.replace('"{{LETTER_AND_NAME_OF_THE_CHOSEN_DIRECTION_IN_DIRECTIONS_MD}}"','"découpage écrit par Guillaume (SCRIPT.md), reel 9:16"')
head=head.replace('"{{styleframes/A1.png (t s), styleframes/A2.png (t s), styleframes/A3.png (t s)}}"','"aucune (look validé sur la frame pilote)"')
head=head.replace("format: 1920x1080","format: 1080x1920")
body='''
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
'''
F=[
(1,"11 août 2026","hook","Les chiffres « 11 AOÛT 2026 » claquent un par un en très gros, puis un téléphone apparaît et se fait barrer d'un trait orange","Si tu trouves tes mandats au téléphone, t'as un problème depuis le onze août.","kinetic-beat-slam, svg-path-draw","titlecard-reveal",
 "aucun (ouverture du film) ; première image = « 11 » en Big Shoulders 900 300 px, blanc, arrivant ×1,4 et flou 10 px au centre du cadre, sur le fond noir avec son halo orange",
 '''Scene 1 (0.00 à 1.60 s) : P1, la date
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
  IMAGE CLÉ : 2.60 : la date en haut, le téléphone barré d'orange au centre, « depuis le onze août. » en bas.'''),
(2,"Démarchage sans accord","context","« DÉMARCHAGE SANS ACCORD = INTERDIT » en titre, une liste de numéros masqués qui se grisent un par un","La loi est passée : tu n'as plus le droit d'appeler un particulier pour lui proposer un mandat, sans son accord.","svg-path-draw, waterfall-entry","typewriter-reveal",CUT,
 '''Scene 1 (0.00 à 4.99 s) : P3, la loi
  TEXTE ÉCRAN : titre « DÉMARCHAGE SANS ACCORD = INTERDIT » (3 lignes : « DÉMARCHAGE » / « SANS ACCORD » / « = INTERDIT », « INTERDIT » en accent) ; liste de 7 numéros masqués (composant number-list) ; sous-titres « La loi est [orange : passée] » (0.16 à 0.80), « tu n'as plus le droit » (0.85 à 1.70), « d'appeler un particulier » (1.75 à 2.85), « pour lui proposer un [orange : mandat], » (2.89 à 4.05), « sans son accord. » (4.14 à 4.99).
  ÉTAPES : 0.00 « DÉMARCHAGE » claque ; 0.20 « SANS ACCORD » ; 0.40 « = INTERDIT » ; 0.60 le trait orange se trace ; 1.00 à 1.80 la liste de numéros tombe en cascade dans la zone visuelle (0,1 s d'écart) ; 2.20 à 4.60 les numéros se grisent et se barrent un par un (0,35 s d'écart) ; 4.50 le dernier se barre en accent.
  PISTE CAMÉRA : poussée +1,5 %/s ; cran à 1.00 vers la liste.
  SON : pop 0.00 ; key-press léger sur chaque numéro barré.
  IMAGE CLÉ : 4.60 : le titre, la liste entièrement grisée et barrée, « sans son accord. » en bas.'''),
(3,"Le téléphone mourait déjà","pain_point","Titre « LE TÉLÉPHONE MOURAIT DÉJÀ », la courbe démarre en haut avec « 2010 : 9 RDV SUR 10 APPELS »","Mais soyons honnêtes : le téléphone mourait déjà. Quand j'ai commencé,","svg-path-draw, counting-dynamic-scale","dataviz-countup",CUT,
 '''Scene 1 (0.00 à 3.50 s) : P4, la courbe commence haut
  TEXTE ÉCRAN : titre « LE TÉLÉPHONE MOURAIT DÉJÀ » (2 lignes) ; sous-titres « Mais soyons honnêtes : » (0.15 à 0.95), « le téléphone [orange : mourait] déjà. » (1.08 à 2.50), « Quand j'ai commencé, » (2.61 à 3.50) ; sur la courbe : axe « 2010 » … « 2026 », étiquette « 2010 : 9 RDV SUR 10 APPELS ».
  ÉTAPES : 0.00 le titre claque ; 0.30 le trait ; 0.60 les axes se tracent ; 1.00 la ligne blanche démarre en haut à gauche (point de départ net) ; 1.70 sur « mourait » la ligne se met à descendre ; 2.61 l'étiquette « 2010 : 9 RDV SUR 10 APPELS » se pose près du départ (le 9 roule de 0 à 9) ; 3.00 à 3.50 la ligne continue jusqu'à 2016 environ.
  PISTE CAMÉRA : travelling lent vers la droite (+40 px/s) qui suit la pointe de la ligne.
  SON : pop 0.00 ; key-press 2.61.
  IMAGE CLÉ : 3.00 : la courbe qui commence à chuter, « 2010 : 9 RDV SUR 10 APPELS », « Quand j'ai commencé, ».'''),
(4,"Aujourd'hui, trois","pain_point","La courbe chute jusqu'en 2026, « 2026 : 3 » se pose, le 3 en orange","sur dix appels, je décrochais neuf rendez-vous. Aujourd'hui, trois.","svg-path-draw, counting-dynamic-scale","dataviz-countup","FROM3",
 '''Scene 1 (0.00 à 3.88 s) : P5, 9 sur 10, puis 3
  TEXTE ÉCRAN : sous-titres « sur [orange : dix] appels, » (0.11 à 0.80), « je décrochais [orange : neuf] rendez-vous. » (0.83 à 2.45), « Aujourd'hui, [orange : trois]. » (2.57 à 3.88) ; étiquette de fin « 2026 : 3 » (le 3 en accent, jumbo 220 px).
  ÉTAPES : 0.11 à 1.80 l'étiquette 2010 pulse une fois sur « neuf » (×1,1) ; 1.90 à 2.80 la ligne plonge jusqu'en 2026 (power2.in) ; 2.57 le travelling accélère ; 3.00 le point d'arrivée accent se pose ; 3.35 sur « trois » : « 2026 : 3 » claque, le 3 en accent roule de 9 à 3 ; 3.40 à 3.88 respiration : le 3 respire une fois (×1,05) et la ligne fait une ombre orange.
  PISTE CAMÉRA : travelling +40 px/s, accélération à 2.57, cran vers l'étiquette finale à 3.20.
  SON : key-press 3.35 ; pop 3.35.
  IMAGE CLÉ : 3.60 : la courbe effondrée, « 2026 : 3 » avec le 3 orange, « Aujourd'hui, trois. ».'''),
(5,"Tout le monde pêche au même endroit","pain_point","Une mosaïque d'annonces auto identiques qui se multiplient jusqu'à remplir l'écran, puis « TOUT LE MONDE PÊCHE AU MÊME ENDROIT »","Le vrai problème, c'est pas la loi. Si tu pêches là où pêchent tous tes concurrents, c'est normal d'avoir de la concurrence.","waterfall-entry, kinetic-beat-slam","overwhelm-surround",CUT,
 '''Scene 1 (0.00 à 2.00 s) : P6, le vrai problème
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
  IMAGE CLÉ : 3.60 : la mosaïque d'annonces identiques assombrie, le titre par-dessus avec son trait.'''),
(6,"1 · Montre ton travail","solution","La carte 1 monte du bas : « MONTRE TON TRAVAIL », un feed qui défile (remise de clés, voiture préparée), le compteur de vues grimpe","Un : montre ton travail. Chaque voiture vendue, chaque client livré, c'est un contenu.","card-morph-anchor, counting-dynamic-scale","fixed-anchor-cycle",CUT,
 '''Scene 1 (0.00 à 4.80 s) : P8, la carte 1
  TEXTE ÉCRAN : carte 1 (composant card, badge « 1 ») titre « MONTRE TON TRAVAIL » ; feed (composant feed) avec 3 légendes courtes dans les posts : « CLÉS REMISES », « PRÊTE À PARTIR », « CLIENT LIVRÉ » (Space Mono 26) ; compteur « VUES » ; sous-titres « Un : [orange : montre] ton travail. » (0.15 à 1.70), « Chaque voiture vendue, » (1.83 à 2.80), « chaque client livré, » (2.88 à 3.70), « c'est un [orange : contenu]. » (3.76 à 4.80).
  ÉTAPES : 0.00 la carte monte du bas (y +900 → 0, 0,35 s expo.out) ; 0.15 le badge « 1 » claque ; 0.65 le titre de la carte claque, 0.90 son trait ; 1.83 le feed commence à défiler ; 2.18 post « PRÊTE À PARTIR » ; 2.88 post « CLÉS REMISES » ; 3.41 post « CLIENT LIVRÉ » ; 3.76 le compteur « VUES » roule de 1 240 à 9 800.
  PISTE CAMÉRA : poussée +1 %/s, cran à 1.80 vers le feed.
  SON : whoosh-short 0.00 ; pop 0.15 ; key-press 3.76.
  IMAGE CLÉ : 4.20 : la carte 1, le feed qui défile, « VUES 9 800 », « c'est un contenu. ».'''),
(7,"Organique, pas pub","solution","Sur la carte 1, une étiquette « PUB » se barre, « ORGANIQUE » s'allume, le compteur de vues continue de grimper","En organique, pas en pub. On achète à quelqu'un qu'on a déjà vu bosser.","counting-dynamic-scale, svg-path-draw","fixed-anchor-cycle","FROM6",
 '''Scene 1 (0.00 à 3.64 s) : P9, organique
  TEXTE ÉCRAN : deux pastilles sur la carte : « ORGANIQUE » (accent) et « PUB » (barrée) ; sous-titres « En [orange : organique], » (0.15 à 0.90), « pas en pub. » (0.93 à 1.60), « On achète à quelqu'un » (1.67 à 2.50), « qu'on a déjà vu [orange : bosser]. » (2.52 à 3.64).
  ÉTAPES : 0.27 la pastille « ORGANIQUE » s'allume en accent ; 0.93 la pastille « PUB » apparaît et 1.22 se fait barrer ; 1.67 le feed accélère ; 2.16 le compteur « VUES » repart de 9 800 à 18 600 ; 3.25 sur « bosser » un post « CLIENT LIVRÉ » se fige au centre avec un cœur accent.
  PISTE CAMÉRA : poussée +1 %/s.
  SON : click 1.22 ; key-press 2.16.
  IMAGE CLÉ : 3.30 : la carte 1, « ORGANIQUE » allumé, « PUB » barré, « VUES 18 600 ».'''),
(8,"2 · Ta réputation","solution","La carte 2 monte et recouvre la carte 1 : « TA RÉPUTATION », cinq étoiles se remplissent, les avis s'empilent","Deux : ta réputation. Les avis, les clients qui reviennent,","card-morph-anchor, waterfall-entry","fixed-anchor-cycle",CUT,
 '''Scene 1 (0.00 à 3.44 s) : P10, la carte 2
  TEXTE ÉCRAN : carte 2 (badge « 2 ») titre « TA RÉPUTATION » ; cinq étoiles (composant stars) ; bulles d'avis sans texte lisible ; sous-titres « Deux : ta [orange : réputation]. » (0.15 à 1.60), « Les [orange : avis], » (1.70 à 2.30), « les clients qui reviennent, » (2.37 à 3.44).
  ÉTAPES : 0.00 la carte 1 réduite (0,94, assombrie) est en place derrière ; la carte 2 monte du bas (0,35 s expo.out) ; 0.15 badge « 2 » ; 0.77 le titre claque, 1.00 son trait ; 1.70 à 2.30 les cinq étoiles se remplissent une à une ; 2.37 une première bulle d'avis se pose ; 2.84 une deuxième ; 3.20 une troisième arrive.
  PISTE CAMÉRA : poussée +1 %/s.
  SON : whoosh-short 0.00 ; pop sur chaque étoile.
  IMAGE CLÉ : 2.60 : la carte 2 sur la carte 1, cinq étoiles orange, une bulle d'avis.'''),
(9,"Aucun concurrent ne peut te le prendre","solution","Sur la carte 2, une flèche de recommandation relie deux bulles (« le beau-frère »), puis un cadenas orange se ferme sur les étoiles","ceux qui t'envoient leur beau-frère. Ça, aucun concurrent ne peut te le prendre.","svg-path-draw, kinetic-beat-slam","fixed-anchor-cycle","FROM8",
 '''Scene 1 (0.00 à 4.14 s) : P11, le beau-frère et le cadenas
  TEXTE ÉCRAN : sous-titres « ceux qui t'envoient » (0.12 à 0.70), « leur [orange : beau-frère]. » (0.64 à 1.40), « Ça, » (1.47 à 2.00), « aucun concurrent ne peut » (2.04 à 2.95), « te le [orange : prendre]. » (2.99 à 4.14).
  ÉTAPES : 0.38 une petite silhouette (cercle + épaules, ligne blanche) apparaît à côté d'une bulle d'avis ; 0.64 une flèche accent courbe part d'elle vers une deuxième silhouette (svg path draw 0,3 s) ; 1.47 les étoiles brillent une fois ; 2.31 sur « concurrent » des silhouettes grises tentent d'entrer par les bords et s'arrêtent ; 3.27 un cadenas orange se ferme sur les étoiles (×1,3 → 1, 0,18 s) ; 3.69 sur « prendre » le cadenas claque.
  PISTE CAMÉRA : poussée +1 %/s, cran à 3.20 sur le cadenas.
  SON : click 3.69.
  IMAGE CLÉ : 3.80 : la carte 2, cinq étoiles, le cadenas orange fermé dessus.'''),
(10,"3 · Sois installé","solution","La carte 3 monte : « SOIS INSTALLÉ », une vitrine s'allume, une adresse apparaît sur une carte avec un repère orange","Trois : sois installé. Un point de vente, une adresse, une vitrine. Face à un inconnu sur Leboncoin, c'est ce qui rassure.","card-morph-anchor, coordinate-target-zoom","fixed-anchor-cycle",CUT,
 '''Scene 1 (0.00 à 5.88 s) : P12, la carte 3
  TEXTE ÉCRAN : carte 3 (badge « 3 ») titre « SOIS INSTALLÉ » ; vitrine et carte de quartier (composant shopfront) ; à la fin, une tuile d'annonce floue étiquetée « INCONNU ? » ; sous-titres « Trois : sois [orange : installé]. » (0.12 à 1.20), « Un point de vente, » (1.30 à 2.00), « une adresse, » (2.05 à 2.60), « une vitrine. » (2.66 à 3.50), « Face à un inconnu » (3.58 à 4.35), « sur Leboncoin, » (4.38 à 4.90), « c'est ce qui [orange : rassure]. » (4.92 à 5.88).
  ÉTAPES : 0.00 les cartes 1 et 2 réduites derrière, la carte 3 monte du bas ; 0.12 badge « 3 » ; 0.48 titre, 0.70 trait ; 1.45 la façade se dessine ; 2.20 sur « adresse » la carte de quartier se pose et le repère accent tombe sur son point ; 2.81 sur « vitrine » la vitrine s'allume (lueur accent) ; 3.58 une tuile d'annonce grise et floue « INCONNU ? » apparaît à gauche, petite ; 5.32 sur « rassure » la vitrine éclaire plus fort et l'annonce floue s'éteint.
  PISTE CAMÉRA : poussée +1 %/s, crans à 2.20 et 3.58.
  SON : whoosh-short 0.00 ; pop 2.20 ; pop 2.81.
  IMAGE CLÉ : 3.20 : la carte 3, la vitrine allumée et le repère orange sur la carte.'''),
(11,"Le mur","punchline","Un mur se construit brique par brique du bas vers le haut, la dernière brique en orange ; « Le marché tranchera pour toi »","Ça prend du temps et de la régularité. Mais une fois en place, personne ne te le prend. Pas le temps d'être régulier ? Le marché tranchera pour toi.","waterfall-entry, kinetic-beat-slam","fixed-anchor-cycle",CUT,
 '''Scene 1 (0.00 à 6.55 s) : P13, brique par brique
  TEXTE ÉCRAN : titre « BRIQUE PAR BRIQUE » ; mur (composant wall) ; sous-titres « Ça prend du [orange : temps] » (0.16 à 0.90), « et de la régularité. » (0.62 à 2.00), « Mais une fois en place, » (2.10 à 3.15), « personne ne te le [orange : prend]. » (3.23 à 4.25), « Pas le temps d'être régulier ? » (4.37 à 5.35), « Le marché [orange : tranchera] pour toi. » (5.45 à 6.55).
  ÉTAPES : 0.00 le titre claque, 0.30 son trait ; 0.40 à 3.70 les briques se posent du bas vers le haut au rythme de la voix (une brique toutes les 0,12 s, rangée après rangée) ; 3.77 sur « prend » la dernière brique, orange, claque au sommet ; 4.37 à 5.40 le mur reste, une lueur orange le parcourt ; 5.81 sur « tranchera » un trait orange tranche l'écran en diagonale et le mur s'éclaire.
  PISTE CAMÉRA : montée lente avec le mur (−30 px/s), cran à 3.70.
  SON : pop doux sur les rangées ; click 3.77 ; whoosh 5.81.
  IMAGE CLÉ : 4.00 : le mur complet, la brique orange au sommet, « personne ne te le prend. ».'''),
(12,"Tu loues tes clients","cta","« LE TÉLÉPHONE : TU LOUES TES CLIENTS. » avec un compteur de jours qui défile dessous","Le téléphone, c'est louer tes clients, et chercher de nouvelles locations tous les jours.","counting-dynamic-scale, kinetic-beat-slam","titlecard-reveal",CUT,
 '''Scene 1 (0.00 à 3.92 s) : P14, louer
  TEXTE ÉCRAN : titre « LE TÉLÉPHONE : » / « TU LOUES TES CLIENTS. » (2 blocs, 5 mots max chacun, un petit téléphone barré à gauche de « LE TÉLÉPHONE », rime de l'accroche) ; compteur (composant day-counter) « JOUR 1 » → « JOUR 214 » ; sous-titres « Le téléphone, » (0.14 à 0.95), « c'est [orange : louer] tes clients, » (1.02 à 1.95), « et chercher de nouvelles locations » (2.00 à 3.25), « tous les [orange : jours]. » (3.32 à 3.92).
  ÉTAPES : 0.14 « LE TÉLÉPHONE : » claque avec le petit téléphone barré ; 1.20 sur « louer » « TU LOUES TES CLIENTS. » claque, 1.40 le trait ; 2.00 le compteur apparaît « JOUR 1 » et défile de plus en plus vite jusqu'à « JOUR 214 » à 3.90.
  PISTE CAMÉRA : poussée +1 %/s.
  SON : pop 0.14 ; pop 1.20 ; key-press 2.00 à 3.90.
  IMAGE CLÉ : 3.50 : le titre en deux blocs, le compteur « JOUR 197 » qui défile.'''),
(13,"Tu les possèdes","cta","« CES CANAUX : TU LES POSSÈDES. », puis « @guillaumeherbin_ » avec un bouton S'abonner","Ces canaux-là, tu les possèdes. Abonne-toi pour la suite.","kinetic-beat-slam, cursor-click-ripple","cta-morph-press","FROM12",
 '''Scene 1 (0.00 à 1.80 s) : P15, posséder
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
  IMAGE CLÉ : 3.40 : « @guillaumeherbin_ », le bouton « ABONNÉ ✓ », la lueur orange.'''),
]
slug={1:"date",2:"loi",3:"courbe",4:"trois",5:"mosaique",6:"carte1",7:"organique",8:"carte2",9:"cadenas",10:"carte3",11:"mur",12:"louer",13:"posseder"}
out=head.rstrip()+"\n"+body
for n,title,typ,scene,vo,rules,bp,hin,scenes in F:
    a,b=B[n-1],B[n]
    if hin.startswith("FROM"): hin=H[int(hin[4:])].replace(H[int(hin[4:])].split(" : ")[0],"à 0.00",1)
    hout=H.get(n, "aucun (fin du film, tenue jusqu'à 4.40)" if n==13 else CUT)
    out+=f'''
## Frame {n}: {title} · {a:.2f} → {b:.2f}

- scene: {scene}
- duration: {b-a:.2f}s
- transition_in: cut
- status: outline
- src: compositions/frames/{n:02d}-{slug[n]}.html
- voiceover: "{vo}"
- type: {typ}
- blueprint: {bp} (Adapt)
- focal: {title}
- rules: {rules}
- world: dark
- handoff_in: {hin}
- handoff_out: {hout}

{cues(n)}

{scenes}
'''
open("STORYBOARD.md","w").write(out)
