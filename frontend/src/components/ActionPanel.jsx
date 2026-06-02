import './ActionPanel.css';

export default function ActionPanel({ state, onRoll, onLoot, onStartCombat, onTravel, onSave, onReset, disabled }) {
  const zones = state?.accessible_zones || [];
  const inCombat = state?.combat?.active;

  return (
    <div className="action-panel" aria-label="Actions principales du jeu">
      <div className="action-group" role="group" aria-label="Commandes rapides">
        <button onClick={onRoll} disabled={disabled} aria-label="Lancer deux dés à six faces">JET 2D6</button>
        <button onClick={onLoot} disabled={disabled || inCombat} aria-label="Fouiller la zone actuelle">FOUILLER</button>
        <button onClick={onStartCombat} disabled={disabled || inCombat} aria-label="Déclencher une rencontre hostile">RENCONTRE</button>
        <button onClick={onSave} disabled={disabled} aria-label="Sauvegarder la partie">SAUVER</button>
        <button onClick={onReset} disabled={disabled} aria-label="Réinitialiser la partie">RESET</button>
      </div>

      <div className="travel-group" role="group" aria-label="Déplacements disponibles">
        <span className="travel-label">DÉPLACEMENT:</span>
        {zones.length === 0 && <span className="travel-empty">aucune sortie</span>}
        {zones.map(zone => (
          <button
            key={zone.id}
            onClick={() => onTravel(zone.id)}
            disabled={disabled || inCombat}
            title={zone.description}
            aria-label={`Se déplacer vers ${zone.name}`}
          >
            {zone.name}
          </button>
        ))}
      </div>
    </div>
  );
}
