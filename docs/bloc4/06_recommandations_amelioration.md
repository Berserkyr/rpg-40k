# 6. Recommandations argumentées d'amélioration

> **Compétence C4.3.1** — Proposer des axes d'amélioration en prenant en compte les indicateurs de
> performance et en analysant les retours utilisateurs afin de maintenir et renforcer
> l'attractivité du logiciel.

## Méthode

Les recommandations qui suivent ne sont pas des intentions générales : chacune part d'un **indicateur
mesuré** ou d'un **défaut constaté**, et se voit affecter un coût, un délai et un gain attendu.

Deux sources alimentent l'analyse :

1. **Les indicateurs de performance**, relevés par `scripts/benchmark.py`, exécutable à volonté pour
   suivre l'évolution ;
2. **Les retours utilisateurs**, collectés par le formulaire
   [`03_retour_utilisateur.yml`](../../.github/ISSUE_TEMPLATE/03_retour_utilisateur.yml).

> **Limite assumée.** Le projet n'a pas encore de base d'utilisateurs constituée : aucun retour
> réel n'a pu être analysé à ce jour. Le canal de collecte a donc été **mis en place** dans le cadre
> de cette compétence, et les recommandations ci-dessous s'appuient sur les indicateurs mesurés
> ainsi que sur les observations de jeu faites en recette. Présenter des retours fictifs aurait
> privé l'analyse de toute valeur.

Le formulaire de retour est volontairement distinct du formulaire d'anomalie : une anomalie se
**corrige**, une demande d'évolution se **priorise**. Il inclut deux champs déterminants pour
l'interprétation — la fréquence de jeu et le nombre de scènes jouées — car plusieurs limites
identifiées ci-dessous n'apparaissent qu'en partie longue.

## Indicateurs de performance mesurés

Relevé du 19/08/2026 (`python scripts/benchmark.py`) :

```
1. LATENCE DES ROUTES (ms)
   route                           p50      p95      max
   GET /api/health                2.59      3.1      3.4
   GET /api/health/ready          4.26     5.02      5.3
   POST /api/roll                  3.2     3.82     4.21
   GET /api/state                 9.97    11.02    11.83
   POST /api/auth/login         248.56   287.24   287.24

2. POIDS LIVRE AU NAVIGATEUR
   VoxelEngine-veB8hzJt.js        481.4 Ko
   index-BmjjWAYe.js              245.7 Ko
   TOTAL JS                       756.3 Ko

3. CROISSANCE DU CONTEXTE LLM (historique non tronque)
      scene     contexte    cumul envoye
          1         1209            1209
         10         3369           22897
         30         8169          140692

4. BASE DE DONNEES
   users                      87 lignes
   session_events            141 lignes
   index explicites : aucun

5. DEMARRAGE
   import du backend : 1.54 s
```

**Lecture.** Les routes de jeu sont très rapides (3 à 10 ms) : le moteur en mémoire n'est pas un
facteur limitant, et aucune optimisation n'est justifiée de ce côté. Les deux points de tension
réels sont le **poids livré au navigateur** et la **croissance du contexte LLM**.

La latence du login (248 ms) est **conforme à l'attendu** : `bcrypt.checkpw` en représente 219 ms.
C'est le coût délibéré de la protection contre la recherche exhaustive, et il ne doit pas être
réduit.

---

## R1 — Charger le moteur 3D à la demande

| | |
|---|---|
| **Indicateur** | `VoxelEngine.js` pèse **481 Ko** sur 756 Ko de JavaScript total, soit **64 % du poids livré** |
| **Constat** | Le jeu est avant tout **textuel**. Un joueur qui ne déclenche jamais de combat 3D télécharge malgré tout l'intégralité du moteur voxel et de Three.js |
| **Coût** | **Faible** — 0,5 à 1 jour |
| **Délai** | Immédiat, sans rupture fonctionnelle |
| **Gain attendu** | **−64 % de JavaScript au premier chargement** ; premier rendu nettement plus rapide, en particulier sur connexion mobile |
| **Risque** | Faible : latence au premier combat 3D, absorbable par un indicateur de chargement |

