# Journal des versions — Survivant de Ruche

Toutes les évolutions notables du projet sont consignées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/) ·
Versionnage sémantique (`MAJEUR.MINEUR.CORRECTIF`).

Ce journal matérialise la **traçabilité des versions** attendue par la grille
(C2.2.4 « historique des différentes versions ») et sert de référence aux points de
**retour arrière** décrits dans le [manuel de mise à jour](docs/module/MANUEL_MISE_A_JOUR.md).

---

## [Non publié]

Aucun incrément en attente.

---

## [1.3.0] — Maintien en condition opérationnelle — 19/08/2026

Réf. branche : `fix/ANO-2026-001-marqueurs-etat`.

Cette version regroupe la refonte gameplay V3 et la mise en place du dispositif
de maintien en condition opérationnelle (bloc 4) : supervision, gestion des
dépendances, traitement d'anomalie et durcissement du déploiement.

### Corrigé

- **ANO-2026-001 — Perte de la progression sur un marqueur d'état invalide**
  *(gravité : majeure, perte de données)*

  Le parseur des marqueurs `[ETAT: ...]` produits par le maître du jeu
  convertissait la valeur d'une ressource par `int()` sans protection. Le texte
  provenant d'un LLM, une valeur non numérique (`rations=aucune`,
  `munitions=+`) levait une `ValueError`. Levée dans le générateur SSE **après**
  l'envoi de la narration mais **avant** `session.save()`, l'exception
  interrompait le flux sans événement `done` — le client restait bloqué — et la
  scène jouée n'était jamais sauvegardée.

  *Correctif* : interception de la valeur non exploitable dans `src/state.py`
  (alignement sur la branche `tracks` qui traitait déjà ce cas), et confinement
  dans `backend/api.py` afin qu'aucune erreur de parsing ne puisse plus empêcher
  la clôture de la scène. 18 tests de non-régression, dont 16 en échec sur le
  code antérieur. Fiche complète : `docs/bloc4/03_collecte_consignation_anomalies.md`.

- **ANO-2026-002 — Perte partielle de progression au redémarrage**
  *(gravité : majeure, perte de données ; remontée via le support)*

  `Session.save()` persistait la progression, l'inventaire, les quêtes, la
  carte, les relations et l'équipe, mais **omettait la fiche de personnage**.
  Celle-ci était systématiquement rechargée depuis le modèle vierge
  `character_sheet.yaml`. Blessures, stress, ressources et points d'attribut
  alloués étaient donc perdus à chaque redémarrage du serveur, alors que le
  niveau et l'inventaire survivaient. Cette perte **partielle** rendait le
  symptôme déroutant et non reproductible en session unique.

  *Correctif* : ajout de `CharacterState.from_dict()` — `to_dict()` existait
  sans réciproque — et persistance de `character.yaml` dans `Session.save()`,
  avec repli sur le modèle vierge pour les sauvegardes antérieures. 8 tests de
  non-régression, dont 6 en échec sur le code antérieur. Fiche complète :
  `docs/bloc4/08_support_client.md`.

- **Version du logiciel incorrectement rapportée.** `backend/api.py` déclarait
  `version="1.0.0"` en dur alors que le journal était à `1.2.0` : `/api/health`
  identifiait donc mal la version en service, rendant impossible le
  rattachement fiable d'une anomalie à une version. La version est désormais
  lue depuis le fichier `VERSION`, source unique de vérité, et un test vérifie
  sa cohérence avec ce journal.

- **Documentation du déploiement contredite par le code.**
  `docs/gestion_projet/strategie_git.md` affirmait un déploiement
  « volontairement manuel », alors que `deploy-vps.yml` déclenche un
  déploiement automatique par `workflow_run` sur CI verte.

### Sécurité

- **Mode debug désactivé par défaut** *(recommandation R6)*. `FastAPI(debug=True)`
  était écrit en dur : toute exception non gérée exposait la trace d'exécution
  et des extraits de code source en production. Le mode est désormais piloté par
  la variable d'environnement `API_DEBUG`, absente par défaut.
- **Garde-fou sur `JWT_SECRET` au déploiement.** Le déploiement créait `.env`
  par copie de `.env.example` lorsqu'il était absent, ce qui signait les jetons
  de production avec le secret d'exemple public du dépôt. Le déploiement échoue
  désormais explicitement si `JWT_SECRET` est absent, trop court, ou laissé à sa
  valeur d'exemple.
- **Sonde de tentatives d'authentification** (`rpg40k_auth_attempts_total`) et
  alerte au-delà de 10 échecs par minute.

### Ajouté — Supervision et alerte (C4.1.2)

- **`backend/monitoring.py`** : sondes Prometheus, middleware HTTP (trafic,
  latence, erreurs), journalisation structurée pilotée par `LOG_LEVEL`.
