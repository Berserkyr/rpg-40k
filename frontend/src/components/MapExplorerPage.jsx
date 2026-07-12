import './MapExplorerPage.css';

const THREAT_ICONS = ['◉', '◈', '◆', '▲', '☠'];
const threatIcon = (level) => THREAT_ICONS[Math.min(4, Math.max(0, (level ?? 1) - 1))];

export default function MapExplorerPage({ state, onTravel, onClose, disabled }) {
  const worldMap = state?.world_map || {};
  const zonesById = worldMap.zones || {};
  const currentZoneId = worldMap.current_zone_id || '';
  const discovered = worldMap.discovered_zones || [];
  const travelHistory = worldMap.travel_history || [];
  const currentZone = zonesById[currentZoneId] || state?.current_zone || null;
  const accessible = state?.accessible_zones || [];
  const accessibleIds = new Set(accessible.map((z) => z.id));

  const knownZones = discovered
    .map((zoneId) => zonesById[zoneId])
    .filter(Boolean);

  const possibleNotTaken = knownZones.filter((zone) => {
    if (!zone?.connections?.length) return false;
    return zone.connections.some((connId) => {
      const destinationKnown = !!zonesById[connId];
      const visited = travelHistory.includes(connId);
      return destinationKnown && !visited;
    });
  });

  return (
    <div className="map-page-overlay" role="dialog" aria-label="Carte d'exploration">
      <div className="map-page-card">
        <div className="map-page-header">
          <h2>🗺 CARTE D'EXPLORATION DYNAMIQUE</h2>
          <button className="map-page-close" onClick={onClose} aria-label="Fermer la carte">✕</button>
        </div>

        <div className="map-page-grid">
          <section className="map-block">
            <h3>POSITION ACTUELLE</h3>
            {currentZone ? (
              <div className="map-current-zone">
                <div className="map-zone-title">{currentZone.name}</div>
                <div className="map-zone-desc">{currentZone.description}</div>
                <div className="map-zone-meta">Danger: {threatIcon(currentZone.threat_level)} · Type: {currentZone.zone_type}</div>
              </div>
            ) : (
              <div className="map-empty">Position inconnue</div>
            )}

            <h3>CHEMINS POSSIBLES (NON EMPRUNTÉS)</h3>
            <div className="map-list">
              {possibleNotTaken.length === 0 && <div className="map-empty">Aucun nouveau chemin identifié</div>}
              {possibleNotTaken.map((zone) => (
                <div key={`untaken-${zone.id}`} className="map-row">
                  <span>{zone.name}</span>
                  <span className="map-muted">exploré, sorties non visitées</span>
                </div>
              ))}
            </div>
          </section>

          <section className="map-block">
            <h3>ZONES EXPLORÉES</h3>
            <div className="map-list">
              {knownZones.length === 0 && <div className="map-empty">Aucune zone découverte</div>}
              {knownZones.map((zone) => {
                const isCurrent = zone.id === currentZoneId;
                const canGo = accessibleIds.has(zone.id);
                return (
                  <div key={zone.id} className={`map-row ${isCurrent ? 'current' : ''}`}>
                    <span>{threatIcon(zone.threat_level)} {zone.name}</span>
                    <div className="map-actions">
                      {isCurrent && <span className="badge-here">ICI</span>}
                      {!isCurrent && canGo && (
                        <button onClick={() => onTravel(zone.id)} disabled={disabled}>Y ALLER</button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </section>

          <section className="map-block full-width">
            <h3>TRACE D'EXPLORATION</h3>
            <div className="map-trace">
              {travelHistory.length === 0 && <div className="map-empty">Aucun déplacement</div>}
              {travelHistory.map((zoneId, idx) => {
                const zone = zonesById[zoneId];
                const isLast = idx === travelHistory.length - 1;
                return (
                  <div key={`${zoneId}-${idx}`} className="map-trace-node">
                    <span className="dot">{isLast ? '⦿' : '•'}</span>
                    <span>{zone?.name || zoneId}</span>
                    {isLast && <span className="badge-here">POSITION</span>}
                  </div>
                );
              })}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
