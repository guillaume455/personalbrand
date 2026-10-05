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

- **One desk, two lights** (frame.md): the camera looks straight down at a desk. Frames 1-3 = PROBLEM at night (desk-night, lamp pool, long shadows); frames 4-8 = SOLUTION in the morning (desk-day, window light); frame 9 = END CARD on the dark stage (the iris from the zero). Each frame paints its own full-bleed desk as a `class="clip"` layer. Camera moves are top-down pans, push-ins and pull-backs over the same desk.
- **Physical objects** carry the story: sheets of paper, rubber stamps, a tear-off calendar, a phone, a laptop, a terracotta pen. They land like real paper (fast in, soft landing, tiny rotation settle), never bounce.
- **Text** (readable without sound): every sentence of the voice is small `phrase` text in a band at the top or bottom (the Scene says which), WORD BY WORD on its timestamp. One word or group per sentence in the traced `accent-pill` ([pill: …]). Printed text on papers is part of the objects.
- **Giant**: « 1 000 € » (printed huge on the quote under a push-in), « STOP. » (a giant rubber stamp), « Aujourd’hui, », « TOI. », and the one [giant-pill: « libre. »].
- **Visible copy**: exactly the quoted copy of the Scene lines and the components of frame.md, nothing else.
- **Negative list**: slideshow, screensaver, colored text instead of the pill, yellow sticky notes, any hue other than terracotta, wood and paper (except tool tiles), bouncy eases.

## Frame 1 : Le devis

- scene: At night under the lamp, one word, then a quote sheet slides onto the desk, its first price counts up to a huge 1 000 € and gets circled in terracotta, then a second line adds 600 €
- duration: 5.74s
- transition_in: cut
- status: animated
- src: compositions/frames/01-devis.html
- voiceover: "Une modification sur ton site... une journée. Mille euros. Une nouvelle page : six cents euros."
- type: pain_point
- blueprint: dataviz-countup (Adapt)
- focal: the quote sheet, then the huge price
- rules: coordinate-target-zoom, counting-dynamic-scale
- world: desk-night

Word cues: Une@0.00 modification@0.24 sur@0.78 ton@1.04 site@1.18 ?@1.52 Une@1.84 journée@2.02 mille-euros@2.72 Une@3.58 nouvelle@3.74 page@3.98 six-cents-euros@4.74
Scene 1 (0.0-0.75s): first image = the word « Une » ALONE, small phrase text dead center on the dark desk in the lamp pool (no logo, no object). « modification » arrives at 0.24 in a traced accent pill [pill: modification].
Scene 2 (0.60-1.70s): the phrase slides down to the bottom band and completes word by word « Une modification sur ton site ? » (sur@0.78 ton@1.04 site@1.18); from the top edge a quote-sheet (frame.md) slides onto the desk into the lamp pool with a tiny rotation settle; its header « DEVIS N° 0147 · Prestations web » is printed; at 1.18 its first row types itself: « Modification sur ton site · 1 jour ».
Scene 3 (1.70-3.45s): the camera pushes in on the price column of row 1 until it fills the frame (→ coordinate-target-zoom); phrase at the top « Une journée. » (Une@1.84 journée@2.02); at 2.72 [giant: « 1 000 € »] prints on the paper, counting up from 0 (→ counting-dynamic-scale, tabular), then at 3.00 a terracotta pen stroke circles it (a hand-drawn ellipse drawn with stroke-dashoffset, 6px, round caps).
Scene 4 (3.45-5.74s): the camera pulls back to the whole sheet, slightly tilted on the desk; phrase at the bottom « Une nouvelle page : » (Une@3.58 nouvelle@3.74 page@3.98) then [pill: 600 €] at 4.74 while row 2 « Nouvelle page · 600 € » types itself and the total box rolls 1 000 → 1 600 €. Hold.

## Frame 2 : La panne et l'attente

- scene: The camera pans along the night desk: a sticky note with the automation gets crossed out and torn, a SUR DEVIS stamp slams on it, then a phone with an unanswered message and a tear-off calendar losing its days
- duration: 5.20s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/02-attente.html
- voiceover: "Réparer une automatisation qui a planté : sur devis. Délai... quand il aura le temps."
- type: pain_point
- blueprint: spatial-pan-stations (Adapt)
- focal: the torn sticky note, then the calendar
- rules: svg-path-draw, kinetic-beat-slam
- world: desk-night

