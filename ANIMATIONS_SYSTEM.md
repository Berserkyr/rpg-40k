# Système d'animations procédurales générées par LLM

Ce système permet de générer et réutiliser automatiquement des animations pour les skills de combat sans avoir à les coder manuellement à chaque fois.

## 🎯 Architecture

### Backend
- **`animations_cache.json`** : Cache persistant des animations générées
- **`animation_generator.py`** : Générateur d'animations via OpenAI API
- **`api.py`** : Endpoints REST pour récupérer/générer/gérer les animations

### Frontend
- **`animation_engine.js`** : Moteur d'interprétation des descripteurs JSON
- **`AnimatedAction.jsx`** : Composant React réutilisable pour animer n'importe quel élément
- **Cache client** : Les animations récupérées sont mises en cache côté client

## 🔄 Workflow

```
1. Un skill est utilisé en combat
   ↓
2. Le frontend demande l'animation via /api/animations/{skill_id}
   ↓
3. Le backend vérifie le cache JSON
   ↓
4. Si absent : génère via GPT-4 et sauvegarde
   ↓
5. Retourne le descripteur JSON au frontend
   ↓
6. Le moteur d'animation interprète et exécute
   ↓
7. Mise en cache côté client pour réutilisation immédiate
```

## 📝 Format des animations

Les animations sont des descripteurs JSON structurés :

```json
{
  "skill_id": "tir_de_precision",
  "name": "Tir de précision",
  "duration": 800,
  "phases": [
    {
      "name": "visée",
      "start": 0,
      "end": 0.3,
      "easing": "easeOut",
      "transforms": {
        "scale": [1.0, 1.15],
        "rotation": [0, -0.1]
      }
    },
    {
      "name": "tir",
      "start": 0.3,
      "end": 0.6,
      "easing": "easeIn",
      "transforms": {
        "translateX": [0, -10],
        "scale": [1.15, 0.95]
      }
    }
  ],
  "particles": [
    {
      "type": "muzzle_flash",
      "at": 0.3,
      "color": "#ff9933",
      "count": 5,
      "spread": 25,
      "speed": 80
    }
  ],
  "cameraShake": {
    "at": 0.3,
    "intensity": 2.0
  }
}
```

## 🚀 Utilisation

### 1. Utilisation basique avec AnimatedAction

```jsx
import AnimatedAction from './components/AnimatedAction';
import EnemySprite from './components/EnemySprite';

function CombatScene() {
  const [attackTrigger, setAttackTrigger] = useState(0);
  
  return (
    <AnimatedAction
      skillId="default_attack"
      skillInfo={{
        name: "Attaque standard",
        description: "Une attaque de mêlée basique",
        category: "combat"
      }}
      trigger={attackTrigger}
      onComplete={() => console.log("Animation terminée!")}
      facing="left"
    >
      <EnemySprite faction="tyranide" archetype="beast" />
    </AnimatedAction>
  );
}
```

### 2. Intégration avec le système de combat

Modifier `CombatPanel.jsx` pour wrapper les EnemySprite avec AnimatedAction :

```jsx
import AnimatedAction from './AnimatedAction';

// Dans le rendu des ennemis :
<AnimatedAction
  skillId={fx.action === 'attack' ? 'enemy_attack' : fx.action}
  trigger={fx.seq}
  facing={i % 2 === 0 ? 'left' : 'right'}
  onComplete={() => {
    // Réinitialiser l'action après l'animation
    setEnemyFx(old => {
      const newFx = [...old];
      newFx[i] = { action: 'idle', seq: fx.seq };
      return newFx;
    });
  }}
>
  <EnemySprite
    faction={e.faction}
    archetype={e.archetype}
    threat={e.threat}
    name={e.name}
    dead={e.is_dead}
  />
</AnimatedAction>
```

### 3. Générer une animation via l'API

**GET** `/api/animations/{skill_id}` - Récupère depuis le cache

