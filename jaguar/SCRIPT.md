# SCRIPT — « 139 891 km sur une voiture plaisir » (reel Jaguar F-Type, 9:16)

Format : 1080×1920, 30 fps, H.264 + AAC, environ 84 s (78 à 92 s), audio 48 kHz stéréo à -14 LUFS, sous-titres
incrustés. Motion design sur fond #0A0A0A orienté chiffres, ponctué de photos de la F-Type (désaturées à 90 %, zoom
lent). Accent orange #FB8000, texte blanc, rouge #E03131 pour les seules déductions. Oswald en capitales.

Le texte de la voix est dans `build.py` (SCENES) : c'est la source des sous-titres.

## Photos (contrôle avant utilisation, `prep-photos.py`)

- Retenues (série K08673, aucune ne porte de filigrane, de logo ni de nom de société ; plaques déjà vierges) :
  1 (3/4 avant, autocollant de stock flouté), 4 (3/4 arrière capote ouverte, feux), 3 (arrière, feux), 7 (roue),
  11 (intérieur cuir), 13 (habitacle, écran flouté), 31 (levier), 32 (compteur à 139 891 km).
- Écartées : 15 (plaque constructeur avec le VIN complet), 25 et 26 (l'écran de navigation affiche la ville du
  marchand), 14, 24, 33 (coffre, rétroviseur, papiers et clés).
- `65075185_2301214799954539_7642515615965511680_n.jpg` n'est pas une photo de la voiture : c'est un document
  d'assurance (carte verte, avec noms et adresses). Écarté. Le plan final reprend la photo de Guillaume.
- Le PDF n'est ni téléchargé ni affiché.

## Texte de la voix (à coller dans ElevenLabs)

Chiffres écrits en lettres. Une seule prise, sans musique. Poser le fichier dans `jaguar/assets/audio/voix.mp3`.

```
Cent trente-neuf mille huit cent quatre-vingt-onze kilomètres. Sur une voiture plaisir.

Une Jaguar F-Type cabriolet S, V6 trois litres compressé, trois cent quatre-vingts chevaux, de mai deux mille quatorze. Sur ce genre de voiture, la valeur tient au kilométrage, parce que ce sont des voitures de week-end. Cent quarante mille, c'est le double de ce qu'un acheteur accepte. Donc tout le monde passe son tour.

Sauf que cette voiture était belge. Et en Belgique, il existe un document que la plupart des Français ne connaissent pas : le Car-Pass. À chaque passage chez un professionnel, le kilométrage est relevé et enregistré. Le vendeur a l'obligation légale de le remettre à l'acheteur, et il se vérifie en ligne.

Ce n'est pas infaillible. Les interventions faites hors de Belgique n'y figurent pas. Mais c'est ce qui se fait de mieux en Europe contre le compteur trafiqué.

Juillet deux mille dix-neuf. Trente mille euros chez un marchand partenaire. Six cents euros de transport pour me la faire livrer. Six cents euros de révision. Trente et un mille deux cents engagés.

Quatre-vingt-dix jours plus tard, elle part à trente-six mille deux cents. Six mille deux cents euros de marge. C'est ce que tout le monde calcule. Et c'est faux.

Moins le transport. Moins la révision. Et la TVA : j'ai collecté six mille trente-trois euros sur la vente, j'en avais déjà récupéré cinq mille deux cents sur l'achat et les frais. Il m'en reste huit cent trente-trois à reverser. Au final : quatre mille cent soixante-sept euros. Pas six mille deux cents.

Quatre mille cent soixante-sept euros sur trente et un mille deux cents engagés, en quatre-vingt-dix jours. Et surtout : aucun retour, aucun service après-vente à gérer.

Le kilométrage n'était pas le risque. Le risque, c'aurait été de ne pas pouvoir le prouver. Un compteur élevé avec un historique complet se vend. Un compteur bas sans historique, non.

Moi c'est Guillaume Herbin, je suis dans l'automobile depuis deux mille dix. Suis-moi si tu veux voir plus de contenus comme celui-ci.
```

## Écarts au brief

- Fin : la présentation de Guillaume (« Moi c'est Guillaume Herbin… », sa photo, @guillaumeherbin_, SUIS-MOI), comme
  il l'a demandé sur le reel Porsche, à la place de « TU L'AURAIS ACHETÉE À 140 000 KM, TOI ? ».
- Coupes pour la durée (demande de Guillaume, marquées ✂ dans `build.py`, retirées de l'enregistrement par
  `place-voice.py`) : le carton « JE N'AI PAS ACHETÉ UN COMPTEUR. / J'AI ACHETÉ UN HISTORIQUE. » ; « parce que ce sont
  des voitures de week-end » ; « Les interventions faites hors de Belgique n'y figurent pas » (la nuance « Ce n'est pas
  infaillible » reste, avec « le meilleur garde-fou d'Europe ») ; le détail dit de la TVA (« j'ai collecté… les
  frais »), qui reste à l'écran (« 6 033 COLLECTÉS − 5 200 RÉCUPÉRÉS »). Voix accélérée ×1,15.
- Sous 13,4 % : « résultat de cette opération, pas une promesse » (interdit n° 6).
- Calculs vérifiés : 36 200 − 30 000 = 6 200 ; 6 200 − 600 − 600 − 833 = 4 167 ; TVA 36 200 / 1,2 × 0,2 = 6 033,
  31 200 / 1,2 × 0,2 = 5 200, net 833 ; 4 167 / 31 200 = 13,4 %.
