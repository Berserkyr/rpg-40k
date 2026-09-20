# C1.6 — Préconisations et décisions proposées au client

**Projet :** RPG 40K Survivor — Survivant de Ruche  
**Auteur :** REBIAI Nehjmehdine Karim  
**Date :** 20 septembre 2026  
**Statut :** proposition pour la simulation de présentation client ; accord non obtenu.

> **Compétence transmise dans la grille :** « Proposer les décisions et les axes de solutions préconisées auprès du client en développant un argumentaire adapté afin d'obtenir son adhésion et sa validation. »

## 1. Décision proposée et besoin auquel elle répond

Je recommande de poursuivre le projet en conservant React et le backend modulaire FastAPI, puis de consacrer la prochaine étape à la fiabilité du service plutôt qu'à une réécriture. L'objectif est de permettre au joueur de se connecter, jouer, sauvegarder et reprendre une partie depuis son navigateur, tout en maîtrisant le coût d'exploitation et la dépendance au fournisseur IA.

**Ma préconisation est un GO sous conditions pour un lot de stabilisation et une recette contrôlée. Je ne recommande pas d'autoriser une nouvelle ouverture publique sur la seule base de cette revue documentaire.** L'état réel du VPS n'a pas été contrôlé ici ; cette réserve n'affirme pas que le service actuellement déployé est en panne.

Le besoin est repris du cadrage du projet, pas d'un nouvel entretien client. Dans la simulation, le commanditaire est le porteur du projet ; les attentes, le budget, le nombre de joueurs simultanés et le délai doivent être confirmés avant engagement. Le jury évalue l'argumentaire : il ne remplace pas une preuve d'accord client réellement obtenu.

## 2. Sur quelles preuves repose la recommandation ?

Je m'appuie sur [l'étude comparative C1.3.2](C1_3_2_ETUDE_COMPARATIVE_ARCHITECTURES.md) et [la veille C1.3.1](C1_3_1_VEILLE_TECHNOLOGIQUE.md), établies à partir du dépôt local au commit `6119aab` et de ses modifications locales.

| Constat | Conséquence pour le client |
|---|---|
| Les règles Python, l'API, React, les tests et Docker Compose existent. | Réutiliser cet investissement évite le coût d'un portage sans bénéfice métier démontré. |
| Une supervision Prometheus/Grafana/Alertmanager et une veille Dependabot sont configurées. | Vérifier et exploiter ces dispositifs avant d'acheter ou de développer une autre solution. Leur présence ne prouve pas leur fonctionnement en production. |
| Les audits de dépendances de la CI sont informatifs (`|| true`). | Ne pas interpréter une CI verte comme une validation de sécurité ; définir un seuil de blocage. |
| Le workflow capture `VERSION_PRECEDENTE` après la mise à jour Git. | Corriger et tester le retour arrière avant de s'y fier en incident. |
| Des fichiers nécessaires au build sont supprimés dans la copie locale examinée. | Clarifier ces suppressions avec le responsable du dépôt et vérifier une reconstruction propre ; ne pas restaurer aveuglément ses changements. |
| Les sessions sont en mémoire et la persistance repose notamment sur SQLite. | Ne pas promettre une réplication transparente ou une capacité non mesurée. |
| La configuration Nginx examinée sert du HTTP. | Vérifier une éventuelle terminaison HTTPS externe avant de conclure à la protection du parcours public. |

Les sources techniques et les limites de vérification sont détaillées dans C1.3.2. Aucun résultat récent de CI distante, de restauration ou de charge n'est revendiqué dans cette proposition.

## 3. Axes de solution : bénéfices, compromis et critères de réussite

