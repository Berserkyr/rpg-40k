# C3.3.1 — Missions, posture managériale et communication

**Auteur :** REBIAI Nehjmehdine Karim  
**Révision :** 20 septembre 2026  
**Contexte :** projet individuel ; responsabilités techniques regroupées sur le candidat.  
**Portée :** bilan des fonctions que j'ai assurées sur le projet complet ; RACI d'équipe présenté uniquement comme modélisation pédagogique, pas comme équipe historique.

## 1. Ce qui a réellement été produit

J'ai réalisé le projet personnellement de bout en bout. Le [dossier historique de support](../bloc4/08_support_client.md) décrit aussi ce contexte individuel. J'ai donc changé de fonction au fil des besoins : concevoir, développer, vérifier, préparer la livraison, corriger et documenter. Ces fonctions ne correspondent pas à des salariés différents. Je peux expliquer l'expérience acquise à partir de mes réalisations, sans attribuer de notes fictives ni inventer des échanges d'équipe.

| Fonction couverte dans le projet | Travail observable | Preuve à présenter | Limite |
| --- | --- | --- | --- |
| Cadrage et conception | Besoin, architecture, modèle de données et parcours. | [Cadrage historique](../module/DOCUMENT_CADRAGE.md), [modèle de données](../module/MCD_MLD.md), [maquettes](../module/WIREFRAMES.md). | Formalisation documentaire et chronologie de conception à distinguer ; pas d'approbation client déduite. |
| Développement métier et backend | Règles, comptes, API, sauvegardes et correction du parsing. | [Domaine métier](../../src), [API](../../backend/api.py), commit `4ec094c`. | Expliquer sa contribution personnelle et les aides utilisées, pas seulement montrer le code. |
| Développement frontend | Interface de jeu, commandes, combat et accès au compte. | [Interface principale](../../frontend/src/App.jsx), [tests de parcours](../../frontend/e2e/game.spec.js). | Fonctionnement actuel à répéter avant démonstration. |
| Expérimentation 3D | Générateur/visualiseur dans le périmètre expérimental. | Commit `d419b7f`, [périmètre commun](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md). | Pas un moteur commercial complet ni une production artistique massive. |
| Qualité | Tests, scénarios et traitement d'anomalie. | [Anomalie historique](../bloc4/03_collecte_consignation_anomalies.md), [arbitrage](03_CAS_ARBITRAGE.md). | Résultats courants dans l'[état de référence](../ETAT_PROJET_REFERENCE.md), pas dans un total historique recopié. |
| Exploitation | Configurations de déploiement, métriques et alertes. | [CI](../../.github/workflows/ci.yml), [supervision](../../docker-compose.monitoring.yml). | Configuration présente ≠ réception réelle des alertes. |
| Pilotage et documentation | Comparaison technique, risques, estimation et procédures. | [C1.6](../bloc1/C1_6_PRECONISATIONS_CLIENT.md), [budget](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md). | Ne démontre pas un suivi multi-intervenants ou une validation du client. |

## 2. Affectation réelle et RACI pédagogique

Dans l'organisation réelle, j'ai porté la réalisation et les décisions techniques internes. L'acceptation externe n'est pas une décision que je peux m'attribuer. La matrice suivante **modélise pédagogiquement** une répartition avec des interlocuteurs complémentaires : elle n'établit ni leur présence passée ni leur disponibilité future.

Légende : **R** réalise ; **A** assume la décision finale ; **C** est consulté ; **I** est informé. Les colonnes externes sont des rôles à pourvoir si une collaboration est organisée. Le cumul R/A du candidat n'est pas une revue indépendante.

| Mission sur le périmètre complet | Moi-même | Commanditaire, rôle non pourvu dans cette matrice | Testeur, à solliciter | Expert externe, si nécessaire |
| --- | --- | --- | --- | --- |
| L01–L02 : besoin, conception et estimation | R pour les livrables | A pour l'approbation externe, non obtenue | C | C |
| L03–L07 : produit, intégration et expérimentation | R/A pour les choix techniques internes | I | C pour observations | C si blocage |
| L08–L11 : qualité, protections, livraison et supervision | R/A pour la mise en œuvre et le rapport | I | C pour observations utilisateur | C pour revue indépendante |
| L12 : suivi, documentation et transfert | R/A pour la production des supports | C | I | I |
| Acceptation, changement budgétaire et ouverture | R pour la recommandation | A | C | C si réserve technique |

