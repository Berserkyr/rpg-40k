/**
 * Page de test/démo du moteur 3D
 */

import { useState } from 'react';
import Combat3DView from '../components/Combat3DView';

export default function Combat3DDemo() {
  const [currentAction, setCurrentAction] = useState(null);
  const [actionCounter, setActionCounter] = useState(0);

  const playerData = {
    faction: 'imperial',
    armorLevel: 'medium',
    weapon: 'bolter'
  };

  const enemies = [
    {
      type: 'tyranid_warrior',
      faction: 'tyranid',
      scale: 1.8
    }
  ];

  const testActions = [
    {
      type: 'attack',
      entityId: 'player',
      targetId: 'enemy0',
      animName: 'attack_melee',
      effectType: 'melee'
    },
    {
      type: 'attack',
      entityId: 'player',
      targetId: 'enemy0',
      animName: 'attack_shoot',
      effectType: 'ranged'
    },
    {
      type: 'attack',
      entityId: 'enemy0',
      targetId: 'player',
      animName: 'attack_melee',
      effectType: 'melee'
    }
  ];

  const triggerAction = (actionIndex) => {
    const action = testActions[actionIndex];
    setCurrentAction({ ...action, id: actionCounter });
    setActionCounter(actionCounter + 1);
  };

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      <Combat3DView
        playerData={playerData}
        enemies={enemies}
        currentAction={currentAction}
        onAnimationComplete={(action) => {
          console.log('Animation terminée:', action);
        }}
      />

      {/* Contrôles de test */}
      <div style={{
        position: 'absolute',
        top: '50%',
        left: '20px',
        transform: 'translateY(-50%)',
        display: 'flex',
        flexDirection: 'column',
        gap: '15px',
        zIndex: 10
      }}>
        <button
          onClick={() => triggerAction(0)}
          style={{
            background: 'rgba(0, 0, 0, 0.8)',
            border: '2px solid #ff4444',
            color: '#ff4444',
            padding: '12px 20px',
            fontSize: '16px',
            fontFamily: 'Courier New, monospace',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          ⚔️ Attaque Mêlée
        </button>

        <button
          onClick={() => triggerAction(1)}
          style={{
            background: 'rgba(0, 0, 0, 0.8)',
            border: '2px solid #44ff44',
            color: '#44ff44',
            padding: '12px 20px',
            fontSize: '16px',
            fontFamily: 'Courier New, monospace',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          🔫 Tir
        </button>

        <button
          onClick={() => triggerAction(2)}
          style={{
            background: 'rgba(0, 0, 0, 0.8)',
            border: '2px solid #ff44ff',
            color: '#ff44ff',
            padding: '12px 20px',
            fontSize: '16px',
            fontFamily: 'Courier New, monospace',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          👹 Ennemi Attaque
        </button>
      </div>

      {/* Info */}
      <div style={{
        position: 'absolute',
        top: '20px',
        left: '20px',
        color: '#fff',
        fontFamily: 'Courier New, monospace',
        fontSize: '24px',
        fontWeight: 'bold',
        textShadow: '2px 2px 4px #000',
        zIndex: 10
      }}>
        🎮 MOTEUR 3D VOXEL - COMBAT RPG 40K
      </div>

      <div style={{
        position: 'absolute',
        bottom: '80px',
        left: '50%',
        transform: 'translateX(-50%)',
        color: '#00ffff',
        fontFamily: 'Courier New, monospace',
        fontSize: '14px',
        textAlign: 'center',
        textShadow: '1px 1px 2px #000',
        zIndex: 10,
        maxWidth: '600px'
      }}>
        <p>✨ Personnages 3D en voxels générés procéduralement</p>
        <p>🎬 Animations skeletal avec keyframes</p>
        <p>💥 Effets de particules, camera shake et flash</p>
        <p>🏗️ Environnements 3D thématiques</p>
      </div>
    </div>
  );
}
