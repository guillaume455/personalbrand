/* =========================================================================
   MODIFIÉ LE 01/10/2026 — deux blocs seulement, le reste est intact.

   1. backend : branché sur le webhook Make qui reçoit les candidatures.
      L'URL d'un webhook Make n'est pas une clé secrète : elle n'autorise
      qu'à envoyer des données, jamais à en lire. Elle a donc sa place
      dans un fichier public, contrairement à une clé d'API Brevo.
   2. aimant.pdf : chemin du calcul de marge une fois le PDF déposé.
   3. aimant.webhook : le webhook du second scénario Make, celui qui range
      l'adresse dans la liste Brevo de l'aimant. Il est distinct de celui
      des candidatures, et il doit le rester (voir l'en-tête de capture.js).
      Mis à jour le 01/10/2026.

   preprod est passé à false le 01/10/2026, une fois le tunnel vérifié
   de bout en bout en conditions réelles : les repères de préproduction
   et les encarts « à fournir » ne s'affichent plus aux visiteurs.
   Le repasser à true pour retrouver les traces dans la console.
   ========================================================================= */
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
  // false depuis la mise en ligne du 01/10/2026 : masque les
  // avertissements de préproduction et les encarts « à fournir ».
  preprod: false,

  /* --- Backend du formulaire -------------------------------------------
     L'hébergement OVH est statique : aucun code ne s'exécute côté serveur.
     Les candidatures partent donc vers un service externe.
       type : 'supabase' | 'webhook' | ''      ('' = mode démo)
       url  : point d'entrée REST complet
       cle  : clé publique anonyme (Supabase) — jamais la service_role
  --------------------------------------------------------------------- */
  backend: {
    type: 'webhook',
    url: 'https://hook.eu1.make.com/6vnc2did7cxpr6fgvmik7pos3ht6enul',
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

    // Lien de paiement Stripe, 490 € TTC. Son adresse de succès doit pointer
    // vers /accompagnement/confirmation/ : c'est cette redirection qui donne
    // accès au calendrier, et rien d'autre.
    checkoutStripe: '',

    // Calendrier. Affiché UNIQUEMENT sur la page de confirmation, donc après
    // un paiement abouti (§34 et §37 : validation, puis Stripe, puis agenda).
    // Ne jamais l'exposer depuis la landing ni depuis la page de paiement.
    url: '',
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
    pdf: '/assets/docs/calcul-marge-guillaume-herbin.pdf',
    listeBrevo: '',             // identifiant de liste Brevo

    // Webhook Make propre à l'aimant, distinct de celui des candidatures.
    // Branché le 01/10/2026 sur le scénario « FORGE - aimant et decisions ».
    // L'adresse déposée part dans la liste Brevo « Aimant - calcul de marge ».
    webhook: 'https://hook.eu1.make.com/muqcspwws27p6gg1gkalkfqvoxgravdu',
  },

  /* --- Tunnel ----------------------------------------------------------
     Champ prévu dès maintenant pour le second tunnel « marchands » (§13) :
     la colonne existe en base dès la première candidature, il n'y aura pas
     de migration à faire.
  --------------------------------------------------------------------- */
  tunnel: 'lancement',
};
