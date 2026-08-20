# 3. Processus de collecte et de consignation des anomalies

> **Compétence C4.2.1** — Consigner les anomalies détectées en élaborant un processus de collecte
> et consignation, en utilisant des outils de collecte et en y intégrant toutes les informations
> pertinentes, afin de déterminer le correctif à mettre en place.

## Adaptation du processus à la typologie du logiciel

Le logiciel présente trois particularités qui déterminent la forme du processus de collecte.

**1. Une partie des sorties est non déterministe.** La narration est produite par un LLM : deux
exécutions du même scénario ne produisent pas le même texte. Une anomalie déclenchée par une
formulation particulière du modèle peut donc être **intermittente et non rejouable à l'identique**.
La fiche impose en conséquence un champ *Fréquence* et un champ *Horodatage*, seul moyen de
retrouver a posteriori le texte incriminé dans les journaux.

**2. Le logiciel se dégrade sans erreur visible.** En cas de panne du fournisseur LLM, l'API répond
`200 OK` avec une narration locale. Une part des anomalies ne se manifeste donc **jamais** par un
code d'erreur : elles ne peuvent être détectées que par les sondes mises en place au titre de
C4.1.2. Un formulaire de consignation distinct est prévu pour ces incidents, qui n'ont pas de
signalement utilisateur.

**3. Le jeu est mono-joueur avec sauvegarde par scène.** Une anomalie survenant en fin de traitement
peut faire perdre la progression d'une scène entière. La gravité est donc évaluée à l'aune de la
**perte de données**, et non du seul caractère bloquant.

## Sources de détection

| Source | Nature | Outil | Délai typique |
|---|---|---|---|
| **Supervision** | Alertes Prometheus / Alertmanager | 13 règles, routage par sévérité | Temps réel (1 à 5 min) |
| **Journaux applicatifs** | `log.warning` / `log.exception` du backend | Journalisation structurée (`backend/monitoring.py`) | Temps réel |
| **Intégration continue** | Échec de test ou de build | GitHub Actions (5 jobs) | À chaque push |
| **Audit de dépendances** | CVE sur une bibliothèque tierce | `pip-audit`, `npm audit` | À chaque push |
| **Signalement joueur** | Retour d'usage | Formulaire GitHub Issues | Variable |
| **Recette manuelle** | Vérification des parcours critiques | Plan de recette | Avant chaque mise en production |

Les quatre premières sources sont **automatiques** : elles ne dépendent pas de la vigilance d'un
utilisateur. C'est un point important pour un logiciel à faible base d'utilisateurs, où l'on ne
peut pas compter sur le volume de signalements pour révéler les défauts.

## Outils de collecte

La collecte est centralisée dans **GitHub Issues**, avec deux formulaires structurés qui
remplacent la saisie libre — celle-ci est désactivée (`blank_issues_enabled: false`) :

| Formulaire | Usage | Champs obligatoires |
|---|---|---|
| [`01_anomalie.yml`](../../.github/ISSUE_TEMPLATE/01_anomalie.yml) | Signalement d'un dysfonctionnement | 10 |
| [`02_incident_supervision.yml`](../../.github/ISSUE_TEMPLATE/02_incident_supervision.yml) | Alerte remontée par la supervision | 5 |

Le choix du formulaire contraint plutôt que du texte libre répond à un constat pratique : une
description en prose omet presque systématiquement la version, l'environnement ou les étapes
exactes, ce qui impose un aller-retour de qualification avant toute analyse. Les dix champs
obligatoires du formulaire d'anomalie sont précisément ceux **sans lesquels le bogue n'est pas
reproductible** : résumé, gravité, périmètre, étapes, comportement attendu, comportement constaté,
fréquence, version, environnement, horodatage.

## Cycle de vie d'une anomalie

