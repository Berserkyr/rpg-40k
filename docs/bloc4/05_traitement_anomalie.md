# 5. Traitement d'une anomalie par le processus d'intégration et de déploiement continu

> **Compétence C4.2.2** — Créer et déployer un correctif en respectant le processus d'intégration
> et de déploiement continu afin de résoudre l'anomalie.

Ce chapitre décrit le traitement complet de l'anomalie **ANO-2026-001**, consignée au chapitre 4,
depuis l'ouverture de la branche de correction jusqu'à la validation en production.

## Chaîne d'intégration et de déploiement mobilisée

| Étape | Déclencheur | Outil | Contrôle exercé |
|---|---|---|---|
| 1. Branche de correction | Manuel | Git (`fix/*` depuis `develop`) | Isolation du correctif |
| 2. Vérification locale | Manuel | `pytest`, `npm test` | Boucle courte avant push |
| 3. Intégration continue | Push / pull request | GitHub Actions — 5 jobs | Non-régression backend, frontend, e2e, audit |
| 4. Revue | Pull request | GitHub | Relecture du correctif et des tests |
| 5. Fusion vers `main` | Manuel après CI verte | Git | Seul un code testé atteint `main` |
| 6. Déploiement | Automatique sur CI verte | `deploy-vps.yml` (`workflow_run`) | Reconstruction et redéploiement Docker |
| 7. Validation post-déploiement | Automatique | `scripts/smoke_test.sh` | 5 contrôles fonctionnels |
| 8. Retour arrière | Automatique si échec | `deploy-vps.yml` | Retour au commit précédent |

## Étape 1 — Branche de correction

Conformément à la stratégie Git du projet, une branche dédiée porte le correctif, nommée d'après
l'identifiant de l'anomalie afin que le lien fiche ↔ code reste explicite :

```bash
git checkout -b fix/ANO-2026-001-marqueurs-etat
```

## Étape 2 — Découpage du correctif en commits cohérents

Le correctif a été découpé de sorte que **chaque commit reste indépendamment testable**, condition
nécessaire pour qu'une bissection (`git bisect`) reste exploitable et pour qu'un retour arrière
partiel soit possible :

```
8da4dca  ci(deploy): valider le deploiement par test de fumee et rollback automatique
26df2a1  fix(narration): ne plus perdre la progression sur un marqueur d'etat invalide
b335510  feat(supervision): instrumenter l'application et outiller l'alerte
e9e52d5  chore(deps): borner les versions et automatiser la veille des dependances
```

L'ordre n'est pas arbitraire : le commit de supervision précède le correctif parce que celui-ci
**s'appuie sur les sondes** qu'il introduit (`state_markers_rejected`). Le commit de correction est
donc le premier à pouvoir rendre l'anomalie mesurable.

Le message de commit suit la convention *Conventional Commits* déjà employée dans le dépôt
(`fix:`, `feat:`, `chore:`, `ci:`) et référence explicitement l'anomalie :

```
fix(narration): ne plus perdre la progression sur un marqueur d'etat invalide
...
Fixes: ANO-2026-001
Refs: C4.2.1
```

Cette référence permet de relier automatiquement le commit à la fiche de consignation, et de
retrouver le contexte d'une modification des mois plus tard.

## Étape 3 — Le correctif mis en place

Le correctif combine deux niveaux, selon un principe de défense en profondeur.

**Niveau 1 — cause racine** (`src/state.py`). La conversion de la valeur d'une ressource est
protégée, alignant la branche `resources` sur la branche `tracks` qui interceptait déjà ce cas :

```python
try:
    if value.startswith(('+', '-')):
        self.update_resource(key, int(value))
        changes.append(f"{key} {value}")
    else:
        self.set_resource(key, int(value))
        changes.append(f"{key} = {value}")
except ValueError:
    self.rejected_updates.append(f"{key}={value}")
    _logger.warning(
        "Marqueur d'etat ignore : valeur non numerique pour "
        "la ressource '%s' (recu : %r)", key, value,
    )
```

