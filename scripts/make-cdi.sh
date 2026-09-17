#!/usr/bin/env bash
# Clip 09 — « se lancer dans l'auto en gardant son CDI ».
# Prise face caméra de 94,18 s, déjà en 1080x1920 : make-clip.sh ne recadre
# donc rien. Deux écarts par rapport aux six clips d'interview :
#   - le son est normalisé en amont (la prise sort à -23,7 LUFS, la cible
#     sociale est à -14) ; la vidéo est copiée telle quelle ;
#   - un carton de constat précède le carton d'abonnement, parce que le propos
#     se termine sur une fin de phrase et non sur une chute.
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/lib.sh

SRC="rushes/0917 (1).mp4"
NORM="work/0917-norm.mp4"
OUT="exports/09-se-lancer-avec-un-cdi.mp4"
T="work/cdi/txt"; FB="$HOOK_FONT"
mkdir -p "$T" work/cdi exports

write() { printf '%s' "$2" > "$T/$1"; }
write f0.txt "Le vrai sujet,"
write f1.txt "ce n'est pas le temps."
write f2.txt "C'est de savoir"
write f3.txt "pourquoi on le fait."

dt() { printf "drawtext=expansion=none:fontfile='%s':textfile='%s':fontcolor=%s:fontsize=%s:x=(w-text_w)/2:y=%s" \
       "$FB" "$T/$1" "$3" "$2" "$4"; }
enc() { echo -c:v "$V_CODEC" -preset "$V_PRESET" -crf "$V_CRF" -profile:v "$V_PROFILE" \
        -pix_fmt "$PIX_FMT" -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2; }

echo "== normalisation du son (vidéo copiée) =="
ffmpeg -y -v error -i "$SRC" -c:v copy \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2 "$NORM"

echo "== corps =="
bash scripts/make-clip.sh --src "$NORM" --start 0 --end 94.18 \
  --hook "Se lancer dans l'auto en gardant son CDI ?" \
  --text "subs/09-se-lancer-avec-un-cdi.txt" \
  --out work/cdi/body.mp4

echo "== carton de constat =="
CARD="null,$(dt f0.txt 62 "$BLANC" 720),$(dt f1.txt 62 "$BLANC" 806)"
CARD+=",$(dt f2.txt 62 "$ACCENT" 950),$(dt f3.txt 62 "$ACCENT" 1036)"
CARD+=",drawbox=x=450:y=1190:w=180:h=6:color=${ACCENT}@1:t=fill"
ffmpeg -y -v error -f lavfi -i "color=c=${NOIR_PROFOND}:s=${OUT_W}x${OUT_H}:r=${FPS}:d=3" \
  -f lavfi -i "anullsrc=channel_layout=stereo:sample_rate=${A_RATE}" \
  -vf "$CARD" -t 3 $(enc) -shortest work/cdi/card.mp4

echo "== carton d'abonnement =="
ffmpeg -y -v error -loop 1 -t 2.5 -i assets/outro-bg.png \
  -f lavfi -t 2.5 -i "anullsrc=channel_layout=stereo:sample_rate=${A_RATE}" \
  -vf "scale=${OUT_W}:${OUT_H}:force_original_aspect_ratio=increase,crop=${OUT_W}:${OUT_H},setsar=1,fps=${FPS}" \
  $(enc) -shortest work/cdi/outro.mp4

echo "== assemblage =="
printf "file '%s'\n" "$PWD/work/cdi/body.mp4" "$PWD/work/cdi/card.mp4" "$PWD/work/cdi/outro.mp4" > work/cdi/list.txt
ffmpeg -y -v error -f concat -safe 0 -i work/cdi/list.txt $(enc) -movflags +faststart "$OUT"

echo "--- $OUT ---"
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height \
  -of default=noprint_wrappers=1 "$OUT"
