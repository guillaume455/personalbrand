# « Mes conseils » — ordre de publication

Toutes les stories : 1080×1920, 30 fps, H.264 High, AAC 48 kHz 192 kb/s, -14 LUFS (±0,3), crête ≤ -0,7 dBFS,
`+faststart`. Ta voix et tes sous-titres d'origine ; aucun logo, aucun appel commercial (les « Abonne-toi » et
« Suis-moi » de fin sont coupés). Coupes uniquement en fin de phrase ; fondu de 0,2 s entre deux passages éloignés.

Publier dans cet ordre (du plus accessible au plus expert), puis les ajouter au Highlight « Mes conseils » :

| Ordre | Fichier | Durée | Reel source | Passages (s du Reel) | Message |
|---|---|---|---|---|---|
| 1 | `02_EXPORTS/01_conseil_erreurs_achat.mp4` | 26,1 s | pire-marge | 0,00–2,99 + 60,38–83,66 | La confiance ne remplace pas un contrôle |
| 2 | `02_EXPORTS/02_conseil_annonce_dossier.mp4` | 26,7 s | porsche997 | 0,00–26,70 | Juge le dossier, pas les photos |
| 3 | `02_EXPORTS/03_conseil_kilometrage.mp4` | 19,6 s | jaguar | 0,00–3,61 + 9,41–15,66 + 63,09–73,19 | Le risque, c'est de ne pas pouvoir prouver le kilométrage |
| 4 | `02_EXPORTS/04_conseil_garantie_4_lignes.mp4` | 26,1 s | garantie-v5 | 26,74–52,83 | Plafond, vétusté, remboursement, exclusions |
| 5 | `02_EXPORTS/05_conseil_marge_achat.mp4` | 13,4 s | mini | 0,00–2,25 + 70,41–81,69 | La marge se fait à l'achat ; la valeur vient du modèle |
| 6 | `02_EXPORTS/06_conseil_vraie_marge.mp4` | 29,6 s | jaguar | 43,61–47,00 (accroche) + 33,12–43,61 + 47,00–63,09 | 6 200 € affichés, 4 167 € réels |
| 7 | `03_VISUELS_FIXES/06b-vraie-marge.png` | fixe | chiffres du Reel Jaguar | — | Le calcul complet, à lire |
| 8 | `02_EXPORTS/07_conseil_reprise.mp4` | 30,6 s | reprise | 0,00–22,30 + 32,43–40,92 | Même client, deux marges, sans surpayer la reprise |
| 9 | `02_EXPORTS/08_conseil_voitures_pas_cheres.mp4` | 20,0 s | cycles | 58,34–78,29 | Au début : voitures qui tournent vite et cassent pas cher |
| 10 | `02_EXPORTS/09_conseil_rotation_147_jours.mp4` | 11,1 s | chiffres | 43,56–54,66 | 147 jours en moyenne : tourner en 30, c'est l'écart |
| 11 | `02_EXPORTS/10_conseil_marchand_intermediaire.mp4` | 24,0 s | marchand | 0,00–8,89 + 46,75–62,09 | Stock ou mandat : 2 300 € bloquant 12 000 €, ou 1 500 € sans stock |
| 12 | `02_EXPORTS/11_conseil_trouver_clients.mp4` | 35,8 s | telephone-fini | 0,00–8,25 + 15,63–43,36 | Montre ton travail, ta réputation, sois installé |
| 13 | `05-metier-pas-adapte.mp4` (Drive, face caméra) | ~33 s | interview | intégral | En attente du fichier dans `01_SOURCES/` |

Retouches d'image (le reste est l'image du Reel) :
- 01 : compteur « TOTAL 66 800 € » effacé dès 2,6 s (cumul propre au Reel complet).
- 09 : mention « 5 / 5 » effacée (numéro dans la série du Reel).
- 06 : l'accroche « 6 200 € de marge. C'est ce que tout le monde calcule. Et c'est faux. » est placée en tête, puis le
  récit reprend dans l'ordre ; rien n'est dit deux fois.
- 11 : la phrase sur la loi (« tu n'as plus le droit d'appeler un particulier… sans son accord ») est gardée, sans elle
  « Le vrai problème, c'est pas la loi » ne se comprend pas.

Refaire une story : `python3 INSTAGRAM/HIGHLIGHTS/MES_CONSEILS/04_RECAP/tools/story.py <reel> <sortie.mp4> <a-b> ...`
depuis la racine du dépôt (voir les passages ci-dessus ; `MASK=x:y:w:h:depuis` pour 01 et 09).
