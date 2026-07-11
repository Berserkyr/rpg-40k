# Dossier Bloc 2 — Concevoir et développer des applications logicielles

**Certification :** Expert en Développement Logiciel — RNCP 39583  
**Bloc évalué :** Bloc 2 — Concevoir et développer des applications logicielles  
**Projet :** RPG 40K Survivor — application web de jeu narratif solo  
**Candidat :** À compléter  
**Date de rendu :** 24/07/2026  
**Version du livrable :** `v1.0.0-rncp`  
**Dépôt source :** `https://github.com/Berserkyr/rpg-40k`  
**Application déployée :** `http://89.116.111.166:8081/`

---

## Sommaire

1. Présentation du projet
2. Environnement de développement, test et déploiement — C2.1.1
3. Intégration continue et déploiement progressif — C2.1.2 / C2.2.4
4. Architecture logicielle et prototype — C2.2.1
5. Développement, évolutivité et choix techniques — C2.2.3
6. Sécurité applicative — C2.2.3
7. Accessibilité — C2.2.3
8. Harnais de tests unitaires et automatisés — C2.2.2
9. Cahier de recette — C2.3.1
10. Plan de correction des anomalies — C2.3.2
11. Documentation technique, exploitation et mise à jour — C2.4.1
12. Historique des versions et traçabilité
13. Conclusion
14. Annexes proposées

---

## 1. Présentation du projet

Le projet **RPG 40K Survivor** est une application web de jeu narratif solo inspirée d’un univers grimdark de science-fiction. L’utilisateur incarne **Karimus**, un technicien vox survivant dans une cité-ruche envahie. L’objectif du prototype est de proposer une expérience jouable dans un navigateur, avec une interface immersive, un backend d’orchestration, des mécaniques de jeu et une persistance des données.

Le projet a évolué d’un prototype CLI Python vers une application web complète composée de :

- un frontend **React / Vite** ;
- un backend **FastAPI** ;
- une base **SQLite** pour les utilisateurs ;
- des sauvegardes YAML isolées par utilisateur ;
- une pipeline CI/CD ;
- des tests backend, frontend et end-to-end ;
- un déploiement Docker sur VPS.

### Objectifs fonctionnels principaux

| Fonction | Description |
|---|---|
| Démarrer une partie | Initialiser une session de jeu pour un joueur |
| Narration MJ | Générer ou simuler une narration en streaming |
| Actions libres | Permettre au joueur de saisir une action textuelle |
| Jets de dés | Lancer un jet `2D6` |
| Inventaire | Fouiller une zone et ajouter du butin |
| Combat | Déclencher et résoudre un combat tour par tour |
| Carte | Se déplacer entre zones accessibles |
| Multi-utilisateur | Isoler les sessions par identifiant joueur |
| Sauvegarde | Persister l’état de partie |

### Correspondance avec le Bloc 2

| Compétence | Preuve principale dans le projet |
|---|---|
| C2.1.1 | [Protocole de déploiement continu + critères qualité/performance](PROTOCOLE_DEPLOIEMENT_CONTINU_QUALITE_PERF.md) |
| C2.1.2 | GitHub Actions, GitLab CI, tests automatisés |
| C2.2.1 | Architecture React / FastAPI / domaine métier / persistance |
| C2.2.2 | Tests `pytest`, Vitest, React Testing Library |
| C2.2.3 | Sécurité OWASP, accessibilité RGAA, évolutivité |
| C2.2.4 | Git, branches, tags, déploiement VPS |
| C2.3.1 | Cahier de recette fonctionnel et technique |
| C2.3.2 | Plan de correction des bugs et gestion des anomalies |
| C2.4.1 | Documentation technique, déploiement, exploitation, mise à jour |

---

## 2. Environnement de développement, test et déploiement — C2.1.1

Le livrable dédié est disponible ici : [PROTOCOLE_DEPLOIEMENT_CONTINU_QUALITE_PERF.md](PROTOCOLE_DEPLOIEMENT_CONTINU_QUALITE_PERF.md).

