# 7. Journal des versions

> **Compétence C4.3.2** — Établir un journal des versions déployées en y intégrant la documentation
> des correctifs réalisés pour suivre les différentes évolutions réalisées sur le logiciel.

## Rôle et emplacement

Le journal des versions est tenu dans [`CHANGELOG.md`](../../CHANGELOG.md), à la racine du dépôt.
Il suit le format *Keep a Changelog* et le versionnage sémantique `MAJEUR.MINEUR.CORRECTIF`.

Il remplit trois fonctions distinctes :

1. **Tracer les évolutions** livrées à chaque version ;
2. **Documenter les correctifs déployés**, en reliant chaque correction à sa fiche d'anomalie ;
3. **Servir de référence au retour arrière** : la section *Correspondance versions ↔ preuves*
   identifie, pour chaque version, le tag ou le commit vers lequel revenir.

## Défaut corrigé : la version rapportée était fausse

Le journal existait, mais **le logiciel ne savait pas quelle version il exécutait**.
`backend/api.py` déclarait la version en dur :

```python
app = FastAPI(title="Survivant de Ruche API", version="1.0.0", debug=True)
```

Cette constante n'avait jamais été mise à jour : la route `/api/health` annonçait `1.0.0` alors que
le journal en était à `1.2.0`, soit **deux versions mineures d'écart**.

La conséquence est directement liée au processus de traitement des anomalies décrit au chapitre 3 :
le formulaire de consignation exige le champ *Version du logiciel*, en indiquant de relever la
valeur retournée par `/api/health`. Un joueur suivant cette consigne aurait donc rapporté une
version **erronée**, rendant impossible le rattachement fiable d'une anomalie à un état du code.

**Correctif appliqué :**

- création d'un fichier `VERSION` à la racine, **source unique de vérité** ;
- `backend/version.py` expose `get_version()` et lit le journal ;
- `backend/api.py` consomme cette valeur au lieu d'une constante ;
- **7 tests** (`tests/test_version.py`) empêchent la dérive de se reproduire.

Vérification que la protection fonctionne réellement — en portant volontairement `VERSION` à une
valeur incohérente avec le journal :

```
$ printf '9.9.9\n' > VERSION && pytest tests/test_version.py -q
FAILED tests/test_version.py::test_la_version_correspond_au_journal
FAILED tests/test_version.py::test_le_journal_documente_la_version_courante
2 failed, 5 passed
```

Le journal ne peut donc plus diverger silencieusement du code : toute publication oubliant de
documenter sa version fait échouer la CI.

## Règles de tenue du journal

| Règle | Justification |
|---|---|
| Une section par version publiée, la plus récente en premier | Lecture immédiate de l'état courant |
| Rubriques normalisées : *Ajouté*, *Modifié*, *Corrigé*, *Sécurité*, *Tests*, *Documentation* | Un lecteur cherchant les correctifs va directement à *Corrigé* |
| Chaque correctif nomme l'anomalie, son symptôme, sa cause et son correctif | Le journal doit se suffire à lui-même |
| Chaque version référence son tag ou sa branche | Permet le retour arrière |
| Les rubriques *Sécurité* sont toujours explicites | Une correction de sécurité ne doit jamais être noyée dans « divers » |
| La section *Non publié* accueille les incréments en attente | Évite la rédaction rétrospective à la publication |

Une entrée de journal est rédigée **au moment du commit**, et non reconstituée au moment de la
publication : c'est la seule façon d'obtenir une description fidèle du correctif.

---

## Exemplaire du journal — version 1.3.0

Extrait de [`CHANGELOG.md`](../../CHANGELOG.md).

---

### [1.3.0] — Maintien en condition opérationnelle — 19/08/2026

Réf. branche : `fix/ANO-2026-001-marqueurs-etat`.

Cette version regroupe la refonte gameplay V3 et la mise en place du dispositif de maintien en
condition opérationnelle : supervision, gestion des dépendances, traitement d'anomalie et
durcissement du déploiement.

#### Corrigé

- **ANO-2026-001 — Perte de la progression sur un marqueur d'état invalide**
  *(gravité : majeure, perte de données)*

  Le parseur des marqueurs `[ETAT: ...]` produits par le maître du jeu convertissait la valeur
  d'une ressource par `int()` sans protection. Le texte provenant d'un LLM, une valeur non
  numérique (`rations=aucune`, `munitions=+`) levait une `ValueError`. Levée dans le générateur SSE
  **après** l'envoi de la narration mais **avant** `session.save()`, l'exception interrompait le
  flux sans événement `done` — le client restait bloqué — et la scène jouée n'était jamais
  sauvegardée.

  *Correctif* : interception de la valeur non exploitable dans `src/state.py` (alignement sur la
  branche `tracks` qui traitait déjà ce cas), et confinement dans `backend/api.py` afin qu'aucune
  erreur de parsing ne puisse plus empêcher la clôture de la scène. 18 tests de non-régression,
  dont 16 en échec sur le code antérieur.

