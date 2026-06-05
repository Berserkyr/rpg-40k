const BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api';
const USER_KEY = 'rpg40k.userId';

export function getCurrentUserId() {
  return localStorage.getItem(USER_KEY) || 'default';
}

export function setCurrentUserId(userId) {
  const normalized = (userId || 'default').trim() || 'default';
  localStorage.setItem(USER_KEY, normalized);
  return normalized;
}

function apiHeaders(extra = {}) {
  return {
    'X-User-Id': getCurrentUserId(),
    ...extra,
  };
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

export async function createUser(userId, displayName = userId) {
  const r = await fetch(`${BASE}/users`, {
    method: 'POST',
    headers: apiHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ user_id: userId, display_name: displayName }),
  });
  return parseResponse(r);
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
