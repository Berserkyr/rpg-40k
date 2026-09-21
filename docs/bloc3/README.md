# Bloc 3 — Coordonner et piloter le projet

**Projet :** Survivant de Ruche — RPG 40K Survivor  
**Candidat :** REBIAI Nehjmehdine Karim  
**Dossier préparé le :** 20 septembre 2026  
**Référentiel utilisé :** grille d'évaluation « Expert en Développement Logiciel (RNCP 39583), BC03 », PDF d'une page fourni par le candidat et lu lors de la préparation.

## 1. Le même projet complet, présenté le même jour

J'ai réalisé ce projet personnellement depuis son origine, de la conception au produit et à sa documentation. Les Blocs 1 et 3 racontent **le même jeu réalisé**, sous deux angles complémentaires ; le Bloc 3 n'est pas un nouveau projet de stabilisation à lancer.

**Phrase commune aux deux présentations :**

> Le produit existe déjà. Le Bloc 1 présente le besoin, les choix d’architecture, le périmètre et le budget du jeu complet. Le Bloc 3 présente l’organisation, la réalisation, le suivi et les arbitrages de ce même projet. Les résultats techniques locaux ne constituent ni une validation client ni une preuve de production.

Le projet n'est pas une simulation. Le RACI collectif est une **modélisation pédagogique** et non le récit d'une équipe encadrée. Le planning global et la lecture Kanban sont formalisés rétrospectivement : je ne prétends ni disposer d'un planning initial approuvé, ni avoir utilisé un tableau Kanban historique démontré. L'expérience de réalisation est réelle ; les temps historiques, échanges client et validations ne sont pas inventés.

La référence Git de cette révision est `e116b88`, avec une **copie de travail non propre**. Les suppressions locales sont conservées. L'[état de référence commun](../ETAT_PROJET_REFERENCE.md) centralise version, environnement et résultats techniques courants : **138 tests backend, 30 tests frontend et build Vite réussi**, selon le [rapport d'exécution](../preuves/VERIFICATION_LOCALE_REFERENCE.md). Aucun contrôle courant du VPS ni réception client n'est établi ici.

## 2. Fil conducteur du projet et portée des preuves

Le socle web est déjà présent dans `64f51d1` le 2 juin 2026 : cette date **n'est pas le début réel démontré** de mon travail. Les incréments de juin portent notamment sur le multiutilisateur, les tests et la configuration VPS ; juillet apporte JWT, automatisation, gameplay V1–V3, bestiaire et 3D expérimentale ; août comprend les correctifs de progression et de sauvegarde, la supervision, l'infrastructure et la documentation. Les commits `0d1af02` et `e116b88` du 20 septembre concernent les dossiers Bloc 3 et Bloc 1.

La [chronologie détaillée](01_METHODOLOGIE_PLANNING_RESSOURCES.md) sépare ces dates attestées de l'ordonnancement reconstitué. Le [tableau de bord](02_TABLEAU_DE_BORD.md) montre les livrables présents sur les douze lots, sans confondre présence, résultat vérifié et réception. L'[arbitrage sur la progression](03_CAS_ARBITRAGE.md) explique une décision réelle, sans inventer les heures ni un comité de décision.

Je présente les documents module et Bloc 4 comme des pièces historiques : ils éclairent la réalisation, mais leurs résultats et affirmations de déploiement ne valident pas automatiquement la version courante.

## 3. Correspondance avec les compétences du Bloc 3

| Compétence / livrable | Pièce | Ce que je présente | Limite explicite |
| --- | --- | --- | --- |
| **C3.1** — Méthode, planning et ressources | [01 — Méthodologie, planning et ressources](01_METHODOLOGIE_PLANNING_RESSOURCES.md) | Douze lots communs au Bloc 1 ; étude, mesure, conception, réalisation et restitution ; dépendances, dates Git séparées, charge et ressources. | Reconstitution et estimation de référence, non planning approuvé historique ; Kanban formalisé après coup. |
| **C3.2.1** — Suivi | [02 — Tableau de bord](02_TABLEAU_DE_BORD.md) | Avancement par livrables, preuves, contrôles, prévu/réalisé, risques et définitions d'indicateurs. | Outil initialisé rétrospectivement ; temps, dépenses et écarts historiques NR, pas de pourcentage global accepté. |
| **C3.2.2** — Arbitrage | [03 — Cas ANO-2026-001](03_CAS_ARBITRAGE.md) | Problème, conséquences, options, choix technique et logigramme reconstitué. | Pas de temps historique ni accord client déduit du correctif. |
| **C3.3.1** — Missions, management et communication | [04 — Missions et management](04_MISSIONS_MANAGEMENT_COMMUNICATION.md) | Fonctions assurées seul, charge de référence affectée par rôle, analyse critique, communication et adaptations. | RACI collectif pédagogique ; pas d'équipe historique inventée. Modalités du contexte individuel à confirmer avec l'organisme. |
| **C3.3.2** — Compétences et développement | [05 — Compétences et formation](05_COMPETENCES_FORMATION.md) | Expérience déjà mobilisée, preuves, limites et approfondissements ciblés après réalisation. | Pas de notes fictives ; modules optionnels non déclarés suivis. |
| **C3.4.1** — Suivi client et satisfaction | [06 — Suivi client et validations](06_SUIVI_CLIENT_VALIDATIONS.md) | CR rétrospectif du parcours complet, supports des prochains points de réception et des options, questionnaire. | CR-00 n'est pas une réunion client ; signatures, validation et satisfaction non obtenues. |
| **C3.4.2** — Démonstration | [07 — Démonstration et recette](07_DEMONSTRATION_RECETTE_CLIENT.md) | Conducteur des parcours, critères, limites et décision à recueillir. | Support à synchroniser avec la référence commune avant la séance ; une trame ne remplace pas la démonstration. |

