# C3.3.2 — Évaluation des besoins et plan de développement des compétences

**Révision :** 20 septembre 2026.  
**Public identifié :** le candidat, intervenant polyvalent du projet individuel.  
**Statut :** analyse des preuves et des besoins ; niveaux personnels à confirmer par entretien et exercices. Aucun recrutement, formation suivie ou résultat d'évaluation n'est inventé.

## 1. Méthode d'évaluation

Je pars des missions à assurer plutôt que d'une liste générique de technologies. Je distingue :

1. **La couverture documentaire actuelle** : ce que le dépôt permet réellement d'examiner.
2. **Le niveau individuel actuel** : ce que la personne sait expliquer et réaliser, qui nécessite une observation. La présence de code, même fonctionnel, ne suffit pas à l'attribuer.
3. **Le niveau requis** pour réaliser la mission et décider d'une formation, d'un accompagnement ou d'une prestation.

Échelle individuelle proposée : 0 = non acquis ; 1 = explique les principes ; 2 = réalise avec aide ; 3 = réalise et vérifie en autonomie ; 4 = transmet et traite un cas complexe. **NE = non évalué**, différent de zéro.

Procédure : auto-positionnement argumenté, exercice sur environnement isolé, lecture de la preuve et questions de justification. Consigner évaluateur, date, conditions, aides utilisées et aménagements. Une auto-évaluation reste signalée comme telle ; une revue par un tuteur ou pair doit être réellement organisée. Les niveaux cibles ci-dessous sont des exigences proposées, pas un diagnostic individuel.

## 2. Grille commentée des compétences actuelles et à acquérir

| Compétence / mission | Éléments actuels observables | Niveau personnel actuel | Cible | Besoin identifié / contrôle attendu |
|---|---|---|---:|---|
| Domaine Python, API et narration | [API](../../backend/api.py), [règles](../../src), correction `4ec094c`, tests associés. | NE | 3 | Expliquer le flux, reproduire un marqueur invalide et vérifier sauvegarde + fin de flux sans aide. |
| React et parcours utilisateur | [Interface](../../frontend/src/App.jsx), [E2E](../../frontend/e2e/game.spec.js), tests frontend archivés. | NE | 3 | Démontrer authentification, état asynchrone, gestion d'erreur et reprise ; pas seulement modifier l'affichage. |
| Stratégie de tests | Suites présentes, recette historique et CI configurée. | NE | 3 | Produire une campagne actuelle traçable, distinguer couverture, réussite et tests non exécutés. |
| Persistance et reprise | SQLite/YAML, correctif `68f0495` ; aucune restauration actuelle observée dans cet audit. | NE | 3 | Sauvegarde cohérente, restauration isolée et vérification d'intégrité : priorité F02. |
| Sécurité et livraison | Audits configurés mais non bloquants ; protection publique non vérifiée. | NE | 3 | Qualifier une vulnérabilité, vérifier accès/rôles/TLS et appliquer une politique de livraison : F03. |
| Supervision et réponse à incident | Prometheus/Grafana/Alertmanager configurés ; pas de notification constatée pendant la revue. | NE | 3 | Distinguer processus arrêté, état unhealthy et sonde publique ; vérifier notification et reprise : F04. |
| Accessibilité et observation d'usage | Effets réduits et critères d'usage présents ; pas d'audit complet ni panel observé. | NE | 2 avec appui spécialisé si besoin | Appliquer un protocole clavier et lire un retour sans suggérer la réponse : F05. |
| Charge, coûts et risques | Budget prévisionnel et tableau de bord initial ; pas d'historique de temps. | NE | 3 | Calculer prévu/réalisé, reste à faire, risque et décision de réserve : F01. |
| Coordination, communication et développement d'équipe | Projet individuel ; styles et missions proposés, pas de management effectif établi. | NE | 2 en mise en situation, puis 3 à confirmer en pratique | Affecter une tâche selon compétence/capacité, reformuler un désaccord et formaliser une décision : F06. |

**Lecture de la grille :** les artefacts offrent un support d'évaluation pour le développement, mais les preuves d'exploitation réelle et de pilotage sont moins complètes. Cela justifie les priorités de formation ; cela ne permet pas de conclure que le candidat ne sait pas faire. Après évaluation, remplacer NE par un niveau et une preuve datée, puis calculer l'écart cible − actuel. Aucun écart numérique n'est calculé sur NE.

## 3. Plan de développement proposé

Les durées couvrent apprentissage et exercices pédagogiques, **pas les corrections de production déjà comptées dans T01–T13**. Une évaluation initiale peut dispenser d'un module ou révéler un besoin plus important.

