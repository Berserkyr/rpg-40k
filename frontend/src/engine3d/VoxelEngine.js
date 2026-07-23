/**
 * Moteur 3D de rendu voxel pour animations pixel art
 * 
 * Génère des personnages, monstres, armes et environnements en voxels
 * avec animations skeletal et rendu pixel art stylisé.
 */

import * as THREE from 'three';

const voxelGeometryCache = new Map();
const voxelMaterialCache = new Map();

function getVoxelGeometry(size) {
  if (!voxelGeometryCache.has(size)) {
    voxelGeometryCache.set(size, new THREE.BoxGeometry(size, size, size));
  }
  return voxelGeometryCache.get(size);
}

function getVoxelMaterial(color, options) {
  const { shininess = 30, emissive = 0x000000, emissiveIntensity = 0, specular = 0x444444 } = options;
  const key = `${color}:${shininess}:${emissive}:${emissiveIntensity}:${specular}`;
  if (!voxelMaterialCache.has(key)) {
    voxelMaterialCache.set(key, new THREE.MeshPhongMaterial({
      color,
      flatShading: true,
      shininess,
      emissive,
      emissiveIntensity,
      specular,
    }));
  }
  return voxelMaterialCache.get(key);
}

/**
 * Crée un voxel (cube) avec couleur et options
 */
export function createVoxel(color = 0xffffff, size = 1, options = {}) {
  const mesh = new THREE.Mesh(getVoxelGeometry(size), getVoxelMaterial(color, options));
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  return mesh;
}

/**
 * Palette de couleurs pixel art
 */
export const PALETTES = {
  skin: [0xffd5a6, 0xffb380, 0xff9966, 0xd97a4d],
  metal: [0xf0f0f0, 0xcccccc, 0x999999, 0x666666],
  gold: [0xffd700, 0xffaa00, 0xff8800, 0xcc6600],
  blood: [0xff0000, 0xcc0000, 0x990000, 0x660000],
  armor: [0x3399ff, 0x2277dd, 0x1155bb, 0x003388],
  tyranid: [0x9933ff, 0x7711dd, 0x5500bb, 0x330088],
  ork: [0x55dd33, 0x33bb11, 0x229900, 0x117700],
  chaos: [0xff3333, 0xdd1111, 0xbb0000, 0x880000],
  energy: [0x00ffff, 0x00ddff, 0x00bbff, 0x0099ff],
  imperial_blue: [0x0055ff, 0x0044dd, 0x0033bb, 0x002288],
  imperial_gold: [0xffdd00, 0xddbb00, 0xbb9900, 0x997700],
  white: [0xffffff, 0xeeeeee, 0xdddddd, 0xcccccc],
};

/**
 * Générateur procédural de corps humanoïde en voxels
 */
export class HumanoidVoxelBuilder {
  constructor() {
    this.parts = {};
    this.skeleton = {};
  }

  /**
   * Génère un humanoïde basique (40K style)
   */
  build({
    faction = 'imperial',
    bodyType = 'human',
    armorLevel = 'medium',
    weapon = 'bolter',
    scale = 1.0
  } = {}) {
    const group = new THREE.Group();
    
    // Palette selon faction
    const palette = this.getPalette(faction);
    
    // Corps (voxels empilés)
    this.parts.head = this.buildHead(palette);
    this.parts.torso = this.buildTorso(palette, armorLevel);
    this.parts.leftArm = this.buildArm(palette, 'left');
    this.parts.rightArm = this.buildArm(palette, 'right', weapon);
    this.parts.leftLeg = this.buildLeg(palette);
    this.parts.rightLeg = this.buildLeg(palette);
    
    // Positionnement
    this.parts.head.position.set(0, 7, 0);
    this.parts.torso.position.set(0, 3, 0);
    this.parts.leftArm.position.set(-2, 4, 0);
    this.parts.rightArm.position.set(2, 4, 0);
    this.parts.leftLeg.position.set(-1, -2, 0);
    this.parts.rightLeg.position.set(1, -2, 0);
    
    // Pivot points pour animation skeletal
    this.skeleton = {
      head: { joint: new THREE.Vector3(0, 6, 0) },
      leftShoulder: { joint: new THREE.Vector3(-2, 5, 0) },
      rightShoulder: { joint: new THREE.Vector3(2, 5, 0) },
      leftHip: { joint: new THREE.Vector3(-1, 1, 0) },
      rightHip: { joint: new THREE.Vector3(1, 1, 0) },
    };
    
    // Ajouter toutes les parties
    Object.values(this.parts).forEach(part => group.add(part));
    
    group.scale.multiplyScalar(scale);
    
    return { model: group, parts: this.parts, skeleton: this.skeleton };
  }

