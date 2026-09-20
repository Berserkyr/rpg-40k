# C3.2.1 — Tableau de bord et registre de pilotage

**Date du relevé initial :** 20 septembre 2026.  
**Périmètre :** préparation de la phase de stabilisation, pas pourcentage d'achèvement historique du jeu.  
**Référence technique observée :** `6119aab` ; version déclarée 1.3.0 ; copie de travail modifiée.  
**Statut :** outil de suivi initialisé, non encore alimenté par une période d'exécution.

## 1. Lecture du tableau

Le [planning](01_METHODOLOGIE_PLANNING_RESSOURCES.md) définit T01–T13. Je retiens un tableau Markdown sous Git pour conserver les références, décisions et écarts au même endroit que les preuves. Je n'assimile ni le nombre de commits à du temps travaillé, ni les métriques serveur à un suivi de budget.

**NR = non renseigné ou non mesuré.** Une absence de mesure n'est ni zéro dépense ni succès. Le symbole « — » indique une date non fixée. Toutes les tâches futures sont à autoriser : le code déjà présent n'est pas déclaré inexistant et les nouvelles pièces Bloc 3 ne clôturent pas les tâches techniques.

## 2. Kanban initial du reste à faire

| ID | Lot / tâche | Responsable proposé | Charge de base (j.h) | État au relevé | Réalisé (j.h) | Reste réestimé | Échéance initiale | Preuve de clôture attendue |
|---|---|---|---:|---|---|---|---|---|
| T01 | Périmètre et référence | Candidat | 1 | À autoriser | NR | À confirmer | S1 | Décision sur copie de travail et commit retenu. |
| T02 | Build et mesure initiale | Candidat | 1 | À autoriser | NR | À confirmer | S1 | Logs datés, commandes et environnement. |
| T03 | Plan de correction | Candidat | 0,5 | À autoriser | NR | À confirmer | S1 | Critères de sortie approuvés. |
| T04 | Protections et accès | Candidat | 2 | À autoriser | NR | À confirmer | S2 | Rapport TLS, accès et exposition. |
| T05 | Audits et blocage | Candidat | 2 | À autoriser | NR | À confirmer | S2 | Rapport qualifié et test de refus. |
| T06 | Sauvegarde et restauration | Candidat | 2 | À autoriser | NR | À confirmer | S3 | Restauration isolée vérifiée. |
| T07 | Retour arrière | Candidat | 2 | À autoriser | NR | À confirmer | S3 | Ancien commit effectivement restauré. |
| T08 | Configuration supervision | Candidat | 1 | À autoriser | NR | À confirmer | S4 | Revue des sondes et privilèges. |
| T09 | Alertes et reprise | Candidat | 2 | À autoriser | NR | À confirmer | S4 | Notification reçue et rétablissement. |
| T10 | Parcours et accessibilité | Candidat | 1,5 | À autoriser | NR | À confirmer | S5 | Recette et retests liés à la version. |
| T11 | Charge et coût IA | Candidat | 1,5 | À autoriser | NR | À confirmer | S5 | Mesures et contrôle du seuil convenu. |
| T12 | Recette et démonstration | Candidat | 1,5 | À autoriser | NR | À confirmer | S7 | Rapport et décision sur les réserves. |
| T13 | Pilotage et transfert | Candidat | 3 | À autoriser | NR | À confirmer | S7 | Comptes rendus et procédures remis. |
| **Total** | | | **21** | **13 tâches à autoriser** | **NR** | **NR** | | |

Le total comprend P01–P05 et le pilotage. Aucun résultat actuel de tests n'est inscrit à partir d'un fichier de log historique.

## 3. Indicateurs définis et premier relevé

Seuils ci-dessous proposés, à ratifier à J0. Le responsable de collecte est le candidat ; le commanditaire arbitre les écarts engageant budget, périmètre ou date.

| Indicateur | Calcul / unité | Valeur au 20/09 | Fréquence et source | Alerte / action |
|---|---|---|---|---|
| Tâches acceptées | Nombre de tâches clôturées avec preuve / 13 | **0/13** pour la nouvelle phase | Hebdomadaire, tableau ci-dessus | Ne mesure pas la complétude du jeu ; blocage > 2 jours ouvrés à escalader. |
| Avancement pondéré | Somme des charges initiales des tâches acceptées / 21 × 100 | **0 %** de clôture de cette phase | Hebdomadaire ; aucune fraction arbitraire pour « presque fini » | Comparer à la référence datée après J0. |
| Charge consommée | Somme des heures saisies / 7 | NR | Hebdomadaire, journal d'activité | Aucune déduction à partir des commits. |
| Prévision finale de charge | Réalisé + reste à faire réestimé | NR ; base indicative 21 j.h | Hebdomadaire | Au-delà de 21 j.h : examiner réserve ; au-delà de 25,2 : réautorisation. |
| Budget de base | 21 × 450 € HT | **9 450 € HT proposés** | À J0 puis à chaque décision | Pas une facture ni une dépense. |
| Réserve | 20 % du budget humain | **1 890 € HT proposés** | Hebdomadaire, décisions d'utilisation | Jamais absorbée sans justification. |
| Coût consommé valorisé | Heures enregistrées / 7 × TJM | NR | Hebdomadaire, temps saisi | Distinguer valorisation du temps et décaissement réel. |
| Frais engagés et payés | Sommes des commandes et factures, séparément | NR | Mensuel, justificatifs | Ne pas ajouter deux fois une facture déjà engagée. |
| Écart d'échéance | Date prévisionnelle actuelle − date approuvée, en jours ouvrés | NR : référence non approuvée | Hebdomadaire, planning | > 2 jours : exposer cause, options et nouvelle cible. |
| Charge / capacité | Travail planifié / jours disponibles | S1–S5 : 4/4 ; S6–S7 : 0,5/4 hors réserve | Hebdomadaire | > 100 % : déplacer ou déléguer, pas supposer des heures supplémentaires. |
| Risques prioritaires ouverts | Nombre de risques ouverts de score ≥ 6 | **6**, selon registre initial | Hebdomadaire | Prioriser mitigation et preuve, pas seulement changer le score. |
| Anomalies bloquantes | Nombre de défauts confirmés empêchant recette/ouverture | NR | À chaque recette, fiches d'anomalie | Un défaut bloquant non résolu empêche le GO. |
| Critères de recette satisfaits | Nombre satisfaits / nombre exécutés, plus couverture exécutés/prévus | NR | À chaque campagne | Ne pas confondre « non exécuté » avec « réussi ». |

