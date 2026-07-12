import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';

import CombatPanel from '../CombatPanel';

const activeCombat = {
  active: true,
  turn: 2,
  player: {
    name: 'Karimus', health: 8, max_health: 10,
    action_points: 2, max_action_points: 2, cover: 'aucune',
    is_aiming: false, is_defending: false, conditions: [],
  },
  abilities: [
    { id: 'parade', name: 'Parade', ap_cost: 1, target: 'self', description: 'En garde', icon: '🛡', once_per_combat: true },
  ],
  enemies: [
    { name: 'Guerrier Tyranide', health: 6, max_health: 12, is_dead: false, cover: 'aucune', conditions: [] },
  ],
  allies: [],
};

describe('CombatPanel', () => {
  it('affiche un état hors combat', () => {
    render(<CombatPanel combat={null} />);

    expect(screen.getByText('Aucun contact hostile')).toBeInTheDocument();
  });

  it('affiche le combat actif et déclenche les actions tactiques', async () => {
    const user = userEvent.setup();
    const onCombatAction = vi.fn();

    render(<CombatPanel combat={activeCombat} onCombatAction={onCombatAction} disabled={false} />);

    expect(screen.getByText('◈ COMBAT · TOUR 2')).toBeInTheDocument();
    expect(screen.getByText('Karimus')).toBeInTheDocument();
    expect(screen.getByText('Guerrier Tyranide')).toBeInTheDocument();

    await user.click(screen.getByLabelText('Attaquer la cible sélectionnée'));
    await user.click(screen.getByLabelText('Viser pour un avantage'));
    await user.click(screen.getByLabelText('Se défendre (fin du tour)'));
    await user.click(screen.getByLabelText('Tenter de fuir le combat'));

    expect(onCombatAction).toHaveBeenNthCalledWith(1, 'attack', { target: 0 });
    expect(onCombatAction).toHaveBeenNthCalledWith(2, 'aim', { target: 0 });
    expect(onCombatAction).toHaveBeenNthCalledWith(3, 'defend', { target: 0 });
    expect(onCombatAction).toHaveBeenNthCalledWith(4, 'flee', { target: 0 });
  });

  it('permet d’utiliser une capacité', async () => {
    const user = userEvent.setup();
    const onCombatAction = vi.fn();

    render(<CombatPanel combat={activeCombat} onCombatAction={onCombatAction} disabled={false} />);

    await user.click(screen.getByLabelText('Parade: En garde'));
    expect(onCombatAction).toHaveBeenCalledWith('ability', { target: 0, abilityId: 'parade' });
  });
});
