# Modèle de storyboard : l'en-tête du film et le bloc d'une séquence

Le gabarit d'un storyboard de niveau agence, tiré de la section 3 de
[`patterns/STORYBOARD-CRAFT.md`](../patterns/STORYBOARD-CRAFT.md) et du storyboard réel de
[`examples/C-le-devis-v7a/STORYBOARD.md`](../examples/C-le-devis-v7a/STORYBOARD.md). Il sert à l'étape 4 de la méthode
(créer le storyboard et les prompts pour l'animation), une fois la direction choisie dans `DIRECTIONS.md`
([`DIRECTIONS-TEMPLATE.md`](DIRECTIONS-TEMPLATE.md)).

Le fichier du projet s'appelle `<projet>/STORYBOARD.md`. Son squelette (avec les champs `{{...}}` à remplacer) est
`.claude/skills/motion-design/templates/STORYBOARD.md` ; ce modèle-ci explique ce que chaque ligne doit contenir, avec un
exemple rempli.

**Vocabulaire**

- **Séquence** (`## Frame n` dans le fichier) : 3 à 6 s, une idée de la voix, un fichier HTML construit par un seul
  sous-agent. Elle devient un prompt (un « paquet ») à part entière.
- **Plan** (`Scene n` dans une séquence) : un cadrage entre deux mouvements de caméra qui changent de sujet. Une arrivée
  d'objet dans le même cadrage n'ouvre pas de plan.
- **Étape** : un événement daté (arrivée, geste, clic, changement d'état, cran de caméra). Une toutes les 0,5 à 1 s,
  toutes les 0,1 à 0,3 s dans l'accroche.
- **Objet-pont** : un objet du plan N qui survit et change de rôle dans le plan N+1 (le prix qui tombe dans sa case, la
  case qui devient un téléphone). À défaut, le **vecteur** : la direction, la vitesse et la courbe de sortie de N fixent
  l'entrée de N+1.
- **Passage de relais** (`handoff_out` de la séquence N, `handoff_in` de la séquence N+1) : l'état exact de l'image à la
  couture (caméra, flou, décor, objets, texte). Les deux lignes sont identiques mot pour mot : c'est ce qui rend la
  couture invisible alors que ce sont deux fichiers écrits par deux agents différents.

**Conventions**

- Temps en secondes avec un point décimal (`5.82`). Dans l'en-tête : temps du film (globaux). Dans une séquence : temps
  locaux (0.00 = début de la séquence), sauf le titre qui rappelle son entrée et sa sortie dans le film.
- `cam(x, y, échelle, rx, rz)` : le point du décor au centre du cadre, l'échelle, l'inclinaison et la rotation de la
  caméra ; `dof(f, b1, b2)` : la ligne nette et les deux niveaux de flou (voir la charte `frame.md` du projet).
- Les noms de champs en anglais (`duration`, `voiceover`, `blueprint`, `rules`, `handoff_in`…) restent tels quels : le
  script qui fabrique les paquets les lit, ligne par ligne : chaque champ `- clé: valeur` et la ligne `Word cues` tiennent
  sur une seule ligne, aussi longue soit-elle. Un identifiant de recette écrit n'importe où dans le bloc est embarqué
  dans le paquet (limite 48 Ko) : n'en cite pas par accident.

## 1. L'en-tête du film (une fois, section « Video direction »)

```
## Video direction

- **Un seul monde** : <le lieu du film (frame.md), l'acte sombre, l'acte clair, la carte de fin>. Chaque séquence peint
  son propre fond sur un calque `class="clip"` de toute sa durée.
- **Coutures invisibles** : toutes les séquences s'enchaînent en `cut` ; la continuité est faite par la caméra : chaque
  couture tombe au sommet du flou d'un mouvement, et le `handoff_out` de la séquence N est recopié à l'identique dans le
  `handoff_in` de la séquence N+1. Exceptions voulues : <t, raison>.
- **Texte** : la phrase de la voix en sous-titre en bas au centre (60 à 64 px, bande y 890 à 980 réservée), mot par
  mot sur ses temps ; un mot clé par phrase dans une petite boîte à la couleur d'accent [boîte : …] ; 3 ou 4 pics
  soulignés d'un trait fin sous LE mot clé [trait : …], jamais un mot géant ni un gros encadré ; 2 ou 3 moments
  typographiques où la phrase est l'image, centrée, 84 px au plus. Aucun autre texte que celui des lignes Scene et des
  vraies interfaces.
- **Une seule chose à regarder** : la caméra isole le sujet de chaque phrase ; un zoom franc dans un seul sens, jamais
  d'aller-retour ; mises en page côte à côte aux marges égales ; zéro décor sans sens, aucune ligne qui traverse une
  phrase.
- **Vraies interfaces** : <lesquelles, d'après quelle capture récente>.
- **Grammaire de mouvement** : deux vitesses (gestes de 1 à 6 images, dérives linéaires permanentes) ; la zone 0,3 à
  0,9 s est réservée à la caméra et au curseur ; aucune tenue figée ; aucune transition « effet ».
- **Négatifs** : diaporama (tout à t = 0), écran de veille (tout qui flotte), objet dédoublé, <…>.

**MONDE**
- Acte <n> (<t> à <t>) : <lieu> ; stations <nom (x, y)>, <nom (x, y)> ; fond <couleur + texture qui rend la dérive visible>
- Couleurs de rôle : accent = <ce qui compte> ; négatif = <…> (une couleur par rôle ou par acte)

**SIGNATURES**
- Mécanisme 1 « <nom> » : <t1, t2, t3, t4> (4 à 8 fois)
- Mécanisme 2 « <nom> » : <…>
- Registres de texte : sous-titre mot à mot = <un mouvement> ; boîte = <un mouvement> ; trait = <un mouvement> ; moment typographique = <un mouvement>
- Rimes : <le geste de la fin (t) rejoue le geste du début (t)>

**PARTITION CAMÉRA** (temps globaux) : <t type cible> · <t type cible> · …

**VOIX** : minutage dans `onsets.json` ; silences de plus de 0,4 s, chacun écrit comme un plan : <t à t (action muette)> · …

**COUPES** (quota selon la voix ; narrative : 0 à 4) : <t · premier mot · raison>

**RYTHME** : douleur <plans / 10 s> ; solution <plans / 10 s> (le tempo change avec l'acte)

**SON** (temps globaux, calé sur les gestes, pas sur les mots) : <bruitage t> · <bruitage t> · …
```

## 2. Le bloc d'une séquence (une par idée de la voix)

```
## Frame <n> : <titre court> · <in> → <out>

- scene: <une phrase : ce qu'on voit du début à la fin de la séquence>
- duration: <durée>s
- transition_in: cut
- status: outline
- src: compositions/frames/<nn>-<slug>.html
- voiceover: "<les phrases exactes de la voix dans cette séquence>"
- type: <hook | pain_point | pivot | demo | payoff | reassurance | cta>
- blueprint: <id de plan type, hyperframes-animation/blueprints-index.md> (Adapt)
- focal: <l'élément principal, puis le suivant>
- rules: <1 à 3 recettes, hyperframes-animation/rules-index.md>
- world: <dark | light>
- handoff_in: à 0.00 : <copie mot pour mot du handoff_out de la séquence n-1>
- handoff_out: à <durée> : cam(<x>, <y>, <échelle>, <rx>, <rz>) flou <px> dof(<f>, <b1>, <b2>) ; caméra <en plein cran, whip, recul…, vitesse> ; dérive <…> ; décor <état> ; <objets à l'écran : position, taille, ancrage> ; lumière <…> ; texte <aucune phrase | …> ; grain <…>

Word cues: <mot@0.00 mot@0.24 …> (temps locaux, depuis onsets.json : onsets.py --window <in> <out>)

Scene <k> (<t> à <t> s) : P<numéro du plan dans le film>, <ce plan en quelques mots>
  TEXTE ÉCRAN : <mots et leurs temps, [boîte : …], [trait : …]> ; écart <avance | synchro | aucun texte>
  IMAGE DE DÉPART : <ce qui est à l'image au début du plan : objets, échelle, position, fond> (ou « handoff_in »)
  ÉTAPES : <t> <élément> <propriété de → à>, <durée>, <courbe> ; <t + 0,5> … (jamais plus de 1 s sans événement,
           0,3 s dans les 3 premières secondes du film)
  PISTE CAMÉRA : dérive <vecteur, %/s ou u/s> ; <t à t> <cran | whip | plongée | recul> vers cam(…) <courbe>, flou <px>
  COUCHES ET PROFONDEUR : avant-plan <flou, coupé par le bord> ; sujet <net> ; fond <flou> ; couches animées <courant / pic>
  OBJET-PONT ET VECTEUR : <objet> devient <rôle> au plan suivant | vecteur : sortie <direction, durée, courbe> reprise à l'entrée
  SON : <bruitage> à <t>, calé sur <le geste>
  IMAGE CLÉ : <t> : <la vignette à dessiner, en une phrase>
```

Cas particuliers :

- **Première séquence** : `handoff_in: aucun (ouverture du film) ; première image = <ce qu'on voit à 0.00>`.
- **Coupe franche voulue** : `handoff_out: aucun raccord de caméra (coupe franche voulue à <t>) ; raccord de position
  seulement : <objet, taille, position>`, et la même phrase en `handoff_in` de la suivante. La séquence qui arrive est
  visible dès sa première image (jamais un fondu depuis le noir).
- **Dernière séquence** : `handoff_out: aucun (fin du film, <noir | iris> à <t>)`.
- **Silence de plus de 0,4 s** : c'est un plan, avec son action muette (un clic, une chute, un objet qui entre).

## 3. Les règles à tenir en l'écrivant

Rappel de la grille de `STORYBOARD-CRAFT.md` (section 5), à passer en entier avant de montrer le storyboard :

- une étape toutes les 0,5 s environ, jamais plus de 1 s sans événement, et aucune tenue figée : chaque tenue nomme ce
  qui continue de bouger (dérive, boucle, rotation) ;
- la caméra n'est jamais à l'arrêt plus de 0,5 s hors silence écrit : une dérive chiffrée et des crans datés avec leur
  cible ;
- toute apparition dure 0,2 s au plus et part d'un état écrit : trop grande (×1,1 à ×6) et floue (6 à 12 px), ou d'un
  point ; jamais un fondu à sa taille finale ;
- l'image devance son mot de 0,1 à 0,6 s ; le texte mot à mot est synchrone à 0,1 s près ; un changement de plan tombe
  sur le premier mot de l'idée ou dans le silence d'avant ;
- chaque couture nomme son objet-pont (ou son vecteur) ; jamais deux copies du même objet à l'écran ; 2 fondus au plus
  sur tout le film ;
- au moins 3 verbes de la voix joués par un objet ; au moins la moitié des plans sur 3 niveaux (avant-plan flou, sujet
  net, fond) ;
- la fin rejoue un geste du début (la rime), puis un curseur arrive d'un seul mouvement et clique directement le seul
  bouton, 2 à 3 s de tenue vivante, sortie au noir ou en iris.

## 4. Exemple rempli (extrait court)

Extrait de [`examples/C-le-devis-v7a/STORYBOARD.md`](../examples/C-le-devis-v7a/STORYBOARD.md), séquence 1 : les champs
de la séquence et un seul de ses cinq plans (le plan 4, une seconde de film). Le décor est un devis de 1500 × 2120 u
décrit au pixel dans `frame.md` ; D1 et D2 sont des états du devis définis dans la même charte. Ce film utilisait
encore la pastille (`[pastille : …]`) ; le film final la remplace par la boîte d'accent du sous-titre (`[boîte : …]`) et
le trait sous le mot-pic (`[trait : …]`) : voir [`examples/ligne-du-temps-v8/STORYBOARD.md`](../examples/ligne-du-temps-v8/STORYBOARD.md).

```
## Frame 1 : Le site, mille euros · 0.00 → 5.82

- scene: Très gros plan sur la ligne 1 d'un vrai devis posé dans le noir ; le mot « site » s'ouvre sur le vrai site et la caméra plonge dedans, puis en ressort pendant que « 1 000 € » tombe dans sa case ; la caméra descend à la ligne 2 où « 600 € » tombe à son tour
- duration: 5.82s
- transition_in: cut
- status: outline
- src: compositions/frames/01-site.html
- voiceover: "Une modification sur ton site ? Une journée. Mille euros. Une nouvelle page : six cents euros."
- type: pain_point
- blueprint: camera-journey (Adapt)
- focal: la ligne 1 du devis et le mot « site », puis le prix qui tombe dans sa case
- rules: depth-of-field-blur, coordinate-target-zoom
- world: dark
- handoff_in: aucun (ouverture du film) ; première image = noir #0d0b0a avec la feuille déjà en place et éteinte en cam(470, 640, 2.00, 32, -4) dof(684, 5.5, 15), devis D0
- handoff_out: à 5.82 : cam(800, 878, 1.46, 30, -4) flou 10 px dof(990, 5.5, 15) ; caméra en plein cran vers le bas (+950 u/s en y), dérive 0 ; devis D2 ; éclairage aller par défaut (.lt-pool, .lt-corner, .lt-warm) ; aucun objet debout, aucun portail, aucune phrase ; grain 6 %

Word cues: Une@0.00 modification@0.24 sur@0.78 ton@1.04 site@1.18 Une@1.84 journée@2.02 mille-euros@2.72 Une@3.58 nouvelle@3.74 page@3.98 six-cents-euros@4.74

Scene 4 (2.40 à 3.40 s) : P4, retour sur la ligne 1, « 1 000 € » tombe
  TEXTE ÉCRAN : [pastille : Mille euros.] (trace 2.68, lettres 2.72) après « Une journée. » ; écart synchro.
  IMAGE DE DÉPART : le vrai site plein cadre (fenêtre Safari), qui va se replier dans le mot « site » du devis.
  ÉTAPES : 2.40 le site recule vers le centre (échelle 1 → 0,06, power2.in 0,14 s, flou 12) ; 2.54 relais sous le
           flou : la feuille revient avec le portail ouvert au centre ; 2.56 l'ombre du prix paraît dans la cellule 1
           (l'image devance « mille euros ») ; 2.70 « 1 000 € » part de la caméra, énorme et flou, avec une traînée ;
           2.90 contact dans la cellule 1 : le prix est imprimé (devis D1), petit coup de caméra ; 2.90 à 3.10 le
           portail se referme dans le mot ; 3.05 à 3.25 les lettres « site » reviennent à l'encre.
  PISTE CAMÉRA : 2.54 à 2.90 recul expo.out jusqu'à cam(800, 590, 1.48, 30, -4) dof(705, 5.5, 15) ; ensuite dérive
                 x +15 u/s, échelle -1 %/s.
  COUCHES ET PROFONDEUR : avant-plan le prix en vol (grand, flou) ; sujet la ligne 1 nette ; fond « Devis » flou en
                          haut à droite et bord du papier sur le noir ; pic 3 couches.
  OBJET-PONT ET VECTEUR : le prix posé reste dans sa cellule jusqu'à « TOI. » (séquence 6) ; la caméra va descendre
                          vers la ligne 2.
  SON : pop à 2.70 (le prix arrive).
  IMAGE CLÉ : 2.88 : la ligne 1 nette, « 1 000 € » énorme presque posé dans sa case, la mini fenêtre du site qui se
              referme dans le mot « site ».
```

La séquence 2 commence par `handoff_in: à 0.00 : cam(800, 878, 1.46, 30, -4) flou 10 px …`, la copie exacte du
`handoff_out` ci-dessus : la caméra est en plein cran vers le bas au moment de la couture, et la séquence 2 finit ce
cran. Le storyboard complet (10 séquences, 27 plans) et sa grille de contrôle passée point par point
(`STORYBOARD-CHECK.md`) sont dans le même dossier.
