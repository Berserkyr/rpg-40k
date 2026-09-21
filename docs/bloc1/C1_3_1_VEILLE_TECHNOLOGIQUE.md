# C1.3.1 — Veille technologique et recherche d’informations

> Cette veille documente le même projet individuel déjà réalisé que le Bloc 3. Les consultations ci-dessous conservent leur date et leur portée ; la [référence commune](../ETAT_PROJET_REFERENCE.md) précise l'état technique actualisé et ne transforme pas ces consultations en étude antérieure au développement.

**Projet :** RPG 40K Survivor — Survivant de Ruche  
**Revue documentaire :** 20 septembre 2026  
**Statut :** première formalisation, fondée sur le dépôt local et les sources ci-dessous.

## 1. Objet et limites de cette pièce

Pour cadrer l'architecture, je dois identifier les solutions disponibles, leurs contraintes et les risques qu'elles introduisent. Ma veille ne se limite donc pas à installer la dernière version d'une bibliothèque. Elle doit alimenter les critères de faisabilité, le budget et le choix comparatif de C1.3.2.

Cette pièce répond aux attendus transmis pour le Bloc 1 : **méthodologie de recherche, principales sources consultées, sources et outils de veille**. Le libellé détaillé et les critères officiels complets de C1.3.1 restent à rapprocher de la grille d'évaluation ; ce document ne vaut pas validation de la compétence.

Les consultations datées ci-dessous ont été réalisées lors de cette revue assistée. Elles ne prouvent pas une veille régulière antérieure ni une étude préalable au développement. Les outils configurés sont distingués des outils seulement proposés. Aucun nouveau scan de vulnérabilités, test de charge ou contrôle du VPS n'a été exécuté pour cette pièce.

## 2. Périmètre de recherche lié au besoin

| Axe | Question de cadrage | Conséquence attendue |
|---|---|---|
| API et streaming | Comment servir des actions REST et une narration SSE sans réécrire les règles Python ? | Comparer les backends et le coût de réutilisation du métier. |
| Capacité et persistance | Les sessions en mémoire et SQLite permettent-elles plusieurs processus ou instances ? | Identifier les prérequis et le coût d'une montée en charge. |
| Hébergement | Docker Compose sur un VPS suffit-il au périmètre actuel ? | Éviter une orchestration distribuée sans besoin démontré. |
| Sécurité | Quelles dépendances, protections d'accès et terminaisons TLS faut-il prévoir ? | Définir les risques et critères de recette avant exposition publique. |
| Interface et accessibilité | Quelles contraintes React, navigation clavier et réduction des animations ? | Intégrer l'accessibilité au périmètre, pas seulement au contrôle final. |
| Fournisseur IA | Quels changements d'API, coûts, limites et traitements de données ? | Prévoir un budget d'usage et un mode dégradé. |
| Exploitation | Comment détecter une panne sans confondre processus actif et service utilisable ? | Prévoir sondes, alertes et vérification du rétablissement. |

## 3. Méthode de recherche et de qualification

1. **Partir d'une question vérifiable.** Exemple : « la condition `service_healthy` suffit-elle à assurer la disponibilité après démarrage ? »
2. **Délimiter le contexte.** Identifier les versions déclarées, l'état des sessions, les contraintes du VPS et les fonctions réellement utilisées.
3. **Chercher une source primaire.** Documentation de l'éditeur, notes de version, avis de sécurité. Exemples de requêtes réutilisables : `site:docs.docker.com compose service_healthy`, `site:fastapi.tiangolo.com workers memory`, `site:docs.github.com dependabot groups schedule`.
4. **Qualifier l'information.** Vérifier l'auteur, la date ou version, la distinction stable/expérimental, le périmètre et les conditions d'application. Une documentation officielle décrit son produit, elle ne démontre pas sa supériorité sur un concurrent.
5. **Recouper avec le projet.** Relier la source à un fichier, un comportement ou un résultat de test. Pour une CVE, recouper l'avis éditeur et une base d'avis, puis vérifier version affectée, dépendance transitive et exposition réelle.
6. **Évaluer l'impact.** Sécurité, compatibilité, effort, coût d'exploitation, accessibilité et réversibilité. Si la source ne suffit pas, proposer un POC ou un test plutôt qu'affirmer un gain.
7. **Consigner la décision.** Conserver URL, date, synthèse reformulée, risque, décision et validation restante. Les options écartées sont aussi tracées.
8. **Réexaminer.** Réouvrir le sujet après une version majeure, une alerte applicable ou un changement de besoin.

