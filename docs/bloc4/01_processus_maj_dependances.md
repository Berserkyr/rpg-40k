# 1. Processus de mise à jour des dépendances

> **Compétence C4.1.1** — Gérer les mises à jour des dépendances et des bibliothèques tiers,
> en surveillant régulièrement les nouvelles versions, en évaluant les impacts des mises à jour,
> et en les intégrant de manière sécurisée pour maintenir l'application à jour et sécurisée.

## Périmètre logiciel concerné

Le périmètre de gestion des dépendances du projet **RPG 40K — Survivant de Ruche** couvre quatre
ensembles distincts :

- **Backend Python** : bibliothèques déclarées dans `requirements.txt`, installées dans un
  environnement virtuel isolé (`.venv`), avec bornes hautes interdisant les montées majeures
  automatiques. Le socle applicatif repose sur **FastAPI** (API REST),
  **Uvicorn** (serveur ASGI), **sse-starlette** (streaming SSE), **PyJWT** et **bcrypt**
  (authentification et hachage), **PyYAML** (sauvegardes), **openai** (client du maître du jeu)
  et **pytest** (tests).
- **Frontend JavaScript** : paquets npm déclarés dans `frontend/package.json`, avec versions
  exactes figées dans `frontend/package-lock.json`. On distingue les dépendances d'exécution
  (**React 19**, **react-dom**, **Three.js** pour le moteur 3D voxel) des dépendances de
  développement (**Vite 8**, **Vitest**, **Playwright**, **Testing Library**, **TypeScript**).
- **Images d'infrastructure Docker** : images de base utilisées par les conteneurs de production,
  soit `python:3.13-slim` (backend, `Dockerfile.backend`), `node:22-alpine` (étape de build
  frontend) et `nginx:1.27-alpine` (service web et reverse proxy, `frontend/Dockerfile`).
  L'orchestration est décrite dans `docker-compose.yml`.
- **Chaîne CI/CD** : actions tierces employées dans les workflows GitHub Actions
  (`actions/checkout@v4`, `actions/setup-python@v5`, `actions/setup-node@v4`) au sein de
  `.github/workflows/ci.yml` et `.github/workflows/deploy-vps.yml`, ainsi que la définition
  GitLab CI de secours `.gitlab-ci.yml`.

Cette séparation est structurante : une régression sur une dépendance de développement (Vite,
Vitest) n'affecte que la chaîne de build, tandis qu'une régression sur une dépendance d'exécution
(FastAPI, React, Three.js) impacte directement le service rendu à l'utilisateur. Les deux
catégories ne sont donc pas traitées avec le même niveau d'exigence.

## Politique de versionnage et types de mises à jour

Le projet applique le **versionnage sémantique** `x.y.z`, matérialisé par des tags Git posés sur
la branche `main` et documenté dans `docs/gestion_projet/strategie_git.md` :

| Tag | Usage |
|---|---|
| `v0.x.y` | Prototype ou incrément technique |
| `v1.0.0-rncp` | Version de présentation RNCP |
| `v1.0.1` | Correctif après validation |

Les mises à jour transitent par le modèle de branches du projet : une branche `fix/*` ou
`feature/*` créée depuis `develop`, fusionnée vers `develop` par pull request, puis vers `main`
pour une version stable étiquetée.

**Typologie et mode d'exécution :**

| Type | Exemple concret | Mode | Justification |
|---|---|---|---|
| **Patch** (`x.y.Z`) | `bcrypt 5.0.0 → 5.0.1`, correctif CVE | **Automatique** | Rétro-compatible par définition ; la CI (82 tests backend + 30 tests frontend) suffit à valider la non-régression. |
| **Mineure** (`x.Y.z`) | `fastapi 0.141 → 0.142` | **Automatique sur `develop`, manuelle vers `main`** | Ajout de fonctionnalités sans rupture annoncée, mais l'écart entre l'intention de l'éditeur et la réalité justifie une validation humaine avant production. |
| **Majeure** (`X.y.z`) | `React 19 → 20`, `Vite 8 → 9`, `openai 3.x → 4.x` | **Manuelle** | Rupture d'API probable. Exige une branche dédiée, la lecture du guide de migration, et une passe de tests complète incluant les tests end-to-end Playwright. |
| **Image de base Docker** | `python:3.13-slim` (rebuild) | **Automatique** au rebuild | L'image est reconstruite à chaque déploiement, ce qui embarque les correctifs de sécurité système de la distribution. |

