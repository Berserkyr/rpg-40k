import { useState, useEffect, useCallback } from 'react';
import Terminal from './components/Terminal';
import InputBar from './components/InputBar';
import CharacterPanel from './components/CharacterPanel';
import MapPanel from './components/MapPanel';
import QuestPanel from './components/QuestPanel';
import InventoryPanel from './components/InventoryPanel';
import CombatPanel from './components/CombatPanel';
import ActionPanel from './components/ActionPanel';
import AuthPanel from './components/AuthPanel';
import MapExplorerPage from './components/MapExplorerPage';
import SkillsPanel from './components/SkillsPanel';
import { useSSEChat } from './hooks/useSSEChat';
import { allocateAttribute, equipItem, getCurrentUserId, getState, isAuthenticated, learnSkill, logout, postAction, unequipItem, useConsumable as consumeItem } from './api';
import './App.css';

const INTRO_ART = String.raw`
███████╗██╗   ██╗██████╗ ██╗   ██╗██╗██╗   ██╗ █████╗ ███╗   ██╗████████╗
██╔════╝██║   ██║██╔══██╗██║   ██║██║██║   ██║██╔══██╗████╗  ██║╚══██╔══╝
███████╗██║   ██║██████╔╝██║   ██║██║██║   ██║███████║██╔██╗ ██║   ██║
╚════██║██║   ██║██╔══██╗╚██╗ ██╔╝██║╚██╗ ██╔╝██╔══██║██║╚██╗██║   ██║
███████║╚██████╔╝██║  ██║ ╚████╔╝ ██║ ╚████╔╝ ██║  ██║██║ ╚████║   ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝`;

