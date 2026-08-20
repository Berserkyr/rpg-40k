# 8. Exemple de problème résolu en collaboration avec le support client

> **Compétence C4.3.3** — Collaborer avec les équipes de support, en fournissant une expertise
> technique, en répondant aux retours clients, en résolvant des problèmes complexes afin
> d'améliorer le logiciel.

## Organisation du support sur ce projet

> **Précision de contexte.** Le projet est développé par une personne seule : il n'existe pas
> d'équipe de support constituée et distincte de l'équipe de développement. Les rôles décrits
> ci-dessous correspondent aux **fonctions réellement exercées** lors du traitement — réception et
> qualification du retour d'une part, expertise technique d'autre part — et non à des personnes
> distinctes. Le cas présenté est authentique : l'anomalie, son diagnostic et son correctif ont
> réellement eu lieu. Inventer des échanges entre équipes fictives aurait retiré toute valeur
> probante à cet exemple.

| Fonction | Responsabilité | Outil |
|---|---|---|
| **Niveau 1 — Réception** | Accuser réception, qualifier, rechercher un doublon, réunir les éléments de reproduction | Formulaire `01_anomalie.yml` |
| **Niveau 2 — Expertise technique** | Reproduire, diagnostiquer la cause racine, concevoir et vérifier le correctif | Dépôt, tests, supervision |
| **Communication** | Informer le joueur du diagnostic, du contournement et de la livraison | Fil de l'issue GitHub |

---

## Contexte du retour client

### Signalement initial

Un joueur ouvre une fiche via le formulaire de consignation :

| Champ | Contenu rapporté |
|---|---|
| **Résumé** | « Mon personnage est revenu à zéro mais j'ai gardé mon niveau et mon équipement » |
| **Gravité constatée** | Majeure — perte de données |
| **Périmètre** | Sauvegarde |
| **Étapes de reproduction** | 1. Jouer une dizaine de scènes, être blessé, consommer des rations, monter de niveau et répartir des points d'attribut. 2. Fermer le jeu. 3. Revenir plus tard et se reconnecter. |
| **Comportement attendu** | Retrouver la partie dans l'état où elle a été laissée |
| **Comportement constaté** | « Je suis niveau 3 avec tout mon équipement, mais mon personnage est de nouveau indemne, mes rations sont pleines et les points que j'avais répartis ont disparu » |
| **Fréquence** | « Ça l'a fait deux fois, mais pas à chaque fois » |
| **Version** | 1.2.0 |

### Le problème à résoudre

Le retour présente trois caractéristiques qui en font un cas difficile.

**1. La perte est partielle, donc contre-intuitive.** Une perte totale de sauvegarde oriente
immédiatement vers l'écriture sur disque. Ici, le joueur **conserve** son niveau, son expérience et
son inventaire, mais **perd** ses blessures, ses ressources et ses points d'attribut. Cette
incohérence apparente suggère à tort un problème d'affichage ou de synchronisation entre panneaux.

**2. Le symptôme est intermittent du point de vue du joueur.** Il ne survient pas à chaque
reconnexion. La formulation « pas à chaque fois » est exacte mais trompeuse : elle décrit une
corrélation que le joueur ne peut pas percevoir.

**3. Le contournement évident est inopérant.** Sauvegarder manuellement via le bouton *SAUVER* ne
change rien, ce qui écarte l'hypothèse d'un oubli de sauvegarde de la part du joueur.

---

## Traitement — contribution des parties prenantes

### Niveau 1 — Réception et qualification

**Contribution :** transformer un ressenti en éléments exploitables.

Trois apports décisifs, obtenus par le formulaire structuré :

- **La distinction entre données perdues et conservées.** Le champ *Comportement constaté* liste
  précisément ce qui subsiste (niveau, équipement) et ce qui disparaît (blessures, rations, points).
  C'est cette liste qui orientera tout le diagnostic.
- **La qualification en gravité majeure.** Le formulaire classe la perte de données en *majeure*
  même sans blocage, ce qui déclenche une prise en charge sous 48 h.
- **La reformulation de l'intermittence.** À la question de savoir ce qui distinguait les sessions
  touchées, le joueur précise qu'il s'agissait des fois où il était revenu « le lendemain », par
  opposition à un simple rechargement de page. **Cette précision est l'élément déterminant** : elle
  transforme un symptôme « aléatoire » en une condition reproductible — un délai suffisant pour que
  le serveur ait redémarré ou que la session en mémoire ait disparu.

