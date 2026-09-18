/* =========================================================================
   Règle de qualification — implémentation littérale de la table du §3.

   | Capital déclaré              | Délai déclaré                  | Statut     |
   |------------------------------|--------------------------------|------------|
   | 5 000 € ou plus (3 tranches) | Ce mois / 3 mois / 6 mois      | qualifié   |
   | 5 000 € ou plus              | Je ne sais pas encore          | à revoir   |
   | Moins de 5 000 €             | peu importe                    | à revoir   |
   | Je veux justement en parler  | peu importe                    | à revoir   |

   Trois points que le cahier des charges impose et qu'il ne faut pas
   « améliorer » en passant :

   1. Le statut ne dépend QUE du capital et du délai. Ni l'avancement, ni le
      temps disponible, ni la question libre n'entrent dans le calcul. Le
      modèle (achat-revente, intermédiation…) n'est pas demandé : c'est
      l'objet même du diagnostic.
   2. « non qualifié » n'est JAMAIS attribué automatiquement. Il résulte
      uniquement d'une lecture manuelle par Guillaume. La fonction ne peut
      donc renvoyer que 'qualifie' ou 'a_revoir'.
   3. Le statut n'est jamais montré au visiteur. Il pilote seulement
      l'affichage du lien de réservation et la notification envoyée.
   ========================================================================= */
(function (racine) {
  'use strict';

  // Valeurs stockées par le formulaire. Les libellés affichés vivent dans le
  // HTML ; ici on ne manipule que ces clés, pour qu'une reformulation de
  // libellé ne casse jamais la règle.
  var CAPITAL = ['moins_5k', '5k_20k', '20k_50k', 'plus_50k', 'a_discuter'];
  var DELAI = ['ce_mois', '3_mois', '6_mois', 'ne_sais_pas'];

  // Les trois tranches hautes, c'est-à-dire « 5 000 € ou plus ».
  var CAPITAL_SUFFISANT = ['5k_20k', '20k_50k', 'plus_50k'];
  // Un délai est engageant dès lors qu'il est daté.
  var DELAI_DATE = ['ce_mois', '3_mois', '6_mois'];

  function qualifier(capital, delai) {
    var capitalOk = CAPITAL_SUFFISANT.indexOf(capital) !== -1;
    var delaiOk = DELAI_DATE.indexOf(delai) !== -1;
    return (capitalOk && delaiOk) ? 'qualifie' : 'a_revoir';
  }

  racine.GH = racine.GH || {};
  racine.GH.qualification = {
    CAPITAL: CAPITAL,
    DELAI: DELAI,
    CAPITAL_SUFFISANT: CAPITAL_SUFFISANT,
    DELAI_DATE: DELAI_DATE,
    qualifier: qualifier,
  };

  // Export Node pour la suite de tests, sans gêner le navigateur.
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = racine.GH.qualification;
  }
})(typeof window !== 'undefined' ? window : globalThis);
