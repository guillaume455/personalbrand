# Highlight « Mes conseils » — Étape 1 : audit et sélection

Statut : **proposition, en attente de validation**. Rien n'est monté.

Les timecodes sont pris dans les exports finaux de chaque Reel (`<reel>/renders/`, 1080×1920, 30 fps, voix GH v1 à
-14 LUFS). Ils viennent de l'alignement mot à mot de la voix (`assets/audio/voix-montage-mots.json`). Chaque coupe
tombe dans une pause entre deux phrases, jamais au milieu d'un mot.

## 1. Audit des contenus

| Reel | Durée | Sujet | Appel final | Pour « Mes conseils » |
|---|---|---|---|---|
| `pire-marge` | 87,6 s | Ferrari 360 : −17 000 €, mes 3 erreurs | Abonne-toi | ✅ erreurs vécues, très fort |
| `porsche997` | 78,6 s | L'annonce ratée qui cachait un bon dossier | Moi c'est GH / Suis-moi | ✅ vérifier le dossier, pas les photos |
| `jaguar` | 80,7 s | 140 000 km, Car-Pass, vraie marge après frais et TVA | Moi c'est GH / Suis-moi | ✅✅ deux conseils distincts |
| `garantie-v5` | 52,8 s | Extension de garantie : les 4 lignes du contrat | aucun | ✅ vérifications avant achat |
| `mini` | 87,3 s | Mini à 2 000 € : la marge se fait à l'achat | question | ✅ choisir un modèle recherché |
| `reprise` | 52,7 s | Préférer l'acheteur avec reprise | Abonne-toi | ✅ thème 4 du brief |
| `cycles` | 82,1 s | Marge × rotation, risque panne sportive/citadine | Abonne-toi | ✅ choisir un véhicule qui tourne |
| `chiffres` | 58,5 s | Marché VO en 5 chiffres | Abonne-toi | ✅ un chiffre isolable (147 jours) |
| `marchand` | 81,2 s | Marchand ou intermédiaire | Abonne-toi | ✅ thème 7 du brief |
| `telephone-fini` | 58,2 s | Fin du démarchage téléphonique, 3 canaux | Abonne-toi | ✅ lancer son activité, avec réserve (voir n°11) |
| `montre` | 53,8 s | Technique de vente de l'extension de garantie | Abonne-toi | ⚪ réserve (vendeur, doublon avec garantie) |
| `xbow` | 57,1 s | Opportunité X-Bow | aucun | ❌ récit, pas de conseil isolable |
| `dubai` | 56,5 s | Rassemblements à Dubaï | Abonne-toi | ❌ lifestyle, pas un conseil |
| `vsl-diagnostic` | 52,6 s | VSL 16:9 | commercial | ❌ format 16:9 et appel commercial |
| `05-metier-pas-adapte` (Drive) | ~33 s | « L'envie ne suffit pas », face caméra | aucun | ✅ seul passage face caméra utilisable |

**Son et sous-titres.** Tous les Reels motion design ont ta vraie voix et des sous-titres incrustés, synchronisés au mot,
mot-clé en orange, jamais plus de 6 mots par bloc. Ils sont placés hors des 250 px du haut et des 400 px du bas, ce qui
couvre aussi les zones masquées en story. Les sous-titres d'origine sont donc conservés tels quels : pas de second jeu de
sous-titres par-dessus.

**Appels commerciaux.** Aucun Reel n'appelle au Plan de lancement, à la franchise ou à une candidature. Les seuls appels
sont des « Abonne-toi » / « Suis-moi » de fin : ils sont tous retirés.

**Visage.** Les Reels montés sont du motion design sur ta voix : tu n'y parles pas face caméra. On y voit seulement tes
photos (Porsche au volant, fin Jaguar). Le seul passage face caméra exploitable est `05-metier-pas-adapte.mp4`, sur Drive
(déjà nettoyé de toute mention de franchise en septembre). Les autres interviews du dossier Drive `Vidéo` tournent autour
de la franchise et du réseau : écartées, comme dans `PLAN-EDITORIAL.md`.

## 2. Sélection proposée (12 stories + 1 visuel fixe)

Ordre conseillé : du plus accessible (acheteur) au plus expert (entreprendre). Chaque story se comprend seule.