### Environnement de développement

| Élément | Choix |
|---|---|
| Éditeur | Visual Studio Code |
| OS de développement | Windows |
| Backend | Python 3.13, FastAPI, Uvicorn |
| Frontend | React, Vite, JavaScript JSX |
| Base de données | SQLite |
| Persistance de partie | YAML par utilisateur |
| Versioning | Git + GitHub |
| CI/CD | GitHub Actions + GitLab CI |
| Conteneurisation | Docker + Docker Compose |
| Déploiement | VPS Linux accessible sur port dédié |

L’environnement permet un développement local rapide et une validation automatisée. Le frontend et le backend sont séparés afin de limiter le couplage. Les dépendances backend sont déclarées dans `requirements.txt`, tandis que les dépendances frontend sont gérées par `package.json` et `package-lock.json`.

### Environnement local

L’application peut être lancée localement avec deux services :

| Service | Commande | URL |
|---|---|---|
| Backend | `python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000` | `http://127.0.0.1:8000` |
| Frontend | `npm run dev -- --host=127.0.0.1 --port=5173` | `http://localhost:5173` |

Un endpoint de supervision permet de vérifier l’état minimal du backend :

```text
GET /api/health
```

Il retourne le statut de l’API, la version et le chemin de la base SQLite côté conteneur.

### Environnement de déploiement

Le déploiement VPS utilise Docker Compose avec deux conteneurs :

| Conteneur | Rôle |
|---|---|
| `rpg40k-backend` | API FastAPI, logique métier, persistance |
| `rpg40k-frontend` | Nginx servant le build React et proxy `/api` |

L’application est exposée sur un port dédié pour ne pas entrer en conflit avec un autre site déjà présent sur le VPS :

```text
http://89.116.111.166:8081/
```

Les données sont persistées via volumes Docker dédiés :

| Volume | Contenu |
|---|---|
| `rpg40k_rpg40k_data` | base SQLite |
| `rpg40k_rpg40k_saves` | sauvegardes YAML |

---

## 3. Intégration continue et déploiement progressif — C2.1.2 / C2.2.4

### Gestion de sources

Le projet utilise Git avec une stratégie de branches simple :

| Branche / tag | Usage |
|---|---|
| `main` | version stable présentable |
| `develop` | branche d’intégration |
| `feature/*` | développement ciblé |
| `fix/*` | correction de bugs |
| `v1.0.0-rncp` | version de présentation RNCP |

Chaque évolution importante est historisée dans Git avec un message de commit explicite. Le tag `v1.0.0-rncp` permet d’identifier la version soumise à l’évaluation.

### Pipeline GitHub Actions

La pipeline GitHub Actions vérifie automatiquement :

1. les tests backend `pytest` ;
2. les tests unitaires frontend `npm test` ;
3. le build frontend `npm run build` ;
4. les tests end-to-end Playwright.

Ce cycle réduit les risques de régression à chaque modification de code.

### Pipeline GitLab CI

Une pipeline GitLab CI est également fournie pour démontrer la portabilité du processus d’intégration continue. Elle reprend les mêmes étapes : test, build, end-to-end, puis un déploiement automatique sur `main` (`when: on_success`) une fois les tests réussis.

### Déploiement continu automatique

Le déploiement VPS est **automatisé** : à chaque push sur `main`, la pipeline **CI**
s'exécute (tests backend, tests unitaires frontend, build, E2E). Lorsqu'elle réussit,
le workflow **Deploy VPS** se déclenche automatiquement (via `workflow_run`) et met à
jour la production sur le VPS, puis vérifie `/api/health`.

Ce fonctionnement satisfait le critère **C2.2.4** (« déployer le logiciel à chaque
modification de code et de façon progressive ») : chaque modification validée par la CI
est déployée sans intervention manuelle. Un push qui casse les tests **ne part pas** en
production (garde-fou de stabilité). Le déclenchement **manuel** reste disponible pour
les rollbacks ou le déploiement d'une branche spécifique.

