# Bloc 2 — Grille officielle : attendus, ordre des livrables et écarts projet

**Certification :** Expert en Développement Logiciel — RNCP 39583
**Bloc évalué :** Bloc 2 — Concevoir et développer des applications logicielles
**Projet support :** RPG 40K Survivor (« Survivant de Ruche »)
**Source :** grille d'évaluation officielle (feuille *Grille Eval Bloc 2*)

Ce document reprend **fidèlement** chaque compétence de la grille (C2.1.1 → C2.4.1),
dans l'ordre, avec :
1. le **livrable attendu** (colonne « Livrable attendu ») ;
2. les **critères d'évaluation** (colonne « Critères d'évaluation ») ;
3. ce que **notre projet fournit déjà** ;
4. ce qui **manque encore** pour sécuriser le critère (« Acquis »).

---

## Vue d'ensemble (ordre de la grille)

| # | Compétence | Livrable attendu | Statut projet |
|---|---|---|---|
| C2.1.1 | Environnements de déploiement et de test + suivi qualité/perf | Protocole de déploiement continu + critères qualité/perf | 🟢 Solide |
| C2.1.2 | Intégration continue (CI) | Protocole d'intégration continue | 🟢 Solide |
| C2.2.1 | Prototype applicatif (ergonomie, cibles, sécurité) | Architecture maintenable + prototype + frameworks | 🟢 Solide |
| C2.2.2 | Harnais de tests unitaires | Jeu de tests couvrant une fonctionnalité | 🟢 Solide |
| C2.2.3 | Sécurité (OWASP) + accessibilité | Mesures sécurité + mesures accessibilité | 🟢 Solide |
| C2.2.4 | Déploiement progressif à chaque modification | Historique des versions + version finale viable | 🟢 Solide |
| C2.3.1 | Cahier de recettes | Cahier de recettes | 🟢 Solide |
| C2.3.2 | Plan de correction des bogues | Plan de correction des bogues | 🟢 Solide |
| C2.4.1 | Documentation technique d'exploitation | Manuels déploiement / utilisation / mise à jour | 🟢 Solide |

Légende : 🟢 preuve claire et suffisante · 🟡 preuve présente mais à renforcer · 🔴 manquant.

---

## C2.1.1 — Environnements de déploiement et de test

**Compétence.** Mettre en œuvre des environnements de déploiement et de test en y
intégrant les outils de suivi de performance et de qualité, afin de permettre le bon
déroulement de la phase de développement du logiciel.

**Livrable attendu.**
- Le protocole de déploiement continu.
- Les critères de qualité et de performance.

**Critères d'évaluation.**
- Le protocole de déploiement continu est explicité.
- L'environnement de développement est détaillé (éditeur de code, compilateur, etc.).
- Les outils mobilisés permettent d'identifier les composants : compilateur, serveur
  d'application, outils de gestion de sources.
- Le protocole permet de définir les différentes séquences de déploiement.
- Les critères de qualité et de performance répondent aux exigences du projet.

**Ce que le projet fournit déjà.**
- Protocole de déploiement continu + critères qualité/performance : [docs/rncp/PROTOCOLE_DEPLOIEMENT_CONTINU_QUALITE_PERF.md](PROTOCOLE_DEPLOIEMENT_CONTINU_QUALITE_PERF.md).
- Environnement de dev décrit : [docs/module/DOC_TECHNIQUE.md](DOC_TECHNIQUE.md) (stack, versions, lancement).
- Déploiement Docker Compose + VPS : [docs/deploiement_vps.md](../deploiement_vps.md).
- Healthcheck `/api/health` et supervision : [docs/module/DOC_TECHNIQUE.md](DOC_TECHNIQUE.md) (section observabilité).
- Gestion de sources Git + workflows : [.github/workflows/ci.yml](../../.github/workflows/ci.yml).

