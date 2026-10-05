---
version: 2
name: "Guillaume Herbin : VSL diagnostic"
description: >
  Video-first frame spec for the 56.8 s sales film of guillaumeherbin.fr/accompagnement, built on ../patterns/PATTERNS.md.
  Metaphor: "essayer, ça coûte" (each try costs months, margin, savings) answered by a route that is computed before
  driving (the plan). One dark stage for the whole film, near-black with the orange and electric-blue rim light of
  Guillaume's banner; the interfaces and the papers (the leboncoin listing, the hand-written draft, the GPS screen,
  the launch plan) are lit objects placed on that stage. One accent only, orange #FC7E15, kept for what matters: the
  key-word box of each subtitle and 3 peak strokes. The sentence of the voice is a subtitle at the bottom center that
  arrives word by word.
unit: 1920×1080
principle: readable without sound · one thing to look at at a time · one accent, one highlight mechanism · the voice cues every reveal

colors:
  canvas: "#0b0b0d"            # the dark stage, whole film
  canvas-2: "#141519"          # raised dark surfaces (dashboard, GPS bezel)
  paper: "#f6efe3"             # cream: the draft sheet, documents
  paper-2: "#ede4d4"           # secondary cream
  card-light: "#ffffff"        # the real interfaces (leboncoin listing, plan pages)
  ink: "#ffffff"               # text on dark
  ink-soft: "#c9ccd3"
  ink-mute: "#8a8f98"
  ink-dark: "#1a1b1f"          # text on cream / white
  ink-dark-soft: "#555a63"
  hairline-light: "#e3dccf"
  accent: "#FC7E15"            # THE brand accent (measured on the covers)
  accent-light: "#ff9a45"
  accent-deep: "#e0620a"
  accent-glow: "#ffb070"
  rim-blue: "#2f7bff"          # ONLY as rim light / back light (banner), never on text or boxes
  pen-red: "#d33a2c"           # ONLY the hand-written red ink of the draft (frame 4), a real-object color like the leboncoin green

fonts:
  Instrument Sans: { files: ["assets/fonts/InstrumentSans-400.woff2 (400)", "assets/fonts/InstrumentSans-500.woff2 (500)", "assets/fonts/InstrumentSans-600.woff2 (600)", "assets/fonts/InstrumentSans-700.woff2 (700)"] }
  Space Mono: { files: ["assets/fonts/SpaceMono-400.woff2 (400)", "assets/fonts/SpaceMono-700.woff2 (700)"] }
  Big Shoulders: { files: ["assets/fonts/BigShoulders-700.woff2 (700)", "assets/fonts/BigShoulders-800.woff2 (800)", "assets/fonts/BigShoulders-900.woff2 (900)"] }
  Montserrat: { files: ["assets/fonts/Montserrat-600.woff2 (600)", "assets/fonts/Montserrat-700.woff2 (700)", "assets/fonts/Montserrat-800.woff2 (800)"] }
  Caveat: { files: ["assets/fonts/Caveat-600.woff2 (600)"] }

typography:
  subtitle:   { fontFamily: "Instrument Sans", px: 62, weight: 600, lineHeight: 74, tracking: "-0.015em", note: "the sentence of the voice at the BOTTOM CENTER (inside the band y 890 to 980 that carries nothing else), 45 characters at most per chunk (a longer sentence splits into chunks that replace each other), word by word on its timestamps; white with a soft dark shadow (0 2px 18px rgba(0,0,0,.55)); a bottom shade (transparent → rgba(0,0,0,.8) over y 640 to 1080) keeps it readable over light interfaces. Never at the top left" }
  type:       { fontFamily: "Instrument Sans", px: 84, weight: 600, lineHeight: 1.12, tracking: "-0.025em", note: "ONLY the 2 typographic moments of the storyboard (the diagnosis 'sans plan', the pivot question): centered, never bigger than 84 px, no subtitle at the bottom meanwhile" }
  numeral-jumbo: { fontFamily: "Big Shoulders", px: 260, weight: 900, lineHeight: 0.9, tabularNums: true, note: "rolling numbers of the dashboard and of '21 ANS · 3 000 €'" }
  ui:         { fontFamily: "Instrument Sans", px: 28, weight: 500, lineHeight: 1.3 }
  hand:       { fontFamily: "Caveat", px: 64, weight: 600, note: "the hand-written draft only (frame 4 and 5)" }
  micro:      { fontFamily: "Space Mono", px: 22, weight: 700, tracking: "0.3em", upper: true, note: "dashboard captions, GPS banner, 'TA PROCHAINE ÉTAPE'" }
  name:       { fontFamily: "Montserrat", px: 54, weight: 800, note: "'Guillaume' in ink + 'Herbin' in accent, as on the banner" }
  cta:        { fontFamily: "Montserrat", px: 52, weight: 800, note: "the end-card button" }

