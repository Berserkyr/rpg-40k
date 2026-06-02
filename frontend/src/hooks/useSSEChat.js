import { useState, useRef, useCallback } from 'react';
import { streamSSE } from '../api';

export function useSSEChat() {
  const [lines, setLines] = useState([]);
  const [streaming, setStreaming] = useState(false);
  const cancelRef = useRef(null);

  const addLine = useCallback((text, type = 'gm') => {
    setLines(prev => [...prev, { text, type, id: Date.now() + Math.random() }]);
  }, []);

  const send = useCallback((path, body, onGameState) => {
    if (streaming) return;
    setStreaming(true);
    let current = '';

    const localId = Date.now();
    setLines(prev => [...prev, { text: '', type: 'gm', id: localId, live: true }]);

    const cancel = streamSSE(
      path,
      body,
      (token) => {
        current += token;
        setLines(prev => prev.map(l => l.id === localId ? { ...l, text: current } : l));
      },
      (data) => {
        setLines(prev => prev.map(l => l.id === localId ? { ...l, live: false } : l));
        setStreaming(false);
        if (onGameState && data.state) onGameState(data.state);
      },
      (error) => {
        const message = error?.message || 'Transmission interrompue';
        setLines(prev => prev.map(l => l.id === localId ? {
          ...l,
          live: false,
          type: 'danger',
          text: `ERREUR VOX: ${message}`,
        } : l));
        setStreaming(false);
      }
    );

    cancelRef.current = cancel;
  }, [streaming]);

  const clear = useCallback(() => setLines([]), []);

  return { lines, streaming, send, addLine, clear };
}