Vite produit déjà des fragments séparés (`VoxelEngine-*.js`, `Combat3DDemo-*.js`) : le découpage
existe, mais les modules sont importés statiquement. Il suffit de convertir ces imports en imports
dynamiques (`React.lazy` / `import()`) pour que le moteur ne soit téléchargé qu'à l'ouverture
effective d'une vue 3D.

**Attractivité** : le temps d'affichage initial est le premier facteur d'abandon d'une application
web. C'est la recommandation au meilleur rapport gain/effort du lot.

---

## R2 — Borner l'historique envoyé au LLM

| | |
|---|---|
| **Indicateur** | Le contexte passe de **1 209 tokens** (scène 1) à **8 169 tokens** (scène 30) ; le cumul envoyé sur une partie atteint **140 692 tokens** |
| **Constat** | `session.messages` n'est jamais tronqué : chaque scène renvoie l'intégralité de l'historique |
| **Coût** | **Faible à moyen** — 1 à 2 jours (fenêtre glissante + résumé périodique) |
| **Délai** | Court terme |
| **Gain attendu** | Croissance **linéaire au lieu de quadratique** ; latence de génération stabilisée ; plafond de contexte du modèle jamais atteint |
| **Risque** | **Moyen** — une troncature naïve fait « oublier » au maître du jeu les événements anciens |

**Argument de coût, présenté honnêtement.** Le gain financier est faible en valeur absolue :
environ **0,021 USD** par partie de 30 scènes, contre **0,015 USD** avec une fenêtre glissante de
10 messages. Ce n'est **pas** l'argument principal, et le présenter comme tel serait trompeur.

Les deux vraies justifications sont ailleurs :

1. **La latence** croît avec le contexte : au-delà de quelques dizaines de scènes, l'attente devient
   perceptible et rompt le rythme de jeu ;
2. **Le plafond de contexte** du modèle finit par être atteint en partie très longue, ce qui
   provoquerait une erreur — donc, aujourd'hui, une bascule en mode dégradé.

**Mise en œuvre recommandée** : conserver le prompt système, les *N* derniers échanges, et un
**résumé condensé** des scènes antérieures régénéré tous les 10 tours. Cette approche préserve la
continuité narrative, qui est précisément ce que le joueur perçoit.

La sonde `rpg40k_gm_context_messages`, déjà en place, permettra de mesurer le gain réel après
déploiement.

---

## R3 — Expirer les sessions conservées en mémoire

| | |
|---|---|
| **Indicateur** | Sonde `rpg40k_active_sessions`, alerte au-delà de 200 |
| **Constat** | Le dictionnaire `_sessions` de `backend/api.py` n'a **ni expiration ni éviction** : toute session créée reste résidente jusqu'au redémarrage du processus |
| **Coût** | **Faible** — 0,5 jour |
| **Délai** | Court terme |
| **Gain attendu** | Consommation mémoire bornée ; disparition d'un risque d'épuisement à long terme sur le VPS |
| **Risque** | Faible : l'état est déjà persisté sur disque et rechargé à la demande |

Une expiration après quelques heures d'inactivité suffit. La sauvegarde étant réalisée à chaque
scène, l'éviction est transparente pour le joueur : la session est simplement reconstruite à la
requête suivante.

---

## R4 — Verrouiller les versions Python installées

| | |
|---|---|
| **Constat** | Le frontend dispose de `package-lock.json` et d'une installation reproductible via `npm ci` ; le backend n'a **aucun équivalent** |
| **Coût** | **Faible** — 0,5 jour |
| **Délai** | Immédiat |
| **Gain attendu** | Installations strictement identiques entre poste de développement, CI et production |
| **Risque** | Très faible |

Les bornes hautes ajoutées au titre de C4.1.1 empêchent les montées majeures, mais deux
installations effectuées à deux dates différentes peuvent encore obtenir des versions correctives
distinctes. La génération d'un `requirements.lock.txt` (via `pip-compile` ou `pip freeze`), utilisé
par le `Dockerfile.backend` et par la CI, supprime cette dérive résiduelle.

**Réserve de faisabilité** : cette évolution modifie la construction de l'image Docker et doit être
validée sur un environnement disposant de Docker, ce qui n'a pas pu être fait dans le cadre de ce
rendu.

