---
version: 2
name: Entrepreneurs 2.0, Launch Frame « Le bureau » (C, top-down desk variant)
description: >
  Variant of film C « Le devis » built on patterns/PATTERNS.md, same voice and timings. The whole
  film is seen from ABOVE a real desk, with physical objects: the quote is a sheet of paper, the verdicts are rubber
  stamps, the wait is a tear-off calendar, the pile of invoices buries the desk. Two lights on the same desk: the
  PROBLEM at night under a desk lamp (dark walnut, warm pool of light, deep shadows), the SOLUTION in morning daylight
  (light oak, soft window light). The end card is the dark stage of films A, B and C. One accent only, terracotta:
  the traced pill in the phrase, the pen, the stamp ink.
unit: 1920×1080
principle: readable without sound · tactile, physical, top-down · one accent, one highlight mechanism · the voice cues every reveal

colors:
  desk-night: "#1c1512"        # dark walnut, problem
  desk-night-lamp: "#3b2b21"   # center of the lamp pool
  desk-day: "#e7dccd"          # light oak, solution
  desk-day-light: "#f3ece2"    # window light bands
  paper: "#fbf8f2"             # sheets of paper
  paper-2: "#efe7dc"           # sticky notes, second sheets
  ink: "#f5efe7"               # text on the dark desk
  ink-soft: "#cdbfb2"
  ink-dark: "#1a1612"          # text on paper / light desk
  ink-dark-soft: "#5a5348"
  hairline: "#d9cfc1"
  accent: "#c25b28"            # pen, stamp ink, pill
  accent-light: "#d4703f"
  accent-deep: "#a84d22"
  accent-glow: "#e08a5c"
  object-dark: "#2e2924"       # phone body, laptop body

fonts:
  Instrument Sans: { files: ["assets/fonts/InstrumentSans-400.woff2 (400)", "assets/fonts/InstrumentSans-500.woff2 (500)", "assets/fonts/InstrumentSans-600.woff2 (600)", "assets/fonts/InstrumentSans-700.woff2 (700)"] }
  Space Mono: { files: ["assets/fonts/SpaceMono-400.woff2 (400)", "assets/fonts/SpaceMono-700.woff2 (700)"] }
  Big Shoulders: { files: ["assets/fonts/BigShoulders-800.woff2 (800)"] }

typography:
  phrase:     { fontFamily: "Instrument Sans", px: 54, weight: 600, lineHeight: 1.18, tracking: "-0.02em", note: "the sentence of the voice, small, in a band at the bottom (y 780-870) or at the top (y 90-170) as the Scene says, word by word on its timestamp; ink on the night desk, ink-dark on the day desk; a very soft shadow (0 2px 12px rgba(0,0,0,.35) on night, none on day)" }
  giant:      { fontFamily: "Instrument Sans", px: 260, weight: 700, lineHeight: 0.9, tracking: "-0.05em", note: "ONLY for the peaks named in the storyboard" }
  paper-title: { fontFamily: "Instrument Sans", px: 40, weight: 600, color: "ink-dark" }
  paper-line: { fontFamily: "Instrument Sans", px: 28, weight: 500, color: "ink-dark" }
  price:      { fontFamily: "Space Mono", px: 30, weight: 700, tabularNums: true, color: "ink-dark" }
  micro:      { fontFamily: "Space Mono", px: 18, weight: 400, tracking: "0.2em", upper: true }
  stamp:      { fontFamily: "Big Shoulders", px: 150, weight: 800, upper: true, color: "accent" }

