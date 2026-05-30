import { test, expect } from '@playwright/test';
import * as path from 'path';

const HTML_PATH = 'file://' + path.resolve(__dirname, '../prompt-generator.html');

test('client-website template generates correct prompt with all wiring rules', async ({ page, context }) => {
  // Grant clipboard permissions
  await context.grantPermissions(['clipboard-read', 'clipboard-write']);

  // 1. Open the generator
  await page.goto(HTML_PATH);

  // 2. Select the "Client Website" template (first one)
  await page.locator('.tpl').first().click();

  // 3. Fill fields that trigger auto-tools
  await page.locator('[data-k="github_refs"]').fill('github.com/acme/old-site');
  await page.locator('[data-k="documents"]').fill('./brief.pdf\n./brand-guide.pptx');
  await page.locator('[data-k="inspiration_urls"]').fill('https://bluebottlecoffee.com\nhttps://trade.coffee');

  // 4. Check "complex repo" to auto-enable graphify
  await page.locator('#complexRepo').check();

  // 5. Enable additional SEO skills
  await page.locator('[data-s="ai-seo"]').click();
  await page.locator('[data-s="seo-audit"]').click();
  await page.locator('[data-s="schema"]').click();

  // 6. Click Copy
  await page.locator('#copy').click();

  // 7. Read clipboard and assert contents
  const copiedText: string = await page.evaluate(async () => {
    return await navigator.clipboard.readText();
  });

  // Ingestion tools
  expect(copiedText).toContain('codefetch --url');
  expect(copiedText).toContain('graphify');
  expect(copiedText).toContain('markitdown');
  expect(copiedText).toContain('designlang');

  // Taste guardrail
  expect(copiedText).toContain('impeccable');

  // SEO skills
  expect(copiedText).toContain('ai-seo');
  expect(copiedText).toContain('seo-audit');
  expect(copiedText).toContain('schema');

  // Testing
  expect(copiedText).toContain('Playwright');

  // Hard stop enforcement
  expect(copiedText).toContain('STOP. Do not proceed to Phase 2');

  // Graceful degradation
  expect(copiedText).toContain('If a skill/CLI is missing, log it and continue');

  // Constraints
  expect(copiedText).toContain('One primary taste guardrail only');
});

test('conflict warning appears when two primary taste guardrails are selected', async ({ page }) => {
  await page.goto(HTML_PATH);

  // Select client-website (defaults to impeccable)
  await page.locator('.tpl').first().click();

  // Try to select taste-skill as a skill chip (should trigger conflict)
  await page.locator('[data-s="taste-skill"]').click();

  // Conflict warning should be visible
  const warnBox = page.locator('#conflictWarn');
  await expect(warnBox).toHaveClass(/show/);
  await expect(warnBox).toContainText('Conflict');
});

test('token estimate changes color at high character counts', async ({ page }) => {
  await page.goto(HTML_PATH);

  // Fill a very long brief to push char count high
  const longBrief = 'A '.repeat(3000);
  await page.locator('[data-k="brief"]').fill(longBrief);

  const stat = page.locator('#stat');
  // Should show warning or danger class if >8000 chars
  const classAttr = await stat.getAttribute('class');
  expect(classAttr).toMatch(/warn|danger/);
});
