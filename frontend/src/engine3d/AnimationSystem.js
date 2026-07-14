/**
 * Système d'animation skeletal pour modèles voxel 3D
 * 
 * Anime les parties du corps avec inverse kinematics et interpolation
 */

import * as THREE from 'three';

/**
 * Contrôleur d'animation skeletal
 */
export class SkeletalAnimator {
  constructor(model, parts, skeleton) {
    this.model = model;
    this.parts = parts;
    this.skeleton = skeleton;
    this.animations = {};
    this.currentAnimation = null;
    this.animationTime = 0;
    this.isPlaying = false;
  }

  /**
   * Enregistre une animation
   */
  registerAnimation(name, animationData) {
    this.animations[name] = animationData;
  }

  /**
   * Joue une animation
   */
  play(name, loop = false) {
    if (!this.animations[name]) {
      console.warn(`Animation ${name} not found`);
      return;
    }

    this.currentAnimation = {
      name,
      data: this.animations[name],
      loop,
      startTime: Date.now()
    };
    this.isPlaying = true;
    this.animationTime = 0;
  }

  /**
   * Arrête l'animation
   */
  stop() {
    this.isPlaying = false;
    this.currentAnimation = null;
  }

  /**
   * Update l'animation (appelé chaque frame)
   */
  update(deltaTime) {
    if (!this.isPlaying || !this.currentAnimation) return;

    this.animationTime += deltaTime;
    const duration = this.currentAnimation.data.duration / 1000; // ms -> s

    let progress = this.animationTime / duration;

    if (progress >= 1.0) {
      if (this.currentAnimation.loop) {
        this.animationTime = 0;
        progress = 0;
      } else {
        this.stop();
        this.resetPose();
        return;
      }
    }

    this.applyAnimation(progress);
  }

  /**
   * Applique l'animation au modèle selon le progress (0-1)
   */
  applyAnimation(progress) {
    const anim = this.currentAnimation.data;

    anim.tracks.forEach(track => {
      const part = this.parts[track.part];
      if (!part) return;

      // Trouver les keyframes autour du progress
      const { keyframe0, keyframe1, localProgress } = this.findKeyframes(track.keyframes, progress);

      // Interpoler position
      if (keyframe0.position && keyframe1.position) {
        part.position.lerpVectors(
          new THREE.Vector3(...keyframe0.position),
          new THREE.Vector3(...keyframe1.position),
          localProgress
        );
      }

      // Interpoler rotation
      if (keyframe0.rotation && keyframe1.rotation) {
        const quat0 = new THREE.Euler(...keyframe0.rotation).toQuaternion();
        const quat1 = new THREE.Euler(...keyframe1.rotation).toQuaternion();
        part.quaternion.slerpQuaternions(quat0, quat1, localProgress);
      }

      // Interpoler scale
      if (keyframe0.scale && keyframe1.scale) {
        const scale0 = typeof keyframe0.scale === 'number' ? 
          new THREE.Vector3(keyframe0.scale, keyframe0.scale, keyframe0.scale) :
          new THREE.Vector3(...keyframe0.scale);
        const scale1 = typeof keyframe1.scale === 'number' ?
          new THREE.Vector3(keyframe1.scale, keyframe1.scale, keyframe1.scale) :
          new THREE.Vector3(...keyframe1.scale);
        part.scale.lerpVectors(scale0, scale1, localProgress);
      }
    });
  }

  /**
   * Trouve les keyframes avant/après le progress
   */
  findKeyframes(keyframes, progress) {
    for (let i = 0; i < keyframes.length - 1; i++) {
      const kf0 = keyframes[i];
      const kf1 = keyframes[i + 1];

      if (progress >= kf0.time && progress <= kf1.time) {
        const duration = kf1.time - kf0.time;
        const localProgress = duration > 0 ? (progress - kf0.time) / duration : 0;
        return { keyframe0: kf0, keyframe1: kf1, localProgress };
      }
    }

    // Dernier keyframe
    const lastKf = keyframes[keyframes.length - 1];
    return { keyframe0: lastKf, keyframe1: lastKf, localProgress: 0 };
  }

