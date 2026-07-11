# Harnais de tests unitaires — C2.2.2

**Certification :** Expert en Développement Logiciel — RNCP 39583  
**Bloc :** Bloc 2 — Concevoir et développer des applications logicielles  
**Critère :** C2.2.2 — Harnais de tests unitaires  
**Projet :** RPG 40K Survivor (« Survivant de Ruche »)

---

## 1. Attendu officiel de la grille

**Compétence C2.2.2.** Développer un harnais de test unitaire en tenant compte des
fonctionnalités demandées afin de prévenir les régressions et de s’assurer du bon
fonctionnement du logiciel.

**Livrable attendu :**
- un jeu de tests unitaires couvrant une fonctionnalité demandée.

**Critère d’évaluation :**
- les tests unitaires couvrent la majorité du code développé.

---

## 2. Stratégie du harnais de tests

Le harnais est organisé en trois niveaux complémentaires :

1. **Tests unitaires backend** (pytest) sur logique métier + API ;
2. **Tests unitaires frontend** (Vitest + RTL) sur composants et client API ;
3. **Tests E2E** (Playwright) pour valider le parcours utilisateur global.

Ce découpage garantit qu’une régression est détectée au plus tôt :
- d’abord au niveau fonction unitaire,
- puis au niveau composant,
- enfin au niveau parcours complet.

---

## 3. Périmètre de tests couvert

### Backend (pytest)

| Fichier de test | Fonctionnalité couverte |
|---|---|
| `tests/test_api.py` | authentification JWT, routes protégées, flux API |
| `tests/test_state.py` | état joueur, chargement/sauvegarde état |
| `tests/test_dice.py` | jets de dés et bornes de résultats |
| `tests/test_entities.py` | génération entités, rencontres, difficulté |
| `tests/test_inventory.py` | poids, stacking, équipement, sérialisation inventaire |
| `tests/test_progression.py` | XP, montée de niveau, déblocage compétences |
| `tests/test_world.py` | découverte zones, déplacements, blocages, sérialisation monde |
| `tests/test_quests.py` | objectifs, timers, récompenses, journal de quêtes |

### Frontend (Vitest / RTL)

| Fichier de test | Fonctionnalité couverte |
|---|---|
| `frontend/src/__tests__/api.test.js` | client API, gestion token/session |
| `frontend/src/components/__tests__/ActionPanel.test.jsx` | actions principales et callbacks |
| `frontend/src/components/__tests__/CharacterPanel.test.jsx` | rendu état personnage |
| `frontend/src/components/__tests__/CombatPanel.test.jsx` | interactions combat |
| `frontend/src/components/__tests__/InputBar.test.jsx` | saisie utilisateur / envoi message |

### E2E (Playwright)

| Fichier E2E | Fonctionnalité couverte |
|---|---|
| `frontend/e2e/game.spec.js` | inscription/connexion, démarrage partie, actions in-game |

---

## 4. Résultats mesurés

### Exécution des tests

```powershell
# Backend
python -m pytest -q
# 39 passed

# Frontend
cd frontend
npm test
# 13 passed
```

### Couverture backend (src + backend)

Commande :

```powershell
python -m pytest --cov=src --cov=backend --cov-report=term -q
```

Résultat global :
- **TOTAL : 64%** (2237 statements, 800 non couverts)

Extraits significatifs :
- `backend/auth.py` : 88%
- `backend/database.py` : 90%
- `src/entities.py` : 93%
- `src/inventory.py` : 76%
- `src/world.py` : 78%
- `src/progression.py` : 71%
- `src/quests.py` : 68%

### Couverture frontend (Vitest v8)

Commande :

```powershell
cd frontend
npx vitest run --coverage.enabled true --coverage.provider=v8 --coverage.reporter=text
```

Résultat global :
- **Statements : 65.78%**
- **Branches : 48.21%**
- **Functions : 80%**
- **Lines : 68.62%**

Lecture importante :
- la couverture des composants JSX testés est très élevée ;
- les fichiers CSS importés sont comptés à 0% par l’outil, ce qui baisse mécaniquement
  le score global sans impacter la logique applicative.

---

## 5. Prévention des régressions

Le harnais empêche la mise en production d’un code cassé :

1. push sur `main` ;
2. exécution CI (`pytest`, `npm test`, `npm run build`, E2E) ;
3. **déploiement VPS uniquement si la CI est verte**.

Le workflow de déploiement est conditionné par la réussite de la CI (`workflow_run`
conclusion = success), ce qui garantit qu’un échec de test bloque le CD.

---

## 6. Exemples de régressions capturées

| Régression détectée | Détection par test | Correction appliquée |
|---|---|---|
| Désérialisation d’armure équipée en `Item` générique | `test_inventory_round_trip_serialization_preserves_equipment` | reconstruction `Armor` dans `item_from_dict()` |
| Couverture métier insuffisante sur modules domaine | analyse de couverture | ajout de tests dédiés inventaire/progression/world/quests |

---

## 7. Conclusion C2.2.2

Le projet dispose d’un **harnais de tests unitaires concret, exécutable et mesuré** :
- jeu de tests backend + frontend couvrant les fonctionnalités critiques ;
- métriques de couverture chiffrées ;
- intégration dans la CI/CD avec blocage de déploiement en cas d’échec.

Le livrable C2.2.2 est donc couvert par ce document et les suites de tests associées.
