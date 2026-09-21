# État de référence — projet commun aux Blocs 1 et 3

**Projet :** RPG 40K Survivor — Survivant de Ruche  
**Candidat :** REBIAI Nehjmehdine Karim  
**Révision documentaire :** 20 septembre 2026 ; vérifications techniques réalisées pendant cette harmonisation, avec une horloge d'exécution datée du 21 septembre (voir le rapport).  
**Référence Git observée :** `e116b88`, version applicative déclarée **1.3.0**. Ce point de référence reste daté : il n'est pas un pointeur permanent vers le dernier commit.

## 1. Un seul projet, deux angles de présentation

> Le produit existe déjà. Le Bloc 1 présente le besoin, les choix d’architecture, le périmètre et le budget du jeu complet. Le Bloc 3 présente l’organisation, la réalisation, le suivi et les arbitrages de ce même projet. Les résultats techniques locaux ne constituent ni une validation client ni une preuve de production.

Le candidat confirme avoir réalisé personnellement le projet depuis son origine. Le dossier présente donc **un projet individuel développé de bout en bout**, et non deux projets ni une équipe fictive. Le premier commit accessible contient déjà une application : il ne fixe pas le jour réel du début du travail.

Les pièces de soutenance mettent en forme cette expérience après réalisation. Un planning reconstitué, un comparatif rédigé aujourd'hui ou une matrice RACI pédagogique ne doivent pas être présentés comme des documents approuvés avant le développement. Les aides et outils effectivement utilisés restent à expliquer lors de la présentation de la contribution personnelle.

## 2. État technique à retenir

| Sujet | État de référence | Ce que cela ne prouve pas |
|---|---|---|
| Architecture | Frontend React/Vite, backend FastAPI, domaine Python, SQLite pour les comptes et traces, YAML pour des états de jeu, Docker Compose/Nginx. | Versions effectivement installées sur le VPS, dimensionnement ou haute disponibilité. |
| Périmètre réalisé | Comptes, narration SSE avec repli local, combat, exploration, inventaire, progression, quêtes, relations, équipe ; expérimentations graphiques/3D et générateur. | Chaque fonction acceptée par un client ou chaque expérimentation prête pour une exploitation commerciale. |
| Authentification | JWT, bcrypt et rôles présents ; elle n'est plus un backlog de développement initial. | Audit complet des accès, gestion des secrets et protection HTTPS publique. |
| Tests backend | **138 tests réussis**, avec un avertissement, dans la vérification locale isolée. | Validation d'un environnement de production ou audit exhaustif. |
| Tests frontend | **30 tests réussis dans 6 fichiers** ; avertissements Canvas dans l'environnement de test. | Tests navigateur E2E complets, validation visuelle ou accessibilité intégrale. |
| Build frontend | **Build Vite réussi**, 62 modules transformés. | Reconstruction Docker complète ni déploiement de ce build. |
| Production | Déploiement historique déclaré dans les archives ; workflows et supervision configurés. | État courant du VPS, version déployée, TLS externe ou réception effective des notifications. |
| Recette / réception | Des documents historiques décrivent une recette ; les scénarios de démonstration sont préparés. | Aucun accord client ou procès-verbal actuel n'est établi par les preuves examinées. Ne pas affirmer qu'aucun test utilisateur n'a jamais eu lieu. |

Source des derniers résultats : [rapport de vérification locale](preuves/VERIFICATION_LOCALE_REFERENCE.md). Ces essais ont été réalisés sur la copie courante sans modification du code applicatif. Ils établissent la réussite des vérifications exécutées, pas l'absence de tout défaut.

**État Git réellement observé : non propre.** Des suppressions et modifications locales préexistaient à cette harmonisation, dont le fichier de construction backend, les anciennes pages d'accueil et des configurations. Elles n'ont pas été annulées. La réussite du build Vite ne permet donc pas d'affirmer que cette copie reconstruit tous les conteneurs. Les nouvelles modifications documentaires sont également locales tant qu'elles ne sont pas commitées.

## 3. Chronologie attestée, distincte du temps passé

| Période observée | Réalisation traçable | Références Git |
|---|---|---|
| 02–05 juin 2026 | Socle web déjà présent, tests API/frontend, données multi-utilisateur, E2E et préparation VPS. | `64f51d1`, `6ec8b04`, `def2fec`, `c1327d5`, `3c4a5c8` |
| 10–12 juillet 2026 | Authentification JWT, documents de conception, automatisation de livraison et enrichissement du gameplay. | `7da31cf`, `d7c1bd0`, `b565b39`, `7d9bf12`, `19df4a2` |
| 13–14 juillet 2026 | Bestiaire, animations et expérimentations de génération/visualisation 3D. | `b623142`, `216c102`, `3ef4a91`, `d419b7f` |
| 19–20 août 2026 | Veille, supervision, corrections narration et sauvegarde, instrumentation serveur. | `c3d478a`, `2bab2f0`, `4ec094c`, `68f0495`, `82a5aba` |
| 20 septembre 2026 | Publication de pièces Bloc 3 puis Bloc 1, avant la présente harmonisation. | `0d1af02`, `e116b88` |

