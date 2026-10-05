# Patterns du motion design SaaS qui performe

Bibliothèque des patterns du motion design, ce qui ressort après avoir regardé pas mal de vidéos de motion design : ceux des films de lancement
SaaS qui circulent le plus sur LinkedIn et X. Les marques citées en exemple sont celles de films de lancement publics ;
elles appartiennent à leurs propriétaires, aucune image ni vidéo n'est reproduite ici, et ce dépôt n'est affilié à
aucune d'elles.

À utiliser **avant d'écrire un storyboard** (choisir les patterns) et **après le premier rendu** (grille de contrôle en fin de
fichier). Les recettes sont écrites pour HyperFrames (HTML + GSAP), mais valent pour n'importe quel outil. Pour écrire le
storyboard plan par plan au dixième de seconde (caméra, objets-ponts, calage voix, gabarit) : `STORYBOARD-CRAFT.md`, qui
a corrigé ici D1, B1, C1, F3, G1 et les règles de rythme et de logo. Les réglages retenus sur le film final de la
méthode (`examples/ligne-du-temps-v8/`) sont signalés « Réglage retenu » : ils passent avant l'observation.

## Le profil type

- **Durée** : 40 à 80 s, souvent autour d'une minute. 16:9 presque toujours.
- **Voix off** : dans la grande majorité. Les autres sont musicales et tout passe par le texte à l'écran.
- **Squelette** (présent dans quasiment toutes) : douleur (20 à 45 % de la durée), pivot, logo, 3 à 4 bénéfices montrés par des
  gestes d'interface, preuve chiffrée, carte de fin avec bouton cliqué.
- **Rythme** : une nouvelle composition toutes les 1 à 4 s, mais surtout **un événement toutes les 0,5 à 1 s** (arrivée,
  geste, clic, cran de caméra) : c'est cette cadence qui compte, pas le nombre de plans (Aikido : 2,8 plans / 10 s, 3 à 6
  temps par plan). Tout s'enchaîne en continu (morph, caméra, objet qui traverse) ; le nombre de coupes franches dépend de
  la voix (voir D1).
- **Logo** : jamais comme signature à la première image. Le logo complet arrive entre 5 et 30 s, au pivot ; il peut
  apparaître plus tôt s'il est un objet du récit qui se transforme aussitôt (Slack : pastille logo à 0,07 s qui devient la
  barre de recherche ; lemlist : pilule à 3,4 s).

## Pourquoi elles circulent

1. **Lisibles sans le son.** Le texte à l'écran reprend la voix mot par mot, en version réécrite et raccourcie : sur un fil
   LinkedIn en lecture automatique muette, la vidéo se comprend quand même.
2. **Elles parlent à la cible dès le premier mot** (« Formateurs indépendants », « Tu es en Terminale », « Frustrated with
   security tools…? »), et l'image de la première seconde illustre exactement ce mot.
3. **La douleur est montrée dans les outils que la cible utilise** (Gmail à badge rouge, tableur Excel, ChatGPT, visio,
   fenêtre Windows rétro) : reconnaissance immédiate, avant toute explication.
4. **Une grammaire visuelle très serrée** : une seule couleur d'accent, un seul mécanisme de mise en valeur, un ou deux fonds.
   Rien ne se contredit, donc l'œil ne se fatigue pas.
5. **De l'émotion** : personnage stressé, voix qui joue un rôle, ironie, chute drôle. C'est ce qui se partage.
6. **Des preuves qui bougent** : chaque chiffre roule jusqu'à sa valeur ou fonce depuis la caméra, au lieu d'être posé.
7. **Une fin qui dit quoi faire** : un seul bouton, qu'un curseur vient cliquer.

(Lecture qualitative : les chiffres de vues ne sont pas publics. Les fréquences ci-dessous sont indicatives : presque
toujours, souvent, régulièrement, parfois.)

---

## A. Accroche (0 à 3 s)

