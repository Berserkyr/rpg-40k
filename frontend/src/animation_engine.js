/**
 * Moteur d'animation procedurale
 * Interprete les descripteurs JSON d'animations et applique les transformations.
 */

// =====================================================================
// Easing functions
// =====================================================================

const EASINGS = {
  linear: (t) => t,
  easeIn: (t) => t * t,
  easeOut: (t) => 1 - (1 - t) * (1 - t),
  easeInOut: (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2),
  easeInCubic: (t) => t * t * t,
  easeOutCubic: (t) => 1 - Math.pow(1 - t, 3),
  easeInQuart: (t) => t * t * t * t,
  easeOutQuart: (t) => 1 - Math.pow(1 - t, 4),
};

/**
 * Interpole entre deux valeurs avec easing.
 */
function lerp(start, end, t, easingName = 'linear') {
  const easing = EASINGS[easingName] || EASINGS.linear;
  const factor = easing(t);
  return start + (end - start) * factor;
}

// =====================================================================
// Calcul des transforms a un instant donne
// =====================================================================

/**
 * Calcule les transforms d'une phase a un instant specifique.
 * @param {Object} phase - Phase d'animation
 * @param {number} globalProgress - Progression globale (0-1 dans l'animation)
 * @returns {Object|null} - Transforms {translateX, translateY, rotation, scale, opacity} ou null si hors phase
 */
function computePhaseTransforms(phase, globalProgress) {
  if (globalProgress < phase.start || globalProgress > phase.end) {
    return null;
  }

  // Progression locale dans la phase (0-1)
  const phaseProgress = (globalProgress - phase.start) / (phase.end - phase.start);
  const easing = phase.easing || 'linear';
  const transforms = {};

  for (const [key, value] of Object.entries(phase.transforms || {})) {
    // Cas special: oscillation
    if (value === 'oscillate') {
      const freq = phase.oscillateFreq || 10;
      const amp = phase.oscillateAmp || 5;
      transforms[key] = Math.sin(phaseProgress * freq * Math.PI * 2) * amp;
      continue;
    }

    // Cas special: random shake
    if (value === 'shake') {
      const amp = phase.shakeAmp || 5;
      transforms[key] = (Math.random() - 0.5) * amp * 2;
      continue;
    }

    // Interpolation standard [start, end]
    if (Array.isArray(value) && value.length === 2) {
      transforms[key] = lerp(value[0], value[1], phaseProgress, easing);
    }
  }

  return transforms;
}

/**
 * Calcule tous les transforms actifs pour un instant donne.
 * @param {Array} phases - Liste des phases d'animation
 * @param {number} globalProgress - Progression globale (0-1)
 * @returns {Object} - Transforms combines {translateX, translateY, rotation, scale, opacity}
 */
export function computeAnimationTransforms(phases, globalProgress) {
  const result = {
    translateX: 0,
    translateY: 0,
    translateZ: 0,
    rotation: 0,
    rotateX: 0,
    rotateY: 0,
    rotateZ: 0,
    scale: 1.0,
    opacity: 1.0,
    perspective: 800,
  };

  // Accumule les transforms de toutes les phases actives
  for (const phase of phases) {
    const phaseTransforms = computePhaseTransforms(phase, globalProgress);
    if (phaseTransforms) {
      // Additionne translateX/Y/Z/rotation/rotateX/Y/Z, multiplie scale, prend le min pour opacity
      if (phaseTransforms.translateX !== undefined) {
        result.translateX += phaseTransforms.translateX;
      }
      if (phaseTransforms.translateY !== undefined) {
        result.translateY += phaseTransforms.translateY;
      }
      if (phaseTransforms.translateZ !== undefined) {
        result.translateZ += phaseTransforms.translateZ;
      }
      if (phaseTransforms.rotation !== undefined) {
        result.rotation += phaseTransforms.rotation;
      }
      if (phaseTransforms.rotateX !== undefined) {
        result.rotateX += phaseTransforms.rotateX;
      }
      if (phaseTransforms.rotateY !== undefined) {
        result.rotateY += phaseTransforms.rotateY;
      }
      if (phaseTransforms.rotateZ !== undefined) {
        result.rotateZ += phaseTransforms.rotateZ;
      }
      if (phaseTransforms.scale !== undefined) {
        result.scale *= phaseTransforms.scale;
      }
      if (phaseTransforms.opacity !== undefined) {
        result.opacity = Math.min(result.opacity, phaseTransforms.opacity);
      }
      if (phaseTransforms.perspective !== undefined) {
        result.perspective = phaseTransforms.perspective;
      }
    }
  }

  return result;
}

