# Manuel de mise à jour — Survivant de Ruche

**Public visé :** exploitant / mainteneur de l'application.
**Compétence RNCP :** C2.4.1 — Documentation technique d'exploitation (manuel de mise à jour).
**Application :** RPG 40K Survivor (« Survivant de Ruche »).
**Cible de production :** VPS Docker Compose (projet `rpg40k`) — `http://89.116.111.166:8081/`.

---

## 1. Objet

Décrire la procédure pour **mettre à jour** l'application en production sans perte de
données, ainsi que la procédure de **retour arrière (rollback)** en cas de régression.

Deux voies coexistent :

1. **Automatique** (recommandée) — pilotée par la CI/CD GitHub Actions.
2. **Manuelle** — via SSH sur le VPS, pour un déploiement contrôlé ou un rollback.

---

## 2. Principe de la mise à jour continue

Le déploiement suit une logique de **livraison continue** :

```
Développeur → push sur main
        │
        ▼
   CI (GitHub Actions) : tests backend + build frontend + audit dépendances
        │  (si vert)
        ▼
   Deploy VPS (workflow_run) : pull → build image → up -d → healthcheck
        │
        ▼
   Application à jour sur http://89.116.111.166:8081/
```

Le workflow de déploiement ne s'exécute que **si la CI est verte**
([.github/workflows/deploy-vps.yml](../../.github/workflows/deploy-vps.yml), condition
`workflow_run.conclusion == 'success'`), ce qui empêche de déployer une version cassée.

---

## 3. Mise à jour automatique (voie normale)

1. Fusionner/pusher les modifications validées sur la branche `main`.
2. La **CI** s'exécute automatiquement (tests + build + audit).
3. Si la CI est **verte**, le workflow **Deploy VPS** se déclenche seul.
4. Sur le VPS, le workflow exécute la séquence suivante :
   1. `git fetch` + `git pull --ff-only origin main` (récupération du code) ;
   2. mise à jour des variables `.env` (bind, port, base API) ;
   3. `docker compose -p rpg40k up -d --build` (reconstruction des images + redémarrage) ;
   4. `docker compose -p rpg40k ps` (vérification des conteneurs) ;
   5. `curl http://127.0.0.1:8081/api/health` (**vérification de santé** post-déploiement).
5. Si le healthcheck échoue, le job est marqué en erreur : voir §6 (rollback).

**Aucune action manuelle** n'est requise dans le cas nominal.

---

## 4. Mise à jour manuelle (contrôlée)

À utiliser pour déployer une branche précise, rejouer un déploiement ou intervenir
directement sur le serveur.

### 4.1 Depuis GitHub (déploiement manuel déclenché)

1. Onglet **Actions** → workflow **Deploy VPS** → **Run workflow**.
2. Renseigner la **branche** (par défaut `main`), l'adresse d'écoute et le port.
3. Lancer : la même séquence qu'en §3 s'exécute pour la branche choisie.

### 4.2 Directement en SSH sur le VPS

```bash
ssh <user>@89.116.111.166
cd /opt/rpg-40k

# 1. Récupérer la dernière version
git fetch origin main
git pull --ff-only origin main

# 2. Reconstruire et redémarrer les conteneurs
docker compose -p rpg40k up -d --build

# 3. Vérifier l'état et la santé
docker compose -p rpg40k ps
curl -fsS http://127.0.0.1:8081/api/health
```

Le script [scripts/deploy_vps.sh](../../scripts/deploy_vps.sh) automatise ces étapes.

---

## 5. Sauvegarde préalable (fortement recommandée)

Avant toute mise à jour sensible, sauvegarder les **volumes de données** :

```bash
cd /opt/rpg-40k
bash scripts/backup_vps.sh
```

Volumes concernés (persistants, non détruits par un rebuild) :

| Volume | Contenu |
|---|---|
| `rpg40k_data` | Base SQLite `rpg40k.sqlite3` (comptes, événements) |
| `rpg40k_saves` | Sauvegardes YAML des parties par utilisateur |

> Un `docker compose up -d --build` **ne supprime pas** ces volumes : les comptes et
> parties sont conservés entre deux versions.

---

## 6. Retour arrière (rollback)

Si une version déployée pose problème :

```bash
ssh <user>@89.116.111.166
cd /opt/rpg-40k

# 1. Identifier la dernière version stable (tag ou commit)
git log --oneline -10
git tag

# 2. Revenir à une version connue comme stable
git checkout v1.0.0-rncp        # ou un SHA de commit précis

# 3. Reconstruire à partir de cette version
docker compose -p rpg40k up -d --build

# 4. Vérifier la santé
curl -fsS http://127.0.0.1:8081/api/health
```

Depuis GitHub : relancer **Deploy VPS** en indiquant la **branche ou le tag** stable
dans *Run workflow*.

Le journal des versions ([CHANGELOG.md](../../CHANGELOG.md)) permet de choisir le point
de retour et de connaître les changements de chaque version.

---

## 7. Mise à jour des dépendances

| Périmètre | Fichier | Procédure |
|---|---|---|
| Backend Python | [requirements.txt](../../requirements.txt) | Mettre à jour la version, relancer `pytest`, pousser (CI + audit `pip-audit`). |
| Frontend Node | [frontend/package.json](../../frontend/package.json) | `npm install`, `npm run build`, `npm test`, pousser (audit `npm audit`). |

La CI exécute un job d'**audit de sécurité des dépendances** à chaque push, signalant
les vulnérabilités connues avant déploiement (OWASP A06).

---

## 8. Vérifications post-déploiement

| Contrôle | Commande / action | Attendu |
|---|---|---|
| Santé API | `curl http://127.0.0.1:8081/api/health` | `200 OK` |
| Conteneurs actifs | `docker compose -p rpg40k ps` | `running` |
| Logs sans erreur | `docker compose -p rpg40k logs -f` | Pas d'exception au démarrage |
| Accès applicatif | Ouvrir `http://89.116.111.166:8081/` | Écran d'authentification affiché |
| Non-régression | Parcours du [cahier de recettes](../rncp/05_plan_de_recette.md) | Cas principaux ✅ |

---

## 9. Justification des choix techniques

| Choix | Raison |
|---|---|
| **Docker Compose** | Reconstruction reproductible, isolation des volumes, redémarrage atomique. |
| **CI verte obligatoire avant déploiement** | Empêche la mise en production d'une version non testée. |
| **Volumes Docker persistants** | Découplent les données du code : mise à jour sans perte de comptes/parties. |
| **Healthcheck `/api/health`** | Détection immédiate d'un déploiement défaillant. |
| **Tags Git / CHANGELOG** | Points de retour arrière fiables et traçables. |

---

## 10. Documents liés

- Déploiement initial : [docs/deploiement_vps.md](../deploiement_vps.md)
- Documentation technique : [docs/module/DOC_TECHNIQUE.md](DOC_TECHNIQUE.md)
- Journal des versions : [CHANGELOG.md](../../CHANGELOG.md)
- Cahier de recettes : [docs/rncp/05_plan_de_recette.md](../rncp/05_plan_de_recette.md)
