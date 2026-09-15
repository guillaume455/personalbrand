#!/usr/bin/env bash
# Produit un clip vertical 1080x1920 prêt pour Reels / LinkedIn :
# recadrage 9:16, sous-titres incrustés, carton d'ouverture signature.
#
# Usage :
#   make-clip.sh --src RUSH.mp4 --start 4.2 --end 38.0 \
#                --hook "70% des voitures sont vendues à distance" \
#                --text texte-sous-titres.txt \
#                --out exports/01-ventes-distance.mp4 \
#                [--crop-bias 0] [--hook-mode overlay|card] [--sub-offset 0]
#
# --crop-bias  décale la fenêtre de recadrage (px source) : négatif = gauche.
# --hook-mode  overlay = le son démarre sous le carton (meilleure rétention)
#              card    = carton muet de 3 s, puis le clip
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/lib.sh

SRC=""; START=""; END=""; HOOK=""; TEXT=""; OUT=""
CROP_BIAS=$CROP_BIAS_DEFAULT; HOOK_MODE="overlay"; SUB_OFFSET=0
HOOK_BG=""; OUTRO=""; OUTRO_DUR="$OUTRO_DUR_DEFAULT"; OUTRO_TEXT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --src) SRC="$2"; shift 2;;
    --start) START="$2"; shift 2;;
    --end) END="$2"; shift 2;;
    --hook) HOOK="$2"; shift 2;;
    --text) TEXT="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    --crop-bias) CROP_BIAS="$2"; shift 2;;
    --hook-mode) HOOK_MODE="$2"; shift 2;;
    --sub-offset) SUB_OFFSET="$2"; shift 2;;
    --hook-bg) HOOK_BG="$2"; shift 2;;
    --outro) OUTRO="$2"; shift 2;;
    --outro-dur) OUTRO_DUR="$2"; shift 2;;
    --outro-text) OUTRO_TEXT="$2"; shift 2;;
    *) echo "Option inconnue : $1" >&2; exit 1;;
  esac
done
[[ -z "$HOOK_BG" || -f "$HOOK_BG" ]] || { echo "Image de hook introuvable : $HOOK_BG" >&2; exit 1; }
[[ -z "$OUTRO" || -f "$OUTRO" ]] || { echo "Image de fin introuvable : $OUTRO" >&2; exit 1; }
[[ -n "$SRC" && -n "$START" && -n "$END" && -n "$OUT" ]] || {
  echo "Paramètres manquants (--src --start --end --out)" >&2; exit 1; }
[[ -f "$SRC" ]] || { echo "Introuvable : $SRC" >&2; exit 1; }

mkdir -p work exports
BASE="$(basename "${OUT%.*}")"
DUR=$(python3 -c "import sys;print('%.3f' % (float(sys.argv[1])-float(sys.argv[2])))" "$END" "$START")