Cette modélisation ne transforme pas mon projet réalisé en simulation. Un éventuel exercice pédagogique de management devra être identifié séparément. Le jury ne devient pas rétroactivement mon client. Je ferai confirmer les modalités d'évaluation de C3.3.1 dans ce contexte individuel, sans inventer une équipe encadrée.

### Charge affectée selon les fonctions, sans timesheet historique

J'affecte les lots du [planning global](01_METHODOLOGIE_PLANNING_RESSOURCES.md) à une fonction principale pour rendre la charge lisible. Les fourchettes sont une estimation de construction comparable depuis zéro, **pas une répartition de mes heures passées**. Un lot n'est compté qu'une fois ; il peut mobiliser plusieurs compétences.

| Fonction principale assumée par moi | Lots affectés | Charge de référence hors réserve | Temps historique |
| --- | --- | ---: | --- |
| Conception et UX | L01 + L02 | 11–18 j.h | NR |
| Métier, backend et narration | L03 + L04 + L06 | 36–60 j.h | NR |
| Interface et expérimentation 3D | L05 + L07 | 18–30 j.h | NR |
| Qualité, sécurité et accessibilité transversales | L08 + L09 | 16–28 j.h | NR |
| Livraison et supervision | L10 + L11 | 11–18 j.h | NR |
| Pilotage, documentation et transfert | L12 | 8–14 j.h | NR |
| **Total, une seule personne** | **L01–L12** | **100–168 j.h** | **NR : absence de timesheet** |

La capacité de 4 jours projet/semaine est une hypothèse de dimensionnement, pas mon rythme historique attesté. Il n'existe pas de partage entre membres à démontrer : mon enjeu est l'alternance des fonctions et la prévention de surcharge. Le Kanban léger et la limite d'une tâche active sont formalisés après coup pour améliorer le suivi, pas présentés comme un outil historique prouvé.

Si un testeur ou expert intervient : lui attribuer une mission bornée, confirmer sa disponibilité et son coût, convenir des accès nécessaires, puis retirer la part réellement transférée de la charge du candidat. Ne pas additionner une délégation à la charge initiale sans expliquer le travail de coordination. Le temps des réunions et des retests fait partie du travail.

## 3. Styles managériaux : choix et limites

Je tire de mon expérience individuelle des règles de décision et de communication. Les styles ci-dessous décrivent leur application possible avec des interlocuteurs ; je ne les présente pas comme des séances de management de salariés déjà tenues.

| Style | Usage adapté au projet | Technique concrète | Point de vigilance |
| --- | --- | --- | --- |
| Directif | Incident de sécurité ou risque de perte de données. | Fixer une priorité unique, des actions immédiates et un critère de retour au service. | Diriger la résolution sans attribuer une faute personnelle ; expliquer après l'urgence. |
| Persuasif | Faire accepter du temps de stabilisation plutôt qu'une nouvelle fonctionnalité. | Exposer le risque joueur, les alternatives et le coût évité ; demander un arbitrage. | Ne pas présenter une estimation comme une certitude pour obtenir l'accord. |
| Participatif | Prioriser le backlog et comprendre les difficultés d'usage avec un testeur/client. | Questions ouvertes, reformulation, restitution écrite, décision explicite. | Écouter sans promettre immédiatement toutes les demandes. |
| Délégatif | Confier un test borné à une personne dont la compétence a été vérifiée. | Donner objectif, données, critères, limite d'autonomie et point de retour. | Pas de délégation fictive ni de tâche critique confiée sans moyens. |

Principes : décrire les faits avant les jugements, reformuler le besoin, reconnaître une limite, permettre un désaccord et séparer la personne de l'anomalie. La qualité du management se vérifie dans les échanges et leur effet sur le travail, pas dans l'affichage de mots comme « bienveillance ».

## 4. Analyse critique d'une posture documentée

**Situation vécue à expliquer :** j'ai assuré à la fois le développement et la vérification de la progression. Le [cas du marqueur narratif invalide](03_CAS_ARBITRAGE.md), corrigé par `4ec094c` le 19 août, montre la nécessité de protéger la sauvegarde plutôt que de compter seulement sur une consigne à l'IA. La correction de fiche personnage `68f0495` illustre un autre besoin de consolidation. Je peux expliquer ces choix à partir de ma réalisation ; je ne reconstitue pas une réunion ni un temps de résolution non consignés.

