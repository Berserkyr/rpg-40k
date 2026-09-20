# C3.3.1 — Missions, posture managériale et communication

**Auteur :** REBIAI Nehjmehdine Karim  
**Révision :** 20 septembre 2026  
**Contexte :** projet individuel ; responsabilités techniques regroupées sur le candidat.  
**Portée :** analyse de l'organisation documentée et proposition pour la suite, pas preuve d'encadrement d'une équipe constituée.

## 1. Ce qui a réellement été produit

Le [dossier de support](../bloc4/08_support_client.md) décrit un projet développé seul. Les fonctions de pilotage, développement, qualité et exploitation ne correspondent donc pas à six salariés différents. Les artefacts suivants permettent de présenter les missions couvertes, mais pas de mesurer automatiquement l'autonomie du candidat ni de prouver des échanges humains.

| Fonction couverte dans le projet | Travail observable | Preuve à présenter | Limite |
|---|---|---|---|
| Développement métier et backend | Règles, comptes, API, sauvegardes et correction du parsing. | [Domaine métier](../../src), [API](../../backend/api.py), commit `4ec094c`. | Expliquer sa contribution personnelle et les aides utilisées, pas seulement montrer le code. |
| Développement frontend | Interface de jeu, commandes, combat et accès au compte. | [Interface principale](../../frontend/src/App.jsx), [tests de parcours](../../frontend/e2e/game.spec.js). | Fonctionnement actuel à répéter avant démonstration. |
| Qualité | Tests, scénarios et résultats archivés. | [Recette historique](../rncp/05_plan_de_recette.md), [tests](../../tests). | Pas une validation actuelle de tous les parcours. |
| Exploitation | Configurations de déploiement, métriques et alertes. | [CI](../../.github/workflows/ci.yml), [supervision](../../docker-compose.monitoring.yml). | Configuration présente ≠ réception réelle des alertes. |
| Pilotage et documentation | Comparaison technique, risques, estimation et procédures. | [C1.6](../bloc1/C1_6_PRECONISATIONS_CLIENT.md), [budget](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md). | Ne démontre pas un suivi multi-intervenants ou une validation du client. |

## 2. Répartition proposée pour la prochaine phase

Légende : **R** réalise ; **A** assume la décision finale ; **C** est consulté ; **I** est informé. Une fonction non pourvue n'est pas une ressource disponible. Un seul A doit être confirmé par ligne à J0 ; le cumul R/A du candidat sur les travaux internes n'est pas une revue indépendante.

| Mission | Candidat | Commanditaire, à identifier | Testeur, à solliciter | Expert externe, si nécessaire |
|---|---|---|---|---|
| Périmètre, budget et calendrier | R | A | C | I |
| T01–T03 : diagnostic et solution | R/A pour la production technique | C ; approbation du périmètre séparée | I | C si blocage |
| T04–T09 : sécurité, continuité et supervision | R/A pour la mise en œuvre | I | I | C si compétence manquante |
| T10–T12 : exécution de recette | R/A pour le rapport | C | C pour observations utilisateur | C si audit spécialisé |
| T13 : suivi et communication | R/A pour le relevé | C | I | I |
| Acceptation, changement budgétaire et ouverture | R pour la recommandation | A | C | C si réserve technique |

Dans une simulation, le rôle du commanditaire peut être joué par un interlocuteur désigné, mais le compte rendu doit porter la mention « simulation » et son contexte. Le jury ne devient pas rétroactivement le client du projet. Faire confirmer par l'organisme la recevabilité du contexte individuel pour C3.3.1 avant de revendiquer cette compétence.

### Charge et équilibre

Le [planning](01_METHODOLOGIE_PLANNING_RESSOURCES.md) prévoit 21 j.h de base pour une seule personne, soit P01 2,5 ; P02 4 ; P03 4 ; P04 3 ; P05 4,5 ; pilotage 3. Les cinq premières semaines restent à 4 j.h de capacité. Il n'existe pas de partage équilibré « entre membres » à démontrer actuellement : seule une prévention de surcharge individuelle est décrite.

Si un testeur ou expert intervient : lui attribuer une mission bornée, confirmer sa disponibilité et son coût, convenir des accès nécessaires, puis retirer la part réellement transférée de la charge du candidat. Ne pas additionner une délégation à la charge initiale sans expliquer le travail de coordination. Le temps des réunions et des retests fait partie du travail.

## 3. Styles managériaux : choix et limites

Ces styles sont **proposés selon les situations futures**. Aucun management de salariés n'est attesté par les sources.

| Style | Usage adapté au projet | Technique concrète | Point de vigilance |
|---|---|---|---|
| Directif | Incident de sécurité ou risque de perte de données. | Fixer une priorité unique, des actions immédiates et un critère de retour au service. | Diriger la résolution sans attribuer une faute personnelle ; expliquer après l'urgence. |
| Persuasif | Faire accepter du temps de stabilisation plutôt qu'une nouvelle fonctionnalité. | Exposer le risque joueur, les alternatives et le coût évité ; demander un arbitrage. | Ne pas présenter une estimation comme une certitude pour obtenir l'accord. |
| Participatif | Prioriser le backlog et comprendre les difficultés d'usage avec un testeur/client. | Questions ouvertes, reformulation, restitution écrite, décision explicite. | Écouter sans promettre immédiatement toutes les demandes. |
| Délégatif | Confier un test borné à une personne dont la compétence a été vérifiée. | Donner objectif, données, critères, limite d'autonomie et point de retour. | Pas de délégation fictive ni de tâche critique confiée sans moyens. |

