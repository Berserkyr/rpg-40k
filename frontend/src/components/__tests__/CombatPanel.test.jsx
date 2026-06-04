import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';

import CombatPanel from '../CombatPanel';

const activeCombat = {
  active: true,
  turn: 2,
  player: { name: 'Karimus', health: 8, max_health: 10 },
  enemies: [
    { name: 'Guerrier Tyranide', health: 6, max_health: 12, is_dead: false },
  ],
};

describe('CombatPanel', () => {
  it('affiche un état hors combat', () => {
    render(<CombatPanel combat={null} />);

    expect(screen.getByText('Aucun contact hostile')).toBeInTheDocument();
  });

  it('affiche le combat actif et déclenche les actions', async () => {
    const user = userEvent.setup();
    const onCombatAction = vi.fn();

    render(<CombatPanel combat={activeCombat} onCombatAction={onCombatAction} disabled={false} />);

    expect(screen.getByText('◈ COMBAT · TOUR 2')).toBeInTheDocument();
    expect(screen.getByText('Karimus')).toBeInTheDocument();
    expect(screen.getByText('Guerrier Tyranide')).toBeInTheDocument();

    await user.click(screen.getByLabelText("Attaquer l'ennemi ciblé"));
    await user.click(screen.getByLabelText('Se défendre pendant ce tour'));
    await user.click(screen.getByLabelText('Tenter de fuir le combat'));

    expect(onCombatAction).toHaveBeenNthCalledWith(1, 'attack');
    expect(onCombatAction).toHaveBeenNthCalledWith(2, 'defend');
    expect(onCombatAction).toHaveBeenNthCalledWith(3, 'flee');
  });
});