### A1. Premier mot = la cible ou sa douleur (presque toujours)
- **Observable** : la voix s'adresse au spectateur dès le premier mot (cible nommée, question-douleur, douleur affirmée) ; la
  première image est **un mot seul** sur fond presque vide, qui se complète mot par mot. Jamais le logo.
- **Recette** : image 0 = le premier mot de la voix, centré, petit ; chaque mot suivant arrive sur son timestamp ; l'image de
  la seconde 1 illustre littéralement ce mot.
- **Exemples** : QIPLIM « Formateurs indépendants » (0 s), Digischool « Tu es en Terminale » (0 s), Aikido (0-2 s), Machina « On »,
  AssessFirst « One », Juicebox « Still ».

### A2. Interface familière + clic du curseur vers 2-3 s, puis rupture (régulièrement)
- **Observable** : une UI que tout le monde connaît (visio, barre de recherche, ChatGPT, fenêtre Windows), un curseur qui tape
  ou clique entre 2 et 3 s, puis glitch, coupe franche ou inondation de couleur.
- **Recette** : reconstituer l'outil (pas de capture réelle), frappe caractère par caractère sur ~2,5 s, clic avec ripple, puis
  rupture de 0,3 à 0,5 s (glitch RVB, aplat plein écran de la couleur de l'outil, noir).
- **Exemples** : Upmeet (clic sur raccrocher à 2 s, glitch à 2,5 s), Slack (recherche, clic à 2,75 s), Juicebox (Windows rétro),
  BabyLoveGrowth (sketch ChatGPT 0-18 s), Gojiberry (clic « envoyer » qui inonde l'écran en bleu LinkedIn à 1,75 s).

### A3. Ouverture sur un écran vide avec un seul élément (régulièrement)
- **Observable** : fond sombre quasi vide, un seul petit élément (mot, point lumineux, anneau, goutte) qui déclenche la
  construction de la scène ; il revient souvent ensuite comme signature (puce, curseur).
- **Exemples** : Eskimoz (carré bleu lumineux qui sert de curseur de frappe puis de puce pendant tout le film), CopilotCRM
  (goutte qui se scinde), Mush (« Pourquoi » dans un anneau rouge traversé par la caméra).

### A4. Promesse de durée (parfois)
- « 60.S » en 3D (lemlist), « J'ai 45 secondes » dans un viseur (Slack) : le spectateur sait que ce sera court.

---

## B. Texte et typographie

### B1. Une composition par phrase, texte mot par mot calé sur la voix (presque toujours)
- **Observable** : chaque phrase de la voix a son écran ; le texte reprend la phrase (ou sa version courte), **centré, petit**
  (2 à 5 % de la hauteur) ; chaque mot arrive au moment où il est prononcé, souvent
  flou ou gris puis net ; parfois les mots à venir sont déjà là en gris très pâle. C'est une **réécriture choisie phrase
  par phrase**, pas un sous-titre intégral : Aikido écrit « One platform to rule them all » sur « No fragmented tools
  required » et n'écrit pas « Aikido makes it simple » pour garder le nom au logo ; certaines phrases n'ont aucun texte
  (lemlist « Vous savez ce petit… ») ; Calendly n'a aucun sous-titre, chaque phrase y a un geste d'image.
- **Recette** : minutage mot par mot de la voix (Whisper) ; par mot `fromTo({opacity:0, filter:'blur(8px)', y:8}, {opacity:1,
  filter:'blur(0)', y:0, 0,3 s, power3.out})` sur son timestamp ; variante « mots à venir » : tous les mots posés à 15 %
  d'opacité, chacun passe à 100 % sur son timestamp.
- **Réglage retenu** : la phrase de la voix est un sous-titre **en bas au centre** (60 à 64 px, bande y 890 à 980 réservée
  à elle seule, 45 signes au plus par morceau), mot par mot : chaque mot arrive gris puis passe à l'encre. Jamais en haut
  à gauche. Seuls 2 ou 3 « moments typographiques » nommés dans le storyboard font de la phrase l'image, centrée, 84 px au
  plus, sans sous-titre en bas pendant ce temps.

### B2. Un seul mot-clé par phrase, dans l'unique couleur d'accent (presque toujours)
- **Observable** : la phrase est neutre (blanc ou noir), un mot ou un groupe de mots passe dans la seule couleur d'accent de la
  marque, en même temps que la voix l'appuie. Cette couleur ne sert à rien d'autre dans le texte. Une deuxième couleur est
  parfois réservée au négatif (rouge).
- **Recette** : décider le mot appuyé de chaque phrase dans le storyboard ; un seul par phrase ; la couleur arrive 0 à 2 images
  avant le mot dit.

### B3. La pastille qui se trace, puis le mot s'écrit dedans (souvent)
- **Observable** : une forme pleine de la couleur d'accent (pastille arrondie, rectangle, coup de pinceau, surligneur) s'étire de
  gauche à droite en 0,25 à 0,3 s, puis le mot s'écrit en blanc à l'intérieur (ou au même rythme). Variantes : la pastille
  arrive inclinée d'environ -10° et se redresse ; bordure pointillée façon outil de design ; la pastille se redimensionne
  quand le texte change.
- **Recette** : `span.pill` avec `transform-origin: left` → `scaleX 0→1` en 0,28 s `power3.out`, puis les lettres du mot
  `opacity 0→1` en stagger 0,02 s ; pour la variante inclinée `rotation:-10 → 0` en 0,4 s.
- **Exemples** : Aikido 1,5-2 s, Digischool 0,5 s (pinceau rose), HIGHCOM 4 s, Tulyp 2,25 s, Free, CareCare, MagicPost, Blitz.
- **Réglage retenu** : le mot clé du sous-titre passe dans une **petite boîte à la couleur d'accent de la marque** (angles
  nets, rayon 3 px, texte dans la couleur du fond), jamais une boîte noire ; elle se trace de gauche à droite en 0,16 s
  `power3.out`, 0 à 2 images avant le mot.

### B4. Contraste d'échelle : texte courant petit, quelques mots géants aux pics (souvent)
- **Observable** : les phrases restent petites ; aux pics émotionnels, un mot isolé arrive à 30-50 % de la hauteur, déborde
  parfois du cadre, passe **derrière** un objet ou une carte d'interface (profondeur), ou **derrière la tête** d'une personne
  détourée en face caméra. Souvent avec flou de mouvement latéral.
- **Exemples** : « Stop » (CareCare, DocShipper), « Hhhmm... » (Eskimoz), « Encore » en dégradé métallique (Collective),
  « But we're at 1M ARR!! » (BabyLoveGrowth), « USERS » derrière le fondateur (Submagic), « telco / OEM / retailer » avec un
  bâtiment 3D devant (Dipli).
- **Réglage retenu** : pas de mot géant ni de gros encadré. Un pic se souligne d'un **trait fin** (4 px, arrondi) ou d'un
  **coup de pinceau effilé** à la couleur d'accent, sous LE mot clé seulement, qui se dessine de gauche à droite en 0,3 à
  0,5 s pendant que le mot est dit. 3 ou 4 pics par film.

### B5. Préfixe fixe, mot qui tourne au même endroit (régulièrement)
- **Observable** : quand la voix énumère, le début de phrase reste en place et seul le dernier mot (ou la pastille) change toutes
  les 1 à 1,5 s, souvent avec l'illustration qui change en même temps.
- **Exemples** : Augment « Faster → Smarter → Stronger », Blabla « C'est perdre » + en engagement / en image / en ventes.

### B6. Trios (régulièrement)
- Trois mots courts ou trois pastilles, un par seconde, au même endroit ou autour d'un objet : « C'est cher / C'est long / C'est
  compliqué » (SHADOW), « Scanning / Alerting / Remediation » (Aikido).

### B7. Détails qui font « fait main »
- **Interlettrage qui se resserre** à l'apparition (lettres très espacées qui se rapprochent en 0,5 à 1 s) : Agilia, YoungData,
  Splitter, Plus que pro, Eyras.
- **Pile d'échos verticale** : le mot net au centre, 4 copies floues et transparentes au-dessus et en dessous qui se resserrent
  (« Stop », « Commencer », « TOUT ») : CareCare, Machina, DocShipper.
- **Mot fantôme** géant et très pâle en fond derrière la phrase nette : Upmeet, Machina, DocShipper.
- **Contraste de style dans la ligne** : partie légère grise + mot gras noir, serif fine + sans grasse, italique coloré.
- **Traits d'emphase dessinés** (éclairs, traits rayonnants, cercle pointillé, point d'interrogation) qui poppent avec le mot fort.
- **Pastilles ✕ / ✓** : ✕ pour les défauts, ✓ pour les bénéfices, dans le même composant.