**Ce qui manque pour valider.**
- [x] Formaliser un **protocole de déploiement en séquences numérotées** (build → test → image → déploiement → vérification santé), en un seul endroit lisible.
- [x] Lister explicitement les **critères de qualité/performance mesurés** (healthcheck, tests, build, bundle, disponibilité) avec valeurs cibles.

---

## C2.1.2 — Intégration continue (CI)

**Compétence.** Configurer le système d'intégration continue dans le cycle de
développement en fusionnant les codes sources et en testant régulièrement les blocs
de code, afin d'assurer un développement efficient réduisant les risques de régression.

**Livrable attendu.**
- Le protocole d'intégration continue.

**Critères d'évaluation.**
- Le protocole d'intégration continue est explicité clairement.
- Il permet de définir les séquences d'intégration.

**Ce que le projet fournit déjà.**
- Pipeline GitHub Actions opérationnelle : [.github/workflows/ci.yml](../../.github/workflows/ci.yml) (tests backend, build frontend, E2E).
- CI GitLab prête : [.gitlab-ci.yml](../../.gitlab-ci.yml).
- Documentation CI : [docs/gestion_projet/strategie_git.md](../gestion_projet/strategie_git.md), [docs/rncp/BLOC2_DOSSIER_FINAL.md](BLOC2_DOSSIER_FINAL.md) (section pipeline).

**Ce qui manque pour valider.**
- [ ] Ajouter une **capture d'écran d'un run CI vert** (preuve visuelle attendue par le jury).
- [ ] Décrire les **séquences d'intégration** sous forme d'étapes (déclencheur push/PR → jobs → conditions de succès) en une phrase par étape.

---

## C2.2.1 — Prototype de l'application logicielle

**Compétence.** Concevoir un prototype en tenant compte des spécificités ergonomiques
et des équipements ciblés (web, mobile…), afin de répondre aux fonctionnalités
attendues et aux exigences de sécurité.

**Livrable attendu.**
- Une architecture logicielle structurée permettant la maintenabilité.
- Une présentation d'un des prototypes réalisés.
- L'utilisation de frameworks et de paradigmes de développement.

**Critères d'évaluation.**
- Les bonnes pratiques de développement sont respectées (frameworks, paradigmes…).
- Le prototype est fonctionnel et répond aux besoins identifiés.
- Le prototype met en œuvre un ensemble cohérent de fonctionnalités principales + user stories.
- Les composants d'interface sont présents et fonctionnels (fenêtres, boutons, menus…).
- Le prototype satisfait aux exigences de sécurité.

**Ce que le projet fournit déjà.**
- Architecture en couches : [docs/module/DOC_TECHNIQUE.md](DOC_TECHNIQUE.md) (présentation / API / domaine).
- Prototype fonctionnel jouable en ligne : `http://89.116.111.166:8081/`.
- Frameworks : React 18 + Vite (front), FastAPI (back) — [docs/module/DOCUMENT_CADRAGE.md](DOCUMENT_CADRAGE.md).
- Composants UI : [docs/module/WIREFRAMES.md](WIREFRAMES.md) + composants React.
- Sécurité intégrée : JWT + bcrypt — [backend/auth.py](../../backend/auth.py).
- **User stories formalisées** (US-01 à US-08) avec critères d'acceptation et preuves : [docs/rncp/USER_STORIES.md](USER_STORIES.md).

**Ce qui manque pour valider.**
- [x] Formaliser 3 à 5 **user stories** explicites (« En tant que joueur, je veux… afin de… ») — fait dans [docs/rncp/USER_STORIES.md](USER_STORIES.md).
- [ ] Ajouter **captures d'écran** des écrans clés (auth, jeu, combat) en annexe.

---

## C2.2.2 — Harnais de tests unitaires

**Compétence.** Développer un harnais de test unitaire en tenant compte des
fonctionnalités demandées, afin de prévenir les régressions et de s'assurer du bon
fonctionnement du logiciel.

**Livrable attendu.**
- Un jeu de tests unitaires couvrant une fonctionnalité demandée.

