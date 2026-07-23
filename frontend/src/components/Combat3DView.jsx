/**
 * Composant de combat 3D avec rendu voxel
 * 
 * Remplace l'ancien système 2D par un moteur 3D complet
 */

import { useEffect, useRef, useState } from 'react';
import { CombatScene3D } from '../engine3d/CombatScene3D';
import './Combat3DView.css';

/**
 * Vue 3D du combat avec personnages voxel animés
 */
export default function Combat3DView({ 
  playerData = {},
  enemies = [],
  onAnimationComplete = null,
  currentAction = null,
  compact = false,
}) {
  const canvasRef = useRef(null);
  const sceneRef = useRef(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const enemySignature = enemies.map((enemy) => `${enemy.type}:${enemy.faction}:${enemy.scale}`).join('|');

  // Initialisation de la scène
  useEffect(() => {
    if (!canvasRef.current) return;

    const combatScene = new CombatScene3D(canvasRef.current);
    sceneRef.current = combatScene;

    // Ajouter le joueur
    combatScene.addPlayer('player', {
      faction: playerData.faction || 'imperial',
      armorLevel: playerData.armorLevel || 'medium',
      weapon: playerData.weapon || 'bolter',
    });

    // Ajouter les ennemis
    enemies.forEach((enemy, index) => {
      combatScene.addEnemy(`enemy${index}`, {
        type: enemy.type || 'enemy',
        faction: enemy.faction || 'chaos',
        bodyType: enemy.bodyType || 'human',
        armorLevel: enemy.armorLevel || 'medium',
        weapon: enemy.weapon || 'chainsword',
        scale: enemy.scale || 1.2
      });
    });

    setIsLoaded(true);

    return () => {
      combatScene.dispose();
      if (sceneRef.current === combatScene) sceneRef.current = null;
    };
  }, []);

  // Update des ennemis si changement
  useEffect(() => {
    if (!sceneRef.current || !isLoaded) return;

    // Supprimer les anciens ennemis
    sceneRef.current.entities.forEach((entity, id) => {
      if (id.startsWith('enemy')) {
        sceneRef.current.removeEntity(id);
      }
    });

    // Ajouter les nouveaux
    enemies.forEach((enemy, index) => {
      sceneRef.current.addEnemy(`enemy${index}`, {
        type: enemy.type || 'enemy',
        faction: enemy.faction || 'chaos',
        bodyType: enemy.bodyType || 'human',
        armorLevel: enemy.armorLevel || 'medium',
        weapon: enemy.weapon || 'chainsword',
        scale: enemy.scale || 1.2
      });
    });
  }, [enemySignature, isLoaded]);

  // Exécution des actions/animations
  useEffect(() => {
    if (!sceneRef.current || !currentAction || !isLoaded) return;

    const scene = sceneRef.current;
    const { type, entityId, targetId, animName, effectType } = currentAction;

    console.log('🎬 Playing action:', currentAction);

    // Jouer l'animation de l'attaquant
    if (animName) {
      scene.playAnimation(entityId, animName, false);
    }

    // Effets selon le type d'action
    setTimeout(() => {
      const targetEntity = scene.entities.get(targetId);
      
      if (targetEntity) {
        const targetPos = targetEntity.model.position.clone();
        targetPos.y += 5; // Centre du corps

        // Particules
        if (type === 'attack') {
          if (effectType === 'melee') {
            scene.createParticleEffect(targetPos, 'spark', 15);
            scene.createParticleEffect(targetPos, 'blood', 10);
          } else if (effectType === 'ranged') {
            scene.createParticleEffect(targetPos, 'energy', 20);
          }
        } else if (type === 'skill') {
          scene.createParticleEffect(targetPos, 'explosion', 30);
        }

        // Camera shake
        scene.shakeCamera(type === 'skill' ? 2.0 : 1.0, 0.3);

        // Flash
        const flashColors = {
          melee: 0xffffff,
          ranged: 0x00ffff,
          explosion: 0xff6600
        };
        scene.flashScreen(flashColors[effectType] || 0xffffff, 0.5, 0.1);

        // Animation de la cible (hurt)
        scene.playAnimation(targetId, 'hurt', false);
      }

      // Callback
      if (onAnimationComplete) {
        setTimeout(() => {
          onAnimationComplete(currentAction);
        }, 800);
      }
    }, 300); // Délai pour l'impact

  }, [currentAction, isLoaded, onAnimationComplete]);

  return (
    <div className={`combat-3d-container ${compact ? 'combat-3d-compact' : ''}`}>
      <canvas 
        ref={canvasRef}
        className="combat-3d-canvas"
      />
      
      {!isLoaded && (
        <div className="combat-3d-loading">
          <div className="loading-spinner"></div>
          <p>Chargement de la scène de combat 3D...</p>
        </div>
      )}

      {!compact && <div className="combat-3d-controls">
        <button 
          onClick={() => sceneRef.current?.createEnvironment('industrial')}
          className="env-btn"
        >
          🏭 Industriel
        </button>
        <button 
          onClick={() => sceneRef.current?.createEnvironment('temple')}
          className="env-btn"
        >
          ⛩️ Temple
        </button>
        <button 
          onClick={() => sceneRef.current?.createEnvironment('wasteland')}
          className="env-btn"
        >
          🏜️ Wasteland
        </button>
      </div>}

      {!compact && <div className="combat-3d-info">
        <div className="info-badge">
          🎮 Moteur 3D Voxel
        </div>
        <div className="info-badge">
          {sceneRef.current?.entities.size || 0} entités
        </div>
        <div className="info-badge">
          {sceneRef.current?.particles.length || 0} particules
        </div>
      </div>}
    </div>
  );
}
