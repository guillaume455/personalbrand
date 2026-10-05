---
titre: Grammaire de storyboard du motion design d'agence
date: 2026-09-29
sources: la grammaire et les patterns du motion design, ce qui ressort après avoir regardé pas mal de vidéos de motion design ; storyboard à l'envers de la v6 du devis (non publié) ; patterns/PATTERNS.md ; réglages retenus sur le film final (examples/ligne-du-temps-v8/)
---

# Grammaire de storyboard du motion design d'agence

`PATTERNS.md` dit **quoi** montrer (accroche, douleur, pivot, preuve, fin). Ce fichier dit **comment l'écrire** au dixième de seconde, pour qu'un agent l'anime en HTML/CSS/GSAP dans HyperFrames (le moteur qui rend une page HTML animée en vidéo) sans improviser la mise en scène. GSAP (GreenSock Animation Platform) est la bibliothèque d'animation JavaScript utilisée : `expo.out` décélère très fort, `power2.in` accélère, `back.out` dépasse puis revient, `none` est linéaire.

Conventions : temps en secondes ; tailles en % de la hauteur (h) ou de la largeur (l) du cadre ; « V 10,54 » = mot dit à 10,54 s ; i/s = images par seconde (1 image = 0,033 s à 30 i/s, 0,04 s à 25 i/s). Les films de lancement cités en exemple, avec leurs temps, sont des films publics : ils appartiennent à leurs auteurs, aucune image ni vidéo n'en est reproduite ici, et ce dépôt n'est affilié à aucune des marques citées. La « v6 » est notre version du devis faite avant cette grammaire (non publiée) ; le même film refait avec elle est dans `examples/C-le-devis-v7a/`.

## 1. Les chiffres

### 1.1 Les 6 références et la v6

| Film (voix) | Durée | Plans | Moy. / méd. | Plans / 10 s | % continu | Coupes franches | Couches animées | Caméra |
|---|---|---|---|---|---|---|---|---|
| Taapit (sans voix, musique ≈ 117 BPM) | 77,6 | 45 | 1,72 / 1,32 | 5,8 (accroche 9,8) | 73 % | 12 (27 %), toutes structurelles | 2 à 6 (accroche 4 à 6) | jamais arrêtée : dérive 2 à 5 %/s + crans de 0,04 à 0,2 s vers le prochain clic |
| Slack (voix jouée, gags) | 66,7 (52,3 montés) | 34 | 1,95 / 1,32 | 5,1 (6,3 montés) | 33 % | 22 (67 %), sur le premier mot de l'idée | 1 à 3 | fixe, mais chaque plan atterrit (×1,15 → ×1) puis recule ; 3 mouvements forts |
| Aikido (voix narrative, anglais) | 77,9 | 22 | 3,5 / 3,6 | 2,8 | 95 % | 1 (5 %), changement d'acte | 2 à 4 (4 ensemble à 1,6 s) | un seul monde parcouru : déplacements de 0,3 à 0,9 s, dérive 1 à 3 %/s |
| Collective (voix narrative) | 60,0 | 40 | 1,5 / 1,3 | 6,7 (douleur 9,3, solution 5,4) | 92 % | 3 (8 %), masquées dans un flou | 2 à 3 + avant-plan flou dans 6 plans | jetée : whips de 0,1 à 0,15 s, zooms éclair de 0,15 s, push de 0,3 à 0,6 s |
| Calendly (voix narrative posée) | 39,5 | 20 | 1,98 / 1,60 | 5,1 | 89 % | 2 (10 %), dans un silence | 2 à 3, max 4, un seul actif | fixe 13 plans sur 20 ; les objets portent le mouvement ; push linéaire 5 %/s, pull décéléré |
| lemlist (voix jouée, rapide) | 51,7 | 43 | 1,20 / 1,03 | 8,3 | 60 % (+ 12 % de coupes à raccord) | 12 (29 %), dont 5 de texte sur fond continu | 2 à 4 + avant-plan flou | 3D mobile : dérive 5 à 10 %/s cassée par des gestes de 2 à 5 images |
| **v6 « Le devis »** (voix narrative) | 43,2 | 20 | 2,16 / 1,75 | 4,6 (douleur 5,6, solution 5,0) | 95 %, dont 58 % d'effets génériques | 1 (5 %), « Stop. » | régime 1,4, pic moyen 2,75 | fixe ≈ 95 % : 5 mouvements, 2,3 s cumulées |

### 1.2 Ce qu'il faut en retenir

- **Le rythme se compte en événements, pas en plans.** Aikido est le plus lent en plans (2,8 / 10 s) mais chaque plan contient 3 à 6 temps espacés de 0,5 à 1 s. Calendly, plan 1 : 5 événements en 1,1 s (curseur 0,13, caret 0,23, barre d'outils 0,40, traits 0,50, pop du O 1,07). La v6 est dans la norme en plans (4,6) mais 31 % de ses tranches de 0,1 s sont quasi immobiles et 20 % totalement immobiles. Règle : **un événement (arrivée, geste, clic, changement d'état, cran de caméra) toutes les 0,5 à 1 s au plus, toutes les 0,1 à 0,3 s dans l'accroche.**
- **Le nombre de plans ne discrimine pas** : de 2,8 à 8,3 plans / 10 s pour six films de référence. Ce qui manque à la v6, ce n'est pas des plans : ce sont des événements, de la caméra et de la profondeur.
- **Le tempo change avec l'acte** : Collective 9,3 plans / 10 s dans la douleur, 5,4 dans la solution ; Taapit 9,8 dans l'accroche. La v6 garde le même tempo (5,6 contre 5,0) : le soulagement ne se sent pas.
- **La continuité se mesure en objets, pas en absence de coupe.** La v6 affiche 95 % de continu comme Aikido, mais 11 de ses 19 jonctions sont des effets (glissement, zoom-through, fondu flouté). Dans les films de référence, les effets purs sont 0 à 2 par film (Aikido 1 flou-fondu, Collective 2, Calendly zéro fondu enchaîné).
- **Caméra fixe ne veut pas dire image fixe.** Quand la caméra ne bouge pas (Calendly, Slack), les objets portent le mouvement ou chaque plan atterrit. La v6 cumule caméra fixe et objets posés.
- **Couches** : 2 à 4 animées en même temps, un seul élément « actif » (Calendly). La v6 tourne à 1,4.
- **Les tenues longues existent** (Taapit écran partagé 8,7 s, Collective réseau 3,4 s, Calendly démo 5,1 s) mais elles sont placées là où il faut lire, et elles vivent.

### 1.3 Ce que ces storyboards corrigent dans PATTERNS.md

Corrections reportées dans `PATTERNS.md` (règles réécrites sur place, pas empilées).

