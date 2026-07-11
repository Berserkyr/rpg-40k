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
| C2.1.1 | Environnements de déploiement et de test + suivi qualité/perf | Protocole de déploiement continu + critères qualité/perf | 🟡 Partiel |
| C2.1.2 | Intégration continue (CI) | Protocole d'intégration continue | 🟢 Solide |
| C2.2.1 | Prototype applicatif (ergonomie, cibles, sécurité) | Architecture maintenable + prototype + frameworks | 🟢 Solide |
| C2.2.2 | Harnais de tests unitaires | Jeu de tests couvrant une fonctionnalité | 🟡 Partiel |
| C2.2.3 | Sécurité (OWASP) + accessibilité | Mesures sécurité + mesures accessibilité | 🟡 Partiel |
| C2.2.4 | Déploiement progressif à chaque modification | Historique des versions + version finale viable | � Solide |
| C2.3.1 | Cahier de recettes | Cahier de recettes | 🟢 Solide |
| C2.3.2 | Plan de correction des bogues | Plan de correction des bogues | 🟡 Partiel |
| C2.4.1 | Documentation technique d'exploitation | Manuels déploiement / utilisation / mise à jour | 🟡 Partiel |

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
- Environnement de dev décrit : [docs/module/DOC_TECHNIQUE.md](DOC_TECHNIQUE.md) (stack, versions, lancement).
- Déploiement Docker Compose + VPS : [docs/deploiement_vps.md](../deploiement_vps.md).
- Healthcheck `/api/health` et supervision : [docs/module/DOC_TECHNIQUE.md](DOC_TECHNIQUE.md) (section observabilité).
- Gestion de sources Git + workflows : [.github/workflows/ci.yml](../../.github/workflows/ci.yml).

**Ce qui manque pour valider.**
- [ ] Formaliser un **protocole de déploiement en séquences numérotées** (build → test → image → déploiement → vérification santé), en un seul endroit lisible.
- [ ] Lister explicitement les **critères de qualité/performance mesurés** (temps de réponse `/api/health`, seuil de tests au vert, taille de build) avec valeurs cibles.

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

**Ce qui manque pour valider.**
- [ ] Formaliser 3 à 5 **user stories** explicites (« En tant que joueur, je veux… afin de… ») pour matérialiser le critère « user stories ».
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
- Tests backend (21) : [tests/test_api.py](../../tests/test_api.py) (auth, routes protégées, hachage).
- Tests frontend (13) : [frontend/src/__tests__/](../../frontend/src/__tests__).
- Tests E2E Playwright : [frontend/e2e/game.spec.js](../../frontend/e2e/game.spec.js).

**Ce qui manque pour valider.**
- [ ] Produire une **mesure de couverture chiffrée** (`pytest --cov` + `vitest --coverage`) et l'inscrire dans le dossier (le critère parle de « majorité du code »).
- [ ] Ajouter une **capture du rapport de couverture** ou le pourcentage global.

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
- Analyse OWASP synthétique : [docs/rncp/02_bloc2_conception_developpement.md](02_bloc2_conception_developpement.md) (section référentiel OWASP).
- Mesures de sécurité : JWT, bcrypt, rôles, routes protégées — [backend/auth.py](../../backend/auth.py).
- Accessibilité : labels ARIA, contrastes, navigation clavier — [docs/module/WIREFRAMES.md](WIREFRAMES.md).

**Ce qui manque pour valider.**
- [ ] Compléter le **tableau OWASP Top 10** avec les **10 catégories** (2021) une par une : statut + mesure + preuve.
- [ ] **Choisir et nommer un référentiel d'accessibilité** (RGAA ou OPQUAST) et justifier le choix.
- [ ] Fournir un **mini-audit d'accessibilité** (Lighthouse / axe) avec score et 3 points corrigés/à corriger.

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
- [ ] Ajouter un **historique de versions lisible** (tags/releases ou CHANGELOG résumant les incréments).
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
- Plan de recette formalisé : [docs/rncp/05_plan_de_recette.md](05_plan_de_recette.md).
- Cahier de recette dans le dossier : [docs/rncp/02_bloc2_conception_developpement.md](02_bloc2_conception_developpement.md) (section cahier de recette).

**Ce qui manque pour valider.**
- [ ] Structurer le cahier en **tableau ID / scénario / étapes / résultat attendu / résultat obtenu / statut**, en couvrant les 3 natures : **fonctionnel, structurel, sécurité**.
- [ ] Tracer au moins un **cas de test de sécurité** (ex. accès route protégée sans JWT → 401).

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
- Plan de correction des bugs : [docs/rncp/04_bloc4_maintenance.md](04_bloc4_maintenance.md) (section plan de correction).
- Anomalies traitées documentées : [docs/rncp/BLOC2_DOSSIER_FINAL.md](BLOC2_DOSSIER_FINAL.md) (tableau des corrections CI/import, fallback IA…).

**Ce qui manque pour valider.**
- [ ] Créer un **registre d'anomalies** dédié : ID / description / criticité / cause / correction / statut / preuve (commit).
- [ ] Relier chaque correction à un **commit** ou un test devenu vert (traçabilité).

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
- Documentation technique (choix, stack, API) : [docs/module/DOC_TECHNIQUE.md](DOC_TECHNIQUE.md).
- README d'utilisation : [README.md](../../README.md).

**Ce qui manque pour valider.**
- [ ] Isoler un **manuel d'utilisation** clair côté joueur (parcours pas à pas avec captures).
- [ ] Ajouter un **manuel de mise à jour** explicite (procédure : pull → rebuild image → redeploy → vérif santé → rollback).
- [ ] Vérifier que chaque manuel **justifie les choix techniques** (pourquoi FastAPI, React, SQLite, JWT).

---

## Synthèse des actions prioritaires (pour passer 🟡 → 🟢)

| Priorité | Critère | Action concrète |
|---|---|---|
| P0 | C2.2.2 | Générer et documenter la **couverture de tests** chiffrée |
| P0 | C2.2.3 | Compléter le **tableau OWASP Top 10** + choisir un **référentiel a11y** + mini-audit |
| P1 | C2.3.1 | Reformater le **cahier de recettes** (fonctionnel/structurel/sécurité) en tableau |
| P1 | C2.3.2 | Créer un **registre d'anomalies** relié aux commits |
| P1 | C2.4.1 | Ajouter **manuel d'utilisation** + **manuel de mise à jour** dédiés |
| P2 | C2.1.1 | Formaliser le **protocole de déploiement** en séquences + critères qualité chiffrés |
| P2 | C2.1.2 | Ajouter **capture CI verte** + séquences d'intégration |
| P2 | C2.2.4 | Ajouter **historique de versions** (tags/CHANGELOG) + justification déploiement manuel |
| P2 | C2.2.1 | Formaliser les **user stories** + captures d'écran |

> Aucun critère n'est 🔴 : le socle technique (prototype, CI, sécurité JWT, tests,
> déploiement) est présent. Les écarts restants sont surtout des **formalisations et
> preuves** à ajouter au dossier pour transformer chaque item en « Acquis » sans
> ambiguïté pour le jury.
