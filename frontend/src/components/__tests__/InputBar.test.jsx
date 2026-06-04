import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';

import InputBar from '../InputBar';

describe('InputBar', () => {
  it('envoie le texte saisi puis vide le champ', async () => {
    const user = userEvent.setup();
    const onSend = vi.fn();

    render(<InputBar onSend={onSend} disabled={false} />);

    const input = screen.getByLabelText('Action libre du joueur');
    await user.type(input, 'Je fouille la coursive');
    await user.click(screen.getByLabelText("Envoyer l'action au maître du jeu"));

    expect(onSend).toHaveBeenCalledWith('Je fouille la coursive');
    expect(input).toHaveValue('');
  });

  it('n’envoie pas de message vide', async () => {
    const user = userEvent.setup();
    const onSend = vi.fn();

    render(<InputBar onSend={onSend} disabled={false} />);
    await user.click(screen.getByLabelText("Envoyer l'action au maître du jeu"));

    expect(onSend).not.toHaveBeenCalled();
  });
});