**Budget du cycle de vie distinct :** la maintenance, les évolutions et les services représentent une provision de 21 015–52 410 € HT/an dans le [budget global](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md). Ce montant n'est pas une dépense constatée de cette phase et ne doit pas être ajouté au tableau hebdomadaire sans distinguer les périodes.

## 4. Registre initial des risques

Échelle proposée : probabilité P de 1 (faible) à 3 (forte), impact I de 1 (limité) à 3 (perte de données, sécurité ou livraison empêchée), score P × I. Ces cotations sont des **appréciations de cadrage**, pas des fréquences mesurées. Tous les risques sont ouverts au relevé ; le responsable de traitement proposé est le candidat.

| ID | Risque / élément observé | P | I | Score | Prévention / preuve de réduction | Échéance |
|---|---|---:|---:|---:|---|---|
| R01 | Reconstruction non reproductible ; fichier de build supprimé localement. | 3 | 3 | 9 | Clarifier les suppressions et reconstruire la référence retenue. | T01–T02 |
| R02 | Retour arrière vers le mauvais commit ; capture de version après mise à jour. | 3 | 3 | 9 | Corriger l'ordre et vérifier une restauration réelle. | T07 |
| R03 | Faux sentiment de sécurité ; audits non bloquants, TLS public non vérifié. | 2 | 3 | 6 | Qualifier audits et protection du parcours exposé. | T04–T05 |
| R04 | Sauvegarde non restaurable ou perte de progression. | 2 | 3 | 6 | Copie cohérente, contrôle d'intégrité et reprise isolée. | T06 |
| R05 | Alerte non reçue malgré configuration présente. | 2 | 2 | 4 | Incident simulé et réception prouvée. | T09 |
| R06 | Dépassement du budget IA ou incapacité sous charge. | 2 | 3 | 6 | Objectifs convenus, mesure et contrôle de dépense testé. | T11 |
| R07 | Indisponibilité de l'unique intervenant et absence de relais. | 2 | 2 | 4 | Procédures, limitation du travail en cours et replanification. | T13 |
| R08 | Validation client indisponible ou exigences modifiées tardivement. | 2 | 2 | 4 | Réserver les jalons et tracer les changements. | J0 puis jalons |
| R09 | Présentation de faits non démontrés au jury : équipe, satisfaction ou résultats actuels. | 2 | 3 | 6 | Distinguer preuves, propositions et simulations ; vérifier leur admissibilité. | Avant soutenance |

## 5. Journal de suivi et décisions

| Date | Nature | Fait ou décision documentée | Effet sur le projet | Suite |
|---|---|---|---|---|
| 19/08/2026 | Historique technique | Commit `4ec094c` : protection des marqueurs d'état et du flux narratif. | Correction ciblée de perte de progression ; effort historique non mesuré. | Voir [cas d'arbitrage](03_CAS_ARBITRAGE.md). |
| 19/08/2026 | Historique technique | Commit `68f0495` : persistance de la fiche de personnage. | Correction d'un autre défaut de sauvegarde ; pas de validation client déduite du commit. | Inclure la reprise dans la prochaine recette. |
| 20/09/2026 | Revue documentaire | Grille BC03 comparée aux pièces existantes ; manques en suivi, management, compétences et validation. | Constitution d'un dossier dédié, sans déclarer les critères acquis. | Revue par le candidat et collecte des preuves manquantes. |
| 20/09/2026 | Initialisation du suivi | Base de 21 j.h et réserve 4,2 j.h pour la phase future. | Budget proposé 11 340 € HT ; calendrier non approuvé. | Décision J0, aucun engagement client présumé. |

### Données à saisir à chaque réalisation

Pour chaque tâche : date, intervenant, heures, travail effectué, preuve, blocage, reste à faire et nouvelle échéance. Pour chaque dépense : fournisseur, objet, période, montant HT/TTC normalisé, état engagé/payé et justificatif. Pour chaque arbitrage : cause, options, décision, impact et approbation.

### Revue hebdomadaire proposée

1. Vérifier les preuves et déplacer uniquement les tâches réellement acceptées.
2. Mettre à jour réalisé, reste à faire, prévision finale et capacité disponible.
3. Examiner risques, anomalies et dépendances ; signaler les changements de scope.
4. Communiquer au commanditaire faits, écarts, options et décisions requises.
5. Conserver un relevé daté avec la référence précédente ; ne pas réécrire l'historique pour supprimer les dérives.

**Limite actuelle pour C3.2.1 :** l'outil et ses définitions sont en place, mais plusieurs relevés réels restent nécessaires pour démontrer un suivi régulier. Aucun coût réel ni retard historique n'a été inventé.