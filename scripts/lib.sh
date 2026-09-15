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
# Orange de la charte, relevé directement sur les covers (valeur dominante
# mesurée : rgb(252,126,21)). Référence commune aux clips et aux carrousels.
ACCENT="0xFC7E15"
DORE="$ACCENT"             # ancien nom, conservé pour compatibilité
BLANC="0xFFFFFF"

# --- Hook (carton d'ouverture) ---
# Les covers fournies portent déjà leur texte : ces réglages ne servent que
# de secours, pour un clip dont la cover manquerait.
HOOK_DUR=3
HOOK_FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
HOOK_FONTSIZE=70
HOOK_LINE_SPACING=22
HOOK_MAX_CHARS=20          # largeur de wrap, en caractères
HOOK_RULE_W=180            # trait d'accent : largeur
HOOK_RULE_H=6              # trait d'accent : épaisseur
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