Une réponse d'assistant ou un article de blog sert de piste, pas de preuve autonome. Je ne transmets ni secrets, ni jetons, ni données personnelles dans les recherches ou les annexes.

## 4. Sources effectivement consultées pendant la revue

| ID | Source primaire et URL | Consultation | Apport retenu | Limite |
|---|---|---|---|---|
| S01 | [Docker — ordre de démarrage Compose](https://docs.docker.com/compose/how-tos/startup-order/) | 20/09/2026 | `service_healthy` attend la réussite du healthcheck de la dépendance au démarrage. | Ne constitue pas une garantie de disponibilité continue ni un mécanisme complet de reprise. |
| S02 | [FastAPI — workers Uvicorn](https://fastapi.tiangolo.com/deployment/server-workers/) | 20/09/2026 | Plusieurs workers sont plusieurs processus ; HTTPS, mémoire et autres aspects du déploiement restent à traiter. | Aucun benchmark du RPG ; la cohérence des sessions doit être étudiée dans notre application. |
| S03 | [GitHub — référence Dependabot](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) | 20/09/2026 | La fréquence et les groupes de versions organisent la création des PR. | Configurer la détection n'atteste ni la fusion des PR ni l'absence de vulnérabilités. |

Ces pages sont évolutives : conserver une capture ou un export daté de la section utilisée avant remise. La date de consultation n'est pas la date de publication.

### Sources supplémentaires identifiées, à consulter et consigner

- [FastAPI — notes de version](https://fastapi.tiangolo.com/release-notes/) et [React — blog officiel](https://react.dev/blog) : ruptures de compatibilité et trajectoire des frameworks.
- [SQLite — cas d'usage adaptés](https://www.sqlite.org/whentouse.html) : limites de concurrence et choix de persistance.
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/), [GitHub Advisory Database](https://github.com/advisories) et [CERT-FR](https://www.cert.ssi.gouv.fr/) : recommandations et avis de sécurité à qualifier.
- [RGAA](https://accessibilite.numerique.gouv.fr/) : critères d'accessibilité à traduire en exigences.
- [Documentation OpenAI](https://platform.openai.com/docs/overview) et [tarification API](https://openai.com/api/pricing/) : compatibilité, limites et estimation de coût à dater.

Cette liste n'est pas présentée comme un historique de consultations déjà réalisées.

## 5. Outils réellement présents dans le projet

| Outil / preuve locale | Ce qui est vérifiable | Limite de la preuve |
|---|---|---|
| [Dependabot](../../.github/dependabot.yml) | Surveillance hebdomadaire pip, npm, Docker et GitHub Actions ; groupes mineures/correctifs. | L'état des exécutions et PR distantes n'a pas été vérifié ; aucune fusion automatique n'est démontrée ici. |
| [CI GitHub Actions](../../.github/workflows/ci.yml) | `pip-audit`, `npm audit` et contrôle d'obsolescence configurés à chaque push/PR. | Les commandes d'audit utilisent `|| true` : une CI verte ne prouve pas l'absence de vulnérabilités. |
| [scripts/check_updates.py](../../scripts/check_updates.py) | Lecture des versions obsolètes pip/npm, classement par changement de version majeure et sortie JSON disponible. | Analyse l'environnement Python courant, pas seulement les dépendances directes ; ce n'est pas un scanner de CVE. Certaines erreurs sont converties en liste vide et peuvent produire un faux message « aucune obsolescence ». |
| [requirements.txt](../../requirements.txt) et [frontend/package.json](../../frontend/package.json) | Périmètre des dépendances et contraintes de versions à comparer aux sources. | Les versions déclarées ne prouvent pas les versions installées en production. |
| Ce registre et [l'étude C1.3.2](C1_3_2_ETUDE_COMPARATIVE_ARCHITECTURES.md) | Capitalisation des informations et argumentaire de choix. | Un document seul ne démontre pas la régularité de la veille. |

Feedly/RSS, Google Alerts, newsletters et GitHub Watch figurent dans l'ancienne trame, mais leur usage n'est pas établi. Ils restent des options, pas des outils déclarés utilisés.

## 6. Registre initial : information → impact → décision

Les entrées suivantes sont une analyse de la revue du 20 septembre 2026. Les décisions sont des préconisations de cadrage, pas des modifications déjà déployées ni une validation client.

| ID | Source et observation locale | Information / risque retenu | Décision proposée et lien C1.3.2 | Validation restante |
|---|---|---|---|---|
| V01 | S01 + [docker-compose.yml](../../docker-compose.yml) | Le frontend attend le backend sain au lancement. Cette condition ne remplace pas les alertes et la reprise après panne. | Maintenir Compose pour le périmètre actuel, sans attribuer au healthcheck une garantie de haute disponibilité. | Tester une panne après démarrage et mesurer le rétablissement. |
| V02 | S02 + [supervision des sessions](../bloc4/02_systeme_supervision.md) | Les sessions du jeu sont conservées en mémoire ; multiplier les processus exige d'étudier leur cohérence. | Conditionner toute réplication et les scores de montée en charge à une stratégie d'état partagé/persisté. | POC multi-processus et test de charge avec contrôle des sauvegardes. |
| V03 | S03 + [configuration Dependabot](../../.github/dependabot.yml) | La collecte hebdomadaire et le regroupement existent déjà ; ils ne prouvent pas une mise à jour validée. | Conserver cet outil plutôt qu'ajouter un agrégateur redondant pour les dépendances ; prévoir une revue humaine des PR. | Conserver une PR réelle, sa CI et la décision de fusion ou de rejet. |
| V04 | Revue locale de [ci.yml](../../.github/workflows/ci.yml) | Les audits sont informatifs et leurs codes d'échec neutralisés. | Ajouter au critère sécurité de C1.3.2 une politique de blocage et d'exceptions justifiées. | Définir la sévérité bloquante et tester le comportement de la CI. |
| V05 | Revue locale de [check_updates.py](../../scripts/check_updates.py) | Une collecte en échec peut ressembler à une absence de mises à jour. | Exiger un état « collecte impossible » distinct avant de se fier au rapport. | Test d'échec réseau et correction dédiée ; non réalisés lors de cette revue. |

Pour les prochaines entrées, conserver également : auteur de la revue, version analysée, date de publication si disponible, priorité, référence du ticket/PR, résultat du test et date de réexamen. Ne pas inventer d'identifiant de ticket ni de résultat pour compléter le tableau.

## 7. Organisation proposée et indicateurs

Dans ce projet individuel, le porteur du projet assure la collecte et l'analyse. La validation d'une modification de périmètre ou de budget doit être distinguée de cette analyse technique.

| Activité | Cadence | Statut |
|---|---|---|
| Détection Dependabot | Hebdomadaire | Configurée ; activité distante à vérifier. |
| Audits et rapport d'obsolescence | Push / pull request | Configurés ; ne constituent pas une revue humaine régulière. |
| Lecture et qualification des sources | 30 minutes par semaine | Organisation proposée, non attestée rétrospectivement. |
| Synthèse et mise à jour du comparatif | Mensuelle et avant décision structurante | Organisation proposée. |
| Analyse d'une alerte applicable | Dès prise de connaissance, selon criticité/exposition | Règle proposée, pas un délai historiquement mesuré. |

Indicateurs à suivre : part des entrées avec source/date/décision complète (objectif 100 %), délai de qualification, nombre de décisions retenues/rejetées avec justification, nombre de collectes en erreur non traitées. Aucun résultat historique n'est revendiqué pour ces indicateurs.

## 8. Présentation au jury et preuves à compléter

Pour la présentation, montrer une question concrète, la source officielle, le rapprochement avec le code, puis la conséquence sur le choix architectural. Par exemple V02 explique pourquoi FastAPI peut utiliser plusieurs workers sans que le RPG soit automatiquement prêt à cette réplication.

Pièces disponibles : méthode, trois consultations datées, cinq analyses et configurations de collecte. Pièces restant à réunir : captures des sources, exemple de PR/rapport réel, validation d'une décision et plusieurs revues successives. **La base documentaire est renforcée, mais une pratique de veille durable reste à démontrer.**

La distinction entre blocs est importante : C1.3.1 utilise la veille pour éclairer le cadrage ; C1.3.2 compare et sélectionne une architecture ; C4.1.1 organise les mises à jour pendant la maintenance. Les mêmes outils peuvent alimenter ces travaux, sans rendre les compétences équivalentes.