Secrets nécessaires :

| Secret | Rôle |
|---|---|
| `VPS_HOST` | IP du VPS |
| `VPS_USER` | utilisateur SSH |
| `VPS_SSH_KEY` | clé privée SSH dédiée |
| `VPS_PORT` | port SSH |

Cette organisation répond à un besoin de déploiement progressif : la qualité est validée automatiquement, mais la mise en production reste déclenchée explicitement.

---

## 4. Architecture logicielle et prototype — C2.2.1

### Vue globale

```text
Navigateur
   |
   v
Frontend React / Vite
   |
   v
API FastAPI REST + SSE
   |
   +--> Domaine métier Python
   |       combat, inventaire, progression, monde, quêtes
   |
   +--> SQLite utilisateurs
   |
   +--> Sauvegardes YAML par utilisateur
```

### Découpage applicatif

| Couche | Rôle | Exemples de fichiers |
|---|---|---|
| Interface | Affichage et interactions joueur | `frontend/src/App.jsx`, composants React |
| Client API | Appels HTTP et SSE | `frontend/src/api.js` |
| API | Endpoints REST/SSE | `backend/api.py` |
| Base de données | Utilisateurs, événements | `backend/database.py` |
| Domaine | Règles de jeu | `src/combat.py`, `src/inventory.py`, `src/world.py` |
| Tests | Non-régression | `tests/`, `frontend/src/**/__tests__`, `frontend/e2e` |
| Déploiement | Production VPS | `docker-compose.yml`, `Dockerfile.backend`, `frontend/Dockerfile` |

Cette architecture permet la maintenabilité : le frontend ne manipule pas directement les fichiers de sauvegarde, les règles de jeu sont isolées dans `src/`, et l’API sert de façade stable.

### Prototype fonctionnel

Le prototype est manipulable en autonomie par un utilisateur. Il propose :

- un écran de démarrage ;
- un identifiant joueur pour le multi-utilisateur ;
- une narration en streaming ;
- des actions rapides ;
- une zone de saisie libre ;
- un panneau personnage ;
- un panneau carte ;
- un panneau inventaire ;
- un panneau combat.

---

## 5. Développement, évolutivité et choix techniques — C2.2.3

### Choix backend

FastAPI a été retenu pour :

- la création rapide d’API typées ;
- la compatibilité avec Pydantic ;
- la documentation automatique possible ;
- la simplicité d’intégration avec Uvicorn ;
- la gestion de flux SSE pour la narration.

Le backend expose des endpoints cohérents :

| Endpoint | Rôle |
|---|---|
| `GET /api/health` | supervision |
| `GET /api/state` | état complet de session |
| `POST /api/users` | création utilisateur |
| `POST /api/start` | démarrage partie |
| `POST /api/chat` | action libre |
| `POST /api/roll` | jet de dés |
| `POST /api/loot` | fouille |
| `POST /api/combat/start` | début combat |
| `POST /api/combat/action` | action de combat |
| `POST /api/travel` | déplacement |
| `POST /api/save` | sauvegarde |
| `POST /api/reset` | réinitialisation |

### Choix frontend

React a été retenu pour :

- sa structuration en composants ;
- sa capacité à gérer des états d’interface ;
- son écosystème de tests ;
- sa compatibilité avec Vite pour un développement rapide.

L’interface est conçue en composants spécialisés :

| Composant | Rôle |
|---|---|
| `Terminal` | affichage narratif |
| `InputBar` | saisie d’action libre |
| `ActionPanel` | actions rapides |
| `CharacterPanel` | état personnage |
| `CombatPanel` | actions et état de combat |
| `InventoryPanel` | inventaire |
| `MapPanel` | carte et déplacements |
| `QuestPanel` | quêtes |

### Multi-utilisateur

