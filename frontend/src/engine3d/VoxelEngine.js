/**
 * Moteur 3D de rendu voxel pour animations pixel art
 * 
 * Génère des personnages, monstres, armes et environnements en voxels
 * avec animations skeletal et rendu pixel art stylisé.
 */

import * as THREE from 'three';

/**
 * Crée un voxel (cube) avec couleur
 */
export function createVoxel(color = 0xffffff, size = 1) {
  const geometry = new THREE.BoxGeometry(size, size, size);
  const material = new THREE.MeshLambertMaterial({ 
    color,
    flatShading: true // Style pixel art
  });
  return new THREE.Mesh(geometry, material);
}

/**
 * Palette de couleurs pixel art
 */
export const PALETTES = {
  skin: [0xffdbac, 0xf1c27d, 0xe0ac69, 0xc68642],
  metal: [0xcccccc, 0x999999, 0x666666, 0x333333],
  gold: [0xffeb3b, 0xffc107, 0xff9800, 0xf57c00],
  blood: [0xff0000, 0xcc0000, 0x990000, 0x660000],
  armor: [0x1565c0, 0x0d47a1, 0x01579b, 0x004d40],
  tyranid: [0x4a148c, 0x311b92, 0x1a237e, 0x000051],
  ork: [0x2e7d32, 0x1b5e20, 0x004d40, 0x00251a],
  chaos: [0xb71c1c, 0x880e4f, 0x4a148c, 0x000000],
  energy: [0x00ffff, 0x00e5ff, 0x00b8ff, 0x0091ff],
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
    
    // Crâne principal (2x2x2)
    for (let x = -1; x <= 0; x++) {
      for (let y = 0; y <= 1; y++) {
        for (let z = -1; z <= 0; z++) {
          const voxel = createVoxel(palette.skin, 1);
          voxel.position.set(x, y, z);
          head.add(voxel);
        }
      }
    }
    
    // Casque/heaume (style 40K)
    const helmetVoxels = [
      [0, 2, 0], [-1, 2, 0], [0, 2, -1], [-1, 2, -1], // Top
      [1, 1, 0], [-2, 1, 0], // Côtés
    ];
    
    helmetVoxels.forEach(([x, y, z]) => {
      const voxel = createVoxel(palette.armor, 1);
      voxel.position.set(x, y, z);
      head.add(voxel);
    });
    
    // Yeux (lumière)
    const leftEye = createVoxel(0xff0000, 0.3);
    leftEye.position.set(-0.3, 0.5, -1.1);
    const rightEye = createVoxel(0xff0000, 0.3);
    rightEye.position.set(-0.7, 0.5, -1.1);
    head.add(leftEye, rightEye);
    
    return head;
  }

  buildTorso(palette, armorLevel) {
    const torso = new THREE.Group();
    
    // Corps principal (3x4x2)
    for (let x = -1; x <= 1; x++) {
      for (let y = 0; y <= 3; y++) {
        for (let z = -1; z <= 0; z++) {
          const voxel = createVoxel(palette.armor, 1);
          voxel.position.set(x, y, z);
          torso.add(voxel);
        }
      }
    }
    
    // Détails armure (épaulières, abdomen)
    if (armorLevel === 'heavy') {
      // Épaulières massives (style Space Marine)
      const shoulderPads = [
        [-2, 3, 0], [-2, 3, -1], [-2, 2, 0],
        [2, 3, 0], [2, 3, -1], [2, 2, 0],
      ];
      shoulderPads.forEach(([x, y, z]) => {
        const voxel = createVoxel(palette.trim, 1);
        voxel.position.set(x, y, z);
        torso.add(voxel);
      });
    }
    
    // Badge/symbole (centre poitrine)
    const badge = createVoxel(palette.trim, 0.6);
    badge.position.set(0, 2.5, -1.1);
    torso.add(badge);
    
    return torso;
  }

  buildArm(palette, side, weapon = null) {
    const arm = new THREE.Group();
    const sign = side === 'left' ? -1 : 1;
    
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
    const group = new THREE.Group();
    
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
    // TODO: Orques musclés et brutaux
    return this.buildGenericMonster(scale);
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
    
    for (let x = -width/2; x < width/2; x++) {
      for (let z = -depth/2; z < depth/2; z++) {
        // Variation de couleur (damier)
        const colorIndex = (x + z) % 2 === 0 ? 0 : 1;
        const voxel = createVoxel(colors.floor[colorIndex], 1);
        voxel.position.set(x, -0.5, z);
        floor.add(voxel);
        
        // Ajouter quelques détails aléatoires
        if (Math.random() < 0.05) {
          const detail = createVoxel(colors.detail, 0.3);
          detail.position.set(
            x + Math.random() * 0.6 - 0.3,
            0,
            z + Math.random() * 0.6 - 0.3
          );
          floor.add(detail);
        }
      }
    }
    
    return floor;
  }

  buildWalls(width, depth, theme) {
    const walls = new THREE.Group();
    const colors = this.getThemeColors(theme);
    
    const wallHeight = 8;
    
    // Murs nord/sud
    for (let x = -width/2; x < width/2; x += 2) {
      for (let y = 0; y < wallHeight; y++) {
        // Mur nord
        const northWall = createVoxel(colors.wall, 2);
        northWall.position.set(x, y * 2, -depth/2 - 1);
        walls.add(northWall);
        
        // Mur sud
        const southWall = createVoxel(colors.wall, 2);
        southWall.position.set(x, y * 2, depth/2 + 1);
        walls.add(southWall);
      }
    }
    
    // Murs est/ouest
    for (let z = -depth/2; z < depth/2; z += 2) {
      for (let y = 0; y < wallHeight; y++) {
        // Mur est
        const eastWall = createVoxel(colors.wall, 2);
        eastWall.position.set(width/2 + 1, y * 2, z);
        walls.add(eastWall);
        
        // Mur ouest
        const westWall = createVoxel(colors.wall, 2);
        westWall.position.set(-width/2 - 1, y * 2, z);
        walls.add(westWall);
      }
    }
    
    return walls;
  }

  buildObstacles(width, depth, theme) {
    const obstacles = new THREE.Group();
    const colors = this.getThemeColors(theme);
    
    // Caisses, barils, couvertures
    const obstacleCount = Math.floor((width * depth) / 50);
    
    for (let i = 0; i < obstacleCount; i++) {
      const x = Math.random() * width - width/2;
      const z = Math.random() * depth - depth/2;
      
      // Ne pas placer trop près du centre
      if (Math.abs(x) < 5 && Math.abs(z) < 5) continue;
      
      const type = Math.random();
      
      if (type < 0.5) {
        // Caisse
        const box = createVoxel(colors.obstacle, 2);
        box.position.set(x, 1, z);
        obstacles.add(box);
      } else if (type < 0.8) {
        // Colonne
        for (let y = 0; y < 4; y++) {
          const segment = createVoxel(colors.wall, 1.5);
          segment.position.set(x, y * 1.5, z);
          obstacles.add(segment);
        }
      } else {
        // Débris
        const debris = createVoxel(colors.detail, 1);
        debris.rotation.set(
          Math.random() * Math.PI,
          Math.random() * Math.PI,
          Math.random() * Math.PI
        );
        debris.position.set(x, 0.5, z);
        obstacles.add(debris);
      }
    }
    
    return obstacles;
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
