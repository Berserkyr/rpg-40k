# MCD / MLD — Modèle de données

**Projet :** RPG 40K Survivor
**SGBD :** SQLite (`data/rpg40k.sqlite3`)

Ce document décrit le modèle conceptuel (MCD) et le modèle logique (MLD) des données
persistées en base relationnelle. Les données de partie détaillées (inventaire, carte,
quêtes) sont sérialisées en fichiers YAML par utilisateur ; la base relationnelle gère
les **comptes**, les **rôles** et les **traces de session**.

---

## 1. Modèle Conceptuel de Données (MCD)

Entités et relation principale :

```
┌────────────────────────┐               ┌────────────────────────┐
│        UTILISATEUR      │               │     EVENEMENT_SESSION   │
├────────────────────────┤   1      0,n   ├────────────────────────┤
│ # id                   │───────────────<│ # id                   │
│   nom_affiche          │  génère        │   type_evenement       │
│   mot_de_passe_hache   │                │   detail               │
│   role                 │                │   date_creation        │
│   date_creation        │                │                        │
│   date_derniere_visite │                │                        │
└────────────────────────┘               └────────────────────────┘
```

**Règles de gestion :**
- Un **utilisateur** possède un identifiant unique (login normalisé).
- Un utilisateur a exactement **un rôle** (`player` ou `admin`).
- Un utilisateur peut générer **zéro ou plusieurs événements** de session.
- Un événement de session appartient à **un seul** utilisateur.
- Le mot de passe n'est jamais stocké en clair : seul son **hash bcrypt** est conservé.

## 2. Modèle Logique de Données (MLD)

Notation relationnelle (clé primaire soulignée `#`, clé étrangère `→`) :

```
UTILISATEUR (#id, nom_affiche, mot_de_passe_hache, role, date_creation, date_derniere_visite)

EVENEMENT_SESSION (#id, user_id → UTILISATEUR.id, type_evenement, detail, date_creation)
```

## 3. Schéma physique SQLite (DDL réel)

```sql
CREATE TABLE users (
    id            TEXT PRIMARY KEY,          -- login normalisé (unique)
    display_name  TEXT NOT NULL,             -- nom affiché
    password_hash TEXT,                      -- hash bcrypt ($2b$...)
    role          TEXT NOT NULL DEFAULT 'player', -- 'player' | 'admin'
    created_at    TEXT NOT NULL,             -- horodatage ISO-8601 UTC
    last_seen_at  TEXT NOT NULL
);

CREATE TABLE session_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     TEXT NOT NULL,
    event_type  TEXT NOT NULL,               -- 'register' | 'login' | ...
    detail      TEXT,
    created_at  TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 4. Dictionnaire de données

### Table `users`

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | TEXT | PK | Identifiant de connexion normalisé |
| display_name | TEXT | NOT NULL | Nom affiché dans l'interface |
| password_hash | TEXT | — | Hash bcrypt du mot de passe |
| role | TEXT | NOT NULL, défaut `player` | Rôle applicatif |
| created_at | TEXT | NOT NULL | Date de création (UTC ISO-8601) |
| last_seen_at | TEXT | NOT NULL | Dernière connexion |

### Table `session_events`

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | INTEGER | PK, auto-incrément | Identifiant technique |
| user_id | TEXT | FK → users.id | Utilisateur concerné |
| event_type | TEXT | NOT NULL | Type d'événement |
| detail | TEXT | — | Détail optionnel |
| created_at | TEXT | NOT NULL | Horodatage de l'événement |

## 5. Normalisation

Le modèle respecte la **3e forme normale (3FN)** :
- **1FN** : chaque attribut est atomique (pas de liste dans une colonne).
- **2FN** : toutes les colonnes dépendent de la clé primaire complète.
- **3FN** : aucune dépendance transitive (le rôle et le hash dépendent
  directement de l'utilisateur, pas d'un autre attribut non-clé).

## 6. Fidélité MLD / implémentation

Le MLD est fidèlement traduit dans le code :
- création et migration du schéma : [backend/database.py](../../backend/database.py) (`init_db`) ;
- accès aux comptes : `create_account`, `get_account`, `list_users` ;
- traces de session : `record_event`.
