import { test, expect } from '@playwright/test';

test('Vigil-AI: Full Scan Flow', async ({ page }) => {
  // 1. Navigate to your specific port
  await page.goto('http://localhost:8080');

  // 2. Locate the button
  const scanButton = page.getByRole('button', { name: /scan now/i });

  // 3. Click the button
  await scanButton.click();

  // 4. Verify Intermediate State: "Scanning"
  // This confirms your React state updated correctly upon click
  const scanningButton = page.getByText(/scanning/i);
  await expect(scanningButton).toBeVisible();

  // 5. Verify Final State: "normal"
  // We use a longer timeout here because the backend/AI processing 
  // happens during the "Scanning" phase.
  // Look specifically for the heading, not the button
  const statusHeading = page.getByRole('heading', { name: /normal/i });
  await expect(statusHeading).toBeVisible({ timeout: 15000 });
});