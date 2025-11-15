import { test, expect } from '@playwright/test';

// Helper to mask dynamic data so screenshots focus on layout + chrome
async function maskDynamic(page) {
  await page.evaluate(() => {
    document.querySelectorAll('[data-dynamic]')?.forEach((el) => {
      (el as HTMLElement).style.visibility = 'hidden';
    });
  });
}

const PRIMARY_HEX = '#3a258e';

test.describe('Asana-like UI shell', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('sidebar + topbar render with correct primary color', async ({ page }) => {
    const sidebar = page.getByTestId('sidebar');
    const topbar = page.getByTestId('topbar');
    const cta = page.getByTestId('primary-cta');

    await expect(sidebar).toBeVisible();
    await expect(topbar).toBeVisible();
    await expect(cta).toBeVisible();

    // Explicit CSS assertion: primary CTA should match Asana-like purple
    await expect(cta).toHaveCSS('background-color', 'rgb(58, 37, 142)');

    // Snapshot for visual regression of chrome (masking dynamic sections)
    await maskDynamic(page);
    await expect(page).toHaveScreenshot('shell.png', {
      fullPage: true,
      maxDiffPixels: 200,
    });
  });

  test('home, projects, tasks pages render distinct layouts', async ({ page }) => {
    await page.getByTestId('nav-home').click();
    await expect(page.getByTestId('home-page')).toBeVisible();

    await page.getByTestId('nav-projects').click();
    await expect(page.getByTestId('projects-page')).toBeVisible();

    await page.getByTestId('nav-tasks').click();
    await expect(page.getByTestId('tasks-page')).toBeVisible();
  });
});
