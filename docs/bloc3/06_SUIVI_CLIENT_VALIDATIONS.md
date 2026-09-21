# C3.4.1 — Comptes rendus, validations et satisfaction

**Révision :** 20 septembre 2026.  
**Statut :** compte rendu rétrospectif de mon projet complet et supports des prochains points de réception ; pas de réunion client passée reconstituée. Signature, réception et satisfaction non obtenues.

## 1. Compte rendu CR-00 — Bilan rétrospectif du parcours complet, 20 septembre 2026

**Auteur et réalisation :** j'ai conçu et réalisé personnellement le projet de bout en bout.

**Nature :** bilan écrit de cette réalisation, destiné à expliquer le parcours et à préparer une réception. Ce n'est ni une réunion client tenue ni une relation client simulée passée.

**Périmètre :** jeu complet, douze lots communs aux Blocs 1 et 3 ; référence Git `e116b88`, copie locale non propre. Les suppressions locales sont conservées.

**Résultats techniques courants :** voir l'[état de référence commun](../ETAT_PROJET_REFERENCE.md) et le [rapport des vérifications locales](../preuves/VERIFICATION_LOCALE_REFERENCE.md) : 138 tests backend, 30 frontend et build Vite réussi. Ces vérifications complètent le bilan ; aucun état de production n'est déduit du dépôt et aucun contrôle courant du VPS n'est établi ici.

**Diffusion au commanditaire :** non attestée ; interlocuteur à confirmer.  
**Décision du commanditaire :** non recueillie.

### Parcours de réalisation et bénéfices recherchés

| Étape et repères | Ce que j'ai réalisé / bénéfice pour le joueur ou l'exploitant | Limite de la preuve |
| --- | --- | --- |
| Étude et conception : [cadrage](../module/DOCUMENT_CADRAGE.md), [maquettes](../module/WIREFRAMES.md), [modèle de données](../module/MCD_MLD.md), pièces historiques. | Définir un jeu web narratif, ses parcours, sa structure et sa persistance. | Ces supports expliquent les choix ; ils ne constituent pas des validations client datées. |
| `64f51d1`, 02/06 : socle web déjà présent. | Rendre le jeu accessible par une interface et une API. | Ce repère ne démontre pas le début réel du travail, qui n'est pas daté ici. |
| `def2fec`, 04/06 ; `c1327d5` et `3c4a5c8`, 05/06. | Ajouter base multiutilisateur et E2E, tests frontend et configuration VPS. | Qualification et livraison préparées ; pas preuve du fonctionnement public courant. |
| `7da31cf`, 10/07 ; `d7c1bd0`, 11/07. | Faire évoluer les accès JWT, leur documentation et la configuration de déploiement automatique. | Configuration et réception sont deux choses différentes. |
| `b565b39`, `7d9bf12`, `19df4a2`, 12/07 ; `b623142`, 13/07 ; `d419b7f`, 14/07. | Enrichir le gameplay V1–V3, le bestiaire et le générateur 3D expérimental. | Incréments réels, sans effort historique mesuré ni acceptation de chaque lot. |
| `4ec094c` et `68f0495`, 19/08. | Protéger la progression face aux marqueurs invalides et améliorer la sauvegarde de fiche personnage. | [Arbitrage réel analysé](03_CAS_ARBITRAGE.md) ; une correction ciblée ne garantit pas toute la reprise après incident. |
| `2bab2f0`, 19/08 ; `82a5aba` et `6119aab`, 20/08. | Ajouter supervision, observation d'infrastructure et documentation. | Les [pièces historiques du Bloc 4](../bloc4/README.md) ne valent pas contrôle courant des alertes ou du VPS. |
| `0d1af02` et `e116b88`, 20/09. | Formaliser les dossiers Bloc 3 et Bloc 1 autour de la même réalisation. | Restitution rétrospective, pas approbation client ni preuve de production. |

### Bilan et décisions restant à obtenir

