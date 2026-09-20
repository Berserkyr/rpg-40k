# Bloc 3 — Coordonner et piloter le projet

**Projet :** Survivant de Ruche — RPG 40K Survivor  
**Candidat :** REBIAI Nehjmehdine Karim  
**Dossier préparé le :** 20 septembre 2026  
**Référentiel utilisé :** grille d'évaluation « Expert en Développement Logiciel (RNCP 39583), BC03 », PDF d'une page fourni par le candidat et lu lors de la préparation.

## 1. Objet et statut du dossier

Ce dossier rassemble les livrables documentaires correspondant aux sept compétences de la grille. Il complète et remplace, pour la préparation courante, la synthèse ancienne [03_bloc3_pilotage](../rncp/03_bloc3_pilotage.md), sans transformer les propositions historiques en faits réalisés.

**Il ne signifie pas « Bloc 3 acquis ».** Le planning et le suivi concernent une phase future ; les compétences individuelles et les échanges client nécessitent encore des observations. La démonstration devant le jury doit être réalisée. Le projet est individuel : aucune équipe, signature, formation suivie ou validation client n'est inventée.

Référence examinée : `6119aab`, version déclarée 1.3.0, copie locale modifiée. Les résultats techniques historiques sont distingués d'une validation de la version actuelle. Aucune application, campagne de tests ou opération de production n'a été lancée pour rédiger ces pièces.

## 2. Matrice de correspondance avec la grille officielle

| Compétence et livrables demandés | Pièce produite | Critères traités | Ce qui reste à observer ou confirmer |
|---|---|---|---|
| **C3.1** — Méthodologie, planning détaillé, ressources nécessaires. | [01 — Méthodologie, planning et ressources](01_METHODOLOGIE_PLANNING_RESSOURCES.md) | Kanban justifié, outil compatible et argumenté, étude/mesure/conception/réalisation/restitution, tâches/dépendances/charge, affectations et handicap, vigilances. | Accord sur dates, disponibilité, rôles et ressources ; référence prévisionnelle non approuvée. |
| **C3.2.1** — Outil de suivi du projet. | [02 — Tableau de bord](02_TABLEAU_DE_BORD.md) | Flux de tâches ; indicateurs quantifiables avancement/coûts/délais/risques/RH ; méthode, sources, seuils et premier relevé. | Plusieurs relevés réels, temps, dépenses et écarts. NR n'est pas zéro. |
| **C3.2.2** — Cas d'arbitrage rencontré. | [03 — Arbitrage ANO-2026-001](03_CAS_ARBITRAGE.md) | Problème et conséquences, options, décision argumentée, logigramme reconstitué et référence Git. | Effort/délai historiques non mesurés ; pas de réunion ni accord client retrouvés. |
| **C3.3.1** — Affectation des missions, styles managériaux, outils de communication et objectifs. | [04 — Missions et management](04_MISSIONS_MANAGEMENT_COMMUNICATION.md) | Fonctions effectivement couvertes, RACI proposé, capacité, styles, analyse critique, partage, aménagements et contexte multiculturel. | Pas d'équipe effectivement encadrée établie ; recevabilité du contexte individuel/simulation à vérifier auprès de l'organisme. |
| **C3.3.2** — Évaluation des compétences et plan de développement. | [05 — Compétences et formation](05_COMPETENCES_FORMATION.md) | Grille commentée fondée sur les preuves, niveaux cibles, protocole d'évaluation, six modules, modalités accessibles, durée/coût/contrôle et renfort. | Positionnement individuel à réaliser ; aucune note actuelle arbitraire ni formation déclarée suivie. |
| **C3.4.1** — Comptes rendus, points de validation, indicateurs de satisfaction. | [06 — Suivi client et validations](06_SUIVI_CLIENT_VALIDATIONS.md) | CR de revue factuel, améliorations et décisions demandées, J0–J4, questionnaire, formules et exploitation des retours. | CR-00 n'est pas une réunion client ; échanges, validations réalisées et réponses à recueillir. |
| **C3.4.2** — Démonstration des fonctionnalités devant le jury. | [07 — Démonstration et recette](07_DEMONSTRATION_RECETTE_CLIENT.md) | Conducteur orienté client, user stories, précontrôles, huit scénarios, limites et demande de validation. | Répétition sur la dernière version, résultats actuels et démonstration devant le jury. |

