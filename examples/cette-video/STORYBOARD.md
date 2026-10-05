---
format: 1920x1080
duration: 44.6s
message: "Cette vidéo a été faite par une IA à qui on a expliqué, avec des mots simples, ce qu'on voulait : pour ton site, tes outils et tes automatisations c'est pareil, il te suffit d'apprendre à demander."
arc: Hook (self-reference) → Credits → Voice → Making-of → Flashback « Avant » → Transfer → Lesson → Reassurance → CTA
audience: indépendants et fondateurs de petites structures (France), non techniques, qui paient un prestataire pour chaque modification
mode: autonomous
captions: disabled
music: "pre-mixed with voice and SFX in assets/audio/mix-A.wav (mounted at root by the orchestrator)"
patterns: patterns/PATTERNS.md
---

## Video direction

- **Worlds** (frame.md): frames 1-3 = the claim on the dark stage (film credits); frame 4 = the making-of on warm paper (a light flood opens into it); frame 5 = « Avant » rewinds into the dark stage; frames 6-10 = the lesson on paper; frame 11 = END CARD back on the dark stage (the iris from the play button). Each frame paints its own full-bleed ground as a `class="clip"` layer.
- **Text** (readable without sound): every sentence of the voice is shown as small centered `phrase` text that arrives WORD BY WORD on the timestamps given in each frame (`word@seconds`, frame-local). At most ONE word or group per sentence sits in the traced `accent-pill` (named in the Scene lines as [pill: …]). No other colored or glowing text.
- **Giant words**: only « Avant, » and « s’apprend. » (named as [giant: …]).
- **Recurring objects** (frame.md): the video-player (frames 1 and 10), persona-toi, role-cards, chat-input, the caret. They must look the same in every frame they appear in.
- **Motion grammar**: smooth long-tail settles (power3.out default, expo.out for fast arrivals), no bounce. One camera move per scene at most. Holds are still.
- **Visible copy**: exactly the quoted copy of the Scene lines (French, typographic ’, non-breaking spaces before : ? !), nothing else.
- **Negative list**: slideshow (everything at t=0), screensaver (many things floating), colored text instead of the pill, big phrase text, any hue other than terracotta except tool-tile brand colors.

## Frame 1 : Cette vidéo

- scene: The words « Cette vidéo, » alone, then the whole screen pulls back into a video player that contains itself, level after level
- duration: 2.25s
- transition_in: cut
- status: animated
- src: compositions/frames/01-cette-video.html
- voiceover: "Cette vidéo, aucune agence ne l'a faite."
- type: hook
- blueprint: zoom-out-workspace-reveal (Adapt)
- focal: the player that contains itself
- rules: coordinate-target-zoom
- world: dark

Word cues: Cette@0.03 vidéo@0.28 aucune@0.85 agence@1.12 ne@1.40 l’a@1.55 faite@1.75 (voice ends 2.03)
Scene 1 (0.0-0.80s): first image = « Cette vidéo, » ALONE, small phrase text dead center on the dark stage (Cette@0.03, vidéo@0.28), nothing else.
Scene 2 (0.80-2.25s): one unbroken decelerating pull-back (0.80-1.70, expo.out): the whole screen, phrase included, shrinks into the screen of a video-player (glass-card-dark, 1100×620 at the end, centered slightly above center) whose screen shows the same image again, 4 nested levels deep (Droste, frame.md video-player); the timecode reads « 0:01 / 0:44 », the playhead moves slightly. The phrase re-appears under the player (above y 900), word by word « aucune agence ne l’a faite. » with [pill: aucune agence] at 0.85. Hold from 1.9.

## Frame 2 : Le générique

- scene: Film credits roll on the black stage, and the names are all « aucun »
- duration: 2.85s
- transition_in: cut
- status: animated
- src: compositions/frames/02-generique.html
- voiceover: "Aucun motion designer. Aucun studio."
- type: pain_point
- blueprint: titlecard-reveal (Adapt)
- focal: the credit names
- rules: discrete-text-sequence, kinetic-beat-slam
- world: dark

Word cues: Aucun@0.07 motion@0.39 designer@0.69 aucun@1.38 studio@1.75 (voice ends 2.08)
Scene 1 (0.0-2.85s, one continuous shot): classic film credits (frame.md credits) centered, the column rolling slowly upward (linear, ~60 px over the frame). Block 1 at 0.0: role « RÉALISATION », name « Une vidéo Entrepreneurs 2.0 ». Block 2: role « MOTION DESIGN » appears at 0.05, its name writes word by word « Aucun motion designer. » (Aucun@0.07, motion@0.39, designer@0.69). Block 3: role « STUDIO » appears at 1.30, its name « Aucun studio. » writes with « Aucun » at 1.38 then [pill: studio.] at 1.75, a tiny camera kick on the pill (→ kinetic-beat-slam). Block 4 at 2.10, dimmer: role « AGENCE », name «, ». Hold, the roll keeps drifting.

