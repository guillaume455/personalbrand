#!/usr/bin/env python3
"""Cut every shot of shots.py into assets/clips/<id>.mp4: vertical 1080x1920, 30 fps, slightly desaturated (so the
orange overlays stand out), optional punch-in (zoom, cx, cy) and plate blur that follows linear keyframes
(blur: [(t, x, y) ...] in relative frame coordinates, box bw x bh). HDR rushes are tone-mapped to SDR BT.709. Clips are 6 s long (or up to the end of the rush);
build.py trims each one to its slot."""
import os, subprocess, sys
from shots import SHOTS, RUSHES

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("assets/clips", exist_ok=True)
W, H, LEN = 1080, 1920, 6.0


def lerp(keys, i):
    """ffmpeg expression of a piecewise-linear keyframe track (component i) over t"""
    e = f"{keys[-1][i]}"
    for (t0, *a), (t1, *b) in reversed(list(zip(keys, keys[1:]))):
        e = f"if(lt(t,{t1}),{a[i - 1]}+({b[i - 1]}-{a[i - 1]})*(t-{t0})/{t1 - t0},{e})"
    return e


only = sys.argv[1:]
for scene, lst in SHOTS.items():
    for shot in lst:
        cid, src, t0 = shot[:3]
        o = shot[3] if len(shot) > 3 else {}
        if only and cid not in only:
            continue
        z = o.get("zoom", 1)
        trc = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer",
                              "-of", "csv=p=0", f"{RUSHES}/{src}.mp4"], capture_output=True, text=True).stdout.strip()
        f = "[0:v]"
        if trc in ("smpte2084", "arib-std-b67"):
            # HDR rush (phone HDR10/HLG): tone-map to SDR BT.709, or HyperFrames renders the whole reel in HDR
            f += ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
                  "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=gamma=1.12:brightness=0.02,")
        if z != 1:
            f += f"crop=iw/{z}:ih/{z}:(iw-iw/{z})*{o.get('cx', .5)}:(ih-ih/{z})*{o.get('cy', .5)},"
        f += f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps=30,eq=saturation=0.72:contrast=1.04"
        if "blur" in o:
            k = o["blur"]; bw, bh = int(W * o["bw"]) // 2 * 2, int(H * o["bh"]) // 2 * 2
            x, y = f"({lerp(k, 1)})*{W}-{bw}/2", f"({lerp(k, 2)})*{H}-{bh}/2"
            f += (f",split[a][b];[b]crop=w={bw}:h={bh}:x='max(0,min({W}-{bw},{x}))':y='max(0,min({H}-{bh},{y}))',boxblur=24:3[p];"
                  f"[a][p]overlay=x='max(0,min({W}-{bw},{x}))':y='max(0,min({H}-{bh},{y}))'")
        f += "[v]"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(t0), "-t", str(LEN), "-i", f"{RUSHES}/{src}.mp4",
                        "-filter_complex", f, "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                        "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", f"assets/clips/{cid}.mp4"], check=True)
        print(cid, end=" ", flush=True)
print()
