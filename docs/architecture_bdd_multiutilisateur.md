# Architecture BDD et multi-utilisateur

## Objectif

Répondre au besoin de persistance structurée et préparer le projet à plusieurs joueurs.

## Choix technique

| Élément | Choix |
|---|---|
| Base de données | SQLite |
| Fichier local | `data/rpg40k.sqlite3` |
| Couche backend | [backend/database.py](../backend/database.py) |
| Isolation utilisateur | En-tête HTTP `X-User-Id` |
| Sauvegardes de partie | YAML isolé par utilisateur |

SQLite est adapté au prototype : simple, local, démontrable, sans serveur externe. Pour une version cloud, l’évolution recommandée est PostgreSQL.

## Schéma actuel

### Table `users`

| Champ | Type | Rôle |
|---|---|---|
| `id` | TEXT PRIMARY KEY | Identifiant normalisé du joueur |
| `display_name` | TEXT | Nom affichable |
| `created_at` | TEXT | Date de création UTC |
| `last_seen_at` | TEXT | Dernière activité UTC |

### Table `session_events`

| Champ | Type | Rôle |
|---|---|---|
| `id` | INTEGER PRIMARY KEY | Identifiant technique |
| `user_id` | TEXT | Joueur concerné |
| `event_type` | TEXT | Type d’événement |
| `detail` | TEXT | Détail optionnel |
| `created_at` | TEXT | Date UTC |

## API multi-utilisateur

| Endpoint | Rôle |
|---|---|
| `GET /api/health` | Vérifie l’API et expose le chemin SQLite |
| `GET /api/users` | Liste les utilisateurs connus |
| `POST /api/users` | Crée ou met à jour un utilisateur |
| `GET /api/state` | Charge l’état du joueur courant |

Les actions de jeu lisent l’utilisateur courant via :

```http
X-User-Id: nom-du-joueur
```

Sans cet en-tête, l’utilisateur `default` est utilisé.

## Isolation des sauvegardes

| Utilisateur | Dossier |
|---|---|
| `default` | `saves/campagne1/` |
| autre joueur | `saves/users/{user_id}/campagne1/` |

Cette approche permet de démontrer le multi-utilisateur sans casser la sauvegarde existante.

## Limites connues

- Pas encore d’authentification par mot de passe.
- Les sauvegardes détaillées restent en YAML.
- La BDD stocke les utilisateurs et prépare l’audit, mais pas encore tout l’état du jeu.

## Évolutions recommandées

1. Ajouter une vraie authentification.
2. Migrer les sauvegardes YAML vers tables relationnelles.
3. Passer de SQLite à PostgreSQL pour un déploiement public.
4. Ajouter des migrations avec Alembic ou SQLModel.
