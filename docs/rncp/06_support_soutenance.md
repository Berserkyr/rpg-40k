# Support de soutenance — trame orale

## 1. Introduction

Bonjour, je présente **Survivant de Ruche**, une application web full-stack de simulation narrative interactive. Le projet prend la forme d’un RPG solo jouable dans un navigateur, mais son intérêt principal est technique : il combine un backend FastAPI, un frontend React, une logique métier modulaire, une persistance locale et un système de narration en streaming.

## 2. Problématique

Le besoin initial était de transformer une expérience de jeu textuelle en terminal en une application web complète, manipulable par un utilisateur sans connaissance technique.

Contraintes :

- interface navigateur ;
- logique métier riche ;
- sauvegarde de l’état ;
- possibilité d’utiliser une IA ;
- fonctionnement dégradé sans IA ;
- projet démontrable localement.

## 3. Architecture

L’architecture est séparée en trois couches :

1. **Frontend React** : interface utilisateur, panneaux de jeu, actions.
2. **Backend FastAPI** : endpoints REST et flux SSE.
3. **Domaine métier Python** : combat, inventaire, progression, carte, quêtes, relations, persistance.

Cette séparation permet de faire évoluer l’interface sans modifier le cœur métier.

## 4. Démonstration

Parcours proposé :

1. Lancer `start_game.bat`.
2. Ouvrir l’interface web.
3. Initialiser la connexion.
4. Montrer la narration en streaming.
5. Lancer un jet 2D6.
6. Fouiller une zone.
7. Déclencher une rencontre.
8. Effectuer une action de combat.
9. Se déplacer.
10. Sauvegarder.

## 5. Choix techniques

| Choix | Justification |
|---|---|
| FastAPI | API moderne, rapide, compatible Pydantic |
| React | Composants UI maintenables |
| Vite | Démarrage et build rapides |
| YAML | Sauvegarde lisible pour prototype |
| SSE | Streaming simple de texte MJ |
| Pytest | Tests unitaires Python standards |

## 6. Difficultés rencontrées

- Mauvais scaffold Vite initial : projet vanilla TypeScript au lieu de React.
- Conflits de ports locaux.
- Sérialisation/désérialisation de l’inventaire.
- Compatibilité du streaming OpenAI.

## 7. Corrections apportées

- Installation React et plugin Vite.
- Ajout de `main.jsx` et correction `index.html`.
- Scripts de lancement.
- Fallback MJ local.
- Reconstruction d’objets inventaire depuis YAML.
- Ajout de panneaux action, combat, inventaire.

## 8. Qualité et maintenance

- Tests backend existants.
- Build frontend vérifié.
- Documentation RNCP créée.
- Plan de recette formalisé.
- Journal de version et processus anomalies définis.

## 9. Limites

- Pas encore de déploiement cloud.
- Couverture de tests à augmenter.
- Pas encore d’authentification multi-utilisateur.
- Supervision production à brancher.
- Audit RGAA/OWASP à approfondir.

## 10. Conclusion

Le projet répond au besoin d’un prototype logiciel full-stack fonctionnel, maintenable et démontrable. Il constitue une base pertinente pour illustrer les compétences de cadrage, conception, développement, pilotage et maintenance attendues dans la grille RNCP Expert en développement logiciel.
