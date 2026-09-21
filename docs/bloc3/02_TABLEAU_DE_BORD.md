# C3.2.1 — Tableau de bord et registre de pilotage

**Date de formalisation :** 20 septembre 2026.

**Périmètre :** jeu complet réalisé personnellement, lots L01–L12 du Bloc 1.

**Référence Git :** `e116b88`, copie de travail non propre.

**Statut :** photographie rétrospective du projet ; outil initialisé après coup, pas journal continu de temps ou de dépenses historiques.

## 1. Règles de lecture

J'ai réalisé le produit de bout en bout. Ce tableau rend visibles ce qui existe, les preuves de réalisation et ce qui reste à contrôler ou à décider. Il ne remet pas le jeu à zéro et ne le déclare pas entièrement accepté. La [WBS et le planning global](01_METHODOLOGIE_PLANNING_RESSOURCES.md) donnent le périmètre et l'estimation de référence ; l'[état de référence commun](../ETAT_PROJET_REFERENCE.md) porte les résultats techniques courants.

- **Présent / réalisé** : livrable ou incrément identifiable ; ne signifie pas que tous les critères de fin du lot sont satisfaits.
- **Résultat historique** : observation rapportée dans une pièce antérieure, à lire avec sa date et son contexte.
- **Contrôle courant** : résultat à reprendre de la référence commune avec version, environnement et preuve, sans recycler un total ancien.
- **Accepté** : décision explicite d'un interlocuteur habilité ; aucune réception client n'est obtenue dans ce dossier.
- **NR** : donnée non renseignée ou non mesurée dans ce suivi, avec motif. NR n'est ni zéro travail, ni échec, ni succès. **À décider** qualifie une option, pas une tâche déjà engagée.

Le Kanban est une formalisation rétrospective de l'organisation ; son usage historique n'est pas démontré. Le nombre de commits n'est pas une unité de charge et un pourcentage d'acceptation ne se calcule pas à partir de la seule présence de fichiers.

## 2. Avancement réel par lot : livrables, preuves et réserves

Les charges « référence » sont les estimations de construction complète, **pas les restes à faire**. J'assume les fonctions de réalisation sur toutes les lignes ; les validations externes restent distinctes.

