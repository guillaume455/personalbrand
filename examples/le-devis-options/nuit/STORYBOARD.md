---
format: 1920x1080
duration: 43.2s
message: "Tu n'as plus besoin d'un prestataire pour la technique : l'IA le fait, il te reste à apprendre à t'en servir."
arc: Hook → Problem → Stop → Turn → Demo → Payoff → Reassurance → CTA
audience: indépendants et fondateurs de petites structures (France), non techniques, qui paient un prestataire pour chaque modification
mode: autonomous
captions: disabled
music: "pre-mixed with voice and SFX in assets/audio/mix-C-v3.wav (mounted at root by the orchestrator)"
patterns: patterns/PATTERNS.md
---

## Video direction

- **Two lights, one dark room** (frame.md): frames 1-3 = PROBLEM on the cold flat dark stage; frames 4-8 = SOLUTION on the WARM NIGHT stage (ground-warm-night, glass-card-warm, ink text: a warm bloom at the end of frame 3 opens into it); frame 9 = END CARD, dark (the iris from the zero). Never a light full-screen ground. Each frame paints its own full-bleed ground as a `class="clip"` layer.
- **Text** (readable without sound): every sentence of the voice is shown as small centered `phrase` text that arrives WORD BY WORD on the timestamps given in each frame (`word@seconds`, frame-local). Exactly ONE word or group per sentence sits in the traced `accent-pill` (named in the Scene lines as [pill: …]). No other colored or glowing text.
- **Giant words**: only the peaks named in the Scene lines as [giant: …] (« 1 000 € », « Stop. », « Aujourd’hui, », « TOI. ») plus the one [giant-pill: « libre. »], the peak of the film.
- **Motion grammar**: smooth long-tail settles (power3.out default, expo.out for fast arrivals), no bounce. One camera move per scene at most. Holds are still.
- **Visible copy**: exactly the quoted copy of the Scene lines (French, typographic ’, non-breaking spaces before : ? !), nothing else.
- **Negative list**: slideshow (everything at t=0), screensaver (many things floating), colored text instead of the pill, big phrase text, any hue other than terracotta except tool-tile brand colors.

## Frame 1 : Le devis

- scene: A single word opens the film, the client's website appears and gets selected, its cost explodes into a giant 1 000 €, then the quote card fills up
- duration: 5.74s
- transition_in: cut
- status: animated
- src: compositions/frames/01-devis.html
- voiceover: "Une modification sur ton site... une journée. Mille euros. Une nouvelle page : six cents euros."
- type: pain_point
- blueprint: dataviz-countup (Adapt)
- focal: the giant count-up, then the quote card
- rules: cursor-click-ripple, coordinate-target-zoom, counting-dynamic-scale
- world: dark

Word cues: Une@0.00 modification@0.24 sur@0.78 ton@1.04 site@1.18 ?@1.52 Une@1.84 journée@2.02 mille-euros@2.72 Une@3.58 nouvelle@3.74 page@3.98 six-cents-euros@4.74
Scene 1 (0.0-0.75s): first image = the word « Une » ALONE, small, dead center on the dark stage (no logo, no UI). « modification » arrives at 0.24 in a traced accent pill [pill: modification].
Scene 2 (0.60-1.70s): the phrase slides down to the lower third and completes word by word « Une modification sur ton site ? » (sur@0.78 ton@1.04 site@1.18); behind it the website-mock (dark glass frame, paper body) rises into the upper 70% of the frame; a dashed accent selection box draws around the site title and a cursor glides in and clicks it at ~1.20 (→ cursor-click-ripple).
Scene 3 (1.70-3.45s): zoom-through the selection box (→ coordinate-target-zoom) to a clean dark stage: phrase « Une journée. » small at the top (Une@1.84 journée@2.02), then at 2.72 [giant: « 1 000 € »] counts up from 0 and grows with its value (→ counting-dynamic-scale), letter-spacing tightening as it lands; micro label « 1 JOUR DE TRAVAIL » under it.
Scene 4 (3.45-5.74s): cut-the-curve leftward: the giant number exits left at peak velocity while the dark quote card (frame.md quote-card) enters from the right, tilted, row 1 already filled; phrase anchored left « Une nouvelle page : » (Une@3.58 nouvelle@3.74 page@3.98) then [pill: 600 €] at 4.74 while row 2 « Nouvelle page · 600 € » lands in the card and the total badge counts 1 000 → 1 600 € (→ counting-dynamic-scale). Hold.

## Frame 2 : La panne et l'attente

- scene: The automation built with real tools (Google Forms, Gmail, Make, Stripe) breaks at Make, SUR DEVIS slams onto it, then the camera pans to a chat where the provider never answers while the days pile up
- duration: 5.20s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/02-attente.html
- voiceover: "Réparer une automatisation qui a planté : sur devis. Délai... quand il aura le temps."
- type: pain_point
- blueprint: spatial-pan-stations (Adapt)
- focal: the broken Make tile, then the unanswered chat
- rules: svg-path-draw, kinetic-beat-slam, viewport-change
- world: dark

