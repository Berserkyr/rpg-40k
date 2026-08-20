# 2. Système de supervision et d'alerte

> **Compétence C4.1.2** — Concevoir un système de supervision et d'alerte en déterminant le
> périmètre de supervision et en identifiant les indicateurs de suivi pertinents, en mettant en
> place des sondes, en configurant la modalité des signalements afin de garantir une disponibilité
> permanente du logiciel.

## État initial et problème identifié

Avant conception, le projet ne disposait d'aucun dispositif de supervision : aucune journalisation
configurée, aucune métrique exposée, et une unique route `/api/health` retournant un dictionnaire
figé :

```python
@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "...", "version": ..., "database": str(DATABASE_PATH)}
```

Cette sonde présentait un défaut majeur : **elle affichait le chemin de la base de données sans
jamais l'interroger**. Une base corrompue, un volume Docker non monté ou un disque plein
laissaient la sonde répondre `"status": "ok"` alors que toute partie était impossible. Le
dispositif décrit ci-après corrige cette situation.

## Adéquation à la typologie du logiciel

Le logiciel supervisé n'est ni un site vitrine ni une API transactionnelle : c'est un **jeu de rôle
narratif mono-joueur**, exposé en API REST + SSE, dont la narration est déléguée à un **fournisseur
LLM externe**, et dont l'état de partie est conservé **en mémoire du processus** puis sérialisé sur
disque. Quatre caractéristiques structurent le dispositif de supervision :

| Caractéristique du logiciel | Conséquence sur la supervision |
|---|---|
| **Dégradation silencieuse prévue par conception** — en cas de panne du LLM, l'application bascule automatiquement sur un narrateur local et continue de répondre `200 OK` | Une supervision fondée sur les seuls codes HTTP déclarerait le service sain alors que la valeur perçue par le joueur s'est effondrée. Une sonde dédiée au **mode de production de la narration** est donc indispensable. |
| **Réponses en streaming SSE** de plusieurs dizaines de secondes | Les routes de narration ne peuvent pas être jugées sur les mêmes seuils de latence que les routes de jeu. Elles sont exclues des alertes de lenteur et suivies par une jauge de **flux ouverts**. |
| **Sessions conservées en mémoire, sans expiration** | La consommation croît avec le nombre de joueurs distincts depuis le démarrage. Une jauge de **sessions résidentes** sert d'indicateur de capacité. |
| **Dépendance à un fournisseur facturé à l'usage**, avec un historique de conversation jamais tronqué | Le coût par appel croît mécaniquement au fil de la partie. Une sonde suit la **taille du contexte** envoyé. |

Ces choix distinguent le dispositif d'une supervision générique : les deux sondes les plus
importantes (mode de narration, taille de contexte) n'auraient aucun sens sur une application web
classique.

## Périmètre de supervision

| Couche | Objet supervisé | Moyen |
|---|---|---|
| **Application** | Trafic, latence, erreurs, sondes métier et sécurité | Instrumentation Prometheus dans `backend/monitoring.py`, exposée sur `/api/metrics` |
| **Dépendances internes** | Base SQLite, fiche de personnage, prompt, répertoire de sauvegarde | Sonde d'aptitude `/api/health/ready` |
| **Dépendance externe** | Fournisseur LLM (OpenAI) | Sondes `rpg40k_gm_*` |
| **Chaîne d'accès utilisateur** | Reverse proxy Nginx et frontend | Sonde « boîte noire » (`blackbox-exporter`) interrogeant l'application depuis l'extérieur |
| **Collecteur** | Prometheus lui-même | Auto-supervision (`job_name: prometheus`) |

L'auto-supervision du collecteur est délibérée : sans elle, l'arrêt de Prometheus produirait un
silence indistinguable d'une absence d'incident.

## Sondes mises en place et finalité

### Sondes de disponibilité

La distinction **vivacité / aptitude** est structurante et suit la séparation classique
*liveness* / *readiness* :

| Sonde | Route | Finalité | Effet d'un échec |
|---|---|---|---|
| **Vivacité** | `GET /api/health` | Atteste que le processus répond | Redémarrage du conteneur par Docker (`healthcheck`) |
| **Aptitude** | `GET /api/health/ready` | Vérifie réellement les dépendances | Retour **503** et retrait du trafic, **sans** redémarrage |

Cette séparation évite un piège d'exploitation : si la sonde de redémarrage vérifiait la base de
données, une indisponibilité disque déclencherait une **boucle de redémarrage** aggravant la panne
au lieu de la contenir.

