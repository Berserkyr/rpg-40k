import './CharacterPanel.css';

export default function CharacterPanel({ state, onAllocateAttribute }) {
  if (!state) return <div className="panel"><div className="panel-title">PERSONNEL</div><div className="panel-empty">— HORS LIGNE —</div></div>;

  const char = state.character || {};
  const prog = state.progression || {};
  const build = state.character_build || {};
  const tracks = char.tracks || {};
  const attrs = build.effective_attributes || char.attributes || {};
  const baseAttrs = build.base_attributes || char.attributes || {};
  const derived = build.derived_stats || {};
  const resources = char.resources || {};
  const talents = build.talents || [];
  const gifts = build.special_gifts || [];
  const abilities = build.special_abilities || [];

  // Statut de blessure (texte : Indemne, Légère, etc.)
  const blessures = tracks.blessures || 'Indemne';
  const stress = tracks.stress ?? 0;

  // XP bar
  const xpCurrent = prog.current_xp ?? 0;
  const xpNext = prog.xp_to_next_level ?? 100;
  const xpPct = Math.min(100, Math.round((xpCurrent / xpNext) * 100));

  const blessureColor = blessures === 'Indemne' ? '#00ff41'
    : blessures.includes('Critique') ? '#ff3333' : '#ffa500';

  return (
    <div className="panel">
      <div className="panel-title">◈ PERSONNEL</div>
      <div className="char-name">{char.name || 'INCONNU'}</div>
      <div className="char-sub">{char.role} · Niv.{prog.level ?? 1}</div>

      <div className="stat-row">
        <span className="stat-label">ÉTAT</span>
        <span className="stat-val" style={{ color: blessureColor }}>{blessures}</span>
      </div>

      <div className="stat-row">
        <span className="stat-label">STRESS</span>
        <span className="stat-val" style={{ color: stress > 3 ? '#ffa500' : '#556655' }}>{stress}</span>
      </div>

      <div className="stat-row">
        <span className="stat-label">XP</span>
        <div className="bar-track">
          <div className="bar-fill" style={{ width: `${xpPct}%`, background: '#ffa500' }} />
        </div>
        <span className="stat-val amber">{xpCurrent}/{xpNext}</span>
      </div>

      <div className="stat-row">
        <span className="stat-label">COMPÉTENCES</span>
        <span className="stat-val">{prog.skills_unlocked?.length ?? 0}</span>
      </div>

      <div className="stat-row">
        <span className="stat-label">POINTS ATTR.</span>
        <span className="stat-val amber">{prog.attribute_points_available ?? 0}</span>
      </div>

      <div className="panel-title" style={{ marginTop: '0.5rem' }}>STATS DÉRIVÉES</div>
      {Object.entries(derived).map(([k, v]) => (
        <div key={k} className="stat-row">
          <span className="stat-label">{k.toUpperCase()}</span>
          <span className="stat-val amber">{v}</span>
        </div>
      ))}

      <div className="panel-title" style={{ marginTop: '0.5rem' }}>ATTRIBUTS</div>
      {Object.entries(attrs).map(([k, v]) => (
        <div key={k} className="stat-row">
          <span className="stat-label">{k.toUpperCase()}</span>
          <span className="stat-val">{v}{baseAttrs[k] !== undefined && v !== baseAttrs[k] ? ` (${baseAttrs[k]}→${v})` : ''}</span>
          {(prog.attribute_points_available ?? 0) > 0 && onAllocateAttribute && (
            <button
              className="attr-plus-btn"
              onClick={() => onAllocateAttribute(k, 1)}
              aria-label={`Augmenter ${k}`}
              title={`Augmenter ${k}`}
            >
              +
            </button>
          )}
        </div>
      ))}

      {!!talents.length && <div className="panel-title" style={{ marginTop: '0.5rem' }}>TALENTS</div>}
      {talents.map((t) => (
        <div key={t} className="stat-row"><span className="stat-val">• {t}</span></div>
      ))}

      {!!gifts.length && <div className="panel-title" style={{ marginTop: '0.5rem' }}>DONS SPÉCIAUX</div>}
      {gifts.map((g) => (
        <div key={g} className="stat-row"><span className="stat-val amber">✦ {g}</span></div>
      ))}

      {!!abilities.length && <div className="panel-title" style={{ marginTop: '0.5rem' }}>APTITUDES</div>}
      {abilities.slice(0, 5).map((a) => (
        <div key={a} className="stat-row"><span className="stat-val">→ {a}</span></div>
      ))}

      <div className="panel-title" style={{ marginTop: '0.5rem' }}>RESSOURCES</div>
      {Object.entries(resources).map(([k, v]) => (
        <div key={k} className="stat-row">
          <span className="stat-label">{k.toUpperCase()}</span>
          <span className="stat-val amber">{v}</span>
        </div>
      ))}
    </div>
  );
}
