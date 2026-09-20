# C3.4.1 — Comptes rendus, validations et satisfaction

**Révision :** 20 septembre 2026.  
**Statut :** compte rendu de revue documentaire rédigé et protocole client préparé ; échanges et validations client non attestés.

## 1. Compte rendu CR-00 — Revue de préparation, 20 septembre 2026

**Nature :** synthèse écrite issue de l'examen du dépôt, destinée à préparer une décision. Ce n'est pas une réunion client tenue.  
**Périmètre examiné :** dépôt local `6119aab`, version déclarée 1.3.0, avec modifications locales. Aucun contrôle du VPS ni nouvelle exécution des tests dans cette revue.  
**Diffusion au commanditaire :** non attestée ; interlocuteur à confirmer.  
**Décision du commanditaire :** non recueillie.

### Évolutions et améliorations vérifiables

| Évolution dans le dépôt | Bénéfice attendu pour le joueur / exploitant | Limite de la preuve |
|---|---|---|
| `4ec094c`, 19/08 : protection du traitement des marqueurs narratifs. | Éviter qu'une valeur invalide interrompe la sauvegarde et la fin du flux. | Correction dans Git et essais historiques documentés ; dernière version à retester. |
| `68f0495`, 19/08 : persistance de la fiche personnage. | Conserver davantage d'état lors de la reprise. | Ne prouve pas une restauration complète après incident. |
| `9f98298`, 19/08 : test de fin d'animation rendu déterministe. | Réduire un résultat instable de test. | Pas de résultat actuel de toute la suite. |
| `82a5aba`, 20/08 : supervision des ressources et tableau de bord infrastructure. | Observer CPU, mémoire et ressources du service. | Déploiement effectif et réception des alertes non vérifiés ici. |

### Situation et décisions demandées

| Sujet | Fait / conséquence | Proposition soumise à décision |
|---|---|---|
| Livraison | Des fichiers nécessaires à la construction sont supprimés localement. | Clarifier la référence avant reconstruction, sans écraser le travail local. |
| Continuité | Le workflow capture la version précédente après la mise à jour. | Vérifier/corriger le rollback et démontrer une restauration isolée. |
| Qualité publique | Audits informatifs, TLS externe et capacité non vérifiés. | Refuser un nouveau GO public sans preuves sur la version retenue. |
| Budget | Estimations initiales et récurrentes désormais distinctes. | Autoriser d'abord le diagnostic P01 de 2–3 j.h, inclus dans la stabilisation. |
| Délai | Proposition centrale : 21 j.h + 20 % de réserve, 4 j/semaine. | Confirmer disponibilité et dates ; aucune échéance ferme n'est acquise. |
| Service après livraison | Maintenance, évolutions et frais fournisseurs ne sont pas gratuits après ouverture. | Choisir séparément capacité de maintenance, backlog évolutif et limite IA. |

Les variantes de budget et leurs exclusions sont détaillées dans [C1.6](../bloc1/C1_6_PRECONISATIONS_CLIENT.md) et le [budget du cycle de vie](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md). Une provision ne constitue pas un engagement fournisseur.

### Actions proposées après cette revue

| Action | Responsable proposé | Échéance / condition | État |
|---|---|---|---|
| Confirmer interlocuteur, contexte réel/simulé et critères d'acceptation. | Candidat + commanditaire à identifier | J0 | À organiser |
| Revoir l'estimation et autoriser diagnostic ou réviser le périmètre. | Commanditaire | J0 | Accord non obtenu |
| Qualifier la référence technique et produire le relevé initial. | Candidat | J1, après autorisation | Non exécuté dans cette revue |
| Désigner un testeur et réserver une démonstration. | Candidat + interlocuteur | Avant J3 | Participation non confirmée |

## 2. Points de validation planifiés

Les dates reprennent le [planning indicatif](01_METHODOLOGIE_PLANNING_RESSOURCES.md). Ce sont des propositions, pas des invitations acceptées. Chaque point comporte un ordre du jour, un support transmis et une réponse écrite ; l'absence de réponse n'est jamais une acceptation tacite.

| Point | Date cible indicative | Question de décision | Support / preuve attendue | État actuel |
|---|---|---|---|---|
| J0 — cadrage de phase | 28/09/2026 | Que finance-t-on, à quelles conditions et avec quelle capacité ? | Périmètre, budget, charge cible, service attendu et participants. | À confirmer |
| J1 — référence et estimation | S1, après T03 et avant T04 | Peut-on autoriser les lots suivants sur cette baseline ? | Build/tests identifiés, anomalies, nouvelle prévision ; sans accord, suite suspendue. | Non tenu |
| J2 — exploitation | Fin S4 | Les protections et procédures sont-elles démontrées ? | Sécurité, restauration, rollback et notification. | Non tenu |
| J3 — recette | 06/11/2026, à réviser si besoin | Les parcours attendus sont-ils satisfaits ? | Rapport de recette, réserves et résultats d'observation. | Non tenu |
| J4 — démonstration / réception | 12/11/2026, à confirmer | Acceptation, acceptation limitée ou refus ? | Dernière version identifiée, démonstration, limites et PV. | Non tenu |