## Frame 3 : Cette voix

- scene: The real waveform of this voice plays across the screen; a voice-actor casting card is struck; the waveform collapses into a point of light
- duration: 3.15s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/03-voix.html
- voiceover: "Et cette voix ? Ce n'est pas un comédien non plus."
- type: pain_point
- blueprint: video-text-pivot (Adapt)
- focal: the waveform, then the struck casting card
- rules: stat-bars-and-fills, svg-path-draw
- world: dark

Word cues: Et@0.21 cette@0.40 voix@0.62 Ce@1.34 n’est@1.45 pas@1.58 un@1.70 comédien@1.88 non@2.18 plus@2.40 (voice ends 2.64)
Scene 1 (0.0-1.25s): a wide waveform (frame.md waveform, 72 bars across 1500 px, centered at y 470) grows in from the center line (bars scale from 0, 0.0-0.5, → stat-bars-and-fills); its heights are the REAL envelope of this voice (given in the dispatch); an accent playhead sweeps left to right over the whole frame duration (0.0-2.85, linear), the bars it passes turn accent-light. Phrase at the top, word by word « Et cette voix ? ».
Scene 2 (1.25-2.85s): a casting-card (frame.md, « CASTING », « Comédien voix off », « 450 € / session ») rises under the waveform at 1.34; at 1.88 an accent line draws across its title (→ svg-path-draw) and the card dims to 45%. Phrase replaces the first one at the top, word by word « Ce n’est pas un comédien » + [pill: non plus.] at 2.18.
Scene 3 (2.85-3.15s): the waveform and the card collapse fast into a light-point at (960,540) (power3.in); the orchestrator's light flood starts from that exact point at 2.90.

## Frame 4 : Elle a tout construit

- scene: On paper, a request typed in plain words; then the editor timeline of this very film fills itself
- duration: 5.15s
- transition_in: cut
- status: animated
- src: compositions/frames/04-construit.html
- voiceover: "Tout a été expliqué à l'IA, avec des mots simples. Et elle a tout construit."
- type: product_intro
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the typed request, then the timeline filling
- rules: waterfall-entry, cursor-click-ripple
- world: light

Word cues: Tout@0.20 a@0.35 été@0.49 expliqué@0.80 à@1.20 l’IA@1.37 avec@1.76 des@2.01 mots@2.17 simples@2.31 et@3.07 elle@3.20 a@3.35 tout@3.47 construit@3.75 (voice ends 4.17)
Scene 1 (0.0-2.75s): paper ground (the light flood fades into it during the first 0.4 s: keep that time calm); a card-light chat-input (frame.md) centered, micro label « TA DEMANDE, EN FRANÇAIS »; from 0.40 to 2.40 it types char by char « Fais-moi une vidéo de 40 secondes pour ma page d’accueil. Le message : plus besoin d’agence. »; the cursor clicks the send button at 2.55 (→ cursor-click-ripple). Phrase at the top, word by word « Tout a été expliqué à l’IA, avec » + [pill: des mots simples.] at 2.01.
Scene 2 (2.75-5.15s): the input slides up and out; a timeline-editor (frame.md) rises in its place and fills itself (→ waterfall-entry): eleven thumbnail blocks drop into the IMAGE track left to right from 2.95 to 3.90, each with one tiny word « Cette vidéo », « Générique », « Voix », « Construit », « Avant », « Pareil », « Demander », « S’apprend », « Activité », « Zéro », « Fin »; the VOIX waveform and the MUSIQUE bar draw in at 3.60; the playhead runs from 3.75 to the end. Phrase replaces the first one, word by word « Et elle a » + [pill: tout construit.] at 3.47. Hold.

## Frame 5 : Avant

- scene: A rewind into the dark stage; « Avant, » giant; then the old way: an agency, a quote, and a wait counter that keeps climbing
- duration: 4.10s
- transition_in: cut
- status: animated
- src: compositions/frames/05-avant.html
- voiceover: "Avant, pour ça, il fallait une agence, un devis, et attendre."
- type: pain_point
- blueprint: spatial-pan-stations (Adapt)
- focal: the giant word, then the quote and the wait counter
- rules: chromatic-glitch, vertical-spring-ticker
- world: dark