**POST** `/api/animations/generate` - Génère ou récupère
```json
{
  "skill_id": "tir_plasma",
  "skill_name": "Tir de plasma",
  "skill_description": "Tire un projectile d'énergie plasma incandescent qui inflige des dégâts massifs",
  "skill_category": "ranged"
}
```

**GET** `/api/animations` - Liste toutes les animations en cache

**DELETE** `/api/animations/{skill_id}` - Supprime du cache (admin)

## 🎨 Types de transforms disponibles

- **translateX** / **translateY** : Déplacement en pixels
- **rotation** : Rotation en radians
- **scale** : Échelle (1.0 = normal)
- **opacity** : Transparence (0-1)

### Valeurs spéciales
- `"oscillate"` : Oscillation (nécessite `oscillateFreq` et `oscillateAmp`)
- `"shake"` : Tremblement aléatoire (nécessite `shakeAmp`)

## ✨ Types de particules

- **spark** / **muzzle_flash** : Éclairs/flash d'arme
- **blood** / **blood_splatter** : Sang
- **energy** / **aura** : Énergie psyker/magique
- **projectile** : Projectile dirigé
- **explosion** : Explosion

## 🎮 Fonctions d'easing disponibles

- `linear` : Linéaire
- `easeIn` / `easeOut` / `easeInOut` : Quadratique
- `easeInCubic` / `easeOutCubic` : Cubique
- `easeInQuart` / `easeOutQuart` : Quartique

## 🔧 Fonctions utilitaires

### Backend (animation_generator.py)

```python
from backend.animation_generator import (
    get_or_generate_animation,  # Récupère ou génère
    get_cached_animation,        # Récupère uniquement du cache
    list_cached_animations,      # Liste les IDs en cache
    clear_animation_cache,       # Efface le cache
)

# Exemple
animation = get_or_generate_animation(
    skill_id="epee_electrique",
    skill_name="Épée électrique",
    skill_description="Une lame crépitante d'énergie électrique",
    skill_category="melee"
)
```

### Frontend (animation_engine.js)

```javascript
import {
  fetchAnimation,              // Récupère via API + cache client
  preloadAnimations,           // Précharge plusieurs animations
  clearClientAnimationCache,   // Efface cache client
  AnimationPlayer,             // Classe pour gérer une animation
} from './animation_engine';

// Précharger des animations
await preloadAnimations(['attack', 'shoot', 'psyker_bolt']);

// Utiliser manuellement le player
const player = new AnimationPlayer(descriptor);
player.start();
const state = player.update(performance.now());
// state contient: { transforms, particles, cameraShake, flash, isComplete }
```

## 🧪 Tests

Tester la génération d'une animation :

```bash
# Backend
pytest tests/test_animations.py

# Frontend
npm test -- AnimatedAction
```

## 📦 Configuration

Le système nécessite une clé API OpenAI dans `.env` :

```env
OPENAI_API_KEY=sk-...
```

Sans clé API, le système utilise des animations par défaut prédéfinies.

## 🎯 Conventions de nommage des skills

- **Mêlée** : `melee_XXX` (ex: `melee_slash`, `melee_heavy`)
- **Tir** : `ranged_XXX` ou `shoot_XXX` (ex: `ranged_laser`, `shoot_plasma`)
- **Psyker** : `psyker_XXX` (ex: `psyker_bolt`, `psyker_warp`)
- **Support** : `buff_XXX`, `heal_XXX` (ex: `buff_inspire`, `heal_medkit`)
- **Réaction** : `hurt`, `death`, `dodge`, `block`

## 🚀 Optimisations futures

- [ ] Préchargement des animations au début du combat
- [ ] Compression du cache JSON (animations similaires)
- [ ] Animations par faction (styles visuels spécifiques)
- [ ] Système de variantes (même skill, animation différente selon arme/faction)
- [ ] Editor d'animations in-game (admin)

## 🎨 Exemples d'animations pré-générées

Le système vient avec 4 animations de base :
- **default_attack** : Attaque de mêlée standard
- **shoot** : Tir à distance
- **hurt** : Réaction aux dégâts
- **death** : Animation de mort

Toutes les autres animations sont générées dynamiquement à la demande.