  /**
   * Réinitialise la pose par défaut
   */
  resetPose() {
    // Reset positions d'origine (T-pose)
    if (this.parts.head) this.parts.head.position.set(0, 7, 0);
    if (this.parts.torso) this.parts.torso.position.set(0, 3, 0);
    if (this.parts.leftArm) this.parts.leftArm.position.set(-2, 4, 0);
    if (this.parts.rightArm) this.parts.rightArm.position.set(2, 4, 0);
    if (this.parts.leftLeg) this.parts.leftLeg.position.set(-1, -2, 0);
    if (this.parts.rightLeg) this.parts.rightLeg.position.set(1, -2, 0);

    // Reset rotations
    Object.values(this.parts).forEach(part => {
      part.rotation.set(0, 0, 0);
      part.scale.set(1, 1, 1);
    });
  }
}

/**
 * Bibliothèque d'animations prédéfinies pour modèles voxel
 */
export const VOXEL_ANIMATIONS = {
  idle: {
    duration: 2000,
    tracks: [
      {
        part: 'torso',
        keyframes: [
          { time: 0, position: [0, 3, 0], scale: 1 },
          { time: 0.5, position: [0, 3.2, 0], scale: 1.02 },
          { time: 1.0, position: [0, 3, 0], scale: 1 }
        ]
      },
      {
        part: 'head',
        keyframes: [
          { time: 0, position: [0, 7, 0], rotation: [0, 0, 0] },
          { time: 0.5, position: [0, 7.2, 0], rotation: [0.05, 0, 0] },
          { time: 1.0, position: [0, 7, 0], rotation: [0, 0, 0] }
        ]
      }
    ]
  },

  attack_melee: {
    duration: 800,
    tracks: [
      {
        part: 'torso',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.2, rotation: [0, -0.4, 0] },
          { time: 0.35, rotation: [0, 0.6, 0.1] },
          { time: 0.7, rotation: [0, 0.2, 0] },
          { time: 1.0, rotation: [0, 0, 0] }
        ]
      },
      {
        part: 'rightArm',
        keyframes: [
          { time: 0, rotation: [0, 0, 0], position: [2, 4, 0] },
          { time: 0.2, rotation: [-1.2, 0, 0.5], position: [1.5, 5, 0] },
          { time: 0.35, rotation: [0.8, 0, -0.3], position: [2.5, 2, -1] },
          { time: 0.7, rotation: [0.3, 0, 0], position: [2.2, 3.5, 0] },
          { time: 1.0, rotation: [0, 0, 0], position: [2, 4, 0] }
        ]
      },
      {
        part: 'leftArm',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.35, rotation: [0.4, 0, 0.2] },
          { time: 1.0, rotation: [0, 0, 0] }
        ]
      },
      {
        part: 'head',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.2, rotation: [0, -0.3, 0] },
          { time: 0.35, rotation: [-0.1, 0.5, 0] },
          { time: 1.0, rotation: [0, 0, 0] }
        ]
      }
    ]
  },

  attack_shoot: {
    duration: 600,
    tracks: [
      {
        part: 'rightArm',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.15, rotation: [-0.5, 0, 0] },
          { time: 0.25, rotation: [-0.3, 0, 0.2] },
          { time: 0.6, rotation: [-0.4, 0, 0.1] },
          { time: 1.0, rotation: [0, 0, 0] }
        ]
      },
      {
        part: 'leftArm',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.15, rotation: [-0.6, 0, -0.2] },
          { time: 1.0, rotation: [0, 0, 0] }
        ]
      },
      {
        part: 'torso',
        keyframes: [
          { time: 0, position: [0, 3, 0] },
          { time: 0.25, position: [0, 2.8, -0.3] },
          { time: 1.0, position: [0, 3, 0] }
        ]
      }
    ]
  },

  hurt: {
    duration: 500,
    tracks: [
      {
        part: 'torso',
        keyframes: [
          { time: 0, position: [0, 3, 0], rotation: [0, 0, 0] },
          { time: 0.2, position: [-0.8, 2.7, 0.2], rotation: [0.2, -0.3, 0.3] },
          { time: 0.5, position: [-0.3, 2.9, 0], rotation: [0.1, 0, 0.1] },
          { time: 1.0, position: [0, 3, 0], rotation: [0, 0, 0] }
        ]
      },
      {
        part: 'head',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.2, rotation: [-0.3, 0.2, 0.2] },
          { time: 1.0, rotation: [0, 0, 0] }
        ]
      },
      {
        part: 'leftArm',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.2, rotation: [0.5, 0, -0.4] },
          { time: 1.0, rotation: [0, 0, 0] }
        ]
      },
      {
        part: 'rightArm',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.2, rotation: [0.5, 0, 0.4] },
          { time: 1.0, rotation: [0, 0, 0] }
        ]
      }
    ]
  },

  death: {
    duration: 1500,
    tracks: [
      {
        part: 'torso',
        keyframes: [
          { time: 0, position: [0, 3, 0], rotation: [0, 0, 0] },
          { time: 0.3, position: [0, 2, 0], rotation: [0.3, 0, 0] },
          { time: 0.6, position: [0, 0, 0], rotation: [1.2, 0, 0.3] },
          { time: 1.0, position: [0, -1, 0], rotation: [1.57, 0, 0.5], scale: 0.9 }
        ]
      },
      {
        part: 'head',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.3, rotation: [-0.5, 0, 0] },
          { time: 1.0, rotation: [-0.8, 0.3, 0] }
        ]
      },
      {
        part: 'leftArm',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.3, rotation: [1.2, 0, -0.5] },
          { time: 1.0, rotation: [1.8, 0, -0.8] }
        ]
      },
      {
        part: 'rightArm',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.3, rotation: [1.2, 0, 0.5] },
          { time: 1.0, rotation: [1.8, 0, 0.8] }
        ]
      },
      {
        part: 'leftLeg',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.6, rotation: [0.8, 0, -0.3] },
          { time: 1.0, rotation: [1.2, 0, -0.5] }
        ]
      },
      {
        part: 'rightLeg',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.6, rotation: [0.8, 0, 0.3] },
          { time: 1.0, rotation: [1.2, 0, 0.5] }
        ]
      }
    ]
  },

  victory: {
    duration: 2000,
    tracks: [
      {
        part: 'rightArm',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.3, rotation: [-2.5, 0, 0] },
          { time: 0.5, rotation: [-2.8, 0, 0.2] },
          { time: 0.7, rotation: [-2.5, 0, -0.2] },
          { time: 1.0, rotation: [-2.5, 0, 0] }
        ]
      },
      {
        part: 'head',
        keyframes: [
          { time: 0, rotation: [0, 0, 0] },
          { time: 0.3, rotation: [0.3, 0, 0] },
          { time: 1.0, rotation: [0.3, 0, 0] }
        ]
      },
      {
        part: 'torso',
        keyframes: [
          { time: 0, position: [0, 3, 0] },
          { time: 0.5, position: [0, 3.5, 0], scale: 1.05 },
          { time: 1.0, position: [0, 3.2, 0], scale: 1.05 }
        ]
      }
    ]
  },

  walk: {
    duration: 1000,
    tracks: [
      {
        part: 'leftLeg',
        keyframes: [
          { time: 0, rotation: [-0.5, 0, 0] },
          { time: 0.5, rotation: [0.5, 0, 0] },
          { time: 1.0, rotation: [-0.5, 0, 0] }
        ]
      },
      {
        part: 'rightLeg',
        keyframes: [
          { time: 0, rotation: [0.5, 0, 0] },
          { time: 0.5, rotation: [-0.5, 0, 0] },
          { time: 1.0, rotation: [0.5, 0, 0] }
        ]
      },
      {
        part: 'leftArm',
        keyframes: [
          { time: 0, rotation: [0.3, 0, 0] },
          { time: 0.5, rotation: [-0.3, 0, 0] },
          { time: 1.0, rotation: [0.3, 0, 0] }
        ]
      },
      {
        part: 'rightArm',
        keyframes: [
          { time: 0, rotation: [-0.3, 0, 0] },
          { time: 0.5, rotation: [0.3, 0, 0] },
          { time: 1.0, rotation: [-0.3, 0, 0] }
        ]
      },
      {
        part: 'torso',
        keyframes: [
          { time: 0, position: [0, 3, 0] },
          { time: 0.25, position: [0, 3.2, 0] },
          { time: 0.5, position: [0, 3, 0] },
          { time: 0.75, position: [0, 3.2, 0] },
          { time: 1.0, position: [0, 3, 0] }
        ]
      }
    ]
  }
};
