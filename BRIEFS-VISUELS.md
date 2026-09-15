# Charte visuelle et covers

Charte arrêtée le 15/09, alignée sur les carrousels existants : covers produites
avec ChatGPT, texte compris dans l'image.

## Couleurs

| Rôle | Valeur | Usage |
|---|---|---|
| Accent | `#FC7E15` | chiffres clés, mots à faire ressortir, soulignés, puces |
| Texte | `#FFFFFF` | titres et corps |
| Fond | noir profond | dégradé sombre, ou photo assombrie |
| Encadré | crème clair | fond des blocs de données, texte noir dessus |

L'accent est relevé directement sur la cover du clip 1 (valeur dominante mesurée :
`rgb(252,126,21)`). C'est la même valeur dans `scripts/lib.sh`, variable `ACCENT`.

## Typographie

Sans-serif condensée grasse en capitales pour les titres, sans-serif régulière
pour le corps, manuscrite pour la citation de bas de cover. Pas de serif :
la direction Georgia envisagée au départ est abandonnée.

## Format

**1080×1920 px**, ratio 9:16 strict. Les premières covers ont été livrées en
941×1672 : ça fonctionne, mais impose un agrandissement de 15 % qui adoucit les
textes fins. Demander explicitement 1080×1920 à la génération.

## Structure de la cover d'ouverture

Celle du clip 1 sert de gabarit :

1. **sur-titre** court, blanc, capitales, deux lignes maximum ;
2. **titre principal**, très gros, capitales, avec le chiffre clé en accent,
   souligné d'un trait tracé à la main ;
3. **encadré crème** avec une donnée dérivée et son pictogramme ;
4. **trois puces** cochées, une idée chacune ;
5. **citation manuscrite** en bas, à la première personne.

Seul le titre principal est lu pendant les 3 secondes d'affichage. Le reste est
du renfort visuel — ne pas y placer d'information indispensable.

## Gabarit de prompt

À reprendre pour chaque clip en remplaçant les crochets :

```
Crée une cover verticale 1080x1920 pour un Reel, dans ce style :
fond photo sombre avec éclairage bleuté, texte blanc en capitales
sans-serif condensée grasse, accents en orange #FC7E15.

Structure de haut en bas :
- sur-titre blanc sur deux lignes : "[SUR-TITRE]"
- titre principal très gros, avec "[MOTS EN ACCENT]" en orange,
  souligné d'un trait orange tracé à la main
- encadré crème avec un pictogramme et la donnée : "[DONNÉE CLÉ]"
- trois puces cochées en orange : "[PUCE 1]", "[PUCE 2]", "[PUCE 3]"
- en bas, citation manuscrite blanche : "[CITATION]"

Français correct, accents inclus. Pas de logo, pas de nom de marque.
```

Vérifier systématiquement les accents et la ponctuation à la sortie : les
générateurs les escamotent régulièrement sur le français.

## Textes proposés pour les covers restantes

Dérivés des hooks et du contenu réel de chaque rush. À ajuster librement.

### Clip 2 — de salarié à gérant
- Sur-titre : IL Y A QUELQUES MOIS
- Titre : **IL ÉTAIT SALARIÉ.** (« SALARIÉ » en accent)
- Donnée : aujourd'hui gérant indépendant
- Puces : Sorti son premier salaire · Aucune hiérarchie · Vit de sa passion
- Citation : « Comment je fais pour optimiser ma fiscalité ? »

### Clip 3 — types de locaux
- Sur-titre : ON A DÉMARRÉ DANS
- Titre : **40 M² EN CENTRE-VILLE.** (« 40 M² » en accent)
- Donnée : aujourd'hui, l'inverse exactement
- Puces : Périphérie · Entrepôt et stockage · Showroom
- Citation : « Le modèle s'est adapté au fur et à mesure. »

### Clip 4 — retours sur investissement
- Sur-titre : UN MARCHAND CLASSIQUE
- Titre : **REMBOURSE EN 7 ANS.** (« 7 ANS » en accent)
- Donnée : en intermédiation, quelques mois
- Puces : Pas de stock immobilisé · Charges réduites · Retour rapide
- Citation : « Les retours sont beaucoup plus rapides. »

### Clip 5 — un métier pas pour tout le monde
- Sur-titre : DANS L'AUTOMOBILE
- Titre : **L'ENVIE NE SUFFIT PAS.** (« NE SUFFIT PAS » en accent)
- Donnée : ce qui fait vraiment la différence
- Puces : Le tempérament · Les expériences passées · La capacité à s'adapter
- Citation : « Il y a ces premières fois où il faut se faire violence. »

### Clip 6 — tous les âges
- Sur-titre : CEUX QUI SE LANCENT ONT
- Titre : **DE 19 À PLUS DE 60 ANS.** (« 19 » et « 60 » en accent)
- Donnée : aucun profil type
- Puces : Aucun diplôme requis · Tous les parcours · Tous les âges
- Citation : « Il n'y a pas de profil type. »

**Contrainte à respecter sur toutes les covers** : aucune occurrence de
« franchise », « franchisé » ou « réseau », aucun logo ni nom d'enseigne, aucune
mention de FORGE. Voir `PLAN-EDITORIAL.md`.

## Cover de fin

Une seule suffit pour les six clips : « Tu veux plus de contenu auto ?
Abonne-toi. » Elle est dans `assets/outro-bg.png` et s'applique telle quelle,
3 secondes, sans texte surimprimé.

## Intégration

```bash
bash scripts/make-clip.sh \
  --src "rushes/…" --start … --end … \
  --hook-bg assets/cover-0X.png \
  --outro assets/outro-bg.png --outro-dur 3 \
  --out exports/0X-….mp4
```

Une cover qui porte son texte s'utilise sans `--hook`, ce qui empêche toute
surimpression. `--hook` n'est utile que pour un carton de secours en texte seul.