Word cues: Réparer@0.08 une@0.42 automatisation@0.58 qui@1.20 a@1.40 planté@1.54 sur@2.04 devis@2.36 Délai@3.20 quand@3.94 il@4.16 aura@4.30 le@4.46 temps@4.64
Scene 1 (0.0-1.95s): station A: a sticky-note (frame.md, paper-2, 420px, slight rotation) on the night desk; on it four small tool-tiles (googleforms, gmail, make, stripe) get linked by hand-drawn ink lines from 0.08 (→ svg-path-draw). Phrase at the top, word by word « Réparer une automatisation qui a » + [pill: planté] at 1.54; at the same instant a terracotta pen scribble crosses out the Make tile and the note tears in two along a jagged line (the two halves drift 30px apart and rotate a little).
Scene 2 (1.95-2.90s): at 2.04 a rubber-stamp « SUR DEVIS » (frame.md) slams onto the torn note with a tiny camera shake (→ kinetic-beat-slam).
Scene 3 (2.90-5.20s): the camera pans right along the same desk to station B: a smartphone (frame.md) lying on the desk, its screen showing the outgoing bubble « Bonjour, où en est la modification ? » landing at 3.20 and a gray bubble with waiting dots that never answers; next to the phone a tear-off-calendar showing « J+1 »: its top sheet is torn off at 4.30 revealing « J+3 », torn off again at 4.66 revealing « J+8 ». Phrase at the bottom: « Délai : » at 3.20 then [pill: quand il aura le temps.] at 3.94.

## Frame 3 : Le prix à payer, puis STOP

- scene: Papers pile up on the night desk until they bury it, then one giant STOP stamp freezes everything
- duration: 3.56s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/03-prix.html
- voiceover: "Pendant des années, c'était le prix à payer pour tout ce qui est technique."
- type: pain_point
- blueprint: overwhelm-surround (Adapt)
- focal: the pile, then the STOP stamp
- rules: center-outward-expansion, kinetic-beat-slam
- world: desk-night

Word cues: Pendant@0.08 des@0.34 années@0.54 c’était@0.78 le@1.00 prix@1.20 à@1.30 payer@1.46 pour@1.62 tout@1.88 ce@2.04 qui@2.18 est@2.24 technique@2.36 (silence from 3.11)
Scene 1 (0.0-1.60s): the camera is higher above the night desk (wider view); sheets start dropping onto the desk one after another from above (quote sheets, sheets titled « FACTURE », envelopes, sticky notes), each landing with a soft shadow and a tiny rotation. Phrase at the top, word by word « Pendant des années, c’était » + [pill: le prix à payer.] at 1.20.
Scene 2 (1.60-3.05s): from 1.62 the drops accelerate (→ center-outward-expansion): ~16 papers in total, overlapping, until the desk is buried; pain-pills are printed on some of them as they land, one by one ≈0.12 s apart: « ✕ 1 000 € », « ✕ 600 € », « ✕ Sur devis », « ✕ J+8 », « ✕ Délai », « ✕ Prestataire », « ✕ Réparation »; the lamp pool dims slightly (the room gets heavier).
Scene 3 (3.05-3.56s): at 3.08 [giant: « STOP. »] as a giant rubber-stamp (frame.md, ~260px text, 12px border) slams dead center across the pile with a hard camera kick (→ kinetic-beat-slam); everything freezes, hold still. The orchestrator floods morning light from the center at 3.4.

## Frame 4 : Aujourd'hui

- scene: Morning light on a clean desk, « Aujourd’hui, » lands giant, then a laptop with the AI orb and three sticky notes of tasks around it
- duration: 2.86s
- transition_in: cut
- status: animated
- src: compositions/frames/04-aujourdhui.html
- voiceover: "Sauf qu'aujourd'hui, l'IA sait faire tout ça."
- type: product_intro
- blueprint: constellation-hub (Adapt)
- focal: the laptop and its orb
- rules: ambient-glow-bloom
- world: desk-day

