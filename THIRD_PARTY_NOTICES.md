# Mentions tierces

Tout ce dépôt est sous licence MIT (`LICENSE`, © 2026 Colin Blain), **sauf** les éléments tiers listés ici, qui gardent leur propre licence.

## Skills HyperFrames (HeyGen)

- **Auteur** : HeyGen, Inc. (© 2026 HeyGen, Inc.)
- **Licence** : Apache License 2.0, texte complet dans `.claude/skills/LICENSE-HEYGEN-APACHE-2.0` (récupéré sur la branche `main` du dépôt amont, identique à celui du commit audité).
- **Source** : https://github.com/heygen-com/hyperframes, dossier `skills/`
- **Commit audité** : `93ab2899f13a1120002986793a7b11b657841b69` (court : `93ab289`, repris dans `.claude/skills/AUDITED_COMMIT.txt`), audit de sécurité du 2026-09-28.
- **Dossiers copiés** dans `.claude/skills/` : `hyperframes`, `hyperframes-animation`, `hyperframes-audio`, `hyperframes-cli`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-keyframes`, `hyperframes-registry`, `media-use`, `product-launch-video`.
- **Non tiers** : `.claude/skills/motion-design/` (le skill de ce dépôt, MIT) et `.claude/skills/AUDITED_COMMIT.txt`.

### Fichiers modifiés (Apache 2.0, section 4 b)

La copie n'est pas identique à l'amont : elle a été durcie pendant l'audit du 2026-09-28, dans l'atelier de travail où l'audit a été fait (nommé `motion-launch`, d'où ce nom dans les consignes ajoutées). Tous les autres fichiers sont identiques octet pour octet à ceux du commit `93ab289` (vérifié par `diff -r` le 2026-09-28).

| Fichier | Changement |
|---|---|
| `hyperframes/SKILL.md` | description resserrée (point d'entrée de l'atelier, plus « obligatoire pour toute vidéo ») ; plus de mise à jour du logiciel sans le « oui » explicite de l'utilisateur ; `npx hyperframes skills update` remplacé par la règle du commit audité figé |
| `hyperframes-animation/adapters/animate-text.md` | installation du skill tiers `animate-text` (non audité, sans licence) retirée ; les effets se codent en GSAP |
| `hyperframes-animation/adapters/lottie.md` | `@lottiefiles/dotlottie-web` épinglé en `0.80.0` |
| `hyperframes-cli/SKILL.md` | envois `feedback` (notes, recherches ratées) vers un canal public remplacés par une règle d'interdiction |
| `hyperframes-cli/references/preview-render.md` | section `feedback` remplacée par la même règle |
| `hyperframes-creative/references/design-picker.md` | petit serveur local limité à `127.0.0.1` au lieu de tout le réseau |
| `hyperframes-registry/SKILL.md` | envoi des recherches ratées remplacé par la règle d'interdiction |
| `media-use/scripts/eval.mjs` | supprimé |

### Contenus embarqués dans ces skills

- `media-use/audio/assets/sfx/*.mp3` : bruitages de [Pixabay](https://pixabay.com/sound-effects/), [Pixabay Content License](https://pixabay.com/service/license-summary/) (détail dans `CREDITS.md` du même dossier). Ce sont les bruitages utilisés par le mixage de la méthode.
- `hyperframes-creative/frame-presets/code-editorial/fonts/` : EB Garamond, Inter, JetBrains Mono, SIL Open Font License 1.1 (textes de licence dans le même dossier).

## Éléments que tu récupères toi-même (non inclus)

- **Polices** : Instrument Sans, Space Mono et Big Shoulders, [Google Fonts](https://fonts.google.com), SIL Open Font License 1.1. Téléchargées dans chaque projet (commandes dans `.claude/skills/motion-design/references/method.md`).
- **Logos d'outils** : [Simple Icons](https://simpleicons.org), licence CC0 pour les fichiers SVG. Les logos restent des marques de leurs propriétaires : ne les utilise que pour montrer l'outil tel qu'il est.
- **Musique** : des morceaux sous licence CC0 (domaine public) de ton choix, par exemple de [HoliznaCC0](https://freemusicarchive.org/music/holiznacc0/), [Loyalty Freak Music](https://freemusicarchive.org/music/Loyalty_Freak_Music/) ou [Komiku](https://freemusicarchive.org/music/Komiku/) (morceaux marqués CC0 seulement) sur Free Music Archive. Vérifie la licence sur la page de chaque morceau. Les dix morceaux utilisés pour les options du devis sont listés, avec leurs liens, dans `.claude/skills/motion-design/references/music.md` (les fichiers ne sont pas inclus).
- **Voix** : générée par toi sur [ElevenLabs](https://elevenlabs.io), soumise à leurs conditions (forfait payant obligatoire pour un usage commercial).

## Films d'exemple (`examples/`)

Les vidéos d'exemple contiennent une voix générée sur ElevenLabs (forfait payant, usage commercial), des bruitages Pixabay (Pixabay Content License) et, pour `examples/le-devis-options/poli/le-devis-poli.mp4`, deux morceaux en CC0 1.0 : « Waiting TTTT » de Loyalty Freak Music et « Dear Mr Super Computer » de HoliznaCC0 (freemusicarchive.org). Pour `examples/le-devis/le-devis.mp4`, la musique est « Night Life » de HoliznaCC0, en CC0 1.0 également. La mention est facultative en CC0, elle est donnée par courtoisie.

## Patterns (`patterns/PATTERNS.md`, `patterns/STORYBOARD-CRAFT.md`)

Synthèse originale : la grammaire et les patterns du motion design, ce qui ressort après avoir regardé pas mal de vidéos de motion design. Aucune image ni vidéo tierce n'est reproduite ici. Les noms cités en exemple sont ceux de marques dont les films de lancement sont publics : ces films appartiennent à leurs auteurs, les marques à leurs propriétaires. Ce dépôt n'est affilié ni à ces marques, ni à HeyGen, ni à ElevenLabs.
