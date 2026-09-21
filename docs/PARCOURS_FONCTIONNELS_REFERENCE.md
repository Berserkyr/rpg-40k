# Besoins et parcours fonctionnels — référence commune

**Révision :** 20 septembre 2026. **Périmètre :** jeu réalisé présenté dans les Blocs 1 et 3.  
Cette synthèse reprend les huit besoins formalisés dans les pièces locales de conception et les rattache aux sources partageables. Elle ne reprend aucun verdict ancien de recette et ne prétend pas avoir été approuvée avant le développement.

| ID | Besoin du joueur | Critères à observer pour l'acceptation | Réalisation dans le dépôt | Démonstration préparée |
|---|---|---|---|---|
| US-01 | Créer un compte pour accéder à sa partie et la retrouver. | Inscription/connexion, jeton, refus sans droit, séparation des comptes. | [Authentification](../backend/auth.py), [API](../backend/api.py). | D01 ; isolation à contrôler séparément. |
| US-02 | Vivre une aventure narrative qui répond à ses actions. | Narration diffusée, fin de flux, commande disponible et repli local annoncé. | [API et narration](../backend/api.py), [saisie](../frontend/src/components/InputBar.jsx). | D02. Le repli local n'est pas une IA générative équivalente. |
| US-03 | Affronter les menaces par des actions de combat. | Combat déclenché, actions et coûts lisibles, PV/PA actualisés, issue gérée. | [Combat](../src/combat.py), [panneau](../frontend/src/components/CombatPanel.jsx). | D06 ; un tour montré ne démontre pas toutes les issues. |
| US-04 | Explorer et se repérer sur une carte. | Déplacement accessible, position et zones cohérentes avec l'état. | [Monde](../src/world.py), [carte](../frontend/src/components/MapExplorerPage.jsx). | D04. |
| US-05 | Fouiller, s'équiper et utiliser ses ressources. | Butin visible, équipement pris en compte, consommables décomptés. | [Inventaire](../src/inventory.py), [interface](../frontend/src/components/InventoryPanel.jsx). | D03/D04 ; étendre la recette pour tous les effets. |
| US-06 | Personnaliser et faire progresser son personnage. | Attributs et compétences soumis aux prérequis, effets observables. | [Progression](../src/progression.py), [compétences](../frontend/src/components/SkillsPanel.jsx). | D08 ; consultation seule ≠ acquisition validée. |
| US-07 | Sauvegarder et reprendre sa progression. | Confirmation d'écriture, valeurs convenues retrouvées avec le même compte. | [Session et sauvegarde](../backend/api.py), [persistance métier](../src/persistence.py). | D05 ; reconnexion mémoire ≠ restauration après redémarrage. |
| US-08 | Jouer avec un affichage confortable et accessible. | Effets réduits, préférence mémorisée, parcours clavier et libellés compréhensibles. | [Interface](../frontend/src/App.jsx). | D07 ; aucun audit RGAA complet revendiqué. |

Les références D01–D08 renvoient au [conducteur de démonstration](bloc3/07_DEMONSTRATION_RECETTE_CLIENT.md). Les fonctionnalités existent dans le produit ; ces critères décrivent comment les présenter et les accepter. Leur présence dans ce tableau ne signifie pas qu'une séance de recette client a été réalisée.

Fonctions complémentaires du périmètre réalisé : quêtes, relations, négociation, équipe et expérimentations graphiques/3D. Elles figurent dans les lots de construction, sans être toutes promises dans la démonstration courte. Le multijoueur temps réel, une application mobile native et une production massive d'assets ne font pas partie de ce périmètre.

Référence technique et limites communes : [état du projet](ETAT_PROJET_REFERENCE.md). Aucune dépendance à un dossier documentaire ignoré par Git n'est nécessaire pour lire cette synthèse.