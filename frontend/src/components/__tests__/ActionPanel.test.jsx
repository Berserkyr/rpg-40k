import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';

import ActionPanel from '../ActionPanel';

const baseState = {
  combat: null,
  accessible_zones: [
    { id: 'zone-1', name: 'Coursive nord', description: 'Une coursive sombre.' },
  ],
};

describe('ActionPanel', () => {
  it('affiche les commandes principales et déclenche les callbacks', async () => {
    const user = userEvent.setup();
    const handlers = {
      onRoll: vi.fn(),
      onLoot: vi.fn(),
      onStartCombat: vi.fn(),
      onTravel: vi.fn(),
      onSave: vi.fn(),
      onReset: vi.fn(),
    };

    render(<ActionPanel state={baseState} disabled={false} {...handlers} />);

    await user.click(screen.getByLabelText('Lancer deux dés à six faces'));
    await user.click(screen.getByLabelText('Fouiller la zone actuelle'));
    await user.click(screen.getByLabelText('Déclencher une rencontre hostile'));
    await user.click(screen.getByLabelText('Sauvegarder la partie'));
    await user.click(screen.getByLabelText('Réinitialiser la partie'));
    await user.click(screen.getByLabelText('Se déplacer vers Coursive nord'));

    expect(handlers.onRoll).toHaveBeenCalledTimes(1);
    expect(handlers.onLoot).toHaveBeenCalledTimes(1);
    expect(handlers.onStartCombat).toHaveBeenCalledTimes(1);
    expect(handlers.onSave).toHaveBeenCalledTimes(1);
    expect(handlers.onReset).toHaveBeenCalledTimes(1);
    expect(handlers.onTravel).toHaveBeenCalledWith('zone-1');
  });

  it('désactive fouille, rencontre et déplacements pendant un combat', () => {
    render(<ActionPanel state={{ ...baseState, combat: { active: true } }} disabled={false} />);

    expect(screen.getByLabelText('Fouiller la zone actuelle')).toBeDisabled();
    expect(screen.getByLabelText('Déclencher une rencontre hostile')).toBeDisabled();
    expect(screen.getByLabelText('Se déplacer vers Coursive nord')).toBeDisabled();
  });
});