components:
  desk-night (problem ground):
    background: "solid desk-night + a warm lamp pool: radial ellipse centered at (760, 420), desk-night-lamp at the center fading to desk-night at 1100px + faint wood grain (repeating-linear-gradient of 1px lines at 3-4% opacity, slightly irregular spacing, deterministic) + static film grain 5%. Objects cast long soft shadows away from the lamp (offset +22px +28px, blur 40px, rgba(0,0,0,.55))."
  desk-day (solution ground):
    background: "solid desk-day + window light: 3 or 4 soft diagonal bands of desk-day-light (45deg, 180-260px wide, blurred 60px, 50% opacity) + faint wood grain 3% + grain 3%. Objects cast short soft shadows (offset +8px +12px, blur 24px, rgba(60,40,20,.22))."
  sheet (a sheet of paper, top-down):
    look: "paper fill, 1px hairline border, radius 3px, subtle paper texture (tiny noise 2%), shadow per desk light. A4 ratio (0.707) unless the Scene says otherwise. Text printed in ink-dark."
    motion: "slides in and settles with a tiny rotation settle (e.g. -3deg → -1deg), power3.out, like a sheet dropped on a desk; never bounces."
  quote-sheet (le devis): "a sheet: header micro 'DEVIS N° 0147' + paper-title 'Prestations web'; rows = label (paper-line) · qty (micro) · price (price, right). Rows: Modification sur ton site · 1 jour · 1 000 € / Nouvelle page · 600 € / Réparer l’automatisation · sur devis / Délai · quand il aura le temps. Total box at the bottom right: micro 'TOTAL' + price."
  rubber-stamp (the verdict mechanism of the problem part):
    look: "stamp text in the 'stamp' style, accent, inside a 7px accent border radius 14px, ink texture: SVG feTurbulence + feDisplacementMap mask with a FIXED seed (deterministic) so the edges look inked and slightly broken; rotated -8deg; multiply blend on paper."
    motion: "slams: from scale 1.35 + opacity 0 to scale 1 + opacity 0.92 in 0.12 s power4.in, with a 2-frame camera shake (4px) and a faint ink spread (the border blur 2px → 0)."
  pen (the accent object of the solution part):
    look: "a terracotta ballpoint pen seen from above: body accent-deep with a lighter accent-light highlight stripe, silver tip, ~420px long, soft shadow."
    motion: "writes and strikes: the pen tip follows the stroke path (SVG path drawn with stroke-dashoffset in sync with the pen position), strokes are accent 5px round caps, slightly wavy (hand-made)."
  tear-off-calendar (the wait): "a small desk calendar block seen from above (paper sheets on a dark top binding), huge Space Mono 700 day label in ink-dark ('J+1'); tearing = the top sheet lifts, rotates and flies off (power3.in) revealing the next."
  sticky-note: "square paper-2 note 260px, slight rotation, folded corner shadow, content drawn in ink-dark (lines, small tool tiles)."
  tool-tiles: "Real tool logos from assets/icons/*.svg (Simple Icons, CC0: gmail, make, googleforms, stripe): inline SVG path in a 72px white rounded tile filled with the brand color (Gmail #EA4335, Make #6D00CC, Google Forms #7248B9, Stripe #635BFF). Brand colors are the ONLY exception to the one-accent rule."
  smartphone (top-down): "object-dark body 300×620 radius 44px, thin bezel, screen with a dark chat UI: an outgoing accent bubble and a gray incoming bubble with 3 waiting dots (finite pulses)."
  laptop (top-down, open): "object-dark keyboard deck with a grid of faint keys + the open screen above it seen at a slight perspective (screen area light when it shows a site, dark when it shows the chat), soft shadow."
  pain-pills: "small dark pills (Space Mono 22px, white text on object-dark, radius 999px) printed like labels on the papers of the pile, each with a tiny ✕ drawn in SVG in accent."
  orb: "the AI on the laptop screen: a terracotta orb with a warm glow."
  cursor: "White macOS arrow with dark outline + drop shadow; click = press (scale .85) + accent ripple ring."
  giant-pill: "the accent-pill mechanism scaled to giant, used ONCE on « libre. »: accent fill radius 28px, white 260px 700 text; traces from the left, then the letters land with the tracking tighten."

negative:
  - "No second highlight mechanism in the phrase: the traced accent pill is the only emphasis of the text (stamps and pen strokes are objects, not text emphasis)."
  - "No hue other than terracotta, the wood browns and paper whites, except real brand colors inside tool tiles. No yellow sticky notes, no blue, no green."
  - "No emoji, no icons in round pills, no Inter/Space Grotesk/Geist/system-ui."
  - "No bouncy/elastic/back.out eases. No breathing loops, no repeat:-1. Objects settle like real paper: fast in, soft landing."
  - "Never tween letterSpacing: split letters and tween x."
  - "No visible text that is not listed in the frame's Scene lines or in the components above."
---

# Entrepreneurs 2.0, frame spec « Le bureau »

The camera looks straight down at a desk. At night, under the lamp, the problem piles up in real objects: the quote
sheet whose prices get circled, the sticky note with the automation that gets crossed out and torn, the SUR DEVIS stamp,
the phone that never gets an answer, the tear-off calendar losing its days, then invoices and envelopes that bury the
desk until one huge stamp says **STOP.** Morning light floods the desk: it is clean, a laptop opens with the AI orb, the
request is typed in plain French, and the terracotta pen strikes every line of the quote, writes the last one, and the
sheet flies away to leave **libre.** The iris from the zero drawn in the notebook opens on the dark end card.

Text: the voice's sentences stay small, word by word, in a band at the top or bottom; one word per sentence in the traced
terracotta pill. Printed text on the papers is part of the objects.