Word cues: Réparer@0.08 une@0.42 automatisation@0.58 qui@1.20 a@1.40 planté@1.54 sur@2.04 devis@2.36 Délai@3.20 quand@3.94 il@4.16 aura@4.30 le@4.46 temps@4.64
Scene 1 (0.0-1.95s): station A: four tool-tiles (frame.md tool-tiles, inline SVG from assets/icons: googleforms, gmail, make, stripe) in a row, revealed left to right from 0.08 while accent links draw between them (→ svg-path-draw) and a bright dot travels along; micro labels under each tile « FORMULAIRE », « E-MAIL », « AUTOMATISATION », « FACTURE ». Phrase at the top, word by word « Réparer une automatisation qui a » + [pill: planté] at 1.54, at the same instant the Make tile shakes, turns grey, an accent badge « ERREUR » pops on it, the link after it goes dashed and dim, the dot dies.
Scene 2 (1.95-2.90s): at 2.04 the stamp « SUR DEVIS » (frame.md stamp) slams onto the row with a tiny camera shake (→ kinetic-beat-slam).
Scene 3 (2.90-5.20s): the camera pans right along the same canvas (→ viewport-change) to station B: a dark glass chat. At 3.20 the outgoing accent bubble « Bonjour, où en est la modification ? » lands; under it the provider's bubble only shows pulsing waiting dots (finite pulses, never answers). Right of the chat, a Space Mono counter with micro label « SANS RÉPONSE DEPUIS » flips « J+1 » (3.94) → « J+3 » (4.30) → « J+8 » (4.66) by hard cut. Phrase at the bottom (above y 900): « Délai : » at 3.20 then [pill: quand il aura le temps.] at 3.94.

## Frame 3 : Le prix à payer, puis Stop

- scene: The entrepreneur, hands on his head, is surrounded by his pain pills and a swarm of quotes; then one word, STOP, freezes everything
- duration: 3.56s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/03-prix.html
- voiceover: "Pendant des années, c'était le prix à payer pour tout ce qui est technique."
- type: pain_point
- blueprint: overwhelm-surround (Adapt)
- focal: the persona, then « Stop. »
- rules: center-outward-expansion, kinetic-beat-slam
- world: dark

Word cues: Pendant@0.08 des@0.34 années@0.54 c’était@0.78 le@1.00 prix@1.20 à@1.30 payer@1.46 pour@1.62 tout@1.88 ce@2.04 qui@2.18 est@2.24 technique@2.36 (silence from 3.11)
Scene 1 (0.0-1.60s): the persona « toi » (frame.md persona, redrawn: forearms raised, two clearly drawn hands gripping the head, worried eyebrows, a sweat drop), big and centered-low (head at y≈560, body cut by the bottom keep-out at y 900), stress strokes popping at 0.2; a slow tremble of the hands (2px, 3 finite cycles). Phrase at the top, word by word « Pendant des années, c’était » + [pill: le prix à payer.] at 1.20.
Scene 2 (1.60-3.05s): from 1.62, pain-pills (Space Mono 24px, bigger than before) pop around the persona one by one (≈0.12 s apart, → center-outward-expansion): « ✕ 1 000 € », « ✕ 600 € », « ✕ Sur devis », « ✕ J+8 », « ✕ Délai », « ✕ Prestataire », « ✕ Réparation »; at the same time a swarm of ~10 small dark quote cards and envelopes with an accent badge fly in from the four edges in 3D rotation and stack around him, crowding the frame (surrounded, not zoomed-into).
Scene 3 (3.05-3.56s): at 3.08 everything vanishes in one frame (hard cut to the empty dark stage) and [giant: « Stop. »] lands dead center as an echo-stack (frame.md echo-stack) with a small camera kick (→ kinetic-beat-slam); hold still. The orchestrator floods the light leak from the center at 3.4.

## Frame 4 : Aujourd'hui

- scene: On the warm night stage, « Aujourd’hui, » lands giant, then the terracotta AI orb appears with the three tasks orbiting around it
- duration: 2.86s
- transition_in: cut
- status: animated
- src: compositions/frames/04-aujourdhui.html
- voiceover: "Sauf qu'aujourd'hui, l'IA sait faire tout ça."
- type: product_intro
- blueprint: constellation-hub (Adapt)
- focal: the orb at the center
- rules: orbit-3d-entry, ambient-glow-bloom
- world: warm-night

