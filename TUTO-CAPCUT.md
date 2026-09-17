# Exporter un rush en vertical avec CapCut

Objectif : sortir un fichier exploitable pour le montage, sans rien perdre.
CapCut sert ici de simple convertisseur — aucun montage n'y est fait.

## Ce qu'on veut obtenir

| | |
|---|---|
| Format | vertical, 9:16 |
| Définition | 1080x1920, ou 720x1280 si le poids coince |
| Durée | **identique à l'originale**, du premier au dernier mot |
| Habillage | aucun : pas de sous-titre, pas d'effet, pas de logo |
| Poids | moins de 25 Mo (limite du dépôt GitHub) |

## Sur téléphone

1. **Nouveau projet**, puis importe la vidéo.
2. **Supprime le carton CapCut.** Fais défiler la timeline jusqu'au bout : un
   bloc à la marque CapCut y est ajouté d'office. Tape dessus, puis la
   corbeille. Si tu l'oublies, il part avec l'export.
3. **Format → 9:16.** C'est le réglage décisif. Un projet en 16:9 pose ta vidéo
   verticale au milieu d'un cadre horizontal, avec du noir de chaque côté.
4. **Regarde l'aperçu** : l'image doit remplir tout le cadre, sans bande noire
   à gauche ni à droite.
5. **Vérifie la durée affichée.** Elle doit correspondre à celle de l'original.
6. **Exporter** (la flèche en haut à droite) : `1080p`, `30 images/s`.
7. CapCut affiche une **taille estimée**. Au-dessus de 25 Mo, repasse en `720p`.
8. **Enregistre dans la galerie.** N'utilise pas « Partager vers » : les
   partages recompressent le fichier sans le dire.

## Sur ordinateur

1. **Créer un projet**, importer la vidéo, la glisser sur la timeline.
2. **Ratio → 9:16** dans les réglages du lecteur.
3. Vérifie l'aperçu (aucune bande noire) et la durée totale.
4. **Exporter** : format `MP4`, résolution `1080p`, fréquence `30`,
   débit `Recommandé`.
5. Exporte **en local**. Pas de « publier sur TikTok » ni d'export lié à un
   compte : ces chemins réencodent et peuvent marquer la vidéo.

## Les trois pièges, tous déjà rencontrés

**Le cadre paysage.** Au premier envoi, il ne restait que 406 pixels de large
d'image utile sur un cadre de 1280 — le reste était du noir. Deux tiers de la
définition perdus. C'est toujours un projet réglé en 16:9.

**La timeline tronquée.** Au même envoi, les cinq prises s'arrêtaient en cours
de phrase : il manquait au moins les deux tiers de chacune. Et c'est le pire
endroit où couper, puisque les chutes sont toutes à la fin.

**Le montage fait en amont.** Pas de sous-titres automatiques, pas d'effet, pas
de recadrage, pas de template — les templates sont ce qui déclenche le
filigrane CapCut. Tout ce qui est incrusté là devra être recouvert ensuite,
comme on a dû le faire sur la vidéo italienne.

## Avant d'envoyer, quatre vérifications

- [ ] La durée du fichier exporté est celle de l'original
- [ ] L'image est verticale, sans bande noire sur les côtés
- [ ] Aucun logo, sous-titre ou carton de fin
- [ ] Le fichier pèse moins de 25 Mo

## Ordre d'envoi

Commence par la prise 1 **seule**. Vérification faite, tu lances les autres.

| | Prise | Sujet | État |
|---|---|---|---|
| 1 | `20260916_163152` | se lancer en gardant son CDI | aucun arbitrage, à monter en premier |
| 2 | `20260916_163845` | les faux précurseurs | un mot à arbitrer |
| 3 | `20260916_164134` | immobilier vs automobile | deux phrases à couper |
| 4 | `20260916_163652` | les débuts à 20 m² | à retourner plutôt qu'à monter |
| 5 | `20260916_163508` | retour sur le post Lotus | story plutôt que Reel |
