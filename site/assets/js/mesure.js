/* =========================================================================
   Consentement et mesure.

   §10 : GA4 et pixel Meta, « tous deux chargés après consentement ».
   §11 : bandeau cookies « avec refus aussi accessible que l'acceptation ».

   Conséquence tenue ici : AUCUN script tiers, AUCUN cookie, AUCUN appel
   réseau de mesure tant que le visiteur n'a pas cliqué « Accepter ». Les
   événements déclenchés avant la décision ne sont pas perdus pour autant :
   ils sont mis en file d'attente et rejoués si le consentement arrive.
   S'il est refusé, la file est jetée.
   ========================================================================= */
(function () {
  'use strict';

  var CLE = 'gh-consent';         // 'oui' | 'non'
  var cfg = (window.GH && window.GH.config) || {};
  var mesure = cfg.mesure || {};
  var file = [];
  var charge = false;

  function lire() {
    try { return localStorage.getItem(CLE); } catch (e) { return null; }
  }
  function ecrire(v) {
    try { localStorage.setItem(CLE, v); } catch (e) {}
  }

  /* ---------- Chargement effectif des outils, après accord seulement ---- */
  function chargerGA4() {
    if (!mesure.ga4) return;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(mesure.ga4);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', mesure.ga4, { anonymize_ip: true });
  }

  function chargerMeta() {
    if (!mesure.meta) return;
    /* eslint-disable */
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}
    (window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    /* eslint-enable */
    window.fbq('init', mesure.meta);
    window.fbq('track', 'PageView');
  }

  function activer() {
    if (charge) return;
    charge = true;
    chargerGA4();
    chargerMeta();
    file.forEach(function (e) { envoyer(e.nom, e.params); });
    file = [];
  }

  /* ---------- Envoi d'un événement --------------------------------------
     Correspondance GA4 -> Meta pour les deux événements qui comptent
     vraiment côté publicité : le formulaire et l'achat.               */
  var VERS_META = { form_submit: 'Lead', purchase: 'Purchase', lead_magnet_submit: 'Lead' };

  function envoyer(nom, params) {
    params = params || {};
    if (!charge) {
      // Avant la décision : on retient, on n'envoie rien.
      if (file.length < 50) file.push({ nom: nom, params: params });
      if (cfg.preprod) console.info('[mesure, en attente de consentement]', nom, params);
      return;
    }
    if (window.gtag) window.gtag('event', nom, params);
    if (window.fbq && VERS_META[nom]) {
      var m = {};
      if (nom === 'purchase') { m.value = params.value; m.currency = params.currency; }
      window.fbq('track', VERS_META[nom], m);
    }
    if (cfg.preprod) console.info('[mesure]', nom, params);
  }

  /* ---------- Bandeau ---------------------------------------------------- */
  function bandeau() {
    var el = document.querySelector('[data-cookies]');
    if (!el) return;
    var choix = lire();
    if (choix === 'oui') { activer(); return; }
    if (choix === 'non') return;

    // Aucun choix enregistré : on propose, sans rien charger. Le drapeau posé
    // sur le body réserve la place occupée par le bandeau, pour qu'il ne
    // recouvre pas le pied de page et ses liens légaux.
    requestAnimationFrame(function () {
      el.setAttribute('data-visible', 'true');
      document.body.setAttribute('data-bandeau', 'visible');
    });

    function refermer() {
      el.removeAttribute('data-visible');
      document.body.removeAttribute('data-bandeau');
    }
    el.querySelector('[data-accepter]').addEventListener('click', function () {
      ecrire('oui'); refermer(); activer();
    });
    el.querySelector('[data-refuser]').addEventListener('click', function () {
      ecrire('non'); refermer(); file = [];
    });
  }

  /* ---------- Événements automatiques ------------------------------------ */
  function auto() {
    envoyer('page_view', { page_path: location.pathname });

    // Chaque CTA porte sa position, pour savoir lequel convertit (§10).
    document.querySelectorAll('[data-cta]').forEach(function (b) {
      b.addEventListener('click', function () {
        envoyer('cta_click', { position: b.dataset.cta });
      });
    });

    // UTM de la première visite, conservés jusqu'à l'envoi du formulaire.
    try {
      var p = new URLSearchParams(location.search);
      var u = {};
      ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
        if (p.get(k)) u[k] = p.get(k);
      });
      if (Object.keys(u).length && !sessionStorage.getItem('gh-utm')) {
        sessionStorage.setItem('gh-utm', JSON.stringify(u));
      }
    } catch (e) {}
  }

  function utm() {
    try { return JSON.parse(sessionStorage.getItem('gh-utm') || '{}'); }
    catch (e) { return {}; }
  }

  window.GH = window.GH || {};
  window.GH.mesure = { envoyer: envoyer, utm: utm, consentement: lire };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { bandeau(); auto(); });
  } else { bandeau(); auto(); }
})();