| Réf. / priorité | Préconisation | Bénéfice pour le client | Compromis ou risque résiduel | Preuve attendue |
|---|---|---|---|---|
| P01 — préalable | Conserver React/FastAPI, clarifier les fichiers supprimés et reconstruire la version choisie. | Livrer plus directement les parcours existants et disposer d'une version identifiable. | Pas de gain de performance chiffré ; dette existante à traiter progressivement. | Build propre, référence Git et tests de cette même version. |
| P02 — avant ouverture | Vérifier HTTPS, secrets, rôles, exposition des métriques et rendre les audits bloquants selon la politique retenue. | Réduire le risque d'accès non autorisé et de diffusion de données. | Aucun audit automatisé ne couvre tous les risques ; exceptions à motiver et limiter dans le temps. | Parcours HTTPS vérifié, refus 401/403 attendus et rapport d'audit examiné. |
| P03 — avant ouverture | Tester sauvegarde/restauration et corriger le rollback. | Protéger la progression et réduire la durée d'un incident. | Une copie de fichiers SQLite pendant des écritures ne suffit pas à garantir une sauvegarde cohérente. | Restauration isolée avec contrôle de la base et d'une partie ; retour au véritable commit précédent démontré. |
| P04 — avant ouverture | Vérifier les sondes, tableaux de bord et notifications déjà configurés. | Détecter les pannes et la narration en mode dégradé avant qu'elles ne durent. | Coût CPU, RAM et stockage ; privilèges des exportateurs à encadrer. | Incident simulé, notification reçue et retour à l'état nominal constaté. |
| P05 — avant recette | Valider les parcours essentiels, l'accessibilité ciblée, une charge représentative et une limite de dépense IA. | Donner au joueur une expérience exploitable sans facture imprévisible. | Le mode narratif local reste moins riche ; une recette ciblée n'est pas un audit RGAA exhaustif. | Scénarios signés, mesures de charge et contrôle du comportement au seuil IA. |
| P06 — différé | Réexaminer PostgreSQL, l'état partagé ou l'extraction d'un service uniquement si un besoin mesuré le justifie. | Éviter le surcoût d'une architecture distribuée prématurée. | Capacité initiale volontairement limitée ; migration ultérieure à chiffrer. | Dépassement d'un objectif convenu, analyse de cause et nouvelle décision d'architecture. |

Je propose de considérer comme bloquante toute vulnérabilité critique ou élevée applicable au périmètre livré, sauf exception formalisée avec mesure compensatoire, responsable et échéance. Cette politique est à valider puis à implémenter ; elle n'est pas présentée comme déjà active.

Un conteneur déclaré `unhealthy` n'est pas automatiquement redémarré par Docker Compose du seul fait de cet état. Le healthcheck, la politique de redémarrage du processus et la procédure de reprise répondent à des besoins différents ; la recette d'exploitation doit les distinguer.

## 4. Options écartées et arbitrages explicites

| Option | Intérêt possible | Pourquoi je ne la recommande pas maintenant | Quand la réexaminer |
|---|---|---|---|
| Réécriture du backend en Node.js | Langage commun avec le frontend. | Portage des règles et nouveaux risques de régression, sans gain de service démontré. | Contrainte d'équipe ou d'intégration nouvelle, après chiffrage. |
| Microservices et Kubernetes | Déploiement indépendant de domaines et capacité distribuée. | Complexité d'exploitation et cohérence des données supplémentaires. L'installation de Kubernetes ne justifie pas son adoption. | Charge ou organisation exigeant une indépendance réelle des services. |
| Nouvelles fonctions avant stabilisation | Démonstration plus riche. | Repousse la sécurisation des sauvegardes et de la livraison. | Après acceptation du socle et arbitrage du budget restant. |
| Désactiver les contrôles pour livrer plus vite | Réduction apparente du délai. | Transfère le risque au joueur et à l'exploitant. | Non retenu pour contourner un contrôle d'accès ou une protection indispensable. |

Le périmètre proposé ne comprend ni réécriture, ni garantie de haute disponibilité multi-site, ni montée en charge illimitée. Une migration de base ne suffirait pas à elle seule à résoudre l'état des sessions en mémoire.

## 5. Charge et enveloppe de décision — hypothèses à valider

Les documents budgétaires ont été complétés par le [chiffrage du cycle de vie](C1_4_CHARGE_BUDGET_CYCLE_VIE.md). L'estimation ci-dessous reste une **proposition indicative pour le seul lot de stabilisation**, et non un devis, un temps réellement passé ou le coût total du développement initial. Sa déclinaison opérationnelle proposée figure dans le [planning du Bloc 3](../bloc3/01_METHODOLOGIE_PLANNING_RESSOURCES.md).

### 5.1 Révision de l'estimation