// =====================================================================
// Systeme de particules
// =====================================================================

/**
 * Cree une particule a partir d'un descripteur.
 */
export function createParticle(descriptor, sourceX, sourceY) {
  const angle = (Math.random() * descriptor.spread - descriptor.spread / 2) * (Math.PI / 180);
  const speed = descriptor.speed || 100;
  const vx = Math.cos(angle) * speed;
  const vy = Math.sin(angle) * speed;
  
  // Support 3D: vitesse en profondeur
  const depth = descriptor.depth || 0;
  const vz = depth > 0 ? (Math.random() - 0.5) * depth * 2 : 0;

  return {
    type: descriptor.type,
    x: sourceX,
    y: sourceY,
    z: 0,
    vx,
    vy,
    vz,
    color: descriptor.color || '#ffffff',
    life: 1.0, // 0-1, decremente au fil du temps
    maxLife: descriptor.duration || 0.8, // duree en secondes
    size: descriptor.size || 4,
    gravity: descriptor.gravity || 0,
    fadeOut: descriptor.fadeOut !== false,
  };
}

/**
 * Met a jour une particule (mouvement, vie).
 * @returns {boolean} - true si la particule est encore vivante
 */
export function updateParticle(particle, deltaTime) {
  particle.x += particle.vx * deltaTime;
  particle.y += particle.vy * deltaTime;
  particle.z = (particle.z || 0) + (particle.vz || 0) * deltaTime;
  particle.vy += particle.gravity * deltaTime * 100; // gravite
  particle.life -= deltaTime / particle.maxLife;

  return particle.life > 0;
}

/**
 * Dessine une particule sur un canvas.
 */
