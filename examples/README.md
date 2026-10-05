# Exemples

Des films faits avec la méthode de ce dépôt pour la landing page d'[Entrepreneurs 2.0](https://entrepreneurs2-0.com) :
trois films le 2026-09-28, les options du devis dans la nuit qui a suivi, le devis refait à partir d'un vrai
storyboard le 2026-09-29 (`C-le-devis-v7a/`, plus bas), puis le film final le 2026-09-30.

**Le film phare, à imiter en premier** : [`ligne-du-temps-v8/`](ligne-du-temps-v8/), « La ligne du temps » (49,5 s),
le résultat final de la méthode en 5 étapes, celui qui tourne en haut du site : charte, storyboard, code commun du
décor, les 9 séquences, l'assemblage et le mix (détail et marche à suivre dans son `README.md`).

| Dossier | Film | Durée | Idée |
| --- | --- | --- | --- |
| `le-devis/` | Le devis | 43 s | Le devis qui gonfle, la panne, l'attente, puis « Stop. » et l'IA qui fait tout. Vidéo finale : `le-devis/le-devis.mp4`. |
| `traduire/` | Traduire | 50 s | Pendant des décennies il fallait parler la langue de l'ordinateur (le code) et payer un traducteur ; aujourd'hui il parle français. |
| `cette-video/` | Cette vidéo | 45 s | Le film parle de lui-même : un lecteur vidéo qui se contient à l'infini, un générique où tous les noms sont « aucun », la vraie onde de la voix. |

## Les options du devis (nuit du 28 au 29 septembre 2026)

Le devis a été retenu. Trois directions ont ensuite été faites sur **la même voix et le même minutage**, et quatre
musiques sur ce même minutage : chaque musique va avec chaque image (méthode : `.claude/skills/motion-design/references/variants.md`
et `music.md`).

| Dossier | Option | Idée |
| --- | --- | --- |
| `le-devis-options/poli/` | 1, Poli | Le devis avec le personnage « toi » redessiné (mains sur la tête lisibles, sourcils inquiets, goutte de sueur) et « libre. » en pic, dans une pastille géante pendant que le devis barré s'envole. C'est la première version mise en ligne sur le site, avec la musique M1 : `le-devis-options/poli/le-devis-poli.mp4` (encodage web, 5,6 Mo). |
| `le-devis-options/nuit/` | 2, Nuit | Le même film tout en sombre : la solution sur une « nuit chaude » éclairée en terracotta, cartes en verre chaud, pas de fond papier, flash chaud. Fait pour se fondre dans le haut sombre d'une page. |
| `le-devis-options/bureau/` | 3, Le bureau | Une direction neuve : le film vu du dessus d'un bureau, avec de vrais objets (devis papier, stylo terracotta, post-it déchiré, tampon SUR DEVIS, éphéméride, pile de factures, portable, carnet où le zéro est dessiné). |

Les quatre musiques (M1 tic-tac puis élan, M2 rétro synthé, M3 montée électro, M4 cinéma) sont construites par
`le-devis-options/poli/build-music-options.py` : musique coupée net sur « Stop. » avec un impact grave, drop calé sur le
flash, musique qui baisse sous la voix, fin en fondu, -16 LUFS. Les dix morceaux sont en CC0 (domaine public) ; leurs
liens de téléchargement sont dans `.claude/skills/motion-design/references/music.md`.

Pour refaire une option :

1. Fabrique le montage de la voix avec `le-devis/build-audio.sh` (voir plus bas), puis les mixages :
   `MUSIC_DIR=/chemin/vers/les/morceaux python3 le-devis-options/poli/build-music-options.py` (écrit
   `assets/audio/mix-C-M1.wav` à `mix-C-M4.wav` dans `poli/` ; `SFX_DIR` prend par défaut les bruitages du skill
   `media-use`).
2. Copie le mixage voulu dans le dossier de l'option (`nuit/assets/audio/`, `bureau/assets/audio/`) et les polices dans
   `assets/fonts/`.
3. Depuis le dossier de l'option : `MIX=mix-C-M1.wav ./assemble.sh`, puis le rendu comme ci-dessous.
4. Pour les autres musiques, pas besoin de refaire le rendu :
   `ffmpeg -i film.mp4 -i assets/audio/mix-C-M2.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k film-M2.mp4`.

Seule la vidéo de l'option Poli est incluse. La direction Bureau pèse lourd au rendu (69 Mo pour 43 s, à cause du bois
et du grain) : à ré-encoder pour le web avant de la mettre sur un site (`.claude/skills/motion-design/references/landing-integration.md`).

## Le devis refait à partir d'un vrai storyboard (`C-le-devis-v7a/`, 29 septembre 2026)