La première estimation de 5,5 à 9 jours-homme était trop optimiste pour ce périmètre : elle supposait surtout des vérifications nominales de dispositifs déjà fonctionnels. Elle sous-évaluait la préparation des environnements, les scénarios d'échec, les corrections suivies de nouveaux tests et les preuves de recette. Elle est remplacée par la décomposition ci-dessous, et ne constitue plus l'enveloppe recommandée.

Hypothèses : un intervenant polyvalent connaissant le projet, réutilisation du code actuel, pas de migration majeure ni de refonte graphique. Un jour-homme représente ici 7 heures de travail projet. Les bornes sont des estimations de planification fondées sur les travaux à réaliser, non des mesures issues d'un historique de temps. La borne basse suppose peu de défauts ; la haute prévoit davantage de corrections dans le même périmètre, pas une réarchitecture complète.

| Lot | Charge basse | Charge haute | Travaux inclus et livrable |
|---|---:|---:|---|
| P01 — diagnostic et baseline | 2 j | 3 j | Clarifier les suppressions, préparer l'environnement isolé, reconstruire et exécuter les tests ; rapport initial des écarts. |
| P02 — sécurité et livraison | 3 j | 5 j | Examiner TLS, secrets, rôles et exposition réseau ; qualifier les audits, appliquer les correctifs ciblés et tester la politique de blocage. |
| P03 — continuité des données | 3 j | 5 j | Préparer une sauvegarde cohérente, restaurer en isolation, corriger le rollback, simuler les échecs et contrôler l'intégrité. |
| P04 — supervision | 2 j | 4 j | Vérifier configuration et privilèges, simuler des incidents, vérifier notifications et rétablissement, ajuster les seuils. |
| P05 — recette et corrections | 3 j | 6 j | Préparer les jeux de données, tester les parcours et l'accessibilité ciblée, mesurer une charge convenue, vérifier le contrôle de dépense IA, corriger et retester. |
| Transverse — pilotage et transmission | 2 j | 4 j | Arbitrages client, consolidation des preuves et procédures, bilan de recette et transfert ; hors tests déjà comptés dans les lots. |
| **Total hors réserve** | **15 j.h** | **27 j.h** | **105 à 189 heures de travail projet.** |

Les corrections ciblées et leurs retests sont inclus dans les lots : ils ne sont pas facturés une seconde fois au titre de la réserve. Restent exclus : audit d'intrusion externe, audit RGAA exhaustif, migration de base ou des sessions, refonte du jeu, haute disponibilité multi-site et maintenance récurrente. Une découverte imposant ces travaux déclenche un nouveau chiffrage.

### 5.2 Coût et réserve de risque

Le TJM de **450 € HT/jour** reste l'hypothèse du cadrage ancien, pas un tarif de marché vérifié ni un prix accepté. Le coût augmente ici parce que le travail est mieux décomposé, pas parce qu'un tarif supérieur serait arbitrairement présenté comme plus réaliste.

| Poste | Borne basse | Borne haute |
|---|---:|---:|
| Travail estimé à 450 € HT/j.h | 6 750 € | 12 150 € |
| Réserve proposée de 20 % | 1 350 € | 2 430 € |
| **Enveloppe avec réserve** | **8 100 € HT** | **14 580 € HT** |

La réserve représente 3 à 5,4 jours-homme supplémentaires, soit une capacité budgétée de **18 à 32,4 jours-homme**. Elle couvre les incertitudes résiduelles de configuration, de compatibilité et de reprise dans le périmètre accepté. Elle n'est ni une dépense automatique ni une garantie de couverture de toute anomalie ; son utilisation doit être tracée et approuvée.

Une base de discussion centrale est **21 jours-homme + 20 % de réserve = 25,2 jours-homme**, soit **11 340 € HT à 450 €/jour**. C'est le milieu de la fourchette, pas une prévision probabiliste.

Sensibilité au tarif : à **600 € HT/jour**, hypothèse alternative non validée, le même travail avec réserve représente **10 800 à 19 440 € HT**. Un devis réel devra préciser intervenants, spécialités, tarifs et livrables.

### 5.3 Charge, calendrier et décision progressive

Pour une personne disponible 4 jours projet par semaine, 18 à 32,4 jours-homme correspondent à environ **5 à 9 semaines**, arrondies, avant éventuels délais externes d'accès, de commande ou de validation. À temps partiel, le calendrier s'allonge ; mobiliser plusieurs personnes ne divise pas mécaniquement la durée, car les lots sont dépendants.

