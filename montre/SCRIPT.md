# SCRIPT — « Ne vends pas. Montre. » (reel 9:16)

Format : 1080×1920, 30 fps, environ 55 s (53,8 s une fois la voix montée). Fond #0A0A0A, accent #FB8000, texte blanc,
rouge sombre #B3261E réservé à la facture de la boîte de vitesses (scène 6, demandé dans le brief). Titres Anton en
capitales avec le trait orange. Sous-titres de la voix, mot-clé en orange. Jamais plus de 6 mots par bloc. Montants en
compteur. Aucun billet ni espèce. Fin : « @guillaumeherbin_ ».

**Statut** : brief et découpage écrits par Guillaume (2026-10-06), voix enregistrée le même jour
(`assets/audio/voix.mp3`). Le texte de la voix est dans `build.py` (SCENES) : c'est la seule source.

Scène 4 : facture stylisée (nom du garage, client, immatriculation et numéro flous) en attendant une vraie facture ou
un accord de prise en charge en PNG.

## Texte de la voix (ElevenLabs)

```
Arrête de vendre l'extension de garantie.
Tu expliques la couverture, les options, le prix. Le client n'entend qu'une chose : un vendeur qui veut lui vendre un truc en plus.
Alors arrête d'argumenter. Montre-lui trois choses.
Un : une vraie facture. Un client, un turbo, deux mille cinq cents euros de réparation. Reste à charge : zéro. Il ne t'écoute plus décrire une couverture, il regarde ce qu'elle a déjà payé.
Deux : les autres. Huit clients sur dix la prennent. Il n'est plus le pigeon à qui on refile une option. Il est celui qui hésite alors que les autres ont tranché.
Trois : celui qui a dit non. Huit mois plus tard, la boîte de vitesses. Six mille sept cents euros de sa poche. Tu ne le racontes pas pour faire peur. Tu le racontes parce que c'est arrivé.
À ce stade, la question n'est plus de savoir s'il la prend. C'est de savoir comment il la paie : au comptant ou tous les mois. Tu lui laisses choisir, c'est tout.
Une facture, un chiffre, une histoire. Une preuve vaut dix arguments.
Ne vends pas. Montre. Abonne-toi pour plus de contenu comme celui-ci.
```

## Recaler sur une nouvelle prise

```
python3 build-voice.py && python3 align.py && python3 build.py && bash build-mix.sh && bash assemble.sh
```
(align.py : ANCHORS force « Reste à charge : | zéro. | Il ne t'écoute plus » sur les pauses de la prise du 2026-10-06 ;
à vider ou ajuster pour une autre prise.)