**Niveau 2 — confinement** (`backend/api.py`). L'application de l'état ne peut plus interrompre la
clôture de la scène : quel que soit le défaut de parsing, l'événement `done` est émis et la partie
est sauvegardée.

```python
changes: list[str] = []
try:
    changes = session.character.apply_updates_from_text(full_text)
except Exception as exc:
    STATE_PARSE_FAILURES.labels(reason=type(exc).__name__).inc()
    log.exception("Echec d'application des marqueurs d'etat : %s", exc)
```

Le niveau 1 résout l'anomalie constatée ; le niveau 2 garantit que **la même famille de défaut ne
pourra plus produire une perte de données**, y compris pour des cas non encore identifiés.

## Étape 4 — Preuve de résolution par les tests

La validité du correctif est établie en exécutant la **même suite de tests** contre le code
antérieur puis contre le code corrigé :

```
# Sur le commit precedant le correctif (b335510)
16 failed, 2 passed in 4.01s

# Sur le commit du correctif (26df2a1)
18 passed in 2.80s
```

Ce double passage est la démonstration recherchée : les tests **échouent effectivement** sur le
code d'origine, ce qui prouve qu'ils décrivent bien l'anomalie et non un comportement quelconque.
Les deux tests qui passaient déjà sont ceux vérifiant le comportement nominal — le correctif ne
devait pas les modifier, et ne les a pas modifiés.

Comportement observé sur l'application en fonctionnement, avant et après :

| | Avant correctif | Après correctif |
|---|---|---|
| Statut HTTP | interruption (`ValueError`) | `200` |
| Événements `token` | 5 (narration reçue) | 6 |
| Événement `done` | **0** — client bloqué | **1** |
| `session.save()` | **non atteint** — scène perdue | atteint |
| Sonde marqueurs rejetés | inexistante | `1.0` |

## Étape 5 — Validation par l'intégration continue

La pull request déclenche les cinq jobs de `.github/workflows/ci.yml`. Exécution locale de la même
séquence sur la branche de correction :

```
--- job: backend-tests ---
120 passed in 6.12s

--- job: frontend-unit-tests ---
 Test Files  6 passed (6)
      Tests  30 passed (30)

--- job: frontend-build ---
✓ built in 297ms

--- job: security-audit (veille) ---
Total : 13 dependance(s) obsolete(s).
```

Le job `e2e-tests` ne s'exécute qu'après succès des trois premiers (`needs:`), ce qui évite de
mobiliser un navigateur Chromium sur une base déjà cassée.

## Étape 6 — Déploiement continu

La fusion vers `main` déclenche `deploy-vps.yml` par `workflow_run`, **conditionné au succès de la
CI**. Le déploiement se connecte au VPS en SSH, met à jour le dépôt et reconstruit la stack :

```bash
docker compose -p rpg40k up -d --build
```

## Étape 7 — Validation post-déploiement et retour arrière

L'ancien déploiement se terminait sur un simple `curl` de `/api/health`, c'est-à-dire la **sonde de
vivacité**. Or celle-ci répond `ok` dès que le processus démarre : une version inapte au trafic
— base injoignable, volume non monté — était déclarée déployée avec succès. Aucun retour arrière
n'était prévu.

Le processus a donc été renforcé dans le cadre de ce traitement :

```bash
# Version actuellement en service, conservee pour un retour arriere.
VERSION_PRECEDENTE="$(git -C "$APP_DIR" rev-parse HEAD)"

docker compose -p rpg40k up -d --build

if ! ./scripts/smoke_test.sh "http://127.0.0.1:$RPG40K_HTTP_PORT"; then
  echo "::error::Test de fumee en echec — retour a $VERSION_PRECEDENTE"
  git -C "$APP_DIR" checkout --force "$VERSION_PRECEDENTE"
  docker compose -p rpg40k up -d --build
  exit 1
fi
```

Le test de fumée exerce cinq contrôles, choisis pour distinguer un service *démarré* d'un service
*opérationnel* :

