# Bloc 4 — Maintenir l'Application Logicielle en Condition Opérationnelle

Dossier de travail. Chaque section est rédigée séparément puis assemblée en un rapport
unique (PDF) une fois l'ensemble des compétences traité.

**Projet support :** RPG 40K — Survivant de Ruche
**Auteur :** _(à compléter)_

## Avancement

| # | Section | Compétence | Fichier | État |
|---|---|---|---|---|
| 1 | Processus de mise à jour des dépendances | C4.1.1 | [01_processus_maj_dependances.md](01_processus_maj_dependances.md) | ✅ Rédigé |
| 2 | Système de supervision et d'alerte | C4.1.2 | [02_systeme_supervision.md](02_systeme_supervision.md) | ✅ Rédigé |
| 3 | Collecte et consignation des anomalies | C4.2.1 | [03_collecte_consignation_anomalies.md](03_collecte_consignation_anomalies.md) | ✅ Rédigé |
| 4 | Fiche de consignation ANO-2026-001 | C4.2.1 | [03_collecte_consignation_anomalies.md](03_collecte_consignation_anomalies.md) *(section 4)* | ✅ Rédigé |
| 5 | Traitement d'une anomalie (CI/CD) | C4.2.2 | [05_traitement_anomalie.md](05_traitement_anomalie.md) | ✅ Rédigé |
| 6 | Recommandations argumentées d'amélioration | C4.3.1 | [06_recommandations_amelioration.md](06_recommandations_amelioration.md) | ✅ Rédigé |
| 7 | Journal des versions | C4.3.2 | [07_journal_versions.md](07_journal_versions.md) | ✅ Rédigé |
| 8 | Problème résolu avec le support client | C4.3.3 | [08_support_client.md](08_support_client.md) | ✅ Rédigé |

_Le plan ci-dessus reprend la structure du rapport d'exemple ; il sera ajusté au fil des
compétences fournies._

## Conventions de rédaction

- Rédaction en **français**, registre technique et professionnel.
- Chaque affirmation s'appuie sur un **élément réel et vérifiable du dépôt** (fichier, workflow,
  commande, résultat de test) — pas de procédure théorique non outillée.
- Chaque section se termine par un **tableau de couverture** reliant explicitement le contenu aux
  critères d'évaluation de la grille.
- Les chiffres cités (82 tests backend, 30 tests frontend, 32 routes, 4 vulnérabilités npm) sont
  issus d'exécutions réelles et doivent être remis à jour si le code évolue avant la soutenance.

## Modifications apportées au code

Le rapport ne décrit aucun processus qui ne soit pas réellement outillé dans le dépôt. Les
éléments suivants ont été **ajoutés ou corrigés** pour que la section 1 corresponde au code :

| # | Modification | Fichier | Motif |
|---|---|---|---|
| 1 | Configuration Dependabot (pip, npm, Docker ×2, GitHub Actions) | `.github/dependabot.yml` *(créé)* | Rien n'assurait la « surveillance régulière des nouvelles versions » exigée par C4.1.1 |
| 2 | Bornes hautes `<N.0.0` sur les 12 dépendances backend | `requirements.txt` *(modifié)* | Les contraintes `>=` seules laissaient passer les montées majeures non décidées |
| 3 | Script de veille d'obsolescence | `scripts/check_updates.py` *(créé)* | Matérialise la veille et classe les écarts majeure / mineure |
| 4 | Rapport de veille intégré au job `security-audit` | `.github/workflows/ci.yml` *(modifié)* | Rend la veille automatique plutôt que déclarative |
| 5 | Correction de la description du déclenchement du déploiement | `docs/gestion_projet/strategie_git.md` *(modifié)* | Le document affirmait un déploiement « volontairement manuel », contredit par le `workflow_run` de `deploy-vps.yml` |

### Section 2 — C4.1.2 (supervision)

| # | Modification | Fichier | Motif |
|---|---|---|---|
| 6 | Module de supervision : sondes Prometheus, middleware HTTP, journalisation structurée, sonde d'aptitude | `backend/monitoring.py` *(créé)* | Aucune métrique ni journalisation n'existait |
| 7 | Routes `/api/health/ready` et `/api/metrics`, instrumentation des parcours auth / narration / combat | `backend/api.py` *(modifié)* | `/api/health` retournait « ok » sans jamais interroger la base |
| 8 | Collecte Prometheus, 13 règles d'alerte, routage Alertmanager | `monitoring/` *(créé)* | Aucun dispositif d'alerte |
| 9 | Tableau de bord d'exploitation (13 panneaux) et provisionnement Grafana | `monitoring/grafana/` *(créé)* | Supervision versionnée avec le code |
| 10 | Pile de supervision en surcouche Docker Compose | `docker-compose.monitoring.yml` *(créé)* | Déploiement optionnel, pile applicative inchangée |
| 11 | 20 tests de non-régression du dispositif | `tests/test_monitoring.py` *(créé)* | Vérifie que les sondes détectent réellement les pannes |
| 12 | Ajout de `prometheus-client` (borné) | `requirements.txt` *(modifié)* | Exposition au format Prometheus |

**Vérifications après modification :** **102 tests backend au vert** (82 avant instrumentation),
30 tests frontend au vert, build de production fonctionnel, fichiers YAML et JSON valides,
sondes vérifiées sur l'application en fonctionnement.

### Sections 3 et 4 — C4.2.1 (anomalies)