  getPalette(faction) {
    const factionPalettes = {
      imperial: { armor: PALETTES.armor[1], skin: PALETTES.skin[1], trim: PALETTES.gold[1] },
      tyranid: { armor: PALETTES.tyranid[0], skin: PALETTES.tyranid[1], trim: PALETTES.tyranid[2] },
      ork: { armor: PALETTES.ork[0], skin: PALETTES.ork[1], trim: PALETTES.metal[2] },
      chaos: { armor: PALETTES.chaos[0], skin: PALETTES.skin[2], trim: PALETTES.gold[2] },
    };
    return factionPalettes[faction] || factionPalettes.imperial;
  }

  buildHead(palette) {
    const head = new THREE.Group();
    
    // Crâne principal (agrandi pour mieux voir)
    for (let x = -1.2; x <= 1.2; x += 0.8) {
      for (let y = 0; y <= 2; y += 0.8) {
        for (let z = -1.2; z <= 0; z += 0.8) {
          const voxel = createVoxel(palette.skin, 0.8);
          voxel.position.set(x, y, z);
          head.add(voxel);
        }
      }
    }
    
    // Casque/heaume massif (style Space Marine)
    const helmetVoxels = [
      // Top du casque
      [0, 2.5, 0], [-0.8, 2.5, 0], [0.8, 2.5, 0],
      [0, 2.5, -0.8], [-0.8, 2.5, -0.8], [0.8, 2.5, -0.8],
      // Crête
      [0, 3.2, -0.4],
      // Côtés épais
      [1.6, 1.2, 0], [1.6, 1.2, -0.8],
      [-1.6, 1.2, 0], [-1.6, 1.2, -0.8],
      // Mentonnière
      [0, 0, -1.2], [-0.8, 0, -1.2], [0.8, 0, -1.2],
    ];
    
    helmetVoxels.forEach(([x, y, z]) => {
      const voxel = createVoxel(palette.armor, 0.8, { shininess: 60 });
      voxel.position.set(x, y, z);
      head.add(voxel);
    });
    
    // Détails dorés (aquila, insignes)
    const goldDetails = [
      [0, 1.6, -1.3], // Aquila centre
      [-0.4, 1.6, -1.3], [0.4, 1.6, -1.3], // Ailes
    ];
    goldDetails.forEach(([x, y, z]) => {
      const voxel = createVoxel(PALETTES.gold[0], 0.4, { shininess: 100 });
      voxel.position.set(x, y, z);
      head.add(voxel);
    });
    
    // Yeux lumineux (plus gros)
    const leftEye = createVoxel(0xff0000, 0.5, { emissive: 0xff0000, emissiveIntensity: 0.8 });
    leftEye.position.set(-0.4, 1.2, -1.4);
    const rightEye = createVoxel(0xff0000, 0.5, { emissive: 0xff0000, emissiveIntensity: 0.8 });
    rightEye.position.set(0.4, 1.2, -1.4);
    head.add(leftEye, rightEye);
    
    return head;
  }