Le choix d'automatiser les correctifs et de garder la main sur les montées majeures est un
compromis assumé entre **réactivité de sécurité** et **stabilité du service**.

### Mise en application technique de la politique

Une politique de mise à jour qui n'est pas outillée reste une intention. Trois mécanismes la
rendent effective dans le dépôt :

**1. Bornage des versions dans `requirements.txt`.** Chaque dépendance est déclarée avec un
plancher et un plafond :

```
fastapi>=0.141.1,<1.0.0
openai>=3.3.0,<4.0.0
bcrypt>=5.0.0,<6.0.0
```

Le plancher correspond à la version validée par la suite de tests ; le plafond bloque la montée
majeure. Conséquence directe : une version mineure ou corrective est récupérée automatiquement,
alors qu'une montée majeure **impose de modifier ce fichier**, donc d'ouvrir une pull request et
de tracer la décision. La règle « majeure = manuelle » n'est plus une consigne écrite, elle est
appliquée par l'outil d'installation.

**2. Détection automatisée via `.github/dependabot.yml`.** Dependabot inspecte chaque lundi les
quatre écosystèmes du périmètre et ouvre les pull requests correspondantes. Les versions mineures
et correctives sont **regroupées** par écosystème afin de limiter le bruit, tandis que les montées
majeures arrivent en **pull request isolée**, ce qui force une revue individuelle.

**3. Rapport de veille via `scripts/check_updates.py`.** Le script interroge `pip list --outdated`
et `npm outdated`, compare les numéros de version majeure et classe chaque écart selon la
politique. Il est exécuté dans le job `security-audit` de la CI et peut être lancé à la demande :

```bash
python scripts/check_updates.py
```

Il retourne le code de sortie `1` lorsqu'au moins une montée majeure est en attente, ce qui permet
de le brancher sur une alerte sans bloquer les correctifs de routine.

### Incident ayant motivé le bornage

Le bornage n'est pas une précaution théorique : il corrige une dérive réellement constatée sur ce
projet. Le fichier `requirements.txt` ne déclarait initialement que des planchers (`openai>=1.51.0`,
`bcrypt>=4.2.0`, `rich>=13.8.1`, `pytest>=8.3.2`). Une installation propre effectuée le 19/08/2026
a résolu ces contraintes vers :

| Dépendance | Version déclarée (plancher) | Version réellement installée | Écart |
|---|---|---|---|
| `openai` | `>=1.51.0` | **3.3.0** | **2 versions majeures** |
| `rich` | `>=13.8.1` | **15.0.0** | 2 versions majeures |
| `bcrypt` | `>=4.2.0` | **5.0.0** | 1 version majeure |
| `pytest` | `>=8.3.2` | **9.1.1** | 1 version majeure |

Autrement dit, **chaque nouvelle installation et chaque exécution de la CI embarquaient des
montées majeures que personne n'avait décidées ni évaluées**, avec un risque de rupture d'API
silencieuse — le cas le plus sensible étant le client `openai`, dont dépend tout le moteur de
narration.

L'évaluation d'impact a consisté à vérifier que la surface d'API réellement appelée par le code
(`AsyncOpenAI`, `chat.completions.create` avec les paramètres `messages` et `stream`, utilisés en
`backend/api.py`) reste disponible en version 3.3.0. La vérification étant concluante et les
82 tests backend au vert, la version 3.3.0 a été **retenue comme nouveau plancher validé**, puis
plafonnée à `<4.0.0`. La dérive est ainsi convertie en décision explicite et documentée.

