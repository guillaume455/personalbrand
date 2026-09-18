# Plan éditorial — 6 clips verticaux marque perso

Règle appliquée à chaque coupe : le clip doit tenir debout sans le mot « franchise »,
sans logo ni habillage réseau, et sans jamais ressembler à du recrutement de franchisés.
FORGE n'est mentionné nulle part.

Les points de coupe ci-dessous sont exprimés en **repères de texte**. Les timecodes exacts
seront calés dès réception des rushes (`silencedetect` donne les bornes de parole à ~0,1 s).

Légende : ✅ aucun arbitrage — ⚠️ arbitrage à trancher par Guillaume

---

## 1. `01-ventes-distance.mp4` ✅ **PRODUIT ET VALIDÉ**
**Source** : `12. VENTES DE DISTANCE.mp4` (1080×1920, 32,72 s, 50 fps)
**Hook** : « 70% des voitures de cette agence sont vendues à distance »

**Coupe retenue : 2,0 s → 32,72 s** (durée finale 30,7 s).
Retire l'amorce « J'ai eu des stats sympas d'ailleurs à ce sujet », sans valeur
hors contexte d'interview. Se termine sur la chute « c'est vraiment impressionnant ».
Le hook masque 2,0→5,0 s : l'image se révèle exactement sur « font 70% de leurs
ventes ». « Pour cette vidéo », audible sous le carton noir, est conservé (arbitré).

**Analyse** : aucune occurrence de « franchise », « franchisé » ou « réseau ».
Le clip se comprend seul. « L'agence dans laquelle on se trouve » fonctionne comme
décor de crédibilité sans jamais devenir le sujet. La fin sur la livraison physique
donne la nuance qui évite l'effet « tout digital » — on la garde comme demandé.

---

## 2. `02-salarie-gerant.mp4` ⚠️
**Source** : `43. DE SALARIÉ A GERANT, QUE DU BONHEUR.mp4`
**Hook** : « Il y a quelques mois, il était salarié »

**Coupe** : intégral. Chute sur « comment je fais pour optimiser ma fiscalité ? /
Vraiment pour le coup, c'est que du bonheur ».

**⚠️ À trancher** : la toute première phrase est « Quand je vois **des franchisés** qui
étaient salariés il y a encore quelques mois ». Le mot porte le sujet grammatical de
toute la tirade — il n'est pas retirable proprement. Trois options :

1. **Garder tel quel.** Le mot passe une fois, en ouverture, et le reste du clip parle
   d'indépendance et de fiscalité. C'est l'option la plus propre au montage.
2. **Micro-coupe sur le mot** (~0,4 s) : « Quand je vois des — qui étaient salariés ».
   Techniquement faisable, mais la coupe s'entend.
3. **Démarrer après** : le clip ouvre sur « qui étaient salariés il y a encore quelques
   mois... ». Le hook pose le sujet, mais la phrase démarre sur un relatif orphelin.

Également présent : « des passionnés **qui rentrent chez nous** » — implique une structure
d'accueil sans la nommer. Je le considère comme acceptable (décor), à confirmer.

---

## 3. `03-types-locaux.mp4` ✅ **PRODUIT**
**Source** : `03. CHANGEMENT DES TYPES DE LOCAUX.mp4` (1080×1920, 25,64 s)
**Hook** : « On a démarré avec des agences de 40 m². Aujourd'hui on fait l'inverse »

**Coupe retenue : 1,28 s → 25,64 s** (durée finale 27,4 s avec la cover de fin).
Le rush ouvre sur « Quand on a vraiment lancé **la franchise**, quand on a eu nos
premières agences… ». L'analyse d'énergie audio situe la pause après « franchise, »
à 1,18-1,28 s, « quand on » reprenant à 1,30 s : la coupe à 1,28 s retire le mot
sans casser la syntaxe. La cover masque jusqu'à 4,28 s, le sous-titre d'origine
« LA FRANCHISE, QUAND ON » restant affiché jusqu'à 1,50 s. L'image se révèle sur
« vraiment pas les mêmes qu'aujourd'hui », en fin de proposition.

**Analyse** : les deux propositions d'ouverture disent la même chose, on supprime la
première et on garde la seconde. Zéro perte de sens, mot évacué. Le reste est un pur
propos de stratégie immobilière et d'adaptation de modèle.