Je propose d'autoriser d'abord **P01 : 2 à 3 jours-homme, soit 900 à 1 350 € HT** à ce TJM. Cette charge est **incluse** dans le total, pas ajoutée. À sa sortie, les anomalies sont qualifiées, le reste à faire est réestimé et le client valide ou révise l'enveloppe avant engagement des autres lots.

### 5.4 Ne pas confondre stabilisation et coût total du projet

Cette enveloppe ne couvre pas le développement initial. L'ancien cadrage évoquait 25 jours-homme et 11 250 € pour un prototype : ce montant ne représente pas le périmètre actuel. La [décomposition globale de charge et de coût du cycle de vie](C1_4_CHARGE_BUDGET_CYCLE_VIE.md) distingue désormais les scénarios suivants, sous hypothèse de 450 € HT/j.h :

| Décision | Enveloppe indicative |
|---|---:|
| Construction complète du périmètre technique depuis zéro, réserve incluse | 54 000 à 90 720 € HT (100 à 168 j.h hors réserve) |
| Maintenance courante + évolutions + frais de production sur douze mois, réserves de travail incluses | 21 015 à 52 410 € HT/an |
| Construction complète + douze mois de production | 75 015 à 143 130 € HT |
| **Stabilisation de l'existant + douze mois de production** | **29 115 à 66 990 € HT** |

Ces sous-totaux excluent notamment la production artistique lourde, les droits/licences, les audits externes et les frais d'environnement avant les douze mois de production. Les frais récurrents sont des provisions, pas des prix fournisseurs vérifiés. La pièce globale détaille les exclusions et les calculs. Ne pas additionner la stabilisation à la construction complète, car leurs travaux se recouvrent.

La maintenance courante est provisionnée à 2 à 4 j.h/mois ; les mises à jour évolutives ont une enveloppe optionnelle distincte de 12 à 36 j.h/an. La surveillance automatisée n'est pas une astreinte 24/7. Chaque évolution majeure, dépassement d'incident ou changement de charge exige un arbitrage. Les factures et tarifs IA doivent remplacer les provisions avant engagement, et une limite de dépense doit être réellement implémentée et testée.

En cas d'écart dépassant l'enveloppe approuvée, je demande un nouvel arbitrage avant d'engager le complément. Réduire le périmètre fonctionnel est préférable à supprimer une protection indispensable.

## 6. Séquencement et conditions de décision

| Jalon | Livrable de décision | Décideur / contributeur proposé | Condition de passage |
|---|---|---|---|
| J0 — cadrage | Périmètre, budget, utilisateurs simultanés cibles, coût IA et critères de recette. | Commanditaire, avec proposition du développeur. | Accord explicite et daté. |
| J1 — version de référence | Build et tests sur un commit identifié, clarification des suppressions. | Développeur / mainteneur. | Base reproductible et absence de défaut bloquant connu. |
| J2 — exploitation | Résultats P02 à P04 : protections, restauration, rollback, alertes. | Mainteneur, résultats soumis au commanditaire. | Preuves conservées et réserves qualifiées. |
| J3 — recette contrôlée | Rapport des parcours P05 et liste des anomalies résiduelles. | Joueur testeur et commanditaire. | Critères convenus satisfaits ; risques restants acceptés explicitement. |
| J4 — autorisation d'ouverture | Compte rendu GO / GO limité / NO-GO. | Commanditaire, sur avis technique. | Pas de réserve bloquante ; périmètre et capacité autorisés précisés. |

Les rôles peuvent être tenus par la même personne dans ce projet individuel, mais les décisions doivent rester distinguées. Ces jalons sont proposés : aucun testeur, accord ou rendez-vous n'est inventé.

**NO-GO pour une nouvelle ouverture** si la construction échoue, si l'intégrité restaurée n'est pas établie, si l'authentification ne protège pas les données ou si la sécurité du point d'entrée public n'est pas vérifiée. Une démo locale isolée ne vaut pas autorisation de production.

Les cibles de disponibilité, latence, RPO (perte de données acceptable) et RTO (temps de rétablissement acceptable) doivent être convenues à J0 et mesurées avant J4. Elles ne sont pas déduites d'un simple healthcheck.

## 7. Argumentaire adapté au client et réponses aux objections