« Le devis est le décor », 43,2 s, le film du début de la vidéo YouTube sur la méthode. Même voix, même musique et mêmes
bruitages que les versions précédentes : seule la mise en scène change, et elle est entièrement écrite avant d'animer
(étape 4 de la méthode). Le film « Le devis » tourne sur [entrepreneurs2-0.com](https://entrepreneurs2-0.com), juste
sous le haut de page, en lecture muette automatique.

Ce que montre cet exemple, dans l'ordre où il a été fait :

| Fichier | Ce qu'il montre |
| --- | --- |
| `DIRECTIONS.md` | Les trois directions proposées sur la même voix : A « Le devis est le décor » (retenue), B « Deux conversations », C « La ligne du temps », chacune avec son concept, son fil d'objets-ponts et ses trois images de style à dessiner. Modèle : `../../templates/DIRECTIONS-TEMPLATE.md`. |
| `render-styleframes.py` | Le rendu des images de style (une page HTML 1920 × 1080 par image, dans `styleframes/`) en PNG, avec Chromium sans fenêtre. Même script que `.claude/skills/motion-design/scripts/render-styleframes.py` : `python3 render-styleframes.py <projet> [A1 B2 …]`. |
| `frame.md` | La charte de la direction A : un seul lieu, un vrai devis d'agence de 1500 × 2120 u décrit au pixel (lignes, cellules prix, case TOTAL, états du devis d'une séquence à l'autre), la caméra 3D et son flou de profondeur à trois couches, l'éclairage aller (nuit) et retour (plein jour), les vraies interfaces (iPhone 18, WhatsApp iOS 2026, fenêtre Claude, vrai site). |
| `reference/devis-decor.html` | Le code exécutable du décor et du kit caméra : ouvre le fichier dans Chrome et appelle `demo({...})` dans la console pour voir n'importe quel état. Chaque séquence recopie ce bloc mot pour mot : le devis est le même des deux côtés de chaque couture. |
| `STORYBOARD.md` | Le storyboard complet : l'en-tête du film (monde, deux mécanismes signature, rimes, partition caméra, silences, une seule coupe franche sur « Stop. », rythme, bruitages), puis 10 séquences et 27 plans, chacun en étapes toutes les 0,5 s environ avec sa piste caméra, sa profondeur, son objet-pont, son bruitage et son image clé. Chaque `handoff_out` est recopié mot pour mot dans le `handoff_in` de la séquence suivante. Modèle : `../../templates/STORYBOARD-TEMPLATE.md`. |
| `STORYBOARD-CHECK.md` | La grille de contrôle en 15 points de `patterns/STORYBOARD-CRAFT.md` passée sur ce storyboard, point par point : tenu, tenu après correction (avec la correction), ou non tenu (avec sa raison). |

Ne sont pas inclus : la vidéo, la voix, la musique, les bruitages, les polices, les images (images de style en PNG,
capture du site), les séquences HTML animées, ni les fichiers `reference/v6-*.html` cités par la charte (les vraies
interfaces reprises de la version précédente, non publiée ; les séquences les plus proches publiées ici sont dans
`le-devis-options/poli/compositions/frames/`). Cet exemple sert à lire et à copier la méthode du storyboard, pas à
refaire le rendu.

## Contenu des dossiers de film

Chaque dossier de film (les trois films et les trois options) contient :

- `frame.md` : la charte (couleurs par rôle, typographie, composants, interdits).
- `STORYBOARD.md` : le film découpé en séquences, minuté mot par mot sur la voix.
- `compositions/frames/*.html` : une séquence animée par fichier, écrite par un sous-agent.
- `assemble.sh` : l'assemblage (scripts HeyGen, transitions, puis la couche orchestrateur : fond papier, flash de lumière, iris, son).
- `build-audio.sh` (+ `assets/audio/sfx-events.json`) : le montage de la voix et le mixage (musique, bruitages).
- `index.html` : le résultat de l'assemblage, tel qu'il a servi au rendu.

## Refaire un rendu

Les voix (ElevenLabs), la musique, les bruitages et les polices ne sont pas inclus. Pour refaire un rendu d'un exemple :

1. Dépose ta voix dans `assets/audio/` sous le nom attendu par `build-audio.sh` (`voix-C-devis.mp3`, `voix-B-traduire.mp3` ou `voix-A-cette-video.mp3`). Avec une autre voix, recale d'abord les temps avec `.claude/skills/motion-design/scripts/onsets.py` et mets à jour le storyboard et les séquences.
2. Mets les polices dans `assets/fonts/` (Instrument Sans 400/500/600/700, Space Mono 400/700, Big Shoulders 800 en `.woff2`, voir `.claude/skills/motion-design/references/method.md`).
3. Indique où sont tes bruitages et ta musique : `export SFX_DIR=/chemin/vers/bruitages MUSIC=/chemin/vers/musique.mp3` (les noms de fichiers attendus sont dans `assets/audio/sfx-events.json` : `pop.wav`, `click.wav`, `click-soft.wav`, `whoosh.wav`, `whoosh-short.wav`, `typing.wav`, `key-press.wav`, `ping.wav`, `error.wav`).
4. Depuis le dossier de l'exemple : `./build-audio.sh && ./assemble.sh`, puis `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1 npx hyperframes render -q high -o renders/film.mp4`.

Le plus simple reste de demander à Claude Code, ouvert à la racine du dépôt : « Refais le rendu de l'exemple traduire avec ma voix ».
