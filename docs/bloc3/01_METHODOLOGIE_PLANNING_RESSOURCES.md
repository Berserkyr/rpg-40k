# C3.1 — Méthodologie, planning et ressources

**Projet :** Survivant de Ruche — RPG 40K Survivor  
**Auteur :** REBIAI Nehjmehdine Karim  
**Révision :** 20 septembre 2026  
**Statut :** organisation proposée pour la prochaine phase ; calendrier non approuvé.

## 1. Périmètre et point de départ

Le jeu existe déjà : règles Python, API FastAPI, interface React, comptes, sauvegardes, narration, tests, livraison et supervision configurées. Le dépôt examiné pointe sur `6119aab`, avec la version déclarée 1.3.0 et des modifications locales. Cela ne prouve ni la version du VPS ni sa disponibilité.

Je ne reconstruis pas un planning historique fictif à partir des commits. Le [budget du cycle de vie](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md) estime une réalisation complète depuis zéro à 100–168 jours-homme hors réserve. Le planning ci-dessous concerne **le reste à faire de stabilisation**, P01 à P05 et pilotage transverse de [C1.6](../bloc1/C1_6_PRECONISATIONS_CLIENT.md). Il ne promet pas de développer l'ensemble du jeu en sept semaines.

L'ancien planning de six semaines du [premier dossier](../rncp/03_bloc3_pilotage.md) reste une proposition historique, pas un relevé des travaux effectivement réalisés.

## 2. Choix de méthode et d'outils

Je retiens pour cette phase un **Kanban léger, limité en travail en cours**, associé à un planning capacitaire hebdomadaire. Les anomalies de persistance, de sécurité et de déploiement peuvent imposer de modifier l'ordre des travaux. Une méthode entièrement séquentielle rendrait ces adaptations difficiles ; un Scrum formel ajouterait des rôles et cérémonies disproportionnés pour un intervenant unique.

Le suivi de référence est le [tableau Markdown versionné](02_TABLEAU_DE_BORD.md), avec identifiants de tâches, critères de sortie, liens vers tests et décisions. Ce choix utilise l'environnement Git déjà présent, rend les différences lisibles et évite de dépendre d'un abonnement. Les formulaires d'issues existants peuvent accueillir les anomalies ; l'existence d'un GitHub Project alimenté n'est pas revendiquée.

Le tableau hebdomadaire ci-dessous joue le rôle de **Gantt simplifié** : il montre séquence, dépendances et charge sans prétendre mesurer une vitesse historique. Kanban pilote le flux quotidien ; ce planning donne les jalons et limites de capacité. Les deux sont compatibles : une nouvelle urgence provoque une mise à jour de prévision, pas une modification silencieuse de la référence approuvée.

Limites : le Markdown ne calcule pas automatiquement les écarts ni les dépendances. Une revue hebdomadaire est donc nécessaire. Avec plusieurs intervenants ou des tâches concurrentes, transférer le même référentiel vers un outil de tableau partagé, après choix explicite, plutôt que maintenir deux tableaux divergents.

### Règles de fonctionnement proposées

- États : à autoriser, prêt, en cours, bloqué, en validation, terminé.
- Au plus **une tâche de réalisation en cours** et une en validation pour l'intervenant unique.
- Une urgence de sécurité ou de perte de données peut interrompre la tâche active ; noter l'interruption et réestimer la date, sans multiplier les travaux parallèles.
- Une tâche est prête quand son périmètre, son responsable, ses accès et son critère de sortie sont définis.
- Une tâche n'est terminée qu'avec preuve accessible, résultat vérifié et réserve éventuelle documentée. Un commit seul n'est pas une acceptation.
- Point quotidien individuel de 10 minutes ; revue hebdomadaire de 30 minutes incluse dans le pilotage. Points commanditaire aux jalons, sous réserve de sa disponibilité.

## 3. Décomposition détaillée de la phase

**Base de discussion centrale : 21 j.h, à 7 h/j.h.** Elle reste dans la fourchette C1.6 de 15–27 j.h. Lissage des lots : P01 = 2,5 ; P02 = 4 ; P03 = 4 ; P04 = 3 ; P05 = 4,5 ; transverse = 3.

