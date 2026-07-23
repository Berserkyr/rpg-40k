/**
 * BIBLIOTHÈQUE DE MODÈLES 3D GÉNÉRÉS AUTOMATIQUEMENT
 * Ce fichier est mis à jour par le générateur IA
 * 
 * Pour générer de nouveaux modèles:
 * 1. Allez sur http://localhost:5174/generator
 * 2. Choisissez faction, types, complexité
 * 3. Cliquez sur "Générer" - le code s'ajoute automatiquement ici
 * 
 * Pour utiliser un modèle:
 * import { buildModelName } from './GeneratedModels.js';
 * const model = buildModelName(scale);
 * scene.add(model);
 */
import * as THREE from 'three';
import { createVoxel, PALETTES } from './VoxelEngine.js';

// ============================================================================
// MODÈLES GÉNÉRÉS
// ============================================================================

// Les modèles générés apparaîtront ici automatiquement

// ============================================================================
// Généré le 14/07/2026
// ============================================================================

export function buildSpaceMarine(scale = 1) {
  const model = new THREE.Group();
  
  // Corps du Space Marine
  for (let x = -1; x <= 1; x += 0.4) {
    for (let y = 0; y <= 2.4; y += 0.4) {
      for (let z = -0.6; z <= 0.6; z += 0.4) {
        const voxel = createVoxel(PALETTES.armor[0], 0.4 * scale);
        voxel.position.set(x * scale, y * scale, z * scale);
        model.add(voxel);
      }
    }
  }

  // Détails lumineux pour les yeux
  const eyeGlow = createVoxel(PALETTES.energy[0], 0.2 * scale, {
    emissive: PALETTES.energy[1],
    emissiveIntensity: 1
  });
  eyeGlow.position.set(0, 2 * scale, 0.4 * scale);
  model.add(eyeGlow);

  // Insigne sur la poitrine
  const insignia = createVoxel(PALETTES.imperial_blue[0], 0.3 * scale, {
    shininess: 50
  });
  insignia.position.set(0, 1.5 * scale, -0.5 * scale);
  model.add(insignia);

  return model;
}

export function buildImperialGuard(scale = 1) {
  const model = new THREE.Group();
  
  // Corps et arms de l'Imperial Guard
  for (let x = -1; x <= 1; x += 0.4) {
    for (let y = 0; y <= 2; y += 0.4) {
      for (let z = -0.5; z <= 0.5; z += 0.4) {
        const voxel = createVoxel(PALETTES.imperial_blue[0], 0.4 * scale);
        voxel.position.set(x * scale, y * scale, z * scale);
        model.add(voxel);
      }
    }
  }

  // Casque avec détails
  const helmetDetail = createVoxel(PALETTES.gold[0], 0.5 * scale, {
    shininess: 80,
    emissive: PALETTES.gold[1],
    emissiveIntensity: 0.5
  });
  helmetDetail.position.set(0, 1.8 * scale, 0);
  model.add(helmetDetail);

  return model;
}

export function buildBolter(scale = 1) {
  const model = new THREE.Group();
  
  // Canon du bolter
  for (let x = -1; x <= 1; x += 0.2) {
    for (let y = -0.2; y <= 0.2; y += 0.4) {
      for (let z = -0.4; z <= 0.4; z += 0.2) {
        const voxel = createVoxel(PALETTES.metal[0], 0.2 * scale);
        voxel.position.set(x * scale, y * scale, z * scale);
        model.add(voxel);
      }
    }
  }

  // Détails lumineux pour l'énergie du bolter
  const energyGlow = createVoxel(PALETTES.energy[0], 0.4 * scale, {
    emissive: PALETTES.energy[1],
    emissiveIntensity: 0.7
  });
  energyGlow.position.set(0, 0.1 * scale, 0.5 * scale);
  model.add(energyGlow);

  return model;
}

export function buildImperialVehicle(scale = 1) {
  const model = new THREE.Group();
  
  // Structure du véhicule
  for (let x = -2; x <= 2; x += 0.8) {
    for (let y = -1; y <= 1; y += 0.8) {
      for (let z = -1 * scale; z <= 1 * scale; z += 0.8) {
        const voxel = createVoxel(PALETTES.armor[0], 0.8 * scale);
        voxel.position.set(x * scale, y * scale, z * scale);
        model.add(voxel);
      }
    }
  }

  // Détails de lumière sur le véhicule
  const lightDetail = createVoxel(PALETTES.energy[0], 0.4 * scale, {
    emissive: PALETTES.energy[1],
    emissiveIntensity: 1
  });
  lightDetail.position.set(0, 1 * scale, 0);
  model.add(lightDetail);

  return model;
}

export function buildGothicStructure(scale = 1) {
  const model = new THREE.Group();

  // Structure de base de l'église gothique
  for (let x = -2; x <= 2; x += 0.8) {
    for (let y = 0; y <= 4; y += 0.8) {
      for (let z = -1; z <= 1; z += 0.8) {
        const voxel = createVoxel(PALETTES.imperial_blue[0], 0.8 * scale);
        voxel.position.set(x * scale, y * scale, z * scale);
        model.add(voxel);
      }
    }
  }

  // Détails ornementaux dorés
  const ornateDetail = createVoxel(PALETTES.gold[0], 0.5 * scale, {
    shininess: 100,
    emissive: PALETTES.gold[1],
    emissiveIntensity: 0.3
  });
  ornateDetail.position.set(0, 4 * scale, 0);
  model.add(ornateDetail);

  return model;
}