export default function App() {
  const [gameState, setGameState] = useState(null);
  const [started, setStarted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [authed, setAuthed] = useState(isAuthenticated());
  const [playerId, setPlayerId] = useState(getCurrentUserId());
  const [inventoryOpen, setInventoryOpen] = useState(false);
  const [mapOpen, setMapOpen] = useState(false);
  const [skillsOpen, setSkillsOpen] = useState(false);
  const [reducedEffects, setReducedEffects] = useState(() => {
    if (typeof globalThis === 'undefined' || !globalThis.localStorage) return false;
    const stored = globalThis.localStorage.getItem('reducedEffects');
    if (stored !== null && stored !== undefined) return stored === 'true';
    return globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;
  });
  const { lines, streaming, send, addLine, clear } = useSSEChat();

  useEffect(() => {
    if (typeof document !== 'undefined') {
      document.body.classList.toggle('reduced-effects', reducedEffects);
    }
    globalThis.localStorage?.setItem('reducedEffects', String(reducedEffects));
  }, [reducedEffects]);

  const refreshState = useCallback(async () => {
    const state = await getState();
    setGameState(state);
    return state;
  }, []);

  useEffect(() => {
    if (!authed) {
      setLoading(false);
      return;
    }
    refreshState()
      .catch((error) => addLine(`ERREUR BACKEND: ${error.message}`, 'danger'))
      .finally(() => setLoading(false));
  }, [authed, refreshState, addLine]);

  const handleAuthenticated = useCallback((user) => {
    setPlayerId(user?.id || getCurrentUserId());
    setAuthed(true);
    setLoading(true);
  }, []);

  const handleLogout = useCallback(() => {
    logout();
    setAuthed(false);
    setStarted(false);
    setGameState(null);
    clear();
  }, [clear]);

  const applyAction = useCallback(async (label, action) => {
    try {
      const result = await action();
      if (result.state) setGameState(result.state);
      return result;
    } catch (error) {
      addLine(`${label}: ${error.message}`, 'danger');
      throw error;
    }
  }, [addLine]);

  const handleStart = async () => {
    await refreshState();
    setStarted(true);
    clear();
    addLine(`CONNEXION AU RÉSEAU OBSCURANT... UTILISATEUR ${(playerId || 'joueur').toUpperCase()}`, 'system');
    send('/start', {}, (state) => setGameState(state));
  };

  const handleSend = (text) => {
    addLine(text, 'player');
    send('/chat', { message: text }, (state) => setGameState(state));
  };

  const handleRoll = async () => {
    const result = await applyAction('JET 2D6', () => postAction('/roll'));
    addLine(result.formatted || `Jet: ${result.total}`, 'loot');
  };

  const handleLoot = async () => {
    const threat = String(gameState?.current_zone?.threat_level || 'standard');
    const result = await applyAction('FOUILLE', () => postAction('/loot', { command: 'loot', args: [threat] }));
    if (!result.items?.length) {
      addLine('Fouille terminée: rien d’exploitable.', 'system');
      return;
    }
    addLine(`Butin récupéré: ${result.items.map(i => i.name).join(', ')}`, 'loot');
  };

  const handleStartCombat = async () => {
    const result = await applyAction('RENCONTRE', () => postAction('/combat/start', { faction: 'tyranide', level: 'standard' }));
    addLine(result.message, 'danger');
  };

  const handleCombatAction = async (command) => {
    const result = await applyAction('COMBAT', () => postAction('/combat/action', { command, args: [] }));
    for (const entry of result.log || []) addLine(entry, command === 'defend' ? 'system' : 'danger');
    if (result.ended) addLine(result.victory ? 'Combat terminé: victoire.' : 'Combat terminé: repli.', result.victory ? 'loot' : 'system');
  };

  const handleTravel = async (zoneId) => {
    const result = await applyAction('DÉPLACEMENT', () => postAction('/travel', { zone_id: zoneId }));
    addLine(result.message, 'system');
    if (result.event) addLine(`Incident de route: ${result.event}`, 'danger');
  };

  const handleSave = async () => {
    const result = await applyAction('SAUVEGARDE', () => postAction('/save'));
    addLine(result.message || 'Sauvegarde effectuée.', 'system');
    await refreshState();
  };

  const handleReset = async () => {
    await applyAction('RESET', () => postAction('/reset'));
    const state = await refreshState();
    setGameState(state);
    setStarted(false);
    clear();
  };

  const handleEquip = async (itemId, slot = 'main') => {
    const result = await applyAction('ÉQUIPEMENT', () => equipItem(itemId, slot));
    addLine(result.message || 'Objet équipé.', 'system');
  };

  const handleUnequip = async (slot) => {
    const result = await applyAction('ÉQUIPEMENT', () => unequipItem(slot));
    addLine(result.message || 'Objet retiré.', 'system');
  };

  const handleAllocateAttribute = async (attribute, points = 1) => {
    const result = await applyAction('ATTRIBUT', () => allocateAttribute(attribute, points));
    addLine(result.message || `${attribute} amélioré.`, 'loot');
  };

  const handleUseConsumable = async (itemId) => {
    const result = await applyAction('CONSOMMABLE', () => consumeItem(itemId));
    addLine(result.message || 'Consommable utilisé.', 'system');
  };

  const handleLearnSkill = async (skillId) => {
    const result = await applyAction('SKILL', () => learnSkill(skillId));
    addLine(result.message || 'Compétence apprise.', 'loot');
  };

  const combat = gameState?.combat;
  const disabled = loading || streaming;

  return (
    <div className="app-shell">
      <header className="app-header">
        <span className="header-logo">⚙ HIVE-NODE//SECTEUR-7</span>
        <span className="header-status" aria-live="polite">
          {loading ? '◌ SYNCHRONISATION...' : streaming ? '● TRANSMISSION VOX...' : '○ SYSTÈME OPÉRATIONNEL'}
          <button
            className="effects-btn"
            onClick={() => setReducedEffects((v) => !v)}
            aria-pressed={reducedEffects}
            aria-label={reducedEffects ? 'Réactiver les effets visuels' : 'Réduire les effets visuels pour un meilleur confort de lecture'}
            title="Accessibilité : réduire les effets visuels"
          >
            {reducedEffects ? '◍ EFFETS RÉDUITS' : '◉ EFFETS COMPLETS'}
          </button>
          {authed && (
            <button
              className="effects-btn"
              onClick={() => setInventoryOpen((v) => !v)}
              aria-pressed={inventoryOpen}
              aria-label="Ouvrir ou fermer le sac à dos"
              title="Sac à dos"
            >
              🎒 SAC
            </button>
          )}
          {authed && (
            <button className="effects-btn" onClick={() => setMapOpen(true)} aria-label="Ouvrir la carte explorateur" title="Carte explorateur">
              🗺 CARTE
            </button>
          )}
          {authed && (
            <button className="effects-btn" onClick={() => setSkillsOpen(true)} aria-label="Ouvrir le panneau skills" title="Skills">
              🧠 SKILLS
            </button>
          )}
          {authed && (
            <button className="logout-btn" onClick={handleLogout} aria-label="Se déconnecter">
              ⏻ DÉCONNEXION
            </button>
          )}
        </span>
      </header>

      {!authed ? (
        <div className="app-body auth-body">
          <main className="main-pane">
            <AuthPanel onAuthenticated={handleAuthenticated} />
          </main>
        </div>
      ) : (
      <div className="app-body">
        <aside className="sidebar-left">
          <CharacterPanel state={gameState} onAllocateAttribute={handleAllocateAttribute} />
          <MapPanel state={gameState} />
          <QuestPanel state={gameState} />
        </aside>

        <main className="main-pane">
          {!started ? (
            <div className="start-screen">
              <pre className="skull-art">{INTRO_ART}</pre>
              <p className="start-subtitle">RUCHES DE KHARAD-RHO · INVASION TYRANIDE · SURVIE SOLO</p>
              <p className="start-user">Opérateur authentifié : <strong>{(playerId || 'joueur').toUpperCase()}</strong></p>
              <button className="start-btn" onClick={handleStart} disabled={disabled} aria-label="Initialiser la connexion et démarrer la partie">
                [ INITIALISER LA CONNEXION ]
              </button>
              <p className="start-hint">Mode MJ local activé si aucune clé OpenAI n’est configurée.</p>
            </div>
          ) : (
            <>
              <Terminal lines={lines} streaming={streaming} />
              <ActionPanel
                state={gameState}
                onRoll={handleRoll}
                onLoot={handleLoot}
                onStartCombat={handleStartCombat}
                onTravel={handleTravel}
                onSave={handleSave}
                onReset={handleReset}
                disabled={disabled}
              />
              <InputBar onSend={handleSend} disabled={disabled} />
            </>
          )}
        </main>

        <aside className="sidebar-right">
          <CombatPanel combat={combat} onCombatAction={handleCombatAction} disabled={disabled} />
          {!inventoryOpen && <InventoryPanel state={gameState} onEquip={handleEquip} onUnequip={handleUnequip} onUseConsumable={handleUseConsumable} />}
        </aside>

        {inventoryOpen && (
          <div className="inventory-modal" role="dialog" aria-label="Sac à dos">
            <div className="inventory-modal-inner">
              <button className="inventory-close" onClick={() => setInventoryOpen(false)} aria-label="Fermer le sac à dos">✕</button>
              <InventoryPanel state={gameState} onEquip={handleEquip} onUnequip={handleUnequip} onUseConsumable={handleUseConsumable} />
            </div>
          </div>
        )}

        {mapOpen && (
          <MapExplorerPage
            state={gameState}
            onTravel={handleTravel}
            onClose={() => setMapOpen(false)}
            disabled={disabled || combat?.active}
          />
        )}

        {skillsOpen && (
          <SkillsPanel
            state={gameState}
            onLearnSkill={handleLearnSkill}
            onClose={() => setSkillsOpen(false)}
          />
        )}
      </div>
      )}
    </div>
  );
}