| Lot | Référence hors réserve (j.h) | Réalisation / preuve disponible | Contrôles ou restes à qualifier |
| --- | ---: | --- | --- |
| L01 — Cadrage et conception | 5–8 | Choix et périmètre documentés dans le [cadrage historique](../module/DOCUMENT_CADRAGE.md) et le [budget commun](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md). | Approbation client du périmètre et des objectifs : non obtenue ; temps passé NR. |
| L02 — UX et conception des écrans | 6–10 | [Maquettes historiques](../module/WIREFRAMES.md), parcours dans le [manuel historique](../module/MANUEL_UTILISATION.md), socle web `64f51d1`. | Observation représentative d'usage et accessibilité à qualifier ; réception non obtenue. |
| L03 — Domaine métier RPG | 18–30 | Gameplay `b565b39`, `7d9bf12`, `19df4a2`, bestiaire `b623142` ; domaine décrit dans la [documentation technique historique](../module/DOC_TECHNIQUE.md). | Résultats courants dans la référence commune ; charge résiduelle NR avant qualification des défauts. |
| L04 — API, comptes et persistance | 10–16 | Multiutilisateur `def2fec`, JWT `7da31cf`, fiche sauvegardée `68f0495` ; [modèle de données historique](../module/MCD_MLD.md). | Reprise et isolation à relier à des résultats de la version retenue ; restauration après incident distincte. |
| L05 — Interface React et combat 2D | 12–20 | Socle web, incréments gameplay, tests frontend `c1327d5` ; [manuel historique](../module/MANUEL_UTILISATION.md). | Parcours de la version montrée et réserves à relever ; pas d'acceptation déduite des écrans. |
| L06 — Narration IA et SSE | 8–14 | Flux documenté et correction `4ec094c` ; [arbitrage progression](03_CAS_ARBITRAGE.md). | Gestion des erreurs et du contexte, dépense IA et comportement au seuil à qualifier. |
| L07 — Générateur/visualiseur et 3D expérimentale | 6–10 | Générateur `d419b7f` ; périmètre borné dans le [budget commun](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md). | Résultat de démonstration ciblée NR ici ; ne pas promettre un moteur commercial ni des assets massifs. |
| L08 — Durcissement sécurité et accessibilité | 6–10 | Mesures d'accès/JWT et contrôles décrits dans la [documentation technique historique](../module/DOC_TECHNIQUE.md). | Durcissement transversal non soldé par la présence de JWT ; TLS public, dépendances et accessibilité à qualifier. |
| L09 — Qualification globale | 10–18 | E2E `def2fec`, tests frontend `c1327d5`, [anomalie et résultats historiques](../bloc4/03_collecte_consignation_anomalies.md). | Résultats locaux courants : référence commune ; couverture métier, performance et recette client à distinguer. |
| L10 — Industrialisation et livraison | 6–10 | Configuration VPS `3c4a5c8`, automatisation `d7c1bd0`, [procédures historiques](../module/MANUEL_MISE_A_JOUR.md). | Copie locale modifiée ; reconstruction, restauration et rollback à qualifier. État courant du VPS non contrôlé. |
| L11 — Supervision et préparation à l'exploitation | 5–8 | Supervision `2bab2f0`, infrastructure `82a5aba` ; [dispositif historique](../bloc4/02_systeme_supervision.md). | Configuration ≠ notification reçue ; panne/rétablissement et exploitation courante à prouver. |
| L12 — Pilotage, documentation et transfert | 8–14 | Documentation `6119aab`, [support historique](../bloc4/08_support_client.md), [arbitrage rétrospectif](03_CAS_ARBITRAGE.md). | Transfert et réception à recueillir ; suivi formalisé après coup. Les dossiers de certification ne sont pas comptés dans cette charge. |
| **Ensemble** | **100–168** | **Des livrables existent sur les douze lots ; le produit est réalisé.** | **Pas de pourcentage global accepté ; contrôles, coûts et restes à qualifier séparément.** |

Les pièces module/Bloc 4 sont historiques. Leurs affirmations de déploiement et leurs résultats ne deviennent pas des preuves de production ou de réussite courante par simple renvoi. La chronologie détaillée des commits figure dans le [planning](01_METHODOLOGIE_PLANNING_RESSOURCES.md).

## 3. Prévu / réalisé : ce qui est comparable et ce qui ne l'est pas

Le « prévu » ci-dessous est une **référence estimative reconstituée**, non une commande initiale. Sans relevé de temps, factures et calendrier approuvé, je ne calcule pas de dérive historique.

| Dimension | Référence estimative | Réalisé / constat | Écart ou reste |
| --- | --- | --- | --- |
| Charge de construction | 100–168 j.h hors réserve ; centre hypothétique 134. | Temps passé NR : absence de timesheet, malgré une réalisation effective. | NR ; ne pas soustraire les commits ou les jours calendaires aux j.h. |
| Travail valorisé | 45 000–75 600 € HT à 450 €/j.h. | NR : valorisation réelle non calculable sans heures. | NR ; ce montant n'est pas une facture passée. |
| Réserve de construction | 20 %, soit 9 000–15 120 € HT. | Consommation NR : aucune réserve historique approuvée et suivie établie. | Ne pas déclarer la réserve disponible ou dépensée. |
| Total construction avec réserve | 54 000–90 720 € HT. | Coût réel NR ; justificatifs à rapprocher séparément. | Aucun dépassement ou gain réel calculable. |
| Délai et capacité | 30–51 semaines théoriques à 4 j/semaine, réserve incluse. | Dates d'incréments connues ; début réel et capacité historique NR. | NR : aucune comparaison de retard avec l'intervalle juin–septembre. |
| Périmètre | Douze lots communs au Bloc 1. | Livrables et incréments identifiés dans le tableau précédent. | Effort résiduel NR avant qualification ; réception non obtenue. |
| Qualité locale | Critères liés à la version et à l'environnement. | **138 tests backend, 30 tests frontend et build Vite réussi**, selon le [rapport local](../preuves/VERIFICATION_LOCALE_REFERENCE.md), avec avertissements et conditions d'isolation précisés. | Ne pas remplacer la couverture de recette par un nombre de tests. |
| Production et réception | Objectifs de service et critères à convenir. | Aucun contrôle courant du VPS ni réception client établi ici. | Vérifications et décision externe requises. |
| Maintenance + évolutions + services | 21 015–52 410 € HT/an, après mise en production. | Dépenses annuelles constatées NR. | Provision distincte de la construction ; pas une année déjà facturée. |