- **D1 « 0 à 4 coupes franches »** : ne vaut qu'avec une voix narrative (Aikido 1, Calendly 2, Collective 3 masquées). Voix jouée : Slack 22, lemlist 12 plus 5 coupes à raccord. Sans voix : Taapit 12, toutes structurelles. Voir loi 6.
- **« Une nouvelle composition toutes les 2 à 4 s »** : vrai mais secondaire ; la cadence qui compte est celle des événements (0,5 à 1 s).
- **B1 « le texte reprend la voix mot par mot »** : c'est une réécriture choisie phrase par phrase. Calendly n'a aucun sous-titre (chaque phrase a un geste) ; Aikido écrit « One platform to rule them all » sur « No fragmented tools required » et n'écrit pas « Aikido makes it simple » (3,26 à 4,40) pour garder le nom au logo ; Slack n'écrit jamais « alors ».
- **F3 « chaque chiffre roule »** : il roule (Taapit +42 → +100 en ≈ 1,2 s, 24,18 à 25,4) ou il fonce entier depuis la caméra (Aikido « -85% », 44,88 à 45,16). Jamais posé en fondu.
- **« Logo jamais avant 5 s »** : Slack ouvre sur une pastille logo à 0,07 s qui devient la barre de recherche à 1,00 ; lemlist écrit sa pilule à 3,40. Le logo n'ouvre pas le film comme signature, mais il peut arriver tôt s'il est un objet du récit qui se transforme.
- **C1 « une seule couleur d'accent »** : une couleur par rôle ou par acte. lemlist passe l'accent du bleu au rouge dans l'acte sombre (16,33 à 17,2) ; Aikido attribue violet au mot-clé, lavande aux chiffres, teal aux contours, rouge à la douleur.
- **G1 « tenue de 3 à 8 s, puis fondu »** : aucune des 6 ne finit en fondu. Iris noir (Aikido 74,32), tenue vivante de 2 à 3 s après le clic (Taapit, Collective, lemlist), variante sans bouton (Calendly).
- **D3 « deux vitesses »** (tempo de montage) est confirmé par Collective. Ne pas le confondre avec la loi 2 ci-dessous (deux vitesses de mouvement).

## 2. Les lois de mise en scène

### Loi 1. Le monde est un lieu, la caméra est une piste à part

**Énoncé.** On pose d'abord un monde (sol texturé, scènes placées à des coordonnées fixes), puis on écrit la caméra comme une piste séparée avec sa propre partition : une dérive de fond qui ne s'arrête jamais, et des événements datés (cran, whip, révélation) qui ont chacun une cible. On ne change pas d'écran : on se déplace.

**Preuves.**
- Aikido 0 à 25 s : toute la douleur est une seule carte 2D. Pan (9,8 à 10,7), push-in ×1,5 (13,4 à 14,2), recul + pan (17,0 à 17,4), travelling diagonal (21,2 à 22,4). La mascotte et la légende « Drown you in endless alerts » repassent dans le cadre aux plans 5, 6 et 7. Sur « With » (V 25,34), dézoom ×0,55 en 0,45 s : la douleur apparaît comme UNE carte, puis whip tilt (25,73 à 25,85) qui la jette.
- Taapit : la grille du sol (cellule ≈ 6 % h) bouge avec la caméra et rend la dérive lisible. Crans qui visent la zone du prochain clic 0,2 à 0,5 s avant : push ×2 en 0,16 s (12,02), cran ×1,2 → ×1,8 (43,2 à 43,32), whip-pan (44,94 à 45,14), dézoom ×1,8 → ×0,8 en 0,15 s (45,74 à 45,90).
- Collective 42,2 à 45,0 : vol dans le réseau de job boards, un atterrissage par nom (LinkedIn 42,30, Indeed 42,98, Google 43,60, Collective 44,28).
- Calendly : la caméra ne bouge que pour raconter. Push linéaire ≈ 5 %/s pendant l'escalade (10,03 à 14,5), pull ×1,9 → ×1 avec 70 % du trajet dans les 0,4 premières secondes quand le drapeau est planté (15,07 à 16,1).

**Recette.**
```html
<div id="stage">          <!-- 1920×1080, overflow:hidden, perspective:1600px -->
  <div id="drift">        <!-- dérive de fond, une tween linéaire par plan -->
    <div id="cam">        <!-- échelle et rotation autour du centre du cadre -->
      <div id="world">    <!-- translation ; 3×2 écrans par acte (5760×2160) -->
        <section class="scene" style="left:0;top:0">…</section>
        <section class="scene" style="left:1920px;top:0">…</section>
```
```js
gsap.set('#cam',{transformOrigin:'960px 540px'});
const CAM = gsap.timeline();                 // piste caméra : une timeline à part, ajoutée au master à 0
// dérive par plan : un vecteur (x, y, échelle) sur toute la durée du plan, alterné d'un plan à l'autre,
// remis à zéro sous le couvert d'un cran ou d'un whip (le flou masque le saut)
const drift=(t,d,{x=-24,y=0,s=.03}={})=>CAM.fromTo('#drift',{x:0,y:0,scale:1},{x,y,scale:1+s,duration:d,ease:'none'},t);
// cran : (px,py) = point du monde à amener au centre du cadre
function cran(t,px,py,s,d=.12){
  CAM.to('#world',{x:960-px,y:540-py,duration:d,ease:'expo.inOut'},t)
     .to('#cam',{scale:s,duration:d,ease:'expo.inOut'},t)
     .to('#cam',{filter:'blur(6px)',duration:d/2,yoyo:true,repeat:1,ease:'none'},t);
}
```
Le fond porte une texture qui rend la dérive visible : grille (Taapit), trame de points (lemlist), lignes topographiques (Collective), cercles concentriques (Aikido). Un aplat uni cache la dérive.

### Loi 2. Deux vitesses de mouvement, aucune tenue figée

**Énoncé.** Presque tout mouvement est soit un **geste** (0,04 à 0,2 s, 1 à 6 images), soit une **dérive** (toute la durée du plan, 1 à 10 %/s, linéaire). La zone 0,3 à 0,9 s est réservée à la caméra qui change de scène et au curseur, toujours avec une courbe très asymétrique (70 à 90 % du trajet dans le premier tiers), si bien que l'œil lit un geste suivi d'une dérive. Aucune tenue n'est une image fixe : au moins une couche dérive ou boucle.

