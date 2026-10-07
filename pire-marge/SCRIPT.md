# SCRIPT — « Ma pire marge » (série « Je me suis fait avoir », épisode 3, reel 9:16)

Format : 1080×1920, 30 fps, environ 65 s. Fond #0A0A0A, accent #FB8000, texte blanc ; rouge sombre #B3261E réservé à la
jauge de température et aux culasses. Titres Anton en capitales avec le trait orange. Sous-titres de la voix, mot-clé
en orange. Jamais plus de 6 mots par bloc. Compteur TOTAL cumulatif en haut à droite à partir de la scène 2
(49 000 → 51 000 → 51 800 → 66 800 €). Aucun billet ni espèce. Fin : « @guillaumeherbin_ ».

Photos réelles (branche `claude/vertical-clips-personal-brand-6rv5uf`, `rushes/ferrari/`), désaturées, cadre orange :
- scène 2 : `photo lors de l'achat/IMG_3325.PNG` (capture reçue sur le téléphone, plaque floutée) et
  `carnet entretien (1)` à `(6)` en vignettes floues ;
- scène 5 : `IMG_20210205_174513.jpg` (moteur déposé) ;
- scène 6 : `742829927-IMG-20230417-WA0023.jpg` (départ export, plaque déjà masquée) ;
- scène 8 : `IMG_20221216_155808.jpg` (plaque floutée).

Écarts avec le brief : à l'écran « - 16 800 € » (66 800 - 50 000), la voix garde « moins 17 000 euros » (arrondi) ;
erreur n° 2 raccourcie en « PAS À N'IMPORTE QUEL MÉCANO. » (6 mots) ; « ÉPISODE 3 : JE ME SUIS FAIT AVOIR » affiché
en pastille « ÉPISODE 3 » + titre « JE ME SUIS FAIT AVOIR. ».

Le texte de la voix est dans `build.py` (SCENES) : c'est la seule source.

## Texte de la voix (ElevenLabs)

```
Ma pire marge en seize ans de métier, c'est sur une Ferrari.
Septembre deux mille dix-neuf. J'ai trente ans. Ma première Ferrari, une trois cent soixante Modena, quarante-neuf mille euros. Je l'achète sur photos. Les factures d'entretien ? Sur photos aussi. Je me la fais livrer sans l'avoir vue. Le vendeur, je bosse avec lui depuis des années. Alors je ne vérifie rien.
Je la revends à un particulier en quelques semaines. Puis il m'appelle : le moteur chauffe. Je ne discute pas, je le rembourse intégralement, carte grise comprise, et je rapatrie la voiture dans mon garage.
Diagnostic : joint de culasse. Sur une Ferrari, ça veut dire déposer le moteur. Et tant qu'on y est, la distribution.
Je confie le chantier à un mécano. Il commence. Puis il abandonne, moteur ouvert. Je dois tout reprendre à zéro : trouver quelqu'un capable d'intervenir sur place, dans mon garage, parce que la voiture ne bouge plus. Elle reste plus d'un an immobilisée.
Le mécano qui reprend le chantier me fait commander l'embrayage en plus, pour anticiper. Cette fois, j'écoute. Avril deux mille vingt-trois, je la revends cinquante mille euros à l'export. Trois ans et demi plus tard. Moins dix-sept mille euros, sans compter l'argent bloqué pendant tout ce temps.
Mes trois erreurs. Un : j'ai acheté avec le cœur. Pas d'essai, pas de contrôle, aucune des vérifications que je fais sur n'importe quelle occasion. La confiance, même après des années, ne remplace pas un contrôle. Deux : j'ai confié ce moteur à quelqu'un qui pensait en être capable. Ce type de mécanique ne se confie pas à tout le monde. Trois : j'ai cru pouvoir gérer ça seul, sans demander à ceux qui savaient vraiment.
J'ai perdu dix-sept mille euros. J'ai gardé les leçons. Abonne-toi, il y a d'autres épisodes.
```

## Recaler sur la prise

```
python3 build-voice.py && python3 align.py && python3 build.py && bash build-mix.sh && bash assemble.sh
```
