# 🎮 Moteur 3D Voxel - Combat RPG 40K

## Vue d'ensemble

Moteur de rendu 3D complet utilisant **Three.js** pour créer des combats immersifs en **pixel art 3D / voxel** (style Minecraft/rétro).

### Fonctionnalités principales

✨ **Personnages 3D procéduraux** - Génération automatique de modèles voxel
- Humanoïdes (Space Marines, Gardes Impériaux, Chaos, etc.)
- Monstres aliens (Tyranides, Orques)
- Détails : armures, armes, casques, tenues selon faction

🎬 **Système d'animation skeletal**
- Keyframe-based avec interpolation smooth
- Animations : idle, attack_melee, attack_shoot, hurt, death, victory, walk
- Inverse kinematics pour mouvements réalistes
- Support des rotations, positions et scales

🏗️ **Environnements 3D**
- Thèmes : Industrial, Temple, Wasteland
- Génération procédurale : sol, murs, obstacles, couvertures
- Occultation et fog pour profondeur

💥 **Effets visuels spectaculaires**
- Particules 3D : sang, étincelles, énergie, explosions
- Camera shake avec intensité variable
- Flash d'écran coloré selon le type d'attaque
- Physique des particules (gravité, vélocité, fade)

🎨 **Rendu pixel art**
- Caméra orthographique pour look 2D isométrique
- Image rendering pixelated (crisp-edges)
- Palettes de couleurs thématiques (40K)
- Flat shading pour look voxel/pixel

## Structure du code

```
frontend/src/
├── engine3d/
│   ├── VoxelEngine.js          # Génération de modèles voxel
│   ├── AnimationSystem.js      # Système d'animation skeletal
│   └── CombatScene3D.js        # Gestionnaire de scène 3D
├── components/
│   ├── Combat3DView.jsx        # Composant React principal
│   └── Combat3DView.css        # Styles
└── pages/
    └── Combat3DDemo.jsx        # Page de démo/test
```

## Accès à la démo

1. **Serveur de développement** : `http://localhost:5174/combat3d`
2. **Production** : `http://89.116.111.166/combat3d`

## Utilisation

### Composant de base

```jsx
import Combat3DView from './components/Combat3DView';

<Combat3DView
  playerData={{
    faction: 'imperial',
    armorLevel: 'medium',
    weapon: 'bolter'
  }}
  enemies={[
    {
      type: 'tyranid_warrior',
      scale: 1.8
    }
  ]}
  currentAction={{
    type: 'attack',
    entityId: 'player',
    targetId: 'enemy0',
    animName: 'attack_melee',
    effectType: 'melee'
  }}
  onAnimationComplete={(action) => {
    console.log('Animation terminée', action);
  }}
/>
```

### API de la scène 3D

```js
import { CombatScene3D } from './engine3d/CombatScene3D';

// Créer la scène
const scene = new CombatScene3D(canvasElement);

// Ajouter des entités
const playerAnimator = scene.addPlayer('player', {
  faction: 'imperial',
  weapon: 'bolter'
});

const enemyAnimator = scene.addEnemy('enemy1', {
  type: 'tyranid_warrior',
  scale: 1.5
});

// Jouer des animations
scene.playAnimation('player', 'attack_melee', false);

// Créer des effets
scene.createParticleEffect(
  new THREE.Vector3(8, 5, 0), // Position
  'spark',                     // Type
  20                           // Nombre de particules
);

scene.shakeCamera(2.0, 0.3);  // Intensité, durée
scene.flashScreen(0xffffff, 0.5, 0.1);

// Changer l'environnement
scene.createEnvironment('wasteland');
```

## Personnalisation des modèles

### Humanoïdes

```js
import { HumanoidVoxelBuilder } from './engine3d/VoxelEngine';

const builder = new HumanoidVoxelBuilder();
const { model, parts, skeleton } = builder.build({
  faction: 'imperial',      // imperial, tyranid, ork, chaos
  bodyType: 'human',        // human, bestial, machine
  armorLevel: 'heavy',      // light, medium, heavy
  weapon: 'bolter',         // bolter, chainsword, lasgun
  scale: 1.2
});
```

### Monstres

