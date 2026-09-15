#!/usr/bin/env bash
# Charte visuelle et specs techniques communes aux 6 clips.
# Toute modification ici s'applique à l'ensemble des exports.

# --- Format de sortie (Instagram Reels / LinkedIn) ---
OUT_W=1080
OUT_H=1920
V_CODEC="libx264"
V_CRF=18
V_PRESET="slow"
V_PROFILE="high"
PIX_FMT="yuv420p"
A_CODEC="aac"
A_BITRATE="192k"
A_RATE=48000
FPS=30

# --- Signature visuelle ---
NOIR_PROFOND="0x0A0A0A"
DORE="0xC9A84C"
BLANC="0xFFFFFF"

# --- Hook (carton d'ouverture) ---
HOOK_DUR=3
# Georgia n'est pas disponible sous Linux. DejaVu Serif est la serif la plus
# proche en graisse et en chasse ; Liberation Serif est l'alternative
# (métriquement compatible Times New Roman, donc plus fine).
HOOK_FONT="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
HOOK_FONTSIZE=70
HOOK_LINE_SPACING=22
HOOK_MAX_CHARS=20          # largeur de wrap, en caractères
HOOK_RULE_W=180            # trait doré : largeur
HOOK_RULE_H=3              # trait doré : épaisseur
HOOK_RULE_GAP=72           # espace entre le bas du texte et le trait

# --- Sous-titres incrustés ---
SUB_FONT="DejaVu Sans"
SUB_FONTSIZE=62
SUB_OUTLINE=3              # fine bordure noire
SUB_SHADOW=0
SUB_MARGIN_V=300           # remonte les sous-titres dans le tiers bas
SUB_MAX_CHARS=27           # largeur d'une ligne de sous-titre (2 lignes max par cue)

# --- Recadrage vertical ---
# Les rushes sont en 16:9. On découpe une fenêtre 9:16 pleine hauteur.
# CROP_BIAS décale la fenêtre horizontalement : 0 = centré,
# négatif = vers la gauche, positif = vers la droite (en pixels source).
CROP_BIAS_DEFAULT=0

# --- Visuel de fin ---
OUTRO_DUR_DEFAULT=2.5       # durée d'affichage du carton de fin, en secondes
