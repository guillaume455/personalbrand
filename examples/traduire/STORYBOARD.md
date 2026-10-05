---
format: 1920x1080
duration: 50.4s
message: "L'ordinateur parle enfin ta langue : tu n'as plus besoin d'un traducteur technique, il te reste à apprendre quoi lui dire."
arc: Hook → Problem → Loop → Break → Pivot → Turn → Demo → Payoff → Twist → Reassurance → CTA
audience: indépendants et fondateurs de petites structures (France), non techniques, qui paient un prestataire pour chaque modification
mode: autonomous
captions: disabled
music: "pre-mixed with voice and SFX in assets/audio/mix-B.wav (mounted at root by the orchestrator)"
patterns: patterns/PATTERNS.md
---

## Video direction

- **Two worlds** (frame.md): frames 1-4 = PROBLEM on the dark stage; frames 5-9 = SOLUTION on warm paper (the light flood at the end of frame 4 opens into it); frame 10 = END CARD back on the dark stage (the iris from station 0). Each frame paints its own full-bleed ground as a `class="clip"` layer.
- **Text** (readable without sound): every sentence of the voice is shown as small centered `phrase` text that arrives WORD BY WORD on the timestamps given in each frame (`word@seconds`, frame-local). Exactly ONE word or group per sentence sits in the traced `accent-pill` (named in the Scene lines as [pill: …]). No other colored or glowing text.
- **Giant words**: only the peaks named as [giant: …] (« Aujourd’hui, » and « s’apprend. ») plus the year counter of frame 1 (numeral-jumbo).
- **Recurring objects** (frame.md): the code-window and its canonical code lines, persona-toi, persona-traducteur, the computer, the caret. They must look the same in every frame they appear in.
- **Motion grammar**: smooth long-tail settles (power3.out default, expo.out for fast arrivals), no bounce. One camera move per scene at most. Holds are still.
- **Visible copy**: exactly the quoted copy of the Scene lines (French, typographic ’, non-breaking spaces before : ? !), nothing else.
- **Negative list**: slideshow (everything at t=0), screensaver (many things floating), colored text instead of the pill, big phrase text, any hue other than terracotta except tool-tile brand colors, terminal green.

## Frame 1 : Des décennies

- scene: A single year alone on the dark stage rolls through the decades, shrinks into the title bar of a code window, and the window floods with code
- duration: 4.10s
- transition_in: cut
- status: animated
- src: compositions/frames/01-decennies.html
- voiceover: "Pendant des décennies, pour parler à un ordinateur, il fallait parler sa langue."
- type: hook
- blueprint: dataviz-countup (Adapt)
- focal: the year counter, then the code window
- rules: counting-dynamic-scale, waterfall-entry
- world: dark

Word cues: Pendant@0.09 des@0.36 décennies@0.58 pour@1.15 parler@1.32 à@1.60 un@1.76 ordinateur@1.98 il@2.66 fallait@2.78 parler@2.96 sa@3.28 langue@3.46 (silence 3.74-4.10)
Scene 1 (0.0-1.15s): first image = the year « 1975 » ALONE, dead center, numeral-jumbo in ink on the dark stage with a soft terracotta halo (no logo, no UI). From 0.58 it rolls through the years to « 2022 » (→ counting-dynamic-scale: tabular digits, the number grows slightly as it counts, lands at 1.10). Phrase under it, word by word « Pendant des décennies, ».
Scene 2 (1.15-2.60s): the year shrinks and flies up into the micro title of a code-window (glass-card-dark, ~1100×560, centered) that rises from below at 1.15; the window shows an empty first line with the blinking caret. Phrase moves to the bottom (above y 900) and continues word by word « pour parler à un ordinateur, ».
Scene 3 (2.60-4.10s): the canonical code lines type in and then cascade faster and faster (→ waterfall-entry), scrolling up inside the window; from 3.40 the lines overflow the window edges until code fills the whole frame at 4.0 (the code wall). Phrase « il fallait parler » + [pill: sa langue.] at 3.28.

