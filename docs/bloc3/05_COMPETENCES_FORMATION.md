# C3.3.2 — Évaluation des besoins et plan de développement des compétences

**Révision :** 20 septembre 2026.  
**Public identifié :** le candidat, intervenant polyvalent du projet individuel.  
**Statut :** bilan qualitatif des compétences mobilisées dans ma réalisation de bout en bout, puis besoins de consolidation. Aucune note, formation suivie ou certification non obtenue n'est inventée.

## 1. Méthode d'évaluation

Je pars des missions que j'ai réalisées sur le jeu complet plutôt que d'une liste de technologies à apprendre avant de commencer. Le produit existe ; mon expérience couvre conception, développement, intégration, correction, préparation de livraison et documentation. Je distingue :

1. **Les compétences déjà mises en pratique** : je les explique à partir de mes choix et de mes réalisations personnelles.
2. **Les preuves disponibles et leurs limites** : une correction et sa justification étayent l'expérience ; elles ne suffisent pas à prouver une exploitation continue, une réception ou tous les cas complexes.
3. **Les besoins de consolidation** : approfondir une compétence, obtenir une revue indépendante ou préparer un service plus exigeant, même après réalisation du produit.

Pour un positionnement formel ultérieur seulement, échelle proposée : 0 = non acquis ; 1 = explique les principes ; 2 = réalise avec aide ; 3 = réalise et vérifie en autonomie ; 4 = transmet et traite un cas complexe. **NE = niveau chiffré non évalué**, différent de zéro et différent d'une absence d'expérience. Je ne remplace pas le bilan qualitatif par une série de notes inventées.

Procédure : auto-positionnement argumenté, exercice sur environnement isolé, lecture de la preuve et questions de justification. Consigner évaluateur, date, conditions, aides utilisées et aménagements. Une auto-évaluation reste signalée comme telle ; une revue par un tuteur ou pair doit être réellement organisée. Les niveaux cibles ci-dessous sont des exigences proposées, pas un diagnostic individuel.

## 2. Compétences actuelles, preuves et approfondissements