Support complémentaire : [08 — Présentation orale](08_SUPPORT_PRESENTATION.md), séquence de présentation adaptable à la durée fixée par l'organisme.

## 3. Lecture des chiffres et des statuts

- **Fait vérifié** : référence Git ou contenu examiné ; ne prouve pas automatiquement le déploiement ou l'auteur individuel de chaque travail.
- **Résultat historique** : essai rapporté par une pièce antérieure, non réexécuté pour ce dossier.
- **Proposition** : calendrier, budget, seuil, rôle ou formation à discuter avant engagement.
- **Simulation** : uniquement si une séance est réellement organisée et identifiée comme telle, avec recevabilité confirmée.
- **NR / NE** : non renseigné / non évalué ; aucune valeur fictive n'est substituée.

La phase centrale prévoit **21 j.h + 4,2 j.h de réserve**, soit **11 340 € HT** sous hypothèse de 450 €/j.h. Les estimations basse/haute restent celles de [C1.6](../bloc1/C1_6_PRECONISATIONS_CLIENT.md) : 15–27 j.h hors réserve. Les formations optionnelles ont une charge distincte et peuvent modifier le calendrier.

Le [budget du jeu et de son cycle de vie](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md) traite séparément construction complète, stabilisation, maintenance, évolutions et services. Le planning du Bloc 3 ne réduit pas le jeu complet à sept semaines de réalisation.

## 4. Actions indispensables avant de déclarer le dossier prêt pour l'évaluation

| Action | Responsable / interlocuteur à mobiliser | Pourquoi la rédaction seule ne suffit pas |
|---|---|---|
| Confirmer les modalités BC03 pour le projet individuel. | Candidat et organisme de formation. | Le management d'équipe ne peut être déduit de plusieurs rôles assumés seul. |
| Relire et approuver la baseline de phase. | Candidat et commanditaire réel ou interlocuteur de simulation identifié. | Les dates et montants ne sont pas un accord acquis. |
| Alimenter le tableau de bord pendant l'exécution. | Candidat. | Le suivi régulier exige des relevés réels, pas seulement des formules. |
| Effectuer le positionnement de compétences. | Candidat et évaluateur/tuteur à solliciter. | Le dépôt ne suffit pas à attribuer un niveau personnel. |
| Tenir un point de validation et recueillir des retours. | Interlocuteurs effectivement participants. | Une opinion et une signature ne s'inventent pas. |
| Répéter puis présenter le logiciel courant. | Candidat. | Un scénario écrit ne prouve pas l'utilisabilité de la version ni la prestation devant le jury. |

## 5. Principales preuves de référence

- [Préconisations C1.6](../bloc1/C1_6_PRECONISATIONS_CLIENT.md) et [budget du cycle de vie](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md).
- [Anomalie ANO-2026-001](../bloc4/03_collecte_consignation_anomalies.md), commit `4ec094c` du 19 août 2026.
- [User stories](../rncp/USER_STORIES.md), [recette historique](../rncp/05_plan_de_recette.md), [manuel utilisateur](../module/MANUEL_UTILISATION.md).
- [CI](../../.github/workflows/ci.yml), [déploiement](../../.github/workflows/deploy-vps.yml), [supervision optionnelle](../../docker-compose.monitoring.yml), [E2E](../../frontend/e2e/game.spec.js).

Les anciennes captures, exports PDF/Word et anciens tableaux ne sont pas régénérés par cette rédaction. Avant dépôt du dossier, sélectionner des versions cohérentes et signaler l'âge des preuves réutilisées.