import { useEffect, useRef } from 'react';
import './Terminal.css';

const LINE_CLASSES = {
  gm: 'line-gm',
  player: 'line-player',
  system: 'line-system',
  danger: 'line-danger',
  loot: 'line-loot',
};

export default function Terminal({ lines, streaming }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [lines]);

  return (
    <div className="terminal-output">
      {lines.map(line => (
        <div key={line.id} className={`terminal-line ${LINE_CLASSES[line.type] || ''}`}>
          {line.type === 'player' && <span className="prompt">&gt;&gt; </span>}
          {line.type === 'gm' && <span className="prompt gm-prompt">◈ </span>}
          <span className={line.live ? 'typing' : ''}>{line.text}</span>
          {line.live && <span className="cursor">█</span>}
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
