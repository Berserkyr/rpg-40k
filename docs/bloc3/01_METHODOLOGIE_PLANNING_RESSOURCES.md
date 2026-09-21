# C3.1 — Méthodologie, planning et ressources

**Projet :** Survivant de Ruche — RPG 40K Survivor  
**Auteur :** REBIAI Nehjmehdine Karim  
**Révision :** 20 septembre 2026  
**Statut :** projet réalisé personnellement de bout en bout ; organisation formalisée rétrospectivement. Le planning global est une **reconstitution et estimation de référence, non un planning approuvé historique**.

## 1. Un même projet pour les Blocs 1 et 3

J'ai réalisé le projet depuis son origine : conception, moteur de jeu, API, interface, comptes, sauvegardes, narration, tests, configurations de livraison et supervision, puis documentation. Le Bloc 1 explique le besoin, le périmètre, les choix et le budget ; ici, je présente l'organisation et les étapes de réalisation de ce même jeu. L'existence du produit ne signifie pas que sa réception client ou son exploitation en production sont validées.

La référence Git au moment de cette révision est `e116b88`, avec une **copie de travail non propre**. Les suppressions locales ne sont pas annulées. Pour la version, les contrôles locaux et leurs résultats courants, je renvoie à l'[état de référence commun](../ETAT_PROJET_REFERENCE.md) et au [rapport d'exécution](../preuves/VERIFICATION_LOCALE_REFERENCE.md). Je ne déduis pas l'état du VPS de celui du dépôt.

Je sépare trois lectures : les dates de commits attestées, l'ordre logique des travaux reconstitué, et la charge estimée d'une construction comparable depuis zéro. Ni les commits ni les documents de certification ne remplacent un relevé de temps.

## 2. Méthode : expliciter l'organisation d'une réalisation individuelle

Le **Kanban léger** est la lecture que je formalise rétrospectivement pour rendre mon organisation explicable : découper en résultats observables, relier les dépendances, traiter les anomalies et limiter la dispersion. Je ne prétends pas avoir conservé un tableau Kanban historique ni utilisé un GitHub Project alimenté pendant toute la réalisation. Les incréments et corrections sont traçables dans Git ; les cérémonies, durées et décisions client ne le sont pas par ce seul moyen.

Le [tableau de bord Markdown](02_TABLEAU_DE_BORD.md) est initialisé après coup. Il rassemble les lots présents, leurs preuves, les limites et les décisions encore nécessaires. Git permet d'en conserver les révisions ; cet outil simple convient à un projet individuel. Il n'automatise ni les dépendances ni le calcul des écarts. Un Scrum avec plusieurs rôles permanents ne décrirait pas mon organisation réelle.

Pour les prochains travaux, je propose les états « à décider, prêt, en cours, bloqué, en vérification, clos », une tâche de réalisation active au maximum et une revue hebdomadaire. Ces règles sont des améliorations du suivi, pas des pratiques historiques démontrées. Une tâche close exige une preuve de résultat ; la réception client reste une décision distincte. Une urgence touchant les données justifie un arbitrage explicite plutôt qu'un empilement de travaux parallèles.

## 3. WBS globale commune au Bloc 1

Les douze lots, leurs fourchettes et leur contenu sont repris du [budget du cycle de vie](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md). Les identifiants L01–L12 servent au suivi du Bloc 3. **Ce n'est pas une liste de travaux tous encore à faire.** Les contenus décrivent le périmètre de référence, y compris les contrôles dont le résultat reste à établir.

| ID | Lot | Bas (j.h) | Haut (j.h) | Contenu / résultat attendu |
| --- | --- | ---: | ---: | --- |
| L01 | Cadrage et conception | 5 | 8 | Besoins, risques, veille, comparaison, architecture, périmètre de recette. |
| L02 | UX et conception des écrans | 6 | 10 | Parcours, maquettes, règles d'interface et d'accessibilité ; hors production artistique lourde. |
| L03 | Domaine métier RPG | 18 | 30 | Combat, dés, bestiaire, inventaire, progression, monde, quêtes, relations, négociation, équipe et tests unitaires associés. |
| L04 | API, comptes et persistance | 10 | 16 | Contrats REST, JWT/rôles, isolation des utilisateurs, SQLite/YAML, reprise et tests de composants. |
| L05 | Interface React et combat 2D | 12 | 20 | Panneaux, commandes, états d'erreur, adaptation des écrans et tests de composants. |
| L06 | Narration IA et SSE | 8 | 14 | Intégration, streaming, fallback, erreurs fournisseur, contrôle de contexte et de dépense à valider. |
| L07 | Générateur/visualiseur et 3D expérimentale | 6 | 10 | Fonctionnalités techniques comparables au prototype, avec tests ciblés ; pas de production massive d'assets. |
| L08 | Durcissement sécurité et accessibilité | 6 | 10 | Revue transversale des accès, secrets, dépendances, clavier et lisibilité ; hors implémentations déjà comptées. |
| L09 | Qualification globale | 10 | 18 | Intégration, E2E, performance, recette utilisateur, corrections et retests transversaux. |
| L10 | Industrialisation et livraison | 6 | 10 | Environnements, Docker/CI/CD, HTTPS, sauvegarde cohérente, restauration et rollback testés. |
| L11 | Supervision et préparation à l'exploitation | 5 | 8 | Métriques, tableaux de bord, alertes et simulation de panne. |
| L12 | Pilotage, documentation et transfert | 8 | 14 | Suivi, arbitrages, procédures d'exploitation et transfert ; hors rédaction des dossiers de certification. |
| **Total hors réserve** | | **100** | **168** | **700 à 1 176 heures à 7 h/j.h.** |