**Analyse :** le regroupement des rôles permet d'aller vite, mais fait disparaître la contradiction entre réalisation, contrôle et décision. Une fonctionnalité peut paraître terminée au développeur alors que sa reprise après incident n'est pas démontrée. Les documents historiques ne permettent pas d'affirmer que cette difficulté a été discutée avec une équipe.

**Apprentissage et posture :** cette expérience m'a conduit à distinguer « fonctionnalité réalisée », « comportement vérifié » et « périmètre accepté ». Je rends les inconnues visibles et je demande une lecture indépendante sur les risques élevés. Les choix de budget et de réception doivent être soumis à l'interlocuteur compétent ; ils ne se confondent pas avec mes décisions techniques.

**Mesures réalistes :** une tâche active maximum, revue hebdomadaire, critères de sortie explicites et relevé des demandes utilisateur. Ces mesures figurent maintenant dans le [tableau de bord](02_TABLEAU_DE_BORD.md). Leur efficacité n'est pas encore mesurée : observer, après deux revues réelles, les tâches rouvertes, le temps de blocage et les décisions en attente.

**Limite de la démonstration :** il s'agit d'une analyse critique de l'organisation individuelle, pas du récit d'un conflit résolu ou d'une équipe mobilisée. Si la grille exige une situation d'encadrement observée, une expérience réelle complémentaire ou une mise en situation autorisée reste nécessaire.

## 5. Outils et communication

| Support | Situation constatée | Objectif / règle d'usage proposée |
| --- | --- | --- |
| Dépôt Git et Markdown | Fichiers et historique disponibles. | Partager le référentiel, rendre les changements consultables et conserver les décisions. Ne prouve pas que d'autres personnes ont lu les pièces. |
| Formulaires GitHub d'anomalie et de retour | [Modèles présents](../../.github/ISSUE_TEMPLATE). | Centraliser reproduction, impact et demande ; lier l'issue au correctif. Aucun échange réel n'est déduit d'un formulaire vide. |
| Comptes rendus courts | [Support client préparé](06_SUIVI_CLIENT_VALIDATIONS.md). | Présenter résultats, écarts, options, responsable et échéance ; diffusion à confirmer. |
| Courriel ou visioconférence accessible | Aucun canal d'équipe effectif établi ici. | Choisir avec l'interlocuteur au prochain point de réception ; compte rendu écrit après réunion, pas décision perdue dans un chat privé. |

Pour la suite, je propose un point bref en cas de blocage, un relevé hebdomadaire des travaux autorisés et une revue aux points de réception convenus. Ce rythme n'est pas une cadence passée attestée. En incident critique, contacter l'interlocuteur convenu, puis consigner. Les délais de réponse sont à négocier ; aucune astreinte 24/7 n'est implicite.

## 6. Handicap, profils et contexte multiculturel

Aucun diagnostic, handicap ou contexte international individuel n'est connu dans ce dossier. Les adaptations sont donc préparées, pas attribuées à une personne inventée :

- demander les besoins pratiques de communication, d'horaires et de poste, sans documenter une donnée médicale ;
- supports avec titres structurés, consignes écrites, textes lisibles, équivalents aux couleurs et possibilité de navigation clavier ;
- visioconférence avec sous-titres si souhaités, compte rendu asynchrone et pauses ; vérifier l'accessibilité réelle de l'outil choisi ;
- prévoir un temps supplémentaire et réviser la charge si nécessaire ; aucune baisse de notation du fait d'un aménagement ;
- en contexte multilingue, définir langue commune, glossaire métier, dates non ambiguës et fuseau horaire ; reformuler les décisions et vérifier leur compréhension ;
- partager seulement les accès utiles et éviter que les échanges contiennent mots de passe, clés API ou données de joueurs.

## 7. Pièces humaines restant à recueillir

Pour une collaboration complémentaire, je devrai faire confirmer les rôles et disponibilités, conserver l'affectation acceptée et recueillir les échanges effectivement tenus. Je peux dès maintenant présenter mon expérience de réalisation et ses limites ; elle n'atteste pas un encadrement collectif. Les adaptations demandées seront documentées sans données sensibles. Aucune signature, satisfaction ou conversation passée n'est inventée.