Word cues: Sauf@0.44 qu’aujourd’hui@0.60 l’IA@1.54 sait@1.68 faire@1.86 tout@2.04 ça@2.28 (silence until 0.35)
Scene 1 (0.0-1.40s): warm night ground (the warm bloom has just settled into it); micro « SAUF QUE » at 0.30, then [giant: « Aujourd’hui, »] in ink lands centered at 0.44 with the letter-spacing tighten. Hold.
Scene 2 (1.40-2.86s): hard-cut swap: the giant word is gone; a terracotta orb blooms at the center (→ ambient-glow-bloom) and three light cards with a small accent dot « Modifier ton site », « Créer une page », « Réparer une automatisation » flip in from 3D onto an elliptical orbit around it (→ orbit-3d-entry), orbiting slowly (finite tween). Phrase lower-center, word by word « L’IA sait faire » (1.54-1.86) + [pill: tout ça.] at 2.04.

## Frame 5 : Tu lui expliques

- scene: On the warm night stage, a request types itself into a big light chat input, a cursor sends it, and the button appears on the client's website
- duration: 3.24s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/05-demande.html
- voiceover: "Tu lui expliques ce que tu veux avec tes mots. Elle le fait."
- type: feature_showcase
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the chat input, then the new button on the site
- rules: cursor-click-ripple, scale-swap-transition
- world: warm-night

Word cues: Tu@0.00 lui@0.14 expliques@0.32 ce@0.58 que@0.78 tu@0.90 veux@1.04 avec@1.22 tes@1.64 mots@1.80 Elle@2.30 le@2.46 fait@2.72
Scene 1 (0.0-0.40s): a large glass-card-warm chat-input arrives centered (≈75% width) with a short push-in; micro label « TA DEMANDE, EN FRANÇAIS ». Phrase at the top, word by word « Tu lui expliques, » + [pill: avec tes mots.] at 1.22.
Scene 2 (0.20-1.95s): the prompt « Ajoute un bouton « Réserver une séance » sur ma page d’accueil. » types char by char behind an accent caret, ending by 1.90.
Scene 3 (1.90-2.30s): a cursor glides to the send button and clicks it at ~2.10 (→ cursor-click-ripple).
Scene 4 (2.30-3.24s): scale-swap (→ scale-swap-transition): the input shrinks away as the website-mock rises to the same center; at 2.34 the accent button « Réserver une séance » appears in the site with a glow ring and a small mono tag « AJOUTÉ À L’INSTANT »; the top phrase is replaced by « Elle » « le » + [pill: fait.] at 2.72.

## Frame 6 : Toi

- scene: On the warm night stage, the quote card stays pinned while the question rotates and each giant « TOI. » strikes one line
- duration: 5.38s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/06-toi.html
- voiceover: "La modification ? Toi. La page ? Toi. L'automatisation ? Toi."
- type: benefit_highlight
- blueprint: fixed-anchor-cycle (Adapt)
- focal: « TOI. » and the struck lines
- rules: discrete-text-sequence, kinetic-beat-slam
- world: warm-night

Word cues: La-modification@0.08 ?@0.88 Toi@1.22 La-page@1.88 ?@2.46 Toi@2.80 L’automatisation@3.48 ?@4.40 Toi@4.68
Scene 1 (0.0-0.30s): the glass-card-warm quote card (4 rows + accent total badge « 1 600 € ») enters from the left and pins in the left 45% of the frame; it never moves again.
Scene 2 (0.08-1.80s): right region: phrase-size question « La modification ? » at 0.08; at 1.22 [giant: « TOI. »] slams in under it in ink with the letter-spacing tighten (→ kinetic-beat-slam) and, in the card, row 1 gets struck (✕, accent line, price flips to « toi »).
Scene 3 (1.80-3.40s): in-place token swap (→ discrete-text-sequence): the question becomes « La page ? » at 1.88; « TOI. » re-slams at 2.80; row 2 struck.
Scene 4 (3.40-5.38s): swap to « L’automatisation ? » at 3.48; « TOI. » at 4.68; row 3 struck; at 5.00 row 4 « Délai » flips to « maintenant » and the total badge fades to 30%. Hold.

## Frame 7 : Il ne reste qu'une ligne

- scene: On the warm night stage, the struck quote shows one last glowing line; the camera dives into it; then the phrase « C’est la seule qui te rend libre. » lands
- duration: 5.92s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/07-ligne.html
- voiceover: "Il ne reste qu'une ligne sur le devis... apprendre à t'en servir. Et c'est la seule qui te rend libre."
- type: benefit_highlight
- blueprint: titlecard-reveal (Adapt)
- focal: the last line, then the title
- rules: coordinate-target-zoom, motion-blur-streak
- world: warm-night