La sonde d'aptitude effectue quatre contrôles **actifs** :

1. `SELECT count(*) FROM users` — une requête réelle, non un simple test d'existence de fichier ;
2. présence et taille non nulle de `character_sheet.yaml` ;
3. présence et taille non nulle de `prompt_survivant.md` ;
4. écriture puis suppression d'un fichier témoin dans le répertoire de sauvegarde.

Résultat observé en fonctionnement nominal :

```json
{
  "status": "ready",
  "checks": {
    "database":        { "ok": true },
    "character_sheet": { "ok": true },
    "prompt_file":     { "ok": true },
    "save_dir":        { "ok": true }
  },
  "llm_configured": false
}
```

### Sondes applicatives

| Sonde | Type | Finalité |
|---|---|---|
| `rpg40k_http_requests_total{method,endpoint,status_class}` | Compteur | Trafic et taux d'erreur par famille de code (2xx/4xx/5xx) |
| `rpg40k_http_request_duration_seconds{method,endpoint}` | Histogramme | Distribution des temps de réponse, calcul des centiles |
| `rpg40k_http_exceptions_total{endpoint,exception}` | Compteur | Exceptions non gérées remontées au middleware |
| `rpg40k_ready`, `rpg40k_dependency_up{dependency}` | Jauges | État des dépendances internes |

### Sondes de la dépendance LLM — cœur du dispositif

| Sonde | Type | Finalité |
|---|---|---|
| `rpg40k_gm_generations_total{mode}` | Compteur | Distingue `openai`, `local_fallback` et `local_no_key` |
| `rpg40k_gm_generation_duration_seconds{mode}` | Histogramme | Temps de génération perçu par le joueur |
| `rpg40k_gm_errors_total{reason}` | Compteur | Nature des échecs (délai, quota, authentification) |
| `rpg40k_gm_context_messages` | Histogramme | Croissance de l'historique envoyé au LLM |

Le libellé `mode` est ce qui rend la **dégradation observable**. Le code correspondant marque le
mode réellement utilisé, y compris lors du repli :

```python
except Exception as exc:
    mode = "local_fallback"
    GM_ERRORS.labels(reason=type(exc).__name__).inc()
    log.error("Bascule en mode degrade : fournisseur LLM indisponible (%s: %s)", ...)
```

### Sondes de sécurité et de capacité

| Sonde | Type | Finalité |
|---|---|---|
| `rpg40k_auth_attempts_total{action,result}` | Compteur | Détection de tentatives d'authentification répétées |
| `rpg40k_active_sessions` | Jauge | Sessions résidentes en mémoire (indicateur de capacité) |
| `rpg40k_sse_streams_active` | Jauge | Flux de streaming simultanés (charge réelle) |
| `rpg40k_combats_started_total{faction}` | Compteur | Indicateur métier : variété des rencontres générées |
| `rpg40k_save_failures_total` | Compteur | Échec d'écriture — risque de perte de progression |

### Maîtrise de la cardinalité

Les chemins porteurs d'identifiants sont ramenés à leur gabarit de route avant étiquetage :

```python
/api/animations/tir_bolter      ->  /api/animations/{skill_id}
/api/animations/coup_de_grace   ->  /api/animations/{skill_id}
```

Sans cette normalisation, chaque identifiant créerait une série temporelle distincte et saturerait
le stockage du collecteur. Un test dédié vérifie que cent identifiants distincts ne produisent
qu'un seul libellé.

## Critères de qualité et de performance

Les seuils sont calibrés sur la nature réelle des traitements, mesurée sur l'application en
fonctionnement, et non repris d'un référentiel générique.

| Indicateur | Objectif | Seuil d'alerte | Justification |
|---|---|---|---|
| **Disponibilité** de l'API | ≥ 99 % mensuel | Injoignable > 1 min | Jeu solo non critique : une indisponibilité brève est tolérable, une panne prolongée ne l'est pas |
| **Latence p95** des routes de jeu | < 250 ms | > 1 s pendant 10 min | Les actions de jeu sont des calculs en mémoire ; mesure réelle : **1,0 ms** en moyenne sur `/api/roll` |
| **Latence de `/api/auth/login`** | < 500 ms | — | Mesure réelle : **~230 ms** (p95 mesuré à 287 ms), dont **219 ms de `bcrypt.checkpw`**. Cette lenteur est **voulue** : elle protège contre la recherche exhaustive et ne doit pas être « optimisée » |
| **Taux d'erreur 5xx** | < 1 % | > 5 % pendant 5 min | Une erreur serveur interrompt une partie en cours |
| **Narration servie par le LLM** | 100 % hors incident | ≥ 1 repli en 10 min | Toute génération en mode `local_fallback` traduit une panne du fournisseur |
| **Latence p95 de génération** | < 10 s | > 20 s pendant 10 min | Au-delà, l'attente devient perceptible et rompt le rythme de jeu |
| **Taille du contexte LLM** | < 100 messages | p95 > 200 pendant 30 min | Croissance non bornée : impact direct sur coût et latence |
| **Échecs d'authentification** | — | > 10/min pendant 5 min | Signature d'une recherche exhaustive |
| **Sessions en mémoire** | — | > 200 pendant 15 min | Absence d'expiration : indicateur de dérive mémoire |

