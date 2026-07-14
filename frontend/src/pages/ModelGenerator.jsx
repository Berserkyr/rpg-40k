import React, { useState, useEffect } from 'react';
import './ModelGenerator.css';
import { login as apiLogin, logout as apiLogout, getRole, isAuthenticated, generateModels } from '../api.js';

const FACTIONS = ['Imperial', 'Chaos', 'Tyranid', 'Ork', 'Eldar', 'Tau', 'Necron'];
const MODEL_TYPES = ['character', 'weapon', 'vehicle', 'structure', 'creature'];
const COMPLEXITIES = ['simple', 'medium', 'high'];

const FACTION_DESCRIPTIONS = {
  Imperial: 'Humains: Space Marines, Garde Impériale, Adeptus Mechanicus',
  Chaos: 'Forces du Chaos: Marines renégats, démons, cultistes',
  Tyranid: 'Xenos biologiques: Créatures alien, biomorphes',
  Ork: 'Peaux-vertes: Guerriers, véhicules bricolés',
  Eldar: 'Aliens élégants: Aspect Warriors, technologie avancée',
  Tau: 'Empire Tau: Méchas, drones, Fire Warriors',
  Necron: 'Robots immortels: Squelettes métalliques, armes nécroniques'
};

export default function ModelGenerator() {
  const [faction, setFaction] = useState('Imperial');
  const [selectedTypes, setSelectedTypes] = useState(['character', 'weapon']);
  const [count, setCount] = useState(5);
  const [complexity, setComplexity] = useState('medium');
  const [generating, setGenerating] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // Vérifier si déjà connecté en tant qu'admin
  useEffect(() => {
    if (isAuthenticated() && getRole() === 'admin') {
      setIsLoggedIn(true);
    }
  }, []);

  const toggleType = (type) => {
    setSelectedTypes(prev =>
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const data = await apiLogin(username, password);
      if (data?.user?.role !== 'admin') {
        apiLogout();
        throw new Error('Ce compte n\u2019est pas administrateur.');
      }
      setIsLoggedIn(true);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleGenerate = async () => {
    if (selectedTypes.length === 0) {
      setError('Sélectionnez au moins un type de modèle');
      return;
    }

    setGenerating(true);
    setError(null);
    setResult(null);

    try {
      const data = await generateModels({
        modelTypes: selectedTypes,
        faction,
        count,
        complexity,
      });
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setGenerating(false);
    }
  };

  // Formulaire de connexion si pas connecté
  if (!isLoggedIn) {
    return (
      <div className="model-generator">
        <div className="generator-header">
          <h1>🎨 Générateur de Modèles 3D IA</h1>
          <p className="subtitle">Connexion admin requise</p>
        </div>

        <div className="login-panel">
          <form onSubmit={handleLogin} className="login-form">
            <h2>🔐 Connexion Administrateur</h2>
            
            {error && <div className="error-box"><p>{error}</p></div>}
            
            <div className="form-group">
              <label>Nom d'utilisateur</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="admin"
                required
              />
            </div>

            <div className="form-group">
              <label>Mot de passe</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="admin123"
                required
              />
            </div>

            <button type="submit" className="login-btn">
              Se connecter
            </button>

            <div className="login-hint">
              <p>💡 <strong>Compte par défaut:</strong></p>
              <code>admin / admin123</code>
            </div>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="model-generator">
      <div className="generator-header">
        <h1>🎨 Générateur de Modèles 3D IA</h1>
        <p className="subtitle">Créez automatiquement des bibliothèques de voxels Warhammer 40K avec GPT</p>
        <button 
          className="logout-btn"
          onClick={() => {
            apiLogout();
            setIsLoggedIn(false);
          }}
        >
          Déconnexion
        </button>
      </div>

      <div className="generator-content">
        <div className="generator-panel">
          <section className="config-section">
            <h2>📦 Faction</h2>
            <div className="faction-grid">
              {FACTIONS.map(f => (
                <button
                  key={f}
                  className={`faction-btn ${faction === f ? 'active' : ''}`}
                  onClick={() => setFaction(f)}
                  title={FACTION_DESCRIPTIONS[f]}
                >
                  {f}
                </button>
              ))}
            </div>
            <p className="faction-desc">{FACTION_DESCRIPTIONS[faction]}</p>
          </section>

          <section className="config-section">
            <h2>🎯 Types de Modèles</h2>
            <div className="types-grid">
              {MODEL_TYPES.map(type => (
                <button
                  key={type}
                  className={`type-btn ${selectedTypes.includes(type) ? 'active' : ''}`}
                  onClick={() => toggleType(type)}
                >
                  {type === 'character' && '👤'}
                  {type === 'weapon' && '⚔️'}
                  {type === 'vehicle' && '🚜'}
                  {type === 'structure' && '🏛️'}
                  {type === 'creature' && '🐉'}
                  <span>{type}</span>
                </button>
              ))}
            </div>
          </section>

          <section className="config-section">
            <h2>⚙️ Paramètres</h2>
            <div className="params-grid">
              <div className="param">
                <label>Nombre de modèles</label>
                <input
                  type="range"
                  min="1"
                  max="20"
                  value={count}
                  onChange={(e) => setCount(parseInt(e.target.value))}
                />
                <span className="param-value">{count}</span>
              </div>

              <div className="param">
                <label>Complexité</label>
                <div className="complexity-btns">
                  {COMPLEXITIES.map(c => (
                    <button
                      key={c}
                      className={`complexity-btn ${complexity === c ? 'active' : ''}`}
                      onClick={() => setComplexity(c)}
                    >
                      {c}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </section>

          <button
            className="generate-btn"
            onClick={handleGenerate}
            disabled={generating || selectedTypes.length === 0}
          >
            {generating ? (
              <>
                <span className="spinner"></span>
                Génération en cours...
              </>
            ) : (
              <>
                🚀 Générer {count} modèle{count > 1 ? 's' : ''}
              </>
            )}
          </button>
        </div>

        <div className="result-panel">
          {generating && (
            <div className="generating-info">
              <div className="ai-visual">
                <div className="ai-icon">🤖</div>
                <div className="ai-waves">
                  <div className="wave"></div>
                  <div className="wave"></div>
                  <div className="wave"></div>
                </div>
              </div>
              <p>GPT génère du code JavaScript...</p>
              <p className="small">Création de modèles voxel {faction}</p>
            </div>
          )}

          {error && (
            <div className="error-box">
              <h3>❌ Erreur</h3>
              <p>{error}</p>
            </div>
          )}

          {result && (
            <div className="success-box">
              <h3>✅ {result.message}</h3>
              <p className="file-path">📁 {result.file}</p>
              
              <div className="code-preview">
                <h4>Aperçu du code généré:</h4>
                <pre>{result.preview}</pre>
              </div>

              <div className="next-steps">
                <h4>🎯 Prochaines étapes:</h4>
                <ol>
                  <li>Les fonctions sont maintenant dans <code>GeneratedModels.js</code></li>
                  <li>Importez-les: <code>import {'{ buildModelName }'} from './GeneratedModels.js'</code></li>
                  <li>Utilisez-les: <code>const model = buildModelName(scale)</code></li>
                  <li>Testez sur <a href="/combat3d">/combat3d</a></li>
                </ol>
              </div>
            </div>
          )}

          {!generating && !error && !result && (
            <div className="placeholder">
              <div className="placeholder-icon">📚</div>
              <p>Configurez les paramètres et lancez la génération</p>
              <div className="info-cards">
                <div className="info-card">
                  <strong>Simple</strong>
                  <span>50-150 voxels</span>
                </div>
                <div className="info-card">
                  <strong>Medium</strong>
                  <span>150-400 voxels</span>
                </div>
                <div className="info-card">
                  <strong>High</strong>
                  <span>400-1000 voxels</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