export function renderParticle(ctx, particle) {
  // Effet de profondeur 3D basé sur z
  const z = particle.z || 0;
  const depthScale = 1 + z / 500; // Plus proche = plus grand
  const depthAlpha = Math.max(0.2, Math.min(1, 1 + z / 300)); // Plus proche = plus opaque
  
  const alpha = (particle.fadeOut ? particle.life : 1.0) * depthAlpha;
  const size = particle.size * depthScale;
  
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.fillStyle = particle.color;

  // Differents types de rendu
  if (particle.type === 'spark' || particle.type === 'muzzle_flash') {
    // Étoile brillante avec halo
    const grad = ctx.createRadialGradient(particle.x, particle.y, 0, particle.x, particle.y, size * 3);
    grad.addColorStop(0, particle.color);
    grad.addColorStop(0.5, particle.color + '88');
    grad.addColorStop(1, 'transparent');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(particle.x, particle.y, size * 3 * particle.life, 0, Math.PI * 2);
    ctx.fill();
    
    // Point central brillant
    ctx.fillStyle = '#ffffff';
    ctx.globalAlpha = alpha * 0.9;
    ctx.beginPath();
    ctx.arc(particle.x, particle.y, size * 0.8, 0, Math.PI * 2);
    ctx.fill();
  } else if (particle.type === 'blood' || particle.type === 'blood_splatter') {
    // Goutte de sang avec éclaboussure
    ctx.fillStyle = particle.color;
    ctx.globalAlpha = alpha * 0.9;
    ctx.beginPath();
    ctx.arc(particle.x, particle.y, size * particle.life * 1.2, 0, Math.PI * 2);
    ctx.fill();
    
    // Traînée
    ctx.fillRect(
      particle.x - size * 0.5, 
      particle.y - size * 0.5, 
      size * 0.8, 
      size * 1.5
    );
  } else if (particle.type === 'energy' || particle.type === 'aura') {
    // Halo lumineux pulsant
    const pulseSize = size * (2 + Math.sin(Date.now() * 0.01) * 0.3);
    const grad = ctx.createRadialGradient(particle.x, particle.y, 0, particle.x, particle.y, pulseSize * 2);
    grad.addColorStop(0, particle.color + 'cc');
    grad.addColorStop(0.3, particle.color + '88');
    grad.addColorStop(0.6, particle.color + '33');
    grad.addColorStop(1, 'transparent');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(particle.x, particle.y, pulseSize * 2 * particle.life, 0, Math.PI * 2);
    ctx.fill();
  } else if (particle.type === 'projectile') {
    // Projectile avec traînée lumineuse
    const trailLength = 15;
    const grad = ctx.createLinearGradient(
      particle.x - particle.vx * 0.02,
      particle.y - particle.vy * 0.02,
      particle.x,
      particle.y
    );
    grad.addColorStop(0, 'transparent');
    grad.addColorStop(0.5, particle.color + '88');
    grad.addColorStop(1, particle.color);
    ctx.strokeStyle = grad;
    ctx.lineWidth = size * 1.5;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(particle.x - particle.vx * 0.02, particle.y - particle.vy * 0.02);
    ctx.lineTo(particle.x, particle.y);
    ctx.stroke();
    
    // Point lumineux central
    ctx.fillStyle = '#ffffff';
    ctx.globalAlpha = alpha;
    ctx.beginPath();
    ctx.arc(particle.x, particle.y, size * 0.7, 0, Math.PI * 2);
    ctx.fill();
  } else if (particle.type === 'explosion') {
    // Explosion avec cercles
    for (let i = 0; i < 3; i++) {
      const offset = i * 0.15;
      const explSize = size * (3 - i) * particle.life;
      ctx.globalAlpha = alpha * (0.8 - i * 0.2);
      ctx.fillStyle = i === 0 ? '#ffffff' : particle.color;
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, explSize, 0, Math.PI * 2);
      ctx.fill();
    }
  } else {
    // Générique: carré lumineux
    const genericSize = size * particle.life;
    ctx.fillRect(particle.x - genericSize / 2, particle.y - genericSize / 2, genericSize, genericSize);
  }

  ctx.restore();
}

// =====================================================================
// Cache d'animations cote client
// =====================================================================

const CLIENT_ANIMATION_CACHE = new Map();

/**
 * Recupere une animation depuis le cache client ou l'API.
 * @param {string} skillId - ID du skill
 * @param {Object} skillInfo - Info supplementaire pour generation (name, description, category)
 * @returns {Promise<Object>} - Descripteur d'animation
 */
export async function fetchAnimation(skillId, skillInfo = {}) {
  // Verifier cache client
  if (CLIENT_ANIMATION_CACHE.has(skillId)) {
    return CLIENT_ANIMATION_CACHE.get(skillId);
  }

  // Les tests Vitest/jsdom résolvent `fetch` avec Node, qui refuse les URL
  // relatives. Le fallback local garde les animations testables sans bruit réseau.
  if (import.meta.env.MODE === 'test' || typeof globalThis.location === 'undefined' || globalThis.location.protocol === 'about:') {
    return createFallbackAnimation(skillId);
  }

  // Tenter de recuperer depuis l'API
  try {
    // D'abord essayer de recuperer depuis le cache serveur
    let response = await fetch(`/api/animations/${skillId}`);
    let animation = await response.json();

    // Si c'est une animation par defaut et qu'on a plus d'info, generer
    if (animation.skill_id === skillId && skillInfo.name && skillInfo.description) {
      response = await fetch('/api/animations/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          skill_id: skillId,
          skill_name: skillInfo.name || skillId,
          skill_description: skillInfo.description || '',
          skill_category: skillInfo.category || 'combat',
        }),
      });
      animation = await response.json();
    }

    // Mettre en cache client
    CLIENT_ANIMATION_CACHE.set(skillId, animation);
    return animation;
  } catch (err) {
    console.warn(`Erreur fetch animation ${skillId}:`, err);
    return createFallbackAnimation(skillId);
  }
}

