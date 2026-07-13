import { useEffect, useMemo, useRef } from 'react';

/**
 * Sprite pixel art procedural et ANIME d'un ennemi (aucun asset externe).
 *
 * Pipeline "pixel art + vectorisation" :
 *  1. Un bitmap pixel est genere une seule fois dans un canvas hors-ecran,
 *     de maniere deterministe (faction + archetype + nom).
 *  2. Une boucle requestAnimationFrame redessine ce bitmap sur le canvas
 *     visible en appliquant des transformations VECTORIELLES (translation,
 *     rotation, echelle) pour des animations de combat fluides :
 *       - idle  : respiration / balancement continu
 *       - attack: bond vers la cible puis retour
 *       - hurt  : tremblement + flash rouge
 *       - death : bascule + fondu
 */

// ---- PRNG deterministe (mulberry32) ----
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

// ---- Palettes par faction (corps, contour, accent/yeux) ----
const PALETTES = {
  tyranide: { body: '#6a1b3a', edge: '#3a0d20', accent: '#ff4d4d' },
  culte_genestealer: { body: '#1b4a6a', edge: '#0d2a3a', accent: '#4dff9e' },
  culte: { body: '#1b4a6a', edge: '#0d2a3a', accent: '#4dff9e' },
  chaos: { body: '#4a1030', edge: '#200814', accent: '#ff2a2a' },
  mechanicus: { body: '#5a3210', edge: '#2a1808', accent: '#ff9d2a' },
  arbites: { body: '#20242c', edge: '#0c0e12', accent: '#3aa0ff' },
  ecclesiarchie: { body: '#4a4230', edge: '#242014', accent: '#ffe08a' },
  garde_imperiale: { body: '#2c3a24', edge: '#141c10', accent: '#a8ff6a' },
  civil: { body: '#3a3630', edge: '#1a1814', accent: '#c0c0c0' },
};

// ---- Profils de silhouette par archetype ----
// widths = demi-largeur (en cellules) pour chaque ligne, du haut vers le bas.
const PROFILES = {
  humanoid: {
    grid: 11, widths: [1, 2, 1, 4, 3, 3, 3, 3, 3, 3, 3],
    eyeRow: 1, legsFrom: 8, density: 0.9,
  },
  beast: {
    grid: 11, widths: [0, 1, 1, 3, 5, 5, 5, 5, 4, 0, 0],
    eyeRow: 3, legsFrom: 7, density: 0.85, quadruped: true,
  },
  brute: {
    grid: 12, widths: [2, 3, 5, 6, 6, 6, 6, 6, 5, 5, 4, 4],
    eyeRow: 1, legsFrom: 9, density: 0.96,
  },
  swarm: {
    grid: 9, widths: [0, 0, 0, 1, 2, 3, 4, 4, 4],
    eyeRow: 5, legsFrom: 99, density: 0.7, blobs: true,
  },
  psyker: {
    grid: 11, widths: [1, 2, 1, 2, 2, 3, 3, 4, 4, 5, 5],
    eyeRow: 1, legsFrom: 99, density: 0.85, aura: true,
  },
  daemon: {
    grid: 12, widths: [1, 2, 2, 5, 4, 4, 4, 4, 4, 3, 3, 3],
    eyeRow: 2, legsFrom: 9, density: 0.9, spikes: true, horns: true,
  },
  machine: {
    grid: 11, widths: [2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3],
    eyeRow: 3, legsFrom: 9, density: 0.98, lights: true, boxy: true,
  },
};

// Genere la grille de cellules (0 vide, 1 corps, 2 accent) symetrique gauche/droite.
function buildCells(profile, rng) {
  const { grid } = profile;
  const half = Math.ceil(grid / 2);
  const center = Math.floor(grid / 2);
  const cells = Array.from({ length: grid }, () => Array(grid).fill(0));

  for (let y = 0; y < grid; y += 1) {
    const w = Math.min(half, profile.widths[y] ?? 0);
    for (let x = 0; x <= w; x += 1) {
      const onEdge = x >= w - 1;
      const on = onEdge || rng() < profile.density;
      if (!on) continue;
      cells[y][center - x] = 1;
      cells[y][center + x] = 1;
    }
  }

  // Jambes bipedes : evide la colonne centrale en bas.
  if (profile.legsFrom < grid && !profile.quadruped && !profile.boxy) {
    for (let y = profile.legsFrom; y < grid; y += 1) cells[y][center] = 0;
  }
  // Quadrupede : pattes espacees.
  if (profile.quadruped) {
    const y = grid - 2;
    for (let x = 0; x < grid; x += 1) if (cells[y][x] && x % 2 === 1) cells[y][x] = 0;
  }
  // Nuee : plusieurs petits amas.
  if (profile.blobs) {
    for (let x = 0; x < grid; x += 1) {
      for (let y = 0; y < grid; y += 1) if (cells[y][x] && rng() < 0.35) cells[y][x] = 0;
    }
  }

  // Yeux / accent central.
  cells[profile.eyeRow][center - 1] = 2;
  cells[profile.eyeRow][center + 1] = 2;

  if (profile.horns) { cells[0][center - 2] = 2; cells[0][center + 2] = 2; }
  if (profile.spikes) { cells[3][0] = 2; cells[3][grid - 1] = 2; }
  if (profile.lights) { cells[5][center] = 2; cells[7][center - 1] = 2; cells[7][center + 1] = 2; }
  if (profile.aura) {
    cells[4][Math.max(0, center - 3)] = 2;
    cells[6][Math.min(grid - 1, center + 3)] = 2;
  }

  return cells;
}

