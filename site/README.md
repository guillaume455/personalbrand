# guillaumeherbin.fr

Site statique. Pas de framework, pas d'étape de build : les fichiers `.html` du
dossier sont exactement ce que le serveur envoie. On les ouvre, on les modifie,
on les remet en ligne.

## Structure

```
site/
├── index.html  parcours.html  presse.html  contact.html  mentions-legales.html
├── index-en.html  parcours-en.html  presse-en.html  contact-en.html
│                                             mentions-legales-en.html
├── assets/
│   ├── css/style.css     toute la mise en forme du site, un seul fichier
│   ├── js/app.js         menu mobile, thème, apparitions, filtres
│   ├── fonts/            Archivo (variable), auto-hébergée
│   └── img/              photos en .webp + repli .jpg/.png
├── favicon.svg  site.webmanifest  robots.txt  sitemap.xml
```

Le CSS et le JS sont **partagés par les dix pages**. Une modification de couleur,
d'espacement ou de comportement se fait une seule fois dans `style.css` ou
`app.js`, et s'applique partout.

## Modifications courantes

**Changer un texte** — ouvrir la page concernée, modifier entre les balises.
Penser à reporter dans la page `-en.html` correspondante.

**Ajouter un article de presse** — dans `presse.html`, dupliquer un bloc
`<a class="carte">` et remplacer lien, média, titre et date.

**Ajouter une vidéo ou un podcast** — même chose, mais remplacer
`data-cat="presse"` par `data-cat="video"` ou `data-cat="podcast"`. Les boutons
de filtre apparaissent automatiquement dès qu'il existe deux catégories : il n'y
a rien d'autre à activer.

**Ajouter une photo** — la déposer dans `assets/img/`, puis l'appeler avec ses
dimensions réelles, sinon la page « saute » pendant le chargement :

```html
<picture>
  <source srcset="assets/img/nom.webp" type="image/webp">
  <img src="assets/img/nom.jpg" width="800" height="600" alt="Description"
       loading="lazy" decoding="async">
</picture>
```

**Changer la couleur d'accent** — dans `style.css`, bloc `:root`. Attention :
`--accent` (#FC7E15) ne sert qu'au décoratif (filets, surlignages, puces). Sur
fond blanc il ne fait que 2,58:1 de contraste, sous le minimum WCAG de 4,5:1.
Le texte accent utilise `--accent-ink`, plus foncé. Les deux doivent rester
cohérents si l'accent change.

## Avant la mise en ligne

`mentions-legales.html` et `mentions-legales-en.html` contiennent des champs
encadrés en orange (classe `.a-remplir`) : statut juridique, adresse, numéro
SIREN/SIRET, hébergeur, durée de conservation des messages. Ils sont obligatoires
au titre de la LCEN et doivent être renseignés. Supprimer aussi le paragraphe
`.rappel` en haut de chaque page une fois que c'est fait.

Vérifier également que `contact@guillaumeherbin.fr` est bien confirmée côté
[FormSubmit](https://formsubmit.co) : sans cette validation, le formulaire
n'envoie rien.

## Choix techniques, et pourquoi

- **Images en fichiers, pas en base64.** Les pages d'origine embarquaient
  1,7 Mo d'images encodées dans le HTML. Rien n'était mis en cache : chaque
  page rechargeait tout. Les dix pages pèsent aujourd'hui 141 Ko de HTML au
  total, contre 1 706 Ko pour quatre pages avant.
- **Police auto-hébergée.** Pas de requête vers Google Fonts : un aller-retour
  DNS de moins avant le premier rendu, et aucune adresse IP transmise à un tiers.
- **Pas d'`animation-timeline: view()`.** Cette animation native est pilotée par
  le défilement : un bloc déjà à l'écran au chargement reste figé à mi-opacité
  tant que la page ne bouge pas, ce qui fait passer son texte sous le seuil de
  contraste. L'IntersectionObserver d'`app.js` se déclenche une fois et va au
  bout. Un filet dans le `<head>` réaffiche tout si `app.js` ne se charge pas.
- **Photos de témoignages sans recadrage.** Elles portent le nom du franchisé
  incrusté en bas. Tout `aspect-ratio` imposé ampute un nom — d'où des hauteurs
  légèrement différentes d'une carte à l'autre, assumées.

## Contrôles

Le site est vérifié sans violation axe-core (WCAG 2.1 AA) sur les dix pages, en
thème clair et sombre, sans erreur console ni débordement horizontal, du mobile
360 px au grand écran.