Je suis l'intervenant de réalisation sur l'ensemble du périmètre. La [répartition par fonctions](04_MISSIONS_MANAGEMENT_COMMUNICATION.md) n'ajoute aucune personne ni charge à ces lots. La préparation des dossiers de certification n'est pas imputée fictivement à L12.

## 4. Planning global reconstitué : phases, dépendances et jalons logiques

Ce tableau constitue un ordonnancement de référence. Les phases de mesure et de conception reviennent à chaque incrément ; elles ne sont pas cinq périodes étanches. Les jalons ci-dessous sont des critères de lecture du parcours, **pas des réunions d'approbation historiques**.

| Phase | Travaux / lots | Dépendances structurantes | Résultat ou jalon logique | Lecture rétrospective / limite |
| --- | --- | --- | --- | --- |
| Étude | L01 ; contribution de L12 | Besoin de jeu, périmètre et contraintes à expliciter. | Besoin et architecture argumentés. | Le [cadrage historique](../module/DOCUMENT_CADRAGE.md) et le Bloc 1 documentent les choix ; la date de début réelle n'est pas établie par le premier commit. |
| Mesure initiale et continue | L09, L11 ; retours vers L01 et L08 | Une version exécutable pour mesurer, des critères et un environnement identifiés. | Résultats techniques et anomalies reliés à une version. | Tests et instrumentation font partie du projet ; résultats courants dans la référence commune, pas de réception client déduite. |
| Conception | L02 ; contrats et modèles de L03, L04, L06 ; préparation L10 | Cadrage, parcours et modèle de données. | Écrans, contrats API et flux narration/état cohérents. | La [documentation technique historique](../module/DOC_TECHNIQUE.md) sert à expliquer ces choix, sans dater chaque décision. |
| Réalisation incrémentale | L03–L07, puis consolidation L08–L11 ; L12 transverse | Domaine et contrats avant intégration des écrans ; API/état avant SSE ; socle avant 3D ; version reconstruisible avant qualification de livraison. | Parcours jouables, enrichissements, correctifs et moyens d'exploitation présents. | Les commits ci-dessous attestent des incréments, pas le temps passé ni l'acceptation exhaustive des lots. |
| Restitution et transfert | L12 avec les résultats L09–L11 | Version et périmètre explicités, réserves identifiées. | Manuel, procédures, bilan et démonstration préparée ; réception à recueillir. | La documentation existe ; la soutenance et les prochains points de réception ne sont pas des validations déjà obtenues. |

Enchaînement technique de référence : L01 → L02 et modèles L03/L04 → intégration L05/L06 → extension L07 ; L08 et L09 contrôlent les incréments ; L10 permet la livraison, L11 son observation. L12 accompagne l'ensemble. Les corrections rebouclent vers conception et mesure. Ces chevauchements logiques **ne multiplient pas ma capacité individuelle**.

## 5. Dates attestées, séparées du planning estimatif

| Date du commit | Référence | Incrément traçable | Ce que je peux en déduire |
| --- | --- | --- | --- |
| 02/06/2026 | `64f51d1` | Socle web déjà présent. | Premier repère retenu ici, **pas début réel démontré du projet**. |
| 04/06/2026 | `def2fec` | Base multiutilisateur et E2E. | Évolution comptes/persistance et moyens de qualification. |
| 05/06/2026 | `c1327d5` ; `3c4a5c8` | Tests frontend ; configuration VPS. | Qualification et livraison préparées, pas contrôle actuel du VPS. |
| 10/07/2026 | `7da31cf` | JWT et documentation. | Évolution des accès et de leur documentation. |
| 11/07/2026 | `d7c1bd0` | Configuration de déploiement automatique. | Automatisation configurée, pas preuve de production courante. |
| 12/07/2026 | `b565b39`, `7d9bf12`, `19df4a2` | Gameplay V1, V2, V3. | Réalisation par incréments fonctionnels. |
| 13/07/2026 | `b623142` | Bestiaire. | Enrichissement du domaine. |
| 14/07/2026 | `d419b7f` | Générateur 3D. | Extension expérimentale du périmètre. |
| 19/08/2026 | `4ec094c` ; `68f0495` ; `2bab2f0` | Correctif parsing/progression ; sauvegarde de fiche personnage ; supervision. | Consolidation fonctionnelle et instrumentation. |
| 20/08/2026 | `82a5aba` ; `6119aab` | Infrastructure ; documentation. | Poursuite de la préparation à l'exploitation et de la restitution. |
| 20/09/2026 | `0d1af02` ; `e116b88` | Documentation des Blocs 3 et 1. | Formalisation du dossier ; pas livraison technique ni réception client. |