---

## C. Couleur, fond, lumière

### C1. Une couleur d'accent par rôle, jamais deux pour le même rôle (presque toujours)
- Tout le reste en neutres ; l'accent sert au mot-clé, à la pastille, au bouton final, au curseur. Le plus souvent une
  seule couleur pour tout le film ; variantes : un accent par acte (lemlist, bleu au clair,
  rouge dans l'acte sombre) ou une couleur par rôle (Aikido : violet mot-clé, lavande chiffres, teal contours, rouge
  douleur).

### C2. Deux univers : un fond pour la douleur, un fond pour la solution (souvent)
- **Observable** : la douleur vit sur un fond sombre ou saturé ; au pivot (logo), le fond passe franchement au clair de la marque
  et y reste pour les bénéfices ; souvent retour au sombre pour la carte de fin. C'est le changement de fond qui dit « on
  change d'acte », sans texte. **Alternative** tout aussi fréquente : un seul fond clair toute la vidéo (lot Eyras, Agilia,
  Free…), le rythme venant du texte.
- **Exemples** : LK360 noir → jaune par un cône de projecteur (28-30 s), CareCare anthracite → pêche (19 s), Eskimoz bleu nuit →
  bleu glacier (21,7 s), Crisp noir → blanc (20 s), Dipli violet → blanc par un éclat de particules (28-30 s).