  buildTorso(palette, armorLevel) {
    const torso = new THREE.Group();
    
    // Corps principal (plus large et détaillé)
    for (let x = -1.5; x <= 1.5; x += 0.8) {
      for (let y = 0; y <= 4; y += 0.8) {
        for (let z = -1.2; z <= 0.8; z += 0.8) {
          const voxel = createVoxel(palette.armor, 0.8, { shininess: 40 });
          voxel.position.set(x, y, z);
          torso.add(voxel);
        }
      }
    }
    
    // Plaques de plastron (détails en relief)
    const chestPlates = [
      // Plaques centrales
      [-0.4, 2.5, -1.3], [0.4, 2.5, -1.3],
      [-0.4, 3.2, -1.3], [0.4, 3.2, -1.3],
      // Abdomen segmenté
      [-0.6, 1.5, -1.3], [0, 1.5, -1.3], [0.6, 1.5, -1.3],
      [-0.6, 0.8, -1.3], [0, 0.8, -1.3], [0.6, 0.8, -1.3],
    ];
    chestPlates.forEach(([x, y, z]) => {
      const voxel = createVoxel(PALETTES.metal[0], 0.6, { shininess: 80 });
      voxel.position.set(x, y, z);
      torso.add(voxel);
    });
    
    // Épaulières MASSIVES (style Space Marine)
    if (armorLevel === 'heavy' || armorLevel === 'medium') {
      const shoulderPads = [
        // Gauche
        [-2.5, 4, 0], [-2.5, 4, -0.8], [-2.5, 3.2, 0], [-2.5, 3.2, -0.8],
        [-3, 3.6, -0.4], [-2.2, 4.5, -0.4],
        // Droite  
        [2.5, 4, 0], [2.5, 4, -0.8], [2.5, 3.2, 0], [2.5, 3.2, -0.8],
        [3, 3.6, -0.4], [2.2, 4.5, -0.4],
      ];
      shoulderPads.forEach(([x, y, z]) => {
        const voxel = createVoxel(PALETTES.imperial_gold[0], 0.9, { shininess: 90 });
        voxel.position.set(x, y, z);
        torso.add(voxel);
      });
    }
    
    // Aquila impériale géante (centre poitrine)
    const aquilaVoxels = [
      [0, 3, -1.4], // Corps
      [-0.6, 3, -1.4], [0.6, 3, -1.4], // Ailes
      [-0.9, 2.7, -1.4], [0.9, 2.7, -1.4], // Bout des ailes
      [0, 3.4, -1.4], // Tête
    ];
    aquilaVoxels.forEach(([x, y, z]) => {
      const voxel = createVoxel(PALETTES.gold[0], 0.5, { 
        shininess: 100,
        emissive: PALETTES.gold[1],
        emissiveIntensity: 0.3
      });
      voxel.position.set(x, y, z);
      torso.add(voxel);
    });
    
    return torso;
  }

  buildArm(palette, side, weapon = null) {
    const arm = new THREE.Group();
    
    // Bras (1x4x1)
    for (let y = 0; y <= 3; y++) {
      const voxel = createVoxel(palette.armor, 1);
      voxel.position.set(0, -y, 0);
      arm.add(voxel);
    }
    
    // Main
    const hand = createVoxel(palette.skin, 0.8);
    hand.position.set(0, -4, 0);
    arm.add(hand);
    
    // Arme si présente
    if (weapon && side === 'right') {
      const weaponModel = this.buildWeapon(weapon, palette);
      weaponModel.position.set(0, -3.5, -0.5);
      weaponModel.rotation.x = Math.PI / 4;
      arm.add(weaponModel);
    }
    
    return arm;
  }

  buildLeg(palette) {
    const leg = new THREE.Group();
    
    // Cuisse (1x3x1)
    for (let y = 0; y <= 2; y++) {
      const voxel = createVoxel(palette.armor, 1);
      voxel.position.set(0, -y, 0);
      leg.add(voxel);
    }
    
    // Mollet (1x2x1)
    for (let y = 3; y <= 4; y++) {
      const voxel = createVoxel(palette.skin, 0.8);
      voxel.position.set(0, -y, 0);
      leg.add(voxel);
    }
    
    // Pied (1x0.5x1.5)
    const foot = createVoxel(palette.armor, 1);
    foot.position.set(0, -5, 0.5);
    foot.scale.set(1, 0.5, 1.5);
    leg.add(foot);
    
    return leg;
  }

