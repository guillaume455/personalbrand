#!/usr/bin/env bash
# À LANCER SUR TA MACHINE, pas dans la session Claude.
#
# Ramène une vidéo sous la limite de 25 Mo de l'interface web de GitHub,
# en 1080x1920. Aucune perte visible : Instagram ré-encode de toute façon
# tout ce qu'on lui envoie autour de 3 à 5 Mb/s.
#
#   bash compresser-avant-envoi.sh 20260916_163152.mp4
#   bash compresser-avant-envoi.sh *.mp4          # les cinq d'un coup
#
# Le fichier d'origine n'est jamais modifié : la sortie s'appelle
# <nom>-web.mp4, à côté.
set -euo pipefail
CIBLE_MO=${CIBLE_MO:-22}          # marge sous les 25 Mo de GitHub

command -v ffmpeg >/dev/null || { echo "ffmpeg n'est pas installé." >&2; exit 1; }

for SRC in "$@"; do
  [[ -f "$SRC" ]] || { echo "Introuvable : $SRC" >&2; continue; }
  OUT="${SRC%.*}-web.mp4"
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC")
  # Budget vidéo = taille cible convertie en kb/s, moins la piste audio.
  VB=$(awk -v m="$CIBLE_MO" -v d="$DUR" 'BEGIN{printf "%d", (m*8192)/d - 128}')
  # Portrait -> largeur 1080 ; paysage -> hauteur 1080. Les deux tiennent
  # dans 1920 sur le grand côté.
  VF="scale=w='if(gt(iw,ih),-2,1080)':h='if(gt(iw,ih),1080,-2)':flags=lanczos"

  echo "== $SRC (${DUR}s) -> ${VB} kb/s"
  ffmpeg -y -v error -i "$SRC" -vf "$VF" -c:v libx264 -b:v "${VB}k" \
    -preset slow -pass 1 -an -f null /dev/null
  ffmpeg -y -v error -stats -i "$SRC" -vf "$VF" -c:v libx264 -b:v "${VB}k" \
    -preset slow -pass 2 -profile:v high -pix_fmt yuv420p \
    -c:a aac -b:a 128k -ar 48000 -ac 2 -movflags +faststart "$OUT"
  rm -f ffmpeg2pass-*.log*
  echo "   -> $(du -h "$OUT" | cut -f1)"
done