| Compétence / lots | Expérience que je peux expliquer aujourd'hui | Preuve ou repère | Limite et besoin de consolidation | Cible formelle proposée |
| --- | --- | --- | --- | --- |
| Conception et UX / L01–L02 | J'ai relié besoin de jeu, architecture, données et parcours. | [Cadrage](../module/DOCUMENT_CADRAGE.md), [maquettes](../module/WIREFRAMES.md), pièces historiques. | Confronter les choix à des observations utilisateur et à une réception externe. | 3 |
| Métier, API et narration / L03, L04, L06 | J'ai construit les règles et flux, puis protégé la progression face aux données narratives invalides. | Multiutilisateur `def2fec`, gameplay de juillet, [arbitrage `4ec094c`](03_CAS_ARBITRAGE.md). | Expliquer les limites du correctif et qualifier les cas d'erreur sur la version retenue. | 3 |
| React, intégration et 3D expérimentale / L05, L07 | J'ai réalisé l'interface, intégré les actions et développé le générateur/visualiseur expérimental. | Socle `64f51d1`, tests frontend `c1327d5`, générateur `d419b7f` ; [manuel historique](../module/MANUEL_UTILISATION.md). | Approfondir états asynchrones et observation des parcours ; ne pas confondre prototype 3D et moteur commercial. | 3 |
| Stratégie de tests / L09 | J'ai intégré tests et traitement de non-régression à la réalisation. | E2E `def2fec`, [fiche d'anomalie historique](../bloc4/03_collecte_consignation_anomalies.md). | Résultats courants dans l'[état de référence](../ETAT_PROJET_REFERENCE.md) ; mieux relier couverture métier et critères de réception. | 3 |
| Persistance et reprise / L04, L10 | J'ai développé les sauvegardes et corrigé la persistance de la fiche personnage. | `68f0495`, [modèle de données historique](../module/MCD_MLD.md). | Distinguer sauvegarde fonctionnelle et restauration après incident ; approfondissement F02 si nécessaire. | 3 |
| Sécurité et livraison / L08, L10 | J'ai mis en place les accès JWT et les configurations de livraison. | `7da31cf`, `3c4a5c8`, `d7c1bd0`, [documentation technique historique](../module/DOC_TECHNIQUE.md). | Vérifier politiques bloquantes, secrets et exposition ; pas de contrôle actuel du VPS. F03 ciblé. | 3 |
| Supervision / L11 | J'ai instrumenté le projet et préparé l'observation applicative et infrastructure. | `2bab2f0`, `82a5aba`, [dispositif historique](../bloc4/02_systeme_supervision.md). | Configuration distincte d'une notification reçue et d'une exploitation durable ; F04 selon positionnement. | 3 |
| Accessibilité / L02, L08 | J'ai intégré des préoccupations de lisibilité et d'usage aux parcours. | [Manuel historique](../module/MANUEL_UTILISATION.md), [conducteur de démonstration](07_DEMONSTRATION_RECETTE_CLIENT.md). | Approfondir contrôle clavier et observation sans déclarer de conformité exhaustive ; F05. | 2, avec appui spécialisé selon périmètre |
| Estimation, risques et organisation / L12 | J'ai porté les arbitrages et formalisé le budget global, les dépendances et les risques. | [Planning](01_METHODOLOGIE_PLANNING_RESSOURCES.md), [tableau de bord](02_TABLEAU_DE_BORD.md). | Formalisation rétrospective, pas de timesheet ; renforcer la collecte régulière pour les prochains travaux, F01. | 3 |
| Communication et coordination / L12 | J'ai articulé plusieurs fonctions dans un projet individuel et préparé des supports explicables. | [Missions et analyse critique](04_MISSIONS_MANAGEMENT_COMMUNICATION.md), [CR rétrospectif](06_SUIVI_CLIENT_VALIDATIONS.md). | L'organisation personnelle ne démontre pas l'encadrement d'une équipe ; F06 peut préparer une collaboration réelle. | 2 en exercice, puis 3 à confirmer en pratique |

Mon bilan actuel est qualitatif et fondé sur la réalisation. Les niveaux chiffrés restent NE jusqu'à une évaluation identifiée ; cela ne remet pas le travail accompli au futur. Après observation, je consignerai date, preuve et niveau, puis l'écart à la cible. Je ne calcule aucun écart numérique sur NE. L'expérience acquise ne dispense pas des contrôles opérationnels ni d'une validation indépendante.

## 3. Plan de développement proposé

Ce plan accompagne une montée en compétence **après réalisation**, pas un préalable fictif à tout le développement. Les durées couvrent apprentissage et exercices, pas une seconde facturation de la réalisation ou des contrôles opérationnels de la WBS. Un positionnement peut dispenser d'un module ou révéler un besoin plus important.