  buildWeapon(type, palette) {
    const weapon = new THREE.Group();
    
    switch (type) {
      case 'bolter':
        // Crosse
        for (let z = 0; z <= 2; z++) {
          const voxel = createVoxel(palette.trim, 0.8);
          voxel.position.set(0, 0, z * 0.8);
          weapon.add(voxel);
        }
        // Canon
        const barrel = createVoxel(PALETTES.metal[1], 1.5);
        barrel.scale.set(0.6, 0.6, 2);
        barrel.position.set(0, 0, -1.5);
        weapon.add(barrel);
        // Chargeur
        const mag = createVoxel(PALETTES.metal[2], 1);
        mag.scale.set(0.5, 1.2, 0.8);
        mag.position.set(0, -0.8, 0.5);
        weapon.add(mag);
        break;
        
      case 'chainsword':
        // Poignée
        for (let i = 0; i < 3; i++) {
          const voxel = createVoxel(PALETTES.metal[3], 0.6);
          voxel.position.set(0, i * 0.6, 0);
          weapon.add(voxel);
        }
        // Lame
        for (let i = 0; i < 5; i++) {
          const blade = createVoxel(PALETTES.metal[0], 1);
          blade.scale.set(0.3, 0.4, 1.2);
          blade.position.set(0, 2 + i * 0.4, -0.6);
          weapon.add(blade);
          // Dents
          const tooth = createVoxel(0xffffff, 0.2);
          tooth.position.set(0.2, 2 + i * 0.4, -0.9);
          weapon.add(tooth);
        }
        break;
        
      case 'lasgun':
        // Similaire au bolter mais plus fin
        for (let z = 0; z <= 2; z++) {
          const voxel = createVoxel(PALETTES.metal[2], 0.6);
          voxel.position.set(0, 0, z * 0.6);
          weapon.add(voxel);
        }
        const laserBarrel = createVoxel(PALETTES.energy[1], 1.2);
        laserBarrel.scale.set(0.4, 0.4, 1.8);
        laserBarrel.position.set(0, 0, -1.2);
        weapon.add(laserBarrel);
        break;
    }
    
    return weapon;
  }
}

/**
 * Générateur de monstres aliens (Tyranides, etc.)
 */
export class MonsterVoxelBuilder {
  build({
    type = 'tyranid_warrior',
    variant = 0,
    scale = 1.5
  } = {}) {
    if (type.startsWith('tyranid')) {
      return this.buildTyranid(variant, scale);
    } else if (type.startsWith('ork')) {
      return this.buildOrk(variant, scale);
    }
    
    return this.buildGenericMonster(scale);
  }

  buildTyranid(variant, scale) {
    const group = new THREE.Group();
    const palette = PALETTES.tyranid;
    
    // Corps alien (forme bestiale)
    const body = new THREE.Group();
    
    // Torse élargi
    for (let x = -2; x <= 2; x++) {
      for (let y = 0; y <= 4; y++) {
        for (let z = -1; z <= 1; z++) {
          if (Math.abs(x) + Math.abs(z) <= 2.5) {
            const voxel = createVoxel(palette[0], 1);
            voxel.position.set(x, y, z);
            body.add(voxel);
          }
        }
      }
    }
    
    // Tête monstrueuse
    const head = new THREE.Group();
    for (let x = -1; x <= 1; x++) {
      for (let y = 0; y <= 2; y++) {
        for (let z = -2; z <= 0; z++) {
          const voxel = createVoxel(palette[1], 1);
          voxel.position.set(x, y, z);
          head.add(voxel);
        }
      }
    }
    
    // Mâchoires/mandibules
    const leftMandible = createVoxel(palette[2], 1.5);
    leftMandible.scale.set(0.4, 0.4, 1.2);
    leftMandible.position.set(-1.2, 0.5, -2.5);
    head.add(leftMandible);
    
    const rightMandible = createVoxel(palette[2], 1.5);
    rightMandible.scale.set(0.4, 0.4, 1.2);
    rightMandible.position.set(1.2, 0.5, -2.5);
    head.add(rightMandible);
    
    // Yeux multiples
    for (let i = 0; i < 4; i++) {
      const eye = createVoxel(0xff00ff, 0.3);
      eye.position.set(
        -0.8 + (i % 2) * 1.6,
        1 + Math.floor(i / 2) * 0.6,
        -2.1
      );
      head.add(eye);
    }
    
    head.position.set(0, 5, 0);
    
    // Griffes/armes bio
    const leftClaw = this.buildClaw(palette);
    leftClaw.position.set(-3, 3, -1);
    leftClaw.rotation.z = Math.PI / 6;
    
    const rightClaw = this.buildClaw(palette);
    rightClaw.position.set(3, 3, -1);
    rightClaw.rotation.z = -Math.PI / 6;
    
    // Pattes arrière
    const leftLeg = this.buildMonsterLeg(palette);
    leftLeg.position.set(-1.5, -2, 0);
    
    const rightLeg = this.buildMonsterLeg(palette);
    rightLeg.position.set(1.5, -2, 0);
    
    group.add(body, head, leftClaw, rightClaw, leftLeg, rightLeg);
    group.scale.multiplyScalar(scale);
    
    return { 
      model: group, 
      parts: { body, head, leftClaw, rightClaw, leftLeg, rightLeg },
      skeleton: {
        head: { joint: new THREE.Vector3(0, 4.5, 0) },
        leftShoulder: { joint: new THREE.Vector3(-2.5, 3.5, 0) },
        rightShoulder: { joint: new THREE.Vector3(2.5, 3.5, 0) },
      }
    };
  }