**Critères d'évaluation.**
- Les tests unitaires couvrent la **majorité du code** développé.

**Ce que le projet fournit déjà.**
- Livrable dédié C2.2.2 : [docs/rncp/HARNAIS_TESTS_UNITAIRES.md](HARNAIS_TESTS_UNITAIRES.md).
- Tests backend (39) : [tests/test_api.py](../../tests/test_api.py), [tests/test_inventory.py](../../tests/test_inventory.py), [tests/test_progression.py](../../tests/test_progression.py), [tests/test_world.py](../../tests/test_world.py), [tests/test_quests.py](../../tests/test_quests.py).
- Tests frontend (13) : [frontend/src/__tests__/](../../frontend/src/__tests__).
- Tests E2E Playwright : [frontend/e2e/game.spec.js](../../frontend/e2e/game.spec.js).

**Ce qui manque pour valider.**
- [x] Produire une **mesure de couverture chiffrée** (`pytest --cov` + `vitest --coverage`) et l'inscrire dans le dossier.
- [x] Documenter le **pourcentage global** et la méthode de calcul dans le livrable dédié.

---

## C2.2.3 — Sécurité (OWASP) et accessibilité

**Compétence.** Développer le logiciel en veillant à l'évolutivité et à la
sécurisation du code source, aux exigences d'accessibilité et aux spécifications
techniques et fonctionnelles.

**Livrable attendu.**
- Une présentation des mesures de sécurité mises en œuvre.
- Une présentation des actions pour l'accès aux personnes en situation de handicap.

**Critères d'évaluation.**
- Les mesures couvrent les **10 failles principales OWASP**.
- Le référentiel d'accessibilité choisi est présenté et justifié (RGAA, OPQUAST…).
- Le prototype répond aux exigences du référentiel d'accessibilité établi.

**Ce que le projet fournit déjà.**
- Livrable dédié C2.2.3 : [docs/rncp/MESURES_SECURITE_ACCESSIBILITE.md](MESURES_SECURITE_ACCESSIBILITE.md).
- Mesures de sécurité : JWT, bcrypt, rôles, routes protégées — [backend/auth.py](../../backend/auth.py).
- CORS restreignable via `CORS_ALLOWED_ORIGINS` et audit `pip-audit`/`npm audit` en CI — [backend/api.py](../../backend/api.py), [.github/workflows/ci.yml](../../.github/workflows/ci.yml).
- Accessibilité : labels ARIA, groupes sémantiques, navigation clavier, messages d'erreur accessibles, option « effets réduits » + `prefers-reduced-motion` — [frontend/src/components](../../frontend/src/components), [frontend/src/App.jsx](../../frontend/src/App.jsx).

**Ce qui manque pour valider.**
- [x] Tableau **OWASP Top 10 (2021)** complété avec statut, mesure et preuve.
- [x] Référentiel d'accessibilité **RGAA** choisi et justifié.
- [x] Mini-audit d'accessibilité manuel formalisé avec forces, écarts et actions d'amélioration.
- [x] Mesures renforcées **implémentées** : CORS restreignable (A05), audit dépendances CI (A06), option d'accessibilité (réduction d'effets).

---

## C2.2.4 — Déploiement progressif à chaque modification

**Compétence.** Déployer le logiciel à chaque modification de code et de façon
progressive en vérifiant la performance fonctionnelle et technique, afin de présenter
une solution stable et conforme à l'attendu.

**Livrable attendu.**
- L'historique des différentes versions.
- La dernière version du logiciel fonctionnel, fiable et viable.

**Critères d'évaluation.**
- Un système de gestion de versions est utilisé.
- Les évolutions du prototype sont tracées.
- Le logiciel est fonctionnel et manipulable en autonomie par un utilisateur.