Toutes les tâches sont **à autoriser** au 20 septembre. Les livrables documentaires rédigés aujourd'hui ne valent pas exécution de ces tâches techniques.

| ID | Phase / lot | Travail et résultat attendu | j.h | Dépendances | Fenêtre indicative |
|---|---|---|---:|---|---|
| T01 | Étude / P01 | Clarifier le périmètre et les suppressions locales ; retenir une version de référence. | 1 | Accord de démarrage | S1 |
| T02 | Mesure / P01 | Reconstruction isolée et relevé initial des builds, tests et anomalies. | 1 | T01 | S1 |
| T03 | Conception / P01 | Plan de correction, critères de recette et scénarios d'échec priorisés. | 0,5 | T02 | S1 |
| T04 | Réalisation / P02 | Revue TLS, rôles, secrets et exposition ; mesures correctives ciblées. | 2 | T03 et autorisation de poursuite J1 | S1–S2 |
| T05 | Mesure et réalisation / P02 | Qualifier audits, convenir d'une politique bloquante, l'appliquer et la tester. | 2 | T04 | S2 |
| T06 | Réalisation et mesure / P03 | Sauvegarde cohérente et restauration isolée avec contrôle des données. | 2 | T03 | S2–S3 |
| T07 | Réalisation et mesure / P03 | Corriger la capture de version du rollback ; tester retour arrière et échec. | 2 | T05, T06 | S3 |
| T08 | Conception et réalisation / P04 | Examiner sondes, privilèges et seuils ; ajuster la configuration. | 1 | T03 | S4 |
| T09 | Mesure / P04 | Simuler une panne en isolation, vérifier notification et rétablissement. | 2 | T07, T08 | S4 |
| T10 | Mesure / P05 | Recette des parcours et accessibilité ciblée ; correction et retest. | 1,5 | T05, T07, T09 | S4–S5 |
| T11 | Mesure / P05 | Charge représentative et dépense IA ; vérifier le comportement au seuil convenu. | 1,5 | T10, objectifs approuvés | S5 |
| T12 | Restitution / P05 | Consolider la recette, traiter les dernières réserves, préparer et réaliser la démonstration. | 1,5 | T10, T11 | S5–S7 |
| T13 | Pilotage et restitution / transverse | Revues, décisions, coûts, procédures, transfert et compte rendu final. | 3 | Réparti sur la phase | S1–S7 |
| **Total** | | | **21** | | |

