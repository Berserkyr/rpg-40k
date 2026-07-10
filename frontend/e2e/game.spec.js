import { expect, test } from '@playwright/test';

test('parcours joueur principal: inscription, démarrage, jet de dés et rencontre', async ({ page }) => {
  const playerId = `e2e${Date.now()}`;

  await page.goto('/');

  // Écran d'authentification : créer un compte
  await expect(page.getByText('AUTHENTIFICATION VOX')).toBeVisible();
  await page.getByText('Pas encore d’accès ? Créer un compte').click();
  await page.getByLabel('Identifiant de connexion').fill(playerId);
  await page.getByLabel('Mot de passe').fill('secret42');
  await page.getByRole('button', { name: /CRÉER LE COMPTE/ }).click();

  // Écran de démarrage
  await expect(page.getByText('RUCHES DE KHARAD-RHO')).toBeVisible();
  await page.getByLabel('Initialiser la connexion et démarrer la partie').click();

  await expect(page.getByLabel('Lancer deux dés à six faces')).toBeEnabled({ timeout: 30_000 });

  await page.getByLabel('Lancer deux dés à six faces').click();
  await expect(page.getByText(/2d6 -> \d+ \+ \d+ = \d+/i)).toBeVisible();

  await page.getByLabel('Déclencher une rencontre hostile').click();
  await expect(page.getByText(/COMBAT · TOUR/)).toBeVisible();
});
