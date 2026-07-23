/**
 * Scène de combat 3D complète avec personnages voxel
 * 
 * Gère le rendu, les animations, la caméra et les effets
 */

import * as THREE from 'three';
import { HumanoidVoxelBuilder, MonsterVoxelBuilder, EnvironmentBuilder } from './VoxelEngine';
import { SkeletalAnimator, VOXEL_ANIMATIONS } from './AnimationSystem';

/**
 * Gestionnaire principal de la scène de combat 3D
 */
export class CombatScene3D {
  constructor(canvasElement) {
    this.canvas = canvasElement;
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.entities = new Map(); // ID -> { model, animator, data }
    this.environment = null;
    this.lights = [];
    this.particles = [];
    this.particleResources = new Map();
    this.lastTime = 0;
    this.frameId = null;
    this.running = false;
    this.cameraShake = { intensity: 0, duration: 0, elapsed: 0 };
    this.flash = null;
    this.onResize = this.onResize.bind(this);
    
    this.init();
  }

  /**
   * Initialise la scène 3D
   */
  init() {
    // Scène
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x080b14);
    this.scene.fog = new THREE.FogExp2(0x080b14, 0.028);

    // Caméra orthographique (style pixel art) - plus proche pour mieux voir
    const { width, height } = this.getViewportSize();
    const aspect = width / height;
    const viewSize = 13;
    this.camera = new THREE.OrthographicCamera(
      -viewSize * aspect, viewSize * aspect,
      viewSize, -viewSize,
      0.1, 1000
    );
    this.camera.position.set(15, 17, 18);
    this.camera.lookAt(0, 3.5, 0);

