import './MapPanel.css';

const THREAT_ICONS = ['◉', '◈', '◆', '▲', '☠'];

const threatIcon = (level) => THREAT_ICONS[Math.min(4, Math.max(0, (level ?? 1) - 1))];
export default function MapPanel({ state }) {
  if (!state) return <div className="panel"><div className="panel-title">CARTE</div><div className="panel-empty">— HORS LIGNE —</div></div>;

  const currentZone = state.current_zone || {};
  const accessible = state.accessible_zones || [];
  const worldMap = state.world_map || {};
  const travelHistory = worldMap.travel_history || [];
  const zonesById = worldMap.zones || {};

  return (
    <div className="panel">
      <div className="panel-title">◈ SECTEUR 7 — CARTE</div>
      <div className="current-zone">
        <span className="zone-label">POSITION:</span>
        <span className="zone-name">{currentZone.name || '?'}</span>
      </div>
      {currentZone.description && (
        <div style={{ color: '#334433', fontSize: '0.65rem', marginBottom: '0.4rem', lineHeight: 1.4 }}>
          {currentZone.description?.slice(0, 100)}…
        </div>
      )}
      <div className="panel-title" style={{ marginTop: '0.3rem' }}>ZONES ACCESSIBLES</div>
      <div className="zones-list">
        {accessible.length === 0 && (
          <div className="zone-row" style={{ color: '#334433' }}>Aucune zone accessible</div>
        )}
        {accessible.map((zone) => {
          const icon = threatIcon(zone.threat_level);
          return (
            <div key={zone.id} className="zone-row">
              <span className="zone-icon">{icon}</span>
              <span className="zone-id">{zone.name || zone.id}</span>
            </div>
          );
        })}
      </div>

      <div className="panel-title" style={{ marginTop: '0.4rem' }}>TRACE DE DÉPLACEMENT</div>
      <div className="zones-list">
        {travelHistory.length === 0 && <div className="zone-row" style={{ color: '#334433' }}>Aucun déplacement</div>}
        {travelHistory.slice(-10).map((zoneId, idx, arr) => {
          const zone = zonesById[zoneId];
          const isHere = idx === arr.length - 1;
          return (
            <div key={`${zoneId}-${idx}`} className={`zone-row ${isHere ? 'zone-current' : ''}`}>
              <span className="zone-icon">{isHere ? '⦿' : '•'}</span>
              <span className="zone-id">{zone?.name || zoneId}</span>
              {isHere && <span className="zone-here">ICI</span>}
            </div>
          );
        })}
      </div>
    </div>
  );
}