Word cues: Sauf@0.44 qu’aujourd’hui@0.60 l’IA@1.54 sait@1.68 faire@1.86 tout@2.04 ça@2.28 (silence until 0.35)
Scene 1 (0.0-1.40s): the desk-day ground, clean, with window light bands (the light flood has just settled into it: keep the first 0.35 s calm); micro « SAUF QUE » at 0.30, then [giant: « Aujourd’hui, »] in ink-dark lands centered at 0.44 with the tracking tighten. Hold.
Scene 2 (1.40-2.86s): hard-cut swap: the giant word is gone; an open laptop (frame.md, top-down) sits in the center, its screen dark with a terracotta orb blooming (→ ambient-glow-bloom); three sticky-notes « Modifier ton site », « Créer une page », « Réparer une automatisation » slide in from three sides and land around the laptop, one per beat. Phrase at the bottom, word by word « L’IA sait faire » (1.54-1.86) + [pill: tout ça.] at 2.04.

## Frame 5 : Tu lui expliques

- scene: The camera dives onto the laptop screen: the request types itself in plain French, a click, and the button appears on the client's website
- duration: 3.24s
- transition_in: push-slide UP
- status: animated
- src: compositions/frames/05-demande.html
- voiceover: "Tu lui expliques ce que tu veux avec tes mots. Elle le fait."
- type: feature_showcase
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the chat input, then the new button on the site
- rules: cursor-click-ripple, coordinate-target-zoom
- world: desk-day

Word cues: Tu@0.00 lui@0.14 expliques@0.32 ce@0.58 que@0.78 tu@0.90 veux@1.04 avec@1.22 tes@1.64 mots@1.80 Elle@2.30 le@2.46 fait@2.72
Scene 1 (0.0-0.40s): top-down desk-day, the laptop centered; the camera pushes in onto its screen until the screen fills ~80% of the frame (the keyboard edge and the desk still visible at the bottom and the sides) (→ coordinate-target-zoom).
Scene 2 (0.20-1.95s): on the screen, a light chat-input with micro label « TA DEMANDE, EN FRANÇAIS »; the prompt « Ajoute un bouton « Réserver une séance » sur ma page d’accueil. » types char by char behind an accent caret, ending by 1.90. Phrase at the top band, word by word « Tu lui expliques, » + [pill: avec tes mots.] at 1.22.
Scene 3 (1.90-2.30s): a cursor glides to the send button and clicks it at ~2.10 (→ cursor-click-ripple).
Scene 4 (2.30-3.24s): the screen switches to the client's website (Studio Lumen, url « ton-site.fr »); at 2.34 the accent button « Réserver une séance » appears with a glow ring and a small mono tag « AJOUTÉ À L’INSTANT »; the top phrase is replaced by « Elle » « le » + [pill: fait.] at 2.72.

## Frame 6 : Toi

- scene: The quote sheet on the morning desk; the terracotta pen strikes one line per beat, and each time a giant « TOI. » slams next to it
- duration: 5.38s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/06-toi.html
- voiceover: "La modification ? Toi. La page ? Toi. L'automatisation ? Toi."
- type: benefit_highlight
- blueprint: fixed-anchor-cycle (Adapt)
- focal: the pen strike and « TOI. »
- rules: svg-path-draw, kinetic-beat-slam
- world: desk-day

Word cues: La-modification@0.08 ?@0.88 Toi@1.22 La-page@1.88 ?@2.46 Toi@2.80 L’automatisation@3.48 ?@4.40 Toi@4.68
Scene 1 (0.0-0.30s): the quote-sheet (all four rows + total « 1 600 € ») lies on the desk-day in the left 48% of the frame, large enough to read the rows (≈640px wide), slightly rotated; a terracotta pen (frame.md) rests beside it.
Scene 2 (0.08-1.80s): right region: phrase-size question « La modification ? » at 0.08; at 1.22 the pen strikes row 1 (a wavy accent line drawn with the pen tip moving along it, → svg-path-draw) and writes « toi » next to the price, while [giant: « TOI. »] slams in the right region under the question in ink-dark with the tracking tighten (→ kinetic-beat-slam).
Scene 3 (1.80-3.40s): the question becomes « La page ? » at 1.88; at 2.80 the pen strikes row 2 and writes « toi »; « TOI. » re-slams.
Scene 4 (3.40-5.38s): the question becomes « L’automatisation ? » at 3.48; at 4.68 the pen strikes row 3 and writes « toi »; « TOI. » re-slams; at 5.00 the pen strikes the « Délai » row and writes « maintenant », and scribbles over the total. Hold.

