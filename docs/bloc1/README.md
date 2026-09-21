# Bloc 1 — Cadrage et décisions du projet complet

**Projet :** Survivant de Ruche — RPG 40K Survivor  
**Candidat :** REBIAI Nehjmehdine Karim  
**Révision :** 20 septembre 2026 ; dossier aligné avec la présentation du Bloc 3 le même jour.

## Positionnement commun

> Le produit existe déjà. Le Bloc 1 présente le besoin, les choix d’architecture, le périmètre et le budget du jeu complet. Le Bloc 3 présente l’organisation, la réalisation, le suivi et les arbitrages de ce même projet. Les résultats techniques locaux ne constituent ni une validation client ni une preuve de production.

Le candidat indique avoir réalisé le projet personnellement depuis son origine. Le Bloc 1 n'est donc pas le devis d'un jeu encore inexistant. Il formalise le cadrage et explique les choix du produit construit, puis distingue les améliorations possibles. Les dates de rédaction des pièces ne doivent pas être confondues avec les dates des décisions initiales.

Référence commune à lire d'abord : [état du projet](../ETAT_PROJET_REFERENCE.md), comprenant la version, les résultats techniques observés, les limites de production et les quatre périmètres budgétaires. Le dépôt observé est `e116b88`, version déclarée 1.3.0, **avec changements locaux**, et non une copie propre.

## Besoin, périmètre et choix matérialisés

Le besoin est un jeu de rôle narratif accessible dans un navigateur, dans lequel un joueur gère un personnage, agit, explore, combat, fait évoluer son équipement et retrouve sa progression. Les [huit parcours communs](../PARCOURS_FONCTIONNELS_REFERENCE.md) relient ce besoin aux fonctions développées et à la démonstration du Bloc 3.

Le candidat a réalisé le domaine Python, l'API FastAPI, l'interface React/Vite, la persistance SQLite/YAML et l'authentification JWT/bcrypt. L'intégration OpenAI et le repli local répondent au besoin narratif ; ils n'offrent pas une expérience identique. Les configurations Docker, CI/CD et supervision matérialisent la préparation de l'exploitation. Leur fonctionnement en production doit être vérifié séparément.

Les responsabilités de cadrage, développement, qualité et exploitation ont été regroupées sur le candidat. Un commanditaire distinct, un testeur participant ou une équipe ne sont pas ajoutés artificiellement pour la soutenance. Les rôles externes à solliciter pour une réception restent identifiés comme tels.

## Pièces du Bloc 1 et passage au Bloc 3

| Sujet | Pièce principale | Suite dans le même projet |
|---|---|---|
| Besoin et périmètre | [Parcours fonctionnels](../PARCOURS_FONCTIONNELS_REFERENCE.md) | [Démonstration du produit](../bloc3/07_DEMONSTRATION_RECETTE_CLIENT.md). |
| Veille technologique | [C1.3.1](C1_3_1_VEILLE_TECHNOLOGIQUE.md) | Évolutions de dépendances, risques et compétences à entretenir. |
| Choix d'architecture | [C1.3.2](C1_3_2_ETUDE_COMPARATIVE_ARCHITECTURES.md) | [Lots et dépendances](../bloc3/01_METHODOLOGIE_PLANNING_RESSOURCES.md). |
| Charge et économie du jeu complet | [Budget du cycle de vie](C1_4_CHARGE_BUDGET_CYCLE_VIE.md) | [Suivi global](../bloc3/02_TABLEAU_DE_BORD.md), sans temps historiques inventés. |
| Décisions et recommandations | [C1.6](C1_6_PRECONISATIONS_CLIENT.md) | [Arbitrage réel](../bloc3/03_CAS_ARBITRAGE.md) et [restitution](../bloc3/06_SUIVI_CLIENT_VALIDATIONS.md). |
| Présentation de ce cadrage | [Support oral Bloc 1](SUPPORT_PRESENTATION.md) | [Support oral Bloc 3](../bloc3/08_SUPPORT_PRESENTATION.md). |

Cet index ne constitue pas un audit exhaustif de tous les critères de la grille Bloc 1 : il organise les pièces disponibles et leur cohérence avec le Bloc 3.

## Budget à annoncer sans ambiguïté

- **Construction complète depuis zéro :** 100–168 j.h hors réserve, valorisation estimative de 54 000–90 720 € HT avec réserve. Pas un relevé du temps consommé par le candidat.
- **Stabilisation complémentaire de l'existant :** 15–27 j.h hors réserve, à réestimer selon les vérifications nécessaires ; ce n'est pas le planning principal du projet.
- **Centre de cette option de stabilisation :** 21 + 4,2 j.h de réserve = 11 340 € HT.
- **Maintenance, évolutions et services pendant douze mois après ouverture :** 21 015–52 410 € HT/an.

Les exclusions et hypothèses de TJM, réserve et consommation restent celles du document budgétaire. La construction déjà réalisée ne doit pas être facturée fictivement une seconde fois.

## Présent et historique

Le [cadrage du module](../module/DOCUMENT_CADRAGE.md) et les autres [archives](../module/README.md) permettent d'expliquer les étapes antérieures. Leurs anciens budgets, tests et statuts ne remplacent pas l'état de référence. Les supports courants ne dépendent pas des anciennes pièces RNCP ignorées par Git.