**Preuves.**
- Gestes : lemlist traversée du O en 3 images (0,83 à 0,90), carte qui jaillit en 2 images (12,90 à 12,97), filé de 0,13 s (36,90 à 37,03) ; Slack atterrissage en 1 à 3 images (17,57 → 17,60) ; Collective whips de 0,1 à 0,15 s ; Taapit crans de 0,04 à 0,2 s, pops d'interface à 0,04 s d'écart (11,14 à 11,46).
- Mouvements longs asymétriques : Taapit recul d'ouverture 0,64 s avec 90 % du trajet fait à 0,45 ; Calendly pull 1,1 s, 70 % dans les 0,4 premières ; Aikido déplacements de 0,3 à 0,9 s, en ease-in pour sortir et ease-out pour entrer, qui se chevauchent de 0,2 à 0,3 s.
- Tenues vivantes : Aikido « aucune tenue n'est figée », cartes qui tournent, notifications qui dérivent de 1 à 3 %/s, traits de stress redessinés à chaque image (12,0 à 13,3) ; Calendly boucle de vie sur chaque plan tenu (Lola cligne à 3,1, pinceau, queue du chien) ; Collective orbites qui tournent de ≈ 15°/s (9,4 à 11,2), horloge (47,2 à 49,6).

**Recette.**

| Mouvement | Durée | Courbe | Détail |
|---|---|---|---|
| Apparition d'un élément | 0,06 à 0,15 s | `expo.out` ou `back.out(2)` | jamais un fondu seul (voir loi 4) |
| Cran, whip, filé de caméra | 0,08 à 0,15 s | `expo.inOut` | flou 6 à 12 px au milieu du trajet |
| Traversée, jaillissement | 3 à 5 images | `power2.in` | la cible est déjà posée derrière |
| Changement de scène (caméra) | 0,3 à 0,9 s | sortie `power2.in`, entrée `expo.out` | chevauchement 0,2 à 0,3 s |
| Dérive de caméra | durée du plan | `none` | 2 à 5 % d'échelle/s ou 10 à 30 px/s |
| Vie d'une tenue | boucle de 1 à 2 s | `sine.inOut`, `yoyo` | 1 à 3° ou 2 à 6 px, désynchronisée |

