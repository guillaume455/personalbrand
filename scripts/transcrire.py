#!/usr/bin/env python3
"""Transcrit un rush en français, découpé sur les pauses réelles de parole.

Aucun modèle n'étant téléchargeable depuis huggingface dans cette session, on
utilise Whisper small au format ONNX, publié en release GitHub par sherpa-onnx.
Le son est normalisé avant reconnaissance : les rushes extérieurs sortent 5 à
11 LU sous la cible et Whisper y perd des mots.
"""
import math, re, subprocess, sys, wave
from pathlib import Path
import numpy as np, sherpa_onnx

M = Path("work/asr/sherpa-onnx-whisper-small")
MAX_CHUNK = 25.0          # Whisper travaille sur une fenêtre de 30 s

def wav16k(src, dst):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ac", "1",
                    "-ar", "16000", "-c:a", "pcm_s16le", str(dst)], check=True)

def segments(wav):
    """Bornes de parole, d'après les silences détectés."""
    out = subprocess.run(["ffmpeg", "-i", str(wav), "-af",
                          "silencedetect=noise=-30dB:d=0.22", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    with wave.open(str(wav)) as w:
        dur = w.getnframes() / w.getframerate()
    speech, cur = [], 0.0
    for s in starts:
        if s > cur + 0.2:
            speech.append([cur, s])
        cur = next((e for e in ends if e > s), dur)
    if dur > cur + 0.2:
        speech.append([cur, dur])
    # Regroupe en morceaux de 25 s au plus.
    chunks = []
    for s, e in speech:
        if chunks and e - chunks[-1][0] <= MAX_CHUNK:
            chunks[-1][1] = e
        else:
            chunks.append([s, e])
    chunks = chunks or [[0.0, dur]]
    # Un passage débité sans pause franche dépasse la fenêtre de Whisper, qui
    # n'en garderait que les 30 premières secondes. On le redécoupe en parts
    # égales : la coupure tombe en plein mot, mais rien n'est perdu.
    taille = []
    for s, e in chunks:
        n = max(1, math.ceil((e - s) / MAX_CHUNK))
        pas = (e - s) / n
        taille += [[s + i * pas, s + (i + 1) * pas] for i in range(n)]
    return taille

def main(paths):
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(M / "small-encoder.int8.onnx"),
        decoder=str(M / "small-decoder.int8.onnx"),
        tokens=str(M / "small-tokens.txt"),
        language="fr", task="transcribe", num_threads=4)
    for p in paths:
        p = Path(p)
        tmp = Path("work/asr/_t.wav")
        wav16k(p, tmp)
        with wave.open(str(tmp)) as w:
            sr = w.getframerate()
            data = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        lines = []
        for s, e in segments(tmp):
            st = rec.create_stream()
            st.accept_waveform(sr, data[int(s * sr):int(e * sr)])
            rec.decode_stream(st)
            txt = st.result.text.strip()
            if txt:
                lines.append(f"[{s:6.2f} -> {e:6.2f}]  {txt}")
        print(f"\n════════ {p.name}")
        print("\n".join(lines))
        Path(f"transcripts/facecam/{p.stem}.txt").write_text("\n".join(lines))

main(sys.argv[1:])