**Ce que le projet fournit déjà.**
- Git + GitHub (historique de commits) : `https://github.com/Berserkyr/rpg-40k`.
- Workflow de déploiement VPS : [.github/workflows/deploy-vps.yml](../../.github/workflows/deploy-vps.yml).
- **Déploiement continu automatique** : push sur `main` → CI verte → déploiement VPS auto (`workflow_run`).
- Application en ligne autonome : `http://89.116.111.166:8081/`.

**Ce qui manque pour valider.**
- [x] Déploiement automatique à chaque modification validée par la CI (fait).
- [x] Ajouter un **historique de versions lisible** — [CHANGELOG.md](../../CHANGELOG.md) (versions 1.0.0-rncp → 1.2.0 + preuves).
- [ ] Capturer la **dernière version fonctionnelle** (écran de jeu opérationnel) comme preuve de viabilité.

---

## C2.3.1 — Cahier de recettes

**Compétence.** Élaborer le cahier de recettes en rédigeant les scénarios de tests et
les résultats attendus, afin de détecter les anomalies et régressions.

**Livrable attendu.**
- Le cahier de recettes.

**Critères d'évaluation.**
- Le cahier de recettes reprend l'ensemble des fonctionnalités attendues.
- Les tests fonctionnels, structurels et de sécurité exécutés sont conformes au plan.

**Ce que le projet fournit déjà.**
- Cahier de recettes complet et exécuté : [docs/rncp/05_plan_de_recette.md](05_plan_de_recette.md) (fonctionnel / structurel / sécurité, format ID / scénario / étapes / attendu / obtenu / statut).
- Cahier de recette dans le dossier : [docs/rncp/02_bloc2_conception_developpement.md](02_bloc2_conception_developpement.md) (section cahier de recette).

**Ce qui manque pour valider.**
- [x] Structurer le cahier en **tableau ID / scénario / étapes / résultat attendu / résultat obtenu / statut**, couvrant les 3 natures **fonctionnel, structurel, sécurité** — fait.
- [x] Tracer au moins un **cas de test de sécurité** (route protégée sans JWT → 401) — cas REC-SEC-001 à 008, adossés à [tests/test_api.py](../../tests/test_api.py).

---

## C2.3.2 — Plan de correction des bogues

**Compétence.** Élaborer un plan de correction des bogues à partir de l'analyse des
anomalies et régressions détectées en recette, afin de garantir le fonctionnement
conforme à l'attendu.

**Livrable attendu.**
- Le plan de correction des bogues.

**Critères d'évaluation.**
- Les bogues de code sont détectés, qualifiés et traités.
- Une analyse des points d'amélioration est réalisée pour chaque test en échec.
- Les corrections et améliorations sont conformes à l'attendu et garantissent le bon fonctionnement.

**Ce que le projet fournit déjà.**
- Plan de correction des bogues dédié : [docs/rncp/PLAN_CORRECTION_BOGUES.md](PLAN_CORRECTION_BOGUES.md).
- Plan de correction des bugs : [docs/rncp/04_bloc4_maintenance.md](04_bloc4_maintenance.md) (section plan de correction).
- Anomalies traitées documentées : [docs/rncp/BLOC2_DOSSIER_FINAL.md](BLOC2_DOSSIER_FINAL.md) (tableau des corrections CI/import, fallback IA…).

**Ce qui manque pour valider.**
- [x] Créer un **registre d'anomalies** dédié : ID / description / criticité / cause / correction / statut / preuve.
- [x] Relier chaque correction à un **test devenu vert**, une validation CI/CD ou une preuve d'exploitation.

---

## C2.4.1 — Documentation technique d'exploitation

**Compétence.** Rédiger la documentation technique d'exploitation détaillant le
fonctionnement du logiciel, afin d'assurer une traçabilité pour le suivi des équipes
et des évolutions futures.

**Livrable attendu.**
- Le manuel de déploiement.
- Le manuel d'utilisation.
- Le manuel de mise à jour.

**Critères d'évaluation.**
- Les manuels sont rédigés avec clarté.
- La documentation décrit les choix opérés (technologies, langages, etc.).

