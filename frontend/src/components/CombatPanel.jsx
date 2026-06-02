import './CombatPanel.css';

export default function CombatPanel({ combat, onCombatAction, disabled }) {
  if (!combat?.active) {
    return (
      <div className="panel combat-panel">
        <div className="panel-title">◈ COMBAT</div>
        <div className="panel-empty">Aucun contact hostile</div>
      </div>
    );
  }

  const playerPct = Math.max(0, Math.round((combat.player.health / combat.player.max_health) * 100));

  return (
    <div className="panel combat-panel combat-active">
      <div className="panel-title danger-title">◈ COMBAT · TOUR {combat.turn}</div>
      <div className="combatant-row">
        <span>{combat.player.name}</span>
        <span>{combat.player.health}/{combat.player.max_health}</span>
      </div>
      <div className="bar-track combat-bar"><div className="bar-fill" style={{ width: `${playerPct}%`, background: playerPct > 35 ? '#00ff41' : '#ff3333' }} /></div>

      <div className="enemies-list">
        {combat.enemies.map((enemy, i) => {
          const pct = Math.max(0, Math.round((enemy.health / enemy.max_health) * 100));
          return (
            <div key={`${enemy.name}-${i}`} className="enemy-card">
              <div className="combatant-row">
                <span>{enemy.name}</span>
                <span>{enemy.is_dead ? 'MORT' : `${enemy.health}/${enemy.max_health}`}</span>
              </div>
              <div className="bar-track combat-bar"><div className="bar-fill" style={{ width: `${pct}%`, background: enemy.is_dead ? '#333' : '#ff3333' }} /></div>
            </div>
          );
        })}
      </div>

      <div className="combat-actions" role="group" aria-label="Actions de combat">
        <button onClick={() => onCombatAction('attack')} disabled={disabled} aria-label="Attaquer l'ennemi ciblé">ATTAQUER</button>
        <button onClick={() => onCombatAction('defend')} disabled={disabled} aria-label="Se défendre pendant ce tour">DÉFENDRE</button>
        <button onClick={() => onCombatAction('flee')} disabled={disabled} aria-label="Tenter de fuir le combat">FUIR</button>
      </div>
    </div>
  );
}