components:
  ground-dark:
    background: "solid canvas + 1-2 soft radial halos behind the focal element (accent 14-22 %, rim-blue 10-18 %, blur 100px+) + static film grain 5 %. A rim of rim-blue light along an arc at the top of the frame (the banner's back light), 20-40 % opacity. Painted as a full-duration class=\"clip\" layer, never on #root."
  word-by-word:
    rule: "Each word of the subtitle appears ON its voice timestamp, at 35 % white: fromTo {opacity:0, y:8, filter:blur(6px)} → {opacity:1, y:0, blur(0)} in 0.14 s, immediateRender:false, then it turns to full white in 0.2 s. Never the whole sentence at once. Before a seam the subtitle leaves: opacity 1 → 0 and blur 0 → 6 px in 0.14 s."
  key-word-box:
    look: "a small rectangle in accent, radius 10px, padding 0 14px 4px, overflowing the word; the word turns to ink-dark inside. Never a black box."
    motion: "the box traces from the left (scaleX 0 → 1, transform-origin left, 0.16 s power3.out), 0 to 2 frames before the word is spoken; the word changes color as the box passes (0.1 s)."
    rule: "ONE box per sentence, on the word the storyboard names as [boîte : …]. No other colored text anywhere (real interfaces excepted)."
  peak-stroke:
    look: "a tapered accent brush stroke, 9 px, round attack, thin exit, rotated -1.2°, under THE key word only."
    motion: "draws from the left (scaleX 0 → 1, 0.35 s power2.out) while the word is spoken."
    rule: "named [trait : …] in the storyboard (3 peaks: 'sans plan', 'métier', 'moins de casse'). Never under the whole sentence."
  listing:
    description: "the REAL leboncoin listing (assets/img/annonce-audi.png, 2000×1325, dealer names, logos, plates and account already blurred), placed as one image on a white sheet with a 40px radius and a soft shadow, like a browser page floating on the stage; the camera reframes it by scale and translation only. Overlays drawn in HTML on top of it, aligned to its pixels (coordinates below are in the 2000×1325 image): price '86 900 €' x 78-218 y 1172-1208 (green #1d6b43, Montserrat 800), date 'avant-hier à 12:11' x 78-250 y 1280-1302, button 'Envoyer un message' x 1367-1900 y 573-648 (center 1633, 610), seller card x 1325-1942 y 308-795. The new price and the date are drawn in the same font and green as the real page."
  search:
    description: "the leboncoin search bar rebuilt in HTML from the screenshot (white pill 1000×86, grey #f2f2f4, placeholder 'Rechercher sur leboncoin', orange #ec5a13 search button with a white magnifier, leboncoin wordmark at its left from the screenshot crop x 78-365 y 25-90). The query types char by char: 'voiture occasion'."
  balance:
    description: "a plain banking balance card (dark glass, Space Mono label 'SOLDE ÉPARGNE', numeral in Big Shoulders 900 white) that rolls down: 12 400 € → 4 150 €. No bank brand."
  draft:
    description: "a sheet of lined cream paper (paper, blue lines rgba(47,123,255,.18) every 70px, two soft creases), slight rotation -4°, deep shadow; hand-written lines in Caveat ink-dark: 'Essai n°2 — la voiture', 'Achat ……… 11 800', 'Contrôle + pneus … 640', 'Carte grise, annonce … 310', 'Baisse de prix …… 900', a ruled total line, 'Marge :' and '− 650 €' in pen-red, circled in pen-red. Each line writes itself (clip-path inset from the right, 0.25 s) as if a pen wrote it."
  pen:
    description: "a black ballpoint pen, blurred, in the foreground, its tip following the writing; never sharp."
  dashboard:
    description: "the night instrument cluster of the styleframes B1/B2: round dials (canvas-2 radial dial, ticks in ink-soft, orange glowing arc), a central panel with two rolling digit drums in accent (numeral-jumbo) and a caption in micro; the 'ÉPARGNE' gauge with a red reserve arc (pen-red is NOT used: the reserve arc is #ff3b2f, a real dashboard warning color) and a glowing '€' warning light in accent."
  gps:
    description: "the GPS screen of styleframe B3: rounded screen 1580×760 (radius 44px, canvas-2 bezel), dark map with curved roads #1f232b, the route in accent (16px, glow), the start point in rim-blue with a white ring, waypoints as accent rings, pins in Instrument Sans 30 on dark pills; the active pin fills with accent; top banner 'Itinéraire calculé · ton plan'."
  portrait:
    description: "Guillaume's real portrait (assets/img/portrait.png, the round cut-out with its orange and blue halo), 660px, on the dark stage; a soft accent + rim-blue radial behind it. Never redrawn."
  years:
    description: "a horizontal timeline of years 2010 → 2026 in Big Shoulders 800 ink-mute, the current year in white; small hand-written errors in Caveat ink-soft ('mauvais achat', 'marge mal calculée', 'charges oubliées') that get struck through by an accent stroke as the camera passes. The line of the timeline becomes the GPS route (bridge)."
  plan:
    description: "the real launch plan (assets/img/plan-lancement.png, 1536×1024: cover, 'Ton point d'équilibre' page, 'Tes 30 premiers jours' page). The camera frames the middle page; the box 'Ventes nécessaires par mois pour répondre à l'objectif : 2' sits at x 750-1070 y 595-695 of the image; an accent ring (5px, radius 20) traces around it."
  cursor:
    description: "dark macOS arrow with a white outline + drop shadow; it arrives in ONE curved move (0.4 to 0.5 s power3.out) and clicks directly: press (scale .85, 0.06 s) + accent ripple ring. The gag of frame 3 is the ONLY written exception: there the hesitation IS the joke (3 stops of 0.4 s, then the move to the close button)."
  end-card:
    description: "dark stage with the orange and blue arcs of the banner; micro 'TA PROCHAINE ÉTAPE'; ONE button 'Voir si mon profil correspond' (accent fill, ink-dark Montserrat 800 52px, radius 80, glow 0 30px 90px rgba(252,126,21,.45)); under it '5 questions · 2 minutes · aucun paiement à ce stade' (Instrument Sans 30 ink-soft, the last part in white) and the URL 'guillaumeherbin.fr/accompagnement' in Space Mono 26 ink-mute; the launch plan blurred in the background; a cursor arrives and clicks the button directly, then 3 s of living hold."

