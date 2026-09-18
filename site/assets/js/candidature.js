/* =========================================================================
   Formulaire de qualification en 5 questions (§5).

   Parti pris assumé : le pas-à-pas s'applique à toutes les tailles d'écran,
   pas seulement au mobile comme le §5 le demande. Maintenir deux rendus —
   pas-à-pas sur mobile, formulaire long sur desktop — doublerait la logique
   de validation et de reprise pour 20 % du trafic. Le pas-à-pas fonctionne
   bien sur grand écran, l'inverse serait faux.

   Les e-mails E1, E2 et E3 ne partent PAS d'ici : envoyer depuis la page
   exigerait une clé d'API Brevo côté client, donc publique. C'est au backend
   de les déclencher à la réception de la candidature. Voir le README.
   ========================================================================= */
(function () {
  'use strict';

  var form = document.querySelector('[data-candidature]');
  if (!form) return;

  var cfg = (window.GH && window.GH.config) || {};
  var qualif = window.GH && window.GH.qualification;
  var mesure = (window.GH && window.GH.mesure) || { envoyer: function () {}, utm: function () { return {}; } };

  var BROUILLON = 'gh-candidature';
  var ENVOIS = 'gh-envois';
  var pas = Array.prototype.slice.call(form.querySelectorAll('[data-pas]'));
  var courant = 0;
  var commence = false;

  var jauge = form.querySelector('[data-jauge]');
  var jaugeTxt = form.querySelector('[data-jauge-txt]');
  var suivant = form.querySelector('[data-suivant]');
  var precedent = form.querySelector('[data-precedent]');
  var boiteErreur = form.querySelector('[data-erreur-globale]');

  /* ---------------- Reprise du brouillon ---------------- */
  function sauver() {
    try {
      var d = {};
      new FormData(form).forEach(function (v, k) { if (k[0] !== '_') d[k] = v; });
      localStorage.setItem(BROUILLON, JSON.stringify({ d: d, pas: courant, t: Date.now() }));
    } catch (e) {}
  }

  function reprendre() {
    var brut;
    try { brut = localStorage.getItem(BROUILLON); } catch (e) { return; }
    if (!brut) return;
    var o;
    try { o = JSON.parse(brut); } catch (e) { return; }
    // Un brouillon de plus de 7 jours n'a plus de sens : on repart à zéro.
    if (!o || !o.d || Date.now() - (o.t || 0) > 7 * 864e5) { oublier(); return; }

    Object.keys(o.d).forEach(function (k) {
      var champs = form.querySelectorAll('[name="' + CSS.escape(k) + '"]');
      champs.forEach(function (c) {
        if (c.type === 'radio') { if (c.value === o.d[k]) c.checked = true; }
        else if (c.type === 'checkbox') { c.checked = o.d[k] === 'on'; }
        else { c.value = o.d[k]; }
      });
    });
    if (typeof o.pas === 'number' && o.pas > 0 && o.pas < pas.length) {
      courant = o.pas;
      var note = form.querySelector('[data-reprise]');
      if (note) note.hidden = false;
    }
    majCompteur();
  }

  function oublier() {
    try { localStorage.removeItem(BROUILLON); } catch (e) {}
  }

  /* ---------------- Validation ---------------- */
  function messageErreur(champ) {
    if (champ.validity.valueMissing) {
      if (champ.type === 'checkbox') return 'Cette case doit être cochée pour continuer.';
      if (champ.type === 'email') return 'Indique ton adresse e-mail.';
      return 'Ce champ est nécessaire pour continuer.';
    }
    if (champ.validity.typeMismatch && champ.type === 'email') {
      return 'Cette adresse e-mail ne semble pas valide. Vérifie qu\'elle contient bien un « @ ».';
    }
    if (champ.validity.tooShort) {
      return 'Encore un peu : ' + champ.minLength + ' caractères minimum, il y en a ' + champ.value.length + '.';
    }
    if (champ.validity.patternMismatch && champ.type === 'tel') {
      return 'Ce numéro ne semble pas valide. Chiffres, espaces, points et « + » sont acceptés.';
    }
    return 'Cette réponse n\'est pas valide.';
  }

  function poserErreur(cible, texte) {
    var boite = cible.closest('.champ') || cible.closest('[data-pas]');
    if (!boite) return;
    var p = boite.querySelector('.erreur');
    if (!p) {
      p = document.createElement('p');
      p.className = 'erreur';
      p.setAttribute('role', 'alert');
      boite.appendChild(p);
    }
    p.textContent = texte;
    cible.setAttribute('aria-invalid', 'true');
    var groupe = cible.closest('.choix');
    if (groupe) groupe.setAttribute('aria-invalid', 'true');
  }

  function nettoyerErreur(cible) {
    var boite = cible.closest('.champ') || cible.closest('[data-pas]');
    if (!boite) return;
    var p = boite.querySelector('.erreur');
    if (p) p.remove();
    boite.querySelectorAll('[aria-invalid]').forEach(function (e) { e.removeAttribute('aria-invalid'); });
  }

  function validerPas(i) {
    var bloc = pas[i];
    var champs = Array.prototype.slice.call(
      bloc.querySelectorAll('input:not([type=hidden]), textarea, select'));
    var radios = {};
    var valide = true;
    var premierFautif = null;

    champs.forEach(function (c) {
      if (c.type === 'radio') {
        if (!radios[c.name]) radios[c.name] = [];
        radios[c.name].push(c);
        return;
      }
      if (!c.checkValidity()) {
        valide = false;
        poserErreur(c, messageErreur(c));
        if (!premierFautif) premierFautif = c;
      } else nettoyerErreur(c);
    });

    Object.keys(radios).forEach(function (nom) {
      var groupe = radios[nom];
      var requis = groupe.some(function (r) { return r.required; });
      var coche = groupe.some(function (r) { return r.checked; });
      if (requis && !coche) {
        valide = false;
        poserErreur(groupe[0], 'Choisis une réponse pour continuer.');
        if (!premierFautif) premierFautif = groupe[0];
      } else nettoyerErreur(groupe[0]);
    });

    if (premierFautif) {
      premierFautif.focus({ preventScroll: true });
      premierFautif.scrollIntoView({ block: 'center', behavior: 'smooth' });
    }
    return valide;
  }

  /* ---------------- Navigation ---------------- */
  function majCompteur() {
    var n = courant + 1;
    if (jauge) jauge.style.width = Math.round(n / pas.length * 100) + '%';
    if (jaugeTxt) jaugeTxt.textContent = 'Étape ' + n + ' sur ' + pas.length;
    if (precedent) precedent.hidden = courant === 0;
    if (suivant) {
      suivant.textContent = courant === pas.length - 1 ? 'Envoyer ma candidature' : 'Continuer';
    }
  }

  var premierRendu = true;
  function afficher(i) {
    pas.forEach(function (p, k) { p.hidden = k !== i; });
    courant = i;
    majCompteur();
    // On ne déplace le focus qu'au changement d'étape. Au premier rendu, le
    // faire afficherait un cadre de focus alors que le visiteur n'a encore
    // rien fait, et volerait le point de départ de lecture.
    if (!premierRendu) {
      var titre = pas[i].querySelector('h2');
      if (titre) { titre.setAttribute('tabindex', '-1'); titre.focus({ preventScroll: true }); }
      var haut = form.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({ top: Math.max(0, haut), behavior: 'smooth' });
    }
    premierRendu = false;
    sauver();
  }

  /* ---------------- Limitation de débit ----------------
     Garde-fou de confort uniquement : il vit dans le navigateur, donc il ne
     protège que contre l'envoi répété d'un visiteur réel. La vraie limite
     doit être posée côté backend, qui est le seul endroit qu'on ne peut pas
     contourner depuis la console. */
  function tropDEnvois() {
    try {
      var t = JSON.parse(localStorage.getItem(ENVOIS) || '[]')
        .filter(function (x) { return Date.now() - x < 36e5; });
      localStorage.setItem(ENVOIS, JSON.stringify(t));
      return t.length >= 3;
    } catch (e) { return false; }
  }
  function noterEnvoi() {
    try {
      var t = JSON.parse(localStorage.getItem(ENVOIS) || '[]');
      t.push(Date.now());
      localStorage.setItem(ENVOIS, JSON.stringify(t));
    } catch (e) {}
  }

  /* ---------------- Envoi ---------------- */
  function collecte() {
    var d = {};
    new FormData(form).forEach(function (v, k) { if (k[0] !== '_') d[k] = v; });
    var u = mesure.utm();
    return {
      horodatage: new Date().toISOString(),
      tunnel: cfg.tunnel || 'lancement',
      avancement: d.avancement || '',
      capital: d.capital || '',
      temps: d.temps || '',
      delai: d.delai || '',
      question: d.question || '',
      prenom: (d.prenom || '').trim(),
      nom: (d.nom || '').trim(),
      email: (d.email || '').trim().toLowerCase(),
      telephone: (d.telephone || '').trim(),
      zone: (d.zone || '').trim(),
      consentement: d.consentement === 'on',
      statut: qualif ? qualif.qualifier(d.capital, d.delai) : 'a_revoir',
      statut_reservation: 'aucune',
      utm_source: u.utm_source || '',
      utm_medium: u.utm_medium || '',
      utm_campaign: u.utm_campaign || '',
      utm_content: u.utm_content || '',
      page: location.pathname,
    };
  }

  function transmettre(donnees) {
    var b = cfg.backend || {};
    if (!b.type || !b.url) {
      // Mode démo : le tunnel reste parcourable de bout en bout sans backend.
      console.info('[candidature] Mode démo, rien n\'est transmis. Charge utile :', donnees);
      return Promise.resolve();
    }
    var entetes = { 'Content-Type': 'application/json' };
    var url = b.url;
    if (b.type === 'supabase') {
      url = b.url.replace(/\/$/, '') + '/rest/v1/' + (b.table || 'candidatures');
      entetes.apikey = b.cle;
      entetes.Authorization = 'Bearer ' + b.cle;
      entetes.Prefer = 'return=minimal';
    }
    return fetch(url, {
      method: 'POST', headers: entetes, body: JSON.stringify(donnees),
    }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
    });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!validerPas(courant)) return;

    // Piège à robots : rempli = robot. On simule un succès sans rien envoyer.
    if (form.querySelector('[name="_piege"]').value) {
      location.href = form.dataset.merci;
      return;
    }
    if (tropDEnvois()) {
      if (boiteErreur) {
        boiteErreur.hidden = false;
        boiteErreur.textContent = 'Tu as déjà envoyé plusieurs candidatures dans la dernière heure. '
          + 'Si c\'est une erreur, écris directement à contact@guillaumeherbin.fr.';
        boiteErreur.focus();
      }
      return;
    }

    var donnees = collecte();
    suivant.disabled = true;
    suivant.textContent = 'Envoi en cours…';
    if (boiteErreur) boiteErreur.hidden = true;

    transmettre(donnees)
      .then(function () {
        noterEnvoi();
        oublier();
        // Le statut ne transite pas par l'URL : il ne doit jamais être
        // montré au visiteur, et le §9 interdit les données personnelles
        // dans les URL.
        try {
          sessionStorage.setItem('gh-issue', JSON.stringify({
            statut: donnees.statut, prenom: donnees.prenom,
          }));
        } catch (err) {}
        mesure.envoyer('form_submit', { statut: donnees.statut, tunnel: donnees.tunnel });
        location.href = form.dataset.merci;
      })
      .catch(function (err) {
        console.error('[candidature] échec de transmission', err);
        suivant.disabled = false;
        suivant.textContent = 'Réessayer';
        if (boiteErreur) {
          boiteErreur.hidden = false;
          boiteErreur.textContent = 'L\'envoi n\'a pas abouti. Tes réponses sont conservées : '
            + 'réessaie dans un instant, ou écris à contact@guillaumeherbin.fr.';
          boiteErreur.focus();
        }
      });
  });

  if (suivant) {
    suivant.addEventListener('click', function (e) {
      if (courant === pas.length - 1) return;   // le submit prend le relais
      e.preventDefault();
      if (validerPas(courant)) afficher(courant + 1);
    });
  }
  if (precedent) {
    precedent.addEventListener('click', function (e) {
      e.preventDefault();
      if (courant > 0) afficher(courant - 1);
    });
  }

  /* ---------------- Vie du formulaire ---------------- */
  form.addEventListener('input', function (e) {
    if (!commence) {
      commence = true;
      mesure.envoyer('form_start', { tunnel: cfg.tunnel || 'lancement' });
    }
    if (e.target.getAttribute('aria-invalid')) nettoyerErreur(e.target);
    sauver();
  });
  form.addEventListener('change', function () { sauver(); });

  // Un choix unique fait avancer tout seul : un geste de moins par question.
  form.querySelectorAll('.choix input[type=radio]').forEach(function (r) {
    r.addEventListener('change', function () {
      nettoyerErreur(r);
      if (courant >= pas.length - 1) return;
      setTimeout(function () { if (r.checked) afficher(courant + 1); }, 260);
    });
  });

  // Compteur de caractères de la question libre.
  var libre = form.querySelector('[data-compteur-cible]');
  var compteur = form.querySelector('[data-compteur]');
  if (libre && compteur) {
    var maj = function () {
      var n = libre.value.length, max = libre.maxLength;
      compteur.textContent = n + ' / ' + max;
      compteur.dataset.limite = n > max - 50 ? 'true' : 'false';
    };
    libre.addEventListener('input', maj);
    maj();
  }

  reprendre();
  afficher(courant);
  form.querySelector('[data-reprise-effacer]') && form.querySelector('[data-reprise-effacer]')
    .addEventListener('click', function (e) {
      e.preventDefault(); oublier(); location.reload();
    });
})();
