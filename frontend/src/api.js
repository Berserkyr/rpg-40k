const BASE = 'http://localhost:8000/api';

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
  const r = await fetch(`${BASE}/state`);
  return parseResponse(r);
}

export async function postAction(path, body = {}) {
  const r = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