```
   Détection                Qualification              Traitement            Clôture
┌──────────────┐         ┌─────────────────┐       ┌───────────────┐    ┌──────────────┐
│ supervision  │         │ reproduction    │       │ branche fix/  │    │ test de non- │
│ journaux     │────────▶│ gravité         │──────▶│ correctif     │───▶│ régression   │
│ CI           │  fiche  │ périmètre       │       │ + test         │    │ + fermeture  │
│ joueur       │         │ priorisation    │       │ revue PR       │    │              │
└──────────────┘         └─────────────────┘       └───────────────┘    └──────────────┘
   à-qualifier               confirmée                 en-cours              corrigée
```

Les états correspondent aux étiquettes GitHub et aux colonnes du kanban
(`docs/gestion_projet/kanban.md`).

## Grille de gravité et délais de traitement

| Gravité | Définition | Délai de prise en charge | Exemple |
|---|---|---|---|
| **Bloquante** | Le jeu est inutilisable | Immédiat | API injoignable, impossibilité de se connecter |
| **Majeure** | Fonctionnalité inutilisable **ou perte de données** | 48 h | ANO-2026-001 (perte de progression) |
| **Mineure** | Gêne sans perte de données | Lot mensuel | Libellé erroné, bouton mal aligné |
| **Cosmétique** | Affichage uniquement | Opportuniste | Faute de frappe |

La perte de données est classée *majeure* même sans blocage : dans un jeu à sauvegarde par scène,
perdre une scène équivaut à annuler plusieurs minutes de jeu, ce que l'utilisateur perçoit comme
une régression grave.

## Informations consignées

Chaque fiche porte, au-delà des champs de saisie :

- un **identifiant** `ANO-AAAA-NNN` ;
- l'**analyse technique** (fichier et ligne en cause, mécanisme) ;
- les **préconisations de correction**, avec les options envisagées et la justification du choix ;
- les **tests de non-régression** ajoutés ;
- le **lien vers la pull request** de correction.

---

# 4. Exemple de fiche de consignation — ANO-2026-001

## Identification

| Champ | Valeur |
|---|---|
| **Identifiant** | ANO-2026-001 |
| **Résumé** | La scène se fige après la narration ; la progression de la scène est perdue |
| **Gravité** | **Majeure** — perte de données |
| **Périmètre** | Narration / maître du jeu |
| **Version** | v1.0.0-rncp |
| **Environnement** | Développement local et production |
| **Fréquence** | Intermittente — dépend du texte produit par le LLM |
| **Détectée par** | Revue de code, puis reproduction dirigée |
| **Date** | 19/08/2026 |
| **État** | **Corrigée** |

## Description

À l'issue de certaines scènes, le joueur reçoit intégralement le texte de narration, puis
l'interface reste bloquée sur l'indicateur d'attente. Aucun message d'erreur ne s'affiche. En
rechargeant la page, **la scène qui vient d'être jouée a disparu** : la partie est revenue à son
état antérieur.

Le phénomène est intermittent et ne dépend pas de l'action du joueur, ce qui a longtemps orienté à
tort vers un problème réseau.

## Étapes de reproduction

Le déclencheur étant une sortie particulière du LLM, la reproduction fiable passe par la
substitution du narrateur :

1. Se connecter avec un compte joueur et démarrer une partie.
2. Faire produire au maître du jeu une narration contenant un marqueur d'état dont la valeur de
   ressource n'est **pas numérique** :

   ```
   Karimus partage ses dernières provisions avec les survivants.
   [ETAT: rations=aucune, stress=+1]
   ```

3. Observer le flux SSE renvoyé par `POST /api/chat`.

**Reproduction automatisée :**

```bash
.venv/Scripts/python.exe -m pytest tests/test_state_markers.py -q
```

## Comportement attendu

Le flux transmet la narration, puis un événement `done` portant l'état mis à jour. La partie est
sauvegardée. Un marqueur inexploitable est ignoré sans conséquence.

## Comportement constaté

Relevé avant correctif, sur le même parcours avec deux narrations différentes :

```
--- NOMINAL  (rations=-1) ---
  statut HTTP        : 200
  evenements 'token' : 5
  evenements 'done'  : 1

--- DEFAILLANT (rations=aucune) ---
  !! Exception : ValueError: invalid literal for int() with base 10: 'aucune'
```

La narration parvient au joueur, puis le flux s'interrompt : **aucun événement `done` n'est émis**.

