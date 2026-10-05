#!/bin/bash
# Final delivery of the VSL: speed-up of the rendered film (picture + voice + sound effects, pitch kept),
# then the music (assets/music/fresh.mp3, Pixabay) mounted on the FINAL timeline, ducked under the voice,
# loudness -16 LUFS / -1.5 dBTP.
# Usage: bash vsl-diagnostic/build-final.sh [renders/video-hq.mp4] [renders/vsl-diagnostic.mp4]
set -euo pipefail
cd "$(dirname "$0")"
IN="${1:-renders/video-hq.mp4}"; OUT="${2:-renders/vsl-diagnostic.mp4}"
SPEED="${SPEED:-1.08}"
MUSIC="${MUSIC:-assets/music/fresh.mp3}"
SFX=../.claude/skills/media-use/audio/assets/sfx
TMP=$(mktemp -d)
# film times after the speed-up (voice silences of the montage / SPEED)
PIVOT=$(python3 -c "print(round(22.83/$SPEED,3))")     # the draft sheet is black: music cut
DROP=$(python3 -c "print(round(27.57/$SPEED,3))")      # « Un plan fait par quelqu'un… »: the drop
DUR=$(python3 -c "print(round(56.8/$SPEED,3))")
A_START=51.49      # track: a section that starts on a drop, energetic from the first image
B_START=17.24      # track: the main drop (biggest low-end jump of the track)
A_GAIN=0.27; B_GAIN=0.36   # part A about 2.5 dB under part B
LEN_A=$PIVOT; LEN_B=$(python3 -c "print(round($DUR-$DROP,3))")
GAP=$(python3 -c "print(round($DROP-$PIVOT,3))")
RISER_AT=$(python3 -c "print(round($PIVOT-3.5,3))")

# 1. picture + voice/sfx sped up
ffmpeg -v error -y -i "$IN" -filter_complex "[0:v]setpts=PTS/$SPEED,fps=30[v];[0:a]atempo=$SPEED,aresample=48000[a]" \
  -map "[v]" -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p "$TMP/v.mp4" -map "[a]" -c:a pcm_s16le "$TMP/vo.wav"

# 2. music bed on the final timeline, ducked by the voice, then loudness
ffmpeg -v error -y -i "$MUSIC" -i "$TMP/vo.wav" -i "$SFX/riser.mp3" -i "$SFX/impact-bass-1.mp3" -filter_complex "
[0:a]atrim=$A_START:$(python3 -c "print($A_START+$LEN_A)"),asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st=$(python3 -c "print($LEN_A-0.12)"):d=0.12,volume=$A_GAIN,aresample=48000,aformat=channel_layouts=stereo[a];
anullsrc=r=48000:cl=stereo,atrim=0:$GAP[g];
[0:a]atrim=$B_START:$(python3 -c "print($B_START+$LEN_B)"),asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=$(python3 -c "print($LEN_B-3)"):d=3,volume=$B_GAIN,aresample=48000,aformat=channel_layouts=stereo[b];
[a][g][b]concat=n=3:v=0:a=1[mus];
[2:a]atrim=6.5:10,asetpts=PTS-STARTPTS,volume=0.22,adelay=$(python3 -c "print(int($RISER_AT*1000))")|$(python3 -c "print(int($RISER_AT*1000))"),afade=t=out:st=$PIVOT:d=0.05,aresample=48000,aformat=channel_layouts=stereo[ris];
[3:a]volume=0.35,adelay=$(python3 -c "print(int($PIVOT*1000))")|$(python3 -c "print(int($PIVOT*1000))"),aresample=48000,aformat=channel_layouts=stereo[imp];
[mus][ris][imp]amix=inputs=3:normalize=0:duration=first[bed];
[1:a]aformat=channel_layouts=stereo,asplit=2[vo][key];
[bed][key]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=300:makeup=1[duck];
[vo][duck]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,alimiter=limit=0.82:level=false[out]" \
  -map "[out]" -t "$DUR" -c:a pcm_s16le "$TMP/mix.wav"

# 3. mux
ffmpeg -v error -y -i "$TMP/v.mp4" -i "$TMP/mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
rm -rf "$TMP"
echo "final: $OUT ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT") s; pivot $PIVOT, drop $DROP)"