## Fréquence des mises à jour

| Activité | Fréquence | Outillage |
|---|---|---|
| **Audit de sécurité automatisé** | **À chaque push et chaque pull request** | Job `security-audit` de `.github/workflows/ci.yml` : `pip-audit -r requirements.txt` (backend) et `npm audit --audit-level=high` (frontend) |
| **Rapport de veille en CI** | **À chaque push et chaque pull request** | `python scripts/check_updates.py`, intégré au job `security-audit` |
| **Détection des nouvelles versions** | **Hebdomadaire (lundi 06 h 00, Europe/Paris)** | `.github/dependabot.yml` — pull requests automatiques sur les 4 écosystèmes du périmètre |
| **Lot de mises à jour mineures** | **Mensuel** | Pull requests groupées par Dependabot (`groups`), fusionnées après CI verte |
| **CVE de criticité élevée ou critique** | **Sous 48 h** | Traitement hors lot, branche `fix/` dédiée |
| **Montées de version majeures** | **Trimestrielle** | Pull request isolée (non groupée), après évaluation d'impact sur branche `feature/` |

L'audit de sécurité est intentionnellement configuré en **mode non bloquant** (suffixe `|| true`
dans le workflow). Ce choix est documenté dans la CI par le commentaire *« Non bloquant : informe
sans casser la CI sur une vulnérabilité tierce »*. Il évite qu'une CVE publiée dans une dépendance
transitive n'immobilise toute l'équipe, tout en garantissant que l'information remonte dans les
logs de chaque exécution. La contrepartie — le risque qu'une alerte passe inaperçue — est
compensée par la revue hebdomadaire d'obsolescence.

## Évaluation d'impact avant intégration

Avant toute intégration, trois questions sont tranchées :

1. **La dépendance est-elle embarquée en production ?** Une vulnérabilité dans Vite ou PostCSS
   n'affecte que le poste de développement et la CI, puisque ces outils ne figurent pas dans le
   bundle livré. La criticité réelle est donc inférieure à la criticité affichée par l'outil d'audit.
2. **Quelle est la surface d'appel dans le code ?** Une montée de FastAPI touche les 32 routes de
   `backend/api.py` ; une montée de Three.js ne touche que `frontend/src/engine3d/`. Le périmètre
   de test est calibré en conséquence.
3. **Le correctif est-il disponible sans rupture ?** Si `npm audit fix` résout la vulnérabilité
   sans passer en `--force`, la mise à jour reste dans la catégorie patch.

### Exemple d'application réelle

Lors de l'installation complète du projet, l'audit npm a remonté **4 vulnérabilités de sévérité
« high »** sur les paquets `vite`, `postcss`, `nanoid` et `undici`.

L'évaluation d'impact a établi que **ces quatre paquets sont des dépendances de développement** :
ils interviennent au moment du build et des tests, mais aucun n'est présent dans le bundle de
production servi par Nginx. Le vecteur d'attaque décrit par les avis de sécurité (traversée de
chemin PostCSS via `sourceMappingURL`, contournement de `server.fs.deny` de Vite sur Windows)
suppose un accès au serveur de développement, absent en production.

**Décision :** traitement en lot mensuel via `npm audit fix` — qui résout les quatre avis sans
montée majeure — plutôt qu'en correctif d'urgence sous 48 h. La justification est consignée dans
le ticket de suivi.

## Déroulé opérationnel (du ticket à la mise en production)

1. **Création du ticket** — Ouverture d'une carte dans le kanban du projet
   (`docs/gestion_projet/kanban.md`), qualifiée par périmètre (backend / frontend / infra / CI),
   type de montée (patch / mineure / majeure) et criticité. La carte suit le cycle
   *À faire → En cours → À vérifier → Terminé*.

2. **Branche et implémentation** — Création d'une branche `fix/maj-<dependance>` ou
   `feature/maj-<dependance>` depuis `develop`. La mise à jour porte sur le manifeste **et** sur le
   fichier de verrouillage (`package-lock.json`), afin que l'environnement soit reproductible à
   l'identique en CI et en production.

