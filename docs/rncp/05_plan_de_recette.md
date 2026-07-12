# Cahier de recettes — Survivant de Ruche (C2.3.1)

**Certification :** Expert en Développement Logiciel — RNCP 39583
**Compétence visée :** C2.3.1 — Élaborer le cahier de recettes en rédigeant les
scénarios de tests et les résultats attendus afin de détecter les anomalies de
fonctionnement et les régressions éventuelles.
**Projet support :** RPG 40K Survivor (« Survivant de Ruche »)
**Version recettée :** `v1.0.0-rncp` (+ incréments Gameplay V1/V2)
**Application déployée :** `http://89.116.111.166:8081/`

---

## 1. Objectif

Vérifier que l'application web répond aux fonctionnalités attendues et qu'elle est
démontrable devant un jury, en couvrant les **trois natures de tests** exigées par la
grille :

- **fonctionnels** — le comportement métier attendu par l'utilisateur ;
- **structurels** — la construction/compilation, les tests automatisés, l'intégrité technique ;
- **sécurité** — le contrôle d'accès et la robustesse des entrées.

Chaque cas suit le format : **ID · scénario · préconditions · étapes · résultat attendu ·
résultat obtenu · statut**.

Légende statut : ✅ Conforme · ⚠️ Conforme avec réserve · ❌ Non conforme · ⏳ À exécuter.

---

## 2. Environnement de recette

| Élément | Valeur |
|---|---|
| Poste | Windows 11, PowerShell 5.1 |
| Backend | Python 3.13 / FastAPI — `http://127.0.0.1:8000` |
| Frontend | React 18 / Vite — `http://localhost:5173` |
| Production | Docker Compose (VPS) — `http://89.116.111.166:8081/` |
| Lancement local | [start_game.bat](../../start_game.bat) |
| Date d'exécution | 12/07/2026 |

---

## 3. Tests fonctionnels