```js
import { MonsterVoxelBuilder } from './engine3d/VoxelEngine';

const builder = new MonsterVoxelBuilder();
const { model, parts, skeleton } = builder.build({
  type: 'tyranid_warrior',  // tyranid_warrior, ork_boy
  variant: 0,                // 0-N pour variations
  scale: 1.8
});
```

## Création d'animations personnalisées

```js
const customAnimation = {
  duration: 1000, // ms
  tracks: [
    {
      part: 'rightArm',    // Partie du corps
      keyframes: [
        { 
          time: 0,         // 0-1 (progression)
          position: [2, 4, 0],
          rotation: [0, 0, 0],
          scale: 1
        },
        { 
          time: 0.5,
          position: [2.5, 2, -1],
          rotation: [0.8, 0, -0.3],
          scale: 1.1
        },
        { 
          time: 1.0,
          position: [2, 4, 0],
          rotation: [0, 0, 0],
          scale: 1
        }
      ]
    }
    // ... autres tracks
  ]
};

animator.registerAnimation('my_attack', customAnimation);
animator.play('my_attack', false);
```

## Thèmes d'environnement

- **Industrial** : Usine sombre, métal, débris industriels
- **Temple** : Pierre ancienne, dorures, atmosphère sacrée
- **Wasteland** : Désert post-apocalyptique, ruines, végétation rare

## Performance

- **~60 FPS** avec 2-4 entités + environnement complet
- **Shadow maps** 1024x1024 pour ombres dynamiques
- **Particle pooling** pour minimiser GC
- **LOD automatique** sur les obstacles distants

## Types de particules

- `spark` : Étincelles métalliques (impacts, frottements)
- `blood` : Éclaboussures de sang (dégâts biologiques)
- `energy` : Plasma/énergie (armes futuristes)
- `explosion` : Déflagration (explosifs, pouvoirs)
- `muzzle_flash` : Éclat de tir (armes à feu)

## Intégration au système de combat

Pour intégrer le moteur 3D au flux de combat principal :

```jsx
// Dans CombatPanel.jsx
import Combat3DView from './Combat3DView';

// Remplacer l'ancien système d'affichage par :
<Combat3DView
  playerData={{
    faction: state.character.faction,
    weapon: state.inventory.equipped.weapon?.name
  }}
  enemies={activeCombat.enemies.map(e => ({
    type: e.type,
    faction: e.faction_key,
    scale: e.difficulty > 3 ? 1.5 : 1.2
  }))}
  currentAction={currentCombatAction}
  onAnimationComplete={handleActionComplete}
/>
```

## Roadmap futures améliorations

🚀 **V2 - Améliorations prévues**
- [ ] Pixelation post-processing shader (rendu encore plus pixel art)
- [ ] Animations plus complexes (combo chains, esquive, parade)
- [ ] Modèles plus détaillés (badges, insignes, customisation)
- [ ] Effets météo (pluie, brouillard épais, tempête)
- [ ] Destruction d'environnement (obstacles destructibles)
- [ ] Ragdoll physics pour les morts
- [ ] Système de lumières dynamiques (torches, projectiles lumineux)

## Dépendances

- `three@^0.170.0` - Moteur 3D WebGL
- React 19.2.6 - Framework UI

## Notes techniques

### Pourquoi voxel/pixel art ?

- **Pas besoin de modèles 3D externes** - Tout est généré procéduralement
- **Style cohérent** avec l'esthétique rétro/old-school
- **Performances optimales** - Géométrie simple
- **Extensible facilement** - Ajouter des voxels = ajouter des cubes
- **Pas de textures à gérer** - Couleurs flat

### Caméra orthographique vs perspective

On utilise une **caméra orthographique** pour :
- Maintenir le style pixel art 2D
- Pas de distorsion de perspective
- Distances prévisibles pour le gameplay
- Look "isométrique" familier aux RPG classiques

### Flat shading

Le `flatShading: true` sur les materials donne l'effet "facetté" parfait pour le pixel art 3D, où chaque face de voxel est une couleur unie.

## Support

Testé sur navigateurs modernes avec WebGL 2.0 :
- ✅ Chrome/Edge 100+
- ✅ Firefox 100+
- ✅ Safari 15+

---

**Créé pour RPG 40K** - Moteur de combat immersif nouvelle génération 🎮⚔️
