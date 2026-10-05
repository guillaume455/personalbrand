/* =========================================================================
   Règle de qualification.

   Révisée le 01/10/2026 pour coller à l'arbitrage pris sur l'offre : le
   budget ne sert JAMAIS à écarter quelqu'un. La page de vente affirme que
   toutes les façons d'exercer ne demandent pas le même capital ; trier sur
   le capital contredirait cette promesse. Le capital reste demandé, mais
   uniquement pour préparer la séance.

   | Temps déclaré        | Délai déclaré                | Statut     |
   |----------------------|------------------------------|------------|
   | 5 h ou plus          | Ce mois / 3 mois / 6 mois    | qualifié   |
   | 5 h ou plus          | Je ne sais pas encore        | à revoir   |
   | Moins de 5 heures    | peu importe                  | à revoir   |

   Ce que la règle garde de la version précédente, et qu'il ne faut pas
   « améliorer » en passant :

   1. Le statut ne dépend que de deux réponses. Ni l'avancement, ni le
      capital, ni la question libre n'entrent dans le calcul.
   2. « non qualifié » n'est JAMAIS attribué automatiquement. Il résulte
      d'une lecture manuelle. La fonction ne renvoie que 'qualifie' ou
      'a_revoir'.
   3. Le statut n'est jamais montré au visiteur. Il choisit seulement la
      variante de la page de remerciement.

   Cette règle doit rester identique à celle du routeur Make, qui décide de
   l'e-mail envoyé. Si l'une change, changer l'autre le même jour : sinon
   la page peut annoncer un lien de réservation que l'e-mail contredit.
   ========================================================================= */
(function (racine) {
  'use strict';

  // Valeurs stockées par le formulaire. Les libellés affichés vivent dans le
  // HTML ; ici on ne manipule que ces clés, pour qu'une reformulation de
  // libellé ne casse jamais la règle.
  var TEMPS = ['moins_5h', '5_15h', '15_35h', 'plein'];
  var DELAI = ['ce_mois', '3_mois', '6_mois', 'ne_sais_pas'];

  // Les trois tranches hautes, c'est-à-dire « 5 heures ou plus ».
  var TEMPS_SUFFISANT = ['5_15h', '15_35h', 'plein'];
  // Un délai est engageant dès lors qu'il est daté.
  var DELAI_DATE = ['ce_mois', '3_mois', '6_mois'];

  function qualifier(temps, delai) {
    var tempsOk = TEMPS_SUFFISANT.indexOf(temps) !== -1;
    var delaiOk = DELAI_DATE.indexOf(delai) !== -1;
    return (tempsOk && delaiOk) ? 'qualifie' : 'a_revoir';
  }

  racine.GH = racine.GH || {};
  racine.GH.qualification = {
    TEMPS: TEMPS,
    DELAI: DELAI,
    TEMPS_SUFFISANT: TEMPS_SUFFISANT,
    DELAI_DATE: DELAI_DATE,
    qualifier: qualifier,
  };

  // Export Node pour la suite de tests, sans gêner le navigateur.
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = racine.GH.qualification;
  }
})(typeof window !== 'undefined' ? window : globalThis);
