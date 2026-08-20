/**
 * Capture des copies d'ecran de l'application pour le dossier Bloc 4.
 *
 * Pilote un navigateur Chromium sans interface, parcourt les ecrans reels du
 * jeu et enregistre les images dans docs/bloc4/latex/figures/.
 *
 * Prerequis : backend sur 127.0.0.1:8000 et frontend sur localhost:5173.
 * Usage : node scripts/capture_screenshots.mjs  (depuis frontend/)
 */
import { chromium } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

// Le script vit dans frontend/scripts/ : la racine du depot est deux niveaux au-dessus.
const RACINE = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const SORTIE = join(RACINE, 'docs', 'bloc4', 'latex', 'figures');
const BASE = 'http://localhost:5173';

const captures = [];

async function capturer(page, nom, description) {
  const chemin = join(SORTIE, `${nom}.png`);
  await page.screenshot({ path: chemin });
  captures.push({ nom, description });
  console.log(`  [OK] ${nom}.png  -  ${description}`);
}

async function main() {
  await mkdir(SORTIE, { recursive: true });

  const navigateur = await chromium.launch();
  const contexte = await navigateur.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2, // rendu net a l'impression
  });
  const page = await contexte.newPage();

  try {
    // --- 1. Ecran d'authentification -------------------------------------
    await page.goto(BASE, { waitUntil: 'networkidle' });
    await page.waitForSelector('text=AUTHENTIFICATION VOX', { timeout: 15000 });
    await capturer(page, '01_authentification', "Ecran d'authentification (JWT)");

    // --- 2. Session demarree ---------------------------------------------
    await page.getByRole('button', { name: /LANCER LA DEMO|LANCER LA DÉMO/i }).click();
    await page.waitForSelector('text=/Operateur authentifie|Opérateur authentifié/i', { timeout: 15000 });
    await page.getByRole('button', { name: /Initialiser la connexion/i }).click();

    // La narration arrive en streaming SSE : on attend la fin du flux.
    await page.waitForSelector('text=/Karimus reprend conscience/i', { timeout: 45000 });
    await page.waitForTimeout(2500);
    await capturer(page, '02_partie_en_cours', 'Scene d ouverture diffusee en SSE');

    // --- 3. Combat tactique ----------------------------------------------
    await page.getByRole('button', { name: /Declencher une rencontre|Déclencher une rencontre/i }).click();
    await page.waitForSelector('text=/THEATRE D|THÉÂTRE D/i', { timeout: 20000 });
    await page.waitForTimeout(1500);
    await capturer(page, '03_combat_tactique', 'Arene de combat tactique');

    // --- 4 et 5. Reponses d'API ------------------------------------------
    // Ces pages ne contiennent que du texte : un cadre a la taille du contenu
    // evite une figure aux trois quarts blanche dans le rapport.
    const cadreApi = await navigateur.newContext({
      viewport: { width: 1180, height: 760 },
      deviceScaleFactor: 2,
    });

    const metriques = await cadreApi.newPage();
    await metriques.goto('http://127.0.0.1:8000/api/metrics', { waitUntil: 'domcontentloaded' });
    await metriques.waitForTimeout(500);
    await capturer(metriques, '04_metriques', 'Point de collecte Prometheus /api/metrics');

    const cadreSante = await navigateur.newContext({
      viewport: { width: 1180, height: 150 },
      deviceScaleFactor: 2,
    });
    const sante = await cadreSante.newPage();
    await sante.goto('http://127.0.0.1:8000/api/health/ready', { waitUntil: 'domcontentloaded' });
    await sante.waitForTimeout(300);
    await capturer(sante, '05_sonde_aptitude', "Sonde d'aptitude /api/health/ready");

    // --- 6bis. Ecrans de jeu complementaires -------------------------------
    // Le combat est deja capture ; on documente ici les panneaux lateraux qui
    // portent la progression et l'equipement.
    try {
      await page.getByRole('button', { name: /Ouvrir le panneau skills/i }).click();
      await page.waitForTimeout(1200);
      await capturer(page, '07_competences', 'Panneau de progression et arbre de competences');
      await page.keyboard.press('Escape');
      await page.waitForTimeout(600);
    } catch (err) {
      console.log(`  [IGNORE] panneau skills : ${String(err.message).slice(0, 80)}`);
    }

    try {
      await page.getByRole('button', { name: /Ouvrir la carte explorateur/i }).click();
      await page.waitForTimeout(1200);
      await capturer(page, '08_carte', 'Carte d exploration du secteur');
      await page.keyboard.press('Escape');
      await page.waitForTimeout(600);
    } catch (err) {
      console.log(`  [IGNORE] carte : ${String(err.message).slice(0, 80)}`);
    }

    // --- 6. Integration continue -----------------------------------------
    // Depot public : la page des executions de la CI constitue une preuve
    // directe pour C4.2.2. Echec tolere (reseau, mise en page GitHub).
    try {
      const ci = await navigateur.newContext({
        viewport: { width: 1400, height: 900 },
        deviceScaleFactor: 2,
      });
      const pageCi = await ci.newPage();
      await pageCi.goto('https://github.com/Berserkyr/rpg-40k/actions', {
        waitUntil: 'domcontentloaded',
        timeout: 30000,
      });
      await pageCi.waitForTimeout(4000);
      await capturer(pageCi, '06_ci_github', 'Executions de la CI GitHub Actions');

      // NOTE : /issues/new/choose exige une session authentifiee ; une capture
      // anonyme ne renvoie que la page de connexion GitHub. Les formulaires
      // sont donc documentes par leur source YAML, non par une copie d'ecran.

      // Pull requests ouvertes par Dependabot : preuve du fonctionnement de la
      // politique de mise a jour decrite au titre de C4.1.1.
      const pagePr = await ci.newPage();
      await pagePr.goto('https://github.com/Berserkyr/rpg-40k/pulls', {
        waitUntil: 'domcontentloaded', timeout: 30000,
      });
      await pagePr.waitForTimeout(3500);
      await capturer(pagePr, '10_dependabot', 'Pull requests ouvertes par Dependabot');
    } catch (err) {
      console.log(`  [IGNORE] capture GitHub indisponible : ${String(err.message).slice(0, 90)}`);
    }

  } finally {
    await navigateur.close();
  }

  console.log(`\n${captures.length} capture(s) enregistree(s) dans ${SORTIE}`);
}

main().catch((err) => {
  console.error('Echec de la capture :', err.message);
  process.exit(1);
});
