# Briefs visuels — page de garde et visuel de fin

Prompts destinés à un générateur d'images (Midjourney, Flux, GPT Image, Firefly).

## Règle de base

L'IA génère **le fond uniquement**, jamais le texte. Deux raisons :

1. les générateurs déforment la typographie, surtout les accents français ;
2. le texte incrusté par `make-clip.sh` est rigoureusement identique d'un clip
   à l'autre — c'est ce qui fait la signature de série.

Le fond doit donc réserver une **zone calme au centre** (là où le texte se pose)
et concentrer l'intérêt visuel en haut et en bas du cadre.

## Spécifications de livraison

| | |
|---|---|
| Ratio | 9:16 strict |
| Définition | 1080×1920 minimum (plus grand accepté, je recadre) |
| Format | PNG ou JPG qualité maximale |
| Où | `assets/hook-bg.png` et `assets/outro-bg.png` |

Zone à garder lisible : une bande centrale d'environ 1080×600 px, sans détail
contrasté ni texture agitée.

---

## 1. Page de garde — direction A : matière (recommandée)

La plus polyvalente : elle fonctionne pour les six clips sans se répéter à l'écran,
et ne date pas.

```
Vertical 9:16 cinematic still. Extreme close-up of brushed dark metal meeting
matte black leather, shot in very low key light. Near-black background, deep
charcoal tones. A single thin warm gold light streak rakes across the bottom
edge of the frame, catching the texture. Large uncluttered negative space
across the entire centre of the image — smooth, unlit, no detail there.
Visual interest concentrated only at the top and bottom edges. Directional key
light from the left, deep shadow falloff, fine film grain. Restrained editorial
luxury aesthetic, masculine, expensive, understated. No text, no letters, no
logo, no people, no faces, no visible car. 85mm lens, shallow depth of field.
```

Paramètres : Midjourney `--ar 9:16 --style raw --stylize 150` · GPT Image
« format portrait 1024×1792 » · Flux ratio 9:16.

## 2. Page de garde — direction B : carrosserie

Plus explicitement automobile. À réserver si tu veux que le sujet se lise
immédiatement.

```
Vertical 9:16 cinematic still. Extreme macro of a dark car body panel curve,
deep black paint with a soft satin finish. One warm gold reflection line traces
the panel edge along the lower portion of the frame. The upper and central
areas fall into near-black shadow with generous empty space. Studio lighting,
single large softbox, no environment visible, no reflections of people.
Moody, premium, restrained. Fine film grain. No text, no letters, no logo,
no badge, no brand marking, no wheels, no headlights.
```

Attention : exiger explicitement l'absence de badge ou de marque, sinon le
générateur ajoute des logos automobiles inventés.

## 3. Page de garde — direction C : espace

Plus « autorité » que « automobile ». Intéressant si tu veux t'éloigner du
registre produit.

```
Vertical 9:16 cinematic still. Empty dark industrial space, polished concrete
floor, bare walls receding into black. A single shaft of warm low-angle light
enters from the left and grazes the floor at the bottom of the frame. The
centre and upper area are deep shadow, almost pure black, completely empty.
Architectural, silent, monumental. Fine film grain, no haze machine look.
No text, no people, no furniture, no vehicles, no signage.
```

---

## 4. Visuel de fin

Plus sobre que la page de garde : c'est une respiration, pas une accroche.
Il doit se lire comme la même famille visuelle, en plus fermé.

```
Vertical 9:16 abstract background. Almost entirely deep near-black, matte,
with a very subtle dark texture like fine brushed metal catching almost no
light. One faint warm gold glow bleeding softly from the bottom edge, barely
visible. Completely empty and calm across the centre and upper two-thirds.
Minimal, quiet, expensive, like the closing frame of a film. Fine grain.
No text, no letters, no logo, no objects, no people.
```

Volontairement plus vide que la page de garde : le nom incrusté doit y être
l'unique point d'attention.

---

## Intégration

```bash
bash scripts/make-clip.sh \
  --src "rushes/…" --start … --end … \
  --hook "…" --hook-bg assets/hook-bg.png \
  --outro assets/outro-bg.png --outro-text "Guillaume Herbin" \
  --out exports/0X-….mp4
```

Réglages associés dans `scripts/lib.sh` : `OUTRO_DUR_DEFAULT` (2,5 s),
`HOOK_FONTSIZE`, `HOOK_RULE_*` pour le trait doré.

## Si un fond passe mal à l'écran

Le texte blanc doit rester lisible. Deux correctifs possibles sans regénérer :
assombrir le fond sous le texte, ou réduire son contraste. Les deux se règlent
au montage — signaler le clip concerné plutôt que relancer le générateur.