Responsable de réalisation proposé pour T01–T13 : **le candidat**, sous différentes fonctions. Les responsabilités de décision et de consultation sont distinguées dans la [matrice d'affectation](04_MISSIONS_MANAGEMENT_COMMUNICATION.md). Une ressource externe n'est ni réservée ni considérée comme gratuite.

## 4. Calendrier et contrôle de capacité

**Hypothèse : démarrage le lundi 28 septembre 2026, à confirmer ; 4 jours projet par semaine.** Le jour restant ne constitue pas une capacité automatiquement mobilisable. Une indisponibilité ou un besoin d'aménagement réduit la capacité et décale la prévision, sans être traité comme une défaillance personnelle.

| Semaine | Dates calendaires | Répartition du travail de base | Base (j.h) | Réserve disponible (j.h) |
|---|---|---|---:|---:|
| S1 | 28/09–02/10 | T01 1 ; T02 1 ; T03 0,5 ; T04 1 ; T13 0,5 | 4 | 0 |
| S2 | 05/10–09/10 | T04 1 ; T05 2 ; T06 0,5 ; T13 0,5 | 4 | 0 |
| S3 | 12/10–16/10 | T06 1,5 ; T07 2 ; T13 0,5 | 4 | 0 |
| S4 | 19/10–23/10 | T08 1 ; T09 2 ; T10 0,5 ; T13 0,5 | 4 | 0 |
| S5 | 26/10–30/10 | T10 1 ; T11 1,5 ; T12 1 ; T13 0,5 | 4 | 0 |
| S6 | 02/11–06/11 | T12 0,25 ; T13 0,25 | 0,5 | 3,5 |
| S7 | 09/11–13/11 | T12 0,25 pour la démonstration ; T13 0,25 pour décision et compte rendu ; ajuster selon jours non travaillés locaux. | 0,5 | 0,7 |
| **Total** | | | **21** | **4,2** |

La réserve de 20 % porte la capacité budgétée à **25,2 j.h**, soit 11 340 € HT à 450 €/jour. Ce n'est pas un délai garanti : attentes client, jours fériés et problèmes hors périmètre sont à intégrer à J0. Le 11 novembre ne doit pas être supposé travaillé. La réserve n'autorise pas des fonctionnalités supplémentaires sans arbitrage.

### Jalons proposés, pas rendez-vous déjà tenus

| Jalon | Cible indicative | Condition de passage |
|---|---|---|
| J0 — autorisation | Début S1, 28/09 | Périmètre, capacité, budget, interlocuteurs et objectifs approuvés. |
| J1 — baseline | S1, après T03 et avant T04 | Rapport T02 et plan T03, estimation actualisée et autorisation explicite de poursuivre ; sinon T04 et les lots suivants restent suspendus. |
| J2 — exploitation | Fin S4 | Résultats sécurité, restauration, rollback et notifications examinés. |
| J3 — recette | Fin S6, 06/11 | Scénarios et réserves qualifiés ; objectif révisé si la réserve est consommée. |
| J4 — démonstration et décision | S7, cible 12/11 | Version identifiée, parcours répété, décision tracée ; date négociable. |

## 5. Ressources nécessaires et vigilances

| Ressource | Besoin | Situation / limite |
|---|---|---|
| Intervenant polyvalent | Backend, frontend, qualité, exploitation et pilotage, 4 j/semaine. | Candidat identifié ; disponibilité à confirmer. Ne pas compter chaque rôle comme une personne distincte. |
| Commanditaire | Valider périmètre, budget, service attendu et réception. | Interlocuteur et créneaux non confirmés ; si simulation, l'indiquer. |
| Testeur représentatif | Observer les parcours et recueillir la satisfaction. | Participation à organiser ; contribution externe non incluse comme ressource acquise. |
| Poste et accès dépôt | Environnement reproductible, droits nécessaires. | Copie locale modifiée ; ne pas annuler les suppressions sans clarification. |
| Préproduction isolée | Restauration, panne et tests de charge sans impact utilisateur. | Disponibilité à vérifier avant T02 ; pas d'essais destructifs sur le VPS public. |
| Données et services | Comptes de test, données fictives, quota IA, stockage externe et canal d'alerte. | Coûts prévus dans le budget du cycle de vie ; frais avant ouverture à ajouter si nécessaires. |

Points de vigilance : perte de progression, sauvegarde incohérente, état en mémoire, rollback erroné, audits non bloquants, accès HTTPS non vérifié, dépenses IA, indisponibilité de l'unique intervenant et absence de validations. Ils sont suivis dans le [registre des risques](02_TABLEAU_DE_BORD.md).

Pour les besoins liés au handicap : demander les aménagements fonctionnels souhaités sans collecter de diagnostic médical ; fournir supports structurés, information autrement que par la couleur, navigation clavier, échanges écrits et pauses adaptées. Ajuster ensemble capacité et calendrier. Aucune situation individuelle de handicap n'est présumée. Le [plan de compétences](05_COMPETENCES_FORMATION.md) précise les modalités de formation accessibles.

## 6. Actualisation et portée du livrable

Après approbation, conserver une version de référence datée. À chaque revue : saisir le réalisé, le reste à faire, les blocages et la nouvelle date ; garder l'ancienne référence pour mesurer les écarts. Une migration majeure, une exigence 24/7 ou une nouvelle fonctionnalité sort de cette baseline et exige un chiffrage distinct.

Ce document fournit la méthode, le planning et les ressources **prévisionnels** demandés par C3.1. Le respect du planning et la coordination effective devront être établis par les prochains relevés, pas par la seule rédaction.