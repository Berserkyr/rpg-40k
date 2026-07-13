/**
 * @vitest-environment jsdom
 */
import { describe, it, expect, beforeEach } from 'vitest';
import {
  computeAnimationTransforms,
  createParticle,
  updateParticle,
  AnimationPlayer,
} from '../animation_engine';

describe('Animation Engine', () => {
  describe('computeAnimationTransforms', () => {
    it('retourne des transforms par défaut à progression 0', () => {
      const phases = [
        {
          name: 'test',
          start: 0,
          end: 1,
          easing: 'linear',
          transforms: {
            translateX: [0, 100],
            scale: [1.0, 1.5],
          },
        },
      ];
      const result = computeAnimationTransforms(phases, 0);
      expect(result.translateX).toBe(0);
      expect(result.scale).toBe(1.0);
    });

    it('interpole correctement à mi-progression', () => {
      const phases = [
        {
          name: 'test',
          start: 0,
          end: 1,
          easing: 'linear',
          transforms: {
            translateX: [0, 100],
            scale: [1.0, 2.0],
          },
        },
      ];
      const result = computeAnimationTransforms(phases, 0.5);
      expect(result.translateX).toBeCloseTo(50);
      expect(result.scale).toBeCloseTo(1.5);
    });

    it('atteint les valeurs finales à progression 1', () => {
      const phases = [
        {
          name: 'test',
          start: 0,
          end: 1,
          easing: 'linear',
          transforms: {
            translateX: [0, 100],
            rotation: [0, 1.57],
            opacity: [1, 0],
          },
        },
      ];
      const result = computeAnimationTransforms(phases, 1);
      expect(result.translateX).toBeCloseTo(100);
      expect(result.rotation).toBeCloseTo(1.57);
      expect(result.opacity).toBeCloseTo(0);
    });

    it('ignore les phases hors de la progression actuelle', () => {
      const phases = [
        {
          name: 'phase1',
          start: 0,
          end: 0.3,
          easing: 'linear',
          transforms: { translateX: [0, 50] },
        },
        {
          name: 'phase2',
          start: 0.7,
          end: 1.0,
          easing: 'linear',
          transforms: { translateX: [50, 0] },
        },
      ];
      // À progression 0.5, aucune phase n'est active
      const result = computeAnimationTransforms(phases, 0.5);
      expect(result.translateX).toBe(0);
    });

    it('accumule les transforms de phases multiples', () => {
      const phases = [
        {
          name: 'phase1',
          start: 0,
          end: 0.5,
          easing: 'linear',
          transforms: { translateX: [0, 30] },
        },
        {
          name: 'phase2',
          start: 0.4,
          end: 1.0,
          easing: 'linear',
          transforms: { translateX: [0, 20], rotation: [0, 0.5] },
        },
      ];
      // À progression 0.45, les deux phases sont actives
      const result = computeAnimationTransforms(phases, 0.45);
      expect(result.translateX).toBeGreaterThan(0);
      expect(result.rotation).toBeGreaterThan(0);
    });
  });

  describe('Particle System', () => {
    it('crée une particule avec les bonnes propriétés', () => {
      const descriptor = {
        type: 'spark',
        color: '#ff0000',
        count: 5,
        spread: 45,
        speed: 100,
      };
      const particle = createParticle(descriptor, 50, 50);
      
      expect(particle.type).toBe('spark');
      expect(particle.color).toBe('#ff0000');
      expect(particle.x).toBe(50);
      expect(particle.y).toBe(50);
      expect(particle.life).toBe(1.0);
    });

    it('met à jour la position de la particule', () => {
      const particle = {
        x: 0,
        y: 0,
        vx: 100,
        vy: 50,
        life: 1.0,
        maxLife: 1.0,
        gravity: 0,
      };
      const alive = updateParticle(particle, 0.1);
      
      expect(alive).toBe(true);
      expect(particle.x).toBeCloseTo(10);
      expect(particle.y).toBeCloseTo(5);
      expect(particle.life).toBeLessThan(1.0);
    });

    it('détecte quand une particule meurt', () => {
      const particle = {
        x: 0,
        y: 0,
        vx: 0,
        vy: 0,
        life: 0.05,
        maxLife: 1.0,
        gravity: 0,
      };
      const alive = updateParticle(particle, 0.1);
      expect(alive).toBe(false);
    });
  });

  describe('AnimationPlayer', () => {
    let descriptor;

    beforeEach(() => {
      descriptor = {
        skill_id: 'test_skill',
        duration: 600,
        phases: [
          {
            name: 'action',
            start: 0,
            end: 0.5,
            easing: 'easeOut',
            transforms: {
              translateX: [0, 50],
              scale: [1.0, 1.2],
            },
          },
          {
            name: 'recovery',
            start: 0.5,
            end: 1.0,
            easing: 'easeIn',
            transforms: {
              translateX: [50, 0],
              scale: [1.2, 1.0],
            },
          },
        ],
        particles: [
          {
            type: 'spark',
            at: 0.3,
            color: '#ffcc00',
            count: 3,
            spread: 30,
            speed: 80,
          },
        ],
        cameraShake: {
          at: 0.3,
          intensity: 2.0,
        },
      };
    });

    it('démarre correctement', () => {
      const player = new AnimationPlayer(descriptor);
      player.start();
      expect(player.startTime).not.toBeNull();
      expect(player.isComplete).toBe(false);
    });

    it('progresse au fil du temps', () => {
      const player = new AnimationPlayer(descriptor);
      player.start();
      
      const now = player.startTime + 300; // 50% progression
      const state = player.update(now);
      
      expect(state.transforms).toBeDefined();
      expect(state.isComplete).toBe(false);
    });

    it('se termine à la fin de la durée', () => {
      const player = new AnimationPlayer(descriptor);
      player.start();
      
      const now = player.startTime + 600; // 100% progression
      const state = player.update(now);
      
      expect(state.isComplete).toBe(true);
    });

    it('émet des particules au bon moment', () => {
      const player = new AnimationPlayer(descriptor);
      player.start();
      
      // Avant le moment d'émission
      let state = player.update(player.startTime + 100);
      expect(state.particles.length).toBe(0);
      
      // Après le moment d'émission (0.3 * 600 = 180ms)
      state = player.update(player.startTime + 200);
      expect(state.particles.length).toBe(3);
    });

    it('déclenche camera shake au bon moment', () => {
      const player = new AnimationPlayer(descriptor);
      player.start();
      
      // Avant le shake
      let state = player.update(player.startTime + 100);
      expect(state.cameraShake).toBeNull();
      
      // Au moment du shake (0.3 * 600 = 180ms)
      state = player.update(player.startTime + 200);
      expect(state.cameraShake).toBe(2.0);
      
      // Après (ne se déclenche qu'une fois)
      state = player.update(player.startTime + 300);
      expect(state.cameraShake).toBeNull();
    });

    it('se réinitialise correctement', () => {
      const player = new AnimationPlayer(descriptor);
      player.start();
      player.update(player.startTime + 300);
      
      player.reset();
      
      expect(player.startTime).toBeNull();
      expect(player.particles.length).toBe(0);
      expect(player.isComplete).toBe(false);
    });
  });

  describe('Easing Functions', () => {
    it('linear retourne une progression linéaire', () => {
      // Testé indirectement via computeAnimationTransforms
      const phases = [
        {
          name: 'test',
          start: 0,
          end: 1,
          easing: 'linear',
          transforms: { translateX: [0, 100] },
        },
      ];
      
      const result25 = computeAnimationTransforms(phases, 0.25);
      const result50 = computeAnimationTransforms(phases, 0.5);
      const result75 = computeAnimationTransforms(phases, 0.75);
      
      expect(result25.translateX).toBeCloseTo(25);
      expect(result50.translateX).toBeCloseTo(50);
      expect(result75.translateX).toBeCloseTo(75);
    });

    it('easeOut ralentit en fin de course', () => {
      const phases = [
        {
          name: 'test',
          start: 0,
          end: 1,
          easing: 'easeOut',
          transforms: { scale: [1.0, 2.0] },
        },
      ];
      
      const result50 = computeAnimationTransforms(phases, 0.5);
      // Avec easeOut, à 50% on devrait être plus avancé que 1.5
      expect(result50.scale).toBeGreaterThan(1.5);
    });
  });
});
