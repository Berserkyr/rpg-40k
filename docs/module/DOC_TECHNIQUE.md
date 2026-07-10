# Documentation technique

**Projet :** RPG 40K Survivor
**Stack :** React (Vite) · FastAPI · SQLite · OpenAI

---

## 1. Architecture logicielle

Trois couches clairement séparées :

1. **Présentation** — SPA React (`frontend/`).
2. **API / logique applicative** — FastAPI (`backend/`).
3. **Domaine métier du jeu** — modules Python (`src/`).

```
frontend (React/Vite)
   │  REST (actions) + SSE (narration)
   ▼
backend/api.py (FastAPI)
   ├─ backend/auth.py       → JWT + bcrypt + rôles
   ├─ backend/database.py   → SQLite (comptes, événements)
   └─ src/*.py              → état, combat, inventaire, monde, quêtes, IA
   │
   ▼
OpenAI API (narration) + SQLite + sauvegardes YAML
```

## 2. Stack et versions

| Composant | Version | Rôle |
|---|---|---|
| Python | 3.13 | Runtime backend |
| FastAPI | ≥ 0.136 | Framework API REST + SSE |
| PyJWT | ≥ 2.9 | Génération / vérification JWT |
| bcrypt | ≥ 4.2 | Hachage des mots de passe |
| React | 18 | Interface |
| Vite | 8 | Build / dev server |
| SQLite | intégré | Persistance relationnelle |

## 3. Flux de données (exemple : action de jeu)

```
1. L'utilisateur clique "FOUILLER" dans le frontend.
2. api.js envoie POST /api/loot avec l'en-tête Authorization: Bearer <JWT>.
3. FastAPI valide le JWT (dépendance get_current_user) → identité + rôle.
4. La session du joueur est chargée/instanciée (isolée par utilisateur).
5. Le domaine (src/inventory.py) génère du butin.
6. L'état est sauvegardé (YAML) et renvoyé en JSON.
7. Le frontend met à jour l'inventaire et le terminal.
```

Pour la **narration** (`/api/start`, `/api/chat`), la réponse est un flux **SSE** :
le backend streame les tokens de l'IA au fur et à mesure (`_gm_stream`).

## 4. Sécurité

| Mesure | Implémentation |
|---|---|
| Mots de passe hachés | bcrypt (`backend/auth.py: hash_password`) |
| Jetons signés | JWT HS256 avec expiration (`create_access_token`) |
| Vérification à chaque requête | dépendance `get_current_user` |
| Rôles | `player` / `admin`, `require_admin` sur routes sensibles |
| Secrets hors dépôt | `JWT_SECRET`, `OPENAI_API_KEY` en variables d'environnement |
| 401 / 403 | accès refusé sans jeton / sans rôle suffisant |

## 5. Points d'API principaux

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/api/health` | non | État de santé |
| POST | `/api/auth/register` | non | Créer un compte (retourne JWT) |
| POST | `/api/auth/login` | non | Se connecter (retourne JWT) |
| GET | `/api/auth/me` | JWT | Identité courante |
| GET | `/api/users` | admin | Liste des utilisateurs |
| GET | `/api/state` | JWT | État complet de la partie |
| POST | `/api/start` | JWT | Démarrer (SSE) |
| POST | `/api/chat` | JWT | Message au MJ (SSE) |
| POST | `/api/roll` | JWT | Jet 2D6 |
| POST | `/api/combat/start` | JWT | Démarrer un combat |
| POST | `/api/combat/action` | JWT | Action de combat |
| POST | `/api/travel` | JWT | Déplacement |
| POST | `/api/loot` | JWT | Butin |
| POST | `/api/learn` | JWT | Compétence |
| POST | `/api/save` | JWT | Sauvegarde |
| POST | `/api/reset` | JWT | Nouvelle partie |

La documentation interactive OpenAPI est disponible sur `/docs` (Swagger UI généré par FastAPI).

## 6. Installation et lancement

### Backend

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.api:app --reload --port 8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

### Variables d'environnement (`.env`)

```env
OPENAI_API_KEY=sk-...        # optionnel (repli local sinon)
JWT_SECRET=une-chaine-secrète
JWT_EXPIRE_MINUTES=720
```

### Créer un administrateur (pour tester les rôles)

```powershell
python -m backend.create_admin monadmin motdepasse
```

## 7. Tests

```powershell
pytest            # tests backend (dont auth JWT)
cd frontend
npm test          # tests unitaires frontend
```
