#!/bin/bash
# Voice montage + final mix for « Traduire ».
# One cut, in the MIDDLE of the silence before « Aujourd'hui » (raw 18.28 → 19.60), +0.6 s of silence for the pivot,
# 5 ms fades on the join; after raw 19.10 every cue is +0.6 s. Tail hold to 50.4 s for the end card.
set -e
cd "$(dirname "$0")/assets/audio"
RAW=voix-B-traduire.mp3
S="${SFX_DIR:?Set SFX_DIR to a folder of sound effects (pop.wav, click.wav, whoosh.wav...), see examples/README.md}"
M="${MUSIC:?Set MUSIC to a CC0 music file, see examples/README.md}"
C1=19.10
ffmpeg -v error -y -i "$RAW" -filter_complex "\
[0]atrim=0:$C1,asetpts=PTS-STARTPTS,afade=t=out:st=$(echo "$C1-0.005" | bc):d=0.005[a];\
[0]atrim=$C1,asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st=$(echo "46.08-$C1" | bc):d=0.025[b];\
anullsrc=r=44100:cl=mono,atrim=0:0.6[g1];anullsrc=r=44100:cl=mono,atrim=0:4.0[g2];\
[a][g1][b][g2]concat=n=4:v=0:a=1,atrim=0:50.4[out]" -map "[out]" -ar 44100 -ac 1 voix-B-montage.wav
python3 - "$S" "$M" <<'EOF'
import sys, subprocess, json
S, M = sys.argv[1], sys.argv[2]
ev = json.load(open("sfx-events.json"))
args=["ffmpeg","-v","error","-y","-i","voix-B-montage.wav","-i",M]
for n,_,_ in ev: args+=["-i",f"{S}/{n}.wav"]
fc=["[0]aformat=sample_rates=44100:channel_layouts=stereo[v]",
    "[1]atrim=0:50.4,asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo,afade=t=in:d=0.8,afade=t=out:st=47.4:d=3,volume='0.12*(1-0.85*clip((t-18.3)/0.25\\,0\\,1)*clip((19.7-t)/0.12\\,0\\,1))':eval=frame[m]"]
lab=["[v]","[m]"]
for i,(n,t,vol) in enumerate(ev):
    d=int(t*1000); fc.append(f"[{i+2}]aformat=sample_rates=44100:channel_layouts=stereo,volume={vol},adelay={d}|{d}[e{i}]"); lab.append(f"[e{i}]")
fc.append("".join(lab)+f"amix=inputs={len(lab)}:normalize=0:duration=first,alimiter=limit=0.95[out]")
subprocess.run(args+["-filter_complex",";".join(fc),"-map","[out]","-t","50.4","mix-B.wav"],check=True)
print("mix B ok")
EOF