  buildClaw(palette) {
    const claw = new THREE.Group();
    
    // Bras
    for (let y = 0; y <= 2; y++) {
      const segment = createVoxel(palette[0], 1);
      segment.position.set(0, -y, 0);
      claw.add(segment);
    }
    
    // Pinces
    for (let i = 0; i < 3; i++) {
      const talon = createVoxel(palette[2], 1.2);
      talon.scale.set(0.3, 0.3, 1.5);
      talon.rotation.y = (i - 1) * Math.PI / 6;
      talon.position.set(
        (i - 1) * 0.4,
        -3,
        -1
      );
      claw.add(talon);
    }
    
    return claw;
  }

  buildMonsterLeg(palette) {
    const leg = new THREE.Group();
    
    // Cuisse épaisse
    for (let y = 0; y <= 2; y++) {
      const voxel = createVoxel(palette[1], 1.2);
      voxel.position.set(0, -y, 0);
      leg.add(voxel);
    }
    
    // Articulation
    const joint = createVoxel(palette[2], 1);
    joint.position.set(0, -3, 0.5);
    leg.add(joint);
    
    // Patte griffue
    for (let y = 4; y <= 5; y++) {
      const voxel = createVoxel(palette[2], 1);
      voxel.position.set(0, -y, 0);
      leg.add(voxel);
    }
    
    // Griffes
    const claw1 = createVoxel(0xffffff, 0.8);
    claw1.scale.set(0.3, 0.3, 1.2);
    claw1.position.set(0, -6, 0.8);
    leg.add(claw1);
    
    return leg;
  }

  buildOrk(variant, scale) {
    const builder = new HumanoidVoxelBuilder();
    return builder.build({
      faction: 'ork',
      bodyType: variant % 2 === 0 ? 'brute' : 'human',
      armorLevel: 'heavy',
      weapon: 'chainsword',
      scale,
    });
  }

  buildGenericMonster(scale) {
    const builder = new HumanoidVoxelBuilder();
    return builder.build({ faction: 'chaos', armorLevel: 'heavy', scale });
  }
}

/**
 * Générateur d'environnement (sol, obstacles, décors)
 */
export class EnvironmentBuilder {
  buildArena({
    width = 30,
    depth = 20,
    theme = 'industrial'
  } = {}) {
    const environment = new THREE.Group();
    
    // Sol (grille de voxels)
    const floor = this.buildFloor(width, depth, theme);
    environment.add(floor);
    
    // Murs/limites
    const walls = this.buildWalls(width, depth, theme);
    environment.add(walls);
    
    // Obstacles/couvertures
    const obstacles = this.buildObstacles(width, depth, theme);
    environment.add(obstacles);
    
    return environment;
  }

