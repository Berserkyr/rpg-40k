import './SkillsPanel.css';

const CATEGORIES = {
  combat: 'Combat',
  survie: 'Survie',
  social: 'Social',
  technique: 'Technique',
  foi: 'Foi',
  ombre: 'Ombre',
};

export default function SkillsPanel({ state, onLearnSkill, onClose }) {
  const progression = state?.progression || {};
  const build = state?.character_build || {};
  const unlocked = build.skills || [];
  const unlockedIds = new Set(unlocked.map((s) => s.id));

  const allSkills = progression.skill_tree || [];
  const available = progression.available_skills || [];
  const availableIds = new Set(available.map((s) => s.id));

  const grouped = {};
  for (const skill of allSkills) {
    const cat = skill.category || 'autre';
    if (!grouped[cat]) grouped[cat] = [];
    grouped[cat].push(skill);
  }

  return (
    <div className="skills-overlay" role="dialog" aria-label="Panneau des compétences">
      <div className="skills-card">
        <div className="skills-header">
          <h2>🧠 COMPÉTENCES, TALENTS ET DONS</h2>
          <button className="skills-close" onClick={onClose} aria-label="Fermer le panneau compétences">✕</button>
        </div>

        <div className="skills-meta">
          <span>Niveau: {progression.level ?? 1}</span>
          <span>XP: {progression.current_xp ?? 0}</span>
          <span>Points attribut: {progression.attribute_points_available ?? 0}</span>
        </div>

        <div className="skills-grid">
          {Object.entries(grouped).map(([cat, skills]) => (
            <section key={cat} className="skills-group">
              <h3>{CATEGORIES[cat] || cat.toUpperCase()}</h3>
              {skills.map((skill) => {
                const isUnlocked = unlockedIds.has(skill.id);
                const canLearn = availableIds.has(skill.id);
                return (
                  <div key={skill.id} className={`skill-row ${isUnlocked ? 'unlocked' : ''}`}>
                    <div className="skill-main">
                      <div className="skill-name">{skill.name}</div>
                      <div className="skill-desc">{skill.description}</div>
                    </div>
                    <div className="skill-side">
                      <div className="skill-cost">Niv {skill.level_required} · {skill.xp_cost} XP</div>
                      {isUnlocked ? (
                        <span className="skill-badge">ACQUIS</span>
                      ) : canLearn ? (
                        <button onClick={() => onLearnSkill(skill.id)} className="skill-btn">APPRENDRE</button>
                      ) : (
                        <span className="skill-locked">VERROUILLÉ</span>
                      )}
                    </div>
                  </div>
                );
              })}
            </section>
          ))}
        </div>
      </div>
    </div>
  );
}
