# SCRIPT — « 3 voitures, 3 cycles de vente » (reel 9:16)

Format : 1080×1920, 30 fps, environ 70 s. Fond #0A0A0A, accent #FB8000, texte blanc. Titres Anton en capitales avec le
trait orange. Sous-titres de la voix, mot-clé en orange. Jamais plus de 6 mots par bloc. Montants en compteur. Frise de
12 mois en bas d'écran : chaque voiture y avance d'un cycle de vente à la fois, un compteur annuel à droite. Aucun
billet ni espèce. Fin : « @guillaumeherbin_ ». Musique : même morceau que « Ma pire marge » (coma-media slim).

Photos de Guillaume (plaques floutées, enseigne floutée derrière la Mustang) : Mustang (sportive), BMW X4 (SUV),
Golf 7, Fiat 500L, Mini (citadines). Document « GARANTIE » inventé (aucun nom). Réparations : 6 000 € / 1 200 €
(chiffres d'exemple du brief).

Écarts au brief : « JUSQU'À 7 FOIS PLUS » (54 000 / 15 000 = 3,6, 108 000 / 15 000 = 7,2) ; scène 6, « une
réparation à 30 000 euros de standing » remplacé par « ça se paie au prix d'une sportive » ; « cycles sur 12 mois »
précisé (demande de Guillaume) ; accroche « Une seule sort vraiment du lot, je t'explique. »

Le texte de la voix est dans `build.py` (SCENES) : c'est la seule source.

## Texte de la voix (ElevenLabs)

```
Tu as trente mille euros pour démarrer et douze mois devant toi. Trois façons de les placer. Une seule sort vraiment du lot, je t'explique.
Option un : une sportive. Achetée trente mille, revendue trente-cinq mille. Cinq mille euros de marge, c'est beau. Mais son délai de rotation de stock, c'est quatre mois. Trois cycles de vente sur douze mois. Quinze mille euros.
Option deux : un SUV à vingt mille et une citadine à dix mille. Le SUV fait trois mille de marge et tourne en trente jours : douze cycles de vente, trente-six mille euros. La citadine fait mille cinq cents et tourne en quinze jours : vingt-quatre cycles, trente-six mille aussi. Total : soixante-douze mille euros.
Option trois : trois citadines. Mille cinq cents euros de marge chacune, quinze jours de rotation. Sur le papier, cent huit mille euros dans l'année. Soyons honnêtes : enchaîner soixante-douze cycles de vente, c'est un vrai métier. Divise par deux. Tu es encore à cinquante-quatre mille.
Même budget de départ. La voiture à la plus grosse marge est celle qui te rapporte le moins. Ce qui compte, c'est pas la marge d'une vente. C'est la rotation de ta trésorerie : combien de fois ton argent revient dans l'année.
Et je n'ai pas encore parlé du risque. En tant que pro, tu es tenu par la garantie légale de conformité et par les vices cachés. Une panne sur une sportive, ça se paie au prix d'une sportive. La même panne sur une citadine, c'est cinq fois moins. La voiture la plus chère, c'est aussi celle qui te coûte le plus cher quand ça casse.
Ce que tu gagnes, c'est ta marge fois ton nombre de cycles de vente. Au début, prends les voitures qui tournent vite et qui cassent pas cher. Abonne-toi pour plus de contenu comme celui-ci.
```

## Recaler sur la prise

```
python3 build-voice.py && python3 align.py && python3 build.py && bash build-mix.sh && bash assemble.sh
```
