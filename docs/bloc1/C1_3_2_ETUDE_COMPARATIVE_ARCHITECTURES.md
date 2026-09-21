# C1.3.2 — Étude comparative des solutions techniques et choix d’architecture

> Révision documentaire du 20 septembre 2026. Le candidat a réalisé le projet de bout en bout ; cette étude formalise les choix du produit et réévalue leur pertinence. La première revue portait sur `6119aab` ; la référence commune actualisée est `e116b88`, avec modifications locales, dans [l'état du projet](../ETAT_PROJET_REFERENCE.md). Ce n'est pas la preuve qu'une étude identique a été rédigée avant le développement. Les alternatives n'ont pas été prototypées ni soumises à des benchmarks comparatifs. Le VPS et les dernières exécutions GitHub Actions n'ont pas été contrôlés.

## 1. Contexte de décision

Le besoin du client est de disposer d’une application web RPG :

- accessible depuis un navigateur ;
- capable de gérer des règles métier riches (combat, inventaire, quêtes, progression) ;
- maintenable et démontrable devant un jury ;
- sécurisable (authentification, contrôle d’accès, gestion des secrets) ;
- déployable simplement sur VPS.

La décision C1.3.2 porte donc sur la **sélection de l’architecture technique** la plus adaptée, avec un niveau de sécurité cohérent avec le projet.

Le cadrage ancien décrit une étape antérieure : il n'est pas l'inventaire actuel. Pour la soutenance, je présente d'abord l'architecture effectivement construite et son adéquation au besoin du jeu complet, puis les alternatives et la décision actuelle de la conserver. L'effort de migration est pertinent pour cette seconde décision, mais ne doit pas servir à justifier rétrospectivement le choix initial. Le [Bloc 3](../bloc3/README.md) décrit la réalisation du même périmètre, pas d'un autre projet limité à la stabilisation.

### Sources locales vérifiées

| Preuve | Constat et limite |
|---|---|
| [docker-compose.yml](../../docker-compose.yml), [frontend/nginx.conf](../../frontend/nginx.conf) | Deux services applicatifs, proxy REST/SSE, volumes de données ; Nginx écoute en HTTP sur le port 80. Une terminaison TLS externe reste à vérifier. |
| [requirements.txt](../../requirements.txt), [frontend/package.json](../../frontend/package.json) | FastAPI, React/Vite, dépendances Python bornées et bibliothèque Prometheus ; ces manifestes ne prouvent pas les versions réellement installées sur le VPS. |
| [backend/auth.py](../../backend/auth.py) | JWT, bcrypt et contrôle des rôles ; présence de code ne vaut pas audit de sécurité complet. |
| [.github/workflows/ci.yml](../../.github/workflows/ci.yml) | Tests backend/frontend, build, E2E, audits pip/npm et contrôle d'obsolescence configurés. Les audits utilisent `|| true` et ne bloquent donc pas sur leur code d'échec. |
| [.github/dependabot.yml](../../.github/dependabot.yml) | Veille hebdomadaire des dépendances configurée ; aucune preuve de fusion automatique ou de traitement de toutes les alertes. |
| [backend/monitoring.py](../../backend/monitoring.py), [docker-compose.monitoring.yml](../../docker-compose.monitoring.yml) | Instrumentation, logs structurés et pile optionnelle Prometheus, Alertmanager, Grafana, node-exporter, cAdvisor et blackbox-exporter. Leur présence ne prouve pas leur activation en production. |
| [.github/workflows/deploy-vps.yml](../../.github/workflows/deploy-vps.yml) | Déploiement automatique conditionné par la CI, déclenchement manuel, contrôle du secret JWT et test de fumée. Le rollback nécessite une correction : `VERSION_PRECEDENTE` est capturée après la mise à jour Git. |

**Écart local à résoudre :** Git signale notamment la suppression locale du fichier de construction backend, du modèle de variables d'environnement et du fichier d'exclusions Docker. Le [relevé de référence](../ETAT_PROJET_REFERENCE.md) distingue ces suppressions de la réussite des tests et du build frontend. Je ne peux pas conclure à une reconstruction Docker reproductible depuis cette copie en l'état. Ces suppressions n'ont pas été annulées par la revue documentaire.

---

## 2. Solutions comparées

### Option A — Backend monolithique modulaire Python et frontend React séparé

- Backend FastAPI (API REST + SSE).
- Frontend React (Vite) derrière Nginx.
- Persistance SQLite + sauvegardes YAML.
- Déploiement Docker Compose.
- Pile de supervision optionnelle existante, séparée de la logique métier.

Le terme « monolithe » concerne ici les domaines métier du backend, pas un conteneur unique : React/Nginx et FastAPI sont deux services distincts. Ajouter Prometheus ne transforme pas les domaines du jeu en microservices.

### Option B — Full JavaScript (Node.js/Express + React)

- Backend Express (NestJS constituerait une variante à étudier séparément).
- Frontend React.
- Conservation de SQLite et du format de sauvegarde pour isoler le coût du changement de backend ; pas de changement simultané vers NoSQL dans cette comparaison.
- Déploiement Docker Compose.

### Option C — Microservices (Backend découpé par domaines)

- Service combat, service quêtes, service inventaire, service auth, etc.
- API Gateway + communication inter-services.
- Orchestration plus avancée (Kubernetes/Service Mesh à terme).

Kubernetes et un service mesh ne sont pas obligatoires pour des microservices. Leur adoption demanderait une justification propre ; l'installation locale d'un outil Kubernetes ne prouve pas que le projet en a besoin.

---

## 3. Critères d’évaluation

Barème : note sur 5, pondérée par l’importance métier.

Les poids et notes sont une proposition d'analyse, non une validation client ni des mesures de performance. Une note élevée signifie une meilleure adéquation au contexte actuel (1 : très défavorable ; 3 : compromis ; 5 : très favorable). Pour le déploiement, 5 signifie le plus simple. Les scores restent provisoires tant que les hypothèses de charge, de budget et les alternatives n'ont pas été validées.

| Critère | Pondération | Justification |
|---|---:|---|
| Adéquation fonctionnelle | 20% | Couvrir rapidement les besoins du jeu et du dossier RNCP. |
| Sécurité applicative | 20% | Auth, rôles, gestion des secrets, surface d’attaque. |
| Maintenabilité | 15% | Lisibilité, modularité, coût de correction. |
| Délai de réalisation | 15% | Respect du planning de formation. |
| Coût d’exploitation | 10% | Simplicité d’hébergement et d’exploitation. |
| Montée en charge future | 10% | Capacité d’évolution à moyen terme. |
| Complexité de déploiement | 10% | Fiabilité et simplicité du cycle de livraison. |

---

## 4. Matrice comparative

| Critère | Poids | Option A FastAPI+React | Option B Node+React | Option C Microservices |
|---|---:|---:|---:|---:|
| Adéquation fonctionnelle | 20 | 5 | 4 | 4 |
| Sécurité applicative | 20 | 4 | 4 | 4 |
| Maintenabilité | 15 | 4 | 4 | 3 |
| Délai de réalisation | 15 | 5 | 4 | 2 |
| Coût d’exploitation | 10 | 5 | 4 | 2 |
| Montée en charge future | 10 | 3 | 4 | 5 |
| Complexité de déploiement | 10 | 5 | 4 | 2 |
| **Score pondéré (/5)** | 100 | **4,45** | **4,00** | **3,25** |

Méthode de calcul : somme(note × poids) / 100.

### Justification des notes et réserves

- **Fonctionnel et délai :** A réutilise les règles Python déjà intégrées ; B nécessite leur portage et C un découpage des états et échanges. Les notes évaluent ce coût relatif, pas une supériorité intrinsèque de Python.
- **Sécurité :** le 4 commun représente un potentiel sous réserve de contrôles équivalents (TLS, rôles, secrets, audits, cloisonnement). Ce n'est pas une note d'audit de l'existant : les défauts et contrôles manquants ci-dessous restent à traiter.
- **Maintenabilité :** A et B permettent une séparation modulaire ; C exige aussi de maintenir les contrats réseau et de diagnostiquer les pannes distribuées.
- **Exploitation et déploiement :** les notes favorisent le faible nombre de services métier ; le coût de supervision, de stockage des métriques et des sauvegardes n'est pas nul. Aucun devis ni relevé de consommation comparatif n'a été réalisé. La note A suppose également de résoudre les suppressions locales constatées.
- **Montée en charge :** les sessions en mémoire et SQLite limitent la réplication directe de A. Le 4 de B et le 5 de C supposent une externalisation de l'état et une conception adaptées ; Node.js ou des microservices ne suffisent pas à les obtenir. Sans cette évolution, B doit être ramenée à 3 sur ce critère, soit 3,90/5.

L'écart de score guide la discussion mais ne prouve pas une capacité maximale, une disponibilité ou un coût. Une campagne de charge est nécessaire avant de dimensionner une production multi-instance.

---

## 5. Analyse sécurité par option

### Option A — FastAPI + React (retenue)

Points forts :

- authentification JWT et rôles (`player`, `admin`) déjà en place ;
- mots de passe hashés avec `bcrypt` ;
- endpoint de santé `/api/health` et architecture Docker lisible ;
- backend non publié directement par Compose ; accès via Nginx, dont l'exposition publique dépend de la configuration de déploiement.

Points de vigilance :

- durcir les secrets en production (`JWT_SECRET`, clé API) ;
- exploiter les audits déjà présents et définir un seuil de blocage des vulnérabilités : aujourd'hui leurs erreurs sont neutralisées par `|| true` ;
- vérifier l'activation de la supervision existante, la réception effective des notifications et la protection des métriques ;
- confirmer HTTPS sur le point d'entrée public : ni Compose applicatif ni Nginx interne ne suffisent à le démontrer ;
- encadrer les privilèges de supervision : cAdvisor est configuré avec `privileged: true` et des montages de l'hôte.

### Option B — Node + React

Points forts :

- homogénéité JavaScript côté front/back ;
- écosystème mature pour auth et middleware sécurité.

Limites projet :

- migration backend à refaire alors que la logique métier Python est déjà développée ;
- risque de retarder la livraison sans gain immédiat de valeur.

### Option C — Microservices

Points forts :

- scalabilité et isolation fortes à long terme ;
- cloisonnement possible des surfaces d’attaque.

Limites projet :

- complexité très élevée pour un périmètre RNCP ;
- coût de mise en place disproportionné (observabilité, orchestration, CI/CD multi-services).

---

## 6. Architecture retenue et argumentaire client

### 6.1 Décision

Je retiens l’**Option A : architecture monolithique modulaire FastAPI + React**, conteneurisée avec Docker Compose.

### 6.2 Argumentaire de décision

1. **Meilleur compromis valeur/risque/délai** pour le contexte de certification.
2. **Contrôles de sécurité implémentés** (JWT, rôles, bcrypt), sans conclure à une sécurité de production vérifiée.
3. **Déploiement prévu sur VPS** avec scripts existants, sous réserve de rétablir les fichiers locaux nécessaires et de valider la chaîne de livraison.
4. **Évolutivité maîtrisée** : possibilité d’extraire des services plus tard si la charge l’impose.
5. **Coût total maîtrisé** : peu d’infrastructure supplémentaire, maintenance plus directe.

### 6.3 Préconisations d’axes d’amélioration

- Rendre bloquants les audits existants selon une politique de sévérité explicitement définie.
- Ajouter une stratégie de rotation des secrets.
- Tester de bout en bout les alertes de la pile de supervision déjà configurée.
- Corriger et tester le retour arrière, notamment la capture du commit précédent avant mise à jour.
- Préparer une trajectoire d’évolution vers un découpage en services si volumétrie forte.

---

## 7. Schéma de l’architecture retenue

```mermaid
flowchart LR
    U[Navigateur exécutant React] -->|HTTP - TLS externe à vérifier| N[Nginx]
    N -->|Fichiers statiques React| U
    N -->|REST JSON et SSE /api| B[FastAPI Backend]
    B --> A[Authentification JWT + rôles]
    B --> M[Modules métier RPG]
    B --> D[(SQLite + YAML)]
    B --> H[/api/health]
    B --> X[OpenAI optionnel]
    P[Prometheus optionnel] -->|Collecte /api/metrics| B
    G[Grafana] -->|Requêtes| P
    P --> AM[Alertmanager]
```

---

## 8. Synthèse C1.3.2

Je recommande de conserver le backend modulaire FastAPI et le frontend React, car une réécriture ou une distribution des domaines ajouterait un coût et des risques sans besoin de charge démontré. Cette recommandation est conditionnelle : le budget réel, la charge cible, les protections de production et la restauration doivent être validés. Pour C1.3.2, cette pièce documente une comparaison argumentée de l'existant et d'alternatives ; elle ne remplace ni un benchmark ni une validation client et ne doit pas être présentée comme un audit achevé de production.
