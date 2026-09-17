#!/usr/bin/env bash
# Ramène un master au débit que la destination conserve réellement.
#
# Le pipeline encode en CRF 18, quasiment sans perte : utile pour archiver,
# absurde pour publier. Instagram ré-encode tout ce qu'il reçoit autour de
# 3 à 5 Mb/s, et la limite de transfert de la session est de 30 Mo.
#
#   bash pour-publication.sh exports/09-mon-clip.mp4        # vise 28 Mo
#   CIBLE_MO=60 bash pour-publication.sh exports/09-mon-clip.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/lib.sh
CIBLE_MO=${CIBLE_MO:-28}

for SRC in "$@"; do
  OUT="${SRC%.*}-web.mp4"
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC")
  VB=$(awk -v m="$CIBLE_MO" -v d="$DUR" 'BEGIN{printf "%d", (m*8192)/d - 192}')
  echo "== $(basename "$SRC") — ${DUR}s -> ${VB} kb/s"
  ffmpeg -y -v error -i "$SRC" -c:v "$V_CODEC" -b:v "${VB}k" -preset "$V_PRESET" \
    -pass 1 -an -f null /dev/null
  ffmpeg -y -v error -i "$SRC" -c:v "$V_CODEC" -b:v "${VB}k" -preset "$V_PRESET" \
    -pass 2 -profile:v "$V_PROFILE" -pix_fmt "$PIX_FMT" \
    -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2 \
    -movflags +faststart "$OUT"
  rm -f ffmpeg2pass-*.log*
  echo "   -> $(du -h "$OUT" | cut -f1)"
done