# --- Dimensions source, pour un recadrage en pixels entiers et pairs ---
IFS=',' read -r SRC_W SRC_H < <(ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height -of csv=p=0 "$SRC")
CROP_W=$(python3 -c "
import sys
w,h=int(sys.argv[1]),int(sys.argv[2])
cw=min(w,int(h*9/16))
print(cw-(cw%2))" "$SRC_W" "$SRC_H")
CROP_X=$(python3 -c "
import sys
w,cw,b=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
x=(w-cw)//2+b
x=max(0,min(w-cw,x))
print(x-(x%2))" "$SRC_W" "$CROP_W" "$CROP_BIAS")
echo "Source ${SRC_W}x${SRC_H} -> fenêtre ${CROP_W}x${SRC_H} à x=${CROP_X} (biais ${CROP_BIAS})"

# --- Sous-titres ---
SUBS="work/${BASE}.ass"
if [[ -n "$TEXT" && -f "$TEXT" ]]; then
  SUB_FONT="$SUB_FONT" SUB_FONTSIZE="$SUB_FONTSIZE" SUB_OUTLINE="$SUB_OUTLINE" \
  SUB_SHADOW="$SUB_SHADOW" SUB_MARGIN_V="$SUB_MARGIN_V" SUB_MAX_CHARS="$SUB_MAX_CHARS" \
  OUT_W="$OUT_W" OUT_H="$OUT_H" \
  python3 scripts/build_subs.py --src "$SRC" --start "$START" --end "$END" \
    --text "$TEXT" --out "$SUBS" --offset "$SUB_OFFSET"
else
  echo "Pas de fichier texte : clip produit sans sous-titres."
  SUBS=""
fi

# --- Carton d'ouverture : une ligne par fichier, pour un centrage exact ---
HOOK_PREFIX="work/${BASE}-hook"
NLINES=1
if [[ -n "$HOOK" ]]; then
  rm -f "${HOOK_PREFIX}"-*.txt
  NLINES=$(HOOK_MAX_CHARS="$HOOK_MAX_CHARS" python3 scripts/wrap_hook.py "$HOOK" "$HOOK_PREFIX")
fi

LINE_H=$((HOOK_FONTSIZE + HOOK_LINE_SPACING))
TEXT_H=$((NLINES * LINE_H - HOOK_LINE_SPACING))
TEXT_Y=$(( (OUT_H - TEXT_H) / 2 - 40 ))
RULE_Y=$((TEXT_Y + TEXT_H + HOOK_RULE_GAP))
RULE_X=$(( (OUT_W - HOOK_RULE_W) / 2 ))

# drawtext aligne un bloc multi-lignes à gauche : on dessine chaque ligne
# séparément pour qu'elles soient réellement centrées.
build_hook_text() {
  local en="$1" out="" i y
  for ((i = 0; i < NLINES; i++)); do
    y=$((TEXT_Y + i * LINE_H))
    out+=",drawtext=expansion=none:fontfile='${HOOK_FONT}':textfile='${HOOK_PREFIX}-${i}.txt'"
    out+=":fontcolor=${BLANC}:fontsize=${HOOK_FONTSIZE}:x=(w-text_w)/2:y=${y}"
    if [[ -n "$en" ]]; then out+=":${en}"; fi
  done
  printf '%s' "$out"
}

# --- Chaîne de filtres ---
VF="crop=${CROP_W}:${SRC_H}:${CROP_X}:0,scale=${OUT_W}:${OUT_H}:flags=lanczos,setsar=1,fps=${FPS}"
if [[ -n "$SUBS" ]]; then VF="${VF},ass='${SUBS}'"; fi

# Habillage du hook. Trois cas :
#  - image seule  : la cover porte déjà son texte, on ne surimprime rien ;
#  - image + texte : le texte et le trait doré se posent sur l'image ;
#  - texte seul   : aplat noir profond derrière le texte.
HOOK_OVERLAY=""; HOOK_TEXT_CHAIN=""
if [[ ( -n "$HOOK" || -n "$HOOK_BG" ) && "$HOOK_MODE" == "overlay" ]]; then
  EN="enable='lt(t,${HOOK_DUR})'"
  if [[ -n "$HOOK_BG" ]]; then
    HOOK_OVERLAY="yes"
  else
    VF="${VF},drawbox=x=0:y=0:w=${OUT_W}:h=${OUT_H}:color=${NOIR_PROFOND}@1:t=fill:${EN}"
  fi
  if [[ -n "$HOOK" ]]; then
    HOOK_TEXT_CHAIN="$(build_hook_text "$EN"),drawbox=x=${RULE_X}:y=${RULE_Y}:w=${HOOK_RULE_W}:h=${HOOK_RULE_H}:color=${DORE}@1:t=fill:${EN}"
  fi
  if [[ -z "$HOOK_OVERLAY" ]]; then VF="${VF}${HOOK_TEXT_CHAIN}"; fi
fi

# Sortie principale : fichier final, ou segment intermédiaire si un visuel
# de fin doit être concaténé derrière.
MAIN="$OUT"
if [[ -n "$OUTRO" ]]; then MAIN="work/${BASE}-main.mp4"; fi

echo "Encodage -> $MAIN"
if [[ "$HOOK_MODE" == "card" && -n "$HOOK" ]]; then
  CARD="work/${BASE}-card.mp4"
  ffmpeg -y -v warning -stats \
    -f lavfi -i "color=c=${NOIR_PROFOND}:s=${OUT_W}x${OUT_H}:r=${FPS}:d=${HOOK_DUR}" \
    -f lavfi -i "anullsrc=channel_layout=stereo:sample_rate=${A_RATE}" \
    -vf "null$(build_hook_text ""),drawbox=x=${RULE_X}:y=${RULE_Y}:w=${HOOK_RULE_W}:h=${HOOK_RULE_H}:color=${DORE}@1:t=fill" \
    -t "$HOOK_DUR" -c:v "$V_CODEC" -preset "$V_PRESET" -crf "$V_CRF" \
    -profile:v "$V_PROFILE" -pix_fmt "$PIX_FMT" \
    -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2 -shortest "$CARD"

  BODY="work/${BASE}-body.mp4"
  ffmpeg -y -v warning -stats -ss "$START" -t "$DUR" -i "$SRC" \
    -vf "$VF" -c:v "$V_CODEC" -preset "$V_PRESET" -crf "$V_CRF" \
    -profile:v "$V_PROFILE" -pix_fmt "$PIX_FMT" \
    -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2 "$BODY"

  printf "file '%s'\nfile '%s'\n" "$PWD/$CARD" "$PWD/$BODY" > "work/${BASE}-list.txt"
  ffmpeg -y -v warning -stats -f concat -safe 0 -i "work/${BASE}-list.txt" \
    -c:v "$V_CODEC" -preset "$V_PRESET" -crf "$V_CRF" \
    -profile:v "$V_PROFILE" -pix_fmt "$PIX_FMT" \
    -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2 \
    -movflags +faststart "$MAIN"
elif [[ -n "$HOOK_OVERLAY" ]]; then
  # Image de hook en surimpression sur les premières secondes, texte par-dessus.
  ffmpeg -y -v warning -stats -ss "$START" -t "$DUR" -i "$SRC" -i "$HOOK_BG" \
    -filter_complex "[0:v]${VF}[v];\
[1:v]scale=${OUT_W}:${OUT_H}:force_original_aspect_ratio=increase,\
crop=${OUT_W}:${OUT_H},setsar=1[bg];\
[v][bg]overlay=0:0:enable='lt(t,${HOOK_DUR})'[ov];\
[ov]${HOOK_TEXT_CHAIN:+${HOOK_TEXT_CHAIN#,}}${HOOK_TEXT_CHAIN:-null}[vout]" \
    -map "[vout]" -map 0:a:0 \
    -c:v "$V_CODEC" -preset "$V_PRESET" -crf "$V_CRF" \
    -profile:v "$V_PROFILE" -pix_fmt "$PIX_FMT" \
    -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2 \
    -movflags +faststart "$MAIN"
else
  ffmpeg -y -v warning -stats -ss "$START" -t "$DUR" -i "$SRC" \
    -vf "$VF" \
    -c:v "$V_CODEC" -preset "$V_PRESET" -crf "$V_CRF" \
    -profile:v "$V_PROFILE" -pix_fmt "$PIX_FMT" \
    -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2 \
    -movflags +faststart "$MAIN"
fi

# --- Visuel de fin ---
if [[ -n "$OUTRO" ]]; then
  echo "Visuel de fin (${OUTRO_DUR}s) -> $OUT"
  OUTRO_SEG="work/${BASE}-outro.mp4"
  OUTRO_VF="scale=${OUT_W}:${OUT_H}:force_original_aspect_ratio=increase,crop=${OUT_W}:${OUT_H},setsar=1,fps=${FPS}"
  if [[ -n "$OUTRO_TEXT" ]]; then
    rm -f "work/${BASE}-outrotxt"-*.txt
    ON=$(HOOK_MAX_CHARS="$HOOK_MAX_CHARS" python3 scripts/wrap_hook.py "$OUTRO_TEXT" "work/${BASE}-outrotxt")
    OY=$(( (OUT_H - (ON * LINE_H - HOOK_LINE_SPACING)) / 2 ))
    for ((i = 0; i < ON; i++)); do
      OUTRO_VF+=",drawtext=expansion=none:fontfile='${HOOK_FONT}':textfile='work/${BASE}-outrotxt-${i}.txt'"
      OUTRO_VF+=":fontcolor=${BLANC}:fontsize=${HOOK_FONTSIZE}:x=(w-text_w)/2:y=$((OY + i * LINE_H))"
    done
  fi
  ffmpeg -y -v warning -stats -loop 1 -t "$OUTRO_DUR" -i "$OUTRO" \
    -f lavfi -t "$OUTRO_DUR" -i "anullsrc=channel_layout=stereo:sample_rate=${A_RATE}" \
    -vf "$OUTRO_VF" \
    -c:v "$V_CODEC" -preset "$V_PRESET" -crf "$V_CRF" \
    -profile:v "$V_PROFILE" -pix_fmt "$PIX_FMT" \
    -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2 -shortest "$OUTRO_SEG"

  printf "file '%s'\nfile '%s'\n" "$PWD/$MAIN" "$PWD/$OUTRO_SEG" > "work/${BASE}-outrolist.txt"
  ffmpeg -y -v warning -stats -f concat -safe 0 -i "work/${BASE}-outrolist.txt" \
    -c:v "$V_CODEC" -preset "$V_PRESET" -crf "$V_CRF" \
    -profile:v "$V_PROFILE" -pix_fmt "$PIX_FMT" \
    -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2 \
    -movflags +faststart "$OUT"
fi

echo "--- Résultat ---"
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height \
  -of default=noprint_wrappers=1 "$OUT"
