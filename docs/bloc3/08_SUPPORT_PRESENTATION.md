# Bloc 3 — Support de présentation orale

**Révision :** 20 septembre 2026. **Format :** trame éditable, pas diaporama exporté.  
Durée et ordre à adapter aux consignes de l'organisme ; les dix minutes du conducteur de démonstration ne sont pas présentées comme la durée officielle de l'épreuve.

## 1. Ouverture commune aux Blocs 1 et 3

**À afficher :** un même jeu complet, réalisé personnellement ; deux angles de présentation le même jour.

**Phrase commune exacte à reprendre dans les deux supports :**

> Le produit existe déjà. Le Bloc 1 présente le besoin, les choix d’architecture, le périmètre et le budget du jeu complet. Le Bloc 3 présente l’organisation, la réalisation, le suivi et les arbitrages de ce même projet. Les résultats techniques locaux ne constituent ni une validation client ni une preuve de production.

**Transition personnelle :** « J'ai réalisé le projet de bout en bout, depuis sa conception. Je vais montrer comment j'ai articulé les fonctions de développement, qualité, livraison et documentation. Le projet est réel ; la matrice d'équipe que je présente est seulement une modélisation pédagogique. »

Appuis : [dossier Bloc 3](README.md) et [état de référence commun](../ETAT_PROJET_REFERENCE.md). Pour la version et les résultats courants, utiliser cette référence, pas un ancien total de tests. Référence de rédaction : `e116b88`, copie non propre ; la version effectivement montrée doit être identifiée séparément.

## 2. Parcours de réalisation : les repères attestés

**À afficher :** une frise factuelle, distincte du planning estimatif.

| Période / repère | Éléments à montrer |
| --- | --- |
| 02–05 juin | Socle web déjà présent (`64f51d1`), base multiutilisateur/E2E (`def2fec`), tests frontend (`c1327d5`), configuration VPS (`3c4a5c8`). |
| 10–14 juillet | JWT/documentation (`7da31cf`), automatisation (`d7c1bd0`), gameplay V1–V3 (`b565b39`, `7d9bf12`, `19df4a2`), bestiaire (`b623142`), générateur 3D (`d419b7f`). |
| 19–20 août | Correctif progression (`4ec094c`), sauvegarde de fiche (`68f0495`), supervision (`2bab2f0`), infrastructure (`82a5aba`), documentation (`6119aab`). |
| 20 septembre | Formalisation des dossiers Bloc 3 et Bloc 1 (`0d1af02`, `e116b88`). |

**À dire :** « Le premier repère Git montre déjà un socle web. Je ne le présente pas comme la date réelle de début du projet. Ces incréments montrent la construction et la consolidation du produit, pas mes heures travaillées ni des validations client. »

Appui : [chronologie et planning global](01_METHODOLOGIE_PLANNING_RESSOURCES.md). Les pièces [techniques du module](../module/DOC_TECHNIQUE.md) sont des archives explicatives ; elles ne certifient pas l'état actuel du VPS.

## 3. Organisation et dépendances — C3.1

**À afficher :** étude → mesure → conception → réalisation → restitution, avec retours de mesure ; douze lots communs au Bloc 1.

**À dire :** « Je formalise rétrospectivement mon organisation avec une lecture Kanban légère. Je ne revendique pas un tableau historique dont je n'ai pas conservé la preuve. Le domaine et les contrats API structurent les écrans et la narration ; les incréments sont ensuite qualifiés et corrigés. La livraison et la supervision complètent la réalisation. J'ai assuré ces fonctions seul, sans multiplier artificiellement ma capacité. »

Montrer les dépendances L01 → conception et modèles → L03–L06 → extension L07 ; contrôles L08–L09 ; livraison L10 et supervision L11 ; documentation L12 transverse. Expliquer que cet ordre est une **reconstitution et estimation de référence, non un planning approuvé historique**. Une limite de travail en cours et des relevés hebdomadaires sont proposés pour améliorer la suite, pas affirmés comme cérémonies passées.

Appuis : [WBS globale](01_METHODOLOGIE_PLANNING_RESSOURCES.md) et [affectation par fonctions](04_MISSIONS_MANAGEMENT_COMMUNICATION.md).

## 4. Charge et budget du jeu complet

**À afficher en principal :**

- **100–168 j.h hors réserve**, à **450 € HT/j.h**.
- Travail : 45 000–75 600 € HT ; réserve de 20 % : 9 000–15 120 € HT.
- **Construction complète : 54 000–90 720 € HT, réserve incluse.**
- Maintenance + évolutions + services : **21 015–52 410 € HT/an**, séparément.

**À dire :** « C'est le même chiffrage de référence que dans le Bloc 1, pour construire un périmètre comparable depuis zéro. Ce n'est pas ma facture ni mon relevé de temps. Je n'ai pas de timesheet historique permettant de calculer un coût réel ou une dérive. »

Si le point central est demandé : (100 + 168) / 2 = **134 j.h hypothétiques**, puis 134 × 1,20 = 160,8 j.h, soit **72 360 € HT**. À 4 jours projet/semaine, la fourchette avec réserve représente environ **30–51 semaines** : ne pas la reporter sur la frise Git ni en déduire un retard. Les frais et exclusions restent ceux du [budget commun](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md).

## 5. Suivi du produit réalisé — C3.2.1

**À afficher :** trois colonnes : livrables présents / preuves et résultats / contrôles et décisions restant à qualifier.

**À dire :** « Le tableau de bord est initialisé après coup. Il montre des réalisations sur les douze lots : je ne repars pas d'un jeu inexistant, mais je ne déclare pas non plus une acceptation globale. Je distingue temps passé inconnu, estimation de référence et reste à qualifier. NR signifie non mesuré ou non renseigné, pas zéro travail. »

