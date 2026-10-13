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
  var email = reparerPlus((p.get('email') || '').trim().slice(0, 120));
  var eventId = (p.get('event_id') || '').trim().slice(0, 80);

  /* ---------- Le « + » des adresses e-mail --------------------------------
     Dans une adresse web, « + » est la vieille notation de l'espace.
     URLSearchParams respecte cette convention : si l'outil qui construit le
     lien n'a pas encodé le « + » en %2B, « marie+auto@exemple.fr » nous
     arrive en « marie auto@exemple.fr ».

     On le remet, car une espace n'existe pas dans une adresse e-mail : il n'y
     a donc aucun cas où cette réparation abîme une adresse valide. Si le lien
     est correctement encodé, il n'y a pas d'espace et rien ne se passe — les
     deux cas se rejoignent.

     À ne surtout pas appliquer au prénom : « Jean Pierre » est un prénom,
     pas une adresse abîmée. */
  function reparerPlus(valeur) {
    return valeur.indexOf(' ') === -1 ? valeur : valeur.replace(/ /g, '+');
  }

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
     d'afficher un cadre blanc.

     Pourquoi l'intégration officielle de Cal et non une iframe
     ------------------------------------------------------------
     Une iframe à hauteur fixe défile à l'intérieur d'elle-même. Or le
     formulaire de réservation de Cal porte une case de renonciation au droit
     de rétractation, obligatoire, placée juste avant le bouton de paiement :
     dans un cadre de hauteur fixe elle se retrouve sous le bas du cadre, et
     le client se heurte à un bouton qui refuse de valider sans qu'il voie
     pourquoi. L'intégration « inline » de Cal ajuste la hauteur du cadre à
     son contenu, ce qui supprime le défilement imbriqué.

     Ne pas contraindre la hauteur de l'hôte : c'est tout l'intérêt.
     min-height ne sert qu'à éviter un saut de mise en page au chargement. */

  var SCRIPT_CAL = 'https://app.cal.com/embed/embed.js';

  /* Extrait « guillaume-herbin/plan-de-lancement » de l'adresse de config.
     Renvoie null si ce n'est pas un lien Cal : on retombe alors sur l'iframe,
     pour qu'un changement de prestataire n'efface pas le calendrier. */
  function lienCal(url) {
    var m = /^https?:\/\/(?:app\.)?cal\.com\/([^?#]+)/.exec(url);
    if (!m) return null;
    return m[1].replace(/\/+$/, '') || null;
  }

  /* Chargeur officiel de Cal. Il met les appels en file d'attente tant que
     embed.js n'est pas chargé, d'où sa forme compacte : ne pas le « ranger »,
     c'est le code du prestataire. */
  function amorcerCal() {
    (function (C, A, L) {
      var p = function (a, ar) { a.q.push(ar); };
      var d = C.document;
      C.Cal = C.Cal || function () {
        var cal = C.Cal, ar = arguments;
        if (!cal.loaded) {
          cal.ns = {}; cal.q = cal.q || [];
          d.head.appendChild(d.createElement('script')).src = A;
          cal.loaded = true;
        }
        if (ar[0] === L) {
          var api = function () { p(api, arguments); };
          var nom = ar[1];
          api.q = api.q || [];
          if (typeof nom === 'string') {
            cal.ns[nom] = cal.ns[nom] || api;
            p(cal.ns[nom], ar);
            p(cal, ['initNamespace', nom]);
          } else p(cal, ar);
          return;
        }
        p(cal, ar);
      };
    })(window, SCRIPT_CAL, 'init');
  }

  /* Secours : si Cal n'a rien affiché, un lien visible valant mieux qu'un
     cadre vide. On ne perd pas la vente parce qu'un script n'a pas répondu. */
  function secoursAgenda(hote, url) {
    if (hote.querySelector('iframe')) return;     // Cal a fini par s'afficher
    var sep = url.indexOf('?') === -1 ? '?' : '&';
    var lien = url + (email ? sep + 'email=' + encodeURIComponent(email) : '');
    hote.innerHTML = '';
    var p = document.createElement('p');
    p.textContent = 'Le calendrier met du temps à s’afficher. ';
    var a = document.createElement('a');
    a.className = 'cta';
    a.href = lien;
    a.target = '_blank';
    a.rel = 'noopener';
    a.textContent = 'Choisir mon créneau';
    p.appendChild(a);
    hote.appendChild(p);
  }

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

    var lien = lienCal(url);
    if (!lien) {
      // Prestataire autre que Cal : on garde l'ancien cadre plutôt que rien.
      var sep = url.indexOf('?') === -1 ? '?' : '&';
      var cadre = document.createElement('iframe');
      cadre.src = url + (email ? sep + 'email=' + encodeURIComponent(email) : '');
      cadre.title = 'Choix du créneau et paiement';
      cadre.style.cssText = 'width:100%;min-height:720px;border:0;border-radius:3px';
      hote.appendChild(cadre);
    } else {
      hote.style.minHeight = '520px';
      amorcerCal();
      window.Cal('init');
      // Le prénom et l'e-mail viennent du questionnaire : les redemander
      // allonge le formulaire, et un formulaire plus long cache la case.
      var pre = {};
      if (prenom) pre.name = prenom;
      if (email) pre.email = email;
      window.Cal('inline', {
        elementOrSelector: hote,
        calLink: lien,
        config: pre,
      });
      // Cal peut ne jamais répondre : script bloqué, réseau coupé, panne.
      setTimeout(function () { secoursAgenda(hote, url); }, 9000);
    }

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