// Rend le bitmap pixel dans un canvas hors-ecran (1 px = 1 cellule).
function renderBitmap(cells, palette) {
  const grid = cells.length;
  const off = document.createElement('canvas');
  off.width = grid;
  off.height = grid;
  const ctx = off.getContext('2d');
  if (!ctx) return off;
  for (let y = 0; y < grid; y += 1) {
    for (let x = 0; x < grid; x += 1) {
      const v = cells[y][x];
      if (!v) continue;
      const edge = !cells[y - 1]?.[x] || !cells[y + 1]?.[x] || !cells[y][x - 1] || !cells[y][x + 1];
      ctx.fillStyle = v === 2 ? palette.accent : (edge ? palette.edge : palette.body);
      ctx.fillRect(x, y, 1, 1);
    }
  }
  return off;
}

export default function EnemySprite({
  faction = 'tyranide',
  archetype = 'beast',
  threat = 'standard',
  name = '',
  size = 46,
  dead = false,
  action = 'idle',
  actionSeq = 0,
  facing = 'left',
}) {
  const canvasRef = useRef(null);
  const rafRef = useRef(0);
  const oneShotRef = useRef(null);
  const seedPhase = useMemo(() => (hashString(name || archetype) % 1000) / 1000, [name, archetype]);

  // Bitmap genere une seule fois par identite visuelle.
  const bitmap = useMemo(() => {
    const profile = PROFILES[archetype] || PROFILES.beast;
    const palette = PALETTES[faction] || PALETTES.tyranide;
    const rng = mulberry32(hashString(`${faction}|${archetype}|${threat}|${name}`));
    return renderBitmap(buildCells(profile, rng), palette);
  }, [faction, archetype, threat, name]);

  // Declenche une animation ponctuelle quand action/actionSeq change.
  useEffect(() => {
    if (action && action !== 'idle') {
      const durations = { attack: 360, hurt: 420, death: 650 };
      oneShotRef.current = {
        type: action,
        start: performance.now(),
        duration: durations[action] || 360,
      };
    }
  }, [action, actionSeq]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return undefined;
    const ctx = canvas.getContext('2d');
    if (!ctx) return undefined;
    const facingSign = facing === 'left' ? -1 : 1;
    const dpr = Math.min(2, globalThis.devicePixelRatio || 1);
    canvas.width = size * dpr;
    canvas.height = size * dpr;

    let mounted = true;
    const reduced = typeof document !== 'undefined'
      && document.body?.classList.contains('reduced-effects');

    const frame = (now) => {
      if (!mounted) return;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, size, size);
      ctx.imageSmoothingEnabled = false;

      const t = now / 1000;
      let dx = 0;
      let dy = reduced ? 0 : Math.sin((t + seedPhase * 6.28) * 2) * size * 0.02;
      let rot = 0;
      let scale = reduced ? 1 : 1 + Math.sin((t + seedPhase * 6.28) * 2) * 0.015;
      let flash = 0;
      let alpha = 1;

      const os = oneShotRef.current;
      if (os) {
        const p = Math.min(1, (now - os.start) / os.duration);
        if (os.type === 'attack') {
          dx += facingSign * Math.sin(p * Math.PI) * size * 0.28;
          scale += Math.sin(p * Math.PI) * 0.08;
        } else if (os.type === 'hurt') {
          dx += Math.sin(p * 42) * (1 - p) * size * 0.14;
          flash = (1 - p) * 0.7;
        } else if (os.type === 'death') {
          rot = facingSign * p * 0.5;
          dy += p * size * 0.28;
          alpha = 1 - p * 0.65;
        }
        if (p >= 1 && os.type !== 'death') oneShotRef.current = null;
      }

      const dyingDone = os?.type === 'death' && (now - os.start) / os.duration >= 1;
      if ((dead || dyingDone) && os?.type !== 'death') {
        rot = facingSign * 0.5;
        dy = size * 0.28;
        alpha = 0.35;
      }

      const g = bitmap.width;
      const draw = (size / g) * 0.92;
      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.translate(size / 2 + dx, size / 2 + dy);
      ctx.rotate(rot);
      ctx.scale(scale * (facingSign < 0 ? -1 : 1), scale);
      ctx.drawImage(bitmap, (-g * draw) / 2, (-g * draw) / 2, g * draw, g * draw);
      if (flash > 0) {
        ctx.globalCompositeOperation = 'source-atop';
        ctx.globalAlpha = flash;
        ctx.fillStyle = '#ff5050';
        ctx.fillRect((-g * draw) / 2, (-g * draw) / 2, g * draw, g * draw);
      }
      ctx.restore();

      rafRef.current = requestAnimationFrame(frame);
    };

    rafRef.current = requestAnimationFrame(frame);
    return () => {
      mounted = false;
      cancelAnimationFrame(rafRef.current);
    };
  }, [bitmap, size, dead, facing, seedPhase]);

  return (
    <canvas
      ref={canvasRef}
      className="enemy-sprite"
      style={{ imageRendering: 'pixelated', width: size, height: size }}
      aria-hidden="true"
    />
  );
}