## Frame 7 : Il ne reste qu'une ligne

- scene: The pen writes one last line on the struck quote, the camera dives into it, then the sheet flies away and « libre. » lands in a giant pill on the clean desk
- duration: 5.92s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/07-ligne.html
- voiceover: "Il ne reste qu'une ligne sur le devis... apprendre à t'en servir. Et c'est la seule qui te rend libre."
- type: benefit_highlight
- blueprint: titlecard-reveal (Adapt)
- focal: the last written line, then « libre. »
- rules: svg-path-draw, motion-blur-streak
- world: desk-day

Word cues: Il@0.08 ne@0.24 reste@0.44 qu’une@0.64 ligne@0.96 sur@1.14 le@1.36 devis@1.52 Apprendre@2.26 à@2.60 t’en@2.72 servir@2.92 c’est@3.86 la@4.06 seule@4.28 qui@4.46 te@4.64 rend@4.82 libre@4.96
Scene 1 (0.0-2.10s): the struck quote-sheet centered on the desk-day (all rows struck); phrase at the top, word by word « Il ne reste » + [pill: qu’une ligne] at 0.64 « sur le devis. »; at 1.20 the pen draws an empty underlined slot at the bottom of the sheet, with the micro label « LA SEULE LIGNE QUI RESTE » printed above it.
Scene 2 (2.10-3.60s): the camera pushes in onto that slot until it fills the frame; the pen writes « Apprendre à t’en servir » in the slot (the text revealed left to right exactly behind the moving pen tip, paper-line style at 64px) from 2.26 to 3.20, a terracotta comet streak underlines it (→ motion-blur-streak); phrase at the top « Apprendre à » + [pill: t’en servir] at 2.72.
Scene 3 (3.60-5.92s): the camera pulls back to the whole sheet on the desk; small phrase at the top « C’est la seule qui te rend » (3.86 → 4.82); at 4.70 the sheet lifts off the desk (its shadow grows and softens), rotates to -14deg and flies out to the top-right (power3.in, gone by 5.10); at 4.96 [giant-pill: « libre. »] (frame.md giant-pill) lands dead center on the clean desk. Hold still to the end.

## Frame 8 : Pas besoin d'être technique

- scene: A printed code sheet crumples into a ball and is tossed off the desk; then the pen draws a big zero in an open notebook, which fills with terracotta and glows
- duration: 4.25s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/08-zero.html
- voiceover: "Et pas besoin d'être technique. C'est pensé pour ceux qui partent de zéro."
- type: benefit_highlight
- blueprint: titlecard-reveal (Adapt)
- focal: the crumpling sheet, then the zero
- rules: svg-path-draw, stat-bars-and-fills
- world: desk-day

Word cues: Et@0.10 pas@0.20 besoin@0.40 d’être@0.56 technique@0.82 C’est@1.76 pensé@1.88 pour@2.12 ceux@2.36 qui@2.46 partent@2.68 de@2.98 zéro@3.14 (silence from 3.82)
Scene 1 (0.0-1.60s): a sheet printed with ~8 lines of code (Space Mono, keywords in accent) lies on the desk-day; from 0.82 it crumples (successive scale-down with jagged clip-path folds and a rotation, deterministic) into a paper ball that is tossed out of the frame to the bottom-left by 1.45. Phrase centered at the top band, word by word « Pas besoin d’être » + [pill: technique.] at 0.82.
Scene 2 (1.60-3.80s): an open notebook (two lined pages, paper) on the right half of the desk; the pen draws a big hand-drawn « 0 » (an ellipse ~420px tall, accent 8px stroke, round caps) centered EXACTLY at (1400, 450) from 2.98 to 3.30 (→ svg-path-draw), then the inside fills with terracotta at 3.30 (→ stat-bars-and-fills). Phrase on the left half, word by word « C’est pensé pour ceux qui partent » + [pill: de zéro.] at 2.98.
Scene 3 (3.80-4.25s): the filled zero's center brightens into a hot bloom; the orchestrator opens the iris to the dark end card from its center (1400, 450). Every clip of this frame lasts 5.0 s (the iris keeps the frame mounted until 5.0).

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