| ID | Public / objectif observable | Formation et modalités proposées | Durée | Échéance relative | Évaluation de sortie |
|---|---|---|---:|---|---|
| F01 | Candidat en fonction de pilotage : réestimer une phase sans masquer une dérive. | Atelier Kanban, capacité, budget et risque sur les 13 tâches réelles ; étude du [guide Kanban](https://kanbanguides.org/). | 0,5 j | Avant validation de la baseline J0. | Relevé fictif explicitement pédagogique : calcul juste, comparaison conservée, décision justifiée. |
| F02 | Candidat backend/exploitation : prouver une restauration cohérente. | Lecture de la [sauvegarde SQLite](https://www.sqlite.org/backup.html), exercice sur données jetables et débrief avec pair si disponible. | 1 j | Avant T06. | Restaurer un jeu de données connu, vérifier intégrité et contenu ; expliquer les limites de la copie à chaud. |
| F03 | Candidat livraison : distinguer audit informatif et contrôle bloquant. | Parcours ciblé [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), revue CI et exercice rôles/secrets sur sandbox. | 1 j | Avant T04–T05. | Identifier un risque applicable, définir un refus de livraison et une exception bornée sans exposer de secret. |
| F04 | Candidat exploitation : diagnostiquer et notifier un incident. | Lecture [Docker Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/) et [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/), exercice panne/rétablissement isolé. | 1 j | Avant T08–T09. | Expliquer healthcheck/restart et montrer une notification avec retour au nominal dans l'exercice. |
| F05 | Candidat frontend/recette : observer un parcours accessible. | Atelier clavier, focus, lisibilité, effets réduits, à partir des [vérifications WAI](https://www.w3.org/WAI/test-evaluate/preliminary/). | 0,5 j | Avant T10. | Produire trois observations reproductibles avec impact et correction proposée ; pas de déclaration de conformité RGAA. |
| F06 | Candidat en fonction de coordination : conduire un échange de décision. | Jeu de rôle avec tuteur/partenaire à solliciter : délégation, désaccord sur délai, restitution et retour critique. | 0,5 j | Avant première revue client. | Consigne reformulée, capacité vérifiée, options exposées, décision et action consignées ; simulation explicitement identifiée. |
| **Total proposé** | | | **4,5 j / 31,5 h** | | |

Les liens sont des ressources d'apprentissage proposées, pas la preuve d'une inscription, d'une lecture complète ou d'une certification obtenue. Les intervenants pédagogiques ne sont pas réservés.

## 4. Charge, coût et intégration au planning

Si les six modules sont nécessaires, valorisation du temps à l'hypothèse de 450 € HT/j.h : **4,5 × 450 = 2 025 € HT**, hors frais de formation, accompagnement ou examen à deviser. Une réserve optionnelle de 20 % porterait cette enveloppe de travail à **2 430 € HT / 5,4 j.h**. Ce n'est pas le tarif commercial des ressources gratuites citées.

Cette capacité pédagogique n'est **pas comprise automatiquement** dans les 21 j.h de stabilisation. Deux possibilités après positionnement : formation supplémentaire approuvée et calendrier allongé, ou réallocation explicitement justifiée de travaux devenus inutiles. Ne pas supprimer tests ou sécurité pour faire entrer artificiellement la formation dans la baseline. Les essais opérationnels T06/T09 restent nécessaires même après réussite d'un exercice pédagogique, mais leur temps ne doit pas être facturé deux fois.

## 5. Adaptations des modalités

Avant formation, recueillir les besoins fonctionnels volontairement exprimés : supports lisibles, documents structurés, sous-titres, accès clavier, rythme asynchrone, pauses ou temps supplémentaire. Préférer un environnement d'exercice accessible ; proposer une restitution écrite ou orale équivalente selon le besoin. Le critère évalué reste la compétence, non la vitesse quand elle n'est pas essentielle à la mission.

Aucun état de santé n'est enregistré dans cette grille. Limiter l'accès aux évaluations personnelles et conserver seulement les informations utiles. En contexte multilingue, proposer glossaire, consignes écrites et temps de reformulation ; ne pas confondre aisance linguistique et capacité technique.

## 6. Renfort, recrutement et suivi

Il n'existe pas de service RH identifié pour ce projet. Si un niveau indispensable n'est pas atteint avant la tâche, soumettre au commanditaire une demande de renfort : compétence manquante, mission, charge, période, niveau d'accès, coût/devis et preuve de résultat attendue. Un audit de sécurité externe ou un besoin 24/7 ne doit pas être implicitement attribué au candidat après une journée de formation.

Suivi à tenir pour chaque module : date d'évaluation initiale, niveau initial prouvé, décision de formation, date réelle, temps/coût, résultat de l'exercice, niveau observé et action suivante. **Au 20 septembre : aucun module de ce plan n'est déclaré suivi ou validé.** La grille et le plan sont préparés ; l'évaluation individuelle doit encore avoir lieu.