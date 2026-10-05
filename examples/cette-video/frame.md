---
version: 2
name: Entrepreneurs 2.0, Launch Frame « Cette vidéo » (agency motion design patterns)
description: >
  Video-first frame spec for the Entrepreneurs 2.0 motion design A « Cette vidéo », same system as C « Le devis » and
  B « Traduire » (examples/traduire/frame.md), built on patterns/PATTERNS.md. The film
  talks about ITSELF: no agency, no motion designer, no studio, no voice actor made it; it was explained to an AI in
  simple words and the AI built it. Worlds: the claim plays on the dark stage like film credits; the making-of floods
  into warm paper; « Avant » rewinds into the dark; the lesson plays on paper; the end card returns to the dark stage.
  One accent only, terracotta, used for ONE traced pill per sentence. Small centered phrase text arriving word by word;
  a few giant words only at the peaks.
unit: 1920×1080
principle: readable without sound · one accent, one highlight mechanism · the voice cues every reveal

colors:
  canvas: "#0d0b0a"          # dark world (problem + end card)
  canvas-2: "#141010"
  paper: "#f6f1e9"            # light world (solution) full-bleed ground
  paper-2: "#efe7dc"
  card-light: "#fffdf9"
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
  giant:      { fontFamily: "Instrument Sans", px: 260, weight: 700, lineHeight: 0.9, tracking: "-0.05em", note: "ONLY for the peaks named in the storyboard; may sit BEHIND an object" }
  numeral-jumbo: { fontFamily: "Instrument Sans", px: 300, weight: 600, lineHeight: 0.9, tracking: "-0.02em", tabularNums: true }
  ui:         { fontFamily: "Instrument Sans", px: 28, weight: 500, lineHeight: 1.3 }
  title:      { fontFamily: "Instrument Sans", px: 44, weight: 600, lineHeight: 1.1, tracking: "-0.02em" }
  code:       { fontFamily: "Space Mono", px: 26, weight: 400, lineHeight: 1.5, note: "code lines; keywords (const, function, return, if, await, <div>, class) in accent-light, strings in ink-soft, the rest in ink / ink-dark" }
  price:      { fontFamily: "Space Mono", px: 30, weight: 700, tabularNums: true }
  micro:      { fontFamily: "Space Mono", px: 18, weight: 400, tracking: "0.2em", upper: true }
  wordmark:   { fontFamily: "Big Shoulders", px: 64, weight: 800, upper: true, note: "'ENTREPRENEURS' in ink + ' 2.0' in accent-light" }

