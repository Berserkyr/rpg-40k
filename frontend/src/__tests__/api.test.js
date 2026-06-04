import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { createUser, getCurrentUserId, getState, postAction, setCurrentUserId } from '../api';

describe('api client', () => {
  beforeEach(() => {
    localStorage.clear();
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('gère l’identifiant utilisateur courant', () => {
    expect(getCurrentUserId()).toBe('default');
    expect(setCurrentUserId(' Karimus ')).toBe('Karimus');
    expect(getCurrentUserId()).toBe('Karimus');
  });

  it('envoie X-User-Id sur getState', async () => {
    setCurrentUserId('joueur-api');
    fetch.mockResolvedValueOnce(new Response(JSON.stringify({ ok: true }), { status: 200 }));

    await expect(getState()).resolves.toEqual({ ok: true });

    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/state', {
      headers: { 'X-User-Id': 'joueur-api' },
    });
  });

  it('crée un utilisateur via l’API', async () => {
    fetch.mockResolvedValueOnce(new Response(JSON.stringify({ user: { id: 'alpha' } }), { status: 200 }));

    await expect(createUser('alpha', 'Alpha')).resolves.toEqual({ user: { id: 'alpha' } });

    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/users', expect.objectContaining({
      method: 'POST',
      headers: expect.objectContaining({ 'Content-Type': 'application/json', 'X-User-Id': 'default' }),
      body: JSON.stringify({ user_id: 'alpha', display_name: 'Alpha' }),
    }));
  });

  it('remonte les erreurs API', async () => {
    fetch.mockResolvedValueOnce(new Response(JSON.stringify({ detail: 'Erreur test' }), { status: 400 }));

    await expect(postAction('/save')).rejects.toThrow('Erreur test');
  });
});