---

## R5 — Limiter le débit sur l'authentification

| | |
|---|---|
| **Indicateur** | Sonde `rpg40k_auth_attempts_total{result="failure"}`, alerte au-delà de 10 échecs/minute |
| **Constat** | La supervision **détecte** une recherche exhaustive mais rien ne la **bloque** |
| **Coût** | **Faible** — 0,5 jour (`slowapi` ou middleware maison) |
| **Délai** | Court terme |
| **Gain attendu** | Passage de la détection à la prévention ; protection des comptes joueurs |
| **Risque** | Faible, sous réserve d'un seuil assez haut pour ne pas gêner un joueur qui se trompe de mot de passe |

Le coût de `bcrypt` (219 ms par tentative) limite déjà mécaniquement le débit d'une attaque, mais
constitue aussi un **vecteur de déni de service** : quelques dizaines de requêtes simultanées
suffisent à saturer le processus. Une limitation par adresse IP traite les deux problèmes.

---

## R6 — Désactiver le mode debug en production ✅ *mise en œuvre*

> Cette recommandation a été **appliquée immédiatement** (version 1.3.0) : le coût
> étant inférieur à l'heure et l'enjeu relevant de la sécurité, il n'y avait pas
> lieu de la différer. Le mode est désormais piloté par la variable
> `API_DEBUG`, absente par défaut, et un test (`test_version.py`) vérifie que le
> mode debug reste désactivé.

| | |
|---|---|
| **Constat** | `backend/api.py` instanciait `FastAPI(..., debug=True)` **en dur** |
| **Coût** | **Très faible** — moins d'une heure |
| **Délai** | Immédiat |
| **Gain attendu** | Suppression de la divulgation de traces d'exécution et de code source lors d'une erreur non gérée |
| **Risque** | Nul |

La valeur doit être pilotée par variable d'environnement. Le correctif est trivial, mais la
recommandation est classée **prioritaire** car il s'agit d'une exposition d'information en
production (OWASP A05).

---

## R7 — Instaurer une rétention sur la table `session_events`

| | |
|---|---|
| **Indicateur** | 141 lignes, **aucun index explicite**, et surtout **aucune lecture** dans le code |
| **Constat** | La table est alimentée par `record_event()` mais n'est jamais interrogée : elle croît indéfiniment sans consommateur |
| **Coût** | **Faible** — 0,5 jour |
| **Délai** | Moyen terme |
| **Gain attendu** | Volumétrie maîtrisée ; ou, à l'inverse, exploitation effective de la donnée déjà collectée |
| **Risque** | Nul |