3. **Vérification locale** — Exécution de la suite complète avant tout push :

   ```bash
   .venv/Scripts/python.exe -m pytest        # 82 tests backend
   ```

   ```bash
   cd frontend && npm test && npm run build  # 30 tests frontend + build de production
   ```

4. **Intégration continue** — L'ouverture de la pull request vers `develop` déclenche
   `.github/workflows/ci.yml`, composé de cinq jobs : `backend-tests` (pytest sur Python 3.13),
   `frontend-build` (`npm ci` puis `npm run build`), `frontend-unit-tests` (Vitest),
   `security-audit` (pip-audit + npm audit) et `e2e-tests` (Playwright sur Chromium, exécuté
   uniquement si les trois premiers jobs réussissent). L'emploi de `npm ci` — et non `npm install` —
   garantit une installation strictement conforme au lockfile.

5. **Validation fonctionnelle** — Revue de la pull request, contrôle des logs d'audit, puis
   vérification manuelle des parcours critiques : authentification JWT, démarrage de partie,
   streaming SSE du maître du jeu, résolution d'un combat.

6. **Passage en production** — Fusion de `develop` vers `main` et pose du tag de version. Le
   workflow `deploy-vps.yml` se déclenche alors sur succès de la CI (`workflow_run`), reconstruit
   les images Docker et redéploie la stack via Docker Compose sur le VPS. Un déclenchement manuel
   (`workflow_dispatch`) reste disponible pour cibler une branche spécifique.

7. **Rollback** — En cas d'incident, retour au tag de version précédent (`git checkout <tag>`
   puis `docker compose up -d --build`), et réouverture du ticket en *En cours* avec le diagnostic
   joint. Le script `scripts/backup_vps.sh` assure au préalable la sauvegarde du volume de données
   SQLite, ce qui permet de restaurer l'état applicatif indépendamment du code.

## Éléments de preuve dans le dépôt

| Artefact | Rôle dans le processus |
|---|---|
| [`.github/dependabot.yml`](../../.github/dependabot.yml) | Surveillance hebdomadaire des 4 écosystèmes ; groupe les mineures, isole les majeures |
| [`requirements.txt`](../../requirements.txt) | Bornes hautes interdisant toute montée majeure automatique côté Python |
| [`frontend/package-lock.json`](../../frontend/package-lock.json) | Verrouillage des versions exactes côté frontend (installation reproductible via `npm ci`) |
| [`scripts/check_updates.py`](../../scripts/check_updates.py) | Rapport de veille classant les obsolescences par type de montée |
| [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) | Job `security-audit` : `pip-audit`, `npm audit`, rapport de veille |
| [`.github/workflows/deploy-vps.yml`](../../.github/workflows/deploy-vps.yml) | Mise en production conditionnée à une CI verte sur `main` |
| [`docs/gestion_projet/strategie_git.md`](../gestion_projet/strategie_git.md) | Modèle de branches et convention de tags encadrant les montées |

## Synthèse de couverture des critères

| Critère d'évaluation attendu | Traitement dans ce document | Preuve technique |
|---|---|---|
| **La fréquence des mises à jour** | Tableau *Fréquence des mises à jour* : audit et veille à chaque push, détection hebdomadaire, lot mensuel, CVE sous 48 h, majeures trimestrielles | `dependabot.yml` (`interval: weekly`), job `security-audit` |
| **Le périmètre logiciel concerné** | Section *Périmètre logiciel concerné* : backend Python, frontend npm, images Docker, chaîne CI/CD | 4 entrées `updates:` dans `dependabot.yml` |
| **Le type de mise à jour (automatique ou manuel)** | Tableau *Typologie et mode d'exécution* : patch automatique, mineure semi-automatique, majeure manuelle | Bornes `<N.0.0` de `requirements.txt`, `groups` de `dependabot.yml`, classification de `check_updates.py` |
