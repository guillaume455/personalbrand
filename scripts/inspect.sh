#!/usr/bin/env bash
# Inspection d'un rush : durée, résolution, codecs, débit.
set -euo pipefail
SRC="$1"
echo "=== $(basename "$SRC") ==="
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels \
  -of default=noprint_wrappers=1 "$SRC"
