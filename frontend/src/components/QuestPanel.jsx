import './QuestPanel.css';

export default function QuestPanel({ state }) {
  if (!state) return <div className="panel"><div className="panel-title">MISSIONS</div><div className="panel-empty">— HORS LIGNE —</div></div>;

  const active = state.active_quests || [];
  const available = state.available_quests || [];

  return (
    <div className="panel">
      <div className="panel-title">◈ MISSIONS ({active.length} actives)</div>
      <div className="quest-list">
        {active.map((q) => (
          <div key={q.id} className="quest-item quest-active-item">
            <div className="quest-name">{q.title || q.id}</div>
            {q.description && <div className="quest-desc">{q.description?.slice(0, 80)}…</div>}
            <div className="quest-status-badge quest-active">ACTIF</div>
          </div>
        ))}
        {active.length === 0 && available.length === 0 && (
          <div style={{ color: '#334433', fontSize: '0.7rem' }}>Aucune mission</div>
        )}
        {available.slice(0, 2).map((q) => (
          <div key={q.id} className="quest-item quest-done-item">
            <div className="quest-name" style={{ color: '#446644' }}>{q.title || q.id}</div>
            <div className="quest-status-badge" style={{ color: '#446644' }}>DISPONIBLE</div>
          </div>
        ))}
      </div>
    </div>
  );
}
