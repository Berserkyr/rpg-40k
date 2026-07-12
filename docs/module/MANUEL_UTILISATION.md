# Manuel d'utilisation — Survivant de Ruche

**Public visé :** joueur / utilisateur final.
**Compétence RNCP :** C2.4.1 — Documentation technique d'exploitation (manuel d'utilisation).
**Application :** RPG 40K Survivor (« Survivant de Ruche »).
**Accès en ligne :** `http://89.116.111.166:8081/`

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

> Votre progression est **sauvegardée par compte**. Deux joueurs différents ne
> partagent jamais la même partie.

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
| **SAUVER** | Enregistre votre progression. |
| **RESET** | Recommence une nouvelle partie (attention : réinitialise l'état). |

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

L'interface propose une navigation clavier, des libellés accessibles (ARIA) et des
contrastes conformes (voir [MESURES_SECURITE_ACCESSIBILITE.md](MESURES_SECURITE_ACCESSIBILITE.md)).

---

## 12. Sauvegarde et reprise

- Cliquez **SAUVER** à tout moment pour enregistrer la partie.
- La progression est liée à votre compte : à la reconnexion, votre partie est
  rechargée automatiquement.
- **RESET** démarre une nouvelle partie et réinitialise l'état courant.

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
