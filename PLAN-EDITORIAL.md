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
