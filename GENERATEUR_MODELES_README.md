# 🎨 Générateur de Modèles 3D IA

## Vue d'ensemble

Système de génération automatique de modèles 3D voxel Warhammer 40K utilisant GPT-4.
Le code généré s'intègre automatiquement dans votre projet.

## ✨ Fonctionnalités

- **Génération via GPT-4**: L'IA crée du code JavaScript de modèles voxel
- **Auto-intégration**: Le code est automatiquement ajouté à `GeneratedModels.js`
- **Interface web**: Interface graphique à `/generator`
- **Factions variées**: Imperial, Chaos, Tyranid, Ork, Eldar, Tau, Necron
- **Types multiples**: Personnages, armes, véhicules, structures, créatures
- **Complexité ajustable**: Simple (50-150 voxels), Medium (150-400), High (400-1000)

## 🚀 Utilisation

### 1. Via l'interface web

```bash
# Démarrer le backend
cd backend
uvicorn api:app --reload

# Démarrer le frontend
cd frontend
npm run dev

# Ouvrir http://localhost:5174/generator
```

1. **Choisir une faction** (Imperial, Chaos, etc.)
2. **Sélectionner les types** de modèles (character, weapon, etc.)
3. **Ajuster les paramètres**:
   - Nombre: 1-20 modèles
   - Complexité: simple/medium/high
4. **Cliquer "Générer"**

Le code est automatiquement ajouté à `frontend/src/engine3d/GeneratedModels.js`

### 2. Via CLI (ligne de commande)

```bash
# Activer l'environnement
.\.venv\Scripts\Activate.ps1

# Générer des modèles
python backend/model_generator.py <faction> [count] [complexity]

# Exemples
python backend/model_generator.py Imperial 5 medium
python backend/model_generator.py Chaos 10 high
python backend/model_generator.py Tyranid 3 simple
```

### 3. Via API REST

```bash
POST http://localhost:8000/api/models/generate
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "model_types": ["character", "weapon"],
  "faction": "Imperial",
  "count": 5,
  "complexity": "medium"
}
```

## 📦 Utiliser les modèles générés

```javascript
// Importer les fonctions générées
import { 
  buildSpaceMarineSergeant, 
  buildBolterMkII,
  buildTyranidWarrior 
} from './engine3d/GeneratedModels.js';

// Créer un modèle
const marine = buildSpaceMarineSergeant(1.0); // scale = 1.0
scene.add(marine);

// Créer une arme
const bolter = buildBolterMkII(0.8); // scale = 0.8
marine.add(bolter);

// Positionner
marine.position.set(5, 0, 0);
```

## 🎯 Exemples de génération

### Escouade Space Marine complète
```javascript
// Générer 10 Space Marines variés
faction: "Imperial"
types: ["character"]
count: 10
complexity: "high"
```

### Arsenal complet
```javascript
// 15 armes Imperial
faction: "Imperial"
types: ["weapon"]
count: 15
complexity: "medium"
```

### Armée Tyranid
```javascript
// Divers biomorphes
faction: "Tyranid"
types: ["character", "creature"]
count: 20
complexity: "high"
```

### Environnement complet
```javascript
// Structures et fortifications
faction: "Imperial"
types: ["structure", "vehicle"]
count: 8
complexity: "medium"
```

## ⚙️ Configuration

### Variables d'environnement

```env
# .env à la racine
OPENAI_API_KEY=sk-proj-...
```

### Permissions

- **Génération**: Réservée aux admins (évite la surcharge)
- **Lecture**: Tous les utilisateurs peuvent utiliser les modèles générés

## 🏗️ Architecture

```
backend/
  model_generator.py       # Générateur IA
  api.py                   # Endpoint /api/models/generate

frontend/src/
  pages/
    ModelGenerator.jsx     # Interface web
    ModelGenerator.css     # Styles
  engine3d/
    GeneratedModels.js     # Bibliothèque (auto-générée)
    VoxelEngine.js         # API de base (createVoxel, PALETTES)
```

## 🎨 Prompts IA

Le système utilise des prompts spécialisés pour:

1. **Style Warhammer 40K**: Gothique, massif, ornementation
2. **Cohérence faction**: Couleurs et formes appropriées
3. **Optimisation**: Nombre de voxels contrôlé
4. **Détails**: Yeux lumineux, insignes, armes, armures
5. **Code propre**: Commentaires, structure claire

## 📊 Performances

- **Simple** (50-150 voxels): ~2-5ms de rendu
- **Medium** (150-400 voxels): ~5-15ms  
- **High** (400-1000 voxels): ~15-40ms

Target: 60 FPS avec 10-20 entités à l'écran

## 🔧 Dépannage

### "OPENAI_API_KEY non configurée"
```bash
# Vérifier le .env
cat .env | grep OPENAI_API_KEY

# Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1
```

### "401 Unauthorized"
```bash
# Se connecter en admin
# Login: admin
# Password: voir dans la base de données
```

### Le fichier GeneratedModels.js n'est pas mis à jour
```bash
# Vérifier les permissions d'écriture
ls -la frontend/src/engine3d/GeneratedModels.js

# Voir les logs backend
# Les erreurs d'écriture apparaissent dans la console uvicorn
```

## 🚀 Workflow recommandé

1. **Phase 1**: Générer personnages de base (5-10 modèles, medium)
2. **Phase 2**: Générer armes (10-15 modèles, simple)
3. **Phase 3**: Générer créatures (8-12 modèles, high)
4. **Phase 4**: Générer véhicules (3-5 modèles, high)
5. **Phase 5**: Générer structures (5-8 modèles, medium)

Total: ~50-100 modèles uniques pour une bibliothèque complète

## 🎮 Intégration Combat

```javascript
// Dans CombatScene3D.js
import * as GeneratedModels from './GeneratedModels.js';

// Utiliser des modèles générés aléatoirement
addEnemy(enemyData) {
  const modelFunctions = Object.keys(GeneratedModels)
    .filter(key => key.startsWith('buildTyranid'));
  
  const randomBuilder = GeneratedModels[
    modelFunctions[Math.floor(Math.random() * modelFunctions.length)]
  ];
  
  const model = randomBuilder(1.0);
  // ... suite du code
}
```

## 📝 Licence

Ce système génère du code qui appartient à votre projet.
Les modèles générés sont à vous.

---

**Note**: La génération consomme des tokens OpenAI.
Coût approximatif: ~0.01$ par modèle (complexité medium).