### C3. Le pivot : un temps mort ou un mot d'arrêt juste avant la bascule (régulièrement)
- **Observable** : entre la douleur et le logo, un écran presque vide avec un seul mot ou une question (« Stop », « Une question
  se pose », « Game Over », « Let's fix that »), ou 0,5 à 1 s de noir complet.
- **Recette** : 0,6 à 1,2 s, un mot seul (souvent en pile d'échos), puis la bascule de fond sur le mot suivant.

---

## D. Rythme et transitions

### D1. Continu par objets ; le quota de coupes franches dépend de la voix (presque toujours)
- **Voix narrative** (Aikido 1, Calendly 2, Collective 3) : 0 à 4 coupes franches, aux changements d'acte, souvent
  masquées au sommet du flou d'un mouvement, sur le premier mot de l'acte ou dans un silence.
- **Voix jouée**, personnage ou gags (Slack 22, lemlist 12 + 5 coupes à raccord) : la voix porte la continuité, l'image
  coupe sur le premier mot de chaque idée (± 0,1 s) ; les noirs sont des plans de réplique.
- **Sans voix** (Taapit 12) : coupes structurelles seulement (ouverture de chapitre sur cadre vide, changement de couleur
  du monde, raccord dans l'axe).
- Toujours : aucune coupe gratuite, 0 à 2 fondus par film ; tout le reste passe par un objet qui change de rôle ou par la
  caméra. Détail et recettes : `STORYBOARD-CRAFT.md`, loi 6.

### D2. Transitions « objet » plutôt que transitions « effet »
- **Cercle, anneau ou iris** qui naît au centre et ouvre la scène suivante, en 0,25 à 0,75 s (régulièrement) : QIPLIM (3 cercles
  concentriques en 0,75 s, du problème à la solution), Juno, Butterfl.ai, HIGHCOM.
- **Zoom à travers l'élément** : la caméra plonge dans la pastille du mot-clé jusqu'à ce que sa couleur remplisse le cadre et
  devienne le fond suivant (AssessFirst 0-1,25 s), dans un bâtiment (Juno), dans le logo (Slack).
- **Objet du récit qui traverse** : la tour Eiffel monte, pousse et efface le paragraphe, puis revient en icône derrière le titre
  suivant (FundTruck 8,5-9,8 s) ; une cerise tombe du gâteau dans la terre du potager (Nigloland).
- **Titre qui se range** : un titre seul au centre ~1 s, qui rétrécit et monte, le contenu entre dans la place libérée (Aikido,
  Tulyp, Digischool).
- **Flash ou inondation de couleur** de 0,3 à 0,5 s comme coupe de chapitre (Submagic, Chris Scholly, Gojiberry).
- **Flou de mouvement directionnel** avec lignes de vitesse pour les passages rapides (MergerCircle, Collective, Mush).

### D3. Deux vitesses (Plus que pro)
- Problème en escalade très rapide (4 à 5 compositions / 10 s, flashs), puis une pause au noir avec « Respirez… », puis une
  solution calme et régulière (6 à 7 s par pilier, gabarit répété). Le contraste de rythme fait ressentir le soulagement.

---

## E. Raconter la douleur

### E1. Personnage stressé entouré des étiquettes de sa douleur (régulièrement)
- Figure centrale (mascotte, avatar, vraie personne détourée, simple paire d'yeux), mains sur la tête ou traits de stress, 6 à 8
  pastilles de mots qui poppent ou volent autour en moins de 1 s. Eyras, Komgo, Plus que pro, Aikido (Octocat), QIPLIM.
- Variante « décor fixe narratif » : le même personnage au même bureau pendant 20 s, chaque douleur ajoute un accessoire, il
  vieillit (cleaq 9-30 s).

### E2. Essaim d'objets pour montrer le volume (régulièrement)
- L'objet unitaire de la douleur (email à badge rouge, bulle de chat, CV, feuille) se duplique par dizaines et vole en rotation
  3D autour ou à travers le texte : Slack (déferlante Gmail), Crisp, AssessFirst (pluie de CV), lemlist (pile d'emails).

### E3. La métaphore de la voix prise au pied de la lettre (parfois)
- « On casse les codes » = le mot dans une case cassée (HIGHCOM) ; « vous repartez de 0 » = rembobinage VHS (Collective) ;
  « cerise sur le gâteau » = des cerises tombent (cleaq) ; « Game Over » = une fusée pixel s'écrase (Mush).

### E4. Destruction de l'ancien monde (parfois)
- Les outils de la concurrence explosent en particules (CopilotCRM), la carte de profil éclate (Collective), « not intuition »
  barré (MergerCircle).

### E5. Humour et voix jouée (parfois)
- La voix incarne un personnage (vexé, moqueur, qui improvise) et l'image appuie la chute : BabyLoveGrowth (« That felt
  personal. »), LK360 (le post qui ne récolte que deux likes, dont celui de Maman), lemlist (moustique brûlé), Slack (pizza 3D, bêtisier sur
  noir), Free (« cette vidéo nous a coûté 2 € »).

---

## F. Montrer le produit et prouver

### F1. UI en carte inclinée en perspective, qui se redresse pendant que le curseur agit (souvent)
- Capture réelle ou reconstitution, ombre douce, fond de marque ; la caméra glisse ou pivote jusqu'à la mettre à plat ; le curseur
  clique l'élément dont parle la voix.

### F2. Démo par gestes : taper, cocher, activer (souvent)
- Texte tapé dans un vrai champ (prompt, recherche, message), toggle activé par le curseur au moment où la voix nomme la
  fonctionnalité, cases cochées une par une.

### F3. Chiffres qui roulent ou qui foncent, jamais posés (souvent)
- Compteur qui défile jusqu'à la valeur, avec une pastille d'unité dessous ; parfois la taille grandit avec la valeur ; souvent
  flou de mouvement pendant le défilement. Submagic roule de 999 563 à 1 000 000 derrière le fondateur à la seconde 1 ;
  Taapit sort d'un masque en comptant, +42 à +97 en 0,6 s puis les 3 dernières unités en 0,55 s.
- Variante : le chiffre arrive entier depuis la caméra, ×6 et flou, posé en 0,28 s `expo.out` (Aikido « -85% »).

### F4. Orbite ou couronne autour du centre (régulièrement)
- 6 à 12 icônes d'outils ou avatars en cercle autour du logo ou d'un objet ; des points voyagent sur les lignes ; les lignes
  convergent pour former le logo (Eskimoz, CareCare).

### F5. Preuve sociale en mur (régulièrement)
- Mur de logos clients, chiffres géants un par seconde, visages réels ronds, badges (SOC 2, avis clients).

### F6. Rappel de l'accroche (parfois)
- Un élément de l'accroche revient pour fermer la boucle : « No booleans needed » répond à la requête booléenne du début
  (Juicebox), le bouton raccrocher revient (Upmeet).

---

## G. Fin

### G1. La carte de fin standard (presque toujours)
- Logo (souvent construit : lettres qui tombent ou s'écrivent), promesse d'une ligne, **un seul bouton** plein de la couleur
  d'accent, **un curseur qui entre en courbe, hésite et clique** (onde ou anneau qui s'étend, bouton qui se remplit), URL
  en petit ou tapée dans une barre de recherche. Carte de 3 à 6 s, dont 2 à 3 s de tenue vivante après le clic (orbites,
  dérive), puis iris ou noir : aucune des 6 références de `STORYBOARD-CRAFT.md` ne finit en fondu sur image figée.
  Variante sans bouton : logo rejoué et personnage qui respire (Calendly).
- **Réglage retenu** : pas d'hésitation. Le curseur arrive d'un seul mouvement en courbe (0,4 à 0,5 s `power3.out`) et
  clique directement le bouton (pression, onde).

---

## Grille de contrôle (à passer sur tout storyboard puis sur le rendu)

- [ ] La première image est le premier mot ou ce qu'il désigne, jamais le logo ; le premier mot nomme la cible ou sa douleur.
- [ ] L'image de la seconde 1 illustre exactement le premier mot.
- [ ] Chaque phrase de la voix a sa composition ; la phrase arrive mot par mot sur la voix, en sous-titre en bas au centre (ou centrée pour 2 ou 3 moments typographiques).
- [ ] Un seul mot clé par phrase, dans une petite boîte à la couleur d'accent ; une seule couleur d'accent par rôle (ou par acte), jamais deux pour le même rôle.
- [ ] Un seul mécanisme de mise en valeur (la boîte d'accent qui se trace) répété toute la vidéo.
- [ ] Les pics : un trait fin ou un coup de pinceau effilé sous LE mot clé ; jamais un gros encadré ni un mot géant.
- [ ] Une seule chose à regarder à la fois : la caméra isole le sujet de la phrase.
- [ ] La douleur est montrée dans un outil que la cible reconnaît, et son volume par un essaim.
- [ ] Il y a un pivot explicite (mot seul, noir, question) avant le logo, et le fond change avec lui.
- [ ] Le logo complet n'arrive pas avant 5 s (sauf s'il est un objet du récit qui se transforme aussitôt).
- [ ] Coupes franches au quota de la voix (narrative : 0 à 4, aux changements d'acte ; jouée : sur le premier mot de chaque idée) ; 0 à 2 fondus ; le reste s'enchaîne par des objets.
- [ ] Chaque chiffre roule jusqu'à sa valeur ou fonce depuis la caméra ; aucun n'est posé en fondu.
- [ ] Le produit est montré par des gestes (taper, cocher, cliquer), pas par une capture posée.
- [ ] Un élément de l'accroche revient avant la fin.
- [ ] Carte de fin : un seul bouton, un curseur qui arrive d'un seul mouvement et clique directement, 2 à 3 s de tenue vivante après le clic, puis iris ou noir.
- [ ] Lisible sans le son de bout en bout.
- [ ] Rendu : aucune animation de `letterSpacing` (lettres découpées et déplacées à la place) ; un fond du monde clair posé sous toutes ses séquences, pour que les fondus ne grisent pas.