| # | Modification | Fichier | Motif |
|---|---|---|---|
| 13 | **Correctif ANO-2026-001** : interception de la valeur non numérique | `src/state.py` *(modifié)* | `ValueError` non interceptée : flux SSE interrompu et **perte de la progression de la scène** |
| 14 | Protection du générateur SSE (défense en profondeur) | `backend/api.py` *(modifié)* | Aucune erreur de parsing ne doit plus empêcher `session.save()` |
| 15 | Sondes `state_markers_rejected` et `state_parse_failures` | `backend/monitoring.py` *(modifié)* | Rend mesurable l'anomalie résiduelle |
| 16 | 18 tests de non-régression | `tests/test_state_markers.py` *(créé)* | Échouent sur le code antérieur au correctif |
| 17 | Formulaires de consignation structurés | `.github/ISSUE_TEMPLATE/` *(créé)* | Aucun outil de collecte n'existait ; garantit les informations de reproduction |

**Vérifications après correctif :** **120 tests backend au vert** (102 avant), symptôme d'origine
vérifié comme résolu sur l'application en fonctionnement.

### Section 5 — C4.2.2 (traitement CI/CD)

| # | Modification | Fichier | Motif |
|---|---|---|---|
| 18 | Test de fumée post-déploiement (5 contrôles) | `scripts/smoke_test.sh` *(créé)* | Le déploiement se validait sur la sonde de vivacité, qui répond « ok » même si la base est injoignable |
| 19 | Rollback automatique vers le commit précédent | `.github/workflows/deploy-vps.yml` *(modifié)* | Aucun retour arrière n'existait : une version cassée restait en production |
| 20 | Garde-fou `JWT_SECRET` au déploiement | `.github/workflows/deploy-vps.yml` *(modifié)* | `.env` copié depuis `.env.example` signait les jetons avec le secret public du dépôt |
| 21 | Historique Git structuré en 4 commits atomiques | branche `fix/ANO-2026-001-marqueurs-etat` | Chaque commit indépendamment testable (`git bisect` exploitable) |

**Vérification CI locale :** 120 tests backend, 30 tests frontend, build de production,
rapport de veille — tous les jobs au vert sur la branche de correction.

### Section 6 — C4.3.1 (recommandations)

| # | Modification | Fichier | Motif |
|---|---|---|---|
| 22 | Mesure des indicateurs de performance | `scripts/benchmark.py` *(créé)* | Aucune mesure n'existait : les recommandations devaient reposer sur des relevés reproductibles |
| 23 | Canal de retour d'expérience utilisateur | `.github/ISSUE_TEMPLATE/03_retour_utilisateur.yml` *(créé)* | Aucun dispositif ne permettait d'« analyser les retours utilisateurs » |
| 24 | **Correction d'un chiffre erroné** : latence du login | `docs/bloc4/02_systeme_supervision.md` *(corrigé)* | La valeur de 117 ms était une moyenne incluant un login rejeté avant bcrypt ; mesure réelle ~230 ms dont 219 ms de bcrypt |

**Relevés obtenus :** VoxelEngine = 481 Ko sur 756 Ko de JS ; contexte LLM 1 209 → 8 169 tokens
(scène 1 → 30) ; `session_events` alimentée mais jamais lue ; aucun index explicite en base.

### Section 7 — C4.3.2 (journal des versions)

| # | Modification | Fichier | Motif |
|---|---|---|---|
| 25 | Fichier `VERSION` — source unique de vérité | `VERSION` *(créé)* | La version était écrite en dur et avait dérivé de deux versions mineures |
| 26 | Lecture de la version et du journal | `backend/version.py` *(créé)* | `/api/health` annonçait `1.0.0` alors que le journal était à `1.2.0` |
| 27 | **Application de R6** : mode debug piloté par `API_DEBUG` | `backend/api.py` *(modifié)* | `debug=True` en dur exposait les traces d'exécution en production |
| 28 | Entrée `[1.3.0]` documentant les correctifs déployés | `CHANGELOG.md` *(modifié)* | Livrable de C4.3.2 |
| 29 | 7 tests interdisant la dérive version ↔ journal | `tests/test_version.py` *(créé)* | Vérifié : une version incohérente fait échouer la CI |

**Vérifications :** **127 tests backend au vert** (120 avant), 30 tests frontend.

### Section 8 — C4.3.3 (support client)

| # | Modification | Fichier | Motif |
|---|---|---|---|
| 30 | **Correctif ANO-2026-002** : `CharacterState.from_dict()` | `src/state.py` *(modifié)* | `to_dict()` existait sans réciproque : l'état du personnage pouvait être écrit, jamais relu |
| 31 | Persistance et rechargement de `character.yaml` | `backend/api.py` *(modifié)* | `Session.save()` omettait `self.character` : blessures, ressources et points d'attribut perdus à chaque redémarrage |
| 32 | 8 tests de non-régression (6 en échec avant correctif) | `tests/test_character_persistence.py` *(créé)* | Aucun test ne simulait un redémarrage du serveur |
| 33 | Entrée ANO-2026-002 au journal des versions | `CHANGELOG.md` *(modifié)* | Traçabilité du correctif déployé |

**Vérifications :** **135 tests backend au vert** (127 avant), 30 tests frontend.

## Points à trancher avant l'assemblage final

- **Nom de l'auteur** à porter en page de couverture.
- **Absence de verrouillage côté Python** : le frontend dispose de `package-lock.json` (installation
  reproductible via `npm ci`), le backend n'a pas d'équivalent. Les bornes hautes limitent le
  risque sans le supprimer : deux installations à deux dates différentes peuvent encore obtenir des
  versions correctives distinctes. Piste à verser à la section 6 (*Recommandations argumentées
  d'amélioration*) plutôt qu'à traiter maintenant.
