const BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api';
const USER_KEY = 'rpg40k.userId';
const TOKEN_KEY = 'rpg40k.token';
const ROLE_KEY = 'rpg40k.role';

export function getCurrentUserId() {
  return localStorage.getItem(USER_KEY) || 'default';
}

export function setCurrentUserId(userId) {
  const normalized = (userId || 'default').trim() || 'default';
  localStorage.setItem(USER_KEY, normalized);
  return normalized;
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || '';
}

export function getRole() {
  return localStorage.getItem(ROLE_KEY) || '';
}

export function isAuthenticated() {
  return Boolean(getToken());
}

function storeSession(data) {
  if (data?.access_token) localStorage.setItem(TOKEN_KEY, data.access_token);
  if (data?.user?.id) localStorage.setItem(USER_KEY, data.user.id);
  if (data?.user?.role) localStorage.setItem(ROLE_KEY, data.user.role);
  return data;
}

export function logout() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(ROLE_KEY);
}

function apiHeaders(extra = {}) {
  const headers = { ...extra };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
}

async function parseResponse(response) {
  const text = await response.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { detail: text || 'Réponse invalide du serveur' };
  }
  if (!response.ok) {
    throw new Error(data?.detail || `Erreur HTTP ${response.status}`);
  }
  return data;
}

export async function getState() {
  const r = await fetch(`${BASE}/state`, { headers: apiHeaders() });
  return parseResponse(r);
}

export async function register(username, password, displayName) {
  const r = await fetch(`${BASE}/auth/register`, {
    method: 'POST',
    headers: apiHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ username, password, display_name: displayName || username }),
  });
  return storeSession(await parseResponse(r));
}

export async function login(username, password) {
  const r = await fetch(`${BASE}/auth/login`, {
    method: 'POST',
    headers: apiHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ username, password }),
  });
  return storeSession(await parseResponse(r));
}

export async function postAction(path, body = {}) {
  const r = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: apiHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(body),
  });
  return parseResponse(r);
}

export function streamSSE(path, body, onToken, onDone, onError) {
  let cancelled = false;

  (async () => {
    try {
      const response = await fetch(`${BASE}${path}`, {
        method: 'POST',
        headers: apiHeaders({ 'Content-Type': 'application/json' }),
        body: JSON.stringify(body),
      });

      if (!response.ok || !response.body) {
        const data = await parseResponse(response);
        throw new Error(data?.detail || 'Flux indisponible');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (!cancelled) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop();

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.type === 'token') onToken(data.content);
              else if (data.type === 'done') onDone(data);
            } catch {}
          }
        }
      }
      if (buffer.trim().startsWith('data: ')) {
        const data = JSON.parse(buffer.trim().slice(6));
        if (data.type === 'done') onDone(data);
      }
    } catch (e) {
      if (!cancelled && onError) onError(e);
    }
  })();

  return () => { cancelled = true; };
}
