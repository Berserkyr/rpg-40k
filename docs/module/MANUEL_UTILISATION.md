# Manuel d'utilisation — Survivant de Ruche

> **Guide opérationnel non vérifié — qualification documentaire le 20/09/2026.** Les parcours restent à répéter sur la version et l'environnement retenus ; ce guide n'atteste ni fonctionnement actuel, ni conformité d'accessibilité, ni validation RNCP/client. Voir l'[état de référence](../ETAT_PROJET_REFERENCE.md) (création prévue par l'utilisateur), le [suivi actuel](../bloc3/02_TABLEAU_DE_BORD.md) et le [conducteur de recette préparé, non exécuté](../bloc3/07_DEMONSTRATION_RECETTE_CLIENT.md).

**Public visé :** joueur / utilisateur final.
**Compétence RNCP :** C2.4.1 — Documentation technique d'exploitation (manuel d'utilisation).
**Application :** RPG 40K Survivor (« Survivant de Ruche »).
**Adresse du déploiement historique déclaré :** `http://89.116.111.166:8081/` — état du VPS non vérifié ; confirmer l'environnement avant utilisation.

---

## 1. Présentation

*Survivant de Ruche* est une application web de jeu de rôle narratif solo dans
l'univers de Warhammer 40 000. Vous incarnez un survivant isolé dans une ruche
envahie par les Tyranides. Un **Maître du Jeu (MJ)** — piloté par une IA, avec un
repli local si aucune clé n'est configurée — raconte l'histoire, réagit à vos actions
et fait évoluer le monde.

**Objectif du joueur :** survivre, explorer les zones, combattre, récupérer de
l'équipement, faire progresser son personnage et faire avancer le récit.

---

## 2. Prérequis

| Élément | Détail |
|---|---|
| Navigateur | Chrome, Edge, Firefox ou Safari récent |
| Connexion | Requise (application en ligne) |
| Compte | Créé au premier lancement (voir §3) |
| Matériel | Ordinateur ou tablette ; interface clavier + souris recommandée |

Aucune installation n'est nécessaire pour jouer à la version en ligne.

---

## 3. Créer un compte et se connecter

1. Ouvrez `http://89.116.111.166:8081/`.
2. Sur l'écran d'accueil, choisissez **Inscription**.
3. Renseignez un **identifiant** et un **mot de passe**.
4. Validez : votre compte est créé et vous êtes automatiquement connecté.
5. Lors des prochaines visites, utilisez **Connexion** avec vos identifiants.

> La sauvegarde est prévue **par compte côté serveur**. L'isolation entre comptes doit être vérifiée par un contrôle distinct ; la simple connexion ne la prouve pas. Pour une reprise, utiliser un compte nommé dont les identifiants sont conservés, pas le compte aux identifiants générés du bouton « LANCER LA DÉMO IMMÉDIATE ».

Pour quitter la session, cliquez sur **⏻ DÉCONNEXION** en haut à droite.

---

## 4. Démarrer une partie

1. Une fois connecté, l'écran-titre affiche votre opérateur authentifié.
2. Cliquez sur **[ INITIALISER LA CONNEXION ]**.
3. La narration d'introduction s'affiche progressivement (effet de transmission).
4. Le jeu est prêt : le terminal central affiche l'histoire, les panneaux latéraux
   affichent votre personnage, la carte et les quêtes.

---

## 5. L'interface

```
┌───────────────────────────────────────────────────────────────┐
│  En-tête : statut · accessibilité · 🎒 SAC · 🗺 CARTE · 🧠 SKILLS · ⏻ │
├────────────┬──────────────────────────────┬───────────────────┤
│ Personnage │  TERMINAL (narration + logs) │  Combat           │
│ Carte      │                              │  Inventaire       │
│ Quêtes     │  Barre d'actions             │                   │
│            │  Barre de saisie libre       │                   │
└────────────┴──────────────────────────────┴───────────────────┘
```

- **Terminal central** : récit du MJ, résultats de vos actions, logs de combat.
- **Barre d'actions** : boutons de jeu principaux (voir §6).
- **Barre de saisie** : tapez une action libre en langage naturel.
- **Panneaux latéraux** : personnage, carte, quêtes, combat, inventaire.

---

## 6. Actions de jeu

| Bouton | Effet |
|---|---|
| **Saisie libre** | Décrivez une action (« je force la porte ») ; le MJ répond. |
| **JET 2D6** | Lance deux dés à six faces pour un test de hasard. |
| **FOUILLER** | Cherche du butin dans la zone courante. |
| **RENCONTRE** | Déclenche un combat contre une menace de la zone. |
| **Se déplacer** | Cliquez une zone accessible pour voyager (voir §7). |
| **SAUVER** | Demande l'enregistrement côté serveur ; vérifier le retour et la reprise selon §12. |
| **RESET** | Retire la session mémoire selon le conducteur ; ne garantit pas l'effacement des sauvegardes ni une remise à zéro complète. À éviter pendant la recette. |

---

## 7. La carte (🗺 CARTE)

Cliquez sur **🗺 CARTE** dans l'en-tête pour ouvrir la carte explorateur, qui évolue
avec votre exploration :

- votre **position actuelle** est mise en évidence ;
- les **zones déjà explorées** sont listées avec un bouton **Y ALLER** ;
- les **chemins possibles non empruntés** sont affichés pour vous guider ;
- une **trace d'exploration** montre votre progression.

