import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # --- Test 1: Main menu button functionality ---
        await page.goto("file:///app/index.html")

        # Wait for the initial content to be visible
        await expect(page.locator("#content-add-subtract")).to_be_visible()

        # Click the "Multiply/Divide" tab and verify its content appears.
        await page.click("#tab-multiply-divide")
        await expect(page.locator("#content-multiply-divide")).to_be_visible()

        # Click the "Timed Test" button and verify it navigates to the game page.
        await page.click("#start-test-multiply-divide")
        await expect(page.locator("#game-page")).to_be_visible()
        await expect(page.locator("#game-title")).to_have_text("Multiply/Divide Test")

        # --- Test 2: Reward menu back button ---
        # Manually show the reward menu page to test its back button.
        await page.evaluate("showPage('reward-menu-page')")
        await expect(page.locator("#reward-menu-page")).to_be_visible()

        # Click the "Back to Main Menu" button.
        await page.locator("#reward-menu-page footer button").click()

        # Verify it navigates back to the home page.
        await expect(page.locator("#home-page")).to_be_visible()

        # Final screenshot of the home page after testing.
        await page.screenshot(path="jules-scratch/verification/verification.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())