Ces jalons doivent contrôler l'adéquation fonctionnalités/besoin, mais aussi budget et calendrier. Un écart entraîne une décision explicite : corriger, limiter le périmètre, décaler ou arrêter. Un rendez-vous reporté reste visible dans l'historique.

## 3. Compte rendu à utiliser après chaque échange réel

Consigner immédiatement : référence du point, date et durée réelles, participants et rôles, contexte réel ou simulation, version présentée, besoins rappelés, faits nouveaux, écarts, options, décision, réserves, actions, responsables et échéances. Faire relire la synthèse ; conserver l'accord ou les corrections avec la pièce.

**Ne pas recopier CR-00 comme preuve de réunion.** Les rubriques suivantes doivent être renseignées à partir de la séance :

| Élément de validation | Valeur au 20/09 |
|---|---|
| Commanditaire / rôle / contexte | Non confirmé |
| Date réelle et participants | Aucun échange client attesté par cette pièce |
| Version effectivement présentée | Non présentée dans cette revue |
| Décision sur périmètre et budget | Non recueillie |
| Demandes et réserves exprimées | Non recueillies ; ne pas attribuer les constats techniques au client |
| Actions acceptées et échéances | À établir pendant l'échange |
| Preuve d'accord ou de correction du CR | Non disponible |

Si les échanges ont eu lieu hors du dépôt, ajouter leur trace autorisée, anonymisée si nécessaire, en conservant date et contexte. Ne pas exposer de données personnelles ou de secrets dans le dossier jury.

## 4. Protocole de satisfaction prêt à utiliser

**Population prévue :** commanditaire et testeurs représentatifs, à recruter ; distinguer leurs rôles. Objectif pratique : trois sessions courtes pour détecter des difficultés, sans prétention de représentativité statistique. Une seule session reste utile mais doit être présentée comme telle. Participation volontaire, données fictives, aucun diagnostic médical.

Après les parcours, poser sans suggérer la réponse :

1. « L'accès au jeu et le début de partie étaient-ils clairs ? » Note de 1 à 5, ou non applicable.
2. « Avez-vous compris les effets de vos actions et l'état du personnage ? » Note de 1 à 5.
3. « La sauvegarde et les conditions de reprise sont-elles compréhensibles ? » Note de 1 à 5.
4. « Globalement, cette version répond-elle au besoin présenté ? » Note de 1 à 5.
5. « Quelle difficulté faut-il corriger en priorité ? » Réponse libre.

Le testeur peut répondre à l'oral, à l'écrit ou avec un support adapté. Noter les aides nécessaires, sans transformer un besoin d'aménagement en défaut de l'utilisateur. Une note de satisfaction n'autorise pas à ignorer une faille de sécurité.

| Indicateur | Définition | Cible proposée | Résultat actuel / action |
|---|---|---|---|
| Couverture d'observation | Sessions complètes / sessions prévues | 3 sessions ciblées, objectif à confirmer | 0 session documentée ici ; pas d'exécution revendiquée. |
| Satisfaction globale | Réponses 4 ou 5 à Q4 / réponses valides à Q4 | ≥ 80 %, à négocier | NR : aucune réponse. Avec 3 répondants, publier aussi le nombre brut ; 2/3 n'atteint pas 80 %. |
| Clarté des parcours | Moyenne Q1–Q3, séparée par question ; exclure NA | ≥ 4/5, à négocier | NR ; une moyenne ne remplace pas les commentaires. |
| Réussite sans aide non prévue | Parcours achevés sans aide fonctionnelle / parcours tentés | ≥ 80 %, à négocier | NR ; aménagements d'accessibilité distingués des aides de compréhension. |
| Réserves bloquantes | Nombre de problèmes empêchant un parcours essentiel | 0 avant acceptation | NR, pas « zéro défaut » faute d'observation. |
| Décisions en attente | Demandes sans réponse à l'échéance convenue | 0 à la décision de réception | NR : aucune échéance client approuvée. |

Pour chaque session : identifiant pseudonymisé, date, rôle, version, environnement, tâches tentées/réussies, aides, notes, commentaire et action associée. Conserver séparément les verbatims et l'interprétation. Avec un dénominateur nul, afficher NR et non 0 % ou 100 %.

## 5. Exploiter les retours

Qualifier un commentaire en défaut, incompréhension, demande d'évolution ou hors périmètre. Reformuler avec l'interlocuteur, créer une action liée à la version, puis indiquer priorité, charge, responsable et échéance. Restituer ce qui est retenu, différé ou refusé, avec la raison ; mesurer à nouveau après correction si le point est important.

**Limite actuelle C3.4.1 :** le compte rendu de revue, les jalons et les instruments de collecte sont produits. Les échanges, validations réalisées et réponses de satisfaction doivent encore être recueillis ; ils ne peuvent pas être attestés par une rédaction seule.