# Charge, budget et coût du cycle de vie du jeu

**Projet :** RPG 40K Survivor — Survivant de Ruche  
**Date :** 20 septembre 2026  
**Usage :** estimation de cadrage, support à C1.4.1 et aux arbitrages C1.6.  
**Statut :** hypothèses à valider ; ni devis fournisseur, ni relevé de temps historique.

**Lecture commune aux deux soutenances :** le candidat a déjà réalisé le projet depuis son origine. Ce budget valorise la construction complète d'un périmètre comparable et ses suites, sans annoncer que le jeu reste à développer. Le [planning global du Bloc 3](../bloc3/01_METHODOLOGIE_PLANNING_RESSOURCES.md) reprend les mêmes douze lots ; les 21 jours de stabilisation sont une perspective complémentaire, pas son sujet principal. Voir [l'état commun du projet](../ETAT_PROJET_REFERENCE.md).

## 1. Trois périmètres à ne pas confondre

1. **Réalisation complète depuis zéro :** estimer ce que demanderait la construction d'un jeu de périmètre comparable à celui du projet, avec livraison exploitable.
2. **Reste à faire sur l'existant :** financer uniquement les travaux encore nécessaires. Le [lot de stabilisation C1.6](C1_6_PRECONISATIONS_CLIENT.md#5-charge-et-enveloppe-de-décision--hypothèses-à-valider) relève de ce cas.
3. **Vie en production :** héberger, surveiller, assister les utilisateurs, corriger, mettre à jour, sauvegarder et faire évoluer le jeu après sa livraison.

Le budget global est construit sur **la réalisation + les douze premiers mois après mise en production**. Ce n'est pas un exercice calendaire de douze mois incluant la construction. Pour le projet déjà développé, on ne refacture pas fictivement le développement passé : on utilise le scénario « reste à financer » de la section 6.

L'ancien montant de 25 jours-homme / 11 250 € concernait un prototype simplifié. Les 15 à 27 jours-homme de C1.6 concernent une stabilisation ciblée. Aucun des deux n'est un chiffrage complet du jeu et de sa vie en production.

## 2. Hypothèses, périmètre et limites

### Socle de l'estimation

