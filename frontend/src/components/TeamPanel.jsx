import './TeamPanel.css';

const ARCHETYPE_ICON = {
  milicien: '🪖',
  eclaireur: '🥷',
  sororitas: '⚔',
  tech_pretre: '🔧',
};

function StatLine({ c }) {
  return (
    <div className="team-stats">
      <span title="Combat">⚔ {c.combat}</span>
      <span title="Défense">🛡 {c.defense}</span>
      <span title="Vitesse">💨 {c.speed}</span>
      <span title="Spécial">✨ {c.special}</span>
      <span title="PV max">❤ {c.max_health}</span>
    </div>
  );
}

export default function TeamPanel({ state, onRecruit, onDismiss, onClose, disabled }) {
  const team = state?.team || {};
  const members = team.members || [];
  const available = team.available || [];
  const maxSize = team.max_size ?? 3;
  const full = members.length >= maxSize;

  return (
    <div className="team-overlay" role="dialog" aria-label="Panneau d'équipe">
      <div className="team-card">
        <div className="team-header">
          <h2>👥 GESTION D'ÉQUIPE ({members.length}/{maxSize})</h2>
          <button className="team-close" onClick={onClose} aria-label="Fermer le panneau équipe">✕</button>
        </div>

        <section className="team-section">
          <h3>Compagnons actifs</h3>
          {members.length === 0 ? (
            <div className="team-empty">Aucun compagnon. Recrutez des alliés ci-dessous.</div>
          ) : (
            members.map((m) => (
              <div key={m.id} className="team-member">
                <div className="team-member-main">
                  <span className="team-name">{ARCHETYPE_ICON[m.archetype] || '•'} {m.name}</span>
                  <StatLine c={m} />
                </div>
                <button
                  className="team-btn danger"
                  onClick={() => onDismiss(m.id)}
                  disabled={disabled}
                  aria-label={`Renvoyer ${m.name}`}
                >
                  RENVOYER
                </button>
              </div>
            ))
          )}
        </section>

        <section className="team-section">
          <h3>Recrutement</h3>
          {available.map((t) => {
            const already = members.some((m) => m.id === t.id);
            const canRecruit = t.unlocked && !already && !full;
            return (
              <div key={t.id} className={`team-member ${t.unlocked ? '' : 'locked'}`}>
                <div className="team-member-main">
                  <span className="team-name">{ARCHETYPE_ICON[t.archetype] || '•'} {t.name}</span>
                  <StatLine c={t} />
                </div>
                {already ? (
                  <span className="team-badge">DANS L'ÉQUIPE</span>
                ) : t.unlocked ? (
                  <button
                    className="team-btn"
                    onClick={() => onRecruit(t.id)}
                    disabled={disabled || !canRecruit}
                    aria-label={`Recruter ${t.name}`}
                    title={full ? 'Équipe complète' : ''}
                  >
                    RECRUTER
                  </button>
                ) : (
                  <span className="team-locked">NIV {t.level_required}</span>
                )}
              </div>
            );
          })}
        </section>
      </div>
    </div>
  );
}
