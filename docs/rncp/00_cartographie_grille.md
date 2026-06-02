# Cartographie du projet avec la grille RNCP 39583

Projet : **Survivant de Ruche — RPG narratif web full-stack**

Objectif de ce dossier : relier le projet aux livrables attendus de la grille *Expert en développement logiciel*.

## Synthèse de couverture

| Bloc | Niveau de couverture après constitution du dossier | Éléments produits |
|---|---:|---|
| Bloc 1 — Cadrer un projet de développement logiciel | Bon | cadrage, parties prenantes, SWOT, risques, architecture, charge, budget |
| Bloc 2 — Concevoir et développer des applications logicielles | Très bon | prototype full-stack, API, frontend, tests, cahier de recette, sécurité, accessibilité |
| Bloc 3 — Coordonner et piloter un projet | Correct | méthode, planning, suivi, arbitrage, démonstration |
| Bloc 4 — Maintenir l’application en condition opérationnelle | Correct | maintenance, supervision, anomalies, journal de version, axes d’amélioration |

## Preuves techniques dans le dépôt

| Preuve | Emplacement |
|---|---|
| Backend API FastAPI | [backend/api.py](../../backend/api.py) |
| Frontend React | [frontend/src/App.jsx](../../frontend/src/App.jsx) |
| Client API et SSE | [frontend/src/api.js](../../frontend/src/api.js) |
| Logique métier combat | [src/combat.py](../../src/combat.py) |
| Inventaire et équipement | [src/inventory.py](../../src/inventory.py) |
| Monde et exploration | [src/world.py](../../src/world.py) |
| Quêtes | [src/quests.py](../../src/quests.py) |
| Relations/factions | [src/relationships.py](../../src/relationships.py) |
| Persistance | [src/persistence.py](../../src/persistence.py) |
| Tests unitaires | [tests](../../tests) |
| Lancement global | [start_game.bat](../../start_game.bat) |

## Angle de présentation recommandé

Ne pas présenter le projet seulement comme un jeu. Le présenter comme :

> Une application web full-stack de simulation narrative interactive, combinant une API Python/FastAPI, un frontend React, une logique métier modulaire, une persistance de données, des tests automatisés et une architecture évolutive.

## Points forts pour le jury

- Architecture modulaire séparant API, domaine métier, persistance et interface.
- Application manipulable par un utilisateur en autonomie.
- Interface web complète avec actions jouables.
- Mode dégradé local si l’API OpenAI n’est pas disponible.
- Sauvegarde et reprise de partie.
- Système de tests existant et extensible.

## Points à présenter honnêtement comme axes d’amélioration

- Couverture de tests à renforcer sur le frontend et les endpoints API.
- CI/CD à finaliser avec déploiement automatique.
- Supervision production non encore connectée à un outil réel.
- Accessibilité à valider avec audit RGAA complet.
- Sécurité à auditer avec outils spécialisés avant production publique.
