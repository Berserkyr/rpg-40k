import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import CharacterPanel from '../CharacterPanel';

describe('CharacterPanel', () => {
  it('affiche un état hors ligne sans données', () => {
    render(<CharacterPanel state={null} />);

    expect(screen.getByText('— HORS LIGNE —')).toBeInTheDocument();
  });

  it('affiche les informations principales du personnage', () => {
    render(
      <CharacterPanel
        state={{
          character: {
            name: 'Karimus',
            role: 'Technicien vox',
            tracks: { blessures: 'Indemne', stress: 2 },
            attributes: { combat: 2, technique: 4 },
            resources: { rations: 1 },
          },
          progression: {
            level: 3,
            current_xp: 40,
            xp_to_next_level: 100,
            skills_unlocked: ['vox'],
          },
        }}
      />
    );

    expect(screen.getByText('Karimus')).toBeInTheDocument();
    expect(screen.getByText('Technicien vox · Niv.3')).toBeInTheDocument();
    expect(screen.getByText('Indemne')).toBeInTheDocument();
    expect(screen.getByText('40/100')).toBeInTheDocument();
  });
});
