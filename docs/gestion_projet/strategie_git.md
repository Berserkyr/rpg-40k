# Stratégie Git — branches, pipeline et tags

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

Deux définitions de pipeline sont disponibles :

| Plateforme | Fichier | Rôle |
|---|---|---|
| GitHub Actions | [.github/workflows/ci.yml](../../.github/workflows/ci.yml) | CI utilisée par le dépôt GitHub actuel |
| GitHub Actions | [.github/workflows/deploy-vps.yml](../../.github/workflows/deploy-vps.yml) | CD manuel vers le VPS |
| GitLab CI | [.gitlab-ci.yml](../../.gitlab-ci.yml) | CI prête si le projet est importé sur GitLab |

Les pipelines vérifient :

1. tests backend `pytest` ;
2. tests unitaires frontend `npm test` ;
3. build frontend `npm run build` ;
4. tests end-to-end Playwright.

Ces pipelines servent de preuve de non-régression et de qualité continue.

## Déclenchement du déploiement VPS

Le workflow [deploy-vps.yml](../../.github/workflows/deploy-vps.yml) dispose de deux déclencheurs :

| Déclencheur | Condition | Usage |
|---|---|---|
| `workflow_run` (automatique) | La CI se termine **avec succès** sur `main` | Déploiement nominal : seul un code testé atteint la production |
| `workflow_dispatch` (manuel) | Lancement explicite depuis GitHub | Rollback, déploiement d’une branche spécifique, changement de port |

La production n’est donc jamais mise à jour par un simple push sur une branche de travail : la
porte d’entrée reste la fusion vers `main`, elle-même conditionnée à une CI verte. Le job utilise
`concurrency: deploy-vps` avec `cancel-in-progress: false`, ce qui sérialise les déploiements et
évite que deux mises en production ne se chevauchent.

## Gestion des dépendances

La surveillance des dépendances est décrite dans
[docs/bloc4/01_processus_maj_dependances.md](../bloc4/01_processus_maj_dependances.md) et outillée par :

- [.github/dependabot.yml](../../.github/dependabot.yml) — détection hebdomadaire sur les quatre
  écosystèmes (pip, npm, Docker, GitHub Actions) ;
- [scripts/check_updates.py](../../scripts/check_updates.py) — rapport de veille à la demande ou en CI ;
- les bornes hautes de [requirements.txt](../../requirements.txt), qui interdisent toute montée de
  version majeure non décidée explicitement.