Le périmètre est reconstitué à partir des modules [src](../../src), de [l'interface React](../../frontend/src), du [backend](../../backend), des tests et des configurations de déploiement/supervision. Il comprend notamment : personnage, dés, combat, entités et bestiaire, négociation, inventaire, progression, quêtes, monde, relations, équipe, sauvegardes, comptes, rôles, narration IA et mode local.

Le frontend couvre les parcours jouables et l'arène tactique 2D. Une enveloppe séparée couvre le générateur/visualiseur et les expérimentations 3D à profondeur comparable à l'existant ; elle ne finance pas un moteur 3D commercial complet.

### Unités de calcul

- Un jour-homme (j.h) = **7 heures de travail projet**.
- TJM de référence : **450 € HT/j.h**, hypothèse héritée du cadrage, sans validation de marché. Une équipe spécialisée pourrait avoir plusieurs tarifs.
- Les charges sont une décomposition prévisionnelle, pas des temps constatés. Les bornes ne sont ni des probabilités de réussite ni une garantie forfaitaire.
- Réserve de risque proposée : **20 % du travail humain**, sous contrôle du commanditaire. Elle n'est pas automatiquement consommée.
- Les corrections ordinaires et retests sont inclus dans les lots ; la réserve ne doit pas les compter deux fois.
- Périmètre de production initial : jeu solo accessible à plusieurs utilisateurs, sur VPS, sans multijoueur temps réel ni haute disponibilité multi-site. La charge simultanée reste à contractualiser et à tester.

### Exclusions à chiffrer séparément

Création artistique originale importante (illustrations, modèles, musique, voix), licences et droits d'exploitation de l'univers et des ressources, localisation multilingue, application mobile native, paiement, modération à grande échelle, multijoueur, audit RGAA exhaustif, pentest externe, migration majeure de données, infrastructure multi-région et astreinte 24 h/24.

Pour une exploitation commerciale, les droits sur l'univers et les ressources doivent être vérifiés : l'usage d'un nom ou d'un contenu dans un prototype ne démontre pas une autorisation commerciale. Ces exclusions empêchent de présenter ce chiffrage comme le coût d'un jeu commercial sans restriction.

## 3. Réalisation complète du périmètre technique depuis zéro

| Lot | Bas (j.h) | Haut (j.h) | Contenu / résultat attendu |
|---|---:|---:|---|
| Cadrage et conception | 5 | 8 | Besoins, risques, veille, comparaison, architecture, périmètre de recette. |
| UX et conception des écrans | 6 | 10 | Parcours, maquettes, règles d'interface et d'accessibilité ; hors production artistique lourde. |
| Domaine métier RPG | 18 | 30 | Combat, dés, bestiaire, inventaire, progression, monde, quêtes, relations, négociation, équipe et tests unitaires associés. |
| API, comptes et persistance | 10 | 16 | Contrats REST, JWT/rôles, isolation des utilisateurs, SQLite/YAML, reprise et tests de composants. |
| Interface React et combat 2D | 12 | 20 | Panneaux, commandes, états d'erreur, adaptation des écrans et tests de composants. |
| Narration IA et SSE | 8 | 14 | Intégration, streaming, fallback, erreurs fournisseur, contrôle de contexte et de dépense à valider. |
| Générateur/visualiseur et 3D expérimentale | 6 | 10 | Fonctionnalités techniques comparables au prototype, avec tests ciblés ; pas de production massive d'assets. |
| Durcissement sécurité et accessibilité | 6 | 10 | Revue transversale des accès, secrets, dépendances, clavier et lisibilité ; hors implémentations déjà comptées. |
| Qualification globale | 10 | 18 | Intégration, E2E, performance, recette utilisateur, corrections et retests transversaux. |
| Industrialisation et livraison | 6 | 10 | Environnements, Docker/CI/CD, HTTPS, sauvegarde cohérente, restauration et rollback testés. |
| Supervision et préparation à l'exploitation | 5 | 8 | Métriques, tableaux de bord, alertes et simulation de panne. |
| Pilotage, documentation et transfert | 8 | 14 | Suivi, arbitrages, procédures d'exploitation et transfert ; hors rédaction des dossiers de certification. |
| **Total hors réserve** | **100** | **168** | **700 à 1 176 heures.** |

Ces charges doivent être affinées avec un backlog accepté et des critères de fin de tâche. La présence d'un module dans le dépôt ne suffit pas à mesurer son effort ni sa qualité. L'estimation ne suppose pas que tous ces travaux restent à réaliser.

| Budget de réalisation | Bas | Haut |
|---|---:|---:|
| Travail à 450 € HT/j.h | 45 000 € | 75 600 € |
| Réserve de 20 % | 9 000 € | 15 120 € |
| **Réalisation avec réserve** | **54 000 € HT** | **90 720 € HT** |

À 4 jours projet par semaine pour une personne, la capacité avec réserve de 120 à 201,6 j.h représente environ **30 à 51 semaines**, hors attentes externes. Ce n'est pas un engagement de délai. Deux personnes ne divisent pas automatiquement cette durée par deux : conception, intégration, compétences et validations imposent des dépendances.

Les frais d'outils, d'IA et d'environnement pendant cette construction ne sont pas connus. Ils doivent être ajoutés au budget sous un poste distinct `F_build`. À temps partiel ou avec davantage d'assets, la durée et le coût changent.

## 4. Maintenance et mises à jour après mise en production

### 4.1 Maintenance corrective, préventive et adaptative

Une pipeline et des mises à jour proposées automatiquement ne suppriment pas le travail humain. Il faut qualifier les alertes, vérifier la compatibilité, tester, déployer, documenter et traiter les incidents.

| Activité récurrente | Bas (j.h/mois) | Haut (j.h/mois) | Limite |
|---|---:|---:|---|
| Surveillance et contrôles d'exploitation | 0,5 | 1 | Examiner alertes, capacité, sauvegardes, coûts IA et accès. Pas d'observation humaine permanente. |
| Mises à jour courantes et sécurité | 0,5 | 1 | Dépendances, runtime, images et système ; tests et livraison inclus. Hors migration majeure. |
| Support et corrections d'incidents | 0,5 | 1,5 | Qualification, corrections ciblées et retests ; capacité limitée, pas forfait illimité. |
| Vérifications périodiques et documentation | 0,5 | 0,5 | Préparation/reporting, exercices de restauration répartis sur l'année ; une opération longue consomme plusieurs créneaux ou la réserve. |
| **Total** | **2** | **4** | **24 à 48 j.h/an.** |

Coût hors réserve : **900 à 1 800 € HT/mois**, soit **10 800 à 21 600 € HT/an**.

Hypothèse de service : intervention planifiée en heures ouvrées. Aucun délai contractuel de résolution ni permanence 24/7 n'est compris. Un incident critique peut dépasser la capacité mensuelle : le contrat doit définir escalade, autorisation d'intervention et facturation. Une astreinte exige une offre et une organisation distinctes.

La période de garantie éventuelle doit être définie : une correction due au titre de la garantie n'est pas facturée une seconde fois en maintenance. La frontière entre garantie, support et évolution doit figurer au contrat.

### 4.2 Maintenance évolutive et mises à jour majeures

Je propose une capacité optionnelle de **12 à 36 j.h/an**, soit **5 400 à 16 200 € HT/an hors réserve**, pour des demandes priorisées. Cela représente 3 à 9 j.h par trimestre, pas la promesse d'un nombre fixe de fonctionnalités.

Exemples à arbitrer : enrichir les quêtes, améliorer un parcours d'inventaire, ajuster le combat, adapter l'intégration IA ou accompagner une montée majeure de framework. Chaque demande comprend analyse d'impact, réalisation, tests, documentation et déploiement.

Une mise à jour mineure compatible relève normalement de la maintenance courante. Une rupture majeure impliquant un portage significatif relève de ce backlog ou d'un devis distinct. Ne pas imputer la même intervention aux deux enveloppes.

Une migration PostgreSQL, l'externalisation des sessions ou du multijoueur peut dépasser la capacité annuelle : ces projets ne sont pas promis dans cette enveloppe. Les évolutions sont reportables ; les protections indispensables ne le sont pas.

### 4.3 Budget annuel de travail après livraison

| Travail annuel | Bas | Haut |
|---|---:|---:|
| Maintenance courante (24–48 j.h) | 10 800 € | 21 600 € |
| Évolutions optionnelles (12–36 j.h) | 5 400 € | 16 200 € |
| Sous-total | 16 200 € | 37 800 € |
| Réserve de 20 % | 3 240 € | 7 560 € |
| **Enveloppe annuelle avec évolutions et réserve** | **19 440 € HT** | **45 360 € HT** |

La réserve couvre un risque résiduel dans le périmètre et n'achète pas une disponibilité garantie. En cas d'incident important ou de nouvelle fonctionnalité, un arbitrage reste nécessaire.

## 5. Frais récurrents de production : enveloppes provisoires

**Ces valeurs sont des provisions de cadrage, pas des tarifs constatés ou devis fournisseurs.** Elles doivent être remplacées par des offres datées et un dimensionnement. Elles n'établissent aucun nombre de joueurs supportés. Les montants sont exprimés hors taxes ou sur une base budgétaire à normaliser selon le fournisseur.

| Poste | Bas / mois | Haut / mois | Périmètre à vérifier |
|---|---:|---:|---|
| Calcul VPS et ressources de supervision | 40 € | 100 € | RAM/CPU/espace suffisants, hors sauvegarde externe et hors préproduction. |
| Stockage de sauvegarde hors serveur | 10 € | 30 € | Volume, rétention, transfert et chiffrement à définir. |
| Préproduction / tests | 20 € | 100 € | Environnement séparé ou temporaire ; éviter un doublon s'il est inclus ailleurs. |
| Consommation IA | 50 € | 300 € | Provision uniquement ; charge, modèle et prix unitaires à mesurer. |
| Notifications / outils d'exploitation | 5 € | 25 € | Les logiciels libres n'impliquent pas nécessairement une licence payante ; poste réductible si non utilisé. |
| CI, artefacts et registre | 5 € | 30 € | Quotas gratuits éventuels et dépassements ; remplacer par le coût réel. |
| **Total mensuel provisionné** | **130 €** | **585 €** | Hors travail humain. |
| Domaine annuel | **15 €/an** | **30 €/an** | Renouvellement à vérifier. |
| **Total annuel** | **1 575 €** | **7 050 €** | 12 mois + domaine. |

Un certificat TLS peut être gratuit ; sa configuration relève de la livraison et son suivi de la maintenance. Un VPS partagé implique une quote-part explicite, pas une double facturation de tout le serveur. L'achat de matériel de développement ou ses amortissements doit être identifié si non inclus dans le TJM.

Pour l'IA, calculer par modèle : coût = (tokens entrants / 1 000 000 × prix d'entrée) + (tokens sortants / 1 000 000 × prix de sortie), puis sommer les appels, générations de modèles et éventuelles reprises. Distinguer aussi cache et autres unités facturées si applicables. Le nombre de sessions et la croissance du contexte influencent fortement la consommation.

