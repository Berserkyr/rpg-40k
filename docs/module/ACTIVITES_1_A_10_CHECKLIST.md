# Checklist de conformité — Activités 1 à 10

Ce document mappe chaque énoncé du dossier `projet jeux video` avec les preuves présentes dans le dépôt.

| Activité | Attendu de l'énoncé | Statut | Preuves dans le projet |
|---|---|---:|---|
| 1 — Architecture globale | Concept de jeu, architecture front/back, technologies, schéma, document d'intention | ✅ OK | [DOCUMENT_CADRAGE.md](DOCUMENT_CADRAGE.md), [DOC_TECHNIQUE.md](DOC_TECHNIQUE.md), [README.md](../../README.md) |
| 2 — MCD / MLD | BDD relationnelle, entités, relations, MCD, MLD | ✅ OK | [MCD_MLD.md](MCD_MLD.md), [backend/database.py](../../backend/database.py) |
| 3 — Routes API REST | BDD opérationnelle, serveur API, routes REST, gestion erreurs | ✅ OK | [backend/api.py](../../backend/api.py), [tests/test_api.py](../../tests/test_api.py), Swagger `/docs` |
| 4 — Lot fonctionnel | MVP, architecture, mockups, fonctionnalité end-to-end, doc technique | ✅ OK | [WIREFRAMES.md](WIREFRAMES.md), [DOC_TECHNIQUE.md](DOC_TECHNIQUE.md), [frontend/src/App.jsx](../../frontend/src/App.jsx) |
| 5 — Sécurisation | `register`, `login`, JWT, routes protégées, token côté front, logout | ✅ OK | [backend/auth.py](../../backend/auth.py), [frontend/src/components/AuthPanel.jsx](../../frontend/src/components/AuthPanel.jsx), [frontend/src/api.js](../../frontend/src/api.js) |
| 6 — Flux clefs | Gestion loading/success/error, affichage dynamique, services API séparés | ✅ OK | [DOC_TECHNIQUE.md](DOC_TECHNIQUE.md), [frontend/src/api.js](../../frontend/src/api.js), [frontend/src/hooks/useSSEChat.js](../../frontend/src/hooks/useSSEChat.js) |
| 7 — Améliorations | Backlog, priorisation, corrections, fonctionnalités critiques, démo | ✅ OK | [SPRINT_FINALISATION.md](SPRINT_FINALISATION.md), [docs/gestion_projet/kanban.md](../gestion_projet/kanban.md) |
| 8 — Optimisation | Audit technique, problèmes détectés, 2 optimisations, gains | ✅ OK | [AUDIT_OPTIMISATION.md](AUDIT_OPTIMISATION.md), [ANALYSE_CRITIQUE.md](ANALYSE_CRITIQUE.md) |
| 9 — Sprint finalisation | MoSCoW, corrections critiques, stabilité, UI/UX, support démo | ✅ OK | [SPRINT_FINALISATION.md](SPRINT_FINALISATION.md), [README.md](../../README.md) |
| 10 — Analyse critique | Points forts/faibles, refactoring, apports module, feuille de route | ✅ OK | [ANALYSE_CRITIQUE.md](ANALYSE_CRITIQUE.md) |

## Synthèse par livrable final demandé

| Livrable final | Statut | Fichiers à fournir / citer |
|---|---:|---|
| Document de cadrage + README complet | ✅ OK | [DOCUMENT_CADRAGE.md](DOCUMENT_CADRAGE.md), [README.md](../../README.md) |
| MCD ou MLD | ✅ OK | [MCD_MLD.md](MCD_MLD.md) |
| API REST sécurisée JWT | ✅ OK | [backend/api.py](../../backend/api.py), [backend/auth.py](../../backend/auth.py) |
| Wireframes + frontend fonctionnel | ✅ OK | [WIREFRAMES.md](WIREFRAMES.md), [frontend/](../../frontend) |
| Dépôt GitHub complet | ✅ OK | `https://github.com/Berserkyr/rpg-40k` |
| Analyse critique | ✅ OK | [ANALYSE_CRITIQUE.md](ANALYSE_CRITIQUE.md) |
| Fonctionnalité IA réelle | ✅ Code OK / ⚠️ billing OpenAI à activer | [backend/api.py](../../backend/api.py), route `/api/chat` |

## Point de vigilance IA

L'intégration OpenAI est réelle et présente dans le code. Si le compte OpenAI renvoie `billing_not_active`, le projet bascule en mode MJ local pour rester démontrable. Pour obtenir tous les points de la fonctionnalité IA, activer la facturation OpenAI ou utiliser une clé liée à un compte actif avant la soutenance.
