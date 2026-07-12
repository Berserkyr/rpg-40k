# User stories — Survivant de Ruche (C2.2.1)

**Certification :** Expert en Développement Logiciel — RNCP 39583
**Compétence visée :** C2.2.1 — Concevoir un prototype répondant aux fonctionnalités
attendues et aux user stories.
**Projet support :** RPG 40K Survivor (« Survivant de Ruche »).

Ce document formalise les principales user stories du prototype, reliées à leurs
critères d'acceptation et aux preuves de réalisation (fonctionnalité + recette).

Format : *En tant que … je veux … afin de …*

---

## US-01 — Créer un compte et jouer en privé

**En tant que** joueur, **je veux** créer un compte sécurisé **afin de** retrouver ma
partie et qu'elle reste isolée des autres joueurs.

**Critères d'acceptation**
- Inscription avec identifiant + mot de passe (haché bcrypt).
- Connexion délivrant un jeton JWT.
- Chaque joueur n'accède qu'à sa propre partie.

**Preuves :** [backend/auth.py](../../backend/auth.py) · recette REC-F-001/002/003 · REC-SEC-008.

---

## US-02 — Vivre une aventure narrative

**En tant que** joueur, **je veux** démarrer une partie et interagir en langage
naturel **afin de** vivre une histoire qui réagit à mes choix.

**Critères d'acceptation**
- Démarrage déclenchant une narration diffusée en temps réel (SSE).
- Saisie d'action libre produisant une réponse du MJ.
- Repli local si aucune IA distante n'est configurée.

**Preuves :** `POST /api/start`, `POST /api/chat` · recette REC-F-006/007/023.

---

## US-03 — Affronter les menaces

**En tant que** joueur, **je veux** déclencher et mener des combats **afin de**
survivre aux ennemis de la ruche.

**Critères d'acceptation**
- Déclenchement d'un combat (`RENCONTRE`).
- Actions attaquer / défendre / fuir avec mise à jour des points de vie.
- Clôture du combat avec résultat (victoire / repli).

**Preuves :** [src/combat.py](../../src/combat.py) · recette REC-F-010/011/012/013.

---

## US-04 — Explorer et me repérer

**En tant que** joueur, **je veux** me déplacer entre les zones et consulter une carte
évolutive **afin de** savoir où je suis et où je peux aller.

**Critères d'acceptation**
- Déplacement vers une zone accessible.
- Carte affichant position, zones explorées et chemins non empruntés.
- Trace d'exploration qui évolue au fil de la partie.

**Preuves :** [src/world.py](../../src/world.py), [frontend/src/components/MapExplorerPage.jsx](../../frontend/src/components/MapExplorerPage.jsx) · recette REC-F-014/015.

---

## US-05 — Équiper et gérer mon inventaire

**En tant que** joueur, **je veux** fouiller, équiper des objets et utiliser des
consommables **afin d'**améliorer mes chances de survie.

**Critères d'acceptation**
- Fouille produisant du butin.
- Équiper / retirer recalcule les attributs.
- Utiliser un consommable applique son effet (ex. soin) et le décompte.

**Preuves :** [src/inventory.py](../../src/inventory.py), [frontend/src/components/InventoryPanel.jsx](../../frontend/src/components/InventoryPanel.jsx) · recette REC-F-009/016/017/018.

---

## US-06 — Faire progresser mon personnage

**En tant que** joueur, **je veux** répartir des attributs et apprendre des compétences
**afin de** personnaliser et renforcer mon survivant.

**Critères d'acceptation**
- Allocation de points d'attribut disponibles.
- Apprentissage de compétences/talents avec effets pris en compte.

**Preuves :** [src/progression.py](../../src/progression.py), [frontend/src/components/SkillsPanel.jsx](../../frontend/src/components/SkillsPanel.jsx) · recette REC-F-019/020.

---

## US-07 — Sauvegarder et reprendre

**En tant que** joueur, **je veux** sauvegarder ma partie **afin de** la reprendre plus
tard sans repartir de zéro.

**Critères d'acceptation**
- Sauvegarde explicite avec confirmation.
- Rechargement automatique de la partie à la reconnexion.

**Preuves :** [src/persistence.py](../../src/persistence.py) · recette REC-F-021/003.

---

## US-08 — Jouer confortablement (accessibilité)

**En tant que** joueur sensible aux animations, **je veux** réduire les effets visuels
**afin de** lire l'interface confortablement.

**Critères d'acceptation**
- Bascule « effets réduits » mémorisée.
- Respect du réglage système `prefers-reduced-motion`.
- Navigation clavier et libellés accessibles.

**Preuves :** [frontend/src/App.jsx](../../frontend/src/App.jsx) · [MESURES_SECURITE_ACCESSIBILITE.md](MESURES_SECURITE_ACCESSIBILITE.md).

---

## Traçabilité synthétique

| US | Fonctionnalité principale | Cas de recette |
|---|---|---|
| US-01 | Authentification / isolation | REC-F-001..003, REC-SEC-008 |
| US-02 | Narration IA (SSE) | REC-F-006, 007, 023 |
| US-03 | Combat | REC-F-010..013 |
| US-04 | Exploration / carte | REC-F-014, 015 |
| US-05 | Inventaire / équipement | REC-F-009, 016..018 |
| US-06 | Progression / compétences | REC-F-019, 020 |
| US-07 | Sauvegarde / reprise | REC-F-021, 003 |
| US-08 | Accessibilité | — (audit a11y) |
