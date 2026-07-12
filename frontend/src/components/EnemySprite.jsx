import { useEffect, useRef } from 'react';

/**
 * Sprite pixel procedural d'un ennemi (aucun asset externe).
 *
 * Le sprite est genere de maniere deterministe a partir de la faction, du
 * niveau de menace et du nom : meme ennemi -> meme apparence. La creature est
 * dessinee symetriquement (miroir vertical) sur un petit canvas puis agrandie
 * avec un rendu "pixelated" pour un rendu retro/pixel-art.
 */

// PRNG deterministe (mulberry32) a partir d'une graine numerique.
function mulberry32(seed) {
  return function next() {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function hashString(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i += 1) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

// Palettes par faction (corps, contour, accent/yeux).
const PALETTES = {
  tyranide: { body: '#6a1b3a', edge: '#3a0d20', accent: '#ff4d4d', glow: '#ffb3b3' },
  culte_genestealer: { body: '#1b4a6a', edge: '#0d2a3a', accent: '#4dff9e', glow: '#b3ffd9' },
  culte: { body: '#1b4a6a', edge: '#0d2a3a', accent: '#4dff9e', glow: '#b3ffd9' },
};

// Densite/taille selon la menace.
const THREAT_DENSITY = {
  sbire: 0.42, minion: 0.42, standard: 0.5, elite: 0.58, boss: 0.66,
};

export default function EnemySprite({ faction = 'tyranide', threat = 'standard', name = '', size = 44, dead = false }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const GRID = 11;              // grille logique (impaire pour un axe central)
    const half = Math.ceil(GRID / 2);
    const palette = PALETTES[faction] || PALETTES.tyranide;
    const density = THREAT_DENSITY[threat] ?? 0.5;
    const rng = mulberry32(hashString(`${faction}|${threat}|${name}`));

    // Genere la moitie gauche puis miroir -> symetrie de creature.
    const cells = Array.from({ length: GRID }, () => Array(GRID).fill(0));
    for (let y = 0; y < GRID; y += 1) {
      for (let x = 0; x < half; x += 1) {
        // Bords verticaux moins denses (silhouette organique).
        const edgeFalloff = 1 - Math.abs(y - GRID / 2) / (GRID / 1.4);
        const on = rng() < density * (0.55 + edgeFalloff);
        const v = on ? 1 : 0;
        cells[y][x] = v;
        cells[y][GRID - 1 - x] = v;
      }
    }
    // Yeux/accent: ligne du haut au centre.
    const eyeRow = Math.floor(GRID * 0.32);
    cells[eyeRow][half - 2] = 2;
    cells[eyeRow][GRID - (half - 1)] = 2;

    const scale = size / GRID;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.imageSmoothingEnabled = false;

    for (let y = 0; y < GRID; y += 1) {
      for (let x = 0; x < GRID; x += 1) {
        const v = cells[y][x];
        if (!v) continue;
        let color = v === 2 ? palette.accent : palette.body;
        if (dead) color = v === 2 ? '#555' : '#2a2a2a';
        ctx.fillStyle = color;
        ctx.fillRect(Math.floor(x * scale), Math.floor(y * scale), Math.ceil(scale), Math.ceil(scale));
      }
    }
  }, [faction, threat, name, size, dead]);

  return (
    <canvas
      ref={canvasRef}
      width={size}
      height={size}
      className="enemy-sprite"
      style={{ imageRendering: 'pixelated', width: size, height: size }}
      aria-hidden="true"
    />
  );
}
