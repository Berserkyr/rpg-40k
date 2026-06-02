# Bloc 3 — Coordonner et piloter un projet de développement logiciel

## 1. Méthodologie projet

Méthode recommandée : **Kanban agile léger**.

Justification :

- Projet individuel ou petite équipe.
- Besoin de prioriser rapidement les fonctionnalités.
- Itérations courtes adaptées au prototype.
- Visualisation simple : à faire, en cours, terminé.
- Compatible avec démonstration progressive au jury.

## 2. Découpage du projet

| Lot | Description | Priorité |
|---|---|---:|
| L1 — Cadrage | besoin, périmètre, risques | Haute |
| L2 — Domaine métier | personnage, dés, combat, monde | Haute |
| L3 — Persistance | sauvegardes YAML, reprise partie | Haute |
| L4 — API | endpoints REST, SSE, fallback IA | Haute |
| L5 — Frontend | interface React, panneaux, actions | Haute |
| L6 — Tests | unitaires, API, recette | Moyenne |
| L7 — Documentation | RNCP, exploitation, utilisateur | Haute |
| L8 — Maintenance | anomalies, versions, supervision | Moyenne |

## 3. Planning prévisionnel

| Semaine | Objectifs | Livrables |
|---|---|---|
| S1 | Cadrage, besoin, architecture | Bloc 1, schéma architecture |
| S2 | Moteur métier Python | Modules `src/`, tests initiaux |
| S3 | API backend | [backend/api.py](../../backend/api.py) |
| S4 | Frontend React | [frontend/src/App.jsx](../../frontend/src/App.jsx) |
| S5 | Stabilisation | scripts, build, tests, recette |
| S6 | Dossier jury | docs RNCP, démo, maintenance |

## 4. Suivi d’avancement

| Indicateur | Mesure | État |
|---|---|---|
| Fonctionnalités principales | % fonctionnalités livrées | Élevé |
| Tests unitaires | nombre tests / périmètre | À renforcer |
| Build frontend | `npm run build` | OK |
| API backend | endpoints testés | OK sur endpoints principaux |
| Documentation | docs RNCP produites | En cours / complète après ce dossier |
| Dette technique | anomalies restantes | Moyenne |

## 5. Affectation des missions

Dans un contexte équipe, les missions seraient réparties ainsi :

| Rôle | Missions |
|---|---|
| Chef de projet | cadrage, planning, priorisation, recette |
| Développeur backend | API, domaine métier, persistance, tests backend |
| Développeur frontend | UI React, ergonomie, intégration API |
| QA | cahier de recette, tests non-régression |
| DevOps | scripts, CI/CD, supervision |
| UX/UI | accessibilité, parcours utilisateur |

Dans le projet actuel, ces rôles sont assumés par le candidat, ce qui démontre une vision transverse.

## 6. Cas d’arbitrage

### Problème rencontré

Le frontend affichait la page par défaut Vite au lieu de l’application React.

### Causes

- Le scaffold initial avait créé un projet TypeScript vanilla.
- Le fichier `index.html` pointait vers `src/main.ts`.
- React n’était pas correctement monté.

### Options possibles

| Option | Avantage | Inconvénient |
|---|---|---|
| Recréer entièrement le frontend | Propre | Risque de perte du travail existant |
| Adapter le scaffold existant | Rapide, préserve composants | Nécessite correction config |
| Utiliser autre framework | Nouvelle base | Hors périmètre |

### Décision

Adapter le scaffold existant : installation React, ajout `vite.config.js`, création `main.jsx`, correction `index.html`.

### Résultat

Le frontend React se lance correctement et le build est fonctionnel.

## 7. Comptes rendus d’activité

### Compte rendu — Itération backend

- Création API FastAPI.
- Ajout endpoints état, narration, combat, déplacement, sauvegarde.
- Correction inventaire.
- Ajout fallback MJ local.

### Compte rendu — Itération frontend

- Création interface terminal grimdark.
- Ajout panneaux personnage, carte, quêtes, combat, inventaire.
- Ajout boutons actions jouables.
- Correction scaffold Vite.

### Compte rendu — Itération stabilisation

- Build frontend validé.
- Endpoints principaux testés.
- Scripts de lancement créés.
- Dossier RNCP initialisé.

## 8. Démonstration jury proposée

Durée : 8 à 12 minutes.

1. Présenter objectif et architecture.
2. Lancer [start_game.bat](../../start_game.bat).
3. Montrer l’écran d’accueil.
4. Démarrer la campagne.
5. Effectuer un jet 2D6.
6. Fouiller une zone.
7. Déclencher une rencontre.
8. Résoudre un tour de combat.
9. Se déplacer vers une zone.
10. Sauvegarder.
11. Montrer rapidement le code backend/frontend.
12. Conclure sur tests, maintenance, améliorations.

## 9. Indicateurs de satisfaction

| Indicateur | Objectif |
|---|---|
| Lancement local | Moins de 2 minutes |
| Manipulation utilisateur | Sans terminal après lancement |
| Compréhension UI | Actions visibles et explicites |
| Robustesse | Pas de blocage si OpenAI indisponible |
| Démonstrabilité | Parcours complet possible en moins de 10 minutes |
