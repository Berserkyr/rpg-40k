# Kanban projet — RPG 40K

> **Archive historique — classement le 20/09/2026.** Période antérieure ; date exacte de la campagne non établie. Les lignes KAN conservent le suivi historique, avec rectification explicite de l'authentification ; elles ne constituent pas le backlog actuel ni une validation RNCP/client. Déploiement historique déclaré ; état du VPS non vérifié. Voir l'[état de référence](../ETAT_PROJET_REFERENCE.md) (création prévue par l'utilisateur) et le [suivi actuel](../bloc3/02_TABLEAU_DE_BORD.md). Le PDF ancien n'est pas régénéré et ne constitue pas une version actuelle.

Cet ancien tableau reste une trace de pilotage. Toute reprise dans GitHub Projects, Trello, Notion ou Jira doit repartir des preuves et réserves du suivi actuel, pas recopier les statuts « Terminé » comme validations acquises.

## Colonnes

| Colonne | Règle d’entrée | Règle de sortie |
|---|---|---|
| Backlog | Besoin identifié | Priorisé et décrit |
| À faire | Tâche prioritaire | Développement commencé |
| En cours | Branche ou commit en cours | Code terminé et testé localement |
| Revue / Tests | Pull request, tests ou recette à vérifier | Preuve vérifiée, résultat consigné, réserves examinées |
| Terminé | DoD ci-dessous satisfaite et acceptation explicite | Traçabilité conservée ; sinon rester en revue ou bloqué |

## Tableau initial — historique annoté

« Terminé » dans cette table est un statut historique déclaré, non revérifié. Les critères sont à confronter à la version évaluée. `X-User-Id` était l'ancien mécanisme d'identification déclarative : il est conservé ici comme contexte uniquement, pas comme critère courant. La présence d'un workflow CI/CD prouve une configuration, pas une exécution réussie.

| ID | Tâche | Priorité | Statut | Critère d’acceptation |
|---|---|---:|---|---|
| KAN-001 | Mettre en place une BDD SQLite | Haute | Terminé | L’API initialise une base SQLite et expose le chemin dans `/api/health` |
| KAN-002 | Isoler les parties par utilisateur | Haute | Terminé déclaré historiquement ; à vérifier | Deux comptes authentifiés par JWT accèdent chacun à leur partie et ne peuvent accéder à celle de l'autre ; preuve de contrôle à recueillir |
| KAN-003 | Ajouter des tests API multi-utilisateur | Haute | Terminé | `pytest` valide la création utilisateur et l’isolation |
| KAN-004 | Mettre en place une pipeline CI | Haute | Terminé | GitHub Actions lance tests backend, build frontend et E2E |
| KAN-005 | Ajouter tests end-to-end Playwright | Haute | Terminé | Le test ouvre le navigateur, démarre le jeu, lance un dé et une rencontre |
| KAN-006 | Mettre en place branches Git | Moyenne | En cours | Branches `main` et `develop` disponibles sur GitHub |
| KAN-007 | Mettre en place tags Git | Moyenne | En cours | Un tag versionné `v1.0.0-rncp` existe |
| KAN-008 | Ajouter authentification réelle | Moyenne | Réalisée : JWT + bcrypt ; ancien statut Backlog dépassé | Authentification et hachage implémentés ; contrôles de production (secret, HTTPS, expiration, refus d'accès et isolation) à vérifier |
| KAN-009 | Remplacer YAML par sauvegardes 100% BDD | Moyenne | Backlog | Les sauvegardes de partie sont persistées en tables relationnelles |
| KAN-010 | Préparer le déploiement VPS | Haute | Terminé | Docker Compose, reverse proxy, guide VPS et scripts de déploiement disponibles |
| KAN-011 | Ajouter HTTPS sur domaine | Moyenne | Backlog | Certificat TLS actif via Caddy, Traefik ou Certbot |

## Definition of Done — règle actuelle de clôture

Cette règle remplace les anciens critères trop larges ; elle ne revalide pas rétroactivement la table historique. Une tâche n'est terminée que si :

1. le livrable/code est versionné et le périmètre ainsi que la version/commit évalués sont identifiés ;
2. chaque critère dispose d'une **preuve vérifiée** (rapport, observation, journal ou run identifié), avec date réelle d'exécution, environnement et vérificateur ; la configuration seule ne suffit pas ;
3. le **résultat observé** est consigné : réussi, échoué, bloqué, non exécuté ou non applicable avec motif ; les tests, build et run CI pertinents sont reliés à la version concernée ;
4. chaque **réserve** est décrite avec impact, responsable et échéance ; aucune réserve bloquante ni contrôle requis non exécuté ne permet une clôture ;
5. la documentation est cohérente avec les preuves et les limites, et une **décision d'acceptation explicite** du responsable/client compétent est consignée, avec périmètre et éventuelles réserves non bloquantes acceptées. La validation RNCP relève du jury, pas de cette checklist.

Sans ces éléments, conserver la tâche en revue ou bloquée dans le [suivi actuel](../bloc3/02_TABLEAU_DE_BORD.md). La [recette préparée](../bloc3/07_DEMONSTRATION_RECETTE_CLIENT.md) fournit un cadre à renseigner, pas un résultat déjà acquis.
