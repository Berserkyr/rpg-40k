# Bloc 3 — Support de présentation orale

**Révision :** 20 septembre 2026. **Format :** trame éditable, pas diaporama exporté.  
Durée et ordre à adapter aux consignes de l'organisme ; les dix minutes du conducteur de démonstration ne sont pas présentées comme la durée officielle de l'épreuve.

## 1. Projet, rôle et limites

**À afficher :** jeu web narratif, périmètre existant, projet individuel, version présentée.

**À dire :** « J'ai réuni les fonctions de développement, qualité, exploitation et pilotage. Je distingue ce que le dépôt démontre de ce qui doit encore être observé avec un interlocuteur. Je ne présente pas une équipe hypothétique comme une équipe encadrée. »

Preuve : [matrice du dossier](README.md). Identifier la contribution personnelle et les aides effectivement utilisées.

## 2. Méthode et planification — C3.1

**À afficher :** Kanban limité, tableau versionné, étude → mesure → conception → réalisation → restitution.

**À dire :** « Le Kanban permet de traiter les anomalies sans figer artificiellement les priorités. Le planning capacitaire donne des engagements discutables et visibles. Une tâche en cours maximum évite de disperser la capacité disponible. »

Preuve : [planning détaillé](01_METHODOLOGIE_PLANNING_RESSOURCES.md). Montrer les dépendances et les dates comme propositions, pas comme réalisations historiques.

## 3. Ressources et budget

**À afficher :** 21 j.h de base, 4,2 j.h de réserve, capacité 4 j/semaine ; budget central indicatif 11 340 € HT.

**À dire :** « Ce lot concerne la stabilisation, pas toute la construction du jeu. La maintenance et les futures évolutions ont un budget annuel séparé. Les aménagements, formations et disponibilités doivent être intégrés avant d'approuver le calendrier. »

Preuve : [budget du cycle de vie](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md). Ne pas additionner une reconstruction complète à la stabilisation de l'existant.

## 4. Tableau de bord — C3.2.1

**À afficher :** tâches, avancement pondéré, consommé/reste à faire, échéances, risques et charge/capacité.

**À dire :** « L'état initial comporte des données non mesurées. Je préfère afficher NR plutôt que zéro dépense ou une progression inventée. Après autorisation, chaque revue doit conserver le réalisé et l'écart à la référence. »

Preuve : [tableau de bord](02_TABLEAU_DE_BORD.md). S'il a été alimenté depuis, montrer les relevés datés ; sinon dire explicitement qu'il est initialisé mais pas encore éprouvé sur plusieurs périodes.

## 5. Cas d'arbitrage — C3.2.2

**À afficher :** progression perdue → prompt seul / parseur / protection du flux → choix combiné.

**À dire :** « Une consigne à l'IA ne garantit pas un format. Le correctif protège la donnée et la fin du flux, puis rend les rejets visibles. Le commit étaye le choix ; je n'en déduis pas un temps passé ou un accord client. »

Preuve : [cas ANO-2026-001 et logigramme](03_CAS_ARBITRAGE.md). Bien distinguer résultats historiques et nouveaux essais.

## 6. Missions et posture — C3.3.1

**À afficher :** fonctions couvertes, RACI proposé, capacité, styles selon situation et partage des ressources.

**À dire :** « Le cumul des rôles facilite les décisions mais limite le contrôle indépendant. Je propose de séparer réalisation, vérification et acceptation. La méthode prévue doit être adaptée à la disponibilité, aux besoins d'accessibilité et à la compréhension de chaque participant. »

Preuve : [analyse critique et communication](04_MISSIONS_MANAGEMENT_COMMUNICATION.md). Ne pas affirmer une pratique collective non observée ; expliquer le contexte accepté par l'organisme.

## 7. Compétences et formation — C3.3.2

**À afficher :** preuves disponibles, niveaux à évaluer, cibles, plan F01–F06.

**À dire :** « Je pars des risques du projet : reprise, sécurité, alertes, qualité et décision. Les formations proposées ont un objectif vérifiable ; leur suivi n'est pas présumé. Les aménagements portent sur les modalités, pas sur une baisse arbitraire de l'exigence. »

Preuve : [grille et plan de formation](05_COMPETENCES_FORMATION.md). Remplacer les niveaux NE uniquement après évaluation réelle.

## 8. Relation client — C3.4.1

**À afficher :** CR-00, jalons J0–J4, décisions attendues, questionnaire et formules.

**À dire :** « Le compte rendu présente les améliorations, les limites et la décision demandée. Le document préparé aujourd'hui n'est pas une réunion tenue. Les retours et validations doivent être recueillis et reliés aux actions. »

Preuve : [suivi client](06_SUIVI_CLIENT_VALIDATIONS.md). Si une séance a été tenue depuis, présenter son compte rendu réel avec les informations sensibles masquées.

## 9. Démonstration — C3.4.2

Basculer vers le [conducteur client](07_DEMONSTRATION_RECETTE_CLIENT.md) : accès, narration, actions, exploration, sauvegarde puis combat. Montrer la version exécutée et annoncer le mode local éventuel.

Ne pas improviser un redémarrage de production ni utiliser RESET pour garantir un état neuf. Montrer les limites de reprise et consigner un échec au lieu de le dissimuler.

## 10. Conclusion et décision

**À dire :** « Voici les critères observés, les réserves et les actions proposées. Quels points empêchent l'acceptation du périmètre présenté ? »

Renseigner la décision de la séance. L'acceptation de la démonstration et l'autorisation de production restent deux décisions distinctes. La maîtrise d'un critère est appréciée par le jury, pas déclarée acquise par ce support.