- **Sonde d'aptitude `/api/health/ready`** : interroge réellement SQLite,
  vérifie les fichiers de jeu et l'accès en écriture, et renvoie `503` si une
  dépendance est indisponible. L'ancienne route `/api/health` répondait « ok »
  sans jamais interroger la base.
- **Point de collecte `/api/metrics`** au format d'exposition Prometheus.
- **Sonde `rpg40k_gm_generations_total{mode}`** : rend visible la bascule
  silencieuse vers le narrateur local lors d'une panne du fournisseur LLM —
  situation où l'application répond `200 OK` tout en rendant un service dégradé.
- **13 règles d'alerte** réparties en 5 groupes (disponibilité, qualité de
  service, dépendance LLM, sécurité, capacité), avec routage Alertmanager par
  sévérité, groupement et inhibition.
- **Tableau de bord Grafana** (13 panneaux) provisionné depuis le dépôt.
- **Pile de supervision** déployable en surcouche
  (`docker-compose.monitoring.yml`), sans modifier la pile applicative.

### Ajouté — Gestion des dépendances (C4.1.1)

- **`.github/dependabot.yml`** : détection hebdomadaire sur les 4 écosystèmes
  (pip, npm, Docker, GitHub Actions). Les versions mineures et correctives sont
  groupées, les majeures isolées en pull request individuelle.
- **Bornes hautes `<N.0.0`** sur les 12 dépendances backend. Les contraintes ne
  déclaraient que des planchers : une installation propre récupérait `openai`
  3.3.0 pour un plancher déclaré à 1.51.0, soit deux versions majeures d'écart
  sans décision ni évaluation d'impact.
- **`scripts/check_updates.py`** : rapport de veille classant les obsolescences
  selon la politique de mise à jour, intégré au job `security-audit`.

### Ajouté — Déploiement (C4.2.2)

- **`scripts/smoke_test.sh`** : 5 contrôles post-déploiement — disponibilité,
  aptitude des dépendances, exposition des sondes, refus d'accès non
  authentifié, livraison de l'interface.
- **Retour arrière automatique** : le commit en service est mémorisé avant
  déploiement ; en cas d'échec du test de fumée, la version précédente est
  restaurée. Le déploiement se terminait auparavant sur un simple `curl` de la
  sonde de vivacité, qui répond « ok » dès le démarrage du processus.

### Ajouté — Qualité et suivi (C4.2.1, C4.3.1, C4.3.2)

- **Formulaires de consignation structurés** (`.github/ISSUE_TEMPLATE/`) :
  anomalie (10 champs obligatoires), incident de supervision, retour
  d'expérience utilisateur. La saisie libre est désactivée.
- **`scripts/benchmark.py`** : mesure de la latence des routes, du poids livré
  au navigateur, de la croissance du contexte LLM et de la volumétrie SQLite.
- **Fichier `VERSION`** : source unique de vérité pour le numéro de version.

### Ajouté — Refonte gameplay V3 (combats tactiques & équipe)
- **Combat tactique** : conditions temporaires (saignement, étourdi, supprimé,
  marqué, aveuglé, inspiré, en garde, enragé), avantage/désavantage tactique
  (visée, couvert, alliés), points d'action, capacités actives de combat
  (frappe puissante, tir de suppression, marquage, parade, cri de ralliement…).
- **Arbre de compétences enrichi** : nouvelles compétences de combat et sociales,
  choix d'une compétence **à chaque montée de niveau** via des points de compétence,
  et **animation de montée de niveau**.
- **Mécanique de négociation** : dialogue avec l'ennemi (persuasion, intimidation,
  marchandage) pour éviter le combat, l'affaiblir ou rallier un adversaire.
  Les factions sans conscience (Tyranides) restent non négociables.
- **Gestion d'équipe & combats de groupe** : recrutement de compagnons
  (archétypes gérés par niveau), les alliés agissent à chaque tour, bonus de
  meneur, persistance de l'équipe.
- **Bestiaire étendu** : 8 factions jouables (Tyranides, Culte Genestealer, Chaos,
  Mechanicus, Arbites, Ecclésiarchie, Garde impériale, Civils) et rencontres
  générées en **groupes variés** (chef + sbires) avec factions aléatoires.
- **Sprites pixel art animés** des ennemis, générés de façon déterministe
  (faction + archétype + nom) sur canvas, sans aucun asset externe, avec
  **animations de combat vectorisées** (idle, attaque, touché, mort) et
  silhouettes distinctes par archétype (nuée, bête, colosse, psyker, humanoïde,
  daemon, machine).
