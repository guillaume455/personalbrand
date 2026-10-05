#!/bin/bash
# Voice montage + final mix for « Cette vidéo ».
# No cut inside the voice (its pauses already breathe); 30 ms fade on the last word, tail hold to 44.6 s for the end card.
set -e
cd "$(dirname "$0")/assets/audio"
RAW=voix-A-cette-video.mp3
S="${SFX_DIR:?Set SFX_DIR to a folder of sound effects (pop.wav, click.wav, whoosh.wav...), see examples/README.md}"
M="${MUSIC:?Set MUSIC to a CC0 music file, see examples/README.md}"
ffmpeg -v error -y -i "$RAW" -filter_complex "\
[0]afade=t=out:st=40.56:d=0.03[a];anullsrc=r=44100:cl=mono,atrim=0:4.01[g];\
[a][g]concat=n=2:v=0:a=1,atrim=0:44.6[out]" -map "[out]" -ar 44100 -ac 1 voix-A-montage.wav
python3 - "$S" "$M" <<'EOF'
import sys, subprocess, json
S, M = sys.argv[1], sys.argv[2]
ev = json.load(open("sfx-events.json"))
args=["ffmpeg","-v","error","-y","-i","voix-A-montage.wav","-i",M]
for n,_,_ in ev: args+=["-i",f"{S}/{n}.wav"]
fc=["[0]aformat=sample_rates=44100:channel_layouts=stereo[v]",
    "[1]atrim=0:44.6,asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo,afade=t=in:d=0.8,afade=t=out:st=41.6:d=3,volume=0.12[m]"]
lab=["[v]","[m]"]
for i,(n,t,vol) in enumerate(ev):
    d=int(t*1000); fc.append(f"[{i+2}]aformat=sample_rates=44100:channel_layouts=stereo,volume={vol},adelay={d}|{d}[e{i}]"); lab.append(f"[e{i}]")
fc.append("".join(lab)+f"amix=inputs={len(lab)}:normalize=0:duration=first,alimiter=limit=0.95[out]")
subprocess.run(args+["-filter_complex",";".join(fc),"-map","[out]","-t","44.6","mix-A.wav"],check=True)
print("mix A ok")
EOF
