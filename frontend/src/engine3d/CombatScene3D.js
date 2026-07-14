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
    this.lastTime = 0;
    this.pixelationEnabled = true;
    
    this.init();
  }

  /**
   * Initialise la scène 3D
   */
  init() {
    // Scène
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x2a2a3e);
    this.scene.fog = new THREE.Fog(0x2a2a3e, 40, 80);

    // Caméra orthographique (style pixel art) - plus proche pour mieux voir
    const aspect = window.innerWidth / window.innerHeight;
    const viewSize = 15;
    this.camera = new THREE.OrthographicCamera(
      -viewSize * aspect, viewSize * aspect,
      viewSize, -viewSize,
      0.1, 1000
    );
    this.camera.position.set(12, 18, 12);
    this.camera.lookAt(0, 3, 0);

    // Renderer
    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: false, // Pixel art
      powerPreference: 'high-performance'
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(1); // Pas de HD pour style pixel
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    // Lumières
    this.setupLights();

    // Environnement
    this.createEnvironment();

    // Redimensionnement
    window.addEventListener('resize', () => this.onResize());

    // Démarrer la boucle de rendu
    this.animate();
  }

  /**
   * Configure l'éclairage
   */
  setupLights() {
    // Lumière ambiante FORTE pour bien voir
    const ambient = new THREE.AmbientLight(0xa0a0c0, 0.8);
    this.scene.add(ambient);
    this.lights.push(ambient);

    // Lumière directionnelle principale (soleil) TRÈS FORTE
    const directional = new THREE.DirectionalLight(0xffffff, 1.5);
    directional.position.set(15, 25, 15);
    directional.castShadow = true;
    directional.shadow.camera.left = -40;
    directional.shadow.camera.right = 40;
    directional.shadow.camera.top = 40;
    directional.shadow.camera.bottom = -40;
    directional.shadow.mapSize.width = 2048;
    directional.shadow.mapSize.height = 2048;
    directional.shadow.bias = -0.001;
    this.scene.add(directional);
    this.lights.push(directional);

    // Lumière d'accentuation avant (éclaire les personnages)
    const frontLight = new THREE.DirectionalLight(0xffffee, 0.8);
    frontLight.position.set(0, 15, 20);
    this.scene.add(frontLight);
    this.lights.push(frontLight);

    // Lumière d'accentuation rouge (dramati)
    const accent = new THREE.PointLight(0xff6644, 1.2, 40);
    accent.position.set(-12, 8, -8);
    this.scene.add(accent);
    this.lights.push(accent);

    // Lumière de remplissage bleue
    const fill = new THREE.PointLight(0x6688ff, 0.8, 40);
    fill.position.set(12, 8, -8);
    this.scene.add(fill);
    this.lights.push(fill);
    
    // Lumière arrière (rim light)
    const rim = new THREE.DirectionalLight(0xaaccff, 0.6);
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

    for (let i = 0; i < count; i++) {
      const geometry = new THREE.BoxGeometry(0.2, 0.2, 0.2);
      const material = new THREE.MeshBasicMaterial({ color });
      const particle = new THREE.Mesh(geometry, material);

      particle.position.copy(position);
      
      // Vélocité aléatoire
      particle.velocity = new THREE.Vector3(
        (Math.random() - 0.5) * 10,
        Math.random() * 8 + 2,
        (Math.random() - 0.5) * 10
      );
      
      particle.life = 1.0;
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
      particle.position.add(particle.velocity.clone().multiplyScalar(deltaTime));
      
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
    const originalPos = this.camera.position.clone();
    const startTime = Date.now();

    const shake = () => {
      const elapsed = (Date.now() - startTime) / 1000;
      if (elapsed < duration) {
        const progress = 1 - elapsed / duration;
        const shakeAmount = intensity * progress;
        
        this.camera.position.x = originalPos.x + (Math.random() - 0.5) * shakeAmount;
        this.camera.position.y = originalPos.y + (Math.random() - 0.5) * shakeAmount;
        this.camera.position.z = originalPos.z + (Math.random() - 0.5) * shakeAmount;
        
        requestAnimationFrame(shake);
      } else {
        this.camera.position.copy(originalPos);
      }
    };

    shake();
  }

  /**
   * Flash d'écran
   */
  flashScreen(color = 0xffffff, intensity = 0.5, duration = 0.1) {
    const flash = new THREE.Mesh(
      new THREE.PlaneGeometry(1000, 1000),
      new THREE.MeshBasicMaterial({
        color,
        transparent: true,
        opacity: intensity,
        depthTest: false
      })
    );
    flash.position.copy(this.camera.position);
    flash.position.z -= 5;
    flash.lookAt(this.camera.position);
    this.scene.add(flash);

    setTimeout(() => {
      this.scene.remove(flash);
    }, duration * 1000);
  }

  /**
   * Gestion du redimensionnement
   */
  onResize() {
    const aspect = window.innerWidth / window.innerHeight;
    const viewSize = 20;
    
    this.camera.left = -viewSize * aspect;
    this.camera.right = viewSize * aspect;
    this.camera.top = viewSize;
    this.camera.bottom = -viewSize;
    this.camera.updateProjectionMatrix();

    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  /**
   * Boucle d'animation principale
   */
  animate(currentTime = 0) {
    requestAnimationFrame((time) => this.animate(time));

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

    // Rendu
    this.renderer.render(this.scene, this.camera);
  }

  /**
   * Nettoie la scène
   */
  dispose() {
    this.entities.forEach(entity => {
      this.scene.remove(entity.model);
    });
    this.entities.clear();
    
    this.particles.forEach(particle => {
      this.scene.remove(particle);
    });
    this.particles = [];
    
    if (this.environment) {
      this.scene.remove(this.environment);
    }
    
    this.renderer.dispose();
  }
}
