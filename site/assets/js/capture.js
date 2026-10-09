/* =========================================================================
   MODIFIÉ LE 01/10/2026 — une seule chose change : la destination.

   Avant, ce formulaire postait vers cfg.backend, c'est-à-dire exactement
   la même adresse que les candidatures. Tant que ce champ était vide,
   personne ne s'en apercevait. Maintenant qu'il pointe sur le webhook
   Make des candidatures, une adresse laissée ici partirait dans le
   scénario des candidatures et déclencherait l'e-mail de réponse, avec
   un prénom vide.

   Il lit donc désormais aimant.webhook, qui lui est propre. Ce champ
   reste vide jusqu'à la création du second scénario Make : d'ici là, le
   formulaire répond normalement au visiteur et journalise dans la
   console, sans rien envoyer.
   ========================================================================= */
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

      // Le formulaire de l'aimant n'emprunte PAS le backend des candidatures.
      // Les deux flux n'ont ni le même contenu ni la même suite d'e-mails :
      // envoyer une simple adresse dans le webhook des candidatures
      // déclencherait l'e-mail de réponse à candidature, avec un prénom vide.
      // Tant que aimant.webhook est vide, ce formulaire reste en mode démo.
      var b = { type: (cfg.aimant && cfg.aimant.webhook) ? 'webhook' : '',
                url: (cfg.aimant && cfg.aimant.webhook) || '' };
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
        mesure.envoyer('lead_magnet_signup', { tunnel: donnees.tunnel });
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
