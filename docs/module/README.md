# Index du module — archives et guides à vérifier

**Classement documentaire : 20/09/2026.** Cette date n'est pas la date des anciennes campagnes : elles concernent une période antérieure, dont la date exacte n'est pas établie. Une nouvelle vérification technique locale est consignée séparément dans le [rapport de référence](../preuves/VERIFICATION_LOCALE_REFERENCE.md) ; aucun déploiement ni contrôle du VPS n'a été exécuté pour ce classement.

## Références de suivi

- [État de référence](../ETAT_PROJET_REFERENCE.md) — référence commune existante des Blocs 1 et 3 : projet réalisé, budgets, résultats techniques locaux et limites de validation.
- [Tableau de bord actuel](../bloc3/02_TABLEAU_DE_BORD.md) — suivre les tâches, preuves et réserves actuelles plutôt que les statuts anciens.
- [Conducteur et recette préparée](../bloc3/07_DEMONSTRATION_RECETTE_CLIENT.md) — scénarios non exécutés dans cette préparation ; ne pas les présenter comme une recette réussie ou une acceptation client.

Le README racine a été supprimé de la copie de travail et est indisponible. Cet index ne le remplace pas et n'atteste pas la complétude du dépôt. La présence d'un document ou du code n'établit ni son fonctionnement ni une validation RNCP/client.

## Archives historiques du module

| Document | Lecture à retenir |
| --- | --- |
| [DOCUMENT_CADRAGE.md](DOCUMENT_CADRAGE.md) | Périmètre, objectifs et jalons de l'époque, pas le planning actuel. |
| [DOC_TECHNIQUE.md](DOC_TECHNIQUE.md) | Description technique historique ; versions et procédures non revalidées. |
| [SPRINT_FINALISATION.md](SPRINT_FINALISATION.md) | 26 tâches du sprint historique, pas une phase future ; « 0 bloquant » historique déclaré. |
| [AUDIT_OPTIMISATION.md](AUDIT_OPTIMISATION.md) | Constats, optimisations et résultats historiques déclarés. |
| [ANALYSE_CRITIQUE.md](ANALYSE_CRITIQUE.md) | Bilan et pistes de l'époque, pas une mesure actuelle. |
| [ACTIVITES_1_A_10_CHECKLIST.md](ACTIVITES_1_A_10_CHECKLIST.md) | Inventaire des livrables/code présents ; aucune conformité RNCP/client acquise. |
| [MCD_MLD.md](MCD_MLD.md) | Annexe de modélisation conservée ; correspondance avec la version actuelle non vérifiée. |
| [WIREFRAMES.md](WIREFRAMES.md) | Annexe de conception conservée ; correspondance avec l'interface actuelle non vérifiée. |
| [Ancien kanban](../gestion_projet/kanban.md) | Table historique annotée, authentification JWT/bcrypt réalisée ; contrôles de production à vérifier et DoD stricte pour le suivi actuel. |

Les **39 tests backend / 13 tests frontend** restent des chiffres historiques déclarés, pas un décompte actuel ni une nouvelle exécution. Les mentions de déploiement renvoient à un **déploiement historique déclaré ; état du VPS non vérifié**. Les preuves et contenus anciens sont conservés, sans inventer de date de campagne.

## Guides opérationnels non vérifiés

| Guide | Vérifications nécessaires avant usage |
| --- | --- |
| [MANUEL_UTILISATION.md](MANUEL_UTILISATION.md) | Répéter les parcours, vérifier l'accessibilité ciblée, la sauvegarde serveur et les limites de reprise ; RESET ne garantit pas l'effacement. |
| [MANUEL_MISE_A_JOUR.md](MANUEL_MISE_A_JOUR.md) | Vérifier prérequis, sauvegarde/restauration, commit livré, CI/CD et rollback sur copie isolée avant intervention. |
| [Stratégie Git](../gestion_projet/strategie_git.md) | GitHub Actions : configuration présente, pas preuve de run ; distinguer voies automatique et manuelle. |

Pour clore une tâche : **preuve vérifiée, résultat observé, réserves traitées et décision d'acceptation explicite**, avec version, environnement et date réelle d'exécution. Ni une case cochée historique ni un guide préparé ne suffisent.

## PDF anciens — non régénérés

Les PDF existants du module et de la gestion de projet sont **anciens et non régénérés**. Ils peuvent conserver les chiffres, liens cassés et formulations non qualifiées d'avant ce classement. Ne pas les présenter comme actuels ni supposer qu'ils reprennent les avertissements des Markdown. Leur diffusion nécessite une qualification explicite comme archives ; toute régénération est hors de cette intervention.