Le multi-utilisateur est mis en place par un identifiant joueur envoyé via l’en-tête HTTP `X-User-Id`. Chaque utilisateur dispose d’une session isolée et d’un répertoire de sauvegarde séparé.

La base SQLite stocke les utilisateurs dans une table `users`, tandis que les sauvegardes détaillées restent en YAML. Ce choix permet de démontrer une base de données structurée tout en conservant une persistance lisible et simple pour le prototype.

---

## 6. Sécurité applicative — C2.2.3

La sécurité est analysée selon les grandes catégories OWASP.

| Risque OWASP | Mesure mise en œuvre ou positionnement |
|---|---|
| Broken Access Control | sessions isolées par `X-User-Id`, authentification forte prévue en évolution |
| Cryptographic Failures | clé OpenAI lue depuis l’environnement, `.env` ignoré par Git |
| Injection | entrées backend typées par Pydantic, absence de SQL dynamique utilisateur |
| Insecure Design | séparation frontend/backend/domaine, documentation des limites |
| Security Misconfiguration | `.dockerignore`, `.gitignore`, variables d’environnement, port dédié VPS |
| Vulnerable Components | dépendances déclarées et installées en CI |
| Authentication Failures | pas de mot de passe dans le prototype, évolution prévue |
| Software/Data Integrity | pipeline CI, lockfile npm, tag de version |
| Logging/Monitoring | logs conteneurs, endpoint `/api/health` |
| SSRF | aucune URL utilisateur n’est appelée par le backend |

### Gestion des secrets

Les secrets ne sont pas versionnés. Les fichiers `.env` sont exclus par `.gitignore`. Les exemples de configuration sont fournis dans `.env.example` sans valeur sensible.

### Sécurité du déploiement

Le déploiement VPS utilise Docker Compose avec un nom de projet isolé `rpg40k`, des volumes dédiés et un port séparé `8081`. Cette stratégie évite d’impacter un autre service déjà présent sur le serveur.

---

## 7. Accessibilité — C2.2.3

Le référentiel retenu est le **RGAA**, adapté aux applications web en contexte français.

### Mesures déjà présentes

| Exigence | Mise en œuvre |
|---|---|
| Contraste | interface terminal sombre avec texte clair |
| Labels explicites | boutons et champs avec libellés fonctionnels |
| ARIA | `aria-label` sur les actions principales |
| Navigation simple | actions regroupées par panneaux |
| Feedback utilisateur | terminal affichant erreurs et résultats |

### Exemples de contrôles accessibles

- bouton de démarrage avec label explicite ;
- champ d’identifiant joueur avec label ;
- boutons `JET 2D6`, `FOUILLER`, `RENCONTRE`, `SAUVER`, `RESET` avec `aria-label` ;
- boutons de combat avec libellés compréhensibles ;
- champ d’action libre accessible.

### Limites et améliorations prévues

- réaliser un audit RGAA complet ;
- vérifier tous les contrastes avec outil spécialisé ;
- proposer une option sans scanlines/animations ;
- renforcer les messages d’erreur pour lecteurs d’écran.

---

## 8. Harnais de tests unitaires et automatisés — C2.2.2

Le projet comporte plusieurs niveaux de tests.

### Tests backend

Outil : `pytest`.

| Fichier | Couverture |
|---|---|
| `tests/test_dice.py` | jets de dés |
| `tests/test_entities.py` | génération d’entités |
| `tests/test_state.py` | état personnage |
| `tests/test_api.py` | endpoints API, healthcheck, multi-utilisateur |

Résultat validé : `17 passed`.

### Tests unitaires frontend

Outils : Vitest, jsdom, React Testing Library.

| Fichier | Couverture |
|---|---|
| `frontend/src/__tests__/api.test.js` | client API et en-tête utilisateur |
| `ActionPanel.test.jsx` | actions principales et désactivation en combat |
| `InputBar.test.jsx` | saisie et envoi d’action |
| `CombatPanel.test.jsx` | affichage et actions de combat |
| `CharacterPanel.test.jsx` | affichage personnage |