negative:
  - "No second highlight mechanism: the key-word box is the ONLY way a word of a subtitle is emphasized; the peak stroke marks the 3 peaks."
  - "No big sentence: subtitle 60 to 64 px, typographic moment 84 px at most; nothing but the subtitle in the band y 890 to 980."
  - "One thing to look at at a time; equal side margins in side-by-side layouts."
  - "No camera back-and-forth on the decor. No cursor hesitation outside the gag of frame 3."
  - "No decor without meaning; no line of the decor crossing a sentence."
  - "No hue other than the accent, except the real interfaces (leboncoin green and blue), the rim-blue back light, the red ink of the draft and the red reserve arc of the gauge."
  - "No revenue figure, no promise: never show the turnover of the accountant's report, the Kbis is not in the film."
  - "No Inter, Space Grotesk, Geist, system-ui. No emoji."
  - "No bouncy/elastic/back.out eases. No breathing loops, no repeat:-1."
  - "No visible text that is not listed in the frame's Scene lines."
  - "Never tween letterSpacing."
---

# Guillaume Herbin : frame spec

The whole film plays on one dark stage, lit like Guillaume's banner: near-black, an orange glow, a blue back light
along an arc. **The problem** is told with real objects placed on it: the leboncoin listing that ages and loses its
price, the savings balance that rolls down, then the hand-written draft of someone who tries alone. A **pivot** on
pure black, « Et si tu essayais… avec un plan ? », and in the silence a GPS screen lights up. **The solution** is told
by Guillaume himself (his real portrait, 21 ans, 3 000 €, sixteen years of corrected mistakes) and by the route the
plan computes: ta situation, ton modèle, tes chiffres, down to the real page of the launch plan. The end card turns the
search bar of the hook into the button of the page.

Everything the viewer reads is Instrument Sans: the sentence of the voice as a subtitle at the bottom center, word by
word, with exactly one key word per sentence in a small accent box. Numbers are Big Shoulders, labels Space Mono, the
name and the button Montserrat, the draft Caveat.
