# SCRIPT — « L'annonce que personne ne voulait » (reel Porsche 997, 9:16)

Format : 1080×1920, 30 fps, H.264 + AAC, environ 80 s (75 à 90 s), audio 48 kHz stéréo à -14 LUFS, sous-titres
incrustés. Motion design sur fond #0A0A0A ponctué des cinq photos de juin 2014 (désaturées à 90 %, zoom lent 3 à 5 %).
Accent orange #FB8000, texte blanc, rouge #E03131 pour les seules pastilles de warning. Oswald en capitales, une
seule famille. Plaques, enseigne et numéro du garage, drapeau du garage floutés (`prep-photos.py`), EXIF et GPS retirés.

Le texte de la voix est dans `build.py` (SCENES) : c'est la source des sous-titres.

## Texte de la voix (à enregistrer ou à coller dans ElevenLabs)

Chiffres écrits en lettres pour la lecture. Une seule prise, sans musique. Poser le fichier dans
`porsche997/assets/audio/voix.mp3`.

```
L'annonce que personne ne voulait.

Leboncoin, deux mille quatorze. Des photos ratées. Un vendeur pressé, qui connaît mal sa voiture, qu'on n'arrive pas à avoir au téléphone, et qui ne vend rien du tout. Cinq raisons de passer son chemin.

Sauf que ces cinq warnings portaient tous sur le vendeur. Sur la voiture, il n'y en avait aucun. Encore fallait-il aller vérifier.

Carnet d'entretien à jour, dernier passage à cinquante-quatre mille kilomètres. Contrôle technique vierge. Rappel constructeur effectué. Historique complet. Une annonce se juge sur ce qu'il y a dans le dossier, pas sur la qualité des photos.

Une neuf cent onze type neuf cent quatre-vingt-dix-sept phase deux de deux mille neuf. Flat six trois litres six, trois cent quarante-cinq chevaux, boîte PDK. Et surtout une phase deux : injection directe, et plus d'arbre intermédiaire. Le fameux problème des phases un n'existe plus sur celle-là. C'est ce détail qui fait sa cote aujourd'hui.

Deux mille quatorze. J'ai vingt-cinq ans. C'est ma première Porsche. Quarante-quatre mille euros.

Je la garde deux ans. Mille euros d'entretien courant, quatre cent cinquante euros de pneus. Je la revends cinquante-deux mille. Six mille cinq cent cinquante euros d'écart, après avoir roulé avec pendant deux ans.

Et aujourd'hui, plus de dix ans après, les mêmes s'affichent à partir de cinquante-sept mille euros. Il y a des voitures qui décotent, et d'autres qui font l'inverse.

La vraie leçon n'est pas là. Une mauvaise annonce n'est pas une mauvaise voiture. La plupart des gens éliminent sur la présentation. Moi je vérifie le dossier. C'est exactement là que se trouvent les bonnes affaires : dans les annonces que les autres ne prennent pas la peine d'ouvrir.
```

Le CTA (« TU SERAIS ALLÉ VOIR CETTE ANNONCE, TOI ? », @guillaumeherbin_) est sans voix. Le hook dure 4 s quelle que
soit la voix (`place-voice.py`). Les scènes prix, deux ans et 2026 s'ajustent à la voix ; le texte ne bouge pas.

## Écarts au brief

- Le brief demande 80 s, mais sa timeline va jusqu'à 1:40. La durée finale suit la voix : à débit normal, le texte
  donne environ 85 à 90 s avec le hook de 4 s et le CTA de 4 s.
- Quelques textes de l'écran dépassent 5 mots parce que le brief les écrit ainsi (« 911 TYPE 997 PHASE 2 — 2009 »,
  la leçon, le CTA) : ils sont coupés en lignes courtes.