- **Version du logiciel incorrectement rapportée.** `backend/api.py` déclarait `version="1.0.0"` en
  dur alors que le journal était à `1.2.0`. La version est désormais lue depuis le fichier
  `VERSION`, et un test vérifie sa cohérence avec ce journal.

- **Documentation du déploiement contredite par le code.** `strategie_git.md` affirmait un
  déploiement « volontairement manuel », alors que `deploy-vps.yml` déclenche un déploiement
  automatique sur CI verte.

#### Sécurité

- **Mode debug désactivé par défaut** *(recommandation R6)*. `FastAPI(debug=True)` était écrit en
  dur : toute exception non gérée exposait la trace d'exécution et des extraits de code source en
  production. Le mode est désormais piloté par `API_DEBUG`, absente par défaut.
- **Garde-fou sur `JWT_SECRET` au déploiement.** Le déploiement créait `.env` par copie de
  `.env.example`, ce qui signait les jetons de production avec le secret d'exemple public du dépôt.
- **Sonde de tentatives d'authentification** et alerte au-delà de 10 échecs par minute.

#### Ajouté — Supervision et alerte

- `backend/monitoring.py` : sondes Prometheus, middleware HTTP, journalisation structurée.
- Sonde d'aptitude `/api/health/ready` interrogeant réellement SQLite et les fichiers de jeu.
- Point de collecte `/api/metrics`.
- Sonde `rpg40k_gm_generations_total{mode}` rendant visible la bascule vers le narrateur local.
- 13 règles d'alerte, routage Alertmanager par sévérité, tableau de bord Grafana (13 panneaux).

#### Ajouté — Gestion des dépendances

- `.github/dependabot.yml` : détection hebdomadaire sur 4 écosystèmes.
- Bornes hautes `<N.0.0` sur les 12 dépendances backend.
- `scripts/check_updates.py` : rapport de veille intégré à la CI.

#### Ajouté — Déploiement

- `scripts/smoke_test.sh` : 5 contrôles post-déploiement.
- Retour arrière automatique vers le commit précédent en cas d'échec.

#### Tests

- `test_monitoring.py` (20), `test_state_markers.py` (18), `test_version.py` (7).
- **Total : 82 → 127 tests backend au vert**, 30 tests frontend.

---

## Correspondance versions ↔ preuves

| Version | Tag / commit | Preuve de fonctionnement |
|---|---|---|
| **1.3.0** | `fix/ANO-2026-001-marqueurs-etat` | CI locale verte (127 backend + 30 frontend), test de fumée exécuté |
| 1.2.0 | `7d9bf12` | CI verte + déploiement VPS |
| 1.1.0 | `b565b39` | CI verte + déploiement VPS |
| 1.0.1 | `5b1164d` | CI verte |
| 1.0.0-rncp | `v1.0.0-rncp` | Application en ligne |

## Articulation avec les autres processus

Le journal n'est pas un document isolé : il est le point de convergence des chapitres précédents.

```
   Anomalie             Correctif              Déploiement          Journal
  (chapitre 3)         (chapitre 5)           (chapitre 5)       (ce chapitre)
┌──────────────┐     ┌──────────────┐      ┌───────────────┐   ┌──────────────┐
│ ANO-2026-001 │────▶│ commit       │─────▶│ CI verte      │──▶│ entrée       │
│ fiche de     │     │ 26df2a1      │      │ smoke test    │   │ [1.3.0]      │
│ consignation │     │ Fixes: ANO-… │      │ + rollback    │   │ rubrique     │
└──────────────┘     └──────────────┘      └───────────────┘   │ « Corrigé »  │
                                                                └──────────────┘
                                                                       │
                                                          VERSION ◀────┘
                                                        /api/health
```

La chaîne est vérifiable dans les deux sens : depuis une version affichée par `/api/health`, on
retrouve l'entrée du journal, le commit, puis la fiche d'anomalie ; inversement, une fiche
d'anomalie mène au commit qui la corrige et à la version qui l'a déployée.

## Éléments de preuve dans le dépôt

| Artefact | Rôle |
|---|---|
| [`CHANGELOG.md`](../../CHANGELOG.md) | Journal des versions, 5 versions documentées |
| [`VERSION`](../../VERSION) | Source unique de vérité du numéro de version |
| [`backend/version.py`](../../backend/version.py) | Lecture de la version et du journal |
| [`tests/test_version.py`](../../tests/test_version.py) | 7 tests interdisant la dérive version ↔ journal |

## Synthèse de couverture des critères

| Critère d'évaluation attendu | Traitement dans ce document |
|---|---|
| **Le journal de version contient les différentes améliorations amenées par cette version (anomalies corrigées, nouvelles fonctionnalités, etc.)** | Exemplaire de la version 1.3.0 : rubriques *Corrigé* (3 entrées), *Sécurité* (3), *Ajouté* (supervision, dépendances, déploiement, gameplay V3), *Tests* |
| **Les correctifs déployés sont documentés** | Chaque correctif nomme l'anomalie, son symptôme, sa cause racine, le correctif appliqué et sa couverture de tests ; la correspondance versions ↔ preuves permet le retour arrière |
