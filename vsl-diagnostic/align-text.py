#!/usr/bin/env python3
"""Word timings without Whisper (model hosts are blocked from this environment).

The voice reads the validated text exactly, and silence detection splits it into 35 phrases (onsets.py --no-whisper).
Each phrase below is mapped by hand to its words; inside a phrase, words are spread by syllable weight.
onsets.py --transcript then snaps every word start onto the real sound onsets.
Usage: python3 align-text.py   (writes assets/audio/voix-montage-mots.json)
"""
import json, re, subprocess

WAV = "assets/audio/voix-montage.wav"
PHRASES = [
    "Tu veux vivre de l'automobile.", "Alors tu te dis :", "j'essaie.",
    "Essayer un modèle...", "ça coûte des mois.", "Essayer une voiture...", "ça coûte ta marge.",
    "Essayer encore...", "ça coûte ton épargne.",
    "Le problème, ce n'est pas de te lancer.", "C'est de te lancer sans plan.",
    "Sans savoir quel modèle te correspond.", "Combien il te faut.", "Combien tu dois vendre.",
    "Et si", "tu essayais...", "avec un plan ?",
    "Un plan fait par quelqu'un qui", "connaît le métier.",
    "Je m'appelle Guillaume Herbin.", "Je me suis lancé à vingt et un ans,", "avec trois mille euros en poche.",
    "Pas de formation.", "Pas d'expérience.", "J'ai appris en me trompant, pendant seize ans.",
    "Toi,", "tu peux commencer avec un plan.",
    "On part de ta situation.", "On tranche le modèle.", "On pose les vrais chiffres.",
    "Moins de casse.", "Moins de temps perdu.",
    "Tu n'as pas besoin de tout savoir.", "Juste", "ta prochaine étape.",
]

out = subprocess.run(["python3", "../.claude/skills/motion-design/scripts/onsets.py", WAV, "--no-whisper"],
                     capture_output=True, text=True, check=True).stdout
spans = [(float(a), float(b)) for a, b in re.findall(r"^#\d+\s+([\d.]+) to\s+([\d.]+)", out, re.M)]
assert len(spans) == len(PHRASES), f"{len(spans)} phrases detected, {len(PHRASES)} mapped"

def syll(w):
    return max(1, len(re.findall(r"[aeiouyàâéèêëîïôûùü]+", w.lower().rstrip("e"))))

words = []
for (a, b), text in zip(spans, PHRASES):
    toks = [t for t in text.split() if re.search(r"\w", t)]
    weights = [syll(t) for t in toks]
    t, step = a, (b - a) / sum(weights)
    for tok, wt in zip(toks, weights):
        words.append({"w": tok, "start": round(t, 2), "end": round(t + wt * step, 2)})
        t += wt * step
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", WAV],
                           capture_output=True, text=True, check=True).stdout)
json.dump({"duration": round(dur, 2), "words": words}, open("assets/audio/voix-montage-mots.json", "w"),
          ensure_ascii=False, indent=1)
print(f"{len(words)} mots, {dur:.2f} s")
