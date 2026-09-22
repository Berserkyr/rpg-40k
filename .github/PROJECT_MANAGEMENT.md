# Organisation GitHub — RPG 40K

Ce document est la référence opérationnelle du pilotage dans GitHub.

## 1) Flux de travail

- Une **issue** = un objectif livrable, testable, avec critères d’acceptation.
- Toute issue doit avoir au minimum :
  - un type (`type:*`),
  - une priorité (`prio:*`),
  - un domaine (`domain:*`),
  - un jalon (`milestone`).
- Une **pull request** doit référencer l’issue (`Closes #123`) et inclure les preuves (tests / captures / logs).
- La clôture d’une issue nécessite : code + preuve + documentation impactée.

## 2) Jalons (milestones)

Les jalons structurent le flux en lots pilotables et sauvegardables.

1. **M1 - Stabilisation API et sécurité**
   - Auth JWT, robustesse API, couverture des cas d’erreur, supervision backend.
2. **M2 - Gameplay et persistance**
   - Combat, progression, quêtes, monde persistant, cohérence des saves.
3. **M3 - Frontend UX et narration**
   - UI/UX, SSE chat, moteur d’animation côté frontend, lisibilité de l’interface.
4. **M4 - Livraison et exploitation**
   - Docker, CI/CD, monitoring, scripts d’exploitation, rollback.
5. **M5 - Documentation et soutenance RNCP**
   - Dossiers Bloc 1/3/4, cohérence documentaire, supports, preuves.

## 3) Labels standards

### Type
- `type:feature`
- `type:bug`
- `type:refactor`
- `type:docs`
- `type:chore`
- `type:test`

### Priorité
- `prio:P0` (bloquant)
- `prio:P1` (haut)
- `prio:P2` (normal)
- `prio:P3` (faible)

### Domaine
- `domain:backend`
- `domain:frontend`
- `domain:infra`
- `domain:docs`
- `domain:tests`

### Statut
- `status:ready`
- `status:in-progress`
- `status:blocked`
- `status:review`
- `status:done`

## 4) Rythme recommandé (solo)

- Limite WIP: **1 tâche principale active**.
- Revue hebdo:
  - fermer ce qui est “done” avec preuve,
  - re-prioriser le backlog,
  - déplacer ce qui bloque en `status:blocked` + cause.

## 5) Convention de commits par catégorie

- `feat(...)`
- `fix(...)`
- `refactor(...)`
- `test(...)`
- `docs(...)`
- `chore(...)`
- `style(python): ...` (si harmonisation uniquement)

Objectif: garder des commits atomiques pour faciliter les retours arrière par catégorie.
