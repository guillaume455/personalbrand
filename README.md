# Clips verticaux — marque perso Guillaume Herbin

Chaîne de production de clips 9:16 pour Instagram Reels et LinkedIn, découpés
depuis des rushes d'interview 16:9.

## Cadre éditorial

La marque perso reste séparée du réseau de franchise. Le réseau peut apparaître
en décor de crédibilité, jamais comme sujet. Aucun clip ne doit ressembler à du
recrutement de franchisés. Les arbitrages clip par clip sont dans
[`PLAN-EDITORIAL.md`](PLAN-EDITORIAL.md).

## Specs de sortie

| | |
|---|---|
| Format | 1080×1920 (9:16), 30 fps |
| Vidéo | H.264 high, CRF 18, `+faststart` |
| Audio | AAC 192 kb/s, 48 kHz, stéréo — son direct, pas de musique |
| Montage | coupe franche, aucune transition, aucun effet |

**Hook** : 3 premières secondes, fond `#0A0A0A`, texte serif blanc centré,
fin trait doré `#C9A84C` sous le texte.
Georgia n'existant pas sous Linux, la serif utilisée est **DejaVu Serif Bold**
(graisse et chasse proches). Alternative : Liberation Serif, plus fine.

**Sous-titres** : incrustés, blanc gras, bordure noire fine, centrés dans le
tiers bas, 2 lignes maximum par cue.

## Sous-titrage sans modèle ASR

Aucun modèle Whisper n'est téléchargeable depuis cet environnement (huggingface.co
et les miroirs sont hors politique réseau). À la place :

1. `ffmpeg silencedetect` repère les pauses réelles de la parole dans la fenêtre du clip ;
2. le texte de `subs/`, corrigé à la main, est découpé en unités de sous-titre ;
3. les unités sont réparties sur les segments de parole au prorata de leur longueur,
   silences sautés — les cues tombent donc sur les respirations.

Les textes de `subs/` disent **exactement** ce qui est prononcé : on corrige la
transcription automatique (noms propres, ponctuation), on ne réécrit pas le propos.
Neutraliser un mot au sous-titre alors qu'on l'entend ne masquerait rien.

Sur une machine avec accès réseau complet, `faster-whisper` donne un calage au mot
et remplace avantageusement cette étape.

## Utilisation

```bash
# Inspecter un rush
bash scripts/inspect.sh "rushes/12. VENTES DE DISTANCE.mp4"

# Produire un clip
bash scripts/make-clip.sh \
  --src "rushes/12. VENTES DE DISTANCE.mp4" \
  --start 0.4 --end 47.2 \
  --hook "70% des voitures de cette agence sont vendues à distance" \
  --text subs/01-ventes-distance.txt \
  --out exports/01-ventes-distance.mp4
```

Options de réglage :

| Option | Effet |
|---|---|
| `--crop-bias N` | décale la fenêtre de recadrage (px source) : négatif = gauche |
| `--sub-offset S` | décale tous les sous-titres de S secondes |
| `--hook-mode card` | carton muet de 3 s avant le clip, au lieu du hook en surimpression |

Par défaut (`--hook-mode overlay`) le son démarre dès la première image, sous le
carton : meilleure rétention qu'un début muet.

La charte (tailles, couleurs, marges) est centralisée dans `scripts/lib.sh`.

## Arborescence

```
rushes/     rushes source (non versionnés)
subs/       textes de sous-titres corrigés, un par clip
transcripts/ transcriptions brutes Fireflies, pour référence
scripts/    chaîne de production
exports/    clips finaux (non versionnés)
work/       fichiers intermédiaires (.ass, cartons, frames de contrôle)
```
