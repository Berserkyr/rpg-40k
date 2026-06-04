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
| GitLab CI | [.gitlab-ci.yml](../../.gitlab-ci.yml) | CI prête si le projet est importé sur GitLab |

Les pipelines vérifient :

1. tests backend `pytest` ;
2. tests unitaires frontend `npm test` ;
3. build frontend `npm run build` ;
4. tests end-to-end Playwright.

Ces pipelines servent de preuve de non-régression et de qualité continue.
