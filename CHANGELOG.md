# Journal des versions — Survivant de Ruche

Toutes les évolutions notables du projet sont consignées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/) ·
Versionnage sémantique (`MAJEUR.MINEUR.CORRECTIF`).

Ce journal matérialise la **traçabilité des versions** attendue par la grille
(C2.2.4 « historique des différentes versions ») et sert de référence aux points de
**retour arrière** décrits dans le [manuel de mise à jour](docs/module/MANUEL_MISE_A_JOUR.md).

---

## [Non publié]

Incréments intégrés sur `main` en vue de la prochaine version.

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
  `test_team.py`, `test_bestiary.py`, `test_animations.py` (82 tests backend au vert).
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
| 1.2.0 | `7d9bf12` | CI verte + déploiement VPS |
| 1.1.0 | `b565b39` | CI verte + déploiement VPS |
| 1.0.1 | `5b1164d` | CI verte |
| 1.0.0-rncp | `v1.0.0-rncp` | Application en ligne `http://89.116.111.166:8081/` |