## Analyse technique

**Cause racine** — `src/state.py`, méthode `apply_updates_from_text()`. Le parseur convertit la
valeur d'une ressource sans protéger la conversion :

```python
elif key in ('rations', 'acces_vox', 'contacts', 'munitions'):
    if value.startswith(('+', '-')):
        delta = int(value)          # ValueError si la valeur n'est pas numérique
        self.update_resource(key, delta)
    else:
        self.set_resource(key, int(value))   # idem
```

**Asymétrie révélatrice** — la branche voisine, qui traite `stress` et `corruption`, intercepte
pourtant exactement le même cas :

```python
try:
    self.tracks[key] = int(value)
except ValueError:
    self.tracks[key] = value        # repli sur la valeur textuelle
```

Le défaut n'est donc pas un oubli de conception mais une **protection appliquée à une branche et
omise sur l'autre**. Vérification par exécution :

| Marqueur | Branche | Résultat avant correctif |
|---|---|---|
| `[ETAT: stress=eleve]` | `tracks` | Accepté — `Stress -> eleve` |
| `[ETAT: rations=aucune]` | `resources` | **ValueError** |
| `[ETAT: munitions=+]` | `resources` | **ValueError** |

**Mécanisme de l'impact** — l'appel se situe dans le générateur SSE, `backend/api.py` :

```python
546  session.messages.append({"role": "assistant", "content": full_text})
547  session.world.advance_scene()
548  changes = session.character.apply_updates_from_text(full_text)   # ← exception ici
549  expired = session.quest_log.advance_all_timers()
550  session.save()                                                   # ← jamais atteint
551  yield json.dumps({"type": "done", ...})                          # ← jamais émis
```

L'ordre des instructions explique les deux symptômes simultanés :

1. l'exception survient **après** l'envoi de la narration — le joueur a donc bien lu la scène ;
2. elle survient **avant** `session.save()` — la progression n'est jamais écrite sur disque ;
3. elle survient **avant** l'événement `done` — le client attend indéfiniment.

**Pourquoi le défaut a échappé aux tests** — la suite existante ne couvrait
`apply_updates_from_text` qu'avec des valeurs numériques valides. Le déclencheur étant une sortie
de LLM, il n'apparaissait pas dans les scénarios déterministes.

## Préconisations de correction

Trois options ont été examinées :

| Option | Analyse | Retenue |
|---|---|---|
| **A.** Renforcer le prompt système pour imposer un format numérique | Ne supprime pas le risque : la sortie d'un LLM ne peut être garantie par une consigne | Non |
| **B.** Intercepter la `ValueError` dans le parseur | Traite la cause racine, aligne la branche `resources` sur la branche `tracks` | **Oui** |
| **C.** Protéger l'appel dans le générateur SSE | Ne traite pas la cause, mais garantit qu'aucune future erreur de parsing ne coûte une sauvegarde | **Oui, en complément** |

Les options B et C sont retenues ensemble, selon un principe de défense en profondeur : B corrige
le défaut identifié, C protège contre les défauts de même famille non encore découverts.

**Correctif B — `src/state.py`**

```python
try:
    if value.startswith(('+', '-')):
        self.update_resource(key, int(value))
        changes.append(f"{key} {value}")
    else:
        self.set_resource(key, int(value))
        changes.append(f"{key} = {value}")
except ValueError:
    self.rejected_updates.append(f"{key}={value}")
    _logger.warning(
        "Marqueur d'etat ignore : valeur non numerique pour "
        "la ressource '%s' (recu : %r)", key, value,
    )
```

**Correctif C — `backend/api.py`**

```python
changes: list[str] = []
try:
    changes = session.character.apply_updates_from_text(full_text)
except Exception as exc:
    STATE_PARSE_FAILURES.labels(reason=type(exc).__name__).inc()
    log.exception("Echec d'application des marqueurs d'etat : %s", exc)

for rejected in getattr(session.character, "rejected_updates", []):
    STATE_MARKERS_REJECTED.inc()
    log.warning("Marqueur d'etat rejete : %s", rejected)
```

