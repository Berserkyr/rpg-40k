import { useEffect, useRef, useState, useMemo } from 'react';
import { fetchAnimation, AnimationPlayer, renderParticle } from '../animation_engine';

/**
 * Composant d'action animée procédurale.
 * 
 * Utilise le système d'animations générées par LLM pour afficher
 * des animations de combat/skill dynamiques et réutilisables.
 * 
 * @param {string} skillId - ID du skill à animer
 * @param {Object} skillInfo - Info pour génération (name, description, category)
 * @param {ReactNode} children - Sprite/element à animer
 * @param {boolean} trigger - Change pour déclencher l'animation
 * @param {Function} onComplete - Callback quand l'animation est terminée
 * @param {string} facing - Direction ("left" ou "right")
 */
export default function AnimatedAction({
  skillId = 'default_attack',
  skillInfo = {},
  children,
  trigger = 0,
  onComplete = null,
  facing = 'left',
}) {
  const containerRef = useRef(null);
  const canvasRef = useRef(null);
  const rafRef = useRef(0);
  const playerRef = useRef(null);
  
  const [animationDescriptor, setAnimationDescriptor] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const facingSign = facing === 'left' ? -1 : 1;

  // Charger l'animation depuis l'API/cache
  useEffect(() => {
    let mounted = true;
    
    fetchAnimation(skillId, skillInfo).then((descriptor) => {
      if (mounted) {
        setAnimationDescriptor(descriptor);
        playerRef.current = new AnimationPlayer(descriptor);
      }
    });

    return () => {
      mounted = false;
    };
  }, [skillId, skillInfo]);

  // Déclencher l'animation quand trigger change
  useEffect(() => {
    if (trigger > 0 && playerRef.current && animationDescriptor) {
      playerRef.current.start();
      setIsPlaying(true);
    }
  }, [trigger, animationDescriptor]);

  // Boucle d'animation
  useEffect(() => {
    if (!isPlaying || !playerRef.current) return undefined;

    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return undefined;

    const ctx = canvas.getContext('2d');
    if (!ctx) return undefined;

    let mounted = true;
    let shakeOffset = { x: 0, y: 0 };
    let shakeDecay = 0;

    const frame = (now) => {
      if (!mounted) return;

      const state = playerRef.current.update(now);

      // Appliquer camera shake
      if (state.cameraShake) {
        shakeDecay = state.cameraShake;
      }
      if (shakeDecay > 0) {
        shakeOffset.x = (Math.random() - 0.5) * shakeDecay * 4;
        shakeOffset.y = (Math.random() - 0.5) * shakeDecay * 4;
        shakeDecay *= 0.92; // decay
        if (shakeDecay < 0.1) shakeDecay = 0;
      }

      // Appliquer transforms au container
      if (container) {
        const t = state.transforms;
        const tx = (t.translateX || 0) * facingSign + shakeOffset.x;
        const ty = (t.translateY || 0) + shakeOffset.y;
        const rot = (t.rotation || 0) * facingSign;
        const scale = t.scale || 1.0;
        const opacity = t.opacity !== undefined ? t.opacity : 1.0;

        container.style.transform = `
          translate(${tx}px, ${ty}px)
          rotate(${rot}rad)
          scale(${scale})
        `;
        container.style.opacity = opacity;

        // Flash
        if (state.flash) {
          container.style.filter = `brightness(${1 + state.flash.intensity}) saturate(${1 + state.flash.intensity * 0.5})`;
        } else {
          container.style.filter = '';
        }
      }

      // Dessiner particules
      if (canvas && ctx) {
        const rect = container.getBoundingClientRect();
        canvas.width = rect.width * 2;
        canvas.height = rect.height * 2;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.scale(2, 2);

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        for (const particle of state.particles) {
          renderParticle(ctx, {
            ...particle,
            x: centerX + particle.x * facingSign,
            y: centerY + particle.y,
          });
        }
      }

      // Vérifier fin
      if (state.isComplete) {
        setIsPlaying(false);
        if (onComplete) onComplete();
        // Reset transforms
        if (container) {
          container.style.transform = '';
          container.style.opacity = 1;
          container.style.filter = '';
        }
        if (canvas && ctx) {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
        return;
      }

      rafRef.current = requestAnimationFrame(frame);
    };

    rafRef.current = requestAnimationFrame(frame);

    return () => {
      mounted = false;
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [isPlaying, facingSign, onComplete]);

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      {/* Canvas pour les particules (derrière) */}
      <canvas
        ref={canvasRef}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          pointerEvents: 'none',
          zIndex: 0,
        }}
      />
      {/* Container du sprite/element (avec transforms) */}
      <div
        ref={containerRef}
        style={{
          position: 'relative',
          zIndex: 1,
          transition: isPlaying ? 'none' : 'transform 0.3s ease-out, opacity 0.3s ease-out',
        }}
      >
        {children}
      </div>
    </div>
  );
}
