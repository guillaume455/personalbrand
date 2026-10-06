#!/bin/bash
# Reel mix: voice montage + sound effects + music (fresh.mp3 from its main drop), ducked, -14 LUFS (social).
set -euo pipefail; cd "$(dirname "$0")"
TOTAL=58.23; MUS_START=${MUS_START:-17.24}; MUS_GAIN=${MUS_GAIN:-0.30}
SFX=../.claude/skills/media-use/audio/assets/sfx
python3 - <<'PY' > /tmp/claude-0/sfxargs.txt
import json; ev=json.load(open("assets/audio/sfx-events.json"))
print(len(ev))
PY
ARGS=(); G=""; L=""; i=3
while read -r name at vol; do ARGS+=(-i "$SFX/$name.mp3"); d=$(python3 -c "print(int($at*1000))"); G+="[$i]volume=$vol,adelay=$d|$d,aformat=channel_layouts=stereo[e$i];"; L+="[e$i]"; i=$((i+1)); done < <(python3 -c "
import json
for n,a,v in json.load(open('assets/audio/sfx-events.json')): print(n,a,v)")
N=$((i-3))
ffmpeg -v error -y -i assets/audio/voix-montage.wav -i assets/music/fresh.mp3 -i assets/audio/voix-montage.wav "${ARGS[@]}" -filter_complex "
[0]aformat=channel_layouts=stereo,apad=whole_dur=$TOTAL[vo];
${G}[vo]${L}amix=inputs=$((N+1)):normalize=0:duration=first[fg];
[1]atrim=$MUS_START:$(python3 -c "print($MUS_START+$TOTAL)"),asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st=$(python3 -c "print($TOTAL-2.5)"):d=2.5,volume=$MUS_GAIN,aformat=channel_layouts=stereo[m];
[2]aformat=channel_layouts=stereo,apad=whole_dur=$TOTAL[key];
[m][key]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=300[duck];
[fg][duck]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100,alimiter=limit=0.84:level=false[out]" \
  -map "[out]" -t $TOTAL -ar 44100 assets/audio/mix.wav
echo "mix: assets/audio/mix.wav ($N sfx)"
