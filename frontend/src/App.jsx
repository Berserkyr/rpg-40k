import { useState, useEffect, useCallback } from 'react';
import Terminal from './components/Terminal';
import InputBar from './components/InputBar';
import CharacterPanel from './components/CharacterPanel';
import MapPanel from './components/MapPanel';
import QuestPanel from './components/QuestPanel';
import InventoryPanel from './components/InventoryPanel';
import CombatPanel from './components/CombatPanel';
import ActionPanel from './components/ActionPanel';
import { useSSEChat } from './hooks/useSSEChat';
import { getState, postAction } from './api';
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
  const { lines, streaming, send, addLine, clear } = useSSEChat();

  const refreshState = useCallback(async () => {
    const state = await getState();
    setGameState(state);
    return state;
  }, []);

  useEffect(() => {
    refreshState()
      .catch((error) => addLine(`ERREUR BACKEND: ${error.message}`, 'danger'))
      .finally(() => setLoading(false));
  }, [refreshState, addLine]);

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

  const handleStart = () => {
    setStarted(true);
    clear();
    addLine('CONNEXION AU RÉSEAU OBSCURANT... INITIALISÉE', 'system');
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

  const combat = gameState?.combat;
  const disabled = loading || streaming;

  return (
    <div className="app-shell">
      <header className="app-header">
        <span className="header-logo">⚙ HIVE-NODE//SECTEUR-7</span>
        <span className="header-status">
          {loading ? '◌ SYNCHRONISATION...' : streaming ? '● TRANSMISSION VOX...' : '○ SYSTÈME OPÉRATIONNEL'}
        </span>
      </header>

      <div className="app-body">
        <aside className="sidebar-left">
          <CharacterPanel state={gameState} />
          <MapPanel state={gameState} />
          <QuestPanel state={gameState} />
        </aside>

        <main className="main-pane">
          {!started ? (
            <div className="start-screen">
              <pre className="skull-art">{INTRO_ART}</pre>
              <p className="start-subtitle">RUCHES DE KHARAD-RHO · INVASION TYRANIDE · SURVIE SOLO</p>
              <button className="start-btn" onClick={handleStart} disabled={disabled}>
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
          <InventoryPanel state={gameState} />
        </aside>
      </div>
    </div>
  );
}
