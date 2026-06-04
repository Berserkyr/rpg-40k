# Kanban projet — RPG 40K

Ce tableau sert de base de pilotage pour la soutenance. Il peut être repris dans GitHub Projects, Trello, Notion ou Jira.

## Colonnes

| Colonne | Règle d’entrée | Règle de sortie |
|---|---|---|
| Backlog | Besoin identifié | Priorisé et décrit |
| À faire | Tâche prioritaire | Développement commencé |
| En cours | Branche ou commit en cours | Code terminé et testé localement |
| Revue / Tests | Pull request, tests ou recette | Validation obtenue |
| Terminé | Fonction livrée | Déployée ou documentée |

## Tableau initial

| ID | Tâche | Priorité | Statut | Critère d’acceptation |
|---|---|---:|---|---|
| KAN-001 | Mettre en place une BDD SQLite | Haute | Terminé | L’API initialise une base SQLite et expose le chemin dans `/api/health` |
| KAN-002 | Isoler les parties par utilisateur | Haute | Terminé | Deux valeurs `X-User-Id` chargent deux sessions distinctes |
| KAN-003 | Ajouter des tests API multi-utilisateur | Haute | Terminé | `pytest` valide la création utilisateur et l’isolation |
| KAN-004 | Mettre en place une pipeline CI | Haute | Terminé | GitHub Actions lance tests backend, build frontend et E2E |
| KAN-005 | Ajouter tests end-to-end Playwright | Haute | Terminé | Le test ouvre le navigateur, démarre le jeu, lance un dé et une rencontre |
| KAN-006 | Mettre en place branches Git | Moyenne | En cours | Branches `main` et `develop` disponibles sur GitHub |
| KAN-007 | Mettre en place tags Git | Moyenne | En cours | Un tag versionné `v1.0.0-rncp` existe |
| KAN-008 | Ajouter authentification réelle | Moyenne | Backlog | Connexion par compte sécurisé au lieu d’un simple identifiant HTTP |
| KAN-009 | Remplacer YAML par sauvegardes 100% BDD | Moyenne | Backlog | Les sauvegardes de partie sont persistées en tables relationnelles |
| KAN-010 | Déploiement public | Moyenne | Backlog | URL publique stable pour démonstration |

## Definition of Done

Une tâche est terminée si :

1. le code est versionné ;
2. les tests liés passent ;
3. la documentation est mise à jour ;
4. la pipeline GitHub Actions est verte ;
5. le comportement est vérifiable par recette manuelle ou automatisée.