Résultat validé : `12 passed`.

### Tests end-to-end

Outil : Playwright.

Le test E2E vérifie un parcours utilisateur complet :

1. ouverture de l’application ;
2. saisie d’un identifiant joueur ;
3. initialisation de la partie ;
4. lancement d’un jet de dés ;
5. déclenchement d’une rencontre ;
6. apparition du panneau combat.

### Intégration dans la CI

Les tests backend, frontend et E2E sont exécutés dans la pipeline. Cela constitue un harnais de test permettant de prévenir les régressions avant livraison.

---

## 9. Cahier de recette — C2.3.1

### Objectif

La recette valide que les fonctionnalités principales sont utilisables et conformes aux attentes du prototype.

| ID | Fonction | Étapes | Résultat attendu |
|---|---|---|---|
| REC-001 | Accès application | ouvrir l’URL | écran d’accueil visible |
| REC-002 | Identifiant joueur | saisir un identifiant | session dédiée créée |
| REC-003 | Démarrage | cliquer initialisation | narration affichée |
| REC-004 | Action libre | saisir une action | réponse affichée |
| REC-005 | Jet de dés | cliquer `JET 2D6` | résultat `2D6` visible |
| REC-006 | Fouille | cliquer `FOUILLER` | butin ou message affiché |
| REC-007 | Rencontre | cliquer `RENCONTRE` | combat actif |
| REC-008 | Attaque | cliquer `ATTAQUER` | log combat et PV mis à jour |
| REC-009 | Défense | cliquer `DÉFENDRE` | action défensive affichée |
| REC-010 | Fuite | cliquer `FUIR` | tentative de fuite résolue |
| REC-011 | Déplacement | choisir une zone | zone actuelle modifiée |
| REC-012 | Sauvegarde | cliquer `SAUVER` | sauvegarde confirmée |
| REC-013 | Reset | cliquer `RESET` | retour état initial |
| REC-014 | Multi-utilisateur | changer identifiant | session isolée |
| REC-015 | Healthcheck | appeler `/api/health` | statut `ok` |

### Tests techniques associés

| ID | Commande | Résultat attendu |
|---|---|---|
| TEC-001 | `pytest` | tests backend OK |
| TEC-002 | `npm test` | tests frontend OK |
| TEC-003 | `npm run build` | build frontend OK |
| TEC-004 | `npm run e2e` | scénario navigateur OK |
| TEC-005 | `docker compose config --quiet` | configuration Docker valide |

---

## 10. Plan de correction des anomalies — C2.3.2

Le livrable dédié est disponible ici : [PLAN_CORRECTION_BOGUES.md](PLAN_CORRECTION_BOGUES.md).

### Processus

Le traitement d’une anomalie suit les étapes suivantes :

1. reproduction du bug ;
2. qualification de la gravité ;
3. identification du composant concerné ;
4. correction sur branche ou commit dédié ;
5. ajout ou mise à jour d’un test ;
6. validation locale ;
7. validation CI ;
8. mise à jour de la documentation si nécessaire.

### Classification

| Niveau | Critère | Exemple |
|---|---|---|
| Critique | application inutilisable | backend indisponible |
| Majeur | fonctionnalité essentielle cassée | combat impossible |
| Mineur | défaut non bloquant | affichage imparfait |
| Amélioration | confort ou dette technique | refactorisation |

### Exemples d’anomalies traitées

| Anomalie | Cause | Correction | Non-régression |
|---|---|---|---|
| Page Vite affichée | mauvais scaffold frontend | configuration React/Vite corrigée | `npm run build` |
| Inventaire invalide | clés d’objets incorrectes | création via templates existants | tests backend |
| CI import Python | chemin module absent | ajout `pytest.ini` | GitHub Actions |
| Tests E2E instables | état utilisateur persistant | identifiant E2E unique | Playwright |
| Risque conflit VPS | ports 80/443 déjà utilisés | port dédié 8081 | healthcheck public |
| Désérialisation d'armure équipée | `Armor` restaurée en `Item` générique | reconstruction `Armor` dans `item_from_dict` | `pytest -q` → `39 passed` |
| Déploiement GitHub Actions refusé | clé SSH dédiée non autorisée / multi-ligne | secret base64 + clé publique VPS | run `Deploy VPS` réussi |

