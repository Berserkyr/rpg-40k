import './LevelUpOverlay.css';

/**
 * Overlay animé affiché lors d'une montée de niveau.
 * Se ferme automatiquement (géré par le parent) ou au clic.
 */
export default function LevelUpOverlay({ level, skillPoints, attributePoints, onClose }) {
  return (
    <div
      className="levelup-overlay"
      role="alertdialog"
      aria-label={`Niveau ${level} atteint`}
      onClick={onClose}
    >
      <div className="levelup-burst" aria-hidden="true">
        {Array.from({ length: 12 }).map((_, i) => (
          <span key={i} className="levelup-ray" style={{ '--i': i }} />
        ))}
      </div>
      <div className="levelup-card">
        <div className="levelup-eyebrow">GLOIRE À L'EMPEREUR</div>
        <div className="levelup-title">NIVEAU {level}</div>
        <div className="levelup-sub">ATTEINT</div>
        <div className="levelup-rewards">
          <span>⭐ +{skillPoints ?? 1} point de compétence</span>
          <span>💪 +{attributePoints ?? 1} point d'attribut</span>
        </div>
        <button className="levelup-close" onClick={onClose}>CONTINUER</button>
      </div>
    </div>
  );
}
