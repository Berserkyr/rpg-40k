# Plan de recette — Survivant de Ruche

## Objectif

Vérifier que l’application web RPG fonctionne conformément aux besoins principaux et qu’elle est démontrable devant un jury.

## Environnement de recette

- OS : Windows.
- Backend : Python/FastAPI sur `http://127.0.0.1:8000`.
- Frontend : React/Vite sur `http://localhost:5173`.
- Lancement : [start_game.bat](../../start_game.bat).

## Cas de test fonctionnels

| ID | Fonction | Précondition | Étapes | Résultat attendu | Statut |
|---|---|---|---|---|---|
| REC-001 | Lancement global | Projet installé | Double-cliquer `start_game.bat` | Backend + frontend lancés | À exécuter |
| REC-002 | Chargement état | Backend lancé | Appeler `/api/state` | JSON avec `character.name = Karimus` | À exécuter |
| REC-003 | Affichage UI | Frontend lancé | Ouvrir navigateur | Écran Survivant de Ruche visible | À exécuter |
| REC-004 | Démarrage partie | UI visible | Cliquer initialisation | Narration affichée en streaming | À exécuter |
| REC-005 | Action libre | Partie démarrée | Saisir une action | Réponse MJ affichée | À exécuter |
| REC-006 | Jet de dés | Partie démarrée | Cliquer `JET 2D6` | Résultat 2D6 affiché | À exécuter |
| REC-007 | Fouille | Partie démarrée | Cliquer `FOUILLER` | Butin ou message de fouille | À exécuter |
| REC-008 | Rencontre | Partie démarrée | Cliquer `RENCONTRE` | Panneau combat actif | À exécuter |
| REC-009 | Attaque | Combat actif | Cliquer `ATTAQUER` | Log combat + PV mis à jour | À exécuter |
| REC-010 | Défense | Combat actif | Cliquer `DÉFENDRE` | Action défensive loggée | À exécuter |
| REC-011 | Fuite | Combat actif | Cliquer `FUIR` | Fuite tentée, état mis à jour | À exécuter |
| REC-012 | Déplacement | Hors combat | Cliquer une zone | Zone actuelle changée | À exécuter |
| REC-013 | Sauvegarde | Partie active | Cliquer `SAUVER` | Message sauvegarde | À exécuter |
| REC-014 | Reset | Partie active | Cliquer `RESET` | Retour écran initial | À exécuter |

## Tests techniques

| ID | Commande | Résultat attendu |
|---|---|---|
| TEC-001 | `pytest` | Tous les tests passent |
| TEC-002 | `cd frontend && npm run build` | Build réussi |
| TEC-003 | `curl http://127.0.0.1:8000/api/state` | JSON valide |
| TEC-004 | `POST /api/start` | Flux SSE `data:` reçu |

## Critères d’acceptation

Le prototype est accepté si :

- Le jeu est lançable localement.
- Le parcours de démonstration fonctionne en moins de 10 minutes.
- Aucune erreur bloquante n’apparaît dans les actions principales.
- Le frontend compile.
- Les tests backend existants passent.
