# Checklist jury — éléments à préparer

## Avant la soutenance

- [ ] Lancer `pytest`.
- [ ] Lancer `npm run build` dans `frontend`.
- [ ] Tester [start_game.bat](../../start_game.bat).
- [ ] Vérifier que `http://localhost:5173` affiche le jeu.
- [ ] Vérifier que `http://127.0.0.1:8000/api/state` répond.
- [ ] Préparer une capture écran de l’architecture.
- [ ] Préparer une capture du frontend.
- [ ] Préparer une capture d’un combat.
- [ ] Préparer une capture du dossier de code.
- [ ] Ne pas afficher de clé API.

## Documents à fournir

- [ ] [00_cartographie_grille.md](00_cartographie_grille.md)
- [ ] [01_bloc1_cadrage.md](01_bloc1_cadrage.md)
- [ ] [02_bloc2_conception_developpement.md](02_bloc2_conception_developpement.md)
- [ ] [03_bloc3_pilotage.md](03_bloc3_pilotage.md)
- [ ] [04_bloc4_maintenance.md](04_bloc4_maintenance.md)
- [ ] [05_plan_de_recette.md](05_plan_de_recette.md)
- [ ] [06_support_soutenance.md](06_support_soutenance.md)

## Points de langage

À dire :

- « J’ai construit une application full-stack. »
- « Le jeu est le contexte métier ; le livrable est une application logicielle. »
- « L’architecture est séparée entre interface, API et domaine métier. »
- « J’ai prévu un mode dégradé si le fournisseur IA est indisponible. »
- « Les axes d’amélioration sont identifiés et priorisés. »

À éviter :

- « C’est juste un petit jeu. »
- « Je n’ai pas besoin de tests. »
- « La sécurité n’est pas importante car c’est local. »
- « La documentation n’est pas nécessaire. »

## Démo minimale si problème technique

Si OpenAI ne fonctionne pas : utiliser le mode MJ local.

Si le frontend ne démarre pas : montrer le build et l’API.

Si le navigateur bug : montrer :

- [backend/api.py](../../backend/api.py)
- [frontend/src/App.jsx](../../frontend/src/App.jsx)
- [src/world.py](../../src/world.py)
- [src/combat.py](../../src/combat.py)
- [docs/rncp](.)
