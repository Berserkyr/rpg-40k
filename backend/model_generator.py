"""
Générateur de modèles 3D voxel via LLM.
Crée dynamiquement du code JavaScript pour des modèles procéduraux.
"""
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
import openai


GENERATED_MODELS_FILE = Path(__file__).parent.parent / "frontend" / "src" / "engine3d" / "GeneratedModels.js"

# Instructions système pour la génération de modèles 3D
MODEL_GENERATION_SYSTEM_PROMPT = """Tu es un expert en génération procédurale de modèles 3D voxel pour un jeu Warhammer 40K.
Tu génères du code JavaScript qui crée des modèles 3D en assemblant des voxels (cubes).

Le code doit utiliser cette API:
- createVoxel(color, size, options) : crée un cube
- PALETTES : objet contenant des palettes de couleurs (skin, metal, gold, armor, tyranid, ork, chaos, energy, imperial_blue, imperial_gold, white, blood)
- THREE.Group() pour assembler les voxels

Format de fonction requis:
```javascript
export function build{NomModele}(scale = 1) {
  const model = new THREE.Group();
  
  // Corps du modèle avec des voxels
  for (let x = -2; x <= 2; x += 0.8) {
    for (let y = 0; y <= 3; y += 0.8) {
      for (let z = -1; z <= 1; z += 0.8) {
        const voxel = createVoxel(PALETTES.armor[0], 0.8 * scale);
        voxel.position.set(x * scale, y * scale, z * scale);
        model.add(voxel);
      }
    }
  }
  
  // Détails avec options
  const detail = createVoxel(PALETTES.gold[0], 0.5 * scale, {
    shininess: 100,
    emissive: PALETTES.gold[1],
    emissiveIntensity: 0.3
  });
  detail.position.set(0, 2 * scale, -1 * scale);
  model.add(detail);
  
  return model;
}
```

Directives créatives:
- Warhammer 40K: style gothique, massif, ornementation excessive
- Utilise les couleurs des palettes de manière cohérente:
  * Imperial: blue + gold + white
  * Chaos: chaos (rouge foncé) + blood + metal
  * Tyranid: tyranid (violet) + blood + skin modifié
  * Ork: ork (vert) + metal rouillé + blood
- Ajoute des détails lumineux (emissive) pour les yeux, armes énergétiques, runes
- Varie les tailles de voxels (0.4 à 1.2) pour les détails
- Options importantes: shininess (30-100), emissive + emissiveIntensity pour lumières
- Les modèles doivent être centrés sur l'origine (0, 0, 0)
- Utilise scale parameter pour permettre le redimensionnement

Types de modèles à créer:
1. **Personnages humanoïdes**: Space Marines (différents chapitres), Garde Impériale, Cultistes
2. **Xenos**: Tyranides (diverses biomorphes), Eldars, Tau
3. **Armes**: Bolters variés, épées énergétiques, fusils plasma, lanceurs lourds
4. **Véhicules**: Rhino, Dreadnought, Speeder
5. **Structures**: Fortifications, autels, générateurs
6. **Créatures**: Démons, bêtes de guerre

Retourne UNIQUEMENT le code JavaScript valide, sans texte additionnel ni balises markdown."""


def generate_models_with_llm(
    model_types: List[str],
    faction: str = "Imperial",
    count: int = 5,
    complexity: str = "medium"
) -> Optional[str]:
    """
    Génère du code JavaScript pour des modèles 3D voxel via OpenAI API.
    
    Args:
        model_types: Liste de types (character, weapon, vehicle, structure, creature)
        faction: Faction Warhammer 40K (Imperial, Chaos, Tyranid, Ork, Eldar)
        count: Nombre de modèles à générer
        complexity: Niveau de détails (simple, medium, high)
    
    Returns:
        Code JavaScript ou None si échec
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY non configurée, génération impossible")
        return None
    
    complexity_voxel_counts = {
        "simple": "50-150 voxels",
        "medium": "150-400 voxels", 
        "high": "400-1000 voxels"
    }
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        user_prompt = f"""Génère {count} fonctions de modèles 3D voxel pour Warhammer 40K:

Faction: {faction}
Types: {', '.join(model_types)}
Complexité: {complexity} ({complexity_voxel_counts.get(complexity, '150-400 voxels')})

Exigences:
- {count} fonctions build{{Nom}}() distinctes et créatives
- Style visuel cohérent avec la faction {faction}
- Détails: yeux lumineux, insignes, armes, armures
- Utilise PALETTES pour les couleurs faction
- Ajoute des commentaires décrivant chaque section du modèle
- Toutes les fonctions doivent être exportées (export function)

Le code doit être prêt à être copié dans GeneratedModels.js et importé.
Commence DIRECTEMENT par les imports Three.js nécessaires, puis les fonctions."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": MODEL_GENERATION_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9,  # Plus créatif
            max_tokens=4000   # Beaucoup de code
        )
        
        generated_code = response.choices[0].message.content.strip()
        
        # Nettoie les balises markdown si présentes
        if generated_code.startswith("```"):
            lines = generated_code.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            generated_code = "\n".join(lines)
        
        return generated_code
        
    except Exception as e:
        print(f"Erreur génération modèles: {e}")
        return None


def append_to_generated_models(code: str) -> bool:
    """
    Ajoute du code généré au fichier GeneratedModels.js.
    """
    try:
        # Crée le fichier s'il n'existe pas
        if not GENERATED_MODELS_FILE.exists():
            GENERATED_MODELS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(GENERATED_MODELS_FILE, 'w', encoding='utf-8') as f:
                f.write("""/**
 * BIBLIOTHÈQUE DE MODÈLES 3D GÉNÉRÉS AUTOMATIQUEMENT
 * Ce fichier est mis à jour par le générateur IA
 */
import * as THREE from 'three';
import { createVoxel, PALETTES } from './VoxelEngine.js';

// ============================================================================
// MODÈLES GÉNÉRÉS
// ============================================================================

""")
        
        # Ajoute le nouveau code
        with open(GENERATED_MODELS_FILE, 'a', encoding='utf-8') as f:
            f.write("\n// " + "=" * 76 + "\n")
            f.write(f"// Généré le {os.popen('date /t').read().strip() if os.name == 'nt' else os.popen('date').read().strip()}\n")
            f.write("// " + "=" * 76 + "\n\n")
            f.write(code)
            f.write("\n\n")
        
        return True
        
    except Exception as e:
        print(f"Erreur écriture fichier: {e}")
        return False


def generate_and_save_models(
    model_types: List[str],
    faction: str = "Imperial",
    count: int = 5,
    complexity: str = "medium"
) -> Dict[str, Any]:
    """
    Génère des modèles et les sauvegarde directement dans le projet.
    
    Returns:
        Dict avec status, message, code généré
    """
    print(f"🎨 Génération de {count} modèles {faction} ({complexity})...")
    
    code = generate_models_with_llm(model_types, faction, count, complexity)
    
    if not code:
        return {
            "success": False,
            "message": "Échec de la génération (API indisponible?)",
            "code": None
        }
    
    if not append_to_generated_models(code):
        return {
            "success": False,
            "message": "Erreur d'écriture dans GeneratedModels.js",
            "code": code
        }
    
    print(f"✅ Modèles générés et ajoutés à {GENERATED_MODELS_FILE.name}")
    
    return {
        "success": True,
        "message": f"{count} modèles {faction} générés avec succès",
        "code": code,
        "file": str(GENERATED_MODELS_FILE)
    }


# CLI pour tests
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python model_generator.py <faction> [count] [complexity]")
        print("Factions: Imperial, Chaos, Tyranid, Ork, Eldar")
        print("Complexity: simple, medium, high")
        sys.exit(1)
    
    faction = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    complexity = sys.argv[3] if len(sys.argv) > 3 else "medium"
    
    result = generate_and_save_models(
        model_types=["character", "weapon"],
        faction=faction,
        count=count,
        complexity=complexity
    )
    
    if result["success"]:
        print(f"\n✅ {result['message']}")
        print(f"📁 Fichier: {result['file']}")
    else:
        print(f"\n❌ {result['message']}")
