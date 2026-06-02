import './ActionPanel.css';

export default function ActionPanel({ state, onRoll, onLoot, onStartCombat, onTravel, onSave, onReset, disabled }) {
  const zones = state?.accessible_zones || [];
  const inCombat = state?.combat?.active;

  return (
    <div className="action-panel">
      <div className="action-group">
        <button onClick={onRoll} disabled={disabled}>JET 2D6</button>
        <button onClick={onLoot} disabled={disabled || inCombat}>FOUILLER</button>
        <button onClick={onStartCombat} disabled={disabled || inCombat}>RENCONTRE</button>
        <button onClick={onSave} disabled={disabled}>SAUVER</button>
        <button onClick={onReset} disabled={disabled}>RESET</button>
      </div>

      <div className="travel-group">
        <span className="travel-label">DÉPLACEMENT:</span>
        {zones.length === 0 && <span className="travel-empty">aucune sortie</span>}
        {zones.map(zone => (
          <button key={zone.id} onClick={() => onTravel(zone.id)} disabled={disabled || inCombat} title={zone.description}>
            {zone.name}
          </button>
        ))}
      </div>
    </div>
  );
}
