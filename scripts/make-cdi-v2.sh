#!/usr/bin/env bash
# Clip 09, version 2 — resserrée, avec accroche prélevée.
#
# Différences avec la v1 :
#   - accroche : la phrase de chute est remontée en tête, son hésitation de
#     2,5 s retirée au passage (86,70-88,62 recollé à 91,28-92,85) ;
#   - carton court qui pose la question, sans quoi « la réponse est oui »
#     ne répond plus à rien, le préambule ayant sauté ;
#   - corps resserré de 94,18 s à 50,7 s : préambule, parenthèse sur les
#     enfants et redite du milieu retirés ;
#   - débruitage avant normalisation ;
#   - sous-titres générés segment par segment pour borner la dérive.
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/lib.sh

CLEAN="work/cdi2/clean.mp4"; W="work/cdi2"; T="$W/txt"
OUT="exports/09-cdi-v2.mp4"; FB="$HOOK_FONT"
mkdir -p "$T" "$W" exports

write() { printf '%s' "$2" > "$T/$1"; }
write q0.txt "Peut-on se lancer dans l'auto"
write q1.txt "en gardant son CDI ?"
dt() { printf "drawtext=expansion=none:fontfile='%s':textfile='%s':fontcolor=%s:fontsize=%s:x=(w-text_w)/2:y=%s" "$FB" "$T/$1" "$3" "$2" "$4"; }
enc() { echo -c:v "$V_CODEC" -preset "$V_PRESET" -crf "$V_CRF" -profile:v "$V_PROFILE" \
        -pix_fmt "$PIX_FMT" -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2; }

# --- Sous-titres, un fichier par segment ---
subs() { # segment texte sortie
  SUB_FONT="$SUB_FONT" SUB_FONTSIZE="$SUB_FONTSIZE" SUB_OUTLINE="$SUB_OUTLINE" \
  SUB_SHADOW="$SUB_SHADOW" SUB_MARGIN_V="$SUB_MARGIN_V" SUB_MAX_CHARS="$SUB_MAX_CHARS" \
  OUT_W="$OUT_W" OUT_H="$OUT_H" \
  python3 scripts/build_subs.py --src "$1" --start 0 \
    --end "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1")" \
    --text "$2" --out "$3" >/dev/null
}

echo "== accroche =="
ffmpeg -y -v error -f concat -safe 0 -i <(printf "file '%s'\n" "$PWD/$W/seg0.mp4" "$PWD/$W/seg1.mp4") \
  $(enc) "$W/accroche-raw.mp4"
subs "$W/accroche-raw.mp4" subs/cdi2/seg-accroche.txt "$W/accroche.ass"
ffmpeg -y -v error -i "$W/accroche-raw.mp4" -vf "ass='$W/accroche.ass'" $(enc) "$W/A.mp4"

echo "== carton question =="
ffmpeg -y -v error -f lavfi -i "color=c=${NOIR_PROFOND}:s=${OUT_W}x${OUT_H}:r=${FPS}:d=1.7" \
  -f lavfi -i "anullsrc=channel_layout=stereo:sample_rate=${A_RATE}" \
  -vf "null,$(dt q0.txt 56 "$BLANC" 870),$(dt q1.txt 56 "$BLANC" 948),drawbox=x=460:y=1080:w=160:h=5:color=${ACCENT}@1:t=fill" \
  -t 1.7 $(enc) -shortest "$W/B.mp4"

echo "== corps =="
ffmpeg -y -v error -f concat -safe 0 \
  -i <(printf "file '%s'\n" "$PWD/$W/seg2.mp4" "$PWD/$W/seg3.mp4" "$PWD/$W/seg4.mp4" "$PWD/$W/seg5.mp4") \
  $(enc) "$W/corps-raw.mp4"
OFF=0; ARGS=()
for s in 2 3 4 5; do
  subs "$W/seg$s.mp4" "subs/cdi2/seg$s.txt" "$W/s$s.ass"
  ARGS+=("$W/s$s.ass" "$OFF")
  OFF=$(awk -v o="$OFF" -v d="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$W/seg$s.mp4")" 'BEGIN{print o+d}')
done
python3 scripts/fusion_ass.py "$W/corps.ass" "${ARGS[@]}"
ffmpeg -y -v error -i "$W/corps-raw.mp4" -vf "ass='$W/corps.ass'" $(enc) "$W/C.mp4"

echo "== carton d'abonnement =="
ffmpeg -y -v error -loop 1 -t 2.5 -i assets/outro-bg.png \
  -f lavfi -t 2.5 -i "anullsrc=channel_layout=stereo:sample_rate=${A_RATE}" \
  -vf "scale=${OUT_W}:${OUT_H}:force_original_aspect_ratio=increase,crop=${OUT_W}:${OUT_H},setsar=1,fps=${FPS}" \
  $(enc) -shortest "$W/D.mp4"

echo "== assemblage =="
printf "file '%s'\n" "$PWD/$W/A.mp4" "$PWD/$W/B.mp4" "$PWD/$W/C.mp4" "$PWD/$W/D.mp4" > "$W/final.txt"
ffmpeg -y -v error -f concat -safe 0 -i "$W/final.txt" $(enc) -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height \
  -of default=noprint_wrappers=1 "$OUT"