Word cues: Avant@0.19 pour@0.56 ça@0.72 il@1.24 fallait@1.40 une@1.58 agence@1.78 un@2.30 devis@2.44 et@2.90 attendre@3.15 (voice ends 3.51)
Scene 1 (0.0-1.15s): rewind: a brief band of horizontal scanlines and a chromatic split (accent + white only, 0.25 s, → chromatic-glitch) sweeps up the dark stage with a rewind mark « ◀◀ » drawn in SVG (two accent triangles) at the top-left; then [giant: « Avant, »] lands centered at 0.19 with the tracking tighten; the small phrase « pour ça, » under it (0.56, 0.72).
Scene 2 (1.15-4.10s): the camera pans right along two stations (→ viewport-change feel, one move): station A at 1.24 a role-card « Agence » + a dark quote card « DEVIS N° 0212 », « Vidéo motion design 45 s », price « 4 800 € » (lands at 2.30); station B at 2.90 a Space Mono counter with micro label « LIVRAISON DANS » that rolls « J+1 » → « J+42 » (→ vertical-spring-ticker, no overshoot, lands at 3.60). Phrase at the bottom, word by word « il fallait une agence, un devis, » + [pill: et attendre.] at 2.90.

## Frame 6 : Exactement pareil

- scene: On paper, your site, your tools and your automations arrive one per beat, then line up with the video player: it is exactly the same
- duration: 4.45s
- transition_in: cut
- status: animated
- src: compositions/frames/06-pareil.html
- voiceover: "Ton site, tes outils, tes automatisations : c'est exactement pareil."
- type: benefit_highlight
- blueprint: constellation-hub (Adapt)
- focal: the three objects snapping into one row with the player
- rules: svg-icon-enrichment, svg-path-draw
- world: light

Word cues: Ton@0.20 site@0.40 tes@0.82 outils@1.00 tes@1.46 automatisations@1.58 c’est@2.66 exactement@2.98 pareil@3.44 (voice ends 4.04)
Scene 1 (0.0-2.50s): hard cut to paper. Three objects land one per beat around the center: at 0.20 a small site-mock (card-light, « Studio Lumen », url « ton-site.fr »); at 0.82 four tool-tiles (gmail, notion, stripe, make; inline SVG from assets/icons, brand colors, → svg-icon-enrichment); at 1.46 an automation chain: the tiles get linked by accent lines that draw (→ svg-path-draw) with a dot traveling once. Phrase at the top, word by word « Ton site, tes outils, tes automatisations : ».
Scene 2 (2.50-4.45s): everything glides into one horizontal row at y≈470: a small video-player (card-light, same drawing as frame 1) « = » site « = » tools « = » automation (the « = » signs in ink-dark ui, 44px). Phrase moves under the row, word by word « c’est » + [pill: exactement pareil.] at 2.98. Hold.

## Frame 7 : Savoir demander

- scene: The person who knows how steps aside; what remains is a well-written request
- duration: 4.20s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/07-demander.html
- voiceover: "Tu n'as plus besoin de quelqu'un qui sait faire. Tu as besoin de savoir demander."
- type: benefit_highlight
- blueprint: comparison-split (Adapt)
- focal: the request being typed
- rules: card-morph-anchor
- world: light

Word cues: Tu@0.27 n’as@0.37 plus@0.51 besoin@0.71 de@0.89 quelqu’un@1.11 qui@1.39 sait@1.59 faire@1.79 Tu@2.50 as@2.61 besoin@2.77 de@2.97 savoir@3.17 demander@3.51 (voice ends 3.96)
Scene 1 (0.0-2.30s): paper, split: on the left a role-card « Quelqu’un qui sait faire » (card-light, micro « RÔLE ») with persona-traducteur (frame.md) above it; on the right an empty chat-input. At 1.59 the left side dims to 30% and slides left out of frame by 2.30 (power3.in). Phrase at the top, word by word « Tu n’as plus besoin de quelqu’un qui sait faire. ».
Scene 2 (2.30-4.20s): the chat-input glides to the center and grows (→ card-morph-anchor); it types char by char from 2.50 to 3.80 « Ajoute un bouton “Réserver” sous le titre, aux couleurs de ma marque. ». Phrase replaces the first one, word by word « Tu as besoin de » + [pill: savoir demander.] at 3.17. Hold.

## Frame 8 : Ça s'apprend

- scene: « s’apprend. » lands giant and an accent underline draws under it like a pen stroke
- duration: 2.25s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/08-apprend.html
- voiceover: "Et ça, ça s'apprend."
- type: benefit_highlight
- blueprint: titlecard-reveal (Adapt)
- focal: the giant word
- rules: svg-path-draw
- world: light