**Cover** : `assets/cover-03.png` — « Comment notre modèle a évolué au fil des années ».
Une première version annonçait « le concept d'intermédiation », mot jamais prononcé dans
ce rush, qui parle de locaux : promesse corrigée.

---

## 4. `04-retours-investissement.mp4` ✅ **PRODUIT ET VALIDÉ**
**Source** : `40. retours sur invest.mp4` (1080×1920, 20,50 s)
**Cover** : `assets/cover-04.png` — « Rentabiliser son activité plus vite qu'on le croit »

**Coupe retenue : 2,58 s → 18,84 s**, durée finale 18,1 s.

- **En tête** : le silence à 2,09-2,60 s permet de retirer « Demain, si tu deviens
  franchisés chez nous » tout en gardant « tu peux rembourser tes charges de structure,
  en tout cas dès les premiers mois d'activité ». Version longue plutôt que les ~15 s
  redoutées. La cover masque jusqu'à 5,58 s, soit le silence de 5,44-6,00 s : l'image
  se révèle juste avant « Contrairement à un marchand classique ».
- **En fin** : coupe à 18,84 s, après « en tout cas », avant « avec le modèle BHCAR ».

**Montage particulier — cover de fin anticipée.** Le sous-titre d'origine groupe
« L'INTERMÉDIATION, EN TOUT CAS AVEC » dans un seul bloc affiché dès 17,60 s. Impossible
de garder le mot à l'audio sans afficher ce « AVEC » jamais prononcé, ce qui donnait
l'impression d'un son coupé. Effacement par interpolation et flou localisé ont tous deux
été essayés : traînées et bande floue visibles, inutilisables.

Solution retenue : **la cover de fin apparaît à 15,02 s, pendant la fin de la phrase.**
L'audio se poursuit jusqu'à 16,26 s sur l'image de fin. Le sous-titre gênant n'est jamais
affiché, sans aucune retouche visible. Assemblage en trois segments :

```bash
# A : source 2,58 -> 17,60, cover d'ouverture en surimpression sur 3 s
# B : source 17,60 -> 18,84, image = cover de fin, son = fin de la phrase
# C : cover de fin en silence, 1,8 s
# puis concat A + B + C
```

---

## 5. `05-metier-pas-adapte.mp4` ✅
**Source** : `37. UN MÉTIER PAS ADAPTÉ A TOUT LE MONDE.mp4`
**Hook** : « L'envie ne suffit pas »

**Coupe** : intégral, échange compris. Chute sur « il faut se faire un peu violence ».

**Analyse** : aucune occurrence de « franchise » ou « réseau » dans tout le rush.
L'échange avec l'interlocuteur tient au montage et apporte la preuve vécue qui manque
à ta seule prise de parole — je recommande de le garder. Le ping-pong court
(« À. » / « S'adapter. ») est un chevauchement de voix : au montage ça s'entend comme
une fin de phrase normale, les sous-titres le lissent en « la faculté qu'on va avoir
aussi à s'adapter ».

Seul point : ton interlocuteur apparaît à l'image. Il n'est jamais nommé et rien
n'indique son statut — le clip se lit comme une conversation entre professionnels.

---

## 6. `06-tous-les-ages.mp4` ⚠️ (format court validé)
**Source** : `35. DES FRANCHISÉS A TOUS LES AGES.mp4`
**Hook** : « De 19 à plus de 60 ans »

**Coupe** : deux fragments seulement, le reste est écarté.
- « on a vu vraiment tous les âges »
- « on a vraiment de 19-20 ans jusqu'à plus de 60. Ça arrive pour le coup, ça fait
  vraiment diversité » — **en coupant les deux derniers mots « dans les franchisés »**.

**Écarté** (contient prénoms/noms, conformément à ta consigne) : l'ouverture « on avait
21 et 22 ans avec Mathieu », tout le passage « Sébastien Guérin et son cousin /
notre animateur réseau », et « le dernier en date, c'est Bruno, de [ville], parti à la
retraite l'année dernière ».

**Durée attendue : ~12 s.** Format court assumé, validé. Le hook porte le clip, la voix
apporte la fourchette d'âges, et le message « pas de profil type » se lit sans contexte.
Si les deux fragments ne se raccordent pas proprement à l'image (changement de posture
entre les deux prises de parole), je te le signale avant export et on avise.

