/* Guillaume Herbin — comportements de la page.
   Chargé en `defer`. Le thème, lui, est appliqué par un script inline dans
   le <head> pour éviter tout flash de couleur au chargement. */
(function () {
  'use strict';

  // Signale au filet de sécurité du <head> que les apparitions sont prises en
  // charge ; sans ce drapeau, il réaffiche tout au bout de 1,2 s.
  document.documentElement.dataset.pret = '1';

  /* ---------- Menu mobile ---------- */
  var burger = document.querySelector('[data-burger]');
  var menu = document.getElementById('nav-liens');

  function fermerMenu() {
    if (!burger || !menu) return;
    burger.setAttribute('aria-expanded', 'false');
    menu.setAttribute('data-ouvert', 'false');
    document.body.removeAttribute('data-menu');
  }

  if (burger && menu) {
    burger.addEventListener('click', function () {
      var ouvert = burger.getAttribute('aria-expanded') === 'true';
      if (ouvert) { fermerMenu(); return; }
      burger.setAttribute('aria-expanded', 'true');
      menu.setAttribute('data-ouvert', 'true');
      document.body.setAttribute('data-menu', 'ouvert');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) fermerMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') {
        fermerMenu();
        burger.focus();
      }
    });
    // Repasser en nav desktop referme proprement.
    matchMedia('(min-width: 861px)').addEventListener('change', function (e) {
      if (e.matches) fermerMenu();
    });
  }

  /* ---------- Apparition au défilement ----------
     Un seul déclenchement par bloc, puis on cesse de l'observer : un élément
     déjà visible au chargement s'affiche donc tout de suite et en entier. */
  var sobre = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cibles = document.querySelectorAll('[data-reveal]');

  if (sobre || !('IntersectionObserver' in window)) {
    cibles.forEach(function (el) { el.classList.add('vu'); });
  } else {
    var obs = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('vu');
        obs.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    cibles.forEach(function (el) { obs.observe(el); });
  }

  /* ---------- Filtres presse & médias ----------
     Les boutons ne s'affichent que si au moins deux catégories existent
     réellement dans la grille : inutile de proposer un filtre à un seul choix. */
  var barre = document.querySelector('[data-filtres]');
  var cartes = document.querySelectorAll('.portfolio .carte');

  if (barre && cartes.length) {
    var cats = [];
    cartes.forEach(function (c) {
      var k = c.dataset.cat;
      if (k && cats.indexOf(k) === -1) cats.push(k);
    });

    if (cats.length < 2) {
      barre.hidden = true;
    } else {
      barre.hidden = false;
      var boutons = barre.querySelectorAll('.filtre');
      boutons.forEach(function (b) {
        var f = b.dataset.filtre;
        if (f !== 'tout' && cats.indexOf(f) === -1) { b.remove(); return; }
        b.addEventListener('click', function () {
          boutons.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
          b.setAttribute('aria-pressed', 'true');
          var n = 0;
          cartes.forEach(function (c) {
            var montre = (f === 'tout' || c.dataset.cat === f);
            c.hidden = !montre;
            if (montre) n++;
          });
          var live = document.querySelector('[data-filtres-live]');
          if (live) {
            live.textContent = document.documentElement.lang === 'en'
              ? n + (n > 1 ? ' items shown' : ' item shown')
              : n + (n > 1 ? ' contenus affichés' : ' contenu affiché');
          }
        });
      });
    }
  }

  /* ---------- Confirmation d'envoi du formulaire ---------- */
  var envoye = new URLSearchParams(location.search).has('envoye')
            || new URLSearchParams(location.search).has('sent');
  if (envoye) {
    var ok = document.getElementById('confirmation');
    var form = document.querySelector('.form');
    if (ok) { ok.hidden = false; ok.setAttribute('tabindex', '-1'); ok.focus(); }
    if (form) form.hidden = true;
  }

  /* ---------- Ouverture directe du fichier (file://) ----------------------
     Un lien vers un dossier, « cgv/ », est résolu en « cgv/index.html » par un
     serveur web, mais pas par le navigateur quand la page est ouverte depuis
     le disque : il affiche le contenu du dossier. On complète donc ces liens,
     et uniquement dans ce cas. Sur le site en ligne, la condition est fausse
     et rien ne se passe : les adresses restent propres. */
  if (location.protocol === "file:") {
    document.querySelectorAll("a[href$=\"/\"], [data-merci$=\"/\"]").forEach(function (el) {
      var att = el.hasAttribute("data-merci") ? "data-merci" : "href";
      var h = el.getAttribute(att);
      if (h && !/^[a-z]+:/i.test(h)) el.setAttribute(att, h + "index.html");
    });
  }

  /* ---------- Année du copyright ---------- */
  document.querySelectorAll('[data-annee]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
