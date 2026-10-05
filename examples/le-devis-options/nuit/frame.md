---
version: 2
name: Entrepreneurs 2.0, Launch Frame « Nuit » (C, all-dark variant)
description: >
  Video-first frame spec for the Entrepreneurs 2.0 landing-page motion design, rebuilt on the patterns mined from 56
  viral SaaS motion designs (patterns/PATTERNS.md). ALL-DARK variant, made to sit seamlessly in the
  dark hero of the landing page: the PROBLEM lives on a cold, flat, dim near-black stage; the SOLUTION lives on a WARM
  NIGHT stage (same near-black, but lit by a big terracotta glow, warm glass cards, depth); the end card is dark too. One accent only, terracotta, used for ONE traced pill per sentence. Small centered phrase text that
  arrives word by word on the voice; a few giant words only at emotional peaks.
unit: 1920×1080
principle: readable without sound · one accent, one highlight mechanism · the voice cues every reveal

colors:
  canvas: "#0d0b0a"          # dark world (problem + end card)
  canvas-2: "#141010"
  paper: "#f6f1e9"            # light world (solution) full-bleed ground
  paper-2: "#efe7dc"          # secondary light surface
  card-light: "#fffdf9"       # cards on the light world
  ink: "#f5efe7"              # text on dark
  ink-soft: "#cdbfb2"
  ink-mute: "#9b9289"
  ink-dark: "#1a1612"         # text on light
  ink-dark-soft: "#5a5348"
  hairline-light: "#e2d9cc"
  accent: "#c25b28"
  accent-light: "#d4703f"
  accent-deep: "#a84d22"
  accent-glow: "#e08a5c"

fonts:
  Instrument Sans: { files: ["assets/fonts/InstrumentSans-400.woff2 (400)", "assets/fonts/InstrumentSans-500.woff2 (500)", "assets/fonts/InstrumentSans-600.woff2 (600)", "assets/fonts/InstrumentSans-700.woff2 (700)"] }
  Space Mono: { files: ["assets/fonts/SpaceMono-400.woff2 (400)", "assets/fonts/SpaceMono-700.woff2 (700)"] }
  Big Shoulders: { files: ["assets/fonts/BigShoulders-800.woff2 (800)"] }

typography:
  phrase:     { fontFamily: "Instrument Sans", px: 54, weight: 600, lineHeight: 1.18, tracking: "-0.02em", note: "the sentence of the voice, SMALL and centered (or anchored as the Scene says), arrives word by word on its timestamp" }
  giant:      { fontFamily: "Instrument Sans", px: 260, weight: 700, lineHeight: 0.9, tracking: "-0.05em", note: "ONLY for the 3-4 emotional peaks named in the storyboard; may overflow or sit BEHIND an object" }
  numeral-jumbo: { fontFamily: "Instrument Sans", px: 300, weight: 600, lineHeight: 0.9, tracking: "-0.02em" }
  ui:         { fontFamily: "Instrument Sans", px: 28, weight: 500, lineHeight: 1.3 }
  title:      { fontFamily: "Instrument Sans", px: 44, weight: 600, lineHeight: 1.1, tracking: "-0.02em" }
  price:      { fontFamily: "Space Mono", px: 30, weight: 700, tabularNums: true }
  micro:      { fontFamily: "Space Mono", px: 18, weight: 400, tracking: "0.2em", upper: true }
  wordmark:   { fontFamily: "Big Shoulders", px: 64, weight: 800, upper: true, note: "'ENTREPRENEURS' in ink + ' 2.0' in accent-light" }
  cta:        { fontFamily: "Big Shoulders", px: 34, weight: 800, upper: true }