- **Système d'animations procédurales générées par LLM** : génération automatique
  d'animations pour les skills de combat via GPT-4, avec **persistance et réutilisation**
  dans un cache JSON. Les animations sont définies par des descripteurs JSON déclaratifs
  (phases, transforms, particules, camera shake, flash) et interprétées par un moteur
  d'animation côté client. Composant React `AnimatedAction` réutilisable pour animer
  n'importe quel élément. Documentation complète dans `ANIMATIONS_SYSTEM.md`.
  Endpoints API : `/api/animations/{skill_id}`, `/api/animations/generate`,
  `/api/animations` (liste), `/api/animations` (delete cache admin).

### Modifié
- Barre d'en-tête enrichie (`👥 ÉQUIPE`).
- API de combat (`/api/combat/action`) refondue pour l'économie de points d'action
  et le ciblage ; nouveaux endpoints `/api/combat/negotiate`, `/api/team`,
  `/api/team/recruit`, `/api/team/dismiss`.

### Tests
- Nouveaux tests unitaires : `test_combat_tactics.py`, `test_negotiation.py`,
  `test_team.py`, `test_bestiary.py`, `test_animations.py`.
- `test_monitoring.py` (20 tests) : sondes, middleware, détection réelle d'une
  base corrompue par la sonde d'aptitude.
- `test_state_markers.py` (18 tests) : non-régression de l'anomalie ANO-2026-001.
- `test_version.py` (7 tests) : cohérence entre le fichier `VERSION`, l'API et ce journal.
- `test_character_persistence.py` (8 tests) : non-régression de l'anomalie ANO-2026-002.
- **Total : 82 → 135 tests backend au vert.**
- Tests frontend : `animation_engine.test.js` avec 16 tests couvrant le moteur
  d'animation, les particules et l'AnimationPlayer (30 tests frontend au vert).

### Documentation
- Cahier de recettes reformaté (fonctionnel / structurel / sécurité) avec statuts exécutés.
- Ajout du manuel d'utilisation et du manuel de mise à jour (C2.4.1).
- Ajout de ce journal des versions.

---

## [1.2.0] — Gameplay V2

Réf. commit : `7d9bf12`.

### Ajouté
- Page **carte explorateur** dédiée : position courante, zones explorées, chemins non
  empruntés, trace d'exploration évolutive.
- **Panneau compétences/talents/dons** avec apprentissage de compétences.
- Système d'**utilisation de consommables** (ex. soin restaurant des points de vie).

### Modifié
- Barre d'en-tête enrichie (`🗺 CARTE`, `🧠 SKILLS`).

---

## [1.1.0] — Gameplay V1

Réf. commit : `b565b39`.

### Ajouté
- **Attributs dynamiques** calculés depuis le niveau, l'équipement et les compétences.
- **Équiper / retirer** de l'équipement avec recalcul des statistiques.
- **Talents et dons spéciaux**.
- **Inventaire** en fenêtre « sac à dos » et **carte des déplacements**.

---

## [1.0.1] — Accessibilité & sécurité (C2.2.3)

Réf. commits : `5b1164d`, `dde37ec`, `6295a2d`.

### Ajouté
- Livrable sécurité/accessibilité (OWASP Top 10 + RGAA).
- Option **effets réduits** et prise en charge de `prefers-reduced-motion`.
- **CORS configurable** (`CORS_ALLOWED_ORIGINS`) et **audit des dépendances** en CI.

### Corrigé
- Contraste des couleurs mis en conformité **WCAG** (audit axe documenté).

---

## [1.0.0-rncp] — Version de référence certification

Réf. tag : `v1.0.0-rncp`.

### Ajouté
- Application web full-stack jouable : narration IA (SSE), combat, inventaire, monde,
  quêtes, progression, sauvegarde/chargement.
- **Authentification JWT + bcrypt**, rôles `player`/`admin`, isolation par utilisateur.
- Persistance **SQLite** (comptes/événements) + **YAML** (parties).
- **CI GitHub Actions** (tests backend, build frontend, E2E) et pipeline GitLab.
- **Déploiement VPS** via Docker Compose ; déploiement automatique sur CI verte.
- Tests unitaires backend (39) et frontend (13), tests E2E Playwright.
- Dossiers de certification RNCP (blocs 1 à 4) et documentation technique.

---

## Correspondance versions ↔ preuves

| Version | Tag / commit | Preuve de fonctionnement |
|---|---|---|
| 1.3.0 | `fix/ANO-2026-001-marqueurs-etat` | CI locale verte (135 backend + 30 frontend), test de fumée exécuté |
| 1.2.0 | `7d9bf12` | CI verte + déploiement VPS |
| 1.1.0 | `b565b39` | CI verte + déploiement VPS |
| 1.0.1 | `5b1164d` | CI verte |
| 1.0.0-rncp | `v1.0.0-rncp` | Application en ligne `http://89.116.111.166:8081/` |