---

## Récapitulatif des mentions traitées

| Clip | Mention repérée | Traitement |
|------|-----------------|------------|
| 1 | — | rien à traiter |
| 2 | « des franchisés » (1re phrase) | ⚠️ indispensable au sens — 3 options ci-dessus |
| 2 | « qui rentrent chez nous » | conservé (décor implicite) |
| 3 | « lancé la franchise » | supprimé, reformulation redondante disponible |
| 4 | « si tu viens te franchiser chez nous » | supprimé (intro) |
| 4 | « le modèle BHK » | supprimé (fin) |
| 5 | — | rien à traiter |
| 6 | « franchisés » (×3), « réseau », 4 noms propres | supprimés, clip réduit aux âges |

---

# Clip 6 : abandonné

Décision du 16/09. Après retrait de tous les prénoms et noms, le rush ne laissait
que 4,3 s de parole exploitable sur 41 s. Le montage produit
(`exports/06-tous-les-ages.mp4`, 10,3 s dont 6 s de cartons) est conservé pour
mémoire mais n'est pas destiné à la publication.

Le message « il n'y a pas d'âge pour se lancer » reste valable et la cover
`assets/cover-06.png` est prête : il demande une prise tournée en solo.

---

# Rushes restants : que reste-t-il d'exploitable ?

Analyse des 12 autres fichiers du dossier Drive `Vidéo`, à partir des
transcriptions Fireflies. Critère : le clip doit tenir sans « franchise »,
« franchisé », « réseau », sans marque BH/BHK ni nom de personne.

## Exploitable en l'état

**`09. DIGITALISATION DES PROCESS.mp4`** (92 Mo) — **aucune mention à traiter.**
Automatisation des tâches sans valeur ajoutée, puis comparaison 2013 / aujourd'hui :
mandats imprimés et remplis à la main, tour du véhicule et fiche technique sur papier,
contre un véhicule en ligne dès le départ du client. L'interlocuteur porte le récit du
« avant », comme dans le clip 5. Le meilleur candidat restant.

## Exploitables avec coupes

**`08. AUTOMATISATION & CRM.mp4`** (38 Mo) — une seule occurrence de « franchisés »,
au milieu d'une phrase. Le reste est propre : automatisations, CRM amélioré de mois en
mois, efficacité sur le cœur de métier — « rentrer des mandats et vendre des véhicules ».
Court, à vérifier au calage.

**`15. LE TRI-METIER.mp4`** (91 Mo) — mentions concentrées au début (« par rapport au
réseau qui existe ») et à la fin (« les nouveaux franchisés », « intégrer la franchise »,
« ouvrir un BHK »). Le milieu tient seul : point de contrôle, passage à l'atelier,
garantie mécanique, vitrage depuis 2018, notion de centre à trois métiers.

## Inexploitables

| Fichier | Motif |
|---|---|
| `17. LOGICIELS DEV. EN INTERNE` | le propos repose sur « on est le seul réseau », cite BHK |
| `21. LA FRANCHISE C'EST COMME AVOIR UN ASSOCIÉ` | la franchise est le sujet même |
| `23. LE RESEAU EN CONVENTION` | conventions nationales, réunions secteur |
| `24. L'HISTOIRE DE JEREMY` | « de franchisé à franchiseur », BHK, bhcar.fr |
| `30. LA BH ACADEMY` | la marque est le sujet |
| `32. PLUS QU'UNE FORMATION` | BH Academy, animateur réseau, siège social |
| `38. LE RECRUTEMENT DES FUTURS FRANCHISÉS` | recrutement de franchisés + nom d'un collaborateur |
| `GUILLAUME 1` / `GUILLAUME 2` | vœux d'entreprise : groupe BH, 30 nouveaux franchisés, 15 ans de la marque |

---

# Clips montés sur vidéos tierces

Format distinct des six clips d'interview : on reprend une vidéo trouvée sur les
réseaux et on la commente. Deux points valent pour tous les clips de cette
série : le compte d'origine doit être crédité à l'écran, et le texte anglais ou
la pastille de sous-titre d'origine doit être recouvert, jamais laissé visible.

