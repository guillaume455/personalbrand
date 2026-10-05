/* =========================================================================
   Pages d'issue : /merci, /reservation, /confirmation.
   ========================================================================= */
(function () {
  'use strict';
  var cfg = (window.GH && window.GH.config) || {};
  var mesure = (window.GH && window.GH.mesure) || { envoyer: function () {} };

  function issue() {
    try { return JSON.parse(sessionStorage.getItem('gh-issue') || 'null'); }
    catch (e) { return null; }
  }

  /* ---------- /accompagnement/merci -------------------------------------
     Deux variantes selon le statut calculé. Le statut lui-même n'est jamais
     écrit à l'écran (§3) : il ne fait que choisir la variante. */
  var merci = document.querySelector('[data-merci]');
  if (merci) {
    var o = issue();
    var qualifie = !!o && o.statut === 'qualifie';
    var vQ = merci.querySelector('[data-variante="qualifie"]');
    var vR = merci.querySelector('[data-variante="a_revoir"]');
    if (vQ) vQ.hidden = !qualifie;
    if (vR) vR.hidden = qualifie;

    if (o && o.prenom) {
      merci.querySelectorAll('[data-prenom]').forEach(function (el) {
        el.textContent = ' ' + o.prenom;
      });
    }
    // Sans passage par le formulaire (accès direct à l'URL), on affiche la
    // variante prudente plutôt qu'un lien de réservation non mérité.
    if (!o && vR) { vR.hidden = false; if (vQ) vQ.hidden = true; }
  }

  /* ---------- /accompagnement/reservation -------------------------------
     §6 et §11 : la case de renoncement au droit de rétractation doit être
     obligatoire à la réservation. Sans elle, toute séance tenue dans les
     14 jours reste remboursable. Le §6 demande de vérifier en semaine 1 si
     Cal.com peut porter cette case ; en attendant, elle est posée ici et
     conditionne l'accès au module. C'est le repli propre décrit au §6. */
  var reserv = document.querySelector('[data-reservation]');
  if (reserv) {
    var accord = reserv.querySelector('[data-renoncement]');
    var zone = reserv.querySelector('[data-module]');
    var attente = reserv.querySelector('[data-avant-accord]');
    var monte = false;

    var afficherModule = function () {
      if (monte) return;
      monte = true;
      if (attente) attente.hidden = true;
      zone.hidden = false;
      try {
        sessionStorage.setItem('gh-renoncement', new Date().toISOString());
      } catch (e) {}

      // §34 : l'ordre est validation, puis paiement, puis agenda. Cette page
      // n'expose donc que le paiement ; l'agenda vit sur la page d'après, que
      // Stripe n'atteint qu'après un règlement abouti.
      var r = cfg.reservation || {};
      if (!r.checkoutStripe) {
        zone.querySelector('[data-demo]').hidden = false;
        return;
      }
      var lien = zone.querySelector('[data-vers-paiement]');
      if (lien) {
        lien.href = r.checkoutStripe;
        lien.hidden = false;
        lien.addEventListener('click', function () {
          mesure.envoyer('checkout_start', {
            value: (cfg.offre || {}).prix || 490,
            currency: (cfg.offre || {}).devise || 'EUR',
          });
        });
      }
    };

    if (accord) {
      accord.addEventListener('change', function () {
        if (accord.checked) afficherModule();
        else if (zone) { /* déjà affiché : on ne le retire pas, la case reste cochée pour valider */ }
      });
    }
  }

  /* ---------- /accompagnement/confirmation ------------------------------- */
  // §37 : l'agenda n'est atteignable qu'ici, c'est-à-dire après paiement.
  var conf = document.querySelector('[data-confirmation]');
  if (conf) {
    var offre = cfg.offre || {};
    var zoneAgenda = conf.querySelector('[data-agenda]');
    if (zoneAgenda) {
      var ra = cfg.reservation || {};
      if (ra.url) {
        var cal = document.createElement('iframe');
        cal.src = ra.url;
        cal.title = 'Choix de ton créneau';
        cal.loading = 'lazy';
        cal.style.cssText = 'width:100%;min-height:760px;border:0;border-radius:16px';
        zoneAgenda.insertBefore(cal, zoneAgenda.firstChild);
        mesure.envoyer('booking_page_view', {});
      } else {
        var d = zoneAgenda.querySelector('[data-demo]');
        if (d) d.hidden = false;
      }
    }
    mesure.envoyer('purchase', {
      value: offre.prix || 490,
      currency: offre.devise || 'EUR',
      items: [{ item_name: 'Diagnostic individuel', price: offre.prix || 490, quantity: 1 }],
    });
    try {
      var o2 = issue();
      if (o2 && o2.prenom) {
        conf.querySelectorAll('[data-prenom]').forEach(function (el) {
          el.textContent = ' ' + o2.prenom;
        });
      }
    } catch (e) {}
  }
})();
