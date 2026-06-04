import { expect, test } from '@playwright/test';

test('parcours joueur principal: démarrage, jet de dés et rencontre', async ({ page }) => {
  const playerId = `e2e-${Date.now()}`;

  await page.goto('/');

  await expect(page.getByText('RUCHES DE KHARAD-RHO')).toBeVisible();
  await page.getByLabel('Identifiant du joueur pour la sauvegarde multi-utilisateur').fill(playerId);
  await page.getByLabel('Initialiser la connexion et démarrer la partie').click();

  await expect(page.getByText(`UTILISATEUR ${playerId.toUpperCase()}`)).toBeVisible();
  await expect(page.getByLabel('Lancer deux dés à six faces')).toBeEnabled({ timeout: 30_000 });

  await page.getByLabel('Lancer deux dés à six faces').click();
  await expect(page.getByText(/2d6 -> \d+ \+ \d+ = \d+/i)).toBeVisible();

  await page.getByLabel('Déclencher une rencontre hostile').click();
  await expect(page.getByText(/COMBAT · TOUR/)).toBeVisible();
});