**Ce que le projet fournit déjà.**
- Manuel de déploiement : [docs/deploiement_vps.md](../deploiement_vps.md).
- **Manuel d'utilisation** joueur dédié : [docs/module/MANUEL_UTILISATION.md](../module/MANUEL_UTILISATION.md).
- **Manuel de mise à jour** dédié (pull → rebuild → redeploy → santé → rollback) : [docs/module/MANUEL_MISE_A_JOUR.md](../module/MANUEL_MISE_A_JOUR.md).
- Documentation technique (choix, stack, API) : [docs/module/DOC_TECHNIQUE.md](DOC_TECHNIQUE.md).
- README d'utilisation : [README.md](../../README.md).

**Ce qui manque pour valider.**
- [x] Isoler un **manuel d'utilisation** clair côté joueur — fait ([MANUEL_UTILISATION.md](../module/MANUEL_UTILISATION.md)).
- [x] Ajouter un **manuel de mise à jour** explicite (pull → rebuild → redeploy → vérif santé → rollback) — fait ([MANUEL_MISE_A_JOUR.md](../module/MANUEL_MISE_A_JOUR.md)).
- [x] Vérifier que chaque manuel **justifie les choix techniques** (FastAPI, React, SQLite, JWT) — sections dédiées ajoutées.
- [ ] Ajouter des **captures d'écran** dans le manuel d'utilisation.

---

## Synthèse des actions prioritaires (pour passer 🟡 → 🟢)

| Priorité | Critère | Action concrète |
|---|---|---|
| ✅ Fait | C2.2.2 | Harnais de tests + couverture chiffrée documentés dans [docs/rncp/HARNAIS_TESTS_UNITAIRES.md](HARNAIS_TESTS_UNITAIRES.md) |
| ✅ Fait | C2.2.3 | Tableau **OWASP Top 10** + référentiel **RGAA** + mini-audit dans [docs/rncp/MESURES_SECURITE_ACCESSIBILITE.md](MESURES_SECURITE_ACCESSIBILITE.md) |
| ✅ Fait | C2.3.1 | **Cahier de recettes** reformaté (fonctionnel/structurel/sécurité, statuts exécutés) dans [docs/rncp/05_plan_de_recette.md](05_plan_de_recette.md) |
| ✅ Fait | C2.3.2 | Registre d'anomalies dédié créé dans [docs/rncp/PLAN_CORRECTION_BOGUES.md](PLAN_CORRECTION_BOGUES.md) |
| ✅ Fait | C2.4.1 | **Manuel d'utilisation** ([MANUEL_UTILISATION.md](../module/MANUEL_UTILISATION.md)) + **manuel de mise à jour** ([MANUEL_MISE_A_JOUR.md](../module/MANUEL_MISE_A_JOUR.md)) |
| ✅ Fait | C2.1.1 | Protocole de déploiement continu + critères qualité/performance formalisés dans [docs/rncp/PROTOCOLE_DEPLOIEMENT_CONTINU_QUALITE_PERF.md](PROTOCOLE_DEPLOIEMENT_CONTINU_QUALITE_PERF.md) |
| ✅ Fait | C2.2.4 | **Historique de versions** dans [CHANGELOG.md](../../CHANGELOG.md) (1.0.0-rncp → 1.2.0 + preuves) |
| ✅ Fait | C2.2.1 | **User stories** formalisées dans [docs/rncp/USER_STORIES.md](USER_STORIES.md) |
| P2 | C2.1.2 | Ajouter **capture CI verte** (preuve visuelle) |
| P2 | Transverse | Ajouter des **captures d'écran** (auth, jeu, combat) en annexe du dossier |

> Aucun critère n'est 🔴. Les livrables documentaires attendus sont désormais tous
> produits. Les seuls écarts restants sont des **preuves visuelles** (captures d'écran
> CI verte et écrans de jeu) à insérer en annexe : elles ne peuvent être générées que
> manuellement (impression d'écran) et n'affectent pas la complétude du dossier.
