import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { getCurrentUserId, getState, getToken, login, logout, postAction, setCurrentUserId } from '../api';

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

  it('n’envoie pas d’en-tête Authorization sans jeton', async () => {
    fetch.mockResolvedValueOnce(new Response(JSON.stringify({ ok: true }), { status: 200 }));

    await expect(getState()).resolves.toEqual({ ok: true });

    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/state', {
      headers: {},
    });
  });

  it('stocke le jeton et l’envoie en Bearer après login', async () => {
    fetch.mockResolvedValueOnce(new Response(
      JSON.stringify({ access_token: 'jwt-123', user: { id: 'alpha', role: 'player' } }),
      { status: 200 },
    ));

    await login('alpha', 'secret42');
    expect(getToken()).toBe('jwt-123');

    fetch.mockResolvedValueOnce(new Response(JSON.stringify({ ok: true }), { status: 200 }));
    await getState();

    expect(fetch).toHaveBeenLastCalledWith('http://localhost:8000/api/state', {
      headers: { Authorization: 'Bearer jwt-123' },
    });
  });

  it('supprime le jeton au logout', async () => {
    fetch.mockResolvedValueOnce(new Response(
      JSON.stringify({ access_token: 'jwt-xyz', user: { id: 'beta', role: 'player' } }),
      { status: 200 },
    ));
    await login('beta', 'secret42');
    expect(getToken()).toBe('jwt-xyz');

    logout();
    expect(getToken()).toBe('');
  });

  it('remonte les erreurs API', async () => {
    fetch.mockResolvedValueOnce(new Response(JSON.stringify({ detail: 'Erreur test' }), { status: 400 }));

    await expect(postAction('/save')).rejects.toThrow('Erreur test');
  });
});