Les paliers de l'histogramme de latence (`0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10 s`) sont
resserrés sous la seconde, là où se situe réellement la distribution des routes de jeu ; des
paliers génériques auraient concentré la quasi-totalité des observations dans un seul intervalle et
rendu le centile p95 inexploitable.

## Modalité des signalements

Le routage Alertmanager traduit la sévérité en canal et en cadence :

| Sévérité | Destinataire | Délai de groupement | Rappel | Exemples |
|---|---|---|---|---|
| **Critique** | Astreinte, notification immédiate | 10 s | 1 h | `ServiceIndisponible`, `ServiceNonPret`, `EchecSauvegarde` |
| **Majeure** | Équipe technique, heures ouvrées | 1 min | 4 h | `ModeDegradeNarration`, `TauxErreurServeurEleve`, `EchecsAuthentificationRepetes` |
| **Mineure** | Consignation seule, revue hebdomadaire | 30 s | 24 h | `ContexteConversationExcessif`, `SessionsMemoireCroissantes` |

Deux mécanismes limitent le bruit, condition d'une supervision réellement exploitée :

- **Groupement** (`group_by: [alertname, severite]`) — une panne déclenchant dix règles produit une
  notification par famille, non dix notifications ;
- **Inhibition** — lorsque `ServiceIndisponible` est actif, les alertes de latence et de taux
  d'erreur qui en découlent mécaniquement sont supprimées.

Les URL de destination ne sont jamais versionnées : elles sont injectées via les variables
d'environnement `ALERT_WEBHOOK_CRITIQUE` et `ALERT_WEBHOOK_EQUIPE`.

**13 règles d'alerte** sont définies, réparties en 5 groupes : `disponibilite` (4), 
`qualite_de_service` (3), `dependance_llm` (3), `securite` (1), `capacite` (2).

## Architecture technique

```
┌──────────────┐   scrape /api/metrics    ┌──────────────┐
│   Backend    │◄─────────────────────────│              │
│   FastAPI    │        toutes les 15 s   │  Prometheus  │
│              │                          │   (30 j de   │
│ /api/health  │                          │  rétention)  │
│ /api/health/ │                          │              │
│      ready   │                          └──────┬───────┘
│ /api/metrics │                                 │ évaluation
└──────────────┘                                 │ des 13 règles
       ▲                                         ▼
       │ sonde boîte noire            ┌──────────────────┐
┌──────┴────────┐                     │   Alertmanager   │
│   Blackbox    │                     │ routage/groupage │
│   exporter    │                     │   /inhibition    │
└───────────────┘                     └────────┬─────────┘
       ▲                                       │
┌──────┴────────┐                    ┌─────────┴──────────┐
│ Nginx + React │                    │ critique → astreinte│
│  (frontend)   │                    │ majeure  → équipe   │
└───────────────┘                    │ mineure  → journal  │
                                     └────────────────────┘
              ┌──────────────┐
              │   Grafana    │  13 panneaux, provisionnés
              │ (lecture des │  automatiquement depuis le dépôt
              │  séries)     │
              └──────────────┘
```

La pile est déployée en surcouche optionnelle, ce qui laisse la pile applicative déployable seule :