Principes : décrire les faits avant les jugements, reformuler le besoin, reconnaître une limite, permettre un désaccord et séparer la personne de l'anomalie. La qualité du management se vérifie dans les échanges et leur effet sur le travail, pas dans l'affichage de mots comme « bienveillance ».

## 4. Analyse critique d'une posture documentée

**Situation observable :** le [premier document Bloc 3](../rncp/03_bloc3_pilotage.md) présentait une équipe hypothétique et des indicateurs « élevé » ou « moyen ». Le dépôt dispose d'une activité technique réelle, mais sans historique de charge ni retours client correspondants. Ce décalage rend le pilotage difficile à examiner et peut donner une image trop assurée de l'avancement.

**Analyse :** le regroupement des rôles permet d'aller vite, mais fait disparaître la contradiction entre réalisation, contrôle et décision. Une fonctionnalité peut paraître terminée au développeur alors que sa reprise après incident n'est pas démontrée. Les documents historiques ne permettent pas d'affirmer que cette difficulté a été discutée avec une équipe.

**Posture retenue pour la suite :** distinguer « réalisé », « vérifié » et « accepté » ; rendre visibles les inconnues ; soumettre les choix engageants au commanditaire ; solliciter une lecture indépendante sur les risques élevés. Cela remplace la déclaration « c'est prêt » par une demande de décision fondée sur des critères.

**Mesures réalistes :** une tâche active maximum, revue hebdomadaire, critères de sortie explicites et relevé des demandes utilisateur. Ces mesures figurent maintenant dans le [tableau de bord](02_TABLEAU_DE_BORD.md). Leur efficacité n'est pas encore mesurée : observer, après deux revues réelles, les tâches rouvertes, le temps de blocage et les décisions en attente.

**Limite de la démonstration :** il s'agit d'une analyse critique de l'organisation individuelle, pas du récit d'un conflit résolu ou d'une équipe mobilisée. Si la grille exige une situation d'encadrement observée, une expérience réelle complémentaire ou une mise en situation autorisée reste nécessaire.

## 5. Outils et communication

| Support | Situation constatée | Objectif / règle d'usage proposée |
|---|---|---|
| Dépôt Git et Markdown | Fichiers et historique disponibles. | Partager le référentiel, rendre les changements consultables et conserver les décisions. Ne prouve pas que d'autres personnes ont lu les pièces. |
| Formulaires GitHub d'anomalie et de retour | [Modèles présents](../../.github/ISSUE_TEMPLATE). | Centraliser reproduction, impact et demande ; lier l'issue au correctif. Aucun échange réel n'est déduit d'un formulaire vide. |
| Comptes rendus courts | [Support client préparé](06_SUIVI_CLIENT_VALIDATIONS.md). | Présenter résultats, écarts, options, responsable et échéance ; diffusion à confirmer. |
| Courriel ou visioconférence accessible | Aucun canal d'équipe effectif établi ici. | Choisir avec l'interlocuteur à J0 ; compte rendu écrit après réunion, pas décision perdue dans un chat privé. |

Rythme proposé : point bref en cas de blocage, relevé hebdomadaire, revue client aux jalons. En incident critique, contacter l'interlocuteur convenu, puis consigner. Les délais de réponse sont à négocier ; aucune astreinte 24/7 n'est implicite.

## 6. Handicap, profils et contexte multiculturel

Aucun diagnostic, handicap ou contexte international individuel n'est connu dans ce dossier. Les adaptations sont donc préparées, pas attribuées à une personne inventée :

- demander les besoins pratiques de communication, d'horaires et de poste, sans documenter une donnée médicale ;
- supports avec titres structurés, consignes écrites, textes lisibles, équivalents aux couleurs et possibilité de navigation clavier ;
- visioconférence avec sous-titres si souhaités, compte rendu asynchrone et pauses ; vérifier l'accessibilité réelle de l'outil choisi ;
- prévoir un temps supplémentaire et réviser la charge si nécessaire ; aucune baisse de notation du fait d'un aménagement ;
- en contexte multilingue, définir langue commune, glossaire métier, dates non ambiguës et fuseau horaire ; reformuler les décisions et vérifier leur compréhension ;
- partager seulement les accès utiles et éviter que les échanges contiennent mots de passe, clés API ou données de joueurs.

## 7. Pièces humaines restant à recueillir

Faire confirmer les rôles et disponibilités ; conserver une affectation réellement acceptée ; recueillir un exemple d'échange et son résultat ; documenter les adaptations effectivement demandées sans données sensibles. Une signature ou un dialogue ne peut pas être produit à la place d'une personne.