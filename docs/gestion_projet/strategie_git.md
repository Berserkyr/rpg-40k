# Stratégie Git — branches, pipeline et tags

> **Guide de stratégie non vérifié en exécution — qualification le 20/09/2026.** Lecture des configurations locales uniquement : aucun run CI/CD, état distant des branches/tags ou contrôle du VPS n'est attesté. Les conventions ci-dessous sont des recommandations, pas la preuve qu'elles sont appliquées. Voir l'[état de référence](../ETAT_PROJET_REFERENCE.md) (création prévue par l'utilisateur) et le [suivi actuel](../bloc3/02_TABLEAU_DE_BORD.md). Le PDF ancien n'est pas régénéré et ne constitue pas une version actuelle.

## Branches

| Branche | Rôle | Règle |
|---|---|---|
| `main` | Version stable présentable | Reçoit uniquement du code testé |
| `develop` | Intégration des évolutions | Sert à préparer les prochaines fonctionnalités |
| `feature/*` | Développement ciblé | Une branche par fonctionnalité importante |
| `fix/*` | Correction d’anomalie | Une branche par bug significatif |

## Workflow recommandé

1. Créer une branche depuis `develop`.
2. Développer la fonctionnalité.
3. Lancer les tests localement.
4. Pousser la branche.
5. Ouvrir une pull request vers `develop`.
6. Fusionner `develop` vers `main` pour une version stable.
7. Poser un tag de version sur `main`.

## Convention de tags

| Tag | Usage |
|---|---|
| `v0.x.y` | Prototype ou incrément technique |
| `v1.0.0-rncp` | Version de présentation RNCP |
| `v1.0.1` | Correctif après validation |

## Pipelines CI

Deux workflows GitHub Actions sont présents et suivis dans le dépôt ; leur contenu est une **preuve de configuration, pas de run réussi** :

| Plateforme | Fichier | Rôle |
|---|---|---|
| GitHub Actions | [.github/workflows/ci.yml](../../.github/workflows/ci.yml) | CI configurée pour push et pull request ; exécution à vérifier |
| GitHub Actions | [.github/workflows/deploy-vps.yml](../../.github/workflows/deploy-vps.yml) | CD automatique après CI réussie sur `main` et déclenchement manuel ; exécution à vérifier |

L'ancienne configuration GitLab CI est supprimée dans la copie de travail et indisponible ; son lien cassé est retiré. Elle n'est pas présentée comme une solution prête. Le suivi décrit ici concerne GitHub Actions.

La configuration CI prévoit :

1. tests backend `pytest` ;
2. tests unitaires frontend `npm test` ;
3. build frontend `npm run build` ;
4. tests end-to-end Playwright.

Elle prévoit aussi des audits de dépendances et une veille d'obsolescence **non bloquants** (`|| true`). Une preuve de non-régression nécessite un run identifié, son commit, ses journaux et résultats effectivement vérifiés ; la configuration seule ou une CI verte ne prouve pas l'absence de vulnérabilité ni l'acceptation client.

## Déclenchement du déploiement VPS

Le workflow [deploy-vps.yml](../../.github/workflows/deploy-vps.yml) dispose de deux déclencheurs :

| Déclencheur | Condition | Usage |
|---|---|---|
| `workflow_run` (automatique) | La CI se termine **avec succès** sur `main` | Voie automatique configurée ; vérifier le commit effectivement récupéré et livré |
| `workflow_dispatch` (manuel) | Lancement explicite depuis GitHub, sans exigence de CI verte dans la condition du job | Déploiement d'une branche ou changement de port ; contrôle et autorisation préalables requis |

La voie automatique est filtrée sur `main`, mais la voie manuelle peut viser une autre branche et ne requiert pas une CI verte dans la condition du job. Les protections de branche et approbations distantes ne sont pas vérifiées. Le workflow récupère la branche au moment du déploiement, sans garantir ici l'identité avec le commit testé.

Le groupe `concurrency` vaut `deploy-vps`, avec `cancel-in-progress: false` : il prévoit la sérialisation de ces jobs, pas des interventions SSH externes. L'état actuel du VPS reste non vérifié ; le déploiement demeure une déclaration historique tant qu'une preuve actuelle n'est pas recueillie.

Le workflow prévoit un test de fumée et une tentative de rollback, mais relève la référence dite précédente après la mise à jour du code : le retour à la version réellement antérieure n'est pas garanti. L'entrée attend une branche ; le rollback par tag/SHA n'est pas présenté comme une capacité vérifiée. Voir les limites du [manuel de mise à jour](../module/MANUEL_MISE_A_JOUR.md).

## Gestion des dépendances

La surveillance des dépendances est décrite dans
[docs/bloc4/01_processus_maj_dependances.md](../bloc4/01_processus_maj_dependances.md) et outillée par :

- [.github/dependabot.yml](../../.github/dependabot.yml) — détection hebdomadaire sur les quatre
  écosystèmes (pip, npm, Docker, GitHub Actions) ;
- [scripts/check_updates.py](../../scripts/check_updates.py) — rapport de veille à la demande ou en CI ;
- les bornes hautes de [requirements.txt](../../requirements.txt), qui interdisent toute montée de
  version majeure non décidée explicitement.