function createFallbackAnimation(skillId) {
  return {
      skill_id: skillId,
      duration: 600,
      phases: [
        {
          name: 'action',
          start: 0,
          end: 0.5,
          easing: 'easeOut',
          transforms: { translateX: [0, 30], scale: [1.0, 1.1] },
        },
        {
          name: 'recovery',
          start: 0.5,
          end: 1.0,
          easing: 'easeIn',
          transforms: { translateX: [30, 0], scale: [1.1, 1.0] },
        },
      ],
      particles: [],
  };
}

/**
 * Precharge plusieurs animations.
 */
export async function preloadAnimations(skillIds) {
  const promises = skillIds.map((id) => fetchAnimation(id));
  await Promise.all(promises);
}

/**
 * Efface le cache client d'animations.
 */
export function clearClientAnimationCache() {
  CLIENT_ANIMATION_CACHE.clear();
}

// =====================================================================
// Hook d'utilisation (pour React)
// =====================================================================

/**
 * Classe pour gerer une animation en cours.
 */
export class AnimationPlayer {
  constructor(descriptor) {
    this.descriptor = descriptor;
    this.startTime = null;
    this.particles = [];
    this.particlesEmitted = new Set();
    this.isComplete = false;
    this.cameraShakeTriggered = false;
    this.flashActive = false;
  }

  /**
   * Demarre l'animation.
   */
  start() {
    this.startTime = performance.now();
    this.isComplete = false;
    this.particles = [];
    this.particlesEmitted.clear();
    this.cameraShakeTriggered = false;
    this.flashActive = false;
  }

  /**
   * Met a jour l'animation et retourne les transforms actuels.
   * @returns {Object} { transforms, particles, cameraShake, flash, isComplete }
   */
  update(now) {
    if (!this.startTime) {
      return { transforms: {}, particles: [], isComplete: true };
    }

    const elapsed = now - this.startTime;
    const progress = Math.min(1.0, elapsed / this.descriptor.duration);
    this.isComplete = progress >= 1.0;

    // Calculer transforms
    const transforms = computeAnimationTransforms(this.descriptor.phases, progress);

    // Emettre particules
    let cameraShake = null;
    if (this.descriptor.particles) {
      for (const pDesc of this.descriptor.particles) {
        if (progress >= pDesc.at && !this.particlesEmitted.has(pDesc)) {
          this.particlesEmitted.add(pDesc);
          // Creer N particules
          for (let i = 0; i < (pDesc.count || 1); i++) {
            this.particles.push(createParticle(pDesc, 0, 0));
          }
        }
      }
    }

    // Camera shake
    if (this.descriptor.cameraShake && progress >= this.descriptor.cameraShake.at && !this.cameraShakeTriggered) {
      this.cameraShakeTriggered = true;
      cameraShake = this.descriptor.cameraShake.intensity || 2;
    }

    // Flash
    let flash = null;
    if (this.descriptor.flash) {
      const flashStart = this.descriptor.flash.at || 0;
      const flashDuration = this.descriptor.flash.duration || 0.2;
      if (progress >= flashStart && progress < flashStart + flashDuration) {
        const flashProgress = (progress - flashStart) / flashDuration;
        this.flashActive = true;
        flash = {
          color: this.descriptor.flash.color,
          intensity: this.descriptor.flash.intensity * (1 - flashProgress),
        };
      } else if (this.flashActive) {
        this.flashActive = false;
      }
    }

    // Mettre a jour particules
    const deltaTime = 0.016; // approximation 60fps
    this.particles = this.particles.filter((p) => updateParticle(p, deltaTime));

    return {
      transforms,
      particles: this.particles,
      cameraShake,
      flash,
      isComplete: this.isComplete,
    };
  }

  /**
   * Reinitialise le lecteur.
   */
  reset() {
    this.startTime = null;
    this.particles = [];
    this.particlesEmitted.clear();
    this.isComplete = false;
    this.cameraShakeTriggered = false;
    this.flashActive = false;
  }
}