## Frame 2 : Le traducteur

- scene: You speak French to the computer, it only understands code; a translator steps in between and you pay him; his role card flips through developer, agency, provider
- duration: 6.30s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/02-traducteur.html
- voiceover: "Et comme tu ne la parlais pas, tu payais un traducteur, un développeur, une agence, un prestataire."
- type: pain_point
- blueprint: comparison-split (Adapt)
- focal: the gap between you and the computer, then the translator
- rules: card-morph-anchor, kinetic-beat-slam
- world: dark

Word cues: Et@0.04 comme@0.22 tu@0.44 ne@0.56 la@0.72 parlais@0.88 pas@1.02 tu@1.69 payais@1.86 un@2.04 traducteur@2.24 un@3.28 développeur@3.56 une@4.47 agence@4.68 un@5.38 prestataire@5.62 (voice ends 6.10)
Scene 1 (0.0-1.55s): dark stage split in two: persona-toi on the left (x≈420, calm) with a speech-bubble « Je veux un bouton “Réserver”. »; the computer on the right (x≈1500) showing code. At 0.90 the bubble flies toward the computer and bounces off the screen with a small accent ✕ drawn in SVG at 1.02 (it does not understand). Phrase at the top, word by word « Et comme tu ne la parlais pas, ».
Scene 2 (1.55-3.10s): persona-traducteur slides in to the center at 1.60 (expo.out); the bubble now travels persona → translator, turns into a code line, and travels translator → computer, which lights up. At 1.86 a small dark « € » pill travels from persona-toi to the translator. Phrase continues on a new line « tu payais » + [pill: un traducteur,] at 2.04.
Scene 3 (3.10-6.30s): an id-card appears above the translator's head and hard-swaps its content on each beat (→ card-morph-anchor, → kinetic-beat-slam, a tiny camera kick on each swap): « Développeur · TJM 450 € » at 3.28, « Agence · Devis 8 400 € » at 4.47, « Prestataire · Sur devis » at 5.38 (micro label « RÔLE »). Phrase line 3, word by word « un développeur, une agence, un prestataire. ». Hold.

## Frame 3 : La boucle

- scene: The four steps of working through a translator turn around a loop: explain by e-mail, he translates into code, you wait, you pay
- duration: 5.40s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/03-boucle.html
- voiceover: "Tu expliquais ce que tu voulais, il traduisait, tu attendais, tu payais."
- type: pain_point
- blueprint: fixed-anchor-cycle (Adapt)
- focal: the traveling dot on the loop, the station it lights
- rules: svg-path-draw, svg-icon-enrichment
- world: dark

Word cues: Tu@0.10 expliquais@0.32 ce@0.70 que@0.86 tu@0.96 voulais@1.14 il@1.79 traduisait@2.02 tu@2.93 attendais@3.16 tu@4.08 payais@4.30 (voice ends 4.50)
Scene 1 (0.0-5.40s, one continuous shot): a large elliptical loop (accent line, 1300×620, centered) draws itself at 0.0-0.5 (→ svg-path-draw); four stations sit on it at 12, 3, 6 and 9 o'clock, each a small glass-card-dark that lights up (from 40% to 100% opacity, slight scale 0.94→1) when a bright dot traveling along the loop reaches it on its cue: station 1 at 0.10 « EXPLIQUER » = Gmail tool-tile + a mini e-mail card « Objet : bouton de réservation »; station 2 at 1.79 « TRADUIRE » = a mini code-window with 3 canonical code lines; station 3 at 2.93 « ATTENDRE » = a Space Mono counter « J+12 » flipping from « J+1 » by hard cuts; station 4 at 4.08 « PAYER » = Stripe tool-tile + an invoice line « Facture · 850 € ». The phrase sits in the middle of the loop, word by word « Tu expliquais ce que tu voulais, il traduisait, tu attendais, » + [pill: tu payais.] at 4.08. After 4.50 the dot keeps going toward station 1 again (the loop restarts), still.

