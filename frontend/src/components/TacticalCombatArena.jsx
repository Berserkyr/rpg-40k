import EnemySprite from './EnemySprite';
import './TacticalCombatArena.css';

function healthPercent(value, max) {
  return Math.max(0, Math.min(100, Math.round((value / Math.max(max, 1)) * 100)));
}

function EnemyUnit({ enemy, index, visualAction }) {
  const isTarget = index === visualAction?.targetIndex;
  const isHit = isTarget && visualAction?.kind === 'hit';
  const isDead = enemy.is_dead;

  return (
    <article className={`tactical-unit tactical-enemy ${isTarget ? 'is-targeted' : ''} ${isHit ? 'is-hit' : ''} ${isDead ? 'is-dead' : ''}`}>
      <div className="unit-aura" />
      <div className="unit-threat">MENACE {enemy.threat || 'STANDARD'}</div>
      <div className="enemy-sprite-frame">
        <EnemySprite
          faction={enemy.faction}
          archetype={enemy.archetype}
          threat={enemy.threat}
          name={enemy.name}
          dead={isDead}
          size={96}
          facing="left"
          action={isHit ? 'hurt' : isDead ? 'death' : 'idle'}
          actionSeq={visualAction?.id || 0}
        />
      </div>
      <div className="unit-name">{enemy.name}</div>
      <div className="unit-health" aria-label={`${enemy.name}: ${enemy.health} points de vie sur ${enemy.max_health}`}>
        <span style={{ width: `${healthPercent(enemy.health, enemy.max_health)}%` }} />
      </div>
      <small>{isDead ? 'NEUTRALISÉ' : `${enemy.health} / ${enemy.max_health} PV`}</small>
    </article>
  );
}

export default function TacticalCombatArena({ combat, visualAction }) {
  if (!combat?.active) return null;
  const player = combat.player;
  const enemies = combat.enemies || [];
  const shotActive = visualAction?.kind === 'shot';

  return (
    <section className={`tactical-arena ${shotActive ? 'shot-active' : ''}`} aria-label="Champ de bataille tactique">
      <div className="arena-scanlines" />
      <div className="arena-heading">
        <div>
          <span>THÉÂTRE D’OPÉRATION</span>
          <h2>{combat.zone_name || 'SECTEUR KHARAD-RHO'}</h2>
        </div>
        <div className="turn-counter">TOUR <strong>{combat.turn}</strong></div>
      </div>

      <div className="battlefield">
        <div className="battlefield-grid" />
        <div className="battlefield-smoke smoke-one" />
        <div className="battlefield-smoke smoke-two" />
        <div className="targeting-line" />

        <article className={`tactical-unit tactical-player ${shotActive ? 'is-firing' : ''}`}>
          <div className="unit-aura" />
          <div className="unit-role">OPÉRATEUR</div>
          <div className="marine-portrait" aria-hidden="true">
            <span className="marine-halo" />
            <span className="marine-pack" />
            <span className="marine-shoulder shoulder-left" />
            <span className="marine-shoulder shoulder-right" />
            <span className="marine-head"><i /><b /></span>
            <span className="marine-body"><i /></span>
            <span className="marine-arm arm-left" />
            <span className="marine-arm arm-right"><i /></span>
            <span className="marine-bolter"><i /><b /></span>
          </div>
          <div className="unit-name">{player.name}</div>
          <div className="unit-health player-health" aria-label={`${player.name}: ${player.health} points de vie sur ${player.max_health}`}>
            <span style={{ width: `${healthPercent(player.health, player.max_health)}%` }} />
          </div>
          <small>{player.health} / {player.max_health} PV · {player.action_points}/{player.max_action_points} PA</small>
        </article>

        <div className="enemy-squad">
          {enemies.map((enemy, index) => (
            <EnemyUnit key={`${enemy.name}-${index}`} enemy={enemy} index={index} visualAction={visualAction} />
          ))}
        </div>
      </div>

      <div className="arena-footer">
        <span><i className="status-dot" /> LIAISON TACTIQUE STABLE</span>
        <span>COUVERTURE · {player.cover || 'AUCUNE'}</span>
        <span>{player.is_aiming ? 'VISÉE ACQUISE' : 'ARMEMENT PRÊT'}</span>
      </div>
    </section>
  );
}