Word cues: Et@0.16 ça@0.30 ça@0.84 s’apprend@1.07 (voice ends 1.35)
Scene 1 (0.0-2.25s): paper; small phrase above center « Et ça, ça » (0.16, 0.30, 0.84); [giant: « s’apprend. »] lands centered at 1.07 with the tracking tighten; at 1.30 a hand-drawn-looking accent underline (one SVG path, slightly wavy, 10px stroke, round caps) draws under it left to right in 0.45 s (→ svg-path-draw). Hold.

## Frame 9 : Sur ton activité

- scene: You at your laptop, your own business around you; the strings that tied you to a developer, an agency and a provider snap one by one
- duration: 4.15s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/09-activite.html
- voiceover: "C'est ce qu'on t'apprend, sur ton activité. Pour que tu ne dépendes plus de personne."
- type: benefit_highlight
- blueprint: constellation-hub (Adapt)
- focal: persona-toi, then the snapping strings
- rules: svg-path-draw
- world: light

Word cues: C’est@0.10 ce@0.36 qu’on@0.46 t’apprend@0.60 sur@0.90 ton@1.12 activité@1.32 pour@2.36 que@2.48 tu@2.66 ne@2.76 dépendes@2.84 plus@3.16 de@3.32 personne@3.52 (voice ends 3.89)
Scene 1 (0.0-2.20s): paper; persona-toi (frame.md, calm) center-low at (960,560) behind a small laptop whose screen shows a tiny site-mock « Studio Lumen »; three role-cards (card-light) around him at left (« Développeur »), top-right (« Agence ») and right (« Prestataire »), each tied to him by a thin ink-dark string (SVG line). Phrase at the top, word by word « C’est ce qu’on t’apprend, » + [pill: sur ton activité.] at 0.90.
Scene 2 (2.20-4.15s): the strings snap one by one at 2.84, 3.16 and 3.52 (each line splits in the middle, the two halves recoil and fade, → svg-path-draw in reverse), and each role-card drifts away and fades after its string snaps. Phrase replaces the first one, word by word « Pour que tu ne dépendes plus » + [pill: de personne.] at 3.32. Hold.

## Frame 10 : De zéro

- scene: Jargon words fall away; the video player of the opening comes back on paper, rewound to 0:00, its play button glowing
- duration: 4.75s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/10-zero.html
- voiceover: "Et pas besoin d'être technique : c'est pensé pour ceux qui partent de zéro."
- type: benefit_highlight
- blueprint: video-text-pivot (Adapt)
- focal: the play button
- rules: stat-bars-and-fills
- world: light

Word cues: Et@0.15 pas@0.31 besoin@0.47 d’être@0.70 technique@0.95 c’est@1.91 pensé@2.07 pour@2.33 ceux@2.57 qui@2.69 partent@2.89 de@3.15 zéro@3.33 (voice ends 3.66)
Scene 1 (0.0-1.75s): paper; technical words scattered around the center in Space Mono (ink-dark, 50%): « API », « DNS », « webhook », « JSON », « CSS », « SSL », « FTP », « cron »; from 0.95 they fall down and away one by one with a slight blur (they are not needed). Phrase centered, word by word « Et pas besoin d’être technique : ».
Scene 2 (1.75-4.75s): the video-player of frame 1 (card-light version, 1000×560) rises to the center at 1.80, its screen shows the paper world; the playhead slides back to the start (→ stat-bars-and-fills, played part shrinking to 0) while the timecode rolls down to « 0:00 / 0:44 » by 3.15; the play button (56px accent disc) sits EXACTLY at (960, 460) and glows brighter from 3.60. Phrase under the player, word by word « c’est pensé pour ceux qui partent » + [pill: de zéro.] at 3.15. Hold (the orchestrator's iris opens from (960,460) at 4.75).

## Frame 11 : Forme-toi pour de bon

- scene: Back on the dark stage: the end card of films B and C
- duration: 7.30s
- transition_in: cut
- status: animated
- src: compositions/frames/11-fin.html
- voiceover: "Entrepreneurs deux point zéro. Forme-toi pour de bon."
- type: cta
- blueprint: logo-assemble-lockup (Adapt)
- focal: the wordmark, then the CTA button
- rules: cursor-click-ripple, press-release-spring
- world: dark

Word cues: Entrepreneurs@0.09 deux-point-zéro@0.70 Forme-toi@2.04 pour@2.91 de@3.05 bon@3.15 (hold to 7.30)
Scene 1-4: the end card of film C, copied and retimed to this voice (compositions/frames/11-fin.html, already animated).
