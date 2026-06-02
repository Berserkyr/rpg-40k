import './InventoryPanel.css';

export default function InventoryPanel({ state }) {
  if (!state) return <div className="panel"><div className="panel-title">INVENTAIRE</div><div className="panel-empty">— HORS LIGNE —</div></div>;

  const inventory = state.inventory || {};
  const items = inventory.items || [];
  const equipped = [inventory.weapon_main, inventory.weapon_secondary, inventory.armor_body, inventory.armor_head].filter(Boolean);

  return (
    <div className="panel inventory-panel">
      <div className="panel-title">◈ INVENTAIRE</div>
      <div className="stat-row">
        <span className="stat-label">CRÉDITS</span>
        <span className="stat-val amber">{inventory.credits ?? 0}</span>
      </div>
      <div className="stat-row">
        <span className="stat-label">CHARGE</span>
        <span className="stat-val">{items.length}/{inventory.max_weight ?? 20}</span>
      </div>

      {equipped.length > 0 && <div className="panel-title small-title">ÉQUIPÉ</div>}
      {equipped.map(item => (
        <div key={`eq-${item.id}`} className="item-row item-equipped">
          <span className="item-name">{item.name}</span>
          <span className="item-type">{item.type}</span>
        </div>
      ))}

      <div className="panel-title small-title">OBJETS</div>
      <div className="items-list">
        {items.length === 0 && <div className="panel-empty">Aucun objet</div>}
        {items.slice(0, 8).map(item => (
          <div key={item.id + item.name} className="item-row">
            <span className="item-name">{item.name}{item.quantity > 1 ? ` x${item.quantity}` : ''}</span>
            <span className={`rarity rarity-${item.rarity}`}>{item.rarity}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
