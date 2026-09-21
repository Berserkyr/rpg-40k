# Checklist des livrables — Activités 1 à 10 (conformité non validée)

> **Archive historique — classement le 20/09/2026.** Période antérieure ; date exacte de la campagne non établie. Cette checklist conserve les attendus historiques mais distingue désormais présence et validation. Aucun statut ci-dessous ne vaut validation RNCP/client, recette réussie ou contrôle de production. Voir l'[état de référence](../ETAT_PROJET_REFERENCE.md) (création prévue par l'utilisateur) et le [suivi actuel](../bloc3/02_TABLEAU_DE_BORD.md). Les PDF anciens ne sont pas régénérés et ne constituent pas une version actuelle.

Ce document met en correspondance les attendus historiques et les livrables ou fichiers de code présents. **Livrable présent / Code présent** signifie présence matérielle uniquement : les contenus, résultats et critères restent à vérifier avant toute acceptation.

Le README racine a été supprimé de la copie de travail et est indisponible ; ses liens cassés ont été retirés. La complétude du dépôt et des livrables attendus n'est donc pas attestée. L'[index du module](README.md) ne remplace pas ce livrable racine.

| Activité | Attendu de l'énoncé | Statut | Preuves dans le projet |
|---|---|---:|---|
| 1 — Architecture globale | Concept de jeu, architecture front/back, technologies, schéma, document d'intention | Livrable présent ; README racine indisponible | [DOCUMENT_CADRAGE.md](DOCUMENT_CADRAGE.md), [DOC_TECHNIQUE.md](DOC_TECHNIQUE.md) |
| 2 — MCD / MLD | BDD relationnelle, entités, relations, MCD, MLD | Livrable présent / Code présent | [MCD_MLD.md](MCD_MLD.md), [backend/database.py](../../backend/database.py) |
| 3 — Routes API REST | BDD opérationnelle, serveur API, routes REST, gestion erreurs | Code présent | [backend/api.py](../../backend/api.py), [tests/test_api.py](../../tests/test_api.py), Swagger `/docs` à vérifier à l'exécution |
| 4 — Lot fonctionnel | MVP, architecture, mockups, fonctionnalité end-to-end, doc technique | Livrable présent / Code présent | [WIREFRAMES.md](WIREFRAMES.md), [DOC_TECHNIQUE.md](DOC_TECHNIQUE.md), [frontend/src/App.jsx](../../frontend/src/App.jsx) |
| 5 — Sécurisation | `register`, `login`, JWT, routes protégées, token côté front, logout | Code présent | [backend/auth.py](../../backend/auth.py), [frontend/src/components/AuthPanel.jsx](../../frontend/src/components/AuthPanel.jsx), [frontend/src/api.js](../../frontend/src/api.js) |
| 6 — Flux clefs | Gestion loading/success/error, affichage dynamique, services API séparés | Livrable présent / Code présent | [DOC_TECHNIQUE.md](DOC_TECHNIQUE.md), [frontend/src/api.js](../../frontend/src/api.js), [frontend/src/hooks/useSSEChat.js](../../frontend/src/hooks/useSSEChat.js) |
| 7 — Améliorations | Backlog, priorisation, corrections, fonctionnalités critiques, démo | Livrable présent | [SPRINT_FINALISATION.md](SPRINT_FINALISATION.md), [docs/gestion_projet/kanban.md](../gestion_projet/kanban.md) |
| 8 — Optimisation | Audit technique, problèmes détectés, 2 optimisations, gains | Livrable présent | [AUDIT_OPTIMISATION.md](AUDIT_OPTIMISATION.md), [ANALYSE_CRITIQUE.md](ANALYSE_CRITIQUE.md) |
| 9 — Sprint finalisation | MoSCoW, corrections critiques, stabilité, UI/UX, support démo | Livrable présent ; README racine indisponible | [SPRINT_FINALISATION.md](SPRINT_FINALISATION.md) |
| 10 — Analyse critique | Points forts/faibles, refactoring, apports module, feuille de route | Livrable présent | [ANALYSE_CRITIQUE.md](ANALYSE_CRITIQUE.md) |

## Synthèse par livrable final demandé

| Livrable final | Statut | Fichiers à fournir / citer |
|---|---:|---|
| Document de cadrage + README racine attendu | Livrable présent pour le cadrage ; README racine indisponible | [DOCUMENT_CADRAGE.md](DOCUMENT_CADRAGE.md) ; README racine supprimé |
| MCD ou MLD | Livrable présent | [MCD_MLD.md](MCD_MLD.md) |
| API REST sécurisée JWT | Code présent | [backend/api.py](../../backend/api.py), [backend/auth.py](../../backend/auth.py) |
| Wireframes + frontend fonctionnel | Livrable présent / Code présent ; fonctionnement non vérifié | [WIREFRAMES.md](WIREFRAMES.md), [frontend/](../../frontend) |
| Dépôt GitHub (complétude attendue, non attestée) | Code présent localement ; complétude et état distant non vérifiés | `https://github.com/Berserkyr/rpg-40k` ; suppressions dans la copie de travail |
| Analyse critique | Livrable présent | [ANALYSE_CRITIQUE.md](ANALYSE_CRITIQUE.md) |
| Fonctionnalité IA réelle | Code présent ; facturation et fonctionnement distant à vérifier | [backend/api.py](../../backend/api.py), route `/api/chat` |

## Point de vigilance IA

L'intégration OpenAI est présente dans le code. Le bilan historique mentionne `billing_not_active` et un repli MJ local. L'état actuel de la facturation, le fonctionnement distant et le parcours de repli restent à vérifier : ni le code présent ni l'activation de la facturation ne garantissent une note ou une acceptation. Consigner l'exécution, les résultats et les réserves dans la [recette préparée](../bloc3/07_DEMONSTRATION_RECETTE_CLIENT.md), non exécutée dans cette intervention.
