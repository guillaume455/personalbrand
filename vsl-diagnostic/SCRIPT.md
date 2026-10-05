# SCRIPT — VSL diagnostic (guillaumeherbin.fr/accompagnement)

Format : 45 s, 16:9, lecteur de la page de vente. Appel à l'action : « Voir si mon profil correspond »
→ https://guillaumeherbin.fr/accompagnement/candidature/

**Angle** : on croit qu'il suffit de se lancer pour essayer. Se lancer, c'est bien, mais avec un plan donné par
quelqu'un qui connaît le métier : ça limite la casse, le temps perdu et le cash dépensé pour rien.

**Garde-fous** :
- aucun chiffre de revenu ni de résultat, aucune promesse ;
- les seuls chiffres sont des faits sur Guillaume, tirés de la page : 21 ans, 3 000 €, 16 ans ;
- le film ne détaille pas l'offre : ni prix, ni durée, ni document (c'est le rôle de la page) ;
- pas de mention du réseau.

**Statut** : texte validé par Guillaume (version B retouchée), le 2026-10-05.

---

## Version validée — « Essayer, ça coûte »

### Version mise en scène

| # | Temps | Voix | À l'écran |
|---|---|---|---|
| 1 | Accroche | Tu veux vivre de l'automobile. Alors tu te dis : j'essaie. | Une recherche « comment se lancer dans l'automobile », les onglets s'ouvrent. |
| | | Essayer un modèle… ça coûte des mois. | Le calendrier défile. |
| | | Essayer une voiture… ça coûte ta marge. | Le calcul : la ligne « résultat » passe au rouge. |
| | | Essayer encore… ça coûte ton épargne. | Le solde du compte qui descend. |
| 2 | Gag muet (2,5 s) | *(pas de voix)* | Le curseur hésite au-dessus de « Acheter » sur une annonce, puis la ferme. |
| 3 | Diagnostic | Le problème, ce n'est pas de te lancer. | |
| | | C'est de te lancer sans plan. | [boîte : sans plan] |
| | | Sans savoir quel modèle te correspond. Combien il te faut. Combien tu dois vendre. | Trois questions qui s'empilent. |
| 4 | Bascule sur noir | Et si tu essayais… avec un plan ? | Fond noir, phrase au centre, 1,5 s de silence. |
| 5 | Solution | Un plan fait par quelqu'un qui connaît le métier. | |
| | | Je m'appelle Guillaume Herbin. Je me suis lancé à l'âge de 21 ans, avec 3 000 € en poche. | Portrait, puis le Kbis 2010. |
| | | On part de ta situation. On tranche le modèle. On pose les vrais chiffres. | Trois gestes : une fiche se remplit, une étiquette se coche, un calcul tombe juste. |
| | | Moins de casse. Moins de temps perdu. | [trait : moins de casse] |
| 6 | Marque et appel à l'action | Guillaume Herbin. Seize ans dans l'automobile. | Nom + portrait. |
| | | Tu n'as pas besoin de tout savoir. Juste ta prochaine étape. | Bouton « Voir si mon profil correspond », un curseur clique. Rappel de l'accroche : la recherche. |

### Version à coller dans ElevenLabs

```
Tu veux vivre de l'automobile. Alors tu te dis : j'essaie.
Essayer un modèle... ça coûte des mois.
Essayer une voiture... ça coûte ta marge.
Essayer encore... ça coûte ton épargne.

Le problème, ce n'est pas de te lancer.
C'est de te lancer sans plan.
Sans savoir quel modèle te correspond. Combien il te faut. Combien tu dois vendre.

Et si tu essayais... avec un plan ?

Un plan fait par quelqu'un qui connaît le métier.
Je m'appelle Guillaume Herbin. Je me suis lancé à l'âge de vingt et un ans, avec trois mille euros en poche.
On part de ta situation. On tranche le modèle. On pose les vrais chiffres.
Moins de casse. Moins de temps perdu.

Guillaume Herbin. Seize ans dans l'automobile.
Tu n'as pas besoin de tout savoir. Juste ta prochaine étape.
```

### Réglages ElevenLabs

- Text to Speech, modèle **Eleven v4**, langue réglée à la main sur **français** (en automatique, l'accent peut dériver).
- Stabilité **40 à 50 %**, Similarité **80 à 90 %**.
- Coller tout le texte d'un coup, générer **2 ou 3 prises**, garder la meilleure.
- Le gag muet et le silence de la bascule se font au montage : ne rien ajouter dans le texte.
- Déposer la prise retenue sous `vsl-diagnostic/assets/audio/voix.mp3`.
- Forfait payant obligatoire pour un usage commercial.

Avec ta propre voix : pièce calme, téléphone près de la bouche, lire le même texte, export MP3, même emplacement.