Chaque déplacement peut déclencher un **incident de route** signalé dans le terminal.

---

## 8. Combat

Quand un combat est actif, le panneau **Combat** (à droite) affiche les points de vie
et les actions disponibles :

| Action | Effet |
|---|---|
| **ATTAQUER** | Inflige des dégâts à l'ennemi. |
| **DÉFENDRE** | Réduit les dégâts subis au prochain tour. |
| **FUIR** | Tente de quitter le combat. |

Le déroulé (jets, dégâts, PV) s'affiche dans le terminal. À la fin, le résultat
(victoire ou repli) est annoncé.

---

## 9. Sac à dos et équipement (🎒 SAC)

Cliquez sur **🎒 SAC** pour ouvrir l'inventaire :

- **ÉQUIPER** : monte une arme/armure sur un emplacement ; vos attributs sont
  **recalculés automatiquement** en tenant compte de l'objet.
- **RETIRER** : déséquipe un objet et le remet dans le sac.
- **UTILISER** : consomme un objet (ex. un soin restaure des points de vie) ;
  la quantité disponible diminue.

L'inventaire s'affiche aussi en permanence dans le panneau latéral droit.

---

## 10. Personnage, attributs et compétences (🧠 SKILLS)

- Le panneau **Personnage** (à gauche) affiche vos attributs effectifs, statistiques
  dérivées, talents et dons.
- Lorsque vous disposez de **points d'attribut**, utilisez le bouton **+** en face
  d'un attribut pour l'améliorer.
- Cliquez sur **🧠 SKILLS** pour ouvrir le panneau des compétences, talents et dons :
  vous pouvez **apprendre** une compétence disponible si vous remplissez les
  conditions. Ses effets sont ensuite pris en compte dans vos statistiques.

---

## 11. Accessibilité

Le bouton **◉ EFFETS COMPLETS / ◍ EFFETS RÉDUITS** de l'en-tête permet de désactiver
les animations et effets visuels pour un meilleur confort de lecture. Ce choix est
mémorisé et respecte aussi le réglage système *« réduire les animations »*
(`prefers-reduced-motion`).

Des dispositifs de navigation clavier, de libellés ARIA et d'effets réduits sont décrits, mais la conformité des contrastes et l'accessibilité globale ne sont pas prouvées. Vérifier le focus, la lisibilité et le parcours clavier sur l'environnement retenu, puis consigner résultats et obstacles dans le [conducteur de démonstration et de recette](../bloc3/07_DEMONSTRATION_RECETTE_CLIENT.md). Le contrôle D07 y est préparé, non exécuté ; il ne remplace pas un audit complet.

---

## 12. Sauvegarde et reprise

- **Navigateur :** le stockage local conserve notamment le jeton de connexion, des informations de compte et le choix d'effets réduits. Ce stockage n'est pas une sauvegarde serveur de la progression ; effacer les données du navigateur ou se déconnecter ne garantit pas l'effacement des données serveur.
- **Serveur :** **SAUVER** demande l'écriture de la progression du compte. Attendre la fin de l'action, vérifier le retour, puis noter zone, ressources et équipement pour comparaison. Le narrateur local nécessite lui aussi un backend disponible ; ce n'est pas un mode hors ligne autonome.
- **Reprise limitée à vérifier :** se reconnecter avec le même compte nommé et comparer les valeurs convenues **avant** de relancer la narration. Si l'écran-titre apparaît, utiliser ensuite « INITIALISER LA CONNEXION » pour poursuivre le parcours.
- Une reconnexion réussie peut retrouver une session encore en mémoire : elle ne prouve pas une restauration depuis le disque après redémarrage serveur. Ce contrôle doit être réalisé séparément sur une copie isolée. La reprise intégrale du terminal narratif ou d'un combat en cours n'est pas démontrée.
- **RESET** retire la session mémoire selon le [conducteur](../bloc3/07_DEMONSTRATION_RECETTE_CLIENT.md), sans établir l'effacement des sauvegardes ; ne pas l'utiliser comme suppression de compte ou garantie de nouvelle partie vierge. Ne pas l'utiliser dans le parcours de recette préparé.

Ces vérifications suivent le [conducteur de recette](../bloc3/07_DEMONSTRATION_RECETTE_CLIENT.md), notamment D05 et les contrôles de livraison distincts ; aucun résultat n'est acquis par la seule lecture du manuel.

---

## 13. Choix techniques (pour information)

Ces choix conditionnent l'expérience utilisateur et sont détaillés dans
[DOC_TECHNIQUE.md](DOC_TECHNIQUE.md) :

| Choix | Bénéfice pour l'utilisateur |
|---|---|
| **React / Vite** | Interface web fluide, sans installation. |
| **FastAPI** | Réponses rapides ; narration en **temps réel** (streaming SSE). |
| **JWT + bcrypt** | Comptes sécurisés, parties privées et isolées. |
| **Repli MJ local** | Le jeu reste jouable même sans service d'IA distant. |

---

## 14. Problèmes fréquents

| Symptôme | Cause probable | Solution |
|---|---|---|
| « Session expirée » / retour à l'écran de connexion | Jeton expiré | Reconnectez-vous. |
| Narration lente ou générique | Pas de clé IA (mode repli local) | Comportement normal ; le jeu reste jouable. |
| Aucun butin après fouille | Résultat aléatoire | Réessayez ou changez de zone. |
| Boutons grisés | Une action est en cours (streaming) | Attendez la fin de la transmission. |
