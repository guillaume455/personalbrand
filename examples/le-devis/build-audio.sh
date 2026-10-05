#!/bin/bash
# Voice montage + final mix for le-devis.
# Cuts sit in the MIDDLE of the raw voice's silences (never on a word onset), with 5 ms fades on every join.
# Offsets stay +0.8 s after the first cut and +1.2 s after the second, so the frame cues do not move.
set -e
cd "$(dirname "$0")/assets/audio"
RAW="${VOICE:-voix-C-devis.mp3}"   # your ElevenLabs take, dropped in assets/audio/
S="${SFX_DIR:?Set SFX_DIR to a folder of sound effects (pop.wav, click.wav, whoosh.wav...), see examples/README.md}"
M="${MUSIC:?Set MUSIC to a CC0 music file, see examples/README.md}"
C1=14.00   # silence before « Sauf qu'aujourd'hui » (onset 14.05)
C2=34.75   # silence between « de zéro. » (ends 34.44) and « Entrepreneurs » (onset 35.04)
ffmpeg -v error -y -i "$RAW" -filter_complex "\
[0]atrim=0:$C1,asetpts=PTS-STARTPTS,afade=t=out:st=$(echo "$C1-0.005" | bc):d=0.005[a];\
[0]atrim=$C1:$C2,asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st=$(echo "$C2-$C1-0.005" | bc):d=0.005[b];\
[0]atrim=$C2,asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st=$(echo "38.0-$C2" | bc):d=0.03[c];\
anullsrc=r=44100:cl=mono,atrim=0:0.8[g1];anullsrc=r=44100:cl=mono,atrim=0:0.4[g2];anullsrc=r=44100:cl=mono,atrim=0:4.0[g3];\
[a][g1][b][g2][c][g3]concat=n=6:v=0:a=1[out]" -map "[out]" -ar 44100 -ac 1 voix-C-devis-montage.wav
python3 - "$S" "$M" <<'EOF'
import sys, subprocess
S, M = sys.argv[1], sys.argv[2]
ev = [("whoosh-short",t,.16) for t in (5.70,10.90,17.32,20.56,25.94)] + [("whoosh-short",31.88,.1)]
ev += [("pop",14.02,.5),("click",14.04,.35),("whoosh",14.26,.5),("whoosh",36.0,.5),
       ("pop",0.24,.18),("click",1.20,.4),("whoosh-short",1.66,.2),("pop",2.70,.3),("pop",4.72,.28),
       ("error",7.26,.22),("pop",7.76,.38),("click",7.80,.3),("ping",8.94,.16),
       ("key-press",9.68,.25),("key-press",10.04,.25),("key-press",10.40,.25),
       ("pop",12.56,.14),("pop",12.80,.12),("pop",13.04,.12),
       ("pop",16.02,.18),("typing",17.56,.2),("typing",18.56,.16),("click",19.46,.45),("pop",19.70,.26),
       ("click-soft",21.80,.4),("click-soft",23.38,.4),("click-soft",25.26,.4),("click-soft",25.58,.25),
       ("whoosh-short",28.06,.2),("ping",30.92,.2),("ping",35.02,.14),("click",41.35,.45)]
args=["ffmpeg","-v","error","-y","-i","voix-C-devis-montage.wav","-i",M]
for n,_,_ in ev: args+=["-i",f"{S}/{n}.wav"]
fc=["[0]aformat=sample_rates=44100:channel_layouts=stereo[v]",
    "[1]atrim=0:43.2,asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo,afade=t=in:d=0.8,afade=t=out:st=40.2:d=3,volume=0.12[m]"]
lab=["[v]","[m]"]
for i,(n,t,vol) in enumerate(ev):
    d=int(t*1000); fc.append(f"[{i+2}]aformat=sample_rates=44100:channel_layouts=stereo,volume={vol},adelay={d}|{d}[e{i}]"); lab.append(f"[e{i}]")
fc.append("".join(lab)+f"amix=inputs={len(lab)}:normalize=0:duration=first,alimiter=limit=0.95[out]")
subprocess.run(args+["-filter_complex",";".join(fc),"-map","[out]","-t","43.2","mix-C-v4.wav"],check=True)
print("mix v4 ok")
EOF