Word cues: Il@0.08 ne@0.24 reste@0.44 qu’une@0.64 ligne@0.96 sur@1.14 le@1.36 devis@1.52 Apprendre@2.26 à@2.60 t’en@2.72 servir@2.92 c’est@3.86 la@4.06 seule@4.28 qui@4.46 te@4.64 rend@4.82 libre@4.96
Scene 1 (0.0-2.10s): the glass-card-warm quote seen straight-on, centered, all four rows struck; phrase above, word by word « Il ne reste » + [pill: qu’une ligne] at 0.64 « sur le devis. »; at 1.20 a new last row assembles at the bottom of the card: an accent-bordered empty line with micro label « LA SEULE LIGNE QUI RESTE ».
Scene 2 (2.10-3.60s): the camera zooms into that last line until it fills the frame (→ coordinate-target-zoom); inside it « Apprendre à » + [pill: t’en servir] writes word by word from 2.26 while a terracotta comet streaks behind (→ motion-blur-streak).
Scene 3 (3.60-5.92s): inverse zoom-through back to the warm night stage where the struck quote card sits centered; phrase small at the top, word by word « C’est la seule qui te rend » (3.86 → 4.82); at 4.70 the struck quote card lifts off (scale 1 → 0.9, rotation to -14deg) and flies out to the top-right with a slight motion blur (power3.in, gone by 5.10: the old way leaves); at 4.96 [giant-pill: « libre. »] (frame.md giant-pill) lands dead center where the card was: the giant terracotta pill traces, then « libre. » writes inside in white with the tracking tighten. This is the emotional peak of the film: hold still to the end.

## Frame 8 : Pas besoin d'être technique

- scene: On the warm night stage, code fades out behind « Pas besoin d’être technique », then a giant outlined zero fills with terracotta next to « pensé pour ceux qui partent de zéro »
- duration: 4.25s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/08-zero.html
- voiceover: "Et pas besoin d'être technique. C'est pensé pour ceux qui partent de zéro."
- type: benefit_highlight
- blueprint: kinetic-type-beats (Adapt)
- focal: the phrase, then the giant zero
- rules: stat-bars-and-fills
- world: warm-night

Word cues: Et@0.10 pas@0.20 besoin@0.40 d’être@0.56 technique@0.82 C’est@1.76 pensé@1.88 pour@2.12 ceux@2.36 qui@2.46 partent@2.68 de@2.98 zéro@3.14 (silence from 3.82)
Scene 1 (0.0-1.60s): background: a tilted glass-card-warm code editor (Space Mono, ~8 lines of JavaScript, keywords in accent) that blurs and fades to 15% from 0.2; foreground centered phrase word by word « Pas besoin d’être » + [pill: technique.] at 0.82.
Scene 2 (1.60-3.80s): cut-the-curve upward to a 50/50 split: left phrase word by word « C’est pensé pour ceux qui partent » + [pill: de zéro.] at 2.98; right, a giant outlined « 0 » (numeral-jumbo, 4px accent stroke, no fill) that fills with terracotta from the bottom up at 3.14 (→ stat-bars-and-fills).
Scene 3 (3.80-4.25s): the filled zero's center brightens into a hot bloom; the orchestrator opens the iris to the dark end card from its center (x≈1400, y≈450).

## Frame 9 : Forme-toi pour de bon

- scene: Back on the dark stage: the wordmark assembles under a terracotta wave texture, « Forme-toi pour de bon. » lands, a cursor clicks « Je prends rendez-vous »
- duration: 7.05s
- transition_in: cut
- status: animated
- src: compositions/frames/09-fin.html
- voiceover: "Entrepreneurs deux point zéro. Forme-toi pour de bon."
- type: cta
- blueprint: logo-assemble-lockup (Adapt)
- focal: the wordmark, then the CTA button
- rules: cursor-click-ripple, press-release-spring
- world: dark

Word cues: Entrepreneurs@0.53 deux-point-zéro@1.11 Forme-toi@2.17 pour@2.59 de@2.81 bon@2.99 (hold to 7.05)
Scene 1 (0.0-1.90s): dark stage with a terracotta wave texture across the top third (~34 thin wavy lines fading down and to the sides) and a warm halo; the wordmark « ENTREPRENEURS » (Big Shoulders, ink) cascades in letter by letter from 0.53, then « 2.0 » lands in accent at 1.11. Upper-center.
Scene 2 (1.90-3.20s): below it, phrase-size but larger (72px) « Forme-toi » at 2.17 + [pill: pour de bon.] at 2.59.
Scene 3 (3.20-4.60s): the sub-line « Pensé pour ceux qui ne sont pas techniques. » (ui, ink-soft) at 3.30; the CTA button « JE PRENDS RENDEZ-VOUS → » (paper fill, accent-deep Big Shoulders text, soft terracotta glow) arrives at 3.60 on a smooth settle; mono URL « entrepreneurs2-0.com » at 4.00.
Scene 4 (4.60-7.05s): a cursor glides in and clicks the button at ~5.20 (→ cursor-click-ripple, → press-release-spring); then everything holds STILL to the end.