| # | Contrôle | Ce qu'il détecte |
|---|---|---|
| 1 | Disponibilité (30 tentatives) | Conteneur non démarré ou build échoué |
| 2 | **Sonde d'aptitude** `/api/health/ready` | Base injoignable, volume non monté, disque plein |
| 3 | Exposition de `/api/metrics` | Version déployée sans supervision — angle mort |
| 4 | `/api/state` sans jeton renvoie `401` | Régression de configuration exposant les routes de jeu |
| 5 | Livraison de l'interface | Panne du reverse proxy Nginx |

Exécution réelle du script contre une instance backend :

```
1. Attente de la disponibilite
  [OK]    service joignable apres 1 tentative(s)
2. Sonde d'aptitude (dependances)
  [OK]    toutes les dependances sont disponibles
3. Point de collecte des metriques
  [OK]    metriques exposees
4. Protection des routes de jeu
  [OK]    acces non authentifie refuse (401)
5. Livraison de l'interface
  [ECHEC] interface non servie par le reverse proxy
```

Le cinquième contrôle échoue ici volontairement : le script visait le backend seul (port 8000), qui
ne sert pas l'interface. En production, la cible est le port du reverse proxy, qui sert à la fois
l'interface et l'API. Ce relevé démontre que **le script détecte réellement une chaîne incomplète**
plutôt que de valider systématiquement.

**Garde-fou de sécurité ajouté au passage.** Le déploiement créait `.env` par copie de
`.env.example` lorsqu'il était absent, ce qui signait les jetons de production avec le
`JWT_SECRET=change-me-...` publié dans le dépôt. Le déploiement échoue désormais explicitement :

```bash
if grep -q '^JWT_SECRET=change-me' .env || ! grep -q '^JWT_SECRET=.\{16,\}' .env; then
  echo "ERREUR : JWT_SECRET absent ou laisse a sa valeur d'exemple dans $APP_DIR/.env"
  exit 1
fi
```

## Bilan du traitement

| Élément | Avant | Après |
|---|---|---|
| Anomalie ANO-2026-001 | Perte de progression, client bloqué | Résolue, vérifiée par 18 tests |
| Suite de tests backend | 102 | **120** |
| Validation post-déploiement | `curl` sur la sonde de vivacité | 5 contrôles fonctionnels |
| Retour arrière | Inexistant | Automatique sur échec du test de fumée |
| Secret de production | Valeur d'exemple possible | Déploiement refusé |
| Visibilité de l'anomalie résiduelle | Nulle | 2 sondes Prometheus |

## Éléments de preuve dans le dépôt

| Artefact | Rôle |
|---|---|
| Branche `fix/ANO-2026-001-marqueurs-etat` | Isolation du correctif, 4 commits cohérents |
| Commit `26df2a1` | Correctif référençant `Fixes: ANO-2026-001` |
| [`src/state.py`](../../src/state.py) | Correction de la cause racine |
| [`backend/api.py`](../../backend/api.py) | Confinement dans le générateur SSE |
| [`tests/test_state_markers.py`](../../tests/test_state_markers.py) | 18 tests, 16 en échec avant correctif |
| [`scripts/smoke_test.sh`](../../scripts/smoke_test.sh) | Validation post-déploiement |
| [`.github/workflows/deploy-vps.yml`](../../.github/workflows/deploy-vps.yml) | Déploiement, test de fumée, rollback |
| [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) | 5 jobs de validation |

## Synthèse de couverture des critères

| Critère d'évaluation attendu | Traitement dans ce document |
|---|---|
| **Le traitement de l'anomalie tire profit du processus d'intégration et de déploiement continu** | Chaîne en 8 étapes : branche dédiée, commits atomiques référençant l'anomalie, validation par les 5 jobs de CI, déploiement conditionné à une CI verte, test de fumée post-déploiement, rollback automatique |
| **Le correctif mis en place est décrit et permet la résolution de l'anomalie** | Section *Le correctif mis en place* (deux niveaux, code à l'appui) et *Preuve de résolution* : mêmes tests exécutés avant (16 échecs) et après (18 succès), relevé avant/après sur l'application en fonctionnement |
