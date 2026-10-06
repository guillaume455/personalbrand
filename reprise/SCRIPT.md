# SCRIPT — « Prends l'acheteur avec reprise » (reel 9:16)

Format : 1080×1920, 30 fps, environ 60 s. Fond #0A0A0A, accent #FB8000, texte blanc. Titres en capitales grasses
soulignés d'un trait orange. Pas de facecam. Sous-titres de la voix, mot-clé de chaque phrase en orange. Jamais plus de
6 mots par bloc de texte. Montants en compteur qui défile (caisse enregistreuse). Aucun billet, liasse ni espèce à
l'écran. Fin : « @guillaumeherbin_ ».

**Statut** : brief et découpage écrits par Guillaume (2026-10-06). Le texte de la voix est dans `build.py` (SCENES),
découpé en sous-titres ; c'est la seule source : toute retouche du texte se fait là.

## Découpage (Guillaume)

| # | Temps (brief) | À l'écran | Voix |
|---|---|---|---|
| 1 | 0 à 5 s | Bandeau orange « TU ACHÈTES TES VOITURES ? », voiture au centre, deux acheteurs ; « MÊME VOITURE. MÊME PRIX. » | Tu achètes et revends des voitures ? … Un seul est le bon. |
| 2 | 5 à 11 s | L'acheteur de gauche s'allume, « 10 000 € COMPTANT », notification « Virement reçu » | Le premier te l'achète dix mille euros comptant… Le rêve. |
| 3 | 11 à 17 s | L'acheteur de droite s'allume, « 10 000 € + REPRISE », une deuxième voiture derrière lui | Le second te l'achète aussi… Erreur. |
| 4 | 17 à 29 s | Deux colonnes : 1 vente, 1 marge / reprise estimée 6 500 €, revendue 8 000 €, « 2 VENTES, 2 MARGES » | Avec lui, tu fais une deuxième vente… deux marges. |
| 5 | 29 à 40 s | Flèche vente (10 000 €) → reprise (6 500 €), banque grisée hors circuit, « PAYÉE PAR LA VENTE » puis « PAS PAR LA BANQUE » | La voiture que tu vends est à toi… que tu gardes. |
| 6 | 40 à 49 s | Panneau ATTENTION, « REPRISE SURPAYÉE = MARGE PERDUE », la marge fond | Mais attention au piège… au centime près. |
| 7 | 49 à 54 s | Une voiture roule vers la caméra, « LA VOITURE VIENT À TOI » | Et en deux mille vingt-six… qui vient à toi. |
| 8 | 54 à 60 s | Retour à la scène 1, l'acheteur de droite s'allume en orange, « PRENDS CELUI QUI A UNE REPRISE. », « @guillaumeherbin_ » | Entre deux clients au même prix… comme celui-ci. |

Le texte de la scène 5 (« PAYÉE PAR LA VENTE, PAS PAR LA BANQUE », 8 mots) s'affiche en deux temps de 4 mots pour
tenir la règle des 6 mots.

## Version à coller dans ElevenLabs

```
Tu achètes et tu revends des voitures ? OK. Prenons le cas de deux acheteurs. Même voiture et même prix.
Le premier te l'achète dix mille euros comptant, sans discuter, virement le jour même. Le rêve.
Le second te l'achète aussi dix mille euros, mais il a une voiture à reprendre. La plupart des vendeurs choisissent le premier. Erreur.
Avec lui, tu fais une deuxième vente. Tu reprends sa voiture au juste prix, tu la revends derrière. Même client, deux marges.
La voiture que tu vends est à toi, donc cette reprise, tu la paies avec l'argent de la vente. Pas de crédit, pas d'intérêts. L'argent emprunté coûte cher : chaque voiture que tu ne finances pas à la banque, c'est de la marge que tu gardes.
Mais attention au piège : surpayer la reprise pour signer la vente. Une reprise trop chère mange la marge que tu viens de faire. Elle s'estime comme un achat, au centime près.
Et en deux mille vingt-six, trouver des voitures, c'est le plus dur. La reprise, c'est une voiture qui vient à toi.
Entre deux clients au même prix, prends celui qui a une reprise. Abonne-toi pour plus de contenu comme celui-ci.
```

## Réglages ElevenLabs

Mêmes réglages que les deux films précédents : Eleven v4, langue française réglée à la main, Stabilité 40 à 50 %,
Similarité 80 à 90 %, tout le texte d'un coup, 2 ou 3 prises. Déposer la prise retenue sous
`reprise/assets/audio/voix.mp3`.

## Recaler sur la voix finale

```
python3 build-voice.py      # pauses resserrées à 0,34 s, voix ×1,08 -> assets/audio/voix-montage.wav
python3 align.py            # temps de chaque mot -> assets/audio/voix-montage-mots.json
python3 build.py            # scènes, coupes, sous-titres, bruitages recalés sur les mots
bash build-mix.sh && bash assemble.sh
```