L'[arbitrage sur la progression](03_CAS_ARBITRAGE.md) explicite une décision technique réelle. Je n'en déduis ni réunion passée, ni durée de correction. Les pièces historiques du module et du Bloc 4 sont des supports d'explication, pas des attestations de l'état courant.

## 6. Charge, budget et capacité de référence

| Calcul commun au Bloc 1 | Borne basse | Borne haute |
| --- | ---: | ---: |
| Construction hors réserve | 100 j.h | 168 j.h |
| Travail × 450 € HT/j.h | 45 000 € | 75 600 € |
| Réserve de 20 % | 20 j.h / 9 000 € | 33,6 j.h / 15 120 € |
| **Construction avec réserve** | **120 j.h / 54 000 € HT** | **201,6 j.h / 90 720 € HT** |
| Capacité théorique à 4 jours projet/semaine | 30 semaines | 50,4 semaines, soit environ 51 |

Le point central **hypothétique** est (100 + 168) / 2 = **134 j.h** ; avec réserve : 134 × 1,20 = **160,8 j.h**, soit **72 360 € HT** et **40,2 semaines** à 4 j/semaine. C'est un repère de dimensionnement, **pas mon temps passé**. Les 30–51 semaines ne s'appliquent pas aux dates Git et ne permettent de conclure ni à une avance ni à une dérive. Je ne dispose pas d'un relevé d'heures et d'un planning initial approuvé permettant cette comparaison.

Les frais pendant construction, les exclusions et les droits restent ceux du budget Bloc 1. L'enveloppe annuelle maintenance + évolutions + services reste **21 015–52 410 € HT/an**, distincte de la construction et d'une dépense constatée.

## 7. Ressources et contraintes du projet complet

| Ressource / fonction | Usage dans le projet | Limite et besoin complémentaire |
| --- | --- | --- |
| Moi-même, intervenant polyvalent | Cadrage, développement, qualité, configurations d'exploitation, documentation. | Pas de timesheet ; cumul des fonctions sans contrôle indépendant systématiquement documenté. |
| Poste, dépôt et outils de développement | Réalisation du produit et conservation des incréments. | Copie locale modifiée ; conserver les changements et qualifier la référence avant toute reconstruction. |
| Environnements et services | API, interface, données, narration, livraison et supervision configurées. | Aucune conclusion sur le VPS courant ; isoler les essais de restauration, de panne et de charge. |
| Interlocuteur de réception / utilisateurs | Nécessaires pour juger l'adéquation au besoin et la satisfaction. | Pas de validation, signature ou participation acquise ; prochains points à convenir. |
| Pair ou spécialiste | Revue indépendante possible sur sécurité, accessibilité ou exploitation. | Renfort optionnel, disponibilité et coût à confirmer ; pas membre d'une équipe historique inventée. |

Les vigilances principales sont la conservation de la progression, la reproductibilité, les droits d'accès, la restauration, le retour arrière, les notifications et les coûts IA. Le [registre des risques](02_TABLEAU_DE_BORD.md) les relie aux lots. Pour les échanges et formations, je propose supports structurés, information non limitée à la couleur, accès clavier, écrit asynchrone et pauses selon les besoins exprimés. Aucun handicap individuel n'est présumé ; capacité et modalités sont ajustées sans recueillir de diagnostic médical.

## 8. Scénario complémentaire, non engagé : stabilisation de l'existant

La [stabilisation C1.6](../bloc1/C1_6_PRECONISATIONS_CLIENT.md) est une **option future secondaire**, pas le planning principal du Bloc 3. Sa fourchette reste **15–27 j.h hors réserve**, soit **8 100–14 580 € HT avec 20 % de réserve**, à 450 €/j.h. Son périmètre doit être actualisé à partir des contrôles de la référence commune avant tout engagement.

Le point central de discussion est 21 j.h : P01 diagnostic 2,5 ; P02 sécurité 4 ; P03 continuité 4 ; P04 supervision 3 ; P05 qualification/restitution 4,5 ; pilotage transverse 3. Calcul : **21 + 4,2 = 25,2 j.h ; 25,2 × 450 = 11 340 € HT**. Aucune date de démarrage, commande ou autorisation n'est acquise. Diagnostic → priorisation → corrections autorisées → contrôles → décision constitue seulement l'ordre proposé.

Je n'ajoute pas cette option au budget de reconstruction complète, qui couvre déjà qualité et livraison. Après accord éventuel, le suivi distinguera charge prévue, charge réellement saisie, reste réestimé et décisions de réserve. Les anciens identifiants T01–T13 désignaient cette option ; ils ne constituent plus le référentiel principal. Le [conducteur de recette](07_DEMONSTRATION_RECETTE_CLIENT.md) présente le produit correspondant à la WBS globale L01–L12.
