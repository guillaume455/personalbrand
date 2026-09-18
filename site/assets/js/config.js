/* =========================================================================
   Configuration du tunnel — SEUL fichier à modifier quand les comptes
   externes sont ouverts. Aucune clé n'est codée en dur ailleurs.

   Tout ce qui est vide ci-dessous met la fonction correspondante en
   « mode démo » : le tunnel reste navigable de bout en bout, les envois
   sont journalisés dans la console au lieu de partir, et un bandeau
   discret le signale en préproduction. Rien ne casse.

   ATTENTION : ce fichier est public, comme tout ce qui est servi au
   navigateur. N'y mettre QUE des clés publiques (clé anonyme Supabase,
   identifiant de mesure, clé publiable Stripe). Jamais de clé secrète,
   jamais de clé d'API Brevo : les envois d'e-mails doivent partir du
   backend, pas de la page.
   ========================================================================= */
window.GH = window.GH || {};

window.GH.config = {

  /* --- Repère d'environnement ------------------------------------------ */
  // Passer à false le jour de la mise en ligne : masque les avertissements
  // de préproduction et les encarts « à fournir ».
  preprod: true,

  /* --- Backend du formulaire -------------------------------------------
     L'hébergement OVH est statique : aucun code ne s'exécute côté serveur.
     Les candidatures partent donc vers un service externe.
       type : 'supabase' | 'webhook' | ''      ('' = mode démo)
       url  : point d'entrée REST complet
       cle  : clé publique anonyme (Supabase) — jamais la service_role
  --------------------------------------------------------------------- */
  backend: {
    type: '',
    url: '',
    cle: '',
    table: 'candidatures',
  },

  /* --- Réservation et paiement -----------------------------------------
     Cal.com de préférence, Calendly en repli (§6). L'événement doit être
     réglé sur 90 min, Google Meet, Europe/Paris, 8 par semaine au plus,
     48 h de préavis, tampons de 30 min, paiement Stripe obligatoire.
  --------------------------------------------------------------------- */
  reservation: {
    fournisseur: '',            // 'cal' | 'calendly' | ''
    url: '',                    // ex. https://cal.com/guillaume-herbin/diagnostic
    // Repli documenté au §6 : si la case de renoncement au droit de
    // rétractation ne peut pas être rendue obligatoire dans Cal.com, on
    // bascule sur un paiement Stripe portant la case, et le lien de
    // réservation part dans l'e-mail de confirmation de paiement.
    checkoutStripe: '',
  },

  /* --- Mesure -----------------------------------------------------------
     Rien ne se charge avant un consentement explicite (§10 et §11).
  --------------------------------------------------------------------- */
  mesure: {
    ga4: '',                    // ex. G-XXXXXXXXXX
    meta: '',                   // identifiant du pixel
  },

  /* --- Offre ------------------------------------------------------------ */
  offre: {
    prix: 490,
    devise: 'EUR',
    prixTexte: '490 €',
    duree: 90,
  },

  /* --- Aimant à e-mails -------------------------------------------------
     Le PDF du calcul de marge, à décliner depuis le carrousel existant.
  --------------------------------------------------------------------- */
  aimant: {
    pdf: '',                    // ex. /assets/doc/calcul-marge.pdf
    listeBrevo: '',             // identifiant de liste Brevo
  },

  /* --- Tunnel ----------------------------------------------------------
     Champ prévu dès maintenant pour le second tunnel « marchands » (§13) :
     la colonne existe en base dès la première candidature, il n'y aura pas
     de migration à faire.
  --------------------------------------------------------------------- */
  tunnel: 'lancement',
};
