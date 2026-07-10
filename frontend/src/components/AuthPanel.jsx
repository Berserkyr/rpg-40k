import { useState } from 'react';
import { login, register } from '../api';

export default function AuthPanel({ onAuthenticated }) {
  const [mode, setMode] = useState('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const isRegister = mode === 'register';

  const submit = async (event) => {
    event.preventDefault();
    setError('');
    setBusy(true);
    try {
      const data = isRegister
        ? await register(username, password, displayName)
        : await login(username, password);
      onAuthenticated(data.user);
    } catch (err) {
      setError(err.message || 'Échec de l’authentification.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="auth-screen">
      <h2 className="auth-title">{isRegister ? 'CRÉER UN ACCÈS' : 'AUTHENTIFICATION VOX'}</h2>
      <form className="auth-form" onSubmit={submit} aria-label="Formulaire d’authentification">
        <label className="auth-label" htmlFor="auth-username">IDENTIFIANT</label>
        <input
          id="auth-username"
          className="auth-input"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          autoComplete="username"
          required
          disabled={busy}
          aria-label="Identifiant de connexion"
        />

        {isRegister && (
          <>
            <label className="auth-label" htmlFor="auth-display">NOM AFFICHÉ (optionnel)</label>
            <input
              id="auth-display"
              className="auth-input"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              disabled={busy}
              aria-label="Nom affiché"
            />
          </>
        )}

        <label className="auth-label" htmlFor="auth-password">MOT DE PASSE</label>
        <input
          id="auth-password"
          className="auth-input"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete={isRegister ? 'new-password' : 'current-password'}
          required
          minLength={4}
          disabled={busy}
          aria-label="Mot de passe"
        />

        {error && <p className="auth-error" role="alert">{error}</p>}

        <button className="auth-submit" type="submit" disabled={busy}>
          {busy ? '...' : isRegister ? '[ CRÉER LE COMPTE ]' : '[ SE CONNECTER ]'}
        </button>
      </form>

      <button
        className="auth-switch"
        type="button"
        onClick={() => { setMode(isRegister ? 'login' : 'register'); setError(''); }}
        disabled={busy}
      >
        {isRegister ? 'Déjà un accès ? Se connecter' : 'Pas encore d’accès ? Créer un compte'}
      </button>
    </div>
  );
}