| ID | Public / objectif observable | Formation et modalités proposées | Durée | Échéance relative | Évaluation de sortie |
| --- | --- | --- | ---: | --- | --- |
| F01 | Moi en fonction de pilotage : suivre un complément sans masquer les inconnues historiques. | Atelier Kanban, capacité, budget et risque à partir des douze lots ; étude du [guide Kanban](https://kanbanguides.org/). | 0,5 j | Avant le suivi d'un nouveau travail autorisé. | Exercice chiffré explicitement pédagogique : calcul juste et référence conservée, sans l'insérer comme temps réel du projet. |
| F02 | Moi en fonction backend/exploitation : prouver une restauration cohérente. | Lecture de la [sauvegarde SQLite](https://www.sqlite.org/backup.html), exercice sur données jetables et débrief avec pair si disponible. | 1 j | Avant qualification complémentaire de restauration, si besoin confirmé. | Restaurer des données connues, vérifier intégrité et contenu ; expliquer les limites de la copie à chaud. |
| F03 | Moi en fonction livraison : approfondir les contrôles bloquants. | Parcours ciblé [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), revue CI et exercice rôles/secrets sur environnement isolé. | 1 j | Avant engagement d'un durcissement complémentaire. | Qualifier un risque applicable, définir refus de livraison et exception bornée sans exposer de secret. |
| F04 | Moi en fonction exploitation : consolider le diagnostic d'incident. | Lecture [Docker Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/) et [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/), exercice panne/rétablissement isolé. | 1 j | Avant exercice complémentaire de notification, si besoin. | Expliquer healthcheck/restart et montrer une notification avec retour au nominal dans l'exercice. |
| F05 | Moi en fonction frontend/recette : approfondir l'observation accessible. | Atelier clavier, focus, lisibilité, effets réduits, à partir des [vérifications WAI](https://www.w3.org/WAI/test-evaluate/preliminary/). | 0,5 j | Avant observation utilisateur complémentaire. | Produire trois observations reproductibles avec impact et correction proposée ; pas de déclaration de conformité RGAA. |
| F06 | Moi en fonction coordination : préparer une collaboration. | Jeu de rôle optionnel avec tuteur/partenaire à solliciter : délégation, désaccord, restitution et retour critique. | 0,5 j | Avant une collaboration, selon modalités de l'organisme. | Consigne reformulée, capacité vérifiée, décision consignée ; seul cet exercice est une simulation, pas le projet réalisé. |
| **Total proposé** | | | **4,5 j / 31,5 h** | | |

Les liens sont des ressources d'apprentissage proposées, pas la preuve d'une inscription, d'une lecture complète ou d'une certification obtenue. Les intervenants pédagogiques ne sont pas réservés.

## 4. Charge, coût et intégration au planning

Si les six modules sont nécessaires, valorisation du temps à l'hypothèse de 450 € HT/j.h : **4,5 × 450 = 2 025 € HT**, hors frais de formation, accompagnement ou examen à deviser. Une réserve optionnelle de 20 % porterait cette enveloppe de travail à **2 430 € HT / 5,4 j.h**. Ce n'est pas le tarif commercial des ressources gratuites citées.

Cette capacité pédagogique n'est **pas ajoutée automatiquement** aux 100–168 j.h de référence du jeu complet ni à l'option de stabilisation de 15–27 j.h. Après positionnement : autoriser uniquement les modules utiles, préciser leur charge additionnelle éventuelle et éviter tout double compte. Le centre de stabilisation de 21 j.h reste un scénario non engagé, pas le planning de ma réalisation. La réussite d'un exercice ne remplace pas une qualification opérationnelle de restauration ou d'alerte. Je ne supprime pas des contrôles de sécurité pour faire entrer une formation dans une enveloppe.

## 5. Adaptations des modalités

Avant formation, recueillir les besoins fonctionnels volontairement exprimés : supports lisibles, documents structurés, sous-titres, accès clavier, rythme asynchrone, pauses ou temps supplémentaire. Préférer un environnement d'exercice accessible ; proposer une restitution écrite ou orale équivalente selon le besoin. Le critère évalué reste la compétence, non la vitesse quand elle n'est pas essentielle à la mission.

Aucun état de santé n'est enregistré dans cette grille. Limiter l'accès aux évaluations personnelles et conserver seulement les informations utiles. En contexte multilingue, proposer glossaire, consignes écrites et temps de reformulation ; ne pas confondre aisance linguistique et capacité technique.

## 6. Renfort, recrutement et suivi

Il n'existe pas de service RH identifié pour ce projet individuel. Si un besoin complémentaire dépasse mon niveau ou ma capacité, je proposerai un renfort explicite : compétence, mission, charge, période, accès, coût/devis et preuve attendue. Un audit de sécurité externe ou un besoin 24/7 ne devient pas couvert par une journée de formation.

Suivi à tenir pour chaque module retenu : positionnement initial, décision, date réelle, temps/coût, résultat, niveau observé et action suivante. **Au 20 septembre, les modules de ce plan ne sont pas déclarés suivis ou validés.** Les compétences mises en pratique dans le produit sont décrites ci-dessus ; leur évaluation formelle et ces éventuels approfondissements sont des étapes distinctes.
