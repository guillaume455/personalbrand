/* =========================================================================
   Capture e-mail du calcul de marge (bloc 10 et page /calcul-marge).
   §11 : consentement séparé, non pré-coché.
   ========================================================================= */
(function () {
  'use strict';
  var cfg = (window.GH && window.GH.config) || {};
  var mesure = (window.GH && window.GH.mesure) || { envoyer: function () {}, utm: function () { return {}; } };

  document.querySelectorAll('[data-capture]').forEach(function (form) {
    var etat = form.querySelector('[data-capture-etat]');
    var bouton = form.querySelector('button[type=submit]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = form.querySelector('input[type=email]');
      var accord = form.querySelector('input[type=checkbox]');

      var dire = function (texte, erreur) {
        if (!etat) return;
        etat.hidden = false;
        etat.textContent = texte;
        etat.className = erreur ? 'erreur' : 'encart encart-ok';
      };

      if (!email.checkValidity()) {
        email.setAttribute('aria-invalid', 'true');
        dire('Cette adresse e-mail ne semble pas valide.', true);
        email.focus();
        return;
      }
      if (accord && !accord.checked) {
        dire('Coche la case pour que je puisse t\'envoyer le document.', true);
        accord.focus();
        return;
      }
      if (form.querySelector('[name="_piege"]').value) { dire('Merci.'); return; }

      email.removeAttribute('aria-invalid');
      bouton.disabled = true;
      var libelle = bouton.textContent;
      bouton.textContent = 'Envoi…';

      var donnees = {
        horodatage: new Date().toISOString(),
        email: email.value.trim().toLowerCase(),
        consentement: true,
        source: 'calcul-marge',
        tunnel: cfg.tunnel || 'lancement',
        page: location.pathname,
        utm: mesure.utm(),
      };

      var b = cfg.backend || {};
      var envoi;
      if (!b.type || !b.url) {
        console.info('[capture] Mode démo, rien n\'est transmis. Charge utile :', donnees);
        envoi = Promise.resolve();
      } else {
        var entetes = { 'Content-Type': 'application/json' };
        var url = b.url;
        if (b.type === 'supabase') {
          url = b.url.replace(/\/$/, '') + '/rest/v1/inscriptions';
          entetes.apikey = b.cle;
          entetes.Authorization = 'Bearer ' + b.cle;
          entetes.Prefer = 'return=minimal';
        }
        envoi = fetch(url, { method: 'POST', headers: entetes, body: JSON.stringify(donnees) })
          .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); });
      }

      envoi.then(function () {
        mesure.envoyer('lead_magnet_submit', { tunnel: donnees.tunnel });
        if (form.dataset.merci) { location.href = form.dataset.merci; return; }
        form.reset();
        bouton.disabled = false;
        bouton.textContent = libelle;
        dire('C\'est envoyé. Regarde ta boîte mail dans quelques minutes — et le dossier « promotions » si tu ne vois rien.');
      }).catch(function (err) {
        console.error('[capture] échec', err);
        bouton.disabled = false;
        bouton.textContent = libelle;
        dire('L\'envoi n\'a pas abouti. Réessaie, ou écris à contact@guillaumeherbin.fr.', true);
      });
    });
  });
})();