  buildFloor(width, depth, theme) {
    const floor = new THREE.Group();
    const colors = this.getThemeColors(theme);
    const evenTiles = [];
    const oddTiles = [];

    for (let x = -width/2; x < width/2; x++) {
      for (let z = -depth/2; z < depth/2; z++) {
        ((x + z) % 2 === 0 ? evenTiles : oddTiles).push([x, -0.5, z]);
      }
    }

    floor.add(
      this.createInstancedBlocks(evenTiles, 1, colors.floor[0]),
      this.createInstancedBlocks(oddTiles, 1, colors.floor[1]),
    );

    const details = [];
    for (let i = 0; i < Math.floor(width * depth * 0.045); i++) {
      details.push([
        Math.random() * width - width / 2,
        0,
        Math.random() * depth - depth / 2,
      ]);
    }
    floor.add(this.createInstancedBlocks(details, 0.25, colors.detail, { emissive: colors.detail, emissiveIntensity: 0.2 }));
    
    return floor;
  }

  buildWalls(width, depth, theme) {
    const walls = new THREE.Group();
    const colors = this.getThemeColors(theme);
    const wallHeight = 8;
    const blocks = [];

    for (let x = -width/2; x < width/2; x += 2) {
      for (let y = 0; y < wallHeight; y++) {
        blocks.push([x, y * 2, -depth / 2 - 1], [x, y * 2, depth / 2 + 1]);
      }
    }
    for (let z = -depth/2; z < depth/2; z += 2) {
      for (let y = 0; y < wallHeight; y++) {
        blocks.push([width / 2 + 1, y * 2, z], [-width / 2 - 1, y * 2, z]);
      }
    }
    walls.add(this.createInstancedBlocks(blocks, 2, colors.wall));
    
    return walls;
  }

  buildObstacles(width, depth, theme) {
    const obstacles = new THREE.Group();
    const colors = this.getThemeColors(theme);
    const obstacleCount = Math.floor((width * depth) / 50);
    const crates = [];
    const columns = [];
    const debris = [];

    for (let i = 0; i < obstacleCount; i++) {
      const x = Math.random() * width - width/2;
      const z = Math.random() * depth - depth/2;
      if (Math.abs(x) < 5 && Math.abs(z) < 5) continue;
      const type = Math.random();
      if (type < 0.5) {
        crates.push([x, 1, z]);
      } else if (type < 0.8) {
        for (let y = 0; y < 4; y++) {
          columns.push([x, y * 1.5, z]);
        }
      } else {
        debris.push([x, 0.5, z]);
      }
    }
    obstacles.add(
      this.createInstancedBlocks(crates, 2, colors.obstacle),
      this.createInstancedBlocks(columns, 1.5, colors.wall),
      this.createInstancedBlocks(debris, 1, colors.detail, { emissive: colors.detail, emissiveIntensity: 0.15 }),
    );
    return obstacles;
  }

  createInstancedBlocks(positions, size, color, options = {}) {
    const mesh = new THREE.InstancedMesh(
      getVoxelGeometry(size),
      getVoxelMaterial(color, options),
      Math.max(positions.length, 1),
    );
    const matrix = new THREE.Matrix4();
    positions.forEach(([x, y, z], index) => {
      matrix.makeTranslation(x, y, z);
      mesh.setMatrixAt(index, matrix);
    });
    mesh.count = positions.length;
    mesh.instanceMatrix.needsUpdate = true;
    mesh.castShadow = false;
    mesh.receiveShadow = true;
    return mesh;
  }

  getThemeColors(theme) {
    const themes = {
      industrial: {
        floor: [0x4a4a4a, 0x3a3a3a],
        wall: 0x2a2a2a,
        obstacle: 0x6a4f2c,
        detail: 0x8b0000
      },
      temple: {
        floor: [0x8b7355, 0x7a6347],
        wall: 0xa0826d,
        obstacle: 0xdaa520,
        detail: 0xffd700
      },
      wasteland: {
        floor: [0x8b7355, 0x6b5345],
        wall: 0x5a4535,
        obstacle: 0x4a4a4a,
        detail: 0x228b22
      }
    };
    
    return themes[theme] || themes.industrial;
  }
}