| ID | Fonction | Préconditions | Étapes | Résultat attendu | Résultat obtenu | Statut |
|---|---|---|---|---|---|---|
| REC-F-001 | Inscription | Backend lancé | Ouvrir l'app → inscription → identifiant + mot de passe → valider | Compte créé, JWT reçu, accès au jeu | Compte créé, redirection écran de jeu | ✅ |
| REC-F-002 | Connexion | Compte existant | Saisir identifiants → valider | Session ouverte, état chargé | Session ouverte, état `Karimus` chargé | ✅ |
| REC-F-003 | Persistance session | Connecté | Recharger la page | Session conservée (JWT en storage) | Reste connecté | ✅ |
| REC-F-004 | Déconnexion | Connecté | Cliquer `⏻ DÉCONNEXION` | Retour à l'écran d'authentification | Retour écran auth | ✅ |
| REC-F-005 | Chargement de l'état | Connecté | Appeler `GET /api/state` | JSON avec `character.name` | JSON complet renvoyé | ✅ |
| REC-F-006 | Démarrage de partie | Écran d'accueil | Cliquer `[ INITIALISER LA CONNEXION ]` | Narration diffusée en streaming (SSE) | Narration streamée (ou repli MJ local) | ✅ |
| REC-F-007 | Action libre | Partie démarrée | Saisir un texte → envoyer | Réponse du MJ affichée dans le terminal | Réponse MJ affichée | ✅ |
| REC-F-008 | Jet de dés | Partie démarrée | Cliquer `JET 2D6` | Résultat 2D6 formaté affiché | Résultat affiché en ligne `loot` | ✅ |
| REC-F-009 | Fouille | Partie démarrée | Cliquer `FOUILLER` | Butin listé ou message « rien d'exploitable » | Butin/inventaire mis à jour | ✅ |
| REC-F-010 | Déclenchement combat | Hors combat | Cliquer `RENCONTRE` | Panneau combat actif, message d'alerte | Combat actif, PV affichés | ✅ |
| REC-F-011 | Attaque | Combat actif | Cliquer `ATTAQUER` | Log de combat + PV ennemi mis à jour | Log + PV mis à jour | ✅ |
| REC-F-012 | Défense | Combat actif | Cliquer `DÉFENDRE` | Action défensive journalisée | Action défensive loggée | ✅ |
| REC-F-013 | Fuite | Combat actif | Cliquer `FUIR` | Tentative de fuite, état mis à jour, combat clôturé le cas échéant | Fuite tentée, état mis à jour | ✅ |
| REC-F-014 | Déplacement | Hors combat | Cliquer une zone accessible | Zone courante changée, message de trajet | Zone changée, trajet journalisé | ✅ |
| REC-F-015 | Carte explorateur | Connecté | Cliquer `🗺 CARTE` | Position, zones explorées et chemins non empruntés affichés | Carte évolutive affichée | ✅ |
| REC-F-016 | Équiper un objet | Objet équipable en sac | Ouvrir `🎒 SAC` → `ÉQUIPER` | Objet monté sur le slot, attributs recalculés | Objet équipé, stats mises à jour | ✅ |
| REC-F-017 | Retirer un objet | Objet équipé | `RETIRER` sur un slot | Objet remis en sac, attributs recalculés | Objet retiré, stats mises à jour | ✅ |
| REC-F-018 | Utiliser un consommable | Consommable en sac | `UTILISER` (ex. soin) | Effet appliqué (ex. PV restaurés), objet consommé | PV restaurés, quantité décrémentée | ✅ |
| REC-F-019 | Allouer un attribut | Points disponibles | `+` sur un attribut | Attribut incrémenté, points décrémentés | Attribut amélioré | ✅ |
| REC-F-020 | Apprendre une compétence | Panneau skills, points requis | `🧠 SKILLS` → apprendre | Compétence débloquée, effets pris en compte | Compétence apprise | ✅ |
| REC-F-021 | Sauvegarde | Partie active | Cliquer `SAUVER` | Message de confirmation, état persisté (YAML) | Sauvegarde confirmée | ✅ |
| REC-F-022 | Nouvelle partie | Partie active | Cliquer `RESET` | Retour à l'écran initial, état réinitialisé | Retour écran initial | ✅ |
| REC-F-023 | Repli MJ local | Sans `OPENAI_API_KEY` | Démarrer une partie | Narration générée localement (mode dégradé) | Narration locale servie, jeu jouable | ✅ |

---

## 4. Tests structurels

| ID | Objet | Étapes / Commande | Résultat attendu | Résultat obtenu | Statut |
|---|---|---|---|---|---|
| REC-S-001 | Tests unitaires backend | `pytest -q` | Tous les tests passent | **39 passed** (12/07/2026) | ✅ |
| REC-S-002 | Tests unitaires frontend | `cd frontend && npm test` | Tous les tests passent | **13 passed** | ✅ |
| REC-S-003 | Build production frontend | `cd frontend && npm run build` | Build réussi, bundle généré | Build OK (40 modules) | ✅ |
| REC-S-004 | Santé du service | `GET /api/health` | `200 OK` | `200 OK` | ✅ |
| REC-S-005 | Contrat d'état | `GET /api/state` (authentifié) | JSON valide conforme au schéma | JSON conforme | ✅ |
| REC-S-006 | Flux narratif | `POST /api/start` (authentifié) | Flux SSE `data:` reçu | Flux SSE reçu | ✅ |
| REC-S-007 | Pipeline CI | Push sur `main` | Jobs verts (tests + build + audit) | CI verte | ✅ |
| REC-S-008 | Tests E2E | `npx playwright test` | Parcours principal validé | Parcours validé | ✅ |

---

## 5. Tests de sécurité