| N° | Titre | Source | Passages retenus (timecodes du Reel) | Durée | Message principal | Pourquoi |
|---|---|---|---|---|---|---|
| 01 | Mes 3 erreurs sur une Ferrari | `pire-marge` | 0,00–3,00 + 60,30–83,75 | 26,5 s | La confiance ne remplace pas un contrôle | Erreur vécue, chiffre réel (−17 000 €), ouvre sur l'humilité |
| 02 | Une mauvaise annonce n'est pas une mauvaise voiture | `porsche997` | 0,00–26,75 | 26,8 s | Juge le dossier, pas les photos | Méthode de vérification concrète (carnet, CT, rappels, historique) |
| 03 | Le kilométrage n'est pas le risque | `jaguar` | 0,00–3,60 + 9,30–15,65 + 63,10–73,40 | 20,3 s | Un compteur élevé avec historique se vend, un compteur bas sans historique non | Contre-intuitif, utile à tout acheteur |
| 04 | Extension de garantie : les 4 lignes à lire | `garantie-v5` | 26,65–52,40 | 25,8 s | Plafond, vétusté, remboursement, exclusions | Checklist directement applicable |
| 05 | La marge se fait à l'achat | `mini` | 0,00–2,35 + 70,30–81,85 | 13,9 s | Une restauration révèle la valeur d'une voiture recherchée, elle ne la crée pas | Choisir un modèle qui se revend |
| 06 | 6 200 € de marge ? Non, 4 167 € | `jaguar` | 33,00–63,10 | 30,1 s | Transport, révision et TVA mangent la marge | Calcul de marge réelle + frais oubliés |
| 06b | (visuel fixe) Le calcul de la vraie marge | chiffres du Reel Jaguar | — | PNG | Vente − achat − transport − révision − TVA due | Laisse le temps de lire le calcul |
| 07 | Prends l'acheteur avec reprise | `reprise` | 0,00–22,30 + 32,35–41,00 | 31,0 s | Même client, deux marges, mais ne surpaie pas la reprise | Thème 4, avec le piège pour rester nuancé |
| 08 | Commence par les voitures qui cassent pas cher | `cycles` | 58,25–78,35 | 20,1 s | Garantie légale et vices cachés : une panne coûte le prix de la voiture | Choisir un véhicule quand on démarre |
| 09 | 147 jours | `chiffres` | 43,45–54,75 | 11,3 s | Tourner en 30 jours, c'est 5 fois plus vite que le marché | Chiffre sourcé, story courte |
| 10 | Marchand ou intermédiaire | `marchand` | 0,00–8,90 + 46,75–62,05 | 24,2 s | Même voiture : 2 300 € avec 12 000 € bloqués, ou 1 500 € sans stock | L'intermédiation chiffrée, sans vendre d'offre |
| 11 | Trouver ses clients sans téléphone | `telephone-fini` | 0,00–3,30 + 15,65–43,45 | 31,1 s | Montre ton travail, soigne ta réputation, sois installé | Lancement d'activité |
| 12 | L'envie ne suffit pas | `05-metier-pas-adapte.mp4` (Drive) | intégral, déjà monté | ~33 s | Tempérament, expérience, faculté d'adaptation | Seule story face caméra |

**Réserves** (si tu veux remplacer une story) :
- `marchand` 62,20–77,40, « Avec 5 000 € en poche, tu peux être intermédiaire dès demain » (15 s) ;
- `chiffres` 13,55–24,60, « 47 % des ventes entre particuliers : un marché à prendre » (11 s) ;
- `montre` 44,60–48,40, « Une preuve vaut dix arguments » (trop court seul).

## 3. Points à trancher

1. **Visage.** Une seule story sur 12 te montre face caméra. Pour en avoir plus, il faudrait tourner de courtes prises :
   on ne peut pas en créer à partir des Reels.
2. **Story 12** : le fichier est privé sur Drive. Je tente de le récupérer ; sinon, dépose-le dans `01_SOURCES/`.
   Ton interlocuteur y apparaît, non nommé.
3. **Story 11** : « depuis le onze août » date la story dans un Highlight permanent. On garde, ou on démarre à
   « Le vrai problème, c'est pas la loi » (moins clair seul) ?
4. **Story 04** : le sous-titre « Demande au vendeur » ; ici le public est acheteur, donc il est cohérent.
5. **Durées** : 4 stories dépassent 25 s (26 à 31 s). Toutes restent sous 60 s ; couper plus enlèverait du contexte.

## 4. Montage prévu

- Coupe sèche dans les pauses, avec un fondu audio de 40 ms de part et d'autre. Quand deux passages sont éloignés, un
  fondu image de 6 images au raccord.
- Les visuels d'origine sont conservés : ta voix, tes sous-titres, aucun nouvel habillage, aucun logo. Seuls les
  « Abonne-toi » / « Suis-moi » sont retirés.
- Musique d'origine conservée sous la voix, avec un fondu de sortie de 0,4 s en fin de story.
- Export H.264 High, 1080×1920, 30 fps (comme les sources), AAC 48 kHz 192 kb/s, -14 LUFS, `+faststart`.
- Prototypes proposés : **01** (erreur vécue, deux passages raccordés) et **06** (calcul, avec le PNG 06b).
