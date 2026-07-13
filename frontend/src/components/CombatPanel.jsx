import { useState, useEffect, useRef } from 'react';
import './CombatPanel.css';
import EnemySprite from './EnemySprite';
import AnimatedAction from './AnimatedAction';

function ConditionChips({ conditions }) {
  if (!conditions?.length) return null;
  return (
    <div className="condition-chips">
      {conditions.map((c) => (
        <span key={c.id} className="condition-chip" title={`${c.label} (${c.turns} tour${c.turns > 1 ? 's' : ''})`}>
          {c.icon} {c.turns}
        </span>
      ))}
    </div>
  );
}

function HealthBar({ value, max, dead }) {
  const pct = Math.max(0, Math.round((value / Math.max(1, max)) * 100));
  const color = dead ? '#333' : pct > 35 ? '#00ff41' : '#ff3333';
  return (
    <div className="bar-track combat-bar">
      <div className="bar-fill" style={{ width: `${dead ? 100 : pct}%`, background: color }} />
    </div>
  );
}

export default function CombatPanel({ combat, onCombatAction, onNegotiate, disabled }) {
  const [target, setTarget] = useState(0);
  // Effets d'animation par ennemi ({action, seq}) et pour le joueur.
  const [enemyFx, setEnemyFx] = useState([]);
  const prevRef = useRef(null);

  // Detecte les changements d'etat pour declencher les animations de combat.
  useEffect(() => {
    const enemiesNow = combat?.enemies || [];
    const playerNow = combat?.player;
    const prev = prevRef.current;
    if (prev) {
      // Touche / mort des ennemis.
      setEnemyFx((old) => enemiesNow.map((e, i) => {
        const po = prev.enemies[i];
        const cur = old[i] || { action: 'idle', seq: 0 };
        if (!po) return cur;
        if (e.is_dead && !po.is_dead) return { action: 'death', seq: cur.seq + 1 };
        if (!e.is_dead && e.health < po.health) return { action: 'hurt', seq: cur.seq + 1 };
        return cur;
      }));
      // Le joueur a encaisse -> les ennemis vivants bondissent (attaque).
      if (playerNow && prev.player && playerNow.health < prev.player.health) {
        setEnemyFx((old) => enemiesNow.map((e, i) => {
          const cur = old[i] || { action: 'idle', seq: 0 };
          if (e.is_dead || cur.action === 'hurt' || cur.action === 'death') return cur;
          return { action: 'attack', seq: cur.seq + 1 };
        }));
      }
    }
    prevRef.current = {
      enemies: enemiesNow.map((e) => ({ health: e.health, is_dead: e.is_dead })),
      player: playerNow ? { health: playerNow.health } : null,
    };
  }, [combat]);

  if (!combat?.active) {
    return (
      <div className="panel combat-panel">
        <div className="panel-title">◈ COMBAT</div>
        <div className="panel-empty">Aucun contact hostile</div>
      </div>
    );
  }

  const player = combat.player;
  const ap = player.action_points ?? 0;
  const maxAp = player.max_action_points ?? 2;
  const abilities = combat.abilities || [];
  const enemies = combat.enemies || [];
  const livingEnemyIndexes = enemies.map((e, i) => (e.is_dead ? -1 : i)).filter((i) => i >= 0);
  const safeTarget = livingEnemyIndexes.includes(target) ? target : (livingEnemyIndexes[0] ?? 0);

  const act = (command, opts = {}) => onCombatAction(command, { target: safeTarget, ...opts });
  const negotiate = (approach) => onNegotiate?.(approach, safeTarget);

  return (
    <div className="panel combat-panel combat-active">
      <div className="panel-title danger-title">◈ COMBAT · TOUR {combat.turn}</div>

      <div className="ap-row" aria-label={`Points d'action: ${ap} sur ${maxAp}`}>
        <span className="ap-label">PA</span>
        {Array.from({ length: maxAp }).map((_, i) => (
          <span key={`ap-slot-${i}`} className={`ap-dot ${i < ap ? 'ap-on' : 'ap-off'}`} />
        ))}
      </div>

      <div className="combatant-row player-row">
        <span>
          {player.name}
          {player.is_aiming && <span className="stance-tag" title="En visée">🎯</span>}
          {player.cover && player.cover !== 'aucune' && <span className="stance-tag" title={`Couvert: ${player.cover}`}>🧱</span>}
        </span>
        <span>{player.health}/{player.max_health}</span>
      </div>
      <HealthBar value={player.health} max={player.max_health} />
      <ConditionChips conditions={player.conditions} />

      <div className="enemies-list">
        {enemies.map((enemy, i) => (
          <button
            type="button"
            key={`${enemy.name}-${i}`}
            className={`enemy-card ${i === safeTarget && !enemy.is_dead ? 'enemy-targeted' : ''} ${enemy.is_dead ? 'enemy-dead' : ''}`}
            onClick={() => !enemy.is_dead && setTarget(i)}
            disabled={enemy.is_dead}
            aria-label={`Cibler ${enemy.name}`}
            aria-pressed={i === safeTarget}
          >
            <div className="enemy-card-body">
              <AnimatedAction
                skillId={enemyFx[i]?.action || 'idle'}
                trigger={enemyFx[i]?.seq || 0}
                facing={i % 2 === 0 ? 'right' : 'left'}
                onComplete={() => {
                  if (enemyFx[i]?.action !== 'idle' && enemyFx[i]?.action !== 'death') {
                    setEnemyFx(old => {
                      const newFx = [...old];
                      newFx[i] = { action: 'idle', seq: newFx[i]?.seq || 0 };
                      return newFx;
                    });
                  }
                }}
              >
                <EnemySprite
                  faction={enemy.faction}
                  archetype={enemy.archetype}
                  threat={enemy.threat}
                  name={enemy.name}
                  dead={enemy.is_dead}
                  size={44}
                />
              </AnimatedAction>
              <div className="enemy-card-info">
                <div className="combatant-row">
                  <span>
                    {i === safeTarget && !enemy.is_dead && <span className="target-marker">▸</span>} {enemy.name}
                    {enemy.cover && enemy.cover !== 'aucune' && <span className="stance-tag" title={`Couvert: ${enemy.cover}`}>🧱</span>}
                  </span>
                  <span>{enemy.is_dead ? 'MORT' : `${enemy.health}/${enemy.max_health}`}</span>
                </div>
                <HealthBar value={enemy.health} max={enemy.max_health} dead={enemy.is_dead} />
                <ConditionChips conditions={enemy.conditions} />
              </div>
            </div>
          </button>
        ))}
      </div>

      {combat.allies?.length > 0 && (
        <div className="allies-list">
          <div className="allies-title">ALLIÉS</div>
          {combat.allies.map((ally, i) => (
            <div key={`${ally.name}-${i}`} className="ally-card">
              <div className="combatant-row">
                <span>{ally.name}</span>
                <span>{ally.is_dead ? 'MORT' : `${ally.health}/${ally.max_health}`}</span>
              </div>
              <HealthBar value={ally.health} max={ally.max_health} dead={ally.is_dead} />
            </div>
          ))}
        </div>
      )}

      <div className="combat-actions" role="group" aria-label="Actions de combat">
        <button onClick={() => act('attack')} disabled={disabled || ap < 1} aria-label="Attaquer la cible sélectionnée" title="1 PA">⚔ ATTAQUER</button>
        <button onClick={() => act('aim')} disabled={disabled || ap < 1} aria-label="Viser pour un avantage" title="1 PA · avantage à la prochaine attaque">🎯 VISER</button>
        <button onClick={() => act('cover')} disabled={disabled || ap < 1} aria-label="Se mettre à couvert" title="1 PA · +défense">🧱 COUVERT</button>
        <button onClick={() => act('defend')} disabled={disabled} aria-label="Se défendre (fin du tour)" title="Termine le tour · +défense">🛡 DÉFENDRE</button>
        <button onClick={() => act('flee')} disabled={disabled} aria-label="Tenter de fuir le combat">🏃 FUIR</button>
      </div>

      {abilities.length > 0 && (
        <div className="combat-abilities">
          <div className="abilities-title">CAPACITÉS</div>
          <div className="abilities-grid">
            {abilities.map((ab) => (
              <button
                key={ab.id}
                className="ability-btn"
                onClick={() => act('ability', { abilityId: ab.id })}
                disabled={disabled || ap < ab.ap_cost}
                title={`${ab.description} (${ab.ap_cost} PA${ab.once_per_combat ? ' · 1×/combat' : ''})`}
                aria-label={`${ab.name}: ${ab.description}`}
              >
                <span className="ability-icon">{ab.icon}</span>
                <span className="ability-name">{ab.name}</span>
                <span className="ability-cost">{ab.ap_cost}PA</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {onNegotiate && (
        <div className="combat-negotiate">
          <div className="abilities-title">DIALOGUE</div>
          {combat.negotiable ? (
            <div className="negotiate-grid" role="group" aria-label="Options de négociation">
              <button
                className="negotiate-btn"
                onClick={() => negotiate('persuasion')}
                disabled={disabled}
                title="Convaincre par la raison (solidarité). Peut rallier un ennemi."
              >
                🕊 PERSUADER
              </button>
              <button
                className="negotiate-btn"
                onClick={() => negotiate('intimidation')}
                disabled={disabled}
                title="Forcer le repli par la peur (sang-froid). Efficace sur les faibles."
              >
                😠 INTIMIDER
              </button>
              <button
                className="negotiate-btn"
                onClick={() => negotiate('marchandage')}
                disabled={disabled}
                title="Proposer un échange (ingéniosité)."
              >
                💰 MARCHANDER
              </button>
            </div>
          ) : (
            <div className="negotiate-impossible">Cet adversaire ne connaît pas le dialogue.</div>
          )}
        </div>
      )}
    </div>
  );
}