components:
  ground-dark:
    background: "solid canvas + 1-2 soft radial terracotta halos (14-28% opacity, blur 100px+) behind the focal element + static film grain 4-6%"
  ground-light:
    background: "solid paper + one very soft warm radial (accent at 6-10%) behind the focal element + grain 3%. Text is ink-dark."
  word-by-word:
    rule: "Each word of the phrase appears ON its voice timestamp: fromTo {opacity:0, y:10, filter:blur(8px)} → {opacity:1, y:0, blur(0)} in 0.3 s power3.out. Never the whole sentence at once."
  accent-pill (THE highlight mechanism, one per sentence):
    look: "filled accent rectangle, radius 12px, padding 0.06em 0.32em, text white, same font as the phrase"
    motion: "the pill traces first: scaleX 0→1 from the left in 0.28 s power3.out (optionally starting at rotation -8deg and straightening to 0 in 0.4 s), THEN the word's letters write inside with a 0.02 s stagger. Starts 0-2 frames before the word is spoken."
    rule: "ONE pill per sentence, on the word the storyboard names. No other colored text anywhere (code keywords inside a code window are the only exception)."
  giant-word:
    motion: "enters with its tracking tightening from 0.35em to -0.05em + opacity 0→1 + blur 12px→0 over 0.5 s expo.out. NEVER tween letterSpacing (it snaps to device pixels under seek capture and the lint blocks it): keep letter-spacing -0.05em static, split the word into inline-block letters and tween each letter's x from (i - (n-1)/2) × 0.4em to 0. A counting number keeps only scale + blur."
  glass-card-dark:
    background: "linear-gradient(160deg, rgba(40,33,28,.92), rgba(24,20,17,.9) 45%, rgba(20,16,14,.9) 80%, rgba(30,24,20,.92)); 1px rgba(245,239,231,.10) border; inset 0 1px 0 rgba(255,255,255,.14); shadow 0 50px 120px rgba(0,0,0,.7); radius 14px"
  card-light:
    background: "card-light, 1px hairline-light border, radius 14px, shadow 0 30px 80px rgba(60,40,20,.14), 0 2px 6px rgba(60,40,20,.08)"
  code-window (the computer's language):
    description: "glass-card-dark on the dark world (card-light on paper) with a top bar (3 small dots + micro title), body = code lines in the 'code' style with line numbers in ink-mute. Canonical code (reuse these lines, in this order, everywhere code appears): 1 `const page = await build(site.routes);` 2 `if (!page.ok) return retry(site);` 3 `<div class=\"hero\">` 4 `  <button onclick=\"book()\">` 5 `export async function deploy(site) {` 6 `  await publish(site, { cache: true });` 7 `}` 8 `for (const route of site.routes) {` then repeat."
  caret:
    description: "the text caret: a 4px × 58px accent-light bar, blinks as finite on/off steps (0.5 s period, NEVER a repeat:-1 loop)."
  persona-toi (the entrepreneur):
    description: "A flat vector character in inline SVG: head + shoulders, simple hair, NO detailed face (two small dot eyes max), ~340px tall. Colors: skin #e8c4a8, hair #2e2924, shirt ink-dark #2e2924 on paper / #3a322c on dark. Default pose: arms down, calm. Friendly and simple, not childish. The same drawing in every frame where it appears."
  persona-traducteur (the translator, i.e. the developer / agency / provider):
    description: "The same flat style as persona-toi but distinguishable: short hair #6b5a4c, round glasses (2 thin ink circles), a headset arc, shirt #4a3f36, holding a small laptop. Neutral, never a caricature: the message is not against developers."
  computer:
    description: "A simple flat monitor in inline SVG (rounded dark screen 300×200 inside a #2e2924 bezel, small stand); its screen shows 3-5 short code lines in the 'code' style scaled down."
  speech-bubble:
    description: "rounded card-light bubble (radius 22px, tail toward the speaker) with ui text in ink-dark; on the dark world it keeps its light fill (it is the user's words)."
  id-card (role cards):
    description: "glass-card-dark 420×150: micro label on top (e.g. 'RÔLE'), title (e.g. 'Développeur'), and a price line in 'price' style right-aligned (e.g. 'TJM 450 €')."
  tool-tiles:
    description: "Real tool logos from assets/icons/*.svg (Simple Icons, CC0: gmail, stripe, make, notion...). Inline SVG path in an 88px white rounded tile (radius 20px, soft shadow) filled with the tool's brand color: Gmail #EA4335, Stripe #635BFF, Make #6D00CC, Notion #000000. Brand colors are the ONLY exception to the one-accent rule, only inside tool tiles."
  chat-input:
    description: "Large card with micro label 'TA DEMANDE, EN FRANÇAIS', prompt typed char by char with an accent caret, square accent send button with a white up-arrow. card-light on paper."
  site-mock:
    description: "Browser card (top bar with 3 dots + mono url 'ton-site.fr'), body on paper for the site 'Studio Lumen' (photographer in Nantes): nav bars, title in ink-dark, grey text bars, image blocks #d8cfc3. Accent elements only for the thing the voice points at."
  prompt-card:
    description: "card-light 520×170: a numbered accent disc (40px, white Space Mono digit) + micro label + one ui line of example text."
  learning-path:
    description: "a horizontal path: a 4px ink-dark line with 5 stations (48px discs, card-light fill, 3px ink-dark border, Space Mono digit 0-4 inside). Station 0 is the start: accent fill, white digit, a soft accent glow, and a micro pin label 'TU ES ICI' above it."
  cursor:
    description: "White macOS arrow with dark outline + drop shadow; click = press (scale .85) + accent ripple ring that expands and fades."
  video-player (the film itself):
    description: "a card (glass-card-dark on the dark world, card-light on paper), 16:9, radius 14px, with a bottom control bar: a circular play button (56px disc, accent fill, white triangle drawn in SVG), a thin progress track (ink-mute) with an accent played part and a round playhead, and a Space Mono timecode « 0:01 / 0:44 ». Droste mode: the player's screen shows a smaller copy of the whole frame, which contains a smaller player, 4 levels deep (each level 0.62 scale), so the film literally contains itself."
  credits (film credits):
    description: "classic end-credits typography on the dark stage: role in micro (Space Mono 18px, 0.2em tracking, ink-mute) above, name in title (Instrument Sans 44px 600, ink) below, centered, 90px between blocks; the whole column rolls upward slowly (linear) like a film credit roll."
  waveform:
    description: "vertical rounded bars (6px wide, 4px gap, ink on dark) mirrored around a horizontal center line, heights from the real voice envelope given by the storyboard; a playhead line in accent sweeps left to right and the bars it has passed turn accent-light."
  casting-card:
    description: "glass-card-dark 460×150: micro label « CASTING », title « Comédien voix off », price line « 450 € / session » in price style."
  timeline-editor:
    description: "a video-editor timeline card (card-light on paper): a time ruler in Space Mono micro, three tracks labeled in micro « IMAGE », « VOIX », « MUSIQUE »; the IMAGE track is filled with thumbnail blocks (paper-2 fill with one tiny ui word each), the VOIX track with a small ink waveform, the MUSIQUE track with an accent-deep 30% bar; an accent playhead."
  role-card:
    description: "same as id-card: glass-card-dark on dark, card-light on paper, 380×120: micro « RÔLE » + title (Développeur / Agence / Prestataire)."
  light-point:
    description: "a white-hot point (radial #fff3ea → accent-glow → transparent) used when the caret turns into light before the flood."

negative:
  - "No second highlight mechanism: the traced accent pill is the ONLY way a word is emphasized (no colored text, no glow text)."
  - "No big phrase text: sentences are 'phrase' size; only the storyboard's named peaks use 'giant' / 'numeral-jumbo'."
  - "No hue other than terracotta, except real brand colors inside tool tiles. No terminal green."
  - "No Inter, Space Grotesk, Geist, system-ui. No emoji. No icons in round pills."
  - "No bouncy/elastic/back.out eases. No breathing loops, no slow push on every scene, no repeat:-1."
  - "No visible text that is not listed in the frame's Scene lines (the canonical code lines and the component labels above are allowed)."
  - "Never tween letterSpacing."
---

# Entrepreneurs 2.0, frame spec « Cette vidéo »

The film is about itself. It opens as a video that contains itself (a player inside a player inside a player), then
rolls its own credits on the black stage: no agency, no motion designer, no studio, and the voice is not an actor
either (the real waveform of this very voice). Light floods in with the making-of: a request typed in plain words and
the editor timeline of this very film filling itself. « Avant » rewinds into the dark stage for the old way (an agency,
a quote, the wait), then paper again for the lesson: your site, your tools, your automations work exactly the same;
you do not need someone who knows how, you need to know how to ask, and that can be learned. The player comes back at
0:00 and the iris opens from its play button into the end card, the same as films B and C.

Everything the viewer reads is Instrument Sans: small sentences that arrive word by word on the voice, with exactly one
word per sentence written inside a terracotta pill that traces itself first. Code, numbers, roles and labels are Space
Mono; the wordmark is Big Shoulders.