## Frame 4 : Ça casse, et le curseur

- scene: The delivered site breaks, the loop spins again and again, then everything vanishes and one caret blinks alone in the dark before turning into light
- duration: 4.10s
- transition_in: cut
- status: animated
- src: compositions/frames/04-casse.html
- voiceover: "Et quand ça cassait, tu recommençais."
- type: pain_point
- blueprint: typewriter-reveal (Adapt)
- focal: the broken site, then the lone caret
- rules: chromatic-glitch, vertical-spring-ticker
- world: dark

Word cues: Et@0.38 quand@0.60 ça@0.78 cassait@1.04 tu@1.54 recommençais@1.90 (voice ends 2.48, then silence to the end)
Scene 1 (0.0-1.45s): a site-mock (glass frame, paper body, Studio Lumen) sits centered; at 1.04 it breaks: a short chromatic-glitch (accent + white channels only, 0.25 s, → chromatic-glitch), two blocks drop and tilt, an accent badge « ERREUR 500 » pops. Phrase at the top, word by word « Et quand ça cassait, ».
Scene 2 (1.45-2.60s): the site shrinks into station 1 of a small copy of the loop (same look as frame 3) and the dot runs the loop again, faster on each lap; a Space Mono counter « TOUR 2 » → « TOUR 3 » → « TOUR 4 » rolls under it (→ vertical-spring-ticker, no overshoot). Phrase « tu » + [pill: recommençais.] at 1.54.
Scene 3 (2.60-4.10s): at 2.62 hard cut: everything is gone, empty dark stage (the pivot). Only the caret, dead center (960,540), blinking in finite steps: on 2.70, off 3.10, on 3.40. From 3.55 the caret glows and contracts into a light-point at (960,540) that brightens until the end (the orchestrator's light flood starts from that exact point at 3.75).

## Frame 5 : Aujourd'hui

- scene: On warm paper, « Aujourd’hui, » lands giant; then the code window decodes character by character into a plain French sentence
- duration: 3.10s
- transition_in: cut
- status: animated
- src: compositions/frames/05-aujourdhui.html
- voiceover: "Aujourd'hui, l'ordinateur parle ta langue."
- type: product_intro
- blueprint: titlecard-reveal (Adapt)
- focal: the giant word, then the decoding sentence
- rules: hacker-flip-3d
- world: light

Word cues: Aujourd’hui@0.30 l’ordinateur@1.17 parle@1.84 ta@2.12 langue@2.30 (voice ends 2.63)
Scene 1 (0.0-1.05s): warm paper ground (the light flood has just faded into it); [giant: « Aujourd’hui, »] in ink-dark lands centered at 0.30 with the tracking tighten. Hold.
Scene 2 (1.05-3.10s): hard-cut swap: the giant word is gone; a card-light code-window (~1200×300, centered, slightly above center) shows the first two canonical code lines; from 1.20 every character flips and scrambles (→ hacker-flip-3d, glyphs from the code) and resolves left to right into the French sentence « Ajoute un bouton de réservation sur ma page d’accueil. » in ink-dark ui text (fully resolved by 2.30); the window's micro title changes from « CODE » to « FRANÇAIS ». Phrase lower-center, word by word « l’ordinateur parle » + [pill: ta langue.] at 2.12.

## Frame 6 : Il le construit

- scene: You type your request in French and the page builds itself block by block
- duration: 4.30s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/06-construit.html
- voiceover: "Tu lui écris ce que tu veux, en français. Il le construit."
- type: feature_demo
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the typed request, then the page assembling
- rules: cursor-click-ripple, depth-scatter-assemble
- world: light

Word cues: Tu@0.16 lui@0.30 écris@0.48 ce@0.74 que@0.98 tu@1.12 veux@1.30 en@1.68 français@1.98 Il@2.79 le@2.94 construit@3.20 (voice ends 3.48)
Scene 1 (0.0-2.50s): card-light chat-input (frame.md), large, centered; the request types char by char from 0.25 to 2.20: « Crée une page Tarifs avec mes trois offres. »; phrase at the top, word by word « Tu lui écris ce que tu veux, » + [pill: en français.] at 1.68. The cursor glides to the send button and clicks it at 2.35 (→ cursor-click-ripple).
Scene 2 (2.50-4.30s): the input slides up and away; a site-mock (card-light browser, url « ton-site.fr/tarifs ») assembles from scattered blocks (→ depth-scatter-assemble): nav bar, title « Tarifs », then three offer cards landing one after another at 2.90 / 3.10 / 3.30: « Portrait · 150 € », « Famille · 220 € », « Mariage · 1 200 € », each with a small accent button « Réserver ». Phrase « Il le » + [pill: construit.] at 3.20. Hold.

## Frame 7 : Plus indispensable

- scene: The same three figures as frame 2, now on paper: the translator steps aside and your words go straight to the computer
- duration: 2.90s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/07-indispensable.html
- voiceover: "Le traducteur n'est plus indispensable."
- type: benefit_highlight
- blueprint: comparison-split (Adapt)
- focal: the direct line between you and the computer
- rules: svg-path-draw
- world: light

Word cues: Le@0.21 traducteur@0.42 n’est@0.88 plus@1.14 indispensable@1.36 (voice ends 2.03)
Scene 1 (0.0-2.90s): paper ground; persona-toi left (x≈420), persona-traducteur center, the computer right (x≈1500), same drawings as frame 2. At 0.42 the translator fades to a dashed ink-dark outline (opacity 35%) and glides down and out of frame by 1.30 (power3.in then out of frame). At 1.14 an accent line draws directly from persona-toi's speech-bubble « Je veux un bouton “Réserver”. » to the computer (→ svg-path-draw) and the computer screen switches from code to the French sentence; a small accent check drawn in SVG appears on the screen at 1.50. Phrase at the top, word by word « Le traducteur n’est » + [pill: plus indispensable.] at 1.14. Hold.

## Frame 8 : Savoir quoi dire

- scene: A vague request gets a bland site (it is not enough); then three prompt cards arrive scrambled and snap into the right order
- duration: 7.10s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/08-quoi-dire.html
- voiceover: "Mais parler une langue, ça ne suffit pas. Il faut savoir quoi dire, quoi demander, comment, dans quel ordre."
- type: benefit_highlight
- blueprint: grid-card-assemble (Adapt)
- focal: the bland result, then the three cards snapping into order
- rules: split-tilt-cards, scale-swap-transition
- world: light

Word cues: Mais@0.18 parler@0.40 une@0.62 langue@0.76 ça@1.20 ne@1.38 suffit@1.54 pas@1.78 Il@2.37 faut@2.50 savoir@2.66 quoi@3.06 dire@3.34 quoi@4.10 demander@4.30 comment@5.10 dans@5.73 quel@6.04 ordre@6.12 (voice ends 6.32)
Scene 1 (0.0-2.20s): a small card-light chat-input at the left types « Fais-moi un site. » (0.10-0.60) and sends; on the right a site-mock appears at 0.80, bland on purpose: grey blocks, a placeholder title « Bienvenue sur mon site », no accent, slightly tilted (humor, it is empty). Phrase at the top, word by word « Mais parler une langue, » + [pill: ça ne suffit pas.] at 1.20.
Scene 2 (2.20-3.90s): scale-swap (→ scale-swap-transition) to a clean paper stage: an empty large chat-input centered with only the caret blinking in finite steps. Phrase above it, word by word « Il faut savoir » + [pill: quoi dire,] at 3.06.
Scene 3 (3.90-7.10s): the input shrinks up; three prompt-cards (frame.md prompt-card) land in a scrambled column, each tilted (→ split-tilt-cards): at 4.10 « 1 · QUOI DEMANDER » « Un bouton “Réserver” sur l’accueil », at 5.10 « 2 · COMMENT » « Aux couleurs de ma marque, sous le titre », at 5.73 « 3 · DANS QUEL ORDRE » « D’abord la page, ensuite le bouton ». They arrive in the order 2, 3, 1 positions (visibly out of order); at 6.12 they straighten and snap into the order 1, 2, 3 (power3.out, 0.5 s). Phrase at the bottom, word by word « quoi demander, comment, dans quel ordre. » (no pill: the sentence already has one). Hold.

## Frame 9 : Ça s'apprend

- scene: « s’apprend. » lands giant; the code wall of the opening comes back and falls away; a learning path starts at station 0 « TU ES ICI »
- duration: 6.05s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/09-apprend.html
- voiceover: "Ça, ça s'apprend. Et pas besoin d'être technique, c'est pensé pour ceux qui partent de zéro."
- type: benefit_highlight
- blueprint: titlecard-reveal (Adapt)
- focal: the giant word, then station 0
- rules: svg-path-draw, stat-bars-and-fills
- world: light

Word cues: Ça@0.14 ça@0.67 s’apprend@0.92 Et@1.79 pas@2.04 besoin@2.22 d’être@2.40 technique@2.68 c’est@3.43 pensé@3.70 pour@3.92 ceux@4.16 qui@4.30 partent@4.52 de@4.82 zéro@4.98 (voice ends 5.23)
Scene 1 (0.0-1.60s): paper; phrase small above center « Ça, ça » (0.14, 0.67), then [giant: « s’apprend. »] lands centered at 0.92 with the tracking tighten, the three prompt-cards of frame 8 stacked and slightly fanned BEHIND it (depth). Hold.
Scene 2 (1.60-3.25s): the giant and cards clear; the canonical code lines of frame 1 (ink-dark, 50% opacity, code style) fill the frame again (hook recall) and then fall down and away line by line with a slight blur from 2.40 (it is not needed). Phrase centered, word by word « Et pas besoin d’être technique, ».
Scene 3 (3.25-6.05s): a learning-path (frame.md) draws from left to right (→ svg-path-draw, 3.30-4.40), stations 0 to 4; station 0 at (560,600) lights up in accent with the pin label « TU ES ICI » at 3.70; a thin accent progress fill starts from station 0 and stops just after it (→ stat-bars-and-fills). Phrase at the top, word by word « c’est pensé pour ceux qui partent » + [pill: de zéro.] at 4.82. From 5.60 station 0 glows brighter (the orchestrator's iris opens from (560,600) at 6.05). Hold.

## Frame 10 : Forme-toi pour de bon

- scene: Back on the dark stage: the wordmark assembles under a terracotta wave texture, « Forme-toi pour de bon. » lands, a cursor clicks « Je prends rendez-vous » (identical to film C)
- duration: 7.05s
- transition_in: cut
- status: animated
- src: compositions/frames/10-fin.html
- voiceover: "Entrepreneurs deux point zéro. Forme-toi pour de bon."
- type: cta
- blueprint: logo-assemble-lockup (Adapt)
- focal: the wordmark, then the CTA button
- rules: cursor-click-ripple, press-release-spring
- world: dark

Word cues: Entrepreneurs@0.28 deux-point-zéro@1.09 Forme-toi@2.17 pour@2.61 de@2.87 bon@3.05 (hold to 7.05)
Scene 1-4: the end card of film C (examples/le-devis/compositions/frames/09-fin.html), copied as is: its cues (0.53, 1.11, 2.17, 2.59, 2.81, 2.99) already match this voice within 0.06 s.