---

## 11. Documentation technique, exploitation et mise à jour — C2.4.1

### Documentation disponible

| Document | Rôle |
|---|---|
| `README.md` | présentation, installation, tests |
| `docs/deploiement_vps.md` | déploiement Docker sur VPS |
| `docs/architecture_bdd_multiutilisateur.md` | BDD et multi-utilisateur |
| `docs/gestion_projet/strategie_git.md` | Git, branches, tags, CI/CD |
| `docs/rncp/05_plan_de_recette.md` | recette fonctionnelle |
| `docs/rncp/04_bloc4_maintenance.md` | maintenance et supervision |

### Manuel d’installation local

1. cloner le dépôt ;
2. créer l’environnement Python ;
3. installer `requirements.txt` ;
4. installer les dépendances frontend avec `npm ci` ;
5. lancer backend et frontend ;
6. ouvrir le navigateur.

### Manuel d’exploitation VPS

1. se connecter au VPS ;
2. se placer dans `/opt/rpg-40k` ;
3. lancer `docker compose -p rpg40k ps` ;
4. consulter les logs avec `docker compose -p rpg40k logs -f` ;
5. mettre à jour avec `git pull` puis `docker compose -p rpg40k up -d --build`.

### Manuel de mise à jour

La mise à jour standard suit ce flux :

1. développer et tester localement ;
2. pousser sur GitHub ;
3. attendre la CI ;
4. déclencher le déploiement manuel si nécessaire ;
5. vérifier `/api/health` ;
6. valider le parcours utilisateur.

---

## 12. Historique des versions et traçabilité

| Version | Contenu |
|---|---|
| `0.1` | prototype CLI, personnage et dés |
| `0.2` | combat, inventaire, progression |
| `0.3` | monde, quêtes, relations |
| `0.4` | FastAPI REST/SSE |
| `0.5` | frontend React/Vite |
| `0.6` | correction Vite, scripts de lancement |
| `0.7` | jouabilité web, fallback MJ local |
| `0.8` | documentation RNCP |
| `0.9` | tests API, healthcheck, accessibilité |
| `1.0` | BDD, multi-utilisateur, CI/CD, E2E, VPS |

La traçabilité est assurée par Git, la branche `main`, la branche `develop`, les commits et le tag `v1.0.0-rncp`.

---

## 13. Conclusion

Le projet répond aux attendus du Bloc 2 car il présente une application logicielle fonctionnelle, structurée, testée et déployable. Les environnements de développement, test et déploiement sont documentés. Le prototype respecte une architecture maintenable avec séparation frontend, backend, domaine métier et persistance. Les tests automatisés backend, frontend et end-to-end réduisent les risques de régression. Les enjeux de sécurité, accessibilité, versioning, recette et exploitation sont pris en compte.

Les limites restantes sont identifiées : authentification réelle, audit RGAA complet, migration complète des sauvegardes en base relationnelle et HTTPS sur sous-domaine. Ces points constituent des évolutions réalistes pour une version ultérieure.

---

## 14. Annexes proposées

Les annexes ne sont pas comptabilisées dans les 30 pages du dossier. Les éléments suivants peuvent être ajoutés à part :

- captures d’écran de l’interface ;
- captures GitHub Actions en succès ;
- sortie `pytest` ;
- sortie `npm test` ;
- sortie `npm run e2e` ;
- extrait du `docker compose ps` sur VPS ;
- extrait du healthcheck public ;
- lien vers le dépôt GitHub ;
- export du Kanban ;
- schéma d’architecture visuel.
