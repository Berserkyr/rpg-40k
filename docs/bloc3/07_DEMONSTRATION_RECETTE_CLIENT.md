# C3.4.2 — Démonstration de la version et décision de réception

**Révision :** 20 septembre 2026.  
**Version déclarée dans le dépôt :** 1.3.0, référence Git `e116b88`, copie de travail modifiée.

**Statut :** conducteur du produit déjà réalisé, commun aux Blocs 1 et 3 ; résultats techniques locaux disponibles, séance de démonstration et réception client à consigner séparément.

## 1. Objectif et règles de présentation

Montrer qu'un joueur peut accéder au jeu, comprendre une action, explorer, gérer son personnage, sauvegarder et affronter une menace. Employer le vocabulaire du joueur : « partie », « progression », « sauvegarde » et « reprise », plutôt que commencer par les frameworks.

Les parcours reprennent les [besoins fonctionnels communs](../PARCOURS_FONCTIONNELS_REFERENCE.md). Le [rapport local](../preuves/VERIFICATION_LOCALE_REFERENCE.md) confirme 138 tests backend, 30 tests frontend et un build réussi ; il ne constitue pas la réalisation des scénarios de séance D01–D08 ci-dessous. Les [E2E présents](../../frontend/e2e/game.spec.js) couvrent l'accès, le démarrage, un jet et l'apparition du combat ; ils n'ont pas été exécutés lors de cette harmonisation et ne couvrent pas toute la sauvegarde, la reprise ou l'isolation des comptes. Les anciennes pièces de recette locales ignorées par Git ne sont plus nécessaires pour lire ce conducteur.

## 2. Préparation obligatoire avant présentation

- Identifier version et commit effectivement exécutés ; noter les modifications locales. Ne pas confondre la version du dépôt avec celle du VPS.
- Choisir une copie de démonstration isolée avec données fictives, jamais un compte administrateur réel.
- Vérifier backend, frontend, authentification, flux narratif et droits d'écriture ; répéter le parcours complet dans le navigateur prévu.
- Pour tester la reprise, utiliser un compte nommé de démonstration avec identifiants conservés en sécurité. Le bouton « LANCER LA DÉMO IMMÉDIATE » crée un compte serveur aux identifiants générés ; il n'est pas un mode anonyme hors ligne.
- Choisir le mode narratif et l'annoncer. Sans clé fournisseur, le narrateur local du backend reste limité ; il dépend toujours du serveur, mais ne nécessite pas d'appel OpenAI.
- Préparer une zone et un état de personnage permettant les actions ; ne pas promettre un butin ou une réussite aléatoire précis.
- Tester clavier, lisibilité, effets réduits et taille de l'écran ; adapter le rythme à l'audience.
- Préparer un secours documentaire daté et identifié comme tel ; une vidéo ou une capture ancienne ne remplace pas automatiquement la démonstration du logiciel devant le jury.

Le [lanceur global](../../start_game.bat) tente de libérer les ports, puis attend un délai fixe : il peut interrompre un autre service et ne constitue pas une sonde de disponibilité. Démarrer et vérifier avant la présentation. Aucune commande de lancement, restauration ou arrêt de production n'a été exécutée pour écrire ce conducteur.

## 3. Conducteur client — cible de 10 minutes

| Temps | Parcours / action | Message à l'audience | Résultat à observer / US |
|---|---|---|---|
| 0:00–0:45 | Présenter but, version et limites du mode narratif. | « Vous pilotez un personnage ; le jeu conserve sa progression. Voici la version présentée et les limites de cette démonstration. » | Périmètre compris ; pas de promesse de production validée. |
| 0:45–1:45 | Se connecter avec le compte nommé préparé ; montrer l'accès à la création de compte si demandé. Pour une visite sans reprise, variante « LANCER LA DÉMO IMMÉDIATE ». | « Chaque joueur accède à son espace de jeu. » | Accès et identité affichés ; US-01. L'isolation multi-compte exige un test distinct. |
| 1:45–2:30 | Si écran-titre, « INITIALISER LA CONNEXION », puis attendre la fin de narration. | « Le récit situe votre personnage et les actions deviennent disponibles. » | Narration terminée et commandes accessibles ; US-02. |
| 2:30–3:15 | « JET 2D6 », puis une action narrative simple. | « Certaines actions utilisent les dés. Le narrateur local n'interprète pas librement toutes les demandes. » | Résultat visible ; aucune réussite particulière garantie. |
| 3:15–4:30 | « FOUILLER », consulter « SAC », puis « CARTE » ; déplacement disponible hors combat. | « Vous trouvez des ressources, consultez votre équipement et choisissez une zone accessible. » | État cohérent et commandes compréhensibles ; US-04, US-05. |
| 4:30–5:00 | Consulter « SKILLS » et les prérequis. | « La progression ouvre des possibilités ; une compétence s'acquiert si les conditions sont remplies. » | Consultation US-06 ; acquisition seulement si le jeu de données le permet. |
| 5:00–6:15 | « SAUVER » ; noter zone, ressources et équipement ; reconnexion avec le même compte. | « La sauvegarde est écrite côté serveur. Nous comparons les valeurs annoncées. » | Données conservées ; US-07. Reconnexion seule ≠ restauration disque après redémarrage. |
| 6:15–8:15 | Après reconnexion, cliquer « INITIALISER LA CONNEXION » si l'écran-titre est affiché et attendre la fin du flux ; puis « RENCONTRE », montrer PV/PA, « ATTAQUER » puis « DÉFENDRE » si pertinent. | « Un combat se joue par tours. Une attaque peut manquer ; défendre termine le tour. » | Tour et état lisibles ; US-03. Comparer les valeurs sauvegardées avant de relancer la narration ; combat placé en dernier pour ne pas bloquer exploration/fouille. |
| 8:15–8:45 | Montrer effets réduits et un parcours clavier préparé. | « L'affichage peut être allégé ; ce contrôle ciblé ne vaut pas audit d'accessibilité complet. » | US-08, constat à consigner. |
| 8:45–10:00 | Récapituler critères, réserves et demander la décision. | « Quels points répondent à votre besoin ? Qu'est-ce qui bloque votre acceptation ? » | Réponses et décision consignées, pas accord supposé. |