La provision de 50 à 300 € n'est **pas un plafond technique installé**. Définir une limite approuvée, une alerte avant dépassement et un comportement au seuil (réduction de service ou fallback) fait partie des travaux à valider. Si la mesure dépasse cette provision, actualiser le budget plutôt que promettre le même service au même coût.

## 6. Synthèse : deux décisions budgétaires distinctes

### A. Construire depuis zéro + douze mois de production

| Poste | Bas | Haut |
|---|---:|---:|
| Réalisation initiale, réserve incluse | 54 000 € | 90 720 € |
| Maintenance et évolutions sur 12 mois, réserve incluse | 19 440 € | 45 360 € |
| Frais récurrents sur 12 mois | 1 575 € | 7 050 € |
| **Sous-total du périmètre chiffré** | **75 015 € HT** | **143 130 € HT** |

Ajouter `F_build` (consommations pendant la construction) et les éventuels achats/prestations exclus de la section 2. Ce sous-total n'est donc pas un prix « tout compris » ni un TCO exhaustif déjà validé. Ne pas ajouter le lot de stabilisation C1.6 à cette réalisation : il recouvre des travaux de qualité et de livraison déjà compris.

### B. Partir du jeu existant + douze mois de production

| Poste | Bas | Haut |
|---|---:|---:|
| Stabilisation C1.6, réserve incluse | 8 100 € | 14 580 € |
| Maintenance et évolutions sur 12 mois, réserve incluse | 19 440 € | 45 360 € |
| Frais récurrents sur 12 mois | 1 575 € | 7 050 € |
| **Reste à financer provisionnel sur ce périmètre** | **29 115 € HT** | **66 990 € HT** |

