#!/usr/bin/env bash
# Retire le filigrane « CapCut AI » incrusté en haut à gauche.
#
# Relevé sur le rush : boîte de 175 x 41 px à (28, 28), fixe sur toute la durée.
#
# Deux méthodes, la première par défaut :
#   delogo    reconstruit la zone par interpolation depuis les bords de la
#             boîte. L'image entière est conservée. Fonctionne ici parce que
#             ce coin reste du ciel flou ; sur un décor détaillé il laisserait
#             une trace.
#   --recadre écarte le coin et remonte en 1080x1920. Aucun risque d'artefact,
#             mais 19 % de l'image en moins et un agrandissement de 1,24.
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/lib.sh

SRC=""; MODE="delogo"
for a in "$@"; do
  case "$a" in
    --recadre) MODE="recadre";;
    *) SRC="$a";;
  esac
done
[[ -f "$SRC" ]] || { echo "Usage : retirer-filigrane.sh RUSH.mp4 [--recadre]" >&2; exit 1; }
OUT="exports/$(basename "${SRC%.*}")${MODE:+-$MODE}.mp4"
mkdir -p exports

if [[ "$MODE" == "recadre" ]]; then
  # 874x1554 à (206,220) : le coin est écarté, le cadrage reste centré en hauteur.
  VF="crop=874:1554:206:220,scale=${OUT_W}:${OUT_H}:flags=lanczos,setsar=1"
else
  # Boîte élargie de quelques pixels, pour que l'interpolation dispose d'un
  # bord propre tout autour.
  VF="delogo=x=24:y=24:w=184:h=50"
fi

ffmpeg -y -v error -i "$SRC" -vf "$VF" \
  -c:v "$V_CODEC" -preset "$V_PRESET" -crf "$V_CRF" -profile:v "$V_PROFILE" \
  -pix_fmt "$PIX_FMT" -c:a copy -movflags +faststart "$OUT"
echo "--- $OUT ---"
ffprobe -v error -show_entries format=duration,size -show_entries stream=width,height \
  -of default=noprint_wrappers=1 "$OUT"
