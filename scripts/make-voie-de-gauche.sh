#!/usr/bin/env bash
# Clip « voie de gauche » : POV autoroute, 6,1 s.
# La pastille de sous-titre d'origine (blanche, y=208..348 en coords source)
# est recouverte par un bandeau à la charte.
#
#   --mask        floute l'afficheur de vitesse numérique du combiné
#   --fin-legende carton de fin renvoyant à la légende, au lieu de la question
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/lib.sh

SRC="rushes/on roule a gauche.mp4"
T="work/gauche/txt"; FB="$HOOK_FONT"
MASK=""; FIN="question"
for a in "$@"; do
  case "$a" in
    --mask) MASK=1;;
    --fin-legende) FIN="legende";;
    *) echo "Option inconnue : $a" >&2; exit 1;;
  esac
done
OUT="exports/08-voie-de-gauche-v2${MASK:+-flou}${FIN:+-$FIN}.mp4"
mkdir -p "$T" work/gauche exports

write() { printf '%s' "$2" > "$T/$1"; }
write h0.txt  "C'est l'histoire d'un gars..."
write h1.txt  "Lis la légende"
write h2.txt  "pour la suite de l'histoire"
write q0.txt  "Et toi sur l'autoroute,"
write q1.txt  "t'es plus"
write q2.txt  "VOIE DE DROITE"
write q3.txt  "ou"
write q4.txt  "VOIE DE GAUCHE ?"
write l0.txt  "La suite de l'histoire"
write l1.txt  "EST EN LÉGENDE"

dt() { printf "drawtext=expansion=none:fontfile='%s':textfile='%s':fontcolor=%s:fontsize=%s:x=(w-text_w)/2:y=%s" \
       "$FB" "$T/$1" "$3" "$2" "$4"; }
enc() { echo -c:v "$V_CODEC" -preset "$V_PRESET" -crf "$V_CRF" -profile:v "$V_PROFILE" \
        -pix_fmt "$PIX_FMT" -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2; }

BAND_H=540                      # recouvre la pastille (source y=348 -> sortie y=522)

# L'afficheur numérique dérive avec les secousses : fenêtre relevée sur les
# 36 images de la séquence, x=250..550 et y=715..885 en coords source.
PRE="[0:v]"
if [[ -n "$MASK" ]]; then
  PRE="[0:v]split[a][b];[b]crop=300:170:250:715,boxblur=24:3[bl];[a][bl]overlay=250:715[m];[m]"
fi

CHAIN="${PRE}scale=${OUT_W}:${OUT_H}:flags=lanczos,setsar=1,fps=${FPS}"
CHAIN+=",drawbox=x=0:y=0:w=${OUT_W}:h=${BAND_H}:color=${NOIR_PROFOND}@1:t=fill"
CHAIN+=",$(dt h0.txt 62 "$BLANC" 130)"
CHAIN+=",drawbox=x=460:y=238:w=160:h=5:color=${ACCENT}@1:t=fill"
CHAIN+=",$(dt h1.txt 44 "$ACCENT" 296)"
CHAIN+=",$(dt h2.txt 44 "$ACCENT" 356)"
CHAIN+="[vout]"

echo "== corps ${MASK:+(vitesse floutée)} =="
ffmpeg -y -v warning -i "$SRC" -filter_complex "$CHAIN" \
  -map '[vout]' -map 0:a:0 $(enc) work/gauche/body.mp4

echo "== carton de fin ($FIN) =="
if [[ "$FIN" == "legende" ]]; then
  CARD="null,$(dt l0.txt 54 "$BLANC" 860),$(dt l1.txt 78 "$ACCENT" 946)"
  CARD+=",drawbox=x=450:y=1090:w=180:h=6:color=${ACCENT}@1:t=fill"
else
  CARD="null,$(dt q0.txt 54 "$BLANC" 680),$(dt q1.txt 54 "$BLANC" 752)"
  CARD+=",$(dt q2.txt 84 "$BLANC" 900),$(dt q3.txt 44 "$ACCENT" 1010)"
  CARD+=",$(dt q4.txt 84 "$ACCENT" 1090)"
  CARD+=",drawbox=x=450:y=1240:w=180:h=6:color=${ACCENT}@1:t=fill"
fi
ffmpeg -y -v warning -f lavfi -i "color=c=${NOIR_PROFOND}:s=${OUT_W}x${OUT_H}:r=${FPS}:d=2.5" \
  -f lavfi -i "anullsrc=channel_layout=stereo:sample_rate=${A_RATE}" \
  -vf "$CARD" -t 2.5 $(enc) -shortest work/gauche/card.mp4

echo "== assemblage =="
printf "file '%s'\n" "$PWD/work/gauche/body.mp4" "$PWD/work/gauche/card.mp4" > work/gauche/list.txt
ffmpeg -y -v warning -f concat -safe 0 -i work/gauche/list.txt $(enc) -movflags +faststart "$OUT"
echo "--- $OUT ---"
ffprobe -v error -show_entries format=duration -show_entries stream=width,height -of default=noprint_wrappers=1 "$OUT"