**Correctif D — rendre le phénomène mesurable.** Deux sondes ont été ajoutées au dispositif de
supervision, afin qu'un marqueur rejeté cesse d'être invisible :

| Sonde | Finalité |
|---|---|
| `rpg40k_state_markers_rejected_total` | Nombre de marqueurs ignorés — révèle une dérive de format du LLM |
| `rpg40k_state_parse_failures_total{reason}` | Échec inattendu du parsing — filet de sécurité |

Un marqueur ignoré reste une **anomalie fonctionnelle mineure** : la ressource n'est pas mise à
jour alors que la narration le laisse entendre. Le correctif supprime la perte de données, mais la
sonde permet de mesurer la fréquence résiduelle du phénomène et, si elle est élevée, de justifier
un travail ultérieur sur le prompt système.

## Vérification du correctif

**18 tests de non-régression** ajoutés dans `tests/test_state_markers.py`, dont huit valeurs non
numériques passées en paramètre (`aucune`, `quelques-unes`, `+`, `-`, chaîne vide, `beaucoup`,
`3 rations`, `N/A`). La suite backend passe de 102 à **120 tests, tous au vert**.

Les tests couvrent quatre propriétés :

1. aucune valeur textuelle ne lève d'exception ;
2. un marqueur rejeté ne modifie pas la ressource et reste traçable ;
3. un marqueur invalide n'annule pas les marqueurs valides de la même ligne ;
4. le flux SSE émet son événement `done` et `session.save()` est bien atteint.

Relevé après correctif, sur le parcours qui échouait :

```
APRES CORRECTIF  ->  statut: 200
  evenements 'token' : 6
  evenements 'done'  : 1
  sonde marqueurs rejetes : 1.0
```

Le flux se termine normalement, la sauvegarde est effectuée, et l'anomalie résiduelle est comptée
par la supervision au lieu d'être silencieuse.

Un test vérifie par ailleurs que l'écrêtage des ressources à zéro — règle de jeu préexistante —
n'a pas été altéré par le correctif.

## Éléments de preuve dans le dépôt

| Artefact | Rôle |
|---|---|
| [`.github/ISSUE_TEMPLATE/01_anomalie.yml`](../../.github/ISSUE_TEMPLATE/01_anomalie.yml) | Formulaire de consignation, 10 champs obligatoires |
| [`.github/ISSUE_TEMPLATE/02_incident_supervision.yml`](../../.github/ISSUE_TEMPLATE/02_incident_supervision.yml) | Consignation des alertes sans signalement utilisateur |
| [`.github/ISSUE_TEMPLATE/config.yml`](../../.github/ISSUE_TEMPLATE/config.yml) | Désactivation de la saisie libre |
| [`src/state.py`](../../src/state.py) | Correctif de la cause racine |
| [`backend/api.py`](../../backend/api.py) | Protection du générateur SSE et alimentation des sondes |
| [`backend/monitoring.py`](../../backend/monitoring.py) | Sondes `state_markers_rejected` et `state_parse_failures` |
| [`tests/test_state_markers.py`](../../tests/test_state_markers.py) | 18 tests de non-régression |

## Synthèse de couverture des critères

| Critère d'évaluation attendu | Traitement dans ce document |
|---|---|
| **Le processus de collecte est structuré et adapté à la typologie du logiciel** | Sections *Adaptation*, *Sources de détection*, *Outils*, *Cycle de vie* : six sources dont quatre automatiques, deux formulaires structurés, grille de gravité fondée sur la perte de données |
| **La fiche de consignation contient les informations permettant de reproduire le bogue** | Fiche ANO-2026-001 : étapes numérotées, marqueur déclencheur exact, commande de reproduction automatisée, relevés avant/après |
| **L'analyse du bogue et les préconisations de corrections sont explicitées et permettent de corriger l'anomalie** | Section *Analyse technique* (cause racine, asymétrie des branches, mécanisme de l'impact ligne à ligne) et *Préconisations* (trois options comparées, deux retenues en défense en profondeur, correctif vérifié par 18 tests) |