| Sujet | Bilan de mon projet | Décision ou vérification complémentaire |
| --- | --- | --- |
| Périmètre | Le jeu est réalisé et les livrables couvrent les douze lots ; critères de réception non approuvés. | Convenir du périmètre effectivement présenté, des réserves et des exclusions, sans recommencer fictivement le projet. |
| Qualité et livraison | Incréments, tests et correctifs existent ; copie locale modifiée. | Relier les résultats de la référence commune à la version montrée, conserver le travail local et qualifier la reconstruction. |
| Continuité et exploitation | Sauvegardes, automatisation et supervision préparées. | Qualifier restauration, rollback, accès publics, notifications, capacité et coût IA avant autorisation d'exploitation. |
| Coût de construction | Référence comparable depuis zéro : 100–168 j.h, 54 000–90 720 € HT réserve incluse. | Utiliser ce montant pour expliquer le périmètre, pas comme facture rétroactive ni charge restante. |
| Délai historique | Incréments datés, mais début réel, temps passé et planning approuvé non établis. | Ne pas conclure à une dérive en comparant dates Git et capacité théorique. |
| Stabilisation complémentaire | Option de 15–27 j.h ; 8 100–14 580 € HT réserve incluse. | Selon les contrôles, autoriser ou non un diagnostic puis des compléments bornés. Aucun engagement acquis. |
| Vie du produit | Maintenance + évolutions + services : provision de 21 015–52 410 € HT/an. | Choisir séparément service attendu, capacité, évolutions et frais ; pas de maintenance illimitée implicite. |

Les variantes et exclusions restent celles du [budget du cycle de vie](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md) et de [C1.6](../bloc1/C1_6_PRECONISATIONS_CLIENT.md). Le centre de stabilisation **21 + 4,2 = 25,2 j.h**, soit **11 340 € HT**, est seulement un scénario complémentaire non engagé. Je ne l'ajoute pas à la reconstruction complète et je ne lui attribue pas de dates fictives.

### Actions proposées à la suite du bilan

| Action | Responsable proposé | Échéance / condition | État |
| --- | --- | --- | --- |
| Identifier l'interlocuteur habilité à recevoir le produit et convenir des critères. | Moi + interlocuteur à confirmer | Avant réception ; date à convenir | Accord non obtenu |
| Relier la version montrée aux résultats courants et aux limites. | Moi | Avant démonstration | Se reporter à la référence commune |
| Organiser les observations utilisateur et recueillir les retours. | Moi + participants volontaires | Selon disponibilités confirmées | Participation non confirmée |
| Décider des réserves et, séparément, d'un éventuel complément. | Interlocuteur habilité | Après examen des preuves | Ni signature ni autorisation obtenue |

## 2. Supports des prochains points de réception et d'options complémentaires

Je ne reconstruis pas des réunions de cadrage qui auraient précédé les travaux. Les points suivants portent sur **le produit déjà réalisé**, sa réception et les éventuels compléments. Leur date sera convenue avec les participants, pas déduite du planning de référence. Aucun de ces points n'est présenté comme tenu ou accepté.

| Point proposé | Condition / ordre logique | Question de décision | Support / preuve attendue | État actuel |
| --- | --- | --- | --- | --- |
| V1 — préparation de réception | Interlocuteur et périmètre identifiés | Quels parcours et limites seront examinés ? | CR-00, [tableau de bord](02_TABLEAU_DE_BORD.md), référence commune. | À organiser |
| V2 — démonstration et observations | Après accord sur V1 | Quels critères sont observés et quelles réserves restent ouvertes ? | [Conducteur](07_DEMONSTRATION_RECETTE_CLIENT.md) à synchroniser avec la version, observations et questionnaire. | Résultats de séance non recueillis |
| V3 — décision de réception | Après examen des résultats et réserves | Acceptation du périmètre, acceptation limitée ou report ? | PV, périmètre exact, réserves et actions acceptées. | Décision et signature non obtenues |
| O1 — option de stabilisation | Uniquement si un besoin complémentaire est retenu | Quel diagnostic puis quels travaux autoriser, pour quelle charge ? | Scénario secondaire, impacts, capacité et devis/accord éventuel. | Non engagé |
| O2 — option d'exploitation et de maintenance | Avant tout engagement de service | Les preuves d'exploitation et le service proposé sont-ils suffisants ? | Restauration, sécurité, notifications, objectifs et budget annuel. | Autorisation non obtenue |