Montrer un lot fonctionnel, un lot de livraison et un risque. Expliquer pourquoi configuration de supervision ≠ notification reçue, sauvegarde ≠ restauration après incident, résultats locaux ≠ réception client. Pour les contrôles courants, ouvrir la référence commune plutôt que réciter un résultat historique.

Appui : [tableau de bord et risques](02_TABLEAU_DE_BORD.md). Aucun historique de dépenses, de vitesse ou de réunions régulières n'est reconstitué artificiellement.

## 6. Arbitrage réel : protéger la progression — C3.2.2

**À afficher :** progression menacée → prompt seul / contrôle du parseur / protection du flux → choix combiné.

**À dire :** « Une consigne au narrateur ne garantit pas son format de sortie. J'ai traité la valeur invalide et protégé la poursuite du flux pour préserver la sauvegarde, tout en rendant les rejets visibles. Le commit étaye la réalisation. Le logigramme explique mon choix rétrospectivement ; je n'en déduis ni temps de correction ni accord client. »

Appui : [cas ANO-2026-001](03_CAS_ARBITRAGE.md), commit `4ec094c` du 19 août. Signaler le risque résiduel : un récit peut annoncer une modification que le moteur a rejetée. Les résultats historiques et les résultats de la version courante restent distincts.

## 7. Missions, posture et expérience — C3.3.1 et C3.3.2

**À afficher :** fonctions que j'ai assurées, charge par rôle sans double compte, compétences mobilisées et approfondissements ciblés.

**À dire :** « J'ai assuré la conception, le développement, les contrôles et la documentation. Cette polyvalence facilite l'intégration mais limite la contradiction indépendante. Je peux expliquer les compétences mises en pratique et les erreurs corrigées. Je ne transforme pas ces réalisations en notes d'évaluation et je ne présente pas plusieurs rôles comme plusieurs personnes. »

Puis : « Le RACI d'équipe est pédagogique. Les formations proposées sont des approfondissements possibles après réalisation : restauration, sécurité, alertes, observation d'usage et suivi. Elles ne signifient pas que tout reste à apprendre avant de construire le jeu. »

Appuis : [missions et analyse critique](04_MISSIONS_MANAGEMENT_COMMUNICATION.md), [bilan des compétences](05_COMPETENCES_FORMATION.md). Les styles de management collectif et exercices optionnels ne sont pas des expériences d'encadrement inventées. Expliquer les adaptations possibles : supports structurés, échanges écrits, pauses et accessibilité selon les besoins exprimés.

## 8. Bilan, réception et satisfaction — C3.4.1

**À afficher :** CR-00 rétrospectif du parcours entier ; prochains points V1–V3 de réception ; options O1–O2 distinctes.

**À dire :** « Le compte rendu récapitule ma réalisation complète, ses bénéfices et ses limites. Ce n'est pas le compte rendu d'une réunion client passée. La réception, la signature et la satisfaction ne sont pas obtenues. Je propose maintenant de convenir des critères, observer les parcours et recueillir une décision et des retours. »

Appui : [suivi client et questionnaire](06_SUIVI_CLIENT_VALIDATIONS.md). Ne pas présenter un répondant fictif, une date de rendez-vous non convenue ou l'avis du jury comme une réception contractuelle. Un éventuel exercice pédagogique sera identifié séparément du projet réel.

## 9. Démonstration du produit — C3.4.2

Basculer vers le [conducteur de démonstration](07_DEMONSTRATION_RECETTE_CLIENT.md), à synchroniser séparément avec l'[état de référence](../ETAT_PROJET_REFERENCE.md) : accès, narration, actions, exploration, sauvegarde puis combat. Identifier version, environnement et mode narratif. Les mentions historiques du conducteur ne remplacent pas ces informations de séance.

**À dire :** « Je montre maintenant les parcours du produit réalisé. J'annonce ce que cette démonstration permet d'observer et ce qu'elle ne valide pas, notamment la restauration après incident et la production. »

Ne pas improviser un redémarrage de production ni utiliser RESET pour garantir un état neuf. Consigner un échec ou une réserve au lieu de le masquer. Une capture ancienne reste un support daté, pas un succès actuel.

## 10. Conclusion : bilan d'abord, suites optionnelles ensuite

**À dire :** « J'ai présenté l'organisation et la réalisation du même jeu que dans le Bloc 1. Le produit et les incréments sont là ; les résultats observés, les réserves et la réception sont distingués. Les compléments éventuels sont une décision séparée, pas le sujet principal de ce bilan. »

Après une observation réelle, demander quels critères sont satisfaits et quelles réserves empêchent la réception. Consigner la réponse sans présumer une signature. L'autorisation de production et l'appréciation des compétences par le jury restent distinctes.

### Annexe orale uniquement : option de stabilisation

Si la suite est abordée : **15–27 j.h hors réserve**, **8 100–14 580 € HT réserve incluse**. Centre de discussion : **21 + 4,2 = 25,2 j.h ; 25,2 × 450 = 11 340 € HT**. Aucune date ni autorisation acquise. Ce scénario sera ajusté selon les contrôles et ne s'ajoute pas au budget de reconstruction complète. Les formations éventuelles sont décidées séparément sans double compte.

Appuis : [scénario secondaire du planning](01_METHODOLOGIE_PLANNING_RESSOURCES.md) et [budget du cycle de vie](../bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md). Ne pas ouvrir la présentation par ce scénario : il ne raconte pas à lui seul le projet réalisé.