Ajouter les frais d'environnement pendant la stabilisation s'ils sont hors des douze mois comptés, ainsi que les prestations exclues éventuellement demandées. Le développement passé n'est pas ajouté une seconde fois. Les factures d'exploitation actuelles doivent remplacer les provisions.

### C. Année suivante, sans nouvelle refonte

- **Maintien courant sans enveloppe d'évolutions : 14 535 à 32 970 € HT/an**, soit maintenance courante + réserve de 20 % + frais récurrents.
- **Avec enveloppe d'évolutions : 21 015 à 52 410 € HT/an**, soit les postes annuels de B hors stabilisation.

Ces montants supposent le même périmètre et des tarifs constants pour la comparaison. Ils doivent être revus chaque année selon utilisateurs, incidents, changements fournisseurs et backlog ; ce ne sont pas des plafonds garantis à vie.

## 7. Engagement progressif et validation client

Avant engagement : confirmer le périmètre fonctionnel (dont 3D), les droits et assets, les objectifs de charge/disponibilité, les heures de support, les objectifs de restauration, les factures et les tarifs. Une commercialisation et une démonstration pédagogique n'impliquent pas les mêmes exigences.

Pour l'existant, commencer par le diagnostic C1.6 de 2 à 3 j.h, déjà inclus dans sa charge. À l'issue, qualifier les défauts, réestimer le reste à faire et obtenir un accord séparé sur :

1. l'investissement ponctuel de stabilisation ;
2. la capacité de maintenance et les conditions d'intervention ;
3. l'enveloppe optionnelle d'évolutions ;
4. les frais de service et la limite IA ;
5. les réserves et modalités de dépassement.

Un suivi mensuel rapproche charge réalisée, capacité restante, dépenses fournisseur, incidents et demandes d'évolution. Une revue trimestrielle priorise les mises à jour. Les réserves utilisées sont justifiées et les évolutions hors enveloppe ne sont pas engagées sans accord.

**Message client :** « La livraison ne termine pas le coût du jeu. Je distingue ce que nous construisons, ce que nous devons maintenir pour que les joueurs continuent à jouer et les nouveautés que vous souhaitez financer. Ces postes sont séparés pour vous permettre de décider sans promettre une maintenance ou des mises à jour illimitées. »