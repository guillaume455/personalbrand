# La ligne du temps (le film phare de la méthode)

Le résultat final de la méthode en 5 étapes (script, voix, storyboard, animation, musique et bruitages) : 49,5 s,
16:9, 30 images/s, voix Eleven v4. C'est le film qui tourne en haut de
[entrepreneurs2-0.com](https://entrepreneurs2-0.com). Une frise du temps, règle fine sur un papier chaud, que la caméra
longe ; les vraies interfaces (le site, le devis, WhatsApp dans un iPhone, la fenêtre de Claude) sont des stations
posées sur sa ligne, chacune à son jour. Les réglages de la méthode (sous-titre en bas au centre, mot clé dans une
petite boîte à la couleur d'accent, trait fin sous le mot-pic, une seule chose à regarder à la fois, clic direct du
curseur, musique de tension à 2 ou 3 dB sous l'élan) viennent des retours sur ce film.

## Les 9 séquences

| N° | Séquence | Durée | Voix |
| --- | --- | --- | --- |
| 1 | Lundi, mercredi | 6,00 s | « Lundi, tu demandes une modif sur ton site. Mercredi, le devis tombe : mille euros. » |
| 2 | Vendredi, toujours rien | 4,34 s | « Vendredi… toujours rien. » puis le gag muet (lu, coches bleues, la seule réponse) |
| 3 | Sois honnête | 3,32 s | « Sois honnête. Ton problème, ce n'est pas la technique. » |
| 4 | Chaque modif, chaque automatisation, chaque vidéo | 6,28 s | « C'est d'attendre quelqu'un pour chaque modif sur ton site, chaque automatisation, chaque vidéo à monter. » |
| 5 | Il est temps de changer | 5,18 s | « Pendant des années, c'était le prix à payer. Il est temps de changer. » (le pivot sur noir) |
| 6 | Aujourd'hui, elle le fait | 7,08 s | « Aujourd'hui, l'IA peut faire tout ça, avec les bons outils et les bonnes méthodes. Tu lui expliques avec tes mots, elle le fait. » |
| 7 | Terminé | 5,40 s | « Terminé, les devis. Terminé, l'attente. Place à tes idées, que tu lances le jour même. » |
| 8 | Apprendre à t'en servir | 4,70 s | « Et pas besoin d'être technique. Il suffit d'apprendre à t'en servir correctement. » |
| 9 | Forme-toi pour de bon | 7,22 s | « Entrepreneurs deux point zéro. Forme-toi pour de bon. » (carte de fin, clic direct) |

## Ce qu'il y a dans le dossier

| Fichier | Ce qu'il montre |
| --- | --- |
| `frame.md` | La charte : couleurs par rôle, polices, sous-titre et ses deux mises en valeur, la frise au u près (coordonnées de chaque station), la caméra 3D et 2D, le monde de la solution, les interdits et les règles de fabrication. |
| `STORYBOARD.md` | L'en-tête du film (monde, signatures, rimes, partition caméra, silences, une seule coupe franche, rythme, son), puis les 9 séquences plan par plan, minutées mot par mot, avec leurs `handoff_in` et `handoff_out` recopiés à l'identique à chaque couture. |
| `reference/frise.html` | Le code commun exécutable : kit caméra, frise, stations, gabarits des interfaces, sous-titre, boîte, trait. Ouvre-le dans Chrome et appelle `demo("1@0.00")` (liste des états dans `frame.md`). Chaque séquence en recopie les blocs mot pour mot. |
| `compositions/frames/*.html` | Les 9 séquences animées, une par sous-agent. |
| `assemble.sh` | L'assemblage (scripts HeyGen, puis le mix audio posé à la racine, puis le lint). |
| `build-audio-v8.py` | Le mix : musique de tension coupée sur « changer. » par un impact grave, silence, musique d'élan sur « Aujourd'hui », musique qui baisse sous la voix, bruitages calés sur l'image, -16 LUFS. `M1` à `M4` : les quatre options de tension refaites après le retour « le début est un peu mou » (2 dB sous l'élan au lieu de 10). |
| `assets/icons/`, `assets/img/` | Les logos d'outils (Simple Icons, CC0) et les captures du site public d'Entrepreneurs 2.0. |

Non inclus : la voix, la musique, les polices, le rendu vidéo, `index.html` (reconstruit par `assemble.sh`) et les
fichiers `reference/v6-*.html` que cite la charte (les interfaces d'une version précédente, non publiée : leur code
final vit dans les séquences).

## Rejouer le film

Le plus simple : ouvre Claude Code à la racine du dépôt et demande « Refais le rendu de l'exemple ligne-du-temps-v8
avec ma voix et ma musique ». À la main, depuis ce dossier :

1. **Ta voix** : un montage de 49,52 s sur ce script, dans `assets/audio/voix-v8.wav`. Avec un autre minutage, recale
   d'abord les temps (`mots.py` puis `onsets.py`, voir `.claude/skills/motion-design/references/method.md` § 4) et
   mets à jour le storyboard et les séquences.
2. **Les polices** dans `assets/fonts/` (Instrument Sans 400 à 700, Space Mono 400 et 700, Big Shoulders 800, en
   `.woff2` : commandes dans `method.md` § 2).
3. **Ta musique** : les morceaux CC0 nommés dans `build-audio-v8.py` (liens dans
   `.claude/skills/motion-design/references/music.md`) dans `assets/music/`, puis `python3 build-audio-v8.py` (ou
   `python3 build-audio-v8.py M1` pour une option de tension). Les bruitages viennent du skill `media-use` du dépôt.
4. `bash assemble.sh` (ou `MIX=mix-v8-M1.wav bash assemble.sh`), puis
   `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1 npx hyperframes render --quality high --output renders/film.mp4`.
