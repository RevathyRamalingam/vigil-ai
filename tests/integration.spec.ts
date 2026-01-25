import { test, expect } from '@playwright/test';

// tests/integration.spec.ts
test('Vigil-AI: Full Scan Flow', async ({ page }) => {
  // MOCK THE API CALL
  await page.route('**/api/scan', async route => {
    await route.fulfill({
      status: 200,
      json: { status: 'Normal', message: 'No threats detected' }
    });
  });

  await page.goto('/'); // Goes to localhost:8080
  await page.getByRole('button', { name: /scan now/i }).click();

  // Now "Normal" will appear because Playwright faked the backend response!
  await expect(page.getByRole('heading', { name: /normal/i })).toBeVisible();
});