```js
// vie d'une tenue : répétitions finies, la timeline doit avoir une durée connue
tl.to('.card',{rotation:'+=2',y:'-=4',duration:1.6,ease:'sine.inOut',yoyo:true,repeat:Math.ceil(D/1.6)},t0);
```
Contrôle au rendu (méthode du storyboard à l'envers de la v6) : différence moyenne entre images successives par tranche de 0,1 s ; aucune fenêtre de 0,5 s sous le seuil « quasi immobile » (< 0,25) hors silence écrit dans le storyboard.

### Loi 3. L'objet-pont change de rôle, le vecteur de sortie fixe l'entrée

**Énoncé.** À chaque jonction, un objet du plan N survit et prend un autre rôle dans le plan N+1. À défaut d'objet, la direction, la vitesse et la courbe de sortie de N fixent l'entrée de N+1 (même vecteur, chevauchement de 0,1 à 0,3 s). Dans un morph, la phase de rétrécissement est 2 à 4 fois plus courte que la phase d'expansion.

**Preuves.**
- lemlist : la caméra traverse le O de « OK » (0,83 à 0,90), l'anneau « 60.S » recule et devient le « o » de « pour » (1,60) ; la pilule signal reste quand le monde passe au bleu (36,00).
- Calendly : curseur qui tire le cadre de Lola (1,17), trace les vignettes, devient un cœur (8,87) ; pièce « lien » qui chasse la silhouette puis devient un iris (18,20 à 19,70) ; carte de confirmation qui devient une bulle du mur (27,57 à 27,90) ; balle qui sert de volet (33,83 à 35,13) ; calendrier qui devient la carte de fin (36,6).
- Collective : le panneau de filtres bascule et devient la grille de profils (8,0) ; la fiche de poste devient le moyeu du réseau (38,8) ; le titre devient l'en-tête (45,73 à 45,83).
- Taapit : modale qui se replie dans la case du widget (17,56 à 17,72) ; QR qui rétrécit en carré en 0,04 s puis s'étire en téléphone en 0,16 s (62,96 à 63,20).
- Vecteur : Taapit « Deep Links » sort vers le haut (29,50 à 29,74), les téléphones montent du bas (29,78) ; Slack la couronne remonte (9,43), la boîte mail monte du bas (9,53) ; Aikido le bloc part à gauche en `power2.in` pendant qu'un point naît à droite (9,8 à 10,7, 0,3 s de coexistence).

**Recette.**
```js
// morph : même nœud DOM ; rétrécir vite, s'étendre lentement ; contenus qui sortent à 1 image d'écart
tl.to(node.children,{opacity:0,duration:.03,stagger:.033},t)
  .to(node,{width:120,height:120,borderRadius:24,duration:.05,ease:'power2.in'},t)
  .to(node,{width:420,height:860,borderRadius:56,backgroundColor:'#0d0b0a',duration:.18,ease:'expo.out'},t+.05);
// vecteur : même direction, même flou, chevauchement 0,1 s
tl.to(sceneN,{x:-2200,filter:'blur(18px)',duration:.2,ease:'power2.in'},t)
  .fromTo(sceneN1,{x:2200,filter:'blur(18px)'},{x:0,filter:'blur(0px)',duration:.3,ease:'expo.out'},t+.1);
```
Coordonnées écrites en dur (cadre fixe 1920×1080) plutôt que mesurées. Interdit : deux copies du même objet à l'écran pendant une transition.

### Loi 4. L'élément arrive trop grand et flou, puis se pose

**Énoncé.** Un élément principal n'apparaît jamais en fondu à sa taille finale. Il arrive plus grand (×1,1 pour un plan entier, ×3 à ×6 pour un objet qui vient de la caméra), flou (6 à 12 px), souvent décalé vers un bord, se pose en 1 à 9 images, puis continue de bouger (recul lent). Pôle opposé, tout aussi valable : il naît d'un point au fond et grossit jusqu'au sujet.

**Preuves.**
- Plan entier : Slack atterrit à chaque fonctionnalité (17,57 ×1,15 flou → ×1 à 17,60 ; 27,10 ×1,1 → 27,20 ; 44,38 ×1,2 → 44,45), puis recul lent.
- Depuis la caméra : Aikido « -85% » ×6, flou, depuis le bord droit, posé en 0,28 s `expo.out` (44,88 à 45,16) ; badges ≈ ×3 flous qui se plaquent inclinés de ±20° (66,1 à 66,9) ; Collective 6 cartes candidats `scale:3`, `blur(10px)`, depuis les 4 bords, 0,2 s, décalage 0,05 s (45,9 à 46,37) ; lemlist moustique (18,70) et curseur géant (30,2 à 31,2) de 15 à 40 % du cadre, qui rétrécissent en devenant nets en touchant leur cible ; pilule logo ×3 → ×1 en 0,45 s (29,13).
- Depuis un point : Collective 5 fois (2,9 ; 6,1 ; 20,07 ; 24,8 ; 52,8), Aikido mascotte (10,44).
- Anticipation : Aikido, le titre se range 0,15 s avant l'arrivée du chiffre ; la ligne glisse 0,2 s avant la pastille (1,32).

**Recette.**
```js
function land(el,t,{from=1.15,blur=6,d=.08,rest=.96,hold=1.5}={}){      // Slack
  tl.fromTo(el,{scale:from,filter:`blur(${blur}px)`},{scale:1,filter:'blur(0px)',duration:d,ease:'expo.out'},t)
    .to(el,{scale:rest,duration:hold,ease:'none'},t+d);
}
function fromCamera(el,t,{s=5,x=40,blur=12,d=.25}={}){                   // Aikido « -85% »
  tl.fromTo(el,{scale:s,xPercent:x,filter:`blur(${blur}px)`},{scale:1,xPercent:0,filter:'blur(0px)',duration:d,ease:'expo.out'},t);
}  // traînée : 1 ou 2 clones à 30 % d'opacité, même tween décalée de 0,03 s
```

### Loi 5. Le calage image/voix se choisit mot par mot

**Énoncé.** On ne cale pas des phrases, on choisit un écart pour chaque mot porteur. L'image **devance** les mots-images de 0,1 à 0,6 s (l'œil lit avant d'entendre) ; le texte mot à mot est synchrone à 0,1 s près ; un changement de composition tombe sur le **premier mot de l'idée** ou dans le silence qui le précède ; chaque silence de plus de 0,4 s est **écrit comme un plan** avec son action muette. Le texte à l'écran est une réécriture de la voix, et certaines phrases n'ont volontairement aucun texte.

**Preuves.**
- Avance : Calendly cadre de Lola 0,3 s avant « Lola », icône 0,5 s avant « découvre », « You are scheduled » 0,6 s avant « confirmer » ; Slack pizza 0,27 s avant « livrer » ; Aikido push 0,3 s avant « From » (8,46), pastilles de piliers 1,6 à 2 s avant leur mot (28,0 contre 29,92) ; Collective la carte file 0,3 s avant « file » (18,6 contre 18,90).
- Coupe sur le premier mot à ± 0,1 s : Slack « Slack » 6,02 / 6,07, « envoyer » 30,16 / 30,27, « mettre » 34,96 / 34,98 ; Collective « Avec » 24,76 / 24,77 ; Aikido « Integrates » 62,84 / 62,8.
- Silences écrits : Calendly clic de réservation dans le silence 24,5 à 25,05 ; lemlist chute muette de la carte 13,4 à 15,7, « Voilà » dit dans 0,5 s de noir (28,62 à 29,12) ; Slack noirs de 0,7 et 2 s qui portent les répliques (40,1 ; 42,4).
- Sans texte : lemlist « Vous savez ce petit… » (20,5 à 22,0) ; Aikido « saving time and headaches » (49,78). Contre-exemples à ne pas copier : les retards subis d'Aikido (tag 0,8 à 1 s après le mot à 13,4 et 17,2, logo 0,9 s après « Aikido »).

**Recette.**

| Type de mot | Écart image / voix |
|---|---|
| Mot-image (objet, métaphore, chiffre) | image 0,1 à 0,6 s avant |
| Texte mot à mot | 0 à 0,1 s avant (0 à 3 images) |
| Titre de chapitre, pilier | 0,5 à 2 s avant |
| Impact (contact, clic, claquement) | sur la syllabe accentuée du verbe, ± 0,1 s |
| Changement de composition | premier mot de l'idée, ± 0,1 s, ou dans le silence d'avant |
| Silence > 0,4 s | un plan : action muette (clic, chute, entrée d'objet) ou noir qui porte la réplique |

```js
const W = transcript.words;                      // Whisper (transcription horodatée mot par mot), en local
const cue = (mot,off=0,n=1) => W.filter(w=>w.word===mot)[n-1].start + off;
tl.add(()=>{},cue('pizza',-.27));                // chaque tween est placée par cue(), jamais par un temps en dur
```

### Loi 6. La coupe franche se mérite, et son quota dépend de la voix

**Énoncé.** Aucune coupe n'est gratuite : chacune tombe sur un premier mot, dans un silence, ou avec un changement de fond, jamais au milieu d'un mot. Le quota dépend de ce qui porte la continuité.
- **Voix narrative** : 0 à 4 coupes, aux changements d'acte, de préférence masquées au sommet du flou d'un mouvement.
- **Voix jouée** (personnage, gags) : la voix porte la continuité, l'image coupe sur le premier mot de chaque idée ; les noirs sont des plans de réplique.
- **Sans voix** : les coupes marquent la structure (chapitre, couleur du monde).
Dans tous les cas : 0 à 2 fondus par film.

**Preuves.** Aikido 1 coupe, sur « Integrates » (62,8), changement d'acte des démos vers l'écosystème. Calendly 2 (10,03 ; 15,07), dans une respiration, 0,15 à 0,25 s avant « Alors » et « Enfin ». Collective 3 (16,80 ; 24,77 ; 52,80), toutes au bout d'un mouvement flou, toutes à un changement d'acte. Slack 22 sur 33 jonctions, au premier mot de chaque fonctionnalité. lemlist 12, dont 5 simples changements de texte sur fond continu, les 4 vraies ruptures de décor étant aux actes (9,10 ; 28,62 ; 29,12 ; 44,92), plus 5 coupes à raccord (dans le mouvement, dans l'axe). Taapit 12 : 4 ouvertures de chapitre sur cadre vide, 6 changements de couleur du monde, 1 entrée dans l'écran partagé, 1 raccord dans l'axe.

**Recette.**
```js
// coupe masquée (Collective 24,77) : au sommet du flou d'un push qui accélère, sur le premier mot de l'acte
const c = cue('Avec');
tl.to('#cam',{scale:1.35,filter:'blur(14px)',duration:.25,ease:'power2.in'},c-.25)
  .set('#acte1',{autoAlpha:0},c).set('#acte2',{autoAlpha:1},c)
  .fromTo('#cam',{scale:.92,filter:'blur(14px)'},{scale:1,filter:'blur(0px)',duration:.15,ease:'expo.out'},c);
// coupe dans l'axe (lemlist 7,10) : même objet, autre échelle, d'une image à l'autre
tl.set(card,{scale:.45},t);
```
Chaque coupe du storyboard porte une ligne de justification : « t, mot, raison (acte, idée, couleur du monde) ».

### Loi 7. La métaphore se joue sur le verbe

**Énoncé.** Pour chaque phrase, on repère le verbe (ou le nom concret) et un objet fait physiquement l'action, contact calé à ± 0,1 s de la syllabe. Le texte peut rester petit ou disparaître : l'image porte le sens.

**Preuves.** Collective : la fiche touche le sol à 1,30 en plein « tombe » (1,16 à 1,56) et la pilule « tombe » tombe hors cadre (1,67 à 1,77) ; tranchée en V sur « creuser » (22,85 à 23,3) ; rembobinage VHS sur « repartez de zéro » (14,8 à 16,1) ; zoom à travers la foule jusqu'à UNE carte nette sur « trouver » (23,9) ; 4 cartes identiques sur « sosies » (51,5 à 52,1). Slack : la nuée d'e-mails passe entre deux feux qui virent au vert sur « 300 par jour » (14,83 à 16,63) ; fenêtre vide 2 s sur « tout est organisé » (17,6 à 19,7). lemlist : la carte jaillit sur « le vôtre » (12,90), la flamme entre sur « change » (27,50). Taapit sans voix : les icônes sont aspirées dans le symbole sur « Tous tes outils en un seul » (7,64 à 7,80).

**Recette.**

| Verbe | Geste d'objet | Réglages |
|---|---|---|
| tomber, planter | chute, contact, rebond | `y:-700 → 0`, 0,13 s `power2.in` ; rebond 14 px, 0,08 s `yoyo` |
| filer, échapper | l'objet fonce vers la caméra et sort par un coin | `scale 1 → 3`, `rotation 25`, `blur 0 → 16`, 0,2 s `power2.in` |
| creuser, chercher | tranchée qui s'ouvre + tilt vers le bas | `clip-path` en V, 0,3 s ; caméra `y -= 300` en 0,05 s |
| repartir de zéro | rembobinage | ◀◀, bandes de tracking, saccades verticales de 3 images, 0,5 s |
| trier, filtrer | perdantes à 30 % puis sortie, gagnantes regroupées | `opacity .3` 0,1 s ; FLIP (animer de l'ancienne à la nouvelle position mesurée) 0,2 s |
| trouver | traversée d'une foule jusqu'à un seul objet net | `scale ×4` 0,3 s `power2.in`, flou croissant sur les autres |
| rassembler, en un seul | aspiration au centre | `x,y → 0`, `scale .2`, 0,16 s `power3.in` |
| supprimer | la ligne jaillit, pivote de -25°, tombe | lemlist 12,90 à 14,77, 3 plans à raccord |

### Loi 8. Un ou deux mécanismes signature, répétés ; un registre de texte = un mouvement

**Énoncé.** Une vidéo choisit **un ou deux mécanismes de révélation** et les répète 4 à 8 fois, au lieu d'en inventer un par plan. Chaque registre de texte n'a qu'un seul mouvement possible. Le mécanisme du logo (et un objet de l'accroche) est rejoué à l'identique à la fin : c'est la rime.

**Preuves.**
- Calendly « la ligne qui s'ouvre » : tablette (4,50), vignettes (6,37 ; 6,63), fente de Pixel (7,80), page de réservation (19,67), vignettes du mur (29,07 ; 30,7 ; 32,1), plus le curseur-auteur des plans 1 à 5.
- Collective : « l'anneau qui apporte l'objet » (1,20 ; 17,1 ; 34,4 ; 35,2 ; 36,1 ; 36,9 ; 50,87), « le mot géant qui file » (plans 3, 9, 20, 37), « le point qui naît » (5 fois). 3 registres de texte, un mouvement chacun : petit mot à mot flou vers net, géant métallique derrière un objet remplacé sur place, géant blanc qui file.
- Taapit : carte de chapitre à interrupteur ×5 (8,2 ; 27,4 ; 38,5 ; 51,5 ; 57,0), seules la direction de sortie et la longueur du fantôme changent ; frappe à tête verte partout.
- Aikido : pastille qui déborde puis se resserre (1,52 ; 27,8 à 30,5 ×3 ; 36,8 ; 58,7 ; 70,1).
- Rimes : Calendly logo identique à 16,43 et 37,0 ; Collective logo identique à 24,8 et 52,8, fiche et anneau de l'accroche rejoués à 17,1, orbites des « mêmes profils » (9,4) devenues le décor de la carte de fin (54,2) ; lemlist pilule logo ×3 (3,40 ; 29,13 ; 44,92).

**Recette.** Le storyboard déclare les signatures en en-tête ; l'animation les code une fois, en fonctions réutilisées.
```js
function lineOpen(panel,t){                         // Calendly : trait de 2 px qui s'ouvre en panneau
  tl.fromTo(panel,{clipPath:'inset(49.5% 0 49.5% 0)'},{clipPath:'inset(0% 0 0% 0)',duration:.22,ease:'power3.out'},t)
    .fromTo(panel.firstElementChild,{scale:1.08},{scale:1,duration:.4,ease:'power2.out'},t);
}
function ringBring(ring,obj,t){                     // Collective : l'anneau apporte l'objet
  tl.fromTo(ring,{scale:0,borderWidth:6,opacity:1},{scale:1,duration:.15,ease:'expo.out'},t)
    .fromTo(obj,{scale:.3,rotation:-40},{scale:1,rotation:0,duration:.3,ease:'back.out(1.6)'},t+.03)
    .to(ring,{scale:1.5,borderWidth:1,opacity:0,duration:.45,ease:'power1.out'},t+.15);
}
```
Règle d'écriture : un plan qui révèle un objet sans passer par une signature doit le justifier (métaphore de la loi 7).

### Loi 9. La profondeur : avant-plan flou, flou de profondeur, parallaxe

**Énoncé.** Chaque plan tenu montre au moins 3 niveaux sans vraie 3D : un **avant-plan flou** coupé par le bord du cadre, un **sujet net**, un **fond** ; la netteté **bascule** sur l'élément actif ; pendant les dérives, les niveaux glissent à des vitesses différentes (**parallaxe** de 2:1 à 3:1). Les mots géants passent derrière ou devant un objet, jamais à côté.

**Preuves.** Taapit : icônes ≈ 3 fois plus rapides que le texte pendant la dérive (+20 px contre +6 px en 0,6 s) ; nuage final net au milieu, flou devant et derrière (69,8 à 72,8). Collective : cartes profil géantes et floues aux bords (2,8 à 6,0) ; mise au point perdue juste avant un mot géant (8,47 à 8,6) ; « LinkedIn », « CVthèques », « Non disponible » derrière la fenêtre ou la carte (4,1 à 14,4). lemlist : réveil flou en avant-plan (0,90), bascule de netteté quand la carte arrive (5,87 à 6,00), moustique (18,70), curseur géant (30,2). Calendly : mur qui passe flou pendant le lancer (34,2 à 34,5), parallaxe 135 px contre 85 px (6,10 à 7,80). Aikido : notifications de bord coupées, translucides et floues ; tuiles de fin en parallaxe de 2 à 4 px/s.

**Recette.**
```css
.fg  { filter: blur(10px); transform: scale(1.8); }   /* coupé par le bord ; pré-flouter l'image si elle est fixe */
.mid { filter: none; }
.bg  { filter: blur(4px); opacity: .85; }
.giant { z-index: 1; } .card { z-index: 2; }           /* le mot géant DERRIÈRE l'objet qui le masque en partie */
```
```js
[['.bg',.35],['.mid',1],['.fg',2.8]].forEach(([s,k])=>tl.to(s,{x:`-=${40*k}`,duration:D,ease:'none'},t0)); // parallaxe
tl.to('.bg',{filter:'blur(8px)',duration:.25},t).to('.hero',{filter:'blur(0px)',duration:.15},t);            // bascule de netteté
```

### Réglages retenus sur le film final, prioritaires sur les références

Issus des retours sur `examples/ligne-du-temps-v8/`. La liste complète, telle que le skill l'applique :
`.claude/skills/motion-design/SKILL.md`, section « House rules ».

- **La phrase de la voix se lit** : sous-titre en bas au centre (y ≈ 900), 60 à 64 px, ombre légère pour se détacher du fond, mot par mot ; jamais en haut à gauche. La bande basse reste libre d'éléments importants.
- **Un seul geste à la fois dans une transition** : trop d'objets qui bougent en même temps perdent le spectateur. Une transition = une idée lisible en une seconde.
- **Une seule chose à regarder à la fois** : la caméra isole le sujet de la phrase et ne montre l'ensemble qu'au moment où il a du sens. Un zoom franc dans un seul sens est bienvenu, jamais un aller-retour du décor.
- **Les pics sont élégants, pas encadrés** : un trait fin ou un coup de pinceau effilé à la couleur d'accent sous LE mot clé, plutôt qu'une grosse pastille pleine ou un mot énorme ; jamais une ligne du décor qui traverse la phrase.
- **Pas de tenue immobile d'une seconde** et pas de symbole abstrait qui ne dit rien (un compteur « J+1 096 → J+0 ») : chaque image illustre littéralement la phrase.

### Loi 10. La fin rassemble le film, puis un curseur arrive et clique

**Énoncé.** La fin ramasse le film en un geste (implosion puis explosion, travelling dans le nuage des interfaces déjà vues, carte qui grandit depuis un point de fuite), puis un curseur arrive d'un seul mouvement en courbe (0,4 à 0,5 s, `power3.out`), clique **directement** avec un état pressé en 3 à 4 couleurs et une onde, et le film sort sans image figée (iris, noir, ou tenue qui vit). Certaines références font hésiter le curseur (contact, recul, retour, chez Taapit) : c'est écarté ici, l'hésitation ralentit la fin.

**Preuves.**
- Aikido : implosion ×0,15 en 0,6 s `power3.in` (68,6 à 69,2), logo + 6 tuiles qui explosent en 0,3 s (69,24 à 69,5) ; curseur en courbe de 1 s à travers le logo (72,2 à 73,2), clic sur « done » (74,04), anneau puis iris noir (74,32 à 75,12).
- Taapit : travelling avant de 3 s dans ≈ 30 cartes de toutes les UI (interfaces) du film, `power2.in`, flou selon la distance (69,8 à 72,8) ; curseur vert qui touche le bouton (73,10), recule avec des éclats, revient (73,58), micro-glitch, clique à 74,38 (1,3 s d'hésitation), pilule qui se remplit en 0,12 s avec surcourse, tenue 3 s.
- Slack : kaléidoscope (46,5 à 48,1), carte qui grandit jusqu'au plein cadre en 0,7 s `expo.out` (48,23), clic à 49,90 avec bouton aubergine, mauve, blanc, mauve, aubergine en 0,27 s.
- Collective : clic 56,85, point blanc qui devient anneau en 0,15 s, orbites qui tournent jusqu'à 60,0. lemlist : bouton qui naît en largeur, clic 46,35, puis URL tapée (48,63 à 49,10).

**Recette.**
```js
tl.to('#lastScene',{scale:.15,duration:.6,ease:'power3.in'},T)                               // implosion
  .set('#endCard',{autoAlpha:1},T+.6)
  .from('.tile',{x:0,y:0,scale:.3,rotation:i=>((i*37)%50)-25,filter:'blur(10px)',             // rotation tirée de l'index,
                 duration:.3,ease:'power2.out',stagger:.02},T+.6);                            // jamais du hasard ; explosion
tl.fromTo(cur,{x:bx+420},{x:bx,duration:.45,ease:'power3.out'},T+1.2)                       // un seul mouvement en courbe :
  .fromTo(cur,{y:by+260},{y:by,duration:.45,ease:'power2.out'},T+1.2)                        // x et y sur deux courbes
  .to([cur,btn],{scale:.85,duration:.06,yoyo:true,repeat:1},T+1.65)                           // clic direct : pression
  .to(btn,{keyframes:[{backgroundColor:ACC_PALE,duration:.03},{backgroundColor:'#fff',duration:.17},
                      {backgroundColor:ACC,duration:.07}]},T+1.65)
  .fromTo(fill,{scaleX:0},{scaleX:1,duration:.12,ease:'power3.out'},T+1.65);                  // bouton qui se remplit
```
Carte de fin : 3 à 6 s, dont 2 à 3 s de tenue vivante après le clic (orbites, dérive, respiration), puis iris ou noir.

## 3. Le format d'un storyboard de ce niveau

### 3.1 En-tête (une fois par film)

```
# Storyboard : <titre> · <durée> s · <format> · voix <narrative | jouée | aucune>
MONDE
- Acte <n> : #world <L×H écrans>, scènes S1 (x, y), S2 (x, y) ; fond <couleur + texture qui rend la dérive visible>
- Couleurs de rôle : accent = <…> ; négatif = <…> (une couleur par rôle ou par acte)
SIGNATURES
- Mécanisme 1 : <nom> · fonction <lineOpen | ringBring | …> · occurrences prévues <t1, t2, …>
- Mécanisme 2 : <…>
- Registres de texte : <petit mot à mot : un mouvement> ; <géant : un mouvement> ; <réservé à …>
- Rimes : <logo t1 = logo t2> ; <objet de l'accroche rejoué à t>
PARTITION CAMÉRA
- Dérive par acte : <vitesse, direction alternée> ; événements : <t · type · facteur · durée · cible>
VOIX
- Mots : <mot@t …> ; silences > 0,4 s : <t à t> (chacun est un plan)
COUPES (quota selon la voix)
- <t · premier mot · raison>
```

### 3.2 Bloc plan (un plan = un bloc)

```
### P<n> · <in> → <out> (<durée> s) · <acte>
VOIX : « mot@t mot@t … » ; silence <t à t>
TEXTE ÉCRAN : « … » · registre <…> · mot accent <…> · écart <avance | synchro | aucun texte>
IMAGE DE DÉPART : <ce qui est à l'image in : objets, échelle en % h, position, fond>
ÉTAPES (≈ toutes les 0,5 s, jamais plus de 1 s sans événement)
- <t> : <élément> <propriété de → à>, <durée>, <courbe> ; <ce qui continue de bouger>
- <t+0,5> : …
PISTE CAMÉRA : dérive <vecteur, %/s> ; <t> <cran | whip | push | pull> <facteur> <durée> <courbe> → cible <…>
COUCHES ET PROFONDEUR : avant-plan <…> / sujet <…> / fond <…> ; parallaxe <k> ; couches animées <courant / pic>
OBJET-PONT ET VECTEUR : <objet> devient <rôle> en P<n+1> | aucun : sortie <direction, durée, courbe> → entrée P<n+1> <même vecteur>
SON : <bruitage> à <t>, calé sur <geste | mot> (la musique n'impose pas les coupes)
IMAGE CLÉ : <t> : <la vignette à dessiner, en une phrase>
```

### 3.3 Exemple rempli : Collective, plan 30

Le plan 30 du film de Collective, écrit comme il aurait dû l'être avant l'animation. La ligne SON et les libellés exacts des pilules sont des propositions ; tout le reste suit le film.

```
### P30 · 33,3 → 37,5 (4,2 s) · solution
VOIX : « … les meilleurs freelances » (fin 34,18) ; « disponibles »@34,18 ; « qualifiées »@35,20 ;
       « TJM »@35,98 (taux journalier moyen) ; « coordonnées »@36,86
TEXTE ÉCRAN : titre « Les meilleurs Freelances » · registre petit, blanc · une pilule blanche par adjectif,
              le mot dit · écart ± 0,2 s
IMAGE DE DÉPART : fin du push-in sur la carte centrale du carrousel : carte freelance (UI blanche : photo, nom,
                  badges, TJM) au centre, coupée par le bas ; fond bleu électrique à lignes topographiques
ÉTAPES
- 33,3 : fin du push (power2.out) ; le titre s'écrit au-dessus de la carte, mot à mot
- 33,8 : titre posé ; la caméra dérive (constante du film : jamais d'image figée)
- 34,3 : anneau blanc 6 px, ø 10 → 20 % h en 0,15 s (expo.out), qui passe PAR-DESSUS le titre
- 34,4 : pilule « Disponibles » dans l'anneau : scale 0,3 → 1, rotation -40° → 0, 0,3 s (back.out(1.6))
- 34,55 à 34,8 : l'anneau s'ouvre encore (×1,5), s'amincit, s'efface ; la pilule reste
- 35,2 : anneau + pilule « Qualifiées » ; la rangée s'allonge et se recentre
- 35,7 : tenue vivante (dérive)
- 36,1 : anneau + pilule « TJM »
- 36,9 : panneau « Coordonnées » glisse à droite de la carte ; anneau + 4e pilule
- 37,5 : whip vers la droite ; « Vous » naît en fondu au centre
PISTE CAMÉRA : dérive permanente ; 33,3 fin de push (power2.out) ; à-coups de 0,1 s à 34,3 / 35,1 / 36,0 / 36,8
               (léger recadrage, flou) ; 36,8 dézoom pour loger le panneau ; 37,5 à 37,67 whip droite (flou fort)
COUCHES ET PROFONDEUR : fond topographique / carte / pilules / anneau devant le titre ; courant 2, pic 3
                        (caméra + anneau + pilule)
OBJET-PONT ET VECTEUR : aucun objet ; vecteur : whip vers la droite (0,17 s) ; « Vous » naît au centre pendant
                        le whip, puis la fiche de poste de P31 grandit au-dessus de lui
SON : (proposition) tic sec sur chaque à-coup ; pop grave sur chaque pilule ; souffle sur le whip de 37,5
IMAGE CLÉ : 36,95 : carte coupée en bas, rangée de 4 pilules blanches sous le titre, anneau blanc grand ouvert
            qui chevauche le titre, panneau Coordonnées qui sort à droite
```

### 3.4 Passage au STORYBOARD.md HyperFrames

- Un bloc plan devient une ligne `Scene n (in à out)` de sa frame ; les ÉTAPES deviennent la description de la Scene, dans l'ordre et avec leurs temps ; VOIX alimente les `Word cues`.
- PISTE CAMÉRA devient une ligne `camera:` par frame, animée sur `#drift`, `#cam` et `#world` (loi 1), jamais mélangée aux tweens des objets.
- L'en-tête remplace la section « Video direction ». À supprimer de celle de la v6 : « One camera move per scene at most. Holds are still. » (contredit les lois 1 et 2).

## 4. Écart avec notre v6

| Loi | Ce que font les agences | Ce que fait la v6 | À changer |
|---|---|---|---|
| Rythme en événements | un événement toutes les 0,5 à 1 s ; douleur 9,3 contre solution 5,4 plans / 10 s (Collective) | 31 % des tranches de 0,1 s quasi immobiles ; tenues sans mouvement à 3,0 ; 4,1 ; 5,3 ; 15,2 (énergie 0,00) ; 24,5 ; 29,0 ; 37,3 (1 s) ; 41,8 (1,4 s) ; douleur 5,6 contre solution 5,0 | douleur à 8 ou 9 plans / 10 s ; plan 13 (20,6 à 26,0) resserré à un « TOI. » toutes les 1,2 s ; aucune fenêtre de 0,5 s immobile hors silence écrit |
| 1. Monde et caméra | un monde parcouru (Aikido 0 à 25), dérive permanente + crans (Taapit) | caméra fixe ≈ 95 %, 5 mouvements (2,3 s cumulées) ; chaque frame peint son propre fond | un `#world` par acte : site, devis, frise, WhatsApp, écran verrouillé sur la même toile sombre ; Claude, site, devis sur le papier ; piste caméra écrite à part ; un cran par « TOI. » vers la ligne barrée |
| 2. Deux vitesses | gestes de 1 à 6 images, dérives, tenues vivantes | direction « smooth long-tail settles (power3.out) », « Holds are still » ; navigateur qui monte en 0,4 s (0,6 à 1,0) ; 1,4 s figée pour finir (41,8 à 43,2) | apparitions ≤ 0,15 s en `expo.out` ; une couche vivante nommée pour chaque tenue ; retirer « Holds are still » |
| 3. Objet-pont et vecteur | 89 à 95 % des jonctions par objet ou caméra, 0 à 2 effets | 11 effets génériques sur 19 ; 3 dédoublements (2 iPhone à 10,94, 2 fenêtres Claude à 17,45, 2 devis à 25,98) ; « 1 000 € » qui s'éteint (3,43) ; devis jeté hors champ (5,74) | « 1 000 € » vole dans la case prix de la ligne 1 ; cran dans la ligne 3 qui s'ouvre sur la frise ; le même iPhone glisse au centre et s'éteint puis se rallume ; la demande tapée vole sous le titre du site et devient le bouton (19,63) ; ce bouton barre la ligne 1 (20,6) ; « libre. » se contracte en caret qui écrit « Pas besoin » (31,9) |
| 4. Trop grand et flou | Slack atterrit (×1,15, 1 à 3 images) ; Aikido « -85% » ×6 depuis la caméra | carte qui glisse de la droite (3,60), navigateur qui monte (0,6 à 1,0), code déjà fondu à 15 % (32,1) ; bons : tampon « SUR DEVIS » (7,80), « TOI. » (21,8) | devis, iPhone, fenêtre Claude et site entrent par `land()` puis reculent ; « 1 000 € » arrive par `fromCamera()` au lieu du compteur de 0,27 s illisible |
| 5. Calage voix | image 0,1 à 0,6 s avant le mot-image ; silences écrits comme des plans ; phrases sans texte choisies | texte bien calé (0 à 0,1 s) mais aucune image en avance (tampon 0,02 s après « sur devis ») ; « pour tout ce qui est technique » dit, jamais montré (12,56 à 13,30) ; 4 s sans voix en fin, dont 1,4 s figée | tampon et « TOI. » 0,15 à 0,3 s avant leur mot ; écrire les silences (14,05 à 14,94 ; 39,14 à 43,2) comme des plans avec action muette ; « technique » : code net et dense 0,4 s |
| 6. Coupe | voix narrative : 1 à 3 coupes, masquées, au changement d'acte | 1 coupe (14,03, « Stop. »), conforme ; mais 4 fondus floutés (15,77 ; 19,63 ; 29,6 ; 31,9) dont un à la place d'une coupe voulue | 15,77 : la fenêtre Claude monte devant « Aujourd'hui, » (profondeur) ; 29,6 : recul caméra continu ; 0 fondu |
| 7. Métaphore sur le verbe | « tombe », « file », « creuser », « trouver » joués à ± 0,1 s (Collective) | bons : « planté » (Make grise, 7,28), « libre » (le devis s'envole, 30,7), « zéro » (plongée, 36,15) ; muets : « expliques » (frappe à 2,5 % h), « servir » (comète de 2 px, 28,4), « technique » | « expliques » : cran ×1,8 dans le champ ; « t'en servir » : la pastille remplit le cadre avec une vraie traînée terracotta ; « relance » : chaque bulle tombe avec rebond |
| 8. Signatures et rimes | 1 ou 2 mécanismes répétés 4 à 8 fois ; logo rejoué | pastille de texte tenue tout le film (bien) ; révélations d'objets toutes différentes ; logo une seule fois ; le bouton « JE PRENDS RENDEZ-VOUS » du site (19,83) et celui de la carte de fin (39,8) riment sans être joués pareil | signature d'objet : le cadre de sélection pointillé de 1,0 s, tracé par le curseur, révèle chaque objet (site, devis, frise, téléphone, fenêtre Claude, zéro) ; le bouton de fin apparaît avec le même anneau qu'à 19,83 |
| 9. Profondeur | 3 niveaux, avant-plan flou, parallaxe 3:1, mot géant derrière un objet | 6 plans sur 20 à 2 niveaux, tous figés ; aucune parallaxe ; aucun mot géant derrière un objet | « Aujourd'hui, » derrière la fenêtre Claude ; « TOI. » devant le devis, sur la ligne qu'il barre ; panoramique de 8,65 en 2 niveaux (frise ×1, halo ×0,35) ; notifications qui passent devant la caméra, floues (12,6 à 13,55) |
| 10. Fin | implosion ou travelling dans les UI ; curseur qui arrive et clique ; bouton qui se remplit ; iris ou tenue vivante | plongée dans le zéro (36,15 à 36,95, le meilleur pont) ; puis carte de 6,3 s d'un bloc, logo seul 1 s, bouton non accent, clic sans hésitation (41,4), 1,4 s figée | après « pour de bon » : 1,5 s de travelling dans le nuage des UI du film ; curseur qui arrive en courbe et clique directement vers 41,6 ; bouton qui se remplit de terracotta ; vagues qui dérivent jusqu'à 43,2 ou iris noir |

## 5. Grille de contrôle d'un storyboard (avant d'animer)

1. L'en-tête existe : carte du monde (coordonnées des scènes par acte), fond texturé par acte, couleurs de rôle, 1 ou 2 signatures avec leurs occurrences datées, registres de texte (un mouvement chacun).
2. Chaque plan a une PISTE CAMÉRA : une dérive chiffrée et des événements datés avec cible ; la caméra n'est jamais à l'arrêt plus de 0,5 s hors silence écrit.
3. Les ÉTAPES de chaque plan ne laissent aucun trou de plus de 1 s (0,3 s dans les 3 premières secondes). Au rendu : aucune fenêtre de 0,5 s sous 0,25 d'énergie de mouvement hors silence écrit.
4. Toute apparition dure ≤ 0,2 s ; toute dérive ≥ 1 s ; la zone 0,3 à 0,9 s n'est utilisée que par la caméra ou le curseur, avec une courbe `expo`, `power3` ou `power4`.
5. Chaque tenue de plus de 0,5 s nomme sa couche vivante (dérive, boucle, rotation) ; zéro image figée, fin comprise.
6. Chaque jonction nomme son objet-pont et son nouveau rôle, ou son vecteur (direction, durée, courbe) repris à l'entrée du plan suivant ; zéro dédoublement d'objet.
7. Transitions « effet » (fondu, flou-fondu, zoom-through ou glissement sans objet) : 2 au plus sur tout le film.
8. Coupes franches au quota de la voix (narrative : 0 à 4, aux changements d'acte, masquées) ; chacune a sa ligne « t, premier mot, raison ».
9. Chaque entrée d'élément principal a un état de départ écrit (×1,1 à ×6 + flou, ou un point) ; aucun fondu à taille finale.
10. Chaque mot-image a son écart écrit (avance de 0,1 à 0,6 s) ; chaque changement de composition tombe sur le premier mot de l'idée à ± 0,1 s ou dans un silence ; chaque silence > 0,4 s est un plan avec son action.
11. Au moins 3 verbes de la voix sont joués physiquement par un objet, contact à ± 0,1 s de la syllabe.
12. Au moins la moitié des plans ont 3 niveaux (avant-plan flou, sujet net, fond), une parallaxe par acte au minimum, et chaque mot géant passe derrière ou devant un objet.
13. Couches animées : régime courant ≥ 2, pic 3 à 4, un seul élément actif à la fois.
14. Rime : le mécanisme du logo ou un objet de l'accroche est rejoué à l'identique avant la fin.
15. Fin : un geste qui rassemble le film, un curseur qui arrive en courbe et clique directement, sans hésitation (état pressé en 3 couleurs, onde), 2 à 3 s de tenue vivante, sortie en iris ou au noir.