La réception du périmètre démontré et l'autorisation de production sont deux décisions différentes. L'absence de réponse n'est pas une acceptation tacite. Toute option retenue aura sa propre référence de charge et de délai ; un report sera conservé, pas effacé du suivi.

## 3. Compte rendu à utiliser après chaque échange réel

Je consignerai : référence du point, date et durée réelles, participants et rôles, version présentée, besoins rappelés, faits nouveaux, écarts, options, décision, réserves, actions, responsables et échéances. La synthèse sera relue et l'accord ou les corrections conservés. Un éventuel exercice pédagogique sera identifié séparément ; il ne remplacera pas une réception réelle et ne changera pas le statut du projet réalisé.

**Ne pas recopier CR-00 comme preuve de réunion.** Les rubriques suivantes doivent être renseignées à partir de la séance :

| Élément de validation | Valeur au 20/09 |
| --- | --- |
| Interlocuteur habilité à la réception / rôle | Non confirmé |
| Date réelle et participants | Aucun échange client attesté par cette pièce |
| Version effectivement présentée | Non présentée dans cette revue |
| Décision sur périmètre et budget | Non recueillie |
| Demandes et réserves exprimées | Non recueillies ; ne pas attribuer les constats techniques au client |
| Actions acceptées et échéances | À établir pendant l'échange |
| Preuve d'accord ou de correction du CR | Non disponible |
| Signature de réception | Non obtenue |
| Satisfaction recueillie | NR : réponses non obtenues |

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
| --- | --- | --- | --- |
| Couverture d'observation | Sessions complètes / sessions prévues | 3 sessions ciblées, objectif à confirmer | 0 session documentée ici ; pas d'exécution revendiquée. |
| Satisfaction globale | Réponses 4 ou 5 à Q4 / réponses valides à Q4 | ≥ 80 %, à négocier | NR : aucune réponse. Avec 3 répondants, publier aussi le nombre brut ; 2/3 n'atteint pas 80 %. |
| Clarté des parcours | Moyenne Q1–Q3, séparée par question ; exclure NA | ≥ 4/5, à négocier | NR ; une moyenne ne remplace pas les commentaires. |
| Réussite sans aide non prévue | Parcours achevés sans aide fonctionnelle / parcours tentés | ≥ 80 %, à négocier | NR ; aménagements d'accessibilité distingués des aides de compréhension. |
| Réserves bloquantes | Nombre de problèmes empêchant un parcours essentiel | 0 avant acceptation | NR, pas « zéro défaut » faute d'observation. |
| Décisions en attente | Demandes sans réponse à l'échéance convenue | 0 à la décision de réception | NR : aucune échéance client approuvée. |

Pour chaque session : identifiant pseudonymisé, date, rôle, version, environnement, tâches tentées/réussies, aides, notes, commentaire et action associée. Conserver séparément les verbatims et l'interprétation. Avec un dénominateur nul, afficher NR et non 0 % ou 100 %.

## 5. Exploiter les retours

Qualifier un commentaire en défaut, incompréhension, demande d'évolution ou hors périmètre. Reformuler avec l'interlocuteur, créer une action liée à la version, puis indiquer priorité, charge, responsable et échéance. Restituer ce qui est retenu, différé ou refusé, avec la raison ; mesurer à nouveau après correction si le point est important.

**Limite actuelle C3.4.1 :** je présente le bilan rétrospectif de ma réalisation complète et les supports de réception. Le produit n'est pas une simulation ; en revanche, ce document n'atteste pas une relation client passée. Les échanges, signatures, décisions et réponses de satisfaction restent à recueillir, sans les déduire des résultats techniques locaux.
