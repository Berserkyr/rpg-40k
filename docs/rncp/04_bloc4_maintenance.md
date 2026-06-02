# Bloc 4 — Maintenir l’application logicielle en condition opérationnelle

## 1. Processus de mise à jour des dépendances

### Périmètre

- Backend Python : `requirements.txt`.
- Frontend Node : `frontend/package.json` et `frontend/package-lock.json`.
- Runtime local : Python, Node.js.

### Fréquence recommandée

| Type | Fréquence |
|---|---|
| Correctifs sécurité critiques | Dès publication |
| Dépendances mineures | Mensuelle |
| Versions majeures | Après analyse d’impact |
| Audit global | Avant chaque version livrable |

### Procédure

1. Lister les versions installées.
2. Consulter changelogs et alertes sécurité.
3. Mettre à jour sur branche dédiée.
4. Lancer tests backend : `pytest`.
5. Lancer build frontend : `npm run build`.
6. Tester parcours de recette.
7. Documenter la mise à jour dans le journal de version.

## 2. Supervision et alertes

### Indicateurs backend

| Indicateur | Méthode actuelle | Évolution recommandée |
|---|---|---|
| Disponibilité API | Appel `/api/state` | Healthcheck `/api/health` |
| Erreurs serveur | Logs Uvicorn | Logs structurés JSON |
| Temps de réponse | Mesure manuelle | Middleware métriques |
| Erreurs OpenAI | Fallback local | Compteur d’erreurs fournisseur |
| Sauvegardes | Présence fichiers YAML | Vérification intégrité périodique |

### Indicateurs frontend

| Indicateur | Méthode |
|---|---|
| Build réussi | `npm run build` |
| Erreurs JS | Console navigateur |
| Fluidité UI | Test manuel |
| Accessibilité | Audit Lighthouse / axe |

## 3. Processus de collecte des anomalies

### Informations à collecter

- Identifiant anomalie.
- Date de détection.
- Version concernée.
- Environnement.
- Étapes de reproduction.
- Résultat obtenu.
- Résultat attendu.
- Gravité.
- Cause probable.
- Correctif appliqué.
- Test de non-régression.

## 4. Exemple de fiche anomalie

| Champ | Valeur |
|---|---|
| ID | BUG-001 |
| Titre | Page Vite affichée au lieu du jeu |
| Gravité | Majeure |
| Version | Prototype web initial |
| Environnement | Windows, Vite local |
| Reproduction | Lancer frontend et ouvrir `localhost:5173` |
| Résultat obtenu | Page `Get Started` Vite |
| Résultat attendu | Interface Survivant de Ruche |
| Cause | Projet Vite vanilla TypeScript, `main.ts` utilisé |
| Correctif | Installation React, `main.jsx`, `vite.config.js`, correction `index.html` |
| Non-régression | `npm run build`, ouverture navigateur |

## 5. Plan de correction des bugs

| Priorité | Type d’anomalie | Délai cible |
|---|---|---:|
| P1 | Application inutilisable | Immédiat |
| P2 | Fonction majeure cassée | 1 à 2 jours |
| P3 | Défaut UI ou confort | Itération suivante |
| P4 | Amélioration | Backlog |

Processus :

1. Reproduire.
2. Isoler le composant.
3. Corriger avec modification minimale.
4. Ajouter ou mettre à jour un test si possible.
5. Vérifier build et recette.
6. Documenter dans le journal de version.

## 6. Journal de version

| Version | Date | Contenu |
|---|---|---|
| 0.1 | Initial | CLI RPG avec prompt, dés, état personnage |
| 0.2 | Domaine métier | Combat, inventaire, progression, monde, quêtes, relations |
| 0.3 | Persistance | Sauvegarde monde et campagne |
| 0.4 | API | FastAPI, endpoints REST, SSE |
| 0.5 | Frontend | React, terminal grimdark, panneaux jeu |
| 0.6 | Stabilisation | Correction Vite, CORS, scripts lancement |
| 0.7 | Jouabilité | Actions, combat UI, inventaire UI, fallback MJ local |
| 0.8 | Dossier RNCP | Documentation cadrage, conception, pilotage, maintenance |

## 7. Recommandations d’amélioration

| Amélioration | Gain | Effort |
|---|---|---:|
| Tests API complets | Réduction régressions | Moyen |
| Tests frontend | Fiabilité UI | Moyen |
| CI GitHub Actions | Qualité continue | Faible |
| Healthcheck backend | Supervision simple | Faible |
| Export/import sauvegarde | Sécurité données | Moyen |
| Déploiement cloud | Démo accessible | Moyen |
| Authentification | Multi-utilisateur | Fort |
| Base de données | Scalabilité | Moyen |
| Audit RGAA | Accessibilité | Moyen |
| Audit sécurité | Réduction risques | Moyen |

## 8. Collaboration support — exemple

### Contexte

Un utilisateur indique : « quand j’ouvre le navigateur, je vois la page Vite et pas le jeu ».

### Diagnostic

- Vérification du port frontend.
- Inspection de `index.html`.
- Vérification du fichier d’entrée Vite.
- Confirmation que React n’était pas monté.

### Résolution

- Ajout du plugin React.
- Création de `main.jsx`.
- Correction du point de montage `#root`.
- Rebuild et relance frontend.

### Contribution des parties

| Partie | Contribution |
|---|---|
| Utilisateur | Remontée avec capture écran |
| Support | Reproduction et qualification |
| Développeur | Correction config Vite/React |
| QA | Vérification build et affichage |

## 9. Critères de maintien en condition opérationnelle

L’application est considérée opérationnelle si :

- `GET /api/state` répond avec un état valide.
- Le frontend s’ouvre sur l’écran du jeu.
- La scène d’ouverture démarre.
- Une action de jeu peut être effectuée.
- La sauvegarde ne génère pas d’erreur.
- Le build frontend réussit.
- Les tests backend existants passent.
