/**
 * Capture des copies d'ecran de la pile de supervision pour le dossier Bloc 4.
 *
 * Prerequis : backend sur 127.0.0.1:8000 et Prometheus sur 127.0.0.1:9090,
 * charge avec monitoring/alert_rules.yml.
 *
 * Usage : node scripts/capture_supervision.mjs   (depuis frontend/)
 */
import { chromium } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const RACINE = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const SORTIE = join(RACINE, 'docs', 'bloc4', 'latex', 'figures');
const PROM = process.env.PROM_URL || 'http://127.0.0.1:9090';

let n = 0;

async function capturer(page, nom, description) {
  await page.screenshot({ path: join(SORTIE, `${nom}.png`) });
  n += 1;
  console.log(`  [OK] ${nom}.png  -  ${description}`);
}

async function main() {
  await mkdir(SORTIE, { recursive: true });
  const navigateur = await chromium.launch();
  const ctx = await navigateur.newContext({
    viewport: { width: 1440, height: 880 },
    deviceScaleFactor: 2,
  });
  const page = await ctx.newPage();

  try {
    // --- Alertes : l'ecran le plus parlant, une regle est en etat firing ----
    await page.goto(`${PROM}/alerts`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2500);
    // Deplie les groupes pour rendre les regles visibles.
    for (const bouton of await page.locator('button:has-text("Expand all")').all()) {
      await bouton.click().catch(() => {});
    }
    await page.waitForTimeout(1500);
    await capturer(page, '11_alertes', "Regles d'alerte evaluees par Prometheus");

    // --- Cibles de collecte -------------------------------------------------
    await page.goto(`${PROM}/targets`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2500);
    await capturer(page, '12_cibles', 'Cibles de collecte et etat de sante');

    // --- Graphe de la sonde structurante -----------------------------------
    const requete = encodeURIComponent('rpg40k_gm_generations_total');
    await page.goto(
      `${PROM}/graph?g0.expr=${requete}&g0.tab=0&g0.range_input=15m`,
      { waitUntil: 'domcontentloaded', timeout: 30000 },
    );
    await page.waitForTimeout(4000);
    await capturer(page, '13_graphe', 'Mode de production de la narration dans le temps');
    // --- Tableau de bord Grafana -------------------------------------------
    // Provisionne automatiquement depuis monitoring/grafana/ : la source de
    // donnees et le tableau de bord ne sont pas crees a la main.
    const GRAFANA = process.env.GRAFANA_URL || 'http://127.0.0.1:3000';
    try {
      const gf = await navigateur.newContext({
        viewport: { width: 1500, height: 900 },
        deviceScaleFactor: 2,
      });
      const pageGf = await gf.newPage();
      await pageGf.goto(
        `${GRAFANA}/d/rpg40k-overview?orgId=1&from=now-30m&to=now&kiosk`,
        { waitUntil: 'domcontentloaded', timeout: 40000 },
      );
      // Les panneaux se peignent apres reception des series : laisser le temps.
      await pageGf.waitForTimeout(9000);
      await capturer(pageGf, '14_grafana', "Tableau de bord d'exploitation Grafana");

      // Tableau de bord infrastructure : CPU, RAM, reseau, joueurs, latence,
      // erreurs, uptime, requetes/s.
      const pageInfra = await gf.newPage();
      await pageInfra.goto(
        `${GRAFANA}/d/rpg40k-infra?orgId=1&from=now-30m&to=now&kiosk`,
        { waitUntil: 'domcontentloaded', timeout: 40000 },
      );
      await pageInfra.waitForTimeout(9000);
      await capturer(pageInfra, '15_infrastructure', 'Tableau de bord infrastructure et jeu');
    } catch (err) {
      console.log(`  [IGNORE] Grafana : ${String(err.message).slice(0, 90)}`);
    }

  } finally {
    await navigateur.close();
  }

  console.log(`\n${n} capture(s) enregistree(s) dans ${SORTIE}`);
}

main().catch((err) => {
  console.error('Echec de la capture :', err.message);
  process.exit(1);
});