## `07-scam-italie.mp4`
Source `rushes/scam italy.mp4`. Voir `transcripts/scam-italy.md` pour le relevé
et `captions/07-scam-italie.md` pour la légende.

**Arbitrage retenu** : ne jamais écrire que l'acheteur est passé par une vente
aux enchères. La source ne parle que de photos d'annonce. L'angle publié est
« acheter sans avoir vu la voiture », qui englobe enchères, annonce et import
sans rien affirmer d'invérifiable.

## `08-voie-de-gauche.mp4`
Source `rushes/on roule a gauche.mp4` (6,1 s, 720x1280). POV autoroute au volant
d'une Porsche. La pastille blanche d'origine (« Y A QUE SUR L'AUTOROUTE QU'ON EST
DE GAUCHE », coords source y=208..348) est recouverte par un bandeau à la charte
portant le texte réécrit. Carton de fin : question d'engagement.

**⚠️ À trancher — la vitesse est lisible.** L'afficheur numérique du combiné passe
de 130 à 185 km/h en six secondes, parfaitement lisible à l'image. Sur une
autoroute européenne, c'est un excès de vitesse caractérisé, et la vidéo est une
séquence d'accélération : l'image ne montre pas un dépassement, elle montre une
montée en vitesse.

Deux exports sont produits :

| Fichier | État |
|---|---|
| `exports/08-voie-de-gauche.mp4` | tel que demandé, vitesse lisible |
| `exports/08-voie-de-gauche-flou.mp4` | afficheur numérique flouté |

Le floutage porte sur une fenêtre de 300x170 px en coords source à (250, 715),
relevée sur les 36 images de la séquence pour couvrir la dérive due aux secousses.
Le compte-tours reste visible : il ne donne pas de vitesse.

**Pas de carton d'abonnement sur ce clip.** Le corps ne dure que 6,1 s : la chute
est une punchline qui gagne à boucler. Ajouter 2,5 s de carton supplémentaire
casserait la boucle, qui compte beaucoup pour la portée en Reels.

---

## `09-se-lancer-avec-un-cdi.mp4` ✅ **PRODUIT**
**Source** : `rushes/0917 (1).mp4` — 1080x1920 natif, 94,18 s, HEVC, plein cadre.
Première prise face caméra correctement exportée : format vertical respecté,
durée complète, aucun habillage incrusté, aucun carton CapCut.

**Coupe retenue : 0 → 94,18 s, intégrale.** Durée finale 99,7 s avec les cartons.