## 4. Indicateurs utilisables à partir de ce relevé

Je suis responsable de la collecte. Les seuils de délai, dépense et charge devront être convenus pour les travaux autorisés ; je ne les présente pas comme des engagements passés.

| Indicateur | Définition / source | Situation et règle d'actualisation |
| --- | --- | --- |
| Couverture documentaire des lots | Lots reliés à un livrable ou incrément identifié. | Douze lots documentés ; indicateur de traçabilité, pas taux d'acceptation. À revoir à chaque changement de périmètre. |
| Critères techniques satisfaits | Critères réussis / exécutés, avec exécutés / prévus, version et environnement. | Référence commune ; NR si dénominateur ou périmètre non défini. Aucun total historique recopié. |
| Charge consommée | Heures réellement saisies / 7. | Historique NR ; saisie sur les futurs travaux effectivement engagés. |
| Prévision finale d'un travail autorisé | Consommé mesuré + reste réestimé, comparés à sa référence approuvée. | NR tant que ces trois données ne sont pas établies ; ne pas utiliser 134 j.h comme consommé. |
| Coûts engagés / payés | Engagements et paiements rapprochés par justificatif. | NR ; tenir séparément valorisation du temps et sorties d'argent, sans double compte. |
| Écart d'échéance | Date prévisionnelle moins date approuvée. | NR pour l'historique ; conserver chaque révision après un accord futur. |
| Charge / capacité individuelle | Jours planifiés / jours disponibles sur une période. | Historique NR ; toute surcharge future appelle réduction du périmètre, report ou renfort confirmé. |
| Risques prioritaires | Risques ouverts de score ≥ 6. | Six dans le registre ci-dessous ; appréciations rétrospectives, non incidents tous survenus. |
| Anomalies bloquantes | Défauts confirmés empêchant un critère essentiel. | Total courant à consolider avec les contrôles ; NR n'est pas « aucun défaut ». |
| Acceptation et satisfaction | Décision signée/confirmée ; réponses valides selon le [protocole](06_SUIVI_CLIENT_VALIDATIONS.md). | Réception et signature non obtenues ; satisfaction NR. |

## 5. Registre des risques du projet complet

P et I sont cotés de 1 à 3 ; score = P × I. Ces cotations sont des appréciations de pilotage au 20 septembre, non des probabilités mesurées. Les risques restent ouverts tant que la preuve de réduction n'est pas reliée à la version concernée. Je porte leur traitement technique ; les choix de service et de budget demandent un accord distinct.