Deux options s'excluent : soit la donnée est utile — il faut alors l'exposer (historique de
connexion, tableau de bord d'administration) et l'indexer sur `user_id` ; soit elle ne l'est pas —
il faut alors instaurer une purge, voire supprimer la collecte. La conserver sans usage cumule le
coût de stockage et l'obligation de protection des données personnelles sans aucune contrepartie.

---

## R8 — Exécuter les conteneurs sans privilèges root

| | |
|---|---|
| **Constat** | Ni `Dockerfile.backend` ni `frontend/Dockerfile` ne comportent de directive `USER` |
| **Coût** | **Faible** — 0,5 jour |
| **Délai** | Moyen terme |
| **Gain attendu** | Réduction de la surface d'attaque : une exécution de code arbitraire n'obtient plus root dans le conteneur |
| **Risque** | Faible : ajuster les droits sur les volumes `/app/data` et `/app/saves` |

**Réserve de faisabilité** : comme R4, à valider sur un environnement Docker.

---

## Synthèse et priorisation

| # | Recommandation | Coût | Délai | Gain principal | Priorité |
|---|---|---|---|---|---|
| **R6** | Désactiver `debug=True` | < 1 h | **Fait (1.3.0)** | Sécurité (fuite d'information) | **1 — critique** |
| **R1** | Chargement 3D à la demande | 0,5–1 j | Immédiat | −64 % de JS au chargement | **2 — fort impact** |
| **R5** | Limitation de débit sur le login | 0,5 j | Court terme | Prévention du bourrage et du déni de service | **3** |
| **R3** | Expiration des sessions | 0,5 j | Court terme | Mémoire bornée | **4** |
| **R2** | Fenêtre glissante du contexte LLM | 1–2 j | Court terme | Latence stabilisée en partie longue | **5** |
| **R4** | Verrouillage des versions Python | 0,5 j | Immédiat | Reproductibilité des installations | **6** |
| **R7** | Rétention `session_events` | 0,5 j | Moyen terme | Volumétrie et conformité | **7** |
| **R8** | Conteneurs sans root | 0,5 j | Moyen terme | Surface d'attaque réduite | **8** |

**Charge résiduelle estimée : 4 à 5,5 jours-homme** (R6 étant déjà appliquée), soit un périmètre réaliste pour un projet de cette
taille. Aucune recommandation n'exige de refonte architecturale : toutes sont des évolutions
incrémentales, déployables une à une par le processus décrit au chapitre 5, et chacune est
vérifiable par les sondes déjà en place.

## Contribution à l'attractivité du logiciel

| Axe | Recommandations | Effet perçu par le joueur |
|---|---|---|
| **Rapidité** | R1, R2 | Démarrage plus rapide, rythme de jeu préservé en partie longue |
| **Fiabilité** | R3, R4 | Service stable dans la durée, comportement identique d'un environnement à l'autre |
| **Confiance** | R5, R6, R8 | Compte protégé, absence de fuite d'information |
| **Évolutivité** | R7 | Base saine pour un futur historique de partie |

L'attractivité d'un jeu narratif tient d'abord à la **fluidité de l'expérience** : un temps de
chargement long (R1) ou une attente croissante entre les scènes (R2) dégradent l'engagement bien
avant qu'une fonctionnalité ne manque. C'est pourquoi ces deux axes sont prioritaires sur toute
extension fonctionnelle.

## Suivi des gains

Chaque recommandation dispose d'un moyen de mesure **déjà disponible**, ce qui permettra de
vérifier le gain réel plutôt que de le supposer :

| Recommandation | Moyen de vérification |
|---|---|
| R1 | `python scripts/benchmark.py` — section *poids livré au navigateur* |
| R2 | Sonde `rpg40k_gm_context_messages` et `rpg40k_gm_generation_duration_seconds` |
| R3 | Sonde `rpg40k_active_sessions` |
| R4 | Comparaison des versions installées entre CI et production |
| R5 | Sonde `rpg40k_auth_attempts_total{result="failure"}` |
| R6 | Contrôle n° 4 de `scripts/smoke_test.sh` |
| R7 | `python scripts/benchmark.py` — section *base de données* |
| R8 | `docker compose exec backend id` |

## Éléments de preuve dans le dépôt

| Artefact | Rôle |
|---|---|
| [`scripts/benchmark.py`](../../scripts/benchmark.py) | Mesure reproductible des indicateurs de performance |
| [`.github/ISSUE_TEMPLATE/03_retour_utilisateur.yml`](../../.github/ISSUE_TEMPLATE/03_retour_utilisateur.yml) | Canal de collecte des retours d'usage |
| [`monitoring/alert_rules.yml`](../../monitoring/alert_rules.yml) | Seuils d'alerte servant d'indicateurs de suivi |

## Synthèse de couverture des critères

| Critère d'évaluation attendu | Traitement dans ce document |
|---|---|
| **Les recommandations sont argumentées et permettent d'évaluer les gains de performance en termes de coût, délai de mise en œuvre, etc.** | Huit recommandations, chacune avec indicateur mesuré, constat, coût en jours-homme, délai, gain chiffré et risque ; tableau de synthèse priorisé (4 à 6 j-h au total) |
| **Les recommandations sont réalistes et réalisables au regard du projet** | Aucune refonte architecturale ; chaque évolution est incrémentale et déployable par le processus du chapitre 5 ; les réserves de faisabilité (R4, R8 nécessitant Docker) sont explicitées |
| **Elles permettent de renforcer l'attractivité du logiciel** | Section *Contribution à l'attractivité* : quatre axes (rapidité, fiabilité, confiance, évolutivité) reliés à l'effet perçu par le joueur, avec priorisation justifiée de R1 et R2 |
