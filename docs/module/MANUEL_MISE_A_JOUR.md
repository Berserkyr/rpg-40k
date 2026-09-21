# Manuel de mise à jour — Survivant de Ruche

> **Guide opérationnel non vérifié — qualification documentaire le 20/09/2026.** Procédures à valider avant usage ; aucun déploiement, test, rollback ou contrôle du VPS n'a été exécuté dans cette intervention. Les workflows cités sont des configurations présentes, pas des preuves de runs réussis. Voir l'[état de référence](../ETAT_PROJET_REFERENCE.md) (création prévue par l'utilisateur) et le [suivi actuel](../bloc3/02_TABLEAU_DE_BORD.md). Des fichiers de déploiement sont supprimés dans la copie de travail : vérifier les prérequis sur la version retenue, sans présumer un dépôt complet.

**Public visé :** exploitant / mainteneur de l'application.
**Compétence RNCP :** C2.4.1 — Documentation technique d'exploitation (manuel de mise à jour).
**Application :** RPG 40K Survivor (« Survivant de Ruche »).
**Cible du déploiement historique déclaré :** VPS Docker Compose (projet `rpg40k`) — `http://89.116.111.166:8081/` ; état actuel non vérifié.

---

## 1. Objet

Décrire les procédures proposées pour **mettre à jour** l'application et préparer un **retour arrière (rollback)**. L'absence de perte de données et l'efficacité du rollback ne sont pas garanties : sauvegarde cohérente, restauration et compatibilité des versions restent à vérifier.

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

Le schéma décrit la **voie automatique configurée**, pas une exécution constatée. Dans [.github/workflows/deploy-vps.yml](../../.github/workflows/deploy-vps.yml), `workflow_run` attend la réussite de la CI sur `main`, mais **`workflow_dispatch` autorise le déclenchement manuel sans cette condition de réussite**. Une CI verte ne garantit pas l'absence de défaut, et les audits de dépendances sont non bloquants. Le workflow récupère la branche au moment du déploiement : vérifier que le commit réellement livré correspond au commit testé.

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
     5. le [script de test de fumée](../../scripts/smoke_test.sh) est appelé pour le contrôle post-déploiement.
5. Le workflow prévoit une tentative de retour arrière si ce test échoue, puis un job en erreur. **Limite de configuration :** la référence dite précédente est relevée après la récupération/mise à jour du code ; elle ne prouve donc pas le retour à la version antérieure réellement en service. Voir §6 et vérifier un point de retour indépendant avant usage.

L'automatisation suppose des secrets, permissions, fichiers et un serveur correctement configurés. Aucun run ni état de ces prérequis n'est attesté ici.

---

## 4. Mise à jour manuelle (contrôlée)

À utiliser pour déployer une branche précise, rejouer un déploiement ou intervenir
directement sur le serveur.

### 4.1 Depuis GitHub (déploiement manuel déclenché)

1. Onglet **Actions** → workflow **Deploy VPS** → **Run workflow**.
2. Renseigner la **branche** (par défaut `main`), l'adresse d'écoute et le port.
3. Lancer : la même séquence qu'en §3 s'exécute pour la branche choisie.

Le lancement manuel n'impose pas une CI verte dans la condition du job : contrôler explicitement le commit testé, les preuves et l'autorisation de déploiement avant déclenchement.

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

> Le rebuild est prévu pour réutiliser les volumes nommés, mais leur présence ne garantit ni une sauvegarde cohérente ni une restauration réussie. Vérifier les montages réels, les sauvegardes et la compatibilité des données avant mise à jour ; aucune conservation effective n'a été contrôlée ici.

---

## 6. Retour arrière (rollback)

Si une version déployée pose problème :

Les commandes ci-dessous sont un exemple non exécuté : identifier un tag/commit stable réellement disponible et une sauvegarde restaurable avant usage. L'existence du tag d'exemple n'est pas attestée.

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

Depuis GitHub, l'entrée de **Deploy VPS** attend une **branche**. La procédure utilise une récupération puis un pull de cette branche : un tag ou un SHA ne doit pas être présenté comme un rollback pris en charge et vérifié. Préparer une procédure de retour vers un commit validé et la tester sur copie isolée, sans supposer le retour automatique fiable (limite §3).

Le journal des versions ([CHANGELOG.md](../../CHANGELOG.md)) permet de choisir le point
de retour et de connaître les changements de chaque version.

---

## 7. Mise à jour des dépendances

| Périmètre | Fichier | Procédure |
|---|---|---|
| Backend Python | [requirements.txt](../../requirements.txt) | Mettre à jour la version, relancer `pytest`, pousser (CI + audit `pip-audit`). |
| Frontend Node | [frontend/package.json](../../frontend/package.json) | `npm install`, `npm run build`, `npm test`, pousser (audit `npm audit`). |

La configuration CI prévoit un job d'**audit de sécurité des dépendances** à chaque push et pull request. Ses commandes tolèrent les erreurs (`|| true`) : une CI verte ne démontre ni l'absence de vulnérabilité ni la réussite de l'audit. Aucun journal de run n'a été vérifié ici.

---

## 8. Vérifications post-déploiement

**Contrôles à exécuter, pas résultats acquis.** Renseigner version/commit, environnement, date réelle, observation, preuve vérifiée, réserves et décision d'acceptation. La recette liée est préparée, non exécutée dans cette intervention.

| Contrôle | Commande / action | Attendu |
|---|---|---|
| Santé API | `curl http://127.0.0.1:8081/api/health` | `200 OK` |
| Conteneurs actifs | `docker compose -p rpg40k ps` | `running` |
| Logs sans erreur | `docker compose -p rpg40k logs -f` | Pas d'exception au démarrage |
| Accès applicatif | Ouvrir `http://89.116.111.166:8081/` | Écran d'authentification affiché |
| Non-régression | [Recette préparée](../bloc3/07_DEMONSTRATION_RECETTE_CLIENT.md) | D01–D08 non exécutés ; résultats et réserves à consigner, contrôles de livraison distincts à prévoir |

---

## 9. Justification des choix techniques

| Choix | Raison |
|---|---|
| **Docker Compose** | Reconstruction et volumes séparés ; atomicité et continuité de service non démontrées. |
| **CI verte pour la voie automatique** | Filtre configuré ; voie manuelle distincte, commit livré et résultats à contrôler. |
| **Volumes Docker persistants** | Séparent données et code ; sauvegarde/restauration et conservation à vérifier. |
| **Healthcheck `/api/health`** | Indicateur partiel de santé, pas preuve de recette fonctionnelle complète. |
| **Tags Git / CHANGELOG** | Repères possibles ; existence, stabilité et capacité de retour à vérifier. |

---

## 10. Documents liés

- Déploiement initial : [docs/deploiement_vps.md](../deploiement_vps.md)
- Documentation technique : [docs/module/DOC_TECHNIQUE.md](DOC_TECHNIQUE.md)
- Journal des versions : [CHANGELOG.md](../../CHANGELOG.md)
- Recette préparée, non exécutée : [docs/bloc3/07_DEMONSTRATION_RECETTE_CLIENT.md](../bloc3/07_DEMONSTRATION_RECETTE_CLIENT.md)