| ID / lots | Risque ou limite | P | I | Score | Traitement / preuve attendue | Point de contrôle |
| --- | --- | ---: | ---: | ---: | --- | --- |
| R01 / L10 | Reconstruction incertaine avec des suppressions locales. | 3 | 3 | 9 | Conserver le travail local, identifier la référence et démontrer sa reconstruction. | Avant livraison de cette référence. |
| R02 / L10 | Retour arrière vers une mauvaise référence. | 3 | 3 | 9 | Vérifier la capture de version et le retour effectif ; ne pas déduire le succès de la configuration. | Avant autorisation d'exploitation. |
| R03 / L04, L08 | Protection incomplète des accès, dépendances ou exposition publique. | 2 | 3 | 6 | Qualifier contrôles bloquants, rôles, secrets et TLS sur le périmètre retenu. | Revue de sécurité avant ouverture. |
| R04 / L04, L06 | Perte de progression ou sauvegarde non restaurable malgré les correctifs. | 2 | 3 | 6 | Contrôler persistance et restauration isolée ; relier les résultats au correctif et à la version. | Recette de reprise. |
| R05 / L11 | Alerte non reçue malgré une configuration présente. | 2 | 2 | 4 | Panne isolée, notification reçue et retour au nominal documentés. | Qualification d'exploitation. |
| R06 / L06, L09 | Coût IA ou capacité incompatibles avec le service souhaité. | 2 | 3 | 6 | Objectifs convenus, mesure représentative et comportement au seuil. | Avant engagement de service. |
| R07 / L12 | Dépendance à mon intervention unique, faible contradiction indépendante. | 2 | 2 | 4 | Procédures, revue externe ciblée si possible, capacité explicite pour la suite. | Transfert et maintenance. |
| R08 / L01, L09, L12 | Réception indisponible ou nouvelle demande confondue avec le périmètre réalisé. | 2 | 2 | 4 | Distinguer réserve, évolution et décision ; obtenir un interlocuteur et des critères. | Prochain point de réception. |
| R09 / Tous | Présenter estimation, équipe pédagogique ou résultat historique comme fait courant. | 2 | 3 | 6 | Référence commune, statuts explicites et discours identique dans les deux blocs. | Avant soutenance et à chaque mise à jour. |

## 6. Journal rétrospectif et décisions de suivi

| Repère | Fait / lecture de pilotage | Limite / suite |
| --- | --- | --- |
| Juin 2026 | Socle web, multiutilisateur, E2E, tests frontend et configuration VPS : construction et préparation de livraison. | Le premier commit ne date pas le début réel ; aucune charge déduite. |
| Juillet 2026 | JWT, automatisation, gameplay V1–V3, bestiaire et générateur 3D : enrichissement du jeu complet. | Pas de validations de jalons client déduites de ces incréments. |
| 19/08/2026 | `4ec094c` et `68f0495` : protection de la progression et sauvegarde de fiche ; `2bab2f0` : supervision. | [Arbitrage documenté](03_CAS_ARBITRAGE.md) ; effort et arbitrage calendaire historiques NR. |
| 20/08/2026 | `82a5aba` et `6119aab` : infrastructure et documentation. | Préparation à l'exploitation, pas attestation de production actuelle. |
| 20/09/2026 | `0d1af02` et `e116b88` : dossiers des Blocs 3 et 1 ; formalisation rétrospective du présent suivi. | Même périmètre complet et mêmes budgets ; ni historique de relevés inventé ni réception acquise. |

À partir de ce relevé, je conserverai pour chaque travail engagé : lot, date, objectif, heures réellement saisies, preuve, blocage, reste réestimé et décision. Chaque dépense sera reliée à un justificatif et une période. Une revue hebdomadaire est proposée pour les prochains travaux ; son application n'est pas revendiquée rétroactivement.

## 7. Option secondaire : stabilisation complémentaire

Le [scénario complémentaire](01_METHODOLOGIE_PLANNING_RESSOURCES.md#8-scénario-complémentaire-non-engagé--stabilisation-de-lexistant) reste **à décider** : 15–27 j.h hors réserve, 8 100–14 580 € HT réserve incluse ; centre 21 + 4,2 = 25,2 j.h, soit 11 340 € HT. Ce n'est ni le suivi principal ni une charge déjà engagée. Son consommé, son reste réestimé et ses échéances sont NR ; les résultats courants détermineront ce qui est réellement nécessaire.

**Limite du tableau :** je peux montrer le produit, ses incréments et mes arbitrages. Ce relevé ne prouve pas une collecte historique régulière des temps/coûts, le respect d'un planning approuvé, une réception client ou une production validée.
