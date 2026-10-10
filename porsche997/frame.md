---
version: 2
name: "Guillaume Herbin : reel « L'annonce que personne ne voulait » (Porsche 997)"
description: >
  Vertical reel 1080×1920 (Instagram), about 80 s, voice-over by Guillaume, no facecam. Motion design on a dark ground
  #0A0A0A punctuated by five real photos of the car (June 2014, 90 % desaturated, slow 3 to 5 % zoom). ONE accent
  orange #FB8000, white text, red #E03131 only for the warning pills. Oswald bold caps, an orange stroke drawn under
  each title in 6 frames. Subtitles at the bottom (12 % from the bottom), key word in orange. Max 5 words per text.
unit: 1080×1920
principle: readable without sound · one thing to look at · short texts · the voice cues every reveal · safe zones of the apps

safe-zones:
  top: "y 0 to 220 carries nothing important (app header)"
  bottom: "y 1560 to 1920 carries nothing (caption, account name, music line)"
  right: "x 940 to 1080 below y 900 carries nothing (like / comment / share buttons)"
  title-zone: "y 260 to 640, centred, side margins 80 px"
  visual-zone: "y 560 to 1220"
  subtitle-band: "y 1560 to 1700 (bottom of the text at y 1690, 12 % from the bottom), nothing else in it"

colors:
  ground: "#0A0A0A"
  ground-2: "#141414"
  card: "#161616"
  card-light: "#ffffff"
  ink: "#ffffff"
  ink-soft: "#bdbdbd"
  ink-mute: "#6f6f6f"
  ink-dark: "#111111"
  accent: "#FB8000"
  accent-deep: "#d96c00"
  accent-glow: "#ffb466"
  alert: "#E03131"         # warning pills only
  dead: "#3a3a3a"          # greyed-out phone numbers, the dying curve after its peak

fonts:
  Oswald: { files: ["assets/fonts/Oswald-var.woff2 (200-700, variable, latin, OFL)"] }

typography:
  title:     { fontFamily: "Oswald", px: 104, weight: 700, upper: true, lineHeight: 1.12, note: "centred, white, the orange stroke drawn under the last line in 6 frames; one family for the whole film" }
  jumbo:     { fontFamily: "Oswald", px: 230, weight: 700, upper: true, lineHeight: 1, note: "the big numbers (0, 44 000 €, + 6 550 €, 57 000 €), cash-register counters" }
  subtitle:  { fontFamily: "Oswald", px: 58, weight: 500, lineHeight: 70, note: "bottom of the text at 12 % of the height from the bottom (y 1690), white, soft shadow, no band; chunks of 2 to 5 words, 42 characters max; the key word turns orange" }
  ui:        { fontFamily: "Oswald", px: 40, weight: 600, note: "warning pills (red #E03131), labels" }
  handle:    { fontFamily: "Oswald", px: 72, weight: 700, note: "« @guillaumeherbin_ » in orange" }

components:
  ground:
    background: "solid #0A0A0A + one soft radial accent halo (10-16 %, blur 120px+) behind the focal element + static grain 4 %. Full-duration class=\"clip\" layer."
  title-stroke:
    look: "an orange stroke under the title: 14 px tall, round caps, slight upward tilt (-1.5°), tapered end, width = title width + 20 px"
    motion: "the title slams in (scale 1.25 → 1, blur 10 → 0, 0.18 s expo.out), then the stroke draws from the left (scaleX 0 → 1, 0.3 s power3.out)"
  word-by-word:
    rule: "each subtitle word appears on its cue: fromTo {opacity:0, y:14, blur 6px} → {opacity:1, y:0, blur 0} in 0.12 s, immediateRender:false. The key word [orange : …] turns #FB8000 as it appears. A chunk leaves in 0.1 s (opacity + blur) before the next one."
  phone:
    description: "a flat smartphone icon drawn in white line (rounded rect 220×420, 10 px stroke, speaker slot, home bar), centred; the strike = an accent stroke 22 px drawn diagonally across it (svg path draw 0.25 s)"
  number-list:
    description: "a column of 7 French mobile numbers in Space Mono 44 px white (« 06 12 48 ·· ·· », digits partly masked with ··), each line greys out to #3a3a3a with a thin strike in order, 0.18 s apart"
  curve:
    description: "a line chart in the visual zone: x axis 2010 → 2026 (Space Mono 30 ink-mute), the line in white 10 px drawn left to right and falling; the start label « 2010 : 9 RDV SUR 10 APPELS » near the top-left of the curve, the end label « 2026 : 3 » with the 3 in accent; the end point an accent dot"
  listing-tile:
    description: "a small leboncoin-like car listing tile (white card 300×380, radius 18, photo top from assets/img/thumb-audi.png or thumb-ford.png, title line and green price #1d6b43), used in a growing mosaic; tiles are identical copies"
  card:
    description: "a solution card: dark card #161616, radius 36, 1px #2a2a2a border, 860×1000, number badge (accent circle 96 px with « 1 », « 2 », « 3 » in Big Shoulders), the card title in Big Shoulders 900 96 px caps with its orange stroke, and an illustration area. Cards stack: each new card slides up from the bottom over the previous one, which scales to 0.94 and darkens."
  feed:
    description: "a vertical social feed inside card 1: posts (photo tile + 2 grey text bars) scrolling up; post photos from assets/img/thumb-audi.png and thumb-ford.png; a views counter « VUES » in Space Mono that rolls up (1 240 → 18 600)"
  stars:
    description: "five stars in accent that fill one by one (0.12 s apart) + review bubbles (white rounded cards with 5 small stars and 2 grey bars, NO readable invented quote) stacking"
  shopfront:
    description: "a flat shopfront: dark facade, a large window that lights up (warm accent glow), a sign bar WITHOUT any brand name; then a minimalist map tile (dark map, a few grey roads) with an accent pin that drops on its spot"
  wall:
    description: "a wall built brick by brick from the bottom (bricks 160×70, #1f1f1f with 2px #2c2c2c joints), the last brick in accent"
  day-counter:
    description: "a mono counter « JOUR 1 », « JOUR 2 »… rolling fast under the title (Space Mono 56 accent), like a meter that never stops"

negative:
  - "Never more than 6 words in one text block. Nothing in the safe zones."
  - "One accent only (#FB8000), except the green price inside the listing tiles."
  - "No invented testimonials, no fake review text, no brand names on the shopfront, no real phone numbers (digits masked)."
  - "No bouncy/elastic eases, no repeat:-1, no CSS animation, no Math.random."
  - "No visible text that the Scene lines do not quote."
---

# Reel « Le téléphone, c'est fini »

Dark ground, orange accent, white type. Every scene opens on its title in heavy capitals with the orange stroke
drawn under it, then the visual plays the sentence of the voice. The voice runs as short subtitles in the
lower-middle band, the key word of each sentence in orange. Scene changes are hard cuts on the voice (a reel
rhythm); inside a scene the camera keeps moving.