```bash
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

Prometheus, Alertmanager et Grafana n'exposent leurs ports que sur `127.0.0.1` : ils n'embarquent
pas d'authentification suffisante pour une exposition publique, et l'accès distant passe par un
tunnel SSH.

## Garantie de disponibilité permanente

Le dispositif couvre les quatre modes de défaillance identifiés :

| Mode de défaillance | Détection | Réaction |
|---|---|---|
| Processus arrêté ou figé | `up == 0` (1 min) + `healthcheck` Docker | Redémarrage automatique du conteneur, alerte critique |
| Processus vivant mais dépendance en panne | `rpg40k_ready == 0` (2 min) | Retrait du trafic (503), alerte critique, **pas** de redémarrage |
| Panne du reverse proxy ou du frontend | `probe_success == 0` (2 min) | Alerte critique — détectée même si le backend est sain |
| Service disponible mais **dégradé** | `rpg40k_gm_generations_total{mode="local_fallback"}` | Alerte majeure — mode dégradé rendu visible |

Le dernier cas est celui que la sonde initiale ne pouvait pas voir, et c'est le plus probable en
exploitation réelle : expiration de la clé API, dépassement de quota ou incident du fournisseur.

## Vérification du dispositif

**20 tests automatisés** couvrent la supervision (`tests/test_monitoring.py`), portant la suite
backend de 82 à **102 tests, tous au vert**. Ils vérifient notamment que la sonde d'aptitude
**détecte réellement** une base corrompue et un fichier de jeu absent — le défaut exact de la sonde
initiale.

Relevé obtenu sur l'application en fonctionnement, après un parcours réel (authentification
échouée puis réussie, trois jets de dés, une scène narrative, un combat) :

```
rpg40k_ready                                                           1.0
rpg40k_dependency_up{dependency="database"}                            1.0
rpg40k_dependency_up{dependency="save_dir"}                            1.0
rpg40k_auth_attempts_total{action="login",result="failure"}            1.0
rpg40k_auth_attempts_total{action="login",result="success"}            1.0
rpg40k_gm_generations_total{mode="local_no_key"}                       1.0
rpg40k_combats_started_total{faction="tyranide"}                       1.0
rpg40k_active_sessions                                                 1.0
rpg40k_http_requests_total{endpoint="/api/auth/login",...,"4xx"}       1.0
rpg40k_http_requests_total{endpoint="/api/roll",...,"2xx"}             3.0
rpg40k_http_request_duration_seconds_sum{endpoint="/api/roll"}      0.00301
```

Chaque sonde reflète fidèlement l'activité produite : l'échec d'authentification est isolé du
succès, le combat est attribué à sa faction, et la narration est correctement classée en
`local_no_key` (aucune clé API configurée sur l'environnement de test).

## Éléments de preuve dans le dépôt

| Artefact | Rôle |
|---|---|
| [`backend/monitoring.py`](../../backend/monitoring.py) | Sondes, middleware, journalisation, sonde d'aptitude |
| [`backend/api.py`](../../backend/api.py) | Routes `/api/health`, `/api/health/ready`, `/api/metrics` et instrumentation des parcours |
| [`monitoring/prometheus.yml`](../../monitoring/prometheus.yml) | Collecte, cibles, auto-supervision |
| [`monitoring/alert_rules.yml`](../../monitoring/alert_rules.yml) | 13 règles d'alerte réparties en 5 groupes |
| [`monitoring/alertmanager.yml`](../../monitoring/alertmanager.yml) | Routage par sévérité, groupement, inhibition |
| [`monitoring/grafana/dashboards/rpg40k-overview.json`](../../monitoring/grafana/dashboards/rpg40k-overview.json) | Tableau de bord d'exploitation (13 panneaux) |
| [`docker-compose.monitoring.yml`](../../docker-compose.monitoring.yml) | Déploiement de la pile de supervision |
| [`tests/test_monitoring.py`](../../tests/test_monitoring.py) | 20 tests de non-régression du dispositif |

## Synthèse de couverture des critères

| Critère d'évaluation attendu | Traitement dans ce document |
|---|---|
| **Le système de supervision est adapté à la typologie de logiciel développé** | Section *Adéquation à la typologie* : quatre caractéristiques du logiciel (dégradation silencieuse, streaming SSE, sessions en mémoire, dépendance facturée) traduites en choix de sondes et de seuils |
| **Les sondes mises en place et leur finalité sont explicitées** | Section *Sondes mises en place* : disponibilité (vivacité/aptitude), applicatives, LLM, sécurité, capacité — chacune avec son type et sa finalité |
| **Les critères de qualité et de performance sont décrits. Ils sont adaptés au projet** | Tableau *Critères de qualité et de performance* : neuf indicateurs, seuils justifiés par des mesures réelles (1,0 ms sur `/api/roll`, ~230 ms sur le login dont 219 ms de bcrypt) |
| **Le système de supervision permet de surveiller la disponibilité du logiciel** | Sections *Garantie de disponibilité permanente* et *Vérification du dispositif* : quatre modes de défaillance couverts, dont la dégradation silencieuse |