components:
  ground-dark:
    background: "solid canvas + 1-2 soft radial terracotta halos (14-28% opacity, blur 100px+) behind the focal element + static film grain 4-6%"
  ground-dark (problem, frames 1-3): keep it FLAT and COLD: halos at 10-14% only, no warm light.
  ground-warm-night (solution, frames 4-8, replaces the old paper world):
    background: "solid #120d0a + one big warm radial behind the focal element (accent-light at 38%, radius 900px, blur 120px) + a second faint radial (accent-glow 12%) off-center for depth + static grain 5%. Text is ink (#f5efe7). It must feel like the same room with the lamp switched on."
  glass-card-warm (cards on the warm night stage, replaces card-light):
    background: "linear-gradient(160deg, rgba(64,46,36,.94), rgba(40,30,24,.92) 50%, rgba(34,25,20,.94)); 1px rgba(255,210,175,.16) border; inset 0 1px 0 rgba(255,235,215,.18); shadow 0 40px 110px rgba(0,0,0,.65), 0 0 60px rgba(194,91,40,.12); radius 14px. Text ink, secondary text ink-soft; UI grey bars rgba(245,239,231,.16)."
  word-by-word:
    rule: "Each word of the phrase appears ON its voice timestamp: fromTo {opacity:0, y:10, filter:blur(8px)} → {opacity:1, y:0, blur(0)} in 0.3 s power3.out. Never the whole sentence at once."
  accent-pill (THE highlight mechanism, one per sentence):
    look: "filled accent rectangle, radius 12px, padding 0.06em 0.32em, text white (on dark) or white (on light), same font as the phrase"
    motion: "the pill traces first: scaleX 0→1 from the left in 0.28 s power3.out (optionally starting at rotation -8deg and straightening to 0 in 0.4 s), THEN the word's letters write inside with a 0.02 s stagger. Starts 0-2 frames before the word is spoken."
    rule: "ONE pill per sentence, on the word the storyboard names. No other colored text anywhere."
  giant-pill (the peak of the film, used ONCE on « libre. »):
    look: "the accent-pill mechanism scaled to giant: filled accent rectangle radius 28px, padding 0.04em 0.26em, text giant size 260px 700 in white (#fffdf9)"
    motion: "the pill traces from the left (scaleX 0→1, 0.36 s power3.out) with a -6deg → 0 rotation settle, then the letters land inside with the tracking tighten (per-letter x, frame.md giant-word)"
  giant-word:
    motion: "enters with its tracking tightening from 0.35em to -0.05em + opacity 0→1 + blur 12px→0 over 0.5 s expo.out; may sit behind a card/object (z-order) for depth. NEVER tween letterSpacing (it snaps to device pixels under seek capture and the lint blocks it): keep letter-spacing -0.05em static, split the word into inline-block letters, and tween each letter's x from (i - (n-1)/2) × 0.4em to 0. A counting number keeps only scale + blur."
  echo-stack:
    look: "the word sharp in the center + 4 copies above and below at 60/35/20/10% opacity, slightly blurred"
    motion: "copies start spread (±180px) and converge to ±70px in 0.4 s power3.out while the center word lands"
  glass-card-dark:
    background: "linear-gradient(160deg, rgba(40,33,28,.92), rgba(24,20,17,.9) 45%, rgba(20,16,14,.9) 80%, rgba(30,24,20,.92)); 1px rgba(245,239,231,.10) border; inset 0 1px 0 rgba(255,255,255,.14); shadow 0 50px 120px rgba(0,0,0,.7); radius 14px"
  card-light:
    background: "card-light, 1px hairline-light border, radius 14px, shadow 0 30px 80px rgba(60,40,20,.14), 0 2px 6px rgba(60,40,20,.08)"
  quote-card (le devis):
    content: "header: micro 'DEVIS N° 0147' + title 'Prestations web'; rows = label (ui) · qty (micro) · price (price, right). Rows: Modification sur ton site · 1 jour · 1 000 € / Nouvelle page · 600 € / Réparer l’automatisation · sur devis / Délai · quand il aura le temps. Total row: micro 'TOTAL' + filled accent badge with the amount."
    strike: "a struck row: ✕ mark before the label, a 3px accent line across the label, label dims, the price flips to 'toi' (row 4 → 'maintenant') in accent."
    worlds: "dark glass on the problem stage (frame 1), glass-card-warm on the warm night stage (frames 6-7)."
  tool-tiles:
    description: "Real tool logos from assets/icons/*.svg (Simple Icons, CC0: gmail, make, googleforms, stripe, wordpress, shopify, notion, zapier). Place the inline SVG path in a 88px white rounded tile (radius 20px, soft shadow) and fill it with the tool's own brand color: Gmail #EA4335, Make #6D00CC, Google Forms #7248B9, Stripe #635BFF, WordPress #21759B, Shopify #7AB55C, Notion #000000, Zapier #FF4F00. These brand colors are the ONLY exception to the one-accent rule, and only inside tool tiles."
  persona (« toi », the entrepreneur):
    description: "A flat vector character in inline SVG, head + shoulders + both arms, ~420px tall. It must READ as a stressed person at thumbnail size: both forearms raised, elbows out, the two HANDS clearly drawn (a palm shape with 4 short fingers each, skin #e8c4a8, ink-dark outline 3px) gripping the top of the head, fingers overlapping the hair; worried eyebrows (two short ink strokes tilted up in the middle), two dot eyes, a small flat mouth; one sweat drop (light blue is forbidden: use paper #f6f1e9 with an ink outline). Hair #2e2924, shirt #3a322c on dark. 3 short accent stress strokes above the head. Friendly and simple, not childish, never round ear-like blobs on the sides of the head."
  pain-pills:
    description: "Small dark pills (Space Mono 20px, white text on #2e2924, radius 999px) that pop around the persona one by one (≈0.12 s apart), slight random rotation (deterministic, from index), each with a tiny ✕ in accent."
  light-point / orb:
    description: "The AI: a white-hot point (radial #fff3ea → accent-glow → transparent) that becomes an orb. On the warm night stage the orb is terracotta with a strong warm bloom that lights the stage around it."
  chat-input:
    description: "Large card with micro label 'TA DEMANDE, EN FRANÇAIS', prompt typed char by char with an accent caret, square accent send button with a white up-arrow. On the warm night stage it is glass-card-warm."
  website-mock:
    description: "Browser card (glass-card-warm frame, top bar with 3 dots + mono url 'ton-site.fr'), body = the client's site kept LIGHT (paper #f6f1e9, it is a real website seen on a screen) with the site 'Studio Lumen' (photographer in Nantes): nav bars, title 'Photographe à Nantes, portraits et mariages' in ink-dark, grey text bars, 3 image blocks (#d8cfc3). New button 'Réserver une séance' = accent fill, white text, glow ring."
  cursor:
    description: "White macOS arrow with dark outline + drop shadow; click = press (scale .85) + accent ripple ring that expands and fades."
  stamp:
    description: "'SUR DEVIS' Big Shoulders 800 uppercase ~150px, accent, 7px accent border, radius 14px, dark translucent fill, rotated -8deg on a wrapper."

