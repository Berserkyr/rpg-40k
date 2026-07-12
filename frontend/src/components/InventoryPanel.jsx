import './InventoryPanel.css';

export default function InventoryPanel({ state, onEquip, onUnequip }) {
  if (!state) return <div className="panel"><div className="panel-title">INVENTAIRE</div><div className="panel-empty">— HORS LIGNE —</div></div>;

  const inventory = state.inventory || {};
  const items = inventory.items || [];
  const slots = [
    { key: 'weapon_main', title: 'MAIN', item: inventory.weapon_main },
    { key: 'weapon_secondary', title: 'SECONDAIRE', item: inventory.weapon_secondary },
    { key: 'armor_body', title: 'TORSO', item: inventory.armor_body },
    { key: 'armor_head', title: 'TÊTE', item: inventory.armor_head },
  ];

  const slotFor = (item) => {
    if (!item) return 'main';
    if (item.type === 'armure') {
      return item.coverage === 'tete' ? 'head' : 'body';
    }
    return 'main';
  };

  const totalWeight = (items || []).reduce((sum, item) => sum + ((item.weight || 0) * (item.quantity || 1)), 0);

  return (
    <div className="panel inventory-panel">
      <div className="panel-title">◈ INVENTAIRE</div>
      <div className="stat-row">
        <span className="stat-label">CRÉDITS</span>
        <span className="stat-val amber">{inventory.credits ?? 0}</span>
      </div>
      <div className="stat-row">
        <span className="stat-label">CHARGE</span>
        <span className="stat-val">{totalWeight.toFixed(1)}/{inventory.max_weight ?? 20} kg</span>
      </div>

      <div className="panel-title small-title">ÉQUIPÉ</div>
      {slots.map((slot) => (
        <div key={slot.key} className="item-row item-equipped">
          <span className="item-name">[{slot.title}] {slot.item?.name || 'vide'}</span>
          <span className="item-type">{slot.item?.type || '-'}</span>
          {slot.item && onUnequip && (
            <button className="item-action" onClick={() => onUnequip(slot.key)} aria-label={`Retirer ${slot.item.name}`}>
              RETIRER
            </button>
          )}
        </div>
      ))}

      <div className="panel-title small-title">OBJETS</div>
      <div className="items-list">
        {items.length === 0 && <div className="panel-empty">Aucun objet</div>}
        {items.map(item => (
          <div key={item.id + item.name} className="item-row">
            <span className="item-name">{item.name}{item.quantity > 1 ? ` x${item.quantity}` : ''}</span>
            <span className={`rarity rarity-${item.rarity}`}>{item.rarity}</span>
            {onEquip && (item.type === 'arme_melee' || item.type === 'arme_distance' || item.type === 'armure') && (
              <button className="item-action" onClick={() => onEquip(item.id, slotFor(item))} aria-label={`Equiper ${item.name}`}>
                ÉQUIPER
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
