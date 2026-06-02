import { useState } from 'react';
import './InputBar.css';

export default function InputBar({ onSend, disabled }) {
  const [value, setValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const text = value.trim();
    if (!text || disabled) return;
    setValue('');
    onSend(text);
  };

  return (
    <form className="input-bar" onSubmit={handleSubmit}>
      <span className="input-prompt">&gt;</span>
      <input
        className="input-field"
        value={value}
        onChange={e => setValue(e.target.value)}
        placeholder={disabled ? '...' : 'Que faites-vous, Survivant ?'}
        disabled={disabled}
        autoFocus
      />
      <button className="input-btn" type="submit" disabled={disabled || !value.trim()}>
        ENVOYER
      </button>
    </form>
  );
}
