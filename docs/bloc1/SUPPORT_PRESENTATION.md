# Bloc 1 — Support oral aligné avec le Bloc 3

**Révision :** 20 septembre 2026. **Format :** trame éditable, pas un diaporama exporté. Adapter la durée aux consignes de l'organisme. Utiliser la même version, les mêmes fonctions et les mêmes limites dans les deux présentations du jour.

## 1. Projet réalisé et besoin de départ

**À afficher :** jeu narratif web, projet individuel, besoin du joueur, périmètre fonctionnel.

**À dire :** « J'ai réalisé ce projet depuis son origine. Je présente d'abord le besoin auquel il répond, le périmètre et les choix qui structurent le produit. Dans le Bloc 3, je reviendrai sur l'organisation de cette réalisation et les arbitrages rencontrés. »

Source : [parcours fonctionnels communs](../PARCOURS_FONCTIONNELS_REFERENCE.md). Ne pas présenter un besoin formalisé aujourd'hui comme un compte rendu signé avant le développement.

## 2. Périmètre et contraintes

**À afficher :** comptes, narration, combat, exploration, inventaire, progression, sauvegarde ; contraintes d'un développement individuel et d'une dépendance IA.

**À dire :** « Le cœur du jeu est réalisé. Les expérimentations 3D et le générateur complètent le périmètre mais ne transforment pas le projet en jeu commercial sans limites. Le multijoueur, la production artistique lourde et une disponibilité 24/7 ne sont pas inclus implicitement. »

Source : [budget et exclusions](C1_4_CHARGE_BUDGET_CYCLE_VIE.md).

## 3. Veille et recherche

**À afficher :** questions concrètes : déploiement, cohérence de sessions, dépendances, consommation IA.

**À dire :** « Les sources et consultations sont datées. Je distingue les outils configurés de leur usage effectivement démontré, ainsi que les décisions implémentées des travaux encore proposés. »

Source : [veille C1.3.1](C1_3_1_VEILLE_TECHNOLOGIQUE.md). Ne pas revendiquer une veille historique régulière sur la seule présence de Dependabot.

## 4. Architecture choisie et alternatives

**À afficher :** React/Vite ↔ API FastAPI ↔ domaine Python ; SQLite/YAML ; narration externe avec repli local ; Docker Compose et supervision.

**À dire :** « Cette architecture est celle du jeu que j'ai construit. Le comparatif formalise ses avantages et limites face à un portage Node ou une distribution en services. L'effort de migration intervient dans la décision actuelle de conservation, pas comme preuve du raisonnement exact tenu avant le premier développement. »

Source : [comparaison C1.3.2](C1_3_2_ETUDE_COMPARATIVE_ARCHITECTURES.md). Les scores guident une décision, ce ne sont pas des benchmarks.

## 5. Charge et budget du projet entier

**À afficher :** les douze lots communs aux deux blocs, 100–168 j.h hors réserve ; 54 000–90 720 € HT avec réserve.

**À dire :** « Cette décomposition valorise une construction complète de périmètre comparable. Ce n'est pas mon relevé d'heures historique ni une facture. Les jalons Git retracent la réalisation ; ils ne permettent pas de transformer automatiquement chaque période en jours-homme. »

Source : [budget du cycle de vie](C1_4_CHARGE_BUDGET_CYCLE_VIE.md). Le Bloc 3 reprend les mêmes lots et fourchettes ; ne pas lui attribuer un projet différent.

## 6. Coût de vie et besoins complémentaires

**À afficher :** maintenance + évolutions + services : 21 015–52 410 € HT/an. À part : stabilisation complémentaire 15–27 j.h ; centre 21 + 4,2 = 11 340 € HT.

**À dire :** « Le développement initial et l'exploitation ne sont pas le même budget. Les 21 jours ne sont pas le temps de construction du jeu : c'est une hypothèse centrale pour un lot complémentaire de robustesse et de préparation à réception, si ce lot est retenu. »

Source : [C1.6](C1_6_PRECONISATIONS_CLIENT.md). Préciser les exclusions et l'absence de validation commerciale du budget.

## 7. État démontrable et recommandations

**À afficher :** référence déclarée 1.3.0 ; 138 tests backend, 30 frontend et build Vite réussi, avec le lien et les limites du rapport.

**À dire :** « Le produit est réalisé et ces vérifications techniques locales réussissent. Elles ne certifient ni l'état du VPS ni une réception client. Je recommande de conserver le socle, de vérifier les conditions d'exploitation et de traiter les risques selon leur impact. »

Sources : [état commun](../ETAT_PROJET_REFERENCE.md), [rapport des vérifications](../preuves/VERIFICATION_LOCALE_REFERENCE.md), [préconisations](C1_6_PRECONISATIONS_CLIENT.md). Les avertissements de test et la copie Git modifiée ne sont pas masqués.

## 8. Transition vers le Bloc 3

> Le produit existe déjà. Le Bloc 1 présente le besoin, les choix d’architecture, le périmètre et le budget du jeu complet. Le Bloc 3 présente l’organisation, la réalisation, le suivi et les arbitrages de ce même projet. Les résultats techniques locaux ne constituent ni une validation client ni une preuve de production.

**À dire :** « Je passe maintenant de la justification des choix à la conduite de leur réalisation : jalons, missions assumées, contrôles, corrections et arbitrages. »

Le [support Bloc 3](../bloc3/08_SUPPORT_PRESENTATION.md) reprend ce fil. Ne pas recommencer par annoncer que tout le développement reste à faire. Réserver une simulation éventuelle au rôle client ou à l'organisation d'équipe hypothétique ; le projet réalisé n'est pas une simulation.