Sans cette qualification, le niveau 2 aurait cherché une anomalie d'écriture disque, alors que le
défaut se situe au **rechargement**.

### Niveau 2 — Expertise technique

**Contribution :** reproduire, diagnostiquer, corriger, prévenir la réapparition.

**Reproduction.** L'hypothèse issue de la qualification — le redémarrage — est reproduite en vidant
les sessions résidentes, ce qui simule exactement un redémarrage du serveur :

```
donnee                    avant redemarrage      apres   verdict
------------------------------------------------------------------------
rations (personnage)                      1          3   >>> PERDU <<<
blessures (personnage)                Grave    Indemne   >>> PERDU <<<
vigueur (personnage)                      9       None   >>> PERDU <<<
niveau (progression)                      3          3   CONSERVE
xp (progression)                        250        250   CONSERVE
```

Le relevé reproduit **exactement** la répartition décrite par le joueur, ce qui valide l'hypothèse
dès le premier essai.

**Diagnostic.** L'examen de `Session.save()` révèle la cause immédiatement :

```python
def save(self) -> None:
    self.world.save(self.save_dir)
    for fname, obj in [
        ("progression.yaml", self.progression),
        ("inventory.yaml", self.inventory),
        ("world_map.yaml", self.world_map),
        ("quests.yaml", self.quest_log),
        ("relationships.yaml", self.relationships),
        ("team.yaml", self.team),
    ]:
```

**`self.character` ne figure pas dans la liste.** Six sous-systèmes sont persistés, le septième est
omis. Au démarrage, la fiche est donc systématiquement reconstruite depuis le modèle vierge :

```python
self.character = CharacterState.from_file(CHARACTER_FILE)
```

La liste des données perdues correspond exactement au contenu de `CharacterState` : attributs,
ressources et jauges. La liste des données conservées correspond aux six sous-systèmes persistés.
**La répartition observée par le joueur est donc la signature directe de la cause.**

L'examen de `src/state.py` confirme qu'il s'agit d'un oubli et non d'un choix : la classe possède
une méthode `to_dict()` et une méthode `save()`, mais **aucune réciproque `from_dict()`**. L'état du
personnage pouvait être sérialisé, mais rien ne permettait de le relire — l'omission dans
`Session.save()` n'avait donc jamais été détectée, faute de chemin de lecture.

**Pourquoi le défaut avait échappé aux tests.** La suite existante instanciait les sessions dans un
même processus, où l'état reste en mémoire. Aucun test ne simulait un redémarrage. Le défaut n'était
observable qu'au rechargement à froid — exactement la condition que le joueur avait décrite sans
pouvoir la nommer.

---

## Résolution apportée

### Correctif

**1. Ajout de la réciproque manquante** (`src/state.py`) :

```python
@classmethod
def from_dict(cls, data: Dict[str, object]) -> "CharacterState":
    modele = data or {}
    return cls(
        name=modele.get("name", "Inconnu"),
        ...
        attributes=dict(modele.get("attributes") or {}),
        resources=dict(modele.get("resources") or {}),
        tracks=dict(modele.get("tracks") or {}),
    )
```

**2. Persistance de la fiche** (`backend/api.py`) :

```python
for fname, obj in [
    ("character.yaml", self.character),   # <- omission corrigee
    ("progression.yaml", self.progression),
    ...
```

**3. Rechargement avec repli.** Les parties créées avant le correctif ne possèdent pas de
`character.yaml` ; un fichier illisible ne doit pas empêcher de jouer :

```python
fichier = save_dir / "character.yaml"
if fichier.exists():
    try:
        ...
        return CharacterState.from_dict(donnees)
    except (OSError, yaml.YAMLError) as exc:
        log.error("Fiche de personnage illisible (%s) : repli sur le modele vierge. %s", fichier, exc)
return CharacterState.from_file(CHARACTER_FILE)
```

Cette compatibilité ascendante est une exigence du support : un correctif qui rendrait
inutilisables les parties existantes transformerait une perte partielle en perte totale.

### Vérification

**8 tests de non-régression** (`tests/test_character_persistence.py`), exécutés contre le code
antérieur puis contre le code corrigé :

```
# Avant correctif
6 failed, 2 passed in 2.26s

# Apres correctif
8 passed in 1.88s
```

Les deux tests qui passaient déjà sont ceux de compatibilité ascendante — le comportement de repli
existait et ne devait pas changer.

Comportement après correctif, sur le scénario exact du joueur :