**Pourquoi rien n'est coupé.** Le propos est une seule phrase enchaînée, du
premier au dernier mot : chaque segment reprend la subordonnée du précédent
(« … ce deuxième travail » / « parce que si vous avez un travail à côté… » /
« et cette liberté, vous allez pouvoir l'avoir à partir du moment où… »).
Retirer le milieu casse la syntaxe. Le relevé technique va dans le même sens :
`silencedetect` ne trouve **aucune pause de plus de 0,25 s avant 57,9 s**.
Il n'existe donc pas de point de coupe propre dans la première minute — c'est
94 s ou rien.

**Analyse éditoriale** : aucune occurrence de « franchise », « franchisé » ou
« réseau ». « Intermédiation » est prononcé une fois, conservé comme au clip 4 :
c'est du vocabulaire métier, pas un nom de marque. Le clip tient seul.

**Deux écarts par rapport aux six clips d'interview**, tous deux dans
`scripts/make-cdi.sh` :

- **Son normalisé en amont.** La prise sort à −23,7 LUFS, la cible sociale est
  à −14. La piste est refaite au `loudnorm`, la vidéo copiée sans ré-encodage.
  Sortie mesurée : −15,6 LUFS intégré, crête −0,66 dBTP.
- **Un carton de constat avant le carton d'abonnement.** Le propos s'achève sur
  « les marges générées vous suffiront à quitter votre CDI » — une fin de
  phrase, pas une chute. Le carton porte la chute à sa place : « Le vrai sujet,
  ce n'est pas le temps. C'est de savoir pourquoi on le fait. » C'est une
  proposition de ma part, pas une citation : à retirer d'une ligne si tu la
  trouves de trop.

**Correction apportée au pipeline commun.** `build_subs.py` remplissait chaque
ligne au maximum, ce qui laissait le reliquat seul en fin de phrase : le dernier
sous-titre du clip était « CDI. », affiché 0,08 s. Le découpage est désormais
équilibré et les fragments de moins de douze caractères sont rattachés au
précédent. Résultat : 33 sous-titres, le plus court durant 1,31 s.

### `09-cdi-v2.mp4` — version resserrée

Produite après retour extérieur : trop longue, manque de rythme, bruit de rue,
et une accroche qui n'accroche pas. Les quatre points étaient fondés.

**Ce que la v1 avait de faux.** J'avais conclu « 94 s ou rien » en cherchant des
silences où couper. Mauvais critère : on ne coupe pas une vidéo sociale sur les
respirations, on la coupe sur les redites. Il y en avait trois.

**Montage retenu** — 58,6 s contre 99,7 :

| Segment source | Contenu |
|---|---|
| 86,70 → 88,62 + 91,28 → 92,85 | accroche prélevée, hésitation retirée |
| *carton 1,7 s* | « Peut-on se lancer dans l'auto en gardant son CDI ? » |
| 14,45 → 32,30 | la réponse, puis la réalité des journées |
| 36,05 → 54,75 | l'autodiscipline, savoir pourquoi |
| 76,25 → 88,62 + 91,28 → 92,85 | la liberté, et la chute en rappel |

Écarté : le préambule de 14 s, la parenthèse sur les enfants, et la redite du
milieu (« parce que si vous avez un travail à côté… soit votre situation
financière ne vous convient pas »).

**L'accroche prélevée.** La phrase de chute contenait une hésitation de 2,5 s,
mesurée à l'enveloppe audio : « les marges générées vous suffiront » / silence /
« à quitter votre CDI ». Les deux moitiés sont recollées, la phrase tient en
3,5 s. Elle revient à la fin, en rappel.

Le carton qui suit n'est pas décoratif : le préambule ayant sauté, « la réponse
est oui » ne répondait plus à rien.

**Bruit.** Mesure sur une pause : plancher à −49,9 dB pour une parole à −28,5,
soit 22 dB de rapport signal/bruit. L'énergie du bruit est concentrée entre 200
et 1000 Hz, en plein dans la voix — c'est de l'ambiance urbaine, le type le plus
difficile à retirer. `afftdn` en réglage moyen gagne 4 dB, bande vocale préservée
à 0,3 dB près à la mesure. La mesure ne détecte pas les artefacts : à écouter au
casque. Le correctif réel est un micro-cravate au tournage.

**Dérive des sous-titres corrigée.** `build_subs.py` répartit le texte au prorata
des caractères ; sur une prise débitée sans pause, l'écart s'accumule — jusqu'à
2,5 s de retard en fin de v1. Les sous-titres sont désormais générés segment par
segment puis recollés par `fusion_ass.py`. Vérifié sur six points de contrôle en
comparant le texte affiché à ce qui est prononcé : concordant partout.


### `08-voie-de-gauche-v2` — bandeau réécrit

Le bandeau ne porte plus la phrase réécrite mais une amorce de récit :

> **C'est l'histoire d'un gars...**
> *Lis la légende pour la suite de l'histoire*

Accroche en blanc 62 px, appel à l'action en orange 44 px sous le trait, pour
que les deux rôles se distinguent au premier coup d'œil. Le bandeau couvre
toujours la pastille d'origine (source y=208..348).

**Le carton de fin entre en conflit avec cette amorce.** « Et toi sur
l'autoroute, t'es plus voie de droite ou voie de gauche ? » envoie en
commentaire, quand le bandeau envoie en légende : la dernière consigne vue
contredit la première. Deux exports sont donc produits, tous deux avec la
vitesse floutée :

| Fichier | Carton de fin |
|---|---|
| `…-flou-question.mp4` | la question d'origine, sur les voies |
| `…-flou-legende.mp4` | « La suite de l'histoire **est en légende** » |

**La légende existante ne convient plus.** `captions/08-voie-de-gauche.md` est
un post de débat sur les files de circulation ; le clip promet désormais une
histoire. Tant que l'histoire n'est pas écrite, la promesse du bandeau n'est
pas tenue — et une amorce de récit sans récit derrière est le seul vrai risque
de ce montage.
