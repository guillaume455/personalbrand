#!/usr/bin/env bash
# Clip "réaction" : montage commenté d'une vidéo tierce (achat auto en Italie).
# Mise en page en bandeau : bandeau haut = notre angle (il masque aussi le
# titre anglais incrusté dans la source), bandeau bas = sous-titres français.
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/lib.sh

SRC="rushes/scam italy.mp4"
T="work/scam/txt"
SUBS="work/scam/subs.ass"
OUT="exports/07-scam-italie.mp4"
FB="$HOOK_FONT"                 # DejaVu Sans Bold
mkdir -p work/scam exports

# --- Textes de l'habillage (générés ici pour que le script soit autonome) ---
mkdir -p "$T"
write() { printf '%s' "$2" > "$T/$1"; }
write hdr-label.txt "ACHETÉE EN ITALIE · SUR PHOTOS"
write hdr-0.txt     "CE QU'IL A"
write hdr-1.txt     "VRAIMENT REÇU"
write hook-0.txt    "Il a acheté cette"
write hook-1.txt    "voiture en Italie."
write hook-2.txt    "Sur photos."
write c1-0.txt      "Acheter à distance,"
write c1-1.txt      "c'est rentable."
write c1-2.txt      "Acheter sans contrôle,"
write c1-3.txt      "c'est un pari."
cp subs/07-scam-italie.ass "$SUBS"

# --- Géométrie du gabarit ---
HDR_H=500                       # bandeau haut : couvre le titre anglais (src y=228..327)
FTR_Y=1430                      # bandeau bas : accueille les sous-titres FR
HOOK_T=2.6                      # durée du carton d'ouverture, son en dessous

# --- Sélection des rushes (timecodes source) ---
# A 0.0-17.0   : l'achat + "ils ont scotché le voyant moteur"
# B 19.9-25.0  : le voyant allumé, gros plan sur le scotch
# C 29.7-34.7  : "tout était masqué sur les photos de l'annonce"
# 34.7-39.2 écarté : insultes seules, aucune information.
SEL="[0:v]trim=0:17,setpts=PTS-STARTPTS[v0];[0:a]atrim=0:17,asetpts=PTS-STARTPTS[a0];\
[0:v]trim=19.9:25,setpts=PTS-STARTPTS[v1];[0:a]atrim=19.9:25,asetpts=PTS-STARTPTS[a1];\
[0:v]trim=29.7:34.7,setpts=PTS-STARTPTS[v2];[0:a]atrim=29.7:34.7,asetpts=PTS-STARTPTS[a2];\
[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[vc][ac]"

dt() { # fichier fontsize couleur y [enable]
  printf "drawtext=expansion=none:fontfile='%s':textfile='%s':fontcolor=%s:fontsize=%s:x=(w-text_w)/2:y=%s%s" \
    "$FB" "$T/$1" "$3" "$2" "$4" "${5:+:$5}"
}

EN="enable='lt(t,${HOOK_T})'"
CHAIN="[vc]scale=${OUT_W}:${OUT_H}:flags=lanczos,setsar=1,fps=${FPS}"
CHAIN+=",drawbox=x=0:y=0:w=${OUT_W}:h=${HDR_H}:color=${NOIR_PROFOND}@1:t=fill"
CHAIN+=",drawbox=x=0:y=${FTR_Y}:w=${OUT_W}:h=$((OUT_H - FTR_Y)):color=${NOIR_PROFOND}@1:t=fill"
CHAIN+=",$(dt hdr-label.txt 34 "$ACCENT" 92)"
CHAIN+=",$(dt hdr-0.txt 76 "$BLANC" 156)"
CHAIN+=",$(dt hdr-1.txt 76 "$BLANC" 250)"
CHAIN+=",drawbox=x=460:y=382:w=160:h=5:color=${ACCENT}@1:t=fill"
CHAIN+=",ass='${SUBS}'"
# Carton d'ouverture, posé par-dessus le gabarit
CHAIN+=",drawbox=x=0:y=0:w=${OUT_W}:h=${OUT_H}:color=${NOIR_PROFOND}@1:t=fill:${EN}"
CHAIN+=",$(dt hook-0.txt 78 "$BLANC" 757 "$EN")"
CHAIN+=",$(dt hook-1.txt 78 "$BLANC" 861 "$EN")"
CHAIN+=",$(dt hook-2.txt 78 "$BLANC" 965 "$EN")"
CHAIN+=",drawbox=x=450:y=1115:w=180:h=6:color=${ACCENT}@1:t=fill:${EN}"
CHAIN+="[vout]"

enc() { echo -c:v "$V_CODEC" -preset "$V_PRESET" -crf "$V_CRF" -profile:v "$V_PROFILE" \
        -pix_fmt "$PIX_FMT" -c:a "$A_CODEC" -b:a "$A_BITRATE" -ar "$A_RATE" -ac 2; }

echo "== corps =="
ffmpeg -y -v warning -stats -i "$SRC" -filter_complex "${SEL};${CHAIN}" \
  -map '[vout]' -map '[ac]' $(enc) work/scam/body.mp4

echo "== carton leçon =="
CARD="null,$(dt c1-0.txt 64 "$BLANC" 760),$(dt c1-1.txt 64 "$BLANC" 848)"
CARD+=",$(dt c1-2.txt 64 "$ACCENT" 990),$(dt c1-3.txt 64 "$ACCENT" 1078)"
ffmpeg -y -v warning -f lavfi -i "color=c=${NOIR_PROFOND}:s=${OUT_W}x${OUT_H}:r=${FPS}:d=3.2" \
  -f lavfi -i "anullsrc=channel_layout=stereo:sample_rate=${A_RATE}" \
  -vf "$CARD" -t 3.2 $(enc) -shortest work/scam/card1.mp4

echo "== carton abonnement =="
ffmpeg -y -v warning -loop 1 -t 2.5 -i assets/outro-bg.png \
  -f lavfi -t 2.5 -i "anullsrc=channel_layout=stereo:sample_rate=${A_RATE}" \
  -vf "scale=${OUT_W}:${OUT_H}:force_original_aspect_ratio=increase,crop=${OUT_W}:${OUT_H},setsar=1,fps=${FPS}" \
  $(enc) -shortest work/scam/card2.mp4

echo "== assemblage =="
printf "file '%s'\n" "$PWD/work/scam/body.mp4" "$PWD/work/scam/card1.mp4" "$PWD/work/scam/card2.mp4" \
  > work/scam/list.txt
ffmpeg -y -v warning -stats -f concat -safe 0 -i work/scam/list.txt $(enc) \
  -movflags +faststart "$OUT"

echo "--- $OUT ---"
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height \
  -of default=noprint_wrappers=1 "$OUT"