negative:
  - "No second highlight mechanism: the traced accent pill is the ONLY way a word is emphasized (no colored text, no glow text)."
  - "No big phrase text: sentences are 'phrase' size; only the storyboard's named peaks use 'giant'."
  - "No hue other than terracotta, except real brand colors inside tool tiles."
  - "No Inter, Space Grotesk, Geist, system-ui. No emoji. No icons in round pills."
  - "No bouncy/elastic/back.out eases (the pill's small rotation settle uses power3.out). No breathing loops, no slow push on every scene."
  - "No visible text that is not listed in the frame's Scene lines."
---

# Entrepreneurs 2.0, frame spec « Nuit »

One room, two lights. **The problem** plays on a cold, flat, dim black stage: the quote that fills up, the automation
that breaks, the provider who never answers, the entrepreneur buried under his pain pills. A single **« Stop. »** freezes
everything, then a warm light blooms from the center and stays: we are on **the warm night stage**, the same black but
lit by a big terracotta glow, with warm glass cards and depth: the AI orb, the request typed in plain French, the button
that appears (the client's website stays light, it is a screen), the quote whose lines get struck one by one. The iris
from the zero takes us into the **end card**, dark as the hero of the landing page. Nothing in this film is ever a light
full-screen ground: it must sit in a dark page without flashing.

Everything the viewer reads is Instrument Sans: small sentences that arrive word by word on the voice, with exactly one
word per sentence written inside a terracotta pill that traces itself first. A handful of giant words mark the peaks, in
ink on the dark stages. Numbers and labels are Space Mono; the wordmark and the CTA are Big Shoulders.