**Ne pas utiliser RESET dans ce parcours :** la route examinée retire la session mémoire sans établir l'effacement des sauvegardes. Le libellé ne suffit pas à promettre une remise à zéro complète. La sauvegarde examinée ne démontre pas non plus la reprise intégrale du terminal narratif ou d'un combat en cours.

## 4. Fiche de recette liée à la démonstration

États autorisés : non exécuté, réussi, échoué, bloqué, non applicable avec motif. Joindre pour chaque résultat date, version, environnement, observation et preuve. **Tous les scénarios de séance ci-dessous sont non exécutés dans cette préparation. Cela ne signifie ni que les fonctionnalités restent à développer ni que leurs tests automatisés n'ont pas été exécutés.**

| ID | Critère d'acceptation proposé | Preuve attendue | État initial |
|---|---|---|---|
| D01 | Le compte de test peut se connecter et accéder à sa partie. | Observation + version + identité pseudonymisée. | Non exécuté |
| D02 | La narration se termine et les commandes redeviennent disponibles, y compris en mode local annoncé. | Observation du flux et de l'état de l'interface. | Non exécuté |
| D03 | Un jet et une fouille donnent un retour compréhensible, sans blocage. | Valeurs avant/après ou trace du résultat. | Non exécuté |
| D04 | Inventaire, carte et action de déplacement sont cohérents avec l'état et les prérequis. | Parcours observé et état après déplacement. | Non exécuté |
| D05 | La sauvegarde confirme l'écriture et les valeurs convenues sont retrouvées après reconnexion. | Comparaison zone/ressources/équipement ; noter limite session mémoire. | Non exécuté |
| D06 | Un tour de combat affiche actions, points et résultat sans empêcher la suite prévue. | Observation de l'attaque et de la fin de tour. | Non exécuté |
| D07 | Le parcours clavier préparé et l'option effets réduits sont utilisables. | Étapes, focus et éventuels obstacles décrits. | Non exécuté |
| D08 | La progression et les prérequis de compétence sont compréhensibles. | Observation de consultation ; acquisition seulement si prévue. | Non exécuté |

**Vérifications de livraison distinctes :** restauration après redémarrage sur copie isolée, accès refusé aux données d'un autre compte, HTTPS public, sauvegarde cohérente, rollback, alertes, charge et limite IA. Elles concernent notamment les lots L04, L06 et L08–L11 du [projet complet](01_METHODOLOGIE_PLANNING_RESSOURCES.md) et ne deviennent pas réussies parce que D01–D08 passent. Un complément éventuel est chiffré séparément dans C1.6, sans remettre le développement du jeu au futur.

## 5. Plan de repli et gestion d'incident de présentation

Si le fournisseur IA ne répond pas : expliquer la limite et utiliser l'environnement local préparé, sans modifier en direct un secret de production. Si le backend est indisponible ou si la sauvegarde échoue : arrêter la manipulation concernée, consigner le défaut et ne pas annoncer une validation. Un support de secours peut expliquer le parcours mais ne prouve pas son exécution actuelle.

Ne pas masquer un incident par une capture non datée ; noter le symptôme, l'action interrompue et la suite proposée. Une réserve bloquante conduit à une nouvelle démonstration après correction.

## 6. Procès-verbal de décision — à renseigner en séance

| Champ | Valeur au 20/09 |
|---|---|
| Date de démonstration et contexte réel/simulé | Non réalisée dans cette préparation |
| Présentateur, commanditaire, observateurs | Participants à confirmer |
| Version/commit/environnement effectivement montrés | À relever avant la séance |
| Scénarios exécutés et résultats | D01–D08 : non exécutés |
| Réserves avec impact, responsable et échéance | À établir à partir des observations |
| Décision | Non recueillie ; ne pas précocher GO |
| Accord, refus ou demande de correction du compte rendu | À conserver après la séance |

Choix possibles à expliquer : acceptation du périmètre démontré, acceptation limitée avec réserves non bloquantes, ou refus/report. L'ouverture publique nécessite en plus les preuves d'exploitation et une autorisation distincte. Compléter le [questionnaire de satisfaction](06_SUIVI_CLIENT_VALIDATIONS.md) sans confondre une bonne note et une réception contractuelle.

**Limite C3.4.2 :** le conducteur et les critères sont prêts ; le candidat doit encore réaliser la démonstration devant le jury selon les modalités de l'organisme. Aucun document ne remplace cette prestation.