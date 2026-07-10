# Wireframes — Écrans clés

**Projet :** RPG 40K Survivor — frontend React

Ces wireframes décrivent les écrans principaux et les flux d'interaction.
Le style visuel est un **terminal grimdark** (vert phosphore sur fond noir, scanlines).

---

## Écran 1 — Authentification (connexion / inscription)

```
┌───────────────────────────────────────────────────────────┐
│  ⚙ HIVE-NODE//SECTEUR-7                 ○ SYSTÈME OK        │
├───────────────────────────────────────────────────────────┤
│                                                           │
│                 AUTHENTIFICATION VOX                       │
│                                                           │
│           IDENTIFIANT                                      │
│           [_______________________]                       │
│                                                           │
│           MOT DE PASSE                                     │
│           [_______________________]                       │
│                                                           │
│               [ SE CONNECTER ]                            │
│                                                           │
│        Pas encore d'accès ? Créer un compte               │
│                                                           │
└───────────────────────────────────────────────────────────┘
```
Composant : [AuthPanel.jsx](../../frontend/src/components/AuthPanel.jsx)
Bascule entre **connexion** et **inscription** (champ « nom affiché » en plus).

## Écran 2 — Démarrage de partie

```
┌───────────────────────────────────────────────────────────┐
│  ⚙ HIVE-NODE//SECTEUR-7        ○ SYSTÈME OK   ⏻ DÉCONNEXION│
├───────────────────────────────────────────────────────────┤
│                 ███ SURVIVANT ███                          │
│         RUCHES DE KHARAD-RHO · INVASION TYRANIDE           │
│                                                           │
│         Opérateur authentifié : KARIMUS                    │
│                                                           │
│              [ INITIALISER LA CONNEXION ]                  │
└───────────────────────────────────────────────────────────┘
```

## Écran 3 — Jeu principal (layout 3 colonnes)

```
┌───────────────────────────────────────────────────────────┐
│  ⚙ HIVE-NODE//SECTEUR-7   ● TRANSMISSION VOX  ⏻ DÉCONNEXION│
├───────────┬───────────────────────────────┬───────────────┤
│ PERSONNAGE│      TERMINAL NARRATIF         │    COMBAT     │
│  - PV     │  > Karimus reprend conscience  │  [ATTAQUER]   │
│  - Stress │    dans la coursive...         │  [DÉFENDRE]   │
│           │  (streaming IA en direct)      │  [FUIR]       │
│  CARTE    │                                │               │
│  - Zone   │                                │  INVENTAIRE   │
│  - Sorties│                                │  - Couteau    │
│           ├───────────────────────────────┤  - Casque     │
│  QUÊTES   │ [DÉS] [FOUILLER] [RENCONTRE]   │               │
│  - ...    │ [VOYAGER] [SAUVER] [RESET]     │               │
│           ├───────────────────────────────┤               │
│           │ > _saisir une action_______    │               │
└───────────┴───────────────────────────────┴───────────────┘
```

**Zones fonctionnelles :**
- **Colonne gauche** : personnage, carte, quêtes ([CharacterPanel](../../frontend/src/components/CharacterPanel.jsx), [MapPanel](../../frontend/src/components/MapPanel.jsx), [QuestPanel](../../frontend/src/components/QuestPanel.jsx)).
- **Colonne centrale** : terminal narratif (streaming IA), panneau d'actions, barre de saisie ([Terminal](../../frontend/src/components/Terminal.jsx), [ActionPanel](../../frontend/src/components/ActionPanel.jsx), [InputBar](../../frontend/src/components/InputBar.jsx)).
- **Colonne droite** : combat et inventaire ([CombatPanel](../../frontend/src/components/CombatPanel.jsx), [InventoryPanel](../../frontend/src/components/InventoryPanel.jsx)).

## Flux de navigation

```
   [Auth] ──succès JWT──▶ [Démarrage] ──"Initialiser"──▶ [Jeu principal]
      ▲                                                       │
      └──────────────── "Déconnexion" ◀──────────────────────┘
```

## Comportement responsive

- ≥ 1100px : 3 colonnes.
- 850–1100px : colonnes latérales réduites.
- < 850px : passage en colonne unique empilée (voir media queries de [App.css](../../frontend/src/App.css)).