Ces jalons attestent des intégrations dans le dépôt, pas des jours-homme consommés ni de la date de chaque déploiement. Les 26 tâches des anciens documents concernent leur sprint historique ; elles ne sont ni les douze lots du jeu complet ni les anciennes tâches prévisionnelles T01–T13 de stabilisation.

## 4. Budget commun : conserver le périmètre dans chaque intitulé

Hypothèses : 7 heures/j.h, TJM de 450 € HT, réserve de 20 % sur le travail humain. Les chiffres sont des estimations de référence, pas des factures, un relevé historique ou un devis accepté.

| Périmètre | Charge / coût de référence |
|---|---|
| **Construction complète depuis zéro d'un jeu de périmètre comparable** | **100–168 j.h hors réserve ; 54 000–90 720 € HT avec réserve.** Il s'agit d'une valorisation estimative, pas du temps réellement consommé. |
| **Stabilisation complémentaire estimée de l'existant** | **15–27 j.h hors réserve ; 8 100–14 580 € HT avec réserve.** Ce n'est pas le projet initial, ni un engagement déjà approuvé. |
| **Hypothèse centrale de cette stabilisation complémentaire** | **21 + 4,2 = 25,2 j.h avec réserve ; 11 340 € HT.** À présenter en perspectives, pas comme le coût ou la durée de création du jeu. |
| **Maintenance, évolutions et services sur douze mois après ouverture** | **21 015–52 410 € HT/an**, avec réserve sur le travail humain et provisions de services. |

Si le centre de la fourchette de construction est montré : 134 j.h hors réserve, 160,8 avec réserve, 72 360 € HT. C'est un calcul de scénario, pas une mesure. Un calendrier théorique calculé à 4 j/semaine ne doit pas être comparé aux dates Git comme une dérive historique.

Sources : [budget complet du cycle de vie](bloc1/C1_4_CHARGE_BUDGET_CYCLE_VIE.md), [préconisations](bloc1/C1_6_PRECONISATIONS_CLIENT.md), [planning global reconstitué](bloc3/01_METHODOLOGIE_PLANNING_RESSOURCES.md). Les exclusions, frais avant ouverture et éventuelles formations restent à considérer. Ne pas additionner construction théorique et stabilisation comme s'il fallait payer deux fois les mêmes travaux.

## 5. Règles de cohérence pour la soutenance commune

- **Bloc 1 :** expliquer le besoin, le périmètre livré, les choix structurants et la viabilité économique ; distinguer décisions matérialisées et préconisations complémentaires.
- **Bloc 3 :** expliquer comment le même projet a été organisé, réalisé et ajusté ; montrer les jalons, missions, preuves, arbitrages et limites de mesure.
- Projet individuel réalisé : ce n'est pas une simulation. Seules une organisation d'équipe hypothétique et une éventuelle séance pédagogique doivent être signalées comme telles.
- Code réalisé ≠ vérification technique ≠ recette utilisateur ≠ acceptation client. La réalisation réelle n'impose pas de prétendre que ces quatre étapes possèdent les mêmes preuves.
- « Sprint de finalisation » désigne une phase historique ; Kanban léger désigne une formalisation du flux et du suivi, pas la preuve d'une cérémonie Scrum tenue.
- Les chiffres historiques 39/13, 82/30 ou 120/30 restent dans leurs archives ; le rapport courant indique 138/30. Ne pas antidater les nouveaux résultats.
- Les tâches complémentaires ne retirent rien à l'existence du produit ; elles concernent sa robustesse, sa réception ou son évolution.

## 6. Documents courants et archives

Points d'entrée : [Bloc 1](bloc1/README.md), [Bloc 3](bloc3/README.md), [archives du module](module/README.md), [besoins et parcours communs](PARCOURS_FONCTIONNELS_REFERENCE.md).

Les anciens documents RNCP sont présents dans cette copie mais ignorés par Git. Un lien qui fonctionne localement peut donc être absent sur GitHub. Les supports courants ne doivent plus dépendre de ces pièces locales ; leurs contenus utiles sont reformulés dans des références partageables, sans importer d'anciens verdicts de recette.

Les PDF historiques ne sont pas régénérés par cette harmonisation. Leur contenu peut différer du Markdown et conserver d'anciens chiffres. Les conserver comme archives, pas comme export à jour des présentations.