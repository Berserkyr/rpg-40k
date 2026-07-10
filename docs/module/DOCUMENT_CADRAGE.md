# Document de cadrage — Projet Jeu Vidéo Fullstack

**Module :** Coordination dev Front & Back — M2 Dev Fullstack (Ynov Connect)
**Auteur :** Projet individuel
**Type de projet :** Jeu vidéo fullstack web
**Dépôt :** https://github.com/Berserkyr/rpg-40k (public)

---

## 1. Présentation du projet

**RPG 40K Survivor** (nom interne « Survivant de Ruche ») est un jeu de rôle solo textuel
au format web, dans un univers grimdark inspiré de la science-fiction militaire.
Le joueur incarne **Karimus**, un technicien vox impérial piégé dans une ruche
lors d'une invasion. Il doit survivre : explorer, combattre, gérer son inventaire,
faire progresser son personnage et interagir avec un **Maître du Jeu (MJ) piloté par une IA**.

Le projet met en œuvre une **communication front/back complète** :
- un **frontend React** (interface terminal grimdark) ;
- un **backend FastAPI** exposant une API REST + streaming SSE ;
- une **base de données SQLite** pour les comptes et les traces de session ;
- une **fonctionnalité IA** (narration dynamique via l'API OpenAI, avec repli local).

## 2. Objectifs

| Objectif | Description |
|---|---|
| Jeu jouable bout en bout | Créer un compte, se connecter, démarrer une partie, agir, sauvegarder |
| Communication front/back | REST pour les actions, SSE pour la narration en flux |
| IA réellement intégrée | Le MJ génère la narration via OpenAI (pas un mock) |
| Sécurité | Authentification JWT, mots de passe hachés, rôles |
| Persistance | Comptes en base, sauvegardes de partie isolées par joueur |

## 3. Périmètre fonctionnel

**Inclus :**
- inscription / connexion sécurisées (JWT) ;
- narration IA en streaming ;
- jets de dés 2D6 ;
- système de combat au tour par tour ;
- inventaire et butin procédural ;
- carte de zones et déplacements ;
- quêtes et relations de faction ;
- progression (XP, compétences) ;
- sauvegarde/chargement par utilisateur.

**Hors périmètre (assumé) :**
- multijoueur temps réel ;
- moteur graphique 2D/3D (le jeu est textuel) ;
- paiement / monétisation.

## 4. Stack technique

| Couche | Technologie | Justification |
|---|---|---|
| Frontend | React 18 + Vite | SPA réactive, build rapide, écosystème mûr |
| Communication | REST + SSE (fetch) | REST pour les actions, SSE pour le flux narratif |
| Backend | FastAPI (Python 3.13) | Async natif, validation Pydantic, OpenAPI auto |
| Sécurité | JWT (PyJWT) + bcrypt | Standard d'authentification stateless + hachage sûr |
| Base de données | SQLite | Légère, sans serveur, suffisante pour le périmètre |
| IA | OpenAI Chat Completions | Génération narrative de qualité, streaming |
| Sauvegardes | YAML par utilisateur | Lisible, versionnable, isolé par joueur |

## 5. Implémentation de l'IA

Le MJ est piloté par l'API **OpenAI** (`gpt-4o-mini`). À chaque action du joueur :
1. le backend construit un prompt système (lore + état du monde) ;
2. il envoie l'historique de conversation à OpenAI ;
3. la réponse est **streamée en direct** vers le frontend via SSE ;
4. l'état du jeu est mis à jour et sauvegardé.

Un **mode de repli local** garantit que le jeu reste jouable même sans clé API
(narration procédurale déterministe), ce qui sécurise la démonstration.

## 6. Architecture globale

```
┌──────────────┐   REST + SSE    ┌──────────────┐    ┌──────────────┐
│  React/Vite  │ ───────────────▶│   FastAPI    │───▶│  OpenAI API  │
│  (frontend)  │◀─────────────── │  (backend)   │    └──────────────┘
└──────────────┘   JSON / flux   └──────┬───────┘
                                        │
                                 ┌──────┴───────┐
                                 │   SQLite     │  comptes, rôles, événements
                                 │  + YAML      │  sauvegardes par joueur
                                 └──────────────┘
```

## 7. Sécurité prévue

- Mots de passe **hachés avec bcrypt** (jamais stockés en clair).
- **JWT signés (HS256)** avec expiration, transmis en `Authorization: Bearer`.
- **Rôles** `player` / `admin` avec routes protégées (ex. liste des utilisateurs).
- Isolation des sauvegardes par utilisateur authentifié.
- Secret JWT et clé OpenAI **hors du dépôt** (variables d'environnement `.env`).

## 8. Livrables (correspondance activités)

| Activité | Livrable | Emplacement |
|---|---|---|
| 1, 4 | Doc de cadrage + README + doc technique | ce document, `README.md`, `docs/module/DOC_TECHNIQUE.md` |
| 2 | MCD / MLD | `docs/module/MCD_MLD.md` |
| 3, 5 | API REST sécurisée JWT | `backend/api.py`, `backend/auth.py` |
| 4, 6 | Wireframes + frontend fonctionnel | `docs/module/WIREFRAMES.md`, `frontend/` |
| 6, 7 | Flux clefs + améliorations | `frontend/src/api.js`, `frontend/src/hooks/useSSEChat.js`, `docs/module/SPRINT_FINALISATION.md` |
| 8 | Audit et optimisations | `docs/module/AUDIT_OPTIMISATION.md` |
| 9 | Sprint de finalisation + playtest | `docs/module/SPRINT_FINALISATION.md` |
| 10 | Analyse critique | `docs/module/ANALYSE_CRITIQUE.md` |
| 1-10 | Checklist de conformité complète | `docs/module/ACTIVITES_1_A_10_CHECKLIST.md` |
| — | Fonctionnalité IA | `backend/api.py` (`_gm_stream`) |

## 9. Critères de réussite

- Un utilisateur peut s'inscrire, se connecter, jouer une partie et se déconnecter.
- Les routes de jeu refusent l'accès sans JWT valide (401).
- La narration IA fonctionne et se voit en streaming.
- Les données de partie sont persistées et isolées par compte.
