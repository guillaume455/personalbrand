/* =========================================================================
   Comportements communs aux pages du tunnel.
   ========================================================================= */
(function () {
  'use strict';

  document.documentElement.dataset.pret = '1';

  /* ---------- Apparitions au défilement ---------------------------------
     Même parti pris que sur le site : IntersectionObserver plutôt que
     `animation-timeline: view()`, qui laisse les blocs déjà visibles figés
     à mi-opacité tant que la page ne bouge pas. */
  var cibles = document.querySelectorAll('[data-reveal]');
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
    cibles.forEach(function (el) { el.classList.add('vu'); });
  } else {
    var obs = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('vu');
        obs.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.05 });
    cibles.forEach(function (el) { obs.observe(el); });
  }

  /* ---------- Bouton collant mobile -------------------------------------
     §8 : « visible dès le deuxième bloc ». On observe la section d'accroche
     elle-même : tant qu'elle est à l'écran, elle porte déjà son propre CTA et
     le bouton collant ferait doublon ; dès qu'elle est sortie, on est au
     deuxième bloc et le bouton apparaît. Observer une sentinelle placée APRÈS
     l'accroche donnerait l'inverse, puisqu'elle est sous la ligne de
     flottaison au chargement. */
  var collant = document.querySelector('[data-collant]');
  var declencheur = document.querySelector('[data-accroche]');
  if (collant && declencheur && 'IntersectionObserver' in window) {
    document.body.dataset.barreBasse = 'actif';
    new IntersectionObserver(function (e) {
      collant.setAttribute('data-visible', e[0].isIntersecting ? 'false' : 'true');
    }, { threshold: 0 }).observe(declencheur);
  } else if (collant) {
    collant.setAttribute('data-visible', 'true');
    document.body.dataset.barreBasse = 'actif';
  }

  /* ---------- FAQ : une seule réponse ouverte à la fois ------------------ */
  var faq = document.querySelectorAll('.faq details');
  faq.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      faq.forEach(function (a) { if (a !== d) a.open = false; });
    });
  });

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

  /* ---------- VSL --------------------------------------------------------
     Les navigateurs n'autorisent la lecture automatique que sans le son.
     La vidéo démarre donc muette dès qu'elle est à l'écran, se met en pause
     quand on la quitte, et le bouton relance depuis le début avec le son. */
  document.querySelectorAll('[data-vsl]').forEach(function (fig) {
    var v = fig.querySelector('video');
    var btn = fig.querySelector('[data-vsl-son]');
    if (!v) return;
    // Fichier absent ou illisible : on retire la section plutôt qu'un cadre noir.
    // Seule une vraie erreur de chargement compte : Safari sur iPhone peut annoncer
    // « aucune source » tant qu'il n'a pas commencé à charger (mode économie
    // d'énergie, données réduites), ce qui masquait la vidéo à tort.
    var masquer = function () { (fig.closest('section') || fig).hidden = true; };
    var sources = v.querySelectorAll('source');
    if (sources.length) sources[sources.length - 1].addEventListener('error', masquer);
    else v.addEventListener('error', masquer);
    v.muted = true;
    // Lecture automatique refusée (iPhone en économie d'énergie) : on affiche
    // les commandes pour que le bouton lecture soit là.
    var lancer = function () {
      var p = v.play();
      if (p && p.catch) p.catch(function () { v.controls = true; });
    };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entrees) {
        entrees.forEach(function (e) {
          if (e.isIntersecting) { if (v.paused && !v.ended) lancer(); }
          else if (!v.paused) v.pause();
        });
      }, { threshold: 0.5 }).observe(v);
    } else {
      lancer();
    }
    if (btn) btn.addEventListener('click', function () {
      v.currentTime = 0;
      v.muted = false;
      v.controls = true;
      btn.hidden = true;
      lancer();
      if (window.GH && window.GH.mesure) window.GH.mesure.envoyer('vsl_son');
    });
  });

  /* ---------- Année du pied de page -------------------------------------- */
  document.querySelectorAll('[data-annee]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- Avertissement de préproduction -----------------------------
     Visible seulement tant que config.preprod vaut true, pour qu'un tunnel
     à moitié branché ne parte jamais en ligne sans que ça se voie. */
  var cfg = (window.GH && window.GH.config) || {};
  if (cfg.preprod) {
    var manques = [];
    if (!cfg.backend || !cfg.backend.type) manques.push('backend du formulaire');
    if (!cfg.reservation || !cfg.reservation.url) manques.push('outil de réservation');
    if (!cfg.mesure || (!cfg.mesure.ga4 && !cfg.mesure.meta)) manques.push('mesure');
    if (manques.length) {
      console.warn('[tunnel] Mode démo, non branché : ' + manques.join(', ') +
        '. Renseigner /assets/js/config.js, puis passer preprod à false.');
    }
  }
})();