```
APRES CORRECTIF
donnee                        avant      apres   verdict
------------------------------------------------------------
rations                           1          1   CONSERVE
blessures                     Grave      Grave   CONSERVE
robustesse                        9          9   CONSERVE
niveau                            3          3   CONSERVE
```

Un test vérifie spécifiquement la **cohérence** entre fiche et progression, puisque c'est leur
divergence qui constituait le symptôme.

### Réponse au joueur

Le fil de l'issue est renseigné avec :

1. **le diagnostic en termes non techniques** — « les blessures et les ressources n'étaient pas
   enregistrées avec le reste de la partie ; c'est pour cela que le niveau et l'équipement
   revenaient bien, mais pas l'état du personnage » ;
2. **l'explication de l'intermittence** — le problème n'apparaissait qu'après un redémarrage du
   serveur, ce qui correspondait aux retours « le lendemain » ;
3. **le contournement provisoire** — jouer une session d'une traite, en attendant la livraison ;
4. **la version de livraison** — 1.3.0, avec le lien vers l'entrée du journal des versions.

Le point 2 est celui qui compte le plus pour le joueur : il valide son observation au lieu de la
contredire. Un signalement qualifié d'« irreproductible » décourage les signalements suivants, qui
sont pourtant la principale source de détection sur un logiciel à faible base d'utilisateurs.

---

## Synthèse des contributions

| Partie prenante | Contribution | Sans elle |
|---|---|---|
| **Joueur** | Distinction précise entre données perdues et conservées ; précision « le lendemain » | Le diagnostic aurait porté sur l'écriture disque, au mauvais endroit |
| **Niveau 1 — Réception** | Formulaire structuré imposant les éléments de reproduction ; qualification en gravité majeure ; reformulation de l'intermittence en condition testable | Un aller-retour supplémentaire, et un symptôme classé « non reproductible » |
| **Niveau 2 — Expertise** | Reproduction dirigée, identification de la cause racine, correctif avec compatibilité ascendante, 8 tests de non-régression | Un correctif partiel, ou une régression sur les parties existantes |
| **Processus CI/CD** | Validation par 135 tests, déploiement conditionné à une CI verte, test de fumée et rollback | Aucune garantie que le correctif n'introduise pas d'autre défaut |

## Amélioration du logiciel au-delà du correctif

Le traitement a produit trois améliorations durables, au-delà de la correction :

1. **Une couverture de test manquante a été comblée.** Aucun test ne simulait un redémarrage du
   serveur ; c'est désormais le cas, ce qui protège l'ensemble des sous-systèmes persistés, pas
   seulement la fiche.
2. **Une asymétrie d'API a été corrigée.** `CharacterState` disposait de `to_dict()` sans
   `from_dict()`. Cette réciproque manquante était la cause profonde de l'omission : elle est
   désormais disponible pour tout autre usage.
3. **Le diagnostic a alimenté les recommandations.** L'anomalie a confirmé l'intérêt de la
   recommandation R3 (expiration explicite des sessions) : le comportement de rechargement, jusque-là
   implicite et non testé, est maintenant couvert.

## Éléments de preuve dans le dépôt

| Artefact | Rôle |
|---|---|
| [`src/state.py`](../../src/state.py) | `CharacterState.from_dict()` — réciproque manquante |
| [`backend/api.py`](../../backend/api.py) | Persistance et rechargement de `character.yaml`, avec repli |
| [`tests/test_character_persistence.py`](../../tests/test_character_persistence.py) | 8 tests, 6 en échec avant correctif |
| [`CHANGELOG.md`](../../CHANGELOG.md) | Entrée ANO-2026-002 dans la version 1.3.0 |
| Commit `0098252` | `Fixes: ANO-2026-002` |

## Synthèse de couverture des critères

| Critère d'évaluation attendu | Traitement dans ce document |
|---|---|
| **Le contexte du retour client avec une explication du problème à résoudre** | Sections *Signalement initial* (fiche complète telle que reçue) et *Le problème à résoudre* : perte partielle contre-intuitive, intermittence apparente, contournement inopérant |
| **La résolution apportée** | Section *Résolution apportée* : trois volets du correctif, compatibilité ascendante, vérification par 8 tests exécutés avant et après, réponse formulée au joueur |
| **Une explication de la contribution des différentes parties prenantes** | Section *Traitement* détaillant l'apport de chaque fonction, et tableau *Synthèse des contributions* indiquant pour chacune ce qui aurait manqué sans elle |
