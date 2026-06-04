# RPG 40K Survivor

Assistant solo textuel inspire de Warhammer 40K : incarnez un citoyen imperial pris dans l'enfer d'une invasion tyranide. Le projet fournit :

- un prompt MJ grimdark pret a l'emploi,
- une fiche de personnage basique,
- un script CLI qui orchestre la partie avec l'API OpenAI,
- des utilitaires pour les jets de des, le suivi d'etat et les sauvegardes par scene,
- des tests simples pour s'assurer que la logique auxiliaire fonctionne.

## Dossier RNCP / soutenance

Un dossier de preuves a été ajouté pour relier le projet à la grille **Expert en développement logiciel RNCP 39583** :

- [Cartographie avec la grille](docs/rncp/00_cartographie_grille.md)
- [Bloc 1 — cadrage projet](docs/rncp/01_bloc1_cadrage.md)
- [Bloc 2 — conception et développement](docs/rncp/02_bloc2_conception_developpement.md)
- [Bloc 3 — pilotage projet](docs/rncp/03_bloc3_pilotage.md)
- [Bloc 4 — maintenance](docs/rncp/04_bloc4_maintenance.md)
- [Plan de recette](docs/rncp/05_plan_de_recette.md)
- [Support de soutenance](docs/rncp/06_support_soutenance.md)
- [Checklist jury](docs/rncp/07_checklist_jury.md)
- [Architecture BDD et multi-utilisateur](docs/architecture_bdd_multiutilisateur.md)
- [Kanban projet](docs/gestion_projet/kanban.md)
- [Stratégie Git, branches, tags et pipeline](docs/gestion_projet/strategie_git.md)

## État des attendus complémentaires

| Attendu | Statut | Preuve |
|---|---|---|
| BDD | En place | SQLite via [backend/database.py](backend/database.py) |
| Multi-utilisateur | En place | En-tête `X-User-Id` + champ joueur dans l’UI |
| Pipeline | En place | [CI GitHub Actions](.github/workflows/ci.yml) + [GitLab CI](.gitlab-ci.yml) |
| Tests end-to-end | En place | Playwright dans [frontend/e2e/game.spec.js](frontend/e2e/game.spec.js) |
| Kanban | En place | [docs/gestion_projet/kanban.md](docs/gestion_projet/kanban.md) |
| Git tag / multibranche | Prévu dans Git | [docs/gestion_projet/strategie_git.md](docs/gestion_projet/strategie_git.md) |

## Plan d'implementation

1. **Prompt & lore** a part : `prompt_survivant.md` fixe la voix du MJ, les jauges et les consignes grimdark.
2. **Donnees joueur** : `character_sheet.yaml` contient attributs, ressources, stress.
3. **Scripts** : `run_session.py` charge prompt + fiche, initialise la conversation et gere les commandes (lancer de des, affichage d'etat, sauvegardes, sortie).
4. **Lib Python** : utilitaires dans `src/` (gestion d'etat, formatage du prompt, tirages 2d6).
5. **Tests** : `pytest` valide chargement de fiche et coherence des jets.
6. **Securite** : la clef OpenAI reste dans l'env (`OPENAI_API_KEY`). Exemple : `.env.example`.

## Prerequis

- Python 3.11+
- Compte OpenAI avec acces aux modeles GPT compatibles chat
- Clef API stockee dans une variable d'environnement `OPENAI_API_KEY`

## Installation

```powershell
cd "c:\Users\ps3ka\OneDrive\Bureau\rpg 40k"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copiez `.env.example` en `.env` puis remplissez votre clef.

## Lancer une session

```powershell
.\.venv\Scripts\Activate.ps1
python run_session.py --model gpt-4.1-mini
```

Commandes disponibles pendant la session :

- `!roll` pour lancer 2d6 localement
- `!status` pour afficher la fiche actuelle
- `!save` pour forcer une sauvegarde meme si l'auto-save est inactive
- `!help` pour recapitulatif
- `!quit` pour terminer

### Sauvegardes par scene

Le script cree automatiquement un snapshot apres chaque scene (`saves/scene_###.yaml` par defaut). Options utiles :

```powershell
python run_session.py --save-dir parties\aelia --save-format json --no-auto-save
```

- `--save-dir` personnalise le dossier
- `--save-format` accepte `yaml` (defaut) ou `json`
- `--no-auto-save` desactive les snapshots automatiques; utilisez `!save` pour capturer une scene manuelle

## Tests unitaires

```powershell
.\.venv\Scripts\Activate.ps1
pytest
```

Les tests couvrent la creation de fiches et la distribution des jets 2d6.

## Tests end-to-end

Les tests navigateur utilisent Playwright.

```powershell
cd frontend
npm run e2e:install
npm run e2e
```

Ils nécessitent que le backend FastAPI soit lancé sur `127.0.0.1:8000` et le frontend Vite sur `127.0.0.1:5173`.

## Structure

```
README.md
prompt_survivant.md
character_sheet.yaml
run_session.py
src/
  __init__.py
  dice.py
  state.py
  prompt_builder.py
requirements.txt
.env.example
tests/
  test_state.py
  test_dice.py
```

## Mentions importantes

- Le projet fournit un cadre narratif grimdark mais n'utilise aucun contenu officiel protege.
- Ne partagez jamais votre clef API publiquement; utilisez `.env` ou le gestionnaire de secrets de votre OS.
- Adaptez librement les attributs et ressources pour varier vos parties.
