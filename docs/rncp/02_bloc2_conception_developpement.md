# Bloc 2 — Concevoir et développer des applications logicielles

## 1. Environnement de développement et de test

| Élément | Outil |
|---|---|
| Éditeur | Visual Studio Code |
| Backend | Python 3.13, FastAPI, Uvicorn |
| Frontend | React, Vite |
| Tests Python | Pytest |
| Gestion dépendances backend | `requirements.txt` |
| Gestion dépendances frontend | `package.json`, `package-lock.json` |
| Persistance | Fichiers YAML |
| Lancement local | [start_game.bat](../../start_game.bat) |

## 2. Architecture logicielle structurée

Le projet est structuré en couches :

```text
frontend/                  Interface React
backend/api.py             API REST + SSE
src/                       Domaine métier
  combat.py                Système de combat
  inventory.py             Inventaire, équipement, loot
  progression.py           XP et compétences
  world.py                 Carte, zones, déplacements
  quests.py                Quêtes
  relationships.py         Factions et PNJ
  persistence.py           Sauvegarde du monde
saves/                     État persistant
```

Cette séparation facilite la maintenabilité : le frontend ne manipule pas directement les fichiers de sauvegarde ; il passe par l’API.

## 3. Prototype fonctionnel

Fonctionnalités actuellement disponibles :

- Démarrage d’une campagne.
- Streaming de narration MJ.
- Mode MJ local si OpenAI est indisponible.
- Affichage personnage, attributs, stress, ressources et XP.
- Carte avec zone actuelle et zones accessibles.
- Quêtes actives.
- Inventaire.
- Jet 2D6.
- Fouille et génération de butin.
- Rencontre hostile.
- Combat tour par tour.
- Déplacement entre zones.
- Sauvegarde et reset.

## 4. API principale

| Endpoint | Rôle |
|---|---|
| `GET /api/state` | Retourne l’état complet de la session |
| `POST /api/start` | Lance la scène d’ouverture en SSE |
| `POST /api/chat` | Envoie une action libre au MJ |
| `POST /api/roll` | Lance 2D6 |
| `POST /api/loot` | Génère du butin |
| `POST /api/combat/start` | Démarre un combat |
| `POST /api/combat/action` | Résout une action de combat |
| `POST /api/travel` | Déplace le joueur |
| `POST /api/save` | Sauvegarde |
| `POST /api/reset` | Réinitialise la session |

## 5. Sécurité

### Mesures déjà présentes

| Risque | Mesure |
|---|---|
| Exposition clé OpenAI | Clé lue depuis variable d’environnement `OPENAI_API_KEY` |
| Panne fournisseur IA | Fallback MJ local |
| Appels cross-origin local | CORS configuré pour le développement |
| Entrées utilisateur | Modèles Pydantic côté API |
| Persistance | Sauvegardes structurées en YAML |

### Référentiel OWASP — analyse synthétique

| Catégorie OWASP | Situation actuelle | Action recommandée |
|---|---|---|
| Broken Access Control | Pas d’authentification car prototype local | Ajouter auth si multi-utilisateur |
| Cryptographic Failures | Pas de données sensibles hors clé API | Ne jamais versionner `.env` |
| Injection | Pas de SQL, entrées typées Pydantic | Échapper/valider davantage si DB future |
| Insecure Design | Mode local mono-utilisateur | Définir modèle de menace si déploiement public |
| Security Misconfiguration | CORS ouvert en dev | Restreindre CORS en production |
| Vulnerable Components | Dépendances npm/pip | Ajouter audit régulier |
| Authentication Failures | Non concerné prototype local | Prévoir session/auth si comptes utilisateurs |
| Software/Data Integrity | YAML local | Sauvegardes horodatées et validation schéma |
| Logging/Monitoring | Logs Uvicorn | Ajouter monitoring structuré |
| SSRF | Pas d’URL utilisateur appelée côté serveur | Maintenir cette restriction |

## 6. Accessibilité

Référentiel conseillé : **RGAA**.

Mesures existantes :

- Interface principalement textuelle.
- Contrastes visuels forts sur fond sombre.
- Boutons explicites.
- Navigation simple.

Améliorations recommandées :

- Vérifier tous les contrastes avec un outil dédié.
- Ajouter labels ARIA sur les boutons d’action.
- Tester la navigation clavier complète.
- Prévoir une option sans scanlines/animations.
- Ajouter messages d’erreurs accessibles.

## 7. Tests unitaires

Tests existants :

- [tests/test_dice.py](../../tests/test_dice.py)
- [tests/test_entities.py](../../tests/test_entities.py)
- [tests/test_state.py](../../tests/test_state.py)

Commande :

```powershell
pytest
```

Tests à ajouter :

- Tests de `Inventory.from_dict()`.
- Tests des endpoints FastAPI.
- Tests du fallback MJ local.
- Tests frontend avec React Testing Library.
- Tests end-to-end Playwright.

## 8. Cahier de recette

| Scénario | Étapes | Résultat attendu |
|---|---|---|
| Démarrer le jeu | Lancer `start_game.bat`, ouvrir navigateur | Interface du jeu visible |
| Charger l’état | Appel `GET /api/state` | État JSON de Karimus retourné |
| Scène d’ouverture | Cliquer initialisation | Texte narratif streamé |
| Lancer les dés | Cliquer `JET 2D6` | Résultat affiché dans terminal |
| Fouiller | Cliquer `FOUILLER` | Butin ajouté ou message rien trouvé |
| Rencontre | Cliquer `RENCONTRE` | Combat actif affiché |
| Combat | Cliquer `ATTAQUER` | PV ennemis/joueur mis à jour |
| Fuite | Cliquer `FUIR` | Combat terminé si fuite réussie |
| Déplacement | Cliquer une zone accessible | Zone actuelle changée |
| Sauvegarde | Cliquer `SAUVER` | Message sauvegarde affiché |
| Reset | Cliquer `RESET` | Session réinitialisée |

## 9. Manuel utilisateur court

1. Lancer [start_game.bat](../../start_game.bat).
2. Attendre l’ouverture du navigateur.
3. Cliquer sur `INITIALISER LA CONNEXION`.
4. Utiliser les boutons d’action pour jouer.
5. Saisir des actions libres dans le champ texte.
6. Sauvegarder régulièrement.

## 10. Documentation d’exploitation

### Backend

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000
```

### Frontend

```powershell
cd frontend
npm run dev -- --host=127.0.0.1 --port=5173
```

### Build frontend

```powershell
cd frontend
npm run build
```

### Tests

```powershell
pytest
```