    // Renderer
    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: true,
      powerPreference: 'high-performance',
      alpha: false,
    });
    this.renderer.setSize(width, height, false);
    this.renderer.setPixelRatio(Math.min(globalThis.devicePixelRatio || 1, 1.5));
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.15;
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFShadowMap;

    // Lumières
    this.setupLights();

    // Environnement
    this.createEnvironment();

    // Redimensionnement
    window.addEventListener('resize', this.onResize);

    // Démarrer la boucle de rendu
    this.running = true;
    this.animate();
  }

  getViewportSize() {
    const rect = this.canvas.getBoundingClientRect();
    return {
      width: Math.max(1, Math.floor(rect.width || window.innerWidth)),
      height: Math.max(1, Math.floor(rect.height || window.innerHeight)),
    };
  }

  /**
   * Configure l'éclairage
   */
  setupLights() {
    const hemisphere = new THREE.HemisphereLight(0x9bbcff, 0x130c10, 1.6);
    this.scene.add(hemisphere);
    this.lights.push(hemisphere);

    // Lumière directionnelle principale (soleil) TRÈS FORTE
    const directional = new THREE.DirectionalLight(0xffe4c2, 2.7);
    directional.position.set(15, 25, 15);
    directional.castShadow = true;
    directional.shadow.camera.left = -40;
    directional.shadow.camera.right = 40;
    directional.shadow.camera.top = 40;
    directional.shadow.camera.bottom = -40;
    directional.shadow.mapSize.width = 1024;
    directional.shadow.mapSize.height = 1024;
    directional.shadow.bias = -0.001;
    this.scene.add(directional);
    this.lights.push(directional);

    // Lumière d'accentuation avant (éclaire les personnages)
    const frontLight = new THREE.DirectionalLight(0xa8c5ff, 1.1);
    frontLight.position.set(0, 15, 20);
    this.scene.add(frontLight);
    this.lights.push(frontLight);

    // Lumière d'accentuation rouge (dramati)
    const accent = new THREE.PointLight(0xff3d55, 22, 26, 2);
    accent.position.set(-12, 8, -8);
    this.scene.add(accent);
    this.lights.push(accent);

    // Lumière de remplissage bleue
    const fill = new THREE.PointLight(0x4a88ff, 16, 24, 2);
    fill.position.set(12, 8, -8);
    this.scene.add(fill);
    this.lights.push(fill);
    
    // Lumière arrière (rim light)
    const rim = new THREE.DirectionalLight(0x63e6ff, 1.4);
    rim.position.set(-10, 10, -15);
    this.scene.add(rim);
    this.lights.push(rim);
  }

  /**
   * Crée l'environnement (sol, murs, obstacles)
   */
  createEnvironment(theme = 'industrial') {
    if (this.environment) {
      this.scene.remove(this.environment);
    }

    const envBuilder = new EnvironmentBuilder();
    this.environment = envBuilder.buildArena({ width: 30, depth: 20, theme });
    this.scene.add(this.environment);
  }

  /**
   * Ajoute un personnage joueur
   */
  addPlayer(playerId, data = {}) {
    const builder = new HumanoidVoxelBuilder();
    const { model, parts, skeleton } = builder.build({
      faction: data.faction || 'imperial',
      bodyType: 'human',
      armorLevel: data.armorLevel || 'medium',
      weapon: data.weapon || 'bolter',
      scale: 1.0
    });

    // Position sur le côté gauche
    model.position.set(-8, 0, 0);
    model.rotation.y = Math.PI / 6; // Légèrement tourné vers l'ennemi

    // Ombre
    model.traverse(child => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
      }
    });

    this.scene.add(model);

    // Animator
    const animator = new SkeletalAnimator(model, parts, skeleton);
    
    // Enregistrer les animations
    Object.entries(VOXEL_ANIMATIONS).forEach(([name, anim]) => {
      animator.registerAnimation(name, anim);
    });

    // Jouer idle par défaut
    animator.play('idle', true);

    this.entities.set(playerId, {
      model,
      parts,
      skeleton,
      animator,
      data,
      type: 'player'
    });

    return animator;
  }

  /**
   * Ajoute un ennemi
   */
  addEnemy(enemyId, data = {}) {
    let builder, buildResult;
    
    if (data.type && (data.type.includes('tyranid') || data.type.includes('alien'))) {
      builder = new MonsterVoxelBuilder();
      buildResult = builder.build({
        type: data.type || 'tyranid_warrior',
        variant: data.variant || 0,
        scale: data.scale || 1.5
      });
    } else {
      builder = new HumanoidVoxelBuilder();
      buildResult = builder.build({
        faction: data.faction || 'chaos',
        bodyType: data.bodyType || 'human',
        armorLevel: data.armorLevel || 'medium',
        weapon: data.weapon || 'chainsword',
        scale: data.scale || 1.2
      });
    }

    const { model, parts, skeleton } = buildResult;

    // Position sur le côté droit
    model.position.set(8, 0, 0);
    model.rotation.y = -Math.PI / 6; // Tourné vers le joueur

    // Ombre
    model.traverse(child => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
      }
    });

    this.scene.add(model);

    // Animator
    const animator = new SkeletalAnimator(model, parts, skeleton);
    
    // Enregistrer les animations
    Object.entries(VOXEL_ANIMATIONS).forEach(([name, anim]) => {
      animator.registerAnimation(name, anim);
    });

    // Jouer idle par défaut
    animator.play('idle', true);

    this.entities.set(enemyId, {
      model,
      parts,
      skeleton,
      animator,
      data,
      type: 'enemy'
    });

    return animator;
  }

  /**
   * Supprime une entité
   */
  removeEntity(entityId) {
    const entity = this.entities.get(entityId);
    if (entity) {
      this.scene.remove(entity.model);
      entity.animator.stop();
      this.entities.delete(entityId);
    }
  }

  /**
   * Joue une animation sur une entité
   */
  playAnimation(entityId, animationName, loop = false) {
    const entity = this.entities.get(entityId);
    if (entity && entity.animator) {
      entity.animator.play(animationName, loop);
      return true;
    }
    return false;
  }

  /**
   * Crée un effet de particules (sang, étincelles, etc.)
   */
  createParticleEffect(position, type = 'spark', count = 20) {
    const colors = {
      spark: 0xffaa33,
      blood: 0xcc0000,
      energy: 0x00ffff,
      explosion: 0xff6600
    };

    const color = colors[type] || colors.spark;
    if (!this.particleResources.has(type)) {
      this.particleResources.set(type, {
        geometry: new THREE.BoxGeometry(0.18, 0.18, 0.18),
        material: new THREE.MeshBasicMaterial({ color, transparent: true, depthWrite: false }),
      });
    }
    const { geometry, material } = this.particleResources.get(type);

    for (let i = 0; i < count; i++) {
      const particle = new THREE.Mesh(geometry, material);

      particle.position.copy(position);
      
      // Vélocité aléatoire
      particle.velocity = new THREE.Vector3(
        (Math.random() - 0.5) * 10,
        Math.random() * 8 + 2,
        (Math.random() - 0.5) * 10
      );
      
      particle.life = 0.7 + Math.random() * 0.35;
      particle.gravity = type === 'energy' ? -2 : -15;

      this.scene.add(particle);
      this.particles.push(particle);
    }
  }

  /**
   * Update des particules
   */
  updateParticles(deltaTime) {
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const particle = this.particles[i];
      
      // Physique
      particle.velocity.y += particle.gravity * deltaTime;
      particle.position.addScaledVector(particle.velocity, deltaTime);
      
      // Vie
      particle.life -= deltaTime;
      particle.material.opacity = Math.max(0, particle.life);
      particle.material.transparent = true;
      
      // Supprimer si mort
      if (particle.life <= 0) {
        this.scene.remove(particle);
        this.particles.splice(i, 1);
      }
    }
  }

  /**
   * Secoue la caméra
   */
  shakeCamera(intensity = 1.0, duration = 0.3) {
    this.cameraShake = { intensity, duration, elapsed: 0 };
  }

  /**
   * Flash d'écran
   */
  flashScreen(color = 0xffffff, intensity = 0.5, duration = 0.1) {
    if (!this.flash) {
      this.flash = new THREE.Mesh(
        new THREE.PlaneGeometry(2, 2),
        new THREE.MeshBasicMaterial({ transparent: true, opacity: 0, depthTest: false, depthWrite: false }),
      );
      this.flash.position.set(0, 0, -1);
      this.camera.add(this.flash);
    }
    this.flash.material.color.setHex(color);
    this.flash.material.opacity = intensity;
    this.flash.userData.remaining = duration;
    this.flash.scale.set(this.camera.right - this.camera.left, this.camera.top - this.camera.bottom, 1);
  }

  /**
   * Gestion du redimensionnement
   */
  onResize() {
    const { width, height } = this.getViewportSize();
    const aspect = width / height;
    const viewSize = 13;
    
    this.camera.left = -viewSize * aspect;
    this.camera.right = viewSize * aspect;
    this.camera.top = viewSize;
    this.camera.bottom = -viewSize;
    this.camera.updateProjectionMatrix();

    this.renderer.setSize(width, height, false);
  }

  /**
   * Boucle d'animation principale
   */
  animate(currentTime = 0) {
    if (!this.running) return;
    this.frameId = requestAnimationFrame((time) => this.animate(time));

    const deltaTime = this.lastTime ? (currentTime - this.lastTime) / 1000 : 0;
    this.lastTime = currentTime;

    // Update les animateurs
    this.entities.forEach(entity => {
      if (entity.animator) {
        entity.animator.update(deltaTime);
      }
    });

    // Update les particules
    this.updateParticles(deltaTime);

    if (this.cameraShake.elapsed < this.cameraShake.duration) {
      this.cameraShake.elapsed += deltaTime;
      const strength = this.cameraShake.intensity * Math.max(0, 1 - this.cameraShake.elapsed / this.cameraShake.duration);
      this.camera.position.set(15, 17, 18).add(new THREE.Vector3(
        (Math.random() - 0.5) * strength,
        (Math.random() - 0.5) * strength,
        (Math.random() - 0.5) * strength,
      ));
      this.camera.lookAt(0, 3.5, 0);
    } else if (this.cameraShake.duration > 0) {
      this.camera.position.set(15, 17, 18);
      this.camera.lookAt(0, 3.5, 0);
      this.cameraShake.duration = 0;
    }

    if (this.flash?.userData.remaining > 0) {
      this.flash.userData.remaining -= deltaTime;
      this.flash.material.opacity = Math.max(0, this.flash.material.opacity - deltaTime * 5);
    }

    // Rendu
    this.renderer.render(this.scene, this.camera);
  }

  /**
   * Nettoie la scène
   */
  dispose() {
    this.running = false;
    if (this.frameId) cancelAnimationFrame(this.frameId);
    window.removeEventListener('resize', this.onResize);
    this.entities.forEach(entity => {
      this.scene.remove(entity.model);
    });
    this.entities.clear();
    
    this.particles.forEach(particle => {
      this.scene.remove(particle);
    });
    this.particles = [];
    this.particleResources.forEach(({ geometry, material }) => {
      geometry.dispose();
      material.dispose();
    });
    this.particleResources.clear();
    
    if (this.environment) {
      this.scene.remove(this.environment);
    }
    this.flash?.geometry.dispose();
    this.flash?.material.dispose();
    this.renderer.dispose();
  }
}