Le [support oral](08_SUPPORT_PRESENTATION.md) reprend ce fil conducteur et assure la transition depuis le [support Bloc 1](../bloc1/SUPPORT_PRESENTATION.md). L'[arbitrage](03_CAS_ARBITRAGE.md) et la [démonstration](07_DEMONSTRATION_RECETTE_CLIENT.md) portent sur le même jeu et renvoient à la référence commune, sans dépendre des anciennes pièces RNCP ignorées par Git.

## 4. Chiffres communs et statuts à ne pas mélanger

| Périmètre | Charge / montant de référence | Signification |
| --- | --- | --- |
| **Construction complète comparable depuis zéro** | **100–168 j.h hors réserve ; 54 000–90 720 € HT avec réserve de 20 %**, à 450 €/j.h. | Référence principale des deux blocs, pas relevé de mon temps passé ni facture rétroactive. |
| Point central facultatif de construction | (100 + 168) / 2 = 134 j.h ; 160,8 j.h avec réserve ; 72 360 € HT. | Hypothèse arithmétique, pas durée constatée. |
| Capacité théorique de construction | 120–201,6 j.h avec réserve / 4 j par semaine = environ 30–51 semaines. | Dimensionnement sans date de départ historique ; aucune conclusion de dérive à partir des dates Git. |
| **Stabilisation complémentaire de l'existant** | **15–27 j.h hors réserve ; 8 100–14 580 € HT avec réserve.** Centre : 21 + 4,2 = 25,2 j.h, soit 11 340 € HT. | Option future secondaire non engagée, sans calendrier fictif ; à réestimer selon les résultats courants. |
| Maintenance + évolutions + services | **21 015–52 410 € HT/an.** | Provision annuelle après mise en production, distincte des dépenses constatées. |

Source et exclusions : [budget du cycle de vie](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md) ; option de stabilisation : [C1.6](../bloc1/C1_6_PRECONISATIONS_CLIENT.md). Je n'additionne pas reconstruction complète et stabilisation de l'existant, qui recouvrent des travaux de qualité et de livraison. Les formations optionnelles ne modifient aucune enveloppe sans décision explicite.

**NR** signifie non renseigné ou non mesuré, avec motif ; **NE** signifie niveau chiffré non évalué, pas absence d'expérience. Une preuve historique, une estimation et une proposition ne sont pas des résultats courants ou des engagements approuvés. L'évaluation du Bloc appartient au jury, pas au rédacteur.

## 5. Préparation de la soutenance et suites distinctes

| Action | Portée |
| --- | --- |
| Consolider la référence commune et identifier la version montrée. | Centraliser les résultats courants sans reprendre des totaux historiques. |
| Vérifier la cohérence des supports Bloc 1 et Bloc 3. | Même produit, douze lots, budgets, phrase commune et limites ; pas deux projets successifs. |
| Expliquer mon parcours et mes arbitrages. | Partir des livrables réels ; préciser les aides effectivement utilisées et les limites des traces, sans remettre ma réalisation au futur. |
| Préparer la démonstration et synchroniser son conducteur. | Montrer les parcours de la version retenue, annoncer les limites et consigner les observations. |
| Confirmer les modalités d'évaluation du management individuel. | La polyvalence n'est pas un encadrement d'équipe ; la modélisation pédagogique reste identifiée. |
| Organiser une réception et recueillir des retours si les interlocuteurs sont disponibles. | Pas de signature, satisfaction ou réunion reconstruite pour combler une absence. |
| Décider d'éventuels compléments et tenir désormais des relevés datés. | Autorisation, charge, coûts et échéances propres aux travaux futurs ; pas de collecte historique inventée. |

## 6. Pièces de référence accessibles dans le dépôt

- [État de référence commun](../ETAT_PROJET_REFERENCE.md), [rapport des vérifications](../preuves/VERIFICATION_LOCALE_REFERENCE.md) et [parcours fonctionnels communs](../PARCOURS_FONCTIONNELS_REFERENCE.md).
- [Budget complet et cycle de vie](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md) et [préconisations complémentaires](../bloc1/C1_6_PRECONISATIONS_CLIENT.md).
- Pièces historiques : [cadrage](../module/DOCUMENT_CADRAGE.md), [documentation technique](../module/DOC_TECHNIQUE.md), [modèle de données](../module/MCD_MLD.md), [maquettes](../module/WIREFRAMES.md), [manuel utilisateur](../module/MANUEL_UTILISATION.md).
- Pièces historiques : [anomalie ANO-2026-001](../bloc4/03_collecte_consignation_anomalies.md), [supervision](../bloc4/02_systeme_supervision.md), [support client](../bloc4/08_support_client.md).
- Synthèse de décision : [arbitrage](03_CAS_ARBITRAGE.md) ; support de séance : [démonstration](07_DEMONSTRATION_RECETTE_CLIENT.md).

Les anciennes pièces, captures et exports ne sont pas supprimés ni régénérés. Leur âge et leur statut doivent rester visibles lors de leur utilisation.