**Synthèse proposée à l'oral :**

> « Votre besoin est de proposer une partie jouable et récupérable, avec un coût maîtrisé. Je recommande de conserver l'application existante plutôt que de financer une réécriture. La prochaine étape doit démontrer que nous savons reconstruire la version, protéger les accès et récupérer une partie après incident. Je propose d'abord un diagnostic de 2 à 3 jours, inclus dans un lot global de stabilisation estimé à 15 à 27 jours-homme hors réserve. À 450 euros par jour, l'enveloppe avec 20 % de réserve est de 8 100 à 14 580 euros HT, hors exploitation. Nous réestimerons le reste à faire après diagnostic, avant votre engagement sur la suite. L'ouverture publique restera conditionnée à la recette. »

> « Ce montant ne finance pas toute la vie du jeu. Il faut ensuite provisionner la maintenance, les services et les nouveautés souhaitées : le scénario avec évolutions représente 21 015 à 52 410 euros HT sur douze mois après ouverture. Nous validerons séparément ces postes, les limites de support et les devis fournisseurs. Une nouvelle fonctionnalité importante ne sera pas promise dans un forfait de maintenance illimité. »

| Question du client | Réponse proposée |
|---|---|
| Pourquoi payer pour de la stabilisation plutôt que des fonctions ? | Une nouvelle fonction a peu de valeur si la partie ne se sauvegarde pas ou ne peut pas être restaurée. La stabilisation protège l'investissement déjà réalisé. |
| Pourquoi ne pas choisir Kubernetes maintenant ? | Nous n'avons pas de charge ou d'organisation démontrant ce besoin. Ajouter une plateforme ne résout pas automatiquement la cohérence des sessions. |
| La CI est verte, pourquoi attendre ? | Les audits actuels sont informatifs ; la restauration et la sécurité publique nécessitent d'autres preuves. |
| La maintenance et les nouveautés sont-elles comprises dans la livraison ? | Non. Les corrections de recette sont comprises dans la livraison ; la garantie éventuelle doit être définie. Ensuite, maintenance courante, capacité d'évolution et services ont des enveloppes distinctes, sans double facturation. |
| Pouvez-vous garantir zéro panne ou zéro perte ? | Non. Je propose des objectifs mesurables, une sauvegarde et une reprise testées, avec des limites explicitement acceptées. |
| Peut-on livrer avec un budget inférieur ? | On peut limiter les fonctions et le nombre d'utilisateurs de la recette, mais pas déclarer une protection validée sans la tester. |

## 8. Validation à obtenir — modèle de compte rendu

**État actuel : non validé.** Compléter après l'échange réel ou la simulation, sans préremplir un accord.

| Élément | Décision / information à renseigner |
|---|---|
| Commanditaire et rôle | À renseigner ; indiquer si client fictif. |
| Date, version du document et participants | À renseigner. |
| Décision | GO stabilisation / demande de révision / NO-GO. |
| Périmètre retenu et exclusions | À confirmer. |
| Enveloppe autorisée et coûts récurrents | À confirmer, avec hypothèses et réserve. |
| Charge cible et critères de recette | À confirmer : parcours, sécurité, accessibilité, latence, restauration. |
| Réserves, responsables et échéances | À consigner individuellement. |
| Autorisation distincte d'ouverture publique | À décider après recette ; non accordée par ce document. |
| Preuve de validation | Compte rendu approuvé, courriel ou retour de simulation, selon le contexte réel. |

## 9. Correspondance avec C1.6

| Attendu | Élément de la présente pièce | Limite actuelle |
|---|---|---|
| Proposer les décisions et axes de solutions | GO sous conditions, P01 à P06 et alternatives écartées. | Proposition, non décision client acquise. |
| Développer un argumentaire adapté | Bénéfices métier, compromis, estimation et réponses aux objections. | Budget et objectifs à négocier. |
| Obtenir l'adhésion et la validation | Demande explicite de décision, jalons et modèle de compte rendu. | L'adhésion doit être obtenue lors de l'échange, pas déduite de la rédaction. |

Cette pièce prépare la présentation orale de cadrage du Bloc 1. Elle complète C1.3.2 : le comparatif explique le choix technique, tandis que C1.6 traduit ce choix en proposition compréhensible et arbitrable par le client.