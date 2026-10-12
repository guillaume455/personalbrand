/* =========================================================================
   Écran d'analyse — /accompagnement/analyse/

   Tally redirige ici en portant le résultat dans l'adresse :
     ?r=ok&prenom=…&email=…&event_id=…   profil retenu
     ?r=non&prenom=…                      profil non retenu

   Trois choses à savoir avant de toucher à ce fichier.

   1. L'animation ne calcule rien. La décision est prise par Tally, bien avant
      l'arrivée ici. Ces quinze secondes servent à faire comprendre qu'une
      règle a été appliquée, pas à simuler une lecture humaine : les libellés
      le disent, et il ne faut pas les transformer en « Guillaume consulte ton
      dossier ».

   2. `r` vient de l'adresse, donc du visiteur, qui peut la changer. Ce n'est
      pas un trou : atteindre l'écran « retenu » ne donne qu'un calendrier,
      et il faut payer 490 € pour bloquer un créneau. La règle qui engage est
      celle de Tally et de Make, jamais celle-ci.

   3. `event_id` doit être le même que celui envoyé par Make à l'API de
      conversions. Il est fabriqué en amont et passé dans l'adresse ; s'il
      manque, l'événement part quand même, mais Meta le comptera deux fois.
   ========================================================================= */
(function () {
  'use strict';

  var cfg = (window.GH && window.GH.config) || {};
  var mesure = (window.GH && window.GH.mesure) || { envoyer: function () {} };

  var DUREE = 15000;                 // durée totale de l'analyse
  var PAS = [0, 5000, 10000];        // instant où chaque ligne se coche

  var p = new URLSearchParams(location.search);
  var resultat = p.get('r') === 'ok' ? 'ok' : 'non';
  var prenom = (p.get('prenom') || '').trim().slice(0, 40);
  var email = (p.get('email') || '').trim().slice(0, 120);
  var eventId = (p.get('event_id') || '').trim().slice(0, 80);

  var ecranAnalyse = document.querySelector('[data-ecran="analyse"]');
  var ecranOk = document.querySelector('[data-ecran="ok"]');
  var ecranNon = document.querySelector('[data-ecran="non"]');
  var lignes = document.querySelectorAll('[data-pas-a]');
  var jauge = document.querySelector('[data-jauge-analyse]');
  var etat = document.querySelector('[data-analyse-etat]');

  /* ---------- Prénom ------------------------------------------------------
     Posé en texte, jamais en HTML : il vient de l'adresse, donc d'une source
     que le visiteur contrôle. */
  function poserPrenom() {
    var h1 = document.querySelector('[data-prenom-h1]');
    if (h1 && prenom) h1.textContent = ', ' + prenom;
    var ok = document.querySelector('[data-prenom-ok]');
    if (ok) ok.textContent = prenom ? prenom + ', ' : '';
    var non = document.querySelector('[data-prenom-non]');
    if (non) non.textContent = prenom ? prenom + ', ' : '';
  }

  /* ---------- Le calendrier ----------------------------------------------
     Il n'apparaît que sur l'écran « retenu », et c'est lui qui encaisse.
     L'adresse vit dans config.js : tant qu'elle est vide, on le dit au lieu
     d'afficher un cadre blanc. */
  function poserAgenda() {
    var hote = document.querySelector('[data-agenda]');
    if (!hote) return;
    var url = (cfg.reservation && cfg.reservation.url) || '';
    if (!url) {
      hote.innerHTML = '<div class="a-fournir"><b>Calendrier non branché</b>'
        + 'Renseigner <code>reservation.url</code> dans <code>/assets/js/config.js</code> : '
        + 'le lien Cal.com de la séance de 1h30, paiement Stripe de 490 € exigé à la '
        + 'réservation.</div>';
      return;
    }
    // L'e-mail prérempli évite une saisie déjà faite dans le questionnaire.
    var sep = url.indexOf('?') === -1 ? '?' : '&';
    var src = url + (email ? sep + 'email=' + encodeURIComponent(email) : '');
    var cadre = document.createElement('iframe');
    cadre.src = src;
    cadre.title = 'Choix du créneau et paiement';
    cadre.loading = 'lazy';
    cadre.style.cssText = 'width:100%;min-height:720px;border:0;border-radius:3px';
    hote.appendChild(cadre);

    // §7.3 : InitiateCheckout à l'ouverture du paiement, et nulle part ailleurs.
    mesure.envoyer('checkout_start', {
      value: (cfg.offre && cfg.offre.prix) || 490,
      currency: (cfg.offre && cfg.offre.devise) || 'EUR',
      event_id: eventId || undefined,
    });
  }

  function montrer(ecran) {
    if (ecranAnalyse) ecranAnalyse.hidden = true;
    if (ecran === 'ok') {
      if (ecranOk) ecranOk.hidden = false;
      mesure.envoyer('qualified_lead', { event_id: eventId || undefined });
      poserAgenda();
    } else {
      if (ecranNon) ecranNon.hidden = false;
      mesure.envoyer('application_complete', {
        tunnel: cfg.tunnel || 'lancement',
        event_id: eventId || undefined,
      });
    }
    // Le titre de l'issue reçoit le focus : sans cela, un lecteur d'écran
    // resterait sur l'écran d'analyse qui vient de disparaître.
    var cible = document.querySelector('[data-ecran="' + ecran + '"] .encart p');
    if (cible) { cible.setAttribute('tabindex', '-1'); cible.focus(); }
  }

  function animer() {
    var debut = Date.now();
    var fini = false;

    PAS.forEach(function (t, i) {
      setTimeout(function () {
        if (lignes[i]) lignes[i].dataset.fait = 'oui';
      }, t);
    });

    // Une seule boucle pour la barre, arrêtée dès qu'elle atteint le bout.
    var tic = setInterval(function () {
      var avance = Math.min(1, (Date.now() - debut) / DUREE);
      if (jauge) jauge.style.width = (avance * 100).toFixed(1) + '%';
      if (avance >= 1 && !fini) {
        fini = true;
        clearInterval(tic);
        if (etat) etat.textContent = 'Analyse terminée.';
        montrer(resultat);
      }
    }, 100);
  }

  poserPrenom();

  // Qui demande à ne pas voir d'animation ne doit pas attendre quinze
  // secondes devant une barre qui ne bouge pas.
  var sobre = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (sobre) {
    lignes.forEach(function (l) { l.dataset.fait = 'oui'; });
    if (jauge) jauge.style.width = '100%';
    montrer(resultat);
  } else {
    animer();
  }
})();