| ID | Risque OWASP | Scénario | Étapes | Résultat attendu | Résultat obtenu | Statut |
|---|---|---|---|---|---|---|
| REC-SEC-001 | A01 — Broken Access Control | Route protégée sans jeton | `GET /api/state` **sans** en-tête `Authorization` | `401 Unauthorized` | `401 Unauthorized` | ✅ |
| REC-SEC-002 | A01 — Broken Access Control | Route admin par un joueur | `GET /api/users` avec JWT rôle `player` | `403 Forbidden` | `403 Forbidden` | ✅ |
| REC-SEC-003 | A07 — Auth Failures | Jeton invalide/expiré | `GET /api/state` avec JWT falsifié | `401 Unauthorized` | `401 Unauthorized` | ✅ |
| REC-SEC-004 | A04 — Insecure Design | Doublon d'inscription | `POST /api/auth/register` avec identifiant existant | `409 Conflict` | `409 Conflict` | ✅ |
| REC-SEC-005 | A03 — Injection / validation | Corps de requête malformé | `POST /api/auth/register` sans mot de passe | `422 Unprocessable Entity` | `422 (validation Pydantic)` | ✅ |
| REC-SEC-006 | A02 — Cryptographic Failures | Stockage des mots de passe | Inspecter la base après inscription | Mot de passe **haché bcrypt**, jamais en clair | Hash bcrypt stocké | ✅ |
| REC-SEC-007 | A05 — Misconfiguration | CORS en production | Définir `CORS_ALLOWED_ORIGINS` puis appeler depuis une origine non listée | Requête cross-origin non autorisée refusée | Origine restreinte appliquée | ✅ |
| REC-SEC-008 | A08 — Isolation des données | Cloisonnement par joueur | Se connecter avec 2 comptes distincts | Chaque joueur ne voit que sa propre partie | Sessions isolées par utilisateur | ✅ |

> Les cas REC-SEC-001 à 005 sont également couverts par des tests automatisés dans
> [tests/test_api.py](../../tests/test_api.py) (statuts HTTP 401/403/409/422),
> garantissant leur non-régression à chaque exécution de la CI.

---

## 6. Conformité au plan et critères d'acceptation

Le prototype est **accepté** si toutes les conditions suivantes sont réunies :

- [x] Le jeu est lançable localement ([start_game.bat](../../start_game.bat)) et accessible en production.
- [x] Le parcours de démonstration se déroule en moins de 10 minutes sans erreur bloquante.
- [x] Les tests fonctionnels principaux (§3) sont ✅.
- [x] Les tests structurels (§4) sont ✅ (backend 39, frontend 13, build OK).
- [x] Les tests de sécurité (§5) sont ✅ (contrôle d'accès 401/403, validation 422, hachage).
- [x] Aucune anomalie de criticité bloquante ouverte (voir [PLAN_CORRECTION_BOGUES.md](PLAN_CORRECTION_BOGUES.md)).

**Verdict de recette : PROTOTYPE ACCEPTÉ.** Les tests exécutés sont conformes au plan
défini (natures fonctionnelle, structurelle et sécurité couvertes).

---

## 7. Traçabilité

| Nature | Preuve automatisée | Emplacement |
|---|---|---|
| Fonctionnel / API | Tests backend `pytest` | [tests/test_api.py](../../tests/test_api.py) |
| Fonctionnel métier | Tests domaine | [tests/test_inventory.py](../../tests/test_inventory.py), [tests/test_world.py](../../tests/test_world.py), [tests/test_progression.py](../../tests/test_progression.py), [tests/test_quests.py](../../tests/test_quests.py) |
| Frontend | Tests Vitest | [frontend/src/__tests__/](../../frontend/src/__tests__) |
| Bout en bout | Playwright | [frontend/e2e/game.spec.js](../../frontend/e2e/game.spec.js) |
| Sécurité | Tests statuts HTTP | [tests/test_api.py](../../tests/test_api.py) |
| Anomalies détectées | Registre des bogues | [PLAN_CORRECTION_BOGUES.md](PLAN_CORRECTION_BOGUES.md) |
